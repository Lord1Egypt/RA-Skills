---
name: agent-sdd-bootstrap
description: "［何时使用］当用户要为项目初始化 OpenSpec/SDD（Spec-Driven Development）工作流时；当用户说"配置 SDD""初始化 openspec""搭建 spec-driven 开发环境"时；当需要在 atomcode、zcode 等 OpenSpec 非原生支持的 Agent CLI 上接入 SDD 时"
version: 1.0.0
author: nieen
license: MIT
skill_type: 通用🟡
created: 2026-07-25
allowed-tools: [bash, read, write, glob, grep]
tags: [sdd, spec-driven, openspec, opencode, atomcode, codebuddy, bootstrap]
---

# Agent SDD Bootstrap

## 📋 功能描述

帮助用户在任意项目中完成 SDD（规范驱动开发）工作流的初始化：安装并校验 OpenSpec CLI、生成项目级 SDD 配置、自动识别项目技术栈并写入上下文，并针对 OpenSpec 原生支持与非原生支持的 Agent CLI 分别完成接入。

## 适用场景

任何项目的首次 SDD 配置 —— 新项目初始化、为 Agent CLI 配置 OpenSpec、或适配到非原生支持的工具。

## 前置条件

- 目标项目已是 git 仓库
- 至少一个可用的 AI 编码 Agent CLI（opencode、atomcode、codebuddy 等）
- Node.js 与 npm 可用（OpenSpec 通过 npm 全局安装）
- bash 或 PowerShell 环境：正文命令以 bash 为主，PowerShell 全套对应命令见 [references/powershell.md](references/powershell.md)

## 工作流程概览

1. `openspec init` —— 生成项目级 SDD 配置
2. 配置 `openspec/config.yaml` 中的项目上下文
3. OpenSpec 原生支持的工具 —— 开箱即用
4. 非原生工具 —— 以原生工具为桥梁，手动镜像生成的技能文件

## Step 0 — 检查并安装 OpenSpec

```bash
# 检测，未安装则全局安装
openspec --version &>/dev/null || npm install -g @fission-ai/openspec@latest

# 验证，预期输出 x.y.z 形式的版本号
openspec --version
```

### 获取原生支持的工具列表

```bash
openspec init --help
```

查看 `--tools` 参数列出的支持工具。**始终以该命令的实际输出为准**——不要依赖任何写死的工具清单（包括本文档中的示例），OpenSpec 的支持列表会随版本变化。

交叉检查本机可用的 Agent CLI：

```bash
for tool in opencode codebuddy atomcode zcode; do
  if command -v $tool &>/dev/null; then
    echo "$tool: ✅ 可用"
  else
    echo "$tool: ❌ 未安装"
  fi
done
```

## Step 1 — 初始化 OpenSpec

```bash
cd /path/to/project
openspec init --tools opencode
```

生成：
- `openspec/config.yaml` —— 项目上下文与规则
- `.opencode/skills/` —— opsx 技能
- `.opencode/commands/` —— opsx 斜杠命令

## Step 2 — 自动识别项目上下文并配置 config.yaml

`openspec init` 生成的默认 `openspec/config.yaml` 是模板。Agent 应：

1. **分析项目结构** —— 扫描根目录，识别语言生态（Go/Python/TS）、框架（Gin/FastAPI/Next.js）、既有约定（Makefile、Dockerfile、.gitignore 模式）
2. **读取当前 config.yaml** —— 用 `read_file` 获取模板内容，确认占位字段
3. **写入更新后的 config.yaml** —— 用 `write_file` **整体覆写** `openspec/config.yaml`，因为 YAML 结构需要整体替换而非局部 patch

典型 `openspec/config.yaml` 更新后的结构示例：

```yaml
project:
  name: "<项目目录名>"
  description: "<从 README 或 package.json 提取的一句话描述>"

context: |
  项目技术栈：Go 1.22 + Gin + PostgreSQL
  目录结构：/<project-name>/cmd/  <project-name>/internal/  <project-name>/pkg/
  编码约定：错误处理统一返回 (data, error)，不使用 panic
  
rules:
  proposal:
    - 数据库变更需附带迁移脚本
    - API 新增需保持向后兼容
  tasks:
    - 按 service / handler / model 分层提交 PR
    - 每个功能分支需通过测试后再合并
```

4. **设置任务规则** —— 根据项目特有约束（数据库迁移、API 兼容性、多服务协调等）配置 `rules.proposal` 与 `rules.tasks` 字段

## Step 3 — 原生工具：直接使用

OpenSpec 原生支持的工具（如 opencode、codebuddy）：

```bash
opencode run '/opsx:propose "your change idea"'
```

Agent 读取 `openspec/config.yaml` 上下文，生成 spec 并实现。

## Step 4 — 非原生工具：镜像技能文件

适用于 OpenSpec 未原生支持的工具（atomcode、zcode 等）。

### 4a — 询问用户选择桥接工具

调用 `request_user_input` 工具向用户确认桥接工具。从 Step 0 的 `openspec init --help` 输出中选一个原生支持的工具做桥梁，**默认推荐 opencode**。

```python
# request_user_input 参数示意
mode: "single"
question: "OpenSpec 不支持 <target-tool>，将使用 opencode 作为桥梁生成参考文件，是否同意？"
options:
  - label: "opencode（默认）"
  - label: "codebuddy"
custom: false  # 选项已覆盖所有原生工具
```

用户选择后，将选中的工具作为桥接工具继续。若用户拒绝，则结束流程并告知用户 SDD 初始化无法完成。

### 4b — 用选定的桥接工具初始化

```bash
# 默认：opencode
openspec init --tools opencode

# 若用户选择 codebuddy：
# openspec init --tools codebuddy
```

### 4c — 研究生成的文件

`<bridge-tool-dir>/skills/` 与 `<bridge-tool-dir>/commands/` 中：每个 skill 是 SDD 流水线指令（markdown），每个 command 是一个斜杠命令（如 `/opsx:propose`、`/opsx:revise`）。

### 4d — 为目标工具创建对应文件

```bash
mkdir -p .<target-tool>/skills .<target-tool>/commands

# 示例：从 opencode 桥梁适配到 atomcode
# cp .opencode/skills/opsx-*.md .atomcode/skills/
# cp .opencode/commands/opsx-*.md .atomcode/commands/
```

将 `<bridge-tool-dir>`、`<target-tool>` 替换为实际名称。

### 4e — 按目标工具格式适配

| 桥梁（源） | 目标 | 动作 |
|-----------|------|------|
| `.opencode/` | `.codebuddy/` | 原生支持 —— 跳过 |
| `.opencode/` | `.atomcode/` | 镜像 + 适配（示例） |
| `.opencode/` | `.zcode/` | 镜像 + 适配 |
| 任意 | 任意 | 查阅目标工具的 skill 格式文档后适配 |

> 表中工具名仅为示例，实际支持情况以 `openspec init --help` 输出为准。

### 4f — 验证

检查文件生成和 TUI 斜杠命令：

```bash
# 检查目标工具目录已生成
ls .<target-tool>/skills/
ls .<target-tool>/commands/

# 确认 config.yaml 上下文已更新
cat openspec/config.yaml
```

接着在目标工具的 TUI 中测试斜杠命令，例如 atomcode 中提交 `/opsx:propose "test"`。

## Step 5 — 验证

```bash
ls openspec/config.yaml
ls .opencode/skills/
opencode run '/opsx:propose "verify SDD is working"'
```

## ⚠️ 常见错误

- **`openspec init` 会覆盖文件** —— 重跑前先 stage/commit
- **非原生工具必须手动镜像** —— OpenSpec 只为原生工具生成技能文件
- **各工具 skill 格式不同** —— 镜像后需逐一核对目标工具的 skill/command schema
- **工具配置目录应加 .gitignore** —— `.opencode/`、`.codebuddy/`、`.atomcode/`、`.zcode/` 属本地开发配置
- **init 前先提交 git** —— 保证干净状态，便于审查与回滚

## 🔧 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| npm 安装失败 | 网络或权限问题 | 切换 npm 镜像源，或以管理员权限重试 |
| `openspec --version` 找不到命令 | npm 全局 bin 不在 PATH | `export PATH="$PATH:$(npm prefix -g)/bin"` 临时修复；建议 Agent 检测并自动添加，而非依赖用户重置终端 |
| `openspec init` 覆盖了已有改动 | init 会重新生成文件 | 提前 git commit；已被覆盖时用 `git diff` 找回 |
| `--tools` 列表中没有目标工具 | OpenSpec 版本过旧 | `npm update -g @fission-ai/openspec` 后重新查看 |
| 镜像后斜杠命令不生效 | 目标工具 skill/command 格式不同 | 对照目标工具文档调整 frontmatter 与目录结构 |

## 🔗 相关资源

- OpenSpec GitHub：https://github.com/Fission-AI/OpenSpec
- OpenSpec npm：https://www.npmjs.com/package/@fission-ai/openspec
