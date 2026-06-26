#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from urllib.parse import parse_qs, urlparse
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
BUILD_SCRIPT = SCRIPT_DIR / "build_daily_context.py"
DEFAULT_OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
WEIXIN_PLUGIN_HINTS = ("openclaw-weixin", "weixin", "wechat", "wxbot")
WEIXIN_ENV_WEBHOOKS = (
    "WEIXIN_BOT_WEBHOOK_URL",
    "WECHAT_BOT_WEBHOOK_URL",
    "WEIXIN_WEBHOOK_URL",
    "WECHAT_WEBHOOK_URL",
    "WEIXINBOTWEBHOOKURL",
    "WECHATBOTWEBHOOKURL",
)
WEIXIN_ENV_KEYS = (
    "WEIXIN_BOT_KEY",
    "WECHAT_BOT_KEY",
    "WX_BOT_KEY",
    "WEIXIN_WEBHOOK_KEY",
    "WECHAT_WEBHOOK_KEY",
    "WEIXINBOTKEY",
    "WECHATBOTKEY",
    "WXBOTKEY",
)
LIKELY_WEBHOOK_FIELDS = (
    "webhook_url",
    "webhookurl",
    "webhook",
    "url",
    "bot_webhook_url",
    "botwebhookurl",
)
LIKELY_KEY_FIELDS = (
    "webhook_key",
    "webhookkey",
    "bot_webhook_key",
    "botwebhookkey",
)
CONTEXTUAL_KEY_FIELDS = ("key",)
USER_AGENT = "daily-morning-greetings/1.1"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build and optionally fan out daily-morning-greetings to Weixin bot."
    )
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    parser.add_argument(
        "--print-message",
        action="store_true",
        help="Emit formatted.message only, preserving blank lines.",
    )
    parser.add_argument(
        "--variant",
        type=int,
        default=0,
        help="Variant index for alternate rerolls. 0 is the standard daily version.",
    )
    parser.add_argument("--city", help="City label for weather lookup, e.g. Shanghai.")
    parser.add_argument("--city-zh", help="Chinese city label used in rendered output.")
    parser.add_argument("--timezone", help="IANA timezone, e.g. Asia/Shanghai.")
    parser.add_argument("--latitude", type=float, help="Latitude for Open-Meteo fallback.")
    parser.add_argument("--longitude", type=float, help="Longitude for Open-Meteo fallback.")
    parser.add_argument(
        "--selection-mode",
        choices=["alternate", "manual", "standard"],
        default="standard",
        help="Selection mode: stable standard, or manual/alternate rerolls with daily non-repeat state.",
    )
    parser.add_argument(
        "--scope-key",
        help="Stable route key for manual/alternate rerolls, e.g. Feishu chat:<chatId>.",
    )
    parser.add_argument(
        "--deliver-weixin",
        choices=["off", "auto", "required"],
        default="off",
        help="Whether to fan out the generated message to a detected Weixin bot config.",
    )
    parser.add_argument(
        "--openclaw-config",
        help="Optional OpenClaw config path for Weixin bot auto-detection.",
    )
    return parser.parse_args()


def normalize_text(value):
    text = str(value or "").strip()
    return text or None


def build_weixin_webhook_from_key(key):
    normalized = normalize_text(key)
    if not normalized:
        return None
    if normalized.startswith(("http://", "https://")):
        return normalized
    encoded = urllib.parse.quote(normalized, safe="")
    return f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={encoded}"


def describe_weixin_target(value):
    normalized = normalize_text(value)
    if not normalized:
        return None
    if looks_like_weixin_key(normalized):
        normalized = build_weixin_webhook_from_key(normalized)
    if not looks_like_webhook_url(normalized):
        return "configured"
    parsed = urlparse(normalized)
    key_value = normalize_text((parse_qs(parsed.query).get("key") or [None])[0])
    if key_value:
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?key=***{key_value[-4:]}"
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def is_weixin_webhook_url(value):
    normalized = normalize_text(value)
    if not normalized:
        return False
    lowered = normalized.lower()
    return "qyapi.weixin.qq.com/cgi-bin/webhook/send" in lowered and "key=" in lowered


def looks_like_webhook_url(value):
    normalized = normalize_text(value)
    if not normalized:
        return False
    return normalized.startswith(("http://", "https://"))


def looks_like_weixin_key(value):
    normalized = normalize_text(value)
    if not normalized:
        return False
    if normalized.startswith(("http://", "https://")):
        return False
    if " " in normalized:
        return False
    if len(normalized) < 12:
        return False
    return True


def has_webhook_context(path_segments):
    return any("webhook" in segment for segment in path_segments)


def load_json(path):
    file_path = Path(path).expanduser()
    return json.loads(file_path.read_text(encoding="utf-8"))


def run_build_script(args):
    cmd = [sys.executable, str(BUILD_SCRIPT), "--compact"]
    if args.variant is not None:
        cmd.extend(["--variant", str(args.variant)])
    if args.city:
        cmd.extend(["--city", args.city])
    if args.city_zh:
        cmd.extend(["--city-zh", args.city_zh])
    if args.timezone:
        cmd.extend(["--timezone", args.timezone])
    if args.latitude is not None:
        cmd.extend(["--latitude", str(args.latitude)])
    if args.longitude is not None:
        cmd.extend(["--longitude", str(args.longitude)])
    if args.selection_mode:
        cmd.extend(["--selection-mode", args.selection_mode])
    if args.scope_key:
        cmd.extend(["--scope-key", args.scope_key])

    completed = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)


def detect_weixin_from_env():
    for key in WEIXIN_ENV_WEBHOOKS:
        value = normalize_text(os.environ.get(key))
        if value:
            webhook = build_weixin_webhook_from_key(value)
            if webhook:
                return {
                    "source": f"env:{key}",
                    "webhook_url": webhook,
                }
    for key in WEIXIN_ENV_KEYS:
        value = normalize_text(os.environ.get(key))
        if value:
            webhook = build_weixin_webhook_from_key(value)
            if webhook:
                return {
                    "source": f"env:{key}",
                    "webhook_url": webhook,
                }
    return None


def candidate_enabled(node):
    if not isinstance(node, dict):
        return True
    enabled = node.get("enabled")
    if enabled is False:
        return False
    return True


def scan_candidate_node(node, path_segments=()):
    if isinstance(node, dict):
        normalized_keys = {
            str(key).replace("-", "_").strip().lower()
            for key in node.keys()
        }
        node_has_webhook_context = has_webhook_context(path_segments) or any(
            "webhook" in key for key in normalized_keys
        )
        for key, value in node.items():
            normalized_key = str(key).replace("-", "_").strip().lower()
            current_path = (*path_segments, normalized_key)
            normalized_value = normalize_text(value)
            if normalized_value:
                if is_weixin_webhook_url(normalized_value):
                    return build_weixin_webhook_from_key(normalized_value)
                if normalized_key in LIKELY_WEBHOOK_FIELDS:
                    if "webhook" in normalized_key and looks_like_weixin_key(normalized_value):
                        return build_weixin_webhook_from_key(normalized_value)
                if normalized_key in LIKELY_KEY_FIELDS and looks_like_weixin_key(normalized_value):
                    return build_weixin_webhook_from_key(normalized_value)
                if (
                    normalized_key in CONTEXTUAL_KEY_FIELDS
                    and node_has_webhook_context
                    and looks_like_weixin_key(normalized_value)
                ):
                    return build_weixin_webhook_from_key(normalized_value)
            nested = scan_candidate_node(value, current_path)
            if nested:
                return nested
    elif isinstance(node, list):
        for idx, item in enumerate(node):
            nested = scan_candidate_node(item, (*path_segments, str(idx)))
            if nested:
                return nested
    return None


def iter_weixin_candidates(payload):
    if not isinstance(payload, dict):
        return
    plugins = ((payload.get("plugins") or {}).get("entries") or {})
    for key, value in plugins.items():
        identifier = str(key or "").strip().lower()
        if any(hint in identifier for hint in WEIXIN_PLUGIN_HINTS):
            yield f"plugins.entries.{key}", value
    channels = payload.get("channels") or {}
    for key, value in channels.items():
        identifier = str(key or "").strip().lower()
        if any(hint in identifier for hint in WEIXIN_PLUGIN_HINTS):
            yield f"channels.{key}", value


def detect_weixin_from_openclaw_config(path):
    config_path = Path(path).expanduser()
    if not config_path.exists():
        return None
    payload = load_json(config_path)
    for source, node in iter_weixin_candidates(payload):
        if not candidate_enabled(node):
            continue
        webhook = scan_candidate_node(node)
        if webhook:
            return {
                "source": f"config:{source}",
                "webhook_url": webhook,
                "config_path": str(config_path),
            }
    return None


def detect_weixin_target(config_path=None):
    env_match = detect_weixin_from_env()
    if env_match:
        return env_match

    override = normalize_text(config_path) or normalize_text(os.environ.get("OPENCLAW_CONFIG_PATH"))
    candidates = []
    if override:
        candidates.append(override)
    candidates.append(str(DEFAULT_OPENCLAW_CONFIG))
    seen = set()
    for candidate in candidates:
        normalized = str(Path(candidate).expanduser())
        if normalized in seen:
            continue
        seen.add(normalized)
        match = detect_weixin_from_openclaw_config(normalized)
        if match:
            return match
    return None


def send_to_weixin_bot(message, webhook_url):
    payload = json.dumps(
        {
            "msgtype": "text",
            "text": {"content": message},
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        body = response.read().decode(charset)
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise RuntimeError(f"Weixin bot returned non-JSON body: {exc}") from exc

    if int(data.get("errcode", 0) or 0) != 0:
        raise RuntimeError(
            f"Weixin bot send failed: errcode={data.get('errcode')} errmsg={data.get('errmsg')}"
        )
    return data


def maybe_deliver_weixin(message, mode, config_path=None):
    status = {
        "mode": mode,
        "attempted": False,
        "sent": False,
        "source": None,
        "target": None,
        "error": None,
    }
    if mode == "off":
        return status

    target = detect_weixin_target(config_path)
    if not target:
        status["error"] = "No enabled Weixin bot config detected"
        if mode == "required":
            raise RuntimeError(status["error"])
        return status

    status["attempted"] = True
    status["source"] = target.get("source")
    status["target"] = describe_weixin_target(target.get("webhook_url"))
    try:
        send_to_weixin_bot(message, target["webhook_url"])
    except Exception as exc:
        status["error"] = str(exc)
        if mode == "required":
            raise
        return status

    status["sent"] = True
    return status


def emit_output(payload, print_message=False, compact=False):
    if print_message:
        print(payload["formatted"]["message"])
        return
    if compact:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
        return
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main():
    args = parse_args()
    payload = run_build_script(args)
    message = (
        ((payload.get("formatted") or {}).get("message"))
        or "\n\n".join(
            [
                ((payload.get("formatted") or {}).get("greeting") or "").strip(),
                ((payload.get("formatted") or {}).get("weather") or "").strip(),
                ((payload.get("formatted") or {}).get("wisdom") or "").strip(),
            ]
        ).strip()
    )
    if not message:
        raise SystemExit("No formatted.message produced by build_daily_context.py")

    delivery_status = maybe_deliver_weixin(
        message,
        args.deliver_weixin,
        config_path=args.openclaw_config,
    )
    payload["delivery"] = {
        "weixin": delivery_status,
    }

    if delivery_status.get("error") and args.deliver_weixin == "auto":
        print(
            f"[daily-morning-greetings] Weixin bot fanout skipped: {delivery_status['error']}",
            file=sys.stderr,
        )

    emit_output(payload, print_message=args.print_message, compact=args.compact)


if __name__ == "__main__":
    main()
