#!/usr/bin/env bash
# 本地门禁 = .github/workflows/ci.yml 的等价实现。
# 本地结果是唯一验收依据（曾因 Actions 计费停摆全红；现已转 public，但门禁仍以本地为准）。
#
# Usage:
#   bash scripts/gate.sh            # 只跑静态门禁（离线可跑）
#   bash scripts/gate.sh --smoke    # 额外对每个后端实跑一次（需要网络）
#
# 与 ci.yml 的对应关系：脚本语法 / JSON 合法 / SKILL.md metadata.version / 密钥不入库 /
# workflow 与 action 的 YAML 可解析。
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
rc=0
ok() { printf '  \033[32mok\033[0m   %s\n' "$1"; }
warn() { printf '  \033[33mwarn\033[0m %s\n' "$1"; }
no() { printf '  \033[31mFAIL\033[0m %s\n' "$1"; rc=1; }

# 本机 `python3` 可能是 Microsoft Store 别名存根（exit 0 但无输出），必须验证真实输出。
py=""
for cand in "${PYTHON:-}" python3 python; do
  [ -n "$cand" ] || continue
  if [ "$("$cand" -c 'print(1)' 2>/dev/null)" = "1" ]; then py="$cand"; break; fi
done
if [ -n "$py" ]; then ok "python 解释器: $py"; else no "找不到可用的 python3/python（设 PYTHON=/path/to/python）"; fi

echo "[1/5] 脚本语法"
node --check scripts/search.mjs && ok "node --check scripts/search.mjs" || no "node --check scripts/search.mjs"
bash -n scripts/search.sh && ok "bash -n scripts/search.sh" || no "bash -n scripts/search.sh"

echo "[2/5] JSON 合法"
for f in evals/evals.json secrets.example.json; do
  if "$py" -c 'import json,sys;json.load(sys.stdin)' < "$f" 2>/dev/null; then ok "$f"; else no "$f"; fi
done

echo "[3/5] SKILL.md metadata.version"
if "$py" -c '
import re,sys
t=open("SKILL.md",encoding="utf-8").read()
m=re.search(r"^metadata:\s*$\n\s+version:\s*\"(\d+\.\d+\.\d+)\"", t, re.M)
if not m: sys.exit("SKILL.md frontmatter 缺少 metadata.version")
print("   metadata.version =", m.group(1))
'; then ok "metadata.version 存在"; else no "metadata.version 缺失"; fi

echo "[4/5] 密钥不入库"
if git ls-files --error-unmatch secrets.json >/dev/null 2>&1; then
  no "secrets.json 被 git 跟踪了"
else
  ok "secrets.json 未被跟踪"
fi
if "$py" -c '
import json,sys
d=json.load(open("secrets.example.json",encoding="utf-8"))
filled=[k for k,v in d.items() if v]
sys.exit("secrets.example.json 存在非空值: "+", ".join(filled)) if filled else None
'; then ok "secrets.example.json 全为空值"; else no "secrets.example.json 有非空值"; fi

echo "[5/5] workflow 与 action 的 YAML 可解析"
# 缩进错一个空格在 GH 上要等一轮才知道；本地解析能在 push 前抓住。
if "$py" -c 'import yaml' 2>/dev/null; then
  if "$py" - <<'PY'
import glob, sys
import yaml

files = sorted(glob.glob(".github/workflows/*.yml") + glob.glob(".github/actions/*/action.yml"))
bad = 0
for f in files:
    try:
        d = yaml.safe_load(open(f, encoding="utf-8"))
    except Exception as e:
        print("   FAIL %s: %s: %s" % (f, type(e).__name__, e))
        bad = 1
        continue
    if f.endswith("action.yml"):
        steps = d.get("runs", {}).get("steps", [])
        missing = [s.get("name", "<unnamed>") for s in steps if "shell" not in s]
        if missing:
            print("   FAIL %s: composite step 缺 shell: %s" % (f, ", ".join(missing)))
            bad = 1
            continue
    print("   ok   %s" % f)
sys.exit(bad)
PY
  then ok "workflow / action YAML 合法"; else no "workflow / action YAML 非法"; fi
else
  warn "PyYAML 缺失，跳过 YAML 校验（pip install pyyaml 可启用）"
fi

if [ "${1:-}" = "--smoke" ]; then
  echo "[smoke] 每个后端实跑一次（search.mjs）"
  for b in bing context7 qqnews hupu so github hn zhihu tencent; do
    out=$(node scripts/search.mjs "$b" "rust async" --limit 2 2>&1)
    n=$("$py" -c 'import json,sys
try: d=json.load(sys.stdin)
except Exception: print("unparseable"); raise SystemExit
errs="; ".join(e.get("backend","")+": "+str(e.get("error","")) for e in d.get("errors",[]))
print("%d results%s" % (len(d.get("results",[])), ("  ["+errs+"]") if errs else ""))' <<< "$out")
    case "$n" in
      0\ results*)
        # 已知可容忍的外部限制不该让门禁变红：未认证限流、缺 key、未配置。
        case "$n" in
          *rate-limited*|*missing\ key*|*not\ configured*|*not\ found*)
            warn "$b: $n（外部限制，不计入失败）" ;;
          *) no "$b: $n" ;;
        esac ;;
      *) ok "$b: $n" ;;
    esac
  done
fi

echo
if [ "$rc" -eq 0 ]; then printf '\033[32m门禁通过\033[0m\n'; else printf '\033[31m门禁未通过\033[0m\n'; fi
exit "$rc"
