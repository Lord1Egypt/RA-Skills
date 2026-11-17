#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["beam-network-sdk[s3,r2]>=0.13.3,<0.14"]
# ///
"""Check the API key, and estimate, run, inspect and cancel Beam transfers for an agent.

Every stdout line is one JSON object with an "event" field. Diagnostics go to
stderr. Storage credentials are read from environment variables, signed
locally by the Beam SDK, and never printed.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import posixpath
import re
import signal
import sys
from dataclasses import dataclass, field
from typing import Any, NoReturn
from urllib.parse import parse_qs, urlsplit

import httpx
from beam_network_sdk import (
    BEAM_PROD_URL,
    BeamAPIError,
    BeamAuthError,
    BeamProviderTransferError,
    BeamRouteRecoveryPendingError,
    BeamSDK,
    BeamStorageAccessError,
    BeamTimeoutError,
    BeamTransferFailedError,
    HippiusProviderDestination,
    HippiusProviderSource,
    HuggingFaceProviderDestination,
    HuggingFaceProviderSource,
    R2ProviderDestination,
    R2ProviderSource,
    S3CompatibleProviderDestination,
    S3CompatibleProviderSource,
    S3ProviderDestination,
    S3ProviderSource,
    prepare_provider_source_for_plan,
)
from pydantic import ValidationError

API_URL = "https://beamcore.b1m.ai"
BYTES_PER_GB = 1_000_000_000

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_TIMEOUT = 3
EXIT_AUTH = 4
EXIT_INTERRUPTED = 130

UNSUPPORTED_SCHEMES = {
    "gs": "Google Cloud Storage is not supported as a Beam transfer endpoint.",
    "gcs": "Google Cloud Storage is not supported as a Beam transfer endpoint.",
    "azure": "Azure Blob Storage is not supported as a Beam transfer endpoint.",
    "http": "HTTP endpoints need the SDK's HTTP connector (https://docs.b1m.ai/docs/connectors/http).",
    "https": "HTTP endpoints need the SDK's HTTP connector (https://docs.b1m.ai/docs/connectors/http).",
}

HF_TYPE_PREFIXES = {
    "models": "model",
    "datasets": "dataset",
    "spaces": "space",
    "kernels": "kernel",
}
HF_SPECIAL_REVISION = re.compile(r"^refs/(?:convert/[\w.-]+|pr/\d+)")
ENV_PREFIX = re.compile(r"^[A-Z][A-Z0-9_]*$")


class UsageError(Exception):
    def __init__(self, kind: str, message: str, **details: Any):
        super().__init__(message)
        self.kind = kind
        self.details = details


def emit(event: str, **fields: Any) -> None:
    print(json.dumps({"event": event, **fields}), flush=True)


def fail(kind: str, message: str, code: int, **details: Any) -> int:
    emit("error", kind=kind, message=message, **details)
    return code


@dataclass
class Endpoint:
    uri: str
    scheme: str
    prefix: str
    bucket: str = ""
    key: str = ""
    hf_repo_type: str = "model"
    hf_repo_id: str = ""
    hf_revision: str = "main"
    credentials: list[str] = field(default_factory=list)

    @property
    def basename(self) -> str:
        return posixpath.basename(self.key.rstrip("/"))

    @property
    def location(self) -> str:
        if self.scheme == "hf":
            kind = "" if self.hf_repo_type == "model" else f"{self.hf_repo_type}s/"
            return f"hf://{kind}{self.hf_repo_id}@{self.hf_revision}/{self.key}"
        return f"{self.scheme}://{self.bucket}/{self.key}"

    def env(self, name: str, *, required: bool = True) -> str | None:
        variable = f"{self.prefix}{name}"
        value = os.environ.get(variable, "").strip()
        if value:
            self.credentials.append(variable)
            return value
        if required:
            raise UsageError(
                "missing_env",
                f"{variable} is not set; it is required for {self.scheme}:// endpoints.",
                variable=variable,
                endpoint=self.uri,
            )
        return None


def parse_endpoint(raw: str) -> Endpoint:
    parts = urlsplit(raw)
    scheme = parts.scheme.lower()
    if scheme in UNSUPPORTED_SCHEMES:
        raise UsageError("unsupported_scheme", UNSUPPORTED_SCHEMES[scheme], endpoint=raw)
    if scheme not in {"s3", "r2", "s3c", "hippius", "hf"}:
        raise UsageError(
            "unsupported_scheme",
            "Use s3://, r2://, s3c://, hippius:// or hf:// URIs.",
            endpoint=raw,
        )
    query = parse_qs(parts.query, keep_blank_values=True)
    unknown = sorted(set(query) - {"env"})
    if unknown or parts.fragment:
        raise UsageError(
            "invalid_uri", "The only supported URI option is ?env=PREFIX.", endpoint=raw
        )
    prefix = ""
    if "env" in query:
        value = query["env"][0].strip().upper()
        if not ENV_PREFIX.match(value):
            raise UsageError(
                "invalid_uri", "?env= takes a prefix such as SRC or DST.", endpoint=raw
            )
        prefix = f"{value}_"
    display = raw.split("?", 1)[0]
    if scheme == "hf":
        return parse_hf(display, prefix)
    bucket, _, key = f"{parts.netloc}{parts.path}".partition("/")
    if not bucket:
        raise UsageError("invalid_uri", f"{display} names no bucket.", endpoint=raw)
    return Endpoint(uri=display, scheme=scheme, prefix=prefix, bucket=bucket, key=key)


def parse_hf(uri: str, prefix: str) -> Endpoint:
    """Parse hf://[<type>/]<org>/<repo>[@<revision>]/<path>."""
    rest = uri[len("hf://") :]
    repo_type = "model"
    head = rest.split("/", 1)
    if len(head) == 2 and head[0] in HF_TYPE_PREFIXES:
        repo_type = HF_TYPE_PREFIXES[head[0]]
        rest = head[1]
    revision = "main"
    if "@" in rest:
        repo_id, remainder = rest.split("@", 1)
        special = HF_SPECIAL_REVISION.match(remainder)
        if special:
            revision = special.group(0)
            path = remainder[len(revision) :].lstrip("/")
        else:
            revision, _, path = remainder.partition("/")
    else:
        segments = rest.split("/")
        repo_id, path = "/".join(segments[:2]), "/".join(segments[2:])
    if repo_id.count("/") != 1 or not all(repo_id.split("/")):
        raise UsageError("invalid_uri", f"{uri} must name the repo as <org>/<repo>.", endpoint=uri)
    return Endpoint(
        uri=uri,
        scheme="hf",
        prefix=prefix,
        key=path,
        hf_repo_type=repo_type,
        hf_repo_id=repo_id,
        hf_revision=revision,
    )


def source_model(endpoint: Endpoint) -> Any:
    if not endpoint.key or endpoint.key.endswith("/"):
        raise UsageError(
            "invalid_uri", f"Source {endpoint.uri} must name one object.", endpoint=endpoint.uri
        )
    return build_model(endpoint, source=True, hf_options={})


def destination_model(endpoint: Endpoint, source: Endpoint, hf_options: dict[str, Any]) -> Any:
    if not endpoint.key or endpoint.key.endswith("/"):
        endpoint.key = f"{endpoint.key}{source.basename}"
    return build_model(endpoint, source=False, hf_options=hf_options)


def build_model(endpoint: Endpoint, *, source: bool, hf_options: dict[str, Any]) -> Any:
    e = endpoint.env
    if endpoint.scheme == "s3":
        model = S3ProviderSource if source else S3ProviderDestination
        return model(
            bucket=endpoint.bucket,
            key=endpoint.key,
            region=e("AWS_DEFAULT_REGION", required=False) or "us-east-1",
            access_key_id=e("AWS_ACCESS_KEY_ID"),
            secret_access_key=e("AWS_SECRET_ACCESS_KEY"),
            session_token=e("AWS_SESSION_TOKEN", required=False),
        )
    if endpoint.scheme == "r2":
        model = R2ProviderSource if source else R2ProviderDestination
        access_key_id = e("R2_ACCESS_KEY_ID")
        secret_access_key = e("R2_SECRET_ACCESS_KEY")
        endpoint_url = e("R2_ENDPOINT_URL", required=False)
        account_id = e("R2_ACCOUNT_ID", required=endpoint_url is None)
        return model(
            bucket=endpoint.bucket,
            key=endpoint.key,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            account_id=account_id,
            endpoint_url=endpoint_url,
        )
    if endpoint.scheme == "s3c":
        model = S3CompatibleProviderSource if source else S3CompatibleProviderDestination
        return model(
            provider=e("S3_PROVIDER", required=False) or "s3-compatible",
            endpoint_url=e("S3_ENDPOINT_URL"),
            region=e("S3_REGION", required=False),
            bucket=endpoint.bucket,
            key=endpoint.key,
            access_key_id=e("S3_ACCESS_KEY_ID"),
            secret_access_key=e("S3_SECRET_ACCESS_KEY"),
        )
    if endpoint.scheme == "hippius":
        model = HippiusProviderSource if source else HippiusProviderDestination
        return model(
            bucket=endpoint.bucket,
            key=endpoint.key,
            api_token=e("HIPPIUS_API_TOKEN"),
            base_url=e("HIPPIUS_BASE_URL", required=False) or "https://api.hippius.com",
        )
    hf = {
        "repo_id": endpoint.hf_repo_id,
        "path": endpoint.key,
        "repo_type": endpoint.hf_repo_type,
        "revision": endpoint.hf_revision,
        "token": e("HF_TOKEN"),
        "endpoint": e("HF_ENDPOINT", required=False) or "https://huggingface.co",
    }
    if source:
        return HuggingFaceProviderSource(**hf)
    return HuggingFaceProviderDestination(**hf, **hf_options)


@dataclass
class TransferSpec:
    source: Endpoint
    destinations: list[Endpoint]
    source_model: Any
    destination_models: list[Any]

    def describe(self) -> dict[str, Any]:
        def entry(endpoint: Endpoint) -> dict[str, Any]:
            return {"uri": endpoint.location, "env": sorted(set(endpoint.credentials))}

        return {
            "source": entry(self.source),
            "destinations": [entry(destination) for destination in self.destinations],
        }


def build_spec(args: argparse.Namespace) -> TransferSpec:
    source = parse_endpoint(args.source)
    destinations = [parse_endpoint(raw) for raw in args.dest]
    hf_options = {
        "commit_message": getattr(args, "hf_commit_message", None),
        "create_pr": getattr(args, "hf_create_pr", False),
        "allow_source_rehash": getattr(args, "hf_allow_source_rehash", False),
    }
    try:
        source_config = source_model(source)
        destination_configs = [
            destination_model(destination, source, hf_options) for destination in destinations
        ]
    except ValidationError as exc:
        problems = "; ".join(
            f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
            for error in exc.errors()
        )
        raise UsageError("invalid_endpoint", problems) from None
    if len({d.location for d in destinations}) != len(destinations):
        raise UsageError("duplicate_destination", "Each --dest must be a different object.")
    return TransferSpec(source, destinations, source_config, destination_configs)


def estimated_credits(delivered_bytes: int) -> float:
    """0.01 credit per decimal GB delivered, rounded up per transfer to 0.01 credit."""
    return -(-delivered_bytes // BYTES_PER_GB) / 100


def require_api_key() -> str:
    api_key = os.environ.get("BEAM_API_KEY", "").strip()
    if not api_key:
        raise UsageError("missing_env", "BEAM_API_KEY is not set.", variable="BEAM_API_KEY")
    return api_key


def beam_client(api_key: str) -> BeamSDK:
    return BeamSDK(api_key=api_key, nats_url=BEAM_PROD_URL, environment="prod")


def cmd_estimate(args: argparse.Namespace) -> int:
    spec = build_spec(args)
    try:
        planned = prepare_provider_source_for_plan(spec.source_model)
    except Exception as exc:  # noqa: BLE001
        return fail(
            "source_unreadable",
            f"Could not read the source object's size: {type(exc).__name__}: {exc}",
            EXIT_FAILED,
            source=spec.source.uri,
        )
    delivered = planned.size * len(spec.destinations)
    credits = estimated_credits(delivered)
    emit(
        "estimate",
        **spec.describe(),
        size_bytes=planned.size,
        delivered_bytes=delivered,
        estimated_credits=credits,
        estimated_usd=round(credits * 0.5, 3),
        note="Estimate only: 0.01 credit per GB delivered; the Console shows the actual charge.",
    )
    return EXIT_OK


async def fetch_transfer(
    client: httpx.AsyncClient, api_key: str, transfer_id: str
) -> httpx.Response:
    return await client.get(
        f"{API_URL}/transfers/{transfer_id}", headers={"X-Api-Key": api_key}, timeout=20.0
    )


async def report_progress(api_key: str, transfer_id: str, interval: float) -> None:
    last: tuple[Any, Any] | None = None
    async with httpx.AsyncClient() as client:
        while True:
            await asyncio.sleep(interval)
            try:
                response = await fetch_transfer(client, api_key, transfer_id)
            except httpx.HTTPError as exc:
                print(f"progress check failed: {type(exc).__name__}", file=sys.stderr)
                continue
            if response.status_code != 200:
                continue
            transfer = response.json()
            current = (transfer.get("status"), transfer.get("bytes_transferred"))
            if current == last:
                continue
            last = current
            total = transfer.get("total_bytes") or 0
            done = transfer.get("bytes_transferred") or 0
            emit(
                "progress",
                transfer_id=transfer_id,
                status=transfer.get("status"),
                bytes_transferred=done,
                total_bytes=total,
                percent=round(100 * done / total, 1) if total else None,
            )


async def cmd_run(args: argparse.Namespace) -> int:
    spec = build_spec(args)
    if args.dry_run:
        emit("plan", **spec.describe(), name=args.name, timeout_seconds=args.timeout)
        return EXIT_OK
    api_key = require_api_key()
    transfer_id = ""
    async with beam_client(api_key) as beam:
        try:
            try:
                prepared = await beam.transfers.create_transfer(
                    sources=[spec.source_model],
                    destinations=spec.destination_models,
                    name=args.name,
                )
            except BeamRouteRecoveryPendingError as exc:
                transfer_id = exc.transfer_id
                emit("created", transfer_id=transfer_id, recovering=True, **spec.describe())
            else:
                if not prepared.success:
                    return fail(
                        "create_rejected",
                        prepared.error or prepared.message or "Beam rejected the transfer.",
                        EXIT_FAILED,
                    )
                transfer_id = prepared.transfer_id
                delivered = prepared.total_size * max(prepared.total_destinations, 1)
                emit(
                    "created",
                    transfer_id=transfer_id,
                    **spec.describe(),
                    size_bytes=prepared.total_size,
                    chunks=prepared.logical_chunks,
                    delivery_tasks=prepared.total_chunks,
                    estimated_credits=estimated_credits(delivered),
                )

            progress = asyncio.create_task(
                report_progress(api_key, transfer_id, args.progress_interval)
            )
            try:
                status = await beam.transfers.wait_complete(transfer_id, timeout=args.timeout)
            finally:
                progress.cancel()
            emit(
                "completed",
                transfer_id=transfer_id,
                size_bytes=status.source_bytes_total,
                delivered_bytes=status.delivery_bytes_completed,
                destinations_completed=status.destinations_completed,
                started_at=status.started_at,
                completed_at=status.completed_at,
                integrity_check_warning=status.integrity_check_warning,
            )
            return EXIT_OK
        except BeamStorageAccessError as exc:
            emit(
                "failed",
                transfer_id=transfer_id,
                code=exc.code,
                error_message=exc.error_message,
                hint="Grant the key read (source) or write and multipart (destination) access, "
                "with no IP or network restriction.",
            )
            return EXIT_FAILED
        except BeamTransferFailedError as exc:
            emit("failed", transfer_id=transfer_id, error_message=exc.error_message)
            return EXIT_FAILED
        except BeamProviderTransferError as exc:
            emit(
                "failed",
                transfer_id=exc.transfer_id,
                error_message=str(exc),
                transfer_cancelled=exc.transfer_cancelled,
            )
            return EXIT_FAILED
        except BeamTimeoutError as exc:
            emit(
                "timeout",
                transfer_id=transfer_id,
                message=str(exc),
                hint="The transfer may still finish. Check it with `status`. This process "
                "stopped re-signing its routes, so rerun long transfers with a larger --timeout.",
            )
            return EXIT_TIMEOUT
        except BeamAPIError as exc:
            if exc.status_code == 409 and transfer_id:
                emit("cancelled", transfer_id=transfer_id)
                return EXIT_FAILED
            if exc.status_code in (401, 403):
                return fail("auth", exc.detail, EXIT_AUTH, status_code=exc.status_code)
            kind = "insufficient_credits" if exc.status_code == 402 else "api_error"
            return fail(kind, exc.detail, EXIT_FAILED, status_code=exc.status_code)
        except asyncio.CancelledError:
            emit(
                "interrupted",
                transfer_id=transfer_id or None,
                hint="The transfer was not cancelled. Check it with `status`, or stop it with "
                "`cancel`.",
            )
            return EXIT_INTERRUPTED


async def cmd_status(args: argparse.Namespace) -> int:
    api_key = require_api_key()
    async with httpx.AsyncClient() as client:
        response = await fetch_transfer(client, api_key, args.transfer_id)
    if response.status_code == 200:
        emit("status", transfer=response.json())
        return EXIT_OK
    if response.status_code in (401, 403):
        return fail(
            "auth", "Beam refused the API key.", EXIT_AUTH, status_code=response.status_code
        )
    if response.status_code == 404:
        return fail("not_found", "No transfer with that ID in this organization.", EXIT_USAGE)
    return fail("api_error", response.text[:300], EXIT_FAILED, status_code=response.status_code)


async def cmd_whoami(args: argparse.Namespace) -> int:
    api_key = require_api_key()
    headers = {"X-Api-Key": api_key}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/auth/me", headers=headers, timeout=20.0)
    if response.status_code == 200:
        account = response.json()
        emit(
            "whoami",
            status=account.get("status"),
            user_type=account.get("user_type"),
            key_role=account.get("current_key_role"),
            key_prefix=account.get("current_key_prefix"),
        )
        return EXIT_OK
    if response.status_code in (401, 403):
        return fail(
            "auth", "Beam refused the API key.", EXIT_AUTH, status_code=response.status_code
        )
    return fail("api_error", response.text[:300], EXIT_FAILED, status_code=response.status_code)


async def cmd_cancel(args: argparse.Namespace) -> int:
    api_key = require_api_key()
    async with beam_client(api_key) as beam:
        result = await beam.transfers.cancel(args.transfer_id)
    emit("cancel", transfer_id=args.transfer_id, success=result.success, message=result.message)
    return EXIT_OK if result.success else EXIT_FAILED


def positive_seconds(value: str) -> float:
    seconds = float(value)
    if seconds <= 0:
        raise argparse.ArgumentTypeError("must be a positive number of seconds")
    return seconds


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        emit("error", kind="usage", message=message)
        self.print_usage(sys.stderr)
        raise SystemExit(EXIT_USAGE)


def parser() -> argparse.ArgumentParser:
    root = JsonArgumentParser(
        prog="beam_transfer.py",
        description="Beam transfers for agents. Prints one JSON object per line.",
    )
    commands = root.add_subparsers(dest="command", required=True, parser_class=JsonArgumentParser)

    def endpoints(command: argparse.ArgumentParser) -> None:
        command.add_argument("--source", required=True, help="Source object URI")
        command.add_argument(
            "--dest",
            action="append",
            required=True,
            help="Destination object URI; repeat to fan out to several destinations",
        )

    estimate = commands.add_parser(
        "estimate",
        help="Read the source size from storage and estimate the cost; Beam is not contacted",
    )
    endpoints(estimate)

    run = commands.add_parser("run", help="Create a transfer and wait for it to finish")
    endpoints(run)
    run.add_argument("--name", help="Transfer name shown in the Console")
    run.add_argument(
        "--timeout", type=positive_seconds, default=21600.0, help="Seconds to wait (default 21600)"
    )
    run.add_argument(
        "--progress-interval",
        type=positive_seconds,
        default=30.0,
        help="Seconds between progress events (default 30)",
    )
    run.add_argument("--hf-commit-message", help="Commit summary for hf:// destinations")
    run.add_argument(
        "--hf-create-pr", action="store_true", help="Open hf:// uploads as a pull request"
    )
    run.add_argument(
        "--hf-allow-source-rehash",
        action="store_true",
        help="Let the SDK read the source once to hash it; required to upload a non-Hub source to hf://",
    )
    run.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate URIs and credentials without contacting anything",
    )

    status = commands.add_parser("status", help="Read a transfer from the Beam API")
    status.add_argument("transfer_id")

    cancel = commands.add_parser("cancel", help="Cancel a transfer")
    cancel.add_argument("transfer_id")

    commands.add_parser("whoami", help="Check BEAM_API_KEY against the Beam API")
    return root


async def dispatch(args: argparse.Namespace) -> int:
    task = asyncio.current_task()
    loop = asyncio.get_running_loop()
    for signum in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(signum, task.cancel)
        except (NotImplementedError, RuntimeError):
            pass
    handlers = {"run": cmd_run, "status": cmd_status, "cancel": cmd_cancel, "whoami": cmd_whoami}
    return await handlers[args.command](args)


def main() -> int:
    logging.basicConfig(
        stream=sys.stderr, level=logging.WARNING, format="%(levelname)s %(message)s"
    )
    args = parser().parse_args()
    try:
        if args.command == "estimate":
            return cmd_estimate(args)
        return asyncio.run(dispatch(args))
    except UsageError as exc:
        return fail(exc.kind, str(exc), EXIT_USAGE, **exc.details)
    except BeamAuthError as exc:
        return fail("auth", str(exc), EXIT_AUTH)
    except (KeyboardInterrupt, asyncio.CancelledError):
        emit("interrupted", hint="Check the transfer with `status`, or stop it with `cancel`.")
        return EXIT_INTERRUPTED
    except Exception as exc:  # noqa: BLE001
        return fail("unexpected", f"{type(exc).__name__}: {exc}", EXIT_FAILED)


if __name__ == "__main__":
    sys.exit(main())
