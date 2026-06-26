#!/bin/bash

set -euo pipefail

# Usage: render-video.sh <brief-json-file> <setup-state-file> [curl-bin]

BRIEF_FILE="${1:-}"
SETUP_STATE_FILE="${2:-}"
CURL_BIN="${3:-curl}"
POLL_INTERVAL_SECONDS="${VIDEO_POLL_INTERVAL_SECONDS:-10}"
TIMEOUT_SECONDS="${VIDEO_TIMEOUT_SECONDS:-300}"

if [ -z "$BRIEF_FILE" ] || [ -z "$SETUP_STATE_FILE" ]; then
  echo "Usage: render-video.sh <brief-json-file> <setup-state-file> [curl-bin]" >&2
  exit 1
fi

if [ ! -f "$BRIEF_FILE" ]; then
  echo "Brief file not found: $BRIEF_FILE" >&2
  exit 1
fi

normalize_warning() {
  python3 -c 'import sys; print(sys.stdin.read().strip().replace("\n", " | "))'
}

print_result() {
  python3 - "$@" <<'PY'
import json
import sys

(
    render_mode,
    video_url,
    tracking_url,
    provider,
    model,
    genre,
    fallback_reason,
    warning,
) = sys.argv[1:]

print(
    json.dumps(
        {
            "render_mode": render_mode,
            "video_url": video_url,
            "tracking_url": tracking_url,
            "provider": provider,
            "model": model,
            "genre": genre,
            "fallback_reason": fallback_reason,
            "warning": warning,
        },
        ensure_ascii=True,
    )
)
PY
}

read_runtime_bundle() {
  python3 - "$BRIEF_FILE" "$SETUP_STATE_FILE" <<'PY'
import json
import os
import re
import sys
from pathlib import Path

brief_path = Path(sys.argv[1])
setup_path = Path(sys.argv[2]).expanduser()
DEFAULT_API_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_VIDEO_MODEL = "doubao-seedance-1-5-pro-251215"
DEFAULT_TEXT_TO_VIDEO_MODEL = "doubao-seedance-1-0-pro-250528"


def emit(**kwargs):
    print(json.dumps(kwargs, ensure_ascii=True))


def parse_duration_seconds(value: str) -> str:
    text = (value or "").strip().lower()
    match = re.search(r"(\d+)", text)
    if not match:
        return "5"
    seconds = match.group(1)
    return seconds


def build_prompt(brief):
    user_input = str(brief.get("user_input") or "").strip()
    scene_description = str(brief.get("scene_description") or "").strip()
    genre = str(brief.get("video_genre") or "").strip()
    motion_strategy = str(brief.get("motion_strategy") or "").strip()
    duration_hint = str(brief.get("duration_hint") or "").strip()
    style_hint = str(brief.get("style_hint") or "").strip()
    aspect_ratio_hint = str(brief.get("aspect_ratio_hint") or "").strip()
    loop = brief.get("loop")

    primary = user_input or scene_description
    if not primary:
        return "", "", ""

    lines = [primary]
    if scene_description and scene_description != primary:
        lines.append(f"Scene focus: {scene_description}.")
    if genre:
        lines.append(f"Video genre: {genre}.")
    if motion_strategy:
        lines.append(f"Motion strategy: {motion_strategy}.")
    if style_hint:
        lines.append(f"Visual style guidance: {style_hint}.")
    if loop is True:
        lines.append("Make the clip loop cleanly.")
    elif loop is False:
        lines.append("Do not force a loop unless the motion naturally resolves that way.")

    ratio = aspect_ratio_hint if re.fullmatch(r"\d+:\d+", aspect_ratio_hint) else "adaptive"
    duration_seconds = parse_duration_seconds(duration_hint)

    return "\n".join(lines).strip(), ratio, duration_seconds


def normalize_video_mode(raw_mode: str, reference_image_url: str, first_frame_image_url: str, last_frame_image_url: str) -> str:
    mode = (raw_mode or "").strip().lower()
    aliases = {
        "text-to-video": "text-to-video",
        "text_only": "text-to-video",
        "text-only": "text-to-video",
        "t2v": "text-to-video",
        "first-frame": "first-frame",
        "first_frame": "first-frame",
        "image-to-video": "first-frame",
        "image_to_video": "first-frame",
        "i2v": "first-frame",
        "first-last-frame": "first-last-frame",
        "first_last_frame": "first-last-frame",
        "first+last-frame": "first-last-frame",
        "first-last": "first-last-frame",
    }
    if mode in aliases:
        return aliases[mode]
    if first_frame_image_url and last_frame_image_url:
        return "first-last-frame"
    if reference_image_url or first_frame_image_url:
        return "first-frame"
    return "text-to-video"


def is_remote_url(value: str) -> bool:
    return bool(re.match(r"^https?://", (value or "").strip(), re.IGNORECASE))


try:
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
except Exception:
    emit(status="fallback", fallback_reason="brief_invalid", warning="brief_invalid")
    raise SystemExit(0)

if not setup_path.exists():
    emit(status="fallback", fallback_reason="setup_state_missing", warning="setup_state_missing")
    raise SystemExit(0)

try:
    setup = json.loads(setup_path.read_text(encoding="utf-8"))
except Exception:
    emit(status="fallback", fallback_reason="setup_state_invalid", warning="setup_state_invalid")
    raise SystemExit(0)

video = setup.get("video") or {}
enabled = bool(video.get("enabled"))
provider = str(video.get("provider") or "").strip().lower()
model = str(video.get("model") or "").strip()
api_base_url = str(video.get("api_base_url") or DEFAULT_API_BASE_URL).rstrip("/")
api_key_source = str(video.get("api_key_source") or "").strip()
api_key = str(video.get("api_key") or "")
genre = str(brief.get("video_genre") or "").strip()
video_model_override = str(brief.get("video_model") or "").strip()
reference_image_url = str(
    brief.get("reference_image_url")
    or brief.get("reference_frame_url")
    or ""
).strip()
first_frame_image_url = str(brief.get("first_frame_image_url") or "").strip()
last_frame_image_url = str(brief.get("last_frame_image_url") or "").strip()
video_mode = normalize_video_mode(
    str(brief.get("video_mode") or ""),
    reference_image_url,
    first_frame_image_url,
    last_frame_image_url,
)
generate_audio = brief.get("generate_audio")
prompt, aspect_ratio_hint, duration_seconds = build_prompt(brief)

if not enabled:
    emit(status="fallback", fallback_reason="video_disabled", warning="", provider=provider, model=model, genre=genre)
    raise SystemExit(0)

if not provider or not model:
    emit(status="fallback", fallback_reason="video_config_incomplete", warning="", provider=provider, model=model, genre=genre)
    raise SystemExit(0)

if provider != "volcengine":
    emit(
        status="fallback",
        fallback_reason="video_provider_unsupported",
        warning="video_provider_unsupported",
        provider=provider,
        model=model,
        genre=genre,
    )
    raise SystemExit(0)

has_env_key = bool(api_key_source and os.environ.get(api_key_source))
has_inline_key = bool(api_key)
if not has_env_key and not has_inline_key:
    emit(
        status="fallback",
        fallback_reason="video_api_key_missing",
        warning="video_api_key_missing",
        provider=provider,
        model=model,
        genre=genre,
    )
    raise SystemExit(0)

if not prompt:
    emit(status="fallback", fallback_reason="empty_prompt", warning="", provider=provider, model=model, genre=genre)
    raise SystemExit(0)

if video_mode == "first-frame":
    if not reference_image_url:
        reference_image_url = first_frame_image_url
    if not reference_image_url:
        emit(
            status="fallback",
            fallback_reason="video_reference_image_missing",
            warning="video_reference_image_missing",
            provider=provider,
            model=model,
            genre=genre,
        )
        raise SystemExit(0)
    if not is_remote_url(reference_image_url):
        emit(
            status="fallback",
            fallback_reason="video_reference_image_not_url",
            warning=f"video reference image must be a remote URL, got: {reference_image_url}",
            provider=provider,
            model=model,
            genre=genre,
        )
        raise SystemExit(0)

if video_mode == "first-last-frame":
    if not first_frame_image_url or not last_frame_image_url:
        emit(
            status="fallback",
            fallback_reason="video_reference_frames_incomplete",
            warning="video_reference_frames_incomplete",
            provider=provider,
            model=model,
            genre=genre,
        )
        raise SystemExit(0)
    if not is_remote_url(first_frame_image_url):
        emit(
            status="fallback",
            fallback_reason="video_reference_image_not_url",
            warning=f"video first frame image must be a remote URL, got: {first_frame_image_url}",
            provider=provider,
            model=model,
            genre=genre,
        )
        raise SystemExit(0)
    if not is_remote_url(last_frame_image_url):
        emit(
            status="fallback",
            fallback_reason="video_reference_image_not_url",
            warning=f"video last frame image must be a remote URL, got: {last_frame_image_url}",
            provider=provider,
            model=model,
            genre=genre,
        )
        raise SystemExit(0)

base_model = model or DEFAULT_VIDEO_MODEL
if video_model_override:
    request_model = video_model_override
elif video_mode == "text-to-video" and base_model == DEFAULT_VIDEO_MODEL:
    request_model = DEFAULT_TEXT_TO_VIDEO_MODEL
else:
    request_model = base_model

emit(
    status="ready",
    provider=provider,
    model=request_model,
    api_base_url=api_base_url,
    api_key_source=api_key_source,
    api_key=api_key,
    request_model=request_model,
    genre=genre,
    prompt=prompt,
    aspect_ratio_hint=aspect_ratio_hint,
    duration_seconds=duration_seconds,
    video_mode=video_mode,
    reference_image_url=reference_image_url,
    first_frame_image_url=first_frame_image_url,
    last_frame_image_url=last_frame_image_url,
    generate_audio=bool(generate_audio),
)
PY
}

json_get() {
  python3 - "$1" "$2" <<'PY'
import json
import sys
data = json.loads(sys.argv[1])
value = data.get(sys.argv[2], "")
if isinstance(value, bool):
    print("true" if value else "false")
else:
    print(str(value))
PY
}

create_payload_file() {
  python3 - "$1" "$2" <<'PY'
import json
import sys
from pathlib import Path

runtime = json.loads(sys.argv[1])
payload_path = Path(sys.argv[2])
payload = {
    "model": runtime["request_model"],
    "content": [
        {
            "type": "text",
            "text": runtime["prompt"],
        }
    ],
    "ratio": runtime["aspect_ratio_hint"] or "adaptive",
    "duration": int(runtime["duration_seconds"] or 5),
    "watermark": False,
}
video_mode = str(runtime.get("video_mode") or "")
reference_image_url = str(runtime.get("reference_image_url") or "")
first_frame_image_url = str(runtime.get("first_frame_image_url") or "")
last_frame_image_url = str(runtime.get("last_frame_image_url") or "")

if video_mode == "first-frame" and reference_image_url:
    payload["content"].append(
        {
            "type": "image_url",
            "image_url": {
                "url": reference_image_url,
            },
        }
    )
elif video_mode == "first-last-frame":
    payload["content"].append(
        {
            "type": "image_url",
            "image_url": {
                "url": first_frame_image_url,
            },
            "role": "first_frame",
        }
    )
    payload["content"].append(
        {
            "type": "image_url",
            "image_url": {
                "url": last_frame_image_url,
            },
            "role": "last_frame",
        }
    )

if runtime.get("generate_audio") is True:
    payload["generate_audio"] = True
payload_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
print(str(payload_path))
PY
}

parse_create_response() {
  python3 -c '
import json
import sys

text = sys.stdin.read().strip()
try:
    data = json.loads(text)
except Exception:
    print("")
    raise SystemExit(0)

task_id = (
    data.get("id")
    or data.get("task_id")
    or (data.get("data") or {}).get("id")
    or (data.get("data") or {}).get("task_id")
    or ""
)
print(str(task_id))
'
}

parse_task_response() {
  python3 -c '
import json
import sys

text = sys.stdin.read().strip()

def lower(value):
    return str(value or "").strip().lower()

try:
    data = json.loads(text)
except Exception:
    print(json.dumps({"state": "invalid", "video_url": "", "warning": "task_response_invalid"}, ensure_ascii=True))
    raise SystemExit(0)

container = data.get("data") if isinstance(data.get("data"), dict) else data
status = lower(container.get("status"))
content = container.get("content") if isinstance(container.get("content"), dict) else {}
error = container.get("error")
warning = ""
if isinstance(error, dict):
    warning = str(error.get("message") or error.get("code") or "")
elif error:
    warning = str(error)
video_url = str(
    content.get("video_url")
    or container.get("video_url")
    or ""
)

if status in {"succeeded", "completed", "success"} and video_url:
    state = "completed"
elif status in {"failed", "cancelled", "canceled", "error"}:
    state = "failed"
elif status in {"queued", "running", "pending", "processing", "in_progress"}:
    state = "pending"
elif video_url:
    state = "completed"
else:
    state = "pending"

print(json.dumps({"state": state, "video_url": video_url, "warning": warning}, ensure_ascii=True))
'
}

RUNTIME_JSON="$(read_runtime_bundle)"
RUNTIME_STATUS="$(json_get "$RUNTIME_JSON" status)"

if [ "$RUNTIME_STATUS" != "ready" ]; then
  print_result \
    "fallback_h5" \
    "" \
    "" \
    "$(json_get "$RUNTIME_JSON" provider)" \
    "$(json_get "$RUNTIME_JSON" model)" \
    "$(json_get "$RUNTIME_JSON" genre)" \
    "$(json_get "$RUNTIME_JSON" fallback_reason)" \
    "$(json_get "$RUNTIME_JSON" warning)"
  exit 0
fi

PROVIDER="$(json_get "$RUNTIME_JSON" provider)"
MODEL="$(json_get "$RUNTIME_JSON" model)"
GENRE="$(json_get "$RUNTIME_JSON" genre)"
API_BASE_URL="$(json_get "$RUNTIME_JSON" api_base_url)"
API_KEY_SOURCE="$(json_get "$RUNTIME_JSON" api_key_source)"
INLINE_API_KEY="$(json_get "$RUNTIME_JSON" api_key)"

if [ -n "$API_KEY_SOURCE" ] && [ -n "${!API_KEY_SOURCE:-}" ]; then
  API_KEY="${!API_KEY_SOURCE}"
else
  API_KEY="$INLINE_API_KEY"
fi

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT
PAYLOAD_FILE="$TMPDIR/video-payload.json"
RESPONSE_FILE="$TMPDIR/response.json"

create_payload_file "$RUNTIME_JSON" "$PAYLOAD_FILE" >/dev/null

CREATE_URL="$API_BASE_URL/contents/generations/tasks"
QUERY_RESPONSE="$(
  set +e
  "$CURL_BIN" -fsS -X POST "$CREATE_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    --data "@$PAYLOAD_FILE" 2>&1
  echo "__EXIT_CODE:$?"
)"
CREATE_EXIT_CODE="$(printf '%s' "$QUERY_RESPONSE" | python3 -c 'import sys; text = sys.stdin.read(); print(text.rsplit("__EXIT_CODE:", 1)[1].strip() if "__EXIT_CODE:" in text else "1")')"
CREATE_BODY="$(printf '%s' "$QUERY_RESPONSE" | python3 -c 'import sys; text = sys.stdin.read(); print(text.rsplit("__EXIT_CODE:", 1)[0], end="")')"

if [ "$CREATE_EXIT_CODE" != "0" ]; then
  WARNING="$(printf '%s' "$CREATE_BODY" | normalize_warning)"
  print_result "fallback_h5" "" "" "$PROVIDER" "$MODEL" "$GENRE" "create_failed" "$WARNING"
  exit 0
fi

TASK_ID="$(printf '%s' "$CREATE_BODY" | parse_create_response)"
if [ -z "$TASK_ID" ]; then
  print_result "fallback_h5" "" "" "$PROVIDER" "$MODEL" "$GENRE" "create_response_invalid" "create_response_invalid"
  exit 0
fi

TRACKING_URL="$API_BASE_URL/contents/generations/tasks/$TASK_ID"
START_TS="$(date +%s)"

while true; do
  TASK_RESPONSE="$(
    set +e
    "$CURL_BIN" -fsS "$TRACKING_URL" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -H "Accept: application/json" 2>&1
    echo "__EXIT_CODE:$?"
  )"
  TASK_EXIT_CODE="$(printf '%s' "$TASK_RESPONSE" | python3 -c 'import sys; text = sys.stdin.read(); print(text.rsplit("__EXIT_CODE:", 1)[1].strip() if "__EXIT_CODE:" in text else "1")')"
  TASK_BODY="$(printf '%s' "$TASK_RESPONSE" | python3 -c 'import sys; text = sys.stdin.read(); print(text.rsplit("__EXIT_CODE:", 1)[0], end="")')"

  if [ "$TASK_EXIT_CODE" != "0" ]; then
    WARNING="$(printf '%s' "$TASK_BODY" | normalize_warning)"
    print_result "fallback_h5" "" "$TRACKING_URL" "$PROVIDER" "$MODEL" "$GENRE" "query_failed" "$WARNING"
    exit 0
  fi

  TASK_JSON="$(printf '%s' "$TASK_BODY" | parse_task_response)"
  TASK_STATE="$(json_get "$TASK_JSON" state)"
  VIDEO_URL="$(json_get "$TASK_JSON" video_url)"
  TASK_WARNING="$(json_get "$TASK_JSON" warning)"

  if [ "$TASK_STATE" = "completed" ] && [ -n "$VIDEO_URL" ]; then
    print_result "video_url" "$VIDEO_URL" "$TRACKING_URL" "$PROVIDER" "$MODEL" "$GENRE" "" ""
    exit 0
  fi

  if [ "$TASK_STATE" = "failed" ]; then
    print_result "fallback_h5" "" "$TRACKING_URL" "$PROVIDER" "$MODEL" "$GENRE" "video_task_failed" "$TASK_WARNING"
    exit 0
  fi

  NOW_TS="$(date +%s)"
  if [ "$TIMEOUT_SECONDS" -le 0 ] || [ $((NOW_TS - START_TS)) -ge "$TIMEOUT_SECONDS" ]; then
    print_result "pending_tracking" "" "$TRACKING_URL" "$PROVIDER" "$MODEL" "$GENRE" "" "$TASK_WARNING"
    exit 0
  fi

  sleep "$POLL_INTERVAL_SECONDS"
done
