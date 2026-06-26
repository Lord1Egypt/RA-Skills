#!/usr/bin/env python3
import argparse
import json
import mimetypes
import sys
import time
from contextlib import ExitStack
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from common.drugflow_api import DrugFlowAPIClient


TERMINAL_STATES = {"finished", "aborted", "stopped"}


def parse_int_list(value: str) -> List[int]:
    raw = (value or "").strip()
    if not raw:
        return []
    if raw.startswith("["):
        data = json.loads(raw)
        if not isinstance(data, list):
            raise RuntimeError("selected atoms json must be a list")
        return [int(x) for x in data]
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


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


def run_atom_info(client: DrugFlowAPIClient, sdf_file: str) -> None:
    with open(sdf_file, "rb") as fp:
        payload = client.request_or_raise(
            "POST",
            "/api/toolkits/rdkit/mol_atom_info",
            files={
                "sdf": (
                    Path(sdf_file).name,
                    fp,
                    mimetypes.guess_type(sdf_file)[0] or "chemical/x-mdl-sdfile",
                ),
            },
        )
    atom_list = payload.get("atom_list", [])
    output = {
        "atom_count": len(atom_list),
        "atom_list": atom_list,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def run_extract_partial(client: DrugFlowAPIClient, sdf_file: str, selected_atoms: List[int]) -> None:
    if not selected_atoms:
        raise RuntimeError("selected atoms is empty")
    with open(sdf_file, "rb") as fp:
        payload = client.request_or_raise(
            "POST",
            "/api/toolkits/rdkit/extract_partial_mol",
            data={"selected_atoms": json.dumps(selected_atoms, ensure_ascii=False)},
            files={
                "sdf": (
                    Path(sdf_file).name,
                    fp,
                    mimetypes.guess_type(sdf_file)[0] or "chemical/x-mdl-sdfile",
                ),
            },
        )
    output = {
        "selected_atoms": selected_atoms,
        "smiles": payload.get("smiles"),
        "mol_block_2d": payload.get("mol_block_2d"),
        "mol_block_3d": payload.get("mol_block_3d"),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def run_draw_atom_index(sdf_file: str, output: str, size: int) -> None:
    from rdkit import Chem
    from rdkit.Chem import AllChem
    from rdkit.Chem import Draw

    mol = Chem.SDMolSupplier(sdf_file, sanitize=False)[0]
    if mol is None:
        raise RuntimeError(f"cannot parse sdf: {sdf_file}")

    # Annotate atom indices for manual confirmation.
    for atom in mol.GetAtoms():
        atom.SetProp("atomNote", str(atom.GetIdx()))

    try:
        AllChem.Compute2DCoords(mol)
    except Exception:
        pass

    out_path = Path(output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    Draw.MolToFile(mol, str(out_path), size=(size, size))

    print(
        json.dumps(
            {
                "image": str(out_path),
                "size": size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def run_create_job(client: DrugFlowAPIClient, args: argparse.Namespace) -> None:
    args_obj = json.loads(Path(args.args_file).read_text(encoding="utf-8"))
    if not isinstance(args_obj, dict):
        raise RuntimeError("--args-file must be a JSON object")
    # Skill defaults: non-docking molecular factory with Frag-GPT + REINVENT.
    args_obj.setdefault("need_docking", False)
    args_obj.setdefault("molgen_algos", ["Frag-GPT", "REINVENT"])
    default_pdb_use = {
        "3D-linker": False,
        "Diff-linker": False,
        "Frag-GPT": False,
        "Delete": False,
        "REINVENT": False,
    }
    if not isinstance(args_obj.get("pdb_use"), dict):
        args_obj["pdb_use"] = default_pdb_use.copy()
    else:
        for algo, enabled in default_pdb_use.items():
            args_obj["pdb_use"].setdefault(algo, enabled)
    args_obj.setdefault("account", args.account)

    if args_obj.get("data_from") == "upload" and not args.ligands_file_for_docking:
        raise RuntimeError("args.data_from=upload requires --ligands-file-for-docking")
    if args_obj.get("ori_ligand_from") == "file" and not args.ori_ligand_file:
        raise RuntimeError("args.ori_ligand_from=file requires --ori-ligand-file")

    ws_id = client.ensure_workspace(args.ws_id, args.ws_name)
    balance_tokens = client.get_balance(args_obj.get("account", "person"))
    jobs_before = client.list_jobs(ws_id)

    gen_num = int(args_obj.get("gen_num", 1))
    expect_tokens = args.expect_tokens
    if expect_tokens is None:
        try:
            expect_tokens = estimate_tokens(
                client,
                task_type="molfactory",
                input_amount=gen_num,
                account=args_obj.get("account", "person"),
            )
        except Exception as exc:
            expect_tokens = gen_num * 100
            print(f"[warn] token estimate failed, fallback to {expect_tokens} ({exc})")

    avail_tokens = args.avail_tokens if args.avail_tokens is not None else balance_tokens

    with ExitStack() as stack:
        files: Dict[str, Any] = {}
        data = {
            "name": args.job_name,
            "type": "molecular_factory",
            "args": json.dumps(args_obj, ensure_ascii=False),
            "ws_id": ws_id,
            "expect_tokens": str(expect_tokens),
            "avail_tokens": str(avail_tokens),
            # Keep this key for backend request.data["pdb_file"] access.
            "pdb_file": "",
        }
        if args.ligands_file_smiles_col:
            data["ligands_file_smiles_col"] = args.ligands_file_smiles_col

        if args.pdb_file:
            fp = stack.enter_context(open(args.pdb_file, "rb"))
            files["pdb_file"] = (
                Path(args.pdb_file).name,
                fp,
                mimetypes.guess_type(args.pdb_file)[0] or "chemical/x-pdb",
            )

        if args.ori_ligand_file:
            fp = stack.enter_context(open(args.ori_ligand_file, "rb"))
            files["ori_ligand"] = (
                Path(args.ori_ligand_file).name,
                fp,
                mimetypes.guess_type(args.ori_ligand_file)[0] or "chemical/x-mdl-sdfile",
            )

        if args.ligands_file_for_docking:
            fp = stack.enter_context(open(args.ligands_file_for_docking, "rb"))
            files["ligands_file_for_docking"] = (
                Path(args.ligands_file_for_docking).name,
                fp,
                mimetypes.guess_type(args.ligands_file_for_docking)[0] or "chemical/x-mdl-sdfile",
            )

        if args.ligands_file_for_train:
            fp = stack.enter_context(open(args.ligands_file_for_train, "rb"))
            files["ligands_file_for_train"] = (
                Path(args.ligands_file_for_train).name,
                fp,
                mimetypes.guess_type(args.ligands_file_for_train)[0] or "application/octet-stream",
            )

        created = client.request_or_raise("POST", "/api/jobs", data=data, files=files if files else None)

    job_id = created.get("id")
    if not isinstance(job_id, int):
        raise RuntimeError(f"job create response missing id: {created}")

    if args.no_poll:
        output = {
            "ws_id": ws_id,
            "job_id": job_id,
            "job_state": created.get("state"),
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
    output = {
        "ws_id": ws_id,
        "job_id": job_id,
        "job_state": final_job.get("state"),
        "expect_tokens": expect_tokens,
        "avail_tokens": avail_tokens,
        "jobs_before_count": jobs_before.get("count"),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DrugFlow molecular factory helper flows.")
    parser.add_argument("--base-url", required=True, help="Example: https://new.drugflow.com")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)

    sub = parser.add_subparsers(dest="command", required=True)

    atom = sub.add_parser("atom-info", help="List atom indices/symbols for an SDF.")
    atom.add_argument("--sdf-file", required=True)

    part = sub.add_parser("extract-partial", help="Extract substructure by selected atom indices.")
    part.add_argument("--sdf-file", required=True)
    part.add_argument(
        "--selected-atoms",
        required=True,
        help="Comma list or JSON list, e.g. 1,2,3 or [1,2,3]",
    )

    draw = sub.add_parser("draw-atom-index", help="Render atom-index annotated PNG for manual confirmation.")
    draw.add_argument("--sdf-file", required=True)
    draw.add_argument("--output", required=True, help="Output PNG path.")
    draw.add_argument("--size", type=int, default=900)

    create = sub.add_parser("create-job", help="Create molecular factory job from args.json.")
    create.add_argument("--args-file", required=True, help="JSON object file for molecular factory args.")
    create.add_argument("--ws-id", default=None)
    create.add_argument("--ws-name", default="codex-molfactory-workspace")
    create.add_argument("--account", default="person", choices=["person", "team"])
    create.add_argument("--job-name", default="codex-molfactory-demo")
    create.add_argument("--pdb-file", default=None)
    create.add_argument("--ori-ligand-file", default=None)
    create.add_argument("--ligands-file-for-docking", default=None)
    create.add_argument("--ligands-file-for-train", default=None)
    create.add_argument("--ligands-file-smiles-col", default=None)
    create.add_argument("--expect-tokens", type=int, default=None)
    create.add_argument("--avail-tokens", type=int, default=None)
    create.add_argument("--no-poll", action="store_true")
    create.add_argument("--poll-timeout", type=int, default=7200)
    create.add_argument("--poll-interval", type=int, default=10)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "draw-atom-index":
        run_draw_atom_index(args.sdf_file, output=args.output, size=args.size)
        return

    with requests.Session() as session:
        client = DrugFlowAPIClient(args.base_url, session=session, timeout=120)
        client.signin(args.email, args.password)

        if args.command == "atom-info":
            run_atom_info(client, args.sdf_file)
        elif args.command == "extract-partial":
            selected_atoms = parse_int_list(args.selected_atoms)
            run_extract_partial(client, args.sdf_file, selected_atoms=selected_atoms)
        elif args.command == "create-job":
            run_create_job(client, args)
        else:
            raise RuntimeError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    main()
