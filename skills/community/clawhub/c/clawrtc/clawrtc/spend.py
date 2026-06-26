# SPDX-License-Identifier: MIT
"""
clawrtc spend-side SDK — the other half of the faucet.

`clawrtc` mines RTC (one-way) today; this module adds the spend verbs so a
balance becomes a currency:

    clawrtc pay    <to> <amount> [--memo M]   signed RTC transfer
    clawrtc tip    <to> <amount> [--memo M]   transfer flagged as a tip
    clawrtc gas    <amount>                   top up the network gas pool
    clawrtc settle <job_id> <to> <amount>     pay out a RIP-302 job escrow

All four are the SAME signed transfer underneath, against the node's
`/wallet/transfer/signed` endpoint. The signing form is pinned to the server
verifier (rustchain_v2_integrated_v2.2.1_rip200.py: wallet_transfer_signed):

    tx_data = {"from","to","amount","memo","nonce"[,"chain_id"]}
    message = json.dumps(tx_data, sort_keys=True, separators=(",",":")).encode()
    signature = Ed25519(message)   # hex
    POST {from_address,to_address,amount_rtc,memo,nonce,signature,public_key}

MONEY-PATH GUARDRAILS (RTC transfers are irreversible after the 24h pending
window):
  * Every send prints the exact payload for read-back before transmitting.
  * Confirmation is required unless --yes is passed.
  * --dry-run signs + prints but never transmits (use it to verify the payload).
  * --node lets you point at a testnet node first; verify there before mainnet.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error


# --- low-level: signing (pinned to server canonical form) ------------------------

def build_transfer_message(from_address, to_address, amount_rtc, memo, nonce,
                           chain_id=None):
    """Reconstruct the exact bytes the node signs/verifies for a transfer.

    Must byte-match rustchain wallet_transfer_signed(): compact, key-sorted JSON.
    """
    tx_data = {
        "from": from_address,
        "to": to_address,
        "amount": amount_rtc,
        "memo": memo,
        "nonce": nonce,
    }
    if chain_id:
        tx_data["chain_id"] = chain_id
    return json.dumps(tx_data, sort_keys=True, separators=(",", ":")).encode()


def sign_transfer(wallet, to_address, amount_rtc, memo="", chain_id=None,
                  nonce=None):
    """Build + Ed25519-sign a transfer. Returns the POST payload dict.

    wallet: dict with 'address', 'public_key' (hex), 'private_key' (hex).
    """
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    if nonce is None:
        # Unique per (from_address, nonce); server stores str(nonce).
        nonce = str(int(time.time() * 1000))
    nonce = str(nonce)

    from_address = wallet["address"]
    message = build_transfer_message(
        from_address, to_address, float(amount_rtc), memo, nonce, chain_id
    )
    priv = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(wallet["private_key"]))
    signature = priv.sign(message).hex()

    payload = {
        "from_address": from_address,
        "to_address": to_address,
        "amount_rtc": float(amount_rtc),
        "memo": memo,
        "nonce": nonce,
        "signature": signature,
        "public_key": wallet["public_key"],
    }
    if chain_id:
        payload["chain_id"] = chain_id
    return payload, message


def post_signed_transfer(node_url, payload, timeout=30):
    """POST a signed transfer; return (ok, response_dict)."""
    url = node_url.rstrip("/") + "/wallet/transfer/signed"
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return False, json.loads(e.read().decode())
        except Exception:
            return False, {"error": f"HTTP {e.code}", "detail": str(e)}
    except Exception as e:
        return False, {"error": str(e)}


# --- shared transfer flow (read-back + confirm guardrail) ------------------------

def _do_transfer(to_address, amount, memo, args, *, verb):
    """The one money path all spend verbs funnel through, with guardrails."""
    # Imports from cli kept local to avoid a circular import at module load.
    from clawrtc.cli import _load_wallet, NODE_URL, GREEN, YELLOW, RED, CYAN, DIM, BOLD, NC

    wallet = _load_wallet()
    if not wallet:
        print(f"{RED}No wallet found. Create one: clawrtc wallet create{NC}")
        return 1
    if not wallet.get("private_key"):
        print(f"{RED}Wallet has no private key on disk — cannot sign.{NC}")
        return 1

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        print(f"{RED}Invalid amount: {amount!r}{NC}")
        return 1
    if amount <= 0:
        print(f"{RED}Amount must be positive.{NC}")
        return 1

    node_url = getattr(args, "node", None) or NODE_URL
    chain_id = getattr(args, "chain_id", None)
    payload, message = sign_transfer(
        wallet, to_address, amount, memo=memo, chain_id=chain_id
    )

    # READ-BACK: show exactly what will be signed/sent before anything leaves.
    print(f"\n{BOLD}{CYAN}RTC {verb.upper()} — review before sending{NC}")
    print(f"  {DIM}node   {NC}{node_url}")
    print(f"  {DIM}from   {NC}{payload['from_address']}")
    print(f"  {DIM}to     {NC}{payload['to_address']}")
    print(f"  {GREEN}{BOLD}amount {amount:.6f} RTC{NC}")
    print(f"  {DIM}memo   {NC}{memo or '(none)'}")
    print(f"  {DIM}nonce  {NC}{payload['nonce']}")
    print(f"  {DIM}signed bytes: {message.decode()}{NC}")
    print(f"  {DIM}signature: {payload['signature'][:24]}...{NC}")

    if getattr(args, "dry_run", False):
        print(f"\n{YELLOW}--dry-run: signed but NOT sent. Payload above is exact.{NC}\n")
        return 0

    if not getattr(args, "yes", False):
        try:
            ans = input(f"\n  {YELLOW}Send this transfer? [y/N] {NC}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            ans = ""
        if ans not in ("y", "yes"):
            print(f"{DIM}Cancelled — nothing sent.{NC}")
            return 1

    ok, resp = post_signed_transfer(node_url, payload)
    if ok and resp.get("ok", resp.get("success", True)) and not resp.get("error"):
        txh = resp.get("tx_hash") or resp.get("pending_id") or "(see node)"
        print(f"\n{GREEN}{BOLD}✓ {verb} accepted.{NC} tx={txh}")
        if resp.get("confirms_at") or "pending" in json.dumps(resp).lower():
            print(f"  {DIM}Subject to the node's pending/confirmation window.{NC}")
        return 0
    print(f"\n{RED}✗ {verb} rejected:{NC} {resp.get('error', resp)}")
    if resp.get("code"):
        print(f"  {DIM}code: {resp['code']}{NC}")
    return 1


# --- CLI verb handlers -----------------------------------------------------------

def cmd_pay(args):
    return _do_transfer(args.to, args.amount, getattr(args, "memo", "") or "",
                        args, verb="pay")


def cmd_tip(args):
    memo = getattr(args, "memo", "") or "tip"
    return _do_transfer(args.to, args.amount, memo, args, verb="tip")


def cmd_gas(args):
    """Top up the network gas pool — a signed transfer to the gas address.

    The gas pool address can be set via --to or the RTC_GAS_ADDRESS env var;
    falls back to the documented pool address if neither is given.
    """
    gas_addr = (getattr(args, "to", None)
                or os.environ.get("RTC_GAS_ADDRESS")
                or "RTCgaspool000000000000000000000000000000")
    return _do_transfer(gas_addr, args.amount, "gas-deposit", args, verb="gas")


def cmd_settle(args):
    """Pay out a RIP-302 job escrow: signed transfer with the job id in the memo."""
    memo = f"settle:{args.job_id}"
    return _do_transfer(args.to, args.amount, memo, args, verb="settle")


def add_spend_parsers(sub):
    """Register the spend subcommands on an argparse subparsers object."""
    def _common(p):
        p.add_argument("--memo", default="", help="optional memo")
        p.add_argument("--node", default=None,
                       help="override node URL (point at testnet to verify first)")
        p.add_argument("--chain-id", dest="chain_id", default=None,
                       help="explicit chain_id (optional; must match active network)")
        p.add_argument("--dry-run", action="store_true",
                       help="sign and print the exact payload but DO NOT send")
        p.add_argument("--yes", "-y", action="store_true",
                       help="skip the confirmation prompt (for automation)")

    p_pay = sub.add_parser("pay", help="Send a signed RTC transfer")
    p_pay.add_argument("to"); p_pay.add_argument("amount"); _common(p_pay)
    p_pay.set_defaults(func=cmd_pay)

    p_tip = sub.add_parser("tip", help="Tip RTC to an address (transfer flagged as tip)")
    p_tip.add_argument("to"); p_tip.add_argument("amount"); _common(p_tip)
    p_tip.set_defaults(func=cmd_tip)

    p_gas = sub.add_parser("gas", help="Top up the network gas pool")
    p_gas.add_argument("amount")
    p_gas.add_argument("--to", default=None, help="gas pool address (or RTC_GAS_ADDRESS)")
    _common(p_gas)
    p_gas.set_defaults(func=cmd_gas)

    p_settle = sub.add_parser("settle", help="Pay out a RIP-302 job escrow")
    p_settle.add_argument("job_id"); p_settle.add_argument("to")
    p_settle.add_argument("amount"); _common(p_settle)
    p_settle.set_defaults(func=cmd_settle)
