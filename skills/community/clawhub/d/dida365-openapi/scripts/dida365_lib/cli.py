"""CLI entrypoint helpers for the Dida365 OpenAPI skill."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from dataclasses import replace
from typing import Any, Iterable, Optional, Sequence

from . import auth
from .client import Dida365Client
from .common import (
    compact_list,
    json_dumps,
    load_json_file,
    merge_json_object,
    omit_none,
    parse_bool,
    parse_json_text,
    redact_mapping,
)
from .config import (
    APP_DIR_NAME,
    CONFIG_FIELDS,
    RuntimeSettings,
    clear_token,
    resolve_runtime_settings,
    save_config,
    save_token,
)
from .errors import ApiError, UserFacingError
from .http import HttpResponse, HttpTransport

SECRET_OUTPUT_FIELDS = {"client_secret", "access_token", "refresh_token"}
STABLE_TASK_PRIORITY_VALUES = {0, 1, 3, 5}
PROJECT_KIND_VALUES = {"TASK", "NOTE"}
PROJECT_VIEW_MODE_VALUES = {"list", "kanban", "timeline"}
TASK_KIND_VALUES = {"TEXT", "NOTE"}
GRAY_AREA_REMINDER_VALUES = {"TRIGGER:-P1DT0H0M0S"}
SUPPORTED_DATETIME_FORMATS = (
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S.%f%z",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python scripts/dida365.py",
        description="Dida365 OpenAPI CLI",
    )

    subparsers = parser.add_subparsers(dest="command_group", required=True)

    auth_parser = subparsers.add_parser("auth", help="OAuth helpers")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command", required=True)
    _add_auth_parsers(auth_subparsers)

    project_parser = subparsers.add_parser("project", help="Project operations")
    project_subparsers = project_parser.add_subparsers(dest="project_command", required=True)
    _add_project_parsers(project_subparsers)

    task_parser = subparsers.add_parser("task", help="Task operations")
    task_subparsers = task_parser.add_subparsers(dest="task_command", required=True)
    _add_task_parsers(task_subparsers)

    return parser


def _add_common_runtime_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--client-id", help="OAuth client_id")
    parser.add_argument("--client-secret", help="OAuth client_secret")
    parser.add_argument("--redirect-uri", help="OAuth redirect URI")
    parser.add_argument("--scope", help="OAuth scope list")
    parser.add_argument("--access-token", help="Bearer token override")
    parser.add_argument("--auth-base-url", help="Auth base URL override")
    parser.add_argument("--api-base-url", help="API base URL override")
    parser.add_argument("--config-dir", help=f"Config directory, default {APP_DIR_NAME}")
    parser.add_argument("--timeout", type=float, help="HTTP timeout in seconds")


def _add_json_payload_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json-file", help="JSON payload file")
    parser.add_argument("--json", help="Inline JSON payload")


def _add_project_reference_arguments(
    parser: argparse.ArgumentParser,
    *,
    allow_repeated: bool = False,
    required: bool = False,
) -> None:
    action = "append" if allow_repeated else "store"
    parser.add_argument(
        "--project-id",
        action=action,
        required=required,
        help="Project ID",
    )
    parser.add_argument(
        "--project-name",
        action=action,
        help="Exact project name",
    )


def _add_auth_parsers(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("authorize-url", help="Build authorization URL")
    _add_common_runtime_arguments(parser)
    parser.add_argument("--state", help="OAuth state")
    parser.set_defaults(handler=handle_auth_authorize_url)

    parser = subparsers.add_parser("exchange-code", help="Exchange code for token")
    _add_common_runtime_arguments(parser)
    parser.add_argument("--code", required=True, help="Authorization code")
    parser.set_defaults(handler=handle_auth_exchange_code)

    parser = subparsers.add_parser("login-local", help="Listen for localhost callback")
    _add_common_runtime_arguments(parser)
    parser.add_argument("--state", help="OAuth state")
    parser.set_defaults(handler=handle_auth_login_local)

    parser = subparsers.add_parser("setup", help="Persist auth settings without logging in")
    _add_common_runtime_arguments(parser)
    parser.set_defaults(handler=handle_auth_setup)

    parser = subparsers.add_parser("status", help="Show config status")
    _add_common_runtime_arguments(parser)
    parser.set_defaults(handler=handle_auth_status)

    parser = subparsers.add_parser("clear-token", help="Delete cached token")
    _add_common_runtime_arguments(parser)
    parser.set_defaults(handler=handle_auth_clear_token)


def _add_project_parsers(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("list", help="List projects")
    _add_common_runtime_arguments(parser)
    parser.set_defaults(handler=handle_project_list)

    parser = subparsers.add_parser("get", help="Get one project")
    _add_common_runtime_arguments(parser)
    _add_project_reference_arguments(parser)
    parser.set_defaults(handler=handle_project_get)

    parser = subparsers.add_parser("data", help="Get project with data")
    _add_common_runtime_arguments(parser)
    _add_project_reference_arguments(parser)
    parser.set_defaults(handler=handle_project_data)

    parser = subparsers.add_parser("create", help="Create project")
    _add_common_runtime_arguments(parser)
    _add_json_payload_arguments(parser)
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--color", help="Project color")
    parser.add_argument("--sort-order", type=int, help="Sort order")
    parser.add_argument("--view-mode", help="Project view mode: list, kanban, timeline")
    parser.add_argument("--kind", help="Project kind: TASK or NOTE")
    parser.set_defaults(handler=handle_project_create)

    parser = subparsers.add_parser("update", help="Update project")
    _add_common_runtime_arguments(parser)
    _add_project_reference_arguments(parser)
    _add_json_payload_arguments(parser)
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--color", help="Project color")
    parser.add_argument("--sort-order", type=int, help="Sort order")
    parser.add_argument("--view-mode", help="Project view mode: list, kanban, timeline")
    parser.add_argument("--kind", help="Project kind: TASK or NOTE")
    parser.set_defaults(handler=handle_project_update)

    parser = subparsers.add_parser("delete", help="Delete project")
    _add_common_runtime_arguments(parser)
    _add_project_reference_arguments(parser)
    parser.set_defaults(handler=handle_project_delete)


def _add_task_mutation_arguments(parser: argparse.ArgumentParser) -> None:
    _add_json_payload_arguments(parser)
    parser.add_argument("--title", help="Task title")
    parser.add_argument("--content", help="Task content")
    parser.add_argument("--desc", help="Checklist description")
    parser.add_argument("--kind", help="Task kind: TEXT or NOTE")
    parser.add_argument("--is-all-day", type=parse_bool, help="All day true or false")
    parser.add_argument(
        "--start-date",
        help="Start datetime, format yyyy-MM-dd'T'HH:mm:ssZ",
    )
    parser.add_argument(
        "--due-date",
        help="Due datetime, format yyyy-MM-dd'T'HH:mm:ssZ",
    )
    parser.add_argument("--time-zone", help="Timezone")
    parser.add_argument("--repeat-flag", help="Repeat rule")
    parser.add_argument(
        "--priority",
        type=int,
        help="Task priority: 0=none, 1=low, 3=medium, 5=high",
    )
    parser.add_argument("--sort-order", type=int, help="Sort order")
    parser.add_argument("--reminders-json", help="Reminder array JSON")
    parser.add_argument("--tags-json", help="Tag array JSON")
    parser.add_argument(
        "--items-json",
        help="Checklist items JSON, item status 0=normal 1=completed",
    )


def _add_task_parsers(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("get", help="Get task")
    _add_common_runtime_arguments(parser)
    _add_project_reference_arguments(parser)
    parser.add_argument("--task-id", required=True, help="Task ID")
    parser.set_defaults(handler=handle_task_get)

    parser = subparsers.add_parser("create", help="Create task")
    _add_common_runtime_arguments(parser)
    _add_project_reference_arguments(parser)
    _add_task_mutation_arguments(parser)
    parser.set_defaults(handler=handle_task_create)

    parser = subparsers.add_parser("update", help="Update task")
    _add_common_runtime_arguments(parser)
    _add_project_reference_arguments(parser)
    _add_task_mutation_arguments(parser)
    parser.add_argument("--task-id", required=True, help="Task ID")
    parser.set_defaults(handler=handle_task_update)

    parser = subparsers.add_parser("complete", help="Complete task")
    _add_common_runtime_arguments(parser)
    _add_project_reference_arguments(parser)
    parser.add_argument("--task-id", required=True, help="Task ID")
    parser.set_defaults(handler=handle_task_complete)

    parser = subparsers.add_parser("delete", help="Delete task")
    _add_common_runtime_arguments(parser)
    _add_project_reference_arguments(parser)
    parser.add_argument("--task-id", required=True, help="Task ID")
    parser.set_defaults(handler=handle_task_delete)

    parser = subparsers.add_parser("move", help="Move task(s)")
    _add_common_runtime_arguments(parser)
    _add_json_payload_arguments(parser)
    parser.add_argument("--from-project-id", help="Source project ID")
    parser.add_argument("--from-project-name", help="Source project name")
    parser.add_argument("--to-project-id", help="Destination project ID")
    parser.add_argument("--to-project-name", help="Destination project name")
    parser.add_argument("--task-id", help="Task ID")
    parser.set_defaults(handler=handle_task_move)

    parser = subparsers.add_parser("completed", help="List completed tasks")
    _add_common_runtime_arguments(parser)
    _add_json_payload_arguments(parser)
    _add_project_reference_arguments(parser, allow_repeated=True)
    parser.add_argument(
        "--start-date",
        help="Start datetime, format yyyy-MM-dd'T'HH:mm:ssZ",
    )
    parser.add_argument(
        "--end-date",
        help="End datetime, format yyyy-MM-dd'T'HH:mm:ssZ",
    )
    parser.set_defaults(handler=handle_task_completed)

    parser = subparsers.add_parser("filter", help="Filter tasks")
    _add_common_runtime_arguments(parser)
    _add_json_payload_arguments(parser)
    _add_project_reference_arguments(parser, allow_repeated=True)
    parser.add_argument(
        "--start-date",
        help="Start datetime, format yyyy-MM-dd'T'HH:mm:ssZ",
    )
    parser.add_argument(
        "--end-date",
        help="End datetime, format yyyy-MM-dd'T'HH:mm:ssZ",
    )
    parser.add_argument(
        "--priority-json",
        help="Priority list JSON, values 0/1/3/5",
    )
    parser.add_argument("--tag-json", help="Tag list JSON")
    parser.add_argument(
        "--status-json",
        help="Task status list JSON, values 0=normal 2=completed",
    )
    parser.set_defaults(handler=handle_task_filter)


def runtime_overrides_from_args(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "client_id": getattr(args, "client_id", None),
        "client_secret": getattr(args, "client_secret", None),
        "redirect_uri": getattr(args, "redirect_uri", None),
        "scope": getattr(args, "scope", None),
        "access_token": getattr(args, "access_token", None),
        "auth_base_url": getattr(args, "auth_base_url", None),
        "api_base_url": getattr(args, "api_base_url", None),
        "config_dir": getattr(args, "config_dir", None),
        "timeout": getattr(args, "timeout", None),
    }


def load_runtime_settings(args: argparse.Namespace) -> RuntimeSettings:
    return resolve_runtime_settings(runtime_overrides_from_args(args))


def load_object_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if getattr(args, "json_file", None):
        payload = load_json_file(args.json_file, expected_type=dict)
    if getattr(args, "json", None):
        payload = merge_json_object(payload, parse_json_text(args.json, label="--json", expected_type=dict))
    return payload


def load_array_payload(args: argparse.Namespace) -> list[Any]:
    payload: list[Any] = []
    if getattr(args, "json_file", None):
        payload = load_json_file(args.json_file, expected_type=list)
    if getattr(args, "json", None):
        payload = parse_json_text(args.json, label="--json", expected_type=list)
    return payload


def parse_optional_json_array(value: Optional[str], *, label: str) -> Optional[list[Any]]:
    if value in (None, ""):
        return None
    return parse_json_text(value, label=label, expected_type=list)


def emit_response(response: HttpResponse | dict[str, Any], stdout: Any) -> None:
    if isinstance(response, HttpResponse):
        payload = response.data if response.data is not None else {"ok": True}
        sort_keys = False
    else:
        payload = response
        sort_keys = True
    stdout.write(json_dumps(payload, sort_keys=sort_keys) + "\n")


def emit_required_response(
    command_label: str,
    response: HttpResponse,
    stdout: Any,
    *,
    allow_empty_status_codes: Iterable[int] = (),
) -> None:
    allowed_status_codes = set(allow_empty_status_codes)
    if response.data is None and response.status_code not in allowed_status_codes:
        raise UserFacingError(
            f"{command_label} expected a JSON response body but the API returned no content",
            details={"status_code": response.status_code},
            exit_code=1,
        )
    emit_response(response, stdout)


def emit_error(error: UserFacingError, stderr: Any) -> None:
    stderr.write(json_dumps({"error": error.to_error_dict()}, sort_keys=True) + "\n")


def make_client(args: argparse.Namespace, *, transport: Optional[HttpTransport] = None) -> tuple[RuntimeSettings, Dida365Client]:
    settings = load_runtime_settings(args)
    return settings, Dida365Client(settings, transport=transport)


def resolve_project_ref(
    client: Dida365Client,
    *,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
) -> str:
    return client.resolve_project_id(
        project_id=project_id,
        project_name=project_name,
    )


def resolve_project_refs(
    client: Dida365Client,
    *,
    project_ids: Optional[Iterable[str]] = None,
    project_names: Optional[Iterable[str]] = None,
) -> Optional[list[str]]:
    resolved = list(project_ids or [])
    for project_name in project_names or []:
        resolved.append(client.resolve_project_id(project_name=project_name))
    resolved = compact_list([item for item in resolved if item])
    return resolved or None


def normalize_project_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)

    kind = normalized.get("kind")
    if kind is not None:
        if not isinstance(kind, str):
            raise UserFacingError("Project kind must be a string")
        normalized_kind = kind.upper()
        if normalized_kind not in PROJECT_KIND_VALUES:
            raise UserFacingError(
                "Project kind must be TASK or NOTE",
                details={"kind": kind},
            )
        normalized["kind"] = normalized_kind

    view_mode = normalized.get("viewMode")
    if view_mode is not None:
        if not isinstance(view_mode, str):
            raise UserFacingError("Project viewMode must be a string")
        normalized_view_mode = view_mode.lower()
        if normalized_view_mode not in PROJECT_VIEW_MODE_VALUES:
            raise UserFacingError(
                "Project viewMode must be list, kanban, or timeline",
                details={"viewMode": view_mode},
            )
        normalized["viewMode"] = normalized_view_mode

    return normalized


def validate_task_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)

    validate_optional_datetime_field(normalized, "startDate")
    validate_optional_datetime_field(normalized, "dueDate")

    kind = normalized.get("kind")
    if kind is not None:
        if not isinstance(kind, str):
            raise UserFacingError("Task kind must be a string")
        normalized_kind = kind.upper()
        if normalized_kind not in TASK_KIND_VALUES:
            raise UserFacingError(
                "Task kind must be TEXT or NOTE",
                details={
                    "kind": kind,
                    "hint": "Use checklist items instead of writing task kind CHECKLIST directly.",
                },
            )
        normalized["kind"] = normalized_kind

    tags = normalized.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            raise UserFacingError("Task tags must be a JSON array")
        if any(not isinstance(tag, str) for tag in tags):
            raise UserFacingError("Task tags must be an array of strings")

    priority = normalized.get("priority")
    if priority is not None and priority not in STABLE_TASK_PRIORITY_VALUES:
        raise UserFacingError(
            "Task priority must be one of 0, 1, 3, or 5",
            details={"priority": priority},
        )

    reminders = normalized.get("reminders")
    if reminders is not None:
        if not isinstance(reminders, list):
            raise UserFacingError("Task reminders must be a JSON array")
        gray_area_reminders = [value for value in reminders if value in GRAY_AREA_REMINDER_VALUES]
        if gray_area_reminders:
            raise UserFacingError(
                "This skill does not support gray-area reminder values",
                details={
                    "reminders": gray_area_reminders,
                    "hint": "Use TRIGGER:-PT1440M for a stable 1-day-early reminder.",
                },
            )

    repeat_flag = normalized.get("repeatFlag")
    if repeat_flag is not None:
        if not isinstance(repeat_flag, str):
            raise UserFacingError("Task repeatFlag must be a string")
        gray_area_repeat_reason = classify_gray_area_repeat_flag(repeat_flag)
        if gray_area_repeat_reason:
            raise UserFacingError(
                "This skill does not support gray-area repeat rules",
                details={"repeatFlag": repeat_flag, "reason": gray_area_repeat_reason},
            )
    return normalized


def validate_optional_datetime_field(mapping: dict[str, Any], field_name: str) -> None:
    value = mapping.get(field_name)
    if value in (None, ""):
        return
    if not isinstance(value, str):
        raise UserFacingError(f"{field_name} must be a date-time string")
    for pattern in SUPPORTED_DATETIME_FORMATS:
        try:
            datetime.strptime(value, pattern)
            return
        except ValueError:
            continue
    raise UserFacingError(
        f"{field_name} must use the documented date-time format",
        details={
            field_name: value,
            "accepted_examples": [
                "2019-11-13T03:00:00+0000",
                "2026-03-01T00:58:20.000+0000",
            ],
        },
    )


def classify_gray_area_repeat_flag(repeat_flag: str) -> Optional[str]:
    if not repeat_flag:
        return None

    parts = {}
    normalized_repeat_flag = repeat_flag
    if ":" in normalized_repeat_flag:
        prefix, remainder = normalized_repeat_flag.split(":", 1)
        if prefix in {"RRULE", "ERULE", "LUNAR"}:
            normalized_repeat_flag = remainder

    for item in normalized_repeat_flag.split(";"):
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        parts[key.upper()] = value

    if parts.get("FREQ") == "MONTHLY" and "BYDAY" in parts and "BYSETPOS" in parts and parts["BYSETPOS"] != "1":
        return "Monthly weekday BYSETPOS values other than 1 are gray-area behavior in the app."
    return None


def resolve_concrete_inbox_project_ref(client: Dida365Client, project_id: str) -> str:
    if project_id == "inbox":
        return client.resolve_concrete_inbox_project_id()
    return project_id


def normalize_project_ids_for_endpoint(
    client: Dida365Client,
    project_ids: Optional[Iterable[str]],
) -> Optional[list[str]]:
    if not project_ids:
        return None
    normalized = [resolve_concrete_inbox_project_ref(client, project_id) for project_id in project_ids]
    return compact_list(normalized) or None


def build_project_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_object_payload(args)
    overrides = omit_none(
        {
            "name": getattr(args, "name", None),
            "color": getattr(args, "color", None),
            "sortOrder": getattr(args, "sort_order", None),
            "viewMode": getattr(args, "view_mode", None),
            "kind": getattr(args, "kind", None),
        }
    )
    return normalize_project_payload(merge_json_object(payload, overrides))


def build_task_payload(
    args: argparse.Namespace,
    client: Dida365Client,
    *,
    require_project: bool,
) -> dict[str, Any]:
    payload = load_object_payload(args)
    project_id = resolve_project_ref(
        client,
        project_id=getattr(args, "project_id", None),
        project_name=getattr(args, "project_name", None),
    ) if getattr(args, "project_id", None) or getattr(args, "project_name", None) else payload.get("projectId")

    reminders = parse_optional_json_array(getattr(args, "reminders_json", None), label="--reminders-json")
    tags = parse_optional_json_array(getattr(args, "tags_json", None), label="--tags-json")
    items = parse_optional_json_array(getattr(args, "items_json", None), label="--items-json")

    overrides = omit_none(
        {
            "projectId": project_id,
            "title": getattr(args, "title", None),
            "content": getattr(args, "content", None),
            "desc": getattr(args, "desc", None),
            "kind": getattr(args, "kind", None),
            "isAllDay": getattr(args, "is_all_day", None),
            "startDate": getattr(args, "start_date", None),
            "dueDate": getattr(args, "due_date", None),
            "timeZone": getattr(args, "time_zone", None),
            "repeatFlag": getattr(args, "repeat_flag", None),
            "priority": getattr(args, "priority", None),
            "sortOrder": getattr(args, "sort_order", None),
            "reminders": reminders,
            "tags": tags,
            "items": items,
        }
    )
    payload = merge_json_object(payload, overrides)

    if require_project and not payload.get("projectId"):
        raise UserFacingError("projectId is required for this command")
    return validate_task_payload(payload)


def handle_auth_authorize_url(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del transport, stderr
    settings = load_runtime_settings(args)
    state = args.state or auth.generate_state_token()
    emit_response(
        {
            "authorize_url": auth.build_authorize_url(settings, state=state),
            "state": state,
            "redirect_uri": settings.redirect_uri,
            "scope": settings.scope,
        },
        stdout,
    )
    return 0


def handle_auth_exchange_code(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    settings = load_runtime_settings(args)
    token_response = auth.exchange_code(settings, code=args.code, transport=transport)
    save_config(settings)
    saved_token = save_token(settings, token_response)
    emit_response(
        {
            "ok": True,
            "config_file": str(settings.config_file),
            "token_file": str(settings.token_file),
            "token_response": redact_mapping(saved_token, SECRET_OUTPUT_FIELDS),
        },
        stdout,
    )
    return 0


def handle_auth_login_local(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    settings = load_runtime_settings(args)
    redirect_uri = settings.redirect_uri or "http://127.0.0.1:36500/callback"
    host, port, path, normalized_redirect_uri = auth.derive_local_redirect_uri(redirect_uri)
    state = args.state or auth.generate_state_token()
    settings = replace(settings, redirect_uri=normalized_redirect_uri)
    authorize_url = auth.build_authorize_url(settings, state=state)

    stderr.write(
        f"Open this URL in your browser and finish the Dida365 authorization flow:\n{authorize_url}\n"
    )

    callback_timeout = settings.timeout if settings.timeout > 30 else 300.0
    callback = auth.wait_for_local_callback(host=host, port=port, path=path, timeout=callback_timeout)
    if callback.state and callback.state != state:
        raise UserFacingError(
            "OAuth state mismatch",
            details={"expected": state, "received": callback.state},
            exit_code=1,
        )

    token_response = auth.exchange_code(settings, code=callback.code, transport=transport)
    save_config(settings)
    saved_token = save_token(settings, token_response)
    emit_response(
        {
            "ok": True,
            "authorize_url": authorize_url,
            "redirect_uri": normalized_redirect_uri,
            "token_file": str(settings.token_file),
            "token_response": redact_mapping(saved_token, SECRET_OUTPUT_FIELDS),
        },
        stdout,
    )
    return 0


def handle_auth_setup(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del transport, stderr
    settings = load_runtime_settings(args)
    saveable_fields = [
        field
        for field in CONFIG_FIELDS
        if settings.sources.get(field) not in {"unset", "default"}
    ]
    if not saveable_fields:
        raise UserFacingError(
            "Provide at least one auth setting to persist",
            details={"fields": list(CONFIG_FIELDS)},
        )

    saved_config = save_config(settings, fields=saveable_fields)
    emit_response(
        {
            "ok": True,
            "config_file": str(settings.config_file),
            "saved_fields": saveable_fields,
            "config": redact_mapping(saved_config, SECRET_OUTPUT_FIELDS),
        },
        stdout,
    )
    return 0


def build_auth_status_diagnostics(settings: RuntimeSettings) -> list[str]:
    diagnostics: list[str] = []

    if not settings.config_file.exists():
        diagnostics.append("No persisted config file found. Run auth setup first if you want to save app settings.")

    if not settings.client_id or not settings.client_secret:
        diagnostics.append("Missing OAuth client settings. Run auth setup first or pass --client-id and --client-secret.")

    if settings.token_file.exists() and not settings.token_data.get("access_token"):
        diagnostics.append("Token file exists but does not contain a usable access token.")
    elif not settings.access_token:
        diagnostics.append("No access token available. Run auth login-local or auth exchange-code.")

    return diagnostics


def handle_auth_status(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del transport, stderr
    settings = load_runtime_settings(args)
    emit_response(
        {
            "config_dir": str(settings.config_dir),
            "config_file": str(settings.config_file),
            "token_file": str(settings.token_file),
            "config_file_exists": settings.config_file.exists(),
            "token_file_exists": settings.token_file.exists(),
            "sources": settings.sources,
            "settings": settings.redacted_status(),
            "stored_config": redact_mapping(settings.config_data, SECRET_OUTPUT_FIELDS),
            "stored_token": redact_mapping(settings.token_data, SECRET_OUTPUT_FIELDS),
            "diagnostics": build_auth_status_diagnostics(settings),
        },
        stdout,
    )
    return 0


def handle_auth_clear_token(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del transport, stderr
    settings = load_runtime_settings(args)
    removed = clear_token(settings)
    emit_response(
        {
            "ok": True,
            "removed": removed,
            "token_file": str(settings.token_file),
        },
        stdout,
    )
    return 0


def handle_project_list(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    emit_required_response("project list", client.list_projects(), stdout)
    return 0


def handle_project_get(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    project_id = resolve_project_ref(client, project_id=args.project_id, project_name=args.project_name)
    if project_id == "inbox" or project_id.startswith("inbox"):
        raise UserFacingError(
            "project get is not reliable for inbox. Use project data --project-id inbox instead.",
            details={"project_id": project_id},
        )
    emit_required_response("project get", client.get_project(project_id), stdout)
    return 0


def handle_project_data(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    project_id = resolve_project_ref(
        client,
        project_id=args.project_id,
        project_name=args.project_name,
    )
    emit_required_response("project data", client.get_project_data(project_id), stdout)
    return 0


def handle_project_create(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    payload = build_project_payload(args)
    if not payload.get("name"):
        raise UserFacingError("Project name is required for project create")
    emit_required_response("project create", client.create_project(payload), stdout, allow_empty_status_codes=(201,))
    return 0


def handle_project_update(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    project_id = resolve_project_ref(client, project_id=args.project_id, project_name=args.project_name)
    emit_required_response(
        "project update",
        client.update_project(project_id, build_project_payload(args)),
        stdout,
        allow_empty_status_codes=(201,),
    )
    return 0


def handle_project_delete(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    project_id = resolve_project_ref(client, project_id=args.project_id, project_name=args.project_name)
    emit_response(client.delete_project(project_id), stdout)
    return 0


def handle_task_get(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    project_id = resolve_project_ref(client, project_id=args.project_id, project_name=args.project_name)
    emit_required_response("task get", client.get_task(project_id, args.task_id), stdout)
    return 0


def handle_task_create(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    payload = build_task_payload(args, client, require_project=True)
    if not payload.get("title"):
        raise UserFacingError("Task title is required for task create")
    emit_required_response("task create", client.create_task(payload), stdout, allow_empty_status_codes=(201,))
    return 0


def handle_task_update(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    payload = build_task_payload(args, client, require_project=False)
    existing_id = payload.get("id")
    if existing_id and str(existing_id) != args.task_id:
        raise UserFacingError(
            "Body id must match --task-id",
            details={"task_id": args.task_id, "body_id": str(existing_id)},
        )
    payload["id"] = args.task_id
    if not payload.get("projectId"):
        raise UserFacingError("projectId is required for task update")
    emit_required_response("task update", client.update_task(args.task_id, payload), stdout, allow_empty_status_codes=(201,))
    return 0


def handle_task_complete(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    project_id = resolve_project_ref(client, project_id=args.project_id, project_name=args.project_name)
    emit_response(client.complete_task(project_id, args.task_id), stdout)
    return 0


def handle_task_delete(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    project_id = resolve_project_ref(client, project_id=args.project_id, project_name=args.project_name)
    project_id = resolve_concrete_inbox_project_ref(client, project_id)
    emit_response(client.delete_task(project_id, args.task_id), stdout)
    return 0


def handle_task_move(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    operations = load_array_payload(args)
    if not operations:
        from_project_id = resolve_project_ref(
            client,
            project_id=args.from_project_id,
            project_name=args.from_project_name,
        )
        to_project_id = resolve_project_ref(
            client,
            project_id=args.to_project_id,
            project_name=args.to_project_name,
        )
        if not args.task_id:
            raise UserFacingError("task-id is required when not using --json or --json-file")
        operations = [
            {
                "fromProjectId": from_project_id,
                "toProjectId": to_project_id,
                "taskId": args.task_id,
            }
        ]
    for operation in operations:
        if not isinstance(operation, dict):
            raise UserFacingError("task move payload entries must be JSON objects")
        if "fromProjectId" in operation:
            operation["fromProjectId"] = resolve_concrete_inbox_project_ref(client, str(operation["fromProjectId"]))
        if "toProjectId" in operation:
            operation["toProjectId"] = resolve_concrete_inbox_project_ref(client, str(operation["toProjectId"]))
    emit_required_response("task move", client.move_task(operations), stdout, allow_empty_status_codes=(201,))
    return 0


def handle_task_completed(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    payload = load_object_payload(args)
    project_ids = resolve_project_refs(
        client,
        project_ids=args.project_id,
        project_names=args.project_name,
    )
    if "projectIds" in payload and isinstance(payload["projectIds"], list):
        payload["projectIds"] = normalize_project_ids_for_endpoint(
            client,
            [str(project_id) for project_id in payload["projectIds"]],
        )
    overrides = omit_none(
        {
            "projectIds": normalize_project_ids_for_endpoint(client, project_ids),
            "startDate": args.start_date,
            "endDate": args.end_date,
        }
    )
    merged_payload = merge_json_object(payload, overrides)
    validate_optional_datetime_field(merged_payload, "startDate")
    validate_optional_datetime_field(merged_payload, "endDate")
    emit_required_response(
        "task completed",
        client.list_completed_tasks(merged_payload),
        stdout,
        allow_empty_status_codes=(201,),
    )
    return 0


def handle_task_filter(
    args: argparse.Namespace,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    del stderr
    _, client = make_client(args, transport=transport)
    payload = load_object_payload(args)
    project_ids = resolve_project_refs(
        client,
        project_ids=args.project_id,
        project_names=args.project_name,
    )
    if "projectIds" in payload and isinstance(payload["projectIds"], list):
        payload["projectIds"] = normalize_project_ids_for_endpoint(
            client,
            [str(project_id) for project_id in payload["projectIds"]],
        )
    overrides = omit_none(
        {
            "projectIds": normalize_project_ids_for_endpoint(client, project_ids),
            "startDate": args.start_date,
            "endDate": args.end_date,
            "priority": parse_optional_json_array(args.priority_json, label="--priority-json"),
            "tag": parse_optional_json_array(args.tag_json, label="--tag-json"),
            "status": parse_optional_json_array(args.status_json, label="--status-json"),
        }
    )
    merged_payload = merge_json_object(payload, overrides)
    validate_optional_datetime_field(merged_payload, "startDate")
    validate_optional_datetime_field(merged_payload, "endDate")
    emit_required_response(
        "task filter",
        client.filter_tasks(merged_payload),
        stdout,
        allow_empty_status_codes=(201,),
    )
    return 0


def main(
    argv: Optional[Sequence[str]] = None,
    *,
    transport: Optional[HttpTransport] = None,
    stdout: Any = sys.stdout,
    stderr: Any = sys.stderr,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args, transport=transport, stdout=stdout, stderr=stderr)
    except ApiError as exc:
        emit_error(exc, stderr)
        return exc.exit_code
    except UserFacingError as exc:
        emit_error(exc, stderr)
        return exc.exit_code
    except ValueError as exc:
        emit_error(UserFacingError(str(exc)), stderr)
        return 2
