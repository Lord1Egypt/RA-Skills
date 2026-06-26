# 设计师情报站 - 执行流程说明

## 🔄 全自动执行流程（v1.5.1）

### 执行命令
```bash
./execute_daily.sh
```

### 流程步骤

#### 步骤 1: RSS 抓取
```bash
python3 tools/rss_fetcher.py fetch-all --json
```
- **抓取对象**: 6 个 RSS 源（TechCrunch, The Verge, UX Collective, Dezeen, 优设网 RSS, Moonvy Blog）
- **输出**: `/tmp/dis_daily/rss_items.json`
- **预期**: ~36 条

#### 步骤 2: API 抓取
```bash
python3 tools/api_fetcher.py fetch-all --json
```
- **抓取对象**: 4 个 API 源（GitHub Trending, Product Hunt, Hacker News, Reddit）
- **输出**: `/tmp/dis_daily/api_items.json`
- **预期**: ~15 条

#### 步骤 3: Web 抓取
```bash
python3 tools/web_fetcher_standalone.py fetch-all
```
- **抓取对象**: 28 个网页源（中文媒体 9 + 英文媒体 5 + 设计媒体 7 + 社交平台 7）
- **输出**: `data/cache/web_cache_*.json` → `/tmp/dis_daily/web_items.json`
- **预期**: ~20-24 条

#### 步骤 4: 合并结果
```bash
python3 tools/fetch_all.py --merge \
  /tmp/dis_daily/rss_items.json \
  /tmp/dis_daily/api_items.json \
  /tmp/dis_daily/web_items.json \
  --output /tmp/dis_daily/all_items.json
```
- **功能**: 合并三路数据，去重
- **输出**: `/tmp/dis_daily/all_items.json`
- **预期**: ~75 条（去重后）

#### 步骤 5: Agent 筛选和格式化
Agent 读取 `/tmp/dis_daily/all_items.json`，执行：
1. 按 5 维筛选标准判断每条情报
2. 标注条件编号 [1][2][3][4][5]
3. 分级：S/A/B/C
4. 生成 v1.3.3 格式日报
5. 发送 📊 摘要 + 📄 MD 文件给用户

---

## 📊 数据来源对比

| 来源 | 数量 | 抓取方式 | 工具 |
|------|------|---------|------|
| RSS | 6 个源 | Python requests + feedparser | `rss_fetcher.py` |
| API | 4 个源 | Python requests + 平台 API | `api_fetcher.py` |
| Web | 28 个源 | Python requests + BeautifulSoup | `web_fetcher_standalone.py` |
| **总计** | **38 个源** | **全自动化** | **无需人工干预** |

---

## 🛠️ 三种抓取方式详解

### 1. RSS 抓取

**原理**: 解析 RSS/Atom feed XML

**代码**:
```python
import feedparser
feed = feedparser.parse(url)
for entry in feed.entries:
    items.append({
        'title': entry.title,
        'link': entry.link,
        'published': entry.published,
        'summary': entry.summary
    })
```

**优点**:
- ✅ 结构化数据，解析简单
- ✅ 更新及时，几乎实时
- ✅ 服务器压力小

**缺点**:
- ⚠️ 部分网站不提供 RSS
- ⚠️ 内容摘要可能不完整

---

### 2. API 抓取

**原理**: 调用平台官方 API

**代码**:
```python
# GitHub Trending
response = requests.get('https://github.com/trending')
soup = BeautifulSoup(response.text, 'lxml')
for repo in soup.select('.Box-row'):
    items.append({
        'title': repo.select_one('h2 a').text.strip(),
        'link': repo.select_one('h2 a')['href'],
        'stars': repo.select_one('[href$="stargazers"]').text.strip()
    })
```

**优点**:
- ✅ 数据结构清晰
- ✅ 更新频率高
- ✅ 包含额外信息（stars, forks 等）

**缺点**:
- ⚠️ 部分 API 需要认证
- ⚠️ 有速率限制

---

### 3. Web 抓取

**原理**: 抓取 HTML 页面，解析提取文章列表

**代码**:
```python
headers = {'User-Agent': 'Mozilla/5.0 ...'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
for article in soup.select('article'):
    items.append({
        'title': article.select_one('h2').text,
        'link': article.select_one('a')['href'],
        'summary': article.select_one('.summary').text
    })
```

**优点**:
- ✅ 适用范围广（几乎所有网站）
- ✅ 内容完整
- ✅ 不依赖 RSS/API 支持

**缺点**:
- ⚠️ 网站结构变化会导致解析失败
- ⚠️ 可能有反爬措施
- ⚠️ 需要维护多个解析策略

---

## 📬 输出内容

### 1. 日报摘要（文字消息）

```
✅ 设计师情报站 · 2026-03-24 日报生成完成！

📊 抓取结果:
- RSS 源：36 条（4/6 成功）
- API 源：15 条（2/4 成功）
- Web 源：24 条（16/28 成功）
- 总计：75 条（去重后）

📈 分级统计:
- S 级（头条）：3 条
- A 级（重点）：5 条
- B 级（简讯）：12 条

🔥 头条情报:
1. [标题 1](链接)
2. [标题 2](链接)
3. [标题 3](链接)

📄 完整日报已以附件形式发送。
```

### 2. MD 文件（附件）

**位置**: `temp/intelligence-daily-YYYY-MM-DD.md`

**格式**: v1.3.3 结构化表格

**内容**:
- 🔴 P0 级头条（S 级情报）
- 📱 手机领域
- 🤖 AI 领域
- 🔌 智能硬件
- 🎨 设计领域
- 💡 趋势洞察（观察→洞察→建议）
- 💡 今日设计思考
- 📅 明日关注
- 📌 排除内容说明

---

## 🔧 故障排查

### 问题 1: RSS 抓取失败

**检查**:
```bash
python3 tools/rss_fetcher.py fetch-all
```

**解决**: 检查网络连接，RSS 源是否有效

### 问题 2: API 抓取失败

**检查**:
```bash
python3 tools/api_fetcher.py fetch-all
```

**解决**: 检查 API 是否变更，更新解析策略

### 问题 3: Web 抓取失败

**检查**:
```bash
python3 tools/web_fetcher_standalone.py fetch-all
```

**解决**: 
- 检查 User-Agent 是否被屏蔽
- 更新网站解析策略
- 添加代理（如需要）

### 问题 4: 合并失败

**检查**:
```bash
cat /tmp/dis_daily/rss_items.json | head -10
```

**解决**: 确保 JSON 格式正确

---

## 📋 周刊深度抓取指南

### Moonvy 设计素材周刊 + 优设网体验碎周报

**场景**: 当用户要求获取某一期周刊的完整内容时（如"把 206 期设计素材周刊发给我"）

**抓取方式**: 使用 `web_fetch` 工具直接抓取周刊详情页

**操作步骤**:

```bash
# 1. Moonvy 设计素材周刊
# URL 格式：https://moonvy.com/blog/post/设计素材周刊/{期数}/
# 示例：206 期 → https://moonvy.com/blog/post/设计素材周刊/206/

# 2. 优设网体验碎周报
# URL 格式：https://www.ftium4.com/ux-weekly-{期数}.html
# 示例：273 期 → https://www.ftium4.com/ux-weekly-273.html
```

**Agent 执行流程**:

1. **解析用户请求** — 提取周刊名称和期数
2. **构建 URL** — 根据期数拼接对应链接
3. **并行抓取** — 使用 `web_fetch` 工具（extractMode=markdown）
4. **整理输出** — 结构化整理为表格 + 分点格式
5. **发送给用户** — 直接发送整理后的内容到对话框

**注意事项**:

| 事项 | 说明 |
|------|------|
| ✅ 必须深入抓取 | 不能只停留在 RSS 摘要，要进入周刊详情页获取完整内容 |
| ✅ 保留所有链接 | 周刊中的产品/工具链接都要保留，方便用户访问 |
| ✅ 结构化整理 | 按栏目分类（资讯/产品/素材/工具等），使用表格呈现 |
| ⚠️ 期数识别 | 用户可能说"最新一期"或"上周的"，需要根据日期推算期数 |

**示例请求**:

- "把 Moonvy 设计素材周刊 206 期发给我"
- "优设网体验碎周报第 273 期有什么内容？"
- "帮我看看最新两期周刊的内容"

**工具调用示例**:

```python
web_fetch(
  url="https://moonvy.com/blog/post/设计素材周刊/206/",
  extractMode="markdown"
)

web_fetch(
  url="https://www.ftium4.com/ux-weekly-273.html",
  extractMode="markdown"
)
```

---

*最后更新：2026-03-26 | 设计师情报站 v1.6.0*
