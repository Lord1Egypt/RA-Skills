#!/usr/bin/env python3
import argparse
import json
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


def parse_page_list(raw: str) -> List[int]:
    value = (raw or "").strip()
    if not value:
        raise RuntimeError("page list cannot be empty")

    if value.startswith("["):
        data = json.loads(value)
        if not isinstance(data, list):
            raise RuntimeError("page list JSON must be an array")
        pages = [int(x) for x in data]
    else:
        pages = [int(x.strip()) for x in value.split(",") if x.strip()]

    if not pages:
        raise RuntimeError("page list cannot be empty")
    for page in pages:
        if page <= 0:
            raise RuntimeError(f"invalid page number: {page} (must be > 0)")
    return pages


def get_dataset_meta(client: DrugFlowAPIClient, dataset_id: str) -> Dict[str, Any]:
    payload = client.request_or_raise("GET", f"/api/dataset/{dataset_id}/metainfo")
    if not isinstance(payload, dict):
        raise RuntimeError(f"unexpected dataset metainfo payload: {payload}")
    return payload


def estimate_tokens(client: DrugFlowAPIClient, input_amount: int, account: str) -> int:
    payload = client.request_or_raise(
        "POST",
        "/api/token/estimate",
        json={
            "task_type": "img2mol",
            "input_amount": input_amount,
            "account_type": account,
            "docking_type": "img2mol",
            "karmadock_out_amount": 0,
            "extra_multiples": 1,
        },
    )
    except_token = payload.get("except_token")
    if not isinstance(except_token, int):
        raise RuntimeError(f"unexpected estimate payload: {payload}")
    return except_token


def create_img2mol_job(
    client: DrugFlowAPIClient,
    ws_id: str,
    job_name: str,
    dataset_id: str,
    page_list: List[int],
    account: str,
    expect_tokens: int,
    avail_tokens: int,
) -> Dict[str, Any]:
    args_json = {
        "dataset_id": dataset_id,
        "page_list": page_list,
        "account": account,
    }
    return client.request_or_raise(
        "POST",
        "/api/jobs",
        data={
            "name": job_name,
            "type": "img2mol",
            "args": json.dumps(args_json, ensure_ascii=False),
            "ws_id": ws_id,
            "expect_tokens": str(expect_tokens),
            "avail_tokens": str(avail_tokens),
        },
    )


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DrugFlow structure-extract(img2mol) API flow with session auth.")
    parser.add_argument("--base-url", required=True, help="Example: https://new.drugflow.com")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)

    parser.add_argument("--ws-id", default=None)
    parser.add_argument("--ws-name", default="codex-structure-extract-workspace")
    parser.add_argument("--account", default="person", choices=["person", "team"])

    parser.add_argument("--dataset-id", required=True, help="Dataset created by img2mol/data-center-oss flow.")
    parser.add_argument("--page-list", default="1", help="Comma list or JSON list, e.g. 1,2,3 or [1,2,3]")

    parser.add_argument("--job-name", default="codex-img2mol-demo")
    parser.add_argument("--expect-tokens", type=int, default=None)
    parser.add_argument("--avail-tokens", type=int, default=None)

    parser.add_argument("--no-poll", action="store_true")
    parser.add_argument("--poll-timeout", type=int, default=3600)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--result-page-size", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    page_list = parse_page_list(args.page_list)

    with requests.Session() as session:
        client = DrugFlowAPIClient(args.base_url, session=session, timeout=120)
        client.signin(args.email, args.password)

        ws_id = client.ensure_workspace(args.ws_id, args.ws_name)
        jobs_before = client.list_jobs(ws_id)

        dataset_id = args.dataset_id
        dataset_meta = get_dataset_meta(client, dataset_id)
        extras = dataset_meta.get("extras_info")
        if not isinstance(extras, dict) or not extras.get("osskey"):
            raise RuntimeError(
                f"dataset {dataset_id} has no extras_info.osskey; "
                "please use an img2mol-compatible dataset from create_oss/web upload flow."
            )

        balance_tokens = client.get_balance(args.account)

        expect_tokens = args.expect_tokens
        if expect_tokens is None:
            expect_tokens = estimate_tokens(client, input_amount=len(page_list), account=args.account)

        avail_tokens = args.avail_tokens if args.avail_tokens is not None else balance_tokens

        created = create_img2mol_job(
            client=client,
            ws_id=ws_id,
            job_name=args.job_name,
            dataset_id=dataset_id,
            page_list=page_list,
            account=args.account,
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
                "dataset_id": dataset_id,
                "page_list": page_list,
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
            "dataset_id": dataset_id,
            "page_list": page_list,
            "expect_tokens": expect_tokens,
            "avail_tokens": avail_tokens,
            "jobs_before_count": jobs_before.get("count"),
            "result_count": results.get("count"),
            "results_preview": results.get("results", [])[:3],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
