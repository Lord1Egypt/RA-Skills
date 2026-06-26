#!/bin/bash
# ACE-Step Agent 共享接口
# 允许其他本地 Agent 调用 ACE-Step 生成音乐
# 无需关心 Python 环境细节

set -e

# 配置
ACE_STEP_HOME="$HOME/workspace/ace-step"
VENV_PATH="$HOME/ace-step-env"
OUTPUT_DIR="$HOME/Music/ACE-Step"

# 确保输出目录存在
mkdir -p "$OUTPUT_DIR"

# 显示帮助
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "ACE-Step Agent 接口"
    echo "=================="
    echo ""
    echo "用法:"
    echo "  $0 generate \"<prompt>\" [duration] [output_file]"
    echo "  $0 status"
    echo "  $0 install"
    echo ""
    echo "示例:"
    echo "  $0 generate \"Peaceful piano\" 30 /tmp/music.wav"
    echo "  $0 generate \"Upbeat electronic\" 60"
    echo ""
    exit 0
fi

# 检查安装状态
check_installation() {
    if [ ! -d "$VENV_PATH" ]; then
        echo "{\"status\": \"not_installed\", \"error\": \"Virtual environment not found\"}"
        return 1
    fi
    if [ ! -d "$ACE_STEP_HOME" ]; then
        echo "{\"status\": \"not_installed\", \"error\": \"ACE-Step code not found\"}"
        return 1
    fi
    
    # 检查关键文件
    if [ ! -f "$ACE_STEP_HOME/cli.py" ]; then
        echo "{\"status\": \"partial\", \"error\": \"CLI not found\"}"
        return 1
    fi
    
    echo "{\"status\": \"ready\"}"
    return 0
}

# 生成音乐
generate_music() {
    local prompt="$1"
    local duration="${2:-30}"
    local output_file="$3"
    
    if [ -z "$prompt" ]; then
        echo "{\"success\": false, \"error\": \"Prompt is required\"}"
        return 1
    fi
    
    # 生成默认输出文件名
    if [ -z "$output_file" ]; then
        local timestamp=$(date +%s)
        output_file="$OUTPUT_DIR/agent_generated_${timestamp}.wav"
    fi
    
    # 确保目录存在
    mkdir -p "$(dirname "$output_file")"
    
    echo "{\"status\": \"generating\", \"prompt\": \"$prompt\", \"duration\": $duration}" >&2
    
    # 在虚拟环境中执行生成
    # 注意: 这里使用 cli.py 如果有的话，或者创建一个简单的生成脚本
    (
        source "$VENV_PATH/bin/activate"
        cd "$ACE_STEP_HOME"
        
        # 创建临时生成脚本
        cat > /tmp/ace_step_generate.py <> 'EOF'
import sys
import os
import time

# 添加到路径
sys.path.insert(0, os.path.expanduser("~/workspace/ace-step"))

try:
    # 尝试导入 ace_step
    from ace_step import MusicGenerator
    
    prompt = sys.argv[1]
    duration = int(sys.argv[2])
    output_path = sys.argv[3]
    
    start = time.time()
    generator = MusicGenerator()
    music = generator.generate(prompt=prompt, duration=duration)
    music.save(output_path)
    
    elapsed = time.time() - start
    print(f"{{'success': true, 'file': '{output_path}', 'time': {elapsed:.2f}}}")
    
except Exception as e:
    print(f"{{'success': false, 'error': '{str(e)}'}}")
    sys.exit(1)
EOF
        
        python3 /tmp/ace_step_generate.py "$prompt" "$duration" "$output_file" 2>&1 || {
            echo "{\"success\": false, \"error\": \"Generation failed\"}"
            return 1
        }
    )
}

# 获取状态
get_status() {
    check_installation
    echo ","
    echo "\"venv_path\": \"$VENV_PATH\","
    echo "\"code_path\": \"$ACE_STEP_HOME\","
    echo "\"output_dir\": \"$OUTPUT_DIR\""
    echo "}"
}

# 主命令处理
case "$1" in
    generate)
        shift
        generate_music "$@"
        ;;
    status)
        get_status
        ;;
    install)
        echo "请运行: bash /Users/qinghetangzhu/.openclaw/workspace-evolution/skills/ace-step/install_ace_step.sh"
        ;;
    *)
        echo "{\"error\": \"Unknown command: $1\", \"usage\": \"$0 --help\"}"
        exit 1
        ;;
esac
