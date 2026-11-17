#!/usr/bin/env bash
# run_fixtures.sh — 离线五档 runner（零网络、零计费、产物只落临时目录跑完即删）
#
# 档① 机检自测：好样须过、七枚坏样须各发它该发的那一道、钉阈三形、反证四档、本域四形、临时根自清
# 档② 好样与七枚坏样逐枚单跑：每枚报它自己的退码与码集，不并成一个总数
# 档③ 零通道骨架：make_outline.py 把 sources.jsonl 排成待填骨架
# 档④ 骨架过机检：期望发 E-FORMAT——集中度一句话仍是占位，骨架不该被当成台账交付
# 档⑤ 边界形逐枚单跑：口径写招股书→道五点名／口径写产业链→道五点名／口径值认不出→形制红／
#      判断词必红／事实陈述不误红／改数词必红／匿名客户具名必红／占比大于合计必红
#
# 末行自报「档数=N（由上面逐档现报）｜不合=N｜不可判=N」——档数现算，不写死。
# 退码：0 全合期望；1 有不合；3 取值域故障（脚本或夹具取不到，不读成「零违例」）。

set -u
cd "$(dirname "$0")/../.." || exit 3

PY=python3
CHECK="$PY -B scripts/check_concentration.py"
MAKE="$PY -B scripts/make_outline.py"
FX=scripts/fixtures
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

bad=0
unk=0
tiers=0

run_one() {  # run_one <期望退码> <文件> <标签>
  local want="$1" f="$2" tag="$3" out rc
  out="$($CHECK "$f" 2>&1)"; rc=$?
  if [ "$rc" -eq 3 ]; then
    echo "  不可判 $tag：机检取值域故障（rc=3）"
    unk=$((unk + 1)); return
  fi
  if [ "$rc" -ne "$want" ]; then
    echo "  不合 $tag：期望退码 $want，实发 $rc"
    echo "$out" | sed 's/^/      /'
    bad=$((bad + 1)); return
  fi
  local codes
  codes="$(echo "$out" | grep -o 'E-[A-Z]*' | sort -u | tr '\n' ' ')"
  echo "  ok   $tag（退码 $rc${codes:+·码集 $codes}）"
}

edge() {  # edge <标签> <期望退码> <文件> <须含的独有句|-> <须不含的独有句|->
  local tag="$1" want="$2" f="$3" must="$4" mustnot="$5" out rc
  out="$($CHECK "$f" 2>&1)"; rc=$?
  if [ "$rc" -eq 3 ]; then
    echo "  不可判 $tag：机检取值域故障（rc=3）"
    unk=$((unk + 1)); return
  fi
  if [ "$rc" -ne "$want" ]; then
    echo "  不合 $tag：期望退码 $want，实发 $rc"
    echo "$out" | sed 's/^/      /'
    bad=$((bad + 1)); return
  fi
  if [ "$must" != "-" ] && ! echo "$out" | grep -qF "$must"; then
    echo "  不合 $tag：期望详行含「$must」，实发不含"
    bad=$((bad + 1)); return
  fi
  if [ "$mustnot" != "-" ] && echo "$out" | grep -qF "$mustnot"; then
    echo "  不合 $tag：期望详行不含「$mustnot」，实发含"
    bad=$((bad + 1)); return
  fi
  echo "  ok   $tag（退码 $rc）"
}

echo '档① 机检自测'
tiers=$((tiers + 1))
if ! $CHECK --selftest > "$TMP/st.log" 2>&1; then
  echo '  不合 机检自测未全绿'
  sed 's/^/      /' "$TMP/st.log"
  bad=$((bad + 1))
else
  echo "  ok   机检自测全绿（$(grep -c '^  ok' "$TMP/st.log") 项）"
fi

echo '档② 好样与七枚坏样逐枚单跑'
tiers=$((tiers + 1))
run_one 0 "$FX/good-concentration.md" '好样 good-concentration'
run_one 1 "$FX/bad-no-anchor.md" '坏样 bad-no-anchor（道二 锚）'
run_one 1 "$FX/bad-missing-section.md" '坏样 bad-missing-section（道一 形制）'
run_one 1 "$FX/bad-rating-word.md" '坏样 bad-rating-word（道三 红线）'
run_one 1 "$FX/bad-gap-unlisted.md" '坏样 bad-gap-unlisted（道四 未取到）'
run_one 1 "$FX/bad-scope-prospectus.md" '坏样 bad-scope-prospectus（道五 边界）'
run_one 1 "$FX/bad-anon-named.md" '坏样 bad-anon-named（道一 匿名客户）'
run_one 1 "$FX/bad-sum-exceeds.md" '坏样 bad-sum-exceeds（道一 占比自洽）'

echo '档③ 零通道骨架'
tiers=$((tiers + 1))
if ! $MAKE --sources "$FX/sources.jsonl" --out "$TMP/sk.md" --subject 示例公司 --window 2026-11-09 > "$TMP/mk.log" 2>&1; then
  echo '  不合 骨架未出'
  sed 's/^/      /' "$TMP/mk.log"
  bad=$((bad + 1))
else
  echo "  ok   骨架已出（$(grep -c '^- \[S' "$TMP/sk.md") 条来源行）"
fi

echo '档④ 骨架过机检：期望红在集中度一句话占位那一行'
tiers=$((tiers + 1))
edge '骨架该红就红（E-FORMAT·集中度一句话占位）' 1 "$TMP/sk.md" '集中度一句话仍是占位' 'E-COVERAGE'

echo '档⑤ 边界形逐枚单跑'
tiers=$((tiers + 1))
sed 's/^集中度口径：客户依赖（收入来自哪些客户、占比多少、跨期怎么变；不判客户质量、不判风险大小）$/集中度口径：招股书（读一份招股说明书，把八项逐字摘成速览卡）/' \
  "$FX/good-concentration.md" > "$TMP/e-prospectus.md"
edge '口径写招股书→道五点名改走 prospectus-digest-cn' 1 "$TMP/e-prospectus.md" 'prospectus-digest-cn' '-'

sed 's/^集中度口径：客户依赖（收入来自哪些客户、占比多少、跨期怎么变；不判客户质量、不判风险大小）$/集中度口径：产业链（谁在哪个环节、上下游关系）/' \
  "$FX/good-concentration.md" > "$TMP/e-chain.md"
edge '口径写产业链→道五点名改走 cn-supply-chain-map' 1 "$TMP/e-chain.md" 'cn-supply-chain-map' '-'

sed 's/^集中度口径：客户依赖（收入来自哪些客户、占比多少、跨期怎么变；不判客户质量、不判风险大小）$/集中度口径：看情况/' \
  "$FX/good-concentration.md" > "$TMP/e-unknown.md"
edge '口径值认不出→形制红' 1 "$TMP/e-unknown.md" '集中度口径' '-'

sed 's/^- 2024 年度与第二大客户签订框架采购协议，协议期限三年，年报未披露协议金额 \[S1\]$/- 2024 年度与第二大客户签订框架采购协议，协议期限三年，年报未披露协议金额 [S1]\n- 客户结构风险可控，第一大客户为优质客户 [S1]/' \
  "$FX/good-concentration.md" > "$TMP/e-judge.md"
edge '判断词「风险可控／优质客户」必红' 1 "$TMP/e-judge.md" '风险可控' '-'

sed 's/^- 2024 年度与第二大客户签订框架采购协议，协议期限三年，年报未披露协议金额 \[S1\]$/- 2024 年度与第二大客户签订框架采购协议，协议期限三年，年报未披露协议金额 [S1]\n- 公司对前五大客户存在一定依赖，该表述为年报原文 [S1]/' \
  "$FX/good-concentration.md" > "$TMP/e-fact.md"
edge '事实陈述「存在一定依赖」不误红' 0 "$TMP/e-fact.md" '-' 'E-BANWORD'

sed 's/｜占比：27.85%/｜占比：约 27.85%/' "$FX/good-concentration.md" > "$TMP/e-hedge.md"
edge '改数词「约」必红' 1 "$TMP/e-hedge.md" '改数词' '-'

sed 's/客户一（披露未具名）/客户一（华为技术有限公司）/' "$FX/good-concentration.md" > "$TMP/e-anon.md"
edge '匿名客户被具名必红' 1 "$TMP/e-anon.md" '披露没点名' '-'

sed 's/｜占比：27.85%/｜占比：77.85%/' "$FX/good-concentration.md" > "$TMP/e-sum.md"
edge '单客户占比大于合计必红' 1 "$TMP/e-sum.md" '明细不得大于合计' '-'

echo "档数=$tiers（由上面逐档现报）｜不合=$bad｜不可判=$unk"
[ "$unk" -gt 0 ] && exit 3
[ "$bad" -gt 0 ] && exit 1
exit 0
