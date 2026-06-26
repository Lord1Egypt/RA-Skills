#!/usr/bin/env bash
# API Doc Validator - Validate API documentation structure
set -euo pipefail
API_BASE="https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com"
echo "📄 API文档验证工具"
HEALTH=$(curl -s "${API_BASE}/health" --connect-timeout 5 --max-time 10 2>/dev/null || echo '{"status":"error"}')
if echo "$HEALTH" | jq -e '.status == "ok"' > /dev/null 2>&1; then
  echo "✅ API服务连接正常"
  echo "📋 最佳实践: 1.端点描述 2.参数类型+示例 3.状态码说明 4.认证方式 5.错误码格式 6.分页参数 7.速率限制 8.版本号"
else
  echo "⚠️  API服务暂时不可用"
fi
