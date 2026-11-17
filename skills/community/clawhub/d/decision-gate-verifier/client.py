"""
Client SDK for the decision-gate external verifier — the missing piece for anyone who isn't us.

THE PROBLEM THIS FILE SOLVES: without it, using the paid verifier means hand-rolling every one of
these yourself, in order, correctly:
  1. ABI-encode and sign a requestVerification() transaction, estimate gas (not guess it — a
     hardcoded gas limit silently under-provisions and burns the tx with no refund), submit it,
     wait for the receipt, and parse the VerificationRequested event log to get your request_id.
  2. Make three raw HTTP POSTs (/hash, /verify, /reproduce) with exact, easy-to-typo JSON shapes.
  3. ABI-encode and sign a second transaction (recordReceipt()) using args nested three levels
     deep in the /verify response, again with proper gas estimation.
  4. Manage your own nonces across both transactions.
That is real engineering work — it's exactly what verify_server.py's own test scripts had to do,
and it's what production-hardened out to ~130 lines of easy-to-get-subtly-wrong web3 code before
this file existed. A caller who wants "check this claim, get PASS/REFUSE" should not have to
become a competent web3 engineer first. This wraps all four steps into a handful of calls.

WHY web3.py/eth_account ARE REQUIRED HERE (unlike the free decision-gate skill, which is
deliberately stdlib-only): signing a real on-chain transaction needs real ECDSA/keccak. There is
no way around that dependency for a caller who is, by definition, about to sign one. This package
is for people integrating the PAID tier, not people using the free local skill.

Usage — the common case, three lines:

    from decision_gate_verifier import VerifierClient
    client = VerifierClient(private_key="0x...")
    receipt = client.check(contract, proposed_action,
                            observed_inputs={...}, granted_authorities=[...], observed_facts={...})
    print(receipt["verdict"])                 # "PASS" or "REFUSE" — you're paying for the answer
                                               # either way, not just a "yes"
    client.record_receipt(receipt)            # optional: anchor the verdict on Base permanently

Or drive the four steps individually if you need to inspect/log each stage — see check()'s body,
which is just those four calls in order with nothing hidden.
"""
from __future__ import annotations

import base64
import json
import secrets
import time
import urllib.error
import urllib.request

from eth_account import Account
from eth_account.messages import encode_typed_data
from web3 import Web3

DEFAULT_RPC_URL = "https://mainnet.base.org"
DEFAULT_API_URL = "https://soulscore.xyz/api"
DEFAULT_REGISTRY_ADDRESS = "0x2C125C03577296a3e552e5439D356F0294349ce9"
DEFAULT_USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # Base mainnet USDC
DEFAULT_CHAIN_ID = 8453
_UA = "decision-gate-verifier-client/0.3 (+https://soulscore.xyz/decision-gate)"

_REGISTRY_ABI = [
    {"name": "requestVerification", "type": "function", "stateMutability": "nonpayable",
     "inputs": [{"name": "contractHash", "type": "bytes32"}, {"name": "actionHash", "type": "bytes32"}],
     "outputs": [{"name": "requestId", "type": "bytes32"}]},
    {"name": "recordReceipt", "type": "function", "stateMutability": "nonpayable",
     "inputs": [{"name": "requestId", "type": "bytes32"}, {"name": "contractHash", "type": "bytes32"},
                {"name": "actionHash", "type": "bytes32"}, {"name": "receiptHash", "type": "bytes32"},
                {"name": "verdict", "type": "string"}, {"name": "nonce", "type": "bytes32"},
                {"name": "sig", "type": "bytes"}],
     "outputs": []},
    {"name": "requests", "type": "function", "stateMutability": "view",
     "inputs": [{"name": "", "type": "bytes32"}],
     "outputs": [{"name": "caller", "type": "address"}, {"name": "paidAt", "type": "uint256"},
                 {"name": "fulfilled", "type": "bool"}]},
    {"name": "getReceipt", "type": "function", "stateMutability": "view",
     "inputs": [{"name": "requestId", "type": "bytes32"}],
     "outputs": [{"components": [
         {"name": "contractHash", "type": "bytes32"}, {"name": "actionHash", "type": "bytes32"},
         {"name": "receiptHash", "type": "bytes32"}, {"name": "verdict", "type": "string"},
         {"name": "recordedAt", "type": "uint256"}], "name": "", "type": "tuple"}]},
    {"anonymous": False, "name": "VerificationRequested", "type": "event",
     "inputs": [{"indexed": True, "name": "requestId", "type": "bytes32"},
                {"indexed": True, "name": "caller", "type": "address"},
                {"indexed": False, "name": "contractHash", "type": "bytes32"},
                {"indexed": False, "name": "actionHash", "type": "bytes32"},
                {"indexed": False, "name": "fee", "type": "uint256"}]},
]

_ERC20_ABI = [
    {"name": "approve", "type": "function", "stateMutability": "nonpayable",
     "inputs": [{"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}],
     "outputs": [{"name": "", "type": "bool"}]},
    {"name": "allowance", "type": "function", "stateMutability": "view",
     "inputs": [{"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}],
     "outputs": [{"name": "", "type": "uint256"}]},
]

_GAS_HEADROOM = 20_000  # added on top of estimate_gas() — see PRODUCT.md changelog 2026-08-07:
# a hardcoded gas limit is what caused the first live confirmation test's recordReceipt() to run
# out of gas and revert (consuming exactly the limit). estimate_gas() + headroom is the fix;
# never go back to a fixed number here.


class VerifierError(Exception):
    """Raised for both HTTP-layer errors (bad request, payment not found, self-check refused)
    and on-chain failures (reverted tx) — callers catch one exception type either way."""


class VerifierClient:
    def __init__(self, private_key, *, rpc_url=DEFAULT_RPC_URL, api_url=DEFAULT_API_URL,
                 registry_address=DEFAULT_REGISTRY_ADDRESS, usdc_address=DEFAULT_USDC_ADDRESS,
                 chain_id=DEFAULT_CHAIN_ID):
        self.api_url = api_url.rstrip("/")
        self.chain_id = chain_id
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = Account.from_key(private_key)
        self.registry = self.w3.eth.contract(
            address=Web3.to_checksum_address(registry_address), abi=_REGISTRY_ABI)
        self.usdc = self.w3.eth.contract(
            address=Web3.to_checksum_address(usdc_address), abi=_ERC20_ABI)

    @property
    def address(self):
        return self.account.address

    # ── HTTP layer ────────────────────────────────────────────────────────────

    def _post(self, path, payload):
        # Explicit, identifiable UA — Cloudflare's WAF blocks the generic default
        # "Python-urllib/x.y" string outright (403) as a known-scripting signature.
        req = urllib.request.Request(
            f"{self.api_url}{path}", data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": _UA},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                detail = json.loads(body).get("error", body)
            except Exception:
                detail = body
            raise VerifierError(f"HTTP {e.code} from {path}: {detail}") from None

    def get_hashes(self, contract, proposed_action) -> dict:
        """POST /hash — the exact bytes to pay against. Always call this first; the hashes here
        are what requestVerification() commits on-chain, so a hash computed any other way risks
        not matching what /verify later expects."""
        return self._post("/hash", {"contract": contract, "proposed_action": proposed_action})

    # ── on-chain: pay ────────────────────────────────────────────────────────

    def _send(self, fn):
        nonce = self.w3.eth.get_transaction_count(self.address)
        gas = fn.estimate_gas({"from": self.address}) + _GAS_HEADROOM
        tx = fn.build_transaction({
            "from": self.address, "nonce": nonce, "gas": gas,
            "gasPrice": self.w3.eth.gas_price, "chainId": self.chain_id,
        })
        signed = Account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status != 1:
            raise VerifierError(f"transaction {tx_hash.hex()} reverted (gas estimate was {gas})")
        return receipt

    def ensure_usdc_allowance(self, min_amount=50_000):
        """One-time per wallet (or whenever the allowance runs low): approve the registry to pull
        USDC for the flat per-check fee. min_amount is in USDC base units (6 decimals) — the
        default covers one $0.05 check; pass a larger amount to avoid re-approving every call."""
        current = self.usdc.functions.allowance(self.address, self.registry.address).call()
        if current >= min_amount:
            return None
        return self._send(self.usdc.functions.approve(self.registry.address, min_amount))

    def request_verification(self, contract_hash_hex, action_hash_hex) -> str:
        """Pays the flat fee on-chain and returns the request_id to pass to verify(). Raises if
        the USDC allowance is insufficient — call ensure_usdc_allowance() first (check() does)."""
        fn = self.registry.functions.requestVerification(
            bytes.fromhex(contract_hash_hex.removeprefix("0x")),
            bytes.fromhex(action_hash_hex.removeprefix("0x")),
        )
        receipt = self._send(fn)
        events = self.registry.events.VerificationRequested().process_receipt(receipt)
        if not events:
            raise VerifierError("requestVerification() succeeded but emitted no event — unexpected")
        return "0x" + events[0]["args"]["requestId"].hex()

    # ── the check itself ─────────────────────────────────────────────────────

    def verify(self, request_id, contract, proposed_action, *, observed_inputs=None,
               granted_authorities=None, observed_facts=None, joined_records=None,
               policy_version=None, nonce=None) -> dict:
        """POST /verify. request_id must come from request_verification() above — the server
        checks on-chain that it was actually paid and matches this exact contract/action, not
        your say-so. Returns the full receipt; receipt["verdict"] is "PASS" or "REFUSE"."""
        payload = {"request_id": request_id, "contract": contract, "proposed_action": proposed_action}
        if observed_inputs is not None:
            payload["observed_inputs"] = observed_inputs
        if granted_authorities is not None:
            payload["granted_authorities"] = granted_authorities
        if observed_facts is not None:
            payload["observed_facts"] = observed_facts
        if joined_records is not None:
            payload["joined_records"] = joined_records
        if policy_version is not None:
            payload["policy_version"] = policy_version
        if nonce is not None:
            payload["nonce"] = nonce
        return self._post("/verify", payload)

    def reproduce(self, receipt, contract, proposed_action, **kwargs) -> dict:
        """POST /reproduce — third-party fraud-proof check. Recomputes the verdict from scratch
        and compares it against the receipt; returns {"matches": bool, "recomputed": {...}}.
        Anyone can call this, not just the original caller — that's the point."""
        payload = {"receipt": receipt, "contract": contract, "proposed_action": proposed_action, **kwargs}
        return self._post("/reproduce", payload)

    # ── on-chain: anchor the verdict ─────────────────────────────────────────

    def record_receipt(self, receipt) -> str:
        """Submits the signed verdict to recordReceipt(), anchoring it on Base permanently.
        Optional — the receipt returned by verify() is already valid and reproducible without
        this — but anchoring means an auditor can read the verdict straight off Basescan without
        needing to trust this SDK, this server, or the caller who ran the check. Any wallet can
        submit this (the contract allows any relayer), not just the one that paid.
        Returns the transaction hash."""
        onchain = receipt.get("onchain")
        if not onchain:
            err = receipt.get("onchain_error")
            raise VerifierError(
                "receipt has no onchain payload — either REQUIRE_PAYMENT is off on the server "
                f"(free rollout mode, nothing to anchor) or signing failed: {err}"
            )
        args = onchain["record_receipt_call"]["args"]
        fn = self.registry.functions.recordReceipt(
            bytes.fromhex(args["requestId"].removeprefix("0x")),
            bytes.fromhex(args["contractHash"].removeprefix("0x")),
            bytes.fromhex(args["actionHash"].removeprefix("0x")),
            bytes.fromhex(args["receiptHash"].removeprefix("0x")),
            args["verdict"],
            bytes.fromhex(args["nonce"].removeprefix("0x")),
            bytes.fromhex(args["sig"].removeprefix("0x")),
        )
        receipt_tx = self._send(fn)
        return receipt_tx.transactionHash.hex()


    # ── x402: pay by signing, no gas, no approval, no transaction ─────────────

    def _sign_x402(self, terms):
        """Sign an EIP-3009 transfer authorization for the quoted terms.

        This is the whole payment. Your wallet signs a message — it does not send a transaction,
        does not need ETH, and grants no allowance. The verifier submits the transfer and pays the
        gas out of the fee.
        """
        now = int(time.time())
        auth = {
            "from": self.address,
            "to": Web3.to_checksum_address(terms["payTo"]),
            "value": str(int(terms["maxAmountRequired"])),
            "validAfter": str(now - 60),
            "validBefore": str(now + 600),
            "nonce": "0x" + secrets.token_bytes(32).hex(),
        }
        eip = terms["eip712"]
        signable = encode_typed_data(
            domain_data=eip["domain"],
            message_types=eip["types"],
            message_data={
                "from": auth["from"], "to": auth["to"], "value": int(auth["value"]),
                "validAfter": int(auth["validAfter"]), "validBefore": int(auth["validBefore"]),
                "nonce": bytes.fromhex(auth["nonce"][2:]),
            },
        )
        sig = Account.sign_message(signable, private_key=self.account.key).signature.hex()
        payload = {"authorization": auth, "signature": sig}
        return base64.b64encode(json.dumps(payload).encode()).decode()

    def pay_and_verify(self, contract, proposed_action, **verify_kwargs):
        """Verify a claim, paying over x402. NO gas, NO allowance, NO transaction from you.

        Call it and it handles the 402 handshake: request -> quoted terms -> sign -> retry.
        Your wallet needs USDC on Base and nothing else — not even ETH.
        """
        payload = {"contract": contract, "proposed_action": proposed_action}
        payload.update({k: v for k, v in verify_kwargs.items() if v is not None})
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json", "User-Agent": _UA}

        req = urllib.request.Request(f"{self.api_url}/verify", data=body,
                                     headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())          # already paid / free rollout
        except urllib.error.HTTPError as e:
            if e.code != 402:
                detail = e.read().decode("utf-8", errors="replace")
                raise VerifierError(f"HTTP {e.code}: {detail}") from None
            terms_body = json.loads(e.read())

        accepts = (terms_body.get("accepts") or [None])[0]
        if not accepts:
            raise VerifierError("server asked for payment but quoted no terms")

        headers["X-PAYMENT"] = self._sign_x402(accepts)
        req = urllib.request.Request(f"{self.api_url}/verify", data=body,
                                     headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise VerifierError(f"payment rejected (HTTP {e.code}): {detail}") from None

    # ── the whole thing, one call ────────────────────────────────────────────

    def check(self, contract, proposed_action, *, anchor=False, rail="x402", **verify_kwargs) -> dict:
        """Verify a claim and pay for it. Returns the receipt; read receipt["verdict"].

        rail="x402" (default) pays by SIGNING — no gas, no allowance, no transaction from you, and
        the verdict is anchored on-chain for you out of the fee. Your wallet needs USDC on Base
        and nothing else.

        rail="onchain" is the older path: approve an allowance, pay via
        requestVerification(), then anchor yourself. It binds the claim on-chain at payment time,
        which some callers want, but it costs you three transactions and you must hold ETH.
        """
        if rail == "x402":
            return self.pay_and_verify(contract, proposed_action, **verify_kwargs)
        hashes = self.get_hashes(contract, proposed_action)
        self.ensure_usdc_allowance()
        request_id = self.request_verification(hashes["contract_hash"], hashes["action_hash"])
        receipt = self.verify(request_id, contract, proposed_action, **verify_kwargs)
        if anchor and receipt.get("onchain"):
            receipt["record_receipt_tx"] = self.record_receipt(receipt)
        return receipt
