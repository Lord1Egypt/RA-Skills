#!/bin/bash
#
# 加豆AI 上传文件到云存储(OSS) ，获取可访问 URL
#
# 功能：
#   1. 调用 signature 获取 OSS 预签名上传 URL
#   2. 使用 curl 将文件 PUT 直传到 OSS
#   3. 输出 file_url、file_size 供后续 MCP 工具调用
#
# 用法：
#   bash upload_file.sh <file_path>
#
# 依赖：
#   - mcporter（已配置 ClawAgent 服务）
#   - curl
#   - jq
# 输出（成功时）：
#   IMPORT_READY
#   FILE_URL:<file_url>
#   FILE_SIZE:<file_size>
#
# 输出（失败时）：
#   ERROR:<error_message>
#

set -euo pipefail

# ── 检查是否从标准输入读取 need_upload 响应 ───────────────────────────────────────────────────────
NEED_UPLOAD=""
if [[ -p /dev/stdin ]]; then
    NEED_UPLOAD=$(cat)
    if [[ "$NEED_UPLOAD" == *'"error":"need_upload"'* ]]; then
        local_file_path=$(echo "$NEED_UPLOAD" | jq -r '.local_file_path // empty' 2>/dev/null || echo "")
        tool_name=$(echo "$NEED_UPLOAD" | jq -r '.tool_name // empty' 2>/dev/null || echo "")
        if [[ -n "$local_file_path" && -f "$local_file_path" ]]; then
            FILE_PATH="$local_file_path"
        else
            echo "ERROR:invalid_need_upload - 无法从need_upload解析出有效文件路径"
            echo "请检查输入格式或提供有效的本地文件路径"
            exit 1
        fi
    else
        echo "ERROR:invalid_input - 管道输入不是有效的need_upload响应"
        echo "请检查输入格式或提供有效的本地文件路径"
        exit 1
    fi
else
    # ── 参数校验 ───────────────────────────────────────────────────────────────────────────────────
    if [[ $# -ne 1 ]]; then
        echo "ERROR:missing_argument - 缺少文件路径参数"
        echo "用法: bash upload_file.sh <file_path>"
        echo "   或: echo '{\"error\":\"need_upload\",...}' | bash upload_file.sh"
        exit 1
    fi
    FILE_PATH="$1"
fi

# ── 检查是否为引用标记 ─────────────────────────────────────────────────────────────────────────────
if [[ "$FILE_PATH" =~ ^@ ]]; then
    echo "ERROR:reference_not_supported - 检测到文件引用标记($FILE_PATH)，不支持直接使用"
    echo "请提供文件的完整本地路径，例如：/Users/yourname/Downloads/image.jpg"
    exit 1
fi

# ── 检查路径是否为绝对路径 ─────────────────────────────────────────────────────────────────────────
if [[ "$FILE_PATH" != /* ]]; then
    echo "ERROR:relative_path - 请使用完整绝对路径，当前路径: $FILE_PATH"
    echo "示例：/Users/yourname/Downloads/image.jpg"
    exit 1
fi

# ── 检查路径是否包含明显的编造特征 ─────────────────────────────────────────────────────────────────
# 检查是否包含常见的占位符或示例路径
if [[ "$FILE_PATH" =~ (xxx|yourname|yourusername|example|path/to) ]]; then
    echo "ERROR:suspicious_path - 检测到路径可能为AI编造或示例路径: $FILE_PATH"
    echo "请提供真实的本地文件完整路径"
    exit 1
fi

# ── 解析符号链接 ───────────────────────────────────────────────────────────────────────────────────
if [[ -L "$FILE_PATH" ]]; then
    FILE_PATH=$(readlink -f "$FILE_PATH")
fi

# ── 检查文件是否存在 ───────────────────────────────────────────────────────────────────────────────
if [[ ! -f "$FILE_PATH" ]]; then
    echo "ERROR:file_not_found - 文件不存在: $FILE_PATH"
    echo "请检查路径是否正确，或提供文件的实际存储位置"
    exit 1
fi

# ── 检查文件是否可读 ───────────────────────────────────────────────────────────────────────────────
if [[ ! -r "$FILE_PATH" ]]; then
    echo "ERROR:file_not_readable - 文件无读取权限: $FILE_PATH"
    echo "请检查文件权限或尝试使用 sudo"
    exit 1
fi

FILE_NAME=$(basename "$FILE_PATH")

# ── 计算文件大小 ──────────────────────────────────────────────────────────────
if [[ "$(uname)" == "Darwin" ]]; then
    FILE_SIZE=$(stat -f%z "$FILE_PATH")
else
    FILE_SIZE=$(stat -c%s "$FILE_PATH")
fi

if [[ "$FILE_SIZE" -le 0 ]]; then
    echo "ERROR:empty_file - 文件为空: $FILE_PATH"
    echo "请检查文件内容或提供有效的文件"
    exit 1
fi

# ── 检查文件大小是否超限（100MB） ──────────────────────────────────────────────────────────────────
MAX_SIZE=$((100 * 1024 * 1024))
if [[ "$FILE_SIZE" -gt "$MAX_SIZE" ]]; then
    echo "ERROR:file_too_large - 文件过大，最大支持100MB"
    echo "请压缩文件或选择较小的文件"
    exit 1
fi

echo "文件: $FILE_NAME"
echo "文件大小: $FILE_SIZE 字节"

# ── Step 1: 调用 MCP upload 获取 OSS 预签名上传 URL ───────────────────────────
echo "正在获取签名..."

UPLOAD_ARGS=$(cat <<EOF
{"filename": "$FILE_NAME", "content_type": "$(file --mime-type -b "$FILE_PATH")"}
EOF
)

UPLOAD_RESULT=$(mcporter call "ClawAgent" "signature" --args "$UPLOAD_ARGS" 2>&1) || {
    echo "ERROR:signature_failed - 获取上传签名失败"
    echo "请检查网络连接或稍后重试"
    exit 1
}

# 解析返回的 upload_url、file_url 和 headers
UPLOAD_URL=$(echo "$UPLOAD_RESULT" | jq -r '.data.upload_url // empty' 2>/dev/null || echo "")
FILE_URL=$(echo "$UPLOAD_RESULT" | jq -r '.data.file_url // empty' 2>/dev/null || echo "")
CONTENT_TYPE=$(echo "$UPLOAD_RESULT" | jq -r '.data.headers["Content-Type"] // empty' 2>/dev/null || echo "application/octet-stream")

if [[ -z "$UPLOAD_URL" ]]; then
    echo "ERROR:no_upload_url - 未获取到上传链接"
    echo "请检查服务配置或联系管理员"
    exit 1
fi

if [[ -z "$FILE_URL" ]]; then
    echo "ERROR:no_file_url - 未获取到文件访问链接"
    echo "请检查服务配置或联系管理员"
    exit 1
fi

echo "✅ 获取上传签名成功"
echo ""

# ── Step 2: 使用 curl PUT 上传文件到 OSS（V4 签名在 URL 参数中）────────────────────────────────────────
echo "正在上传文件到 OSS..."

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X PUT \
    -H "Content-Type: $CONTENT_TYPE" \
    --data-binary "@$FILE_PATH" \
    "$UPLOAD_URL" 2>&1) || {
    echo "ERROR:upload_failed - 文件上传失败"
    echo "请检查网络连接或稍后重试"
    exit 1
}

if [[ "$HTTP_STATUS" -ge 200 && "$HTTP_STATUS" -lt 300 ]]; then
    echo "✅ 文件上传成功"
else
    echo "ERROR:upload_http_error - OSS 上传返回 HTTP $HTTP_STATUS"
    echo "请检查网络连接或稍后重试"
    exit 1
fi

# ── 输出结果 ───────────────────────────────────────────────────────────────────────────────────────
echo "IMPORT_READY"
echo "FILE_URL:$FILE_URL"
echo "FILE_SIZE:$FILE_SIZE"
if [[ -n "${tool_name:-}" ]]; then
    echo "TOOL_NAME:$tool_name"
fi
echo ""
echo "📋 下一步说明："
if [[ -n "${tool_name:-}" ]]; then
    echo "文件上传成功，使用上述 FILE_URL 调用工具 $tool_name 继续操作"
else
    echo "文件上传成功，使用上述 FILE_URL 继续后续操作"
fi 
