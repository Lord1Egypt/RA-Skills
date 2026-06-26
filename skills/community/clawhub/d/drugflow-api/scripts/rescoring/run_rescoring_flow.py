#!/usr/bin/env python3
import argparse
import json
import mimetypes
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import requests

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from common.drugflow_api import DrugFlowAPIClient


TERMINAL_STATES = {"finished", "aborted", "stopped"}


def upload_dataset(client: DrugFlowAPIClient, ws_id: str, file_path: str) -> str:
    filename = Path(file_path).name
    data = {
        "ws_id": ws_id,
        "from_type": "raw",
        "source": json.dumps({"module": "datacenter"}, ensure_ascii=False),
        "name": filename,
    }
    with open(file_path, "rb") as fp:
        files = {"dataset": (filename, fp, mimetypes.guess_type(filename)[0] or "application/octet-stream")}
        payload = client.request_or_raise("POST", "/api/dataset/upload", data=data, files=files)

    dataset_id = payload.get("dataset_id")
    if not isinstance(dataset_id, str):
        raise RuntimeError(f"dataset upload response missing dataset_id: {payload}")
    return dataset_id


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


def estimate_tokens(client: DrugFlowAPIClient, input_amount: int, account: str) -> int:
    payload = client.request_or_raise(
        "POST",
        "/api/token/estimate",
        json={
            "task_type": "rescoring",
            "input_amount": input_amount,
            "account_type": account,
            "docking_type": "rescoring",
            "karmadock_out_amount": 0,
            "extra_multiples": 1,
        },
    )
    except_token = payload.get("except_token")
    if not isinstance(except_token, int):
        raise RuntimeError(f"unexpected estimate payload: {payload}")
    return except_token


def create_rescoring_job(
    client: DrugFlowAPIClient,
    ws_id: str,
    job_name: str,
    args_json: Dict[str, Any],
    pdb_dataset_id: str,
    ligands_dataset_id: str,
    smiles_col: str,
    expect_tokens: int,
    avail_tokens: int,
) -> Dict[str, Any]:
    data = {
        "name": job_name,
        "type": "rescoring",
        "args": json.dumps(args_json, ensure_ascii=False),
        "pdb": pdb_dataset_id,
        "ligands": ligands_dataset_id,
        "smiles_col": smiles_col,
        "ws_id": ws_id,
        "expect_tokens": str(expect_tokens),
        "avail_tokens": str(avail_tokens),
    }
    return client.request_or_raise("POST", "/api/jobs", data=data)


def poll_job(client: DrugFlowAPIClient, ws_id: str, job_id: int, timeout_s: int, interval_s: int) -> Dict[str, Any]:
    start = time.time()
    while True:
        payload = client.request_or_raise("GET", f"/api/jobs/{job_id}", params={"ws_id": ws_id})
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


def parse_rescoring_functions(values: List[str]) -> List[str]:
    out = [x.strip() for x in values if x.strip()]
    if not out:
        raise RuntimeError("rescoring functions cannot be empty")
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DrugFlow rescoring API flow with session auth.")
    parser.add_argument("--base-url", required=True, help="Example: https://new.drugflow.com")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)

    parser.add_argument("--ws-id", default=None)
    parser.add_argument("--ws-name", default="codex-rescoring-workspace")
    parser.add_argument("--account", default="person", choices=["person", "team"])

    parser.add_argument("--pdb-file", required=True, help="Input protein pdb file (*.pdb).")
    parser.add_argument("--ligands-file", required=True, help="Input ligand sdf file (*.sdf).")
    parser.add_argument("--smiles-col", default="cs-smiles")

    parser.add_argument("--mode", default="semi", choices=["semi"])
    parser.add_argument("--rescoring-functions", nargs="+", default=["RTMS"])

    parser.add_argument("--job-name", default="codex-rescoring-demo")
    parser.add_argument("--expect-tokens", type=int, default=None)
    parser.add_argument("--avail-tokens", type=int, default=None)

    parser.add_argument("--no-poll", action="store_true")
    parser.add_argument("--poll-timeout", type=int, default=1800)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--result-page-size", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rescoring_functions = parse_rescoring_functions(args.rescoring_functions)
    pdb_suffix = Path(args.pdb_file).suffix.lower()
    ligands_suffix = Path(args.ligands_file).suffix.lower()
    if pdb_suffix != ".pdb":
        raise RuntimeError(f"--pdb-file must be a .pdb file, got: {args.pdb_file}")
    if ligands_suffix != ".sdf":
        raise RuntimeError(f"--ligands-file must be a .sdf file, got: {args.ligands_file}")

    with requests.Session() as session:
        client = DrugFlowAPIClient(args.base_url, session=session, timeout=120)
        client.signin(args.email, args.password)

        ws_id = client.ensure_workspace(args.ws_id, args.ws_name)
        jobs_before = client.list_jobs(ws_id)

        pdb_dataset_id = upload_dataset(client, ws_id, args.pdb_file)
        ligands_dataset_id = upload_dataset(client, ws_id, args.ligands_file)

        ligands_count = get_dataset_count(client, ligands_dataset_id)
        balance_tokens = client.get_balance(args.account)

        expect_tokens = args.expect_tokens
        if expect_tokens is None:
            expect_tokens = estimate_tokens(client, input_amount=ligands_count, account=args.account)

        avail_tokens = args.avail_tokens if args.avail_tokens is not None else balance_tokens

        rescoring_args: Dict[str, Any] = {
            "mode": args.mode,
            "rescoring_functions": rescoring_functions,
            "account": args.account,
        }

        created = create_rescoring_job(
            client=client,
            ws_id=ws_id,
            job_name=args.job_name,
            args_json=rescoring_args,
            pdb_dataset_id=pdb_dataset_id,
            ligands_dataset_id=ligands_dataset_id,
            smiles_col=args.smiles_col,
            expect_tokens=expect_tokens,
            avail_tokens=avail_tokens,
        )

        job_id = created.get("id")
        if not isinstance(job_id, int):
            raise RuntimeError(f"job create response missing id: {created}")

        if args.no_poll:
            output = {
                "ws_id": ws_id,
                "job_id": job_id,
                "job_state": created.get("state"),
                "pdb_dataset_id": pdb_dataset_id,
                "ligands_dataset_id": ligands_dataset_id,
                "ligands_count": ligands_count,
                "smiles_col": args.smiles_col,
                "rescoring_functions": rescoring_functions,
                "expect_tokens": expect_tokens,
                "avail_tokens": avail_tokens,
                "jobs_before_count": jobs_before.get("count"),
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return

        final_job = poll_job(
            client=client,
            ws_id=ws_id,
            job_id=job_id,
            timeout_s=args.poll_timeout,
            interval_s=args.poll_interval,
        )
        results = fetch_results(client=client, job_id=job_id, page_size=args.result_page_size)

        output = {
            "ws_id": ws_id,
            "job_id": job_id,
            "job_state": final_job.get("state"),
            "pdb_dataset_id": pdb_dataset_id,
            "ligands_dataset_id": ligands_dataset_id,
            "ligands_count": ligands_count,
            "smiles_col": args.smiles_col,
            "rescoring_functions": rescoring_functions,
            "expect_tokens": expect_tokens,
            "avail_tokens": avail_tokens,
            "jobs_before_count": jobs_before.get("count"),
            "result_count": results.get("count"),
            "results_preview": results.get("results", [])[:3],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
