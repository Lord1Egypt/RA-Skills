# FILE_META
# INPUT:  skills/clawtraces/config.json (version field)
# OUTPUT: SKILL_VERSION constant + default_headers() helper
# POS:    skill lib — single source of truth for the client-side version string
# MISSION: Expose the Skill's semver to every HTTP request so the Server can gate old clients.

"""Skill version + shared HTTP header helper.

The ``version`` field in ``skills/clawtraces/config.json`` is the
single source of truth. Every HTTP request the Skill makes carries
``X-Skill-Version: <semver>`` so the Server's version gate can reject
clients running below ``MIN_SUPPORTED_SKILL_VERSION``.

Bumping protocol: edit ``config.json`` ``version`` field. The
publish-clawhub.sh script reads the same field so the CLI flag and
the packaged config cannot drift.

Historical note: a plain ``VERSION`` file used to live at the Skill
root, but ClawHub's publishing pipeline silently dropped extensionless
files, causing installed copies to fall back to ``0.0.0``.
"""

from __future__ import annotations

import json
import os
import sys


def _read_version() -> str:
    """Read the ``version`` field from the Skill's config.json.

    Layout: skills/clawtraces/scripts/lib/version.py  (this file)
            skills/clawtraces/config.json             (target)

    On any error (missing file, malformed JSON, missing field) we
    return ``"0.0.0"`` so the request still goes out — the server-side
    gate will reject it with an upgrade-required error, which is the
    correct user-facing signal.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.normpath(os.path.join(here, "..", "..", "config.json"))
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        value = str(data.get("version") or "").strip()
        return value or "0.0.0"
    except (OSError, ValueError):
        return "0.0.0"


SKILL_VERSION: str = _read_version()


def default_headers(secret_key: str | None = None) -> dict[str, str]:
    """Return the standard header set for Skill → Server HTTP requests.

    Always included:
      User-Agent       canonical product/version token
      X-Skill-Version  the string the server's version gate checks

    ``secret_key`` is optional because the /auth/send-code and
    /auth/verify-code endpoints are called before a key exists.
    """
    headers: dict[str, str] = {
        "User-Agent": f"ClawTraces/{SKILL_VERSION}",
        "X-Skill-Version": SKILL_VERSION,
    }
    if secret_key:
        headers["X-Secret-Key"] = secret_key
    return headers


def exit_if_upgrade_required(parsed: dict) -> None:
    """Terminate the process cleanly if the server returned 426.

    Every HTTP client in the Skill returns a parsed-JSON dict on error
    (rather than raising). For a version-gate rejection we don't want
    the caller to treat it as a normal business error — the right
    response is to print the upgrade command once and exit.

    Matches on ``error_code == "skill_version_too_old"`` so older
    servers that only set ``error`` (short code) still work for legacy
    test traffic, but the canonical trigger is ``error_code``.

    Exit code 2 distinguishes "must upgrade" from generic failures (1).
    """
    if parsed.get("error_code") != "skill_version_too_old":
        return
    message = parsed.get("message") or parsed.get("error") or "Skill 版本过低，请升级后重试"
    print(f"\n❌ {message}", file=sys.stderr)
    sys.exit(2)


__all__ = ["SKILL_VERSION", "default_headers", "exit_if_upgrade_required"]
