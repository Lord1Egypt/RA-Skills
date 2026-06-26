#!/bin/bash
# init-setup.sh — 检查并引导设置 OPENAI_API_KEY_0011AI
#
# 流程：
#   STEP 1: 触发条件 — credentials.env 不存在
#   STEP 2: Fallback — 优先读环境变量 $OPENAI_API_KEY_0011AI，否则要求用户提供
#   STEP 3: 验证 Key 有效，无效或空则回到 STEP 2
#   STEP 4: 写入 credentials.env，权限 600，结束
#
# 用法：
#   bash init-setup.sh        # 交互式设置向导（Key 无效时循环）
#   bash init-setup.sh check # 仅检查状态

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CRED_FILE="$SKILL_DIR/credentials.env"
ENV_VAR_NAME="OPENAI_API_KEY_0011AI"
WORKDIR="/tmp/codex-setup-test-$$"

trap 'rm -rf "$WORKDIR"' EXIT

mask_key() {
    local key="$1"
    if [[ ${#key} -gt 12 ]]; then
        echo "${key:0:4}...${key: -8}"
    else
        echo "****"
    fi
}

# 读取已有 Key（无则为无）
load_key() {
    if [[ -f "$CRED_FILE" ]]; then
        source "$CRED_FILE" 2>/dev/null
        echo "${OPENAI_API_KEY_0011AI:-}" | tr -d '\r'
    else
        echo ""
    fi
}

# STEP 2: 获取 Key — 优先环境变量，否则要求用户输入
prompt_key() {
    # 优先从环境变量读取
    if [[ -n "$OPENAI_API_KEY_0011AI" ]]; then
        echo "📋 检测到环境变量中的 Key: $(mask_key "$OPENAI_API_KEY_0011AI")"
        read -p "使用这个 Key 吗？(Y/n): " -r || true
        if [[ ! "$REPLY" =~ ^[Nn]$ ]]; then
            echo "$OPENAI_API_KEY_0011AI"
            return 0
        fi
    fi

    # 要求用户提供
    echo ""
    echo "请输入你的 Codex API Key："
    echo "（输入时不会显示，按回车确认）"
    read -p "API Key: " -r NEW_KEY
    echo "$NEW_KEY"
}

# STEP 3: 验证 Key 有效性
validate_key() {
    local key="$1"
    [[ -z "$key" ]] && return 1

    mkdir -p "$WORKDIR"
    cd "$WORKDIR"
    git init -q 2>/dev/null || true

    # 去除 \r（防止 CRLF）
    key="${key//$'\r'}"

    # 实际调用 codex 验证
    env "${ENV_VAR_NAME}=${key}" codex --full-auto exec -o /tmp/setup-verify.txt "echo ok" >/dev/null 2>&1
    return $?
}

# check 模式
do_check() {
    local key
    key=$(load_key)
    if [[ -n "$key" ]]; then
        echo "✅ $ENV_VAR_NAME 已设置: $(mask_key "$key")"
        echo "   文件位置: $CRED_FILE"
        exit 0
    else
        echo "❌ $ENV_VAR_NAME 未设置"
        exit 1
    fi
}

# === 入口 ===

if [[ "${1:-}" == "check" ]]; then
    do_check
fi

# STEP 1: 检查触发条件
if [[ -f "$CRED_FILE" ]]; then
    echo "✅ $ENV_VAR_NAME 已存在: $(mask_key "$(load_key)")"
    echo ""
    read -p "是否重新设置？(y/N): " -r || true
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        echo "保持现有 Key 不变。"
        exit 0
    fi
fi

# STEP 2 + 3: 循环获取并验证 Key，无效则回到 STEP 2
while true; do
    echo ""
    echo "=== STEP 2: 获取 Key ==="

    NEW_KEY=$(prompt_key)
    NEW_KEY="${NEW_KEY//$'\r'}"  # 去除 \r

    if [[ -z "$NEW_KEY" ]]; then
        echo "❌ Key 不能为空，请重试"
        continue
    fi

    echo ""
    echo "=== STEP 3: 验证 Key ==="
    echo "🔍 验证 Key: $(mask_key "$NEW_KEY")..."

    if validate_key "$NEW_KEY"; then
        echo "✅ Key 验证通过！"
        break
    else
        echo "❌ Key 验证失败（无效、额度用完或网络问题）"
        echo "   请提供有效的 Key"
    fi
done

# STEP 4: 写入 credentials.env
cat > "$CRED_FILE" <<EOF
OPENAI_API_KEY_0011AI=$NEW_KEY
EOF
chmod 600 "$CRED_FILE"

echo ""
echo "✅ API Key 已保存: $(mask_key "$NEW_KEY")"
echo "   文件位置: $CRED_FILE"
echo ""
echo "设置完成！现在可以调用 Codex 执行任务了。"
