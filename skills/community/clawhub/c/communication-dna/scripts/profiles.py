"""Speaker profile generator and comparison engine for Communication DNA."""

from db import get_conn
from analyze import (
    vocabulary_fingerprint, filler_analysis, speech_patterns,
    extract_commitments, sentiment_analysis, topic_detection,
)


def get_style_tags(fingerprint, fillers, patterns, sentiment_avg):
    """Generate style tags based on analysis scores."""
    tags = []

    if "error" not in fingerprint:
        formality = fingerprint.get("formality_score", 0.5)
        if formality > 0.6:
            tags.append("Formal")
        elif formality < 0.3:
            tags.append("Casual")

        ttr = fingerprint.get("type_token_ratio", 0.5)
        if ttr > 0.7:
            tags.append("Diverse vocabulary")
        elif ttr < 0.3:
            tags.append("Repetitive")

    if "error" not in fillers:
        rate = fillers.get("filler_rate_per_100", 0)
        if rate > 8:
            tags.append("Filler-heavy")
        elif rate < 2:
            tags.append("Articulate")

    if "error" not in patterns:
        q_rate = patterns.get("question_rate", 0)
        if q_rate > 15:
            tags.append("Inquisitive")

        hedge = patterns.get("hedge_count", 0)
        assertive = patterns.get("assert_count", 0)
        if assertive > hedge:
            tags.append("Assertive")
        elif hedge > assertive:
            tags.append("Cautious")

    if sentiment_avg is not None:
        if sentiment_avg > 0.3:
            tags.append("Optimistic")
        elif sentiment_avg < -0.1:
            tags.append("Critical")

    return tags


def get_speaker_profile(speaker_id, conn=None):
    """Returns a complete speaker profile."""
    own_conn = conn is None
    if own_conn:
        conn = get_conn()

    try:
        speaker = conn.execute("SELECT * FROM speakers WHERE id = ?", (speaker_id,)).fetchone()
        if not speaker:
            return {"error": "Speaker not found"}

        # Basic info
        trans = conn.execute("""
            SELECT t.id, t.title, t.date, t.word_count, t.context
            FROM transcriptions t JOIN transcription_speakers ts ON t.id = ts.transcription_id
            WHERE ts.speaker_id = ? ORDER BY t.date DESC
        """, (speaker_id,)).fetchall()

        total_words = conn.execute(
            "SELECT COALESCE(SUM(word_count), 0) as tw FROM segments WHERE speaker_id = ?",
            (speaker_id,)
        ).fetchone()["tw"]

        seg_count = conn.execute(
            "SELECT COUNT(*) as c FROM segments WHERE speaker_id = ?", (speaker_id,)
        ).fetchone()["c"]

        dates = conn.execute(
            "SELECT MIN(t.date) as first, MAX(t.date) as last FROM transcriptions t JOIN transcription_speakers ts ON t.id = ts.transcription_id WHERE ts.speaker_id = ?",
            (speaker_id,)
        ).fetchone()

        # Analyses
        fp = vocabulary_fingerprint(conn, speaker_id)
        fl = filler_analysis(conn, speaker_id)
        pa = speech_patterns(conn, speaker_id)
        se = sentiment_analysis(conn, speaker_id=speaker_id)
        tp = topic_detection(conn, speaker_id)
        cm = extract_commitments(conn, speaker_id)

        # Sentiment avg
        sentiment_avg = None
        if "error" not in se:
            sa = se.get("speaker_averages", {})
            sentiment_avg = sa.get(str(speaker_id), se.get("overall_average", 0))

        tags = get_style_tags(fp, fl, pa, sentiment_avg)

        # Top words (excluding stop words) - already in fingerprint
        top_words = fp.get("top_words", [])[:10] if "error" not in fp else []

        # Top phrases
        top_phrases = []
        if "error" not in pa:
            top_phrases = (pa.get("top_bigrams", [])[:3] + pa.get("top_trigrams", [])[:2])[:5]

        # Top fillers
        top_fillers = fl.get("distribution", [])[:3] if "error" not in fl else []

        # Commitments (last 10)
        recent_commitments = []
        for c in cm.get("commitments", [])[-10:]:
            t_row = conn.execute("SELECT title FROM transcriptions WHERE id = ?", (c["transcription_id"],)).fetchone()
            recent_commitments.append({
                "text": c["text"],
                "transcription_id": c["transcription_id"],
                "transcription_title": t_row["title"] if t_row else "Unknown",
            })

        # Speaking time estimate
        total_time = conn.execute(
            "SELECT SUM(end_time - start_time) as t FROM segments WHERE speaker_id = ? AND start_time IS NOT NULL AND end_time IS NOT NULL",
            (speaker_id,)
        ).fetchone()["t"]
        wpm = None
        if total_time and total_time > 0:
            wpm = round(total_words / (total_time / 60))

        return {
            "id": speaker_id,
            "name": speaker["name"],
            "aliases": speaker["aliases"],
            "total_transcriptions": len(trans),
            "total_words": total_words,
            "total_segments": seg_count,
            "first_seen": dates["first"],
            "last_seen": dates["last"],
            "transcriptions": [dict(t) for t in trans],
            "style_tags": tags,
            "fingerprint": fp,
            "fillers": fl,
            "patterns": pa,
            "sentiment": se,
            "sentiment_avg": sentiment_avg,
            "topics": tp,
            "top_words": top_words,
            "top_phrases": top_phrases,
            "top_fillers": top_fillers,
            "commitments": recent_commitments,
            "all_commitments": cm,
            "total_time_seconds": total_time,
            "wpm": wpm,
            "richness": fp.get("type_token_ratio", 0) if "error" not in fp else 0,
            "formality": fp.get("formality_score", 0) if "error" not in fp else 0,
            "avg_sentence_length": fp.get("avg_sentence_length", 0) if "error" not in fp else 0,
            "filler_rate": fl.get("filler_rate_per_100", 0) if "error" not in fl else 0,
            "question_rate": pa.get("question_rate", 0) if "error" not in pa else 0,
        }
    finally:
        if own_conn:
            conn.close()


def compare_speakers(id1, id2, conn=None):
    """Side-by-side comparison of two speakers with similarity score."""
    own_conn = conn is None
    if own_conn:
        conn = get_conn()

    try:
        p1 = get_speaker_profile(id1, conn)
        p2 = get_speaker_profile(id2, conn)

        if "error" in p1 or "error" in p2:
            return {"error": "One or both speakers not found"}

        # Build metrics comparison
        metrics = []

        def add_metric(name, v1, v2, higher_better=True, fmt=".2f"):
            winner = None
            if v1 != v2:
                winner = 1 if (v1 > v2) == higher_better else 2
            metrics.append({
                "name": name, "v1": v1, "v2": v2,
                "winner": winner, "fmt": fmt,
            })

        add_metric("Total Words", p1["total_words"], p2["total_words"], True, ",d")
        add_metric("Vocabulary Richness", p1["richness"], p2["richness"], True)
        add_metric("Formality", p1["formality"], p2["formality"], None)
        add_metric("Avg Sentence Length", p1["avg_sentence_length"], p2["avg_sentence_length"], None, ".1f")
        add_metric("Filler Rate /100w", p1["filler_rate"], p2["filler_rate"], False)
        add_metric("Question Rate %", p1["question_rate"], p2["question_rate"], None, ".1f")

        fp1 = p1.get("fingerprint", {})
        fp2 = p2.get("fingerprint", {})
        pa1 = p1.get("patterns", {})
        pa2 = p2.get("patterns", {})

        add_metric("Hedging /100w",
                    pa1.get("hedging_rate_per_100", 0),
                    pa2.get("hedging_rate_per_100", 0), False)
        add_metric("Assertiveness /100w",
                    pa1.get("assertiveness_rate_per_100", 0),
                    pa2.get("assertiveness_rate_per_100", 0), True)

        s1 = p1.get("sentiment_avg") or 0
        s2 = p2.get("sentiment_avg") or 0
        add_metric("Sentiment Avg", s1, s2, None, ".3f")

        # Similarity score (0-100)
        diffs = []
        pairs = [
            (p1["richness"], p2["richness"], 1.0),
            (p1["formality"], p2["formality"], 1.0),
            (p1["filler_rate"], p2["filler_rate"], 20.0),
            (p1["question_rate"], p2["question_rate"], 100.0),
            (s1, s2, 2.0),
        ]
        for v1, v2, max_range in pairs:
            diff = abs(v1 - v2) / max(max_range, 0.001)
            diffs.append(min(diff, 1.0))

        similarity = round((1 - (sum(diffs) / len(diffs))) * 100, 1) if diffs else 50.0

        # Key differences
        key_diffs = []
        for m in metrics:
            if m["winner"] and m["v1"] != 0 and m["v2"] != 0:
                ratio = max(m["v1"], m["v2"]) / max(min(m["v1"], m["v2"]), 0.001)
                if ratio > 1.5:
                    who = p1["name"] if m["winner"] == 1 else p2["name"]
                    key_diffs.append(f"{who} has significantly higher {m['name']}")

        return {
            "speaker1": p1,
            "speaker2": p2,
            "metrics": metrics,
            "similarity": similarity,
            "key_differences": key_diffs[:5],
        }
    finally:
        if own_conn:
            conn.close()
