#!/bin/bash
# ============================================
#   Audio Announcement - Offline Mode
#   离线播报脚本，无需网络
#   使用系统内置语音引擎
# ============================================

set -e

# 配置
DEFAULT_LANG="zh"
QUEUE_DIR="/tmp/audio-announcement-queue"

# 根据时间段获取音量
get_volume() {
    local hour=$(date +%H)
    if [ "$hour" -ge 12 ] && [ "$hour" -lt 14 ]; then
        echo "30"
    elif [ "$hour" -ge 22 ] || [ "$hour" -lt 8 ]; then
        echo "30"
    else
        echo "50"
    fi
}

# 平台检测
detect_platform() {
    case "$(uname -s)" in
        Darwin*)    echo "macos" ;;
        Linux*)     echo "linux" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *) echo "unknown" ;;
    esac
}

# 离线播报 - macOS
speak_macos() {
    local message="$1"
    local volume="$2"
    
    # 使用 say 命令（macOS 内置）
    # 中文语音: Ting-Ting, 英文语音: Samantha
    say -v Ting-Ting "[[volm $volume]] $message" 2>/dev/null || \
    say "$message" 2>/dev/null
}

# 离线播报 - Windows
speak_windows() {
    local message="$1"
    local volume="$2"
    
    powershell -NoProfile -ExecutionPolicy Bypass -Command "
        Add-Type -AssemblyName System.Speech
        \$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
        \$synth.Volume = $volume
        \$synth.SelectVoice('Microsoft Huihui Desktop')
        \$synth.Speak('$message')
        \$synth.Dispose()
    " 2>/dev/null
}

# 离线播报 - Linux
speak_linux() {
    local message="$1"
    local volume="$2"
    
    # 尝试 espeak
    if command -v espeak &> /dev/null; then
        espeak -v zh "$message" -a $volume 2>/dev/null
        return
    fi
    
    # 尝试 festival
    if command -v festival &> /dev/null; then
        echo "$message" | festival --tts 2>/dev/null
        return
    fi
    
    echo "[WARN] Linux 需要安装 espeak 或 festival"
}

# 主播报函数
announce_offline() {
    local type="$1"
    local message="$2"
    local platform=$(detect_platform)
    local volume=$(get_volume)
    
    echo "[INFO] 离线播报 [$type]: $message [音量:${volume}%]"
    
    case "$platform" in
        macos)
            speak_macos "$message" "$volume"
            ;;
        windows)
            speak_windows "$message" "$volume"
            ;;
        linux)
            speak_linux "$message" "$volume"
            ;;
        *)
            echo "[ERROR] 未知平台: $platform"
            return 1
            ;;
    esac
}

# 错误播报
announce_error() {
    local error_type="$1"
    local error_messages=""
    
    case "$error_type" in
        "network")
            error_messages="网络连接失败"
            ;;
        "api")
            error_messages="接口调用失败"
            ;;
        "timeout")
            error_messages="请求超时"
            ;;
        "auth")
            error_messages="认证失败"
            ;;
        "model")
            error_messages="模型服务异常"
            ;;
        "unknown")
            error_messages="发生未知错误"
            ;;
        *)
            error_messages="$error_type"
            ;;
    esac
    
    announce_offline "error" "$error_messages"
}

# 主函数
main() {
    case "$1" in
        -h|--help|help)
            echo "Audio Announcement - Offline Mode"
            echo ""
            echo "用法: $0 <type> <message>"
            echo "     $0 error <error_type>"
            echo ""
            echo "错误类型:"
            echo "  network  网络连接失败"
            echo "  api      接口调用失败"
            echo "  timeout  请求超时"
            echo "  auth     认证失败"
            echo "  model    模型服务异常"
            echo ""
            echo "示例:"
            echo "  $0 error network"
            echo "  $0 error model"
            echo "  $0 complete \"任务完成\""
            exit 0
            ;;
        error)
            announce_error "$2"
            ;;
        *)
            if [ -z "$1" ] || [ -z "$2" ]; then
                echo "用法: $0 <type> <message>"
                exit 1
            fi
            announce_offline "$1" "$2"
            ;;
    esac
}

main "$@"