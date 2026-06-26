#!/usr/bin/env bash
# poll-share-notes.sh — Find new Bear notes tagged #share
set -euo pipefail

TAG="${BEAR_SHARE_TAG:-share}"
STATE_FILE="${BEAR_SHARE_STATE:-$HOME/.bear-share-sync/state.json}"
STATE_DIR=$(dirname "$STATE_FILE")
mkdir -p "$STATE_DIR"

# Initialize state if missing
if [ ! -f "$STATE_FILE" ]; then
  echo '{"processed":[]}' > "$STATE_FILE"
fi

# Fetch notes with the share tag
RAW=$(grizzly open-tag --name "$TAG" --enable-callback --json --token-file ~/.config/grizzly/token 2>/dev/null || echo '[]')

# Extract note IDs already processed
PROCESSED=$(python3 -c "import json; print(json.dumps(json.load(open('$STATE_FILE'))['processed']))")

# Filter to unprocessed notes and output
python3 -c "
import json, sys
raw = json.loads('''$RAW''')
processed = set(json.loads('''$PROCESSED'''))
# grizzly returns a list; adapt to its actual output shape
notes = raw if isinstance(raw, list) else raw.get('notes', raw.get('results', []))
new_notes = [n for n in notes if n.get('id') or n.get('identifier','') not in processed]
ids = []
out = []
for n in new_notes:
    nid = n.get('id') or n.get('identifier','')
    ids.append(nid)
    out.append({
        'id': nid,
        'title': n.get('title',''),
        'content': n.get('text') or n.get('content') or n.get('body',''),
        'tags': n.get('tags', [])
    })
# Update state
state = json.load(open('$STATE_FILE'))
state['processed'] = list(set(state['processed']) | set(ids))
json.dump(state, open('$STATE_FILE','w'))
json.dump(out, sys.stdout)
"
