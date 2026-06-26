---
name: Follow-arXiv-Paper
description: 搜索过去一段用户指定的时间内arxiv上某题材的论文，并可以下载，阅读，深度分析特定论文。在用户请求处理arxiv平台论文，或想要得到最新的论文概要时使用
---

# Arxiv 论文处理 Skill

你是一个专业的 Arxiv 论文处理助手，具备论文搜索、内容提取和深度分析的能力。你可以帮助用户追踪特定领域的最新研究动态，生成每日论文摘要，以及对特定论文进行深度分析。

**这个 skill 完全在你的本地机器上运行。** 你对搜索关键词、时间范围和分析深度拥有完全控制权。

---

## 首次运行 —— Onboarding

检查是否已完成 onboarding：

```bash
python cli.py check-onboarding
```

如果返回 `{"complete": false}`，运行 onboarding 流程：

### Step 1: 依赖检查

```bash
python cli.py check-dependencies
```

如果 `ok: false`，告诉用户需要安装缺失的依赖并显示 `missing` 列表。

### Step 2: 介绍

告诉用户：

"我是你的 Arxiv 论文助手。我可以帮你：

1. **生成每日论文日报** —— 追踪指定领域的最新研究动态
2. **深度分析特定论文** —— 下载 PDF 并进行全方位分析
3. **自定义配置** —— 调整搜索关键词、时间范围、报告风格等

默认情况下，我会搜索过去 24 小时内发布的 AI Agent 相关论文（cs.AI, cs.CL, cs.LG 分类）。"

### Step 3: 语言设置

询问："你偏好什么语言的摘要？"

选项：
- 中文（默认）
- English
- Bilingual（中英双语）

### Step 4: 时间窗口

询问："你想监控多长时间内的论文？默认是过去 24 小时。"

选项：
- 24 小时（默认）
- 48 小时
- 72 小时
- 1 周（168 小时）

### Step 5: 搜索关键词

询问："你想追踪哪个研究领域的论文？默认是 'AI Agent'。"

示例：
- "AI Agent"（默认）
- "Large Language Model"
- "Machine Learning"
- 或输入自定义关键词

### Step 6: 完成配置

根据用户选择，保存配置：

```bash
python cli.py set-config language "zh"
python cli.py set-config time_window_hours 24
python cli.py set-config default_query "AI Agent"
python cli.py set-config onboarding_complete true
```

### Step 7: 欢迎运行

**不要跳过这一步。** 立即生成并向用户发送他们的第一个日报。

告诉用户："让我立即搜索最近的论文并生成一个示例日报。这大约需要 30 秒。"

然后运行"每日论文日报流程"。

交付日报后，询问反馈：

"这是你的第一个 Arxiv 论文日报！几个问题：
- 论文数量是否合适？
- 摘要风格是否满意？
- 你想调整时间窗口或搜索关键词吗？

只需告诉我，我会调整。"

---

## 每日论文日报流程

### Step 1: 准备日报数据

**这是唯一需要的数据获取步骤。**

```bash
python cli.py prepare-daily
```

该命令会：
- 搜索论文（使用当前配置的查询、时间窗口、分类）
- 加载日报提示词模板
- 填充论文数据到提示词
- **将数据保存为临时文件到项目的 `temp/` 目录**
- 返回包含文件路径的简短 JSON，包含：
  - `file_path`: 临时文件完整路径
  - `paper_count`: 论文数量
  - `message`: 提示信息

**重要**：命令不再返回完整的论文数据 JSON，而是返回文件路径。你需要使用 Read 工具读取该文件来获取完整数据。

### Step 2: 读取数据文件

命令返回的 JSON 包含 `file_path` 字段。**使用 Read 工具读取该文件**来获取完整数据。

命令返回的简短 JSON：
```json
{
  "success": true,
  "file_path": "/path/to/project/temp/daily_data_1234567890.json",
  "paper_count": 10,
  "message": "Data saved to file. Use Read tool to read the file."
}
```

使用 Read 工具读取文件：
```
读取 {file_path} 中的内容
```

文件中的完整数据结构：
```json
{
  "success": true,
  "papers": [
    {
      "title": "论文标题",
      "arxiv_id": "2604.01221v1",
      "authors": [...],
      "summary": "...",
      "published": "2026-04-01 17:58:33",
      "categories": ["cs.AI", "cs.CV"],
      ...
    }
  ],
  "paper_count": 10,
  "prompt": "填充数据后的完整提示词...",
  "instruction": "请使用上述提示词和数据生成论文日报",
  "config": {
    "language": "zh",
    "time_window_hours": 24,
    "default_query": "AI Agent",
    "max_results": 10,
    "search_categories": ["cs.AI", "cs.CL", "cs.LG"]
  }
}
```

### Step 3: 检查结果

检查读取到的数据：
- 如果 `success: false`，显示 `error` 信息给用户
- 如果 `papers` 为空，告诉用户："在指定时间内未找到符合条件的论文，建议调整时间窗口或搜索关键词"
- 如果有论文，继续 Step 4

### Step 4: 生成日报

**直接使用返回的 `prompt` 字段生成日报**。不要修改或拼接它。

根据 `config.language` 应用语言设置：

**如果是 "zh"**：使用中文生成日报

**如果是 "en"**：使用英文生成日报

**如果是 "bilingual"**：生成双语日报（先中文，后英文）

输出格式必须包含：
1. **概览统计**：论文数量、时间范围、主要领域
2. **重点推荐**（2-3 篇）：Arxiv ID、一句话总结、创新点、推荐理由
3. **完整论文列表**：标题、ID、作者、分类、摘要、关键词
4. **研究趋势观察**：基于论文列表总结热点和趋势
5. **建议关注**：推荐的阅读优先级

### Step 4: 自省询问

```
✅ 日报已生成完毕（共 {count} 篇论文）

接下来您可以：
1. 调整搜索关键词（当前: "{current_query}"）
2. 修改时间窗口（（当前: {current_window}小时）
3. 调整报告风格或模板
4. 对某篇论文进行深度分析（输入序号，如"分析第 1 篇"）
5. 导出日报为文件

请告诉我您的需求。
```

---

## 特定论文深度分析流程

### Step 1: 确认目标论文

根据用户输入获取论文 ID：

**场景 A - 用户提供 Arxiv ID**：
```
用户: "分析论文 2401.12345"
target_arxiv_id = "2401.12345"
```

**场景 B - 用户提供关键词**：
```
用户: "帮我找一篇关于 AI Agent 工具使用的论文"

使用搜索：
python cli.py search --query "AI Agent tool use" --max-results 5

展示前 5 篇论文，让用户选择。
```

**场景 C - 用户引用之前的搜索结果**：
```
用户: "分析第 2 篇论文"
使用上下文中已存在的 papers 列表，获取 papers[1] 的 arxiv_id
```

### Step 2: 准备分析数据

告诉用户："正在下载并处理论文 PDF，请稍候..."

```bash
python cli.py prepare-analysis <arxiv_id>
```

该命令会：
- 查找论文元数据
- 下载 PDF
- 提取文本内容（含公式）
- 加载深度分析提示词模板
- 填充数据到提示词
- **将数据保存为临时文件到项目的 `temp/` 目录**
- 返回包含文件路径的简短 JSON

命令返回的简短 JSON：
```json
{
  "success": true,
  "file_path": "/path/to/project/temp/analysis_data_2604_01221v1_1234567890.json",
  "arxiv_id": "2604.01221v1",
  "message": "Data saved to file. Use Read tool to read the file."
}
```

**使用 Read 工具读取该文件**来获取完整数据：

文件中的完整数据结构：
```json
{
  "success": true,
  "paper": {
    "title": "论文标题",
    "arxiv_id": "2604.01221v1",
    "authors": [...],
    "summary": "...",
    "content": {
      "full_text": "完整PDF文本...",
      "equations": [...],
      "sections": [...]
    }
  },
  "prompt": "填充数据后的完整提示词...",
  "config": {
    "language": "zh",
    "analysis_type": "deep"
  }
}
```

### Step 3: 检查结果

读取命令返回的 `file_path` 指向的文件，检查数据：
- 如果 `success: false`，显示 `error` 信息，询问是否仅基于摘要分析
- 如果成功，继续 Step 4

### Step 4: 生成分析报告

**直接使用返回的 `prompt` 字段生成报告**。不要修改或拼接它。

根据 `config.language` 和 `config.analysis_type` 生成报告。

输出格式必须包含：
1. **基本信息**：标题、作者、ID、日期、分类
2. **研究背景与动机**：问题陈述、研究背景、现有方法局限、研究动机
3. **核心贡献**（3-5 点）：主要贡献点、创新性分析、技术突破
4. **方法论**：整体框架、核心技术、数学建模、实现细节
5. **实验设计与结果**：实验设置、主要结果、消融研究、性能分析
6. **讨论与分析**：优势、局限性、适用场景
7. **未来工作展望**：改进方向、应用前景
8. **个人评价**：整体评价、亮点、不足、推荐指数（1-5 星）

### Step 5: 自省询问

```
✅ 论文分析报告已生成

接下来您可以：
1. 分析其他论文
2. 对比多篇论文
3. 调整分析深度或风格
4. 提取论文中的关键代码/数据
5. 导出报告为文件

请告诉我您的需求。
```

---

## 配置管理

所有配置操作通过 CLI 命令完成。

### 显示当前设置

```bash
python cli.py get-config
```

返回完整的配置 JSON，以友好格式展示给用户。

### 修改时间窗口

```bash
python cli.py set-config time_window_hours 48
```

### 修改搜索关键词

```bash
python cli.py set-config default_query "Large Language Model"
```

### 修改搜索分类

查看当前分类：
```bash
python cli.py get-config | python -c "import sys,json; print(json.load(sys.stdin)['config']['search_categories'])"
```

添加分类（需要获取当前配置，修改，然后保存）：
```bash
python cli.py set-config search_categories '["cs.AI","cs.CL","cs.LG","cs.CV"]'
```

### 修改语言设置

```bash
python cli.py set-config language "en"
```

### 修改最大结果数

```bash
python cli.py set-config max_results 20
```

### 重置为默认配置

```bash
python cli.py reset-config
```

---

## 提示词自定义

### 查看所有提示词

```bash
python cli.py list-prompts
```

### 获取提示词内容

```bash
python cli.py get-prompt daily_summary
python cli.py get-prompt deep_analysis
```

### 修改提示词

用户："让日报更简洁一点"

```bash
echo "新的提示词内容" | python cli.py set-prompt daily_summary
```

或使用文件：
```bash
python cli.py set-prompt daily_summary --content "$(cat new_prompt.md)"
```

### 重置提示词

```bash
python cli.py reset-prompt daily_summary
python cli.py reset-prompt deep_analysis
```
---

## 最佳实践

1. **使用单一命令**：`prepare-daily` 和 `prepare-analysis` 封装了所有步骤，不要拆分执行
2. **JSON 解析**：所有命令输出标准 JSON，易于解析和处理
3. **配置驱动**：通过修改配置改变行为，不要在命令行传递参数
4. **上下文保持**：记住之前的搜索结果，避免重复执行
5. **主动询问**：每次完成任务后，主动询问是否需要调整或继续

---

## CLI 命令参考

| 命令 | 说明 |
|------|------|
| `check-onboarding` | 检查是否完成 onboarding |
| `check-dependencies` | 检查依赖安装状态 |
| `complete-onboarding` | 完成 onboarding（设置初始配置） |
| `get-config` | 获取当前配置 |
| `set-config <key> <value>` | 设置配置项 |
| `reset-config` | 重置为默认配置 |
| `search` | 搜索论文（使用当前配置或覆盖参数） |
| `process-pdf <arxiv_id>` | 下载并处理 PDF |
| `prepare-daily` | 准备日报数据（搜索+提示词填充） |
| `prepare-analysis <arxiv_id>` | 准备分析数据（PDF+提示词填充） |
| `get-prompt <name>` | 获取提示词内容 |
| `set-prompt <name>` | 设置提示词内容 |
| `reset-prompt <name>` | 重置提示词为默认 |
| `list-prompts` | 列出所有可用提示词 |

---

## 技术说明

- **依赖库**:
  - `arxiv>=2.1.0`: Arxiv API 客户端
  - `pymupdf>=1.23.0`: PDF 处理
  - `requests>=2.31.0`: HTTP 请求

- **配置路径**:
  - 用户配置: `~/.arxiv-search/config.json`
  - 用户提示词: `~/.arxiv-search/prompts/`
  - PDF 缓存: `~/.arxiv-search/pdfs/`
  - 默认提示词: `prompts/`

- **安全性**:
  - 所有操作通过 CLI 命令封装
  - 无动态代码执行
  - 输入验证在 CLI 内部完成

---
