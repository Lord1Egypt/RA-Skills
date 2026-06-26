#!/usr/bin/env python3
import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from common.drugflow_api import DrugFlowAPIClient


TERMINAL_STATES = {"finished", "aborted", "stopped"}
ADMET_JOB_TYPE = "admet-dl"
FALLBACK_UNIT_PRICE = 10


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DrugFlow ADMET API flow with session auth.")
    parser.add_argument("--base-url", required=True, help="Example: https://new.drugflow.com")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)

    parser.add_argument("--ws-id", default=None)
    parser.add_argument("--ws-name", default="codex-admet-workspace")
    parser.add_argument("--account", default="person", choices=["person", "team"])

    parser.add_argument("--dataset-id", default=None, help="Use dataset + smiles_col as ADMET input.")
    parser.add_argument("--smiles-col", default="cs-smiles", help="Used with --dataset-id.")
    parser.add_argument("--smiles", action="append", default=[], help="Direct smiles input, can be repeated.")
    parser.add_argument("--smiles-file", default=None, help="Text/CSV/JSON smiles file for direct input.")

    parser.add_argument("--sme", action="store_true", help="Only for admet-dl: use SME mode.")
    parser.add_argument("--is-calc-vis", action="store_true", help="Only for admet-dl SME mode.")

    parser.add_argument("--job-name", default="codex-admet-demo")
    parser.add_argument("--expect-tokens", type=int, default=None)
    parser.add_argument("--avail-tokens", type=int, default=None)

    parser.add_argument("--no-poll", action="store_true")
    parser.add_argument("--poll-timeout", type=int, default=1800)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--result-page-size", type=int, default=20)
    return parser.parse_args()


def parse_smiles_file(path: str) -> List[str]:
    file_path = Path(path)
    if not file_path.is_file():
        raise RuntimeError(f"smiles file not found: {path}")

    if file_path.suffix.lower() == ".json":
        payload = json.loads(file_path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise RuntimeError("json smiles file must be an array")
        return [str(x).strip() for x in payload if str(x).strip()]

    smiles_list: List[str] = []
    for line in file_path.read_text(encoding="utf-8").splitlines():
        row = line.strip()
        if not row:
            continue
        head = row.split(",")[0].strip()
        if head.lower() == "smiles":
            continue
        smiles_list.append(head)
    return smiles_list


def resolve_smiles(args: argparse.Namespace) -> List[str]:
    smiles_list = [x.strip() for x in args.smiles if x.strip()]
    if args.smiles_file:
        smiles_list.extend(parse_smiles_file(args.smiles_file))
    return smiles_list


def get_dataset_count(client: DrugFlowAPIClient, dataset_id: str) -> int:
    payload = client.request_or_raise(
        "GET",
        f"/api/dataset/{dataset_id}/content",
        params={"page": 1, "page_size": 1},
    )
    count = payload.get("count")
    if not isinstance(count, int):
        raise RuntimeError(f"cannot infer dataset count for {dataset_id}: {payload}")
    return count


def estimate_task_type(sme: bool) -> str:
    return "admet_mga" if sme else "admet_mert"


def estimate_tokens(client: DrugFlowAPIClient, task_type: str, input_amount: int, account: str) -> int:
    payload = client.request_or_raise(
        "POST",
        "/api/token/estimate",
        json={
            "task_type": task_type,
            "input_amount": input_amount,
            "account_type": account,
            "docking_type": task_type,
            "karmadock_out_amount": 0,
            "extra_multiples": 1,
        },
    )
    except_token = payload.get("except_token")
    if not isinstance(except_token, int):
        raise RuntimeError(f"unexpected estimate payload: {payload}")
    return except_token


def build_admet_args(args: argparse.Namespace, input_mode: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"account": args.account}
    out["sme"] = bool(args.sme)
    if args.sme and args.is_calc_vis:
        out["is_calc_vis"] = True
    if input_mode == "dataset":
        out["dataset_id"] = args.dataset_id
        out["smiles_col"] = args.smiles_col
    return out


def create_admet_job(
    client: DrugFlowAPIClient,
    ws_id: str,
    args: argparse.Namespace,
    args_json: Dict[str, Any],
    expect_tokens: int,
    avail_tokens: int,
    smiles_list: Optional[List[str]] = None,
) -> Dict[str, Any]:
    data = {
        "name": args.job_name,
        "type": ADMET_JOB_TYPE,
        "args": json.dumps(args_json, ensure_ascii=False),
        "ws_id": ws_id,
        "expect_tokens": str(expect_tokens),
        "avail_tokens": str(avail_tokens),
    }
    if smiles_list is not None:
        data["smiles"] = json.dumps(smiles_list, ensure_ascii=False)
    return client.request_or_raise("POST", "/api/jobs", data=data)


def poll_job(client: DrugFlowAPIClient, ws_id: str, job_id: int, timeout_s: int, interval_s: int) -> Dict[str, Any]:
    start = time.time()
    while True:
        payload = client.request_or_raise(
            "GET",
            f"/api/jobs/{job_id}",
            params={"ws_id": ws_id},
        )
        state = payload.get("state")
        if state in TERMINAL_STATES:
            return payload
        if time.time() - start > timeout_s:
            raise TimeoutError(f"job {job_id} did not reach terminal state in {timeout_s}s; last_state={state}")
        time.sleep(interval_s)


def fetch_results(client: DrugFlowAPIClient, job_id: int, page_size: int) -> Dict[str, Any]:
    payload = client.request_or_raise(
        "GET",
        f"/api/jobs/{job_id}/results",
        params={"page": 1, "page_size": page_size},
    )
    if not isinstance(payload, dict):
        raise RuntimeError(f"unexpected results payload: {payload}")
    return payload


def main() -> None:
    args = parse_args()
    smiles_list = resolve_smiles(args)

    if args.dataset_id and smiles_list:
        raise RuntimeError("choose one input mode: dataset (--dataset-id) or direct smiles (--smiles/--smiles-file)")
    if not args.dataset_id and not smiles_list:
        raise RuntimeError("missing ADMET input: provide --dataset-id or at least one --smiles/--smiles-file")

    input_mode = "dataset" if args.dataset_id else "smiles"

    with requests.Session() as session:
        client = DrugFlowAPIClient(args.base_url, session=session)
        client.signin(args.email, args.password)
        ws_id = client.ensure_workspace(args.ws_id, args.ws_name)

        balance_tokens = client.get_balance(args.account)
        jobs_before = client.list_jobs(ws_id)

        if input_mode == "dataset":
            input_amount = get_dataset_count(client, args.dataset_id)
        else:
            input_amount = len(smiles_list)

        est_task_type = estimate_task_type(args.sme)
        expect_tokens = args.expect_tokens
        if expect_tokens is None:
            try:
                expect_tokens = estimate_tokens(client, est_task_type, input_amount, args.account)
            except Exception as exc:
                expect_tokens = FALLBACK_UNIT_PRICE * input_amount
                print(f"[warn] token estimate failed, fallback to unit-price estimate: {expect_tokens} ({exc})")

        avail_tokens = args.avail_tokens if args.avail_tokens is not None else balance_tokens
        admet_args = build_admet_args(args, input_mode=input_mode)
        created = create_admet_job(
            client=client,
            ws_id=ws_id,
            args=args,
            args_json=admet_args,
            expect_tokens=expect_tokens,
            avail_tokens=avail_tokens,
            smiles_list=(smiles_list if input_mode == "smiles" else None),
        )

        job_id = created.get("id")
        if not isinstance(job_id, int):
            raise RuntimeError(f"job create response missing id: {created}")

        if args.no_poll:
            output = {
                "ws_id": ws_id,
                "job_id": job_id,
                "job_state": created.get("state"),
                "task_type": ADMET_JOB_TYPE,
                "input_mode": input_mode,
                "input_amount": input_amount,
                "expect_tokens": expect_tokens,
                "avail_tokens": avail_tokens,
                "jobs_before_count": jobs_before.get("count"),
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return

        final_job = poll_job(
            client,
            ws_id=ws_id,
            job_id=job_id,
            timeout_s=args.poll_timeout,
            interval_s=args.poll_interval,
        )
        results = fetch_results(client, job_id=job_id, page_size=args.result_page_size)

        output = {
            "ws_id": ws_id,
            "job_id": job_id,
            "job_state": final_job.get("state"),
            "task_type": ADMET_JOB_TYPE,
            "input_mode": input_mode,
            "input_amount": input_amount,
            "expect_tokens": expect_tokens,
            "avail_tokens": avail_tokens,
            "jobs_before_count": jobs_before.get("count"),
            "result_count": results.get("count"),
            "results_preview": results.get("results", [])[:3],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
