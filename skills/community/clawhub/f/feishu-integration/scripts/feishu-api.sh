#!/bin/bash
# 飞书 API 封装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTH_SCRIPT="${SCRIPT_DIR}/feishu-auth.sh"

# 获取 token
get_token() {
  bash "$AUTH_SCRIPT" get
}

# ========== 文档操作 ==========

# 读取文档
feishu_doc_read() {
  local doc_token=$1
  local token=$(get_token)
  
  curl -s -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/${doc_token}" \
    -H "Authorization: Bearer ${token}"
}

# 读取文档块列表
feishu_doc_list_blocks() {
  local doc_token=$1
  local token=$(get_token)
  
  curl -s -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/${doc_token}/blocks" \
    -H "Authorization: Bearer ${token}"
}

# 写入文档（替换全部内容）
feishu_doc_write() {
  local doc_token=$1
  local content=$2
  local token=$(get_token)
  
  curl -s -X PUT "https://open.feishu.cn/open-apis/docx/v1/documents/${doc_token}/content" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d "{
      \"content\": $(echo "$content" | jq -Rs '.')
    }"
}

# 追加内容到文档
feishu_doc_append() {
  local doc_token=$1
  local content=$2
  local token=$(get_token)
  
  curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/${doc_token}/content" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d "{
      \"content\": $(echo "$content" | jq -Rs '.')
    }"
}

# 批量创建块（推荐使用，避免乱序）
# 参数: doc_token, blocks_json_array
# blocks_json_array 格式: [{"block_type":2,"text":{"elements":[{"text_run":{"content":"内容"}}]}}]
feishu_doc_batch_create() {
  local doc_token=$1
  local blocks_json=$2
  local token=$(get_token)
  
  curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/${doc_token}/blocks/batch_create" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d "{
      \"children\": ${blocks_json},
      \"document_revision_id\": -1
    }"
}

# 从 Markdown 文件批量写入文档（优化版，避免乱序）
# 参数: doc_token, md_file_path
# 策略: 将内容分成 3-5 个大块，减少批次数量，降低乱序概率
feishu_doc_write_md() {
  local doc_token=$1
  local md_file=$2
  local token=$(get_token)
  
  # 读取文件并按段落分块（每 20 行一块）
  local content=$(cat "$md_file")
  local total_lines=$(wc -l < "$md_file")
  local chunk_size=20
  local chunks=$(( (total_lines + chunk_size - 1) / chunk_size ))
  
  echo "Total lines: $total_lines, Chunks: $chunks" >&2
  
  # 分块追加
  local current_chunk=""
  local line_num=0
  
  while IFS= read -r line; do
    current_chunk="${current_chunk}${line}"$'\n'
    line_num=$((line_num + 1))
    
    # 每 chunk_size 行或最后一行发送一次
    if [ $((line_num % chunk_size)) -eq 0 ] || [ $line_num -eq $total_lines ]; then
      echo "Appending chunk $(( (line_num + chunk_size - 1) / chunk_size ))/$chunks (lines $((line_num - chunk_size + 1 > 0 ? line_num - chunk_size + 1 : 1))-$line_num)..." >&2
      
      local result=$(curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/${doc_token}/content" \
        -H "Authorization: Bearer ${token}" \
        -H "Content-Type: application/json" \
        -d "{
          \"content\": $(echo "$current_chunk" | jq -Rs '.')
        }")
      
      if echo "$result" | jq -e '.code != 0 and .code != null' > /dev/null 2>&1; then
        echo "Error: $result" >&2
        return 1
      fi
      
      # 清空当前块
      current_chunk=""
      
      # 批次间延迟 0.5 秒
      sleep 0.5
    fi
  done <<< "$(cat "$md_file")"
  
  echo "Write complete!" >&2
  echo "{\"success\": true}"
}

# ========== 知识库操作 ==========

# 列出知识空间
feishu_wiki_spaces() {
  local token=$(get_token)
  
  curl -s -X GET "https://open.feishu.cn/open-apis/wiki/v2/spaces" \
    -H "Authorization: Bearer ${token}"
}

# 列出空间节点
feishu_wiki_nodes() {
  local space_id=$1
  local token=$(get_token)
  
  curl -s -X GET "https://open.feishu.cn/open-apis/wiki/v2/spaces/${space_id}/nodes" \
    -H "Authorization: Bearer ${token}"
}

# 创建知识库文档
feishu_wiki_create_doc() {
  local space_id=$1
  local title=$2
  local token=$(get_token)
  
  curl -s -X POST "https://open.feishu.cn/open-apis/wiki/v2/spaces/${space_id}/nodes" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d "{
      \"obj_type\": \"docx\",
      \"title\": \"${title}\"
    }"
}

# ========== 文件操作 ==========

# 列出云空间文件
feishu_drive_list() {
  local folder_token=${1:-""}
  local token=$(get_token)
  
  local url="https://open.feishu.cn/open-apis/drive/v1/files"
  if [[ -n "$folder_token" ]]; then
    url="${url}?folder_token=${folder_token}"
  fi
  
  curl -s -X GET "$url" \
    -H "Authorization: Bearer ${token}"
}

# 上传文件
feishu_upload_file() {
  local file_path=$1
  local folder_token=$2
  local token=$(get_token)
  
  local file_name=$(basename "$file_path")
  local file_size=$(stat -c %s "$file_path")
  
  curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/files/upload_all" \
    -H "Authorization: Bearer ${token}" \
    -F "file_name=${file_name}" \
    -F "parent_type=explorer" \
    -F "parent_node=${folder_token}" \
    -F "size=${file_size}" \
    -F "file=@${file_path}"
}

# ========== 导入操作 ==========

# 上传素材（用于导入）
feishu_upload_media() {
  local file_path=$1
  local obj_type=${2:-"docx"}
  local file_ext=${3:-"md"}
  local token=$(get_token)
  
  local file_name=$(basename "$file_path")
  local file_size=$(stat -c %s "$file_path")
  local extra="{\"obj_type\":\"${obj_type}\",\"file_extension\":\"${file_ext}\"}"
  
  curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all" \
    -H "Authorization: Bearer ${token}" \
    -F "file_name=${file_name}" \
    -F "parent_type=ccm_import_open" \
    -F "size=${file_size}" \
    -F "extra=${extra}" \
    -F "file=@${file_path}"
}

# 创建导入任务
feishu_create_import_task() {
  local file_token=$1
  local file_ext=$2
  local folder_token=$3
  local obj_type=${4:-"docx"}
  local token=$(get_token)
  
  curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/import_tasks" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d "{
      \"file_token\": \"${file_token}\",
      \"file_extension\": \"${file_ext}\",
      \"type\": \"${obj_type}\",
      \"point\": {
        \"mount_type\": 1,
        \"mount_key\": \"${folder_token}\"
      }
    }"
}

# 查询导入任务
feishu_get_import_task() {
  local ticket=$1
  local token=$(get_token)
  
  curl -s -X GET "https://open.feishu.cn/open-apis/drive/v1/import_tasks/${ticket}" \
    -H "Authorization: Bearer ${token}"
}

# 导入 Markdown 文件（完整流程）
feishu_import_md() {
  local file_path=$1
  local folder_token=$2
  
  echo "Step 1: Uploading media..." >&2
  local media_response=$(feishu_upload_media "$file_path" "docx" "md")
  local media_token=$(echo "$media_response" | grep -o '"file_token":"[^"]*"' | cut -d'"' -f4)
  
  if [[ -z "$media_token" ]]; then
    echo "Error: Failed to upload media" >&2
    echo "$media_response" >&2
    return 1
  fi
  echo "Media token: $media_token" >&2
  
  echo "Step 2: Creating import task..." >&2
  local task_response=$(feishu_create_import_task "$media_token" "md" "$folder_token" "docx")
  local ticket=$(echo "$task_response" | grep -o '"ticket":"[^"]*"' | cut -d'"' -f4)
  
  if [[ -z "$ticket" ]]; then
    echo "Error: Failed to create import task" >&2
    echo "$task_response" >&2
    return 1
  fi
  echo "Task ticket: $ticket" >&2
  
  echo "Step 3: Waiting for import..." >&2
  local max_attempts=10
  local attempt=0
  
  while [[ $attempt -lt $max_attempts ]]; do
    sleep 2
    local result=$(feishu_get_import_task "$ticket")
    local status=$(echo "$result" | grep -o '"job_status":[0-9]*' | cut -d: -f2)
    
    if [[ "$status" == "0" ]]; then
      local doc_token=$(echo "$result" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
      local url=$(echo "$result" | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
      echo "Import successful!" >&2
      echo "Doc token: $doc_token" >&2
      echo "URL: $url" >&2
      echo "$result"
      return 0
    fi
    
    attempt=$((attempt + 1))
    echo "Attempt $attempt: status=$status" >&2
  done
  
  echo "Error: Import timeout" >&2
  return 1
}

# ========== 主入口 ==========

show_usage() {
  cat << EOF
Usage: $0 <command> [args...]

Commands:
  token                          - Get valid token
  doc-read <doc_token>          - Read document
  doc-list <doc_token>          - List document blocks
  doc-write <doc_token> <content>  - Write document
  doc-append <doc_token> <content> - Append to document (may cause ordering issues)
  doc-batch <doc_token> <blocks_json> - Batch create blocks (recommended)
  doc-write-md <doc_token> <md_file> - Write Markdown file (optimized, 50 blocks/batch)
  wiki-spaces                    - List wiki spaces
  wiki-nodes <space_id>         - List wiki nodes
  wiki-create <space_id> <title>  - Create wiki doc
  drive-list [<folder_token>]    - List files
  upload <file> <folder_token>   - Upload file
  import-md <file> <folder>     - Import Markdown

Examples:
  $0 token
  $0 doc-read V4mYdLUc3oIAklxG1ducsbTQnKc
  $0 doc-write-md V4mYdLUc3oIAklxG1ducsbTQnKc /tmp/test.md
  $0 import-md /tmp/test.md nodcnJ9crfeKQuquKgkUgcRh2ag
EOF
}

# 执行命令
case "${1:-}" in
  "token")
    get_token
    ;;
  "doc-read")
    feishu_doc_read "$2"
    ;;
  "doc-list")
    feishu_doc_list_blocks "$2"
    ;;
  "doc-write")
    feishu_doc_write "$2" "$3"
    ;;
  "doc-append")
    feishu_doc_append "$2" "$3"
    ;;
  "doc-batch")
    feishu_doc_batch_create "$2" "$3"
    ;;
  "doc-write-md")
    feishu_doc_write_md "$2" "$3"
    ;;
  "wiki-spaces")
    feishu_wiki_spaces
    ;;
  "wiki-nodes")
    feishu_wiki_nodes "$2"
    ;;
  "wiki-create")
    feishu_wiki_create_doc "$2" "$3"
    ;;
  "drive-list")
    feishu_drive_list "$2"
    ;;
  "upload")
    feishu_upload_file "$2" "$3"
    ;;
  "import-md")
    feishu_import_md "$2" "$3"
    ;;
  *)
    show_usage
    exit 1
    ;;
esac
