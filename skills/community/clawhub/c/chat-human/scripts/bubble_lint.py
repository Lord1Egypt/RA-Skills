#!/usr/bin/env python3
"""
Deterministic linter for thumb-typed IM chat bubbles, plain-reply micro-beats,
and complementary TTS voice notes.

Checks outbound multi-bubble JSON payloads (`{"messages": [...]}`) or plain-reply
drafts (`--surface auto|json|plain`) against Layer 1 Chat Human invariants:
  - Single voice note max; never attach `voice_mode` / `tts` at batch root with >1 bubble
  - Plain-reply surface hygiene (flags leaked `{"messages": ...}` JSON or `Bubble 1:` labels)
  - Bubble count and mobile thumb-reading length budgets (CJK chars & English words)
  - No Markdown headers, tables, fenced code blocks, bold-bullet walls, or numbered walls
  - No RPG stage-direction brackets (`*sighs*`, `（叹气）`), concierge clichés, `啦` spam,
    trailing-period spam on short beats, unrendered `{{user}}` placeholders, or backend TTS error leaks
  - Unicode emoji gated by `--persona-emoji allow|deny` (default: `deny`)
  - Text bubble × `tts.text` complementarity (flags verbatim paraphrase & raw paths/URLs/numbers)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any, Dict, List, Sequence, Tuple

CJK_CHAR_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
EN_WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
MD_HEADER_RE = re.compile(r"(?m)^\s*#{1,6}\s+\S")
MD_TABLE_RE = re.compile(r"(?m)^\s*\|.*\|\s*$\n^\s*\|[\s:\-|]+\|\s*$")
MD_CODE_FENCE_RE = re.compile(r"```")
MD_BOLD_BULLET_RE = re.compile(r"(?m)^\s*[-*]\s+\*\*[^*\n]+\*\*")
NUMBERED_WALL_RE = re.compile(r"(?:^|\n)\s*1[\.\)]\s+.+(?:\n\s*2[\.\)]\s+.+)", re.DOTALL)
RAW_URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
WIN_OR_UNIX_PATH_RE = re.compile(r"(?:[A-Za-z]:\\[A-Za-z0-9_.\-\\]+|/(?:usr|etc|var|opt|home|Users|tmp)/[A-Za-z0-9_.\-/]+)")
RAW_DECIMAL_OR_TIME_RE = re.compile(r"(?<!\d)(?:\d+\.\d+|\d{1,2}:\d{2})(?!\.\d)")
LA_ENDING_CLAUSE_RE = re.compile(r"啦(?=(?:[\s\U0001F300-\U0001FAFF\u2600-\u27BF！!？?~～。，,]|$))")

PLAIN_META_LEAK_RE = re.compile(
    r'(?:\{\s*"(?:messages|bubbles)"\s*:|(?:^|\n)\s*(?:Bubble|Beat|气泡)\s*[1-9]\s*[:：]|```json)',
    re.IGNORECASE,
)
PLACEHOLDER_LEAK_RE = re.compile(r"\{\{\s*(?:user|char)\s*\}\}", re.IGNORECASE)
SYSTEM_ERROR_LEAK_RE = re.compile(
    r"(?:语音合成插件|语音服务没启用|未配置.{0,8}(?:TTS|语音)|media\s+provider|tts\s+(?:plugin|provider)\s+(?:not|is\s+not|missing))",
    re.IGNORECASE,
)

STAGE_BRACKET_RE = re.compile(
    r"(?:\*[a-zA-Z][a-zA-Z\s\-]{1,28}\*|[（(](?:叹气|笑|微笑|苦笑|歪头|叉腰|双手叉腰|气鼓鼓|摸头|摸摸头|捂脸|扶额|耸肩|小声|轻声|皱眉|眨眼|挑眉|擦汗|深呼吸|sighs?|smiles?|laughs?|giggles?|tilts\s+head|shrugs?|whispers?|grins?|rolls\s+eyes)[）)])",
    re.IGNORECASE,
)

STEWARD_CLICHE_RE = re.compile(
    r"(?:向你汇报|请(?:随时)?检阅|顺手替你|乖乖(?:去)?(?:睡觉|补觉)|希望(?:这)?(?:对您|对你)?有帮助|reporting\s+back\s+to\s+you|for\s+your\s+(?:kind\s+)?review|hope\s+this\s+helps|let\s+me\s+know\s+if\s+you\s+need\s+anything\s+else)",
    re.IGNORECASE,
)

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA70-\U0001FAFF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "]"
)

ABBREV_END_RE = re.compile(r"\b(?:etc|e\.g|i\.e|vs|mr|mrs|ms|dr|st|a\.m|p\.m)\.$", re.IGNORECASE)
CODE_PERIOD_END_RE = re.compile(r"[A-Za-z0-9]{4,}[。\.]$")


def count_units(text: str) -> Tuple[int, int]:
    """Return (cjk_char_count, english_word_count)."""
    cjk = len(CJK_CHAR_RE.findall(text))
    en_words = len(EN_WORD_RE.findall(CJK_CHAR_RE.sub(" ", text)))
    return cjk, en_words


def _ends_with_formal_period(text: str) -> bool:
    s = text.strip()
    if not s:
        return False
    if s.endswith("。"):
        return True
    if s.endswith(".") and not s.endswith("..") and not ABBREV_END_RE.search(s):
        return True
    return False


def _is_short_single_clause_with_period(text: str) -> bool:
    s = text.strip()
    if not _ends_with_formal_period(s):
        return False
    if CODE_PERIOD_END_RE.search(s):
        return True
    body = s[:-1].strip()
    # Exclude multi-sentence text containing internal sentence-final stops
    if re.search(r"[。！？!?；;]", body):
        return False
    cjk, en_words = count_units(body)
    if cjk > 0 and cjk <= 22 and en_words <= 6:
        return True
    if cjk == 0 and 0 < en_words <= 12:
        return True
    return False


def char_bigrams(text: str) -> set[str]:
    cleaned = re.sub(r"[\s\W_]+", "", text.lower())
    if len(cleaned) < 2:
        return {cleaned} if cleaned else set()
    return {cleaned[i : i + 2] for i in range(len(cleaned) - 1)}


def compute_overlap(bubble_texts: Sequence[str], tts_text: str) -> float:
    """Compute directional bigram coverage of tts_text already present in bubble_texts."""
    joined_bubbles = " ".join(bubble_texts)
    b_grams = char_bigrams(joined_bubbles)
    t_grams = char_bigrams(tts_text)
    if not b_grams or not t_grams:
        return 0.0
    return len(b_grams & t_grams) / float(len(t_grams))


def _split_plain_beats(stripped: str, *, explicit_plain_surface: bool) -> List[str]:
    if not stripped:
        return []
    if re.search(r"\n\s*\n", stripped):
        return [blk.strip() for blk in re.split(r"\n\s*\n+", stripped) if blk.strip()]
    if MD_TABLE_RE.search(stripped) or MD_CODE_FENCE_RE.search(stripped) or NUMBERED_WALL_RE.search(stripped):
        return [stripped]
    lines = [ln.strip() for ln in stripped.splitlines() if ln.strip()]
    if explicit_plain_surface and len(lines) <= 2:
        # Preserve tightly coupled 2-line copy-paste units (e.g. locker + pickup code)
        return ["\n".join(lines)]
    return lines


def parse_payload(
    raw: str,
    explicit_tts: str | None = None,
    *,
    surface: str = "auto",
) -> Dict[str, Any]:
    if surface not in ("auto", "json", "plain"):
        raise ValueError(f"Unsupported surface {surface!r}; expected auto, json, or plain")

    stripped = raw.strip()
    if surface == "plain":
        meta_leak = bool(PLAIN_META_LEAK_RE.search(stripped))
        beats = _split_plain_beats(stripped, explicit_plain_surface=True)
        payload: Dict[str, Any] = {
            "messages": [{"text": b} for b in beats],
            "_plain_meta_leak": meta_leak,
        }
    elif surface == "json" or (surface == "auto" and (stripped.startswith("{") or stripped.startswith("["))):
        data = json.loads(stripped)
        if isinstance(data, list):
            payload = {"messages": data}
        elif isinstance(data, dict):
            payload = dict(data)
        else:
            raise ValueError("JSON input must be an object or array of messages")
    else:
        meta_leak = bool(PLAIN_META_LEAK_RE.search(stripped))
        beats = _split_plain_beats(stripped, explicit_plain_surface=False)
        payload = {
            "messages": [{"text": b} for b in beats],
            "_plain_meta_leak": meta_leak,
        }

    if explicit_tts:
        msgs = payload.setdefault("messages", [])
        if msgs and isinstance(msgs[-1], dict):
            msgs[-1] = dict(msgs[-1])
            msgs[-1]["voice_mode"] = "append"
            msgs[-1]["tts"] = {"text": explicit_tts}
        else:
            payload["tts"] = {"text": explicit_tts}
    return payload


def lint_payload(
    payload: Dict[str, Any],
    *,
    max_bubbles: int | None = None,
    max_cjk_chars: int = 55,
    max_en_words: int = 45,
    persona_emoji: str = "deny",
    max_tts_overlap: float = 0.50,
) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []

    if payload.get("_plain_meta_leak"):
        issues.append(
            {
                "code": "plain.meta_leak",
                "level": "error",
                "message": "Plain-reply output leaked raw `{\"messages\": ...}` / `{\"bubbles\": ...}` JSON or `Bubble 1:` labels.",
            }
        )

    raw_bubbles = payload.get("bubbles")
    raw_messages = payload.get("messages")
    used_bubbles_protocol = raw_bubbles is not None and raw_messages is None
    effective_max_bubbles = max_bubbles if max_bubbles is not None else (4 if used_bubbles_protocol else 3)

    if used_bubbles_protocol:
        if not isinstance(raw_bubbles, list):
            return [{"code": "schema.invalid_bubbles", "level": "error", "message": "`bubbles` must be an array of strings."}]
        messages = [b if isinstance(b, dict) else {"text": str(b)} for b in raw_bubbles]
        voice_note = payload.get("voice_note")
        if isinstance(voice_note, dict) and str(voice_note.get("text") or "").strip():
            if messages:
                messages[-1] = {
                    **messages[-1],
                    "voice_mode": "append",
                    "tts": {"text": str(voice_note.get("text") or "").strip(), "emotion": voice_note.get("emotion")},
                }
            else:
                messages = [{"text": "", "voice_mode": "only", "tts": {"text": str(voice_note.get("text") or "").strip()}}]
        used_messages_array = False
    elif raw_messages is None:
        single_text = payload.get("text")
        messages = [
            {
                "text": single_text or "",
                "voice_mode": payload.get("voice_mode"),
                "tts": payload.get("tts"),
            }
        ]
        used_messages_array = False
    else:
        if not isinstance(raw_messages, list):
            return [{"code": "schema.invalid_messages", "level": "error", "message": "`messages` must be an array."}]
        messages = [m if isinstance(m, dict) else {"text": str(m)} for m in raw_messages]
        used_messages_array = True

    non_empty_texts = [str(m.get("text") or "").strip() for m in messages if str(m.get("text") or "").strip()]
    has_any_tts = any(
        (m.get("voice_mode") in ("append", "only")) or isinstance(m.get("tts"), dict) for m in messages
    ) or (payload.get("voice_mode") in ("append", "only")) or isinstance(payload.get("tts"), dict)

    if len(messages) == 0 or (not non_empty_texts and not has_any_tts):
        issues.append({"code": "bubble.empty", "level": "error", "message": "No chat bubbles found in payload."})
        return issues

    if len(messages) > effective_max_bubbles:
        issues.append(
            {
                "code": "bubble.too_many",
                "level": "error",
                "message": f"Found {len(messages)} bubbles (max {effective_max_bubbles}); consolidate or offload long detail.",
            }
        )

    # Check batch-root TTS duplication hazard
    top_voice_mode = payload.get("voice_mode")
    top_tts = payload.get("tts")
    if used_messages_array and len(messages) > 1:
        if (top_voice_mode and top_voice_mode != "none") or top_tts is not None:
            issues.append(
                {
                    "code": "tts.batch_root_duplication",
                    "level": "error",
                    "message": "Top-level `voice_mode`/`tts` on a multi-bubble `messages[]` call duplicates voice notes; attach TTS only on the final bubble.",
                }
            )

    bubble_texts: List[str] = []
    tts_entries: List[Tuple[int, str]] = []
    la_endings = 0
    formal_period_bubbles = 0
    short_period_flagged = False

    for idx, item in enumerate(messages):
        text = str(item.get("text") or "").strip()
        bubble_texts.append(text)

        if not payload.get("_plain_meta_leak") and PLAIN_META_LEAK_RE.search(text):
            issues.append(
                {
                    "code": "plain.meta_leak",
                    "level": "error",
                    "message": f"Bubble {idx + 1} contains `Bubble 1:` labels or raw `messages` JSON markup.",
                }
            )

        if (
            MD_HEADER_RE.search(text)
            or MD_TABLE_RE.search(text)
            or MD_CODE_FENCE_RE.search(text)
            or MD_BOLD_BULLET_RE.search(text)
            or NUMBERED_WALL_RE.search(text)
        ):
            issues.append(
                {
                    "code": "bubble.markdown_structure",
                    "level": "error",
                    "message": f"Bubble {idx + 1} contains Markdown headers, tables, code fences, or structured list walls; move dense content to an artifact.",
                }
            )

        if STAGE_BRACKET_RE.search(text):
            issues.append(
                {
                    "code": "style.stage_brackets",
                    "level": "error",
                    "message": f"Bubble {idx + 1} contains RPG stage-direction brackets (`*sighs*` / `（叹气）`).",
                }
            )

        if PLACEHOLDER_LEAK_RE.search(text):
            issues.append(
                {
                    "code": "style.placeholder_leak",
                    "level": "error",
                    "message": f"Bubble {idx + 1} contains unrendered `{{{{user}}}}` / `{{{{char}}}}` template placeholders.",
                }
            )

        if SYSTEM_ERROR_LEAK_RE.search(text):
            issues.append(
                {
                    "code": "style.system_error_leak",
                    "level": "error",
                    "message": f"Bubble {idx + 1} leaks backend TTS/plugin diagnostics into user-facing chat text.",
                }
            )

        if STEWARD_CLICHE_RE.search(text):
            issues.append(
                {
                    "code": "style.steward_cliche",
                    "level": "warning",
                    "message": f"Bubble {idx + 1} uses subordinate/concierge boilerplate (`向你汇报` / `顺手替你` / `for your review`).",
                }
            )

        if persona_emoji == "deny" and EMOJI_RE.search(text):
            issues.append(
                {
                    "code": "style.unicode_emoji",
                    "level": "warning",
                    "message": f"Bubble {idx + 1} contains Unicode emoji while `--persona-emoji deny` is active.",
                }
            )

        if LA_ENDING_CLAUSE_RE.search(text):
            la_endings += 1

        if _ends_with_formal_period(text):
            formal_period_bubbles += 1
        if _is_short_single_clause_with_period(text) and not short_period_flagged:
            short_period_flagged = True
            issues.append(
                {
                    "code": "style.trailing_period",
                    "level": "warning",
                    "message": f"Bubble {idx + 1} ends a short single-clause beat or copyable code with a formal period (`。` / `.`).",
                }
            )

        vm = item.get("voice_mode")
        tts_obj = item.get("tts")
        has_voice = (vm in ("append", "only")) or isinstance(tts_obj, dict)
        if has_voice:
            tts_text = ""
            if isinstance(tts_obj, dict):
                tts_text = str(tts_obj.get("text") or "").strip()
            if not tts_text and vm in ("append", "only"):
                tts_text = text
            tts_entries.append((idx, tts_text))

    if not short_period_flagged and len(non_empty_texts) >= 2 and formal_period_bubbles == len(non_empty_texts):
        issues.append(
            {
                "code": "style.trailing_period",
                "level": "warning",
                "message": f"All {len(non_empty_texts)} beats end with formal periods (`。` / `.`); omit trailing periods on mobile chat beats.",
            }
        )

    # Total length budget check
    total_cjk = sum(count_units(t)[0] for t in bubble_texts)
    total_en = sum(count_units(t)[1] for t in bubble_texts)
    if total_cjk > max_cjk_chars:
        issues.append(
            {
                "code": "bubble.over_cjk_budget",
                "level": "warning",
                "message": f"Total CJK length is {total_cjk} chars (budget <= {max_cjk_chars}); trim filler or offload details.",
            }
        )
    if total_en > max_en_words:
        issues.append(
            {
                "code": "bubble.over_en_budget",
                "level": "warning",
                "message": f"Total English word count is {total_en} words (budget <= {max_en_words}); tighten clauses.",
            }
        )

    if len(messages) >= 2 and la_endings / float(len(messages)) > 0.5:
        issues.append(
            {
                "code": "style.particle_spam",
                "level": "warning",
                "message": f"{la_endings}/{len(messages)} bubbles end with `啦`; vary bare verb endings and natural particles.",
            }
        )

    # Voice note checks
    if len(tts_entries) > 1:
        issues.append(
            {
                "code": "tts.multiple_clips",
                "level": "error",
                "message": f"Found {len(tts_entries)} voice notes in one turn; send at most 1 voice note.",
            }
        )
    elif len(tts_entries) == 1:
        tts_idx, tts_text = tts_entries[0]
        if used_messages_array and len(messages) > 1 and tts_idx != len(messages) - 1:
            issues.append(
                {
                    "code": "tts.not_on_final_bubble",
                    "level": "warning",
                    "message": f"Voice note is attached to bubble {tts_idx + 1} instead of final bubble {len(messages)}.",
                }
            )
        if tts_text:
            overlap = compute_overlap(bubble_texts, tts_text)
            if overlap > max_tts_overlap and any(t.strip() for t in bubble_texts):
                issues.append(
                    {
                        "code": "tts.verbatim_overlap",
                        "level": "error",
                        "message": f"`tts.text` overlaps {overlap:.0%} with text bubbles; write a complementary aside instead of reading the text bubble aloud.",
                    }
                )
            if RAW_URL_RE.search(tts_text) or WIN_OR_UNIX_PATH_RE.search(tts_text):
                issues.append(
                    {
                        "code": "tts.raw_path_or_url",
                        "level": "error",
                        "message": "`tts.text` contains a raw URL or filesystem path; keep identifiers in text bubbles only.",
                    }
                )
            tts_without_urls = RAW_URL_RE.sub(" ", tts_text)
            if RAW_DECIMAL_OR_TIME_RE.search(tts_without_urls):
                issues.append(
                    {
                        "code": "tts.unnormalized_numbers",
                        "level": "warning",
                        "message": "`tts.text` contains raw decimals or clock colons (`19.9`, `14:30`); spell them as spoken words.",
                    }
                )

    return issues


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint IM chat-bubble payloads, plain-reply beats, and TTS complementarity.")
    parser.add_argument("--input", "-i", type=pathlib.Path, default=None, help="JSON or plain-text file (defaults to stdin)")
    parser.add_argument(
        "--surface",
        choices=("auto", "json", "plain"),
        default="auto",
        help="Delivery surface mode: auto (default), json (SendMessage payload), or plain (ordinary reply stream)",
    )
    parser.add_argument("--tts-text", type=str, default=None, help="Optional TTS script when linting plain-text bubbles")
    parser.add_argument("--max-bubbles", type=int, default=None, help="Maximum bubbles per turn (default: 4 for bubbles[], 3 for messages[])")
    parser.add_argument("--max-cjk-chars", type=int, default=55, help="Maximum total CJK characters (default: 55)")
    parser.add_argument("--max-en-words", type=int, default=45, help="Maximum total English words (default: 45)")
    parser.add_argument("--persona-emoji", choices=("deny", "allow"), default="deny", help="Whether active persona permits Unicode emoji")
    parser.add_argument("--max-tts-overlap", type=float, default=0.50, help="Max allowed bigram coverage between bubbles and TTS")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args(argv)

    if args.input is not None:
        raw = args.input.read_text(encoding="utf-8")
    else:
        if sys.stdin.isatty():
            parser.error("Provide --input <file> or pipe a JSON/text payload via stdin.")
        raw = sys.stdin.read()

    try:
        payload = parse_payload(raw, explicit_tts=args.tts_text, surface=args.surface)
    except Exception as exc:
        report = {"ok": False, "issues": [{"code": "input.parse_error", "level": "error", "message": str(exc)}]}
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"[error] input.parse_error: {exc}", file=sys.stderr)
        return 2

    issues = lint_payload(
        payload,
        max_bubbles=args.max_bubbles,
        max_cjk_chars=args.max_cjk_chars,
        max_en_words=args.max_en_words,
        persona_emoji=args.persona_emoji,
        max_tts_overlap=args.max_tts_overlap,
    )
    ok = len(issues) == 0

    if args.json:
        print(json.dumps({"ok": ok, "issue_count": len(issues), "issues": issues}, ensure_ascii=False, indent=2))
    else:
        if ok:
            print("OK: chat-human lint passed (0 issues).")
        else:
            for item in issues:
                print(f"[{item['level']}] {item['code']}: {item['message']}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
