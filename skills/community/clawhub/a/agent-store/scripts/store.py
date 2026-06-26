#!/usr/bin/env python3

from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

API_HOST = os.environ.get("API_HOST", "https://api.tkns.store")
AUTH_CHAIN_ID = 8453
BASE_MAINNET_RPC_URL = os.environ.get("X402_BASE_RPC_URL", "https://mainnet.base.org")
DELIVERY_TERMINAL_STATUSES = {"delivered", "failed", "dead_letter"}
DELIVERY_POLL_INTERVAL_SECONDS = 0.05
DELIVERY_POLL_MAX_ATTEMPTS = 20
PERMIT2_ADDRESS = "0x000000000022D473030F116dDEE9F6B43aC78BA3"
X402_PROXY_ADDRESS = "0x402085c248EeA27D92E8b30b2C58ed07f9E20001"
MASK_64 = (1 << 64) - 1
RATE_BYTES = 136
REDACTED = "[REDACTED]"
ROTATION_OFFSETS = (
    (0, 36, 3, 41, 18),
    (1, 44, 10, 45, 2),
    (62, 6, 43, 15, 61),
    (28, 55, 25, 21, 56),
    (27, 20, 39, 8, 14),
)
ROUND_CONSTANTS = (
    0x0000000000000001,
    0x0000000000008082,
    0x800000000000808A,
    0x8000000080008000,
    0x000000000000808B,
    0x0000000080000001,
    0x8000000080008081,
    0x8000000000008009,
    0x000000000000008A,
    0x0000000000000088,
    0x0000000080008009,
    0x000000008000000A,
    0x000000008000808B,
    0x800000000000008B,
    0x8000000000008089,
    0x8000000000008003,
    0x8000000000008002,
    0x8000000000000080,
    0x000000000000800A,
    0x800000008000000A,
    0x8000000080008081,
    0x8000000000008080,
    0x0000000080000001,
    0x8000000080008008,
)
SECRET_KEYS = {
  "api_key",
  "key",
  "password",
  "payment-signature",
  "sessiontoken",
    "session_token",
    "signature",
    "x-signature",
}
SUPPORTED_PRODUCT_TYPES = {"api_credits", "api_key", "vps_instance"}
DEFAULT_HTTP_HEADERS = {
    "accept": "application/json",
    "user-agent": "agent-store-skill/1.0",
}
KNOWN_PAYMENT_ASSETS_BY_ADDRESS = {
    "0x0000d0e38e9c6ba147b0098bb42007b942ef00a1": "awp",
    "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa": "awp",
    "0xfde4c96c8593536e31f229ea8f37b2ada2699bb2": "usdc",
    "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb": "usdc",
    "0xcccccccccccccccccccccccccccccccccccccccc": "usdt",
}
KNOWN_PAYMENT_ASSETS_BY_NAME = {
    "awp": "awp",
    "awp token": "awp",
    "usd coin": "usdc",
    "usdc": "usdc",
    "usdt": "usdt",
}


class PurchaseError(RuntimeError):
    pass


@dataclass
class WalletSession:
    address: str
    token: str


@dataclass
class JsonResponse:
    headers: dict[str, str]
    payload: dict[str, Any]
    status: int


class StepLogger:
    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log_path.write_text("", encoding="utf8")

    def info(self, step: str, message: str, payload: Any | None = None) -> None:
        self._write("INFO", step, message, payload)

    def error(self, step: str, message: str, payload: Any | None = None) -> None:
        self._write("ERROR", step, message, payload)

    def _write(
        self,
        level: str,
        step: str,
        message: str,
        payload: Any | None = None,
    ) -> None:
        timestamp = utc_now()
        line = f"{timestamp} [{level}] {step}: {message}"

        if payload is not None:
            line = f"{line} {json.dumps(redact(payload), sort_keys=True)}"

        with self._log_path.open("a", encoding="utf8") as handle:
            handle.write(f"{line}\n")

    def attempt_path(self) -> Path:
        return Path(f"{self._log_path}.attempt.json")


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}

        for key, item in value.items():
            normalized_key = key.lower()
            if normalized_key in SECRET_KEYS:
                redacted[key] = REDACTED
            else:
                redacted[key] = redact(item)

        return redacted

    if isinstance(value, list):
        return [redact(item) for item in value]

    return value


def rotate_left(value: int, shift: int) -> int:
    if shift == 0:
        return value & MASK_64

    return ((value << shift) | (value >> (64 - shift))) & MASK_64


def keccak_f1600(state: list[int]) -> None:
    for round_constant in ROUND_CONSTANTS:
        column_parity = [0] * 5
        for x in range(5):
            column_parity[x] = (
                state[x]
                ^ state[x + 5]
                ^ state[x + 10]
                ^ state[x + 15]
                ^ state[x + 20]
            )

        delta = [0] * 5
        for x in range(5):
            delta[x] = column_parity[(x - 1) % 5] ^ rotate_left(
                column_parity[(x + 1) % 5],
                1,
            )

        for x in range(5):
            for y in range(5):
                state[x + (5 * y)] ^= delta[x]

        temporary = [0] * 25
        for x in range(5):
            for y in range(5):
                temporary[y + (5 * (((2 * x) + (3 * y)) % 5))] = rotate_left(
                    state[x + (5 * y)],
                    ROTATION_OFFSETS[x][y],
                )

        for x in range(5):
            for y in range(5):
                state[x + (5 * y)] = (
                    temporary[x + (5 * y)]
                    ^ (
                        (~temporary[((x + 1) % 5) + (5 * y)])
                        & temporary[((x + 2) % 5) + (5 * y)]
                    )
                ) & MASK_64

        state[0] ^= round_constant


def keccak256_hex(payload: bytes) -> str:
    padded = bytearray(payload)
    padded.append(0x01)
    while len(padded) % RATE_BYTES != RATE_BYTES - 1:
        padded.append(0x00)
    padded.append(0x80)

    state = [0] * 25
    for offset in range(0, len(padded), RATE_BYTES):
        block = padded[offset : offset + RATE_BYTES]
        for lane_index in range(RATE_BYTES // 8):
            lane_bytes = block[lane_index * 8 : (lane_index + 1) * 8]
            state[lane_index] ^= int.from_bytes(lane_bytes, byteorder="little")
        keccak_f1600(state)

    squeezed = bytearray()
    for lane in state:
        squeezed.extend(lane.to_bytes(8, byteorder="little"))
        if len(squeezed) >= 32:
            break

    return f"0x{squeezed[:32].hex()}"


def encode_base64_json(value: dict[str, Any]) -> str:
    return base64.b64encode(
        json.dumps(value, separators=(",", ":")).encode("utf8"),
    ).decode("utf8")


def decode_base64_json(value: str) -> dict[str, Any]:
    decoded = base64.b64decode(value.encode("utf8")).decode("utf8")
    payload = json.loads(decoded)

    if not isinstance(payload, dict):
        raise PurchaseError("x402 header did not decode to a JSON object")

    return payload


def load_attempt_state(attempt_path: Path) -> dict[str, Any] | None:
    if not attempt_path.exists():
        return None

    try:
        loaded = json.loads(attempt_path.read_text(encoding="utf8"))
    except (OSError, json.JSONDecodeError):
        return None

    return loaded if isinstance(loaded, dict) else None


def persist_attempt_state(attempt_path: Path, state: dict[str, Any]) -> None:
    attempt_path.write_text(
        json.dumps(state, separators=(",", ":"), sort_keys=True),
        encoding="utf8",
    )


def resolve_attempt_idempotency_key(
    *,
    attempt_path: Path,
    logger: StepLogger,
    payment_asset: str,
    product_id: str,
    product_type: str,
    quantity: int,
    wallet_address: str,
) -> str:
    existing_state = load_attempt_state(attempt_path)
    if (
        isinstance(existing_state, dict)
        and existing_state.get("payment_asset") == payment_asset
        and existing_state.get("product_id") == product_id
        and existing_state.get("product_type") == product_type
        and existing_state.get("quantity") == quantity
        and existing_state.get("wallet_address") == wallet_address
        and isinstance(existing_state.get("idempotency_key"), str)
    ):
        logger.info("order", "reusing in-progress attempt state", existing_state)
        return str(existing_state["idempotency_key"])

    idempotency_key = f"idem-order-{uuid4()}"
    next_state = {
        "idempotency_key": idempotency_key,
        "payment_asset": payment_asset,
        "product_id": product_id,
        "product_type": product_type,
        "quantity": quantity,
        "wallet_address": wallet_address,
    }
    persist_attempt_state(attempt_path, next_state)
    logger.info("order", "stored in-progress attempt state", next_state)
    return idempotency_key


def clear_attempt_state(logger: StepLogger, attempt_path: Path, reason: str) -> None:
    if not attempt_path.exists():
        return

    attempt_path.unlink(missing_ok=True)
    logger.info("order", reason, {"attempt_path": str(attempt_path)})


def should_clear_attempt_state_on_error(message: str) -> bool:
    return any(
        token in message
        for token in (
            "terminal failure status",
            "terminal status",
            "order reached terminal status",
        )
    )


def resolve_product_payment_asset(product: dict[str, Any]) -> str:
    price_asset = product.get("price_asset")

    if not isinstance(price_asset, str) or not price_asset:
        raise PurchaseError("catalog product is missing price_asset")

    normalized_price_asset = price_asset.lower()

    if normalized_price_asset in {"awp", "usdc", "usdt"}:
        return normalized_price_asset

    raise PurchaseError("catalog product does not support a known x402 payment asset")


def run_wallet_command(arguments: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            ["awp-wallet", *arguments],
            capture_output=True,
            check=False,
            text=True,
        )
    except FileNotFoundError as error:
        raise PurchaseError("awp-wallet must be installed and on PATH") from error

    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()

    if completed.returncode != 0:
        detail = stderr or stdout or f"exit code {completed.returncode}"
        raise PurchaseError(
            f"awp-wallet {' '.join(arguments[:2] or arguments)} failed: {detail}",
        )

    if not stdout:
        return {}

    try:
        return json.loads(stdout)
    except json.JSONDecodeError as error:
        raise PurchaseError(
            f"awp-wallet {' '.join(arguments[:2] or arguments)} did not return JSON",
        ) from error


def ensure_wallet_available() -> None:
    if shutil.which("awp-wallet") is None:
        raise PurchaseError("awp-wallet must be installed and on PATH")


def extract_wallet_address(result: dict[str, Any]) -> str:
    return str(result.get("address") or result.get("eoaAddress") or "")


def ensure_wallet_session(logger: StepLogger) -> WalletSession:
    logger.info("wallet", "checking awp-wallet availability")
    ensure_wallet_available()

    address: str | None = None

    try:
        receive_result = run_wallet_command(["receive"])
        address = extract_wallet_address(receive_result)
        logger.info("wallet", "reused existing wallet", receive_result)
    except PurchaseError:
        logger.info("wallet", "creating new wallet")
        init_result = run_wallet_command(["init"])
        address = extract_wallet_address(init_result)
        logger.info("wallet", "created wallet", init_result)

    if not address:
        raise PurchaseError("awp-wallet did not provide a wallet address")

    unlock_result = run_wallet_command(["unlock", "--duration", "3600"])
    token = str(unlock_result.get("sessionToken") or "")

    if not token:
        raise PurchaseError("awp-wallet did not return a session token")

    logger.info("wallet", "unlocked wallet session", unlock_result)
    return WalletSession(address=address, token=token)


def lock_wallet_session(logger: StepLogger) -> None:
    try:
        result = run_wallet_command(["lock"])
        logger.info("wallet", "locked wallet session", result)
    except PurchaseError as error:
        logger.error("wallet", "failed to lock wallet session", {"error": str(error)})


def build_transport_url(path: str) -> str:
    return f"{API_HOST.rstrip('/')}{path}"


def uses_loopback_transport(url: str) -> bool:
    hostname = urllib.parse.urlparse(url).hostname
    return hostname in {"127.0.0.1", "::1", "localhost"}


def open_request(
    request: urllib.request.Request,
    *,
    timeout: float | None = None,
):
    if uses_loopback_transport(request.full_url):
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        if timeout is None:
            return opener.open(request)
        return opener.open(request, timeout=timeout)

    if timeout is None:
        return urllib.request.urlopen(request)

    return urllib.request.urlopen(request, timeout=timeout)


def build_agent_request_typed_data(
    *,
    wallet_address: str,
    method: str,
    path: str,
    body_text: str,
    timestamp: str,
) -> dict[str, Any]:
    return {
        "types": {
            "AgentRequest": [
                {"name": "wallet_address", "type": "string"},
                {"name": "method", "type": "string"},
                {"name": "path", "type": "string"},
                {"name": "body_hash", "type": "bytes32"},
                {"name": "timestamp", "type": "string"},
            ],
        },
        "primaryType": "AgentRequest",
        "domain": {
            "name": "Agent Store",
            "version": "1",
            "chainId": AUTH_CHAIN_ID,
        },
        "message": {
            "wallet_address": wallet_address,
            "method": method,
            "path": path,
            "body_hash": keccak256_hex(body_text.encode("utf8")),
            "timestamp": timestamp,
        },
    }


def sign_headers(
    *,
    wallet: WalletSession,
    method: str,
    path: str,
    body_text: str,
) -> dict[str, str]:
    timestamp = utc_now()
    typed_data = build_agent_request_typed_data(
        wallet_address=wallet.address,
        method=method,
        path=path,
        body_text=body_text,
        timestamp=timestamp,
    )
    signature_result = run_wallet_command(
        [
            "sign-typed-data",
            "--token",
            wallet.token,
            "--data",
            json.dumps(typed_data, separators=(",", ":")),
        ],
    )
    signature = str(signature_result.get("signature") or "")

    if not signature:
        raise PurchaseError("awp-wallet did not return a signature")

    return {
        "x-signature": signature,
        "x-timestamp": timestamp,
        "x-wallet-address": wallet.address,
    }


def request_json_response(
    *,
    logger: StepLogger,
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    extra_headers: dict[str, str] | None = None,
    allowed_statuses: set[int] | None = None,
    wallet: WalletSession | None = None,
    step: str,
) -> JsonResponse:
    body_text = (
        json.dumps(body, separators=(",", ":")) if body is not None else ""
    )
    headers: dict[str, str] = {}
    headers.update(DEFAULT_HTTP_HEADERS)

    if body_text:
        headers["content-type"] = "application/json"

    if wallet is not None:
        headers.update(
            sign_headers(
                wallet=wallet,
                method=method,
                path=path,
                body_text=body_text,
            ),
        )

    if extra_headers is not None:
        headers.update(extra_headers)

    request = urllib.request.Request(
        build_transport_url(path),
        data=body_text.encode("utf8") if body is not None else None,
        headers=headers,
        method=method,
    )

    logger.info(
        step,
        f"request {method} {path}",
        {
            "body": body,
            "headers": headers,
        },
    )

    try:
        with open_request(request, timeout=30) as response:
            response_text = response.read().decode("utf8")
            status = response.status
            response_headers = {
                key.lower(): value for key, value in response.headers.items()
            }
    except urllib.error.HTTPError as error:
        response_text = error.read().decode("utf8")
        status = error.code
        response_headers = {
            key.lower(): value for key, value in error.headers.items()
        }
        if allowed_statuses is None or status not in allowed_statuses:
            logger.error(
                step,
                f"http {method} {path} failed",
                {
                    "response_body": try_parse_json(response_text),
                    "status": status,
                },
            )
            raise PurchaseError(f"{method} {path} failed with status {status}") from error
    except urllib.error.URLError as error:
        raise PurchaseError(f"{method} {path} failed: {error.reason}") from error

    payload = try_parse_json(response_text)
    if not isinstance(payload, dict):
        raise PurchaseError(f"{method} {path} did not return a JSON object")

    logger.info(
        step,
        f"response {method} {path}",
        {
            "headers": response_headers,
            "payload": payload,
            "status": status,
        },
    )
    return JsonResponse(headers=response_headers, payload=payload, status=status)


def request_json(
    *,
    logger: StepLogger,
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    wallet: WalletSession | None = None,
    step: str,
) -> dict[str, Any]:
    return request_json_response(
        logger=logger,
        method=method,
        path=path,
        body=body,
        wallet=wallet,
        step=step,
    ).payload


def try_parse_json(text: str) -> Any:
    if not text:
        return {}

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def resolve_payment_asset(requirement: dict[str, Any]) -> str:
    extra = requirement.get("extra")
    if isinstance(extra, dict):
        name = str(extra.get("name") or "").lower()
        if name in KNOWN_PAYMENT_ASSETS_BY_NAME:
            return KNOWN_PAYMENT_ASSETS_BY_NAME[name]

    asset_address = str(requirement.get("asset") or "").lower()
    if asset_address in KNOWN_PAYMENT_ASSETS_BY_ADDRESS:
        return KNOWN_PAYMENT_ASSETS_BY_ADDRESS[asset_address]

    raise PurchaseError("x402 payment requirement uses an unsupported asset")


def resolve_payment_extension(
    payment_required: dict[str, Any],
    extension_name: str,
) -> dict[str, Any] | None:
    extensions = payment_required.get("extensions")

    if not isinstance(extensions, dict):
        return None

    extension = extensions.get(extension_name)
    return extension if isinstance(extension, dict) else None


def choose_x402_requirement(payment_required: dict[str, Any]) -> tuple[dict[str, Any], str]:
    accepts = payment_required.get("accepts")
    if not isinstance(accepts, list) or not accepts:
        raise PurchaseError("PAYMENT-REQUIRED does not include accepted payment options")

    options: list[tuple[str, dict[str, Any]]] = []
    for requirement in accepts:
        if isinstance(requirement, dict):
            options.append((resolve_payment_asset(requirement), requirement))

    for preferred_asset in ("awp", "usdc", "usdt"):
        for asset, requirement in options:
            if asset == preferred_asset:
                return requirement, asset

    raise PurchaseError("PAYMENT-REQUIRED did not expose a supported payment asset")


def extract_chain_id(requirement: dict[str, Any]) -> int:
    network = str(requirement.get("network") or "")
    parts = network.split(":", 1)

    if len(parts) != 2 or not parts[1].isdigit():
        raise PurchaseError("x402 payment requirement network is invalid")

    return int(parts[1])


def resolve_rpc_url_for_network(network: str, extension: dict[str, Any] | None) -> str:
    extension_rpc_url = extension.get("rpcUrl") if extension else None
    if isinstance(extension_rpc_url, str) and extension_rpc_url:
        return extension_rpc_url

    if network == "eip155:8453":
        return BASE_MAINNET_RPC_URL

    raise PurchaseError(f"x402 payment requirement network is unsupported: {network}")


def rpc_json(
    *,
    logger: StepLogger,
    rpc_url: str,
    method: str,
    params: list[Any],
) -> Any:
    request_body = json.dumps(
        {
            "id": 1,
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
        },
        separators=(",", ":"),
    ).encode("utf8")
    request = urllib.request.Request(
        rpc_url,
        data=request_body,
        headers={
            **DEFAULT_HTTP_HEADERS,
            "content-type": "application/json",
        },
        method="POST",
    )

    try:
        with open_request(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf8", errors="replace")
        raise PurchaseError(f"x402 rpc request failed: {detail or error.reason}") from error
    except urllib.error.URLError as error:
        raise PurchaseError(f"x402 rpc request failed: {error.reason}") from error

    if not isinstance(payload, dict):
        raise PurchaseError("x402 rpc response was not a JSON object")

    if payload.get("error"):
        raise PurchaseError(f"x402 rpc response returned an error: {payload['error']}")

    logger.info("x402", "fetched rpc payload", {"method": method, "rpc_url": rpc_url})
    return payload.get("result")


def fetch_eip2612_nonce(
    *,
    logger: StepLogger,
    requirement: dict[str, Any],
    owner: str,
    extension: dict[str, Any] | None,
) -> str:
    asset = str(requirement.get("asset") or "")
    network = str(requirement.get("network") or "")

    if not asset:
        raise PurchaseError("x402 payment requirement is missing asset for EIP-2612")

    selector = keccak256_hex(b"nonces(address)")[2:10]
    owner_hex = owner.lower().removeprefix("0x")
    if len(owner_hex) != 40:
        raise PurchaseError("wallet address is invalid for EIP-2612 nonce lookup")

    call_data = f"0x{selector}{owner_hex.rjust(64, '0')}"
    rpc_url = resolve_rpc_url_for_network(network, extension)
    result = rpc_json(
        logger=logger,
        rpc_url=rpc_url,
        method="eth_call",
        params=[
            {
                "data": call_data,
                "to": asset,
            },
            "latest",
        ],
    )

    if not isinstance(result, str) or not result.startswith("0x"):
        raise PurchaseError("x402 rpc nonce response was not a hex string")

    return str(int(result, 16))


def ensure_permit2_allowance(
    *,
    logger: StepLogger,
    wallet: WalletSession,
    requirement: dict[str, Any],
) -> None:
    amount = str(requirement.get("amount") or "")
    asset = str(requirement.get("asset") or "")

    if not amount or not asset:
        raise PurchaseError("x402 payment requirement is missing amount or asset")

    allowance_result = run_wallet_command(
        [
            "allowances",
            "--token",
            wallet.token,
            "--asset",
            asset,
            "--spender",
            PERMIT2_ADDRESS,
        ],
    )
    logger.info("x402", "checked permit2 allowance", allowance_result)

    allowance_value = str(allowance_result.get("allowance") or "0")
    if int(allowance_value) >= int(amount):
        return

    approval_result = run_wallet_command(
        [
            "approve",
            "--token",
            wallet.token,
            "--asset",
            asset,
            "--spender",
            PERMIT2_ADDRESS,
            "--amount",
            amount,
            "--mode",
            "direct",
        ],
    )
    logger.info("x402", "approved permit2 allowance", approval_result)


def build_permit2_typed_data(
    *,
    requirement: dict[str, Any],
    wallet_address: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    chain_id = extract_chain_id(requirement)
    now = int(time.time())
    deadline = str(now + int(requirement.get("maxTimeoutSeconds") or 300))
    nonce = str(uuid4().int)
    permit2_authorization = {
        "deadline": deadline,
        "from": wallet_address,
        "nonce": nonce,
        "permitted": {
            "amount": str(requirement.get("amount") or ""),
            "token": str(requirement.get("asset") or ""),
        },
        "spender": X402_PROXY_ADDRESS,
        "witness": {
            "to": str(requirement.get("payTo") or ""),
            "validAfter": str(now - 600),
        },
    }

    typed_data = {
        "types": {
            "PermitWitnessTransferFrom": [
                {"name": "permitted", "type": "TokenPermissions"},
                {"name": "spender", "type": "address"},
                {"name": "nonce", "type": "uint256"},
                {"name": "deadline", "type": "uint256"},
                {"name": "witness", "type": "Witness"},
            ],
            "TokenPermissions": [
                {"name": "token", "type": "address"},
                {"name": "amount", "type": "uint256"},
            ],
            "Witness": [
                {"name": "to", "type": "address"},
                {"name": "validAfter", "type": "uint256"},
            ],
        },
        "primaryType": "PermitWitnessTransferFrom",
        "domain": {
            "name": "Permit2",
            "chainId": chain_id,
            "verifyingContract": PERMIT2_ADDRESS,
        },
        "message": {
            "permitted": permit2_authorization["permitted"],
            "spender": permit2_authorization["spender"],
            "nonce": permit2_authorization["nonce"],
            "deadline": permit2_authorization["deadline"],
            "witness": permit2_authorization["witness"],
        },
    }

    return typed_data, permit2_authorization


def build_eip2612_typed_data(
    *,
    requirement: dict[str, Any],
    spender: str,
    wallet_address: str,
    nonce: str,
    deadline: str,
) -> dict[str, Any]:
    extra = requirement.get("extra")
    if not isinstance(extra, dict):
        raise PurchaseError("x402 payment requirement is missing EIP-2612 metadata")

    name = str(extra.get("name") or "")
    version = str(extra.get("version") or "")
    asset = str(requirement.get("asset") or "")
    if not name or not version or not asset:
        raise PurchaseError("x402 payment requirement is missing EIP-2612 domain fields")

    return {
        "types": {
            "Permit": [
                {"name": "owner", "type": "address"},
                {"name": "spender", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "nonce", "type": "uint256"},
                {"name": "deadline", "type": "uint256"},
            ],
        },
        "primaryType": "Permit",
        "domain": {
            "name": name,
            "version": version,
            "chainId": extract_chain_id(requirement),
            "verifyingContract": asset,
        },
        "message": {
            "owner": wallet_address,
            "spender": spender,
            "value": str(requirement.get("amount") or ""),
            "nonce": nonce,
            "deadline": deadline,
        },
    }


def build_payment_signature_header(
    *,
    logger: StepLogger,
    payment_required: dict[str, Any],
    wallet: WalletSession,
) -> tuple[str, str]:
    requirement, payment_asset = choose_x402_requirement(payment_required)
    eip2612_extension = resolve_payment_extension(
        payment_required,
        "eip2612GasSponsoring",
    )
    if eip2612_extension is None:
        ensure_permit2_allowance(
            logger=logger,
            wallet=wallet,
            requirement=requirement,
        )
    typed_data, permit2_authorization = build_permit2_typed_data(
        requirement=requirement,
        wallet_address=wallet.address,
    )
    signature_result = run_wallet_command(
        [
            "sign-typed-data",
            "--token",
            wallet.token,
            "--data",
            json.dumps(typed_data, separators=(",", ":")),
        ],
    )
    signature = str(signature_result.get("signature") or "")
    if not signature:
        raise PurchaseError("awp-wallet did not return an x402 payment signature")

    payment_payload = {
        "accepted": requirement,
        "payload": {
            "permit2Authorization": permit2_authorization,
            "signature": signature,
        },
        "resource": payment_required.get("resource"),
        "x402Version": int(payment_required.get("x402Version") or 2),
    }
    if eip2612_extension is not None:
        spender = str(eip2612_extension.get("spender") or PERMIT2_ADDRESS)
        permit_deadline = str(permit2_authorization.get("deadline") or "")
        permit_nonce = fetch_eip2612_nonce(
            logger=logger,
            requirement=requirement,
            owner=wallet.address,
            extension=eip2612_extension,
        )
        permit_typed_data = build_eip2612_typed_data(
            requirement=requirement,
            spender=spender,
            wallet_address=wallet.address,
            nonce=permit_nonce,
            deadline=permit_deadline,
        )
        permit_signature_result = run_wallet_command(
            [
                "sign-typed-data",
                "--token",
                wallet.token,
                "--data",
                json.dumps(permit_typed_data, separators=(",", ":")),
            ],
        )
        permit_signature = str(permit_signature_result.get("signature") or "")
        if not permit_signature:
            raise PurchaseError("awp-wallet did not return an x402 permit signature")

        payment_payload["extensions"] = {
            "eip2612GasSponsoring": {
                "info": {
                    "amount": str(requirement.get("amount") or ""),
                    "asset": str(requirement.get("asset") or ""),
                    "deadline": permit_deadline,
                    "from": wallet.address,
                    "nonce": permit_nonce,
                    "signature": permit_signature,
                    "spender": spender,
                    "version": "1",
                },
            },
        }
    logger.info(
        "x402",
        "created payment payload for retry",
        {
            "payment_asset": payment_asset,
            "payment_payload": payment_payload,
        },
    )

    return encode_base64_json(payment_payload), payment_asset

def poll_delivery(
    *,
    logger: StepLogger,
    order_id: str,
    wallet: WalletSession,
) -> dict[str, Any]:
    for attempt in range(1, DELIVERY_POLL_MAX_ATTEMPTS + 1):
        delivery_response = request_json_response(
            logger=logger,
            method="GET",
            path=f"/orders/{order_id}/delivery",
            allowed_statuses={404},
            wallet=wallet,
            step="delivery",
        )

        if delivery_response.status == 404:
            error_code = str(delivery_response.payload.get("code") or "")
            if error_code == "order_not_found":
                logger.info(
                    "delivery",
                    f"delivery polling waiting for delivery record on attempt {attempt}",
                    delivery_response.payload,
                )
                time.sleep(DELIVERY_POLL_INTERVAL_SECONDS)
                continue

            raise PurchaseError(
                f"delivery lookup returned an unexpected 404: {error_code or 'unknown_error'}",
            )

        delivery = delivery_response.payload
        delivery_status = str(delivery.get("delivery_status") or "")
        if delivery_status == "delivered":
            logger.info(
                "delivery",
                f"delivery polling completed on attempt {attempt}",
                delivery,
            )
            return delivery

        if delivery_status in DELIVERY_TERMINAL_STATUSES:
            raise PurchaseError(f"delivery reached terminal failure status: {delivery_status}")

        time.sleep(DELIVERY_POLL_INTERVAL_SECONDS)

    raise PurchaseError("timed out waiting for delivered order delivery")


def run(product_type: str, logger: StepLogger) -> dict[str, Any]:
    if product_type not in SUPPORTED_PRODUCT_TYPES:
        raise PurchaseError(
            f"product_type must be one of {sorted(SUPPORTED_PRODUCT_TYPES)}",
        )

    wallet: WalletSession | None = None

    try:
        wallet = ensure_wallet_session(logger)
        catalog_path = (
            "/catalog/products?"
            + urllib.parse.urlencode(
                {
                    "product_type": product_type,
                },
            )
        )
        catalog_response = request_json(
            logger=logger,
            method="GET",
            path=catalog_path,
            step="catalog",
        )
        products = catalog_response.get("products")

        if not isinstance(products, list) or not products:
            raise PurchaseError(f"no active product found for product_type={product_type}")

        product = products[0]
        if not isinstance(product, dict):
            raise PurchaseError("catalog response did not return a valid product object")

        logger.info(
            "catalog",
            "selected first matching product",
            {
                "product": product,
            },
        )

        payment_asset = resolve_product_payment_asset(product)
        attempt_path = logger.attempt_path()
        order_request = {
            "idempotency_key": resolve_attempt_idempotency_key(
                attempt_path=attempt_path,
                logger=logger,
                payment_asset=payment_asset,
                product_id=str(product.get("product_id") or ""),
                product_type=product_type,
                quantity=1,
                wallet_address=wallet.address,
            ),
            "payment_asset": payment_asset,
            "product_id": str(product.get("product_id") or ""),
            "quantity": 1,
        }
        if not order_request["product_id"]:
            raise PurchaseError("catalog product is missing product_id")

        order_response = request_json_response(
            logger=logger,
            method="POST",
            path="/orders",
            body=order_request,
            allowed_statuses={402},
            wallet=wallet,
            step="order",
        )
        if order_response.status != 402:
            raise PurchaseError("POST /orders did not return PAYMENT-REQUIRED")

        payment_required_header = order_response.headers.get("payment-required")
        if not payment_required_header:
            raise PurchaseError("PAYMENT-REQUIRED header is missing from the order response")

        payment_required = decode_base64_json(payment_required_header)
        logger.info("x402", "received payment requirements", payment_required)
        payment_signature_header, payment_asset = build_payment_signature_header(
            logger=logger,
            payment_required=payment_required,
            wallet=wallet,
        )
        paid_order_response = request_json_response(
            logger=logger,
            method="POST",
            path="/orders",
            body=order_request,
            extra_headers={"PAYMENT-SIGNATURE": payment_signature_header},
            wallet=wallet,
            step="x402",
        )
        settlement_header = paid_order_response.headers.get("payment-response")
        if not settlement_header:
            raise PurchaseError("PAYMENT-RESPONSE header is missing from the paid order response")

        settlement_response = decode_base64_json(settlement_header)
        logger.info(
            "x402",
            "received payment settlement response",
            {
                "payment_asset": payment_asset,
                "settlement": settlement_response,
            },
        )
        order = paid_order_response.payload
        order_id = str(order.get("order_id") or "")
        if not order_id:
            raise PurchaseError("order response is missing order_id")

        delivery = poll_delivery(logger=logger, order_id=order_id, wallet=wallet)
        logger.info("delivery", "completed purchase flow", delivery)
        clear_attempt_state(
            logger,
            attempt_path,
            "cleared in-progress attempt state after successful delivery",
        )
        return delivery
    except PurchaseError as error:
        if "attempt_path" in locals() and should_clear_attempt_state_on_error(str(error)):
            clear_attempt_state(
                logger,
                attempt_path,
                "cleared in-progress attempt state after terminal failure",
            )
        raise
    finally:
        if wallet is not None:
            lock_wallet_session(logger)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: python3 apps/agent-store-skill/scripts/store.py <product_type> <log_file>",
            file=sys.stderr,
        )
        return 1

    product_type = argv[1]
    log_path = Path(argv[2]).expanduser()
    logger = StepLogger(log_path)

    try:
        delivery = run(product_type, logger)
    except PurchaseError as error:
        logger.error("purchase", str(error))
        print(str(error), file=sys.stderr)
        return 1

    print(json.dumps(delivery, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
