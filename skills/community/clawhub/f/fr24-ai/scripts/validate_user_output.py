#!/usr/bin/env python3
"""校验脚本 stdout：userView 结构、无调试字段、示例与日期解析。"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent

_USER_FORBIDDEN = (
    "traceId",
    "processingTime",
    "offerId",
    "verifyOfferId",
    "payloadFile",
    "FR_NEWAPI_SKIP",
    "FR_BOOKING_TEST",
    "SKIP_IP_WHITELIST",
    "setup-maintainer",
    "skill.local.env",
    "flight-deve",
    "fr24-skip",
    "张三",
    "王明",
)


def _walk_strings(obj, path: str = "") -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.extend(_walk_strings(v, f"{path}.{k}" if path else k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(_walk_strings(v, f"{path}[{i}]"))
    elif isinstance(obj, str):
        out.append((path, obj))
    return out


def check_envelope(envelope: dict, *, action: str) -> list[str]:
    errors: list[str] = []
    if envelope.get("action") != action:
        errors.append(f"action expected {action}, got {envelope.get('action')}")
    if "data" in envelope and "userView" not in envelope:
        errors.append("legacy `data` without userView — update script output")
    if "userView" not in envelope:
        errors.append("missing userView")
        return errors

    uv = envelope["userView"]
    for path, text in _walk_strings(uv):
        for token in _USER_FORBIDDEN:
            if token in text:
                errors.append(f"userView{path} contains forbidden {token!r}")
    if "agentOnly" in envelope:
        ao_text = json.dumps(envelope["agentOnly"], ensure_ascii=False)
        if "traceId" not in ao_text and action == "search" and envelope.get("status") == "success":
            # search may omit trace in agentOnly only when failed early
            pass

    msg = envelope.get("message", "")
    for token in _USER_FORBIDDEN:
        if token in msg:
            errors.append(f"message contains forbidden {token!r}")

    if action in ("parse", "refine") and envelope.get("status") == "success":
        if "payload" in uv:
            errors.append("userView must not contain payload")
        legs = uv.get("legs") or []
        if not legs:
            errors.append("userView.legs empty")
        if "深圳" in json.dumps(envelope, ensure_ascii=False):
            pass
    if action == "search" and envelope.get("status") == "success":
        if not uv.get("directLowest") and not uv.get("transferLowest"):
            errors.append("search userView missing directLowest and transferLowest")
        for key in ("directLowest", "transferLowest"):
            o = uv.get(key)
            if o and "offerId" in o:
                errors.append(f"userView.{key} must not contain offerId")
        if "traceId" in msg:
            errors.append("search message contains traceId")
    return errors


def run_json(cmd: list[str]) -> dict:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        cmd,
        cwd=str(_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    if proc.returncode not in (0, 1):
        raise RuntimeError(proc.stderr or proc.stdout or f"exit {proc.returncode}")
    if not proc.stdout or not proc.stdout.strip():
        raise RuntimeError(f"empty stdout: stderr={proc.stderr!r}")
    return json.loads(proc.stdout)


def main() -> int:
    errors: list[str] = []

    # 日期：下周二
    parse_text = "\u6df1\u5733\u5230\u66fc\u8c37 \u4e0b\u5468\u4e8c"  # 深圳到曼谷 下周二
    p = run_json(
        [sys.executable, str(_SCRIPTS / "nl_to_search.py"), "parse", "--text", parse_text]
    )
    errors.extend(check_envelope(p, action="parse"))
    dep = (p.get("userView") or {}).get("legs", [{}])[0].get("depDate")
    if dep != "2026-06-02":
        errors.append(f"下周二 expected 2026-06-02, got {dep}")

    r = run_json(
        [
            sys.executable,
            str(_SCRIPTS / "nl_to_search.py"),
            "refine",
            "--text",
            "\u8981CA\u822a\u53f8 \u4e2d\u534812\u70b9\u8d77\u98de",
        ]
    )
    errors.extend(check_envelope(r, action="refine"))
    if r.get("action") != "refine":
        errors.append(f"refine action expected refine, got {r.get('action')}")
    sf = (r.get("userView") or {}).get("searchFilters") or {}
    if "CA" not in (sf.get("preferredCarrier") or []):
        errors.append("refine userView.searchFilters missing CA")
    prefs = (r.get("agentOnly") or {}).get("payload", {}).get("preferences", {})
    if "CA" not in (prefs.get("preferredCarrier") or []):
        errors.append("refine payload.preferences.preferredCarrier missing CA")
    if not prefs.get("depTimeWindow"):
        errors.append("refine payload missing depTimeWindow")

    # 乘客示例含张三
    from booking_guidance import PASSENGER_INFO_USER_PROMPT  # noqa: E402

    if "张三" not in PASSENGER_INFO_USER_PROMPT:
        errors.append("PASSENGER_INFO_USER_PROMPT missing 张三")
    if "李四" in PASSENGER_INFO_USER_PROMPT:
        errors.append("PASSENGER_INFO_USER_PROMPT still has 李四")

    # 配置失败文案
    pax_text = (
        "\u5f20\u4e09 \u7537 1990-01-15 \u62a4\u7167E12345678 2030-12-31 \u5230\u671f \u56fd\u7c4dCN"
    )
    cfg = run_json(
        [
            sys.executable,
            str(_SCRIPTS / "skill_booking_client.py"),
            "parse-passengers",
            "--text",
            pax_text,
        ]
    )
    errors.extend(check_envelope(cfg, action="parse-passengers"))
    if "FR_NEWAPI" in cfg.get("message", ""):
        errors.append("parse-passengers message leaks FR_NEWAPI")

    # 搜索（消耗 1 次配额）
    if "--skip-search" not in sys.argv:
        s = run_json(
            [
                sys.executable,
                str(_SCRIPTS / "skill_search_client.py"),
                "search",
                "--payload-file",
                ".cache/pending_search.json",
            ]
        )
        errors.extend(check_envelope(s, action="search"))
        if s.get("status") == "success":
            msg = s.get("message", "")
            if "【直飞最低】" not in msg and "直飞最低" not in msg:
                errors.append("search message missing direct offer line")
            if "退票" not in msg and "改期" not in msg:
                errors.append("search message missing refund/change summary")
            if prefs.get("preferredCarrier") and "筛选条件" not in msg:
                errors.append("search with carrier filter should show 筛选条件 in message")
        else:
            code = str((s.get("agentOnly") or {}).get("code", ""))
            if code not in ("307901", "404", "NETWORK_ERROR"):
                errors.append(f"search failed unexpectedly: code={code}")

    out = {"ok": len(errors) == 0, "errors": errors}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.path.insert(0, str(_ROOT))
    sys.path.insert(0, str(_SCRIPTS))
    raise SystemExit(main())
