---
name: fusion-search
description: 融合搜索引擎：Playwright + stealth.js 反爬 + 16引擎智能路由。支持中文/英文搜索、自动引擎选择、全文抓取、质量评分。
version: 1.0.0
author: qianliyan + xiaoxiao
trigger_keywords:
  - 搜索
  - 查一下
  - 调研
  - 最新
  - 新闻
  - 教程
  - 是什么
  - search
  - find
  - research
tools:
  - name: fusion_search
    description: 融合16引擎搜索，智能路由选择最佳引擎链，支持全文抓取和多引擎Fallback
    script: scripts/fusion_search.py
    parameters:
      query:
        type: string
        description: 搜索关键词，支持中文和英文
        required: true
      max_results:
        type: integer
        description: 最大返回结果数，默认10，最大20
        required: false
      full_content:
        type: integer
        description: 前N条结果全文抓取，默认0（不抓取），最大5
        required: false
      engine:
        type: string
        description: '搜索引擎: auto(自动)/baidu/bing_cn/google/duckduckgo/brave/sogou (默认auto)'
        required: false
      filter_low_quality:
        type: boolean
        description: 过滤低质量域名，默认true
        required: false
      rewrite:
        type: boolean
        description: 低质量时自动改写query重试，默认true
        required: false
      freshness:
        type: string
        description: '时效: hour/day/week/month/year'
        required: false
---

# 🔗 Fusion Search v1.0.0 — 融合搜索

## 概述

**Fusion Search** 融合了 Playwright 反爬浏览器和 16 引擎智能路由的搜索能力。

核心特性：
- **反爬强** — Playwright 物理浏览器 + stealth.js 反检测 + 请求节流 + 退避重试
- **引擎广** — 16个搜索引擎（7国内 + 9国际），智能路由
- **质量高** — 多引擎合并去重 + 域名信誉评分 + 低分改写重试
- **全文抓取** — 支持前N条结果自动全文提取
- **结构化输出** — 统一 JSON 格式，含 source 和 score 字段

## 安装

```bash
pip install playwright
playwright install chromium
```

## 引擎列表

### 国内引擎（7个）

| 引擎名 | URL | 语言 | 说明 |
|--------|-----|------|------|
| baidu | baidu.com | 中文 | 百度搜索，中文首选 |
| bing_cn | cn.bing.com | 中文 | Bing中国站，稳定 |
| sogou | sogou.com | 中文 | 搜狗搜索 |
| so_360 | so.com | 中文 | 360搜索 |
| wechat | wx.sogou.com | 中文 | 微信搜狗 |
| shenma | m.sm.cn | 中文 | 神马搜索（移动端） |
| bing_int | bing.com | 英文 | Bing国际站，兜底用 |

### 国际引擎（9个）

| 引擎名 | URL | 语言 | 说明 |
|--------|-----|------|------|
| google | google.com | 英文 | Google搜索，国际首选 |
| duckduckgo | duckduckgo.com | 英文 | 隐私友好 |
| brave | search.brave.com | 英文 | Brave Search |
| yahoo | search.yahoo.com | 英文 | Yahoo Search |
| startpage | startpage.com | 英文 | 隐私代理搜索 |
| ecosia | ecosia.org | 英文 | 环保搜索 |
| qwant | qwant.com | 英文 | 法国隐私引擎 |
| wolframalpha | wolframalpha.com | 英文 | 计算/知识引擎 |

## 智能路由规则

| 输入特征 | 引擎链 | 全文 |
|----------|--------|------|
| 数学/公式/计算 | WolframAlpha → DDG → Bing INT | 否 |
| 中文 + 技术/深度 | Bing CN → Baidu → Sogou → 360 → Bing INT | 3条 |
| 中文 + 新闻/时效 | 百度 → Bing CN → Sogou → Bing INT | 否 |
| 中文（普通搜索） | Baidu → Bing CN → Sogou → 360 → WeChat → Bing INT | 否 |
| 英文 + 短查询（≤3词） | Google → DDG → Brave → Yahoo | 否 |
| 英文 + 技术/深度 | Google → Bing INT → DDG | 3条 |
| 英文 + 新闻/时效 | Google(tbs) → Bing INT → Brave | 否 |
| 用户指定引擎 | 只查指定引擎 | 看参数 |

## 工作流程

```
1. 路由决策阶段
   route_query() 分析 query 特征：
   - 语言检测（中文 vs 非中文）
   - 词数判断（短查询 vs 长查询）
   - 关键词检测（技术/新闻/教程/数学）
   → 输出引擎链 + 全文配置

2. 搜索执行阶段
   Playwright 浏览器：
   - headless Chromium 启动
   - stealth.js 反检测注入
   - 引擎 URL 构建（含时效参数）
   - 请求节流（≥3s间隔）
   - 引擎切换冷却（≥2s）
   - 0结果指数退避（5s→10s→15s）
   → DOM 选择器解析 → 结构化结果

3. 评分优化阶段
   - 域名信誉评分（低质量域名-0.3）
   - 内容质量评分（含数字+0.15）
   - 权威性加分（.gov/.org+0.2）
   - 单域名集中度检测
   - 低分自动优化：
     a. 单域名排除重试
     b. 意图识别改写重试
     c. 简化query重试

4. 结果处理阶段
   - 多引擎同源去重
   - 质量评分排序
   - 低质量域名过滤
   - 全文抓取（前N条）
   → 输出 JSON 数组
```

## 输出格式

```json
[
    {
        "title": "Python 教程 — Python 3.14.5 文档",
        "url": "https://docs.python.org/zh-cn/3/tutorial/index.html",
        "snippet": "本教程被设计为针对新入门 Python 语言的程序员...",
        "content": "索引 模块 | 下一页...（9000字全文）",
        "engine": "bing_cn",
        "score": 0.85
    }
]
```

## CLI 用法

```bash
# 基本搜索（auto模式，自动路由）
python scripts/fusion_search.py "Python 教程" --max=5

# 指定引擎
python scripts/fusion_search.py "machine learning" --engine=google --max=3

# 全文抓取前2条
python scripts/fusion_search.py "最佳实践" --full=2

# 时效搜索
python scripts/fusion_search.py "news today" --freshness=day --max=5

# 中文搜索
python scripts/fusion_search.py "今天天气" --engine=baidu --max=3

# 禁用自动改写
python scripts/fusion_search.py "特殊查询" --no-rewrite

# 禁用低质量过滤
python scripts/fusion_search.py "论坛讨论" --no-filter
```

## Python API

```python
from fusion_search import search

# 基本搜索
results = search("Python 教程", max_results=5)

# 深度技术搜索 + 全文
results = search(
    "machine learning tutorial",
    max_results=5,
    full_content=3,
    engine="auto"
)

# 中文时效搜索
results = search(
    "最新科技新闻",
    max_results=10,
    freshness="day"
)

# 处理结果
for r in results:
    source = r["engine"]
    title = r["title"]
    score = r.get("score", 0)
    print(f"[{source}] {title} (评分: {score:.2f})")
```

## 引擎路由源码参考

路由决策在 `router.py` 中实现的 `route_query()` 函数：

```python
def route_query(query, engine="auto", max_results=10, freshness=None):
    lang = detect_language(query)
    is_short = len(query.split()) <= 3
    has_math = bool(re.search(r'[\d+\-*/^=]', query))
    has_tech = bool(re.search(r'Python|API|tutorial|教程', query, re.I))
    has_trend = bool(re.search(r'news|最新|新闻', query, re.I))

    if has_math and is_short:
        return {chain: ["wolframalpha", "duckduckgo"]}
    if lang == "zh":
        if has_tech or not is_short:
            return {chain: ["bing_cn","baidu","sogou","bing_int"], full: 3}
        return {chain: ["baidu","bing_cn","sogou","bing_int"], full: 0}
    # 非中文...
    return {chain: ["google","duckduckgo","brave"], full: 0}
```

## 注意事项

- ⚠️ 首次执行需要 `playwright install chromium`（约 300MB）
- ⚠️ Google/DDG 反爬较强，CN 环境下 Google 自动降级到 Bing
- ⚠️ 搜索耗时 10-30 秒，取决于引擎链长度和被搜索网站响应速度
- ⚠️ 部分搜索引擎 DOM 结构会变化，选择器需不定期维护
- ⚠️ 搜索引擎返回的 URL 可能是重定向链接，全文抓取会跟随

## 性能指标

| 操作 | 典型耗时 | 说明 |
|------|---------|------|
| 浏览器启动 | 1-3s | 首次搜索 |
| Bing搜索(单次) | 5-10s | 包含页面加载和DOM解析 |
| 全文抓取(单页) | 2-5s | 取决于页面复杂度和网络 |
| 链式搜索(完整) | 15-30s | 2-3个引擎+质量检查 |

## 依赖

- Python >= 3.8
- playwright（pip install playwright）
- Chromium（playwright install chromium）

## 文件结构

```
fusion-search/
├── SKILL.md              ← 本文档
├── metadata.json         ← 包元数据
├── CHANGELOG.md          ← 变更日志
├── scripts/
│   ├── fusion_search.py  ← 主入口脚本
│   ├── engines.py        ← 16引擎URL+选择器定义
│   ├── router.py         ← 路由决策逻辑
│   ├── stealth.js        ← 反检测JS脚本
│   └── scorer.py         ← 质量评分+query改写
├── references/
│   └── engine_list.md    ← 引擎手册
└── tests/
    └── test_basic.py     ← 单元测试
```

## 版权

MIT-0 — 无限制使用
