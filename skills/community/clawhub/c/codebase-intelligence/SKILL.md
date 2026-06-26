---
name: codebase-intelligence
description: Intelligent codebase analysis and understanding with caching. Automatically explores project structure, identifies modules, analyzes dependencies, and answers questions about the codebase. Use when onboarding to a new project, before refactoring, or when you need to understand code relationships.
---

# Codebase Intelligence

智能代码库分析工具，自动理解项目结构、模块边界和依赖关系。

**Version**: 1.0  
**Features**: 增量索引缓存、符号搜索、智能问答、架构图生成

---

## Quick Start

### 1. 首次索引（自动缓存）

```bash
cd /path/to/project
python3 /path/to/codebase-intelligence/scripts/main.py analyze .
```

第一次会创建 `.codebase-intelligence/` 目录并缓存索引。后续查询秒开！

### 2. 智能问答

```bash
# 查找代码位置
python3 main.py ask "Where is authentication implemented?"

# 了解工作流程
python3 main.py ask "How does the user login flow work?"

# 查找如何修改
python3 main.py ask "What files need to change to add OAuth?"
```

### 3. 符号搜索

```bash
# 查找类定义
python3 main.py analyze --symbol "UserManager" --symbol-type class

# 查找函数
python3 main.py analyze --symbol "authenticate" --symbol-type func
```

### 4. 依赖分析

```bash
# 查看文件依赖什么
python3 main.py deps src/auth.py

# 查看什么依赖这个文件
python3 main.py deps src/utils.py --reverse
```

### 5. 生成架构图

```bash
# Mermaid 图
python3 main.py diagram --format mermaid

# 流程图
python3 main.py diagram --format mermaid-flow --entry-points main.py app.py
```

---

## Commands

| 命令 | 功能 | 示例 |
|------|------|------|
| `analyze` | 分析代码库（带缓存） | `main.py analyze . --stats` |
| `analyze --search` | 搜索文件 | `main.py analyze --search "auth"` |
| `analyze --symbol` | 查找符号 | `main.py analyze --symbol "User"` |
| `ask` | 智能问答 | `main.py ask "How does X work?"` |
| `deps` | 依赖分析 | `main.py deps src/main.py --reverse` |
| `diagram` | 生成图表 | `main.py diagram --format mermaid` |
| `index` | 更新索引 | `main.py index --export index.json` |

---

## Features

### ✅ 增量缓存

- 首次分析后自动缓存
- 后续只更新修改过的文件
- 大型项目也能秒开

```bash
# 第一次：建立索引（可能需要几秒）
python3 main.py analyze .

# 第二次：秒开！
python3 main.py analyze .  # 瞬间完成
```

### ✅ 符号索引

自动索引：
- 函数定义
- 类/接口定义
- 导入语句
- 文件元数据（语言、行数）

### ✅ 智能问答

支持问题类型：
- **Location**: "Where is X?" → 定位代码
- **How it works**: "How does X work?" → 理解流程
- **Definition**: "What is X?" → 查找定义
- **Dependencies**: "What depends on X?" → 依赖分析
- **Modification**: "How to add X?" → 修改建议

### ✅ 多语言支持

| 语言 | 符号解析 | 依赖提取 |
|------|----------|----------|
| Python | ✅ | ✅ |
| JavaScript/TypeScript | ✅ | ✅ |
| Go | ✅ | ✅ |
| Java | ✅ | ✅ |
| Rust | ✅ | ⚠️ |
| Ruby | ⚠️ | ⚠️ |
| PHP | ⚠️ | ⚠️ |

---

## Examples

### 场景 1：接手新项目

```bash
# 1. 获取整体概览
python3 main.py analyze /path/to/project --stats

# 2. 了解主要模块
python3 main.py analyze --search "module"

# 3. 查找核心类
python3 main.py analyze --symbol "App" --symbol-type class

# 4. 了解工作流程
python3 main.py ask "How does data flow through the system?"

# 5. 生成架构图
python3 main.py diagram --format mermaid-component
```

### 场景 2：重构前分析

```bash
# 1. 检查谁依赖要重构的模块
python3 main.py deps src/old-module.py --reverse --depth 3

# 2. 了解影响范围
python3 main.py ask "What would break if I refactor the auth module?"

# 3. 查看修改建议
python3 main.py ask "How to migrate from class X to class Y?"
```

### 场景 3：代码审查

```bash
# 查看变更影响
python3 main.py ask "What depends on src/utils/helpers.py?"
```

---

## Configuration

### 忽略文件

在 `.codebase-intelligence.json` 中配置：

```json
{
  "ignore": [
    "node_modules",
    ".git",
    "*.test.js",
    "vendor/"
  ],
  "entryPoints": [
    "src/main.py",
    "src/index.js"
  ]
}
```

### 缓存位置

默认缓存位置：`<project>/.codebase-intelligence/codebase_index.pkl`

也可以指定：

```bash
python3 main.py analyze . --cache-dir /path/to/cache
```

---

## Output Formats

### Markdown Report

```bash
python3 main.py analyze --stats
```

包含：
- 项目概览
- 语言分布表
- 模块结构树
- 符号统计

### JSON Export

```bash
python3 main.py index --export index.json
```

结构化数据，包含完整索引信息。

### Mermaid Diagrams

```bash
python3 main.py diagram --format mermaid
```

可直接在 Markdown/GitHub/GitLab 中渲染。

---

## Performance

| 项目规模 | 首次索引 | 增量更新 |
|----------|----------|----------|
| 小 (<100文件) | <1s | <0.1s |
| 中 (100-1000文件) | 2-5s | <0.5s |
| 大 (1000-5000文件) | 10-30s | <2s |

---

## Files

```
skills/codebase-intelligence/
├── SKILL.md                    # 本文件
└── scripts/
    ├── main.py                 # ⭐ 统一入口
    ├── indexer.py              # 索引引擎（带缓存）
    ├── ask_v2.py               # 智能问答
    ├── analyze.py              # 基础分析
    ├── deps.py                 # 依赖分析
    └── diagram.py              # 图表生成
```

---

## Integration

### Git Hooks

```bash
# .git/hooks/pre-commit
python3 scripts/main.py index
```

### CI/CD

```yaml
# .github/workflows/analysis.yml
- name: Analyze Codebase
  run: |
    python3 scripts/main.py analyze --stats
    python3 scripts/main.py diagram --format mermaid > architecture.md
```

---

## Next Steps / Roadmap

- [x] 增量缓存
- [x] 符号索引
- [x] 智能问答
- [ ] AST 解析（提高准确性）
- [ ] 接入 LLM（语义理解）
- [ ] 实时 watch 模式
- [ ] Web UI

---

## Production Ready? ✅

当前状态：**可用，适合日常使用**

- 缓存机制 ✅
- 增量更新 ✅
- 符号索引 ✅
- 智能问答 ✅
- 性能优化 ✅

待完善：
- AST 解析（当前使用正则，有 5-10% 误差）
- LLM 集成（当前基于关键词匹配）
