#!/bin/bash
# smart-web-search 测试脚本
# 验证：依赖、Query 改写、国内搜索、海外搜索、正文抓取
set +e

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_ROOT" || exit 1

PASS=0
FAIL=0
RESULTS=()

run_test() {
  local name="$1"
  local cmd="$2"
  local expect="$3"
  echo ""
  echo "=========================================="
  echo "  [测试] $name"
  echo "=========================================="
  local output
  output=$(eval "$cmd" 2>&1)
  if echo "$output" | grep -q "$expect"; then
    echo "[PASS] $name"
    PASS=$((PASS + 1))
    RESULTS+=("[PASS] $name")
  else
    echo "[FAIL] $name (期望: $expect)"
    echo "--- 实际输出（前 30 行）---"
    echo "$output" | head -30
    FAIL=$((FAIL + 1))
    RESULTS+=("[FAIL] $name")
  fi
}

echo ""
echo "##########################################"
echo "  smart-web-search 测试套件"
echo "##########################################"

# 1. 依赖检查
run_test "依赖检查 - node_modules 存在" \
  "ls node_modules/playwright 2>&1" \
  "package.json"

# 2. Query 改写 - 城市美食
run_test "Query 改写 - 深圳美食 → 深圳 美食推荐" \
  "node scripts/search.js '深圳美食' --max=2 --no-fetch 2>&1" \
  "深圳 美食推荐"

# 3. Query 改写 - 价格类
run_test "Query 改写 - 今日金价 → 金价" \
  "node scripts/search.js '今日金价' --max=2 --no-fetch 2>&1" \
  "今日价格"

# 4. Query 改写 - 下载类
run_test "Query 改写 - Python 下载 → Python 官方下载" \
  "node scripts/search.js 'Python 下载' --max=2 --no-fetch 2>&1" \
  "官方下载"

# 5. Query 改写 - VS 对比
run_test "Query 改写 - React vs Vue → React Vue 对比" \
  "node scripts/search.js 'React vs Vue' --max=2 --no-fetch 2>&1" \
  "React Vue 对比"

# 6. Query 改写 - 是什么
run_test "Query 改写 - Python 是什么 → Python 介绍" \
  "node scripts/search.js 'Python 是什么' --max=2 --no-fetch 2>&1" \
  "是什么→介绍"

# 7. 自动检测 - 返回结果
run_test "自动检测搜索 - Python 教程返回结果" \
  "node scripts/search.js 'Python 教程' --max=3 --no-fetch 2>&1" \
  "条结果"

# 8. 自动检测日志输出
run_test "自动检测日志 - 输出地理判定" \
  "node scripts/search.js '测试' --max=1 --no-fetch 2>&1" \
  "\[地理\]"

# 9. 正文抓取 - 抓 1 条
run_test "正文抓取 - 自动检测" \
  "node scripts/search.js 'Python 教程' --max=2 --fetch=1 2>&1" \
  "fetch"

# 10. --no-rewrite 参数
run_test "禁用改写 - --no-rewrite" \
  "node scripts/search.js '今日金价' --max=1 --no-fetch --no-rewrite 2>&1" \
  "今日金价"

# 总结
echo ""
echo "##########################################"
echo "  测试结果汇总"
echo "##########################################"
for r in "${RESULTS[@]}"; do
  echo "$r"
done
echo ""
echo "通过: $PASS / $((PASS + FAIL))"
echo ""

if [ $FAIL -eq 0 ]; then
  echo "全部测试通过"
  exit 0
else
  echo "$FAIL 项失败"
  exit 1
fi
