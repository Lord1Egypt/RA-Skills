# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx>=0.27.0"]
# ///
"""NFT minting client — communicates with the ClawMBTI centralized minting API."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# ============================================================
# API config
# ============================================================
API_BASE_URL = "https://clawmbti-dev.myfinchain.com/api/v1"
API_KEY = "sk-clawmbti"


def get_nft_status_path(mbti_dir: str | None = None) -> Path:
    if mbti_dir:
        base = Path(mbti_dir).expanduser().resolve()
    else:
        base = Path.home() / ".mbti"
    return base / "nft-status.json"


def update_nft_status(mbti_dir: str | None, data: dict[str, Any]) -> None:
    path = get_nft_status_path(mbti_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def cmd_check(args: argparse.Namespace) -> None:
    """Check if a wallet has already minted via GET /nft/status/:walletAddress"""
    import httpx

    wallet = args.wallet_address
    if not wallet:
        print(json.dumps({"error": "missing --wallet-address"}), file=sys.stderr)
        sys.exit(1)

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.get(
                f"{API_BASE_URL}/nft/status/{wallet}",
                headers=_headers(),
            )
            resp.raise_for_status()
            print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except httpx.HTTPStatusError as e:
        print(json.dumps({"error": str(e), "response": e.response.text}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def cmd_mint(args: argparse.Namespace) -> None:
    """Mint an NFT via POST /nft/mint"""
    import httpx

    mint_data: dict[str, Any] = json.loads(args.data)

    required_fields = ["wallet_address", "mbti_type", "dimensions"]
    for field in required_fields:
        if field not in mint_data:
            print(json.dumps({"error": f"missing required field: {field}"}), file=sys.stderr)
            sys.exit(1)

    # Normalize dimensions: accept both old format {ei:{e,i}} and new flat format {EI, NS, TF, JP}
    dims = mint_data["dimensions"]
    if "EI" not in dims and "ei" in dims:
        ei = dims["ei"]
        ns = dims.get("sn", dims.get("ns", {}))
        tf = dims.get("tf", {})
        jp = dims.get("jp", {})
        mint_data["dimensions"] = {
            "EI": ei.get("e", 50) - ei.get("i", 50),
            "NS": ns.get("n", 50) - ns.get("s", 50),
            "TF": tf.get("t", 50) - tf.get("f", 50),
            "JP": jp.get("j", 50) - jp.get("p", 50),
        }

    payload = {
        "wallet_address": mint_data["wallet_address"],
        "mbti_type": mint_data["mbti_type"],
        "dimensions": mint_data["dimensions"],
    }
    if "referred_by" in mint_data:
        payload["referred_by"] = mint_data["referred_by"]
    if "agent_name" in mint_data:
        payload["agent_name"] = mint_data["agent_name"]
    if "model" in mint_data:
        payload["model"] = mint_data["model"]

    try:
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                f"{API_BASE_URL}/nft/mint",
                headers=_headers(),
                json=payload,
            )

            # 409 = already minted — treat as success
            if resp.status_code == 409:
                data = resp.json()
                nft_status: dict[str, Any] = {
                    "status": "minted",
                    "token_id": data.get("tokenId", ""),
                    "tx_hash": data.get("txHash", ""),
                    "image_url": data.get("imageUrl", ""),
                    "mock": False,
                    "error": None,
                }
                update_nft_status(args.mbti_dir, nft_status)
                print(json.dumps({"status": "already_minted", "result": data}, indent=2))
                return

            # 503 = insufficient SOL balance
            if resp.status_code == 503:
                data = resp.json()
                msg = data.get("error", "今日龙虾已全部出海，明日再来捞一只吧 🦞")
                nft_status = {
                    "status": "failed",
                    "token_id": None,
                    "tx_hash": None,
                    "image_url": None,
                    "error": msg,
                }
                update_nft_status(args.mbti_dir, nft_status)
                print(json.dumps({"status": "quota_exhausted", "error": msg}, indent=2, ensure_ascii=False))
                return

            resp.raise_for_status()
            data = resp.json()

            nft_status = {
                "status": "minted",
                "token_id": data.get("tokenId", ""),
                "tx_hash": data.get("txHash", ""),
                "image_url": data.get("imageUrl", ""),
                "mock": data.get("mock", False),
                "error": None,
            }
            update_nft_status(args.mbti_dir, nft_status)
            print(json.dumps({"status": "ok", "result": data}, indent=2, ensure_ascii=False))

    except httpx.HTTPStatusError as e:
        nft_status = {
            "status": "failed",
            "token_id": None,
            "tx_hash": None,
            "image_url": None,
            "error": str(e),
        }
        update_nft_status(args.mbti_dir, nft_status)
        print(json.dumps({"error": str(e), "response": e.response.text}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        nft_status = {
            "status": "failed",
            "token_id": None,
            "tx_hash": None,
            "image_url": None,
            "error": str(e),
        }
        update_nft_status(args.mbti_dir, nft_status)
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def cmd_share(args: argparse.Namespace) -> None:
    """Get share content via POST /nft/share-content"""
    import httpx

    if not args.token_id:
        print(json.dumps({"error": "missing --token-id"}), file=sys.stderr)
        sys.exit(1)

    payload: dict[str, Any] = {"token_id": args.token_id}
    if args.wallet_address:
        payload["wallet_address"] = args.wallet_address

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                f"{API_BASE_URL}/nft/share-content",
                headers=_headers(),
                json=payload,
            )
            resp.raise_for_status()
            print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except httpx.HTTPStatusError as e:
        print(json.dumps({"error": str(e), "response": e.response.text}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def cmd_status(args: argparse.Namespace) -> None:
    """Read local nft-status.json"""
    path = get_nft_status_path(args.mbti_dir)
    if not path.exists():
        print(json.dumps({"status": "none"}))
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_report(args: argparse.Namespace) -> None:
    """Report detect result via POST /detect/result"""
    import httpx

    report_data: dict[str, Any] = json.loads(args.data)

    required_fields = ["session_id", "mbti_type", "dimensions"]
    for field in required_fields:
        if field not in report_data:
            print(json.dumps({"error": f"missing required field: {field}"}), file=sys.stderr)
            sys.exit(1)

    # Normalize dimensions: accept both {ei:{e,i}} and flat {EI, NS, TF, JP}
    dims = report_data["dimensions"]
    if "EI" not in dims and "ei" in dims:
        ei = dims["ei"]
        ns = dims.get("sn", dims.get("ns", {}))
        tf = dims.get("tf", {})
        jp = dims.get("jp", {})
        report_data["dimensions"] = {
            "EI": ei.get("e", 50) - ei.get("i", 50),
            "NS": ns.get("n", 50) - ns.get("s", 50),
            "TF": tf.get("t", 50) - tf.get("f", 50),
            "JP": jp.get("j", 50) - jp.get("p", 50),
        }

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                f"{API_BASE_URL}/detect/result",
                headers=_headers(),
                json=report_data,
            )
            resp.raise_for_status()
            print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        # 上报失败不影响主流程，静默忽略
        print(json.dumps({"error": str(e)}), file=sys.stderr)


def cmd_update_report(args: argparse.Namespace) -> None:
    """Update agent_name for an existing test record via PATCH /detect/result"""
    import httpx

    data: dict[str, Any] = json.loads(args.data)
    if "id" not in data or "agent_name" not in data:
        print(json.dumps({"error": "missing required fields: id, agent_name"}), file=sys.stderr)
        sys.exit(1)

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.patch(
                f"{API_BASE_URL}/detect/result",
                headers=_headers(),
                json=data,
            )
            resp.raise_for_status()
            print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="ClawMBTI NFT minting client")
    parser.add_argument("--mbti-dir", type=str, default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    # check
    check_parser = subparsers.add_parser("check", help="Check if wallet already minted")
    check_parser.add_argument("--wallet-address", required=True)

    # mint
    mint_parser = subparsers.add_parser("mint", help="Mint NFT")
    mint_parser.add_argument("--data", required=True, help="JSON: wallet_address, mbti_type, dimensions")

    # share
    share_parser = subparsers.add_parser("share", help="Get share content")
    share_parser.add_argument("--token-id", required=True)
    share_parser.add_argument("--wallet-address", default=None)

    # status
    subparsers.add_parser("status", help="Read local mint status")

    # report
    report_parser = subparsers.add_parser("report", help="Report detect result to server")
    report_parser.add_argument("--data", required=True, help="JSON: session_id, mbti_type, dimensions, [evidence, description, agent_name, model, wallet_address]")

    # update-report
    update_report_parser = subparsers.add_parser("update-report", help="Update agent_name for an existing test record")
    update_report_parser.add_argument("--data", required=True, help="JSON: id, agent_name")

    args = parser.parse_args()
    commands: dict[str, Any] = {
        "check": cmd_check,
        "mint": cmd_mint,
        "share": cmd_share,
        "status": cmd_status,
        "report": cmd_report,
        "update-report": cmd_update_report,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
