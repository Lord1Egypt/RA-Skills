#!/usr/bin/env bash
# 列出本机已安装的 aikey 家族 skill：名字 + description 第一行 + 真源路径。
# 只读，不改任何东西。给 /aikey 模式 A 做候选发现用。
#   --handoff  另外打印每个技能正文里的「## 接手与交出」一节（模式 B 推下一步用）
PREFIX="${SKILL_PREFIX:-aikey}"   # 技能族前缀，改名时改这里
HANDOFF=0
[ "${1:-}" = "--handoff" ] && HANDOFF=1

set -uo pipefail

# 优先按已安装位置找（宿主实际加载的就是这里），找不到再回退到仓库
ROOTS=("$HOME/.claude/skills" "$HOME/.agents/skills" "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)")

found=0
for root in "${ROOTS[@]}"; do
  [ -d "$root" ] || continue
  for d in "$root"/"$PREFIX"*/ $(for a in ${SKILL_ALIASES:-key}; do [ -d "$root/$a" ] && echo "$root/$a/"; done); do
    [ -f "$d/SKILL.md" ] || continue
    name=$(basename "${d%/}")
    [ "$name" = "$PREFIX" ] && continue          # 排除入口自己
    real=$(cd "$d" && pwd -P)
    # description: frontmatter 里 description 之后、下一个顶格 key 之前的首个非空行
    desc=$(awk '/^description:/{f=1;sub(/^description:[[:space:]]*\|?[[:space:]]*/,"");if($0!="")
{print;exit}next} f&&/^[a-zA-Z_-]+:/{exit} f&&NF{print;exit}' "$d/SKILL.md")
    printf '%-20s %s\n' "$name" "${desc:-（无 description）}"
    printf '%-20s   ↳ %s\n' "" "$real"
    if [ "$HANDOFF" -eq 1 ]; then
      # The section runs from its heading to the next "## " heading (exclusive).
      if grep -q '^## 接手与交出' "$d/SKILL.md"; then
        awk '/^## 接手与交出/{f=1;next} f&&/^## /{exit} f&&NF{print "                       " $0}' "$d/SKILL.md"
      else
        echo "                       （无「接手与交出」，版本可能过旧）"
      fi
    fi
    found=$((found+1))
  done
  [ "$found" -gt 0 ] && break
done

# Same-name copies in more than one root: the host may load a different copy
# than the one being edited. Report it; never pick one silently.
dups=""
for name in $(for r in "${ROOTS[@]}"; do [ -d "$r" ] && ls -1 "$r" 2>/dev/null | grep -E "^${PREFIX}(-|$)"; done | sort | uniq -d); do
  reals=$(for r in "${ROOTS[@]}"; do [ -f "$r/$name/SKILL.md" ] && (cd "$r/$name" && pwd -P); done | sort -u)
  [ "$(printf '%s\n' "$reals" | grep -c .)" -gt 1 ] && dups="$dups $name"
done
if [ -n "$dups" ]; then
  echo "⚠️ 同名技能在多处各有一份不同的副本：$dups —— 宿主加载的未必是你改的那份，先确认再继续" >&2
fi

if [ "$found" -eq 0 ]; then
  echo "（没有发现任何已安装的 $PREFIX 家族 skill）" >&2
  exit 1
fi
echo
echo "共 $found 个"
