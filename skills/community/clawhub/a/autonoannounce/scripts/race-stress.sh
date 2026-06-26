#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
CFG="$ROOT/config/tts-queue.json"
LIB="$ROOT/.openclaw/earcon-library.json"
SCRIPT_DIR="$ROOT/skills/autonoannounce/scripts"

mkdir -p "$ROOT/.openclaw" "$ROOT/config"

# Seed minimal config if missing
if [[ ! -f "$CFG" ]]; then
  cat > "$CFG" <<EOF
{
  "earcons": {
    "enabled": true,
    "style": "test",
    "categories": {"start":"","end":"","update":"","important":"","error":""},
    "libraryPath": "$LIB"
  },
  "playback": {"backend":"auto","device":""}
}
EOF
fi

"$SCRIPT_DIR/earcon-library.sh" init >/dev/null

# Concurrency test 1: atomic config rewrite via python setup dry-runs/writes
pids=()
for i in $(seq 1 6); do
  "$SCRIPT_DIR/setup-first-run.sh" --noninteractive --earcons y --style "stress-$i" --backend auto --generate-starters n >/dev/null 2>&1 &
  pids+=("$!")
done
for p in "${pids[@]}"; do wait "$p"; done
python3 - <<PY
import json
json.load(open('$CFG'))
print('config_json_ok')
PY

# Concurrency test 2: concurrent category metadata updates (no API calls)
ROOT_DIR="$ROOT" python3 - <<'PY'
import json,threading,time,os,tempfile
root=os.environ['ROOT_DIR']
cfg_path=os.path.join(root,'config','tts-queue.json')
lib_path=os.path.join(root,'.openclaw','earcon-library.json')
os.makedirs(os.path.dirname(lib_path), exist_ok=True)
if not os.path.exists(lib_path):
    json.dump({'version':1,'earcons':{}}, open(lib_path,'w'))

cats=['start','end','update','important','error']
lock=os.path.join(root,'.openclaw','locks','earcon-library.lock')
os.makedirs(os.path.dirname(lock), exist_ok=True)

import fcntl

def atomic_write(path,obj):
    d=os.path.dirname(path)
    fd,tmp=tempfile.mkstemp(dir=d,prefix='.tmp-',text=True)
    with os.fdopen(fd,'w') as f:
        json.dump(obj,f,indent=2); f.write('\n')
    os.replace(tmp,path)

def worker(cat,idx):
    with open(lock,'w') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        cfg=json.load(open(cfg_path))
        lib=json.load(open(lib_path))
        p=f'/tmp/{cat}-{idx}.mp3'
        cfg['earcons']['categories'][cat]=p
        lib.setdefault('earcons',{})[cat]={'path':p,'created_at':time.time()}
        atomic_write(cfg_path,cfg)
        atomic_write(lib_path,lib)

threads=[]
for i in range(20):
    c=cats[i%len(cats)]
    t=threading.Thread(target=worker,args=(c,i))
    t.start(); threads.append(t)
for t in threads: t.join()

json.load(open(cfg_path)); json.load(open(lib_path))
print('metadata_race_ok')
PY

echo "race_stress_ok"
