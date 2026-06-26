#!/usr/bin/env bash
# SimpleViking 基础库
# 提供：路径解析、层级生成、日志输出、向量搜索等基础函数

export SV_WORKSPACE="${SV_WORKSPACE:-$HOME/.openclaw/viking}"
export SV_LOG_LEVEL="${SV_LOG_LEVEL:-INFO}"

# 向量搜索配置
export OLLAMA_HOST="${OLLAMA_HOST:-http://192.168.5.110:11434}"
export EMBED_MODEL="${EMBED_MODEL:-nomic-embed-text:latest}"
export VECTOR_INDEX_FILE=".viking_vectors.json"

# 日志函数
sv_log() {
  local level=$1
  shift
  if [[ "$SV_LOG_LEVEL" == "DEBUG" ]] || [[ "$level" != "DEBUG" ]]; then
    echo "[$level] $*" >&2
  fi
}

# 检查路径是否为 viking:// URI
sv_parse_uri() {
  local uri="$1"
  if [[ "$uri" =~ ^viking:// ]]; then
    local path="${uri#viking://}"
    echo "$path"
    return 0
  else
    sv_log ERROR "无效的 viking URI: $uri"
    return 1
  fi
}

# 获取文件的绝对路径
sv_resolve_path() {
  local uri="$1"
  local rel_path
  rel_path=$(sv_parse_uri "$uri") || return 1
  echo "$SV_WORKSPACE/$rel_path"
}

# 确保目录存在
sv_ensure_dir() {
  local dir="$1"
  mkdir -p "$dir"
}

# 生成 L0 摘要（前 100 字符或第一行）
sv_generate_l0() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo ""
    return
  fi
  # 取第一行，截断到 100 字符
  head -n1 "$file" | tr -d '\n' | cut -c1-100
}

# 生成 L1 概览（前 2k tokens ≈ 2000 字符或前 20 行）
sv_generate_l1() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo ""
    return
  fi
  # 取前 2000 字符或前 20 行
  head -c2000 "$file" | tr -d '\n' | cut -c1-2000
}

# 更新目录的 .abstract 和 .overview 文件
sv_update_dir_layers() {
  local dir="$1"
  sv_ensure_dir "$dir"

  # 收集该目录及其子目录下的所有内容文件（排除 .abstract/.overview）
  local files
  files=$(find "$dir" -type f ! -name '.abstract' ! -name '.overview' | head -n 100)

  if [[ -z "$files" ]]; then
    sv_log DEBUG "目录为空: $dir"
    return
  fi

  # 生成 L0：合并所有文件的第一行，节选
  local l0=""
  while IFS= read -r f; do
    local first_line
    first_line=$(head -n1 "$f" | tr -d '\n')
    if [[ -n "$first_line" ]]; then
      l0+="$first_line; "
    fi
  done <<< "$files"
  l0=$(echo "$l0" | cut -c1-150)
  echo "$l0" > "$dir/.abstract"

  # 生成 L1：扫描关键信息（简化：取各文件开头部分拼接，截断到 2k）
  local l1=""
  while IFS= read -r f; do
    local snippet
    snippet=$(head -c200 "$f" | tr -d '\n' | sed 's/"/\\"/g')
    if [[ -n "$snippet" ]]; then
      l1+="$snippet\n---\n"
    fi
  done <<< "$files"
  echo "$l1" | cut -c1-2000 > "$dir/.overview"

  sv_log DEBUG "已更新目录层级: $dir"
}

# 递归更新整棵树
sv_update_tree_layers() {
  local root="$1"
  sv_log INFO "开始更新目录层级: $root"
  # 后序遍历：先子目录后父目录
  find "$root" -type d | sort -r | while IFS= read -r dir; do
    sv_update_dir_layers "$dir"
  done
  sv_log INFO "层级更新完成"
}

# 检索：关键词匹配（文件和内容）
sv_find_keyword() {
  local query="$1"
  local root="${2:-$SV_WORKSPACE}"

  sv_log INFO "检索关键词: $query (根目录: $root)"

  # 第一步：路径匹配（高优先级）
  echo "=== 路径匹配 ==="
  find "$root" -type f ! -name '.abstract' ! -name '.overview' -iname "*$query*" 2>/dev/null | while IFS= read -r path; do
    rel="${path#$root/}"
    echo "FILE: viking://$rel"
  done

  # 第二步：内容匹配（带路径上下文）
  echo "=== 内容匹配 ==="
  rg -n --no-messages "$query" "$root" --type-add 'abstract:*.abstract' --type-add 'overview:*.overview' --type-not 'abstract' --type-not 'overview' 2>/dev/null | while IFS=: read -r file line content; do
    rel="${file#$root/}"
    echo "viking://$rel:$line | $content"
  done
}

# 的高级检索（带目录定位）
sv_find_smart() {
  local query="$1"
  local start_uri="${2:-viking://resources}"

  start_path=$(sv_resolve_path "$start_uri")
  if [[ ! -d "$start_path" ]]; then
    sv_log ERROR "起始目录不存在: $start_uri"
    return 1
  fi

  sv_log INFO "智能检索: $query (从: $start_uri)"

  # 先用 L0/L1 摘要匹配目录
  echo "🔍 正在分析意图..."
  local candidates=()
  while IFS= read -r dir; do
    if [[ -f "$dir/.abstract" ]]; then
      local abs=$(cat "$dir/.abstract")
      if echo "$abs" | tr '[:upper:]' '[:lower:]' | grep -q "$(echo "$query" | tr '[:upper:]' '[:lower:]')"; then
        candidates+=("$dir")
        echo "  → 目录候选: ${dir#$SV_WORKSPACE/} (摘要匹配)"
      fi
    fi
  done < <(find "$start_path" -type d)

  # 如果没有摘要匹配，则默认搜索整个树
  if [[ ${#candidates[@]} -eq 0 ]]; then
    candidates=("$start_path")
  fi

  # 在候选目录中递归搜索内容
  echo "🔎 细化搜索..."
  for cand in "${candidates[@]}"; do
    sv_find_keyword "$query" "$cand"
  done
}

# ===== 向量搜索功能 =====

# 获取文本的 embedding 向量
sv_get_embedding() {
  local text="$1"
  
  # 调用 Ollama API
  local response
  response=$(curl -s -s --max-time 30 "$OLLAMA_HOST/api/embeddings" \
    -d "{\"model\": \"$EMBED_MODEL\", \"prompt\": \"$text\"}")
  
  if [[ -z "$response" ]]; then
    sv_log ERROR "Ollama API 调用失败"
    return 1
  fi
  
  # 提取 embedding 数组
  echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    emb = data.get('embedding', [])
    print(json.dumps(emb))
except:
    print('[]')
" 2>/dev/null
}

# 计算两个向量的余弦相似度
sv_cosine_similarity() {
  local vec1="$1"
  local vec2="$2"
  
  python3 -c "
import sys, json, math
try:
    v1 = json.loads('''$vec1''')
    v2 = json.loads('''$vec2''')
    if len(v1) != len(v2) or len(v1) == 0:
        print(0)
        sys.exit(0)
    
    dot = sum(a*b for a,b in zip(v1,v2))
    mag1 = math.sqrt(sum(a*a for a in v1))
    mag2 = math.sqrt(sum(a*a for a in v2))
    
    if mag1 == 0 or mag2 == 0:
        print(0)
    else:
        print(dot / (mag1 * mag2))
except:
    print(0)
"
}

# 加载向量索引
sv_load_vector_index() {
  local workspace="${1:-$SV_WORKSPACE}"
  local index_file="$workspace/$VECTOR_INDEX_FILE"
  
  if [[ -f "$index_file" ]]; then
    cat "$index_file"
  else
    echo '{"files": {}, "version": "1.0"}'
  fi
}

# 保存向量索引
sv_save_vector_index() {
  local workspace="${1:-$SV_WORKSPACE}"
  local index_file="$workspace/$VECTOR_INDEX_FILE"
  local data="$2"
  
  echo "$data" > "$index_file"
  sv_log INFO "向量索引已保存"
}

# 构建向量索引（索引指定目录下的所有文本文件）
sv_build_vector_index() {
  local root="${1:-$SV_WORKSPACE}"
  local limit="${2:-100}"
  
  sv_log INFO "开始构建向量索引: $root"
  
  # 加载现有索引
  local index_json
  index_json=$(sv_load_vector_index "$root")
  
  # 查找需要索引的文件
  local files
  files=$(find "$root" -type f ! -name '.abstract' ! -name '.overview' ! -name '*.md' -prune \
    -o -type f -name "*.md" -print 2>/dev/null | head -n "$limit")
  
  local indexed=0
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    
    local rel_path="${file#$root/}"
    local mtime
    mtime=$(stat -c %Y "$file" 2>/dev/null || stat -f %m "$file" 2>/dev/null)
    
    # 跳过系统文件
    [[ "$rel_path" == *"$VECTOR_INDEX_FILE" ]] && continue
    
    # 获取文件内容（取前2000字符作为索引）
    local content
    content=$(head -c 2000 "$file" | tr -d '\n')
    
    # 获取 embedding
    local embedding
    embedding=$(sv_get_embedding "$content")
    
    if [[ -n "$embedding" && "$embedding" != "[]" ]]; then
      index_json=$(echo "$index_json" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    data['files']['$rel_path'] = {
        'embedding': json.loads('''$embedding'''),
        'mtime': $mtime,
        'size': $(wc -c < "$file" 2>/dev/null || echo 0)
    }
    print(json.dumps(data))
except Exception as e:
    print(sys.stdin.read())
")
      ((indexed++))
    fi
  done <<< "$files"
  
  sv_save_vector_index "$root" "$index_json"
  sv_log INFO "向量索引构建完成，已索引 $indexed 个文件"
}

# 向量语义搜索
sv_semantic_search() {
  local query="$1"
  local root="${2:-$SV_WORKSPACE}"
  local top_k="${3:-5}"
  
  sv_log INFO "语义搜索: $query (top_k=$top_k)"
  
  # 获取查询的 embedding
  local query_embedding
  query_embedding=$(sv_get_embedding "$query")
  
  if [[ -z "$query_embedding" || "$query_embedding" == "[]" ]]; then
    sv_log ERROR "无法获取查询向量"
    return 1
  fi
  
  # 加载索引
  local index_json
  index_json=$(sv_load_vector_index "$root")
  
  # 计算相似度并排序
  echo "$index_json" | python3 -c "
import sys, json

top_k = $top_k
data = json.load(sys.stdin)
query_emb = json.loads('''$query_embedding''')

results = []
for path, info in data.get('files', {}).items():
    emb = info.get('embedding', [])
    if not emb:
        continue
    
    dot = sum(a*b for a,b in zip(query_emb, emb))
    mag1 = sum(a*a for a in query_emb) ** 0.5
    mag2 = sum(a*a for a in emb) ** 0.5
    
    if mag1 > 0 and mag2 > 0:
        sim = dot / (mag1 * mag2)
        results.append((sim, path))

results.sort(reverse=True, key=lambda x: x[0])
for sim, path in results[:top_k]:
    print(f'{sim:.4f} viking://{path}')
" 2>/dev/null
}

# 混合搜索（语义 + 关键词）
sv_hybrid_search() {
  local query="$1"
  local root="${2:-$SV_WORKSPACE}"
  local top_k="${3:-5}"
  
  sv_log INFO "混合搜索: $query"
  
  echo "=== 语义搜索结果 ==="
  sv_semantic_search "$query" "$root" "$top_k"
  
  echo ""
  echo "=== 关键词搜索结果 ==="
  sv_find_keyword "$query" "$root"
}
# 增量更新向量索引（写入文件后自动调用）
sv_update_vector_index() {
  local file="$1"
  local workspace="${2:-$SV_WORKSPACE}"
  
  # 检查文件是否存在
  if [[ ! -f "$file" ]]; then
    return 1
  fi
  
  local rel_path="${file#$workspace/}"
  
  # 跳过系统文件
  [[ "$rel_path" == *"$VECTOR_INDEX_FILE" ]] && return 0
  [[ "$rel_path" == ".viking_"* ]] && return 0
  
  # 获取文件修改时间和内容
  local mtime
  mtime=$(stat -c %Y "$file" 2>/dev/null || stat -f %m "$file" 2>/dev/null)
  local content
  content=$(head -c 2000 "$file" | tr -d '\n')
  
  # 获取 embedding
  local embedding
  embedding=$(sv_get_embedding "$content")
  
  if [[ -z "$embedding" || "$embedding" == "[]" ]]; then
    sv_log WARN "无法获取向量: $rel_path"
    return 1
  fi
  
  # 加载现有索引
  local index_json
  index_json=$(sv_load_vector_index "$workspace")
  
  # 增量更新
  index_json=$(echo "$index_json" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    data['files']['$rel_path'] = {
        'embedding': json.loads('''$embedding'''),
        'mtime': $mtime,
        'size': $(wc -c < "$file" 2>/dev/null || echo 0)
    }
    print(json.dumps(data))
except Exception as e:
    print(sys.stdin.read())
" 2>/dev/null)
  
  if [[ -n "$index_json" ]]; then
    sv_save_vector_index "$workspace" "$index_json"
    sv_log INFO "向量索引已更新: $rel_path"
  fi
}
