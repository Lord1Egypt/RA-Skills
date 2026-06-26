"""Ingestion pipeline for transcription files (TXT, SRT, VTT, JSON)."""

import json
import os
import re
from difflib import SequenceMatcher

from db import get_conn

# Speaker label patterns
SPEAKER_PATTERNS = [
    re.compile(r'^\[([^\]]+)\]\s*:?\s*(.*)'),        # [John]: text or [John] text
    re.compile(r'^([A-Za-z][A-Za-z0-9 _.\'()-]{0,30}):\s+(.+)'),  # John: text
]

SRT_TIME_RE = re.compile(
    r'(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})'
)


def _parse_timestamp(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def _detect_speaker(line):
    """Try to extract (speaker_name, text) from a line. Returns (None, line) if no speaker."""
    for pat in SPEAKER_PATTERNS:
        m = pat.match(line.strip())
        if m:
            name = m.group(1).strip()
            text = m.group(2).strip()
            # Filter out false positives (common non-speaker prefixes)
            if name.lower() in ('http', 'https', 'note', 'edit', 'file', 'the', 'this', 'that'):
                continue
            return name, text
    return None, line.strip()


def _find_or_create_speaker(conn, name):
    """Find existing speaker by name (fuzzy) or create new one."""
    name_clean = name.strip()
    if not name_clean:
        name_clean = "Unknown Speaker"

    # Exact match first
    row = conn.execute("SELECT id FROM speakers WHERE LOWER(name) = LOWER(?)", (name_clean,)).fetchone()
    if row:
        return row["id"]

    # Check aliases
    for r in conn.execute("SELECT id, aliases FROM speakers WHERE aliases IS NOT NULL").fetchall():
        try:
            aliases = json.loads(r["aliases"])
            for a in aliases:
                if a.lower() == name_clean.lower():
                    return r["id"]
        except (json.JSONDecodeError, TypeError):
            pass

    # Fuzzy match on existing names
    for r in conn.execute("SELECT id, name FROM speakers").fetchall():
        if SequenceMatcher(None, r["name"].lower(), name_clean.lower()).ratio() > 0.85:
            return r["id"]

    # Create new
    cur = conn.execute("INSERT INTO speakers (name) VALUES (?)", (name_clean,))
    return cur.lastrowid


def parse_txt(text):
    """Parse plain text, detecting speaker labels. Returns list of (speaker, text, start, end)."""
    segments = []
    current_speaker = None
    current_lines = []

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        speaker, content = _detect_speaker(line)
        if speaker and speaker != current_speaker:
            if current_lines:
                segments.append((current_speaker, ' '.join(current_lines), None, None))
            current_speaker = speaker
            current_lines = [content] if content else []
        else:
            if speaker and speaker == current_speaker:
                if content:
                    current_lines.append(content)
            else:
                current_lines.append(line)

    if current_lines:
        segments.append((current_speaker, ' '.join(current_lines), None, None))

    return segments


def parse_srt(text):
    """Parse SRT subtitle format. Returns list of (speaker, text, start, end)."""
    segments = []
    blocks = re.split(r'\n\s*\n', text.strip())
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue
        # Find timestamp line
        time_match = None
        text_lines = []
        for i, line in enumerate(lines):
            m = SRT_TIME_RE.search(line)
            if m:
                time_match = m
                text_lines = lines[i + 1:]
                break
        if not time_match or not text_lines:
            continue
        start = _parse_timestamp(*time_match.groups()[:4])
        end = _parse_timestamp(*time_match.groups()[4:])
        content = ' '.join(l.strip() for l in text_lines if l.strip())
        # Strip HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        speaker, content = _detect_speaker(content)
        segments.append((speaker, content, start, end))
    return segments


def parse_vtt(text):
    """Parse WebVTT format. Returns list of (speaker, text, start, end)."""
    # Strip WEBVTT header and metadata
    text = re.sub(r'^WEBVTT.*?\n\n', '', text, flags=re.DOTALL)
    # Remove style/note blocks
    text = re.sub(r'STYLE\n.*?\n\n', '', text, flags=re.DOTALL)
    text = re.sub(r'NOTE\n.*?\n\n', '', text, flags=re.DOTALL)
    return parse_srt(text)  # SRT and VTT share similar structure after header


def parse_json(text):
    """Parse JSON transcription (Whisper / Otter.ai style). Returns list of (speaker, text, start, end)."""
    data = json.loads(text)
    segments = []

    # Whisper-style: {"segments": [{"start": 0.0, "end": 2.5, "text": "..."}]}
    if isinstance(data, dict) and "segments" in data:
        for seg in data["segments"]:
            speaker = seg.get("speaker") or seg.get("speaker_id") or seg.get("speaker_name")
            segments.append((
                str(speaker) if speaker else None,
                seg.get("text", "").strip(),
                seg.get("start"),
                seg.get("end"),
            ))
        return segments

    # Otter.ai style: {"results": [{"speaker": "...", "start_time": ..., "transcript": "..."}]}
    if isinstance(data, dict) and "results" in data:
        for r in data["results"]:
            segments.append((
                r.get("speaker"),
                r.get("transcript", r.get("text", "")).strip(),
                r.get("start_time", r.get("start")),
                r.get("end_time", r.get("end")),
            ))
        return segments

    # Array of segments
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                segments.append((
                    item.get("speaker"),
                    item.get("text", item.get("transcript", "")).strip(),
                    item.get("start", item.get("start_time")),
                    item.get("end", item.get("end_time")),
                ))
        return segments

    return segments


PARSERS = {
    '.txt': parse_txt,
    '.srt': parse_srt,
    '.vtt': parse_vtt,
    '.json': parse_json,
}

SUPPORTED_EXTENSIONS = set(PARSERS.keys())


ALLOWED_EXTENSIONS = {'.txt', '.srt', '.vtt', '.json'}

def ingest_file(filepath, title=None, date=None, context=None, conn=None):
    """Ingest a transcription file into the database.

    Returns the transcription_id on success.
    """
    filepath = os.path.abspath(filepath)
    ext = os.path.splitext(filepath)[1].lower()

    # Validate file extension
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}. Supported: {', '.join(sorted(ALLOWED_EXTENSIONS))}")

    if ext not in PARSERS:
        raise ValueError(f"Unsupported file type: {ext}. Supported: {', '.join(sorted(PARSERS))}")

    with open(filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    parser = PARSERS[ext]
    if ext == '.json':
        raw_segments = parser(raw_text)
    else:
        raw_segments = parser(raw_text)

    own_conn = conn is None
    if own_conn:
        conn = get_conn()

    try:
        # Compute total word count and raw text for storage
        all_text = ' '.join(seg[1] for seg in raw_segments if seg[1])
        total_words = len(all_text.split())

        # Insert transcription
        cur = conn.execute(
            """INSERT INTO transcriptions (title, source_file, source_type, date, context, raw_text, word_count)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (title or os.path.basename(filepath), filepath, ext.lstrip('.'), date, context, raw_text, total_words)
        )
        tid = cur.lastrowid

        # Track speakers for this transcription
        speaker_ids_seen = set()

        for seq, (speaker_name, text, start, end) in enumerate(raw_segments):
            if not text:
                continue
            sid = _find_or_create_speaker(conn, speaker_name or "Unknown Speaker")

            if sid not in speaker_ids_seen:
                conn.execute(
                    "INSERT OR IGNORE INTO transcription_speakers (transcription_id, speaker_id) VALUES (?, ?)",
                    (tid, sid)
                )
                speaker_ids_seen.add(sid)

            wc = len(text.split())
            conn.execute(
                """INSERT INTO segments (transcription_id, speaker_id, start_time, end_time, text, word_count, sequence_order)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (tid, sid, start, end, text, wc, seq)
            )

        conn.commit()
        return tid
    except Exception:
        conn.rollback()
        raise
    finally:
        if own_conn:
            conn.close()
