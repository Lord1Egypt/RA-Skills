#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict

import requests

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from common.drugflow_api import DrugFlowAPIClient
from common.pdb_parser import auto_pocket_from_file
from common.pdb_parser import auto_pocket_from_file_with_site


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
        payload = client.request_or_raise(
            "POST",
            "/api/dataset/upload",
            data=data,
            files=files,
        )

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


def estimate_tokens(
    client: DrugFlowAPIClient,
    task_type: str,
    input_amount: int,
    account_type: str,
    extra_multiples: int,
) -> int:
    payload = client.request_or_raise(
        "POST",
        "/api/token/estimate",
        json={
            "task_type": task_type,
            "input_amount": input_amount,
            "account_type": account_type,
            "docking_type": task_type,
            "karmadock_out_amount": 0,
            "extra_multiples": extra_multiples,
        },
    )
    except_token = payload.get("except_token")
    if not isinstance(except_token, int):
        raise RuntimeError(f"unexpected estimate payload: {payload}")
    return except_token


def build_args(args: argparse.Namespace, pdb_dataset_id: str, ligands_dataset_id: str) -> Dict[str, Any]:
    return {
        "pdb_name": args.pdb_name,
        "ligands_name": args.ligands_name,
        "pdb": [pdb_dataset_id],
        "mol": [ligands_dataset_id],
        "protein": {
            "pdb_tab": "数据中心",
            "need_prot_process": True,
            "if_delete_comps_by_user_define": False,
            "delete_water": [],
            "delete_hets": [],
            "delete_chains": [],
            "irrelevant_waters": False,
            "chain": [args.chain],
            "add_missing_residue": True,
            "addh": True,
            "modify_protonation": True,
            "ph": 7.4,
            "opt_hydrogen": True,
            "force_field": "amber14/protein.ff14SB",
        },
        "ligands": {
            "mol_tab": "数据中心",
            "ligands": args.ligands_name,
            "molecule_minimize": "MMFF94",
            "protonation": "set_pH",
            "min_ph": args.min_ph,
            "max_ph": args.max_ph,
            "disconnect_group": True,
            "keep_large_fragment": True,
            "isomer_limit": args.isomer_limit,
            "tautomers": True,
            "stereoisomers": "general_all",
            "is_isomer": True,
        },
        "docking": {
            "center": [str(args.center[0]), str(args.center[1]), str(args.center[2])],
            "size": [args.size[0], args.size[1], args.size[2]],
            "site": args.site,
            "radius": args.radius,
            "distance": args.distance,
            "scoring_function": args.scoring_function,
            "num_poses": args.num_poses,
            "flexible": args.flexible,
            "rescoring_functions": [args.rescoring],
        },
        "account": args.account,
    }


def create_docking_job(
    client: DrugFlowAPIClient,
    name: str,
    ws_id: str,
    pdb_dataset_id: str,
    ligands_dataset_id: str,
    smiles_col: str,
    pdb_content_path: str,
    args_json: Dict[str, Any],
    expect_tokens: int,
    avail_tokens: int,
) -> Dict[str, Any]:
    data = {
        "name": name,
        "type": "docking",
        "args": json.dumps(args_json, ensure_ascii=False),
        "pdb": pdb_dataset_id,
        "ligands": ligands_dataset_id,
        "ws_id": ws_id,
        "smiles_col": smiles_col,
        "expect_tokens": str(expect_tokens),
        "avail_tokens": str(avail_tokens),
    }

    with open(pdb_content_path, "rb") as fp:
        files = {
            "pdb_content": (
                Path(pdb_content_path).name,
                fp,
                mimetypes.guess_type(pdb_content_path)[0] or "application/octet-stream",
            )
        }
        return client.request_or_raise("POST", "/api/jobs", data=data, files=files)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DrugFlow docking API flow with session auth.")

    parser.add_argument("--base-url", required=True, help="Example: http://127.0.0.1:8888")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)

    parser.add_argument("--ws-id", default=None)
    parser.add_argument("--ws-name", default="codex-docking-workspace")
    parser.add_argument("--account", default="person", choices=["person", "team"])

    parser.add_argument("--pdb-file", default=None,
                        help="Local pdb file path for upload and pdb_content. "
                             "Also used for auto-detecting site/docking box when pocket args are omitted.")
    parser.add_argument("--ligands-file", default=None, help="Local ligands file path (.sdf/.csv) for upload")
    parser.add_argument("--pdb-dataset-id", default=None)
    parser.add_argument("--ligands-dataset-id", default=None)
    parser.add_argument("--pdb-content-file", default=None,
                        help="File sent as form field pdb_content. Can also drive auto pocket detection "
                             "when --pdb-file is not provided.")

    parser.add_argument("--job-name", default="codex-docking-demo")
    parser.add_argument("--pdb-name", default="protein.pdb")
    parser.add_argument("--ligands-name", default="ligands.sdf")
    parser.add_argument("--smiles-col", default="cs-smiles")

    parser.add_argument("--scoring-function", default="carsidock", choices=["carsidock", "carsidock-cov", "karmadock", "vina", "vina_gpu", "boltz"])
    parser.add_argument("--site", default=None,
                        help="Binding site, e.g. 'A:KY9'. Auto-detected from PDB file when omitted.")
    parser.add_argument("--site-label", default=None,
                        help="Binding site label, e.g. 'A:KY9:601'. Auto-detected from PDB file when omitted.")
    parser.add_argument("--chain", default="A")
    parser.add_argument("--center", nargs=3, type=float, default=None,
                        help="Pocket center [x y z]. Auto-detected from PDB file when omitted.")
    parser.add_argument("--size", nargs=3, type=float, default=None,
                        help="Pocket box dimensions [x y z]. Auto-detected from PDB file when omitted.")
    parser.add_argument("--radius", type=float, default=None,
                        help="Pocket search radius. Auto-detected from PDB file when omitted.")
    parser.add_argument("--distance", type=float, default=4.5)
    parser.add_argument("--expand", type=float, default=10.0,
                        help="Bounding-box padding for auto-detected pocket (default: 10 Å).")
    parser.add_argument("--num-poses", type=int, default=1)
    parser.add_argument("--flexible", default="semi", choices=["none", "semi", "flex"])
    parser.add_argument("--rescoring", default="RTMS")

    parser.add_argument("--min-ph", type=float, default=6.4)
    parser.add_argument("--max-ph", type=float, default=8.4)
    parser.add_argument("--isomer-limit", type=int, default=5)

    parser.add_argument("--expect-tokens", type=int, default=None)
    parser.add_argument("--avail-tokens", type=int, default=None)
    parser.add_argument("--poll-timeout", type=int, default=1800)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--result-page-size", type=int, default=20)
    return parser.parse_args()


def resolve_pocket_args(args: argparse.Namespace) -> None:
    """Fill in site/center/size/radius from a local PDB file when not explicitly provided."""
    needs_auto = args.site is None or args.center is None or args.size is None or args.radius is None
    if not needs_auto:
        return

    pdb_path = args.pdb_file or args.pdb_content_file
    if not pdb_path:
        raise RuntimeError(
            "Pocket params (--site, --center, --size, --radius) not fully specified "
            "and neither --pdb-file nor --pdb-content-file is provided for auto-detection."
        )

    pocket = None
    # If user already provided site/site_label but omitted box params,
    # prefer deriving center/size/radius from the same site.
    site_selector = args.site_label or args.site
    if site_selector:
        pocket = auto_pocket_from_file_with_site(pdb_path, site_selector=site_selector, expand=args.expand)
    if pocket is None:
        pocket = auto_pocket_from_file(pdb_path, expand=args.expand)
    if pocket is None:
        raise RuntimeError(
            f"No ligand with >= 6 atoms found in {pdb_path}; "
            "cannot auto-detect pocket. Provide --site, --center, --size, --radius explicitly."
        )

    if args.site is None:
        args.site = pocket.site
    if getattr(args, "site_label", None) is None:
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
        client = DrugFlowAPIClient(args.base_url, session=session, timeout=120)
        client.signin(args.email, args.password)
        ws_id = client.ensure_workspace(args.ws_id, args.ws_name)

        pdb_dataset_id = args.pdb_dataset_id
        if not pdb_dataset_id:
            if not args.pdb_file:
                raise RuntimeError("pdb dataset missing: provide --pdb-dataset-id or --pdb-file")
            pdb_dataset_id = upload_dataset(client, ws_id, args.pdb_file)

        ligands_dataset_id = args.ligands_dataset_id
        if not ligands_dataset_id:
            if not args.ligands_file:
                raise RuntimeError("ligands dataset missing: provide --ligands-dataset-id or --ligands-file")
            ligands_dataset_id = upload_dataset(client, ws_id, args.ligands_file)

        pdb_content_file = args.pdb_content_file or args.pdb_file
        if not pdb_content_file or not os.path.isfile(pdb_content_file):
            raise RuntimeError("pdb_content file is required: provide --pdb-content-file or --pdb-file")

        balance_tokens = client.get_balance(args.account)

        ligands_count = get_dataset_count(client, ligands_dataset_id)
        expect_tokens = args.expect_tokens
        if expect_tokens is None:
            expect_tokens = estimate_tokens(
                client,
                task_type=args.scoring_function,
                input_amount=ligands_count,
                account_type=args.account,
                extra_multiples=args.isomer_limit,
            )

        avail_tokens = args.avail_tokens if args.avail_tokens is not None else balance_tokens

        docking_args = build_args(args, pdb_dataset_id, ligands_dataset_id)
        created = create_docking_job(
            client,
            name=args.job_name,
            ws_id=ws_id,
            pdb_dataset_id=pdb_dataset_id,
            ligands_dataset_id=ligands_dataset_id,
            smiles_col=args.smiles_col,
            pdb_content_path=pdb_content_file,
            args_json=docking_args,
            expect_tokens=expect_tokens,
            avail_tokens=avail_tokens,
        )

        job_id = created.get("id")
        if not isinstance(job_id, int):
            raise RuntimeError(f"job create response missing id: {created}")

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
            "pdb_dataset_id": pdb_dataset_id,
            "ligands_dataset_id": ligands_dataset_id,
            "ligands_count": ligands_count,
            "expect_tokens": expect_tokens,
            "avail_tokens": avail_tokens,
            "job_id": job_id,
            "job_state": final_job.get("state"),
            "result_count": results.get("count"),
            "results_preview": results.get("results", [])[:3],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
