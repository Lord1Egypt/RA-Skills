#!/bin/bash
#
# mp_mention_detect.sh
# 向量相似度提及检测
# 会话结束时，用当前会话内容与历史记忆做向量相似度匹配
# 相似度 > 0.8 → access_count +1
#

set -e

AGENT_NAME="${AGENT_NAME:-maojingli}"
SV_WORKSPACE="$HOME/.openclaw/viking-$AGENT_NAME"

OLLAMA_HOST="${OLLAMA_HOST:-http://192.168.5.110:11434}"
EMBED_MODEL="${EMBED_MODEL:-nomic-embed-text:latest}"

# 相似度阈值 (0.6-0.8 较合理，推荐 0.63)
SIMILARITY_THRESHOLD=0.63

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 临时文件
TEMP_DIR="/tmp/mp_mention_detect"
mkdir -p "$TEMP_DIR"

# ===== 核心函数 =====

# 获取文本的 embedding
get_embedding() {
    local text="$1"
    
    # 处理特殊字符
    local safe_text=$(echo "$text" | tr '\n' ' ' | sed 's/"/\\"/g' | head -c 8000)
    
    local tmpfile=$(mktemp)
    echo "{\"model\": \"$EMBED_MODEL\", \"prompt\": \"$safe_text\"}" > "$tmpfile"
    
    curl -s --max-time 30 "$OLLAMA_HOST/api/embeddings" -d @"$tmpfile" | \
        python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin).get('embedding', [])))" 2>/dev/null
    
    rm -f "$tmpfile"
}

# 计算余弦相似度
cosine_similarity() {
    local vec1="$1"
    local vec2="$2"
    
    python3 << EOF
import json, math
try:
    v1 = json.loads('''$vec1''')
    v2 = json.loads('''$vec2''')
    if not v1 or not v2:
        print(0)
        exit(0)
    
    dot = sum(a*b for a,b in zip(v1,v2))
    mag1 = math.sqrt(sum(a*a for a in v1))
    mag2 = math.sqrt(sum(a*a for a in v2))
    
    if mag1 == 0 or mag2 == 0:
        print(0)
    else:
        print(round(dot / (mag1 * mag2), 4))
except:
    print(0)
EOF
}

# 更新记忆的 access_count
update_access_count() {
    local file="$1"
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}文件不存在: $file${NC}"
        return 1
    fi
    
    # 读取当前的 access_count
    local current_count
    current_count=$(grep -E "^access_count:" "$file" | head -1 | sed 's/.*access_count: *//' | tr -d ' ')
    
    if [ -z "$current_count" ]; then
        current_count=0
    fi
    
    local new_count=$((current_count + 1))
    
    # 更新 access_count
    sed -i "s/^access_count:.*/access_count: $new_count/" "$file"
    
    # 同时更新 last_access 时间
    local now=$(date -Iseconds)
    sed -i "s/^last_access:.*/last_access: $now/" "$file"
    
    echo -e "${GREEN}✓ 更新 $(basename "$file"): access_count $current_count → $new_count${NC}"
}

# 获取记忆列表
get_memory_list() {
    local workspace="$1"
    local mem_file="$TEMP_DIR/memories.json"
    
    python3 << EOF
import os
import json

workspace = '''$workspace'''
memories = []

for tier in ['hot', 'warm']:
    tier_dir = os.path.join(workspace, 'agent', 'memories', tier)
    if not os.path.exists(tier_dir):
        continue
    
    for f in os.listdir(tier_dir):
        if not f.endswith('.md') or f.startswith('.'):
            continue
        
        filepath = os.path.join(tier_dir, f)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()[:1500]
                # 提取标题
                title = f
                for line in content.split('\n'):
                    if line.startswith('title:'):
                        title = line.replace('title:', '').strip().strip('"')
                        break
                memories.append({
                    'file': filepath,
                    'content': content,
                    'title': title,
                    'tier': tier
                })
        except:
            continue

with open('$mem_file', 'w') as f:
    json.dump(memories, f)

print(len(memories))
EOF
}

# 主检测逻辑
detect_mentions() {
    local session_content="$1"
    local workspace="${2:-$SV_WORKSPACE}"
    
    echo "=== 向量相似度提及检测 ==="
    echo "工作区: $workspace"
    echo ""
    
    # 检查 session_content
    if [ -z "$session_content" ] || [ "$session_content" = "" ]; then
        echo -e "${YELLOW}无会话内容，跳过检测${NC}"
        return 0
    fi
    
    # 获取会话内容的 embedding
    echo -e "${YELLOW}获取会话内容向量...${NC}"
    local session_emb
    session_emb=$(get_embedding "$session_content")
    
    if [ "$session_emb" = "[]" ] || [ -z "$session_emb" ]; then
        echo -e "${RED}获取会话内容向量失败${NC}"
        return 1
    fi
    
    # 保存到临时文件
    echo "$session_emb" > "$TEMP_DIR/session_emb.json"
    
    local dim
    dim=$(python3 -c "import json; print(len(json.load(open('$TEMP_DIR/session_emb.json'))))")
    echo -e "${GREEN}✓ 向量维度: $dim${NC}"
    echo ""
    
    # 获取记忆列表
    echo -e "${YELLOW}加载历史记忆...${NC}"
    local mem_count
    mem_count=$(get_memory_list "$workspace")
    
    if [ "$mem_count" = "0" ]; then
        echo -e "${YELLOW}未找到历史记忆${NC}"
        return 0
    fi
    
    echo -e "${GREEN}✓ 加载 $mem_count 条记忆${NC}"
    echo ""
    
    # 遍历记忆，计算相似度
    echo -e "${YELLOW}计算相似度...${NC}"
    echo ""
    
    local matched=0
    
    # 使用 Python 计算相似度
    python3 -c "
import json
import urllib.request
import urllib.parse
import os

OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://192.168.5.110:11434')
EMBED_MODEL = os.environ.get('EMBED_MODEL', 'nomic-embed-text:latest')
TEMP_DIR = '$TEMP_DIR'
threshold = $SIMILARITY_THRESHOLD

with open(TEMP_DIR + '/session_emb.json') as f:
    session_emb = json.load(f)

with open(TEMP_DIR + '/memories.json') as f:
    memories = json.load(f)

for mem in memories:
    filepath = mem['file']
    content = mem['content'][:1500]
    title = mem['title']
    tier = mem['tier']
    
    # 获取记忆的 embedding
    safe_text = content.replace('\"', '\\\"').replace('\n', ' ')
    
    data = json.dumps({'model': EMBED_MODEL, 'prompt': safe_text[:8000]}).encode('utf-8')
    req = urllib.request.Request(
        OLLAMA_HOST + '/api/embeddings',
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            mem_emb = result.get('embedding', [])
    except Exception as e:
        continue
    
    if not mem_emb:
        continue
    
    # 计算余弦相似度
    dot = sum(a*b for a,b in zip(session_emb, mem_emb))
    mag1 = sum(a*a for a in session_emb) ** 0.5
    mag2 = sum(a*a for a in mem_emb) ** 0.5
    
    if mag1 > 0 and mag2 > 0:
        sim = round(dot / (mag1 * mag2), 4)
        if sim > threshold:
            print('MATCH|' + filepath + '|' + title + '|' + tier + '|' + str(sim))
" | while IFS='|' read -r type filepath title tier sim; do
        if [ "$type" = "MATCH" ]; then
            echo -e "✓ 匹配 [${tier}]: $title (相似度: $sim)"
            update_access_count "$filepath"
            matched=$((matched + 1))
        fi
    done
    
    echo ""
    if [ "$matched" -gt 0 ]; then
        echo -e "${GREEN}检测完成: 匹配 $matched 条记忆${NC}"
    else
        echo -e "${YELLOW}检测完成: 无匹配记忆${NC}"
    fi
    
    return 0
}

# ===== 主入口 =====
case "$1" in
    detect)
        detect_mentions "$2" "$3"
        ;;
    test)
        echo "=== 测试向量相似度检测 ==="
        echo ""
        
        # 测试 Ollama 连接
        echo "1. 测试 Ollama 连接..."
        curl -s "$OLLAMA_HOST/api/tags" | python3 -c "
import json, sys
data = json.load(sys.stdin)
models = data.get('models', [])
print('可用模型:')
for m in models:
    print('  - ' + m.get('name', '?'))" 2>/dev/null && echo "✅ Ollama 正常" || echo "❌ Ollama 不可用"
        
        echo ""
        echo "2. 测试 embedding..."
        test_emb=$(get_embedding "测试内容")
        if [ "$test_emb" != "[]" ]; then
            echo "✅ Embedding 正常"
        else
            echo "❌ Embedding 失败"
        fi
        
        echo ""
        echo "3. 测试相似度计算..."
        sim=$(cosine_similarity "[1,0,0]" "[1,0,0]")
        echo "相同向量相似度: $sim (预期: 1.0)"
        
        sim=$(cosine_similarity "[1,0,0]" "[0,1,0]")
        echo "正交向量相似度: $sim (预期: 0.0)"
        
        echo ""
        echo "4. 测试检测功能..."
        detect_mentions "今天天气不错" "$SV_WORKSPACE"
        ;;
    help|--help|-h)
        echo "用法:"
        echo "  $0 detect <会话内容> [工作区]"
        echo "  $0 test"
        echo "  $0 help"
        echo ""
        echo "说明:"
        echo "  - detect: 检测会话内容与历史记忆的相似度，相似度 > 0.8 时更新 access_count"
        echo "  - test: 测试功能和连接"
        echo ""
        echo "示例:"
        echo "  $0 detect \"今天完成了项目交付\""
        echo "  $0 detect \"今天完成了项目交付\" ~/.openclaw/viking-maoxiami"
        ;;
    *)
        echo "用法: $0 detect <会话内容> [工作区] | test | help"
        exit 1
        ;;
esac
