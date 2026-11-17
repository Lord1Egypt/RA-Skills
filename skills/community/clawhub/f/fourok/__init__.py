from __future__ import annotations

import importlib.resources
from dataclasses import dataclass
from typing import Any

from opentelemetry import trace

from fourok.etl.extract.source_records import SourceRecord
from fourok.governance import GovernedContext
from fourok.governance.policy import PrincipalContext
from fourok.retrieval.api import RetrievalAPI

CLIENT_CAPABILITIES = ("retrieve", "open", "status", "onboard")
PACKAGE_NAME = "fourok-openclaw"


def client_capabilities() -> tuple[str, ...]:
    return CLIENT_CAPABILITIES


def skill_markdown() -> str:
    return _resource_text("SKILL.md")


def instructions_markdown() -> str:
    return _resource_text("instructions.md")


def readme_markdown() -> str:
    return _resource_text("README.md")


def skill_manifest() -> dict[str, object]:
    return {
        "name": PACKAGE_NAME,
        "display_name": "fourok Retrieval",
        "description": (
            "Source-backed company context retrieval for OpenClaw agents via the fourok CLI."
        ),
        "version": "0.1.0",
        "license": "MIT",
        "transport": "cli",
        "entrypoint": "SKILL.md",
        "instructions": "instructions.md",
        "capabilities": list(CLIENT_CAPABILITIES),
        "required_commands": ["fourok"],
        "recommended_commands": [
            "fourok status",
            "fourok retrieve <query> --json",
            "fourok open <source_ref>",
        ],
        "source_path": "src/fourok/retrieval/clients/openclaw",
    }


def package_files() -> dict[str, str]:
    return {
        "README.md": readme_markdown(),
        "SKILL.md": skill_markdown(),
        "instructions.md": instructions_markdown(),
    }


def _resource_text(name: str) -> str:
    return importlib.resources.files(__package__).joinpath(name).read_text(encoding="utf-8")


@dataclass(frozen=True)
class OpenClawMessage:
    session_id: str
    agent_id: str
    sender_id: str
    role: str
    content: str
    timestamp: str
    provider: str
    message_index: int


def capture_openclaw_messages(
    context: GovernedContext,
    messages: list[OpenClawMessage],
) -> list[SourceRecord]:
    records = openclaw_messages_to_source_records(messages)
    context.ingest_source_records(records)
    return records


class OpenClawSearchTools:
    def __init__(self, context: GovernedContext, principal: PrincipalContext) -> None:
        self._api = RetrievalAPI(context_factory=lambda *_args, **_kwargs: context)
        self._principal = principal

    def fourok_search_context(self, query: str, *, limit: int = 5) -> dict[str, object]:
        _validate_search_args(query, limit)
        return self._api.search_evidence(
            query,
            limit=limit,
            roles=self._principal.roles,
            human_id=self._principal.human_id,
            agent_id=self._principal.agent_id,
        )


def openclaw_tool_contracts() -> list[dict[str, object]]:
    return [
        {
            "name": "fourok_search_context",
            "description": (
                "Search governed company context and return permission-filtered evidence. "
                "Does not return hidden fields or inject context automatically."
            ),
            "input_schema": {
                "type": "object",
                "additionalProperties": False,
                "required": ["query"],
                "properties": {
                    "query": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Search query for governed context evidence.",
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 5,
                        "description": "Maximum number of primary evidence candidates.",
                    },
                },
            },
        }
    ]


def call_openclaw_tool(
    tools: OpenClawSearchTools,
    name: str,
    arguments: dict[str, Any],
) -> dict[str, object]:
    if name != "fourok_search_context":
        raise ValueError(f"unsupported OpenClaw fourok tool: {name}")
    query = arguments.get("query")
    limit = arguments.get("limit", 5)
    _validate_search_args(query, limit)
    return tools.fourok_search_context(str(query), limit=int(limit))


def _validate_search_args(query: object, limit: object) -> None:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("fourok_search_context.query must be a non-empty string")
    if not isinstance(limit, int) or limit < 1 or limit > 20:
        raise ValueError("fourok_search_context.limit must be between 1 and 20")


def openclaw_messages_to_source_records(messages: list[OpenClawMessage]) -> list[SourceRecord]:
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("fourok.openclaw.capture") as span:
        records = [_openclaw_message_to_source_record(message) for message in messages]
        span.set_attribute("fourok.openclaw.message_count", len(messages))
        span.set_attribute("fourok.openclaw.record_count", len(records))
        span.set_attribute(
            "fourok.openclaw.session_count",
            len({message.session_id for message in messages}),
        )
        return records


def _openclaw_message_to_source_record(message: OpenClawMessage) -> SourceRecord:
    source_ref = f"openclaw:session:{message.session_id}:message:{message.message_index:06d}"
    source_id = f"{message.session_id}:{message.message_index}"
    raw_ref = f"{source_ref}:raw"
    return SourceRecord(
        source_ref=source_ref,
        source_system="openclaw",
        source_id=source_id,
        record_type="message",
        title=f"OpenClaw {message.role} message in {message.session_id}",
        body=_strip_openclaw_boilerplate(message.content),
        occurred_at=message.timestamp,
        updated_at=message.timestamp,
        author_ref=message.sender_id,
        thread_ref=f"openclaw:session:{message.session_id}",
        identity_refs=(f"openclaw:sender:{message.sender_id}",) if message.sender_id else (),
        metadata={
            "session_id": message.session_id,
            "agent_id": message.agent_id,
            "sender_id": message.sender_id,
            "role": message.role,
            "provider": message.provider,
            "message_index": message.message_index,
            "source_object_type": "chat_message",
        },
        raw={
            "session_id": message.session_id,
            "agent_id": message.agent_id,
            "sender_id": message.sender_id,
            "role": message.role,
            "content": message.content,
            "timestamp": message.timestamp,
            "provider": message.provider,
            "message_index": message.message_index,
        },
        raw_ref=raw_ref,
    )


def _strip_openclaw_boilerplate(content: str) -> str:
    lines = content.splitlines()
    kept: list[str] = []
    skipping_untrusted_block = False
    for line in lines:
        if line.startswith("Conversation info (untrusted metadata):"):
            skipping_untrusted_block = True
            continue
        if skipping_untrusted_block and _looks_like_metadata_line(line):
            continue
        skipping_untrusted_block = False
        if _is_control_boilerplate(line):
            continue
        kept.append(line)
    return "\n".join(kept).strip()


def _looks_like_metadata_line(line: str) -> bool:
    if not line.strip():
        return True
    return "=" in line or ":" in line and len(line.split()) <= 4


def _is_control_boilerplate(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return stripped in {"HEARTBEAT_OK"} or stripped.startswith("<system-reminder>")
