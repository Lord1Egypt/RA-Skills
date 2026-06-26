# Deep Research v6.0 + Web Fetcher 集成指南

> 版本：v2.0  
> 描述：Web Fetcher 与深度研究v6.0的完整集成方案

---

## 架构概览

```
深度研究 v6.0
├── 配置层 (config/)
├── 检索层 (多源自适应)
│   ├── arXiv API → PDF下载 → 全文解析
│   ├── PubMed API → 摘要获取
│   ├── Web Search → URL列表
│   └── Web Fetcher → 内容抓取 ⬅️ 新增
├── 提取层 (prompts/)
└── 输出层 (templates/)
```

---

## 核心脚本

### 1. fetch-card-from-web.py

从网页URL生成深度研究v6.0标准JSON卡片。

**用法**：
```bash
python3 scripts/fetch-card-from-web.py <card_id> <url> [options]

# 示例
python3 scripts/fetch-card-from-web.py card-mckinsey-001 \
  "https://www.mckinsey.com/industries/healthcare/our-insights/..." \
  --domain healthcare --timeout 90 -v
```

**输出**：`sources/card-{id}.json`

### 2. convert-card-to-md.py

将JSON卡片转换为Markdown格式。

**用法**：
```bash
# 通过文件路径
python3 scripts/convert-card-to-md.py sources/card-xxx.json

# 通过卡片ID（自动查找sources/目录）
python3 scripts/convert-card-to-md.py card-xxx --by-id

# 批量转换
python3 scripts/convert-card-to-md.py sources/*.json
```

**输出**：`sources/card-{id}.md`

### 3. batch-fetch.py

批量网页抓取，支持并发、断点续抓。

**用法**：
```bash
# 基础用法
python3 scripts/batch-fetch.py urls.txt --domain healthcare

# 完整参数
python3 scripts/batch-fetch.py urls.txt \
  --domain healthcare \
  --prefix mckinsey \
  --concurrent 3 \
  --timeout 90 \
  --delay-min 2 --delay-max 5
```

**URL文件格式**：
```
# 注释行
https://www.mckinsey.com/article1
https://www.mckinsey.com/article2
```

---

## 使用场景

### 场景1：已知URL的深度研究

适用于已有具体URL，需要提取内容并纳入研究流程。

```bash
cd skills/deep-research

# Step 1: 抓取并生成JSON卡片
python3 scripts/fetch-card-from-web.py \
  card-web-001 \
  "https://www.mckinsey.com/industries/healthcare/..." \
  --domain healthcare

# Step 2: 转换为Markdown卡片（可选）
python3 scripts/convert-card-to-md.py card-web-001 --by-id

# Step 3: 纳入研究流程，生成报告
bash scripts/run-research.sh "AI healthcare cost control"
```

### 场景2：搜索+抓取自动化

适用于先搜索获取URL列表，再批量抓取。

```bash
cd skills/deep-research

# Step 1: 搜索获取URL列表（手动或使用搜索工具）
# 将URL保存到 urls.txt

# Step 2: 批量抓取
python3 scripts/batch-fetch.py urls.txt \
  --domain insurance \
  --prefix mckinsey \
  --concurrent 3

# Step 3: 批量转换为Markdown
python3 scripts/convert-card-to-md.py sources/mckinsey-*.json

# Step 4: 分析生成报告
bash scripts/run-research.sh "healthcare cost control McKinsey"
```

---

## 数据流

```
用户输入
    ↓
┌─────────────────────────────────────────┐
│ 方式A: fetch-card-from-web.py (单URL)   │
│ 方式B: batch-fetch.py (批量URL)         │
└─────────────────────────────────────────┘
    ↓
调用 web-fetcher.py 抓取
    ↓
提取正文 + 元数据 + 指标
    ↓
生成JSON卡片 (sources/card-xxx.json)
    ↓
┌─────────────────────────────────────────┐
│ 可选: convert-card-to-md.py             │
└─────────────────────────────────────────┘
    ↓
生成Markdown卡片 (可选)
    ↓
纳入深度研究v6.0流程
    ↓
生成三层报告
```

---

## 集成优势

| 维度 | 融合前 | 融合后 |
|------|--------|--------|
| **数据来源** | 仅学术数据库 | 学术+网页+报告 |
| **覆盖范围** | PubMed/arXiv | + 政府网/咨询公司/新闻 |
| **数据完整度** | 依赖开放获取 | 可直接抓取全文 |
| **成本** | 免费 | 免费 |

---

## 常见问题

### Q1: 抓取失败怎么办？

1. 增加超时：`--timeout 90`
2. 增加重试：`--retries 5`
3. 查看详细日志：`-v`
4. 检查是否需要Cookie（登录网站）

### Q2: 内容提取不完整？

1. 复杂布局网站可能需要人工复核
2. 检查 `content_preview` 字段了解提取质量
3. 查看 `data_level` 评估（high/medium/low）

### Q3: 批量抓取被拦截？

1. 降低并发：`--concurrent 1`
2. 增加延迟：`--delay-min 3 --delay-max 6`
3. 使用Cookie绕过登录限制
4. 分批处理，使用断点续抓

---

## 文件清单

```
skills/deep-research/
├── scripts/
│   ├── fetch-card-from-web.py   # URL → JSON卡片
│   ├── convert-card-to-md.py    # JSON → Markdown
│   ├── batch-fetch.py           # 批量抓取
│   └── test-integration.sh      # 集成测试
└── INTEGRATION.md               # 本文件

skills/web-fetcher/
├── scripts/
│   ├── web-fetcher.py           # 核心抓取脚本
│   └── cookie_manager.py        # Cookie管理
└── SKILL.md                     # 使用文档
```

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v2.0 | 2026-03-20 | 完整集成方案，新增批量抓取、Markdown转换 |
| v1.0 | 2026-03-19 | 初始融合方案 |

---

*集成版本：v2.0 | 最后更新：2026-03-20*
