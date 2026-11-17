#!/usr/bin/env bash
# run_fixtures.sh —— sector-overview check_sector 总探针(工单 M47/2.1;题单=verify/sector-badspec.md M46 共 13 题)。
# 断言口径(题单 §0):每题 3 断言=①exit 1 ②输出含目标节号 ③指定诊断关键词;
# 第三路=唯一目标纯度(协议 2:其余三道标记不得并报)。good 族 3 枚(基线/改名族/语词族)。
# 卫生 6 枚:证据 fail-closed×2(含 B09 无证据路)/窗口申报漂移/缺参×2/--help。
# 合计 13×3+4+6 = 49 断言;合同分解与逐题映射见 verify/sector-coverage-m47.md。
# 纪律:退出码直取禁管道吞码;--window 全 case 显式。
set -u
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
CHECK="check_sector.py"
W="--window 2025-10-01~2026-09-30"
E="--evidence fixtures/evidence-good"
TMP="$(mktemp "${TMPDIR:-/tmp}/sector_fixture.XXXXXX")"
trap 'rm -f "$TMP" "$TMP.x"' EXIT
pass=0; total=0; fail=0

a() { # a <期望exit> <期望子串(可空)> <说明> <命令...>
  local want="$1" needle="$2" name="$3"; shift 3
  total=$((total+1))
  "$@" >"$TMP" 2>&1
  local got=$?
  if grep -q "Traceback" "$TMP" 2>/dev/null; then
    echo "FAIL $name (traceback=事故)"; sed 's/^/     | /' "$TMP"; fail=1
  elif [ "$got" -ne "$want" ] || { [ -n "$needle" ] && ! grep -qF -- "$needle" "$TMP"; }; then
    echo "FAIL $name (exit=$want→got=$got needle='${needle}')"; sed 's/^/     | /' "$TMP"; fail=1
  else
    pass=$((pass+1))
  fi
}

# 题单:ID|目标节号|诊断关键词
QS=(
"SO-B01|①|缺声明字段「通道用量」"
"SO-B02|②|判断词「回暖」无锚"
"SO-B03|②|态二句被改写"
"SO-B04|③|命中禁词「看好」"
"SO-B05|④|「据估计」无源句"
"SO-B06|④|「政策」段出现在「格局」段之前"
"SO-B07|④|六节不完整:缺「复核」节"
"SO-B08|④|格局段出现点评句"
"SO-B09|④|法定锚不可核:statute 伪满/断链"
"SO-B10|②|判断词「回暖」无锚"
"SO-B11|②|判断词「拐点」无锚"
"SO-B12|③|sources 第 1 行"
"SO-B13|④|代表公司 2 < 3"
)
ALL_SECTIONS="① ② ③ ④"
for entry in "${QS[@]}"; do
  IFS='|' read -r qid sec kw <<< "$entry"
  a 1 "[$sec]" "$qid exit+节号"   "$PY" "$CHECK" "fixtures/$qid.md" --sources "fixtures/$qid.jsonl" $W $E
  a 1 "$kw"    "$qid 诊断关键词"  "$PY" "$CHECK" "fixtures/$qid.md" --sources "fixtures/$qid.jsonl" $W $E
  # 第三断言:唯一目标纯度——其余三道标记不得出现在输出中(协议 2)
  "$PY" "$CHECK" "fixtures/$qid.md" --sources "fixtures/$qid.jsonl" $W $E >"$TMP.x" 2>&1
  total=$((total+1)); cross=0
  for d in $ALL_SECTIONS; do
    [ "$d" = "$sec" ] && continue
    grep -qF -- "[$d]" "$TMP.x" && cross=1
  done
  if [ "$cross" -eq 0 ]; then pass=$((pass+1)); else echo "FAIL $qid 跨道并报"; sed 's/^/     | /' "$TMP.x"; fail=1; fi
  rm -f "$TMP.x"
done

# good 族(协议 5:整词铁律不冤杀;协议 4:改名不关闸也不误报)
a 0 "" "good-sector     (六节全形基线)"     "$PY" "$CHECK" fixtures/good-sector.md     --sources fixtures/good-sources.jsonl $W $E
a 0 "" "good-renamed    (六节全改名含把关清单,语义定位)" "$PY" "$CHECK" fixtures/good-renamed.md --sources fixtures/good-sources.jsonl $W $E
a 0 "" "good-linguistic (同比上升/降幅不触发+带锚判断词过)" "$PY" "$CHECK" fixtures/good-linguistic.md --sources fixtures/good-sources.jsonl $W $E
a 0 "" "good-datagap    (M49 薄简报形制:量价节缺数句不关闸,画像态二合法)" "$PY" "$CHECK" fixtures/good-datagap.md --sources fixtures/good-datagap-sources.jsonl $W
# ---- M47 卫生:证据 fail-closed/窗口漂移/缺参/help ----
a 1 "法定锚不可核:statute 行 S6 未提供 --evidence" "good 无证据=fail-closed(不放行,题单 B09 括号合同)" "$PY" "$CHECK" fixtures/good-sector.md --sources fixtures/good-sources.jsonl $W
a 1 "法定锚不可核" "SO-B09 无证据路(伪满样双路皆死)" "$PY" "$CHECK" fixtures/SO-B09.md --sources fixtures/SO-B09.jsonl $W
a 1 "[①] 标题声明窗口" "窗口申报漂移(标题≠--window)" "$PY" "$CHECK" fixtures/good-sector.md --sources fixtures/good-sources.jsonl --window 2026-01-01~2026-04-01 $E
a 1 "[参数] 缺 --sources" "缺 sources=FAIL 清单 exit1" "$PY" "$CHECK" fixtures/good-sector.md $W $E
a 1 "[参数] 缺 --window" "缺 window=FAIL 清单 exit1" "$PY" "$CHECK" fixtures/good-sector.md --sources fixtures/good-sources.jsonl $E
a 0 "" "--help (CONTRIBUTING §3)" "$PY" "$CHECK" --help

# ---- M166 码表断言:每类一枚(码表自身入册) ----
a 1 "[E-FORMAT]"   "ecode-format  (SO-B01 声明缺)"    "$PY" "$CHECK" fixtures/SO-B01.md --sources fixtures/SO-B01.jsonl $W $E
a 1 "[E-ANCHOR]"   "ecode-anchor  (SO-B02 命门无锚)"  "$PY" "$CHECK" fixtures/SO-B02.md --sources fixtures/SO-B02.jsonl $W $E
a 1 "[E-BANWORD]"  "ecode-banword (SO-B04 看好)"      "$PY" "$CHECK" fixtures/SO-B04.md --sources fixtures/SO-B04.jsonl $W $E
a 1 "[E-COVERAGE]" "ecode-coverg  (SO-B05 据估计补数)" "$PY" "$CHECK" fixtures/SO-B05.md --sources fixtures/SO-B05.jsonl $W $E

echo "----"
echo "assertions: $pass/$total"
[ "$fail" -eq 0 ] && [ "$pass" -eq "$total" ] && { echo "ALL GREEN (assertions: $pass/$total)"; exit 0; }
echo "NOT GREEN"; exit 1
