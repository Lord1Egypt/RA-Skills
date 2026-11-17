# 示例：Airtable 社区爬虫完整案例（v3.4.0）

> 来源：TRAE 社区《编程实践：如何使用 AI 写爬虫获取数据》教程
> 演示方法论：M22+M23+M24+M26 联动
> 用途：场景 1 旗舰案例，演示 SPA 识别→动态 Key 模拟→增量唯一 ID→飞书双存储完整流程

## 案例背景

**用户需求**：抓取 airtable community 论坛的帖子数据，本地 CSV + 飞书多维表格双存储，增量同步（只抓新的，不重复）。

**字段需求**：帖子标题 / 发送人 / 帖子发送时间 / 点赞量 / 阅读量 / 评论数 / 帖子分类 / 内容 / 帖子链接 / 主题帖链接 / 项目类型 / 唯一ID

---

## Step 1：需求提示词（用户填写）

```
URL：https://community.airtable.com/search/activity/recent

需求：爬取 airtable community 的数据

需要获取的内容：
- 帖子标题
- 发送人
- 帖子发送时间
- 点赞量
- 阅读量
- 评论数
- 帖子分类
- 内容
- 帖子链接
- 主题帖链接
- 项目类型
- 唯一ID

其他要求：
- 只获取最新的帖子和回复
- 重复的内容请自动忽略，不要保存
- 测试的状态获取 5 条数据

存储：
- 先保存一份为本地 csv 文件
- 再把数据保存在多维表格里
- 往多维表格里写入的方式，参考「BaseOpenSDK（Python）官方文档.md」
- PERSONAL_BASE_TOKEN 是 "xxx"
```

---

## Step 2：网站类型评估（M22 SPA 识别）

### AI 分析

**判断 1：是否 SPA？**

打开 `https://community.airtable.com/search/activity/recent`，按 Ctrl+U 查看源码，搜索帖子标题 → **搜不到** → 是 SPA。

**判断 2：找真实数据 API**

F12 → Network → XHR/Fetch → 刷新页面 → 搜索帖子标题 → 定位到请求：

```
URL：https://xxxx.algolia.net/query
Method：POST
Headers：
  - X-API-Key: [动态]
  - Content-Type: application/json
Body：
{
  "requests": [{
    "indexName": "topics",
    "params": "query=&hitsPerPage=20&page=0"
  }]
}
```

**判断 3：API Key 是否动态？**

复制 Key 直接用 → 几分钟后 401 → 是动态 Key。

**结论**：场景 1 + M22（SPA）+ M23（动态 Key）+ M14（增量）+ M24（唯一 ID）+ M26（飞书存储）

---

## Step 3：动态 Key 模拟（M23）

### Key 获取链路分析

通过 Network 面板追踪：

1. 用户访问页面 → 返回 HTML + Cookie
2. HTML 内嵌 JS 脚本 → 请求授权端点
3. 授权端点返回 Algolia API Key
4. 前端用 Key 调用 Algolia API

### Python 实现

```python
import requests
import re

session = requests.Session()

# Step 1: 访问页面，获取初始 Cookie
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
resp1 = session.get('https://community.airtable.com/', headers=headers)

# Step 2: 从 HTML 提取授权参数（或请求授权端点）
# 假设 HTML 中有 <script>window.algoliaConfig = {...}</script>
match = re.search(r'window\.algoliaConfig\s*=\s*({.*?})', resp1.text, re.DOTALL)
if match:
    import json
    config = json.loads(match.group(1))
    api_key = config.get('api_key')
else:
    # 请求授权端点
    auth_resp = session.post(
        'https://community.airtable.com/api/algolia/key',
        headers={'X-CSRF-Token': session.cookies.get('csrf_token')}
    )
    api_key = auth_resp.json()['key']

# Step 3: 用动态 Key 调用 Algolia API
algolia_resp = session.post(
    'https://xxxx.algolia.net/query',
    headers={
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    },
    json={
        "requests": [{
            "indexName": "topics",
            "params": "query=&hitsPerPage=5&page=0"
        }]
    }
)

data = algolia_resp.json()
hits = data['results'][0]['hits']
print(f"获取到 {len(hits)} 条数据")
```

---

## Step 4：增量唯一 ID 设计（M24）

### ID 策略选择

按决策树：

1. 有 URL？✅ `topic_url`
2. 选策略 1：URL 解析 ID

### 实现

```python
import re

def extract_tid(topic_url: str) -> str:
    """从 topic_url 解析 tid 作为唯一 ID"""
    match = re.search(r'/t/topic/(\d+)', topic_url)
    if match:
        return match.group(1)
    return None

# 测试
url = "https://community.airtable.com/t/topic/12345"
print(extract_tid(url))  # "12345"
```

### 增量缓存

```python
import json
import os

def load_cache(cache_path='ids_cache.json'):
    """加载已抓取的 ID"""
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

def save_cache(ids, cache_path='ids_cache.json'):
    """保存 ID 缓存"""
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(list(ids), f, ensure_ascii=False)

# 增量过滤
existing_ids = load_cache()
new_hits = [h for h in hits if extract_tid(h['topic_url']) not in existing_ids]

print(f"总抓取：{len(hits)} 条，新增：{len(new_hits)} 条")
```

---

## Step 5：字段映射与转换（M26）

### 字段映射表

| 业务字段 | API 字段路径 | 飞书字段名 | 飞书类型 | Python 数据 |
|---------|------------|----------|---------|------------|
| 帖子标题 | hits[].title | 帖子标题 | 文本 | str |
| 发送人 | hits[].author.name | 发送人 | 文本 | str |
| 帖子发送时间 | hits[].created_at | 帖子发送时间 | 日期 | Unix 秒→毫秒 |
| 点赞量 | hits[].like_count | 点赞量 | 数字 | int |
| 阅读量 | hits[].views | 阅读量 | 数字 | int |
| 评论数 | hits[].posts_count | 评论数 | 数字 | int |
| 帖子分类 | hits[].category.name | 帖子分类 | 单选 | str |
| 内容 | hits[].first_post | 内容 | 多行文本 | str |
| 帖子链接 | hits[].topic_url | 帖子链接 | 超链接 | dict |
| 主题帖链接 | hits[].parent_url | 主题帖链接 | 超链接 | dict |
| 项目类型 | hits[].type | 项目类型 | 单选 | str |
| 唯一ID | extract_tid(topic_url) | 唯一ID | 文本 | str |

### 数据转换

```python
from datetime import datetime

def format_record(hit: dict) -> dict:
    """把 API 响应转为飞书多维表格格式"""
    return {
        "帖子标题": hit.get('title', ''),
        "发送人": hit.get('author', {}).get('name', ''),
        "帖子发送时间": hit.get('created_at', 0) * 1000,  # 秒→毫秒
        "点赞量": hit.get('like_count', 0),
        "阅读量": hit.get('views', 0),
        "评论数": hit.get('posts_count', 0),
        "帖子分类": hit.get('category', {}).get('name', '未分类'),
        "内容": hit.get('first_post', '')[:10000],  # 截断到 10000 字符
        "帖子链接": {"link": hit.get('topic_url', ''), "text": "查看原文"},
        "主题帖链接": {"link": hit.get('parent_url', ''), "text": "查看主题"},
        "项目类型": hit.get('type', '帖子'),
        "唯一ID": extract_tid(hit.get('topic_url', ''))
    }
```

---

## Step 6：双存储实现（M26）

### CSV + 飞书双存储

```python
import csv
import os
import requests
from typing import List, Dict

def save_to_csv(records: List[Dict], filepath='airtable_posts.csv'):
    """CSV 存储（追加模式）"""
    if not records:
        return
    keys = list(records[0].keys())
    write_header = not os.path.exists(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if write_header:
            writer.writeheader()
        writer.writerows(records)

def save_to_feishu(records: List[Dict], app_token, table_id, token):
    """飞书多维表格批量写入"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"records": [{"fields": r} for r in records]}
    resp = requests.post(url, headers=headers, json=payload)
    return resp.json()

# 主流程
def crawl_and_store():
    # ...（省略前面抓取逻辑）
    
    # 增量过滤
    existing_ids = load_cache()
    new_hits = [h for h in hits if extract_tid(h['topic_url']) not in existing_ids]
    
    if not new_hits:
        print("无新数据")
        return
    
    # 格式化
    records = [format_record(hit) for hit in new_hits]
    
    # 双存储
    save_to_csv(records)
    save_to_feishu(records, APP_TOKEN, TABLE_ID, FEISHU_TOKEN)
    
    # 更新缓存
    new_ids = {r['唯一ID'] for r in records}
    save_cache(existing_ids | new_ids)
    
    print(f"✅ 完成：抓取 {len(hits)} 条，新增 {len(new_hits)} 条")
```

---

## Step 7：测试验证（M7 验真）

### 测试 5 条数据

```python
# 测试模式：只抓 5 条
test_hits = hits[:5]
test_records = [format_record(hit) for hit in test_hits]

# 验证字段完整性
for r in test_records:
    assert r['帖子标题'], "帖子标题为空"
    assert r['唯一ID'], "唯一ID 为空"
    assert isinstance(r['帖子发送时间'], int), "时间格式错误"
    assert isinstance(r['帖子链接'], dict), "超链接格式错误"

print("✅ 字段验证通过")

# 测试双存储
save_to_csv(test_records, 'test.csv')
save_to_feishu(test_records, APP_TOKEN, TABLE_ID, FEISHU_TOKEN)
print("✅ 双存储测试通过")
```

### 验真抽查 3 件事

1. **抽查 5 条数据**：打开飞书多维表格，确认 5 条数据已写入
2. **验证字段类型**：
   - 日期字段显示为"2026-07-26"格式（非数字）
   - 超链接可点击（非纯文本）
   - 单选显示为标签（非纯文本）
3. **验证增量**：再跑一次，应该 0 条新增

---

## 调试历程（教程原话）

> "Airtable 社区爬虫的开发经历了一个较为复杂的调试过程，主要挑战在于其前端内容依赖于 JavaScript 动态加载，并且其核心数据通过背后调用的 Algolia 搜索服务获取，该服务需要动态生成的 API 密钥。"

**调试顺序**：
1. ❌ 初步尝试 `requests.get()` → 抓不到数据（SPA）
2. ✅ 转向网络请求分析（XHR/Fetch）→ 找到 Algolia API
3. ❌ 直接复制 API Key → 401（动态 Key）
4. ✅ 用 Session 模拟完整链路 → 成功
5. ✅ 设计 tid 唯一 ID → 增量同步成功
6. ✅ 飞书字段类型转换 → 双存储成功

---

## 经验总结

### 教程核心经验（原话）

1. **动态内容与 SPA 的挑战**：必须分析其背后真实的数据 API
2. **API 密钥的动态性**：必须模拟前端获取动态 Key 的完整流程
3. **`requests.Session` 的妙用**：Cookie 管理神器
4. **User-Agent 与请求头**：必须接近真实浏览器
5. **仔细分析 API 响应结构**：不要假设字段名
6. **增量抓取的关键：唯一且稳定的 ID**
7. **外部 SDK 的使用：数据格式化与对端系统要求**

### 模型选择经验（教程原话）

> "从 0 写一个项目的时候，使用有「推理」能力的大模型，它的规划能力会更强。例如 Gemini 2.5 Pro、DeepSeek R1。"
> "修改文案、配置之类的，可以用普通的模型，例如 DeepSeek V3。"
> "修复同一个问题，超过 3 次还没解决，需要让 AI 想一些其他办法。"

---

## 成果

- ✅ 成功抓取 airtable community 论坛数据
- ✅ 双存储：本地 CSV + 飞书多维表格
- ✅ 增量同步：每天自动跑，只抓新增
- ✅ 重复自动忽略

**后续可拓展**：
- 抓取回复内容（reply 字段）
- 抓取主题帖（parent topic）
- 增加情感分析
- 接入飞书 IM 推送新帖通知

## 版本

- v3.4.0（2026-07-26）：首次创建，源自 TRAE 社区爬虫教程
