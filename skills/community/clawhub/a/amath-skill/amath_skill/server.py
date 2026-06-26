from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import AmathApiError, client
from .config import settings
from .models import ApiEnvelope, AuthResult, SessionTokenState

mcp = FastMCP(settings.server_name)


def _wrap(endpoint: str, data: Any) -> dict[str, Any]:
    return ApiEnvelope(endpoint=endpoint, data=data).model_dump()


def _normalize_error(exc: Exception) -> RuntimeError:
    if isinstance(exc, AmathApiError):
        return RuntimeError(str(exc))
    return RuntimeError(f"Skill execution failed: {exc}")


@mcp.tool()
async def amath_healthcheck() -> dict[str, Any]:
    """Check whether the amath backend is reachable."""
    try:
        data = await client.request("GET", "/health")
        return _wrap("GET /health", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def auth_login(username: str, password: str, persist: bool = True) -> dict[str, Any]:
    """Log in with username/email/phone and password, then optionally persist the bearer token."""
    try:
        data = await client.request(
            "POST",
            "/auth/login",
            json_body={"username": username, "password": password},
        )
        token = data.get("access_token") if isinstance(data, dict) else None
        persisted = bool(token and persist and settings.auto_persist_token)
        if persisted:
            client.set_token(token)
        result = AuthResult(
            access_token=token or "",
            token_type=(data or {}).get("token_type", "bearer") if isinstance(data, dict) else "bearer",
            persisted=persisted,
        )
        return _wrap("POST /auth/login", result.model_dump())
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def auth_me(token: str | None = None) -> dict[str, Any]:
    """Fetch the current authenticated user profile."""
    try:
        data = await client.request("GET", "/auth/users/me", token=token)
        return _wrap("GET /auth/users/me", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def auth_clear_session() -> dict[str, Any]:
    """Clear the persisted bearer token stored by this skill process."""
    client.clear_token()
    return _wrap(
        "local/session/clear",
        SessionTokenState(has_token=False, token_preview=None).model_dump(),
    )


@mcp.tool()
async def auth_session_state() -> dict[str, Any]:
    """Show whether a bearer token is currently stored in this skill process."""
    return _wrap(
        "local/session/state",
        SessionTokenState(has_token=client.has_token(), token_preview=client.get_token_preview()).model_dump(),
    )


@mcp.tool()
async def curriculum_get_system_tree(system_name: str = settings.default_system_name) -> dict[str, Any]:
    """Fetch the curriculum tree by system name. Default is 奥数探险课."""
    try:
        data = await client.request("GET", f"/curriculum/system/name/{system_name}/tree")
        return _wrap("GET /curriculum/system/name/{system_name}/tree", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def curriculum_get_topic(topic_id: int) -> dict[str, Any]:
    """Fetch full topic detail, including breadcrumb and quest problems."""
    try:
        data = await client.request("GET", f"/curriculum/topic/{topic_id}")
        return _wrap("GET /curriculum/topic/{topic_id}", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def knowledge_curriculum_guide() -> dict[str, Any]:
    """Fetch the knowledge curriculum guide used by the adventure-style course page."""
    try:
        data = await client.request("GET", "/knowledge/curriculum-guide")
        return _wrap("GET /knowledge/curriculum-guide", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def question_get_problem(problem_id: str) -> dict[str, Any]:
    """Fetch a single problem from the question bank."""
    try:
        data = await client.request("GET", f"/question-bank/problems/{problem_id}")
        return _wrap("GET /question-bank/problems/{problem_id}", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def question_recommended(
    limit: int = 10,
    difficulty: int | None = None,
    problem_type: str | None = None,
    lecture: str | None = None,
    topic_id: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Fetch recommended problems, optionally personalized when a bearer token is available."""
    try:
        data = await client.request(
            "GET",
            "/question-bank/recommended",
            params={
                "limit": limit,
                "difficulty": difficulty,
                "problem_type": problem_type,
                "lecture": lecture,
                "topic_id": topic_id,
            },
            token=token,
        )
        return _wrap("GET /question-bank/recommended", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def chat_start_session(
    user_id: str,
    problem_id: str | None = None,
    mode: str = "LECTURE",
    script_json: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Start a Socratic chat session from a problem or a full script JSON payload."""
    try:
        if not problem_id and not script_json:
            raise RuntimeError("Either problem_id or script_json is required")
        data = await client.request(
            "POST",
            "/chat/start",
            json_body={
                "user_id": user_id,
                "problem_id": problem_id,
                "mode": mode,
                "script_json": script_json,
            },
        )
        return _wrap("POST /chat/start", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def chat_send_message(session_id: str, user_input: str, direct_submit: bool = False) -> dict[str, Any]:
    """Send a learner message to an active Socratic chat session."""
    try:
        data = await client.request(
            "POST",
            "/chat/interact",
            json_body={
                "session_id": session_id,
                "user_input": user_input,
                "direct_submit": direct_submit,
            },
        )
        return _wrap("POST /chat/interact", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def chat_submit_mcq(session_id: str, option_id: str) -> dict[str, Any]:
    """Submit a multiple-choice answer inside an active Socratic chat session."""
    try:
        data = await client.request(
            "POST",
            "/chat/mcq-answer",
            json_body={"session_id": session_id, "option_id": option_id},
        )
        return _wrap("POST /chat/mcq-answer", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def chat_hint(session_id: str) -> dict[str, Any]:
    """Trigger a hint for an active Socratic chat session."""
    try:
        data = await client.request("POST", "/chat/hint", json_body={"session_id": session_id})
        return _wrap("POST /chat/hint", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def chat_get_session(session_id: str) -> dict[str, Any]:
    """Fetch chat session status and progress."""
    try:
        data = await client.request("GET", f"/chat/session/{session_id}")
        return _wrap("GET /chat/session/{session_id}", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def quiz_start(
    mode: str,
    topic_id: str | None = None,
    lecture: str | None = None,
    difficulty_min: int = 1,
    difficulty_max: int = 5,
    limit: int = 10,
    time_limit: int = 900,
    token: str | None = None,
) -> dict[str, Any]:
    """Start a quiz session. Requires an authenticated bearer token."""
    try:
        data = await client.request(
            "POST",
            "/quiz/start",
            json_body={
                "mode": mode,
                "topic_id": topic_id,
                "lecture": lecture,
                "difficulty_min": difficulty_min,
                "difficulty_max": difficulty_max,
                "limit": limit,
                "time_limit": time_limit,
            },
            token=token,
        )
        return _wrap("POST /quiz/start", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def quiz_answer(
    session_id: str,
    question_id: str,
    selected_option: str,
    time_spent: int | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Persist or update an answer for one quiz question."""
    try:
        data = await client.request(
            "PATCH",
            "/quiz/answer",
            json_body={
                "session_id": session_id,
                "question_id": question_id,
                "selected_option": selected_option,
                "time_spent": time_spent,
            },
            token=token,
        )
        return _wrap("PATCH /quiz/answer", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def quiz_submit(session_id: str, time_used: int | None = None, token: str | None = None) -> dict[str, Any]:
    """Submit a quiz session and receive server-side scoring."""
    try:
        data = await client.request(
            "POST",
            "/quiz/submit",
            json_body={"session_id": session_id, "time_used": time_used},
            token=token,
        )
        return _wrap("POST /quiz/submit", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def quiz_active(token: str | None = None) -> dict[str, Any]:
    """Fetch the current user's active quiz session, if any."""
    try:
        data = await client.request("GET", "/quiz/active", token=token)
        return _wrap("GET /quiz/active", data)
    except Exception as exc:
        raise _normalize_error(exc)


@mcp.tool()
async def quiz_history(
    limit: int = 20,
    offset: int = 0,
    mode: str | None = None,
    lecture: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """Fetch quiz history for the authenticated user."""
    try:
        data = await client.request(
            "GET",
            "/quiz/history",
            params={"limit": limit, "offset": offset, "mode": mode, "lecture": lecture},
            token=token,
        )
        return _wrap("GET /quiz/history", data)
    except Exception as exc:
        raise _normalize_error(exc)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
