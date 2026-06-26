# Installation

Save the script from `scripts/mail-search` to your PATH:

```bash
mkdir -p ~/bin
cp scripts/mail-search ~/bin/mail-search
chmod +x ~/bin/mail-search
```

If `scripts/mail-search` was not bundled with this skill, create it from the source below:

```bash
cat > ~/bin/mail-search << 'SCRIPT_EOF'
#!/bin/bash
# mail-search - Fast Apple Mail search via SQLite (~50ms)
# Queries Envelope Index directly, bypassing AppleScript (which hangs at 100K+ emails)
# Safe: copies DB to temp file to avoid conflicts with running Mail.app

set -e

find_db() {
    local db
    for v in 11 10 9; do
        db="$HOME/Library/Mail/V$v/MailData/Envelope Index"
        if [[ -f "$db" ]]; then echo "$db"; return 0; fi
    done
    return 1
}

DB_PATH="${DB_PATH:-$(find_db)}"
if [ -z "$DB_PATH" ]; then echo "Error: Mail database not found" >&2; exit 1; fi

detect_epoch() {
    local sample
    sample=$(sqlite3 "$1" "SELECT date_sent FROM messages ORDER BY ROWID DESC LIMIT 1" 2>/dev/null)
    if [ -n "$sample" ] && [ "$sample" -lt 978307200 ] 2>/dev/null; then echo "978307200"; else echo "0"; fi
}

LIMIT=20; FORMAT="table"; QUIET=""; COPY_DB=true; CMD=""; ARGS=()

usage() {
    cat >&2 <<EOF
Usage: mail-search <command> [args] [options]

Commands:
  subject <query>        Search by subject line
  sender <query>         Search by sender email address
  from <query>           Search by sender display name
  to <query>             Search by recipient address
  unread                 List unread emails
  recent [days]          Last N days (default: 7)
  date-range <from> <to> Search date range (YYYY-MM-DD)
  attachments            Emails with attachments
  thread <id>            Conversation thread for a message
  body <id>              Print email body text
  open <id>              Open email in Mail.app
  stats                  Database statistics

Options:
  -n, --limit N    Max results (default: 20)
  -j, --json       JSON output
  -c, --csv        CSV output
  -q, --quiet      No headers
  --db PATH        Override database path
  --no-copy        Query live DB directly
EOF
    exit 1
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--limit) LIMIT="$2"; shift 2 ;;
        -j|--json) FORMAT="json"; shift ;;
        -c|--csv) FORMAT="csv"; shift ;;
        -q|--quiet) QUIET=1; shift ;;
        --db) DB_PATH="$2"; shift 2 ;;
        --no-copy) COPY_DB=false; shift ;;
        -h|--help) usage ;;
        *) if [ -z "$CMD" ]; then CMD="$1"; else ARGS+=("$1"); fi; shift ;;
    esac
done

[ -z "$CMD" ] && usage

if $COPY_DB; then
    TEMP_DB=$(mktemp -t mail-search.XXXXXX)
    cleanup() { rm -f "$TEMP_DB" 2>/dev/null || true; }
    trap cleanup EXIT INT TERM
    cp "$DB_PATH" "$TEMP_DB"
    QUERY_DB="$TEMP_DB"
else
    QUERY_DB="$DB_PATH"
fi

EPOCH_OFFSET=$(detect_epoch "$QUERY_DB")
DATE_EXPR="datetime(m.date_sent + $EPOCH_OFFSET, 'unixepoch')"
NOW_EXPR="(strftime('%s', 'now') - $EPOCH_OFFSET)"

case $CMD in
    subject)
        [ ${#ARGS[@]} -lt 1 ] && { echo "Usage: mail-search subject <query>" >&2; exit 1; }
        SEARCH="${ARGS[0]}"
        QUERY="SELECT m.ROWID as id, CASE WHEN (m.read = 0) THEN '●' ELSE ' ' END as unread,
               $DATE_EXPR as date, COALESCE(a.comment, a.address, 'Unknown') as sender, s.subject
               FROM messages m JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               WHERE s.subject LIKE '%${SEARCH//\'/\'\'}%'
               ORDER BY m.date_sent DESC LIMIT $LIMIT" ;;
    sender)
        [ ${#ARGS[@]} -lt 1 ] && { echo "Usage: mail-search sender <query>" >&2; exit 1; }
        SEARCH="${ARGS[0]}"
        QUERY="SELECT m.ROWID as id, CASE WHEN (m.read = 0) THEN '●' ELSE ' ' END as unread,
               $DATE_EXPR as date, a.address as sender, s.subject
               FROM messages m JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               WHERE a.address LIKE '%${SEARCH//\'/\'\'}%'
               ORDER BY m.date_sent DESC LIMIT $LIMIT" ;;
    from)
        [ ${#ARGS[@]} -lt 1 ] && { echo "Usage: mail-search from <name>" >&2; exit 1; }
        SEARCH="${ARGS[0]}"
        QUERY="SELECT m.ROWID as id, CASE WHEN (m.read = 0) THEN '●' ELSE ' ' END as unread,
               $DATE_EXPR as date, COALESCE(a.comment, '') || ' <' || a.address || '>' as sender, s.subject
               FROM messages m JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               WHERE a.comment LIKE '%${SEARCH//\'/\'\'}%'
               ORDER BY m.date_sent DESC LIMIT $LIMIT" ;;
    to)
        [ ${#ARGS[@]} -lt 1 ] && { echo "Usage: mail-search to <address>" >&2; exit 1; }
        SEARCH="${ARGS[0]}"
        QUERY="SELECT m.ROWID as id, $DATE_EXPR as date, ra.address as to_addr, s.subject
               FROM messages m JOIN subjects s ON m.subject = s.ROWID
               JOIN recipients r ON r.message = m.ROWID
               JOIN addresses ra ON r.address = ra.ROWID
               WHERE ra.address LIKE '%${SEARCH//\'/\'\'}%'
               ORDER BY m.date_sent DESC LIMIT $LIMIT" ;;
    unread)
        QUERY="SELECT m.ROWID as id, $DATE_EXPR as date,
               COALESCE(a.comment, a.address, 'Unknown') as sender, s.subject
               FROM messages m JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               WHERE m.read = 0 AND m.deleted = 0
               ORDER BY m.date_sent DESC LIMIT $LIMIT" ;;
    recent)
        DAYS="${ARGS[0]:-7}"
        QUERY="SELECT m.ROWID as id, CASE WHEN (m.read = 0) THEN '●' ELSE ' ' END as unread,
               $DATE_EXPR as date, COALESCE(a.comment, a.address, 'Unknown') as sender, s.subject
               FROM messages m JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               WHERE m.date_sent > ($NOW_EXPR - ($DAYS * 86400)) AND m.deleted = 0
               ORDER BY m.date_sent DESC LIMIT $LIMIT" ;;
    date-range)
        [ ${#ARGS[@]} -lt 2 ] && { echo "Usage: mail-search date-range YYYY-MM-DD YYYY-MM-DD" >&2; exit 1; }
        FROM_DATE="${ARGS[0]}"; TO_DATE="${ARGS[1]}"
        QUERY="SELECT m.ROWID as id, CASE WHEN (m.read = 0) THEN '●' ELSE ' ' END as unread,
               $DATE_EXPR as date, COALESCE(a.comment, a.address, 'Unknown') as sender, s.subject
               FROM messages m JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               WHERE m.date_sent >= (strftime('%s', '$FROM_DATE') - $EPOCH_OFFSET)
               AND m.date_sent < (strftime('%s', '$TO_DATE', '+1 day') - $EPOCH_OFFSET) AND m.deleted = 0
               ORDER BY m.date_sent DESC LIMIT $LIMIT" ;;
    attachments)
        QUERY="SELECT m.ROWID as id, $DATE_EXPR as date,
               COALESCE(a.comment, a.address, 'Unknown') as sender, s.subject, att.filename
               FROM messages m JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               JOIN attachments att ON att.message_id = m.ROWID
               WHERE m.deleted = 0 ORDER BY m.date_sent DESC LIMIT $LIMIT" ;;
    thread)
        [ ${#ARGS[@]} -lt 1 ] && { echo "Usage: mail-search thread <message_id>" >&2; exit 1; }
        MSG_ID="${ARGS[0]}"
        QUERY="SELECT m.ROWID as id, CASE WHEN (m.read = 0) THEN '●' ELSE ' ' END as unread,
               $DATE_EXPR as date, COALESCE(a.comment, a.address, 'Unknown') as sender, s.subject
               FROM messages m JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               WHERE m.conversation_id = (SELECT conversation_id FROM messages WHERE ROWID = $MSG_ID)
               ORDER BY m.date_sent ASC LIMIT $LIMIT" ;;
    body)
        [ ${#ARGS[@]} -lt 1 ] && { echo "Usage: mail-search body <message_id>" >&2; exit 1; }
        MSG_ID="${ARGS[0]}"
        EMLX=$(find ~/Library/Mail/V*/  -name "${MSG_ID}.emlx" 2>/dev/null | head -1)
        if [ -z "$EMLX" ]; then echo "Error: .emlx file not found for message $MSG_ID" >&2; exit 1; fi
        python3 -c "
import email, sys, re
with open('$EMLX', 'r', errors='replace') as f:
    f.readline()
    raw = f.read()
    idx = raw.find('<?xml')
    if idx > 0: raw = raw[:idx]
    msg = email.message_from_string(raw)
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            payload = part.get_payload(decode=True)
            if payload: print(payload.decode('utf-8', errors='replace')); sys.exit(0)
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            payload = part.get_payload(decode=True)
            if payload:
                text = re.sub('<[^>]+>', ' ', payload.decode('utf-8', errors='replace'))
                print(re.sub(r'\s+', ' ', text).strip()); sys.exit(0)
    print('(no text content found)', file=sys.stderr)
"
        exit $? ;;
    open)
        [ ${#ARGS[@]} -lt 1 ] && { echo "Usage: mail-search open <message_id>" >&2; exit 1; }
        MSG_ID="${ARGS[0]}"
        MSG_UUID=$(sqlite3 "$QUERY_DB" "SELECT document_id FROM messages WHERE ROWID = $MSG_ID" 2>/dev/null)
        if [ -n "$MSG_UUID" ]; then open "message://%3c${MSG_UUID}%3e"
        else echo "Error: Message $MSG_ID not found" >&2; exit 1; fi ;;
    stats)
        QUERY="SELECT (SELECT COUNT(*) FROM messages) as total_messages,
               (SELECT COUNT(*) FROM messages WHERE read = 0 AND deleted = 0) as unread,
               (SELECT COUNT(*) FROM addresses) as addresses,
               (SELECT COUNT(*) FROM subjects) as subjects,
               (SELECT COUNT(*) FROM mailboxes) as mailboxes,
               $DATE_EXPR as newest_email
               FROM messages m ORDER BY m.date_sent DESC LIMIT 1" ;;
    *) echo "Unknown command: $CMD" >&2; usage ;;
esac

if [ -n "$QUERY" ]; then
    if [ "$FORMAT" = "json" ]; then sqlite3 "$QUERY_DB" -json "$QUERY"
    elif [ "$FORMAT" = "csv" ]; then sqlite3 "$QUERY_DB" -csv -header "$QUERY"
    else
        if [ -n "$QUIET" ]; then sqlite3 "$QUERY_DB" -separator ' | ' "$QUERY"
        else sqlite3 "$QUERY_DB" -header -separator ' | ' "$QUERY"; fi
    fi
fi
SCRIPT_EOF
chmod +x ~/bin/mail-search
```

Verify installation:

```bash
mail-search stats
```
