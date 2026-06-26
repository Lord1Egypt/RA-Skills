---
name: xhs-explore
description: 小红书笔记浏览与数据采集。首页推荐、详情页抓取、评论采集、内容分析。
emoji: 📖
version: "1.0.0"
triggers:
  - 浏览
  - 推荐
  - 看详情
  - 笔记分析
  - explore
---

# 📖 xhs-explore

> 小红书笔记浏览与数据采集完整指南

## 何时触发

- "看看这篇笔记"
- "浏览首页推荐"
- "采集评论"
- "分析内容结构"
- `/xhs-explore`

---

## 前置必检

```python
status = await mcp.check_login_status()
assert status["logged_in"], "❌ 未登录"
```

---

## 笔记详情采集

### 获取单篇笔记详情

```python
# 获取笔记详细内容
note = await mcp.get_note_detail(
    note_id="64xxxxxxx",
    fetch_comments=True  # 同时获取评论
)

# 返回格式
{
    "note_id": "64xxxxxxx",
    "title": "笔记标题",
    "content": "正文内容（可能已脱敏）",
    "user_id": "xxxxxxxx",
    "nickname": "博主昵称",
    "user_avatar": "https://...",
    "likes": 2345,
    "collects": 1234,
    "comments_count": 89,
    "share_count": 45,
    "created_at": "2026-04-20T10:00:00Z",
    "topics": ["#标签1#", "#标签2#"],
    "image_urls": ["https://..."],
    "video_url": "https://...",  # 视频笔记才有
    "ip_location": "广东",
    "comments": [
        {
            "comment_id": "xxx",
            "user_nickname": "用户名",
            "content": "评论内容",
            "likes": 12,
            "created_at": "2026-04-21T...",
            "replies": [
                {
                    "reply_id": "yyy",
                    "content": "回复内容",
                    "likes": 5
                }
            ]
        }
    ]
}
```

### xsec_token 获取（重要）

某些笔记详情需要 `xsec_token` 参数：
- 从搜索结果中获取：`xsec_token` 字段
- 从推荐流中获取：每次请求会自动刷新
- **不可自行编造**，否则接口报错

```python
# xsec_token 必须从搜索/推荐结果中提取
search_result = await mcp.search_feeds("关键词")
note_id = search_result['items'][0]['note_id']
xsec_token = search_result['items'][0].get('xsec_token')

# 使用 xsec_token 获取详情
note = await mcp.get_note_detail(
    note_id=note_id,
    xsec_token=xsec_token
)
```

---

## 首页推荐流采集

```python
# 获取首页推荐内容
feed = await mcp.get_home_feed(
    feed_type="recommend",  # recommend / following / nearby
    page=1,
    page_size=20
)

# 返回格式
{
    "items": [
        {
            "note_id": "64xxxxxxx",
            "title": "标题",
            "nickname": "博主",
            "likes": 123,
            "image_urls": ["..."],
            "xsec_token": "xxxxx",  # 获取详情时需要
            "created_at": "...",
            "type": "normal"  # normal / video
        }
    ],
    "has_more": true,
    "next_cursor": "xxxxx"
}
```

---

## 评论数据采集

### 分页获取评论

```python
async def get_all_comments(mcp, note_id, max_pages=10):
    """获取笔记所有评论"""
    all_comments = []
    
    for page in range(1, max_pages + 1):
        comments = await mcp.get_note_comments(
            note_id=note_id,
            page=page,
            page_size=20,
            sort="like_desc"  # like_desc=按点赞排序, time_desc=最新
        )
        
        all_comments.extend(comments['items'])
        
        if not comments.get('has_more'):
            break
        
        # 限流
        await asyncio.sleep(2)
    
    return all_comments

# 使用
comments = await get_all_comments(mcp, "64xxxxxxx")
```

### 评论内容分析

```python
def analyze_comments(comments):
    """分析评论特征"""
    total = len(comments)
    if total == 0:
        return None
    
    positive = 0
    negative = 0
    questions = 0
    keywords = []
    
    positive_words = ["喜欢", "种草", "推荐", "好用", "好看", "绝了"]
    negative_words = ["失望", "踩雷", "不好", "后悔", "假货"]
    question_words = ["怎么", "哪里", "多少", "是否", "?"]
    
    for c in comments:
        content = c['content']
        if any(w in content for w in positive_words):
            positive += 1
        if any(w in content for w in negative_words):
            negative += 1
        if any(w in content for w in question_words):
            questions += 1
    
    return {
        'total': total,
        'positive_rate': round(positive / total * 100, 1),
        'negative_rate': round(negative / total * 100, 1),
        'question_rate': round(questions / total * 100, 1),
        'top_liked': sorted(comments, key=lambda x: x['likes'], reverse=True)[:5]
    }
```

---

## 批量采集策略

### 多笔记并发采集

```python
import asyncio

async def batch_fetch_notes(mcp, note_ids, max_concurrent=3):
    """并发采集多篇笔记详情"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_one(note_id):
        async with semaphore:
            try:
                note = await mcp.get_note_detail(note_id)
                await asyncio.sleep(1)  # 避免并发过高
                return note
            except Exception as e:
                print(f"获取失败 {note_id}: {e}")
                return None
    
    results = await asyncio.gather(*[
        fetch_one(nid) for nid in note_ids
    ])
    return [r for r in results if r is not None]

# 使用
note_ids = ["id1", "id2", "id3", "id4", "id5"]
notes = await batch_fetch_notes(mcp, note_ids, max_concurrent=3)
```

### 采集时间分散

```python
def should_fetch_now():
    """判断当前是否适合采集"""
    now = datetime.now().hour
    
    # 避免高峰期（平台风控更严）
    if now in [9, 12, 20, 21]:
        return False, f"高峰时段（{now}点），建议等待"
    
    # 检查今日采集量
    daily_count = get_daily_fetch_count()
    if daily_count > 500:
        return False, "今日采集量已达上限"
    
    return True, "可以采集"
```

---

## 数据存储格式

```python
def save_notes_to_json(notes, filepath):
    """保存笔记数据到 JSON"""
    import json
    from datetime import datetime
    
    data = {
        "fetch_time": datetime.now().isoformat(),
        "total": len(notes),
        "notes": []
    }
    
    for note in notes:
        data["notes"].append({
            "note_id": note.get("note_id"),
            "title": note.get("title"),
            "user_id": note.get("user_id"),
            "nickname": note.get("nickname"),
            "likes": note.get("likes"),
            "collects": note.get("collects"),
            "comments_count": note.get("comments_count"),
            "content": note.get("content", "")[:500],  # 截断存储
            "topics": note.get("topics", []),
            "ip_location": note.get("ip_location"),
            "created_at": note.get("created_at")
        })
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已保存 {len(notes)} 篇笔记到 {filepath}")
```

---

## 内容结构分析

```python
def analyze_note_structure(note):
    """分析单篇笔记内容结构"""
    content = note.get("content", "")
    
    analysis = {
        "content_length": len(content),
        "has_emoji": any(ord(c) > 127 for c in content),  # 包含emoji
        "paragraphs": content.count("\n\n") + 1,
        "has_hashtags": "#" in content,
        "has_mentions": "@" in content,
        "mentions": re.findall(r'@(\w+)', content),  # @的用户
        "hashtags": re.findall(r'#(\w+)#', content),  # 话题标签
        "image_count": len(note.get("image_urls", [])),
        "is_video": "video_url" in note,
    }
    
    # 内容段落分析
    if analysis["paragraphs"] <= 3:
        analysis["structure"] = "短内容（≤3段）"
    elif analysis["paragraphs"] <= 6:
        analysis["structure"] = "中等内容（4-6段）"
    else:
        analysis["structure"] = "长内容（>6段）"
    
    return analysis
```

---

## 防封采集要点

1. **间隔控制**：每次请求间隔 ≥2 秒
2. **批量限制**：单次批量 ≤20 篇
3. **时段选择**：避免 9/12/20/21 点高峰
4. **缓存复用**：相同笔记不重复获取
5. **错峰执行**：大批量任务分散到深夜

---

*Version: 1.0.0 | Updated: 2026-04-23*