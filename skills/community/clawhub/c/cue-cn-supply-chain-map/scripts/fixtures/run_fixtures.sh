#!/usr/bin/env bash
# run_fixtures.sh — 离线五档 runner（零网络、零计费、产物只落临时目录跑完即删）
#
# 档① 机检自测：好样须过、六枚坏样须各发它该发的那一道、钉阈三形、反证四档、本域两形、临时根自清
# 档② 好样与六枚坏样逐枚单跑：每枚报它自己的退码与码集，不并成一个总数
# 档③ 零通道骨架：make_outline.py 把 sources.jsonl 排成待填骨架
# 档④ 骨架过机检：期望发 E-FORMAT——链条一句话仍是占位，骨架不该被当成图谱交付
# 档⑤ 边界形逐枚单跑：链条口径写景气→道五点名／口径值认不出→形制红／推荐词必红／
#      事实陈述不误红／改数词必红／「代表公司：未取到」这一形不误红
#
# 末行自报「档数=5｜不合=N｜不可判=N」。
# 退码：0 全合期望；1 有不合；3 取值域故障（脚本或夹具取不到，不读成「零违例」）。

set -u
cd "$(dirname "$0")/../.." || exit 3

PY=python3
CHECK="$PY -B scripts/check_chain.py"
MAKE="$PY -B scripts/make_outline.py"
FX=scripts/fixtures
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

bad=0
unk=0

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
if ! $CHECK --selftest > "$TMP/st.log" 2>&1; then
  echo '  不合 机检自测未全绿'
  sed 's/^/      /' "$TMP/st.log"
  bad=$((bad + 1))
else
  echo "  ok   机检自测全绿（$(grep -c '^  ok' "$TMP/st.log") 项）"
fi

echo '档② 好样与六枚坏样逐枚单跑'
run_one 0 "$FX/good-chain.md" '好样 good-chain'
run_one 1 "$FX/bad-no-anchor.md" '坏样 bad-no-anchor（道二 锚）'
run_one 1 "$FX/bad-missing-section.md" '坏样 bad-missing-section（道一 形制）'
run_one 1 "$FX/bad-rating-word.md" '坏样 bad-rating-word（道三 红线）'
run_one 1 "$FX/bad-gap-unlisted.md" '坏样 bad-gap-unlisted（道四 未取到）'
run_one 1 "$FX/bad-industry-boom.md" '坏样 bad-industry-boom（道五 边界）'
run_one 1 "$FX/bad-no-position.md" '坏样 bad-no-position（道一 位置）'

echo '档③ 零通道骨架'
if ! $MAKE --sources "$FX/sources.jsonl" --out "$TMP/sk.md" --subject 光伏组件 --window 2026-11-08 > "$TMP/mk.log" 2>&1; then
  echo '  不合 骨架未出'
  sed 's/^/      /' "$TMP/mk.log"
  bad=$((bad + 1))
else
  echo "  ok   骨架已出（$(grep -c '^- \[S' "$TMP/sk.md") 条来源行）"
fi

echo '档④ 骨架过机检：期望红在链条一句话占位那一行'
edge '骨架该红就红（E-FORMAT·链条一句话占位）' 1 "$TMP/sk.md" '链条一句话仍是占位' 'E-COVERAGE'

echo '档⑤ 边界形逐枚单跑'
sed 's/^链条口径：结构（谁在哪个环节、上下游关系；不判景气、不判好坏）$/链条口径：景气（这个行业的量价与格局）/' \
  "$FX/good-chain.md" > "$TMP/e-boom.md"
edge '口径写景气→道五点名改走 sector-overview' 1 "$TMP/e-boom.md" 'sector-overview' '-'

sed 's/^链条口径：结构（谁在哪个环节、上下游关系；不判景气、不判好坏）$/链条口径：看情况/' \
  "$FX/good-chain.md" > "$TMP/e-unknown.md"
edge '口径值认不出→形制红' 1 "$TMP/e-unknown.md" '链条口径' '-'

sed 's/^- 环节：组件封装｜代表公司：隆基绿能（组件制造与出货，位于电池片下游）\[S4\]$/- 环节：组件封装｜代表公司：隆基绿能（组件制造与出货，位于电池片下游）[S4]\n- 环节：组件封装｜代表公司：该环节受益标的明确 [S4]/' \
  "$FX/good-chain.md" > "$TMP/e-beneficiary.md"
edge '推荐词「受益标的」必红' 1 "$TMP/e-beneficiary.md" '受益标的' '-'

sed 's/^- 环节：组件封装｜代表公司：隆基绿能（组件制造与出货，位于电池片下游）\[S4\]$/- 环节：组件封装｜代表公司：隆基绿能（组件制造与出货，位于电池片下游）[S4]\n- 环节：组件封装｜代表公司：隆基绿能（组件出货量约 80GW，位于电池片下游）[S4]/' \
  "$FX/good-chain.md" > "$TMP/e-hedge.md"
edge '改数词「约」必红' 1 "$TMP/e-hedge.md" '改数词' '-'

# 事实陈述不误红：产业链图谱里「位于…上游／下游」是位置陈述，不是推荐语；
# 裸「受益于」是因果陈述，也不该被推荐词族收走。这一档钉住收窄的两个方向。
sed 's/^- 环节：组件封装｜代表公司：隆基绿能（组件制造与出货，位于电池片下游）\[S4\]$/- 环节：组件封装｜代表公司：隆基绿能（组件制造与出货，位于电池片下游，受益于硅料降价）[S4]/' \
  "$FX/good-chain.md" > "$TMP/e-fact.md"
edge '事实陈述「受益于…」不误红' 0 "$TMP/e-fact.md" '-' 'E-BANWORD'

# 「代表公司：未取到」这一形：不要求位置括号，但必须同时出现在第五节。
edge '「代表公司：未取到」这一形不误红（好样原样）' 0 "$FX/good-chain.md" '-' 'E-FORMAT'

echo "档数=5（由上面逐档现报）｜不合=$bad｜不可判=$unk"
[ "$unk" -gt 0 ] && exit 3
[ "$bad" -gt 0 ] && exit 1
exit 0
