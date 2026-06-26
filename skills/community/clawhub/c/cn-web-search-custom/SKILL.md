---
name: cn-web-search-custom
version: 2.3.0
description: 中文网页搜索 - 聚合 17 个免费搜索引擎，无需 API Key，纯网页抓取，支持公众号/财经/技术/学术/知识搜索。
author: joansongjr
author_url: https://github.com/joansongjr
repository: https://github.com/joansongjr/cn-web-search
license: MIT
tags:
  - search
  - chinese
  - wechat
  - 公众号
  - web-search
  - 360-search
  - sogou
  - bing
  - qwant
  - startpage
  - duckduckgo
  - stackoverflow
  - github
  - caixin
  - baidu
  - brave-search
  - yahoo
  - mojeek
  - toutiao
  - jisilu
  - wikipedia
  - no-api-key
  - free
  - 中文搜索
  - 百度
  - 头条搜索
  - 东方财富
  - A股
  - 财经
  - 技术搜索
  - 多引擎
  - 聚合搜索
  - 免费无需API
  - 投资
  - 知识百科
---

# 中文网页搜索 (CN Web Search)

> **⚡ 安装:**
> ```bash
> clawhub install cn-web-search
> ```

多引擎聚合搜索，**全部免费，无需 API Key，纯网页抓取**。17 个引擎覆盖中英文、公众号、技术、财经、知识百科。

## 引擎总览（17 个）

| 类别 | 引擎 | 数量 |
|------|------|------|
| 公众号 | 搜狗微信、必应索引 | 2 |
| 中文综合 | 360、搜狗、必应中文、百度、头条搜索 | 5 |
| 英文综合 | DDG Lite、Qwant、Startpage、必应英文、Yahoo、Brave Search、Mojeek | 7 |
| 技术社区 | Stack Overflow、GitHub Trending | 2 |
| 财经/投资 | 东方财富、集思录、财新 | 3 |
| 知识百科 | Wikipedia 中文、Wikipedia 英文 | 2 |

> 全部通过 `web_fetch` 抓取网页，零 API 依赖。

---

## 1. 公众号搜索

### 1.1 搜狗微信

`https://weixin.sogou.com/weixin?type=2&query=QUERY&page=1`

### 1.2 必应公众号索引

`https://cn.bing.com/search?q=site:mp.weixin.qq.com+QUERY`

---

## 2. 中文综合搜索

### 2.1 360 搜索

`https://m.so.com/s?q=QUERY`

### 2.2 搜狗网页

`https://www.sogou.com/web?query=QUERY`

### 2.3 必应中文

`https://cn.bing.com/search?q=QUERY`

### 2.4 百度

`https://www.baidu.com/s?wd=QUERY`

中文搜索覆盖最全，结果丰富。

### 2.5 头条搜索

`https://so.toutiao.com/search?keyword=QUERY`

字节跳动旗下，中文资讯和短视频内容强。

---

## 3. 英文综合搜索

### 3.1 DuckDuckGo Lite

`https://lite.duckduckgo.com/lite/?q=QUERY`

### 3.2 Qwant

`https://www.qwant.com/?q=QUERY&t=web`

### 3.3 Startpage

`https://www.startpage.com/do/search?q=QUERY&cluster=web`

### 3.4 必应英文

`https://www.bing.com/search?q=QUERY`

### 3.5 Yahoo

`https://search.yahoo.com/search?p=QUERY`

老牌英文搜索引擎，结果稳定。

### 3.6 Brave Search

`https://search.brave.com/search?q=QUERY`

独立索引（非 Bing/Google 代理），隐私友好，结果质量高。

### 3.7 Mojeek

`https://www.mojeek.com/search?q=QUERY`

独立爬虫索引，不依赖任何大厂，适合多样化结果。

---

## 4. 技术社区

### 4.1 Stack Overflow

`https://stackoverflow.com/search?q=QUERY`

### 4.2 GitHub Trending

`https://github.com/trending?since=weekly`

---

## 5. 财经/投资

### 5.1 东方财富

`https://search.eastmoney.com/search?keyword=QUERY`

### 5.2 集思录

`https://www.jisilu.cn/explore/?keyword=QUERY`

投资社区，可转债、基金、LOF 等投资品种讨论。

### 5.3 财新

`https://search.caixin.com/search/?keyword=QUERY`

---

## 6. 知识百科

### 6.1 Wikipedia 中文

`https://zh.wikipedia.org/w/index.php?search=QUERY&title=Special:Search`

中文维基百科，知识查询首选。

### 6.2 Wikipedia 英文

`https://en.wikipedia.org/w/index.php?search=QUERY&title=Special:Search`

英文维基百科，信息量最大的免费百科全书。

---

## 使用示例

**中文搜索：**
- 百度：`web_fetch(url="https://www.baidu.com/s?wd=英伟达财报", extractMode="text", maxChars=12000)`
- 360：`web_fetch(url="https://m.so.com/s?q=英伟达财报", extractMode="text", maxChars=12000)`

**英文搜索：**
- Brave：`web_fetch(url="https://search.brave.com/search?q=AI+news", extractMode="text", maxChars=8000)`
- DDG：`web_fetch(url="https://lite.duckduckgo.com/lite/?q=AI+news", extractMode="text", maxChars=8000)`

**公众号：**
- 搜狗微信：`web_fetch(url="https://weixin.sogou.com/weixin?type=2&query=英伟达&page=1", extractMode="text", maxChars=10000)`

**知识查询：**
- Wikipedia：`web_fetch(url="https://zh.wikipedia.org/w/index.php?search=量子计算&title=Special:Search", extractMode="text", maxChars=8000)`

**投资：**
- 集思录：`web_fetch(url="https://www.jisilu.cn/explore/?keyword=可转债", extractMode="text", maxChars=8000)`

---

## 引擎选择建议

| 场景 | 推荐引擎 |
|------|---------|
| 中文通用搜索 | 百度 → 360 → 搜狗 |
| 英文通用搜索 | Brave → DDG → Bing |
| 公众号文章 | 搜狗微信 → 必应索引 |
| 技术问题 | Stack Overflow → GitHub |
| 最新资讯 | 头条搜索 → 百度 |
| A股/投资 | 东方财富 → 集思录 |
| 财经深度 | 财新 |
| 知识/定义 | Wikipedia 中文 → Wikipedia 英文 |
| 隐私优先 | Brave → Mojeek → DDG |

---

## 实战对比：有 cn-web-search vs 没有

> 以投研场景为例，问同一个问题：**"英伟达2026年Q1财报业绩如何？"**

### ❌ 没有 cn-web-search（纯模型）

```
回答："我的训练数据有截止日期，无法提供最新财报数据。
      建议您查看英伟达官网 investor.nvidia.com。"
```

**结果：什么有用信息都拿不到。**

### ✅ 装了 cn-web-search（百度 + 360 + 搜狗，3 个免费引擎）

```python
web_fetch(url="https://www.baidu.com/s?wd=英伟达2027财年Q1业绩指引", extractMode="text", maxChars=3000)
web_fetch(url="https://m.so.com/s?q=英伟达2026财报Q1业绩", extractMode="text", maxChars=3000)
web_fetch(url="https://www.sogou.com/web?query=英伟达财报2026Q1业绩预测", extractMode="text", maxChars=3000)
```

**拿到的实时数据（多源交叉验证）：**

| 数据点 | 百度 | 360 | 搜狗 |
|--------|:----:|:---:|:----:|
| FY2026 Q1 营收 441 亿美元 (+69%) | ✅ | ✅ | ✅ |
| FY2026 Q4 营收 681 亿美元 (+73%) | ✅ | ✅ | ✅ |
| FY2026 全年营收 2159 亿美元 (+65%) | ✅ | ✅ | ✅ |
| FY2027 Q1 指引 780 亿（超预期 7%） | ✅ | ✅ | ✅ |
| H20 禁令影响 80 亿美元 | ✅ | ✅ | ✅ |
| 毛利率 75% | ✅ | ✅ | — |
| 黄仁勋："代理式 AI 拐点已到来" | ✅ | — | ✅ |

### 对比总结

| 维度 | 无 Skill | cn-web-search |
|------|:--------:|:-------------:|
| 实时数据 | ❌ | ✅ |
| 数据准确性 | N/A | ✅ 多源交叉验证 |
| 成本 | — | 免费 |
| 投研可用性 | 零 | 营收/利润/指引/管理层表态 |
| 信息来源 | 无 | 百度+360+搜狗+雪球+东方财富 |

> **结论：没有 cn-web-search 的 agent 在投研场景下基本是废的。装上后等于给 agent 开了一扇窗，能看到实时世界——而且完全免费。**

---

## 更新日志

### v2.2.0
- 📊 新增「实战对比」章节：有 cn-web-search vs 没有（以英伟达财报投研为例）
- 📈 展示多源交叉验证效果

### v2.1.0
- 🗑️ 移除所有 API 端点引擎（Hacker News、Reddit、ArXiv、DDG API、Wolfram Alpha）
- ✅ 全部 17 个引擎均为纯网页抓取，零 API 依赖
- 📋 更新引擎总览表和选择建议

### v2.0.0
- 🆕 新增 9 个引擎：百度、Yahoo、Brave Search、Mojeek、头条搜索、集思录、Wikipedia 中英文、DDG Instant Answer API
- 📊 引擎总数：13 → 22

### v1.0.0
- ✅ 全新发布！聚合 13+ 免费中文搜索引擎
- ✅ 无需 API Key，真正免费
- ✅ 支持公众号、知乎、财经(A股)、技术搜索
