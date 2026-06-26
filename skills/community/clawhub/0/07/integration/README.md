# 集成指南

本目录包含 07-互联网访问技能与其他 AI 技能的集成工具。

## 🔗 与 AI 技能配合

### 数据流

```
┌──────────────────┐
│ 互联网平台        │ Twitter/YouTube/Reddit
└────────┬─────────┘
         │ 原始数据
         ↓
┌──────────────────┐
│ skill_bridge.py  │ 数据清洗 + 验证
└────────┬─────────┘
         │ 安全数据
         ↓
┌──────────────────────────────────┐
│          AI 技能套装              │
│                                  │
│  02-联网搜索 (缓存)              │
│       ↓                          │
│  01-长期记忆 (存储)              │
│       ↓                          │
│  06-AI总结 (分析)                │
└──────────────────────────────────┘
```

## 📦 skill_bridge.py - 安全桥接工具

**功能**：将互联网数据安全地传递给本地 AI 技能

**使用方法**：
```bash
# 完整管道
python skill_bridge.py pipeline --platform twitter --query "AI news"

# 仅获取数据
python skill_bridge.py fetch --platform youtube --query "Python教程"

# 搜索缓存
python skill_bridge.py search --query "机器学习"
```

### Python API

```python
from integration.skill_bridge import AgentReachBridge

# 初始化
bridge = AgentReachBridge(cache_dir="~/cache")

# 安全管道：获取 → 清洗 → 缓存 → 存储 → 总结
result = bridge.safe_pipeline(
    platform="twitter",
    query="AI news"
)

print(f"获取 {result['count']} 条数据")
print(result['summary'])
```

## 🔌 连接各技能

### 与 02-联网搜索 配合

```python
import sys
sys.path.insert(0, '../02-联网搜索')
from web_search import CachedSearch

# 使用搜索技能缓存互联网数据
search_skill = CachedSearch()

# 缓存 Twitter 数据
from channels.twitter import TwitterChannel
twitter = TwitterChannel()
tweets = twitter.search("AI", limit=10)

for tweet in tweets:
    search_skill._save_cache(tweet['text'], tweet, engine='twitter')
```

### 与 01-长期记忆 配合

```python
import sys
sys.path.insert(0, '../01-长期记忆')
from ai_memory import AIMemory

memory = AIMemory()

# 存储互联网数据到记忆
from integration.skill_bridge import AgentReachBridge
bridge = AgentReachBridge()

# 清洗并存储
cleaned_data = [bridge.sanitize_data(tweet) for tweet in tweets]
for item in cleaned_data:
    memory.add(item['text'], tags=['twitter', 'ai'])
```

### 与 06-AI总结 配合

```python
import sys
sys.path.insert(0, '../06-AI总结')
from summary_review_llm import AIContentSummarizer

summarizer = AIContentSummarizer()

# 总结互联网数据
all_text = '\n'.join([t['text'] for t in tweets])
summary = summarizer.summarize(all_text, 'daily')
print(summary['summary'])
```

## 🛡️ 数据清洗规则

### 自动清洗

```python
{
    'remove_patterns': [
        r'<script[^>]*>.*?</script>',  # XSS
        r'<iframe[^>]*>.*?</iframe>',  # iframe
    ],
    'max_length': 100000,  # 100KB
    'allowed_fields': [
        'text', 'url', 'author', 'timestamp',
        'platform', 'likes', 'shares'
    ]
}
```

### 手动清洗

```python
from integration.skill_bridge import AgentReachBridge

bridge = AgentReachBridge()

# 清洗单条数据
clean = bridge.sanitize_data({
    'text': '<script>alert("xss")</script>Hello',
    'author': 'user123'
})

# 结果：自动移除危险标签，添加数据哈希
```

## 🔒 安全注意事项

### 1. Cookie 管理

```bash
# 使用加密工具
python security/encrypt_cookies.py import --file cookies.json

# 不要在代码中硬编码
# ❌ 错误
cookie = "raw_cookie_value"

# ✅ 正确
from security.encrypt_cookies import CookieEncryptor
encryptor = CookieEncryptor()
cookies = encryptor.decrypt_cookies()
```

### 2. 数据验证

```python
# 验证数据来源
if data.get('platform') not in ['twitter', 'youtube', 'reddit']:
    raise ValueError("Unknown platform")

# 验证数据大小
if len(data.get('text', '')) > 100000:
    data['text'] = data['text'][:100000] + "...[truncated]"
```

### 3. 错误处理

```python
try:
    result = bridge.safe_pipeline(platform, query)
except SecurityError as e:
    log_error(f"安全错误: {e}")
    # 停止处理
except NetworkError as e:
    log_warn(f"网络错误: {e}")
    # 重试或降级
```

## 📊 性能优化

### 批量处理

```python
# 一次性获取多个查询
queries = ["AI", "机器学习", "深度学习"]
results = []

for query in queries:
    result = bridge.safe_pipeline('twitter', query)
    results.append(result)
```

### 缓存策略

```python
# 启用缓存（避免重复请求）
bridge = AgentReachBridge(
    cache_dir="~/cache",
    cache_ttl=3600  # 1小时
)
```

---

## 🎯 完整示例

### Twitter → 记忆 → 总结

```python
import sys
sys.path.insert(0, '../core')
sys.path.insert(0, '../01-长期记忆')
sys.path.insert(0, '../06-AI总结')

from llm_client import UniversalLLMClient
from ai_memory import AIMemory
from summary_review_llm import AIContentSummarizer
from integration.skill_bridge import AgentReachBridge

# 初始化
bridge = AgentReachBridge()
memory = AIMemory()
summarizer = AIContentSummarizer()

# 1. 获取数据
result = bridge.safe_pipeline('twitter', 'AI news')

# 2. 已自动缓存和存储

# 3. 生成总结
print(result['summary'])

# 4. 从记忆中检索
related = memory.search('AI', limit=5)
print(f"找到 {len(related)} 条相关记忆")
```

---

**版本**: 1.0
**更新**: 2025-02-27
