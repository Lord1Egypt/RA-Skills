#!/usr/bin/env python3
"""Communication DNA — CLI for transcription analysis."""

import argparse
import os
import sys

from db import get_conn
from ingest import ingest_file, SUPPORTED_EXTENSIONS
from analyze import (
    vocabulary_fingerprint, filler_analysis, speech_patterns,
    extract_commitments, sentiment_analysis, topic_detection,
    full_analysis, compare_speakers,
)
from integrations import auto_link_crm, auto_link_kb, push_to_kb, cross_search


def cmd_ingest(args):
    """Ingest a single transcription file."""
    if not os.path.isfile(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    conn = get_conn()
    try:
        tid = ingest_file(args.file, title=args.title, date=args.date, context=args.context, conn=conn)
        r = conn.execute("SELECT * FROM transcriptions WHERE id = ?", (tid,)).fetchone()
        segs = conn.execute("SELECT COUNT(*) as c FROM segments WHERE transcription_id = ?", (tid,)).fetchone()
        spks = conn.execute(
            "SELECT s.name FROM speakers s JOIN transcription_speakers ts ON s.id = ts.speaker_id WHERE ts.transcription_id = ?",
            (tid,)
        ).fetchall()
        print(f"✓ Ingested: {r['title']}")
        print(f"  ID: {tid} | Type: {r['source_type']} | Words: {r['word_count']} | Segments: {segs['c']}")
        print(f"  Speakers: {', '.join(s['name'] for s in spks)}")
    finally:
        conn.close()


def cmd_ingest_dir(args):
    """Batch ingest all supported files in a directory."""
    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found: {args.directory}")
        sys.exit(1)
    conn = get_conn()
    count = 0
    try:
        for fname in sorted(os.listdir(args.directory)):
            ext = os.path.splitext(fname)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                path = os.path.join(args.directory, fname)
                try:
                    tid = ingest_file(path, context=args.context, conn=conn)
                    print(f"  ✓ {fname} (id={tid})")
                    count += 1
                except Exception as e:
                    print(f"  ✗ {fname}: {e}")
    finally:
        conn.close()
    print(f"\nIngested {count} file(s).")


def cmd_speakers(args):
    """List all speakers."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT s.id, s.name, COUNT(ts.transcription_id) as t_count
        FROM speakers s
        LEFT JOIN transcription_speakers ts ON s.id = ts.speaker_id
        GROUP BY s.id ORDER BY s.name
    """).fetchall()
    conn.close()
    if not rows:
        print("No speakers found.")
        return
    print(f"{'ID':<5} {'Name':<30} {'Transcriptions':<5}")
    print("-" * 50)
    for r in rows:
        print(f"{r['id']:<5} {r['name']:<30} {r['t_count']:<5}")


def cmd_speaker(args):
    """Show speaker details."""
    conn = get_conn()
    s = conn.execute("SELECT * FROM speakers WHERE id = ?", (args.id,)).fetchone()
    if not s:
        print(f"Speaker {args.id} not found.")
        conn.close()
        return
    print(f"Speaker: {s['name']} (id={s['id']})")
    if s['aliases']:
        print(f"Aliases: {s['aliases']}")
    if s['notes']:
        print(f"Notes: {s['notes']}")

    ts = conn.execute("""
        SELECT t.id, t.title, t.date, t.word_count
        FROM transcriptions t JOIN transcription_speakers ts ON t.id = ts.transcription_id
        WHERE ts.speaker_id = ? ORDER BY t.date
    """, (args.id,)).fetchall()
    conn.close()
    if ts:
        print(f"\nTranscriptions ({len(ts)}):")
        for t in ts:
            print(f"  [{t['id']}] {t['title']}  {t['date'] or ''} ({t['word_count']} words)")


def cmd_transcriptions(args):
    """List all transcriptions."""
    conn = get_conn()
    rows = conn.execute("SELECT id, title, source_type, date, context, word_count FROM transcriptions ORDER BY id").fetchall()
    conn.close()
    if not rows:
        print("No transcriptions found.")
        return
    print(f"{'ID':<5} {'Title':<35} {'Type':<5} {'Date':<12} {'Context':<12} {'Words':<8}")
    print("-" * 80)
    for r in rows:
        print(f"{r['id']:<5} {(r['title'] or '')[:34]:<35} {r['source_type'] or '':<5} {r['date'] or '':<12} {r['context'] or '':<12} {r['word_count'] or 0:<8}")


def cmd_transcription(args):
    """Show transcription details."""
    conn = get_conn()
    t = conn.execute("SELECT * FROM transcriptions WHERE id = ?", (args.id,)).fetchone()
    if not t:
        print(f"Transcription {args.id} not found.")
        conn.close()
        return
    print(f"Transcription: {t['title']} (id={t['id']})")
    print(f"  Source: {t['source_file']}")
    print(f"  Type: {t['source_type']} | Date: {t['date'] or 'N/A'} | Context: {t['context'] or 'N/A'}")
    print(f"  Words: {t['word_count']} | Duration: {t['duration_seconds'] or 'N/A'}s")

    spks = conn.execute("""
        SELECT s.id, s.name, ts.role FROM speakers s
        JOIN transcription_speakers ts ON s.id = ts.speaker_id
        WHERE ts.transcription_id = ?
    """, (args.id,)).fetchall()
    if spks:
        print(f"\n  Speakers:")
        for s in spks:
            role = f" ({s['role']})" if s['role'] else ""
            print(f"    - {s['name']}{role}")

    seg_count = conn.execute("SELECT COUNT(*) as c FROM segments WHERE transcription_id = ?", (args.id,)).fetchone()
    print(f"\n  Segments: {seg_count['c']}")
    conn.close()


def cmd_search(args):
    """FTS5 search across segments."""
    conn = get_conn()
    query = args.query
    rows = conn.execute("""
        SELECT s.id, s.transcription_id, s.speaker_id, s.text, s.start_time, s.end_time,
               sp.name as speaker_name, t.title
        FROM segments_fts fts
        JOIN segments s ON fts.rowid = s.id
        LEFT JOIN speakers sp ON s.speaker_id = sp.id
        LEFT JOIN transcriptions t ON s.transcription_id = t.id
        WHERE segments_fts MATCH ?
        ORDER BY rank LIMIT ?
    """, (query, args.limit)).fetchall()
    conn.close()
    if not rows:
        print(f"No results for: {query}")
        return
    print(f"Found {len(rows)} result(s) for '{query}':\n")
    for r in rows:
        time_str = ""
        if r['start_time'] is not None:
            time_str = f" [{r['start_time']:.1f}s]"
        print(f"  [{r['transcription_id']}] {r['title']} — {r['speaker_name'] or 'Unknown'}{time_str}")
        print(f"    {r['text'][:200]}")
        print()


def cmd_stats(args):
    """Show overall statistics."""
    conn = get_conn()
    t = conn.execute("SELECT COUNT(*) as c FROM transcriptions").fetchone()['c']
    s = conn.execute("SELECT COUNT(*) as c FROM speakers").fetchone()['c']
    sg = conn.execute("SELECT COUNT(*) as c FROM segments").fetchone()['c']
    w = conn.execute("SELECT COALESCE(SUM(word_count), 0) as c FROM transcriptions").fetchone()['c']
    conn.close()
    print("Communication DNA — Stats")
    print(f"  Transcriptions: {t}")
    print(f"  Speakers:       {s}")
    print(f"  Segments:       {sg}")
    print(f"  Total words:    {w:,}")


def _print_fingerprint(fp, label=""):
    if "error" in fp:
        print(f"  {fp['error']}")
        return
    if label:
        print(f"\n{'='*60}\n  {label}\n{'='*60}")
    print(f"  Total words:         {fp['total_words']:,}")
    print(f"  Unique words:        {fp['unique_words']:,}")
    print(f"  Type-token ratio:    {fp['type_token_ratio']}")
    print(f"  Avg sentence length: {fp['avg_sentence_length']} words")
    print(f"  Formality score:     {fp['formality_score']} (formal:{fp['formal_count']} informal:{fp['informal_count']})")
    print(f"  Top words: {', '.join(f'{w}({c})' for w,c in fp['top_words'][:15])}")
    if fp.get('unique_to_speaker'):
        print(f"  Unique to speaker:   {', '.join(fp['unique_to_speaker'][:10])}")


def _print_fillers(fl, label=""):
    if "error" in fl:
        print(f"  {fl['error']}")
        return
    if label:
        print(f"\n--- Filler Words ({label}) ---")
    print(f"  Filler rate: {fl['filler_rate_per_100']:.2f} per 100 words ({fl['total_fillers']} / {fl['total_words']})")
    if fl['distribution']:
        print(f"  Distribution: {', '.join(f'{w}({c})' for w,c in fl['distribution'] if c > 0)}")


def _print_patterns(pa, label=""):
    if "error" in pa:
        print(f"  {pa['error']}")
        return
    if label:
        print(f"\n--- Speech Patterns ({label}) ---")
    print(f"  Questions: {pa['question_count']} ({pa['question_rate']}%) | Statements: {pa['statement_count']}")
    print(f"  Hedging rate:       {pa['hedging_rate_per_100']:.2f}/100w ({pa['hedge_count']} total)")
    print(f"  Assertiveness rate: {pa['assertiveness_rate_per_100']:.2f}/100w ({pa['assert_count']} total)")
    if pa['top_bigrams']:
        print(f"  Top phrases: {', '.join(f'{p}({c})' for p,c in pa['top_bigrams'][:8])}")


def _speaker_name(conn, sid):
    r = conn.execute("SELECT name FROM speakers WHERE id = ?", (sid,)).fetchone()
    return r["name"] if r else f"Speaker {sid}"


def cmd_analyze(args):
    """Run full analysis on a speaker."""
    conn = get_conn()
    name = _speaker_name(conn, args.id)
    print(f"Full Analysis: {name} (id={args.id})")
    result = full_analysis(conn, args.id)
    _print_fingerprint(result["fingerprint"], f"Vocabulary — {name}")
    _print_fillers(result["fillers"], name)
    _print_patterns(result["patterns"], name)

    cm = result["commitments"]
    print(f"\n--- Extractions ---")
    print(f"  Commitments: {len(cm['commitments'])} | Questions: {len(cm['questions'])} | Decisions: {len(cm['decisions'])}")
    for c in cm["commitments"][:5]:
        print(f"    → {c['text'][:100]}")

    se = result["sentiment"]
    if "error" not in se:
        avg = se.get("speaker_averages", {}).get(str(args.id), se.get("overall_average", 0))
        print(f"\n--- Sentiment ---")
        print(f"  Average: {avg}")

    tp = result["topics"]
    if "error" not in tp and tp.get("top_topics"):
        print(f"\n--- Topics ---")
        print(f"  {', '.join(f'{w}({s})' for w,s in tp['top_topics'][:10])}")
    conn.close()


def cmd_analyze_all(args):
    """Run analysis on all speakers."""
    conn = get_conn()
    speakers = conn.execute("SELECT id, name FROM speakers ORDER BY name").fetchall()
    if not speakers:
        print("No speakers found.")
        conn.close()
        return
    for s in speakers:
        print(f"\n{'#'*60}")
        print(f"# {s['name']} (id={s['id']})")
        print(f"{'#'*60}")
        result = full_analysis(conn, s["id"])
        _print_fingerprint(result["fingerprint"])
        _print_fillers(result["fillers"])
        _print_patterns(result["patterns"])
        cm = result["commitments"]
        print(f"  Commitments: {len(cm['commitments'])} | Questions: {len(cm['questions'])} | Decisions: {len(cm['decisions'])}")
        se = result["sentiment"]
        if "error" not in se:
            print(f"  Sentiment avg: {se.get('overall_average', 0)}")
        tp = result["topics"]
        if "error" not in tp and tp.get("top_topics"):
            print(f"  Topics: {', '.join(w for w,_ in tp['top_topics'][:8])}")
    conn.close()


def cmd_fingerprint(args):
    conn = get_conn()
    name = _speaker_name(conn, args.id)
    fp = vocabulary_fingerprint(conn, args.id)
    _print_fingerprint(fp, f"Vocabulary Fingerprint — {name}")
    conn.close()


def cmd_fillers(args):
    conn = get_conn()
    name = _speaker_name(conn, args.id)
    fl = filler_analysis(conn, args.id)
    _print_fillers(fl, name)
    conn.close()


def cmd_patterns(args):
    conn = get_conn()
    name = _speaker_name(conn, args.id)
    pa = speech_patterns(conn, args.id)
    _print_patterns(pa, name)
    conn.close()


def cmd_commitments(args):
    conn = get_conn()
    cm = extract_commitments(conn, speaker_id=args.id)
    for kind in ("commitments", "questions", "decisions"):
        items = cm[kind]
        print(f"\n{kind.upper()} ({len(items)}):")
        for item in items[:20]:
            spk = _speaker_name(conn, item["speaker_id"]) if item["speaker_id"] else "?"
            print(f"  [{spk}] {item['text'][:120]}")
    conn.close()


def cmd_sentiment(args):
    conn = get_conn()
    t = conn.execute("SELECT title FROM transcriptions WHERE id = ?", (args.id,)).fetchone()
    if not t:
        print(f"Transcription {args.id} not found.")
        conn.close()
        return
    print(f"Sentiment Arc: {t['title']} (id={args.id})")
    se = sentiment_analysis(conn, transcription_id=args.id)
    if "error" in se:
        print(f"  {se['error']}")
    else:
        print(f"  Overall average: {se['overall_average']}")
        print(f"  Speaker averages: {se['speaker_averages']}")
        print(f"\n  {'Seq':<5} {'Score':>6}  {'Speaker':>10}  Text")
        print(f"  {'-'*60}")
        for a in se["arc"]:
            bar = "+" * max(int(a["score"] * 5), 0) + "-" * max(int(-a["score"] * 5), 0)
            print(f"  {a['sequence'] or 0:<5} {a['score']:>6.3f}  {str(a['speaker_id'] or '?'):>10}  {bar} {a['text_preview'][:50]}")
    conn.close()


def cmd_topics(args):
    conn = get_conn()
    tp = topic_detection(conn, speaker_id=args.id)
    if "error" in tp:
        print(tp["error"])
    else:
        label = _speaker_name(conn, args.id) if args.id else "All Speakers"
        print(f"Topics — {label}")
        for word, score in tp["top_topics"]:
            bar = "█" * max(int(score), 1)
            print(f"  {word:<20} {score:>8.2f}  {bar}")
    conn.close()


def cmd_compare(args):
    conn = get_conn()
    result = compare_speakers(conn, args.id1, args.id2)
    n1, n2 = result["speakers"]
    fp1, fp2 = result["fingerprint"]
    fl1, fl2 = result["fillers"]
    pa1, pa2 = result["patterns"]
    se1, se2 = result["sentiment"]

    print(f"{'COMPARISON':^60}")
    print(f"{'':>25} {n1:>15}  {n2:>15}")
    print(f"  {'-'*55}")

    if "error" not in fp1 and "error" not in fp2:
        print(f"  {'Total words':<23} {fp1['total_words']:>15,}  {fp2['total_words']:>15,}")
        print(f"  {'Unique words':<23} {fp1['unique_words']:>15,}  {fp2['unique_words']:>15,}")
        print(f"  {'Type-token ratio':<23} {fp1['type_token_ratio']:>15}  {fp2['type_token_ratio']:>15}")
        print(f"  {'Avg sentence len':<23} {fp1['avg_sentence_length']:>15}  {fp2['avg_sentence_length']:>15}")
        print(f"  {'Formality':<23} {fp1['formality_score']:>15}  {fp2['formality_score']:>15}")

    if "error" not in fl1 and "error" not in fl2:
        print(f"  {'Filler rate/100w':<23} {fl1['filler_rate_per_100']:>15.2f}  {fl2['filler_rate_per_100']:>15.2f}")

    if "error" not in pa1 and "error" not in pa2:
        print(f"  {'Question rate %':<23} {pa1['question_rate']:>15}  {pa2['question_rate']:>15}")
        print(f"  {'Hedging/100w':<23} {pa1['hedging_rate_per_100']:>15.2f}  {pa2['hedging_rate_per_100']:>15.2f}")
        print(f"  {'Assertive/100w':<23} {pa1['assertiveness_rate_per_100']:>15.2f}  {pa2['assertiveness_rate_per_100']:>15.2f}")

    if "error" not in se1 and "error" not in se2:
        print(f"  {'Sentiment avg':<23} {se1.get('overall_average',0):>15}  {se2.get('overall_average',0):>15}")

    conn.close()


# ── Integration commands ──────────────────────────────────────

def cmd_link_crm(args):
    matches = auto_link_crm()
    if not matches:
        print("No matches found between speakers and CRM contacts.")
        return
    print(f"✓ Linked {len(matches)} speaker(s) to CRM contacts:\n")
    for m in matches:
        print(f"  {m['speaker_name']} → {m['contact_name']} ({m['contact_email'] or 'no email'}) [{m['confidence']:.0%}]")


def cmd_link_kb(args):
    matches = auto_link_kb()
    if not matches:
        print("No matches found between topics and KB entities.")
        return
    print(f"✓ Linked {len(matches)} topic(s) to KB entities:\n")
    for m in matches:
        print(f"  [{m['kb_entity_type']}] {m['kb_entity']} ← topic '{m['topic']}' (speaker {m['speaker_id']}) [{m['confidence']:.0%}]")


def cmd_push_to_kb(args):
    result = push_to_kb(args.id)
    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    if result.get("status") == "already_exists":
        print(f"Already in KB (source_id={result['source_id']})")
    else:
        print(f"✓ Pushed to KB: source_id={result['source_id']}, {result['word_count']} words")


def cmd_cross_search(args):
    results = cross_search(args.query, limit=args.limit if hasattr(args, 'limit') else 20)
    if not results:
        print("No results found.")
        return
    for i, r in enumerate(results, 1):
        src = "🧬 DNA" if r["source"] == "communication_dna" else "📚 KB"
        title = r.get("title") or ""
        speaker = r.get("speaker") or ""
        label = f"{speaker} in {title}" if speaker else title
        text = (r.get("text") or "")[:120]
        print(f"  {i}. [{src}] {label}")
        print(f"     {text}")
        print()


def main():
    parser = argparse.ArgumentParser(prog="dna", description="Communication DNA — transcription analysis CLI")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("ingest", help="Ingest a transcription file")
    p.add_argument("file")
    p.add_argument("--title")
    p.add_argument("--date")
    p.add_argument("--context")

    p = sub.add_parser("ingest-dir", help="Batch ingest a directory")
    p.add_argument("directory")
    p.add_argument("--context")

    sub.add_parser("speakers", help="List all speakers")

    p = sub.add_parser("speaker", help="Show speaker details")
    p.add_argument("id", type=int)

    sub.add_parser("transcriptions", help="List all transcriptions")

    p = sub.add_parser("transcription", help="Show transcription details")
    p.add_argument("id", type=int)

    p = sub.add_parser("search", help="Search segments")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=20)

    sub.add_parser("stats", help="Overall statistics")

    # Analysis commands
    p = sub.add_parser("analyze", help="Full analysis for a speaker")
    p.add_argument("id", type=int)

    sub.add_parser("analyze-all", help="Full analysis for all speakers")

    p = sub.add_parser("fingerprint", help="Vocabulary fingerprint for a speaker")
    p.add_argument("id", type=int)

    p = sub.add_parser("fillers", help="Filler word report for a speaker")
    p.add_argument("id", type=int)

    p = sub.add_parser("patterns", help="Speech patterns for a speaker")
    p.add_argument("id", type=int)

    p = sub.add_parser("commitments", help="List extracted commitments")
    p.add_argument("id", type=int, nargs="?", default=None)

    p = sub.add_parser("sentiment", help="Sentiment arc for a transcription")
    p.add_argument("id", type=int)

    p = sub.add_parser("topics", help="Top topics")
    p.add_argument("id", type=int, nargs="?", default=None)

    p = sub.add_parser("compare", help="Compare two speakers side-by-side")
    p.add_argument("id1", type=int)
    p.add_argument("id2", type=int)

    # Integration commands
    sub.add_parser("link-crm", help="Auto-link speakers to CRM contacts")
    sub.add_parser("link-kb", help="Auto-link topics/entities to KB")

    p = sub.add_parser("push-to-kb", help="Push a transcription into the Knowledge Base")
    p.add_argument("id", type=int)

    p = sub.add_parser("cross-search", help="Search across DNA + KB")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "ingest": cmd_ingest,
        "ingest-dir": cmd_ingest_dir,
        "speakers": cmd_speakers,
        "speaker": cmd_speaker,
        "transcriptions": cmd_transcriptions,
        "transcription": cmd_transcription,
        "search": cmd_search,
        "stats": cmd_stats,
        "analyze": cmd_analyze,
        "analyze-all": cmd_analyze_all,
        "fingerprint": cmd_fingerprint,
        "fillers": cmd_fillers,
        "patterns": cmd_patterns,
        "commitments": cmd_commitments,
        "sentiment": cmd_sentiment,
        "topics": cmd_topics,
        "compare": cmd_compare,
        "link-crm": cmd_link_crm,
        "link-kb": cmd_link_kb,
        "push-to-kb": cmd_push_to_kb,
        "cross-search": cmd_cross_search,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
