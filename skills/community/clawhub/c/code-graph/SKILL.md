---
name: code-graph
description: 一键安装 GitNexus 并为当前项目构建代码知识图谱。当用户说「安装GitNexus」「设置GitNexus」「初始化GitNexus」「配置GitNexus」「用GitNexus建图」「GitNexus一键配置」时使用。
---

# 代码图谱（GitNexus）

为当前项目一键完成 GitNexus 安装、MCP 配置和知识图谱构建。**每一步都有跳过检测，已完成的步骤不会重复执行。**

## 语言支持

TypeScript、JavaScript、Python、Java、C、C++、C#、Go、Rust、PHP、Swift、Dart、Kotlin、Ruby 等 14 种语言。

---

## 执行流程

**按顺序执行以下步骤。每步先检测当前状态，已完成则跳过。**

### 第 1 步：定位项目根目录

`gitnexus analyze` 需在项目根目录下执行。首先检查当前工作目录是否即为项目根目录：

```bash
git rev-parse --show-toplevel 2>&1 && echo "已定位到项目根目录"
```

如果 Git 未初始化，则通过常见项目标志文件判断：

```bash
ls package.json 2>&1 || ls pom.xml 2>&1 || ls go.mod 2>&1 || ls Cargo.toml 2>&1 || ls requirements.txt 2>&1 || echo "未找到项目根目录标志文件"
```

- 当前目录即为根目录 → 继续下一步
- 检测到其他目录为根目录 → `cd` 到该目录
- 找不到任何项目标志 → 询问用户项目根目录在哪，或使用 `git init` 初始化

### 第 2 步：检查 Node.js 环境

```bash
node --version
```

**要求 Node.js >= 22。** 如果版本过低或未安装：

- 引导用户到 [nodejs.org](https://nodejs.org/) 下载 LTS 版本
- Windows 用户也可用 `winget install OpenJS.NodeJS.LTS` 安装
- 升级完成后重新执行本技能

### 第 3 步：安装 GitNexus

**先检测，再决定是否安装：**

```bash
gitnexus --version 2>&1
```

**判断逻辑：**
- 输出类似 `1.x.x` 的版本号 → **已安装，跳过本步骤**，直接进入第 4 步
- 输出 `command not found` 或 `not recognized` → 未安装，执行以下安装

**安装命令（Windows，推荐全局安装）：**

```bash
set GITNEXUS_SKIP_OPTIONAL_GRAMMARS=1 && npm install -g gitnexus
```

**安装命令（macOS / Linux）：**

```bash
GITNEXUS_SKIP_OPTIONAL_GRAMMARS=1 npm install -g gitnexus
```

> `GITNEXUS_SKIP_OPTIONAL_GRAMMARS=1` 跳过 Dart/Proto 原生语法解析器的编译，安装只需几秒，无需 C++ 工具链。

**权限不足时的回退方案** — 如果全局安装失败（EACCES / Permission denied），后续命令统一改用 `npx` 前缀：

```bash
npx gitnexus analyze    # 代替 gitnexus analyze
npx gitnexus setup      # 代替 gitnexus setup
npx gitnexus status     # 代替 gitnexus status
```

### 第 4 步：配置 MCP 服务

`gitnexus setup` 自动检测已安装的编辑器并写入 MCP 配置，全局只需执行一次。

**先检测是否已配置：**

```bash
gitnexus setup 2>&1
```

**判断逻辑：**
- 输出包含 `already configured`、`up to date`、`MCP configuration exists` 等字样 → **已配置，跳过**
- 输出包含 `wrote`、`created`、`configured`、`Updated` 等字样 → 配置成功
- 若 `gitnexus` 命令不可用（未全局安装），使用 `npx gitnexus setup`

> `setup` 是幂等的，重复执行不会产生重复配置，可安全地直接运行。

### 第 5 步：构建知识图谱

**先检测当前项目是否已索引：**

```bash
gitnexus status 2>&1
```

**判断逻辑：**
- 输出包含 `Indexed`、`symbols`、`up to date`、`fresh` 等字样 → **已索引且是最新的，跳过本步骤**
- 输出包含 `Not indexed`、`No index found`、`unknown` 等字样 → 未索引，执行以下命令
- 如果 `gitnexus` 不可用，改用 `npx gitnexus status`

**执行索引：**

```bash
gitnexus analyze
```

此命令解析整个代码库、解析导入关系、追踪调用链、检测代码社区，在项目根目录生成 `.gitnexus/` 索引（自动加入 `.gitignore`）。优先使用gitnexus analyze进行索引，若出现错误则尝试增加选项。

**如果需要强制重建（已索引但过期）：**

```bash
gitnexus analyze --force
```

**常用选项：**

| 选项 | 用途 |
|------|------|
| `--embeddings` | 启用语义/向量搜索，速度较慢但搜索更强 |
| `--force` | 强制重建索引（索引过期时使用） |
| `--skip-embeddings` | 跳过嵌入生成，大幅加速（默认行为） |
| `--skip-git` | 允许对非 git 目录构建索引 |
| `--skip-agents-md` | 保留自定义的 CLAUDE.md / AGENTS.md |
| `--verbose` | 输出详细日志，包括被跳过的文件 |
| `--worker-timeout 60` | 大型仓库增加 Worker 超时时间 |

预期输出：

```
Scanning files... ✓ (1,247 files)
Parsing code... ✓ (TypeScript, Python, etc.)
Resolving imports... ✓ (3,892 relationships)
Tracing calls... ✓ (104 processes)
Creating indexes... ✓
Done! Indexed 30,816 symbols in 12s
```

### 第 6 步：验证

```bash
gitnexus status
gitnexus list
```

`status` 确认当前项目的索引状态，`list` 展示全局所有已索引的仓库。

---

## 索引后可用的 MCP 工具

| 工具 | 用途 |
|------|------|
| `list_repos` | 查看所有已索引的仓库 |
| `query` | 混合搜索（关键词 + 语义），按执行流程分组 |
| `context` | 360° 符号视图（调用者、被调用、所属流程） |
| `impact` | 爆炸半径分析 — 修改某个符号会影响哪些地方 |
| `detect_changes` | Git diff 影响映射 |
| `cypher` | 原始图谱查询语言 |
| `rename` | 多文件协调重命名 |

**MCP 资源：**

| 资源 | 用途 |
|------|------|
| `gitnexus://repo/{name}/context` | 代码库概览 + 索引新鲜度检查 |
| `gitnexus://repo/{name}/clusters` | 所有功能聚类 |
| `gitnexus://repo/{name}/processes` | 所有执行流程 |
| `gitnexus://repo/{name}/schema` | 图谱 Schema（Cypher 查询用） |

---

## 常见问题排查

### "Not inside a git repository"（不在 git 仓库中）

```bash
git init && git add . && git commit -m "initial"
gitnexus analyze
```

或使用 `--skip-git` 跳过 git 检查：

```bash
gitnexus analyze --skip-git
```

### "Permission denied"（npm install -g 权限不足）

改用 npx 免安装运行：

```bash
npx gitnexus analyze
```

### "Already indexed"（已索引）

索引已存在且是最新的，无需操作。如需强制重建：

```bash
gitnexus analyze --force
```

### "Node version too old"（Node 版本过旧）

需要 Node.js >= 22，升级后重试：
- Windows: `winget install OpenJS.NodeJS.LTS`
- macOS: `brew install node`
- Linux: 使用 [nvm](https://github.com/nvm-sh/nvm)

### MCP 工具未出现在 Claude Code / Cursor 中

1. 重新执行 `gitnexus setup`
2. 重启编辑器
3. 确认 gitnexus 在 PATH 中：Windows 用 `where gitnexus`，Unix 用 `which gitnexus`

### 索引过期（代码变更后）

```bash
gitnexus analyze    # 增量更新，保留已有嵌入
gitnexus analyze --force  # 完全重建
```

---

## 对话示例

**用户**："安装GitNexus"

执行：
1. 定位项目根目录
2. `node --version` → 确认 >= 22
3. `gitnexus --version` → 未安装 → `npm install -g gitnexus`
4. `gitnexus setup` → MCP 已配置则跳过
5. `gitnexus status` → 未索引 → `gitnexus analyze`
6. `gitnexus status` → 验证成功
7. 回复用户："已索引 N 个符号，生成知识图谱。可通过 context / impact / query 等 MCP 工具查询代码库。"