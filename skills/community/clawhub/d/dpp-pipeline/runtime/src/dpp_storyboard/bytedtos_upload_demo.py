from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from dotenv import load_dotenv

_INSTALL_COMMAND = "python -m pip install tos"


class BytedTosDemoError(ValueError):
    """Raised when the demo configuration or inputs are invalid."""


class BytedTosDependencyError(RuntimeError):
    """Raised when the public `tos` package is unavailable."""


@dataclass(frozen=True, slots=True)
class TosUploadDemoConfig:
    bucket: str
    access_key: str
    secret_key: str
    endpoint: str
    region: str
    object_prefix: str
    enable_https: bool
    force_endpoint: bool
    timeout_seconds: float
    connect_timeout_seconds: float

    @classmethod
    def from_env(cls) -> "TosUploadDemoConfig":
        load_dotenv(dotenv_path=os.getenv("DPP_DOTENV_PATH"))
        return cls.from_mapping(os.environ)

    @classmethod
    def from_mapping(cls, env: Mapping[str, object]) -> "TosUploadDemoConfig":
        bucket = _require_non_empty(env, "TOS_BUCKET")
        access_key = _require_non_empty(env, "TOS_AK")
        secret_key = _require_non_empty(env, "TOS_SK")
        endpoint = _require_non_empty(env, "TOS_ENDPOINT")
        region = _require_non_empty(env, "TOS_REGION")

        return cls(
            bucket=bucket,
            access_key=access_key,
            secret_key=secret_key,
            endpoint=endpoint,
            region=region,
            object_prefix=_normalize_prefix(_read_str(env, "TOS_OBJECT_PREFIX", "demo/dpp")),
            enable_https=_read_bool(env, "TOS_ENABLE_HTTPS", default=False),
            force_endpoint=_read_bool(env, "TOS_FORCE_ENDPOINT", default=False),
            timeout_seconds=_read_float(env, "TOS_TIMEOUT_SECONDS", default=30.0),
            connect_timeout_seconds=_read_float(env, "TOS_CONNECT_TIMEOUT_SECONDS", default=5.0),
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Upload a local file or inline text to TOS using TOS_BUCKET/TOS_AK/TOS_SK/TOS_ENDPOINT/TOS_REGION "
            "from the environment."
        )
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Local file path to upload. If omitted, the demo uploads inline text content.",
    )
    parser.add_argument(
        "--key",
        help="Explicit object key. Defaults to TOS_OBJECT_PREFIX/<timestamp>-<filename>.",
    )
    parser.add_argument(
        "--prefix",
        help="Override TOS_OBJECT_PREFIX for this run.",
    )
    parser.add_argument(
        "--content",
        default="hello from tos demo\n",
        help="Inline text payload used when no file argument is provided.",
    )
    parser.add_argument(
        "--skip-head",
        action="store_true",
        help="Skip the post-upload head_object verification call.",
    )
    return parser.parse_args(argv)


def build_object_key(
    prefix: str,
    source_name: str,
    *,
    now: datetime | None = None,
) -> str:
    timestamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    filename = Path(source_name).name or "upload.bin"
    normalized_prefix = _normalize_prefix(prefix)
    object_name = f"{timestamp}-{filename}"
    if not normalized_prefix:
        return object_name
    return f"{normalized_prefix}/{object_name}"


def create_client(config: TosUploadDemoConfig) -> Any:
    try:
        from tos import TosClientV2
    except ModuleNotFoundError as exc:
        raise BytedTosDependencyError(
            "`tos` is not installed. Install it with:\n"
            f"  {_INSTALL_COMMAND}"
        ) from exc

    return TosClientV2(
        ak=config.access_key,
        sk=config.secret_key,
        endpoint=config.endpoint,
        region=config.region,
        request_timeout=config.timeout_seconds,
        connection_time=config.connect_timeout_seconds,
        enable_verify_ssl=config.enable_https,
        is_custom_domain=config.force_endpoint,
    )


def upload_inline_text(client: Any, config: TosUploadDemoConfig, *, key: str, content: str) -> Any:
    return client.put_object(bucket=config.bucket, key=key, content=content.encode("utf-8"))


def upload_local_file(client: Any, config: TosUploadDemoConfig, *, key: str, path: Path) -> Any:
    with path.open("rb") as file_obj:
        return client.put_object(bucket=config.bucket, key=key, content=file_obj)


def verify_object(client: Any, config: TosUploadDemoConfig, *, key: str) -> Any:
    return client.head_object(bucket=config.bucket, key=key)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        config = TosUploadDemoConfig.from_env()
        if args.prefix is not None:
            config = replace(config, object_prefix=_normalize_prefix(args.prefix))

        upload_path = _resolve_upload_path(args.file)
        source_name = upload_path.name if upload_path else "inline-demo.txt"
        object_key = args.key or build_object_key(config.object_prefix, source_name)

        client = create_client(config)
        if upload_path is not None:
            upload_response = upload_local_file(client, config, key=object_key, path=upload_path)
            print(f"uploaded_file={upload_path}")
        else:
            upload_response = upload_inline_text(client, config, key=object_key, content=args.content)
            print("uploaded_file=<inline-text>")

        print(f"bucket={config.bucket}")
        print(f"endpoint={config.endpoint}")
        print(f"object_key={object_key}")
        print(f"object_url={build_public_object_url(config, object_key)}")

        request_id = _get_request_id(upload_response)
        if request_id:
            print(f"request_id={request_id}")

        if not args.skip_head:
            head_response = verify_object(client, config, key=object_key)
            size = getattr(head_response, "size", None)
            last_modify_time = getattr(head_response, "last_modify_time", None)
            if size is not None:
                print(f"size={size}")
            if last_modify_time is not None:
                print(f"last_modify_time={last_modify_time}")

        print("upload_status=success")
        return 0
    except (BytedTosDemoError, BytedTosDependencyError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _resolve_upload_path(raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    path = Path(raw_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"upload file not found: {path}")
    return path


def _get_request_id(response: Any) -> str | None:
    request_id = getattr(response, "request_id", None)
    if request_id:
        return str(request_id)
    headers = getattr(response, "headers", None) or {}
    for key in ("x-tos-request-id", "X-Tos-Request-Id", "X-TOS-REQUEST-ID"):
        if key in headers:
            return str(headers[key])
    return None


def build_public_object_url(config: TosUploadDemoConfig, object_key: str) -> str:
    scheme = "https" if config.enable_https else "http"
    return f"{scheme}://{config.bucket}.{config.endpoint}/{object_key}"


def _require_non_empty(env: Mapping[str, object], name: str) -> str:
    value = _read_str(env, name, "")
    if not value:
        raise BytedTosDemoError(f"{name} is required.")
    return value


def _read_str(env: Mapping[str, object], name: str, default: str) -> str:
    raw = env.get(name, default)
    if raw is None:
        return default
    return str(raw).strip()


def _read_bool(env: Mapping[str, object], name: str, *, default: bool) -> bool:
    raw = _read_str(env, name, "")
    if not raw:
        return default
    normalized = raw.lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise BytedTosDemoError(
        f"{name} must be one of: 1, 0, true, false, yes, no, on, off."
    )


def _read_float(env: Mapping[str, object], name: str, *, default: float) -> float:
    raw = _read_str(env, name, "")
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise BytedTosDemoError(f"{name} must be a number.") from exc
    if value <= 0:
        raise BytedTosDemoError(f"{name} must be greater than 0.")
    return value


def _normalize_prefix(prefix: str) -> str:
    return prefix.strip().strip("/")


if __name__ == "__main__":
    raise SystemExit(main())
