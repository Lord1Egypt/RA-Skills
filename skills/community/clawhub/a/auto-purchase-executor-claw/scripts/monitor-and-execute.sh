#!/usr/bin/env bash
# monitor-and-execute.sh — 自动下单执行虾核心脚本
# 依赖: bash, curl, jq, python3, mysql-client
# 用法:
#   ./monitor-and-execute.sh monitor [--daemon]   启动监控
#   ./monitor-and-execute.sh execute --rule-id ID  手动执行单笔采购
#   ./monitor-and-execute.sh status               查看状态

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${SCRIPT_DIR}/../config"
LOG_FILE="${SCRIPT_DIR}/../logs/purchase.log"
PID_FILE="/tmp/auto-purchase-executor.pid"

# ── 日志 ──────────────────────────────────────────────────────────────────────
log() {
  local level="$1"; shift
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

# ── 数据库查询 ─────────────────────────────────────────────────────────────────
db_query() {
  mysql -h "${DB_HOST:-localhost}" -P "${DB_PORT:-3306}" \
        -u "${DB_USER}" -p"${DB_PASSWORD}" \
        "${DB_NAME}" -sN -e "$1" 2>/dev/null
}

# ── 飞书通知 ───────────────────────────────────────────────────────────────────
notify_feishu() {
  local title="$1" content="$2"
  if [[ -z "${FEISHU_WEBHOOK_URL:-}" ]]; then
    log "WARN" "FEISHU_WEBHOOK_URL 未配置，跳过通知"
    return 0
  fi
  curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
    -H "Content-Type: application/json" \
    -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"【自动采购通知】${title}\n${content}\"}}" \
    > /dev/null
}

# ── 查询供应商库存 ──────────────────────────────────────────────────────────────
check_supplier_inventory() {
  local supplier_id="$1" sku="$2"
  local config_file="${CONFIG_DIR}/suppliers.json"

  if [[ ! -f "$config_file" ]]; then
    log "ERROR" "供应商配置文件不存在: $config_file"
    return 1
  fi

  local api_url api_key
  api_url=$(jq -r ".\"${supplier_id}\".api_base_url" "$config_file")
  api_key_env=$(jq -r ".\"${supplier_id}\".api_key_env" "$config_file")
  api_key="${!api_key_env:-}"

  if [[ -z "$api_key" ]]; then
    log "ERROR" "供应商 ${supplier_id} API Key 未配置 (env: ${api_key_env})"
    return 1
  fi

  local mapped_sku
  mapped_sku=$(jq -r ".\"${supplier_id}\".sku_mapping.\"${sku}\"" "$config_file")

  curl -s -f "${api_url}/inventory?sku=${mapped_sku}" \
    -H "Authorization: Bearer ${api_key}" \
    -H "Content-Type: application/json"
}

# ── 生成采购订单 ───────────────────────────────────────────────────────────────
generate_order() {
  local rule_id="$1"
  local order_id="PO-$(date '+%Y%m%d')-$(shuf -i 1000-9999 -n 1)"

  log "INFO" "生成订单 ${order_id}，规则 ${rule_id}"

  # 从数据库读取规则详情
  local rule_json
  rule_json=$(db_query "SELECT rule_config FROM purchase_rules WHERE rule_id='${rule_id}' AND enabled=1 LIMIT 1")

  if [[ -z "$rule_json" ]]; then
    log "ERROR" "规则 ${rule_id} 不存在或已禁用"
    return 1
  fi

  echo "$rule_json" | python3 -c "
import sys, json, datetime

rule = json.load(sys.stdin)
order = {
    'order': {
        'external_order_id': '${order_id}',
        'rule_id': '${rule_id}',
        'created_at': datetime.datetime.now().isoformat(),
        'items': rule.get('items', []),
        'delivery': rule.get('delivery', {}),
        'payment': {
            'method': rule.get('payment_method', 'bank_transfer'),
            'currency': 'CNY'
        }
    }
}
print(json.dumps(order, ensure_ascii=False, indent=2))
"
}

# ── 执行支付 ───────────────────────────────────────────────────────────────────
execute_payment() {
  local order_json="$1" supplier_id="$2"
  local config_file="${CONFIG_DIR}/suppliers.json"
  local max_retries=3 retry=0

  local api_url api_key_env api_key
  api_url=$(jq -r ".\"${supplier_id}\".api_base_url" "$config_file")
  api_key_env=$(jq -r ".\"${supplier_id}\".api_key_env" "$config_file")
  api_key="${!api_key_env:-}"

  while [[ $retry -lt $max_retries ]]; do
    local response http_code
    response=$(curl -s -w "\n%{http_code}" -X POST "${api_url}/orders" \
      -H "Authorization: Bearer ${api_key}" \
      -H "Content-Type: application/json" \
      -d "$order_json")

    http_code=$(echo "$response" | tail -1)
    local body
    body=$(echo "$response" | head -n -1)

    case "$http_code" in
      200|201)
        log "INFO" "下单成功，HTTP ${http_code}"
        echo "$body"
        return 0
        ;;
      429|503)
        retry=$((retry + 1))
        local wait_sec=$((retry * 300))  # 5min, 10min, 15min
        log "WARN" "供应商限流/不可用 (${http_code})，${wait_sec}s 后重试 (${retry}/${max_retries})"
        sleep "$wait_sec"
        ;;
      *)
        log "ERROR" "下单失败，HTTP ${http_code}: ${body}"
        return 1
        ;;
    esac
  done

  log "ERROR" "重试 ${max_retries} 次后仍失败，放弃"
  return 1
}

# ── 检查触发条件 ───────────────────────────────────────────────────────────────
check_trigger_conditions() {
  log "INFO" "检查所有启用的采购规则..."

  local rules
  rules=$(db_query "SELECT rule_id, rule_name, trigger_condition, supplier_id, budget_per_order FROM purchase_rules WHERE enabled=1 ORDER BY priority ASC")

  if [[ -z "$rules" ]]; then
    log "INFO" "没有启用的采购规则"
    return 0
  fi

  while IFS=$'\t' read -r rule_id rule_name trigger_condition supplier_id budget_limit; do
    log "INFO" "检查规则 [${rule_id}] ${rule_name}"

    # 去重检查：60分钟内是否已执行
    local recent_count
    recent_count=$(db_query "SELECT COUNT(*) FROM purchase_orders WHERE rule_id='${rule_id}' AND created_at > DATE_SUB(NOW(), INTERVAL 60 MINUTE)")
    if [[ "${recent_count:-0}" -gt 0 ]]; then
      log "INFO" "规则 ${rule_id} 在去重窗口内已执行，跳过"
      continue
    fi

    # 评估触发条件（通过 Python 执行）
    local triggered
    triggered=$(python3 "${SCRIPT_DIR}/evaluate_condition.py" \
      --rule-id "$rule_id" \
      --condition "$trigger_condition" \
      --db-host "${DB_HOST:-localhost}" \
      --db-user "${DB_USER}" \
      --db-password "${DB_PASSWORD}" \
      --db-name "${DB_NAME}" 2>/dev/null || echo "false")

    if [[ "$triggered" == "true" ]]; then
      log "INFO" "规则 ${rule_id} 触发！执行采购..."
      execute_purchase "$rule_id" "$supplier_id" "$budget_limit"
    fi
  done <<< "$rules"
}

# ── 执行采购（完整流程）──────────────────────────────────────────────────────────
execute_purchase() {
  local rule_id="$1" supplier_id="$2" budget_limit="$3"

  # 生成订单
  local order_json
  order_json=$(generate_order "$rule_id") || {
    log "ERROR" "订单生成失败，规则 ${rule_id}"
    notify_feishu "❌ 订单生成失败" "规则 ${rule_id} 订单生成失败，请人工检查"
    return 1
  }

  # 预算校验
  local total_amount
  total_amount=$(echo "$order_json" | jq '[.order.items[].total_price] | add // 0')
  if (( $(echo "$total_amount > $budget_limit" | python3 -c "import sys; print(eval(sys.stdin.read()))") )); then
    log "WARN" "订单金额 ${total_amount} 超过预算上限 ${budget_limit}，暂停并通知财务"
    notify_feishu "⚠️ 采购预算超限" "规则 ${rule_id}\n订单金额: ¥${total_amount}\n预算上限: ¥${budget_limit}\n请财务审批后手动执行"
    return 1
  fi

  # 查询供应商库存
  local sku
  sku=$(echo "$order_json" | jq -r '.order.items[0].sku')
  local inventory_resp
  inventory_resp=$(check_supplier_inventory "$supplier_id" "$sku") || {
    log "WARN" "主供应商 ${supplier_id} 库存查询失败，尝试备选供应商"
    # TODO: 切换备选供应商逻辑
    return 1
  }

  local available_qty
  available_qty=$(echo "$inventory_resp" | jq -r '.available_quantity // 0')
  local need_qty
  need_qty=$(echo "$order_json" | jq '[.order.items[].quantity] | add // 0')

  if [[ "$available_qty" -lt "$need_qty" ]]; then
    log "WARN" "供应商 ${supplier_id} 库存不足 (需要: ${need_qty}, 可用: ${available_qty})"
    notify_feishu "⚠️ 供应商库存不足" "规则 ${rule_id}\n供应商: ${supplier_id}\n需要: ${need_qty}，可用: ${available_qty}"
    return 1
  fi

  # 执行支付
  local result
  result=$(execute_payment "$order_json" "$supplier_id") || {
    log "ERROR" "支付执行失败，规则 ${rule_id}"
    notify_feishu "❌ 采购支付失败" "规则 ${rule_id}\n供应商: ${supplier_id}\n请人工处理"
    return 1
  }

  # 记录订单到数据库
  local order_id
  order_id=$(echo "$order_json" | jq -r '.order.external_order_id')
  db_query "INSERT INTO purchase_orders (order_id, rule_id, supplier_id, amount, status, created_at) VALUES ('${order_id}', '${rule_id}', '${supplier_id}', ${total_amount}, 'success', NOW())"

  log "INFO" "采购成功！订单号: ${order_id}，金额: ¥${total_amount}"
  notify_feishu "✅ 自动采购成功" "订单号: ${order_id}\n规则: ${rule_id}\n供应商: ${supplier_id}\n金额: ¥${total_amount}"
}

# ── 主命令 ─────────────────────────────────────────────────────────────────────
CMD="${1:-help}"
shift || true

case "$CMD" in
  monitor)
    mkdir -p "$(dirname "$LOG_FILE")"
    if [[ "${1:-}" == "--daemon" ]]; then
      log "INFO" "以后台模式启动监控..."
      nohup bash "$0" monitor >> "$LOG_FILE" 2>&1 &
      echo $! > "$PID_FILE"
      log "INFO" "监控进程已启动，PID: $(cat "$PID_FILE")"
    else
      log "INFO" "启动监控循环（每5分钟检查一次）..."
      while true; do
        check_trigger_conditions
        sleep 300
      done
    fi
    ;;

  execute)
    RULE_ID=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --rule-id) RULE_ID="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    if [[ -z "$RULE_ID" ]]; then
      echo "用法: $0 execute --rule-id <RULE_ID>"
      exit 1
    fi
    log "INFO" "手动执行规则 ${RULE_ID}..."
    SUPPLIER_ID=$(db_query "SELECT supplier_id FROM purchase_rules WHERE rule_id='${RULE_ID}' LIMIT 1")
    BUDGET=$(db_query "SELECT budget_per_order FROM purchase_rules WHERE rule_id='${RULE_ID}' LIMIT 1")
    execute_purchase "$RULE_ID" "$SUPPLIER_ID" "${BUDGET:-999999}"
    ;;

  status)
    echo "=== 自动下单执行虾 状态 ==="
    if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
      echo "监控进程: 运行中 (PID: $(cat "$PID_FILE"))"
    else
      echo "监控进程: 未运行"
    fi
    echo ""
    echo "=== 最近10条执行记录 ==="
    db_query "SELECT order_id, rule_id, supplier_id, amount, status, created_at FROM purchase_orders ORDER BY created_at DESC LIMIT 10" | \
      column -t -s $'\t' 2>/dev/null || echo "(无记录或数据库未连接)"
    echo ""
    echo "=== 启用的规则 ==="
    db_query "SELECT rule_id, rule_name, priority, enabled FROM purchase_rules WHERE enabled=1 ORDER BY priority" | \
      column -t -s $'\t' 2>/dev/null || echo "(无规则或数据库未连接)"
    ;;

  *)
    echo "用法:"
    echo "  $0 monitor [--daemon]        启动监控（--daemon 后台运行）"
    echo "  $0 execute --rule-id <ID>    手动执行单笔采购"
    echo "  $0 status                    查看状态和最近记录"
    ;;
esac
