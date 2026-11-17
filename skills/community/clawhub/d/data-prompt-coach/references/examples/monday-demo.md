# 示例：Monday 论坛爬虫案例（v3.4.0 简化版）

> 来源：TRAE 社区《编程实践：如何使用 AI 写爬虫获取数据》教程（成果展示部分）
> 演示方法论：M22+M24+M26 联动（无 M23，因为 Monday API Key 是静态的）
> 用途：场景 1 案例变体，演示不同网站类型的处理差异

## 案例背景

**用户需求**：抓取 monday.com 社区论坛数据，结构与 airtable 类似但 API 不同。

**与 airtable 案例的差异**：
- ✅ 同：都是 SPA，数据通过 API 加载
- ❌ 异：API Key 是静态的（无需 M23）
- ❌ 异：API 原生 id 字段稳定（直接用 M24 策略 2，无需 URL 解析）

---

## Step 1：网站评估

### AI 分析结果

| 评估项 | airtable community | monday community |
|--------|-------------------|-----------------|
| 是否 SPA | ✅ 是 | ✅ 是 |
| 数据 API | Algolia（动态 Key） | 原生 REST API（静态 Key） |
| 唯一 ID 策略 | URL 解析 tid | API 原生 id 字段 |
| 是否需 M23 | ✅ 是 | ❌ 否 |
| 是否需 M22 | ✅ 是 | ✅ 是 |
| 是否需 M24 | ✅ 是 | ✅ 是 |
| 是否需 M26 | ✅ 是 | ✅ 是 |

**结论**：场景 1 + M22+M24+M26（不需要 M23）

---

## Step 2：API 分析（简化）

### 找到 API

F12 → Network → 搜索帖子标题 → 定位到：

```
URL：https://api.monday.com/v2/community/posts
Method：GET
Headers：
  - Authorization: Bearer [静态 Token]
  - User-Agent: ...
Query：
  - page: 1
  - per_page: 20
  - sort: created_at:desc
```

### 响应结构

```json
{
  "data": {
    "posts": [
      {
        "id": "abc123",
        "title": "...",
        "author": {"name": "..."},
        "created_at": "2026-07-26T10:00:00Z",
        "like_count": 42,
        "views": 100,
        "comments_count": 5,
        "category": "技术",
        "content": "...",
        "url": "https://community.monday.com/t/post/abc123"
      }
    ]
  },
  "meta": {
    "total": 1000,
    "page": 1,
    "per_page": 20
  }
}
```

---

## Step 3：唯一 ID 设计（M24 策略 2）

### 选择

按决策树：
1. 有 URL？✅
2. 但选策略 2（API 原生 ID），因为 `id` 字段稳定且 API 自带

### 实现

```python
def get_unique_id(post: dict) -> str:
    """直接用 API 原生 id"""
    return post.get('id', '')

# 测试
post = {"id": "abc123", "title": "..."}
print(get_unique_id(post))  # "abc123"
```

**对比 airtable**：airtable 用 URL 解析 tid，monday 用 API 原生 id，两种策略都可行。

---

## Step 4：字段映射与转换（M26）

### 字段映射表

| 业务字段 | API 字段路径 | 飞书字段名 | 飞书类型 | 转换逻辑 |
|---------|------------|----------|---------|---------|
| 标题 | data.posts[].title | 标题 | 文本 | str |
| 作者 | data.posts[].author.name | 作者 | 文本 | str |
| 时间 | data.posts[].created_at | 时间 | 日期 | ISO 8601 → 毫秒 |
| 点赞 | data.posts[].like_count | 点赞 | 数字 | int |
| 浏览 | data.posts[].views | 浏览 | 数字 | int |
| 评论 | data.posts[].comments_count | 评论 | 数字 | int |
| 分类 | data.posts[].category | 分类 | 单选 | str |
| 内容 | data.posts[].content | 内容 | 多行文本 | str |
| 链接 | data.posts[].url | 链接 | 超链接 | dict |
| 唯一ID | data.posts[].id | 唯一ID | 文本 | str |

### 时间转换差异

**airtable**：Unix 秒 → 毫秒（`ts * 1000`）
**monday**：ISO 8601 → 毫秒（`datetime.fromisoformat().timestamp() * 1000`）

```python
from datetime import datetime

def convert_time(created_at: str) -> int:
    """ISO 8601 转 Unix 毫秒"""
    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
    return int(dt.timestamp() * 1000)

# 测试
iso_str = "2026-07-26T10:00:00Z"
print(convert_time(iso_str))  # 1785042594000
```

---

## Step 5：完整代码（简化版）

```python
import csv
import os
import json
import requests
from datetime import datetime
from typing import List, Dict

# 配置
API_URL = "https://api.monday.com/v2/community/posts"
API_TOKEN = "your_static_token"  # monday 的 Token 是静态的
FEISHU_APP_TOKEN = "BascXXX"
FEISHU_TABLE_ID = "tblXXX"
FEISHU_TOKEN = os.getenv("PERSONAL_BASE_TOKEN")

# 抓取
def fetch_posts(page=1, per_page=5):
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'User-Agent': 'Mozilla/5.0 ...'
    }
    params = {'page': page, 'per_page': per_page, 'sort': 'created_at:desc'}
    resp = requests.get(API_URL, headers=headers, params=params)
    return resp.json()['data']['posts']

# 格式化
def format_record(post: dict) -> dict:
    return {
        "标题": post.get('title', ''),
        "作者": post.get('author', {}).get('name', ''),
        "时间": convert_time(post.get('created_at', '')),
        "点赞": post.get('like_count', 0),
        "浏览": post.get('views', 0),
        "评论": post.get('comments_count', 0),
        "分类": post.get('category', '未分类'),
        "内容": post.get('content', '')[:10000],
        "链接": {"link": post.get('url', ''), "text": "查看原文"},
        "唯一ID": post.get('id', '')
    }

# 双存储
def save_to_csv(records, filepath='monday_posts.csv'):
    if not records: return
    keys = list(records[0].keys())
    write_header = not os.path.exists(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if write_header: writer.writeheader()
        writer.writerows(records)

def save_to_feishu(records):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{FEISHU_TABLE_ID}/records/batch_create"
    headers = {"Authorization": f"Bearer {FEISHU_TOKEN}", "Content-Type": "application/json"}
    payload = {"records": [{"fields": r} for r in records]}
    return requests.post(url, headers=headers, json=payload).json()

# 增量
def load_cache():
    if os.path.exists('monday_ids.json'):
        with open('monday_ids.json', 'r') as f:
            return set(json.load(f))
    return set()

def save_cache(ids):
    with open('monday_ids.json', 'w', encoding='utf-8') as f:
        json.dump(list(ids), f)

# 主流程
def main():
    posts = fetch_posts(page=1, per_page=5)
    existing_ids = load_cache()
    new_posts = [p for p in posts if p.get('id') not in existing_ids]
    
    if not new_posts:
        print("无新数据")
        return
    
    records = [format_record(p) for p in new_posts]
    save_to_csv(records)
    save_to_feishu(records)
    
    new_ids = {p['id'] for p in new_posts}
    save_cache(existing_ids | new_ids)
    print(f"✅ 完成：抓取 {len(posts)} 条，新增 {len(new_posts)} 条")

if __name__ == "__main__":
    main()
```

---

## 与 airtable 案例对比

| 维度 | airtable | monday |
|------|---------|--------|
| 数据 API | Algolia | 原生 REST |
| API Key | 动态（需 M23） | 静态（无需 M23） |
| 唯一 ID | URL 解析 tid | API 原生 id |
| 时间格式 | Unix 秒 | ISO 8601 字符串 |
| 复杂度 | 高（需模拟 Key） | 中（直接调 API） |

**结论**：不同网站的处理方式不同，方法论组合需按实际情况选择。

---

## 成果

- ✅ 成功抓取 monday community 论坛数据
- ✅ 双存储：本地 CSV + 飞书多维表格
- ✅ 增量同步：每天自动跑，只抓新增

## 版本

- v3.4.0（2026-07-26）：首次创建，源自 TRAE 社区爬虫教程成果展示
