#!/usr/bin/env python3
"""Communication DNA — Flask Web UI."""

import json
import os
import tempfile

from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

from db import get_conn
from ingest import ingest_file
from analyze import (
    vocabulary_fingerprint, filler_analysis, speech_patterns,
    extract_commitments, sentiment_analysis, topic_detection,
)
from profiles import get_speaker_profile, compare_speakers
from integrations import (
    auto_link_crm, auto_link_kb, get_crm_info, get_kb_links,
    cross_search, integration_stats, init_links, push_to_kb,
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

TAG_COLORS = {
    "Formal": "bg-blue-600", "Casual": "bg-orange-500",
    "Assertive": "bg-red-500", "Cautious": "bg-yellow-500",
    "Inquisitive": "bg-purple-500", "Filler-heavy": "bg-pink-500",
    "Articulate": "bg-green-500", "Optimistic": "bg-emerald-500",
    "Critical": "bg-rose-600", "Diverse vocabulary": "bg-cyan-500",
    "Repetitive": "bg-gray-500",
}

SPEAKER_COLORS = [
    "#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6",
    "#ec4899", "#06b6d4", "#f97316", "#6366f1", "#14b8a6",
]


def sentiment_emoji(score):
    if score is None:
        return "😐"
    if score > 0.3:
        return "😊"
    if score > 0.1:
        return "🙂"
    if score > -0.1:
        return "😐"
    if score > -0.3:
        return "😕"
    return "😟"


app.jinja_env.globals.update(
    tag_colors=TAG_COLORS,
    speaker_colors=SPEAKER_COLORS,
    sentiment_emoji=sentiment_emoji,
)


# ── Dashboard ─────────────────────────────────────────────────
@app.route("/")
def dashboard():
    conn = get_conn()
    stats = {
        "transcriptions": conn.execute("SELECT COUNT(*) as c FROM transcriptions").fetchone()["c"],
        "speakers": conn.execute("SELECT COUNT(*) as c FROM speakers").fetchone()["c"],
        "segments": conn.execute("SELECT COUNT(*) as c FROM segments").fetchone()["c"],
        "total_words": conn.execute("SELECT COALESCE(SUM(word_count),0) as c FROM transcriptions").fetchone()["c"],
    }
    recent = conn.execute("SELECT * FROM transcriptions ORDER BY id DESC LIMIT 10").fetchall()
    top_speakers = conn.execute("""
        SELECT s.id, s.name, COALESCE(SUM(seg.word_count),0) as total_words, COUNT(DISTINCT seg.transcription_id) as t_count
        FROM speakers s LEFT JOIN segments seg ON s.id = seg.speaker_id
        GROUP BY s.id ORDER BY total_words DESC LIMIT 10
    """).fetchall()
    int_stats = integration_stats(conn)
    conn.close()
    return render_template("dashboard.html", stats=stats, recent=recent, top_speakers=top_speakers, int_stats=int_stats)


# ── Speakers ──────────────────────────────────────────────────
@app.route("/speakers")
def speakers_list():
    conn = get_conn()
    rows = conn.execute("""
        SELECT s.id, s.name, COUNT(DISTINCT ts.transcription_id) as t_count,
               COALESCE(SUM(seg.word_count),0) as total_words
        FROM speakers s
        LEFT JOIN transcription_speakers ts ON s.id = ts.speaker_id
        LEFT JOIN segments seg ON s.id = seg.speaker_id
        GROUP BY s.id ORDER BY total_words DESC
    """).fetchall()

    speakers = []
    for r in rows:
        fl = filler_analysis(conn, r["id"])
        pa = speech_patterns(conn, r["id"])
        fp = vocabulary_fingerprint(conn, r["id"])
        se = sentiment_analysis(conn, speaker_id=r["id"])
        sa = 0
        if "error" not in se:
            sa = se.get("speaker_averages", {}).get(str(r["id"]), se.get("overall_average", 0))
        from profiles import get_style_tags
        tags = get_style_tags(fp, fl, pa, sa)
        speakers.append({
            "id": r["id"], "name": r["name"], "t_count": r["t_count"],
            "total_words": r["total_words"], "tags": tags, "sentiment_avg": sa,
        })
    conn.close()
    return render_template("speakers.html", speakers=speakers)


# ── Speaker Profile ───────────────────────────────────────────
@app.route("/speaker/<int:sid>")
def speaker_profile(sid):
    conn = get_conn()
    profile = get_speaker_profile(sid, conn)
    if "error" in profile:
        conn.close()
        return render_template("error.html", message=profile["error"]), 404
    crm_info = get_crm_info(sid, conn)
    kb_links = get_kb_links(sid, conn)
    conn.close()
    return render_template("speaker.html", p=profile, crm_info=crm_info, kb_links=kb_links)


# ── Transcriptions ────────────────────────────────────────────
@app.route("/transcriptions")
def transcriptions_list():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM transcriptions ORDER BY id DESC").fetchall()
    trans = []
    for r in rows:
        spks = conn.execute("""
            SELECT s.name FROM speakers s JOIN transcription_speakers ts ON s.id = ts.speaker_id
            WHERE ts.transcription_id = ?
        """, (r["id"],)).fetchall()
        se = sentiment_analysis(conn, transcription_id=r["id"])
        avg = se.get("overall_average", 0) if "error" not in se else 0
        trans.append({**dict(r), "speakers": [s["name"] for s in spks], "sentiment_avg": avg})
    conn.close()
    return render_template("transcriptions.html", transcriptions=trans)


# ── Transcription Detail ─────────────────────────────────────
@app.route("/transcription/<int:tid>")
def transcription_detail(tid):
    conn = get_conn()
    t = conn.execute("SELECT * FROM transcriptions WHERE id = ?", (tid,)).fetchone()
    if not t:
        conn.close()
        return render_template("error.html", message="Transcription not found"), 404

    spks = conn.execute("""
        SELECT s.id, s.name FROM speakers s JOIN transcription_speakers ts ON s.id = ts.speaker_id
        WHERE ts.transcription_id = ?
    """, (tid,)).fetchall()

    segments = conn.execute("""
        SELECT seg.*, sp.name as speaker_name FROM segments seg
        LEFT JOIN speakers sp ON seg.speaker_id = sp.id
        WHERE seg.transcription_id = ? ORDER BY seg.sequence_order
    """, (tid,)).fetchall()

    se = sentiment_analysis(conn, transcription_id=tid)
    arc = se.get("arc", []) if "error" not in se else []

    # Extractions
    commitments = conn.execute(
        "SELECT e.*, sp.name as speaker_name FROM extractions e LEFT JOIN speakers sp ON e.speaker_id = sp.id WHERE e.transcription_id = ? AND e.type = 'commitment'", (tid,)
    ).fetchall()
    decisions = conn.execute(
        "SELECT e.*, sp.name as speaker_name FROM extractions e LEFT JOIN speakers sp ON e.speaker_id = sp.id WHERE e.transcription_id = ? AND e.type = 'decision'", (tid,)
    ).fetchall()
    questions = conn.execute(
        "SELECT e.*, sp.name as speaker_name FROM extractions e LEFT JOIN speakers sp ON e.speaker_id = sp.id WHERE e.transcription_id = ? AND e.type = 'question'", (tid,)
    ).fetchall()

    # Build speaker color map
    speaker_map = {s["id"]: i % len(SPEAKER_COLORS) for i, s in enumerate(spks)}

    conn.close()
    return render_template("transcription.html", t=dict(t), speakers=spks,
                           segments=segments, arc=arc, commitments=commitments,
                           decisions=decisions, questions=questions,
                           speaker_map=speaker_map)


# ── Compare ───────────────────────────────────────────────────
@app.route("/compare")
def compare_page():
    conn = get_conn()
    all_speakers = conn.execute("SELECT id, name FROM speakers ORDER BY name").fetchall()
    s1 = request.args.get("s1", type=int)
    s2 = request.args.get("s2", type=int)
    comparison = None
    if s1 and s2:
        comparison = compare_speakers(s1, s2, conn)
    conn.close()
    return render_template("compare.html", speakers=all_speakers, comparison=comparison, s1=s1, s2=s2)


# ── Search ────────────────────────────────────────────────────
@app.route("/search")
def search_page():
    conn = get_conn()
    q = request.args.get("q", "").strip()
    speaker_filter = request.args.get("speaker", type=int)
    all_speakers = conn.execute("SELECT id, name FROM speakers ORDER BY name").fetchall()
    results = []

    if q:
        try:
            sql = """
                SELECT s.id, s.transcription_id, s.speaker_id, s.text, s.start_time,
                       sp.name as speaker_name, t.title, t.date
                FROM segments_fts fts
                JOIN segments s ON fts.rowid = s.id
                LEFT JOIN speakers sp ON s.speaker_id = sp.id
                LEFT JOIN transcriptions t ON s.transcription_id = t.id
                WHERE segments_fts MATCH ?
            """
            params = [q]
            if speaker_filter:
                sql += " AND s.speaker_id = ?"
                params.append(speaker_filter)
            sql += " ORDER BY rank LIMIT 50"
            results = conn.execute(sql, params).fetchall()
        except Exception:
            results = []

    conn.close()
    return render_template("search.html", q=q, results=results,
                           speakers=all_speakers, speaker_filter=speaker_filter)


# ── Ingest ────────────────────────────────────────────────────
@app.route("/ingest", methods=["GET", "POST"])
def ingest_page():
    if request.method == "GET":
        return render_template("ingest.html", result=None)

    files = request.files.getlist("files")
    title = request.form.get("title", "").strip()
    date = request.form.get("date", "").strip()
    context = request.form.get("context", "").strip()

    results = []
    conn = get_conn()
    for f in files:
        if not f.filename:
            continue
        safe_name = secure_filename(f.filename)
        if not safe_name:
            continue
        path = os.path.join(UPLOAD_DIR, safe_name)
        f.save(path)
        try:
            tid = ingest_file(path, title=title or f.filename, date=date or None, context=context or None, conn=conn)
            t = conn.execute("SELECT * FROM transcriptions WHERE id = ?", (tid,)).fetchone()
            segs = conn.execute("SELECT COUNT(*) as c FROM segments WHERE transcription_id = ?", (tid,)).fetchone()["c"]
            spks = conn.execute("""
                SELECT s.name FROM speakers s JOIN transcription_speakers ts ON s.id = ts.speaker_id
                WHERE ts.transcription_id = ?
            """, (tid,)).fetchall()
            results.append({
                "filename": f.filename, "tid": tid, "success": True,
                "words": t["word_count"], "segments": segs,
                "speakers": [s["name"] for s in spks],
            })
        except Exception as e:
            results.append({"filename": f.filename, "success": False, "error": str(e)})
    conn.close()
    return render_template("ingest.html", result=results)


# ── API Endpoints ─────────────────────────────────────────────
@app.route("/api/speakers")
def api_speakers():
    conn = get_conn()
    rows = conn.execute("""
        SELECT s.id, s.name, COUNT(DISTINCT ts.transcription_id) as t_count,
               COALESCE(SUM(seg.word_count),0) as total_words
        FROM speakers s LEFT JOIN transcription_speakers ts ON s.id = ts.speaker_id
        LEFT JOIN segments seg ON s.id = seg.speaker_id
        GROUP BY s.id ORDER BY s.name
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/speaker/<int:sid>")
def api_speaker(sid):
    conn = get_conn()
    profile = get_speaker_profile(sid, conn)
    conn.close()
    return jsonify(profile)


@app.route("/api/search")
def api_search():
    conn = get_conn()
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    try:
        rows = conn.execute("""
            SELECT s.id, s.transcription_id, s.speaker_id, s.text,
                   sp.name as speaker_name, t.title, t.date
            FROM segments_fts fts JOIN segments s ON fts.rowid = s.id
            LEFT JOIN speakers sp ON s.speaker_id = sp.id
            LEFT JOIN transcriptions t ON s.transcription_id = t.id
            WHERE segments_fts MATCH ? ORDER BY rank LIMIT 50
        """, (q,)).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception:
        conn.close()
        return jsonify([])


@app.route("/api/ingest", methods=["POST"])
def api_ingest():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "No file"}), 400
    safe_name = secure_filename(f.filename)
    if not safe_name:
        return jsonify({"error": "Invalid filename"}), 400
    path = os.path.join(UPLOAD_DIR, safe_name)
    f.save(path)
    conn = get_conn()
    try:
        tid = ingest_file(path, title=request.form.get("title", safe_name),
                          date=request.form.get("date"),
                          context=request.form.get("context"), conn=conn)
        conn.close()
        return jsonify({"transcription_id": tid})
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400


# ── Integrations ──────────────────────────────────────────────
@app.route("/integrations")
def integrations_page():
    conn = get_conn()
    stats = integration_stats(conn)
    conn.close()
    return render_template("integrations.html", stats=stats)


@app.route("/api/link-crm", methods=["POST"])
def api_link_crm():
    matches = auto_link_crm()
    return jsonify({"matches": matches, "count": len(matches)})


@app.route("/api/link-kb", methods=["POST"])
def api_link_kb():
    matches = auto_link_kb()
    return jsonify({"matches": matches, "count": len(matches)})


@app.route("/api/cross-search")
def api_cross_search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    return jsonify(cross_search(q))


@app.route("/api/push-to-kb/<int:tid>", methods=["POST"])
def api_push_to_kb(tid):
    result = push_to_kb(tid)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5053, debug=False)
