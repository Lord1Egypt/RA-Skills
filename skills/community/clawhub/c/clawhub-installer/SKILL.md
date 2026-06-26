---
name: clawhub-installer
description: 根据当前任务需求，使用 ClawHub 搜索、筛选并安装最合适的技能；支持指定版本安装与安装后验证。
---

# ClawHub Installer

当用户表达“为了完成某个任务需要找并安装技能”时，使用本技能。

## 适用场景

- 用户说“帮我找个技能来做 X”
- 用户说“安装一个能处理 X 的 skill”
- 当前任务缺少能力，需要动态补齐技能

## 工作目标

1. 基于任务需求生成搜索关键词
2. 用 `clawhub search` 找候选技能
3. 给出精简推荐（默认 Top 3）
4. 在用户确认后执行安装（可指定版本）
5. 安装后提供验证与后续建议

## 执行流程

### 1) 澄清任务需求（最小必要）

如果用户需求模糊，先问 1 个问题即可：

- “你是要处理哪类任务（例如 GitHub、视频处理、天气、RAG 检索）？”

需求明确则直接进入搜索。

### 2) 搜索候选技能

```bash
clawhub search "<task keywords>"
```

关键词策略：

- 优先保留任务动词 + 领域名词（如 `extract video frames`, `github pr review`, `weather forecast`）
- 可并行尝试 1-2 组同义关键词并合并结果

### 3) 推荐与选择

返回候选时给出：

- `slug`
- 简短用途说明（1 行）
- 推荐理由（和当前任务的匹配点）

默认推荐 Top 3，避免信息过载。然后询问：

- “要我安装第几个？是否锁定版本（如 `--version 1.2.3`）？”

### 4) 执行安装

安装最新版本：

```bash
clawhub install <slug>
```

安装指定版本：

```bash
clawhub install <slug> --version <x.y.z>
```

### 5) 安装后验证

```bash
clawhub list
```

验证点：

- 技能已出现在列表
- 名称/版本与预期一致

然后给用户一句可执行建议：

- “已安装完成，现在我可以直接用这个技能来处理你的任务。”

## 失败处理

- 未找到结果：
  - 改写关键词后再搜一次（更短、更通用）
- 版本不存在：
  - 提示可用最新版本，或让用户改版本号
- 安装失败：
  - 返回原始错误摘要，并建议重试或切换候选技能

## 命令速查

```bash
clawhub search "<query>"
clawhub install <slug>
clawhub install <slug> --version <x.y.z>
clawhub list
clawhub update <slug>
clawhub update --all
```

## 使用原则

- 先推荐、后安装（除非用户明确“直接装”）
- 默认装最新稳定版；仅在用户要求时锁版本
- 输出简洁，始终围绕“能否完成当前任务”
