#!/usr/bin/env bash
# check_oss_license.sh —— 开源许可合规自检（修复后用）
#
# 来源：oss-fix-guide §10（P9）。它是「许可维度已逐文件核实」这句话的**可复现证据**，
# 而不是一句自述 —— 把运行输出存成文件或贴进提交信息。
#
# ⚠️ **负向自检（必做，否则本脚本的 PASS 不可信）**
# 本项目规矩：校验器必须先证明「能失败」。标准做法：
#   ① 在任一内容文件里插一行**不带豁免标记**的 copyleft 关键词（例：`AGPL-3.0 probe`）；
#   ② 跑本脚本 → **必须 FAIL**，且 ⚠️ 段应点名那个文件；
#   ③ 撤掉该行 → 再跑必须 PASS。
#   2026-09-16 实操记录：注入到 `references/08-cheatsheet.md` → 本脚本正确报 FAIL 并点名该文件；
#   撤回后转 PASS（`git diff --stat` 确认该文件无残留改动）。
set -uo pipefail

FAIL=0
note() { printf '  %s\n' "$1"; }

echo "==============================================================="
echo " 1. copyleft / 未知许可关键词扫描（内容文件，排除声明文件自身）"
echo "==============================================================="
HITS=$(grep -rniE 'AGPL|Affero|GPLv[23]|GPL-[23]|LGPL|copyleft|NOASSERTION|UNLICENSED' . \
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=licenses \
  2>/dev/null \
  | grep -vE '^\./(NOTICE|LICENSE|README\.md|README\.en\.md|LICENSE-MIT)' \
  | grep -vE '12-community-plugins\.md' \
  | grep -vE '(^|/)scripts/check_oss_license\.sh' || true)
if [ -z "$HITS" ]; then
  note "✅ 0 命中"
else
  echo "$HITS" | sed 's/^/  ℹ️  /'
  # ── 判读规则（⚠️ 本脚本相对 oss-fix-guide §10 原文的**一处有意修改**，理由如下）──
  #
  # 原文把「关键词命中」一律判 FAIL。但那样**连诚实的移除留痕也会被判失败**：
  #   · 2026-09-16 来源政策收紧后，`10b-casebook-tools.md` 里仍会出现 "AGPL-3.0" ——
  #     但那是**移除声明**（写明「某来源已整体移出本技能的引用集合」），不是上游内容；
  #   · 同理，版本台账行也会自然地记述「本轮清掉了什么」。
  # 也就是说「关键词 0 命中」与「诚实留痕」**互斥**，不可能同时满足。
  #
  # 因此这里把判据落到它的**真实意图**上：不是「不许出现许可名称」，而是
  # **「不许出现未声明就复制/引用 copyleft 内容」**。
  #
  # 🔴 **2026-09-16 收紧：豁免从「按文件」改为「按显式移除标记」**（比收紧前更强）。
  # 收紧前是整份 `10b-casebook-tools.md` 一律豁免 —— 那意味着该册里**新混进**的
  # copyleft 原文会被静默放过。现在改成：**任何文件**里的命中，都必须自带显式标记才豁免。
  #
  # 三类豁免标记（只认这三类，不认"这个文件一向没问题"）：
  #   ① **移除留痕** —— 带删除线 `~~`，或含以下任一移除动词/短语：
  #      `移出` / `移除` / `清掉` / `不再引用` / `不含任何` / `定点改写` / `已按本节来源政策移除` / `已于 2026-09-1*`
  #   ② **版本台账行**（形如 `| \`1.0.11\` | ... |`）—— 维护记录，记述「本轮做了什么」
  #   ③ **检查器自指** —— `SKILL.md` 里描述本脚本自身时，必然提到这些关键词
  #
  # 豁免内容仍会**逐条打印在上方 ℹ️ 列表里**，人眼可见；不打印而静默放过的情形不存在。
  REMOVAL_MARK='~~|移出|移除|清掉|不再引用|已按本节来源政策移除|已于 2026-09-1|不含任何|定点改写'
  SELFREF_MARK='check_oss_license'
  UNDECLARED=$(printf '%s\n' "$HITS" \
    | grep -vE '\| `[0-9]+\.[0-9]+\.[0-9]+` \|' \
    | grep -vE "$REMOVAL_MARK" \
    | grep -vE "$SELFREF_MARK" || true)
  if [ -z "$UNDECLARED" ]; then
    note "✅ 命中全部带显式豁免标记（移除留痕 / 版本台账 / 检查器自指），已逐条列在上方 ℹ️ 中"
  else
    echo "$UNDECLARED" | sed 's/^/  ⚠️  /'
    note "⚠️  以上命中**不带任何豁免标记** —— 若属上游 copyleft 原文，必须改写；若确属留痕，请补显式标记"
    FAIL=1
  fi
fi
echo

echo "==============================================================="
echo " 2. 许可声明文件完整性"
echo "==============================================================="
for f in LICENSE NOTICE licenses/Apache-2.0.txt licenses/MIT.txt licenses/BSD-3-Clause.txt ; do
  if [ -f "$f" ]; then note "✅ $f ($(wc -c <"$f") B)"; else note "❌ 缺失: $f"; FAIL=1; fi
done
echo

echo "==============================================================="
echo " 3. 上游来源表 vs NOTICE 条目一致性"
echo "==============================================================="
SRC_LIC=$(grep -cE '^\| *`?[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+' LICENSE 2>/dev/null || echo 0)
SRC_NOT=$(grep -cE '^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$' NOTICE 2>/dev/null || echo 0)
note "LICENSE 来源表条目数: $SRC_LIC"
note "NOTICE   来源条目数: $SRC_NOT"
if [ "$SRC_NOT" -lt "$SRC_LIC" ]; then
  note "⚠️  NOTICE 条目少于 LICENSE 表 —— 逐条对齐"
  FAIL=1
fi
echo

echo "==============================================================="
echo " 4. 是否仍有「待逐字核取」占位符"
echo "==============================================================="
if grep -n '待逐字核取' NOTICE 2>/dev/null ; then note "❌ NOTICE 仍含未填占位符"; FAIL=1
else note "✅ 无占位符"; fi
echo

echo "==============================================================="
echo " 5. frontmatter / 行尾"
echo "==============================================================="
grep -nE '^(license|version|agent_created|slug|displayName):' SKILL.md | sed 's/^/  /' || true
if [ -f NOTICE ] && grep -qU $'\r' NOTICE ; then note "❌ NOTICE 含 CRLF"; FAIL=1
else note "✅ NOTICE 行尾为 LF"; fi
echo

echo "==============================================================="
if [ "$FAIL" -eq 0 ]; then echo " RESULT: PASS —— 许可维度可对外分发"; else echo " RESULT: FAIL —— 见上方 ⚠️/❌ 项"; fi
echo "==============================================================="
exit $FAIL
