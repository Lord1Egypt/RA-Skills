---
name: design-inspiration-collector
description: 双平台设计灵感收集技能。当用户需要设计参考、UI灵感、视觉创意时触发。用户提出设计方向（如"医疗App"、"移动端UI"、"金融Dashboard"等），技能负责：(1) 使用Tavily搜索Dribbble、Pinterest两个平台的官方搜索结果（不包含个人作品集、画板）(2) 整理内容并附上链接 (3) 输出 Markdown 文档，命名为"关键词+日期时间"格式 (4) 推荐其他相关方向（不带链接）。触发词：找灵感、收集灵感、设计参考、UI参考、视觉灵感、设计趋势、Dribbble、Pinterest。
---

# 双平台设计灵感收集器（Dribbble + Pinterest）

帮助用户从 **Dribbble、Pinterest 两大平台**高效收集设计灵感，**只取平台官方搜索/标签页结果**，不混入个人作品集与个人画板。

## 功能特点

1. **双平台搜索**：自动搜索 Dribbble 和 Pinterest 两个设计平台
2. **过滤策略**：只保留平台**官方搜索页 / 官方标签页 / 官方话题页**，不包含个人作品集、个人画板
3. **趋势分析**：提取 AI 设计趋势摘要
4. **推荐相关**：推荐相关设计方向供进一步探索

---

## 工作流程

### Step 1: 理解需求

当用户提出设计方向时，确认：
- 具体领域（App 类型、设计风格、平台等）
- 是否有细分要求（如"只看移动端"、"只要 Dashboard"）

### Step 2: 双平台搜索（核心）

使用 Tavily API 搜索两个平台。**关键约束**：搜索结果必须是平台的"大搜索"入口或标签页，**不能是个人作品集或个人画板**。

#### 搜索 Query 模板

```python
# Dribbble - 搜索页 / 标签页
dribbble_query = f"site:dribbble.com {主题} ui design 2026"

# Pinterest - 大搜索 / ideas 页
pinterest_query = f"site:pinterest.com {主题} ui design"
```

#### URL 白名单（必须严格遵守）

**Dribbble 只允许保留以下 URL 模式：**
- ✅ `https://dribbble.com/search/...`（关键词搜索页）
- ✅ `https://dribbble.com/tags/...`（标签页）
- ✅ `https://dribbble.com/shots/popular/...`（热门作品页）
- ❌ `https://dribbble.com/{用户名}/...`（个人作品集 — 禁止）
- ❌ `https://dribbble.com/shots/{id}-...`（单个作品页 — 禁止，过于具体）

**Pinterest 只允许保留以下 URL 模式（按优先级）：**
- 🥇 **首选** `https://www.pinterest.com/search/pins/?q=...`（大搜索页 — 用户日常使用的搜索体验，海量内容 + 顶部筛选标签）
- 🥈 备选 `https://www.pinterest.com/ideas/...`（ideas 主题页 — 编辑策展，内容偏少）
- ❌ `https://www.pinterest.com/{用户名}/...`（个人画板 — 禁止）
- ❌ `https://www.pinterest.com/pin/...`（单个图钉详情 — 禁止）

> **重要**：Pinterest 必须**优先使用大搜索 URL**（`/search/pins/?q=...`），它是用户最熟悉的 Pinterest 搜索体验，内容更多、更新更快、支持顶部筛选标签二次精准。`/ideas/` 仅作为补充。

#### 过滤逻辑

```python
# Dribbble 过滤
def is_valid_dribbble(url):
    if "/search/" in url or "/tags/" in url:
        return True
    return False

# Pinterest 过滤  
def is_valid_pinterest(url):
    if "/search/pins" in url or "/ideas/" in url or "/search/?" in url:
        return True
    return False
```

如果搜索结果命中过多个人页面，**必须**调整 query 重搜，或者直接构造平台标准搜索 URL：

```
Dribbble 标准搜索:  https://dribbble.com/search/{关键词用-连接}
Dribbble 标签页:    https://dribbble.com/tags/{关键词用-连接}
Pinterest 大搜索:   https://www.pinterest.com/search/pins/?q={关键词用%20连接}
Pinterest ideas:   https://www.pinterest.com/ideas/{关键词用-连接}/
```

### Step 3: 整理输出

不再创建腾讯文档，直接生成 **Markdown 文件** 写入工作区，命名格式：`{关键词}_{YYYYMMDD_HHMMSS}.md`

### Step 4: 输出模板

```markdown
# {主题} 设计灵感收集

> 收集时间：{YYYY年MM月DD日 HH:MM}
> 来源：Dribbble、Pinterest
> 总计：10 条精选搜索入口

---

## 📊 趋势概览

{AI 分析的设计趋势 5-7 条要点}

---

## 🎯 Dribbble 搜索精选 (5条)

### 1. {搜索/标签名} ⭐⭐⭐⭐⭐
- **链接**：{URL — 必须是 /search/ 或 /tags/ 类型}
- **类型**：{搜索页 / 标签页}
- **描述**：{这个搜索/标签下大概有哪些类型的作品}

...（共5条，全部为搜索页或标签页）

---

## 🎨 Pinterest 搜索精选 (5条)

### 1. {搜索/ideas 名} ⭐⭐⭐⭐⭐
- **链接**：{URL — 必须是 /search/pins 或 /ideas/ 类型}
- **类型**：{大搜索 / ideas 主题页}
- **描述**：{这个搜索下大概有哪些类型的内容}

...（共5条，全部为大搜索或 ideas 页）

---

## 🔍 推荐搜索关键词

- `{主题} ui design`
- `{主题} app ui`
- `{主题} dashboard`
- `{主题} mobile`

---

## 📌 相关方向推荐

需要我帮你搜索以下细分主题吗？

1. **{方向1}** - {简短描述}
2. **{方向2}** - {简短描述}
3. **{方向3}** - {简短描述}
```

---

## 依赖工具

| 工具 | 用途 | 安装 |
|------|------|------|
| Tavily API | 搜索 Dribbble 和 Pinterest | `pip install tavily-python` |

## 配置说明

### Tavily API Key

在环境中设置：
```bash
export TAVILY_API_KEY="tvly-你的key"
```

---

## 使用方法

### 基本用法

当用户说"帮我收集 XXX 的设计灵感"时：

1. 使用 Tavily 分别搜索 Dribbble 和 Pinterest
2. 每个平台取前 5 条**仅限搜索页/标签页/ideas 页**的结果
3. 如果初次搜索包含太多个人作品集/画板链接，**重新构造 query 或直接构造标准搜索 URL**
4. 整理成 Markdown 文件输出
5. 推荐相关方向

### 关键提示

- **必须过滤个人作品集与画板**：见 URL 白名单
- **优先返回大搜索/标签页**：让用户进入这些入口可以浏览大量作品，而非局限于某一个人
- **不再使用 Behance**：用户已确认排除

### 示例对话

**用户：** 帮我收集医疗App的设计灵感

**正确执行：**
1. 搜索 Dribbble：`site:dribbble.com healthcare app ui design`
2. 过滤后保留 5 条：例如 `dribbble.com/search/healthcare-app`、`dribbble.com/tags/medical-ui` 等
3. 搜索 Pinterest：`site:pinterest.com healthcare app ui design`
4. 过滤后保留 5 条：例如 `pinterest.com/search/pins/?q=healthcare+app+ui`、`pinterest.com/ideas/healthcare-app-design/...` 等
5. 输出 Markdown 文档：`医疗App设计灵感_20260521_102200.md`
6. 推荐相关方向：AI 问诊、健康追踪、远程医疗

**错误示范：**
- ❌ 返回 `https://dribbble.com/some-user/shots`（个人作品集）
- ❌ 返回 `https://www.pinterest.com/azart108/health-apps/`（个人画板）
- ❌ 返回 `https://dribbble.com/shots/12345-design`（单个作品页）

---

## 搜索技巧

### 构造标准搜索 URL（备用方案）

当 Tavily 搜不到合适的官方搜索入口时，可以**直接构造**：

```python
def build_dribbble_urls(keyword):
    kw = keyword.replace(" ", "-").lower()
    return [
        f"https://dribbble.com/search/{kw}",
        f"https://dribbble.com/tags/{kw}",
        f"https://dribbble.com/search/{kw}-ui",
        f"https://dribbble.com/search/{kw}-mobile",
        f"https://dribbble.com/search/{kw}-app",
    ]

def build_pinterest_urls(keyword):
    kw_q = keyword.replace(" ", "+").lower()
    kw_d = keyword.replace(" ", "-").lower()
    return [
        f"https://www.pinterest.com/search/pins/?q={kw_q}+ui+design",
        f"https://www.pinterest.com/search/pins/?q={kw_q}+app+design",
        f"https://www.pinterest.com/ideas/{kw_d}-design/",
        f"https://www.pinterest.com/search/pins/?q={kw_q}+mobile",
        f"https://www.pinterest.com/search/pins/?q={kw_q}+inspiration",
    ]
```

### 热门设计方向关键词

| 方向 | 关键词 |
|------|--------|
| 移动 App | mobile app, ios, android, app ui |
| 网页设计 | web design, landing page, website |
| 仪表盘 | dashboard, admin panel, data viz |
| 电商 | ecommerce, shop, checkout |
| 金融 | fintech, banking, crypto, payment |
| 健康 | health, medical, fitness, wellness |
| 风格 | glassmorphism, neumorphism, minimal |

---

## 注意事项

1. ✅ **只搜两个平台**：Dribbble + Pinterest，**不再搜 Behance**
2. ✅ **只要大搜索/标签页**：禁止返回个人作品集、个人画板、单个作品/图钉详情页
3. ✅ **每个平台 5 条**：合计 10 条搜索入口
4. ✅ **过滤校验**：输出前必须按 URL 白名单校验
5. ✅ **找不到合适入口时构造**：可以直接基于关键词构造标准搜索 URL
6. ✅ **Markdown 命名**：`{关键词}_{YYYYMMDD_HHMMSS}.md`
7. ✅ **星级评分**：按相关度给出 1-5 星
8. ✅ **推荐方向**：最后推荐 3-5 个相关细分方向（不带链接）
