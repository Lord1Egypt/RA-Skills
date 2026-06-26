#!/bin/bash
#
# memory-embed.sh
# 记忆向量化和语义搜索
#

set -e

OLLAMA_HOST="${OLLAMA_HOST:-http://192.168.5.110:11434}"
EMBED_MODEL="${EMBED_MODEL:-nomic-embed-text:latest}"
VECTOR_INDEX=".viking_vectors.json"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取文本的 embedding
get_embedding() {
    local text="$1"
    
    curl -s --max-time 30 "$OLLAMA_HOST/api/embeddings" \
        -d "{\"model\": \"$EMBED_MODEL\", \"prompt\": \"$text\"}" | \
        python3 -c "
import sys, json
data = json.load(sys.stdin)
emb = data.get('embedding', [])
print(json.dumps(emb))
" 2>/dev/null || echo "[]"
}

# 计算余弦相似度
cosine_similarity() {
    local vec1="$1"
    local vec2="$2"
    
    python3 -c "
import sys, json, math
try:
    v1 = json.loads('''$vec1''')
    v2 = json.loads('''$vec2''')
    if not v1 or not v2:
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

# 为单个文件生成并存储向量
embed_file() {
    local file="$1"
    local workspace="$2"
    
    # 读取文件内容（取前2000字符，去除特殊字符）
    local content
    content=$(head -c 2000 "$file" | tr '\n' ' ' | sed 's/"/ /g' | tr -s ' ')
    
    # 获取 embedding（使用临时文件避免引号问题）
    local embedding
    local tmpfile=$(mktemp)
    echo "{\"model\": \"$EMBED_MODEL\", \"prompt\": \"$content\"}" > "$tmpfile"
    
    embedding=$(curl -s --max-time 30 "$OLLAMA_HOST/api/embeddings" \
        -d @"$tmpfile" | python3 -c "
import sys, json
data = json.load(sys.stdin)
emb = data.get('embedding', [])
print(json.dumps(emb))
" 2>/dev/null)
    
    rm -f "$tmpfile"
    
    if [ "$embedding" = "[]" ] || [ -z "$embedding" ]; then
        echo -e "${RED}Failed to get embedding for: $file${NC}"
        return 1
    fi
    
    # 获取相对路径
    local rel_path="${file#$workspace/}"
    
    # 读取现有向量索引
    local index_file="$workspace/$VECTOR_INDEX"
    
    # 更新索引
    python3 -c "
import json

rel_path = '''$rel_path'''
embedding = '''$embedding'''
index_file = '''$index_file'''

try:
    with open(index_file, 'r') as f:
        index = json.load(f)
except:
    index = {'vectors': [], 'files': {}}

# 更新或添加向量
index['files'][rel_path] = {
    'embedding': json.loads(embedding),
    'updated': '$(date -Iseconds)'
}

# 保存
with open(index_file, 'w') as f:
    json.dump(index, f, indent=2)

print('OK')
" 2>/dev/null || echo "OK"
    
    echo -e "${GREEN}✓ $rel_path${NC}"
}

# 搜索记忆
search_memories() {
    local query="$1"
    local workspace="${2:-$HOME/.openclaw/viking-maojingli}"
    local top_k="${3:-5}"
    
    echo "=== 语义搜索 ==="
    echo "查询: $query"
    echo "工作区: $workspace"
    echo ""
    
    # 获取查询的 embedding
    echo -e "${YELLOW}获取查询向量...${NC}"
    local query_emb
    query_emb=$(get_embedding "$query")
    
    if [ "$query_emb" = "[]" ]; then
        echo -e "${RED}获取查询向量失败${NC}"
        return 1
    fi
    
    local index_file="$workspace/$VECTOR_INDEX"
    
    if [ ! -f "$index_file" ]; then
        echo -e "${YELLOW}未找到向量索引，请先存储记忆${NC}"
        return 1
    fi
    
    # 搜索相似记忆
    echo -e "${YELLOW}搜索中...${NC}"
    python3 -c "
import json
import sys

query_emb = json.loads('''$query_emb''')
top_k = $top_k

with open('$index_file', 'r') as f:
    index = json.load(f)

# 计算相似度
results = []
for path, data in index.get('files', {}).items():
    emb = data.get('embedding', [])
    if not emb:
        continue
    
    # 计算余弦相似度
    dot = sum(a*b for a,b in zip(query_emb, emb))
    mag1 = sum(a*a for a in query_emb) ** 0.5
    mag2 = sum(a*a for a in emb) ** 0.5
    
    if mag1 > 0 and mag2 > 0:
        sim = dot / (mag1 * mag2)
        results.append((sim, path))

# 排序
results.sort(reverse=True, key=lambda x: x[0])

# 输出结果
for i, (sim, path) in enumerate(results[:top_k], 1):
    print(f'{i}. [{sim:.3f}] viking://{path}')
" 2>/dev/null
}

# 主入口
case "$1" in
    embed)
        embed_file "$2" "$3"
        ;;
    search)
        search_memories "$2" "$3" "$4"
        ;;
    test)
        echo "测试 Ollama 连接..."
        curl -s "$OLLAMA_HOST/api/tags" | python3 -c "
import json, sys
data = json.load(sys.stdin)
models = data.get('models', [])
print('可用模型:')
for m in models:
    print(f'  - {m.get(\"name\", \"?\")}')" 2>/dev/null || echo "连接失败"
        ;;
    rebuild)
        # 重建整个向量库
        workspace="${2:-$HOME/.openclaw/viking-maojingli}"
        echo "重建向量库: $workspace"
        
        # 删除旧索引
        rm -f "$workspace/$VECTOR_INDEX"
        
        # 遍历所有 md 文件
        find "$workspace" -name "*.md" -type f ! -name '.abstract' ! -name '.overview' | while read f; do
            embed_file "$f" "$workspace"
        done
        echo "重建完成"
        ;;
    *)
        echo "用法:"
        echo "  $0 embed <文件路径> <工作区>"
        echo "  $0 search <查询> [工作区] [top-k]"
        echo "  $0 test"
        echo "  $0 rebuild [工作区]"
        ;;
esac
