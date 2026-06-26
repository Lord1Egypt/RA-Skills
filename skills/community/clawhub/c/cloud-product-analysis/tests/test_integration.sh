#!/bin/bash
# Integration tests - require network access and installed dependencies
# Run: CLOUD_DOC_SCRAPER_INTEGRATION=1 bash tests/test_integration.sh

set +e

if [ "$CLOUD_DOC_SCRAPER_INTEGRATION" != "1" ]; then
    echo "Skipping integration tests (set CLOUD_DOC_SCRAPER_INTEGRATION=1 to run)"
    exit 0
fi

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
echo "  cloud-product-analysis 集成测试"
echo "##########################################"

# 1. 依赖检查
run_test "依赖检查" \
  "python scripts/cloud_doc_scraper.py --list 2>&1" \
  "All dependencies satisfied"

# 2. 产品列表
run_test "产品列表 - 包含 ECS" \
  "python scripts/cloud_doc_scraper.py --list 2>&1" \
  "ecs"

# 3. 产品列表 - 包含 CDN
run_test "产品列表 - 包含 CDN" \
  "python scripts/cloud_doc_scraper.py --list 2>&1" \
  "cdn"

# 4. 文档抓取 - CDN (2页轻量测试)
run_test "文档抓取 - CDN（限制 2 页）" \
  "python scripts/cloud_doc_scraper.py --product cdn --max-pages 2 --output tests/_test_cdn.md 2>&1 && ls tests/_test_cdn.md" \
  "_test_cdn.md"

# 5. 输出格式 - 包含对比表格
if [ -f tests/_test_cdn.md ]; then
  run_test "输出格式 - 包含对比表格" \
    "cat tests/_test_cdn.md 2>&1" \
    "对比"

  # 6. 输出格式 - 包含 Aliyun 章节
  run_test "输出格式 - 包含 Aliyun 章节" \
    "cat tests/_test_cdn.md 2>&1" \
    "Aliyun"

  # 7. 输出格式 - 包含 Huawei 章节
  run_test "输出格式 - 包含 Huawei 章节" \
    "cat tests/_test_cdn.md 2>&1" \
    "Huawei"

  # 8. 输出格式 - 包含 Changelog
  run_test "输出格式 - 包含更新日志" \
    "cat tests/_test_cdn.md 2>&1" \
    "更新日志"
fi

# 9. 错误产品名
run_test "错误处理 - 未知产品" \
  "python scripts/cloud_doc_scraper.py --product invalid_xxx 2>&1" \
  "Unknown product"

# 10. 三方对比测试 - CDN (aliyun,huawei,aws)
run_test "三方对比 - CDN (aliyun,huawei,aws)" \
  "python scripts/cloud_doc_scraper.py --product cdn --providers aliyun,huawei,aws --max-pages 1 --output tests/_test_cdn_3way.md 2>&1 && ls tests/_test_cdn_3way.md" \
  "_test_cdn_3way.md"

# 11. 四方对比测试 - ECS (aliyun,huawei,aws,tencent)
run_test "四方对比 - ECS (aliyun,huawei,aws,tencent)" \
  "python scripts/cloud_doc_scraper.py --product ecs --providers aliyun,huawei,aws,tencent --max-pages 1 --output tests/_test_ecs_4way.md 2>&1 && ls tests/_test_ecs_4way.md" \
  "_test_ecs_4way.md"

# 清理测试文件
rm -f tests/_test_*.md

# 总结
echo ""
echo "##########################################"
echo "  集成测试结果汇总"
echo "##########################################"
for r in "${RESULTS[@]}"; do
  echo "$r"
done
echo ""
echo "通过: $PASS / $((PASS + FAIL))"
echo ""

if [ $FAIL -eq 0 ]; then
  echo "全部集成测试通过"
  exit 0
else
  echo "$FAIL 项失败"
  exit 1
fi
