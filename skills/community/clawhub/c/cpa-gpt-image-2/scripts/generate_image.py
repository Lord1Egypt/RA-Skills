#!/usr/bin/env python3
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def fail(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def find_image_b64(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get("b64_json"), str):
            return obj["b64_json"]
        if obj.get("type") == "image_generation_call":
            result = obj.get("result")
            if isinstance(result, str):
                return result
        for value in obj.values():
            hit = find_image_b64(value)
            if hit:
                return hit
    elif isinstance(obj, list):
        for item in obj:
            hit = find_image_b64(item)
            if hit:
                return hit
    return None


def load_json_if_exists(path: Path):
    try:
        if path.exists():
            return json.loads(path.read_text())
    except Exception:
        return None
    return None


def load_openclaw_provider_defaults():
    status_path = Path.home() / "openclaw/agents/main/agent/models.json"
    data = load_json_if_exists(status_path) or {}
    providers = data.get("providers") or {}
    otcbot = providers.get("otcbot") or {}
    return {
        "base_url": (otcbot.get("baseUrl") or "").rstrip("/"),
        "api_key": otcbot.get("apiKey") or "",
    }


def infer_default_model():
    env_model = os.getenv("OTCBOT_IMAGE_MODEL") or os.getenv("CPA_MODEL")
    if env_model:
        return env_model
    status_json = os.popen("openclaw models status --json 2>/dev/null").read().strip()
    if status_json:
        try:
            status = json.loads(status_json)
            image_model = status.get("imageModel")
            if image_model and "/" in image_model:
                return image_model.split("/", 1)[1]
            default_model = status.get("resolvedDefault") or status.get("defaultModel")
            if default_model and "/" in default_model:
                return default_model.split("/", 1)[1]
        except Exception:
            pass
    return os.getenv("IMAGE_GEN_MODEL", "gpt-5.4")


def parse_sse_events(raw: str):
    payloads = []
    buf = []
    for line in raw.splitlines():
        if line.startswith("data:"):
            data = line[5:].strip()
            if data == "[DONE]":
                continue
            buf.append(data)
        elif not line.strip() and buf:
            payloads.append("\n".join(buf))
            buf = []
    if buf:
        payloads.append("\n".join(buf))
    parsed = []
    for item in payloads:
        try:
            parsed.append(json.loads(item))
        except Exception:
            continue
    return parsed


def extract_retry_delay_ms(raw: str, parsed):
    text = raw or ""
    m = re.search(r"Please try again in (\d+)ms", text)
    if m:
        return int(m.group(1))
    if isinstance(parsed, list):
        for item in parsed:
            err = item.get("error") if isinstance(item, dict) else None
            if isinstance(err, dict):
                msg = err.get("message", "")
                m = re.search(r"Please try again in (\d+)ms", msg)
                if m:
                    return int(m.group(1))
    elif isinstance(parsed, dict):
        err = parsed.get("error")
        if isinstance(err, dict):
            msg = err.get("message", "")
            m = re.search(r"Please try again in (\d+)ms", msg)
            if m:
                return int(m.group(1))
    return None


def is_rate_limit_error(raw: str, parsed):
    text = raw or ""
    if "rate_limit_exceeded" in text:
        return True
    if isinstance(parsed, list):
        for item in parsed:
            if isinstance(item, dict) and item.get("type") == "error":
                err = item.get("error") or {}
                if err.get("code") == "rate_limit_exceeded":
                    return True
    elif isinstance(parsed, dict):
        err = parsed.get("error") or {}
        if err.get("code") == "rate_limit_exceeded":
            return True
    return False


def has_tools_empty_fallback(raw: str, parsed):
    text = raw or ""
    if '"tools":[]' in text and 'response.output_text.delta' in text:
        return True
    if isinstance(parsed, list):
        saw_created = False
        saw_text = False
        for item in parsed:
            if not isinstance(item, dict):
                continue
            t = item.get('type')
            if t in ('response.created', 'response.in_progress'):
                response = item.get('response') or {}
                if response.get('tools') == []:
                    saw_created = True
            if t == 'response.output_text.delta':
                saw_text = True
        return saw_created and saw_text
    return False


parser = argparse.ArgumentParser(description="Generate an image through an otcbot/OpenAI-compatible Responses API")
parser.add_argument("--prompt", required=True, help="Image prompt")
parser.add_argument("--output", required=True, help="Output image path")
parser.add_argument("--model", default=infer_default_model())
parser.add_argument("--format", default=os.getenv("IMAGE_GEN_OUTPUT_FORMAT", "png"), choices=["png", "jpeg", "webp"])
parser.add_argument("--instructions", default="you are a helpful assistant")
parser.add_argument("--session-id", default=os.getenv("CPA_SESSION_ID", "test-session"))
parser.add_argument("--stream", dest="stream", action="store_true", default=False)
parser.add_argument("--no-stream", dest="stream", action="store_false")
parser.add_argument("--retries", type=int, default=4)
args = parser.parse_args()

provider_defaults = load_openclaw_provider_defaults()
base_url = (os.getenv("IMAGE_GEN_BASE_URL") or os.getenv("OTCBOT_BASE_URL") or os.getenv("CPA_BASE_URL") or os.getenv("OPENAI_BASE_URL") or provider_defaults["base_url"] or "").rstrip("/")
api_key = os.getenv("IMAGE_GEN_KEY") or os.getenv("OTCBOT_API_KEY") or os.getenv("CPA_API_KEY") or os.getenv("OPENAI_API_KEY") or provider_defaults["api_key"] or ""
user_agent = os.getenv("CPA_USER_AGENT", "codex-tui/0.122.0 (Manjaro 26.1.0-pre; x86_64) vscode/3.0.12 (codex-tui; 0.122.0)")
version = os.getenv("CPA_VERSION", "0.122.0")
originator = os.getenv("CPA_ORIGINATOR", "codex_cli_rs")

if not base_url:
    fail("Missing OTCBOT_BASE_URL / CPA_BASE_URL / OPENAI_BASE_URL and no otcbot baseUrl found in models.json")
if not api_key:
    fail("Missing OTCBOT_API_KEY / CPA_API_KEY / OPENAI_API_KEY and no otcbot apiKey found in models.json")

url = f"{base_url}/responses" if base_url.endswith("/v1") else f"{base_url}/v1/responses"
payload = {
    "model": args.model,
    "input": args.prompt,
    "tools": [
        {
            "type": "image_generation",
            "output_format": args.format,
        }
    ],
    "instructions": args.instructions,
    "tool_choice": "auto",
    "stream": args.stream,
    "store": False,
}

last_raw = ""
last_parsed = None
for attempt in range(args.retries + 1):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "user-agent": user_agent,
            "version": version,
            "originator": originator,
            "session_id": args.session_id,
            "accept": "text/event-stream" if args.stream else "application/json",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            status = resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        fail(f"HTTP {e.code}\n{body}")
    except Exception as e:
        fail(f"Request failed: {e}")

    if status < 200 or status >= 300:
        fail(f"Unexpected HTTP status: {status}\n{raw}")

    parsed = None
    if args.stream:
        events = parse_sse_events(raw)
        if events:
            parsed = events
    if parsed is None:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            fail(f"Response was not valid JSON or SSE JSON:\n{raw[:4000]}")

    b64 = find_image_b64(parsed)
    if b64:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(base64.b64decode(b64))
        print(str(out))
        sys.exit(0)

    last_raw = raw
    last_parsed = parsed
    if attempt < args.retries and is_rate_limit_error(raw, parsed):
        delay_ms = extract_retry_delay_ms(raw, parsed) or 1000
        time.sleep(max(delay_ms, 200) / 1000.0)
        continue
    if attempt < args.retries and has_tools_empty_fallback(raw, parsed):
        time.sleep(0.8 + attempt * 0.4)
        continue
    break

fail("No base64 image found in response. Inspect raw payload.\n" + last_raw[:4000])
