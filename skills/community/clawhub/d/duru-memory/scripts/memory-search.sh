#!/usr/bin/env bash
set -euo pipefail

# Deterministic markdown memory search with optional semantic second pass
# Usage: memory-search.sh "query" [workspace]
# Intended for local maintenance/debugging alongside OpenClaw built-in memory_search.

QUERY="${1:-}"
WORKSPACE="${2:-$(pwd)}"
MEMORY_DIR="${WORKSPACE}/memory"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SEMANTIC_SCRIPT="${SCRIPT_DIR}/memory-semantic-search.py"
CONFIG_FILE="${SCRIPT_DIR}/../config.yaml"
EXAMPLE_CONFIG_FILE="${SCRIPT_DIR}/../config.example.yaml"
ACTIVE_CONFIG_FILE="$CONFIG_FILE"
if [[ ! -f "$ACTIVE_CONFIG_FILE" ]]; then
  ACTIVE_CONFIG_FILE="$EXAMPLE_CONFIG_FILE"
fi
cfg_read() {
  python3 - "$ACTIVE_CONFIG_FILE" "$1" "$2" <<'PY'
import sys, yaml
from pathlib import Path
cfg = {}
p = Path(sys.argv[1])
key = sys.argv[2]
default = sys.argv[3]
if p.exists():
    cfg = yaml.safe_load(p.read_text(encoding='utf-8')) or {}
cur = cfg
for part in key.split('.'):
    if not isinstance(cur, dict) or part not in cur:
        print(default)
        raise SystemExit
    cur = cur[part]
print(cur)
PY
}
SEMANTIC_MIN_SCORE="${SEMANTIC_MIN_SCORE:-$(cfg_read semantic.min_score 0.48)}"
FUSION_MODE="${FUSION_MODE:-$(cfg_read fusion.mode rrf)}"          # rrf | linear
RRF_K="${RRF_K:-$(cfg_read fusion.rrf_k 60)}"
KEYWORD_BOOST="${KEYWORD_BOOST:-$(cfg_read fusion.keyword_boost 0.006)}"   # extra boost for strong keyword matches in RRF mode
PRIOR_BOOST="${PRIOR_BOOST:-$(cfg_read fusion.prior_boost 0.004)}"       # directory prior boost
FUSION_SEM_WEIGHT="${FUSION_SEM_WEIGHT:-$(cfg_read fusion.semantic_weight 0.65)}"
FUSION_KEY_WEIGHT="${FUSION_KEY_WEIGHT:-$(cfg_read fusion.keyword_weight 0.35)}"

if [[ -z "$QUERY" ]]; then
  echo "Usage: $0 \"query\" [workspace]"
  exit 2
fi

if [[ ! -d "$MEMORY_DIR" ]]; then
  echo "memory directory not found: $MEMORY_DIR"
  exit 1
fi

echo "=== memory search ==="
echo "query: $QUERY"
echo "workspace: $WORKSPACE"

tmp_all="$(mktemp)"
tmp_sem="$(mktemp)"
cleanup() { rm -f "$tmp_all" "$tmp_sem"; }
trap cleanup EXIT

# Build tolerant regex: exact query OR any whitespace-split token
alt_regex="$(printf '%s' "$QUERY" | tr ' ' '\n' | sed '/^$/d' | paste -sd'|' -)"
search_regex="$QUERY"
if [[ -n "$alt_regex" ]]; then
  search_regex="$QUERY|$alt_regex"
fi

# Search markdown files with line number. Keep first 200 matches for speed.
grep -RInE --exclude-dir=archive --include='*.md' -- "$search_regex" "$MEMORY_DIR" 2>/dev/null | head -n 200 > "$tmp_all" || true

no_direct_hits=0
if [[ ! -s "$tmp_all" ]]; then
  no_direct_hits=1
  printf '\nNo direct keyword hits.\n'
  echo "Tip: try narrower keywords or project/person names."
fi

show_section() {
  local title="$1"
  local pattern="$2"
  printf '\n[%s]\n' "$title"
  grep -Ei "$pattern" "$tmp_all" | head -n 12 | sed "s#^${WORKSPACE}/##" | sed 's/^/ - /' || true
}

if [[ "$no_direct_hits" -eq 0 ]]; then
  # Categorized outputs (heuristic)
  show_section "Decisions" "decision|decide|选择|决定|方案"
  show_section "Todos / Next actions" "todo|next|next action|\[ \]|待办|下一步|blocker|阻碍"
  show_section "Facts / Preferences" "fact|preference|偏好|习惯|deadline|截止|commitment|承诺"

  printf '\n[Top recent hits]\n'
  sort -r "$tmp_all" | head -n 15 | sed "s#^${WORKSPACE}/##" | sed 's/^/ - /'
fi

semantic_json=''
if [[ -x "$SEMANTIC_SCRIPT" ]]; then
  printf '\n[Semantic hits via Ollama embedding]\n'
  if semantic_json="$(cd "${SCRIPT_DIR}/.." && uv run python "$SEMANTIC_SCRIPT" "$QUERY" "$WORKSPACE" --min-score "$SEMANTIC_MIN_SCORE" 2>/dev/null)"; then
    printf '%s\n' "$semantic_json" > "$tmp_sem"
    printf '%s\n' "$semantic_json" | python3 -c 'import json,sys
obj=json.load(sys.stdin)
print(" model: {}".format(obj.get("model","unknown")))
print(" min_score: {}".format(obj.get("min_score")))
hits=obj.get("hits",[])
if not hits:
    print(" - no semantic hits")
else:
    for h in hits[:6]:
        print(" - {} (score={})".format(h.get("path"), h.get("score")))'
  else
    echo " - semantic search unavailable (ollama/model not ready)"
  fi
fi

printf '\n[Fused ranking (keyword + semantic)]\n'
python3 - "$tmp_all" "$tmp_sem" "$WORKSPACE" "$FUSION_MODE" "$RRF_K" "$KEYWORD_BOOST" "$PRIOR_BOOST" "$FUSION_SEM_WEIGHT" "$FUSION_KEY_WEIGHT" <<'PY'
import json,sys,collections
kw_file, sem_file, workspace, mode, rrf_k, kw_boost, prior_boost, w_sem, w_key = sys.argv[1:10]
mode=(mode or 'rrf').lower()
rrf_k=float(rrf_k)
kw_boost=float(kw_boost)
prior_boost=float(prior_boost)
w_sem=float(w_sem); w_key=float(w_key)
kw_counts=collections.Counter()
try:
    with open(kw_file,'r',encoding='utf-8',errors='ignore') as f:
        for line in f:
            p=line.split(':',1)[0].strip()
            if p:
                p=p.replace(workspace.rstrip('/')+'/', '')
                kw_counts[p]+=1
except Exception:
    pass

sem_scores={}
try:
    with open(sem_file,'r',encoding='utf-8') as f:
        obj=json.load(f)
    for h in obj.get('hits',[]):
        p=h.get('path')
        if p:
            sem_scores[p]=float(h.get('score',0.0))
except Exception:
    pass

all_paths=set(kw_counts) | set(sem_scores)
if not all_paths:
    print(' - no fused hits')
    sys.exit(0)

# per-signal ranks (1 is best)
sem_rank={p:i+1 for i,(p,_) in enumerate(sorted(sem_scores.items(), key=lambda kv: kv[1], reverse=True))}
kw_rank={p:i+1 for i,(p,_) in enumerate(sorted(kw_counts.items(), key=lambda kv: kv[1], reverse=True))}
max_kw=max(kw_counts.values()) if kw_counts else 1

def prior_weight(path:str)->float:
    p=path.replace('\\','/')
    if p.startswith('memory/CORE/'): return 1.00
    if p.startswith('memory/projects/'): return 0.80
    if p.startswith('memory/people/'): return 0.70
    if p.startswith('memory/handoff/'): return 0.60
    if p.startswith('memory/daily/'): return 0.50
    if p.startswith('memory/concepts/'): return 0.40
    return 0.30

import re, pathlib

def read_meta(path_rel:str):
    meta={'status':'active','polarity':'positive','confidence':'medium','avoid_reason':''}
    abs_path=pathlib.Path(workspace)/path_rel
    try:
        text=abs_path.read_text(encoding='utf-8',errors='ignore')[:8000]
    except Exception:
        return meta
    for key in ('status','polarity','confidence','avoid_reason'):
        m=re.search(rf'(?im)^\s*{key}\s*:\s*(.+?)\s*$', text)
        if m:
            meta[key]=m.group(1).strip().strip('"\'')

    # fallback signals (body-only; avoid frontmatter field false positives)
    body=re.sub(r'(?s)^---\n.*?\n---\n?', '', text, count=1)
    explicit_pitfall = re.search(r'(?im)^\s*(?:-|\*)?\s*avoid\s*:\s*\S+', body) or re.search(r'(?im)^\s*(?:-|\*)?\s*do_instead\s*:\s*\S+', body)
    if explicit_pitfall or ('anti-patterns.md' in path_rel.lower()):
        if meta.get('polarity','positive')=='positive':
            meta['polarity']='negative'
        if meta.get('status','active')=='active':
            meta['status']='invalid'
    return meta

active_rows=[]
pitfalls=[]
for p in all_paths:
    sem=sem_scores.get(p,0.0)
    kw=min(1.0, kw_counts.get(p,0)/max_kw)
    prior=prior_weight(p)
    meta=read_meta(p)

    # linear baseline
    linear=w_sem*sem + w_key*kw

    # rrf (missing rank contributes 0)
    rrf=0.0
    if p in sem_rank:
        rrf += 1.0/(rrf_k + sem_rank[p])
    if p in kw_rank:
        rrf += 1.0/(rrf_k + kw_rank[p])

    # keyword boost for explicit-match queries (only in RRF mode)
    kw_extra = kw_boost * max(0.0, kw - 0.5) * 2.0  # kw>=0.5 starts getting boost
    prior_extra = prior_boost * prior
    rrf_boosted = rrf + kw_extra + prior_extra

    fused = rrf_boosted if mode=='rrf' else (linear + prior_extra)
    row=(fused, rrf_boosted, rrf, linear, sem, kw, prior, p, meta)

    is_negative = str(meta.get('polarity','positive')).lower()=='negative' or str(meta.get('status','active')).lower() in ('invalid','superseded')
    if is_negative:
        pitfalls.append(row)
    else:
        active_rows.append(row)

active_rows.sort(key=lambda x: x[0], reverse=True)
pitfalls.sort(key=lambda x: x[0], reverse=True)

print(f" mode: {mode} (rrf_k={rrf_k}, keyword_boost={kw_boost}, prior_boost={prior_boost}, sem_w={w_sem}, key_w={w_key})")
for fused, rrfb, rrf, linear, sem, kw, prior, p, meta in active_rows[:8]:
    print(f" - {p} (fused={fused:.6f}, rrf_boosted={rrfb:.6f}, rrf={rrf:.6f}, linear={linear:.4f}, sem={sem:.4f}, key={kw:.2f}, prior={prior:.2f})")

if pitfalls:
    print("\n[⚠ Avoided Pitfalls — do NOT use as execution basis]")
    for fused, rrfb, rrf, linear, sem, kw, prior, p, meta in pitfalls[:6]:
        reason=meta.get('avoid_reason','').strip()
        reason=f" | avoid_reason={reason}" if reason else ""
        print(f" - {p} (status={meta.get('status')}, polarity={meta.get('polarity')}, confidence={meta.get('confidence')}{reason})")
PY

printf '\n=== end ===\n'
