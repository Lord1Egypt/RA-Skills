---
name: flow-hugo-publisher
description: Hugo 文章托管发布技能。用于检测 hugo/git 环境、管理工作目录、引导或初始化 Git 仓库、启动本地预览、执行提交，并通过 GitHub Actions 自动部署到可访问的 GitHub Pages。支持全托管执行与人工介入确认，并记录/读取用户当前工作目录与对应 Git 状态。
---

# Hugo 托管发布技能

面向 Hugo 文章发布场景，提供可重复、可恢复、可人工介入的托管流程。
本技能只关注发布链路，不参与文章具体内容创作。

## 触发场景

当用户表达以下意图时触发：

- 管理或发布 Hugo 文章
- 初始化 Hugo 工作目录
- 在本地预览 Hugo 站点
- 将文章变更提交到 Git
- 询问“当前在哪个目录、对应哪个 Git 仓库”

## 执行总则

1. 默认全托管执行：能自动完成的步骤优先自动完成。
2. 关键节点可人工介入：目录创建、初始化模板选择、`git init`、提交信息确认。
3. 每一步都更新状态文件；失败时保留现场并输出恢复建议。
4. 所有命令执行前，先输出“将要做什么 + 为什么”，执行后反馈结果。
5. 仅处理发布流程，不扩展到文章内容生成。
6. 每一步必须输出统一进度格式：`[阶段/步骤] [状态] [下一步]`。

## 状态文件约定

状态文件默认保存在：

`~/.openclaw/state/hugo-publisher-state.json`

字段定义见 `references/state-schema.md`，状态按“多工作目录项目”管理，最小闭环字段如下：

- `activeWorkspace`
- `projects.<workspacePath>.gitRoot`
- `projects.<workspacePath>.currentBranch`
- `projects.<workspacePath>.lastPreviewCommand`
- `projects.<workspacePath>.lastCommitHash`
- `projects.<workspacePath>.updatedAt`

## 托管工作流（分阶段）

每一步都必须回显进度，例如：

- `[阶段A/步骤1] 进行中：检测 hugo/git 环境`
- `[阶段A/步骤1] 完成：环境通过；下一步进入工作目录确认`
- `[阶段B/步骤2] 等待用户：请确认是否创建目录 <workspacePath>`

### 阶段 A：环境确认与安装（首次或环境变化时）

#### 步骤 1：环境检测

检查命令：

```bash
command -v hugo >/dev/null 2>&1
command -v git >/dev/null 2>&1
```

判定规则：

- 两者都存在：进入阶段 B。
- 任一缺失：输出系统对应安装指引（见 `references/workflow.md`），暂停后等待用户确认继续。

### 阶段 B：初始化项目（首次进入某工作目录时）

#### 步骤 2：工作目录管理（人工可介入）

输入优先级：

1. 用户本轮明确指定目录
2. 状态文件中的 `workspacePath`
3. 引导用户新建目录

若目录不存在，先提示并确认后创建：

```bash
mkdir -p "<workspacePath>"
```

#### 步骤 3：Hugo 模板初始化（仅首次）

若目录下不存在 `hugo.toml` / `hugo.yaml` / `hugo.json`，视为未初始化 Hugo 站点，必须进入模板选择。

内置常用模板：

1. `ananke`（官方示例主题，通用博客）
2. `PaperMod`（技术博客常用，轻量）
3. `Stack`（内容型博客，侧边栏结构）
4. `Docsy`（文档站点，适合知识库）
5. `blowfish`（现代简洁，适合内容创作）

也允许用户输入自定义模板仓库地址（Git URL）。

初始化约定：

- 空站点：`hugo new site "<workspacePath>"`
- 内置/自定义主题：站点初始化后，拉取主题到 `themes/<themeName>`，并在 Hugo 配置中设置 `theme`。

模板来源、模板名称、初始化方式必须写入状态文件。

模板详情与选型建议见 `references/template-catalog.md`。

#### 步骤 4：Git 仓库检测与引导创建（人工可介入）

检测是否为 Git 仓库：

```bash
git -C "<workspacePath>" rev-parse --is-inside-work-tree
```

若不是 Git 仓库，按自动引导策略执行：

```bash
git -C "<workspacePath>" init
```

然后提示并协助用户完成首次提交（可托管执行）。

#### 步骤 5：测试文章预览（初始化验收）

在工作目录启动预览：

```bash
hugo server --buildDrafts --bind 127.0.0.1 --port 1313
```

要求：

- 输出预览地址（默认 `http://127.0.0.1:1313`）。
- 若端口占用，尝试 `1314`、`1315` 递增端口并记录实际命令到状态。
- 提示停止命令（通常 `Ctrl+C`）。

#### 步骤 6：初始化提交（可选）

提交前检查：

```bash
git -C "<workspacePath>" status --short
```

若无改动，明确提示“无可提交内容”并仅更新状态。

若有改动，执行：

```bash
git -C "<workspacePath>" add .
git -C "<workspacePath>" commit -m "<commitMessage>"
```

提交信息需先向用户确认；用户未给出时使用建议模板：

`docs(hugo): update post content and site config`

#### 步骤 7：GitHub Actions 首次发布验证（推荐）

当用户希望“发布并公网可访问”时，执行 GitHub Pages 部署引导：

1. 检查远程仓库（`origin`）是否存在并可 push
2. 创建/更新 `.github/workflows/hugo-pages.yml`
3. 在工作目录生成 `hugo-github-deploy-guide.md`
4. 引导用户在仓库 Settings 中开启 Pages（Source: GitHub Actions）
5. 推送分支触发 Actions 并等待部署完成
6. 输出站点 URL（通常为 `https://<user>.github.io/<repo>/`）
7. 发布前提醒用户可选配置自定义域名，并引导修改域名相关文件

完整模板与操作说明见 `references/github-actions.md`。

约束：`hugo-github-deploy-guide.md` 跟随 Hugo 工作目录存放，不写入 `~/.openclaw`。

### 阶段 C：日常发布快路径（后续默认）

当 `activeWorkspace` 已完成初始化后，默认走快路径：

1. 检测未发布文章（`content/` 下有未提交变更）
2. 若存在未发布文章，提醒用户先确认预览与编辑
3. 运行本地预览
4. 用户确认后执行提交与推送，触发 GitHub Actions 发布
5. 更新该工作目录对应项目状态

### 阶段 D：状态写回与读取确认

流程结束后写回状态，并向用户展示：

- 当前工作目录
- Git 根目录
- 当前分支
- 当前工作目录未发布文章数量（如有）
- 最近一次预览命令
- 最近一次提交哈希（如有）
- 最近一次部署 URL（如有）

最后固定输出：

- `[完成] 发布流程已结束；下一步可直接走“未发布检测 -> 预览 -> 发布”`

## 人工介入点

详细规范见 `references/interaction-points.md`。默认在下列节点进行可中断确认：

1. 新目录创建前
2. 首次 Hugo 初始化时模板选择确认（内置或自定义）
3. 非 Git 目录自动初始化前
4. Git commit 执行前（确认提交信息）
5. 首次写入 GitHub Actions 工作流前（确认是否启用自动部署）
6. 检测到未发布文章时，确认是否先预览再发布

## 失败恢复策略

见 `references/validation-checklist.md`，至少覆盖：

- 未安装 hugo/git
- 目录权限不足
- 非 Git 目录
- 端口占用
- 空提交
- commit 失败
- Actions 构建失败或 Pages 未启用

## 参考文档

- [工作流与命令模板](references/workflow.md)
- [状态文件结构](references/state-schema.md)
- [人工介入规范](references/interaction-points.md)
- [校验与恢复清单](references/validation-checklist.md)
- [模板目录与选型建议](references/template-catalog.md)
- [GitHub Actions 部署指南](references/github-actions.md)
