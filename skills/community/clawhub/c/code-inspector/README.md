# code-inspector

AI 生成代码质量检测工具 —— 基于特征签名的 AI 代码异味检测器。

## 功能

自动检测 AI 生成代码中的 8 种常见质量问题：

| 检测类型 | 严重程度 | 说明 |
|---------|---------|------|
| **截断代码** (truncation) | 🔴 严重 | LLM 输出被截断的标记，如 `// ...`、`# ...`、`# rest of the code` |
| **思维泄露** (thinking_skip) | 🟡 警告 | LLM 的思考过程泄露到注释中，如 `// Let me`、`# First,`、`# Now,` |
| **硬编码密钥** (hardcoded_secret) | 🔴 严重 | API Key、Token、密码等敏感信息硬编码在源码中 |
| **缺少错误处理** (missing_error_handling) | 🟡 警告 | 文件操作、网络请求未使用 try/except 包裹 |
| **TODO 炸弹** (todo_bomb) | 🟡 警告 | 文件中存在超过 3 个 TODO/FIXME/HACK 标记 |
| **重复代码** (copy_paste) | 🟡 警告 | 超过 5 行的相同代码块重复出现 |
| **不完整导入** (incomplete_import) | 🔵 提示 | 使用了未导入的函数或变量（如 `pd`、`np`） |
| **裸 except** (bare_except) | 🟡 警告 | `except:` 未指定异常类型 |

## 快速开始

### 安装

```bash
pip install -e .
```

### 使用

```bash
# 检查单个文件
code-inspector check app.py

# 扫描整个目录
code-inspector scan ./src

# 查看统计信息
code-inspector stats ./project
```

### 输出示例

```
╭───────────────── Code Inspector ─────────────────╮
│ app.py  |  Language: Python                       │
╰───────────────────────────────────────────────────╯
Quality Score: ████████████████░░░░ 80/100

╭──────────────────── Smells Found: 2 ────────────────────╮
│ # │ Line │ Severity  │ Type           │ Description     │
├───┼──────┼───────────┼────────────────┼─────────────────┤
│ 1 │  42  │ 🔴 critical │ hardcoded_secret│ API key hardcoded │
│ 2 │  15  │ 🟡 warning  │ todo_bomb      │ TODO markers >3 │
╰──────────────────────────────────────────────────────────╯
```

## 支持语言

- Python (`.py`)
- JavaScript (`.js`)
- TypeScript (`.ts`)

## 质量评分

每个文件初始评分 100 分，根据检测到的气味扣分：

- 截断代码: -20
- 硬编码密钥: -25
- 思维泄露: -15
- 重复代码: -12
- 缺少错误处理: -10
- 不完整导入: -10
- TODO 炸弹: -8
- 裸 except: -7

## 生态系统

| Tool | Description |
|---|---|
| [prompt-inspector](https://github.com/minirr890112-byte/prompt-inspector) | Scan prompts for censorship triggers |
| [api-cost-compare](https://github.com/minirr890112-byte/api-cost-compare) | Compare LLM API pricing |
| [model-watch](https://github.com/minirr890112-byte/model-watch) | Monitor models for degradation |
| [task-cost-estimator](https://github.com/minirr890112-byte/task-cost-estimator) | Estimate dev task costs |

## 许可证

MIT License
