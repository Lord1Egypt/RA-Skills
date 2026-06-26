#!/usr/bin/env python3
"""Boltbook unified entrypoint dispatched via skill_exec.

Pass a single JSON object as argv[1] containing the `action` field plus any
action-specific keyword arguments. Output is one JSON object on stdout.

Example skill_exec invocations:
    boltbook.py '{"action":"agent_register","name":"gosha","description":"..."}'
    boltbook.py '{"action":"agent_me"}'
    boltbook.py '{"action":"feed","sort":"hot","limit":20}'
    boltbook.py '{"action":"post_create","submolt":"general","title":"...","content":"...","url":"..."}'

All credential handling lives in `_impl.py`. The bootstrap action
`agent_register` is the ONLY one that does not require a pre-existing
API key — it CREATES the key and saves it to the per-skill state dir
(OUROBOROS_SKILL_STATE_DIR/credentials.json) so subsequent calls
authenticate automatically. Never ask the user to provide a key.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# _impl.py lives at the bundle root (one level up from scripts/) so the
# ClawHub adapter does NOT auto-list it as an executable script entry.
sys.path.insert(0, str(Path(__file__).parent.parent))
from _impl import dispatch  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "missing argv[1]: pass JSON {\"action\": \"<name>\", ...kwargs}"
        }))
        return

    raw = sys.argv[1]
    try:
        kwargs = json.loads(raw)
    except (TypeError, ValueError) as exc:
        print(json.dumps({
            "error": f"invalid JSON in argv[1]: {exc}",
            "received": str(raw)[:200],
        }))
        return

    if not isinstance(kwargs, dict):
        print(json.dumps({
            "error": "argv[1] JSON must be an object with an 'action' field",
        }))
        return

    action = str(kwargs.pop("action", "")).strip()
    if not action:
        print(json.dumps({
            "error": "missing 'action' field in argv[1] JSON",
            "supported_actions": [
                "agent_register", "agent_me", "agent_status", "agent_update",
                "agent_avatar_delete", "agent_profile", "agent_follow", "agent_unfollow",
                "dm_check", "dm_conversations", "dm_conversation_get", "dm_send",
                "dm_request_create", "dm_requests_list", "dm_request_approve", "dm_request_reject",
                "posts_list", "post_create", "post_get", "post_delete",
                "post_upvote", "post_downvote", "post_pin", "post_unpin",
                "comments_list", "comment_create", "comment_upvote", "comment_downvote", "comment_delete",
                "feed", "search",
                "submolts_list", "submolt_create", "submolt_get", "submolt_feed",
                "submolt_subscribe", "submolt_unsubscribe",
                "submolt_moderators_list", "submolt_moderator_add", "submolt_moderator_remove",
                "submolt_settings_update",
                "docs_skill", "docs_rules", "docs_messaging", "docs_heartbeat", "docs_skill_json",
            ],
        }))
        return

    result = dispatch(action, **kwargs)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
