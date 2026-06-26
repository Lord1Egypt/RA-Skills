#!/bin/bash
set -euo pipefail

# Usage: post-delivery.sh <gift-metadata-json> <setup-state-json>
# Performs guaranteed mechanical bookkeeping only:
# - update setup-state timestamps and recent_gifts
# - append to gift-history.jsonl

METADATA_FILE="${1:-}"
SETUP_STATE_FILE="${2:-}"

if [ -z "$METADATA_FILE" ] || [ -z "$SETUP_STATE_FILE" ]; then
  echo "Usage: post-delivery.sh <gift-metadata-json> <setup-state-json>" >&2
  exit 1
fi

if [ ! -f "$METADATA_FILE" ]; then
  echo "metadata file not found: $METADATA_FILE" >&2
  exit 1
fi

python3 - "$METADATA_FILE" "$SETUP_STATE_FILE" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

meta_path = Path(sys.argv[1]).expanduser()
setup_path = Path(sys.argv[2]).expanduser()
history_path = setup_path.parent / "gift-history.jsonl"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_json(path: Path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty_dict(value):
    if not isinstance(value, dict):
        return {}
    return {k: v for k, v in value.items() if v not in ("", None, [])}


TEXT_PLAY_OUTPUT_SHAPES = {
    "worldbuilder": "text-play-worldbuilder",
    "one-word-worldbuilder": "text-play-worldbuilder",
    "riddle": "text-play-riddle",
    "riddle-chain": "text-play-riddle",
    "emoji-riddle": "text-play-riddle",
    "emoji-riddle-chain": "text-play-riddle",
    "micro-story": "text-play-micro-story",
    "relay-story": "text-play-micro-story",
    "micro-adventure": "text-play-micro-story",
    "three-choice-micro-adventure": "text-play-micro-story",
    "choose-your-own-adventure": "text-play-micro-story",
    "roleplay": "text-play-roleplay",
    "role-play": "text-play-roleplay",
    "roleplay-micro-theater": "text-play-roleplay",
    "role-play-micro-theater": "text-play-roleplay",
    "micro-theater": "text-play-roleplay",
}


def infer_text_play_output_shape(text_play_type: str) -> str:
    normalized = text_play_type.strip().lower().replace("_", "-")
    if not normalized:
        return "text-play-micro-story"
    return TEXT_PLAY_OUTPUT_SHAPES.get(normalized, "text-play-micro-story")


def merge_from_meta(explicit_entry, keep_keys):
    base_entry = {k: meta[k] for k in keep_keys if k in meta and meta[k] not in ("", None, [])}
    return {**base_entry, **nonempty_dict(explicit_entry)}


def apply_runtime_defaults(entry):
    pattern_or_format = str(entry.get("pattern_or_format") or meta.get("pattern_or_format") or "").strip()
    if pattern_or_format != "text-play":
        return entry

    for key in [
        "text_play_type",
        "text_play_turn_count",
        "text_play_completed",
        "text_play_exit_reason",
    ]:
        if key not in entry and meta.get(key) not in ("", None, []):
            entry[key] = meta[key]

    text_play_type = str(entry.get("text_play_type") or "").strip()
    entry.setdefault("output_shape", infer_text_play_output_shape(text_play_type))
    entry.setdefault("visual_style", "chat-native")
    entry.setdefault("content_direction", "play")
    return entry


meta = read_json(meta_path)
setup = read_json(setup_path)

timestamp = (
    meta.get("sent_at")
    or meta.get("recorded_at")
    or meta.get("timestamp")
    or now_iso()
)

summary = str(meta.get("summary") or meta.get("last_gift_summary") or "").strip()
trigger_mode = str(meta.get("trigger_mode") or meta.get("last_run_mode") or "unknown").strip()
decision = str(meta.get("decision") or "sent").strip()

recent_limit = int(setup.get("recent_gifts_limit") or 30)
recent_gifts = list(setup.get("recent_gifts") or [])

recent_entry = meta.get("recent_gift_entry")
recent_keep_keys = [
    "sent_at",
    "trigger_mode",
    "gift_weight",
    "narrative_role",
    "tone",
    "pattern_or_format",
    "output_shape",
    "visual_style",
    "content_direction",
    "content_tags",
    "emotional_direction",
    "summary",
    "visual_elements",
    "concept_family",
    "concept_theme",
    "text_play_type",
    "text_play_turn_count",
    "text_play_completed",
    "text_play_exit_reason",
]
recent_entry = merge_from_meta(recent_entry, recent_keep_keys)
recent_entry = apply_runtime_defaults(recent_entry)
recent_entry.setdefault("sent_at", timestamp)
recent_entry.setdefault("trigger_mode", trigger_mode)
if summary:
    recent_entry.setdefault("summary", summary)

recent_gifts.append(recent_entry)
setup["recent_gifts"] = recent_gifts[-recent_limit:]
setup["last_sent_at"] = timestamp
setup["last_gift_summary"] = summary
setup["last_run_at"] = timestamp
setup["last_run_mode"] = trigger_mode
setup["last_run_outcome"] = decision

setup_path.parent.mkdir(parents=True, exist_ok=True)
setup_path.write_text(json.dumps(setup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

history_record = meta.get("history_record")
history_keep_keys = [
    "record_type",
    "recorded_at",
    "sent_at",
    "trigger_mode",
    "decision",
    "gift_weight",
    "narrative_role",
    "tone",
    "pattern_or_format",
    "output_shape",
    "visual_style",
    "content_direction",
    "content_tags",
    "emotional_direction",
    "used_memory_dates",
    "used_source_quotes",
    "used_source_images",
    "summary",
    "why_it_mattered",
    "quality_note",
    "visual_elements",
    "concept_family",
    "concept_theme",
    "image_mode",
    "video_mode",
    "generate_audio",
    "text_play_type",
    "text_play_turn_count",
    "text_play_completed",
    "text_play_exit_reason",
]
history_record = merge_from_meta(history_record, history_keep_keys)
history_record = apply_runtime_defaults(history_record)
history_record.setdefault("record_type", "gift")
history_record.setdefault("recorded_at", timestamp)
history_record.setdefault("sent_at", timestamp)
history_record.setdefault("trigger_mode", trigger_mode)
history_record.setdefault("decision", decision)
if summary:
    history_record.setdefault("summary", summary)

history_path.parent.mkdir(parents=True, exist_ok=True)
with history_path.open("a", encoding="utf-8") as fh:
    fh.write(json.dumps(history_record, ensure_ascii=False) + "\n")
PY
