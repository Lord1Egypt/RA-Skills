#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "references"
FAQ_URL = "https://platform.minimaxi.com/docs/token-plan/faq"
REMAINS_URL = "https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains"


def load_api_key():
    env = os.environ.get("MINIMAX_API_KEY")
    if env:
        return env, "MINIMAX_API_KEY"
    cfg = Path("~/.openclaw/openclaw.json").expanduser()
    if cfg.exists():
        try:
            data = json.loads(cfg.read_text())
            providers = data.get("models", {}).get("providers", {})
            for name, p in providers.items():
                if "minimax" in name.lower() and p.get("apiKey"):
                    return p["apiKey"], "~/.openclaw/openclaw.json"
        except Exception:
            pass
    return None, None


def fetch_faq():
    try:
        r = requests.get(FAQ_URL, timeout=30)
        r.raise_for_status()
        return {"ok": True, "text": r.text}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def fetch_remains(api_key):
    try:
        r = requests.get(REMAINS_URL, headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }, timeout=30)
        r.raise_for_status()
        return {"ok": True, "json": r.json()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def read_json(path):
    return json.loads(Path(path).read_text())


def extract_signals_from_faq(text):
    lower = text.lower()
    return {
        "mentions_rolling_5h": ("5 小时滚动" in text) or ("5-hour" in lower),
        "mentions_daily_non_text": ("每日配额" in text) or ("daily" in lower),
        "mentions_weekly_limit": ("周使用额度" in text) or ("weekly" in lower),
        "contains_image_01": "image-01" in text,
        "contains_music_25": ("music-2.5" in lower),
        "contains_speech_hd": ("speech-2.8-hd" in lower) or ("speech-2.6-hd" in lower) or ("speech-02-hd" in lower),
        "contains_hailuo_23": ("hailuo-2.3" in lower),
    }


def compare_local_refs(faq_signals, remains_json, costs_json, quota_mapping):
    findings = []

    if faq_signals["mentions_rolling_5h"] and not faq_signals["mentions_daily_non_text"]:
        findings.append("⚠️ FAQ 只明显提到 5 小时窗口，未明确捕获非文本每日配额语义，请人工复核页面内容。")

    buckets = {row.get("model_name") for row in remains_json.get("model_remains", [])}
    mapped_buckets = {v.get("bucket") for v in quota_mapping.values() if isinstance(v, dict) and v.get("bucket")}
    missing = sorted(mapped_buckets - buckets)
    extra = sorted(buckets - mapped_buckets)

    if missing:
        findings.append(f"⚠️ quota_mapping 中这些 bucket 未在 remains 返回中出现: {', '.join(missing)}")
    if extra:
        findings.append(f"ℹ️ remains 返回中有这些 bucket 未被 quota_mapping 收录: {', '.join(extra)}")

    if costs_json.get("rolling_window_hours") != 5:
        findings.append("⚠️ costs.json 的 rolling_window_hours 不是 5，请复核。")

    return findings


def write_report(report_text):
    checks = REF / "checks"
    checks.mkdir(parents=True, exist_ok=True)
    target = checks / "latest-check.md"
    target.write_text(report_text)
    return target


def main():
    api_key, key_source = load_api_key()
    quota_mapping = read_json(REF / "quota_mapping.json")
    costs_json = read_json(REF / "costs.json")

    faq = fetch_faq()
    remains = fetch_remains(api_key) if api_key else {"ok": False, "error": "No Token Plan API Key found"}

    lines = ["# Official Doc Check Report", ""]
    lines.append(f"- FAQ fetch: {'OK' if faq['ok'] else 'FAIL'}")
    lines.append(f"- remains API: {'OK' if remains['ok'] else 'FAIL'}")
    lines.append(f"- API key source: {key_source or 'NOT FOUND'}")
    lines.append("")

    if faq["ok"]:
        faq_signals = extract_signals_from_faq(faq["text"])
        lines.append("## FAQ signals")
        for k, v in faq_signals.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    else:
        faq_signals = {}
        lines.append("## FAQ fetch failed")
        lines.append(f"- Error: {faq['error']}")
        lines.append("")

    if remains["ok"]:
        rows = remains["json"].get("model_remains", [])
        lines.append("## remains buckets")
        for row in rows:
            total = row.get("current_interval_total_count", 0)
            used = row.get("current_interval_usage_count", 0)
            lines.append(f"- {row.get('model_name')}: {used}/{total}")
        lines.append("")
    else:
        lines.append("## remains query failed")
        lines.append(f"- Error: {remains['error']}")
        lines.append("")

    if faq["ok"] and remains["ok"]:
        findings = compare_local_refs(faq_signals, remains["json"], costs_json, quota_mapping)
    else:
        findings = []
        lines.append("## degraded mode")
        lines.append("- One or more online checks failed. Continue using local references only.")
        lines.append("- See `references/troubleshooting.md` for diagnostics.")
        lines.append("")

    lines.append("## findings")
    if findings:
        lines.extend([f"- {x}" for x in findings])
    else:
        lines.append("- No obvious inconsistency detected in this check.")

    report = "\n".join(lines) + "\n"
    target = write_report(report)
    print(report)
    print(f"Report written to: {target}")


if __name__ == "__main__":
    main()
