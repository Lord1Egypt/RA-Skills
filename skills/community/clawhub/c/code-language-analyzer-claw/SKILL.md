---
name: code-language-analyzer
description: "项目编程语言代码量分析专家。扫描项目目录，统计各编程语言的文件数、代码行数及占比，生成可视化的语言分布报告。当用户需要分析项目使用了哪些语言、各语言代码量占比、技术栈构成、代码行数统计时触发此技能。典型场景包括：分析项目语言占比、统计代码行数、看看这个项目用了哪些语言、分析技术栈、code language analysis 等。"
agent_created: true
---

# Code Language Analyzer

## Overview

项目编程语言代码量分析技能。通过扫描项目目录，识别文件类型，
统计各编程语言的文件数量、代码行数（含总行数和有效代码行数），
计算占比，并生成包含 ASCII 柱状图的可读报告。

支持 60+ 种编程语言，覆盖前端、后端、移动端、脚本、配置等常见类型。

## Quick Start

### 1. 确认项目路径

确认待分析的项目目录存在：

```bash
ls <project-path>
```

### 2. 运行分析脚本

使用内置脚本进行分析：

```bash
python <skill-dir>/scripts/analyze_languages.py <project-path>
```

常用选项：

| 选项 | 说明 |
|------|------|
| `--detail` | 显示每个语言下 Top 20 文件的明细 |
| `--json` | 以 JSON 格式输出（适合后续程序处理） |
| `--exclude <dir1,dir2>` | 额外排除的目录（逗号分隔） |
| `--extensions` | 列出所有支持的扩展名 |

### 3. 呈现结果

将脚本输出的分析报告展示给用户。报告包含：
- 总览统计（文件数、总行数、代码行数、语言数）
- 分语言明细表（文件数、行数、占比）
- ASCII 柱状图直观展示分布

## Workflow

### 标准分析流程

1. **确认路径** — 验证用户指定的项目目录是否存在
2. **运行脚本** — 执行 `analyze_languages.py`，传入项目路径
3. **解读结果** — 向用户展示报告，解读主要发现：
   - 主要使用的语言及其占比
   - 技术栈构成（前端 / 后端 / 脚本 / 配置）
   - 项目规模概览
4. **可选深入** — 如用户需要文件级明细，追加 `--detail` 参数重新运行

### JSON 模式

当需要将结果用于后续处理（生成图表、写入报告等）时，使用 `--json`：

```bash
python <skill-dir>/scripts/analyze_languages.py <project-path> --json
```

JSON 结构：

```json
{
  "JavaScript": {
    "files": 120,
    "total_lines": 15000,
    "code_lines": 12000,
    "files_detail": [
      {"path": "src/index.js", "total": 300, "code": 250}
    ]
  }
}
```

## Scripts

### analyze_languages.py

核心分析脚本，位于 `scripts/analyze_languages.py`。

**功能：**
- 递归扫描项目目录
- 按文件扩展名识别编程语言（支持 60+ 种）
- 统计每个语言的文件数、总行数、有效代码行数（非空行）
- 自动跳过 `node_modules`、`.git`、`dist`、`build`、`venv` 等常见忽略目录
- 输出格式化报告，包含占比表格和 ASCII 柱状图

**统计口径：**
- `total_lines`：文件总行数（含空行和注释）
- `code_lines`：非空行数（有效代码行，含注释行）

**默认排除目录：**
`.git`, `node_modules`, `vendor`, `__pycache__`, `.venv`, `venv`,
`dist`, `build`, `out`, `target`, `.next`, `coverage`, `.idea`,
`.vscode`, `Pods`, `.terraform`, `bin`, `obj`, `.cache` 等

**自定义排除：**

```bash
python <skill-dir>/scripts/analyze_languages.py <project-path> --exclude custom_dir,other_dir
```

## Output Format

标准输出示例：

```
======================================================================
  Code Language Analysis Report
======================================================================

  Total files:        248
  Total lines:     45,230
  Code lines:      36,180
  Blank/comment:    9,050
  Languages:            6

----------------------------------------------------------------------
  Language                      Files       Lines       Code        %
----------------------------------------------------------------------
  TypeScript                       85     20,000     16,000    44.21%
  JavaScript                       60     12,000      9,600    26.53%
  CSS                              40      8,000      6,400    17.69%
  HTML                             30      3,000      2,400     6.63%
  JSON                             20      1,500      1,500     3.32%
  Markdown                         13        730        280     1.61%
----------------------------------------------------------------------

======================================================================
  Distribution Chart
======================================================================
  TypeScript           |################ |  44.21%
  JavaScript           |##########       |  26.53%
  CSS                  |######           |  17.69%
  HTML                 |##               |   6.63%
  JSON                 |#                |   3.32%
  Markdown             |                 |   1.61%
======================================================================
```

## Tips

- 对于大型项目，脚本可能需要数秒完成扫描
- 如结果中包含大量配置文件（JSON/YAML），可关注代码语言而非配置语言
- `--json` 输出可用于生成自定义可视化或写入分析报告
- 使用 `--extensions` 可查看所有支持的文件类型
