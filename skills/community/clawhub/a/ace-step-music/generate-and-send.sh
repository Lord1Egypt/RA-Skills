#!/bin/bash
# ACE-Step 音乐生成 + 自动发送脚本
# 支持: 飞书(Feishu) / Telegram / Discord

set -e

# 配置
ACE_STEP_HOME="$HOME/workspace/ace-step"
VENV_PATH="$HOME/ace-step-env"
OUTPUT_DIR="$HOME/Music/ACE-Step"

# 默认发送到飞书 (从当前上下文推断)
DEFAULT_CHANNEL="feishu"
DEFAULT_CHAT="user:ou_232e435f3b7b35533206709e19cb19b5"

# 显示帮助
show_help() {
    cat << 'EOF'
🎵 ACE-Step 音乐生成 + 发送工具

用法:
  generate-and-send.sh "<prompt>" [选项]

选项:
  -d, --duration SECONDS    音乐时长 (默认: 30)
  -c, --channel CHANNEL     发送渠道: feishu|telegram|discord (默认: feishu)
  -t, --to TARGET           接收者ID (默认: 主人)
  -o, --output FILE         保存路径 (默认: 自动生成)
  -s, --send-only FILE      只发送已有文件
  --no-send                 不发送，只保存本地

示例:
  # 生成并发送到飞书
  generate-and-send.sh "Peaceful piano melody"

  # 生成60秒音乐发送到Telegram
  generate-and-send.sh "Upbeat electronic music" -d 60 -c telegram

  # 发送已有文件
  generate-and-send.sh -s ~/Music/my-music.wav -c discord

EOF
}

# 生成音乐
generate_music() {
    local prompt="$1"
    local duration="${2:-30}"
    local output_file="$3"
    
    echo "🎵 正在生成音乐..."
    echo "   描述: $prompt"
    echo "   时长: ${duration}秒"
    
    # 激活虚拟环境并生成
    (
        source "$VENV_PATH/bin/activate"
        cd "$ACE_STEP_HOME"
        
        # 使用 ACE-Step 生成
        python cli.py \
            --prompt "$prompt" \
            --duration "$duration" \
            --output "$output_file" \
            2>&1
    )
    
    if [ -f "$output_file" ]; then
        echo "✅ 生成成功: $output_file"
        return 0
    else
        echo "❌ 生成失败"
        return 1
    fi
}

# 发送到飞书
send_feishu() {
    local file="$1"
    local user_id="${2:-ou_232e435f3b7b35533206709e39cb19b5}"
    
    echo "📤 发送到飞书..."
    
    # 使用 OpenClaw 的消息工具发送文件
    # 注意: 这里调用 openclaw 命令发送
    # 实际文件发送可能需要上传到云存储后发送链接
    
    # 先发送文字通知
    cat > /tmp/send_feishu_msg.json <> EOF
{
  "channel": "feishu",
  "target": "$user_id",
  "text": "🎵 音乐生成完成！\\n📁 文件: $(basename $file)\\n📍 位置: $file"
}
EOF
    
    echo "   通知已准备 (文件: $file)"
    
    # 由于 Feishu API 限制，大文件需要特殊处理
    # 这里提供两种方案:
    # 1. 上传到飞书云文档/云盘，发送链接
    # 2. 转换为音频链接发送
    
    # 提示用户手动上传
    echo ""
    echo "💡 文件已保存，请手动上传到飞书:"
    echo "   $file"
}

# 发送到 Telegram
send_telegram() {
    local file="$1"
    local chat_id="${2:-}"
    
    echo "📤 发送到 Telegram..."
    
    # 检查是否有 Bot Token
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        echo "⚠️  未设置 TELEGRAM_BOT_TOKEN 环境变量"
        echo "   请设置: export TELEGRAM_BOT_TOKEN=your_token"
        return 1
    fi
    
    # 使用 Telegram Bot API 发送音频
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendAudio" \
        -F "chat_id=${chat_id}" \
        -F "audio=@${file}" \
        -F "caption=🎵 ACE-Step 生成的音乐" \
        2>&1 | grep -q '"ok":true' && echo "✅ 发送成功" || echo "❌ 发送失败"
}

# 发送到 Discord
send_discord() {
    local file="$1"
    local webhook_url="${2:-}"
    
    echo "📤 发送到 Discord..."
    
    if [ -z "$webhook_url" ]; then
        echo "⚠️  未设置 Discord Webhook URL"
        return 1
    fi
    
    # 使用 Webhook 发送
    curl -s -X POST "$webhook_url" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@${file}" \
        -F "content=🎵 ACE-Step 生成的音乐" \
        2>&1 | grep -q '"id"' && echo "✅ 发送成功" || echo "❌ 发送失败"
}

# 主函数
main() {
    local prompt=""
    local duration=30
    local channel="$DEFAULT_CHANNEL"
    local target=""
    local output_file=""
    local send_only=""
    local no_send=false
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -d|--duration)
                duration="$2"
                shift 2
                ;;
            -c|--channel)
                channel="$2"
                shift 2
                ;;
            -t|--to)
                target="$2"
                shift 2
                ;;
            -o|--output)
                output_file="$2"
                shift 2
                ;;
            -s|--send-only)
                send_only="$2"
                shift 2
                ;;
            --no-send)
                no_send=true
                shift
                ;;
            *)
                if [ -z "$prompt" ] && [ -z "$send_only" ]; then
                    prompt="$1"
                fi
                shift
                ;;
        esac
    done
    
    # 设置默认输出路径
    if [ -z "$output_file" ]; then
        mkdir -p "$OUTPUT_DIR"
        local timestamp=$(date +%Y%m%d_%H%M%S)
        output_file="$OUTPUT_DIR/music_${timestamp}.wav"
    fi
    
    # 如果只发送已有文件
    if [ -n "$send_only" ]; then
        if [ ! -f "$send_only" ]; then
            echo "❌ 文件不存在: $send_only"
            exit 1
        fi
        output_file="$send_only"
    elif [ -z "$prompt" ]; then
        echo "❌ 请提供音乐描述或文件路径"
        show_help
        exit 1
    else
        # 生成音乐
        generate_music "$prompt" "$duration" "$output_file" || exit 1
    fi
    
    # 发送
    if [ "$no_send" = false ]; then
        echo ""
        case "$channel" in
            feishu)
                send_feishu "$output_file" "$target"
                ;;
            telegram)
                send_telegram "$output_file" "$target"
                ;;
            discord)
                send_discord "$output_file" "$target"
                ;;
            *)
                echo "❌ 未知的渠道: $channel"
                exit 1
                ;;
        esac
    fi
    
    echo ""
    echo "✅ 完成!"
    echo "📁 文件: $output_file"
}

main "$@"
