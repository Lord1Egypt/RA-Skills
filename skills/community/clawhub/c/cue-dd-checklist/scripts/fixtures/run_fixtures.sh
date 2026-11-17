#!/usr/bin/env bash
# run_fixtures.sh — dd-checklist 机检题库跑（题单 R0-I + M63 增题，逐样验 exit 与**诊断码集合精确相等**）
#
#   bash scripts/fixtures/run_fixtures.sh              # 全量
#   bash scripts/fixtures/run_fixtures.sh bad-B14      # 只跑名字含 bad-B14 的样
#
# 每个样目录自带 cmd.txt（一行完整命令，在该目录内执行）与 expect.txt：
#   exit=<期望退出码>  need=<允许的诊断码，可多行>  [must-not=<禁止出现的码>]  [verdict=must-fail]
# 判据（题单 §0.7 / 契约 §v2-6）：**实际 DD-* 码集合必须与声明集合精确相等**，多码=FAIL；
# ctl-* 是 runner 自证样（负控与边界），单列计数、不占合同主集之数（样数只存在于题单矩阵与本 runner 现报，C-19）；崩溃一律不算命中（题单 §0.1）。
set -uo pipefail

FIXROOT_PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -d "$FIXROOT_PKG/samples" ] || [ ! -f "$FIXROOT_PKG/unpack.py" ]; then
  echo "FAIL 缺样容器（samples/ 或 unpack.py）——重铺：python3 scripts/gen_fixtures.py --badspec <题单>"
  exit 1
fi
# M225：渠道两道硬限——条目 ≤200（目录条目照计，K-20）与扩展名白名单（压缩包属拒收面，K-22）。
# 所以每枚样并成一枚文本容器、共享语料留 .json/.md 散件；这里把容器铺回临时目录，
# **下面的 cmd/expect 判卷逻辑一字未动**（铺法与生成器自证同源＝同一个 unpack.materialize）。
WORK="$(mktemp -d "${TMPDIR:-/tmp}/dd-samples-XXXXXX")" || exit 1
mkdir -p "$WORK/scripts/fixtures"
# M294：题单里 103 枚样的 cmd 各自 `mktemp -d` 建工作区，旧写法把它们全留在**调用方的**临时根上
# （现测：跑一次漏 107 枚／9.3 MB）。现在把子进程的 TMPDIR 指进本 runner 私有的 $WORK/tmp，
# 退出时由下面那枚 trap 连 $WORK 一起带走——外场一枚不落。调用方的临时根只被**观测**（零新增判据），
# 本 runner 绝不删那里任何不是我建的东西（`DD_OUTER_TMP` 只为那条判据与注入反证可见）。
DD_OUTER_TMP="${TMPDIR:-/tmp}"; export DD_OUTER_TMP
RUNTMP="$WORK/tmp"
mkdir -p "$RUNTMP" || { echo "FAIL 建不起 runner 私有临时根 $RUNTMP（环境故障，不续跑不假绿）"; rm -rf "$WORK"; exit 1; }
export TMPDIR="$RUNTMP"
if ls -A "$DD_OUTER_TMP" >/dev/null 2>&1; then
  tmp_before="$(cd "$DD_OUTER_TMP" && ls -A | sort)"; tmp_snap_ok=1
else
  tmp_before=""; tmp_snap_ok=0        # 快照取不到＝本档红，空值绝不充当「零新增」
fi
if ! python3 "$FIXROOT_PKG/unpack.py" --all "$FIXROOT_PKG" "$WORK/scripts/fixtures"; then
  echo "FAIL 样容器铺回失败（容器形制或 python3 可用性问题，不静默继续）"
  rm -rf "$WORK"; exit 1
fi
cp -R "$FIXROOT_PKG/_shared" "$WORK/scripts/fixtures/_shared"
cp "$FIXROOT_PKG/../check_dd.py" "$WORK/scripts/check_dd.py"     # 判卷面用包内真件，不用容器副本
FIXROOT="$WORK/scripts/fixtures"
trap 'rm -rf "$WORK"' EXIT
FILTER="${1:-}"
gb_ok=0
gb_fail=0
gb_total=0
ctl_ok=0
ctl_fail=0
ctl_total=0
failed_cases=()

for dir in "$FIXROOT"/*/; do
  name="$(basename "$dir")"
  case "$name" in
    good-* | bad-*) kind=contract ;;
    ctl-*) kind=ctl ;;
    *) continue ;;
  esac
  if [ -n "$FILTER" ] && ! printf '%s' "$name" | grep -q -- "$FILTER"; then
    continue
  fi
  if [ ! -f "$dir/cmd.txt" ] || [ ! -f "$dir/expect.txt" ]; then
    echo "FAIL $name 缺 cmd.txt / expect.txt"
    failed_cases+=("$name")
    [ "$kind" = contract ] && gb_fail=$((gb_fail + 1)) || ctl_fail=$((ctl_fail + 1))
    continue
  fi
  cmd="$(head -n 1 "$dir/cmd.txt")"
  want_exit="$(sed -n 's/^exit=//p' "$dir/expect.txt" | head -n 1)"
  verdict="$(sed -n 's/^verdict=//p' "$dir/expect.txt" | head -n 1)"
  out="$(cd "$dir" && bash -c "$cmd" 2>&1)"
  got_exit=$?

  allowed="$(sed -n 's/^need=//p' "$dir/expect.txt" | sort -u | tr '\n' ' ' | sed 's/[[:space:]]*$//')"
  actual="$(printf '%s\n' "$out" | sed -n 's/^\(\[E-[A-Z]*\] \)\?\(DD-[A-Z]*\): .*/\2/p' | sort -u | tr '\n' ' ' | sed 's/[[:space:]]*$//')"
  forbidden="$(sed -n 's/^must-not=//p' "$dir/expect.txt" | tr ' ' '\n' | sed '/^$/d' | sort -u | tr '\n' ' ' | sed 's/[[:space:]]*$//')"

  exact_ok=1
  if [ "$got_exit" != "$want_exit" ]; then
    exact_ok=0
    why=" exit≠$want_exit"
  else
    why=""
  fi
  if [ "$allowed" != "$actual" ]; then
    exact_ok=0
    why="$why 码集不等(允许[$allowed] 实发[$actual])"
  fi
  for code in $forbidden; do
    case " $actual " in
      *" $code "*) exact_ok=0; why="$why 出现禁码$code" ;;
    esac
  done
  if printf '%s\n' "$out" | grep -qE 'Traceback|SyntaxError'; then
    exact_ok=0
    why="$why 崩溃(不算命中)"
  fi

  if [ "$verdict" = "must-fail" ]; then
    # runner 负控：本样故意多打未声明的码，runner **必须**判它失败——判对了控制样才算过
    if [ "$exact_ok" = 0 ]; then
      printf 'ok   %-38s ctl(负控按预期判失败:%s)\n' "$name" "${why# }"
      ctl_ok=$((ctl_ok + 1))
      ctl_total=$((ctl_total + 1))
    else
      printf 'FAIL %-38s ctl(负控未被拦下=runner 只做包含式检查)\n' "$name"
      ctl_fail=$((ctl_fail + 1))
      failed_cases+=("$name")
    fi
    continue
  fi

  if [ "$exact_ok" = 1 ]; then
    printf 'ok   %-38s exit=%s codes[%s]\n' "$name" "$got_exit" "$actual"
    if [ "$kind" = contract ]; then gb_ok=$((gb_ok + 1)); else ctl_ok=$((ctl_ok + 1)); fi
  else
    printf 'FAIL %-38s exit=%s want=%s |%s\n' "$name" "$got_exit" "$want_exit" "$why"
    printf '%s\n' "$out" | sed 's/^/        /'
    if [ "$kind" = contract ]; then gb_fail=$((gb_fail + 1)); else ctl_fail=$((ctl_fail + 1)); fi
    failed_cases+=("$name")
  fi
  [ "$kind" = contract ] && gb_total=$((gb_total + 1)) || ctl_total=$((ctl_total + 1))
done

# ---- M166 码表自检:每类一枚破坏样触发对应 [E-XXX] 行首前缀(计入 controls 自证列) ----
for spec in "bad-B01-anchor-missing|[E-FORMAT]" "bad-B22-statute-fake|[E-ANCHOR]" "bad-X10-redline-in-ledger|[E-BANWORD]" "bad-X07-coverage-missing-row|[E-COVERAGE]"; do
  d="${spec%%|*}"; mark="${spec##*|}"
  cmd="$(head -n 1 "$FIXROOT/$d/cmd.txt")"
  ctl_total=$((ctl_total + 1))
  ec_out="$(cd "$FIXROOT/$d" && eval "$cmd" 2>&1 || true)"
  case "$ec_out" in *"$mark"*) hit=1 ;; *) hit=0 ;; esac
  if [ "$hit" -eq 1 ]; then
    echo "ok   ecode-${d} (前缀 ${mark})"; ctl_ok=$((ctl_ok + 1))
  else
    echo "FAIL ecode-${d} (缺前缀 ${mark})"; ctl_fail=$((ctl_fail + 1)); failed_cases+=("ecode-${d}")
  fi
done

# ---- M294 临时根零新增自证：跑完一趟，调用方的临时根不得多出一枚（样里漏下的话这一档必红并点名） ----
#    这一档是**包内判据**，不是回执里的一句话：以后谁把样内 cmd 改回不落清理的写法，这里当场红。
ctl_total=$((ctl_total + 1))
if [ "$tmp_snap_ok" -ne 1 ]; then
  echo "FAIL ctl-tmp-root-clean (调用方临时根快照取不到＝不可读，不判绿)"; ctl_fail=$((ctl_fail + 1)); failed_cases+=("ctl-tmp-root-clean")
else
  tmp_after="$(cd "$DD_OUTER_TMP" && ls -A | sort)"
  tmp_new="$(comm -13 <(printf '%s\n' "$tmp_before") <(printf '%s\n' "$tmp_after"))"
  if [ -z "$tmp_new" ]; then
    echo "ok   ctl-tmp-root-clean (调用方临时根零新增；样内临时区全落 runner 私有根，随退出清理)"; ctl_ok=$((ctl_ok + 1))
  else
    printf 'FAIL ctl-tmp-root-clean (跑完仍新增 %d 枚，逐枚点名：\n' "$(printf '%s\n' "$tmp_new" | grep -c . )"
    printf '%s\n' "$tmp_new" | sed 's/^/        泄漏 /'
    ctl_fail=$((ctl_fail + 1)); failed_cases+=("ctl-tmp-root-clean")
  fi
fi

echo "----"
printf 'fixtures: %d ok / %d fail / %d total\n' "$gb_ok" "$gb_fail" "$((gb_ok + gb_fail))"
printf 'controls: %d ok / %d fail / %d total\n' "$ctl_ok" "$ctl_fail" "$ctl_total"
if [ "$((gb_fail + ctl_fail))" -gt 0 ]; then
  printf 'failing: %s\n' "${failed_cases[*]}"
  exit 1
fi
exit 0
