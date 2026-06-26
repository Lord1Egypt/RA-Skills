#!/usr/bin/env bash

# 中文笑话 API 工具
# 用法：chinese-joke <command>

set -e

# 获取一言搞笑
get_hitokoto() {
    local result
    result=$(curl -s --max-time 5 "https://v1.hitokoto.cn?c=j" 2>/dev/null) || {
        echo "一言 API 获取失败"
        return 1
    }
    
    echo "$result" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f'「{d[\"hitokoto\"]}」')
    print(f'—— {d.get(\"from_\", d.get(\"from\", \"\"))}')
except:
    print('解析失败')
"
}

# 获取简短笑话
get_simple_joke() {
    local result
    result=$(curl -s --max-time 5 "https://api.jokeapi.cn/joke/Any?safe-mode" 2>/dev/null) || {
        echo "简短笑话 API 获取失败"
        return 1
    }
    
    echo "$result" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if d.get('type') == 'single':
        print(d['joke'])
    else:
        print(d['setup'])
        print()
        print(d['delivery'])
except:
    print('解析失败')
"
}

# 显示帮助
show_help() {
    cat << EOF
中文笑话 API 工具

用法：chinese-joke <command>

命令:
  hitokoto   获取一言搞笑 (默认)
  simple     获取简短笑话
  help       显示帮助信息

示例:
  chinese-joke hitokoto   # 获取一言搞笑
  chinese-joke simple     # 获取简短笑话
EOF
}

# 默认命令
COMMAND="${1:-hitokoto}"

case $COMMAND in
    hitokoto)
        get_hitokoto
        ;;
    simple)
        get_simple_joke
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令：$COMMAND"
        show_help
        exit 1
        ;;
esac
