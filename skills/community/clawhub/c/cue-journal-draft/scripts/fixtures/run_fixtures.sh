#!/usr/bin/env bash
# run_fixtures.sh —— journal-draft 包内自带自测面（零网络、纯 stdlib + bash；runner 形，无参直跑）。
#
# 判什么（判定全集在各脚本现值，本件不另立规矩；改任何一条判据都要先看这里会不会红）：
#   A 生成器好样链：随包真件（assets/templates/content.example.json × assets/examples/*/stylespec.json）
#     走完 build_draft.py → 退码 0、draft.html 与 manifest.csv 齐、报告行自报 pages/units/unknown，
#     且同一输入双跑产物逐字节同（确定性）。
#   B 量级门禁是判定不是崩溃：同一输入加 --stats 必须退 1 并打 [FAIL]；
#     再把 baseline 现场配到与内容同量级，同一道门必须放行退 0——这一枚是防恒真哨兵，
#     少了它，「--stats 必红」可能只是门永远关着。
#   C 坏输入不落半成品：--content / --spec 给截断 JSON、JSON 数组、JSON 字符串三种形，
#     一律非零退码且**产物目录零文件**（只判「有没有半成品」，不判它用什么方式报错——
#     现值 build_draft 对坏 JSON 仍抛 Python 堆栈，那是待修的另一件事，本件不把它固化成期望）。
#   D 语义层生成器 enrich_from_omni：好样退 0 且 semantic.json 与 unit-patterns.draft.md 齐；
#     --outline 坏 JSON／非对象两种形各退 1、零产物、首行点名 --outline、且零 Traceback（这条判据是实的）。
#   E 派生面↔生成器 同源档 check_derived_sync：重跑生成器现产 example 面与在盘按块比。应检枚数从盘上名册
#     现算，实跑≠应检即红；本轮走登记态（已知漂移逐枚自报、退 0），超出登记、少测、双向锁、豁免键缺位都红。
#
# 退出形制：全过末行 "ALL GREEN（N 项）" 退 0；任一不符打 FAIL 行并附输出，末行 "NOT GREEN" 退 1。
# 判定一律直取 "$?"（勿 `cmd | tail`——管道会把退出码换成 tail 的）。
set -u
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
ROOT='../../'          # 本件在 scripts/fixtures/ 下，包根在两级之上
BD="${ROOT}scripts/build_draft.py"
EN="${ROOT}scripts/enrich_from_omni.py"
SPEC="${ROOT}assets/examples/qiming-regional-sample/stylespec.json"
CONTENT="${ROOT}assets/templates/content.example.json"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/journal-draft-fixtures.XXXXXX")"   # 唯一名，并发与多窗不互踩
trap 'rm -rf "$TMP"' EXIT
fail=0
n=0

say() { local t="${1//"$TMP"/@TMP@}"; printf '%s\n' "$t"; }   # 临时根一律打成一个短标记，双跑输出逐字节可比

expect_rc() { # expect_rc <期望退码> <说明> <命令...>
  local want="$1" name="$2"; shift 2
  n=$((n + 1))
  "$@" >"$TMP/log" 2>&1
  local got=$?
  if [ "$got" -eq "$want" ]; then say "ok   $name（退码 $got）"
  else say "FAIL $name（期望退码 $want，实得 $got）"; sed 's/^/     | /' "$TMP/log" | head -8; fail=1; fi
}

expect_file() { # expect_file <说明> <路径>：存在且非空
  n=$((n + 1))
  if [ -s "$2" ]; then say "ok   $2 在场且非空（$1）"
  else say "FAIL $1：$2 缺位或为空"; fail=1; fi
}

expect_in() { # expect_in <说明> <子串> <文件>
  n=$((n + 1))
  if grep -qF -- "$2" "$3"; then say "ok   $3 含「$2」（$1）"
  else say "FAIL $1：$3 未含「$2」"; sed 's/^/     | /' "$3" | head -6; fail=1; fi
}

expect_head() { # expect_head <说明> <日志> <参数名> <病灶词>：错误输出第 1 行必须同时含参数名与病灶词
  n=$((n + 1))
  local first hp hn
  first="$(head -1 "$2")"
  hp=0; hn=0
  printf '%s' "$first" | grep -qF -- "$3" && hp=1
  printf '%s' "$first" | grep -qF -- "$4" && hn=1
  if [ "$hp" -eq 1 ] && [ "$hn" -eq 1 ]; then
    say "ok   $1：首行同点参数名「$3」与病灶「$4」"
  else
    say "FAIL $1：首行未同时点出参数名与病灶（参数名命中=$hp 病灶命中=$hn）；首行实得：$(printf '%s' "$first" | cut -c1-96)"
    sed 's/^/     | /' "$2" | head -3; fail=1
  fi
}

expect_last() { # expect_last <说明> <文件> <子串1> <子串2>：末行（去空行）必须同时含两枚子串
  n=$((n + 1))
  local last l1 l2
  last="$(grep -v '^[[:space:]]*$' "$2" | tail -1)"
  l1=0; l2=0
  printf '%s' "$last" | grep -qF -- "$3" && l1=1
  printf '%s' "$last" | grep -qF -- "$4" && l2=1
  if [ "$l1" -eq 1 ] && [ "$l2" -eq 1 ]; then
    say "ok   末行同含「$3」与「$4」（$1）"
  else
    say "FAIL $1：末行未同时含两枚子串（命中 $l1/$l2）；末行实得：$(printf '%s' "$last" | cut -c1-96)"
    fail=1
  fi
}

expect_absent() { # expect_absent <说明> <目录>：目录不存在或内零文件
  n=$((n + 1))
  local c=0
  [ -d "$2" ] && c=$(find "$2" -type f | wc -l | tr -d ' ')
  if [ "$c" -eq 0 ]; then say "ok   $2 零产物（$1）"
  else say "FAIL $1：$2 里落了 $c 枚文件"; fail=1; fi
}

expect_no_tb() { # expect_no_tb <说明> <日志文件>
  n=$((n + 1))
  if grep -qF 'Traceback' "$2"; then say "FAIL $1：$2 里出现 Traceback（规格 0 次）"; sed 's/^/     | /' "$2" | head -4; fail=1
  else say "ok   $2 零 Traceback（$1）"; fi
}

# ---------- A 生成器好样链 ----------
expect_rc 0 'A1 build_draft 好样（--no-baseline-gate）' \
  "$PY" -B "$BD" --spec "$SPEC" --content "$CONTENT" --out "$TMP/A" --no-baseline-gate
expect_file 'A2 主稿 HTML' "$TMP/A/draft.html"
expect_file 'A3 页面清单 manifest.csv' "$TMP/A/manifest.csv"
expect_in 'A4 报告自报页数与单元数' 'pages=' "$TMP/log"
expect_in 'A5 报告自报溯源口径' 'unknown=' "$TMP/log"

"$PY" -B "$BD" --spec "$SPEC" --content "$CONTENT" --out "$TMP/A1" --no-baseline-gate >"$TMP/l1" 2>&1
r1=$?
"$PY" -B "$BD" --spec "$SPEC" --content "$CONTENT" --out "$TMP/A2" --no-baseline-gate >"$TMP/l2" 2>&1
r2=$?
n=$((n + 1))
if [ "$r1" -eq 0 ] && [ "$r2" -eq 0 ] && cmp -s "$TMP/A1/draft.html" "$TMP/A2/draft.html" \
   && cmp -s "$TMP/A1/manifest.csv" "$TMP/A2/manifest.csv"; then
  say "ok   A6 同输入双跑产物逐字节同（draft.html 与 manifest.csv）"
else
  say "FAIL A6 双跑产物不同或退码非 0（实得 $r1/$r2）"; fail=1
fi

# ---------- B 量级门禁：红是真红，且能放行 ----------
expect_rc 1 'B1 同输入加 --stats 必须按门禁红' \
  "$PY" -B "$BD" --spec "$SPEC" --content "$CONTENT" --out "$TMP/B" --stats
expect_in 'B2 红话术点名是判定不是崩溃' '门禁判定结果' "$TMP/log"

# 现场把 baseline 配到与内容同量级（临时件，不落包内），同一道门必须放行
"$PY" - "$SPEC" "$TMP/spec.matched.json" <<'PYEOF'
import json, sys
spec = json.load(open(sys.argv[1], encoding='utf-8'))
spec['scale_baseline'] = {'pages': 8, 'articles': 1, 'chars': 400}
open(sys.argv[2], 'w', encoding='utf-8').write(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
PYEOF
expect_rc 0 'B3 baseline 配平后同一道门必须放行（防恒真哨兵）' \
  "$PY" -B "$BD" --spec "$TMP/spec.matched.json" --content "$CONTENT" --out "$TMP/B3" --stats

# ---------- C 坏输入不落半成品 ----------
# 面上承诺「所有脚本对常见操作失误都给出可执行的下一步，而不是抛 traceback」——
# 所以这一组除「零半成品」外，逐形再断言零 Traceback；坏形走的是取数错误出口，退码 1、首行点名参数名。
for shape in truncated array string; do
  case $shape in
    truncated) lesion='不是合法 JSON' ;;
    *)         lesion='只收对象' ;;
  esac
  expect_rc 1 "C$shape build_draft 收 ${shape} 形 --content" \
    "$PY" -B "$BD" --spec "$SPEC" --content "fixtures-$shape.json" --out "$TMP/C-$shape" --no-baseline-gate
  expect_no_tb "C$shape 零 Traceback（面上承诺给下一步，不给堆栈）" "$TMP/log"
  expect_head "C$shape 首行断言" "$TMP/log" '--content' "$lesion"
  expect_absent "C$shape 零半成品" "$TMP/C-$shape"
done
expect_rc 1 'Cstr2 build_draft 收 string 形 --spec' \
  "$PY" -B "$BD" --spec "fixtures-string.json" --content "$CONTENT" --out "$TMP/C-spec" --no-baseline-gate
expect_no_tb 'Cstr2 零 Traceback' "$TMP/log"
expect_head 'Cstr2 首行断言' "$TMP/log" '--spec' '只收对象'
expect_absent 'Cstr2 零半成品' "$TMP/C-spec"
expect_rc 2 'Creq 缺 --content 按 argparse 用法退 2' \
  "$PY" -B "$BD" --spec "$SPEC" --out "$TMP/C-req" --no-baseline-gate
expect_absent 'Creq 零半成品（用法错也不许先建目录留壳）' "$TMP/C-req"

# ---------- D 语义层生成器 ----------
# D 组：好样两件齐 ＋ 四条坏形支路逐枚断言。
# 坏形一律走「退 1＋首行点名--outline 与病灶＋零 Traceback＋零产物」四件套，一支不许少一枚：
# 上一版只有截断形有零产物断言，数组形那支没有——于是「报错后仍偷偷落一个文件」这种回归照抓不到。
expect_rc 0 'D1 enrich_from_omni 好样（md × outline 对象）' \
  "$PY" -B "$EN" --md omni.sample.md --outline omni.outline.json --out "$TMP/D1"
expect_file 'D2 semantic.json' "$TMP/D1/semantic.json"
expect_file 'D3 unit-patterns.draft.md' "$TMP/D1/unit-patterns.draft.md"

for shape in truncated array string missingfile; do
  case $shape in
    truncated)     src=fixtures-truncated.json; needle='不是合法 JSON' ;;
    array)         src=fixtures-array.json;     needle='只收对象' ;;
    string)        src=fixtures-string.json;    needle='只收对象' ;;
    missingfile)   src=no-such-outline.json;    needle='指向的文件不存在' ;;
  esac
  expect_rc 1 "D-$shape --outline 收 ${shape} 形退 1（指了路径却读不到 ≠ 没给）" \
    "$PY" -B "$EN" --md omni.sample.md --outline "$src" --out "$TMP/D-$shape"
  expect_head "D-$shape 首行断言" "$TMP/log" '--outline' "$needle"
  expect_no_tb "D-$shape 零 Traceback" "$TMP/log"
  expect_absent "D-$shape 零产物（坏形一律不落语义层）" "$TMP/D-$shape"
done

# ---------- E 派生面↔生成器 同源档（登记态） ----------
# 判的是「在盘的派生 example 面还和生成器现产对得上吗」：名册现算应检枚数 → 逐枚重跑生成器 → 按块比。
# 登记态＝已知漂移逐枚自报并退 0（归属路线待定，先把发布链留着）；红支路五条：
# 实测超出登记、未登记的块或键漂了、实跑≠应检（少测一枚即尺不可信）、人工拥有项双向锁（盘面缺失或生成器长出）、
# 豁免键在任一侧不在场。E4 另锁末行必须带「实跑／应检」双数——少测这件事不许只在心里知道。
DSY="${ROOT}scripts/check_derived_sync.py"
expect_rc 0 'E1 同源档（登记态）必须放行' "$PY" -B "$DSY"
expect_in 'E2 同源档自报已知漂移枚数' '已知漂移' "$TMP/log"
expect_in 'E3 同源档自报的是登记态不是判定制' '（登记态，归属路线待定）' "$TMP/log"
expect_last 'E4 同源档末行必须带实跑与应检双数' "$TMP/log" '实跑' '应检'

echo "------------------------------------------------------------"
if [ "$fail" -eq 0 ]; then
  echo "ALL GREEN（$n 项）——生成器好样链／量级门禁可放行／坏输入不落半成品／语义层坏形响亮退出／派生面与生成器同源（登记态）"
  exit 0
fi
echo "NOT GREEN（$n 项里有不符，见上列 FAIL 行）"
exit 1
