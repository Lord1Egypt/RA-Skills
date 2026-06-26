#!/usr/bin/env python3
# Copyright North Model Labs — MIT (see repo LICENSE)
"""Atlas realtime (**passthrough** only) + offline avatar — agent-facing verb CLI.

This is **not** a meeting bot: it calls the Atlas HTTP API only. ``start`` always
uses ``mode=passthrough`` (BYO STT/LLM/TTS; you publish audio in your viewer). After
``start``, connect a LiveKit client (web / @northmodellabs/atlas-react) using
``livekit_url``, ``token``, and ``room`` from the JSON output.

Requires ATLAS_API_KEY. Optional ATLAS_API_BASE (default https://api.atlasv1.com).

Usage:
  python atlas_session.py start [--face PATH] [--face-url URL]
  python atlas_session.py status --session-id ID
  python atlas_session.py face-swap --session-id ID --face PATH
  python atlas_session.py leave --session-id ID
  python atlas_session.py viewer-token --session-id ID
  python atlas_session.py offline --audio PATH --image PATH [--callback-url URL]
  python atlas_session.py jobs-list [--limit N] [--offset N]
  python atlas_session.py jobs-wait JOB_ID [--interval 2] [--timeout 600]
  python atlas_session.py jobs-result JOB_ID
  python atlas_session.py me
  python atlas_session.py health
  python atlas_session.py index

Exit codes: 0 ok, 2 validation/config, 3 HTTP error (or failed job on jobs-wait).
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Monorepo root: ATLAS_AGENT_REPO, or skills/atlas-avatar/scripts/ → parents[3]
_HERE = Path(__file__).resolve()
_override = os.environ.get("ATLAS_AGENT_REPO", "").strip()
_REPO_ROOT = Path(_override).expanduser().resolve() if _override else _HERE.parents[3]
_CORE = _REPO_ROOT / "core"
if not _CORE.is_dir():
    print(
        "Could not find core/ next to this monorepo root:\n"
        f"  expected: {_CORE}\n"
        "Clone the full repo (core/ + skills/) or set ATLAS_AGENT_REPO to the repo root.",
        file=sys.stderr,
    )
    sys.exit(2)
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))

import atlas_api as api  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(
        description="Atlas avatar session helper — API calls only (see docstring).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser(
        "start",
        help="Create realtime passthrough session (POST /v1/realtime/session, mode=passthrough)",
    )
    s.add_argument("--face", default="", help="Local face image (multipart)")
    s.add_argument("--face-url", default="", dest="face_url", help="HTTPS face URL (JSON)")
    s.set_defaults(
        fn=lambda a: api.emit_response(
            api.api_realtime_create("passthrough", a.face or None, a.face_url or None)
        )
    )

    st = sub.add_parser("status", help="GET realtime session")
    st.add_argument("--session-id", required=True, dest="session_id")
    st.set_defaults(fn=lambda a: api.emit_response(api.api_realtime_get(a.session_id)))

    fs = sub.add_parser("face-swap", help="PATCH new face (multipart) mid-session")
    fs.add_argument("--session-id", required=True, dest="session_id")
    fs.add_argument("--face", required=True)
    fs.set_defaults(fn=lambda a: api.emit_response(api.api_realtime_patch(a.session_id, a.face)))

    lv = sub.add_parser("leave", help="DELETE realtime session (billing + teardown)")
    lv.add_argument("--session-id", required=True, dest="session_id")
    lv.set_defaults(fn=lambda a: api.emit_response(api.api_realtime_delete(a.session_id)))

    vw = sub.add_parser(
        "viewer-token",
        help="POST …/realtime/session/{id}/viewer — view-only LiveKit token (multi-viewer)",
    )
    vw.add_argument("--session-id", required=True, dest="session_id")
    vw.set_defaults(
        fn=lambda a: api.emit_response(api.api_realtime_viewer(a.session_id))
    )

    off = sub.add_parser("offline", help="POST /v1/generate (async video job)")
    off.add_argument("--audio", required=True)
    off.add_argument("--image", required=True)
    off.add_argument("--callback-url", default="", dest="callback_url")
    off.set_defaults(
        fn=lambda a: api.emit_response(
            api.api_generate(a.audio, a.image, a.callback_url or None)
        )
    )

    jl = sub.add_parser("jobs-list", help="GET /v1/jobs")
    jl.add_argument("--limit", type=int, default=None)
    jl.add_argument("--offset", type=int, default=None)
    jl.set_defaults(fn=lambda a: api.emit_response(api.api_jobs_list(a.limit, a.offset)))

    jw = sub.add_parser("jobs-wait", help="Poll job until completed or failed")
    jw.add_argument("job_id")
    jw.add_argument("--interval", type=float, default=2.0)
    jw.add_argument("--timeout", type=int, default=600)
    jw.set_defaults(
        fn=lambda a: api.api_jobs_wait(a.job_id, a.interval, a.timeout)
    )

    jr = sub.add_parser("jobs-result", help="GET presigned result URL")
    jr.add_argument("job_id")
    jr.set_defaults(fn=lambda a: api.emit_response(api.api_jobs_result(a.job_id)))

    sub.add_parser("me", help="GET /v1/me").set_defaults(
        fn=lambda _: api.emit_response(api.api_me())
    )
    sub.add_parser("health", help="GET /v1/health").set_defaults(
        fn=lambda _: api.emit_response(api.api_health())
    )
    sub.add_parser("index", help="GET / API index").set_defaults(
        fn=lambda _: api.emit_response(api.api_index())
    )

    args = p.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
