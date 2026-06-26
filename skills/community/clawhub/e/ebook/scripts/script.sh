#!/usr/bin/env bash
# ebook/scripts/script.sh — Digital Book Collection & Reading Tracker
# Data: ~/.ebook/data.jsonl
set -euo pipefail
VERSION="1.0.0"
DATA_DIR="$HOME/.ebook"
DATA_FILE="$DATA_DIR/data.jsonl"
mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

CMD="${1:-help}"
shift 2>/dev/null || true

show_help() {
cat << 'HELPEOF'
Ebook — Digital Book Collection & Reading Tracker  v1.0.0

Usage: bash scripts/script.sh <command> [options]

Commands:
  add          Add a new ebook to the collection
  list         List all ebooks with optional filters
  search       Search ebooks by title, author, tag, or keyword
  update       Update metadata for an existing ebook
  delete       Remove an ebook from the collection
  read         Log a reading session with pages and duration
  progress     Show reading progress for a book or all books
  highlight    Add a highlighted passage or annotation
  review       Add or update a rating and review for a book
  stats        Show reading statistics
  export       Export the library or highlights
  help         Show this help message
  version      Print the tool version
HELPEOF
}

case "$CMD" in
  add|list|search|update|delete|read|progress|highlight|review|stats|export)
    SKILL_CMD="$CMD" SKILL_ARGV="$(printf '%s\n' "$@")" python3 << 'PYEOF'
import sys, json, os, uuid, datetime

DATA_DIR = os.path.expanduser("~/.ebook")
DATA_FILE = os.path.join(DATA_DIR, "data.jsonl")

def load_records():
    records = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return records

def save_records(records):
    with open(DATA_FILE, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

def append_record(record):
    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

def gen_id():
    return uuid.uuid4().hex[:8]

def now_iso():
    return datetime.datetime.now().isoformat()

def parse_args(args):
    parsed = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:]
            if i + 1 < len(args) and not args[i+1].startswith("--"):
                parsed[key] = args[i+1]
                i += 2
            else:
                parsed[key] = True
                i += 1
        else:
            i += 1
    return parsed

def find_book(records, book_id):
    for r in records:
        if r.get("type") == "book" and r.get("id") == book_id:
            return r
    return None

def cmd_add(args):
    opts = parse_args(args)
    title = opts.get("title", "Untitled")
    author = opts.get("author", "Unknown")
    fmt = opts.get("format", "epub")
    pages = int(opts.get("pages", "0"))
    tags_str = opts.get("tags", "")
    tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []
    status = opts.get("status", "unread")

    valid_formats = ["epub", "pdf", "mobi", "azw3", "txt", "djvu"]
    if fmt not in valid_formats:
        print(json.dumps({"error": f"Invalid format '{fmt}'", "valid": valid_formats}))
        sys.exit(1)

    valid_statuses = ["unread", "reading", "finished", "abandoned", "wishlist"]
    if status not in valid_statuses:
        print(json.dumps({"error": f"Invalid status '{status}'", "valid": valid_statuses}))
        sys.exit(1)

    record = {
        "id": gen_id(),
        "type": "book",
        "title": title,
        "author": author,
        "format": fmt,
        "pages": pages,
        "tags": tags,
        "status": status,
        "pages_read": 0,
        "created_at": now_iso(),
        "updated_at": now_iso()
    }
    append_record(record)
    print(json.dumps(record, indent=2))

def cmd_list(args):
    opts = parse_args(args)
    status_filter = opts.get("status", "")
    author_filter = opts.get("author", "").lower()
    format_filter = opts.get("format", "")
    records = load_records()
    books = [r for r in records if r.get("type") == "book"]

    if status_filter:
        books = [b for b in books if b.get("status") == status_filter]
    if author_filter:
        books = [b for b in books if author_filter in b.get("author", "").lower()]
    if format_filter:
        books = [b for b in books if b.get("format") == format_filter]

    if not books:
        print("No ebooks found matching criteria.")
        return

    print(f"{'ID':<10} {'Title':<30} {'Author':<20} {'Format':<6} {'Status':<10} {'Progress':<10}")
    print("-" * 86)
    for b in books:
        pages = b.get("pages", 0)
        pages_read = b.get("pages_read", 0)
        pct = f"{round(pages_read/pages*100)}%" if pages > 0 else "N/A"
        title = b.get("title", "?")[:28]
        author = b.get("author", "?")[:18]
        print(f"{b['id']:<10} {title:<30} {author:<20} {b.get('format','?'):<6} {b.get('status','?'):<10} {pct:<10}")

def cmd_search(args):
    opts = parse_args(args)
    query = opts.get("query", "").lower()
    author_q = opts.get("author", "").lower()
    tag_q = opts.get("tag", "").lower()
    records = load_records()
    books = [r for r in records if r.get("type") == "book"]
    results = []

    for b in books:
        match = False
        if query:
            searchable = f"{b.get('title','')} {b.get('author','')} {' '.join(b.get('tags',[]))}".lower()
            if query in searchable:
                match = True
        if author_q and author_q in b.get("author", "").lower():
            match = True
        if tag_q and tag_q in [t.lower() for t in b.get("tags", [])]:
            match = True
        if match:
            results.append(b)

    if not results:
        print("No matching books found.")
        return
    for b in results:
        print(f"[{b['id']}] {b.get('title','')} by {b.get('author','')} ({b.get('format','')}) [{b.get('status','')}]")

def cmd_update(args):
    opts = parse_args(args)
    book_id = opts.get("id", "")
    if not book_id:
        print(json.dumps({"error": "Please provide --id"}))
        sys.exit(1)
    records = load_records()
    found = False
    for r in records:
        if r.get("type") == "book" and r.get("id") == book_id:
            found = True
            if "title" in opts:
                r["title"] = opts["title"]
            if "author" in opts:
                r["author"] = opts["author"]
            if "status" in opts:
                valid_statuses = ["unread", "reading", "finished", "abandoned", "wishlist"]
                if opts["status"] in valid_statuses:
                    r["status"] = opts["status"]
            if "tags" in opts:
                r["tags"] = [t.strip() for t in opts["tags"].split(",") if t.strip()]
            if "format" in opts:
                r["format"] = opts["format"]
            if "pages" in opts:
                r["pages"] = int(opts["pages"])
            r["updated_at"] = now_iso()
            print(json.dumps(r, indent=2))
            break
    if not found:
        print(json.dumps({"error": f"Book with id '{book_id}' not found"}))
        sys.exit(1)
    save_records(records)

def cmd_delete(args):
    opts = parse_args(args)
    book_id = opts.get("id", "")
    if not book_id:
        print(json.dumps({"error": "Please provide --id"}))
        sys.exit(1)
    records = load_records()
    original_len = len(records)
    # Remove book and all related records (sessions, highlights, reviews)
    records = [r for r in records if not (r.get("id") == book_id or r.get("book_id") == book_id)]
    if len(records) == original_len:
        print(json.dumps({"error": f"Book with id '{book_id}' not found"}))
        sys.exit(1)
    save_records(records)
    removed = original_len - len(records)
    print(json.dumps({"deleted": True, "id": book_id, "records_removed": removed}))

def cmd_read(args):
    opts = parse_args(args)
    book_id = opts.get("id", "")
    start_page = int(opts.get("start-page", opts.get("start_page", "0")))
    end_page = int(opts.get("end-page", opts.get("end_page", "0")))
    duration = int(opts.get("duration", "0"))  # in minutes

    if not book_id:
        print(json.dumps({"error": "Please provide --id"}))
        sys.exit(1)

    records = load_records()
    book = find_book(records, book_id)
    if not book:
        print(json.dumps({"error": f"Book '{book_id}' not found"}))
        sys.exit(1)

    pages_in_session = end_page - start_page
    session = {
        "id": gen_id(),
        "type": "session",
        "book_id": book_id,
        "start_page": start_page,
        "end_page": end_page,
        "pages_read": pages_in_session,
        "duration_minutes": duration,
        "created_at": now_iso()
    }

    # Update book's pages_read
    for r in records:
        if r.get("type") == "book" and r.get("id") == book_id:
            r["pages_read"] = max(r.get("pages_read", 0), end_page)
            if r.get("pages", 0) > 0 and r["pages_read"] >= r["pages"]:
                r["status"] = "finished"
            elif r.get("status") == "unread":
                r["status"] = "reading"
            r["updated_at"] = now_iso()
            break

    save_records(records)
    append_record(session)
    print(json.dumps(session, indent=2))

def cmd_progress(args):
    opts = parse_args(args)
    book_id = opts.get("id", "")
    records = load_records()

    if book_id:
        book = find_book(records, book_id)
        if not book:
            print(json.dumps({"error": f"Book '{book_id}' not found"}))
            sys.exit(1)
        pages = book.get("pages", 0)
        pages_read = book.get("pages_read", 0)
        pct = round(pages_read / pages * 100, 1) if pages > 0 else 0
        bar_len = 30
        filled = round(bar_len * pct / 100)
        bar = "█" * filled + "░" * (bar_len - filled)
        sessions = [r for r in records if r.get("type") == "session" and r.get("book_id") == book_id]
        total_time = sum(s.get("duration_minutes", 0) for s in sessions)
        print(f"Title:    {book.get('title', '?')}")
        print(f"Author:   {book.get('author', '?')}")
        print(f"Status:   {book.get('status', '?')}")
        print(f"Progress: [{bar}] {pct}%  ({pages_read}/{pages} pages)")
        print(f"Sessions: {len(sessions)}  |  Total time: {total_time} min")
    else:
        books = [r for r in records if r.get("type") == "book"]
        if not books:
            print("No books in collection.")
            return
        for book in books:
            pages = book.get("pages", 0)
            pages_read = book.get("pages_read", 0)
            pct = round(pages_read / pages * 100) if pages > 0 else 0
            bar_len = 20
            filled = round(bar_len * pct / 100)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"[{book['id']}] {book.get('title','?')[:25]:<25} [{bar}] {pct}%")

def cmd_highlight(args):
    opts = parse_args(args)
    book_id = opts.get("id", "")
    page = int(opts.get("page", "0"))
    text = opts.get("text", "")
    color = opts.get("color", "yellow")

    if not book_id:
        print(json.dumps({"error": "Please provide --id"}))
        sys.exit(1)

    records = load_records()
    book = find_book(records, book_id)
    if not book:
        print(json.dumps({"error": f"Book '{book_id}' not found"}))
        sys.exit(1)

    highlight = {
        "id": gen_id(),
        "type": "highlight",
        "book_id": book_id,
        "book_title": book.get("title", ""),
        "page": page,
        "text": text,
        "color": color,
        "created_at": now_iso()
    }
    append_record(highlight)
    print(json.dumps(highlight, indent=2))

def cmd_review(args):
    opts = parse_args(args)
    book_id = opts.get("id", "")
    rating = int(opts.get("rating", "0"))
    text = opts.get("text", "")

    if not book_id:
        print(json.dumps({"error": "Please provide --id"}))
        sys.exit(1)
    if rating < 1 or rating > 5:
        print(json.dumps({"error": "Rating must be 1-5"}))
        sys.exit(1)

    records = load_records()
    book = find_book(records, book_id)
    if not book:
        print(json.dumps({"error": f"Book '{book_id}' not found"}))
        sys.exit(1)

    # Check for existing review and update it
    existing_review = None
    for r in records:
        if r.get("type") == "review" and r.get("book_id") == book_id:
            existing_review = r
            break

    if existing_review:
        existing_review["rating"] = rating
        existing_review["text"] = text
        existing_review["updated_at"] = now_iso()
        save_records(records)
        print(json.dumps(existing_review, indent=2))
    else:
        review = {
            "id": gen_id(),
            "type": "review",
            "book_id": book_id,
            "book_title": book.get("title", ""),
            "rating": rating,
            "stars": "★" * rating + "☆" * (5 - rating),
            "text": text,
            "created_at": now_iso()
        }
        append_record(review)
        print(json.dumps(review, indent=2))

def cmd_stats(args):
    records = load_records()
    books = [r for r in records if r.get("type") == "book"]
    sessions = [r for r in records if r.get("type") == "session"]
    highlights = [r for r in records if r.get("type") == "highlight"]
    reviews = [r for r in records if r.get("type") == "review"]

    total_books = len(books)
    status_counts = {}
    for b in books:
        s = b.get("status", "unknown")
        status_counts[s] = status_counts.get(s, 0) + 1

    total_pages_read = sum(b.get("pages_read", 0) for b in books)
    total_time = sum(s.get("duration_minutes", 0) for s in sessions)
    total_sessions = len(sessions)
    avg_pages = round(sum(s.get("pages_read", 0) for s in sessions) / total_sessions, 1) if total_sessions > 0 else 0
    avg_duration = round(total_time / total_sessions, 1) if total_sessions > 0 else 0

    # Reading streak (consecutive days with sessions)
    session_dates = sorted(set(s.get("created_at", "")[:10] for s in sessions))
    streak = 0
    if session_dates:
        current_streak = 1
        max_streak = 1
        for i in range(1, len(session_dates)):
            d1 = datetime.datetime.strptime(session_dates[i-1], "%Y-%m-%d")
            d2 = datetime.datetime.strptime(session_dates[i], "%Y-%m-%d")
            if (d2 - d1).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        streak = max_streak

    stats = {
        "total_books": total_books,
        "by_status": status_counts,
        "total_pages_read": total_pages_read,
        "total_reading_time_minutes": total_time,
        "total_sessions": total_sessions,
        "avg_pages_per_session": avg_pages,
        "avg_minutes_per_session": avg_duration,
        "total_highlights": len(highlights),
        "total_reviews": len(reviews),
        "longest_reading_streak_days": streak
    }
    print(json.dumps(stats, indent=2))

def cmd_export(args):
    opts = parse_args(args)
    fmt = opts.get("format", "json")
    export_type = opts.get("type", "library")
    output = opts.get("output", f"ebook_export.{fmt}")
    records = load_records()

    if export_type == "highlights":
        data = [r for r in records if r.get("type") == "highlight"]
    elif export_type == "reviews":
        data = [r for r in records if r.get("type") == "review"]
    else:
        data = [r for r in records if r.get("type") == "book"]

    if fmt == "json":
        with open(output, "w") as f:
            json.dump(data, f, indent=2)
    elif fmt == "csv":
        import csv as csv_mod
        if data:
            keys = list(data[0].keys())
            with open(output, "w", newline="") as f:
                writer = csv_mod.DictWriter(f, fieldnames=keys, extrasaction="ignore")
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
    elif fmt == "md":
        lines = [f"# Ebook Library Export\n", f"*Exported: {now_iso()}*\n"]
        for item in data:
            if item.get("type") == "book":
                lines.append(f"## {item.get('title', '?')}")
                lines.append(f"- **Author:** {item.get('author', '?')}")
                lines.append(f"- **Format:** {item.get('format', '?')}")
                lines.append(f"- **Pages:** {item.get('pages', 0)}")
                lines.append(f"- **Status:** {item.get('status', '?')}")
                lines.append(f"- **Tags:** {', '.join(item.get('tags', []))}")
                lines.append("")
            elif item.get("type") == "highlight":
                lines.append(f"### Highlight (p.{item.get('page', '?')})")
                lines.append(f"> {item.get('text', '')}")
                lines.append("")
        with open(output, "w") as f:
            f.write("\n".join(lines))
    else:
        with open(output, "w") as f:
            json.dump(data, f, indent=2)

    print(json.dumps({"exported": output, "format": fmt, "type": export_type, "count": len(data)}))

# --- main dispatch ---
import shlex
_cmd = os.environ.get("SKILL_CMD", "")
_argv_raw = os.environ.get("SKILL_ARGV", "")
args = [_cmd] + [a for a in _argv_raw.split("\n") if a] if _cmd else []
cmd = args[0] if args else "help"
rest = args[1:]

dispatch = {
    "add": cmd_add,
    "list": cmd_list,
    "search": cmd_search,
    "update": cmd_update,
    "delete": cmd_delete,
    "read": cmd_read,
    "progress": cmd_progress,
    "highlight": cmd_highlight,
    "review": cmd_review,
    "stats": cmd_stats,
    "export": cmd_export,
}

if cmd in dispatch:
    dispatch[cmd](rest)
else:
    print(f"Unknown command: {cmd}")
    sys.exit(1)
PYEOF
    ;;
  help)
    show_help
    ;;
  version)
    echo "ebook v${VERSION}"
    ;;
  *)
    echo "Error: Unknown command '$CMD'" >&2
    echo "Run 'bash scripts/script.sh help' for usage." >&2
    exit 1
    ;;
esac
