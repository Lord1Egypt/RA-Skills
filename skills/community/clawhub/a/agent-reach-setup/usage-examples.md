# Agent Reach 使用示例

## 基本用法

### 检查系统状态
```bash
agent-reach doctor
```

### 监控渠道状态
```bash
agent-reach watch
```

### 配置代理
```bash
agent-reach configure proxy http://user:pass@ip:port
```

### 配置Twitter cookies
```bash
agent-reach configure twitter-cookies "PASTED_STRING"
```

## 渠道使用示例

### YouTube 视频信息提取
```bash
# 获取视频信息
yt-dlp --dump-json "https://www.youtube.com/watch?v=VIDEO_ID"

# 下载字幕
yt-dlp --write-sub --sub-lang en "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Twitter/X 推文搜索
```bash
# 搜索推文
xreach search "query" --json

# 获取用户时间线
xreach timeline "username" --limit 10
```

### 全网语义搜索
```bash
# 使用 mcporter 进行搜索
mcporter call 'exa.web_search_exa(query="人工智能最新进展", numResults=10)'
```

### 网页内容读取
```bash
# 使用 Jina Reader 读取网页
curl -s "https://r.jina.ai/https://example.com/article"
```

### RSS/Atom 订阅源
```bash
# Python 读取 RSS
python3 -c "
import feedparser
d = feedparser.parse('https://example.com/rss')
for entry in d.entries:
    print(entry.title)
"
```

### 微信公众号文章
```bash
# 搜索公众号文章
python3 -c "
from wechat_article_for_ai import search_articles
results = search_articles('人工智能', max_results=10)
for r in results:
    print(r['title'])
"
```

## 高级用法

### 批量处理 YouTube 视频
```bash
#!/bin/bash
# 批量获取视频信息
VIDEOS=(
    "VIDEO_ID_1"
    "VIDEO_ID_2"
    "VIDEO_ID_3"
)

for video in "${VIDEOS[@]}"; do
    echo "Processing: $video"
    yt-dlp --dump-json "https://www.youtube.com/watch?v=$video" > "video_$video.json"
done
```

### 自动化 Twitter 监控
```bash
#!/bin/bash
# 监控特定关键词
KEYWORDS=("AI" "Machine Learning" "OpenClaw")
INTERVAL=3600 # 每小时

while true; do
    for keyword in "${KEYWORDS[@]}"; do
        xreach search "$keyword" --json > "tweets_$(date +%Y%m%d_%H%M%S)_$keyword.json"
    done
    sleep $INTERVAL
done
```

### 多渠道内容聚合
```python
#!/usr/bin/env python3
# 聚合多个渠道的内容
import json
import subprocess

def get_youtube_videos(query):
    """获取YouTube视频"""
    result = subprocess.run(
        ['yt-dlp', '--dump-json', f'ytsearch10:{query}'],
        capture_output=True, text=True
    )
    return [json.loads(line) for line in result.stdout.strip().split('\n') if line]

def search_twitter(query):
    """搜索Twitter"""
    result = subprocess.run(
        ['xreach', 'search', query, '--json'],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def search_web(query):
    """网页搜索"""
    result = subprocess.run(
        ['curl', '-s', f'https://r.jina.ai/http://ddg.gg/?q={query}'],
        capture_output=True, text=True
    )
    return result.stdout

# 聚合AI相关内容
ai_content = {
    'youtube': get_youtube_videos('人工智能'),
    'twitter': search_twitter('AI 进展'),
    'web': search_web('人工智能新闻')
}

with open('ai_content_aggregation.json', 'w') as f:
    json.dump(ai_content, f, ensure_ascii=False, indent=2)
```

## 集成示例

### 与 OpenClaw 集成
```python
# 在 OpenClaw 技能中使用 Agent Reach
def get_latest_ai_news():
    """获取最新AI新闻"""
    import subprocess
    import json
    
    # 从多个渠道获取信息
    sources = {
        'youtube': 'yt-dlp --dump-json ytsearch5:"AI技术"',
        'twitter': 'xreach search "人工智能" --json',
    }
    
    results = {}
    for source, command in sources.items():
        try:
            result = subprocess.run(
                command.split(), 
                capture_output=True, 
                text=True
            )
            results[source] = json.loads(result.stdout)
        except:
            results[source] = []
    
    return results
```

### 与 Claude Code 集成
```python
# 在 Claude Code 项目中使用
import os
import subprocess

class AgentReachTool:
    def __init__(self):
        self.check_installation()
    
    def check_installation(self):
        """检查 Agent Reach 是否安装"""
        try:
            subprocess.run(['agent-reach', 'doctor'], check=True)
        except:
            print("请先安装 Agent Reach")
    
    def search_content(self, query, sources=['all']):
        """搜索内容"""
        results = {}
        
        if 'youtube' in sources or 'all' in sources:
            results['youtube'] = self.search_youtube(query)
        
        if 'twitter' in sources or 'all' in sources:
            results['twitter'] = self.search_twitter(query)
        
        return results
    
    def search_youtube(self, query):
        """搜索 YouTube"""
        cmd = f'yt-dlp --dump-json ytsearch10:"{query}"'
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        return [json.loads(line) for line in result.stdout.strip().split('\n') if line]
    
    def search_twitter(self, query):
        """搜索 Twitter"""
        cmd = f'xreach search "{query}" --json'
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        return json.loads(result.stdout)

# 使用示例
tool = AgentReachTool()
news = tool.search_content("AI技术突破")
```

## 性能优化

### 并行处理
```bash
# 并行获取多个视频信息
parallel yt-dlp --dump-json {} ::: $(cat video_urls.txt)
```

### 缓存机制
```python
import hashlib
import os
import json
from functools import wraps

def cache_result(cache_dir="/tmp/agent_reach_cache"):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存目录
            os.makedirs(cache_dir, exist_ok=True)
            
            # 生成缓存键
            key = f"{func.__name__}_{hashlib.md5(str(args).encode()).hexdigest()}"
            cache_file = os.path.join(cache_dir, key)
            
            # 检查缓存
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    return json.load(f)
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            with open(cache_file, 'w') as f:
                json.dump(result, f)
            
            return result
        return wrapper
    return decorator

@cache_result()
def get_cached_video_info(video_id):
    """获取并缓存视频信息"""
    import subprocess
    import json
    cmd = f'yt-dlp --dump-json "https://www.youtube.com/watch?v={video_id}"'
    result = subprocess.run(cmd.split(), capture_output=True, text=True)
    return json.loads(result.stdout)
```

---

**这些示例展示了如何在实际项目中使用 Agent Reach 的各种功能。**