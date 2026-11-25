from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import tempfile
import uuid
from pathlib import Path

from . import SCHEMA_VERSION, __version__


class ManagerError(Exception):
    code = "manager_error"


class Conflict(ManagerError):
    code = "conflict"


class GateError(ManagerError):
    code = "capability_gate"


class MissingAttachment(ManagerError):
    code = "missing_attachment"


class DownloadUnavailable(GateError):
    code = "download_unavailable"


class NetworkError(ManagerError):
    code = "network_error"

    def __init__(self, kind, network_mode, *, operation):
        self.kind, self.network_mode, self.operation = kind, network_mode, operation
        description = {"tls_eof": "TLS connection closed unexpectedly; check the selected proxy route",
                       "mcp_transport": "Native MCP connection failed; check the client's network route separately from Python file transfers",
                       "tls_certificate": "TLS certificate verification failed",
                       "tls": "TLS handshake failed", "dns": "Host name lookup failed",
                       "timeout": "Network request timed out"}.get(kind, "Network request failed")
        super().__init__(f"{description} ({network_mode}, {operation}); preserve progress and reconcile before retrying")


class APIError(ManagerError):
    code = "api_error"

    def __init__(self, status: int, message: str = "FlowUs request failed"):
        self.status = status
        super().__init__(f"{message} (HTTP {status})")


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_hash(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def stable_id(vault_id: str, kind: str, key: str) -> str:
    return str(uuid.uuid5(uuid.UUID(vault_id), f"{kind}:{key}"))


def atomic_json(path: Path, value, *, exclusive: bool = False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".cva-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        if exclusive:
            # Linking is atomic and refuses an existing destination.
            os.link(temp, path)
        else:
            os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def load_config(path: Path) -> dict:
    if not path.is_file():
        raise ManagerError("Missing config. Run init --local first; see references/setup.md.")
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != SCHEMA_VERSION:
        raise GateError("Unsupported config schema; upgrade the tool before writing.")
    uuid.UUID(value["vault_id"])
    if not isinstance(value.get("agent_id"), str) or not value["agent_id"].strip():
        raise ManagerError("agent_id must be configured")
    governance_mode(value)
    network_mode(value)
    transport_mode(value)
    rest_auth_mode(value)
    return value


def governance_mode(config):
    # Absence means the original isolated-approval policy, never a silent downgrade.
    mode = config.get("governance_mode", "isolated_approval")
    if mode not in ("trusted_client", "isolated_approval"):
        raise GateError("Unknown governance mode; configure it explicitly before writing")
    return mode


def network_mode(config):
    mode = config.get("network_mode", "system")
    if mode not in ("system", "direct"):
        raise ManagerError("network_mode must be system or direct")
    return mode


def transport_mode(config):
    mode = config.get("transport", "rest")
    if mode not in ("rest", "mcp_relay"):
        raise ManagerError("transport must be rest or mcp_relay")
    if mode == "mcp_relay" and governance_mode(config) != "trusted_client":
        raise GateError("Native MCP relay requires explicitly selected trusted_client governance")
    return mode


def credential_names(config, *, provision=False):
    if governance_mode(config) == "trusted_client":
        return ("FLOWUS_API_TOKEN",)
    return ("FLOWUS_API_TOKEN", "FLOWUS_SETUP_TOKEN" if provision else "FLOWUS_APPROVAL_READ_TOKEN")


def rest_auth_mode(config):
    mode = config.get("rest_auth", "environment")
    if mode not in {"environment", "flowus_cli"}:
        raise GateError("rest_auth must be environment or flowus_cli")
    if mode == "flowus_cli" and (transport_mode(config) != "rest" or governance_mode(config) != "trusted_client"):
        raise GateError("Official CLI authentication requires REST and trusted_client governance")
    return mode


def credential_value(name):
    return os.environ.get(name, "") or (os.environ.get("FLOWUS_TOKEN", "") if name == "FLOWUS_API_TOKEN" else "")


def config_template() -> dict:
    return {"schema_version": SCHEMA_VERSION, "tool_version": __version__,
            "vault_id": str(uuid.uuid4()), "agent_id": "local-agent",
            "governance_mode": "trusted_client",
            "network_mode": "system",
            "transport": "rest",
            "business_parent_id": "", "approval_parent_id": "", "approval_probe_id": "",
            "databases": {}, "rules": {"categories": [], "continuous_keywords": [],
            "title_aliases": [], "business_terms": [], "ambiguous_names": ["untitled", "新建", "未命名"]}}


def safe_relative(root: Path, relative: str) -> Path:
    root = root.resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise ManagerError("Path escapes the requested source or backup directory")
    return target
