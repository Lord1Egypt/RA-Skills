#!/bin/bash

# Audio Announcement Script for OpenClaw
# 使用 edge-tts 进行语音播报
# 版本: 1.7.4 - Windows 默认使用 pygame 方案

set -e

# Windows 平台检测：自动切换到 pygame 方案
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]] || [[ -n "$WINDIR" ]] || [[ -n "$MSYSTEM" ]]; then
    # Windows 平台：使用 pygame 方案
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    python3 "$SCRIPT_DIR/announce_pygame.py" "$@"
    exit $?
fi

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
TEMP_DIR="/tmp/audio-announcement"
CACHE_DIR="$HOME/.cache/audio-announcement"
SESSION_FILE="$CACHE_DIR/session.lock"
MAX_RETRIES=3

# 创建缓存目录
mkdir -p "$TEMP_DIR"
mkdir -p "$CACHE_DIR"

# 会话管理
init_session() {
    # 检查是否是新会话（SESSION_FILE 不存在或超过24小时）
    if [ ! -f "$SESSION_FILE" ] || [ $(($(date +%s) - $(stat -f %m "$SESSION_FILE" 2>/dev/null || echo 0))) -gt 86400 ]; then
        log_info "检测到新会话，初始化语音播报系统..."
        
        # 清理旧的临时文件（保留缓存）
        find "$TEMP_DIR" -name "*.mp3" -mtime +1 -delete 2>/dev/null || true
        
        # 更新会话文件
        touch "$SESSION_FILE"
        
        # 验证依赖
        if ! command -v edge-tts &> /dev/null; then
            log_warn "edge-tts 未安装，将尝试安装..."
            return 1
        fi
        
        if ! command -v ffplay &> /dev/null; then
            log_warn "ffplay 未安装，将尝试使用系统播放器..."
            # 回退到系统播放器
        fi
        
        # 播报会话开始
        local init_msg="语音播报系统已就绪"
        if generate_audio "$init_msg" "zh" "$TEMP_DIR/init.mp3" 2>/dev/null; then
            play_audio "$TEMP_DIR/init.mp3" 2>/dev/null || true
        fi
        
        log_info "语音播报系统初始化完成"
    fi
}

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" >&2
}

# 播放音频函数
play_audio() {
    local audio_file="$1"

    # 检测系统类型，选择合适的播放器
    local player=""
    
    # macOS: 优先使用 afplay
    if [[ "$OSTYPE" == "darwin"* ]] && command -v afplay &> /dev/null; then
        player="afplay"
    # Linux: 优先使用 mpg123
    elif [[ "$OSTYPE" == "linux"* ]] && command -v mpg123 &> /dev/null; then
        player="mpg123"
    # 通用: 使用 ffplay
    elif command -v ffplay &> /dev/null; then
        player="ffplay -nodisp -autoexit -loglevel quiet"
    else
        log_error "未找到可用的音频播放器。请安装："
        log_info "  macOS: afplay (自带) 或 brew install ffmpeg"
        log_info "  Linux: sudo apt-get install mpg123 或 ffmpeg"
        log_info "  Windows: 安装 VLC 或 ffmpeg"
        return 1
    fi

    # 播放音频
    log_info "使用播放器: $player"
    if eval "$player \"$audio_file\" 2>/dev/null"; then
        return 0
    else
        log_warn "播放失败，尝试备用播放器..."
        
        # 备用方案
        if [[ "$player" != "afplay" ]] && command -v afplay &> /dev/null; then
            afplay "$audio_file" 2>/dev/null && return 0
        fi
        if [[ "$player" != "mpg123" ]] && command -v mpg123 &> /dev/null; then
            mpg123 "$audio_file" 2>/dev/null && return 0
        fi
        if [[ "$player" != *"ffplay"* ]] && command -v ffplay &> /dev/null; then
            ffplay -nodisp -autoexit -loglevel quiet "$audio_file" 2>/dev/null && return 0
        fi
        
        log_error "所有播放器都失败了，请检查音频文件：$audio_file"
        return 1
    fi
}

# 使用 edge-tts 生成语音
generate_audio() {
    local text="$1"
    local lang="$2"
    local output_file="$3"

    # 检查是否已缓存
    # macOS 使用 md5, Linux 使用 md5sum
    local cache_key=""
    if command -v md5 &> /dev/null; then
        cache_key=$(echo -n "$text-$lang" | md5 | cut -d' ' -f4)
    elif command -v md5sum &> /dev/null; then
        cache_key=$(echo -n "$text-$lang" | md5sum | cut -d' ' -f1)
    else
        # 如果没有 md5 工具，使用简单的时间戳
        cache_key=$(echo -n "$text-$lang" | shasum -a 256 | cut -d' ' -f1 | head -c 16)
    fi
    local cached_file="$CACHE_DIR/$cache_key.mp3"

    if [ -f "$cached_file" ]; then
        log_info "使用缓存语音..."
        cp "$cached_file" "$output_file"
        return 0
    fi

    # 生成语音
    log_info "正在生成语音..."

    # 确定音色
    local voice=""
    case "$lang" in
        zh)
            voice="zh-CN-XiaoxiaoNeural"
            ;;
        en)
            voice="en-US-JennyNeural"
            ;;
        ja)
            voice="ja-JP-NanamiNeural"
            ;;
        ko)
            voice="ko-KR-SunHiNeural"
            ;;
        es)
            voice="es-ES-ElviraNeural"
            ;;
        fr)
            voice="fr-FR-DeniseNeural"
            ;;
        de)
            voice="de-DE-KatjaNeural"
            ;;
        *)
            log_warn "未知语言 '$lang'，使用中文..."
            voice="zh-CN-XiaoxiaoNeural"
            lang="zh"
            ;;
    esac

    # 尝试生成语音
    for i in $(seq 1 $MAX_RETRIES); do
        if python3 -m edge_tts --voice "$voice" --text "$text" --write-media "$output_file" 2>/dev/null; then
            # 缓存语音
            cp "$output_file" "$cached_file"
            log_info "语音生成成功"
            return 0
        fi

        if [ $i -lt $MAX_RETRIES ]; then
            log_warn "第 $i 次尝试失败，重试中..."
            sleep 1
        fi
    done

    log_error "语音生成失败，请检查："
    log_error "1. edge-tts 是否正确安装"
    log_error "2. 网络连接是否正常（需要访问微软 TTS 服务）"
    return 1
}

# 主函数
main() {
    if [ $# -lt 2 ]; then
        echo "用法: $0 <type> <message> [language]"
        echo ""
        echo "示例:"
        echo "  $0 complete '任务完成' zh"
        echo "  $0 task '处理中...' en"
        echo "  $0 error '发生错误' ja"
        echo ""
        echo "消息类型:"
        echo "  receive   - 收到消息/指令"
        echo "  task      - 任务开始/处理中"
        echo "  complete  - 任务完成"
        echo "  error     - 错误/警告"
        echo "  custom    - 自定义消息"
        echo ""
        echo "支持语言: zh, en, ja, ko, es, fr, de"
        exit 1
    fi

    local msg_type="$1"
    local message="$2"
    local language="${3:-zh}"

    # 初始化会话（确保新会话时系统正常工作）
    init_session

    # 根据类型添加前缀
    local full_message=""
    case "$msg_type" in
        receive)
            full_message="收到: $message"
            ;;
        task)
            full_message="任务: $message"
            ;;
        complete)
            full_message="完成: $message"
            ;;
        error)
            full_message="警告: $message"
            ;;
        custom)
            full_message="$message"
            ;;
        *)
            log_error "未知的消息类型: $msg_type"
            exit 1
            ;;
    esac

    # 生成临时文件
    local temp_file="$TEMP_DIR/announce-$(date +%s).mp3"

    # 生成语音
    if generate_audio "$full_message" "$language" "$temp_file"; then
        # 播放语音
        if play_audio "$temp_file"; then
            log_info "播报完成"
            # 清理临时文件（保留缓存）
            rm -f "$temp_file"
            exit 0
        fi
    fi

    exit 1
}

# 运行主函数
main "$@"
