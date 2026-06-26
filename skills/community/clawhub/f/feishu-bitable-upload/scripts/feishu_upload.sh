#!/bin/bash
# 飞书多维表格素材上传脚本
# 上传文件到多维表格并返回 file_token（供后续 API 引用）
#
# 注：lark-cli 不覆盖 /drive/v1/medias/ 接口（仅支持 /drive/v1/files/）
#     且无法做 multipart 上传，故本脚本需要 APP 凭证。
#
# 鉴权方式（优先级从高到低）：
#   1. 环境变量 FEISHU_APP_ID + FEISHU_APP_SECRET
#   2. --app-id / --app-secret 命令行参数
#
# 上传方式：
#   <= 20MB → upload_all（直接上传）
#   >  20MB → upload_prepare + upload_part × N + upload_finish

set -euo pipefail

FEISHU_BASE="https://open.feishu.cn"
SMALL_FILE_LIMIT=$((20 * 1024 * 1024))

# ========== 帮助 ==========
usage() {
    cat <<EOF
用法: $(basename "$0") <文件路径> [选项]

选项:
  --parent-node TOKEN   多维表格 App Token（必填，或设 FEISHU_PARENT_NODE）
  --parent-type TYPE    上传类型：bitable_file（默认）| bitable_image
  --app-id ID           飞书 App ID（或设 FEISHU_APP_ID）
  --app-secret SECRET   飞书 App Secret（或设 FEISHU_APP_SECRET）
  -h, --help            显示此帮助

鉴权说明:
  需提供 App ID + Secret（可通过参数或环境变量传入）。
  lark-cli 不支持 /drive/v1/medias/ 素材上传，无法代替本脚本鉴权。

示例:
  # 参数模式
  $(basename "$0") ./video.mp4 --parent-node HV5pbfwH7at... \\
    --app-id cli_xxx --app-secret yyy

  # 环境变量模式
  export FEISHU_PARENT_NODE=HV5pbfwH7at...
  export FEISHU_APP_ID=cli_xxx
  export FEISHU_APP_SECRET=yyy
  $(basename "$0") ./image.png
EOF
    exit 0
}

# ========== 参数解析 ==========
FILE_PATH=""
PARENT_NODE="${FEISHU_PARENT_NODE:-}"
PARENT_TYPE="${FEISHU_PARENT_TYPE:-bitable_file}"
APP_ID="${FEISHU_APP_ID:-}"
APP_SECRET="${FEISHU_APP_SECRET:-}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --parent-node) PARENT_NODE="$2"; shift 2 ;;
        --parent-type) PARENT_TYPE="$2"; shift 2 ;;
        --app-id)      APP_ID="$2";      shift 2 ;;
        --app-secret)  APP_SECRET="$2";  shift 2 ;;
        -h|--help)     usage ;;
        -*)            echo "未知选项: $1"; usage ;;
        *)
            [ -z "$FILE_PATH" ] && FILE_PATH="$1" || { echo "多余参数: $1"; usage; }
            shift ;;
    esac
done

[ -z "$FILE_PATH" ] && { echo "Error: 未指定文件路径"; usage; }
[ ! -f "$FILE_PATH" ] && { echo "Error: 文件不存在: $FILE_PATH"; exit 1; }
[ -z "$PARENT_NODE" ] && { echo "Error: 需要 --parent-node 或环境变量 FEISHU_PARENT_NODE"; exit 1; }

FILE_NAME=$(basename "$FILE_PATH")
if stat -f%z "$FILE_PATH" &>/dev/null; then
    FILE_SIZE=$(stat -f%z "$FILE_PATH")
else
    FILE_SIZE=$(stat -c%s "$FILE_PATH")
fi

echo "==================================="
echo "文件: $FILE_NAME"
echo "大小: $FILE_SIZE 字节 ($(( FILE_SIZE / 1024 / 1024 )) MB)"
echo "==================================="

# ========== 工具函数 ==========
json_val() {
    python3 -c "
import sys, json
d = json.load(sys.stdin)
for k in '$1'.split('.'):
    d = d[k]
print(d)
"
}

json_code() {
    python3 -c "import sys,json; print(json.load(sys.stdin).get('code',-1))"
}

filesize() {
    if stat -f%z "$1" &>/dev/null; then stat -f%z "$1"; else stat -c%s "$1"; fi
}

# ========== 鉴权：App 凭证 → tenant_access_token ==========
BEARER_TOKEN=""
AUTH_MODE=""

if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
    echo ""
    echo "Error: 需要提供 App 凭证。请选择以下任一方式："
    echo "  1. 提供 --app-id + --app-secret 参数"
    echo "  2. 设置 FEISHU_APP_ID + FEISHU_APP_SECRET 环境变量"
    echo ""
    echo "注：lark-cli 不支持 /drive/v1/medias/ 素材上传，无法代替凭证鉴权。"
    exit 1
fi

echo "[Auth] 获取 tenant_access_token..."
TOKEN_RESP=$(curl -s -X POST "${FEISHU_BASE}/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"${APP_ID}\",\"app_secret\":\"${APP_SECRET}\"}")

TOKEN_CODE=$(echo "$TOKEN_RESP" | json_code)
if [ "$TOKEN_CODE" != "0" ]; then
    echo "[Auth] 获取 token 失败: $TOKEN_RESP"
    exit 1
fi

BEARER_TOKEN=$(echo "$TOKEN_RESP" | json_val "tenant_access_token")
AUTH_MODE="credentials"
echo "[Auth] token 获取成功（${BEARER_TOKEN:0:20}...）"

# ========== 直接上传（<= 20MB）==========
do_upload_all() {
    echo "" >&2
    echo "[2] 直接上传（upload_all）..." >&2

    local resp
    resp=$(curl -s -X POST "${FEISHU_BASE}/open-apis/drive/v1/medias/upload_all" \
        -H "Authorization: Bearer ${BEARER_TOKEN}" \
        -F "file_name=${FILE_NAME}" \
        -F "parent_type=${PARENT_TYPE}" \
        -F "parent_node=${PARENT_NODE}" \
        -F "size=${FILE_SIZE}" \
        -F "file=@${FILE_PATH}")

    local code
    code=$(echo "$resp" | json_code)
    [ "$code" != "0" ] && { echo "上传失败: $resp" >&2; exit 1; }

    echo "$resp" | json_val "data.file_token"
}

# ========== 分片上传（> 20MB）==========
do_upload_chunked() {
    # Step 2: 预上传
    echo "" >&2
    echo "[2] 预上传，获取 upload_id..." >&2

    local prepare_resp
    prepare_resp=$(curl -s -X POST "${FEISHU_BASE}/open-apis/drive/v1/medias/upload_prepare" \
        -H "Authorization: Bearer ${BEARER_TOKEN}" \
        -H "Content-Type: application/json; charset=utf-8" \
        -d "{\"file_name\":\"${FILE_NAME}\",\"parent_type\":\"${PARENT_TYPE}\",\"parent_node\":\"${PARENT_NODE}\",\"size\":${FILE_SIZE}}")

    local code
    code=$(echo "$prepare_resp" | json_code)
    [ "$code" != "0" ] && { echo "预上传失败: $prepare_resp" >&2; exit 1; }

    local upload_id block_size block_num
    upload_id=$(echo "$prepare_resp"  | json_val "data.upload_id")
    block_size=$(echo "$prepare_resp" | json_val "data.block_size")
    block_num=$(echo "$prepare_resp"  | json_val "data.block_num")

    echo "upload_id: $upload_id | block_size: $block_size | block_num: $block_num" >&2

    # Step 3: 逐片上传
    echo "" >&2
    echo "[3] 上传 $block_num 个分片..." >&2

    local chunk_dir
    chunk_dir=$(mktemp -d)
    # 不用 trap，函数末尾手动清理（trap EXIT 在函数返回后 chunk_dir 已失效）

    for ((seq = 0; seq < block_num; seq++)); do
        local chunk_file="${chunk_dir}/chunk_${seq}"
        dd if="$FILE_PATH" bs="$block_size" skip="$seq" count=1 of="$chunk_file" 2>/dev/null

        local actual_size
        actual_size=$(filesize "$chunk_file")
        echo "  分片 $((seq + 1))/$block_num — $actual_size 字节" >&2

        local part_resp
        part_resp=$(curl -s -X POST "${FEISHU_BASE}/open-apis/drive/v1/medias/upload_part" \
            -H "Authorization: Bearer ${BEARER_TOKEN}" \
            -F "upload_id=${upload_id}" \
            -F "seq=${seq}" \
            -F "size=${actual_size}" \
            -F "file=@${chunk_file}")

        local part_code
        part_code=$(echo "$part_resp" | json_code)
        [ "$part_code" != "0" ] && { echo "  分片 $seq 失败: $part_resp" >&2; exit 1; }

        echo "  分片 $((seq + 1)) 成功" >&2
        rm -f "$chunk_file"
    done

    # Step 4: 完成上传
    echo "" >&2
    echo "[4] 完成上传..." >&2

    local finish_resp
    finish_resp=$(curl -s -X POST "${FEISHU_BASE}/open-apis/drive/v1/medias/upload_finish" \
        -H "Authorization: Bearer ${BEARER_TOKEN}" \
        -H "Content-Type: application/json; charset=utf-8" \
        -d "{\"upload_id\":\"${upload_id}\",\"block_num\":${block_num}}")

    local finish_code
    finish_code=$(echo "$finish_resp" | json_code)
    [ "$finish_code" != "0" ] && { echo "完成上传失败: $finish_resp" >&2; exit 1; }

    echo "$finish_resp" | json_val "data.file_token"
    rm -rf "$chunk_dir"
}

# ========== 主逻辑 ==========
echo ""
if [ "$FILE_SIZE" -le "$SMALL_FILE_LIMIT" ]; then
    echo "文件大小 ≤ 20MB，直接上传（auth: ${AUTH_MODE}）"
    FILE_TOKEN=$(do_upload_all)
else
    echo "文件大小 > 20MB，分片上传（auth: ${AUTH_MODE}）"
    FILE_TOKEN=$(do_upload_chunked)
fi

echo ""
echo "==================================="
echo "上传成功！"
echo "file_token: $FILE_TOKEN"
echo "==================================="
