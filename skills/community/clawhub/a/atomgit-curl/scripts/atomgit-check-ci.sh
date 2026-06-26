#!/bin/bash
# AtomGit CI Check - 安全版
# 用途：解析 openeuler-ci-bot 的 HTML 评论，判断 CI 流水线状态

ATOMGIT_BASE_URL="https://api.atomgit.com/api/v5"

# 从 openclaw.json 读取 Token (自动检测路径)
load_token_from_config() {
    local config_paths=(
        "$HOME/.openclaw/openclaw.json"
        "$USERPROFILE/.openclaw/openclaw.json"
    )
    
    # WSL 环境下检测 Windows 路径
    if command -v uname &> /dev/null && [ "$(uname -r)" == *"Microsoft"* ]; then
        local win_user
        win_user=$(cmd.exe /c "echo %USERPROFILE%" 2>/dev/null | tr -d '\r' | sed 's/.*Users\///i')
        if [ -n "$win_user" ]; then
            config_paths+=("/mnt/c/Users/$win_user/.openclaw/openclaw.json")
        else
            config_paths+=("/mnt/c/Users/default/.openclaw/openclaw.json")
        fi
    fi
    
    for config in "${config_paths[@]}"; do
        if [ -f "$config" ]; then
            local token
            token=$(grep -o '"ATOMGIT_TOKEN"[[:space:]]*:[[:space:]]*"[^"]*"' "$config" 2>/dev/null | cut -d'"' -f4)
            if [ -n "$token" ]; then
                echo "$token"
                return 0
            fi
        fi
    done
    return 1
}

# 加载 Token
if [ -z "$ATOMGIT_TOKEN" ]; then
    ATOMGIT_TOKEN=$(load_token_from_config)
fi

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m'

# 检查 Token
check_token() {
    if [ -z "$ATOMGIT_TOKEN" ]; then
        echo -e "${RED}ERROR: Token not configured${NC}"
        echo -e "${YELLOW}Set ATOMGIT_TOKEN in ~/.openclaw/openclaw.json${NC}"
        exit 1
    fi
}

# CI 检查 (优化版 - 使用 Python 解析 HTML)
check_ci() {
    local owner=$1
    local repo=$2
    local pr=$3
    
    if [ -z "$owner" ] || [ -z "$repo" ] || [ -z "$pr" ]; then
        echo -e "${RED}❌ Usage: $0 <owner> <repo> <pr>${NC}"
        exit 1
    fi
    
    echo -e "\n${CYAN}=== AtomGit CI Check ===${NC}\n"
    check_token
    
    echo -e "${GRAY}Checking PR #$pr...${NC}"
    
    # 使用 Python 解析 HTML 并输出结果 (通过环境变量传递 Token)
    export ATOMGIT_BASE_URL
    export ATOMGIT_TOKEN
    python3 - "$owner" "$repo" "$pr" << 'PYTHON_SCRIPT'
import sys
import json
import urllib.request
import os

# 从环境变量获取敏感信息 (不直接嵌入脚本)
token = os.environ.get('ATOMGIT_TOKEN', '')
base_url = os.environ.get('ATOMGIT_BASE_URL', 'https://api.atomgit.com/api/v5')
owner = sys.argv[1] if len(sys.argv) > 1 else ''
repo = sys.argv[2] if len(sys.argv) > 2 else ''
pr = sys.argv[3] if len(sys.argv) > 3 else ''

# 安全验证
if not token or not owner or not repo or not pr:
    print("Error: Missing required parameters")
    sys.exit(1)

# 获取评论
url = f"{base_url}/repos/{owner}/{repo}/pulls/{pr}/comments"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
try:
    with urllib.request.urlopen(req) as response:
        comments = json.loads(response.read().decode())
except Exception as e:
    print(f"Error: API request failed")
    sys.exit(1)

# 筛选 ci-bot 评论
ci_comments = [c for c in comments if 'openeuler-ci-bot' in c.get('user', {}).get('login', '')]
if not ci_comments:
    print("No CI bot comments found")
    sys.exit(0)

# 获取最新评论
ci_comments.sort(key=lambda x: x.get('created_at', ''), reverse=True)
latest = ci_comments[0]
body = latest.get('body', '')

print(f"Found {len(ci_comments)} CI bot comments")
print()

# 解析 HTML 表格
import re
pattern = r'<tr><td[^>]*>([^<]+)</td>.*?<td[^>]*>(:[a-z_]+:)\s*<strong>([A-Z]+)</strong>'
matches = re.findall(pattern, body, re.DOTALL)

check_items = []
for name, emoji, status in matches:
    if emoji == ':white_check_mark:':
        result = 'success'
    elif emoji == ':x:':
        result = 'failed'
    elif emoji == ':hourglass:':
        result = 'running'
    elif emoji == ':warning:':
        result = 'warning'
    else:
        result = status.lower()
    
    check_items.append({'name': name.strip(), 'result': result, 'status': status})

# 统计
success = sum(1 for i in check_items if i['result'] == 'success')
failure = sum(1 for i in check_items if i['result'] == 'failed')
running = sum(1 for i in check_items if i['result'] in ['running', 'pending'])
total = len(check_items)

print("=== Results ===")
print()
print(f"Total: {total}")
print(f"\033[0;32mSuccess: {success}\033[0m")
print(f"\033[0;31mFailure: {failure}\033[0m")
print(f"\033[1;33mRunning: {running}\033[0m")
print()

if check_items:
    print("Details:")
    for item in check_items:
        if item['result'] == 'success':
            print(f"\033[0;32m[OK] {item['name']}\033[0m")
        elif item['result'] == 'failed':
            print(f"\033[0;31m[FAIL] {item['name']}\033[0m")
        elif item['result'] in ['running', 'pending']:
            print(f"\033[1;33m[RUN] {item['name']}\033[0m")
        else:
            print(f"[?] {item['name']}")
    print()

# 判断整体状态
if failure > 0:
    print("\033[0;31mOverall: FAILED\033[0m")
    print("Failed items:")
    for item in check_items:
        if item['result'] == 'failed':
            print(f"  - {item['name']}")
    sys.exit(2)
elif running > 0:
    print("\033[1;33mOverall: RUNNING\033[0m")
    sys.exit(1)
elif total == 0:
    print("\033[1;33mOverall: NO CHECKS\033[0m")
    sys.exit(0)
else:
    print("\033[0;32mOverall: SUCCESS\033[0m")
    sys.exit(0)
PYTHON_SCRIPT
}

# 主程序
if [ "$#" -eq 3 ]; then
    check_ci "$1" "$2" "$3"
else
    echo -e "${RED}❌ Usage: $0 <owner> <repo> <pr>${NC}"
    echo -e "${YELLOW}Example: $0 openeuler release-management 2564${NC}"
    exit 1
fi
