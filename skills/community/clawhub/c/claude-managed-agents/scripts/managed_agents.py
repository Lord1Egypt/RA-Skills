#!/usr/bin/env python3
"""Claude Managed Agents helper CLI.

SDK-first helper with HTTP fallback for managing the Claude Managed Agents
lifecycle: agents, environments, sessions, and session events.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Iterator, Optional

try:  # pragma: no cover - optional dependency in this environment
    from anthropic import Anthropic
except Exception:  # pragma: no cover
    Anthropic = None

API_BASE_URL = os.environ.get("ANTHROPIC_API_BASE_URL", "https://api.anthropic.com")
ANTHROPIC_VERSION = "2023-06-01"
MANAGED_AGENTS_BETA = os.environ.get("ANTHROPIC_MANAGED_AGENTS_BETA", "managed-agents-2026-04-01")
FILES_API_BETA = os.environ.get("ANTHROPIC_FILES_API_BETA", "files-api-2025-04-14")
DEFAULT_TIMEOUT = float(os.environ.get("ANTHROPIC_TIMEOUT_SECONDS", "60"))
VALID_BUILTIN_TOOLS = {
    "bash",
    "read",
    "write",
    "edit",
    "glob",
    "grep",
    "web_fetch",
    "web_search",
}


class CliError(RuntimeError):
    """Raised for expected CLI/operator failures."""


def _json_dump(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=False)


def _print_json(data: Any) -> None:
    print(_json_dump(data))


def _beta_header_value(betas: list[str] | tuple[str, ...] | None) -> str:
    values = [beta.strip() for beta in (betas or []) if beta and beta.strip()]
    if not values:
        raise CliError("at least one beta header is required")
    return ",".join(values)


def _parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"invalid boolean: {value!r}")


def _load_textish(value: str) -> str:
    if value.startswith("@"):
        with open(value[1:], "r", encoding="utf-8") as handle:
            return handle.read()
    return value


def _load_jsonish(value: str) -> Any:
    text = _load_textish(value)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise CliError(f"invalid JSON value: {exc}") from exc


def _parse_metadata(value: Optional[str]) -> Optional[dict[str, Any]]:
    if not value:
        return None
    parsed = _load_jsonish(value)
    if not isinstance(parsed, dict):
        raise CliError("metadata JSON must be an object")
    return parsed


def _parse_json_list(values: Optional[list[str]]) -> list[Any]:
    return [_load_jsonish(value) for value in (values or [])]


def _parse_tool_policy(spec: str) -> tuple[str, str]:
    if "=" not in spec:
        raise CliError(f"tool policy must be name=allow|ask, got: {spec}")
    name, policy = spec.split("=", 1)
    name = name.strip()
    policy = policy.strip().lower()
    if name not in VALID_BUILTIN_TOOLS:
        raise CliError(f"unknown built-in tool: {name}")
    if policy not in {"allow", "ask"}:
        raise CliError(f"tool policy must be allow or ask, got: {policy}")
    return name, policy


def _permission_policy(policy: str) -> dict[str, str]:
    mapping = {"allow": "always_allow", "ask": "always_ask"}
    try:
        return {"type": mapping[policy.lower()]}
    except KeyError as exc:
        raise CliError(f"unsupported permission policy: {policy}") from exc


def _coerce_host(value: str) -> str:
    value = value.strip()
    if not value:
        raise CliError("allowed host cannot be empty")
    if "://" in value or "/" in value:
        raise CliError(f"allowed host must be a bare hostname like api.example.com, got: {value}")
    return value


def _to_plain(obj: Any) -> Any:
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {key: _to_plain(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_to_plain(item) for item in obj]

    for method_name in ("model_dump", "to_dict", "dict"):
        method = getattr(obj, method_name, None)
        if callable(method):
            try:
                return _to_plain(method(mode="json"))
            except TypeError:
                try:
                    return _to_plain(method())
                except TypeError:
                    pass

    for method_name in ("model_dump_json", "json"):
        method = getattr(obj, method_name, None)
        if callable(method):
            try:
                return json.loads(method())
            except Exception:
                pass

    if hasattr(obj, "data"):
        payload: dict[str, Any] = {"data": _to_plain(getattr(obj, "data"))}
        for attr in ("next_page", "has_more", "id", "type"):
            if hasattr(obj, attr):
                payload[attr] = _to_plain(getattr(obj, attr))
        return payload

    if hasattr(obj, "__dict__"):
        return {
            key: _to_plain(value)
            for key, value in vars(obj).items()
            if not key.startswith("_")
        }

    try:
        return [_to_plain(item) for item in obj]
    except TypeError:
        return str(obj)


class ManagedAgentsClient:
    def __init__(self, *, backend: str = "auto", api_key_env: str = "ANTHROPIC_API_KEY", timeout: float = DEFAULT_TIMEOUT):
        self.api_key_env = api_key_env
        self.timeout = timeout
        self.api_key = os.environ.get(api_key_env)
        if not self.api_key:
            raise CliError(f"{api_key_env} is not set")

        if backend == "auto":
            backend = "sdk" if Anthropic is not None else "http"
        if backend not in {"sdk", "http"}:
            raise CliError(f"unsupported backend: {backend}")
        if backend == "sdk" and Anthropic is None:
            raise CliError("anthropic Python SDK is not installed; use --backend http or install `anthropic`")

        self.backend = backend
        self.sdk = Anthropic(api_key=self.api_key, timeout=timeout) if backend == "sdk" else None

    def _request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[dict[str, Any]] = None,
        payload: Optional[dict[str, Any]] = None,
        raw_data: Optional[bytes] = None,
        content_type: Optional[str] = None,
        accept: str = "application/json",
        betas: Optional[list[str]] = None,
    ) -> Any:
        url = f"{API_BASE_URL.rstrip('/')}{path}"
        if query:
            encoded = urllib.parse.urlencode({k: v for k, v in query.items() if v is not None}, doseq=True)
            if encoded:
                url = f"{url}?{encoded}"

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "anthropic-beta": _beta_header_value(betas or [MANAGED_AGENTS_BETA]),
            "accept": accept,
        }
        if payload is not None and raw_data is not None:
            raise CliError("payload and raw_data cannot both be supplied")

        data = raw_data
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["content-type"] = "application/json"
        elif raw_data is not None and content_type:
            headers["content-type"] = content_type

        request = urllib.request.Request(url=url, data=data, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                if accept == "text/event-stream":
                    return raw
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8")
            try:
                body = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                body = {"message": raw or exc.reason}
            raise CliError(f"Anthropic API error {exc.code}: {_json_dump(body)}") from exc
        except urllib.error.URLError as exc:
            raise CliError(f"network error: {exc}") from exc

    def _sdk_call(self, target: Any, method_names: list[str], *args: Any, **kwargs: Any) -> Any:
        for name in method_names:
            method = getattr(target, name, None)
            if callable(method):
                return method(*args, **kwargs)
        raise CliError(f"SDK object does not support methods: {', '.join(method_names)}")

    def create_agent(self, payload: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.agents.create(**payload))
        return self._request("POST", "/v1/agents", payload=payload)

    def update_agent(self, agent_id: str, payload: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.agents.update(agent_id, **payload))
        return self._request("POST", f"/v1/agents/{agent_id}", payload=payload)

    def retrieve_agent(self, agent_id: str) -> Any:
        if self.backend == "sdk":
            return _to_plain(self._sdk_call(self.sdk.beta.agents, ["retrieve", "get"], agent_id))
        return self._request("GET", f"/v1/agents/{agent_id}")

    def list_agents(self, query: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.agents.list(**query))
        return self._request("GET", "/v1/agents", query=query)

    def list_agent_versions(self, agent_id: str, query: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.agents.versions.list(agent_id, **query))
        return self._request("GET", f"/v1/agents/{agent_id}/versions", query=query)

    def archive_agent(self, agent_id: str) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.agents.archive(agent_id))
        return self._request("POST", f"/v1/agents/{agent_id}/archive")

    def delete_agent(self, agent_id: str) -> Any:
        if self.backend == "sdk":
            result = self.sdk.beta.agents.delete(agent_id)
            return _to_plain(result) if result is not None else {"ok": True}
        return self._request("DELETE", f"/v1/agents/{agent_id}")

    def create_environment(self, payload: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.environments.create(**payload))
        return self._request("POST", "/v1/environments", payload=payload)

    def update_environment(self, environment_id: str, payload: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.environments.update(environment_id, **payload))
        return self._request("POST", f"/v1/environments/{environment_id}", payload=payload)

    def retrieve_environment(self, environment_id: str) -> Any:
        if self.backend == "sdk":
            return _to_plain(self._sdk_call(self.sdk.beta.environments, ["retrieve", "get"], environment_id))
        return self._request("GET", f"/v1/environments/{environment_id}")

    def list_environments(self, query: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.environments.list(**query))
        return self._request("GET", "/v1/environments", query=query)

    def archive_environment(self, environment_id: str) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.environments.archive(environment_id))
        return self._request("POST", f"/v1/environments/{environment_id}/archive")

    def delete_environment(self, environment_id: str) -> Any:
        if self.backend == "sdk":
            result = self.sdk.beta.environments.delete(environment_id)
            return _to_plain(result) if result is not None else {"ok": True}
        return self._request("DELETE", f"/v1/environments/{environment_id}")

    def create_session(self, payload: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.sessions.create(**payload))
        return self._request("POST", "/v1/sessions", payload=payload)

    def upload_file(self, file_path: str, *, filename: Optional[str] = None, mime_type: Optional[str] = None) -> Any:
        body, content_type = _build_file_upload_request(file_path, filename=filename, mime_type=mime_type)
        return self._request(
            "POST",
            "/v1/files",
            raw_data=body,
            content_type=content_type,
            betas=[FILES_API_BETA],
        )

    def list_files(self, query: dict[str, Any]) -> Any:
        return self._request("GET", "/v1/files", query=query, betas=[MANAGED_AGENTS_BETA])

    def delete_file(self, file_id: str) -> Any:
        return self._request("DELETE", f"/v1/files/{file_id}", betas=[FILES_API_BETA])

    def download_file(self, file_id: str) -> bytes:
        url = f"{API_BASE_URL.rstrip('/')}/v1/files/{file_id}/content"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "anthropic-beta": _beta_header_value([MANAGED_AGENTS_BETA]),
            "accept": "application/octet-stream",
        }
        request = urllib.request.Request(url=url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            raise CliError(f"file download error {exc.code}: {raw or exc.reason}") from exc
        except urllib.error.URLError as exc:
            raise CliError(f"file download network error: {exc}") from exc

    def retrieve_session(self, session_id: str) -> Any:
        if self.backend == "sdk":
            return _to_plain(self._sdk_call(self.sdk.beta.sessions, ["retrieve", "get"], session_id))
        return self._request("GET", f"/v1/sessions/{session_id}")

    def list_sessions(self, query: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.sessions.list(**query))
        return self._request("GET", "/v1/sessions", query=query)

    def archive_session(self, session_id: str) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.sessions.archive(session_id))
        return self._request("POST", f"/v1/sessions/{session_id}/archive")

    def delete_session(self, session_id: str) -> Any:
        if self.backend == "sdk":
            result = self.sdk.beta.sessions.delete(session_id)
            return _to_plain(result) if result is not None else {"ok": True}
        return self._request("DELETE", f"/v1/sessions/{session_id}")

    def send_events(self, session_id: str, events: list[dict[str, Any]]) -> Any:
        payload = {"events": events}
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.sessions.events.send(session_id, **payload))
        return self._request("POST", f"/v1/sessions/{session_id}/events", payload=payload)

    def list_events(self, session_id: str, query: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.sessions.events.list(session_id, **query))
        return self._request("GET", f"/v1/sessions/{session_id}/events", query=query)

    def add_session_resource(self, session_id: str, payload: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.sessions.resources.add(session_id, **payload))
        return self._request("POST", f"/v1/sessions/{session_id}/resources", payload=payload)

    def list_session_resources(self, session_id: str, query: dict[str, Any]) -> Any:
        if self.backend == "sdk":
            return _to_plain(self.sdk.beta.sessions.resources.list(session_id, **query))
        return self._request("GET", f"/v1/sessions/{session_id}/resources", query=query)

    def delete_session_resource(self, session_id: str, resource_id: str) -> Any:
        if self.backend == "sdk":
            result = self.sdk.beta.sessions.resources.delete(resource_id, session_id=session_id)
            return _to_plain(result) if result is not None else {"ok": True}
        return self._request("DELETE", f"/v1/sessions/{session_id}/resources/{resource_id}")

    def stream_events(self, session_id: str) -> Iterator[dict[str, Any]]:
        url = f"{API_BASE_URL.rstrip('/')}/v1/sessions/{session_id}/events/stream"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "anthropic-beta": MANAGED_AGENTS_BETA,
            "accept": "text/event-stream",
        }
        request = urllib.request.Request(url=url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data_lines: list[str] = []
                for raw_line in response:
                    line = raw_line.decode("utf-8").rstrip("\r\n")
                    if not line:
                        if data_lines:
                            yield json.loads("\n".join(data_lines))
                            data_lines = []
                        continue
                    if line.startswith(":"):
                        continue
                    if line.startswith("data:"):
                        data_lines.append(line[5:].lstrip())
                if data_lines:
                    yield json.loads("\n".join(data_lines))
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8")
            raise CliError(f"stream error {exc.code}: {raw or exc.reason}") from exc
        except urllib.error.URLError as exc:
            raise CliError(f"stream network error: {exc}") from exc


def _build_agent_toolset(args: argparse.Namespace) -> Optional[dict[str, Any]]:
    use_toolset = args.agent_toolset or any(
        [
            args.enable_tool,
            args.disable_tool,
            args.tool_policy,
            args.default_tool_enabled is not None,
            args.default_tool_policy,
        ]
    )
    if not use_toolset:
        return None

    toolset: dict[str, Any] = {"type": "agent_toolset_20260401"}
    default_config: dict[str, Any] = {}
    if args.default_tool_enabled is not None:
        default_config["enabled"] = args.default_tool_enabled
    if args.default_tool_policy:
        default_config["permission_policy"] = _permission_policy(args.default_tool_policy)
    if default_config:
        toolset["default_config"] = default_config

    configs: dict[str, dict[str, Any]] = {}
    for name in args.enable_tool or []:
        if name not in VALID_BUILTIN_TOOLS:
            raise CliError(f"unknown built-in tool: {name}")
        configs.setdefault(name, {"name": name})["enabled"] = True
    for name in args.disable_tool or []:
        if name not in VALID_BUILTIN_TOOLS:
            raise CliError(f"unknown built-in tool: {name}")
        configs.setdefault(name, {"name": name})["enabled"] = False
    for item in args.tool_policy or []:
        name, policy = _parse_tool_policy(item)
        configs.setdefault(name, {"name": name})["permission_policy"] = _permission_policy(policy)
    if configs:
        toolset["configs"] = [configs[name] for name in sorted(configs)]
    return toolset


def _build_model(args: argparse.Namespace) -> Optional[Any]:
    if args.model is None:
        return None
    if args.speed:
        return {"id": args.model, "speed": args.speed}
    return args.model


def _extend_tools_from_args(args: argparse.Namespace) -> Optional[list[Any]]:
    tools = []
    toolset = _build_agent_toolset(args)
    if toolset is not None:
        tools.append(toolset)
    tools.extend(_parse_json_list(args.tool_json))
    if args.clear_tools:
        return []
    return tools or None


def _parse_skill_ref(spec: str) -> dict[str, Any]:
    parts = spec.split(":")
    if len(parts) not in {2, 3}:
        raise CliError("skill ref must be type:skill_id[:version]")
    skill_type, skill_id = parts[0].strip(), parts[1].strip()
    if skill_type not in {"anthropic", "custom"}:
        raise CliError("skill type must be anthropic or custom")
    payload: dict[str, Any] = {"type": skill_type, "skill_id": skill_id}
    if len(parts) == 3 and parts[2].strip():
        payload["version"] = parts[2].strip()
    return payload


def _extend_skills_from_args(args: argparse.Namespace) -> Optional[list[Any]]:
    if args.clear_skills:
        return []
    skills = _parse_json_list(args.skill_json)
    skills.extend(_parse_skill_ref(spec) for spec in (args.skill_ref or []))
    return skills or None


def _extend_mcp_servers_from_args(args: argparse.Namespace) -> Optional[list[Any]]:
    if args.clear_mcp_servers:
        return []
    servers = _parse_json_list(args.mcp_server_json)
    for item in args.mcp_server or []:
        if "=" not in item:
            raise CliError("mcp server must be name=https://... URL")
        name, url = item.split("=", 1)
        servers.append({"type": "url", "name": name.strip(), "url": url.strip()})
    return servers or None


def _extend_callable_agents_from_args(args: argparse.Namespace) -> Optional[list[Any]]:
    if args.clear_callable_agents:
        return []
    agents = _parse_json_list(args.callable_agent_json)
    return agents or None


def _build_agent_payload(args: argparse.Namespace, *, update: bool) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if update:
        payload["version"] = args.version

    if args.name is not None:
        payload["name"] = args.name

    model = _build_model(args)
    if model is not None:
        payload["model"] = model

    if args.clear_system:
        payload["system"] = None
    elif args.system is not None:
        payload["system"] = _load_textish(args.system)

    if args.clear_description:
        payload["description"] = None
    elif args.description is not None:
        payload["description"] = _load_textish(args.description)

    metadata = _parse_metadata(args.metadata_json)
    if metadata is not None:
        payload["metadata"] = metadata

    tools = _extend_tools_from_args(args)
    if tools is not None:
        payload["tools"] = tools

    mcp_servers = _extend_mcp_servers_from_args(args)
    if mcp_servers is not None:
        payload["mcp_servers"] = mcp_servers

    skills = _extend_skills_from_args(args)
    if skills is not None:
        payload["skills"] = skills

    callable_agents = _extend_callable_agents_from_args(args)
    if callable_agents is not None:
        payload["callable_agents"] = callable_agents

    return payload


def _build_environment_config(args: argparse.Namespace) -> Optional[dict[str, Any]]:
    if args.config_json:
        config = _load_jsonish(args.config_json)
        if not isinstance(config, dict):
            raise CliError("config JSON must be an object")
        return config

    config: dict[str, Any] = {}
    if any([args.network, args.allowed_host, args.allow_mcp_servers, args.allow_package_managers]):
        network_type = args.network or ("limited" if args.allowed_host else "unrestricted")
        if network_type == "unrestricted":
            networking: dict[str, Any] = {"type": "unrestricted"}
        else:
            networking = {"type": "limited"}
            if args.allowed_host:
                networking["allowed_hosts"] = [_coerce_host(item) for item in args.allowed_host]
            if args.allow_mcp_servers:
                networking["allow_mcp_servers"] = True
            if args.allow_package_managers:
                networking["allow_package_managers"] = True
        config["networking"] = networking

    packages: dict[str, list[str]] = {}
    for field in ("apt", "cargo", "gem", "go", "npm", "pip"):
        values = getattr(args, field)
        if values:
            packages[field] = values
    if packages:
        config["packages"] = packages

    if not config:
        return None
    config["type"] = "cloud"
    return config


def _build_environment_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.name is not None:
        payload["name"] = args.name
    if args.description is not None:
        payload["description"] = _load_textish(args.description)
    metadata = _parse_metadata(args.metadata_json)
    if metadata is not None:
        payload["metadata"] = metadata
    config = _build_environment_config(args)
    if config is not None:
        payload["config"] = config
    return payload


def _build_file_upload_request(
    file_path: str,
    *,
    filename: Optional[str] = None,
    mime_type: Optional[str] = None,
) -> tuple[bytes, str]:
    path = Path(file_path).expanduser()
    if not path.exists():
        raise CliError(f"file does not exist: {path}")
    if not path.is_file():
        raise CliError(f"path is not a file: {path}")

    upload_name = filename or path.name
    upload_mime = mime_type or mimetypes.guess_type(upload_name)[0] or "application/octet-stream"
    boundary = f"----anthropic-upload-{uuid.uuid4().hex}"
    file_bytes = path.read_bytes()

    body = b"".join(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            (
                f'Content-Disposition: form-data; name="file"; filename="{upload_name}"\r\n'
            ).encode("utf-8"),
            f"Content-Type: {upload_mime}\r\n\r\n".encode("utf-8"),
            file_bytes,
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
    )
    return body, f"multipart/form-data; boundary={boundary}"


def _build_agent_ref(args: argparse.Namespace) -> Any:
    if args.agent_json:
        return _load_jsonish(args.agent_json)
    if not args.agent_id:
        raise CliError("session create requires --agent-id or --agent-json")
    if args.agent_version is not None:
        return {"type": "agent", "id": args.agent_id, "version": args.agent_version}
    return args.agent_id


def _build_session_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "agent": _build_agent_ref(args),
        "environment_id": args.environment_id,
    }
    if args.title:
        payload["title"] = _load_textish(args.title)
    metadata = _parse_metadata(args.metadata_json)
    if metadata is not None:
        payload["metadata"] = metadata
    if args.vault_id:
        payload["vault_ids"] = args.vault_id
    resources = _parse_json_list(args.resource_json)
    if resources:
        payload["resources"] = resources
    return payload


def _build_resource_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.resource_json:
        payload = _load_jsonish(args.resource_json)
        if not isinstance(payload, dict):
            raise CliError("resource JSON must be an object")
        return payload
    if args.type != "file":
        raise CliError("currently only file resources are supported by the helper")
    if not args.file_id:
        raise CliError("resource add requires --file-id when --type file is used")
    payload = {"type": "file", "file_id": args.file_id}
    if args.mount_path:
        payload["mount_path"] = args.mount_path
    return payload


def _text_block(text: str) -> dict[str, str]:
    return {"type": "text", "text": _load_textish(text)}


def _build_send_events(args: argparse.Namespace) -> list[dict[str, Any]]:
    events = _parse_json_list(args.event_json)
    if args.interrupt:
        events.append({"type": "user.interrupt"})
    if args.message:
        events.append({"type": "user.message", "content": [_text_block(args.message)]})
    if args.confirm_tool_use_id:
        event: dict[str, Any] = {
            "type": "user.tool_confirmation",
            "tool_use_id": args.confirm_tool_use_id,
            "result": args.confirm_result,
        }
        if args.confirm_result == "deny" and args.deny_message:
            event["deny_message"] = _load_textish(args.deny_message)
        events.append(event)
    if args.custom_tool_use_id:
        event = {
            "type": "user.custom_tool_result",
            "custom_tool_use_id": args.custom_tool_use_id,
        }
        if args.custom_tool_text is not None:
            event["content"] = [_text_block(args.custom_tool_text)]
        if args.custom_tool_is_error:
            event["is_error"] = True
        events.append(event)
    if not events:
        raise CliError("session send requires at least one event source")
    return events


def _summarize_stream_event(event: dict[str, Any]) -> Optional[str]:
    event_type = event.get("type")
    if event_type == "agent.message":
        parts = [block.get("text", "") for block in event.get("content", []) if block.get("type") == "text"]
        return "".join(parts)
    if event_type == "agent.tool_use":
        return f"\n[agent tool: {event.get('name')} permission={event.get('evaluated_permission', 'unknown')}]"
    if event_type == "agent.mcp_tool_use":
        return f"\n[mcp tool: {event.get('mcp_server_name')}/{event.get('name')} permission={event.get('evaluated_permission', 'unknown')}]"
    if event_type == "agent.custom_tool_use":
        return f"\n[custom tool: {event.get('name')} id={event.get('id')}]"
    if event_type == "session.status_running":
        return "\n[session running]"
    if event_type == "session.status_idle":
        return f"\n[session idle stop_reason={_json_dump(event.get('stop_reason'))}]"
    if event_type == "session.status_terminated":
        return "\n[session terminated]"
    if event_type == "session.error":
        error = event.get("error") or {}
        return f"\n[session error: {error.get('message', 'unknown')}]"
    return None


def handle_agent_create(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    payload = _build_agent_payload(args, update=False)
    _print_json(client.create_agent(payload))


def handle_agent_update(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    payload = _build_agent_payload(args, update=True)
    _print_json(client.update_agent(args.agent_id, payload))


def handle_agent_get(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.retrieve_agent(args.agent_id))


def handle_agent_list(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    query = {
        "include_archived": args.include_archived,
        "limit": args.limit,
        "page": args.page,
        "created_at[gte]": args.created_after,
        "created_at[lte]": args.created_before,
    }
    _print_json(client.list_agents(query))


def handle_agent_versions(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    query = {"limit": args.limit, "page": args.page}
    _print_json(client.list_agent_versions(args.agent_id, query))


def handle_agent_archive(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.archive_agent(args.agent_id))


def handle_agent_delete(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.delete_agent(args.agent_id))


def _doctor_checks(args: argparse.Namespace) -> dict[str, Any]:
    if args.backend == "auto":
        resolved_backend = "sdk" if Anthropic is not None else "http"
    else:
        resolved_backend = args.backend

    report: dict[str, Any] = {
        "ok": True,
        "backend": args.backend,
        "api_key_env": args.api_key_env,
        "resolved_backend": resolved_backend,
        "checks": [],
        "notes": [],
    }

    api_key = os.environ.get(args.api_key_env)
    report["checks"].append(
        {
            "name": "api_key_present",
            "ok": bool(api_key),
            "detail": f"environment variable {args.api_key_env} {'is set' if api_key else 'is missing'}",
        }
    )
    if not api_key:
        report["ok"] = False
        report["notes"].append("Set ANTHROPIC_API_KEY before using live API operations.")

    report["checks"].append(
        {
            "name": "backend_resolution",
            "ok": True,
            "detail": f"requested backend={args.backend}, resolved backend={resolved_backend}",
        }
    )

    if resolved_backend == "sdk":
        sdk_ok = Anthropic is not None
        report["checks"].append(
            {
                "name": "sdk_installed",
                "ok": sdk_ok,
                "detail": "anthropic SDK is available" if sdk_ok else "anthropic SDK is not installed",
            }
        )
        if not sdk_ok:
            report["ok"] = False
    else:
        report["checks"].append(
            {
                "name": "http_fallback_ready",
                "ok": True,
                "detail": "HTTP fallback path is available",
            }
        )

    beta_headers_ok = bool(MANAGED_AGENTS_BETA and FILES_API_BETA)
    report["checks"].append(
        {
            "name": "beta_headers",
            "ok": beta_headers_ok,
            "detail": f"managed_agents_beta={MANAGED_AGENTS_BETA}, files_api_beta={FILES_API_BETA}",
        }
    )
    if not beta_headers_ok:
        report["ok"] = False

    api_base_url_ok = API_BASE_URL.startswith("https://")
    report["checks"].append(
        {
            "name": "api_base_url",
            "ok": api_base_url_ok,
            "detail": f"api_base_url={API_BASE_URL}",
        }
    )
    if not api_base_url_ok:
        report["ok"] = False

    if args.allowed_host:
        coerced: list[str] = []
        for value in args.allowed_host:
            try:
                coerced.append(_coerce_host(value))
            except CliError as exc:
                report["checks"].append(
                    {
                        "name": "allowed_host_validation",
                        "ok": False,
                        "detail": str(exc),
                    }
                )
                report["ok"] = False
                break
        else:
            report["checks"].append(
                {
                    "name": "allowed_host_validation",
                    "ok": True,
                    "detail": f"validated bare hostnames: {', '.join(coerced)}",
                }
            )
    else:
        report["checks"].append(
            {
                "name": "allowed_host_validation",
                "ok": True,
                "detail": "no allowed hosts supplied for validation",
            }
        )

    report["notes"].append("Allowed hosts must be bare hostnames like api.example.com, not full URLs.")
    report["notes"].append("Uploaded source files may return downloadable=false; file download is mainly for generated artifacts.")
    report["notes"].append("Archive can fail on running sessions; delete may still succeed for disposable cleanup flows.")

    if args.live:
        live_check_names = [
            "live_environment_list",
            "live_session_list",
            "live_file_list",
        ]
        try:
            client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
        except CliError as exc:
            report["ok"] = False
            detail = f"live checks unavailable: {exc}"
            for name in live_check_names:
                report["checks"].append({"name": name, "ok": False, "detail": detail})
            return report

        try:
            envs = client.list_environments({"limit": 1})
            report["checks"].append(
                {
                    "name": "live_environment_list",
                    "ok": True,
                    "detail": f"environment list request succeeded ({len(envs.get('data', []))} item(s) returned)",
                }
            )
        except CliError as exc:
            report["checks"].append(
                {
                    "name": "live_environment_list",
                    "ok": False,
                    "detail": str(exc),
                }
            )
            report["ok"] = False

        try:
            sessions = client.list_sessions({"limit": 1})
            report["checks"].append(
                {
                    "name": "live_session_list",
                    "ok": True,
                    "detail": f"session list request succeeded ({len(sessions.get('data', []))} item(s) returned)",
                }
            )
        except CliError as exc:
            report["checks"].append(
                {
                    "name": "live_session_list",
                    "ok": False,
                    "detail": str(exc),
                }
            )
            report["ok"] = False

        try:
            files = client.list_files({"limit": 1})
            report["checks"].append(
                {
                    "name": "live_file_list",
                    "ok": True,
                    "detail": f"file list request succeeded ({len(files.get('data', []))} item(s) returned)",
                }
            )
        except CliError as exc:
            report["checks"].append(
                {
                    "name": "live_file_list",
                    "ok": False,
                    "detail": str(exc),
                }
            )
            report["ok"] = False

    return report


def handle_doctor(args: argparse.Namespace) -> None:
    _print_json(_doctor_checks(args))


def handle_environment_create(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.create_environment(_build_environment_payload(args)))


def handle_environment_update(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.update_environment(args.environment_id, _build_environment_payload(args)))


def handle_environment_get(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.retrieve_environment(args.environment_id))


def handle_environment_list(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    query = {"include_archived": args.include_archived, "limit": args.limit, "page": args.page}
    _print_json(client.list_environments(query))


def handle_environment_archive(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.archive_environment(args.environment_id))


def handle_environment_delete(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.delete_environment(args.environment_id))


def handle_file_upload(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    result = client.upload_file(args.file_path, filename=args.filename, mime_type=args.mime_type)
    if args.only_id:
        print(result["id"])
        return
    _print_json(result)


def handle_file_list(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    query = {"limit": args.limit, "after": args.after, "before": args.before, "scope_id": args.scope_id}
    _print_json(client.list_files(query))


def handle_file_download(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    output_path = Path(args.output).expanduser() if args.output else Path(args.file_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(client.download_file(args.file_id))
    print(str(output_path))


def handle_file_delete(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.delete_file(args.file_id))


def handle_session_create(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.create_session(_build_session_payload(args)))


def handle_session_get(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.retrieve_session(args.session_id))


def handle_session_list(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    query = {
        "agent_id": args.agent_id,
        "agent_version": args.agent_version,
        "include_archived": args.include_archived,
        "limit": args.limit,
        "page": args.page,
        "order": args.order,
        "created_at[gte]": args.created_after,
        "created_at[lte]": args.created_before,
    }
    _print_json(client.list_sessions(query))


def handle_session_archive(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.archive_session(args.session_id))


def handle_session_delete(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.delete_session(args.session_id))


def handle_session_send(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.send_events(args.session_id, _build_send_events(args)))


def handle_session_events(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    query = {"limit": args.limit, "page": args.page, "order": args.order}
    _print_json(client.list_events(args.session_id, query))


def handle_session_stream(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend="http", api_key_env=args.api_key_env, timeout=args.timeout)
    seen_event_ids: set[str] = set()
    if args.history_dedupe:
        history = client.list_events(args.session_id, {"order": "asc", "limit": args.history_limit})
        for event in history.get("data", []):
            event_id = event.get("id")
            if event_id:
                seen_event_ids.add(event_id)

    for event in client.stream_events(args.session_id):
        event_id = event.get("id")
        if event_id and event_id in seen_event_ids:
            continue
        if event_id:
            seen_event_ids.add(event_id)

        if args.jsonl:
            print(json.dumps(event))
        else:
            summary = _summarize_stream_event(event)
            if summary:
                print(summary, end="" if event.get("type") == "agent.message" else "\n")
            elif args.verbose:
                print(_json_dump(event))

        if event.get("type") == "session.status_idle" and args.until_idle:
            break
        if event.get("type") == "session.error" and args.stop_on_error:
            break


def handle_session_resource_add(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.add_session_resource(args.session_id, _build_resource_payload(args)))


def handle_session_resource_list(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    query = {"limit": args.limit, "after": args.after, "before": args.before}
    _print_json(client.list_session_resources(args.session_id, query))


def handle_session_resource_delete(args: argparse.Namespace) -> None:
    client = ManagedAgentsClient(backend=args.backend, api_key_env=args.api_key_env, timeout=args.timeout)
    _print_json(client.delete_session_resource(args.session_id, args.resource_id))



def _add_common_transport_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--backend", choices=["auto", "sdk", "http"], default="auto")
    parser.add_argument("--api-key-env", default="ANTHROPIC_API_KEY")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)


def _add_agent_mutation_args(parser: argparse.ArgumentParser, *, update: bool) -> None:
    if update:
        parser.add_argument("--version", required=True, type=int)
    parser.add_argument("--name")
    parser.add_argument("--model")
    parser.add_argument("--speed", choices=["standard", "fast"])
    parser.add_argument("--system")
    parser.add_argument("--clear-system", action="store_true")
    parser.add_argument("--description")
    parser.add_argument("--clear-description", action="store_true")
    parser.add_argument("--metadata-json")
    parser.add_argument("--agent-toolset", action="store_true")
    parser.add_argument("--default-tool-enabled", type=_parse_bool)
    parser.add_argument("--default-tool-policy", choices=["allow", "ask"])
    parser.add_argument("--enable-tool", action="append", default=[])
    parser.add_argument("--disable-tool", action="append", default=[])
    parser.add_argument("--tool-policy", action="append", default=[])
    parser.add_argument("--tool-json", action="append", default=[])
    parser.add_argument("--clear-tools", action="store_true")
    parser.add_argument("--mcp-server", action="append", default=[])
    parser.add_argument("--mcp-server-json", action="append", default=[])
    parser.add_argument("--clear-mcp-servers", action="store_true")
    parser.add_argument("--skill-ref", action="append", default=[])
    parser.add_argument("--skill-json", action="append", default=[])
    parser.add_argument("--clear-skills", action="store_true")
    parser.add_argument("--callable-agent-json", action="append", default=[])
    parser.add_argument("--clear-callable-agents", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Claude Managed Agents via SDK-first helper CLI")
    subparsers = parser.add_subparsers(dest="resource", required=True)

    agent = subparsers.add_parser("agent", help="Manage managed agents")
    agent_subparsers = agent.add_subparsers(dest="action", required=True)

    agent_create = agent_subparsers.add_parser("create", help="Create an agent")
    _add_common_transport_flags(agent_create)
    _add_agent_mutation_args(agent_create, update=False)
    agent_create.set_defaults(func=handle_agent_create)

    agent_update = agent_subparsers.add_parser("update", help="Update an agent")
    _add_common_transport_flags(agent_update)
    agent_update.add_argument("--agent-id", required=True)
    _add_agent_mutation_args(agent_update, update=True)
    agent_update.set_defaults(func=handle_agent_update)

    agent_get = agent_subparsers.add_parser("get", help="Retrieve an agent")
    _add_common_transport_flags(agent_get)
    agent_get.add_argument("--agent-id", required=True)
    agent_get.set_defaults(func=handle_agent_get)

    agent_list = agent_subparsers.add_parser("list", help="List agents")
    _add_common_transport_flags(agent_list)
    agent_list.add_argument("--include-archived", action="store_true")
    agent_list.add_argument("--limit", type=int)
    agent_list.add_argument("--page")
    agent_list.add_argument("--created-after")
    agent_list.add_argument("--created-before")
    agent_list.set_defaults(func=handle_agent_list)

    agent_versions = agent_subparsers.add_parser("versions", help="List agent versions")
    _add_common_transport_flags(agent_versions)
    agent_versions.add_argument("--agent-id", required=True)
    agent_versions.add_argument("--limit", type=int)
    agent_versions.add_argument("--page")
    agent_versions.set_defaults(func=handle_agent_versions)

    agent_archive = agent_subparsers.add_parser("archive", help="Archive an agent")
    _add_common_transport_flags(agent_archive)
    agent_archive.add_argument("--agent-id", required=True)
    agent_archive.set_defaults(func=handle_agent_archive)

    agent_delete = agent_subparsers.add_parser("delete", help="Delete an agent")
    _add_common_transport_flags(agent_delete)
    agent_delete.add_argument("--agent-id", required=True)
    agent_delete.set_defaults(func=handle_agent_delete)

    doctor = subparsers.add_parser("doctor", help="Run local preflight checks and optional live read-only API checks")
    _add_common_transport_flags(doctor)
    doctor.add_argument("--live", action="store_true", help="Run live read-only API checks against list endpoints")
    doctor.add_argument("--allowed-host", action="append", default=[], help="Validate one or more allowed-host values")
    doctor.set_defaults(func=handle_doctor)

    environment = subparsers.add_parser("environment", help="Manage environments")
    env_subparsers = environment.add_subparsers(dest="action", required=True)

    def add_environment_mutation_args(cmd: argparse.ArgumentParser, *, require_name: bool = False) -> None:
        _add_common_transport_flags(cmd)
        if require_name:
            cmd.add_argument("--name", required=True)
        else:
            cmd.add_argument("--name")
        cmd.add_argument("--description")
        cmd.add_argument("--metadata-json")
        cmd.add_argument("--config-json")
        cmd.add_argument("--network", choices=["unrestricted", "limited"])
        cmd.add_argument("--allowed-host", action="append", default=[])
        cmd.add_argument("--allow-mcp-servers", action="store_true")
        cmd.add_argument("--allow-package-managers", action="store_true")
        for field in ("apt", "cargo", "gem", "go", "npm", "pip"):
            cmd.add_argument(f"--{field}", action="append", default=[])

    env_create = env_subparsers.add_parser("create", help="Create an environment")
    add_environment_mutation_args(env_create, require_name=True)
    env_create.set_defaults(func=handle_environment_create)

    env_update = env_subparsers.add_parser("update", help="Update an environment")
    add_environment_mutation_args(env_update)
    env_update.add_argument("--environment-id", required=True)
    env_update.set_defaults(func=handle_environment_update)

    env_get = env_subparsers.add_parser("get", help="Retrieve an environment")
    _add_common_transport_flags(env_get)
    env_get.add_argument("--environment-id", required=True)
    env_get.set_defaults(func=handle_environment_get)

    env_list = env_subparsers.add_parser("list", help="List environments")
    _add_common_transport_flags(env_list)
    env_list.add_argument("--include-archived", action="store_true")
    env_list.add_argument("--limit", type=int)
    env_list.add_argument("--page")
    env_list.set_defaults(func=handle_environment_list)

    env_archive = env_subparsers.add_parser("archive", help="Archive an environment")
    _add_common_transport_flags(env_archive)
    env_archive.add_argument("--environment-id", required=True)
    env_archive.set_defaults(func=handle_environment_archive)

    env_delete = env_subparsers.add_parser("delete", help="Delete an environment")
    _add_common_transport_flags(env_delete)
    env_delete.add_argument("--environment-id", required=True)
    env_delete.set_defaults(func=handle_environment_delete)

    file_cmd = subparsers.add_parser("file", help="Upload Files API assets")
    file_subparsers = file_cmd.add_subparsers(dest="action", required=True)

    file_upload = file_subparsers.add_parser("upload", help="Upload a file and return its file_id")
    _add_common_transport_flags(file_upload)
    file_upload.add_argument("--file-path", required=True)
    file_upload.add_argument("--filename")
    file_upload.add_argument("--mime-type")
    file_upload.add_argument("--only-id", action="store_true")
    file_upload.set_defaults(func=handle_file_upload)

    file_list = file_subparsers.add_parser("list", help="List Files API objects")
    _add_common_transport_flags(file_list)
    file_list.add_argument("--limit", type=int)
    file_list.add_argument("--after")
    file_list.add_argument("--before")
    file_list.add_argument("--scope-id")
    file_list.set_defaults(func=handle_file_list)

    file_download = file_subparsers.add_parser("download", help="Download a file to disk")
    _add_common_transport_flags(file_download)
    file_download.add_argument("--file-id", required=True)
    file_download.add_argument("--output")
    file_download.set_defaults(func=handle_file_download)

    file_delete = file_subparsers.add_parser("delete", help="Delete a Files API object")
    _add_common_transport_flags(file_delete)
    file_delete.add_argument("--file-id", required=True)
    file_delete.set_defaults(func=handle_file_delete)

    session = subparsers.add_parser("session", help="Manage sessions and events")
    session_subparsers = session.add_subparsers(dest="action", required=True)

    session_create = session_subparsers.add_parser("create", help="Create a session")
    _add_common_transport_flags(session_create)
    session_create.add_argument("--agent-id")
    session_create.add_argument("--agent-version", type=int)
    session_create.add_argument("--agent-json")
    session_create.add_argument("--environment-id", required=True)
    session_create.add_argument("--title")
    session_create.add_argument("--metadata-json")
    session_create.add_argument("--vault-id", action="append", default=[])
    session_create.add_argument("--resource-json", action="append", default=[])
    session_create.set_defaults(func=handle_session_create)

    session_get = session_subparsers.add_parser("get", help="Retrieve a session")
    _add_common_transport_flags(session_get)
    session_get.add_argument("--session-id", required=True)
    session_get.set_defaults(func=handle_session_get)

    session_list = session_subparsers.add_parser("list", help="List sessions")
    _add_common_transport_flags(session_list)
    session_list.add_argument("--agent-id")
    session_list.add_argument("--agent-version", type=int)
    session_list.add_argument("--include-archived", action="store_true")
    session_list.add_argument("--limit", type=int)
    session_list.add_argument("--page")
    session_list.add_argument("--order", choices=["asc", "desc"])
    session_list.add_argument("--created-after")
    session_list.add_argument("--created-before")
    session_list.set_defaults(func=handle_session_list)

    session_archive = session_subparsers.add_parser("archive", help="Archive a session")
    _add_common_transport_flags(session_archive)
    session_archive.add_argument("--session-id", required=True)
    session_archive.set_defaults(func=handle_session_archive)

    session_delete = session_subparsers.add_parser("delete", help="Delete a session")
    _add_common_transport_flags(session_delete)
    session_delete.add_argument("--session-id", required=True)
    session_delete.set_defaults(func=handle_session_delete)

    session_send = session_subparsers.add_parser("send", help="Send session events")
    _add_common_transport_flags(session_send)
    session_send.add_argument("--session-id", required=True)
    session_send.add_argument("--event-json", action="append", default=[])
    session_send.add_argument("--message")
    session_send.add_argument("--interrupt", action="store_true")
    session_send.add_argument("--confirm-tool-use-id")
    session_send.add_argument("--confirm-result", choices=["allow", "deny"], default="allow")
    session_send.add_argument("--deny-message")
    session_send.add_argument("--custom-tool-use-id")
    session_send.add_argument("--custom-tool-text")
    session_send.add_argument("--custom-tool-is-error", action="store_true")
    session_send.set_defaults(func=handle_session_send)

    session_events = session_subparsers.add_parser("events", help="List session events")
    _add_common_transport_flags(session_events)
    session_events.add_argument("--session-id", required=True)
    session_events.add_argument("--limit", type=int)
    session_events.add_argument("--page")
    session_events.add_argument("--order", choices=["asc", "desc"], default="asc")
    session_events.set_defaults(func=handle_session_events)

    session_stream = session_subparsers.add_parser("stream", help="Stream live session events")
    _add_common_transport_flags(session_stream)
    session_stream.add_argument("--session-id", required=True)
    session_stream.add_argument("--jsonl", action="store_true")
    session_stream.add_argument("--verbose", action="store_true")
    session_stream.add_argument("--until-idle", action="store_true")
    session_stream.add_argument("--stop-on-error", action="store_true")
    session_stream.add_argument("--history-dedupe", action="store_true")
    session_stream.add_argument("--history-limit", type=int, default=200)
    session_stream.set_defaults(func=handle_session_stream)

    session_resource = session_subparsers.add_parser("resource", help="Manage session resources")
    session_resource_subparsers = session_resource.add_subparsers(dest="resource_action", required=True)

    session_resource_add = session_resource_subparsers.add_parser("add", help="Add a resource to a running session")
    _add_common_transport_flags(session_resource_add)
    session_resource_add.add_argument("--session-id", required=True)
    session_resource_add.add_argument("--type", choices=["file"], default="file")
    session_resource_add.add_argument("--file-id")
    session_resource_add.add_argument("--mount-path")
    session_resource_add.add_argument("--resource-json")
    session_resource_add.set_defaults(func=handle_session_resource_add)

    session_resource_list = session_resource_subparsers.add_parser("list", help="List session resources")
    _add_common_transport_flags(session_resource_list)
    session_resource_list.add_argument("--session-id", required=True)
    session_resource_list.add_argument("--limit", type=int)
    session_resource_list.add_argument("--after")
    session_resource_list.add_argument("--before")
    session_resource_list.set_defaults(func=handle_session_resource_list)

    session_resource_delete = session_resource_subparsers.add_parser("delete", help="Delete a session resource")
    _add_common_transport_flags(session_resource_delete)
    session_resource_delete.add_argument("--session-id", required=True)
    session_resource_delete.add_argument("--resource-id", required=True)
    session_resource_delete.set_defaults(func=handle_session_resource_delete)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except CliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
