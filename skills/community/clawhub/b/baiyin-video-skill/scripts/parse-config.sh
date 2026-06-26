#!/usr/bin/env bash
# 解析视频配置 JSON（多运行时自动检测: node → python3 → jq）
# 用法:
#   bash parse-config.sh models                                    → 输出模型列表
#   bash parse-config.sh model-detail <model_code>                 → 输出生成类型 + 各类型参数选项（合并）
#   bash parse-config.sh match <model_code> <type> [dur] [res] [ws] → 匹配方案，返回能力标记

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

COMMAND="${1:-}"
shift || true

CACHE_FILE="$(get_cache_file)"

if [[ ! -f "$CACHE_FILE" ]]; then
  echo "ERROR: cache file not found. Run fetch-config.sh first." >&2
  exit 1
fi

# --- 检测可用运行时 ---
RUNTIME=""
if command -v node &>/dev/null; then
  RUNTIME="node"
elif command -v python3 &>/dev/null; then
  RUNTIME="python3"
elif command -v python &>/dev/null; then
  RUNTIME="python"
elif command -v jq &>/dev/null; then
  RUNTIME="jq"
else
  echo "ERROR: 需要 node、python3 或 jq 中的至少一个来解析 JSON。请安装后重试。" >&2
  exit 1
fi

# ============================================================
# Node.js 实现
# ============================================================
run_node() {
  node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('$CACHE_FILE','utf-8')).data;
const cmd = '$COMMAND';
const args = $(printf '%s\n' "$@" | node -e "const l=[];require('readline').createInterface({input:process.stdin}).on('line',v=>l.push(v)).on('close',()=>console.log(JSON.stringify(l)))" 2>/dev/null || echo '[]');

function filterByType(children, type) {
  switch(type) {
    case '文生视频': return children.filter(c => c.prompt >= 1);
    case '图生视频': return children.filter(c => c.single_image >= 1);
    case '首帧': return children.filter(c => c.first_frame >= 1 && (!c.last_frame || c.last_frame === 0));
    case '首尾帧': return children.filter(c => c.first_frame >= 1 && c.last_frame >= 1);
    case '多图参考': return children.filter(c => c.multi_image >= 1);
    case '音频驱动': return children.filter(c => c.audio >= 1);
    case '视频参考': return children.filter(c => c.video >= 1);
    default: return children;
  }
}

function getOptions(children, type) {
  const plans = filterByType(children, type);
  const d=new Set(), r=new Set(), w=new Set();
  plans.forEach(c => {
    (c.duration||[]).forEach(v=>d.add(v));
    (c.resolution||[]).forEach(v=>r.add(v));
    (c.widescreen||[]).forEach(v=>w.add(v));
  });
  return {duration:[...d],resolution:[...r],widescreen:[...w]};
}

if (cmd === 'models') {
  console.log(JSON.stringify(data.map(m => ({model_code:m.model_code, model_name:m.model_name}))));
} else if (cmd === 'model-detail') {
  const model = data.find(m => m.model_code === args[0]);
  if (!model) { console.error('ERROR: model not found'); process.exit(1); }
  const types = {};
  model.children.forEach(c => {
    if (c.prompt >= 1) types['文生视频'] = true;
    if (c.single_image >= 1) types['图生视频'] = true;
    if (c.first_frame >= 1 && c.last_frame >= 1) types['首尾帧'] = true;
    else if (c.first_frame >= 1) types['首帧'] = true;
    if (c.multi_image >= 1) types['多图参考'] = true;
    if (c.audio >= 1) types['音频驱动'] = true;
    if (c.video >= 1) types['视频参考'] = true;
  });
  const typeList = Object.keys(types);
  const optionsPerType = {};
  typeList.forEach(t => { optionsPerType[t] = getOptions(model.children, t); });
  console.log(JSON.stringify({model_code:model.model_code, model_name:model.model_name, types:typeList, options:optionsPerType}));
} else if (cmd === 'match') {
  const model = data.find(m => m.model_code === args[0]);
  if (!model) { console.error('ERROR: model not found'); process.exit(1); }
  const plans = filterByType(model.children, args[1]);
  const matched = plans.find(c => {
    const durOk = !args[2] || (c.duration||[]).includes(String(args[2]));
    const resOk = !args[3] || (c.resolution||[]).includes(String(args[3]));
    const wsOk  = !args[4] || (c.widescreen||[]).includes(String(args[4]));
    return durOk && resOk && wsOk;
  });
  if (!matched) { console.error('ERROR: no matching plan'); process.exit(1); }
  console.log(JSON.stringify({prompt:matched.prompt,first_frame:matched.first_frame,last_frame:matched.last_frame,single_image:matched.single_image,multi_image:matched.multi_image,audio:matched.audio,video:matched.video}));
}
"
}

# ============================================================
# Python 实现
# ============================================================
run_python() {
  local PY="$1"
  $PY -c "
import json, sys

with open('$CACHE_FILE') as f:
    data = json.load(f)['data']

cmd = '$COMMAND'
args = $( printf '['; first=true; for a in "$@"; do $first && first=false || printf ','; printf '\"%s\"' "$a"; done; printf ']' )

def filter_by_type(children, t):
    m = {
        '文生视频': lambda c: c.get('prompt',0) >= 1,
        '图生视频': lambda c: c.get('single_image',0) is not None and c.get('single_image',0) >= 1,
        '首帧': lambda c: c.get('first_frame',0) >= 1 and (not c.get('last_frame') or c.get('last_frame',0) == 0),
        '首尾帧': lambda c: c.get('first_frame',0) >= 1 and c.get('last_frame',0) >= 1,
        '多图参考': lambda c: c.get('multi_image',0) >= 1,
        '音频驱动': lambda c: c.get('audio',0) >= 1,
        '视频参考': lambda c: c.get('video',0) >= 1,
    }
    return [c for c in children if m.get(t, lambda c: True)(c)]

def get_options(children, t):
    plans = filter_by_type(children, t)
    d,r,w = set(),set(),set()
    for c in plans:
        for v in c.get('duration',[]): d.add(v)
        for v in c.get('resolution',[]): r.add(v)
        for v in c.get('widescreen',[]): w.add(v)
    return {'duration':list(d),'resolution':list(r),'widescreen':list(w)}

if cmd == 'models':
    print(json.dumps([{'model_code':m['model_code'],'model_name':m['model_name']} for m in data], ensure_ascii=False))
elif cmd == 'model-detail':
    model = next((m for m in data if m['model_code'] == args[0]), None)
    if not model: print('ERROR: model not found', file=sys.stderr); sys.exit(1)
    types = set()
    for c in model['children']:
        if c.get('prompt',0) >= 1: types.add('文生视频')
        if c.get('single_image') is not None and c.get('single_image',0) >= 1: types.add('图生视频')
        if c.get('first_frame',0) >= 1 and c.get('last_frame',0) >= 1: types.add('首尾帧')
        elif c.get('first_frame',0) >= 1: types.add('首帧')
        if c.get('multi_image',0) >= 1: types.add('多图参考')
        if c.get('audio',0) >= 1: types.add('音频驱动')
        if c.get('video',0) >= 1: types.add('视频参考')
    type_list = list(types)
    options_per_type = {t: get_options(model['children'], t) for t in type_list}
    print(json.dumps({'model_code':model['model_code'],'model_name':model['model_name'],'types':type_list,'options':options_per_type}, ensure_ascii=False))
elif cmd == 'match':
    model = next((m for m in data if m['model_code'] == args[0]), None)
    if not model: print('ERROR: model not found', file=sys.stderr); sys.exit(1)
    plans = filter_by_type(model['children'], args[1])
    dur,res,ws = (args[2] if len(args)>2 else None), (args[3] if len(args)>3 else None), (args[4] if len(args)>4 else None)
    for c in plans:
        dur_ok = not dur or str(dur) in [str(v) for v in c.get('duration',[])]
        res_ok = not res or str(res) in [str(v) for v in c.get('resolution',[])]
        ws_ok  = not ws  or str(ws)  in [str(v) for v in c.get('widescreen',[])]
        if dur_ok and res_ok and ws_ok:
            print(json.dumps({k:c.get(k) for k in ['prompt','first_frame','last_frame','single_image','multi_image','audio','video']}))
            sys.exit(0)
    print('ERROR: no matching plan', file=sys.stderr); sys.exit(1)
"
}

# ============================================================
# jq 实现
# ============================================================
run_jq() {
  local JQ_TYPE_FILTER='
    def type_filter($t):
      if $t == "文生视频" then .prompt >= 1
      elif $t == "图生视频" then (.single_image // 0) >= 1
      elif $t == "首帧" then .first_frame >= 1 and ((.last_frame // 0) == 0)
      elif $t == "首尾帧" then .first_frame >= 1 and (.last_frame // 0) >= 1
      elif $t == "多图参考" then (.multi_image // 0) >= 1
      elif $t == "音频驱动" then (.audio // 0) >= 1
      elif $t == "视频参考" then (.video // 0) >= 1
      else true end;
  '

  case "$COMMAND" in
    models)
      jq -c '[.data[] | {model_code:.model_code, model_name:.model_name}]' "$CACHE_FILE"
      ;;
    model-detail)
      local mkey="$1"
      jq -c --arg mkey "$mkey" "$JQ_TYPE_FILTER"'
        .data[] | select(.model_code == $mkey) |
        . as $m |
        { model_code: .model_code, model_name: .model_name,
          types: [.children[] |
            (if .prompt >= 1 then "文生视频" else empty end),
            (if (.single_image // 0) >= 1 then "图生视频" else empty end),
            (if .first_frame >= 1 and (.last_frame // 0) >= 1 then "首尾帧"
             elif .first_frame >= 1 then "首帧" else empty end),
            (if (.multi_image // 0) >= 1 then "多图参考" else empty end),
            (if (.audio // 0) >= 1 then "音频驱动" else empty end),
            (if (.video // 0) >= 1 then "视频参考" else empty end)
          ] | unique,
          options: (
            [.children[] |
              (if .prompt >= 1 then "文生视频" else empty end),
              (if (.single_image // 0) >= 1 then "图生视频" else empty end),
              (if .first_frame >= 1 and (.last_frame // 0) >= 1 then "首尾帧"
               elif .first_frame >= 1 then "首帧" else empty end),
              (if (.multi_image // 0) >= 1 then "多图参考" else empty end),
              (if (.audio // 0) >= 1 then "音频驱动" else empty end),
              (if (.video // 0) >= 1 then "视频参考" else empty end)
            ] | unique | . as $types |
            reduce $types[] as $t ({}; . + {
              ($t): ($m.children | map(select(type_filter($t))) |
                { duration: [.[].duration[]?] | unique,
                  resolution: [.[].resolution[]?] | unique,
                  widescreen: [.[].widescreen[]?] | unique })
            })
          ) }' "$CACHE_FILE"
      ;;
    match)
      local mkey="$1" type="$2" dur="${3:-}" res="${4:-}" ws="${5:-}"
      jq -c --arg mkey "$mkey" --arg type "$type" --arg dur "$dur" --arg res "$res" --arg ws "$ws" "$JQ_TYPE_FILTER"'
        .data[] | select(.model_code == $mkey) | .children |
        map(select(type_filter($type))) |
        map(select(
          ($dur == "" or ([.duration[]?] | index($dur) != null)) and
          ($res == "" or ([.resolution[]?] | index($res) != null)) and
          ($ws  == "" or ([.widescreen[]?] | index($ws) != null))
        )) |
        first // error("no matching plan") |
        {prompt, first_frame, last_frame, single_image, multi_image, audio, video}' "$CACHE_FILE"
      ;;
    *)
      echo "Usage: bash parse-config.sh <models|model-detail|match> [args...]" >&2
      exit 1
      ;;
  esac
}

# --- 分发到对应运行时 ---
case "$RUNTIME" in
  node)    run_node "$@" ;;
  python3) run_python python3 "$@" ;;
  python)  run_python python "$@" ;;
  jq)      run_jq "$@" ;;
esac
