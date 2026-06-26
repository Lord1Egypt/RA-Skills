# PPT Insight Generator 脚本集

## 目录结构

```
scripts/
├── 01_search_and_collect.js   # Step 1: 搜索 + 内容抽取 + 文档下载
├── 02_extract_insights.js     # Step 2: 从收集内容中提炼洞察
├── 03_generate_content.js     # Step 3: 生成目录 + 结构化内容
├── 04_optimize_content.js     # Step 4: 反思优化内容
├── 05_generate_ppt.js         # Step 5: PPT 生成 (Node.js)
├── 05_generate_ppt_v2.py      # PPT 生成 (Python, 优化版)
└── run_all.js                 # 一键执行完整流程
```

## 快速开始

### Python 版本（推荐）

```bash
# 生成 PPT
python scripts/05_generate_ppt_v2.py --session-id "abc123" --output "report.pptx"

# 或直接运行（需要已生成 content/slides/）
python scripts/05_generate_ppt_v2.py
```

### Node.js 版本

```bash
node scripts/run_all.js --topic "Claude Code 技术洞察" --slides 10 --output "report.pptx"
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

### 断点续传

```bash
# 从第 3 步开始
node scripts/run_all.js --session-id "abc123" --from-step 3

# 只执行第 5 步
node scripts/run_all.js --session-id "abc123" --only-step 5
```

## 依赖

### Python 版本
```bash
pip install python-pptx
```

### Node.js 版本
```bash
npm install pptxgenjs
```
