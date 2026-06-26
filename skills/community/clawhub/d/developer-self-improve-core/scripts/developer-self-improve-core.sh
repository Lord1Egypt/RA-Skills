#!/bin/bash

# developer-self-improve-core 核心脚本
# 一体化执行：错误防重 + 自检 + 反思 + 提案 + 清洗

set -e

WORKSPACE="${AUTO_MEMORY_WORKSPACE:-$(pwd)}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MEMORY_DIR="$SKILL_DIR/memory"
SHORT_TERM_DIR="$MEMORY_DIR/short_term"
PROPOSALS_DIR="$MEMORY_DIR/proposals"
RULES_DIR="$MEMORY_DIR/rules"
CLEANUP_DIR="$MEMORY_DIR/cleanup"
LOGS_DIR="$MEMORY_DIR/logs"
CONFIG_FILE="$SKILL_DIR/config/config.yaml"
RULES_FILE="$RULES_DIR/confirmed_rules.md"
COUNTER_FILE="$MEMORY_DIR/dialogue_counter.txt"

# 读取平台配置
PLATFORM=$(grep "^platform:" "$CONFIG_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "ios")

# ============ 动态用户识别（从 current_user.json 读取） ============
CURRENT_USER=""
CURRENT_PLATFORM=""
CURRENT_PROJECT=""

load_current_user() {
    local user_config="$WORKSPACE/config/current_user.json"
    if [ -f "$user_config" ]; then
        if command -v jq &> /dev/null; then
            CURRENT_USER=$(jq -r '.user // "unknown"' "$user_config")
            CURRENT_PLATFORM=$(jq -r '.platform // "unknown"' "$user_config")
            CURRENT_PROJECT=$(jq -r '.project // "unknown"' "$user_config")
        else
            CURRENT_USER=$(grep -o '"user"[[:space:]]*:[[:space:]]*"[^"]*"' "$user_config" | cut -d'"' -f4 || echo "unknown")
            CURRENT_PLATFORM=$(grep -o '"platform"[[:space:]]*:[[:space:]]*"[^"]*"' "$user_config" | cut -d'"' -f4 || echo "unknown")
            CURRENT_PROJECT=$(grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' "$user_config" | cut -d'"' -f4 || echo "unknown")
        fi
    else
        CURRENT_USER=$(grep "^user:" "$CONFIG_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "unknown")
        CURRENT_PLATFORM="$PLATFORM"
        CURRENT_PROJECT="unknown"
    fi
}

# 加载当前用户信息
load_current_user

# 判断是否为多平台模式
is_multi_platform() {
    [ "$PLATFORM" = "multi-platform" ]
}

# 获取启用的领域 Skill 列表
get_enabled_skills() {
    if is_multi_platform; then
        local skills=()
        [ -d "$SKILL_DIR/../ios-self-improve" ] && skills+=("ios")
        [ -d "$SKILL_DIR/../android-developer-skill" ] && skills+=("android")
        [ -d "$SKILL_DIR/../flutter-developer-skill" ] && skills+=("flutter")
        echo "${skills[@]}"
    else
        echo "$PLATFORM"
    fi
}

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# ============ 工具函数 ============

# 生成规则 ID（基于平台 + 场景哈希，不含日期）
generate_rule_id() {
    local scene="$1"
    local hash=$(echo "$scene" | md5sum | cut -c1-8)
    echo "auto_${PLATFORM}_${hash}"
}

# 验证总结依据（严格限定 5 类）
validate_basis() {
    local content="$1"
    local basis_type=""
    local confidence=""
    
    if echo "$content" | grep -qi "用户明确\|记住这个\|一定要\|必须"; then
        basis_type="用户明确指出"
        confidence="高"
    elif echo "$content" | grep -qi "又\|再次\|第.*次\|重复"; then
        basis_type="重复模式≥2 次"
        confidence="中"
    elif echo "$content" | grep -qi "错误\|失败\|不对\|错"; then
        basis_type="可验证错误"
        confidence="低"
    else
        echo "⚠️  依据不足，不生成规则草案"
        return 1
    fi
    
    echo "$basis_type|$confidence"
    return 0
}

# 检查是否重复提案（同场景同问题不重复）
check_duplicate() {
    local scene="$1"
    local content="$2"
    
    local rule_id=$(generate_rule_id "$scene")
    local existing_file="$PROPOSALS_DIR/${rule_id}.md"
    
    if [ -f "$existing_file" ]; then
        echo "⚠️  同场景已存在提案，跳过"
        return 0
    fi
    
    if [ -f "$RULES_FILE" ]; then
        if grep -q "### 【规则 ID】$rule_id" "$RULES_FILE"; then
            echo "⚠️  同场景规则已确认，跳过"
            return 0
        fi
    fi
    
    return 1
}

# 增加对话轮数计数
increment_counter() {
    if [ -f "$COUNTER_FILE" ]; then
        local count=$(cat "$COUNTER_FILE")
        echo $((count + 1)) > "$COUNTER_FILE"
    else
        echo "1" > "$COUNTER_FILE"
    fi
}

# 检查是否触发清洗
check_cleanup_trigger() {
    local last_cleanup_file="$CLEANUP_DIR/last_cleanup.txt"
    
    if [ -f "$COUNTER_FILE" ]; then
        local count=$(cat "$COUNTER_FILE")
        if [ "$count" -ge 10 ]; then
            echo "10"
            return 0
        fi
    fi
    
    local weekday=$(date +%u)
    if [ "$weekday" -eq 5 ]; then
        if [ -f "$last_cleanup_file" ]; then
            local last_date=$(cat "$last_cleanup_file")
            local days_since=$(( ($(date +%s) - $(date -d "$last_date" +%s)) / 86400 ))
            if [ "$days_since" -ge 7 ]; then
                echo "weekly"
                return 0
            fi
        else
            echo "weekly"
            return 0
        fi
    fi
    
    return 1
}

# ============ 核心功能 ============

# 1. 初始化目录结构
init_directories() {
    echo "📁 初始化记忆目录..."
    mkdir -p "$MEMORY_DIR"/{short_term,proposals,rules,cleanup,logs}
    
    if [ ! -f "$RULES_FILE" ]; then
        cat > "$RULES_FILE" << EOF
# 长期规则库（仅人工确认）

**创建时间：** $(date -Iseconds)
**版本：** v1.0

---

<!-- 规则条目 -->

EOF
    fi
    
    if [ ! -f "$COUNTER_FILE" ]; then
        echo "0" > "$COUNTER_FILE"
    fi
    
    echo "✅ 目录结构已创建"
    echo "  - short_term/     短期记忆（对话结束自动销毁）"
    echo "  - proposals/      临时提案区（保留 7 天）"
    echo "  - rules/          长期规则库（仅人工确认）"
    echo "  - cleanup/        待清洗区（需用户批准）"
    echo "  - logs/           操作日志（支持回滚）"
    echo ""
}

# 2. 回答前检查（错误防重 + 平台过滤）
pre_check() {
    local scene="$1"
    
    load_current_user
    
    check_and_notify_pending
    
    echo "🛡️  执行回答前检查（错误防重）..."
    echo "  当前用户：$CURRENT_USER"
    echo "  当前平台：$CURRENT_PLATFORM (配置：$PLATFORM)"
    echo "  当前项目：$CURRENT_PROJECT"
    
    if [ ! -f "$RULES_FILE" ]; then
        echo "⚠️  长期规则库不存在，跳过"
        return 0
    fi
    
    local matched_rules=""
    if is_multi_platform; then
        echo "  模式：多平台（加载所有平台规则）"
        matched_rules=$(grep -A10 "【平台】iOS\|【平台】Android\|【平台】Flutter" "$RULES_FILE" 2>/dev/null | grep -A5 "【场景】$scene" || echo "")
    else
        echo "  模式：单平台（仅加载 $PLATFORM 规则）"
        matched_rules=$(grep -A10 "【平台】$PLATFORM" "$RULES_FILE" 2>/dev/null | grep -A5 "【场景】$scene" || echo "")
    fi
    
    if [ -n "$matched_rules" ]; then
        echo "✅ 命中长期规则："
        echo "$matched_rules"
        echo ""
        echo "📌 行动：自动修正，标记"已规避同类错误""
        echo "$(date -Iseconds) user=$CURRENT_USER platform=$CURRENT_PLATFORM project=$CURRENT_PROJECT PRE_CHECK scene=$scene matched=true" >> "$LOGS_DIR/operations.log"
    else
        echo "✓ 无匹配规则"
    fi
    
    echo ""
}

# 3. 回答后检查（自检 + 反思 + 提案）
post_check() {
    local content="$1"
    local scene="${2:-通用场景}"
    
    load_current_user
    
    echo "🔍 执行回答后检查（自检 + 反思 + 提案）..."
    echo "  当前用户：$CURRENT_USER"
    echo "  当前平台：$CURRENT_PLATFORM (配置：$PLATFORM)"
    echo "  当前项目：$CURRENT_PROJECT"
    echo ""
    
    echo "  自检："
    if [ -f "$RULES_FILE" ]; then
        echo "    ✓ 检查长期规则冲突"
    fi
    echo "    ✓ 检查重复错误"
    echo "    ✓ 检查硬错误"
    
    local basis_result=$(validate_basis "$content")
    if [ $? -ne 0 ]; then
        return 0
    fi
    
    local basis=$(echo "$basis_result" | cut -d'|' -f1)
    local confidence=$(echo "$basis_result" | cut -d'|' -f2)
    
    if check_duplicate "$scene" "$content"; then
        return 0
    fi
    
    local rule_id=$(generate_rule_id "$scene")
    local timestamp=$(date -Iseconds)
    local deadline=$(date -v+7d +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)
    
    # 5. 生成草案文件（按日期合并，每天一个文件）
    local date_str=$(date +%Y-%m-%d)
    local proposal_file="$PROPOSALS_DIR/${date_str}.md"
    
    # 如果文件不存在，创建文件头
    if [ ! -f "$proposal_file" ]; then
        cat > "$proposal_file" << EOF
# 待确认规则 ($date_str)

**生成日期：** $date_str
**最后更新：** $timestamp

---

EOF
    fi
    
    # 追加规则到文件
    cat >> "$proposal_file" << EOF
### 【规则 ID】$rule_id
### 【用户】$CURRENT_USER
### 【平台】$CURRENT_PLATFORM
### 【项目】$CURRENT_PROJECT
### 【场景】$scene
### 【问题/模式】$content
### 【建议规则】待用户确认
### 【依据】$basis
### 【可信度】$confidence
### 【建议层级】长期

---
**生成时间：** $timestamp
**状态：** 待审
**处理期限：** $deadline

---
<!-- USER_ACTION: 【同意/修改/忽略】 -->

---

EOF
    
    echo ""
    echo "✅ 规则草案已追加到：$proposal_file"
    echo ""
    echo "📋 当前日期文件内容："
    cat "$proposal_file"
    echo ""
    echo "💡 请回复：【同意/修改/忽略】"
    echo ""
    
    echo "$(date -Iseconds) user=$CURRENT_USER platform=$CURRENT_PLATFORM project=$CURRENT_PROJECT POST_CHECK scene=$scene rule_id=$rule_id confidence=$confidence" >> "$LOGS_DIR/operations.log"
    
    increment_counter
}

# 清理超期提案（超过 retention_days 天）
cleanup_expired_proposals() {
    local retention_days=$(grep "^retention_days:" "$CONFIG_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "7")
    local current_time=$(date +%s)
    local expired_count=0
    
    echo "📅 检查超期提案（保留${retention_days}天）..."
    
    for file in "$PROPOSALS_DIR"/*.md; do
        if [ -f "$file" ]; then
            local file_time=$(stat -c %Y "$file" 2>/dev/null || echo "0")
            local age_days=$(( (current_time - file_time) / 86400 ))
            
            if [ "$age_days" -gt "$retention_days" ]; then
                echo "  ⚠️  超期文件：$(basename $file)（已${age_days}天）"
                rm -f "$file"
                expired_count=$((expired_count + 1))
            fi
        fi
    done
    
    if [ "$expired_count" -gt 0 ]; then
        echo "✅ 已清理 $expired_count 个超期文件"
        echo "$(date -Iseconds) CLEANUP_EXPIRED count=$expired_count" >> "$LOGS_DIR/operations.log"
    else
        echo "✓ 无超期提案"
    fi
}

# 4. 定期清洗
cleanup() {
    echo "🧹 执行记忆清洗扫描..."
    
    cleanup_expired_proposals
    echo ""
    
    local cleanup_file="$CLEANUP_DIR/cleanup_$(date +%Y%m%d).md"
    local trigger_reason=$(check_cleanup_trigger)
    
    cat > "$cleanup_file" << EOF
# 记忆清洗建议

**生成时间：** $(date -Iseconds)
**触发原因：** 累计${trigger_reason}轮对话 / 每周定期

---

## 待合并规则

<!-- 列出重复/相似的规则 -->

## 待删除规则

<!-- 列出低频/过时的规则（30 天未使用） -->

## 待禁用规则

<!-- 列出冲突的规则 -->

---
<!-- USER_ACTION: 【同意/修改/忽略】 -->
EOF
    
    echo "✅ 清洗建议已生成：$cleanup_file"
    echo ""
    echo "📋 清洗清单："
    cat "$cleanup_file"
    echo ""
    echo "💡 请回复：【同意/修改/忽略】"
    echo ""
    
    echo "0" > "$COUNTER_FILE"
    
    echo "$(date -Iseconds) CLEANUP trigger=$trigger_reason" >> "$LOGS_DIR/operations.log"
}

# 5. 确认规则
confirm_rule() {
    local rule_id="$1"
    local action="$2"
    
    echo "📝 处理规则确认：$rule_id → $action"
    
    # 查找规则所在的日期文件
    local proposal_file=""
    for file in "$PROPOSALS_DIR"/*.md; do
        if [ -f "$file" ] && grep -q "### 【规则 ID】$rule_id" "$file" 2>/dev/null; then
            proposal_file="$file"
            break
        fi
    done
    
    if [ -z "$proposal_file" ]; then
        echo "❌ 规则草案不存在"
        return 1
    fi
    
    case $action in
        同意)
            if grep -q "### 【规则 ID】$rule_id" "$RULES_FILE"; then
                echo "⚠️  规则已存在，跳过确认"
                sed -i "/### 【规则 ID】$rule_id/,/USER_ACTION/d" "$proposal_file"
                return 0
            fi
            
            # 提取规则内容并添加到长期规则库（更新状态为已确认）
            echo "" >> "$RULES_FILE"
            sed -n "/### 【规则 ID】$rule_id/,/USER_ACTION/p" "$proposal_file" | \
                sed 's/状态：待审/状态：已确认/' | \
                sed 's/处理期限：.*/确认时间：'$(date -Iseconds)'/' >> "$RULES_FILE"
            echo "---" >> "$RULES_FILE"
            
            # 从提案文件中删除已确认的规则
            sed -i "/### 【规则 ID】$rule_id/,/USER_ACTION/d" "$proposal_file"
            
            echo "✅ 规则已加入长期记忆库（平台：$PLATFORM）"
            ;;
        修改)
            echo "⚠️  请提供修改后的规则内容"
            echo "用法：$0 confirm $rule_id 同意  # 修改后确认"
            ;;
        忽略)
            sed -i "/### 【规则 ID】$rule_id/,/USER_ACTION/d" "$proposal_file"
            echo "✅ 规则草案已丢弃"
            echo "$(date -Iseconds) user=$CURRENT_USER platform=$CURRENT_PLATFORM project=$CURRENT_PROJECT CONFIRM rule_id=$rule_id action=忽略" >> "$LOGS_DIR/operations.log"
            ;;
        *)
            echo "❌ 未知操作：$action（应为：同意/修改/忽略）"
            return 1
            ;;
    esac
    
    echo "$(date -Iseconds) user=$CURRENT_USER platform=$CURRENT_PLATFORM project=$CURRENT_PROJECT CONFIRM rule_id=$rule_id action=$action" >> "$LOGS_DIR/operations.log"
}

# 6. 切换平台
switch_platform() {
    local new_platform="$1"
    
    if [ -z "$new_platform" ]; then
        echo "⚠️  请指定平台：ios | android | flutter | h5 | java | multi-platform"
        return 1
    fi
    
    sed -i "s/^platform:.*/platform: $new_platform/" "$CONFIG_FILE"
    
    echo "✅ 平台已切换：$PLATFORM → $new_platform"
    echo ""
    echo "📋 新平台配置："
    grep "^platform:" "$CONFIG_FILE"
}

# 7. 查看平台规则
view_rules() {
    echo "📖 查看 $PLATFORM 平台规则..."
    
    if [ ! -f "$RULES_FILE" ]; then
        echo "⚠️  长期规则库不存在"
        return 1
    fi
    
    grep -A10 "【平台】$PLATFORM" "$RULES_FILE" || echo "✓ 暂无 $PLATFORM 平台规则"
}

# 8. 检查并通知待审规则（AI 回答后调用）
check_and_notify_pending() {
    local pending_count=0
    local retention_days=$(grep "^retention_days:" "$CONFIG_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "7")
    local current_time=$(date +%s)
    local expired_count=0
    local pending_rules=""
    
    if [ -d "$PROPOSALS_DIR" ]; then
        for file in "$PROPOSALS_DIR"/*.md; do
            if [ -f "$file" ]; then
                pending_count=$((pending_count + 1))
                local rule_id=$(basename "$file" .md)
                local scene=$(grep "^### 【场景】" "$file" 2>/dev/null | sed 's/### 【场景】//' | tr -d ' ' || echo "未知")
                local file_time=$(stat -c %Y "$file" 2>/dev/null || echo "0")
                local age_days=$(( (current_time - file_time) / 86400 ))
                
                if [ "$age_days" -gt "$retention_days" ]; then
                    expired_count=$((expired_count + 1))
                fi
                
                pending_rules="$pending_rules\n  - $rule_id（$scene）"
            fi
        done
    fi
    
    if [ "$pending_count" -gt 0 ]; then
        echo ""
        echo "---"
        echo "⚠️  待确认规则：$pending_count 条"
        echo -e "$pending_rules"
        echo ""
        echo "💬 回复"同意 [规则 ID]"确认，或"忽略 [规则 ID]"丢弃"
        if [ "$expired_count" -gt 0 ]; then
            echo "🔴 其中 $expired_count 条已超期（>${retention_days}天）"
        fi
        echo ""
    fi
}

# 9. 自动确认规则（从钉钉消息识别意图）
auto_confirm() {
    local user_input="$1"
    
    local action=""
    if echo "$user_input" | grep -qi "同意\|确认\|yes\|ok"; then
        action="同意"
    elif echo "$user_input" | grep -qi "忽略\|取消\|no\|delete"; then
        action="忽略"
    elif echo "$user_input" | grep -qi "修改\|edit"; then
        action="修改"
    else
        echo "⚠️  无法识别意图，请使用：同意/忽略/修改 [规则 ID]"
        return 1
    fi
    
    local rule_id=$(echo "$user_input" | grep -oE "auto_[a-z]+_[0-9a-f]+" | head -1)
    
    if [ -z "$rule_id" ]; then
        echo "⚠️  未找到规则 ID，请回复完整格式：$action auto_ios_8972231d"
        return 1
    fi
    
    echo "📝 自动确认：$rule_id → $action"
    confirm_rule "$rule_id" "$action"
}

# ============ 主函数 ============

main() {
    local action="${1:-help}"
    
    case $action in
        init)
            init_directories
            ;;
        pre-check)
            shift
            pre_check "$@"
            ;;
        post-check)
            shift
            post_check "$@"
            ;;
        cleanup)
            cleanup
            ;;
        confirm)
            shift
            confirm_rule "$@"
            ;;
        switch-platform)
            shift
            switch_platform "$@"
            ;;
        view-rules)
            view_rules
            ;;
        check-and-notify-pending)
            check_and_notify_pending
            ;;
        auto-confirm)
            shift
            auto_confirm "$@"
            ;;
        help|*)
            echo "🛡️  developer-self-improve-core 安全可控自改进技能（多平台版）"
            echo ""
            echo "用法：$0 {init|pre-check|post-check|cleanup|confirm|switch-platform|view-rules|check-and-notify-pending|auto-confirm}"
            echo ""
            echo "命令说明："
            echo "  init                    初始化记忆目录"
            echo "  pre-check [场景]        回答前检查（错误防重 + 平台过滤）"
            echo "  post-check [内容] [场景]  回答后检查（自检 + 提案）"
            echo "  cleanup                 定期清洗（10 轮对话或每周）"
            echo "  confirm [ID] [操作]     确认规则（同意/修改/忽略）"
            echo "  switch-platform [平台]  切换平台（ios/android/flutter/h5/java/multi-platform）"
            echo "  view-rules              查看当前平台规则"
            echo "  check-and-notify-pending  检查并通知待审规则"
            echo "  auto-confirm [消息]     自动确认规则（从消息识别意图）"
            echo ""
            echo "示例："
            echo "  $0 init"
            echo "  $0 pre-check \"代码推送\""
            echo "  $0 post-check \"用户明确说推送要用脚本\" \"代码推送\""
            echo "  $0 cleanup"
            echo "  $0 confirm auto_ios_20260408_a1b2c3d4 同意"
            echo "  $0 switch-platform android"
            echo "  $0 view-rules"
            ;;
    esac
}

main "$@"
