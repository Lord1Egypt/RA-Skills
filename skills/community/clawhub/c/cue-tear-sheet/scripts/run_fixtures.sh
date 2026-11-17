#!/usr/bin/env bash
# run_fixtures.sh —— tear-sheet check_page 总探针(工单 M34/2.1;题单=verify/tear-sheet-badspec.md M26+M31 共 22 题)。
# 断言口径(验收协议):每题 3 断言=①exit 1 ②输出含目标节号 [①..④] ③输出含指定诊断关键词;
# good 基线+三个字面改名族(段名同义/去「主体」字面/观点改「观察」)各 PASS=字面形状零依赖。
# 断言总数与构成不写死在本注释(M65 去写死,M61b 同病灶):全数以 verify/tear-sheet-coverage-m43.md 逐题对账表为准。纪律:退出码直取禁管道吞码;--sources 每题配对专用自洽 jsonl。
set -u
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
CHECK="check_page.py"
TMP="$(mktemp "${TMPDIR:-/tmp}/page_fixture.XXXXXX")"
trap 'rm -f "$TMP"' EXIT
pass=0; total=0

a() { # a <期望exit> <期望子串(可空)> <说明> <命令...>
  local want="$1" needle="$2" name="$3"; shift 3
  total=$((total+1))
  "$@" >"$TMP" 2>&1
  local got=$?
  if [ "$got" -ne "$want" ] || { [ -n "$needle" ] && ! grep -qF -- "$needle" "$TMP"; }; then
    echo "FAIL $name (exit=$want→got=$got needle='${needle}')"; sed 's/^/     | /' "$TMP"; fail=1
  else
    pass=$((pass+1))
  fi
}
fail=0

# 题单:ID|目标节号|诊断关键词
QS=(
"TS-B01|①|缺声明字段「通道用量声明」|1"
"TS-B02|②|来源锚为空/不在白名单|1"
"TS-B03|②|来源锚为空/不在白名单|1"
"TS-B04|②|正文孤儿锚|1"
"TS-B05|②|basis 缺失/不在枚举|1"
"TS-B06|③|命中禁词「买入」|1"
"TS-B07|④|风险段出现在事件段之前|1"
"TS-B08|④|41 行 > 40|1"
"TS-B09|④|主体数 6 > 5|6"
"TS-B10|④|估算/非披露明确日期|1"
"TS-B11|④|在场事件 5 > 4|1"
"TS-B12|④|存在非|1"
"TS-B13|④|风险无命中固定句缺失|1"
"TS-B14|④|主体数 6 > 5|6"
"TS-B15|④|风险段出现在事件段之前|1"
"TS-B16|④|存在非|1"
"TS-B17|④|在场事件 5 > 4|1"
"TS-B18|②|孤儿记录未被正文引用|1"
"TS-B19|④|法定锚不可核|1"
"TS-B20|③|命中禁词|1"
"TS-B21|③|sources 第|1"
"TS-B22|④|在场事件 5 > 4|1"
)
ALL_SECTIONS="① ② ③ ④"
for entry in "${QS[@]}"; do
  IFS='|' read -r qid sec kw nsub <<< "$entry"
  a 1 "[$sec]"  "$qid exit+节号" "$PY" "$CHECK" "fixtures/$qid.md" --sources "fixtures/$qid.jsonl" --subjects "$nsub"
  a 1 "$kw"     "$qid 诊断关键词" "$PY" "$CHECK" "fixtures/$qid.md" --sources "fixtures/$qid.jsonl" --subjects "$nsub"
  # 第三断言:唯一目标纯度——其余三道标记不得出现在输出中(跨道冒充=误杀,协议 2)
  "$PY" "$CHECK" "fixtures/$qid.md" --sources "fixtures/$qid.jsonl" --subjects "$nsub" >"$TMP.x" 2>&1
  total=$((total+1)); cross=0
  for d in $ALL_SECTIONS; do
    [ "$d" = "$sec" ] && continue
    grep -qF -- "[$d]" "$TMP.x" && cross=1
  done
  if [ "$cross" -eq 0 ]; then pass=$((pass+1)); else echo "FAIL $qid 跨道并报"; sed 's/^/     | /' "$TMP.x"; fail=1; fi
  rm -f "$TMP.x"
done

# good 基线与字面改名族(协议 6:同义改名/去字面不得关闸)
a 0 "" "good-page"           "$PY" "$CHECK" fixtures/good-page.md            --sources fixtures/good-sources.jsonl --subjects 1
a 0 "" "good-renamed-sections(五段同义改名)" "$PY" "$CHECK" fixtures/good-renamed-sections.md --sources fixtures/good-sources.jsonl --subjects 1
a 0 "" "good-no-subject-word(去「主体」字面)" "$PY" "$CHECK" fixtures/good-no-subject-word.md  --sources fixtures/good-sources.jsonl --subjects 1
a 0 "" "good-view-renamed   (观点→观察)"      "$PY" "$CHECK" fixtures/good-view-renamed.md     --sources fixtures/good-sources.jsonl --subjects 1

# ---- M43:--subjects 双向对齐(必传+申报↔机检对账)+ 11 主体坏样 + B04 方向二 ----
a 1 "[④]"                    "TS-B23 exit+道④   (11 主体真 FAIL,spec §4 >5)" "$PY" "$CHECK" fixtures/TS-B23.md --sources fixtures/TS-B23.jsonl --subjects 11
a 1 "主体数 11 > 5"           "TS-B23 诊断关键词"                              "$PY" "$CHECK" fixtures/TS-B23.md --sources fixtures/TS-B23.jsonl --subjects 11
a 1 "声明 5 ≠ 机检主体数 11"  "TS-B23b 少报多搭(谎报,>5+对账同道并报)"        "$PY" "$CHECK" fixtures/TS-B23.md --sources fixtures/TS-B23.jsonl --subjects 5
a 0 ""                        "TS-B24 基线(3 主体如实申报=3,四道净)"          "$PY" "$CHECK" fixtures/TS-B24.md --sources fixtures/TS-B24.jsonl --subjects 3
a 1 "声明 2 ≠ 机检主体数 3"   "TS-B24b 谎报单因(不借 >5 冒充命中)"            "$PY" "$CHECK" fixtures/TS-B24.md --sources fixtures/TS-B24.jsonl --subjects 2
a 1 "[参数] 缺 --subjects"    "缺参=FAIL 清单 exit1 非 argparse exit2(B6 家规)" "$PY" "$CHECK" fixtures/TS-B01.md --sources fixtures/TS-B01.jsonl
a 1 "sources 孤儿记录未被正文引用" "TS-B04 方向二(协议3:双向各须有明确诊断)"   "$PY" "$CHECK" fixtures/TS-B04.md --sources fixtures/TS-B04.jsonl --subjects 1

# ---- M166 码表断言:每类一枚(码表自身入册) ----
a 1 "[E-FORMAT]"   "ecode-format  (TS-B01)"    "$PY" "$CHECK" fixtures/TS-B01.md --sources fixtures/TS-B01.jsonl --subjects 1
a 1 "[E-ANCHOR]"   "ecode-anchor  (TS-B02)"    "$PY" "$CHECK" fixtures/TS-B02.md --sources fixtures/TS-B02.jsonl --subjects 1
a 1 "[E-BANWORD]"  "ecode-banword (TS-B06)"    "$PY" "$CHECK" fixtures/TS-B06.md --sources fixtures/TS-B06.jsonl --subjects 1
a 1 "[E-COVERAGE]" "ecode-coverg  (TS-B24 谎报 1≠机检 3)" "$PY" "$CHECK" fixtures/TS-B24.md --sources fixtures/TS-B24.jsonl --subjects 1

echo "----"
echo "assertions: $pass/$total"
[ "$fail" -eq 0 ] && [ "$pass" -eq "$total" ] && { echo "ALL GREEN (assertions: $pass/$total)"; exit 0; }
echo "NOT GREEN"; exit 1
