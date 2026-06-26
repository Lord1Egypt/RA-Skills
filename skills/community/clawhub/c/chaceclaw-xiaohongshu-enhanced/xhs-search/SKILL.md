---
name: xhs-search
description: 小红书内容搜索与竞品分析。关键词策略、热门内容挖掘、批量采集。
emoji: 🔍
version: "1.0.0"
triggers:
  - 搜索
  - 竞品分析
  - 找笔记
  - 热门
  - search
---

# 🔍 xhs-search

> 小红书内容搜索与竞品分析完整指南

## 何时触发

- "搜索XX相关内容"
- "找热门笔记"
- "竞品分析"
- "看看这个话题"
- `/xhs-search`

---

## 前置必检

```python
# 1. 确认登录
status = await mcp.check_login_status()
assert status["logged_in"], "❌ 未登录"

# 2. 限流检查（搜索最容易被限流）
# 每小时 ≤30 次，间隔 ≥120 秒
```

---

## 搜索 API 使用

### 基础搜索

```python
# 搜索关键词
results = await mcp.search_feeds(
    keyword="护肤",
    sort="general",    # general=综合, time_desc=最新, popularity_desc=最热
    page=1,
    page_size=20
)

# 返回格式
{
    "items": [
        {
            "note_id": "64xxxxxxx",
            "title": "笔记标题",
            "user_id": "xxxxxxxx",
            "nickname": "博主名",
            "likes": 1234,
            "collects": 567,
            "comments": 89,
            "published_at": "2026-04-20T10:00:00Z",
            "image_urls": ["https://..."],
            "topics": ["#护肤#", "#测评#"]
        },
        ...
    ],
    "total": 15230,
    "has_more": true
}
```

### 搜索参数详解

| 参数 | 类型 | 说明 |
|------|------|------|
| `keyword` | string | 搜索关键词（支持 AND/OR） |
| `sort` | enum | 综合/最新/最热 |
| `page` | int | 页码（从1开始） |
| `page_size` | int | 每页数量（最大20） |
| `image_ratio` | string | 图片比例筛选（3:4/1:1/16:9） |
| `publish_time` | string | 时间筛选（day/week/month） |

---

## 关键词策略

### 关键词分类

| 类型 | 示例 | 用途 |
|------|------|------|
| **品牌词** | 雅诗兰黛、SK-II | 品牌声量监控 |
| **品类词** | 面霜、精华液、洗面奶 | 市场容量分析 |
| **场景词** | 换季、熬夜、通勤 | 用户需求挖掘 |
| **功效词** | 保湿、美白、抗老 | 需求分析 |
| **人群词** | 敏感肌、孕妈、学生党 | 精准定位 |

### 关键词组合

```python
# AND 组合（同时满足）
"护肤 AND 敏感肌"  # 敏感肌护肤

# OR 组合（任一满足）  
"面霜 OR 精华液"   # 护肤品类

# 排除词（不含）
"护肤 -广告 -推广"  # 非广告内容

# 组合示例
keywords = [
    "护肤",
    "敏感肌 护肤",
    "换季 护肤 推荐",
    "护肤 测评 2026"
]
```

### 热搜词跟踪

```python
# 获取实时热搜
hot_search = await mcp.get_hot_search_list()

# 返回
{
    "hot_list": [
        {"rank": 1, "word": "热搜词1", "heat": 999999},
        {"rank": 2, "word": "热搜词2", "heat": 888888},
        ...
    ],
    "update_time": "2026-04-23T12:00:00Z"
}
```

---

## 竞品笔记分析

### 批量采集竞品

```python
async def collect_competitor_notes(brand_keyword, top_n=50):
    """采集竞品爆款笔记"""
    all_notes = []
    
    # 搜索并采集多页
    page = 1
    while len(all_notes) < top_n:
        results = await mcp.search_feeds(
            keyword=brand_keyword,
            sort="popularity_desc",
            page=page,
            page_size=20
        )
        all_notes.extend(results['items'])
        
        if not results['has_more']:
            break
        page += 1
        
        # 限流：每次搜索后等待
        await asyncio.sleep(125)
    
    # 取前 top_n 条
    return all_notes[:top_n]

# 使用
competitor_notes = await collect_competitor_notes("竞品品牌名")
```

### 竞品数据分析

```python
def analyze_competitor(notes):
    """分析竞品爆款特征"""
    if not notes:
        return None
    
    total = len(notes)
    
    # 基础统计
    stats = {
        'avg_likes': sum(n['likes'] for n in notes) / total,
        'avg_collects': sum(n['collects'] for n in notes) / total,
        'top_notes': sorted(notes, key=lambda x: x['likes'], reverse=True)[:5]
    }
    
    # 标题特征词
    title_words = []
    for note in notes[:10]:  # 取前10条爆款
        title_words.extend(note['title'])
    
    # 高频词
    word_freq = Counter(title_words)
    stats['top_words'] = word_freq.most_common(10)
    
    return stats
```

### 爆款笔记特征提取

```python
def extract_viral_patterns(notes):
    """提取爆款共性"""
    patterns = {
        'title_starts': [],      # 标题开头词
        'topics': [],            # 常用话题
        'content_length': [],    # 正文长度
        'image_count': [],       # 图片数量
    }
    
    for note in notes:
        title = note['title']
        # 提取标题开头词（前2字）
        if len(title) >= 2:
            patterns['title_starts'].append(title[:2])
        # 话题
        patterns['topics'].extend(note.get('topics', []))
        # 内容长度（粗估）
        patterns['content_length'].append(len(note.get('content', '')))
    
    return patterns
```

---

## 批量采集防封技巧

```python
class SafeSearcher:
    """安全搜索包装器"""
    
    def __init__(self, mcp, max_per_hour=25):
        self.mcp = mcp
        self.max_per_hour = max_per_hour
        self.count = 0
        self.reset_at = time.time() + 3600
    
    async def search(self, *args, **kwargs):
        now = time.time()
        
        # 重置计数器
        if now > self.reset_at:
            self.count = 0
            self.reset_at = now + 3600
        
        # 检查限流
        if self.count >= self.max_per_hour:
            wait_time = self.reset_at - now
            print(f"⚠️ 限流达到，等待 {wait_time:.0f}秒")
            await asyncio.sleep(wait_time + 5)
        
        # 执行搜索
        result = await self.mcp.search_feeds(*args, **kwargs)
        
        # 计数 + 冷却
        self.count += 1
        jitter = random.uniform(1.1, 1.3)
        await asyncio.sleep(125 * jitter)
        
        return result

# 使用
searcher = SafeSearcher(mcp)
for keyword in keywords:
    results = await searcher.search(keyword=keyword)
```

---

## 搜索结果过滤

```python
# 时间过滤（只取近7天）
from datetime import datetime, timedelta

recent_cutoff = datetime.now() - timedelta(days=7)

filtered = [
    n for n in results['items']
    if datetime.fromisoformat(n['published_at'].replace('Z', '+08:00')) > recent_cutoff
]

# 热度过滤（只取点赞>100）
popular = [n for n in results['items'] if n['likes'] > 100]

# 去重（同一博主只取一篇）
seen_authors = set()
unique = []
for n in results['items']:
    if n['user_id'] not in seen_authors:
        seen_authors.add(n['user_id'])
        unique.append(n)
```

---

## 搜索黑名单

```python
BLACKLIST_WORDS = [
    "广告", "推广", "合作", "赞助",
    "代购", "引流", "私信", "加V",
    "兼职", "副业", "赚钱"
]

def contains_blacklist(title, content=""):
    """检测是否包含黑名单词"""
    text = title + content
    for word in BLACKLIST_WORDS:
        if word in text:
            return word
    return None

# 使用
for note in results['items']:
    blacklisted = contains_blacklist(note['title'], note.get('content', ''))
    if blacklisted:
        print(f"过滤广告内容: {note['title']} (含: {blacklisted})")
```

---

## 搜索命令速查

```bash
# 1. 搜索单一关键词
python3 -c "
import asyncio
from xhs_mcp import Client
async def main():
    c = Client()
    r = await c.search_feeds('护肤 测评', sort='popularity_desc', page=1)
    print(f'找到 {r[\"total\"]} 条笔记')
asyncio.run(main())
"

# 2. 采集竞品爆款（前20篇）
python3 -c "
import asyncio
from xhs_mcp import Client
async def main():
    c = Client()
    r = await c.search_feeds('竞品词', sort='popularity_desc', page=1, page_size=20)
    for n in r['items'][:20]:
        print(f'[{n[\"likes\"]}赞] {n[\"title\"]}')
asyncio.run(main())
"
```

---

*Version: 1.0.0 | Updated: 2026-04-23*