# -*- coding: utf-8 -*-
"""
Question Bank & Error Tracker Manager
Usage (python -X utf8):
  manage_bank.py init                              - Initialize data dirs
  manage_bank.py list [--subject S] [--topic T]    - List questions
  manage_bank.py add <json_file>                   - Add questions from JSON
  manage_bank.py random [--subject S] [--count N]  - Random select for exam
  manage_bank.py export [--subject S] [--count N] [--out F] - Export exam JSON
  manage_bank.py error-add <qid> <student_ans>     - Record a wrong answer
  manage_bank.py error-list [--subject S]          - List errors for review
  manage_bank.py error-mark <qid>                  - Mark error as reviewed
"""
import json, os, sys, random, datetime

DATA_DIR = os.path.join(os.path.expanduser("~"), ".qclaw", "workspace", "exam-data")
Q_DIR = os.path.join(DATA_DIR, "questions")
E_DIR = os.path.join(DATA_DIR, "errors")

def _ensure_dirs():
    os.makedirs(Q_DIR, exist_ok=True)
    os.makedirs(E_DIR, exist_ok=True)

def _q_file(subject):
    return os.path.join(Q_DIR, f"{subject}.json")

def _e_file(subject):
    return os.path.join(E_DIR, f"{subject}_errors.json")

def _load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── Init ──────────────────────────────────────────────────────────────
def cmd_init():
    _ensure_dirs()
    print("OK: data dirs created at", DATA_DIR)

# ── List ──────────────────────────────────────────────────────────────
def cmd_list(subject=None, topic=None):
    files = sorted(os.listdir(Q_DIR)) if os.path.isdir(Q_DIR) else []
    for fn in files:
        if not fn.endswith(".json"):
            continue
        s = fn.replace(".json", "")
        if subject and s != subject:
            continue
        data = _load_json(os.path.join(Q_DIR, fn))
        if not data:
            continue
        print(f"\n=== {s} ({len(data.get('questions',[]))} questions) ===")
        for q in data.get("questions", []):
            if topic and q.get("topic") != topic:
                continue
            qid = q.get("id", "?")
            qtype = q.get("type", "?")
            diff = q.get("difficulty", "?")
            text_preview = q.get("text", "")[:40]
            print(f"  [{qid}] type={qtype} diff={diff} | {text_preview}...")

# ── Add ───────────────────────────────────────────────────────────────
def cmd_add(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        incoming = json.load(f)
    subject = incoming.get("subject", "general")
    qfile = _q_file(subject)
    bank = _load_json(qfile) or {"subject": subject, "questions": []}
    existing_ids = {q["id"] for q in bank["questions"] if "id" in q}
    added = 0
    for q in incoming.get("questions", []):
        if q.get("id") in existing_ids:
            print(f"  SKIP duplicate: {q.get('id')}")
            continue
        bank["questions"].append(q)
        added += 1
    _save_json(qfile, bank)
    print(f"OK: added {added} questions to {subject} (total: {len(bank['questions'])})")

# ── Random / Export ───────────────────────────────────────────────────
def cmd_random(subject=None, count=10, topic=None, difficulty=None):
    qfile = _q_file(subject or "informatics")
    bank = _load_json(qfile)
    if not bank:
        print("ERROR: no question bank for", subject or "informatics")
        return
    pool = bank["questions"]
    if topic:
        pool = [q for q in pool if q.get("topic") == topic]
    if difficulty:
        pool = [q for q in pool if q.get("difficulty") == difficulty]
    if len(pool) < count:
        print(f"WARN: only {len(pool)} questions available, selecting all")
        count = len(pool)
    selected = random.sample(pool, count)
    print(f"Selected {len(selected)} questions:")
    for q in selected:
        print(f"  [{q.get('id','?')}] {q.get('text','')[:50]}")
    return selected

def cmd_export(subject=None, count=10, topic=None, difficulty=None, out=None):
    selected = cmd_random(subject=subject, count=count, topic=topic, difficulty=difficulty)
    if not selected:
        return
    # Group by type
    sections = {}
    for q in selected:
        qtype = q.get("type", "choice")
        sections.setdefault(qtype, []).append(q)

    # Build exam JSON
    exam = {
        "title": "\u4fe1\u606f\u5b66\u5965\u8d5b\u6d4b\u8bd5\u5377",
        "subtitle": "\uff08\u8003\u8bd5\u65f6\u95f4\uff1a60\u5206\u949f    \u6ee1\u5206\uff1a100\u5206\uff09",
        "layout": {
            "info_labels": ["\u59d3\u540d\uff1a____________", "\u73ed\u7ea7\uff1a____________", "\u5b66\u53f7\uff1a____________"],
            "instruction": "\u2605 \u8bf7\u5c06\u7b54\u6848\u586b\u5199\u5728\u7b54\u9898\u5361\u5bf9\u5e94\u4f4d\u7f6e\u3002",
            "footer": "\u2605\u2605\u2605 \u8003\u8bd5\u7ed3\u675f\uff0c\u8bf7\u786e\u8ba4\u6240\u6709\u9898\u76ee\u5df2\u4f5c\u7b54\uff01\u2605\u2605\u2605"
        },
        "sections": []
    }

    type_config = {
        "choice":        {"title": "\u4e00\u3001\u9009\u62e9\u9898", "note": "\uff08\u8bf7\u9009\u51fa\u6700\u7b26\u5408\u9898\u610f\u7684\u7b54\u6848\uff09", "per_score": 4},
        "judgment":      {"title": "\u4e8c\u3001\u5224\u65ad\u9898", "note": "\uff08\u6b63\u786e\u586bv\uff0c\u9519\u8bef\u586bx\uff09", "per_score": 4},
        "programming_fill": {"title": "\u4e09\u3001\u7f16\u7a0b\u586b\u7a7a\u9898", "note": "\uff08\u9605\u8bfb\u7a0b\u5e8f\uff0c\u586b\u5199\u6b63\u786e\u4ee3\u7801\uff09", "per_score": 10},
    }

    for qtype, cfg in type_config.items():
        qs = sections.get(qtype, [])
        if not qs:
            continue
        n = len(qs)
        score = n * cfg["per_score"]
        sec = {
            "type": qtype,
            "title": cfg["title"],
            "count_label": f"\u5171{n}\u9898\uff0c\u6bcf\u9898{cfg['per_score']}\u5206\uff0c\u5171{score}\u5206",
            "note": cfg.get("note", ""),
            "questions": qs
        }
        exam["sections"].append(sec)

    outpath = out or os.path.join(DATA_DIR, f"exam_{datetime.date.today().isoformat()}.json")
    _save_json(outpath, exam)
    print(f"OK: exam JSON exported to {outpath}")

# ── Error tracking ────────────────────────────────────────────────────
def cmd_error_add(qid, student_ans, subject="informatics"):
    efile = _e_file(subject)
    errors = _load_json(efile) or {"subject": subject, "records": []}
    now = datetime.date.today().isoformat()
    errors["records"].append({
        "question_id": qid,
        "date": now,
        "student_answer": student_ans,
        "review_count": 0,
        "last_review": None
    })
    _save_json(efile, errors)
    print(f"OK: error recorded for {qid}")

def cmd_error_list(subject="informatics"):
    efile = _e_file(subject)
    errors = _load_json(efile)
    if not errors or not errors.get("records"):
        print("No errors recorded.")
        return
    # Load question bank for context
    qfile = _q_file(subject)
    bank = _load_json(qfile) or {"questions": []}
    q_map = {q.get("id"): q for q in bank["questions"]}
    print(f"\n=== {subject} Error Records ({len(errors['records'])}) ===")
    for r in errors["records"]:
        qid = r["question_id"]
        q = q_map.get(qid, {})
        text_preview = q.get("text", "")[:40] if q else "(unknown)"
        correct = q.get("answer", "?") if q else "?"
        reviews = r.get("review_count", 0)
        print(f"  [{qid}] your={r.get('student_answer','')} correct={correct} "
              f"reviews={reviews} | {text_preview}...")

def cmd_error_mark(qid, subject="informatics"):
    efile = _e_file(subject)
    errors = _load_json(efile)
    if not errors:
        print("No error file found.")
        return
    now = datetime.date.today().isoformat()
    for r in errors["records"]:
        if r["question_id"] == qid:
            r["review_count"] = r.get("review_count", 0) + 1
            r["last_review"] = now
            break
    _save_json(efile, errors)
    print(f"OK: marked {qid} as reviewed")

# ── CLI ───────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]

    # Parse common flags
    def _flag(name, default=None):
        if name in sys.argv:
            idx = sys.argv.index(name)
            if idx + 1 < len(sys.argv):
                return sys.argv[idx + 1]
        return default

    subject = _flag("--subject", "informatics")
    topic = _flag("--topic")
    count = int(_flag("--count", "10"))
    difficulty = _flag("--difficulty")
    if difficulty:
        difficulty = int(difficulty)
    out = _flag("--out")

    if cmd == "init":
        cmd_init()
    elif cmd == "list":
        cmd_list(subject=subject, topic=topic)
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: manage_bank.py add <json_file>")
            sys.exit(1)
        cmd_add(sys.argv[2])
    elif cmd == "random":
        cmd_random(subject=subject, count=count, topic=topic, difficulty=difficulty)
    elif cmd == "export":
        cmd_export(subject=subject, count=count, topic=topic, difficulty=difficulty, out=out)
    elif cmd == "error-add":
        if len(sys.argv) < 4:
            print("Usage: manage_bank.py error-add <qid> <student_answer>")
            sys.exit(1)
        cmd_error_add(sys.argv[2], sys.argv[3], subject=subject)
    elif cmd == "error-list":
        cmd_error_list(subject=subject)
    elif cmd == "error-mark":
        if len(sys.argv) < 3:
            print("Usage: manage_bank.py error-mark <qid>")
            sys.exit(1)
        cmd_error_mark(sys.argv[2], subject=subject)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()
