#!/usr/bin/env bash
# dsh-tag-matrix.sh —— 对 DSH 仓库的所有 tag（含 HEAD）跑「API 面快照」矩阵。
#
# 目的：机器化地算出「哪个 tag 让哪条 API 断言翻转」，从而得出破坏性变更清单。
# 不依赖 CHANGELOG（DSH 没有），也不依赖任何提交信息标记 ——
# 只用「符号在当前源码树里存不存在」这个客观事实。
#
# 用法：
#   bash dsh-tag-matrix.sh <DSH 仓库路径> [输出文件]
#   默认输出到 stdout（TSV），便于再加工。
set -uo pipefail

REPO="${1:-.}"
OUT="${2:-}"

if [ -z "$REPO" ] || [ ! -d "$REPO" ]; then
  echo "ERROR: 找不到仓库路径: $REPO" >&2; exit 2
fi
if ! git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; then
  echo "ERROR: $REPO 不是 git 仓库（版本矩阵需要完整 tag 历史，源码快照不够）" >&2; exit 2
fi

# ── 断言表 ───────────────────────────────────────────────────────────────────
# 格式: ID<TAB>级别<TAB>描述<TAB>kind<TAB>payload<TAB>scope
#   kind=g : payload 是 ERE，在 scope 里用 git grep 找
#   kind=f : payload 是文件/目录相对 scope 的路径，用 git ls-tree 找
#   kind=n : 计数型，payload 是 git ls-tree 的过滤（统计匹配文件数）
# 级别: S=结构性公理 M=接口名 V=实现细节（V 级只做参考，不判定破坏性）
#
# 选条原则：只收「一旦消失/改名就会让插件作者代码写错」的事实。
# 故意不收枚举类（命令清单、插槽总数）——那些天天变，收了会淹没真信号。
CHECKS=$(cat <<'EOF'
A01	M	服务类用 extends Service	g	extends Service	packages
A02	M	服务插件用默认导出类	g	^export default class	packages
A03	M	defineTool 具名导出	g	export (function|const) defineTool	packages
A04	M	参数 DSL 支持属性级 required	g	required\?: true	packages
A05	M	生命周期 ctx.effect	g	ctx\.effect\(	packages
A06	M	可选服务取用 ctx.get	g	ctx\.get\(	packages
A07	M	UI 插槽 slots.register	g	slots\.register\(	packages
A08	M	UI 插槽 slots.inject	g	slots\.inject\(	packages
A09	M	设置卡片 settings.section	g	settings\.section	packages
A10	M	斜杠命令 commands.register	g	commands\.register\(	packages
A11	M	清单字段 dsh.bundle	g	dsh\.bundle	.
A12	M	清单字段 dsh.client	g	dsh\.client	.
A13	M	事件 agent/pre-step	g	agent/pre-step	packages
A14	M	事件 agent/turn-stopping	g	agent/turn-stopping	packages
A15	M	事件 system-prompt/assemble	g	system-prompt/assemble	packages
A16	M	事件 approval/request	g	approval/request	packages
A17	M	事件 llm/stream	g	llm/stream	packages
A18	M	插槽 tool.call.toolview	g	tool\.call\.toolview	packages
A19	M	插槽 conversation.view	g	conversation\.view	packages
A20	M	内置工具 run_code	g	run_code	packages
A21	M	环境白名单 SENSITIVE_ENV_PATTERN	g	SENSITIVE_ENV_PATTERN	packages
A22	V	DSH_HOME 解析 dshHomePath	g	dshHomePath	packages
A23	V	调试开关 --dump-config	g	\-\-dump-config	.
A24	V	会话格式版本常量	g	SESSION_FORMAT_VERSION	packages
A25	S	包级开发规范 packages/AGENTS.md	f	packages/AGENTS.md
A26	M	决策记录机制 .agents/notes	f	.agents/notes
A27	M	供应商 rescope 映射表	f	docs/rescope.md
A28	V	官方文档 docs/	f	docs
A29	M	复盘子目录 docs/postmortem	f	docs/postmortem
A30	V	官方包数量	n	packages
EOF
)

# ── 版本序列 ─────────────────────────────────────────────────────────────────
mapfile -t REFS < <(git -C "$REPO" for-each-ref --sort=creatordate --format='%(refname:short)' refs/tags)
REFS+=("HEAD")

# ── 逐版本核验 ───────────────────────────────────────────────────────────────
emit() {
  if [ -n "$OUT" ]; then printf '%s\n' "$*" >> "$OUT"; else printf '%s\n' "$*"; fi
}
: > "${OUT:-/dev/null}" 2>/dev/null || true

emit "ID	LEVEL	DESC	$(printf '%s	' "${REFS[@]}")"

while IFS=$'\t' read -r id level desc kind payload scope; do
  [ -z "${id:-}" ] && continue
  [ -z "${scope:-}" ] && scope="."
  row="$id	$level	$desc"
  for ref in "${REFS[@]}"; do
    case "$kind" in
      g)
        if git -C "$REPO" grep -qE -- "$payload" "$ref" -- "$scope" 2>/dev/null; then cell="Y"; else cell="."; fi ;;
      f)
        if git -C "$REPO" ls-tree -r --name-only "$ref" -- "$payload" 2>/dev/null | grep -q .; then cell="Y"; else cell="."; fi ;;
      n)
        c=$(git -C "$REPO" ls-tree -r --name-only "$ref" -- packages 2>/dev/null | grep -c "/package\.json$")
        cell="$c" ;;
      *) cell="?" ;;
    esac
    row="$row	$cell"
  done
  emit "$row"
done <<< "$CHECKS"

emit ""
emit "# 版本日期"
emit "TAG	DATE	COMMIT"
for ref in "${REFS[@]}"; do
  d=$(git -C "$REPO" log -1 --format='%ci' "$ref" 2>/dev/null | cut -d' ' -f1)
  c=$(git -C "$REPO" rev-parse --short "$ref" 2>/dev/null)
  emit "$ref	$d	$c"
done
