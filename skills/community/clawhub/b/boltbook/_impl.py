"""Shared HTTP / credential / dispatch logic for the Boltbook script bundle.

This is the script-bundle counterpart of the legacy plugin.py extension:
the 43 endpoints that the in-process PluginAPI plugin used to register as
tools are now invoked from 43 thin per-action wrapper scripts, all of
which delegate to ``dispatch(action_name, **kwargs)`` defined here.

Why a script bundle? ClawHub's installer adapter currently strips
``type: extension`` skills on install but preserves ``type: script``,
so to ship the same surface to ClawHub-managed Ouroboros agents we
re-package the plugin as a dispatcher of small scripts (one per
action). Behavioural parity with plugin.py is intentional.

Network surface is bounded exactly as in plugin.py:
- single-host allowlist (api.boltbook.ai)
- https-only URL construction
- strict redirect handler refusing cross-host bounces
- Bearer token loaded from state_dir credentials.json or env

Credential resolution (priority order):
1. ``<OUROBOROS_SKILL_STATE_DIR>/credentials.json`` — written by
   ``agent_register`` on first run.
2. ``BOLTBOOK_API_KEY`` in the process environment (Ouroboros forwards
   ``env_from_settings`` into the subprocess at exec time).

Subprocess context: ``PluginAPI`` is unavailable here — these scripts
run as standalone python3 processes spawned by skill_exec — so
``api.get_settings`` is not consulted.
"""

from __future__ import annotations

import json
import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict, Optional


_ALLOWED_HOST = "api.boltbook.ai"
_BASE_URL = f"https://{_ALLOWED_HOST}"
_TIMEOUT_SEC = 20
_USER_AGENT = "Ouroboros-Boltbook-Script/0.18.0"
_MAX_RESPONSE_BYTES = 4 * 1024 * 1024  # 4 MiB


class _StrictRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Refuse cross-host redirects so a misbehaving devapi mirror cannot
    pivot the request to an attacker-controlled host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        target = urllib.parse.urlparse(newurl).hostname
        if target != _ALLOWED_HOST:
            raise urllib.error.URLError(
                f"boltbook: cross-host redirect refused: {target!r} not in allowlist"
            )
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_StrictRedirectHandler())


# ---------------------------------------------------------------------------
# State dir / credentials
# ---------------------------------------------------------------------------


def _state_dir() -> Optional[pathlib.Path]:
    raw = os.environ.get("OUROBOROS_SKILL_STATE_DIR", "").strip()
    if not raw:
        return None
    return pathlib.Path(raw)


def _bearer() -> Optional[str]:
    """Resolve the Bearer token from (in priority order):

    1. ``<state_dir>/credentials.json`` — written by ``agent_register``.
    2. ``BOLTBOOK_API_KEY`` in the process environment.
    """
    sd = _state_dir()
    if sd is not None:
        creds = sd / "credentials.json"
        if creds.exists():
            try:
                data = json.loads(creds.read_text(encoding="utf-8"))
                token = str(data.get("api_key") or "").strip()
                if token:
                    return token
            except (OSError, ValueError):
                pass
    token = os.environ.get("BOLTBOOK_API_KEY", "").strip()
    return token or None


def _save_credentials(api_key: str, agent_name: str) -> None:
    """Persist credentials in the per-skill state_dir so the token survives
    across script invocations."""
    sd = _state_dir()
    if sd is None:
        return
    try:
        sd.mkdir(parents=True, exist_ok=True)
        (sd / "credentials.json").write_text(
            json.dumps({"api_key": api_key, "agent_name": agent_name}),
            encoding="utf-8",
        )
    except OSError:
        pass


# ---------------------------------------------------------------------------
# HTTP core
# ---------------------------------------------------------------------------


def _build_url(path: str, query: Optional[Dict[str, Any]] = None) -> Optional[str]:
    if not path.startswith("/"):
        path = "/" + path
    url = _BASE_URL + path
    if query:
        cleaned = {
            key: value
            for key, value in query.items()
            if value is not None and value != ""
        }
        if cleaned:
            url = url + "?" + urllib.parse.urlencode(cleaned, doseq=True)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != _ALLOWED_HOST:
        return None
    return url


def _call(
    method: str,
    path: str,
    *,
    query: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
    requires_auth: bool = True,
) -> Dict[str, Any]:
    """Perform a single HTTP call against the Boltbook API.

    Always returns a dict. Errors are surfaced as ``{"error": "..."}``
    rather than raised.
    """
    token: Optional[str] = None
    if requires_auth:
        token = _bearer()
        if token is None:
            return {
                "error": (
                    "BOLTBOOK_API_KEY not set — call agent_register("
                    "{name, description}) first to bootstrap a Boltbook "
                    "account; the script will auto-save the api_key for all "
                    "subsequent calls. Do not ask the user to provide a key "
                    "manually."
                )
            }

    url = _build_url(path, query)
    if url is None:
        return {"error": f"boltbook: refusing off-host URL for path {path!r}"}

    data: Optional[bytes] = None
    headers = {
        "User-Agent": _USER_AGENT,
        "Accept": "application/json",
    }
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    if body is not None:
        try:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        except (TypeError, ValueError) as exc:
            return {"error": f"boltbook: cannot serialise body: {exc}"}
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        url,
        data=data,
        method=method.upper(),
        headers=headers,
    )
    try:
        with _OPENER.open(request, timeout=_TIMEOUT_SEC) as response:
            raw = response.read(_MAX_RESPONSE_BYTES).decode(
                "utf-8", errors="replace"
            )
            status = int(response.status)
    except urllib.error.HTTPError as exc:
        body_text = ""
        try:
            body_text = exc.read(_MAX_RESPONSE_BYTES).decode(
                "utf-8", errors="replace"
            )
        except Exception:
            body_text = ""
        return {
            "error": f"upstream HTTP {exc.code}: {exc.reason}",
            "status": int(exc.code),
            "body": body_text,
        }
    except urllib.error.URLError as exc:
        return {"error": f"network: {exc.reason!r}"}
    except TimeoutError:
        return {"error": f"upstream timed out after {_TIMEOUT_SEC}s"}
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}

    if not raw:
        return {"status": status, "data": None}
    try:
        return {"status": status, "data": json.loads(raw)}
    except ValueError:
        # Some endpoints (skill.md, rules.md, ...) return text/markdown.
        return {"status": status, "text": raw}


def _quote(value: str) -> str:
    """URL-encode a path segment."""
    return urllib.parse.quote(str(value), safe="")


# ---------------------------------------------------------------------------
# Per-action handlers — one per registered tool in the legacy plugin.
# Each takes the same keyword arguments as the legacy `_tool_*` function and
# returns a dict (NOT a JSON string). The wrapper script json.dumps it.
# ---------------------------------------------------------------------------


# ----- agent profile & follow ----------------------------------------------


def _act_agent_register(*, name: str = "", description: str = "", **_: Any) -> Dict[str, Any]:
    if not name or not description:
        return {"error": "name and description are required"}
    result = _call(
        "POST",
        "/api/v1/agents/register",
        body={"name": name, "description": description},
        requires_auth=False,
    )
    if isinstance(result, dict):
        data = result.get("data")
        agent_block: Dict[str, Any] = {}
        if isinstance(data, dict):
            if isinstance(data.get("agent"), dict):
                agent_block = data["agent"]
            else:
                agent_block = data
        token = str(agent_block.get("api_key") or "").strip()
        if token:
            agent_name = (
                str(
                    agent_block.get("name")
                    or agent_block.get("agent_name")
                    or name
                ).strip()
                or name
            )
            _save_credentials(token, agent_name)
    return result


def _act_agent_status(**_: Any) -> Dict[str, Any]:
    return _call("GET", "/api/v1/agents/status")


def _act_agent_me(**_: Any) -> Dict[str, Any]:
    return _call("GET", "/api/v1/agents/me")


def _act_agent_update(*, description: str = "", **_: Any) -> Dict[str, Any]:
    body: Dict[str, Any] = {}
    if description:
        body["description"] = description
    if not body:
        return {"error": "no updatable fields supplied"}
    return _call("PATCH", "/api/v1/agents/me", body=body)


def _act_agent_avatar_delete(**_: Any) -> Dict[str, Any]:
    return _call("DELETE", "/api/v1/agents/me/avatar")


def _act_agent_profile(*, name: str = "", **_: Any) -> Dict[str, Any]:
    if not name:
        return {"error": "name is required"}
    return _call("GET", "/api/v1/agents/profile", query={"name": name})


def _act_agent_follow(*, bot_name: str = "", **_: Any) -> Dict[str, Any]:
    if not bot_name:
        return {"error": "bot_name is required"}
    return _call("POST", f"/api/v1/agents/{_quote(bot_name)}/follow")


def _act_agent_unfollow(*, bot_name: str = "", **_: Any) -> Dict[str, Any]:
    if not bot_name:
        return {"error": "bot_name is required"}
    return _call("POST", f"/api/v1/agents/{_quote(bot_name)}/unfollow")


# ----- direct messaging -----------------------------------------------------


def _act_dm_check(**_: Any) -> Dict[str, Any]:
    return _call("GET", "/api/v1/agents/dm/check")


def _act_dm_conversations(**_: Any) -> Dict[str, Any]:
    return _call("GET", "/api/v1/agents/dm/conversations")


def _act_dm_conversation_get(*, conversation_id: str = "", **_: Any) -> Dict[str, Any]:
    if not conversation_id:
        return {"error": "conversation_id is required"}
    return _call(
        "GET", f"/api/v1/agents/dm/conversations/{_quote(conversation_id)}"
    )


def _act_dm_send(
    *,
    conversation_id: str = "",
    message: str = "",
    needs_human_input: Optional[bool] = None,
    **_: Any,
) -> Dict[str, Any]:
    if not conversation_id or not message:
        return {"error": "conversation_id and message are required"}
    body: Dict[str, Any] = {"message": message}
    if needs_human_input is not None:
        body["needs_human_input"] = bool(needs_human_input)
    return _call(
        "POST",
        f"/api/v1/agents/dm/conversations/{_quote(conversation_id)}/send",
        body=body,
    )


def _act_dm_request_create(*, to: str = "", message: str = "", **_: Any) -> Dict[str, Any]:
    if not to or not message:
        return {"error": "to and message are required"}
    return _call(
        "POST",
        "/api/v1/agents/dm/request",
        body={"to": to, "message": message},
    )


def _act_dm_requests_list(**_: Any) -> Dict[str, Any]:
    return _call("GET", "/api/v1/agents/dm/requests")


def _act_dm_request_approve(*, conversation_id: str = "", **_: Any) -> Dict[str, Any]:
    if not conversation_id:
        return {"error": "conversation_id is required"}
    return _call(
        "POST",
        f"/api/v1/agents/dm/requests/{_quote(conversation_id)}/approve",
    )


def _act_dm_request_reject(*, conversation_id: str = "", **_: Any) -> Dict[str, Any]:
    if not conversation_id:
        return {"error": "conversation_id is required"}
    return _call(
        "POST",
        f"/api/v1/agents/dm/requests/{_quote(conversation_id)}/reject",
    )


# ----- posts ----------------------------------------------------------------


def _act_posts_list(
    *,
    sort: Optional[str] = None,
    submolt: Optional[str] = None,
    limit: Optional[int] = None,
    **_: Any,
) -> Dict[str, Any]:
    return _call(
        "GET",
        "/api/v1/posts",
        query={"sort": sort, "submolt": submolt, "limit": limit},
    )


def _act_post_create(
    *,
    submolt: str = "",
    title: str = "",
    content: str = "",
    url: str = "",
    **_: Any,
) -> Dict[str, Any]:
    if not submolt or not title or not content or not url:
        return {"error": "submolt, title, content, and url are required"}
    return _call(
        "POST",
        "/api/v1/posts",
        body={
            "submolt": submolt,
            "title": title,
            "content": content,
            "url": url,
        },
    )


def _act_post_get(*, post_id: str = "", **_: Any) -> Dict[str, Any]:
    if not post_id:
        return {"error": "post_id is required"}
    return _call("GET", f"/api/v1/posts/{_quote(post_id)}")


def _act_post_delete(*, post_id: str = "", **_: Any) -> Dict[str, Any]:
    if not post_id:
        return {"error": "post_id is required"}
    return _call("DELETE", f"/api/v1/posts/{_quote(post_id)}")


def _act_post_upvote(*, post_id: str = "", **_: Any) -> Dict[str, Any]:
    if not post_id:
        return {"error": "post_id is required"}
    return _call("POST", f"/api/v1/posts/{_quote(post_id)}/upvote")


def _act_post_downvote(*, post_id: str = "", **_: Any) -> Dict[str, Any]:
    if not post_id:
        return {"error": "post_id is required"}
    return _call("POST", f"/api/v1/posts/{_quote(post_id)}/downvote")


def _act_post_pin(*, post_id: str = "", **_: Any) -> Dict[str, Any]:
    if not post_id:
        return {"error": "post_id is required"}
    return _call("POST", f"/api/v1/posts/{_quote(post_id)}/pin")


def _act_post_unpin(*, post_id: str = "", **_: Any) -> Dict[str, Any]:
    if not post_id:
        return {"error": "post_id is required"}
    return _call("DELETE", f"/api/v1/posts/{_quote(post_id)}/pin")


# ----- comments -------------------------------------------------------------


def _act_comments_list(
    *,
    post_id: str = "",
    sort: Optional[str] = None,
    limit: Optional[int] = None,
    **_: Any,
) -> Dict[str, Any]:
    if not post_id:
        return {"error": "post_id is required"}
    return _call(
        "GET",
        f"/api/v1/posts/{_quote(post_id)}/comments",
        query={"sort": sort, "limit": limit},
    )


def _act_comment_create(
    *,
    post_id: str = "",
    content: str = "",
    parent_id: Optional[str] = None,
    **_: Any,
) -> Dict[str, Any]:
    if not post_id or not content:
        return {"error": "post_id and content are required"}
    body: Dict[str, Any] = {"content": content}
    if parent_id:
        body["parent_id"] = parent_id
    return _call(
        "POST",
        f"/api/v1/posts/{_quote(post_id)}/comments",
        body=body,
    )


def _act_comment_upvote(*, comment_id: str = "", **_: Any) -> Dict[str, Any]:
    if not comment_id:
        return {"error": "comment_id is required"}
    return _call("POST", f"/api/v1/comments/{_quote(comment_id)}/upvote")


def _act_comment_downvote(*, comment_id: str = "", **_: Any) -> Dict[str, Any]:
    if not comment_id:
        return {"error": "comment_id is required"}
    return _call("POST", f"/api/v1/comments/{_quote(comment_id)}/downvote")


def _act_comment_delete(*, comment_id: str = "", **_: Any) -> Dict[str, Any]:
    if not comment_id:
        return {"error": "comment_id is required"}
    return _call("DELETE", f"/api/v1/comments/{_quote(comment_id)}")


# ----- feed & search --------------------------------------------------------


def _act_feed(
    *,
    sort: Optional[str] = None,
    limit: Optional[int] = None,
    **_: Any,
) -> Dict[str, Any]:
    return _call("GET", "/api/v1/feed", query={"sort": sort, "limit": limit})


def _act_search(
    *,
    q: str = "",
    type: Optional[str] = None,
    limit: Optional[int] = None,
    author: Optional[str] = None,
    submolt: Optional[str] = None,
    **_: Any,
) -> Dict[str, Any]:
    if not q:
        return {"error": "q is required"}
    return _call(
        "GET",
        "/api/v1/search",
        query={
            "q": q,
            "type": type,
            "limit": limit,
            "author": author,
            "submolt": submolt,
        },
    )


# ----- submolts -------------------------------------------------------------


def _act_submolts_list(
    *,
    sort: Optional[str] = None,
    limit: Optional[int] = None,
    fields: Optional[str] = None,
    **_: Any,
) -> Dict[str, Any]:
    return _call(
        "GET",
        "/api/v1/submolts",
        query={"sort": sort, "limit": limit, "fields": fields},
    )


def _act_submolt_create(
    *,
    name: str = "",
    display_name: str = "",
    description: str = "",
    **_: Any,
) -> Dict[str, Any]:
    if not name or not display_name or not description:
        return {"error": "name, display_name, and description are required"}
    return _call(
        "POST",
        "/api/v1/submolts",
        body={
            "name": name,
            "display_name": display_name,
            "description": description,
        },
    )


def _act_submolt_get(*, submolt: str = "", **_: Any) -> Dict[str, Any]:
    if not submolt:
        return {"error": "submolt is required"}
    return _call("GET", f"/api/v1/submolts/{_quote(submolt)}")


def _act_submolt_feed(
    *,
    submolt: str = "",
    sort: Optional[str] = None,
    limit: Optional[int] = None,
    **_: Any,
) -> Dict[str, Any]:
    if not submolt:
        return {"error": "submolt is required"}
    return _call(
        "GET",
        f"/api/v1/submolts/{_quote(submolt)}/feed",
        query={"sort": sort, "limit": limit},
    )


def _act_submolt_subscribe(*, submolt: str = "", **_: Any) -> Dict[str, Any]:
    if not submolt:
        return {"error": "submolt is required"}
    return _call("POST", f"/api/v1/submolts/{_quote(submolt)}/subscribe")


def _act_submolt_unsubscribe(*, submolt: str = "", **_: Any) -> Dict[str, Any]:
    if not submolt:
        return {"error": "submolt is required"}
    return _call("DELETE", f"/api/v1/submolts/{_quote(submolt)}/subscribe")


def _act_submolt_moderators_list(*, submolt: str = "", **_: Any) -> Dict[str, Any]:
    if not submolt:
        return {"error": "submolt is required"}
    return _call("GET", f"/api/v1/submolts/{_quote(submolt)}/moderators")


def _act_submolt_moderator_add(
    *,
    submolt: str = "",
    agent_name: str = "",
    role: str = "",
    **_: Any,
) -> Dict[str, Any]:
    if not submolt or not agent_name or not role:
        return {"error": "submolt, agent_name, and role are required"}
    return _call(
        "POST",
        f"/api/v1/submolts/{_quote(submolt)}/moderators",
        body={"agent_name": agent_name, "role": role},
    )


def _act_submolt_moderator_remove(
    *,
    submolt: str = "",
    agent_name: str = "",
    **_: Any,
) -> Dict[str, Any]:
    if not submolt or not agent_name:
        return {"error": "submolt and agent_name are required"}
    return _call(
        "DELETE",
        f"/api/v1/submolts/{_quote(submolt)}/moderators",
        body={"agent_name": agent_name},
    )


def _act_submolt_settings_update(
    *,
    submolt: str = "",
    description: Optional[str] = None,
    banner_color: Optional[str] = None,
    theme_color: Optional[str] = None,
    **_: Any,
) -> Dict[str, Any]:
    if not submolt:
        return {"error": "submolt is required"}
    body: Dict[str, Any] = {}
    if description is not None:
        body["description"] = description
    if banner_color is not None:
        body["banner_color"] = banner_color
    if theme_color is not None:
        body["theme_color"] = theme_color
    if not body:
        return {"error": "no updatable fields supplied"}
    return _call(
        "PATCH",
        f"/api/v1/submolts/{_quote(submolt)}/settings",
        body=body,
    )


# ----- static documentation fetchers ----------------------------------------


def _act_docs_skill(**_: Any) -> Dict[str, Any]:
    return _call("GET", "/skill.md")


def _act_docs_rules(**_: Any) -> Dict[str, Any]:
    return _call("GET", "/rules.md")


def _act_docs_messaging(**_: Any) -> Dict[str, Any]:
    return _call("GET", "/messaging.md")


def _act_docs_heartbeat(**_: Any) -> Dict[str, Any]:
    return _call("GET", "/heartbeat.md")


def _act_docs_skill_json(**_: Any) -> Dict[str, Any]:
    return _call("GET", "/skill.json")


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------


_ACTIONS: Dict[str, Callable[..., Dict[str, Any]]] = {
    # agent profile & follow (8)
    "agent_register": _act_agent_register,
    "agent_status": _act_agent_status,
    "agent_me": _act_agent_me,
    "agent_update": _act_agent_update,
    "agent_avatar_delete": _act_agent_avatar_delete,
    "agent_profile": _act_agent_profile,
    "agent_follow": _act_agent_follow,
    "agent_unfollow": _act_agent_unfollow,
    # direct messaging (8)
    "dm_check": _act_dm_check,
    "dm_conversations": _act_dm_conversations,
    "dm_conversation_get": _act_dm_conversation_get,
    "dm_send": _act_dm_send,
    "dm_request_create": _act_dm_request_create,
    "dm_requests_list": _act_dm_requests_list,
    "dm_request_approve": _act_dm_request_approve,
    "dm_request_reject": _act_dm_request_reject,
    # posts (8)
    "posts_list": _act_posts_list,
    "post_create": _act_post_create,
    "post_get": _act_post_get,
    "post_delete": _act_post_delete,
    "post_upvote": _act_post_upvote,
    "post_downvote": _act_post_downvote,
    "post_pin": _act_post_pin,
    "post_unpin": _act_post_unpin,
    # comments (5)
    "comments_list": _act_comments_list,
    "comment_create": _act_comment_create,
    "comment_upvote": _act_comment_upvote,
    "comment_downvote": _act_comment_downvote,
    "comment_delete": _act_comment_delete,
    # feed & search (2)
    "feed": _act_feed,
    "search": _act_search,
    # submolts (10)
    "submolts_list": _act_submolts_list,
    "submolt_create": _act_submolt_create,
    "submolt_get": _act_submolt_get,
    "submolt_feed": _act_submolt_feed,
    "submolt_subscribe": _act_submolt_subscribe,
    "submolt_unsubscribe": _act_submolt_unsubscribe,
    "submolt_moderators_list": _act_submolt_moderators_list,
    "submolt_moderator_add": _act_submolt_moderator_add,
    "submolt_moderator_remove": _act_submolt_moderator_remove,
    "submolt_settings_update": _act_submolt_settings_update,
    # static docs (5)
    "docs_skill": _act_docs_skill,
    "docs_rules": _act_docs_rules,
    "docs_messaging": _act_docs_messaging,
    "docs_heartbeat": _act_docs_heartbeat,
    "docs_skill_json": _act_docs_skill_json,
}


def dispatch(action_name: str, **kwargs: Any) -> Dict[str, Any]:
    """Single entrypoint used by every wrapper script.

    Looks up ``action_name`` in the action table and invokes the handler
    with the supplied keyword arguments. Unknown actions return a
    structured error rather than raising.
    """
    handler = _ACTIONS.get(action_name)
    if handler is None:
        return {"error": f"boltbook: unknown action {action_name!r}"}
    try:
        return handler(**kwargs)
    except TypeError as exc:
        # Surfaces wrong/extra/missing kwargs from the wrapper as a
        # structured error instead of a stack trace.
        return {"error": f"boltbook: invalid arguments for {action_name}: {exc}"}


__all__ = ["dispatch"]
