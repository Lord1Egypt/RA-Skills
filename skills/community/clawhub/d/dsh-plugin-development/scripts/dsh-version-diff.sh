#!/usr/bin/env bash
# dsh-version-diff.sh —— 生成「本 skill 基线 → 你本地源码最新」之间的真实差异。
#
# 它把 dsh-sync.sh 拉下来的源码，变成一份可以直接贴进
# references/13-version-history.md 第 2 节表格的 Markdown 片段。
#
# 覆盖六个「破坏性变更高频维度」（选它们是因为名字级的 API 反而最稳）：
#   ① 官方包增删改名   ② base 补丁插件行增删   ③ base 补丁配置键变动
#   ④ 模型 ID          ⑤ 会话格式版本 SESSION_FORMAT_VERSION
#   ⑥ 参数 DSL / 组合包补丁 文件是否变动
# 另加一个「作者自报」维度：提交标题带 `type(scope)!:` 的破坏性提交（Conventional Commits）。
#   它很便宜，但**覆盖不全**——基线前的 tag 链上只有 7 条，且插件作者最痛的几条
#   （模型 ID 改名、配置键 persona→personaPrefix、官方包移除）恰恰没带 `!`。
#   所以它是补充，不是替代。
#
# 用法：
#   bash dsh-version-diff.sh                       # 用 skill 内的 vendor/dsh-src
#   bash dsh-version-diff.sh <DSH 仓库路径>
#   bash dsh-version-diff.sh <路径> --baseline dsh-v0.2.1-rc.3
#   bash dsh-version-diff.sh <路径> --list-only    # 只列基线之后的新 tag
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
STATE="$SKILL_DIR/vendor/dsh-state.json"

REPO=""
BASELINE="dsh-v0.2.2-alpha.2"
LIST_ONLY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --baseline) BASELINE="${2:-}"; shift ;;
    --list-only) LIST_ONLY=1 ;;
    -h|--help) sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) [ -z "$REPO" ] && REPO="$1" || { echo "多余参数: $1" >&2; exit 2; } ;;
  esac
  shift
done

if [ -z "$REPO" ]; then
  for c in "$SKILL_DIR/vendor/dsh-src" "$SKILL_DIR/vendor/dsh-snapshot"; do
    [ -d "$c" ] && { REPO="$c"; break; }
  done
fi

if [ -z "$REPO" ] || [ ! -d "$REPO" ]; then
  cat >&2 <<'MSG'
ERROR: 找不到 DSH 源码目录。
  先运行： bash scripts/dsh-sync.sh
  或显式传入路径： bash scripts/dsh-version-diff.sh <DSH 仓库路径>
MSG
  exit 2
fi

if ! git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; then
  cat >&2 <<'MSG'
ERROR: 该目录不是 git 仓库，无法做逐区间对比。
  逐区间差异需要 tag 历史。请用 dsh-sync.sh 的默认（git）模式重新拉取，
  而不是 --tarball 或 --shallow。
  （仍可用： bash scripts/dsh-api-probe.sh <该目录> 对单点核验 API。）
MSG
  exit 2
fi

# 基线不在本地时优雅降级
if ! git -C "$REPO" rev-parse -q --verify "$BASELINE^{commit}" >/dev/null 2>&1; then
  echo "⚠ 基线 $BASELINE 不在本地 tag 里。改用首个可用 tag 作为起点。"
  BASELINE=$(git -C "$REPO" for-each-ref --sort=creatordate --format='%(refname:short)' refs/tags | head -1)
  [ -z "$BASELINE" ] && { echo "ERROR: 本地没有任何 tag。" >&2; exit 2; }
  echo "  起点改为：$BASELINE"
  echo
fi

# ── 列举基线之后的新版本 ─────────────────────────────────────────────────────
mapfile -t ALLTAGS < <(git -C "$REPO" tag | sort -V)
NEWTAGS=()
seen=0
for t in "${ALLTAGS[@]}"; do
  if [ "$seen" -eq 1 ]; then NEWTAGS+=("$t"); fi
  [ "$t" = "$BASELINE" ] && seen=1
done
HEADREF=""
HEADLABEL=""

if [ "${#NEWTAGS[@]}" -eq 0 ]; then
  echo "✅ 本地没有晚于基线 $BASELINE 的 tag。"
  echo "   当前 HEAD: $(git -C "$REPO" log -1 --format='%h %ci')"
  echo "   若 HEAD 领先基线，说明新变更尚未打 tag —— 用 --baseline 指定更早的 tag 可看未发布差异。"
  exit 0
fi

echo "基线：$BASELINE"
echo "新增版本（${#NEWTAGS[@]} 个）：${NEWTAGS[*]}"
echo

if [ "$LIST_ONLY" -eq 1 ]; then
  for t in "${NEWTAGS[@]}"; do
    printf '%-24s %s  %s\n' "$t" \
      "$(git -C "$REPO" log -1 --format='%ci' "$t" | cut -d' ' -f1)" \
      "$(git -C "$REPO" rev-parse --short "$t")"
  done
  exit 0
fi

# ── 「未发布」「master」代表谁：必须**严格领先于最后一个 tag** ────────────────
# 🔴 缺陷史（2026-10-24 修）：原实现固定把本地工作树的 HEAD 当 master。
#   主工作树按规程「只 fetch、不改工作树」长期冻结在很久以前的 commit，
#    于是每轮都会多出一行 `rc.N → master (未发布)`，内容却是**反向**差异
#    （包被「移除」上百个、SESSION_FORMAT_VERSION 从 4「退回」3），
#    与真相相反且极易被当成真实的上游破坏性变更照抄。
#   现在：优先 origin/master（远端跟踪分支），其次本地 HEAD；且**必须是最后
#   一个 tag 的严格后代**，否则不输出这一行。
LASTTAG="${NEWTAGS[${#NEWTAGS[@]}-1]}"
for cand in origin/master HEAD; do
  if git -C "$REPO" rev-parse -q --verify "$cand^{commit}" >/dev/null 2>&1 && \
     git -C "$REPO" merge-base --is-ancestor "$LASTTAG^{commit}" "$cand^{commit}" 2>/dev/null && \
     [ "$(git -C "$REPO" rev-parse "$cand^{commit}")" != "$(git -C "$REPO" rev-parse "$LASTTAG^{commit}")" ]; then
    HEADREF="$cand"
    HEADLABEL="$cand（未发布，领先 $LASTTAG）"
    break
  fi
done
if [ -z "$HEADREF" ]; then
  HEADLABEL="无未发布提交"
fi

# ── 五个维度的快照函数 ───────────────────────────────────────────────────────
pkgset() {
  git -C "$REPO" grep -h '"name": *"@deepseek-ai/' "$1" -- 'packages/*/*/package.json' 2>/dev/null \
    | sed 's/.*"\(@deepseek-ai\/[^"]*\)".*/\1/' | sort -u
}
idlist() {
  git -C "$REPO" grep -h -- "- id: " "$1" -- 'packages/bundle/base/cordis.patch.yml' 2>/dev/null \
    | sed 's/.*- id: *//' | tr -d '\r' | sort -u
}
modelof() {
  git -C "$REPO" grep -h "^\s*model:" "$1" -- 'packages/bundle/base/cordis.patch.yml' 2>/dev/null \
    | tr -d ' \r' | sort -u | tr '\n' ',' | sed 's/,$//'
}
# base 补丁里的「插件特有」配置键名集合（缩进键）。
# 用途：发现配置键改名/移除——这是插件作者的高频痛点（如 persona → personaPrefix）。
# 过滤掉 name/config/id/disabled/plugin 这类通用键：它们的增删等价于插件行增删，已由 idlist 覆盖。
configkeys() {
  git -C "$REPO" show "$1:packages/bundle/base/cordis.patch.yml" 2>/dev/null \
    | grep -oE '^[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*:' | tr -d ' :' \
    | grep -vxE 'name|config|id|disabled|plugin' | sort -u || true
}
sfv() {
  git -C "$REPO" grep -h "SESSION_FORMAT_VERSION *=" "$1" -- 'packages/core/session/src/*.ts' 2>/dev/null \
    | head -1 | sed 's/.*= *//' | tr -d '\r'
}
filehash() {
  git -C "$REPO" ls-tree "$1" -- "$2" 2>/dev/null | awk '{print substr($3,1,8)}'
}

# 作者自报的破坏性变更（Conventional Commits 的 `type(scope)!:` 标题标记）。
# 注意：`--grep` 默认基本正则 + 子串匹配，匹配带 scope 的形式用 '!:' 最稳。
banglist() {
  git -C "$REPO" log --format="%h %s" "$1..$2" 2>/dev/null \
    | grep -E ' [a-z]+(\([a-z0-9-]+\))?!:' | head -20 || true
}

emit_delta() {
  local a="$1" b="$2"
  local A B NEW GONE out=""
  A=$(mktemp); B=$(mktemp)

  pkgset "$a" > "$A"; pkgset "$b" > "$B"
  NEW=$(comm -13 "$A" "$B"); GONE=$(comm -23 "$A" "$B")
  if [ -n "$NEW" ]; then out+="  **包新增**："$'\n'; while read -r l; do [ -n "$l" ] && out+="    - \`$l\`"$'\n'; done <<< "$NEW"; fi
  if [ -n "$GONE" ]; then out+="  **包移除/改名**（旧名，需检查是否有替代）："$'\n'; while read -r l; do [ -n "$l" ] && out+="    - \`$l\`"$'\n'; done <<< "$GONE"; fi

  idlist "$a" > "$A"; idlist "$b" > "$B"
  NEW=$(comm -13 "$A" "$B"); GONE=$(comm -23 "$A" "$B")
  if [ -n "$NEW" ]; then out+="  **base 补丁插件行新增**：$(echo "$NEW" | tr '\n' ' ')"$'\n'; fi
  if [ -n "$GONE" ]; then out+="  **base 补丁插件行移除**：$(echo "$GONE" | tr '\n' ' ')"$'\n'; fi

  configkeys "$a" > "$A"; configkeys "$b" > "$B"
  NEW=$(comm -13 "$A" "$B"); GONE=$(comm -23 "$A" "$B")
  if [ -n "$NEW" ] || [ -n "$GONE" ]; then
    out+="  **配置键变动**（base 补丁里的插件特有键名）："$'\n'
    [ -n "$NEW" ]  && out+="    - 新增：$(echo "$NEW" | tr '\n' ' ')"$'\n'
    [ -n "$GONE" ] && out+="    - 移除/改名：$(echo "$GONE" | tr '\n' ' ')"$'\n'
  fi

  local ma mb
  ma=$(modelof "$a"); mb=$(modelof "$b")
  if [ "$ma" != "$mb" ]; then out+="  **模型 ID 变化**：\`$ma\` → \`$mb\`"$'\n'; fi

  local sa sb
  sa=$(sfv "$a"); sb=$(sfv "$b")
  if [ "$sa" != "$sb" ]; then out+="  **会话格式版本**：\`$sa\` → \`$sb\`"$'\n'; fi

  local fa fb
  fa=$(filehash "$a" packages/core/tools/src/schema.ts); fb=$(filehash "$b" packages/core/tools/src/schema.ts)
  [ "$fa" != "$fb" ] && out+="  **参数 DSL 源文件变动**（\`packages/core/tools/src/schema.ts\` \`$fa\` → \`$fb\`）"$'\n'
  fa=$(filehash "$a" packages/core/tools/src/index.ts); fb=$(filehash "$b" packages/core/tools/src/index.ts)
  [ "$fa" != "$fb" ] && out+="  **defineTool 源文件变动**（\`packages/core/tools/src/index.ts\` \`$fa\` → \`$fb\`）"$'\n'
  fa=$(filehash "$a" packages/bundle/base/cordis.patch.yml); fb=$(filehash "$b" packages/bundle/base/cordis.patch.yml)
  [ "$fa" != "$fb" ] && out+="  **base 组合包补丁变动**（\`packages/bundle/base/cordis.patch.yml\` \`$fa\` → \`$fb\`）"$'\n'
  fa=$(filehash "$a" packages/AGENTS.md); fb=$(filehash "$b" packages/AGENTS.md)
  [ "$fa" != "$fb" ] && out+="  **包级开发规范变动**（\`packages/AGENTS.md\`）"$'\n'

  local bang
  bang=$(banglist "$a" "$b" || true)
  if [ -n "$bang" ]; then
    out+="  **作者自报的破坏性变更**（\`type(scope)!:\` 标题标记——注意此路覆盖不全）："$'\n'
    while read -r l; do [ -n "$l" ] && out+="    - \`$l\`"$'\n'; done <<< "$bang"
  fi

  rm -f "$A" "$B"
  printf '%s' "$out"
}

# 决策记录条数（只数英文版，与 references/13-version-history.md 口径一致）
notecount() {
  git -C "$REPO" ls-tree -r --name-only "$1" -- .agents/notes 2>/dev/null \
    | grep -E '\.md$' | grep -vcE '\.zh\.md$'
}

# ── 输出 Markdown 片段 ───────────────────────────────────────────────────────
echo "────────────────────────────────────────────────────────────"
echo "以下片段可直接追加到 references/13-version-history.md 第 2 节表格末尾"
echo "────────────────────────────────────────────────────────────"
echo
echo "<!-- 自动生成 $(date -u +%Y-%m-%dT%H:%M:%SZ) · 基于 $(git -C "$REPO" rev-parse --short "${HEADREF:-HEAD}") -->"
echo
echo '| 区间 | 破坏性变更 | 证据 |'
echo '|---|---|---|'

PREV="$BASELINE"
for t in "${NEWTAGS[@]}" $HEADREF; do
  if [ -n "$HEADREF" ] && [ "$t" = "$HEADREF" ]; then
    label="$HEADLABEL"
  else
    label="$t"
  fi
  delta=$(emit_delta "$PREV" "$t")
  na=$(notecount "$PREV"); nb=$(notecount "$t")
  if [ -z "$delta" ]; then
    echo "| $PREV → $label | 未检出上述五维度变化（决策记录条数：$na → $nb） | \`bash scripts/dsh-version-diff.sh\` |"
  else
    # 表格内换行用 <br>，避免撑破表格
    flat=$(printf '%s' "$delta" | sed 's/  \*\*/<br>**/g; s/^<br>//' | tr '\n' ' ' | sed 's/  */ /g; s/|/\\|/g')
    echo "| $PREV → $label | $flat （决策记录条数：$na → $nb） | \`bash scripts/dsh-version-diff.sh\` |"
  fi
  PREV="$t"
done

echo
echo "────────────────────────────────────────────────────────────"
echo "提示："
echo "  · 本片段覆盖六个高破坏性维度 + 作者自报的 \`!:\` 标记提交，不是「全部变更」。"
echo "  · \`!:\` 那一路**覆盖不全**：它抓不到模型 ID / 配置键改名 / 官方包移除。"
echo "  · 「配置键变动」报的是 base 补丁里的插件特有键；键改名往往意味着你的配置也会失效。"
echo "  · 检出变化后，务必人工确认是否影响你的插件（有些包增删与插件开发无关）。"
echo "  · 请同步更新 references/13-version-history.md 里第 1 节的 tag 总表。"
echo "  · 更新完再跑一次： bash scripts/dsh-api-probe.sh \"$REPO\""
