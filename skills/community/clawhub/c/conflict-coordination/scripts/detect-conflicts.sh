#!/bin/bash
# 机制冲突检测脚本 - 每周自动检测
# 检查 crontab、systemd、脚本、日志等潜在冲突

source /home/admin/.openclaw/workspace/scripts/task-utils.sh

WORKSPACE="/home/admin/.openclaw/workspace"
TASK_ID="conflict_detect_$(date +%Y%m%d_%H%M%S)"

# 初始化任务
task_init "$TASK_ID" "冲突检测" "检查机制间潜在冲突"
task_start "$TASK_ID"

log() {
    task_log "$TASK_ID" "INFO" "$1"
}

warn() {
    task_log "$TASK_ID" "WARN" "$1"
}

error() {
    task_log "$TASK_ID" "ERROR" "$1"
}

log "=========================================="
log "⚠️  机制冲突检测开始"
log "=========================================="

# 冲突计数器
CONFLICT_COUNT=0
WARNING_COUNT=0

# ============================================
# 1. 检查 crontab 冲突
# ============================================
task_stage "$TASK_ID" "检查 crontab 冲突" "running"
log "🔍 检查 crontab 配置..."

crontab_file=$(mktemp)
crontab -l > "$crontab_file" 2>/dev/null

if [ -s "$crontab_file" ]; then
    # 检查新闻推送任务
    news_count=$(grep -c "daily-news.sh" "$crontab_file" 2>/dev/null || echo 0)
    if [ "$news_count" -gt 1 ]; then
        warn "发现重复的新闻推送任务：$news_count 个"
        ((CONFLICT_COUNT++))
    else
        log "✅ 新闻推送任务：$news_count 个"
    fi
    
    # 检查健康检查任务
    health_count=$(grep -c "health-check\|maintenance.sh" "$crontab_file" 2>/dev/null || echo 0)
    if [ "$health_count" -gt 2 ]; then
        warn "健康检查任务过多：$health_count 个"
        ((WARNING_COUNT++))
    else
        log "✅ 健康检查任务：$health_count 个"
    fi
    
    # 检查 Git 推送任务
    git_push_count=$(grep -c "git-auto-push.sh" "$crontab_file" 2>/dev/null || echo 0)
    git_pull_count=$(grep -c "git pull" "$crontab_file" 2>/dev/null || echo 0)
    log "✅ Git 推送：$git_push_count 个，Git 拉取：$git_pull_count 个"
    
    # 检查备份任务
    backup_count=$(grep -c "backup.sh" "$crontab_file" 2>/dev/null || echo 0)
    log "✅ 备份任务：$backup_count 个"
else
    warn "crontab 为空或未配置"
    ((WARNING_COUNT++))
fi

rm -f "$crontab_file"
task_stage "$TASK_ID" "检查 crontab 冲突" "done"

# ============================================
# 2. 检查 systemd 服务冲突
# ============================================
task_stage "$TASK_ID" "检查 systemd 冲突" "running"
log "🔍 检查 systemd 服务..."

# 检查 sync 相关服务
sync_count=$(systemctl --user list-units 2>/dev/null | grep -c "sync.*service" || echo 0)
if [ "$sync_count" -gt 2 ]; then
    warn "同步服务过多：$sync_count 个"
    ((WARNING_COUNT++))
else
    log "✅ 同步服务：$sync_count 个"
fi

# 检查 openclaw 相关服务
openclaw_count=$(systemctl --user list-units 2>/dev/null | grep -c "openclaw.*service" || echo 0)
log "✅ OpenClaw 服务：$openclaw_count 个"

# 检查服务状态
gateway_status=$(systemctl --user is-active openclaw-gateway.service 2>/dev/null || echo "unknown")
sync_status=$(systemctl --user is-active sync-realtime.service 2>/dev/null || echo "unknown")

if [ "$gateway_status" = "active" ]; then
    log "✅ openclaw-gateway.service: $gateway_status"
else
    error "openclaw-gateway.service: $gateway_status"
    ((CONFLICT_COUNT++))
fi

if [ "$sync_status" = "active" ]; then
    log "✅ sync-realtime.service: $sync_status"
else
    warn "sync-realtime.service: $sync_status"
    ((WARNING_COUNT++))
fi

task_stage "$TASK_ID" "检查 systemd 冲突" "done"

# ============================================
# 3. 检查脚本功能重叠
# ============================================
task_stage "$TASK_ID" "检查脚本重叠" "running"
log "🔍 检查脚本功能重叠..."

# 检查 check-tasks.sh
if [ -f "$WORKSPACE/scripts/check-tasks.sh" ]; then
    log "ℹ️  check-tasks.sh 存在"
    log "💡 建议：审查是否与 task-utils 框架重复"
    ((WARNING_COUNT++))
fi

# 检查两个健康检查脚本
if [ -f "$WORKSPACE/scripts/system-health-check.sh" ] && \
   [ -f "$WORKSPACE/scripts/system-maintenance.sh" ]; then
    warn "发现两个健康检查脚本"
    log "💡 建议：统一使用 system-maintenance.sh"
    ((WARNING_COUNT++))
else
    log "✅ 健康检查脚本：单一"
fi

# 检查任务工具脚本
if [ -f "$WORKSPACE/scripts/task-utils.sh" ]; then
    log "✅ task-utils.sh 存在"
else
    error "task-utils.sh 不存在"
    ((CONFLICT_COUNT++))
fi

task_stage "$TASK_ID" "检查脚本重叠" "done"

# ============================================
# 4. 检查日志路径一致性
# ============================================
task_stage "$TASK_ID" "检查日志路径" "running"
log "🔍 检查日志路径..."

log_dirs=(
    "/home/admin/.openclaw/logs"
    "/home/admin/.openclaw/workspace/logs"
    "/home/admin/.openclaw/backups"
)

for dir in "${log_dirs[@]}"; do
    if [ -d "$dir" ]; then
        log_count=$(find "$dir" -name "*.log" -type f 2>/dev/null | wc -l)
        log "ℹ️  $dir: $log_count 个日志文件"
    fi
done

log "💡 建议：统一日志路径到 workspace/logs/"
((WARNING_COUNT++))

task_stage "$TASK_ID" "检查日志路径" "done"

# ============================================
# 5. 检查机制文档一致性
# ============================================
task_stage "$TASK_ID" "检查文档一致性" "running"
log "🔍 检查文档一致性..."

docs=(
    "任务保障机制:task-protection.md"
    "系统维护机制:系统维护机制.md"
    "知识库同步机制:知识库同步机制.md"
    "安全审计机制:安全审计机制.md"
    "自我进化机制:self-improvement-design.md"
    "冲突协调机制:机制冲突与协调说明.md"
)

for doc_pair in "${docs[@]}"; do
    doc_name="${doc_pair#*:}"
    doc_label="${doc_pair%%:*}"
    
    if [ -f "$WORKSPACE/docs/$doc_name" ]; then
        log "✅ $doc_label: $doc_name"
    else
        warn "$doc_label 文档缺失：$doc_name"
        ((WARNING_COUNT++))
    fi
done

task_stage "$TASK_ID" "检查文档一致性" "done"

# ============================================
# 6. 生成检测报告
# ============================================
task_stage "$TASK_ID" "生成检测报告" "running"

report_file="$WORKSPACE/learnings/improvements/$(date +%Y-%m-%d)-冲突检测报告.md"

cat > "$report_file" << EOF
# ⚠️  机制冲突检测报告

**生成时间**: $(date +%Y-%m-%d %H:%M)  
**检测范围**: crontab, systemd, 脚本，日志，文档

---

## 📊 检测摘要

| 类型 | 数量 |
|------|------|
| 🔴 冲突 | $CONFLICT_COUNT |
| 🟡 警告 | $WARNING_COUNT |

---

## 🔍 详细检查

### 1. Crontab 配置
- 新闻推送任务：$(grep -c "daily-news.sh" <(crontab -l 2>/dev/null) || echo 0) 个
- 健康检查任务：$(grep -c "health-check\|maintenance.sh" <(crontab -l 2>/dev/null) || echo 0) 个
- Git 推送任务：$(grep -c "git-auto-push.sh" <(crontab -l 2>/dev/null) || echo 0) 个
- Git 拉取任务：$(grep -c "git pull" <(crontab -l 2>/dev/null) || echo 0) 个
- 备份任务：$(grep -c "backup.sh" <(crontab -l 2>/dev/null) || echo 0) 个

### 2. Systemd 服务
- openclaw-gateway.service: $(systemctl --user is-active openclaw-gateway.service 2>/dev/null || echo "unknown")
- sync-realtime.service: $(systemctl --user is-active sync-realtime.service 2>/dev/null || echo "unknown")

### 3. 脚本功能
- check-tasks.sh: $([ -f "$WORKSPACE/scripts/check-tasks.sh" ] && echo "存在" || echo "不存在")
- system-health-check.sh: $([ -f "$WORKSPACE/scripts/system-health-check.sh" ] && echo "存在" || echo "不存在")
- system-maintenance.sh: $([ -f "$WORKSPACE/scripts/system-maintenance.sh" ] && echo "存在" || echo "不存在")
- task-utils.sh: $([ -f "$WORKSPACE/scripts/task-utils.sh" ] && echo "存在" || echo "不存在")

---

## 💡 改进建议

1. 审查 check-tasks.sh 是否与 task-utils 框架重复
2. 统一使用 system-maintenance.sh
3. 统一日志路径到 workspace/logs/

---

_生成者：虾球 🦐 | 冲突协调机制_
EOF

log "✅ 检测报告已生成：$report_file"
task_stage "$TASK_ID" "生成检测报告" "done"

# ============================================
# 7. 推送到飞书
# ============================================
task_stage "$TASK_ID" "飞书推送" "running"

if [ $CONFLICT_COUNT -gt 0 ]; then
    risk_level="🔴 发现冲突"
elif [ $WARNING_COUNT -gt 0 ]; then
    risk_level="🟡 存在警告"
else
    risk_level="🟢 无冲突"
fi

report="⚠️  机制冲突检测报告
**时间**: $(date +%Y-%m-%d)
**状态**: $risk_level

**统计**:
• 🔴 冲突：$CONFLICT_COUNT
• 🟡 警告：$WARNING_COUNT

**检查项目**:
• crontab 配置：✅
• systemd 服务：✅
• 脚本功能：✅
• 日志路径：✅
• 文档一致性：✅

**详情**: $report_file"

openclaw message send --channel feishu --target "user:g68578ee" --message "$report"

if [ $? -eq 0 ]; then
    log "✅ 飞书推送成功"
    task_stage "$TASK_ID" "飞书推送" "done"
else
    warn "❌ 飞书推送失败"
    task_stage "$TASK_ID" "飞书推送" "failed"
fi

# ============================================
# 完成任务
# ============================================
if [ $CONFLICT_COUNT -gt 0 ]; then
    task_fail "$TASK_ID" "发现 $CONFLICT_COUNT 个冲突"
else
    task_complete "$TASK_ID" "冲突检测完成，无冲突"
fi

log "=========================================="
log "⚠️  机制冲突检测结束"
log "=========================================="
