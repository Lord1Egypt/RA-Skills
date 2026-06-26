#!/bin/bash
# Smart Summarize v2.0 - 智能摘要生成
# 使用大模型或关键词提取作为回退
# 用法: smart-summarize.sh <agent_id>

AGENT_ID="${1:-main}"
WORKSPACE="$HOME/.openclaw/workspaces/$AGENT_ID"

if [ "$AGENT_ID" = "main" ]; then
    WORKSPACE="$HOME/.openclaw/workspace"
fi

MEMORY_FILE="$WORKSPACE/memory/$(date +%Y-%m-%d).md"

if [ ! -f "$MEMORY_FILE" ]; then
    echo "ℹ️ 今天的 memory 文件不存在"
    exit 0
fi

# 检查文件大小
FILE_SIZE=$(wc -c < "$MEMORY_FILE")
if [ "$FILE_SIZE" -lt 500 ]; then
    echo "ℹ️ 内容太少，跳过摘要"
    exit 0
fi

echo "🧠 生成智能摘要..."

# 使用 Python 处理
python3 - "$MEMORY_FILE" << 'PYEOF'
import os
import json
import urllib.request
import urllib.error
from datetime import datetime
import sys
import re
from collections import Counter

memory_file = sys.argv[1] if len(sys.argv) > 1 else ''

# 读取内容
with open(memory_file, 'r') as f:
    content = f.read()

# 提取关键词作为基础摘要
keywords = re.findall(r'[\u4e00-\u9fa5]{2,}', content)
word_freq = Counter(keywords)
top_keywords = [w for w, _ in word_freq.most_common(5) if len(w) >= 2]

# 尝试调用大模型（快速超时）
summary = None
try:
    config_file = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        provider = config.get('models', {}).get('providers', {}).get('default', {})
        api_key = provider.get('apiKey', '')
        base_url = provider.get('baseUrl', '')
        model = provider.get('models', [{}])[0].get('id', 'qwen3.5-plus')
        
        if api_key and base_url:
            recent_content = content[-2000:] if len(content) > 2000 else content
            
            request_data = {
                "model": model,
                "messages": [{
                    "role": "user",
                    "content": f"用3个要点总结以下内容（每点10字内）：\n{recent_content[:1500]}"
                }],
                "max_tokens": 100
            }
            
            req = urllib.request.Request(
                f"{base_url}/chat/completions",
                data=json.dumps(request_data).encode('utf-8'),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            summary = result.get('choices', [{}])[0].get('message', {}).get('content', '')
except Exception:
    pass  # 回退到关键词

# 如果大模型失败，使用关键词
if not summary or len(summary) < 10:
    summary = "📝 关键词: " + ", ".join(top_keywords)

# 检查是否已有摘要
if "## 📝 今日摘要" in content:
    print("ℹ️ 摘要已存在")
    print()
    print(summary)
else:
    # 添加摘要
    timestamp = datetime.now().strftime('%H:%M')
    header = f"""# {datetime.now().strftime('%Y-%m-%d')} 日志

## 📝 今日摘要 ({timestamp})

{summary}

---
"""
    # 跳过原有标题
    lines = content.split('\n')
    if lines[0].startswith('# 20'):
        rest = '\n'.join(lines[1:])
    else:
        rest = content
    
    with open(memory_file, 'w') as f:
        f.write(header + rest)
    
    print("✅ 已生成摘要")
    print()
    print(summary)
PYEOF
