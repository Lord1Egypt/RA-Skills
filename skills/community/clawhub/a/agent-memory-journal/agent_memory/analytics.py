from __future__ import annotations

import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

from .normalize import tokenize
from .storage import init_memory_root


def _iter_files(paths, days: int, after_date=None, before_date=None):
    discovered = []
    for p in paths.episodic_dir.glob("*.md"):
        try:
            d = datetime.strptime(p.stem, "%Y-%m-%d").date()
            discovered.append((d, p))
        except ValueError:
            continue
    if not discovered:
        return []
    latest_file_date = max(d for d, _p in discovered)
    anchor_date = min(datetime.now().date(), latest_file_date) if not before_date else before_date
    rolling_cutoff = anchor_date - timedelta(days=max(0, days))
    min_date = max(rolling_cutoff, after_date) if after_date else rolling_cutoff
    max_date = before_date
    candidates = []
    for d, p in discovered:
        if d < min_date:
            continue
        if max_date and d > max_date:
            continue
        candidates.append(p)
    return sorted(candidates, reverse=True)


def _note_words(paths, days: int, after_date=None, before_date=None):
    files = _iter_files(paths, days, after_date=after_date, before_date=before_date)
    words = []
    notes = []
    stop = {
        "the", "and", "for", "with", "that", "this", "from", "have", "was", "were", "are", "but", "not", "into", "out", "new", "added", "gained", "now", "also", "recent", "notes",
        "että", "joka", "tämä", "tuo", "ovat", "oli", "kun", "tai", "jos", "nyt", "sekä", "vielä", "kanssa", "uusi", "lisätty"
    }
    line_re = re.compile(r"^-\s+(\d{2}:\d{2})\s+(.*)$")
    for p in files:
        try:
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for ln in lines:
            m = line_re.match(ln.strip())
            if not m:
                continue
            note = m.group(2).split(" [", 1)[0].strip()
            notes.append(note)
            words.extend(w.lower() for w in re.findall(r"[A-Za-zÅÄÖåäö0-9-]{3,}", note) if w.lower() not in stop)
    return notes, words


def memory_stats(root: str | Path, days: int = 7, top: int = 10):
    paths = init_memory_root(root)
    files = _iter_files(paths, days)
    note_count = 0
    hourly = Counter()
    daily_counts = Counter()
    notes, words = _note_words(paths, days)
    line_re = re.compile(r"^-\s+(\d{2}:\d{2})\s+(.*)$")
    for p in files:
        try:
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for ln in lines:
            m = line_re.match(ln.strip())
            if not m:
                continue
            hhmm = m.group(1)
            hour = hhmm.split(":")[0]
            note_count += 1
            hourly[hour] += 1
            daily_counts[p.stem] += 1
    return {
        "days_scanned": days,
        "files_found": len(files),
        "days_with_notes": len(daily_counts),
        "note_count": note_count,
        "busiest_hours": [{"hour": h, "count": c} for h, c in hourly.most_common(3)],
        "top_words": [{"word": w, "count": c} for w, c in Counter(words).most_common(top)],
    }


def memory_topics(root: str | Path, days: int = 14, top: int = 8, samples: int = 2, min_count: int = 2, after_date=None, before_date=None):
    paths = init_memory_root(root)
    notes, words = _note_words(paths, days, after_date=after_date, before_date=before_date)
    counts = Counter(words)
    word_samples = {}
    for note in notes:
        tokens = set(tokenize(note))
        for word, count in counts.items():
            if count < min_count:
                continue
            if word in tokens:
                word_samples.setdefault(word, [])
                if len(word_samples[word]) < samples and note not in word_samples[word]:
                    word_samples[word].append(note)
    topics = []
    for word, count in counts.most_common():
        if count < min_count:
            continue
        topics.append({"word": word, "count": count, "samples": word_samples.get(word, [])})
        if len(topics) >= max(1, top):
            break
    return {"days_scanned": days, "note_count": len(notes), "topics": topics}


def memory_cadence(root: str | Path, days: int = 14, top_hours: int = 3, after_date=None, before_date=None):
    paths = init_memory_root(root)
    files = _iter_files(paths, days, after_date=after_date, before_date=before_date)
    per_day = []
    hourly = Counter()
    line_re = re.compile(r"^-\s+(\d{2}:\d{2})\s+(.*)$")
    for p in files:
        count = 0
        try:
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for ln in lines:
            m = line_re.match(ln.strip())
            if not m:
                continue
            count += 1
            hourly[m.group(1).split(":")[0]] += 1
        per_day.append({"date": p.stem, "count": count})
    return {"days_scanned": days, "per_day": per_day, "busiest_hours": [{"hour": h, "count": c} for h, c in hourly.most_common(top_hours)]}


def memory_digest(root: str | Path, days: int = 7, recent_limit: int = 5, top: int = 5, after_date=None, before_date=None):
    paths = init_memory_root(root)
    stats = memory_stats(paths.root, days=max(1, days), top=max(1, top))
    cadence = memory_cadence(paths.root, days=max(1, days), top_hours=max(1, min(top, 3)), after_date=after_date, before_date=before_date)
    topics = memory_topics(paths.root, days=max(1, days), top=max(1, top), samples=1, min_count=2, after_date=after_date, before_date=before_date)
    from .episodic_recall import recall_recent
    recent = recall_recent(paths.root, days=max(1, days), k=recent_limit)
    return {"days_scanned": days, "stats": stats, "cadence": cadence, "topics": topics, "recent": [r.__dict__ for r in recent]}


def extract_candidates(text: str, triggers: list[str] | None = None) -> list[str]:
    from .promote import DEFAULT_TRIGGERS
    trig = triggers or DEFAULT_TRIGGERS
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    out = []
    for ln in lines:
        if any(re.search(t, ln.lower()) for t in trig):
            out.append(ln)
    return out
