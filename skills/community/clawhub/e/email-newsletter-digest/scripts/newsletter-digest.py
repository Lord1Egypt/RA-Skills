#!/usr/bin/env python3

import argparse
import base64
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from html import escape
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SETTINGS_PATH = SKILL_ROOT / "settings.json"
SKILL_DISPLAY_NAME = "Email Newsletter Digest"
FAILURE_PLACEHOLDER = "[Summarization failed for this newsletter]"
DEFAULT_RECIPIENT_DELIVERY_MODE = "group"
RECIPIENT_DELIVERY_MODE_ALIASES = {
    "individual": "individual",
    "individual_emails": "individual",
    "separate": "individual",
    "group": "group",
    "single": "group",
    "single_email": "group",
}
DEFAULT_PROMPT = (
    "List each individual news item as a concise bullet point (one sentence each). "
    "No section headers or groupings. Each bullet must stand alone as a self-contained fact."
)
PLACEHOLDER_PATTERNS = (
    "scrambling the email",
    "read it in full online",
)
STOPWORDS = {
    "about",
    "after",
    "amid",
    "among",
    "and",
    "are",
    "because",
    "been",
    "before",
    "being",
    "between",
    "both",
    "but",
    "could",
    "during",
    "from",
    "have",
    "into",
    "just",
    "more",
    "news",
    "newsletter",
    "over",
    "said",
    "says",
    "that",
    "their",
    "them",
    "then",
    "there",
    "these",
    "the",
    "they",
    "this",
    "through",
    "today",
    "told",
    "under",
    "very",
    "what",
    "when",
    "where",
    "which",
    "while",
    "with",
    "would",
}


@dataclass
class Settings:
    newsletter_labels_csv: str | None
    newsletter_senders_csv: str | None
    digest_recipient_emails_csv: str | None
    recipient_delivery_mode: str
    labels: list[str]
    senders: list[str]
    recipients: list[str]


@dataclass
class SummaryOutcome:
    text: str
    error: str | None
    model: str | None


def log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", file=sys.stderr)


def ensure_runtime_path() -> None:
    if shutil.which("summarize"):
        return
    raise RuntimeError("The `summarize` CLI is not available in PATH.")


def sanitize_error_text(text: str, *, fallback: str) -> str:
    cleaned = " ".join(line.strip() for line in text.splitlines() if line.strip())
    cleaned = re.sub(r"(?i)\b(sk-[a-z0-9_-]+)\b", "[redacted]", cleaned)
    cleaned = re.sub(r"(?i)\b(gh[pousr]_[a-z0-9_]+)\b", "[redacted]", cleaned)
    cleaned = re.sub(r"(?i)\b(AIza[0-9A-Za-z\-_]+)\b", "[redacted]", cleaned)
    cleaned = cleaned[:240].strip()
    return cleaned or fallback


def run_command(
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )
    if check and result.returncode != 0:
        cmd = " ".join(shlex.quote(part) for part in args)
        details = sanitize_error_text(
            result.stderr or result.stdout,
            fallback=f"exit code {result.returncode}",
        )
        raise RuntimeError(f"Command failed: {cmd} ({details})")
    return result


def build_account_args(account: str | None) -> list[str]:
    return ["--account", account] if account else []


def parse_csv_list(raw_value: Any) -> list[str]:
    if raw_value is None:
        return []
    if not isinstance(raw_value, str):
        raise ValueError("CSV settings must be strings or null.")

    parts = [item.strip() for item in raw_value.split(",")]
    deduped: list[str] = []
    seen: set[str] = set()
    for part in parts:
        if not part:
            continue
        lowered = part.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(part)
    return deduped


def parse_recipient_delivery_mode(raw_value: Any) -> str:
    if raw_value is None:
        return DEFAULT_RECIPIENT_DELIVERY_MODE
    if not isinstance(raw_value, str):
        raise ValueError("`recipient_delivery_mode` must be a string if provided.")
    normalized = raw_value.strip().lower().replace("-", "_").replace(" ", "_")
    mode = RECIPIENT_DELIVERY_MODE_ALIASES.get(normalized)
    if mode:
        return mode
    allowed = ", ".join(sorted(set(RECIPIENT_DELIVERY_MODE_ALIASES.values())))
    raise ValueError(f"`recipient_delivery_mode` must be one of: {allowed}.")


def load_settings(settings_path: Path) -> Settings:
    raw = json.loads(settings_path.read_text())

    labels = parse_csv_list(raw.get("newsletter_labels_csv"))
    senders = parse_csv_list(raw.get("newsletter_senders_csv"))
    if not labels and not senders:
        raise ValueError(
            "At least one of `newsletter_labels_csv` or `newsletter_senders_csv` must be populated."
        )

    recipients_raw = raw.get("digest_recipient_emails_csv")
    if recipients_raw is None:
        recipients_raw = raw.get("digest_recipient_email")
    recipients = parse_csv_list(recipients_raw)
    if not recipients:
        raise ValueError(
            "At least one recipient must be provided via `digest_recipient_emails_csv`."
        )
    recipient_delivery_mode = parse_recipient_delivery_mode(raw.get("recipient_delivery_mode"))

    return Settings(
        newsletter_labels_csv=raw.get("newsletter_labels_csv"),
        newsletter_senders_csv=raw.get("newsletter_senders_csv"),
        digest_recipient_emails_csv=(
            recipients_raw.strip() if isinstance(recipients_raw, str) else None
        ),
        recipient_delivery_mode=recipient_delivery_mode,
        labels=labels,
        senders=senders,
        recipients=recipients,
    )


def gmail_quote(value: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9._@+\-/]+", value):
        return value
    escaped = value.replace('"', '\\"')
    return f'"{escaped}"'


def build_gmail_query(labels: list[str], senders: list[str]) -> str:
    atoms: list[str] = []
    atoms.extend(f"label:{gmail_quote(label)}" for label in labels)
    atoms.extend(f"from:{gmail_quote(sender)}" for sender in senders)

    if not atoms:
        raise ValueError("Cannot build Gmail query without labels or senders.")

    query_core = atoms[0] if len(atoms) == 1 else f"({' OR '.join(atoms)})"
    return f"{query_core} newer_than:1d"


def looks_like_placeholder_body(body: str) -> bool:
    normalized = body.lower()
    if PLACEHOLDER_PATTERNS[0] in normalized:
        return True
    return PLACEHOLDER_PATTERNS[1] in normalized and "unsubscribe" in normalized


def decode_part_body(part: dict[str, Any]) -> str:
    body = part.get("body") or {}
    data = body.get("data")
    if not data:
        return ""
    padding = "=" * (-len(data) % 4)
    try:
        return base64.urlsafe_b64decode(data + padding).decode("utf-8", "ignore")
    except Exception:
        return ""


def walk_parts(part: dict[str, Any], output: list[dict[str, Any]]) -> None:
    if not isinstance(part, dict):
        return
    output.append(part)
    for child in part.get("parts") or []:
        walk_parts(child, output)


def fetch_best_message_body(message_id: str, account: str | None) -> str:
    result = run_command(
        ["gog", "gmail", "get", message_id, *build_account_args(account), "--json"],
        check=True,
    )
    payload = json.loads(result.stdout)
    message = payload.get("message") or {}
    root_payload = message.get("payload") or {}

    parts: list[dict[str, Any]] = []
    walk_parts(root_payload, parts)

    for mime_type in ("text/html", "text/plain"):
        for part in parts:
            if part.get("mimeType") != mime_type:
                continue
            decoded = decode_part_body(part).strip()
            if decoded:
                return decoded

    body = payload.get("body")
    if isinstance(body, str) and body.strip():
        return body.strip()
    return ""


def search_messages(query: str, account: str | None) -> list[dict[str, Any]]:
    result = run_command(
        ["gog", "gmail", "messages", "search", query, *build_account_args(account), "--json"],
        check=True,
    )
    payload = json.loads(result.stdout or "{}")
    messages = payload.get("messages") or []
    if not isinstance(messages, list):
        raise RuntimeError("Unexpected gog JSON shape: expected `messages` to be a list.")
    return messages


def dedupe_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for message in messages:
        message_id = str(message.get("id") or "").strip()
        if not message_id or message_id in seen_ids:
            continue
        seen_ids.add(message_id)
        deduped.append(message)
    return deduped


def extract_summarize_model(output: str) -> str | None:
    match = re.search(r"\bmodel:\s*([^\s,;]+)", output, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"\bvia model\s+([^\s,;]+)", output, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def summarize_text(file_path: Path, model: str | None, prompt: str) -> SummaryOutcome:
    env = os.environ.copy()
    args = [
        "summarize",
        str(file_path),
        "--length",
        "medium",
        "--plain",
        "--prompt",
        prompt,
    ]
    if model:
        args.extend(["--model", model])
    result = run_command(
        args,
        env=env,
        check=False,
    )
    detected_model = extract_summarize_model(result.stderr) or extract_summarize_model(result.stdout)
    if result.returncode != 0:
        details = sanitize_error_text(
            result.stderr or result.stdout,
            fallback=f"summarize exited {result.returncode}",
        )
        return SummaryOutcome(text="", error=details, model=detected_model)

    text = result.stdout.strip()
    if not text:
        details = sanitize_error_text(result.stderr, fallback="summarize returned no stdout")
        return SummaryOutcome(text="", error=details, model=detected_model)
    return SummaryOutcome(text=text, error=None, model=detected_model)


def extract_bullets(summary: str) -> list[str]:
    bullets: list[str] = []
    for line in summary.splitlines():
        text = line.strip()
        if not re.match(r"^[\*\-\u2022]\s+", text):
            continue
        text = re.sub(r"^[\*\-\u2022]\s+", "", text)
        text = re.sub(r"\*([^*]+)\*", r"\1", text).strip()
        if text:
            bullets.append(text)
    return bullets or [FAILURE_PLACEHOLDER]


def has_real_bullets(summary: dict[str, Any]) -> bool:
    bullets = summary.get("bullets") or []
    return any(bullet != FAILURE_PLACEHOLDER for bullet in bullets)


def build_failure_body(reason: str, settings_path: Path, query: str, details: list[str]) -> str:
    lines = [
        f"{SKILL_DISPLAY_NAME} hit a problem.",
        "",
        f"Reason: {reason}",
        f"Settings file: {settings_path.name}",
        f"Gmail query: {query}",
    ]
    if details:
        lines.extend(["", "Details:"])
        lines.extend(f"- {detail}" for detail in details)
    lines.extend(
        [
            "",
            "Recommended next steps:",
            "- Check the digest runtime logs",
            "- Verify the Gmail runtime is authenticated",
            "- Verify `summarize` is installed and configured",
            "- Verify the required summarization API key is available to the runtime",
        ]
    )
    return "\n".join(lines)


def build_recipient_batches(recipients: list[str], delivery_mode: str) -> list[list[str]]:
    if delivery_mode == "group":
        return [recipients]
    return [[recipient] for recipient in recipients]


def describe_delivery_mode(delivery_mode: str, recipient_count: int) -> str:
    if delivery_mode == "group" and recipient_count > 1:
        return "one group email"
    if delivery_mode == "group":
        return "one email"
    if recipient_count == 1:
        return "one email"
    return "individual emails"


def normalize_text(text: str) -> str:
    cleaned = (
        text.lower()
        .replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
    )
    cleaned = re.sub(r"[^a-z0-9\s]", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in normalize_text(text).split()
        if len(token) >= 3 and token not in STOPWORDS and not token.isdigit()
    }


def extract_numbers(text: str) -> set[str]:
    return set(re.findall(r"\b\d+(?:[.,]\d+)*%?\b", text.lower()))


def build_heuristic_common_groups(newsletters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for newsletter_index, newsletter in enumerate(newsletters):
        for bullet_index, bullet in enumerate(newsletter.get("bullets", [])):
            normalized = normalize_text(bullet)
            if not normalized:
                continue
            entries.append(
                {
                    "newsletter_index": newsletter_index,
                    "bullet_index": bullet_index,
                    "text": bullet,
                    "normalized": normalized,
                    "tokens": tokenize(bullet),
                    "numbers": extract_numbers(bullet),
                }
            )

    if len(entries) < 2:
        return []

    token_frequency: Counter[str] = Counter()
    for entry in entries:
        token_frequency.update(entry["tokens"])

    max_common_frequency = max(2, len(entries) // 3)
    for entry in entries:
        entry["informative_tokens"] = {
            token for token in entry["tokens"] if token_frequency[token] <= max_common_frequency
        }

    parent = list(range(len(entries)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    def is_shared_story(left: dict[str, Any], right: dict[str, Any]) -> bool:
        if left["newsletter_index"] == right["newsletter_index"]:
            return False

        left_tokens = left["informative_tokens"] or left["tokens"]
        right_tokens = right["informative_tokens"] or right["tokens"]
        if not left_tokens or not right_tokens:
            return False

        shared = left_tokens & right_tokens
        if len(shared) < 2:
            return False

        shared_numbers = left["numbers"] & right["numbers"]
        similarity = SequenceMatcher(None, left["normalized"], right["normalized"]).ratio()
        overlap = len(shared) / len(left_tokens | right_tokens)
        return (
            len(shared) >= 3
            or (len(shared) >= 2 and overlap >= 0.34 and similarity >= 0.58)
            or (len(shared) >= 2 and shared_numbers and similarity >= 0.58)
        )

    for left_index in range(len(entries)):
        for right_index in range(left_index + 1, len(entries)):
            if is_shared_story(entries[left_index], entries[right_index]):
                union(left_index, right_index)

    clusters: defaultdict[int, list[dict[str, Any]]] = defaultdict(list)
    for index, entry in enumerate(entries):
        clusters[find(index)].append(entry)

    common_groups: list[dict[str, Any]] = []
    for cluster_entries in clusters.values():
        newsletters_seen = {entry["newsletter_index"] for entry in cluster_entries}
        if len(newsletters_seen) < 2:
            continue

        matches: defaultdict[int, list[int]] = defaultdict(list)
        for entry in sorted(
            cluster_entries,
            key=lambda item: (item["newsletter_index"], item["bullet_index"]),
        ):
            matches[entry["newsletter_index"]].append(entry["bullet_index"])

        representative = min(
            (entry["text"].strip() for entry in cluster_entries if entry["text"].strip()),
            key=lambda text: (len(text), text),
        )
        common_groups.append(
            {
                "common": representative,
                "matches": [
                    {
                        "newsletter_index": newsletter_index,
                        "bullet_indexes": bullet_indexes,
                    }
                    for newsletter_index, bullet_indexes in sorted(matches.items())
                ],
            }
        )

    common_groups.sort(
        key=lambda group: (
            group["matches"][0]["newsletter_index"],
            group["matches"][0]["bullet_indexes"][0],
        )
    )
    return common_groups


def apply_common_groups(
    common_groups: list[dict[str, Any]],
    newsletters: list[dict[str, Any]],
) -> dict[str, Any]:
    removal_map: defaultdict[int, set[int]] = defaultdict(set)
    common_items: list[str] = []
    seen_common: set[str] = set()

    for group in common_groups:
        raw_matches = group.get("matches", [])
        valid_matches: list[tuple[int, list[int]]] = []
        matched_texts: list[str] = []

        for match in raw_matches:
            newsletter_index = match.get("newsletter_index")
            bullet_indexes = match.get("bullet_indexes", [])
            if not isinstance(newsletter_index, int) or not (
                0 <= newsletter_index < len(newsletters)
            ):
                continue

            valid_indexes: list[int] = []
            for bullet_index in bullet_indexes:
                if isinstance(bullet_index, int) and 0 <= bullet_index < len(
                    newsletters[newsletter_index].get("bullets", [])
                ):
                    valid_indexes.append(bullet_index)
                    matched_texts.append(newsletters[newsletter_index]["bullets"][bullet_index])

            if valid_indexes:
                valid_matches.append((newsletter_index, sorted(set(valid_indexes))))

        if len(valid_matches) < 2:
            continue

        common_text = str(group.get("common", "")).strip()
        if not common_text:
            common_text = min(
                (text.strip() for text in matched_texts if text.strip()),
                key=lambda text: (len(text), text),
            )

        normalized_common = normalize_text(common_text)
        if not normalized_common or normalized_common in seen_common:
            continue

        seen_common.add(normalized_common)
        common_items.append(common_text)
        for newsletter_index, bullet_indexes in valid_matches:
            removal_map[newsletter_index].update(bullet_indexes)

    cleaned_newsletters: list[dict[str, Any]] = []
    for newsletter_index, newsletter in enumerate(newsletters):
        cleaned = dict(newsletter)
        cleaned["bullets"] = [
            bullet
            for bullet_index, bullet in enumerate(newsletter.get("bullets", []))
            if bullet_index not in removal_map[newsletter_index]
        ]
        cleaned_newsletters.append(cleaned)

    return {"common": common_items, "newsletters": cleaned_newsletters}


def extract_from_addresses(summaries: list[dict[str, Any]]) -> list[str]:
    addresses: list[str] = []
    seen: set[str] = set()
    for summary in summaries:
        from_field = str(summary.get("from_field", "")).strip()
        if not from_field:
            continue
        match = re.search(r"<([^>]+)>", from_field)
        candidate = match.group(1).strip() if match else from_field
        if "@" not in candidate:
            continue
        lowered = candidate.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        addresses.append(candidate)
    return addresses


def build_footer_model_label(summaries: list[dict[str, Any]]) -> str:
    detected_models = sorted(
        {
            str(summary.get("model")).strip()
            for summary in summaries
            if str(summary.get("model") or "").strip()
        }
    )
    if len(detected_models) == 1:
        return f"{detected_models[0]} (reported by summarize)"
    if len(detected_models) > 1:
        return ", ".join(detected_models) + " (reported by summarize)"
    return "summarize configured/default model"


def build_digest_html(summaries: list[dict[str, Any]], today_human: str, model_label: str) -> str:
    deduped = {"common": [], "newsletters": summaries}
    if len(summaries) >= 2:
        heuristic_groups = build_heuristic_common_groups(summaries)
        deduped = apply_common_groups(heuristic_groups, summaries)

    from_addresses = extract_from_addresses(summaries)
    plural = "s" if len(summaries) != 1 else ""

    from_list_html = ""
    if from_addresses:
        from_list_html = (
            '<p style="color: #999; margin: 0 0 30px 0; font-size: 12px;">'
            f"Sources: {', '.join(escape(address) for address in from_addresses)}"
            "</p>"
        )

    def bullets_html(items: list[str]) -> str:
        rows = "".join(
            f'    <li style="margin-bottom: 13px; line-height: 1.65;">{escape(item)}</li>\n'
            for item in items
        )
        return '<ul style="margin: 10px 0 0 0; padding-left: 24px;">\n' + rows + "</ul>"

    parts = [
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<body style=\"font-family: Georgia, 'Times New Roman', serif; "
        "max-width: 900px; margin: 0 auto; padding: 28px 32px; color: #1a1a1a; "
        'font-size: 17px; line-height: 1.7;">\n\n'
        '<p style="font-size: 22px; font-weight: bold; margin: 0 0 4px 0;">'
        f"{SKILL_DISPLAY_NAME}"
        "</p>\n"
        '<p style="color: #777; margin: 0 0 6px 0; font-size: 14px;">'
        f"{escape(today_human)} &bull; {len(summaries)} newsletter{plural} summarized"
        "</p>\n"
        f"{from_list_html}\n"
    ]

    common = deduped.get("common", [])
    if common:
        parts.append(
            '<div style="background: #f5f5f5; border-left: 3px solid #888; '
            'padding: 14px 18px 14px 18px; margin-bottom: 32px; border-radius: 0 4px 4px 0;">\n'
            '<p style="font-size: 11px; font-weight: bold; text-transform: uppercase; '
            'letter-spacing: 0.9px; color: #666; margin: 0 0 10px 0;">'
            "Mentioned in multiple newsletters"
            "</p>\n"
        )
        parts.append(bullets_html(common))
        parts.append("\n</div>\n\n")

    for summary in deduped.get("newsletters", []):
        bullets = summary.get("bullets", [])
        if not bullets:
            continue
        subject = escape(str(summary.get("subject", "")))
        from_field = escape(str(summary.get("from_field", "")))
        date_text = escape(str(summary.get("date", "")))
        parts.append(
            '<div style="margin-bottom: 32px;">\n'
            '<div style="background: #eef2f8; border-radius: 6px; '
            'padding: 11px 16px 10px 16px; margin-bottom: 10px;">\n'
            f'<p style="margin: 0 0 3px 0; font-size: 17px; font-weight: bold;">{subject}</p>\n'
            f'<span style="color: #666; font-size: 13px;">{from_field} &bull; {date_text} ET</span>\n'
            "</div>\n"
        )
        parts.append(bullets_html(bullets))
        parts.append("\n</div>\n\n")

    parts.append(
        '<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 24px 0 14px 0;">\n'
        '<p style="color: #bbb; font-size: 11px; margin: 0;">'
        f"Summaries generated by summarize.sh &bull; model: {escape(model_label)}"
        "</p>\n"
        "</body>\n"
        "</html>\n"
    )

    return "".join(parts)


def fetch_message_body(message: dict[str, Any], account: str | None) -> str:
    message_id = str(message.get("id") or "")
    thread_id = str(message.get("threadId") or "")
    if not thread_id:
        return ""

    result = run_command(
        ["gog", "gmail", "thread", "get", thread_id, *build_account_args(account), "--full"],
        check=False,
    )
    body = result.stdout.strip() if result.returncode == 0 else ""
    if body and not looks_like_placeholder_body(body):
        return body

    try:
        fallback = fetch_best_message_body(message_id, account)
    except RuntimeError:
        fallback = ""
    return fallback or body


def summarize_messages(
    messages: list[dict[str, Any]],
    *,
    account: str | None,
    model: str | None,
    prompt: str,
    temp_dir: Path,
) -> tuple[list[dict[str, Any]], list[str]]:
    summaries: list[dict[str, Any]] = []
    failures: list[str] = []

    for index, message in enumerate(messages, start=1):
        message_id = str(message.get("id") or "")
        subject = str(message.get("subject") or "(no subject)")
        from_field = str(message.get("from") or "unknown")
        received_date = str(message.get("date") or "unknown")

        log(f"[{index}/{len(messages)}] Fetching: {subject}")
        body = fetch_message_body(message, account)
        if not body:
            body = "[Could not fetch content]"

        temp_file = temp_dir / f"newsletter-{message_id}.html"
        temp_file.write_text(body)

        log(f"[{index}/{len(messages)}] Summarizing...")
        outcome = summarize_text(temp_file, model, prompt)
        bullets = extract_bullets(outcome.text)
        error_message = outcome.error
        if bullets == [FAILURE_PLACEHOLDER]:
            error_message = error_message or "summarize did not return bullet-formatted output"
            failures.append(f"{subject}: {error_message}")
        summaries.append(
            {
                "id": message_id,
                "subject": subject,
                "from_field": from_field,
                "date": received_date,
                "bullets": bullets,
                "error": error_message,
                "model": outcome.model,
            }
        )
        log(f"[{index}/{len(messages)}] Done: {subject}")

    return summaries, failures


def send_digest(account: str | None, recipients: list[str], subject: str, html_body: str) -> None:
    run_command(
        [
            "gog",
            "gmail",
            "send",
            *build_account_args(account),
            "--to",
            ",".join(recipients),
            "--subject",
            subject,
            "--body-html",
            html_body,
        ],
        check=True,
    )


def send_plain_email(account: str | None, recipients: list[str], subject: str, body: str) -> None:
    run_command(
        [
            "gog",
            "gmail",
            "send",
            *build_account_args(account),
            "--to",
            ",".join(recipients),
            "--subject",
            subject,
            "--body-file",
            "-",
        ],
        check=True,
        input_text=body,
    )


def try_send_failure_email(
    account: str | None,
    recipients: list[str],
    delivery_mode: str,
    subject: str,
    body: str,
) -> None:
    for recipient_batch in build_recipient_batches(recipients, delivery_mode):
        try:
            send_plain_email(account, recipient_batch, subject, body)
            log(f"Failure notification sent to {', '.join(recipient_batch)}.")
        except Exception as exc:
            log(f"Could not send failure notification to {', '.join(recipient_batch)}: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and send an email newsletter digest using gog + summarize."
    )
    parser.add_argument(
        "--settings",
        default=str(DEFAULT_SETTINGS_PATH),
        help="Path to the skill settings JSON file.",
    )
    return parser.parse_args()


def main() -> int:
    ensure_runtime_path()
    args = parse_args()
    settings_path = Path(args.settings).expanduser().resolve()
    settings = load_settings(settings_path)
    account = os.environ.get("GOG_ACCOUNT", "").strip() or None
    query = build_gmail_query(settings.labels, settings.senders)
    failure_notified = False

    log(f"Using settings: {settings_path}")
    log(f"Query: {query}")
    print("Processing the email newsletter digest now.")

    messages = dedupe_messages(search_messages(query, account))
    if not messages:
        log("No newsletters found. Nothing to send.")
        print("No matching newsletter emails were found in the last 1 day.")
        return 0

    temp_dir = Path(tempfile.mkdtemp(prefix="email-newsletter-digest-"))
    log(f"Working directory: {temp_dir}")

    try:
        summaries, failures = summarize_messages(
            messages,
            account=account,
            model=None,
            prompt=DEFAULT_PROMPT,
            temp_dir=temp_dir,
        )

        real_summary_count = sum(1 for summary in summaries if has_real_bullets(summary))
        if real_summary_count == 0:
            reason = "All newsletter summaries failed."
            body = build_failure_body(reason, settings_path, query, failures)
            try_send_failure_email(
                account,
                settings.recipients,
                settings.recipient_delivery_mode,
                f"{SKILL_DISPLAY_NAME} Failure - {datetime.now().strftime('%Y-%m-%d')}",
                body,
            )
            failure_notified = True
            raise RuntimeError(reason)

        today_human = datetime.now().strftime("%A, %B %-d, %Y")
        model_label = build_footer_model_label(summaries)
        html_body = build_digest_html(summaries, today_human, model_label)
        output_html_path = temp_dir / "email-newsletter-digest.html"
        output_html_path.write_text(html_body)
        log(f"Digest HTML written to: {output_html_path}")

        subject = f"{SKILL_DISPLAY_NAME} - {today_human}"
        for recipient_batch in build_recipient_batches(
            settings.recipients, settings.recipient_delivery_mode
        ):
            send_digest(account, recipient_batch, subject, html_body)
            log(
                "Digest sent to "
                f"{', '.join(recipient_batch)} ({len(summaries)} newsletter(s))."
            )
        if failures:
            warning_body = build_failure_body(
                "The digest was sent, but one or more newsletters could not be summarized cleanly.",
                settings_path,
                query,
                failures,
            )
            try_send_failure_email(
                account,
                settings.recipients,
                settings.recipient_delivery_mode,
                f"{SKILL_DISPLAY_NAME} Warning - {datetime.now().strftime('%Y-%m-%d')}",
                warning_body,
            )
        log(
            "Digest sent to "
            f"{', '.join(settings.recipients)} ({len(summaries)} newsletter(s))."
        )
        print(
            f"Sent the email newsletter digest to {', '.join(settings.recipients)} "
            f"with {len(summaries)} newsletter(s) as "
            f"{describe_delivery_mode(settings.recipient_delivery_mode, len(settings.recipients))}."
        )
        return 0
    except Exception as exc:
        if not failure_notified:
            body = build_failure_body(str(exc), settings_path, query, [])
            try_send_failure_email(
                account,
                settings.recipients,
                settings.recipient_delivery_mode,
                f"{SKILL_DISPLAY_NAME} Failure - {datetime.now().strftime('%Y-%m-%d')}",
                body,
            )
        print(f"Email newsletter digest failed: {exc}", file=sys.stderr)
        raise
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
