#!/usr/bin/env bash
# cite-holmes 测试套件统一入口（v6.4.0 M4；v6.5.0 F57/F59 扩展）——
# pytest 未装环境（unittest discover）与 CI（--verbose 里程碑）共用一条命令；
# 耗时上限锁防套件腐化。
# 用法:
#   tools/run_tests.sh                 # 标准档（unittest discover -v 1）
#   tools/run_tests.sh --verbose       # CI 档：逐测试名输出+里程碑计时（横向共性①）
#   tools/run_tests.sh --budget 200    # 自定义耗时预算秒（默认 200=基线 152s×1.3）
#   tools/run_tests.sh --shipped       # 只跑随包 sealed 子集（tests/shipped_manifest.json
#                                      #   清单；包内安装验证/部分拷贝损坏哨兵，F57）
#   tools/run_tests.sh --held-out      # 真网闸门档：独立留出集+腐蚀集全批预期比对
#                                      #   （capture=100%+零误杀+忠实度命中，F59；
#                                      #   需网络，退出码 1=闸门拦停）
# 退出码 0=全绿且在预算内；1=有失败或超预算；2=用法/清单错误。
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SK="$(cd "$HERE/.." && pwd)"
VERBOSE=0; BUDGET=200; SHIPPED=0; HELDOUT=0
while [ $# -gt 0 ]; do
  case "$1" in
    --verbose) VERBOSE=1 ;;
    --budget) BUDGET="$2"; shift ;;
    --shipped) SHIPPED=1 ;;
    --held-out) HELDOUT=1 ;;
    *) echo "未知参数: $1"; exit 2 ;;
  esac
  shift
done

cd "$SK" || exit 1

# ── F59 真网闸门档 ──────────────────────────────────────────────
if [ "$HELDOUT" -eq 1 ]; then
  echo "== cite-holmes 留出集真网闸门（F59）=="
  python3 tools/run_eval.py --refs examples/holdout_real.json --net --gate \
    --json-out /tmp/ch_gate_holdout.json --md-out /tmp/ch_gate_holdout.md
  RC1=$?
  python3 tools/run_eval.py --refs examples/holdout_fidelity.json --net \
    --fidelity --gate --json-out /tmp/ch_gate_fid.json --md-out /tmp/ch_gate_fid.md
  RC2=$?
  if [ "$RC1" -ne 0 ] || [ "$RC2" -ne 0 ]; then
    echo "RESULT: FAIL（留出集/腐蚀集闸门拦停——见上方报告）"; exit 1
  fi
  echo "RESULT: PASS（留出集+腐蚀集双闸门全过）"
  exit 0
fi

# ── F57 随包子集档 ──────────────────────────────────────────────
DISCOVER_ARGS=(discover -s tests -p "test_*.py")
if [ "$SHIPPED" -eq 1 ]; then
  MF="tests/shipped_manifest.json"
  if [ ! -f "$MF" ]; then
    echo "ERROR: $MF 不存在（随包子集清单缺失）"; exit 2
  fi
  FILES=$(python3 -c "import json,sys; print(' '.join(json.load(open(sys.argv[1], encoding='utf-8'))['files']))" "$MF")
  if [ -z "$FILES" ]; then
    echo "ERROR: $MF files 为空"; exit 2
  fi
  echo "== cite-holmes 随包 sealed 子集（F57，清单 $(echo $FILES | wc -w) 文件）=="
  RC=0
  for f in $FILES; do
    [ -f "tests/$f" ] || { echo "FAIL: 清单文件缺失 tests/$f（部分拷贝损坏）"; RC=1; continue; }
    case "$f" in
      # helper 模块（_mocks.py 等）只验存在——被测试 import 时即验证
      test_*.py) ;;
      *) continue ;;
    esac
    if [ "$VERBOSE" -eq 1 ]; then
      python3 -m unittest discover -s tests -p "$f" -v 2>&1 | tail -3
    else
      python3 -m unittest discover -s tests -p "$f" 2>&1 | tail -1
    fi
    FRC=${PIPESTATUS[0]}
    [ "$FRC" -ne 0 ] && RC=1
  done
  echo "== 随包子集完成（rc=$RC）=="
  [ "$RC" -eq 0 ] && echo "RESULT: PASS（随包 sealed 子集全绿）" \
                 || echo "RESULT: FAIL（随包子集有失败）"
  exit "$RC"
fi

echo "== cite-holmes 套件（unittest discover）=="
START=$(date +%s)
if [ "$VERBOSE" -eq 1 ]; then
  python3 -m unittest "${DISCOVER_ARGS[@]}" -v 2>&1 | \
    awk '/^test |^Ran |^OK|^FAILED/ { print strftime("[%H:%M:%S]") " " $0; fflush() } !/^test / { print }'
else
  python3 -m unittest "${DISCOVER_ARGS[@]}" 2>&1 | tail -4
fi
RC=${PIPESTATUS[0]}
END=$(date +%s)
ELAPSED=$((END - START))
echo "== 耗时 ${ELAPSED}s（预算 ${BUDGET}s，基线 152s）=="
if [ "$RC" -ne 0 ]; then
  echo "RESULT: FAIL（存在失败用例）"; exit 1
fi
if [ "$ELAPSED" -gt "$BUDGET" ]; then
  echo "RESULT: FAIL（超耗时预算——套件腐化信号，检查新增重负载用例）"; exit 1
fi
echo "RESULT: PASS（全绿且在预算内）"
