# PPT Insight Generator

AI 驱动的技术洞察 PPT 生成器。**深红色主题 (#C00000) + 白色背景**，全流程自动化。

---

## 安装

```bash
npm install pptxgenjs
```

---

## 快速开始

### 一键生成（推荐）

```bash
node scripts/run_all.js --topic "Claude Code 技术洞察" --slides 10
```

### 分步执行

```bash
# Step 1: 搜索
node scripts/01_search_and_collect.js --topic "Claude Code" --session-id "abc123"

# Step 2: 洞察提炼
node scripts/02_extract_insights.js --session-id "abc123"

# Step 3: 内容生成
node scripts/03_generate_content.js --session-id "abc123" --slides 10

# Step 4: 优化
node scripts/04_optimize_content.js --session-id "abc123"

# Step 5: PPT 生成
node scripts/05_generate_ppt.js --session-id "abc123" --output "report.pptx"
```

---

## 输出目录

```
D:\techinsight\reports\insight_{session-id}\
├── collected/          # 搜索结果
│   ├── web_pages/     # 抽取的网页内容
│   └── papers/        # 下载的 PDF
├── insights/          # 洞察提炼
├── content/           # 内容 + 目录
│   ├── outline.json
│   └── slides/
└── output/            # 最终 PPT
    └── *.pptx
```

---

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--topic` | 主题 | `"Claude Code"` |
| `--slides` | 目标页数 | `10` |
| `--session-id` | 会话 ID | `"abc123"` |
| `--output` | 输出文件名 | `"report.pptx"` |
| `--from-step` | 从第几步开始 | `3` |
| `--only-step` | 只执行某一步 | `5` |

### 断点续传

```bash
# 从第 3 步开始
node scripts/run_all.js --session-id "abc123" --from-step 3

# 只执行第 5 步
node scripts/run_all.js --session-id "abc123" --only-step 5
```

---

## PPT 页面类型

| 类型 | 说明 |
|------|------|
| cover | 封面页 |
| toc | 目录页 |
| executive_summary | 执行摘要 |
| tech_overview | 技术全景图 |
| tech_point | 技术点展开 |
| comparison | 对比分析 |
| summary | 总结页 |

---

## 配色方案

| 用途 | 色值 |
|------|------|
| 主色（标题） | `#C00000` |
| 辅助色 | `#C41E3A` |
| 强调色 | `#D4AF37` |
| 背景 | `#FFFFFF` |
| 正文 | `#1A1A1A` |

---

## 故障排除

**pptxgenjs 未安装**
```bash
npm install pptxgenjs
```

**中文显示异常**
确保系统安装了「微软雅黑」字体。

**PPT 无法打开**
检查 Node.js 版本（建议 v16+），重新安装 pptxgenjs。

---

*最后更新：2026 年 4 月*
