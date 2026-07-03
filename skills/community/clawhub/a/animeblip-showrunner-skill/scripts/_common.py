#!/usr/bin/env python3
"""Animeblip Showrunner — shared module: REST client + auth.

Every per-op script (create_project.py, send_message.py, query_session.py,
get_project_state.py, create_episode.py, list_projects.py) imports from here. Nothing in
this module reads argv — it is pure plumbing so the op scripts stay thin.

Stdlib only. Talks to the app's REST directly with an ab_ API key (the same endpoints
the MCP tools wrap) so the skill runs headless under a Claude Code cron routine.

Env:
    ANIMEBLIP_API_KEY   (required) ab_… key — create one in your Animeblip account (API Keys).
    ANIMEBLIP_BASE_URL  (optional) default https://studio.animeblip.com
"""
from __future__ import annotations

import json
import os
import urllib.request
import urllib.error

BASE_URL = os.environ.get("ANIMEBLIP_BASE_URL", "https://studio.animeblip.com").rstrip("/")
API_KEY = os.environ.get("ANIMEBLIP_API_KEY", "")


def _req(method, path, body=None):
    if not API_KEY:
        raise SystemExit("ERROR: ANIMEBLIP_API_KEY is not set.")
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": f"Bearer {API_KEY}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {}


# --- API wrappers (1:1 with the REST the MCP tools call) ---

def api_create_story(title=None, idea=None, genre=None, tone=None, style=None, aspect=None, lang=None):
    body = {"videoConfirmation": "always_allow"}
    for k, v in (("title", title), ("idea", idea), ("genre", genre), ("tone", tone),
                 ("artStyleId", style), ("aspectRatio", aspect), ("languageCode", lang)):
        if v:
            body[k] = v
    return _req("POST", "/api/stories", body)


def api_send(story_id, message):
    return _req("POST", "/api/chat", {"storyId": story_id, "message": message})


def api_status(story_id, after_seq=None):
    # after_seq (the cursor from the previous read, 0 first time) opts into the agent-message
    # tail: the response then includes messages[] (newer than after_seq) and a cursor.
    path = f"/api/chat/session?storyId={story_id}"
    if after_seq is not None:
        path += f"&afterSeq={after_seq}"
    return _req("GET", path)


def api_project_state(story_id):
    return _req("GET", f"/api/stories/{story_id}/project-state")


def api_next_episode(from_story_id):
    return _req("POST", f"/api/stories/{from_story_id}/next-episode", {})


def api_list_projects(limit=20, cursor=None):
    # A "project" = a series; the response lists each series with its full episodes[].
    path = f"/api/series?limit={limit}"
    if cursor:
        path += f"&cursor={cursor}"
    return _req("GET", path)


# --- Output ---

def print_json(data, indent=2):
    """Print a JSON result to stdout. indent=2 for human/agent-readable reads
    (status, project-state); indent=None for compact one-liners."""
    print(json.dumps(data, indent=indent))
