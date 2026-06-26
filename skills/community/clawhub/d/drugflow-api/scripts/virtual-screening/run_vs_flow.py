#!/usr/bin/env python3
import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from common.drugflow_api import DrugFlowAPIClient
from common.pdb_parser import auto_pocket_from_file


TERMINAL_STATES = {"finished", "aborted", "stopped"}


def fetch_vs_db_amount(client: DrugFlowAPIClient, db_id: str) -> Optional[int]:
    payload = client.request_or_raise("GET", "/api/vs/databases")
    if isinstance(payload, list):
        for item in payload:
            if item.get("db_id") == db_id and isinstance(item.get("amount"), int):
                return item["amount"]
    return None


def estimate_tokens(
    client: DrugFlowAPIClient,
    account: str,
    input_amount: int,
    karmadock_out_amount: int,
    extra_multiples: int,
) -> int:
    payload = client.request_or_raise(
        "POST",
        "/api/token/estimate",
        json={
            "task_type": "vs_karmadock",
            "input_amount": input_amount,
            "account_type": account,
            "docking_type": "carsidock",
            "karmadock_out_amount": karmadock_out_amount,
            "extra_multiples": extra_multiples,
        },
    )
    except_token = payload.get("except_token")
    if not isinstance(except_token, int):
        raise RuntimeError(f"unexpected estimate payload: {payload}")
    return except_token


def build_vs_args(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        "pdb": [args.protein_dataset_id],
        "pdb_name": args.pdb_name,
        "input_type": "db",
        "input_source": [args.input_source],
        "input_source_labels": [args.input_source_label],
        "protein": {
            "protein_file": args.protein_dataset_id,
            "site": args.site,
            "site_label": args.site_label,
            "center": [str(args.center[0]), str(args.center[1]), str(args.center[2])],
            "size": [args.size[0], args.size[1], args.size[2]],
            "radius": args.radius,
        },
        "steps": [
            {
                "id": 1,
                "type": "admet",
                "step": "step1",
                "args": {
                    "filter": [
                        {"name": "MW", "rules": [{"condition": "gt", "value": 300}, {"condition": "lt", "value": 400}]},
                        {"name": "TPSA", "rules": [{"condition": "gt", "value": 0}, {"condition": "lt", "value": 140}]},
                        {"name": "LogS", "rules": [{"condition": "gt", "value": -4}, {"condition": "lt", "value": 0.5}]},
                        {"name": "LogP", "rules": [{"condition": "gt", "value": 1}, {"condition": "lt", "value": 3}]},
                    ]
                },
            },
            {
                "id": 2,
                "type": "karmadock",
                "step": "step2",
                "args": {
                    "outpose": 1,
                    "filter": {
                        "type": "top",
                        "order": "desc",
                        "expect": {"condition": "ge", "value": args.karmadock_out_amount},
                    },
                },
            },
            {
                "id": 3,
                "type": "carsidock",
                "step": "step3",
                "isomers": False,
                "args": {
                    "outpose": 1,
                    "filter": {
                        "type": "top",
                        "order": "desc",
                        "expect": {"condition": "ge", "value": args.carsidock_out_amount},
                    },
                },
            },
        ],
        "account": args.account,
    }


def create_vs_job(
    client: DrugFlowAPIClient,
    ws_id: str,
    name: str,
    vs_args: Dict[str, Any],
    expect_tokens: int,
    avail_tokens: int,
) -> Dict[str, Any]:
    return client.request_or_raise(
        "POST",
        "/api/jobs",
        data={
            "name": name,
            "type": "virtual_screening",
            "args": json.dumps(vs_args, ensure_ascii=False),
            "ws_id": ws_id,
            "expect_tokens": str(expect_tokens),
            "avail_tokens": str(avail_tokens),
        },
    )


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


def fetch_vs_results(client: DrugFlowAPIClient, job_id: int, page_size: int) -> Dict[str, Any]:
    payload = client.request_or_raise(
        "GET",
        f"/api/vs/{job_id}/results",
        params={"page": 1, "page_size": page_size},
    )
    if not isinstance(payload, dict):
        raise RuntimeError(f"unexpected VS results payload: {payload}")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DrugFlow VS API flow with session auth.")
    parser.add_argument("--base-url", required=True, help="Example: http://127.0.0.1:8888")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)

    parser.add_argument("--ws-id", default=None)
    parser.add_argument("--ws-name", default="codex-vs-workspace")
    parser.add_argument("--account", default="person", choices=["person", "team"])

    parser.add_argument("--protein-dataset-id", required=True)
    parser.add_argument("--pdb-name", default="protein.pdb")
    parser.add_argument("--pdb-file", default=None,
                        help="Local PDB file path; when provided and --site is omitted, "
                             "pocket params (site/center/size/radius) are auto-detected "
                             "from the largest ligand in this file.")
    parser.add_argument("--input-source", default="repurposing")
    parser.add_argument("--input-source-label", default="Drug Repurposing Compound Library(4317)")

    parser.add_argument("--site", default=None,
                        help="Binding site identifier, e.g. 'A:KY9'. Auto-detected from PDB if --pdb-file is given.")
    parser.add_argument("--site-label", default=None,
                        help="Binding site label, e.g. 'A:KY9:601'. Auto-detected from PDB if --pdb-file is given.")
    parser.add_argument("--center", nargs=3, type=float, default=None,
                        help="Pocket center [x y z] in Angstroms. Auto-detected from PDB if --pdb-file is given.")
    parser.add_argument("--size", nargs=3, type=float, default=None,
                        help="Pocket box dimensions [x y z] in Angstroms. Auto-detected from PDB if --pdb-file is given.")
    parser.add_argument("--radius", type=float, default=None,
                        help="Pocket search radius in Angstroms. Auto-detected from PDB if --pdb-file is given.")
    parser.add_argument("--expand", type=float, default=10.0,
                        help="Padding added to ligand bounding box for auto-detected pocket (default: 10 Å).")

    parser.add_argument("--karmadock-out-amount", type=int, default=50)
    parser.add_argument("--carsidock-out-amount", type=int, default=10)
    parser.add_argument("--extra-multiples", type=int, default=1)

    parser.add_argument("--job-name", default="codex-vs-demo")
    parser.add_argument("--poll-timeout", type=int, default=1800)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--result-page-size", type=int, default=20)
    return parser.parse_args()


def resolve_pocket_args(args: argparse.Namespace) -> None:
    """Fill in site/center/size/radius from a local PDB file when not explicitly provided."""
    needs_auto = args.site is None or args.center is None or args.size is None or args.radius is None
    if not needs_auto:
        return

    if not args.pdb_file:
        raise RuntimeError(
            "Pocket params (--site, --center, --size, --radius) not fully specified "
            "and no --pdb-file given for auto-detection."
        )

    pocket = auto_pocket_from_file(args.pdb_file, expand=args.expand)
    if pocket is None:
        raise RuntimeError(
            f"No ligand with >= 6 atoms found in {args.pdb_file}; "
            "cannot auto-detect pocket. Provide --site, --center, --size, --radius explicitly."
        )

    if args.site is None:
        args.site = pocket.site
    if args.site_label is None:
        args.site_label = pocket.site_label
    if args.center is None:
        args.center = list(pocket.center)
    if args.size is None:
        args.size = list(pocket.size)
    if args.radius is None:
        args.radius = pocket.radius

    print(f"[auto-detect] site={args.site}  site_label={args.site_label}")
    print(f"[auto-detect] center={args.center}  size={args.size}  radius={args.radius}")


def main() -> None:
    args = parse_args()
    resolve_pocket_args(args)

    with requests.Session() as session:
        client = DrugFlowAPIClient(args.base_url, session=session)
        client.signin(args.email, args.password)
        ws_id = client.ensure_workspace(args.ws_id, args.ws_name)

        balance_tokens = client.get_balance(args.account)
        jobs_before = client.list_jobs(ws_id)

        input_amount = fetch_vs_db_amount(client, args.input_source)
        if input_amount is None:
            raise RuntimeError(
                f"cannot resolve input_amount from /api/vs/databases for input_source={args.input_source}; "
                "pick a valid db_id or adjust script."
            )

        expect_tokens = estimate_tokens(
            client,
            args.account,
            input_amount,
            args.karmadock_out_amount,
            args.extra_multiples,
        )

        vs_args = build_vs_args(args)
        created = create_vs_job(
            client,
            ws_id,
            args.job_name,
            vs_args,
            expect_tokens,
            balance_tokens,
        )
        job_id = created.get("id")
        if not isinstance(job_id, int):
            raise RuntimeError(f"job create response missing id: {created}")

        final_job = poll_job(
            client,
            ws_id,
            job_id,
            timeout_s=args.poll_timeout,
            interval_s=args.poll_interval,
        )

        vs_results = fetch_vs_results(client, job_id, args.result_page_size)

        output = {
            "ws_id": ws_id,
            "job_id": job_id,
            "job_state": final_job.get("state"),
            "jobs_before_count": jobs_before.get("count"),
            "vs_result_count": vs_results.get("count"),
            "vs_results_preview": vs_results.get("results", [])[:3],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
