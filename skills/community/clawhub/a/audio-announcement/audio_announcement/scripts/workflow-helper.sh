#!/bin/bash
# Workflow Helper for Audio Announcement
# 音频播报工作流助手脚本

set -e

# 主脚本路径
ANNOUNCE_SCRIPT="$HOME/.openclaw/skills/audio-announcement/scripts/announce.sh"

# 检查主脚本是否存在
check_announce_script() {
    if [ ! -f "$ANNOUNCE_SCRIPT" ]; then
        echo "❌ 音频播报脚本不存在: $ANNOUNCE_SCRIPT"
        echo "💡 请确保 audio-announcement 技能已正确安装"
        return 1
    fi
    if [ ! -x "$ANNOUNCE_SCRIPT" ]; then
        chmod +x "$ANNOUNCE_SCRIPT"
    fi
    return 0
}

# 主播报函数
announce() {
    local type="$1"
    local message="$2"
    local lang="${3:-zh}"
    
    # 检查脚本
    if ! check_announce_script; then
        return 1
    fi
    
    # 执行播报
    "$ANNOUNCE_SCRIPT" "$type" "$message" "$lang" 2>/dev/null || {
        echo "⚠️  语音播报失败: $message" >&2
        return 1
    }
}

# 快捷函数：任务开始
announce_task() {
    announce "task" "$1" "${2:-zh}"
}

# 快捷函数：任务完成
announce_complete() {
    announce "complete" "$1" "${2:-zh}"
}

# 快捷函数：错误提醒
announce_error() {
    announce "error" "$1" "${2:-zh}"
}

# 快捷函数：自定义消息
announce_custom() {
    announce "custom" "$1" "${2:-zh}"
}

# 任务包装器：自动播报任务开始和完成
announce_wrap() {
    local task_name="$1"
    shift
    
    announce_task "$task_name"
    
    # 执行实际命令
    if "$@"; then
        announce_complete "$task_name 完成"
        return 0
    else
        local exit_code=$?
        announce_error "$task_name 失败 (退出码: $exit_code)"
        return $exit_code
    fi
}

# 带进度的任务
announce_with_progress() {
    local task_name="$1"
    local total_steps="${2:-1}"
    shift 2
    
    announce_task "$task_name (0/$total_steps)"
    
    local current_step=1
    for step_cmd in "$@"; do
        announce_task "$task_name 步骤 $current_step/$total_steps"
        
        if eval "$step_cmd"; then
            ((current_step++))
        else
            announce_error "$task_name 步骤 $current_step 失败"
            return 1
        fi
    done
    
    announce_complete "$task_name 完成 ($total_steps 个步骤)"
    return 0
}

# 初始化检查
init_announcement() {
    if check_announce_script; then
        echo "✅ 音频播报系统就绪"
        announce_custom "音频播报助手已加载" zh
        return 0
    else
        echo "❌ 音频播报系统初始化失败"
        return 1
    fi
}

# 测试所有功能
test_announcement() {
    echo "🔊 测试音频播报功能..."
    
    announce_task "测试任务开始"
    sleep 0.5
    
    announce_task "测试处理中状态"
    sleep 0.5
    
    announce_complete "测试任务完成"
    sleep 0.5
    
    announce_error "测试错误提醒"
    sleep 0.5
    
    announce_custom "测试自定义消息"
    
    echo "✅ 所有测试完成！"
}

# 显示使用帮助
show_help() {
    cat << EOF
音频播报工作流助手

使用方法：
  source "$(realpath "${BASH_SOURCE[0]}")"

可用函数：
  announce <type> <message> [lang]     # 通用播报函数
  announce_task <message> [lang]       # 任务开始
  announce_complete <message> [lang]   # 任务完成  
  announce_error <message> [lang]      # 错误提醒
  announce_custom <message> [lang]     # 自定义消息
  
  announce_wrap <任务名> <命令>        # 自动包装命令
  announce_with_progress <任务名> <总步数> <命令1> <命令2> ...
  
  init_announcement                    # 初始化检查
  test_announcement                    # 测试所有功能

示例：
  # 简单使用
  announce_task "开始数据处理"
  process_data.sh
  announce_complete "数据处理完成"
  
  # 自动包装
  announce_wrap "文件备份" backup_files.sh
  
  # 带进度
  announce_with_progress "系统更新" 3 \
    "sudo apt update" \
    "sudo apt upgrade -y" \
    "sudo apt autoremove -y"

支持语言：zh, en, ja, ko, es, fr, de

EOF
}

# 如果直接运行，显示帮助
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    show_help
fi

# 自动初始化（可选）
# init_announcement

echo "✅ 音频播报助手已加载，使用 'test_announcement' 测试功能"
