"""Analysis engine for Communication DNA.

All functions operate on segments already in the DB.
Each takes a speaker_id (or None for all) and returns structured results.
"""

import json
import math
import re
from collections import Counter, defaultdict

from db import get_conn
from wordlists import (
    STOP_WORDS, FILLER_WORDS, HEDGING_PHRASES, ASSERTIVE_PHRASES,
    COMMITMENT_PATTERNS, DECISION_PATTERNS, FORMAL_WORDS, INFORMAL_WORDS,
    POSITIVE_WORDS, NEGATIVE_WORDS,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_segments(conn, speaker_id=None, transcription_id=None):
    """Fetch segments, optionally filtered."""
    sql = "SELECT * FROM segments WHERE 1=1"
    params = []
    if speaker_id is not None:
        sql += " AND speaker_id = ?"
        params.append(speaker_id)
    if transcription_id is not None:
        sql += " AND transcription_id = ?"
        params.append(transcription_id)
    sql += " ORDER BY transcription_id, sequence_order"
    return conn.execute(sql, params).fetchall()


def _tokenize(text):
    """Lowercase word tokenization."""
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def _sentences(text):
    """Split text into sentences."""
    return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

CACHE_SCHEMA = """
CREATE TABLE IF NOT EXISTS analysis_cache (
    id INTEGER PRIMARY KEY,
    speaker_id INTEGER,
    transcription_id INTEGER,
    analysis_type TEXT,
    data TEXT,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def ensure_cache_table(conn):
    conn.executescript(CACHE_SCHEMA)


def _get_cached(conn, analysis_type, speaker_id=None, transcription_id=None):
    """Return cached JSON or None."""
    ensure_cache_table(conn)
    sql = "SELECT data, computed_at FROM analysis_cache WHERE analysis_type = ?"
    params = [analysis_type]
    if speaker_id is not None:
        sql += " AND speaker_id = ?"
        params.append(speaker_id)
    else:
        sql += " AND speaker_id IS NULL"
    if transcription_id is not None:
        sql += " AND transcription_id = ?"
        params.append(transcription_id)
    else:
        sql += " AND transcription_id IS NULL"
    sql += " ORDER BY computed_at DESC LIMIT 1"
    row = conn.execute(sql, params).fetchone()
    if not row:
        return None
    # Check staleness: any segments newer than cache?
    last = conn.execute(
        "SELECT MAX(rowid) as m FROM segments"
    ).fetchone()["m"] or 0
    # Simple staleness: re-compute if segments table has grown
    # Store max_seg_rowid in the JSON itself
    data = json.loads(row["data"])
    if data.get("_max_seg_rowid", 0) < last:
        return None
    return data


def _set_cache(conn, analysis_type, data, speaker_id=None, transcription_id=None):
    ensure_cache_table(conn)
    last = conn.execute("SELECT MAX(rowid) as m FROM segments").fetchone()["m"] or 0
    data["_max_seg_rowid"] = last
    # Delete old
    sql = "DELETE FROM analysis_cache WHERE analysis_type = ?"
    params = [analysis_type]
    if speaker_id is not None:
        sql += " AND speaker_id = ?"
        params.append(speaker_id)
    else:
        sql += " AND speaker_id IS NULL"
    if transcription_id is not None:
        sql += " AND transcription_id = ?"
        params.append(transcription_id)
    else:
        sql += " AND transcription_id IS NULL"
    conn.execute(sql, params)
    conn.execute(
        "INSERT INTO analysis_cache (speaker_id, transcription_id, analysis_type, data) VALUES (?,?,?,?)",
        (speaker_id, transcription_id, analysis_type, json.dumps(data)),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# 1. Vocabulary Fingerprint
# ---------------------------------------------------------------------------

def vocabulary_fingerprint(conn, speaker_id=None, top_n=30):
    """Compute vocabulary fingerprint for a speaker (or all)."""
    cached = _get_cached(conn, "fingerprint", speaker_id=speaker_id)
    if cached:
        return cached

    segments = _get_segments(conn, speaker_id=speaker_id)
    if not segments:
        return {"error": "No segments found"}

    all_words = []
    sentence_count = 0
    for seg in segments:
        words = _tokenize(seg["text"])
        all_words.extend(words)
        sentence_count += max(len(_sentences(seg["text"])), 1)

    total = len(all_words)
    if total == 0:
        return {"error": "No words found"}

    freq = Counter(all_words)
    filtered_freq = Counter({w: c for w, c in freq.items() if w not in STOP_WORDS and len(w) > 1})
    unique_types = len(freq)
    ttr = unique_types / total if total else 0

    # Formality
    formal_count = sum(1 for w in all_words if w in FORMAL_WORDS)
    informal_count = sum(1 for w in all_words if w in INFORMAL_WORDS)
    formality = formal_count / max(formal_count + informal_count, 1)

    # Unique words compared to other speakers
    unique_to_speaker = []
    if speaker_id is not None:
        other_words = set()
        others = _get_segments(conn)
        for seg in others:
            if seg["speaker_id"] != speaker_id:
                other_words.update(_tokenize(seg["text"]))
        unique_to_speaker = [w for w, c in filtered_freq.most_common(200)
                            if w not in other_words and c >= 2][:20]

    result = {
        "total_words": total,
        "unique_words": unique_types,
        "type_token_ratio": round(ttr, 4),
        "avg_sentence_length": round(total / max(sentence_count, 1), 1),
        "formality_score": round(formality, 3),
        "formal_count": formal_count,
        "informal_count": informal_count,
        "top_words": filtered_freq.most_common(top_n),
        "unique_to_speaker": unique_to_speaker,
    }
    _set_cache(conn, "fingerprint", result, speaker_id=speaker_id)
    return result


# ---------------------------------------------------------------------------
# 2. Filler Word Detection
# ---------------------------------------------------------------------------

def filler_analysis(conn, speaker_id=None):
    """Analyze filler word usage."""
    cached = _get_cached(conn, "fillers", speaker_id=speaker_id)
    if cached:
        return cached

    segments = _get_segments(conn, speaker_id=speaker_id)
    if not segments:
        return {"error": "No segments found"}

    total_words = 0
    filler_counts = Counter()

    for seg in segments:
        text = seg["text"].lower()
        total_words += seg["word_count"] or len(text.split())
        for filler in FILLER_WORDS:
            # Count occurrences as phrase
            count = len(re.findall(r'\b' + re.escape(filler) + r'\b', text))
            filler_counts[filler] += count

    total_fillers = sum(filler_counts.values())
    rate = (total_fillers / total_words * 100) if total_words else 0

    result = {
        "total_words": total_words,
        "total_fillers": total_fillers,
        "filler_rate_per_100": round(rate, 2),
        "distribution": filler_counts.most_common(),
    }
    _set_cache(conn, "fillers", result, speaker_id=speaker_id)
    return result


# ---------------------------------------------------------------------------
# 3. Speech Patterns
# ---------------------------------------------------------------------------

def speech_patterns(conn, speaker_id=None, top_n=20):
    """Analyze speech patterns: phrases, questions, hedging, assertiveness."""
    cached = _get_cached(conn, "patterns", speaker_id=speaker_id)
    if cached:
        return cached

    segments = _get_segments(conn, speaker_id=speaker_id)
    if not segments:
        return {"error": "No segments found"}

    bigrams = Counter()
    trigrams = Counter()
    question_count = 0
    statement_count = 0
    hedge_count = 0
    assert_count = 0
    total_words = 0

    for seg in segments:
        text = seg["text"]
        words = _tokenize(text)
        total_words += len(words)

        # Bigrams/trigrams (skip stop-word-only combos)
        for i in range(len(words) - 1):
            bg = f"{words[i]} {words[i+1]}"
            if not all(w in STOP_WORDS for w in (words[i], words[i+1])):
                bigrams[bg] += 1
        for i in range(len(words) - 2):
            tg = f"{words[i]} {words[i+1]} {words[i+2]}"
            if not all(w in STOP_WORDS for w in (words[i], words[i+1], words[i+2])):
                trigrams[tg] += 1

        # Questions vs statements
        sents = _sentences(text)
        for s in sents:
            if text.strip().endswith("?") or s.strip().endswith("?"):
                question_count += 1
            else:
                statement_count += 1

        # Hedging & assertiveness
        lower = text.lower()
        for phrase in HEDGING_PHRASES:
            hedge_count += len(re.findall(r'\b' + re.escape(phrase) + r'\b', lower))
        for phrase in ASSERTIVE_PHRASES:
            assert_count += len(re.findall(r'\b' + re.escape(phrase) + r'\b', lower))

    total_sents = question_count + statement_count
    result = {
        "top_bigrams": [(bg, c) for bg, c in bigrams.most_common(top_n) if c >= 2],
        "top_trigrams": [(tg, c) for tg, c in trigrams.most_common(top_n) if c >= 2],
        "question_count": question_count,
        "statement_count": statement_count,
        "question_rate": round(question_count / max(total_sents, 1) * 100, 1),
        "hedge_count": hedge_count,
        "assert_count": assert_count,
        "hedging_rate_per_100": round(hedge_count / max(total_words, 1) * 100, 2),
        "assertiveness_rate_per_100": round(assert_count / max(total_words, 1) * 100, 2),
    }
    _set_cache(conn, "patterns", result, speaker_id=speaker_id)
    return result


# ---------------------------------------------------------------------------
# 4. Commitment / Question / Decision Extraction
# ---------------------------------------------------------------------------

def extract_commitments(conn, speaker_id=None):
    """Extract commitments, questions, and decisions from segments."""
    segments = _get_segments(conn, speaker_id=speaker_id)
    results = {"commitments": [], "questions": [], "decisions": []}

    for seg in segments:
        text = seg["text"]
        lower = text.lower()
        sid = seg["speaker_id"]
        tid = seg["transcription_id"]
        seg_id = seg["id"]

        # Commitments
        for pat in COMMITMENT_PATTERNS:
            if pat in lower:
                results["commitments"].append({
                    "segment_id": seg_id, "speaker_id": sid,
                    "transcription_id": tid, "text": text,
                })
                # Store in extractions table
                conn.execute(
                    "INSERT OR IGNORE INTO extractions (segment_id, transcription_id, speaker_id, type, content) VALUES (?,?,?,?,?)",
                    (seg_id, tid, sid, "commitment", text),
                )
                break

        # Questions
        if "?" in text:
            results["questions"].append({
                "segment_id": seg_id, "speaker_id": sid,
                "transcription_id": tid, "text": text,
            })
            conn.execute(
                "INSERT OR IGNORE INTO extractions (segment_id, transcription_id, speaker_id, type, content) VALUES (?,?,?,?,?)",
                (seg_id, tid, sid, "question", text),
            )

        # Decisions
        for pat in DECISION_PATTERNS:
            if pat in lower:
                results["decisions"].append({
                    "segment_id": seg_id, "speaker_id": sid,
                    "transcription_id": tid, "text": text,
                })
                conn.execute(
                    "INSERT OR IGNORE INTO extractions (segment_id, transcription_id, speaker_id, type, content) VALUES (?,?,?,?,?)",
                    (seg_id, tid, sid, "decision", text),
                )
                break

    conn.commit()
    return results


# ---------------------------------------------------------------------------
# 5. Sentiment Analysis
# ---------------------------------------------------------------------------

def _score_sentiment(text):
    """Score text from -1 to +1 using word lists."""
    words = _tokenize(text)
    if not words:
        return 0.0
    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    total = pos + neg
    if total == 0:
        return 0.0
    return round((pos - neg) / total, 3)


def sentiment_analysis(conn, transcription_id=None, speaker_id=None):
    """Compute sentiment per segment and arc."""
    segments = _get_segments(conn, speaker_id=speaker_id, transcription_id=transcription_id)
    if not segments:
        return {"error": "No segments found"}

    arc = []
    by_speaker = defaultdict(list)

    for seg in segments:
        score = _score_sentiment(seg["text"])
        arc.append({
            "segment_id": seg["id"],
            "sequence": seg["sequence_order"],
            "speaker_id": seg["speaker_id"],
            "score": score,
            "text_preview": seg["text"][:80],
        })
        by_speaker[seg["speaker_id"]].append(score)

    speaker_avg = {}
    for sid, scores in by_speaker.items():
        speaker_avg[str(sid)] = round(sum(scores) / len(scores), 3) if scores else 0

    overall = [a["score"] for a in arc]
    result = {
        "arc": arc,
        "speaker_averages": speaker_avg,
        "overall_average": round(sum(overall) / max(len(overall), 1), 3),
        "segment_count": len(arc),
    }
    if transcription_id:
        _set_cache(conn, "sentiment", result, transcription_id=transcription_id)
    return result


# ---------------------------------------------------------------------------
# 6. Topic Detection (TF-IDF-like)
# ---------------------------------------------------------------------------

def topic_detection(conn, speaker_id=None, top_n=15):
    """Extract top topics using TF-IDF-like scoring."""
    cached = _get_cached(conn, "topics", speaker_id=speaker_id)
    if cached:
        return cached

    segments = _get_segments(conn, speaker_id=speaker_id)
    all_segments = _get_segments(conn)  # all for IDF

    if not segments:
        return {"error": "No segments found"}

    # Group by transcription for IDF
    docs = defaultdict(Counter)
    for seg in all_segments:
        words = [w for w in _tokenize(seg["text"]) if w not in STOP_WORDS and len(w) > 2]
        docs[seg["transcription_id"]].update(words)

    num_docs = max(len(docs), 1)
    # Document frequency
    df = Counter()
    for doc_words in docs.values():
        for w in doc_words:
            df[w] += 1

    # TF for target speaker/segments
    tf = Counter()
    for seg in segments:
        words = [w for w in _tokenize(seg["text"]) if w not in STOP_WORDS and len(w) > 2]
        tf.update(words)

    # TF-IDF scores
    tfidf = {}
    for word, freq in tf.items():
        idf = math.log(num_docs / max(df.get(word, 1), 1)) + 1
        tfidf[word] = round(freq * idf, 3)

    top_topics = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Per-transcription topics
    per_transcription = {}
    target_tids = set(seg["transcription_id"] for seg in segments)
    for tid in target_tids:
        t_tf = Counter()
        for seg in segments:
            if seg["transcription_id"] == tid:
                words = [w for w in _tokenize(seg["text"]) if w not in STOP_WORDS and len(w) > 2]
                t_tf.update(words)
        t_scores = {}
        for word, freq in t_tf.items():
            idf = math.log(num_docs / max(df.get(word, 1), 1)) + 1
            t_scores[word] = round(freq * idf, 3)
        per_transcription[str(tid)] = sorted(t_scores.items(), key=lambda x: x[1], reverse=True)[:10]

    # Store top topics as extractions
    for word, score in top_topics[:5]:
        conn.execute(
            "INSERT INTO extractions (transcription_id, speaker_id, type, content, confidence) VALUES (?,?,?,?,?)",
            (None, speaker_id, "topic", word, min(score / 10, 1.0)),
        )
    conn.commit()

    result = {
        "top_topics": top_topics,
        "per_transcription": per_transcription,
    }
    _set_cache(conn, "topics", result, speaker_id=speaker_id)
    return result


# ---------------------------------------------------------------------------
# Full Analysis Report
# ---------------------------------------------------------------------------

def full_analysis(conn, speaker_id=None):
    """Run all analyses and return combined results."""
    return {
        "fingerprint": vocabulary_fingerprint(conn, speaker_id),
        "fillers": filler_analysis(conn, speaker_id),
        "patterns": speech_patterns(conn, speaker_id),
        "commitments": extract_commitments(conn, speaker_id),
        "sentiment": sentiment_analysis(conn, speaker_id=speaker_id),
        "topics": topic_detection(conn, speaker_id),
    }


def compare_speakers(conn, speaker_id1, speaker_id2):
    """Side-by-side comparison of two speakers."""
    s1 = conn.execute("SELECT name FROM speakers WHERE id = ?", (speaker_id1,)).fetchone()
    s2 = conn.execute("SELECT name FROM speakers WHERE id = ?", (speaker_id2,)).fetchone()
    name1 = s1["name"] if s1 else f"Speaker {speaker_id1}"
    name2 = s2["name"] if s2 else f"Speaker {speaker_id2}"

    fp1 = vocabulary_fingerprint(conn, speaker_id1)
    fp2 = vocabulary_fingerprint(conn, speaker_id2)
    fl1 = filler_analysis(conn, speaker_id1)
    fl2 = filler_analysis(conn, speaker_id2)
    pa1 = speech_patterns(conn, speaker_id1)
    pa2 = speech_patterns(conn, speaker_id2)
    se1 = sentiment_analysis(conn, speaker_id=speaker_id1)
    se2 = sentiment_analysis(conn, speaker_id=speaker_id2)

    return {
        "speakers": [name1, name2],
        "fingerprint": [fp1, fp2],
        "fillers": [fl1, fl2],
        "patterns": [pa1, pa2],
        "sentiment": [se1, se2],
    }
