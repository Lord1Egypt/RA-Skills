#!/bin/bash
# POI Debug Orchestrator v0.2 — 执行脚本
# 用法：./poi-debug.sh <gsid> <poiid> [module] [env] [timeRange] [pageIndex]

set -e

GSID=$1
POIID=$2
MODULE=$3  # 新增：模块名或 sourceId
ENV=${4:-gray}
TIME_RANGE=${5:-1h ago}
PAGE_INDEX=${6:-2}  # 默认 pageIndex=2

if [ -z "$GSID" ] || [ -z "$POIID" ]; then
    echo "用法：$0 <gsid> <poiid> [module] [env] [timeRange] [pageIndex]"
    echo "示例：$0 31033080013090177494736367500059940538728 B0LR4UPN4M contentPerson gray 30m ago 2"
    exit 1
fi

APP="lse2-us-business-service"
INTERFACE="/search_business/process/middleLayer/poiDetail"
LOG_NAME="nginx_uni"
EMP_ID="501280"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_step() {
    echo -e "${BLUE}[$1]$NC $2"
}

log_success() {
    echo -e "${GREEN}✓$NC $1"
}

log_warn() {
    echo -e "${YELLOW}⚠$NC $1"
}

log_error() {
    echo -e "${RED}✗$NC $1"
}

echo ""
echo "========================================"
echo "  POI Debug Orchestrator v0.2"
echo "========================================"
echo "  GSID:     $GSID"
echo "  POIID:    $POIID"
echo "  MODULE:   ${MODULE:-auto}"
echo "  ENV:      $ENV"
echo "  Time:     $TIME_RANGE"
echo "  Page:     $PAGE_INDEX"
echo "========================================"
echo ""

# Step 0: 确定 sourceId
SOURCE_ID=""
if [ -n "$MODULE" ]; then
    log_step "0/6" "确定模块 sourceId..."
    
    # 先从映射表中查找
    MAP_FILE="$SCRIPT_DIR/../references/source_id_map.md"
    if [ -f "$MAP_FILE" ]; then
        SOURCE_ID=$(grep -E "^\|.*\|$MODULE" "$MAP_FILE" 2>/dev/null | head -1 | awk -F'|' '{print $3}' | tr -d ' ')
    fi
    
    if [ -z "$SOURCE_ID" ]; then
        # 如果模块名本身可能是 sourceId（如 contentPerson）
        SOURCE_ID="$MODULE"
    fi
    
    log_success "sourceId = $SOURCE_ID"
else
    log_step "0/6" "未指定模块，将查询所有相关日志..."
    SOURCE_ID=""
fi

# Step 1: 查日志
log_step "1/6" "查询 Loghouse 日志..."
log_success "查询条件：$LOG_QUERY"

# 构建查询条件
if [ -n "$SOURCE_ID" ]; then
    LOG_QUERY="${GSID} AND pageIndex=${PAGE_INDEX} AND ${SOURCE_ID} AND ${INTERFACE}"
    log_success "使用 sourceId 过滤：$SOURCE_ID"
else
    LOG_QUERY="${GSID} AND pageIndex=${PAGE_INDEX} AND ${INTERFACE}"
fi

LOG_RESULT=$(aone-kit call-tool loghouse-mcp::query_log "{
  \"app_name\": \"$APP\",
  \"log_name\": \"$LOG_NAME\",
  \"query\": \"$LOG_QUERY\",
  \"start_time\": \"$TIME_RANGE\",
  \"end_time\": \"now\",
  \"size\": 5,
  \"reverse\": true,
  \"emp_id\": \"$EMP_ID\"
}" 2>&1)

if [ $? -ne 0 ] || [ -z "$LOG_RESULT" ]; then
    log_error "日志查询失败"
    echo "原始响应：$LOG_RESULT"
    exit 1
fi

if [ $? -ne 0 ] || [ -z "$LOG_RESULT" ]; then
    log_error "日志查询失败"
    exit 1
fi

# 提取日志信息
LOG_COUNT=$(echo "$LOG_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo "0")

if [ "$LOG_COUNT" -eq 0 ]; then
    log_warn "未找到匹配日志，尝试扩大时间范围..."
    TIME_RANGE="4h ago"
    LOG_RESULT=$(aone-kit call-tool loghouse-mcp::query_log "{
      \"app_name\": \"$APP\",
      \"log_name\": \"$LOG_NAME\",
      \"query\": \"$LOG_QUERY\",
      \"start_time\": \"$TIME_RANGE\",
      \"end_time\": \"now\",
      \"size\": 5,
      \"reverse\": true,
      \"emp_id\": \"$EMP_ID\"
    }" 2>/dev/null)
    LOG_COUNT=$(echo "$LOG_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo "0")
fi

if [ "$LOG_COUNT" -eq 0 ]; then
    log_error "未找到任何日志，请检查 GSID 是否正确或时间范围是否太短"
    exit 1
fi

log_success "找到 $LOG_COUNT 条日志"

# 提取第一条日志的 URL 和 traceId
LOG_URL=$(echo "$LOG_RESULT" | python3 -c "
import sys, json
logs = json.load(sys.stdin)
if logs:
    url = logs[0].get('url', '')
    trace_id = logs[0].get('traceId', '')
    resp_time = logs[0].get('upstream_response_time', '')
    print(f'{url}|{trace_id}|{resp_time}')
" 2>/dev/null)

URL_PART=$(echo "$LOG_URL" | cut -d'|' -f1)
TRACE_ID=$(echo "$LOG_URL" | cut -d'|' -f2)
RESP_TIME=$(echo "$LOG_URL" | cut -d'|' -f3)

log_success "TraceID: $TRACE_ID | 耗时：${RESP_TIME}s"

# Step 2: 复现请求
log_step "2/5" "复现请求..."

# 替换内网 IP 为域名
if [ "$ENV" = "gray" ]; then
    TARGET_HOST="http://gray-us-business.amap.com"
else
    TARGET_HOST="http://us-business.amap.com"
fi

# 提取路径和参数（去掉协议和 IP）
URL_PATH=$(echo "$URL_PART" | sed -E 's|http://[0-9.]+||')
FULL_URL="${TARGET_HOST}${URL_PATH}"

# 发起请求
RESP_FILE="/tmp/poi_response_${GSID: -8}.json"
curl -s --max-time 30 "$FULL_URL" -o "$RESP_FILE" 2>/dev/null

if [ ! -s "$RESP_FILE" ]; then
    log_error "请求失败，响应为空"
    exit 1
fi

RESP_SIZE=$(wc -c < "$RESP_FILE")
log_success "请求成功 | 响应大小：${RESP_SIZE} bytes"

# Step 3: 解析返回
log_step "3/5" "解析响应..."

PARSE_RESULT=$(python3 << EOF
import json
import sys

try:
    with open('$RESP_FILE', 'r') as f:
        data = json.load(f)
    
    result = {'success': False, 'fields': {}, 'issues': []}
    
    # 检查响应结构
    if not data.get('success'):
        result['issues'].append('响应 success=false')
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)
    
    middle = data.get('data', {}).get('middleLayerStrategy', {})
    
    # 提取关键字段
    result['fields'] = {
        'shopSettlement': middle.get('shopSettlement'),
        'baseInfo': {
            'pcname': middle.get('baseInfo', {}).get('pcname'),
            'poiId': middle.get('baseInfo', {}).get('poiId'),
        },
        'shopBaseInfo': middle.get('shopBaseInfo'),
        'shopServiceInfo': middle.get('shopServiceInfo'),
    }
    
    # 检查异常
    shop_settlement = middle.get('shopSettlement')
    if not shop_settlement:
        result['issues'].append('shopSettlement 为空')
    elif not shop_settlement.get('shopId'):
        result['issues'].append('shopSettlement.shopId 为空')
    elif not shop_settlement.get('settlementRightInfo'):
        result['issues'].append('settlementRightInfo 为空')
    elif not shop_settlement.get('settlementRightInfo', {}).get('state'):
        result['issues'].append('settlementRightInfo.state 为空')
    
    result['success'] = True
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
except Exception as e:
    print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))
EOF
)

echo "$PARSE_RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('success'):
    issues = d.get('issues', [])
    if issues:
        print(f\"发现 {len(issues)} 个问题:\")
        for i, issue in enumerate(issues, 1):
            print(f\"  {i}. {issue}\")
    else:
        print('✓ 字段完整，无明显异常')
else:
    print(f\"解析失败：{d.get('error', 'unknown')}\")
"

# Step 4: 阅读代码
log_step "4/5" "定位相关代码..."

CODE_RESULT=$(aone-kit call-tool code::search_classes "{
  \"search\": \"ShopSettlementDTO\",
  \"repo\": \"gaode.search/us-business-service\",
  \"pageSize\": 1
}" 2>/dev/null)

if [ $? -eq 0 ] && [ -n "$CODE_RESULT" ]; then
    FILE_PATH=$(echo "$CODE_RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('list'):
    print(d['list'][0]['source']['file_path'])
" 2>/dev/null)
    
    if [ -n "$FILE_PATH" ]; then
        log_success "定位到：$FILE_PATH"
    else
        log_warn "未找到文件路径"
    fi
else
    log_warn "代码搜索失败"
fi

# Step 5: 生成报告
log_step "5/5" "生成排查报告..."

echo ""
echo "========================================"
echo "  📋 排查报告"
echo "========================================"
echo ""
echo "**GSID**: $GSID"
echo "**POIID**: $POIID"
echo "**TraceID**: $TRACE_ID"
echo "**环境**: $ENV"
echo ""
echo "### 日志查询"
echo "- 找到日志数：$LOG_COUNT"
echo "- 上游耗时：${RESP_TIME}s"
echo ""
echo "### 请求复现"
echo "- 目标地址：$TARGET_HOST"
echo "- 响应大小：$RESP_SIZE bytes"
echo ""
echo "### 响应解析"
echo "$PARSE_RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('success'):
    fields = d.get('fields', {})
    shop_settlement = fields.get('shopSettlement')
    if shop_settlement:
        print(f\"- shopSettlement.shopId: {shop_settlement.get('shopId', 'null')}\")
        state = shop_settlement.get('settlementRightInfo', {}).get('state', 'null')
        print(f\"- settlementRightInfo.state: {state}\")
    else:
        print('- shopSettlement: null')
    
    issues = d.get('issues', [])
    if issues:
        print()
        print('⚠️  异常字段:')
        for issue in issues:
            print(f'  - {issue}')
"
echo ""
echo "### 代码定位"
if [ -n "$FILE_PATH" ]; then
    echo "- 相关文件：\`$FILE_PATH\`"
    echo "- 命令：\`aone-kit call-tool code::get_single_file '{\"repo\": \"gaode.search/us-business-service\", \"filePath\": \"$FILE_PATH\"}'\`"
fi
echo ""
echo "### 建议操作"
echo "1. 如 shopSettlement 为空 → 检查商家入驻状态"
echo "2. 如 shopId 为空 → 检查 POI-Shop 绑定关系"
echo "3. 如字段缺失 → 查看代码逻辑或 AB 实验配置"
echo ""
echo "========================================"
echo ""

# 保存完整结果
RESULT_DIR="/tmp/poi-debug-results"
mkdir -p "$RESULT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULT_FILE="$RESULT_DIR/poi_debug_${GSID: -8}_${TIMESTAMP}.json"

python3 << EOF
import json

report = {
    'gsid': '$GSID',
    'poiid': '$POIID',
    'env': '$ENV',
    'trace_id': '$TRACE_ID',
    'log_count': $LOG_COUNT,
    'response_size': $RESP_SIZE,
    'parse_result': $PARSE_RESULT,
    'file_path': '$FILE_PATH',
    'timestamp': '$TIMESTAMP'
}

with open('$RESULT_FILE', 'w') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"完整结果已保存：$RESULT_FILE")
EOF

echo ""
log_success "排查完成！"
