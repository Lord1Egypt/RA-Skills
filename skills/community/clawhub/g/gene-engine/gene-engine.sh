#!/bin/bash
# Gene Engine v1.0 - 自动执行Gene状态管理
# 在心跳时调用：bash ~/.openclaw/workspace/scripts/gene-engine.sh
# 输出：JSON格式的执行结果，供心跳流程读取

set -euo pipefail

GENE_FILE="$HOME/.openclaw/workspace/memory/gene-state.json"
NOW_EPOCH=$(date +%s)
NOW_ISO=$(TZ=Asia/Shanghai date +"%Y-%m-%dT%H:%M:%S+08:00")
CHANGES=()
WARNINGS=()

# 读取JSON
if [ ! -f "$GENE_FILE" ]; then
  echo '{"error": "gene-state.json not found"}'
  exit 1
fi

GENE_JSON=$(cat "$GENE_FILE")

# 辅助函数：计算天数差
days_since() {
  local iso_date="$1"
  if [ -z "$iso_date" ] || [ "$iso_date" = "null" ]; then
    echo "null"
    return
  fi
  local target_epoch
  target_epoch=$(date -d "$iso_date" +%s 2>/dev/null || echo "0")
  if [ "$target_epoch" = "0" ]; then
    echo "null"
    return
  fi
  echo $(( (NOW_EPOCH - target_epoch) / 86400 ))
}

# 辅助函数：更新JSON字段（用python3确保正确性）
update_gene() {
  local gene_key="$1"
  local field="$2"
  local value="$3"
  local is_number="${4:-false}"
  
  if [ "$is_number" = "true" ]; then
    GENE_JSON=$(echo "$GENE_JSON" | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['$gene_key']['$field'] = $value
json.dump(data, sys.stdout, ensure_ascii=False)
")
  else
    GENE_JSON=$(echo "$GENE_JSON" | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['$gene_key']['$field'] = '$value'
json.dump(data, sys.stdout, ensure_ascii=False)
")
  fi
}

# 辅助函数：更新JSON嵌套字段
update_gene_nested() {
  local gene_key="$1"
  local field1="$2"
  local field2="$3"
  local value="$4"
  local is_number="${5:-false}"
  
  if [ "$is_number" = "true" ]; then
    GENE_JSON=$(echo "$GENE_JSON" | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['$gene_key']['$field1']['$field2'] = $value
json.dump(data, sys.stdout, ensure_ascii=False)
")
  else
    GENE_JSON=$(echo "$GENE_JSON" | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['$gene_key']['$field1']['$field2'] = '$value'
json.dump(data, sys.stdout, ensure_ascii=False)
")
  fi
}

# 辅助函数：读取Gene字段
get_gene() {
  local gene_key="$1"
  local field="$2"
  echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('$field') or 'null')"
}

# 辅助函数：读取Gene嵌套字段
get_gene_nested() {
  local gene_key="$1"
  local field1="$2"
  local field2="$3"
  echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('$field1',{}).get('$field2') or 'null')"
}

echo "=== Gene Engine v1.0 启动 ==="
echo "时间: $NOW_ISO"
echo ""

# ============================================
# 1. 退役检查（checkDeprecation逻辑）
# ============================================
echo "--- 退役检查 ---"

for gene_key in _gene17_heartbeat_sampling  _gene24_three_layer_verification _gene25_activation_condition_check _gene26_learning_application_check; do
  # 读取Gene状态
  status=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('status','unknown'))")
  triggered_count=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('triggeredCount',0))")
  last_triggered=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('lastTriggered') or 'null')")
  last_verified=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('lastVerified') or 'null')")
  creation_date=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('creationDate') or 'null')")
  dep_unused=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('deprecationSignal',{}).get('triggeredButUnused',0))")
  dep_candidate=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('deprecationSignal',{}).get('retirementCandidate',False))")
  
  # 跳过internalized
  if [ "$status" = "internalized" ]; then
    echo "  $gene_key: internalized，跳过"
    continue
  fi
  
  # 计算天数（用creationDate或lastVerified作为参考）
  ref_date="$last_triggered"
  if [ "$ref_date" = "null" ] || [ "$ref_date" = "None" ]; then
    ref_date="$creation_date"
  fi
  if [ "$ref_date" = "null" ] || [ "$ref_date" = "None" ]; then
    ref_date="$last_verified"
  fi
  
  days=$(days_since "$ref_date")
  
  # 退役规则1：从未触发+创建超过30天
  if [ "$triggered_count" = "0" ] && [ "$days" != "null" ] && [ "$days" -gt 30 ]; then
    echo "  ⚠️ $gene_key: 创建${days}天从未触发 → 标记retirementCandidate"
    update_gene_nested "$gene_key" "deprecationSignal" "retirementCandidate" "true"
    CHANGES+=("$gene_key: retirementCandidate=true (${days}天未触发)")
  fi
  
  # 退役规则2：连续3次触发未改变判断
  if [ "$dep_unused" -ge 3 ] 2>/dev/null && [ "$dep_candidate" != "True" ]; then
    echo "  ⚠️ $gene_key: triggeredButUnused=$dep_unused → 标记retirementCandidate"
    update_gene_nested "$gene_key" "deprecationSignal" "retirementCandidate" "true"
    CHANGES+=("$gene_key: retirementCandidate=true (${dep_unused}次触发未改变判断)")
  fi
  
  # 退役规则3：连续5次触发未改变判断 → 自动归档
  if [ "$dep_unused" -ge 5 ] 2>/dev/null; then
    echo "  🚨 $gene_key: triggeredButUnused=$dep_unused → 自动归档"
    update_gene "$gene_key" "status" "archived"
    CHANGES+=("$gene_key: 自动归档 (${dep_unused}次触发未改变判断)")
  fi
  
  echo "  $gene_key: status=$status, days=$days, triggered=$triggered_count, unused=$dep_unused"
done

echo ""

# ============================================
# 2. 冷却期检查（cooldown逻辑）
# ============================================
echo "--- 冷却期检查 ---"

for gene_key in _gene17_heartbeat_sampling  _gene24_three_layer_verification _gene25_activation_condition_check _gene26_learning_application_check; do
  status=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('status','unknown'))")
  consecutive_failures=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('consecutiveFailures',0))")
  last_failure=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('lastFailure') or 'null')")
  total_failures=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('totalFailures',0))")
  
  # 连续失败3次 → 进入cooldown
  if [ "$consecutive_failures" -ge 3 ] 2>/dev/null && [ "$status" != "cooldown" ] && [ "$status" != "disabled" ] && [ "$status" != "archived" ] && [ "$status" != "internalized" ]; then
    echo "  ⚠️ $gene_key: consecutiveFailures=$consecutive_failures → 进入cooldown"
    update_gene "$gene_key" "status" "cooldown"
    CHANGES+=("$gene_key: status→cooldown (连续${consecutive_failures}次失败)")
  fi
  
  # 总失败10次 → 禁用
  if [ "$total_failures" -ge 10 ] 2>/dev/null && [ "$status" != "disabled" ] && [ "$status" != "archived" ] && [ "$status" != "internalized" ]; then
    echo "  🚨 $gene_key: totalFailures=$total_failures → 禁用"
    update_gene "$gene_key" "status" "disabled"
    CHANGES+=("$gene_key: status→disabled (总失败${total_failures}次)")
  fi
  
  # cooldown 72小时后恢复
  if [ "$status" = "cooldown" ] && [ "$last_failure" != "null" ] && [ "$last_failure" != "None" ]; then
    failure_days=$(days_since "$last_failure")
    if [ "$failure_days" != "null" ] && [ "$failure_days" -ge 3 ]; then
      echo "  ✅ $gene_key: cooldown已过${failure_days}天 → 恢复active"
      update_gene "$gene_key" "status" "active"
      update_gene "$gene_key" "consecutiveFailures" "0" "true"
      CHANGES+=("$gene_key: cooldown→active (冷却期结束)")
    fi
  fi
done

echo ""

# ============================================
# 3. 主动探测检查（active probing逻辑）
# ============================================
echo "--- 主动探测检查 ---"

# 定义探测阈值
declare -A PROBE_THRESHOLDS
PROBE_THRESHOLDS[_gene17_heartbeat_sampling]=14
PROBE_THRESHOLDS[_gene24_three_layer_verification]=7
PROBE_THRESHOLDS[_gene25_activation_condition_check]=3
PROBE_THRESHOLDS[_gene26_learning_application_check]=3

for gene_key in _gene17_heartbeat_sampling  _gene24_three_layer_verification _gene25_activation_condition_check _gene26_learning_application_check; do
  status=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('status','unknown'))")
  last_triggered=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('lastTriggered') or 'null')")
  last_verified=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('lastVerified') or 'null')")
  creation_date=$(echo "$GENE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['$gene_key'].get('creationDate') or 'null')")
  
  # 跳过非active/verified状态
  if [ "$status" != "active" ] && [ "$status" != "verified" ] && [ "$status" != "pending_verification" ]; then
    echo "  $gene_key: status=$status，跳过探测"
    continue
  fi
  
  # 计算天数
  ref_date="$last_triggered"
  if [ "$ref_date" = "null" ] || [ "$ref_date" = "None" ]; then
    ref_date="$creation_date"
  fi
  if [ "$ref_date" = "null" ] || [ "$ref_date" = "None" ]; then
    ref_date="$last_verified"
  fi
  
  days=$(days_since "$ref_date")
  threshold=${PROBE_THRESHOLDS[$gene_key]}
  
  if [ "$days" != "null" ] && [ "$days" -gt "$threshold" ]; then
    echo "  🔍 $gene_key: ${days}天未触发 (阈值${threshold}天) → 需要主动探测"
    WARNINGS+=("$gene_key: ${days}天未触发，需主动探测")
  else
    echo "  ✅ $gene_key: ${days}天未触发 (阈值${threshold}天) → 正常"
  fi
done

echo ""

# ============================================
# 4. 写回JSON + 更新时间戳
# ============================================
echo "--- 写回 ---"

# 更新_last_audit和_updated
GENE_JSON=$(echo "$GENE_JSON" | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['_last_audit'] = '$NOW_ISO'
data['_updated'] = '$NOW_ISO'
json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
")

echo "$GENE_JSON" > "$GENE_FILE"
echo "✅ gene-state.json 已更新"

echo ""

# ============================================
# 5. 输出摘要
# ============================================
echo "=== 执行摘要 ==="
echo "变更数: ${#CHANGES[@]}"
for change in "${CHANGES[@]}"; do
  echo "  • $change"
done

if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo ""
  echo "需要关注:"
  for warning in "${WARNINGS[@]}"; do
    echo "  ⚠️ $warning"
  done
fi

if [ ${#CHANGES[@]} -eq 0 ] && [ ${#WARNINGS[@]} -eq 0 ]; then
  echo "  ✅ 无变更，无警告，Gene系统健康"
fi

# ============================================
# 6. 验证间隔检查
# ============================================
echo ""
echo "--- 验证间隔检查 ---"

# 验证间隔（天）
declare -A VERIFY_INTERVALS
VERIFY_INTERVALS[_gene17_heartbeat_sampling]=90
VERIFY_INTERVALS[_gene24_three_layer_verification]=90
VERIFY_INTERVALS[_gene25_activation_condition_check]=90
VERIFY_INTERVALS[_gene26_learning_application_check]=30

for gene_key in _gene17_heartbeat_sampling  _gene24_three_layer_verification _gene25_activation_condition_check _gene26_learning_application_check; do
  status=$(get_gene "$gene_key" "status")
  last_verified=$(get_gene "$gene_key" "lastVerified")
  
  if [ "$status" = "internalized" ] || [ "$status" = "archived" ] || [ "$status" = "disabled" ]; then
    continue
  fi
  
  if [ "$last_verified" = "null" ] || [ "$last_verified" = "None" ]; then
    echo "  ⏰ $gene_key: 从未验证过"
    WARNINGS+=("$gene_key: 从未验证过")
    continue
  fi
  
  verify_days=$(days_since "$last_verified")
  interval=${VERIFY_INTERVALS[$gene_key]}
  
  if [ "$verify_days" != "null" ] && [ "$verify_days" -gt "$interval" ]; then
    echo "  ⏰ $gene_key: ${verify_days}天未验证 (间隔${interval}天) → 需要重新验证"
    WARNINGS+=("$gene_key: ${verify_days}天未验证，需重新验证")
  else
    echo "  ✅ $gene_key: ${verify_days}天未验证 (间隔${interval}天) → 正常"
  fi
done

# ============================================
# 7. wakeUpRate 计算
# ============================================
echo ""
echo "--- wakeUpRate ---"

for gene_key in _gene17_heartbeat_sampling _gene20_proactivity_layered  _gene24_three_layer_verification _gene25_activation_condition_check _gene26_learning_application_check; do
  status=$(get_gene "$gene_key" "status")
  triggered_count=$(get_gene "$gene_key" "triggeredCount")
  activation_count=$(get_gene "$gene_key" "activationCount")
  wake_up_rate=$(get_gene "$gene_key" "wakeUpRate")
  
  if [ "$status" = "internalized" ]; then
    echo "  $gene_key: internalized (已内化，无需计算)"
    continue
  fi
  
  if [ "$triggered_count" = "0" ] || [ "$triggered_count" = "null" ]; then
    echo "  $gene_key: 未触发过，wakeUpRate=N/A"
    continue
  fi
  
  if [ "$activation_count" = "null" ] || [ "$activation_count" = "None" ]; then
    activation_count=0
  fi
  
  # 计算唤醒率
  calculated_rate=$(python3 -c "tc=$triggered_count; ac=$activation_count; print(round(ac/tc, 2) if tc > 0 else 0)")
  
  # 如果JSON里的值和计算值不同，更新
  if [ "$wake_up_rate" != "$calculated_rate" ] && [ "$wake_up_rate" != "null" ]; then
    echo "  $gene_key: wakeUpRate $wake_up_rate → $calculated_rate (触发${triggered_count}次，改变判断${activation_count}次)"
    update_gene "$gene_key" "wakeUpRate" "$calculated_rate" "true"
    CHANGES+=("$gene_key: wakeUpRate→$calculated_rate")
  else
    echo "  $gene_key: wakeUpRate=$calculated_rate (触发${triggered_count}次，改变判断${activation_count}次)"
  fi
done

# ============================================
# 8. 总状态报告
# ============================================
echo ""
echo "=== Gene系统状态报告 ==="

echo ""
echo "变更数: ${#CHANGES[@]}"
for change in "${CHANGES[@]}"; do
  echo "  • $change"
done

if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo ""
  echo "需要关注:"
  for warning in "${WARNINGS[@]}"; do
    echo "  ⚠️ $warning"
  done
fi

if [ ${#CHANGES[@]} -eq 0 ] && [ ${#WARNINGS[@]} -eq 0 ]; then
  echo "  ✅ 无变更，无警告，Gene系统健康"
fi

# ============================================
# 9. 健康分数计算
# ============================================
echo ""
echo "--- 健康分数 ---"

HEALTH_SCORE=100
HEALTH_DETAILS=()

for gene_key in _gene17_heartbeat_sampling  _gene24_three_layer_verification _gene25_activation_condition_check _gene26_learning_application_check; do
  status=$(get_gene "$gene_key" "status")
  wake_up_rate=$(get_gene "$gene_key" "wakeUpRate")
  last_triggered=$(get_gene "$gene_key" "lastTriggered")
  last_verified=$(get_gene "$gene_key" "lastVerified")
  creation_date=$(get_gene "$gene_key" "creationDate")
  
  short_name=$(echo "$gene_key" | sed 's/_gene[0-9]*_//')
  
  # 计算天数
  ref_date="$last_triggered"
  if [ "$ref_date" = "null" ] || [ "$ref_date" = "None" ]; then
    ref_date="$creation_date"
  fi
  if [ "$ref_date" = "null" ] || [ "$ref_date" = "None" ]; then
    ref_date="$last_verified"
  fi
  days=$(days_since "$ref_date")
  
  # 扣分规则
  # 1. 非正常状态扣分
  case "$status" in
    cooldown) HEALTH_SCORE=$((HEALTH_SCORE - 15)); HEALTH_DETAILS+=("$short_name: cooldown (-15)");;
    disabled) HEALTH_SCORE=$((HEALTH_SCORE - 25)); HEALTH_DETAILS+=("$short_name: disabled (-25)");;
    archived) HEALTH_SCORE=$((HEALTH_SCORE - 20)); HEALTH_DETAILS+=("$short_name: archived (-20)");;
    pending_verification) HEALTH_SCORE=$((HEALTH_SCORE - 5)); HEALTH_DETAILS+=("$short_name: pending_verification (-5)");;
  esac
  
  # 2. 长时间未触发扣分
  if [ "$days" != "null" ] && [ "$days" -gt 14 ]; then
    penalty=$(( days / 7 ))
    if [ "$penalty" -gt 10 ]; then penalty=10; fi
    HEALTH_SCORE=$((HEALTH_SCORE - penalty))
    HEALTH_DETAILS+=("$short_name: ${days}天未触发 (-$penalty)")
  fi
  
  # 3. 唤醒率低扣分
  if [ "$wake_up_rate" != "null" ] && [ "$wake_up_rate" != "None" ] && [ "$wake_up_rate" != "N/A" ]; then
    rate_int=$(python3 -c "print(int(float('$wake_up_rate') * 100))")
    if [ "$rate_int" -lt 50 ]; then
      HEALTH_SCORE=$((HEALTH_SCORE - 10))
      HEALTH_DETAILS+=("$short_name: 唤醒率${rate_int}% (-10)")
    fi
  fi
done

# 加分规则
# 有verified的Gene加分
verified_count=$(echo "$GENE_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(1 for k in d if k.startswith('_gene') and d[k].get('status')=='verified'))")
HEALTH_SCORE=$((HEALTH_SCORE + verified_count * 3))
if [ "$verified_count" -gt 0 ]; then
  HEALTH_DETAILS+=("${verified_count}个verified Gene (+$((verified_count * 3)))")
fi

# 限制在0-100
if [ "$HEALTH_SCORE" -lt 0 ]; then HEALTH_SCORE=0; fi
if [ "$HEALTH_SCORE" -gt 100 ]; then HEALTH_SCORE=100; fi

# 输出
if [ "$HEALTH_SCORE" -ge 80 ]; then
  HEALTH_GRADE="A"
  HEALTH_EMOJI="🟢"
elif [ "$HEALTH_SCORE" -ge 60 ]; then
  HEALTH_GRADE="B"
  HEALTH_EMOJI="🟡"
elif [ "$HEALTH_SCORE" -ge 40 ]; then
  HEALTH_GRADE="C"
  HEALTH_EMOJI="🟠"
else
  HEALTH_GRADE="D"
  HEALTH_EMOJI="🔴"
fi

echo "  ${HEALTH_EMOJI} 健康分数: ${HEALTH_SCORE}/100 (等级: ${HEALTH_GRADE})"
for detail in "${HEALTH_DETAILS[@]}"; do
  echo "    $detail"
done

# ============================================
# 10. 指标日志（追加到metrics.log）
# ============================================
METRICS_LOG="$HOME/.openclaw/workspace/memory/gene-metrics.log"

# 计算汇总指标
total_genes=$(echo "$GENE_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(1 for k in d if k.startswith('_gene')))")
active_genes=$(echo "$GENE_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(1 for k in d if k.startswith('_gene') and d[k].get('status') in ('active','verified','pending_verification')))")
total_triggers=$(echo "$GENE_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(d[k].get('triggeredCount',0) for k in d if k.startswith('_gene')))")
total_failures=$(echo "$GENE_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(d[k].get('totalFailures',0) for k in d if k.startswith('_gene')))")

# 追加日志
echo "${NOW_ISO} | score=${HEALTH_SCORE} grade=${HEALTH_GRADE} genes=${total_genes} active=${active_genes} triggers=${total_triggers} failures=${total_failures} changes=${#CHANGES[@]} warnings=${#WARNINGS[@]}" >> "$METRICS_LOG"

# ============================================
# 11. JSON摘要输出（机器可读）
# ============================================
echo ""
echo "--- JSON摘要 ---"

python3 -c "
import json, sys

summary = {
  'timestamp': '$NOW_ISO',
  'health_score': $HEALTH_SCORE,
  'health_grade': '$HEALTH_GRADE',
  'changes': ${#CHANGES[@]},
  'warnings': ${#WARNINGS[@]},
  'genes': {}
}

with open('$GENE_FILE') as f:
    data = json.load(f)

for key in data:
    if not key.startswith('_gene'):
        continue
    gene = data[key]
    short = key.replace('_gene', '').split('_', 1)[1] if '_' in key else key
    summary['genes'][short] = {
        'status': gene.get('status'),
        'triggered': gene.get('triggeredCount', 0),
        'wakeUpRate': gene.get('wakeUpRate'),
        'failures': gene.get('totalFailures', 0)
    }

print(json.dumps(summary, ensure_ascii=False, indent=2))
"

# ============================================
# 12. 自动提醒（有警告时输出提醒文案）
# ============================================
if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo ""
  echo "--- 自动提醒 ---"
  ALERT_TEXT="Gene系统需要关注："
  for warning in "${WARNINGS[@]}"; do
    ALERT_TEXT="${ALERT_TEXT}\n⚠️ $warning"
  done
  ALERT_TEXT="${ALERT_TEXT}\n健康分数: ${HEALTH_SCORE}/100 (${HEALTH_GRADE})"
  echo -e "$ALERT_TEXT"
  echo ""
  echo "💡 提醒文案已生成，可由心跳流程发送给老大"
fi

echo ""
echo "=== Gene Engine 完成 ==="
