# Hugo 托管工作流与命令模板（分阶段）

## 统一进度输出（每一步必填）

```text
[阶段X/步骤Y] 进行中：<当前动作>
[阶段X/步骤Y] 完成：<结果摘要>
[阶段X/步骤Y] 下一步：<下一动作>
```

若进入人工介入节点，使用：

```text
[阶段X/步骤Y] 等待用户：<你现在要做什么>
[阶段X/步骤Y] 系统下一步：<你确认后我会做什么>
```

精简约束：

1. 每一步只保留一个“目标 + 命令 + 输出”。
2. 不重复解释背景信息，背景统一放在 `SKILL.md`。
3. 步骤完成后必须立即输出下一步，不允许省略。

## 阶段 A：Hugo 与 Git 确认/安装

### 1. 环境检测

```bash
command -v hugo >/dev/null 2>&1 || echo "MISSING_HUGO"
command -v git >/dev/null 2>&1 || echo "MISSING_GIT"
```

若缺失，输出安装引导并暂停。

输出模板：

```text
[阶段A/步骤1] 进行中：检测 hugo/git 环境
[阶段A/步骤1] 完成：<通过或缺失项>
[阶段A/步骤1] 下一步：<安装或进入阶段B>
```

### 安装引导（macOS）

```bash
brew install hugo git
```

### 安装引导（Ubuntu/Debian）

```bash
sudo apt-get update
sudo apt-get install -y hugo git
```

### 安装引导（Windows）

- Git: 安装 Git for Windows
- Hugo: `winget install Hugo.Hugo.Extended`

> 安装后必须再次执行“环境检测”确认。

---

## 阶段 B：初始化项目（首次）

### 2. 工作目录解析（人工确认）

优先级：

1. 本轮用户显式输入
2. 状态文件 `activeWorkspace`
3. 引导创建新目录

目录创建模板：

```bash
mkdir -p "<workspacePath>"
```

输出模板：

```text
[阶段B/步骤2] 进行中：解析工作目录
[阶段B/步骤2] 等待用户：请确认目录 <workspacePath> 是否创建/使用
[阶段B/步骤2] 系统下一步：确认后创建目录并进入 Hugo 初始化检测
```

---

### 3. Hugo 初始化与模板控制（首次）

检测是否已是 Hugo 站点（任一存在即视为已初始化）：

```bash
[ -f "<workspacePath>/hugo.toml" ] || [ -f "<workspacePath>/hugo.yaml" ] || [ -f "<workspacePath>/hugo.json" ]
```

若未初始化，进入模板选择。
模板仓库与适用场景优先参考：`references/template-catalog.md`。

### 3.1 内置常用模板（建议优先）

- `ananke`：官方示例主题，适合通用博客
- `PaperMod`：技术博客常用，轻量快速
- `Stack`：内容型博客，信息架构清晰
- `Docsy`：文档门户场景
- `blowfish`：现代风格，适合个人内容站

### 3.2 用户自定义模板

允许用户输入 Git 仓库地址，例如：

`https://github.com/<owner>/<theme-repo>.git`

### 3.3 初始化命令模板

先初始化站点：

```bash
hugo new site "<workspacePath>"
```

再按主题来源安装（示例为 `PaperMod`）：

```bash
git -C "<workspacePath>" init
git -C "<workspacePath>" submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

> 若仓库尚未初始化，可先 `git init` 后再 `submodule add`。

配置主题（以 `hugo.toml` 为例）：

```toml
theme = "PaperMod"
```

模板信息需要写入状态：

- `templateType`: `builtin` 或 `custom`
- `templateName`
- `templateSource`

输出模板：

```text
[阶段B/步骤3] 进行中：检查 Hugo 初始化状态并准备模板选择
[阶段B/步骤3] 等待用户：请选择模板（内置编号或自定义地址）
[阶段B/步骤3] 系统下一步：执行初始化并写入模板状态
```

---

### 4. Git 仓库引导（人工确认）

检查：

```bash
git -C "<workspacePath>" rev-parse --is-inside-work-tree
```

若不是仓库，自动引导：

```bash
git -C "<workspacePath>" init
```

首次提交建议模板：

```bash
git -C "<workspacePath>" add .
git -C "<workspacePath>" commit -m "chore(init): bootstrap hugo workspace"
```

输出模板：

```text
[阶段B/步骤4] 进行中：检测 Git 仓库状态
[阶段B/步骤4] 等待用户：请确认是否执行 git init
[阶段B/步骤4] 系统下一步：初始化仓库并进入预览验收
```

---

### 5. 测试文章预览（初始化验收）

默认命令：

```bash
hugo server --buildDrafts --bind 127.0.0.1 --port 1313
```

端口冲突回退策略：

1. `1313`
2. `1314`
3. `1315`

每次回退都要更新状态中的 `lastPreviewCommand` 与 `lastPreviewUrl`。

输出模板：

```text
[阶段B/步骤5] 进行中：启动预览服务
[阶段B/步骤5] 完成：预览地址 <lastPreviewUrl>
[阶段B/步骤5] 下一步：确认是否执行初始化提交
```

---

### 6. 初始化提交（可选）

预检查：

```bash
git -C "<workspacePath>" status --short
```

提交模板：

```bash
git -C "<workspacePath>" add .
git -C "<workspacePath>" commit -m "<commitMessage>"
git -C "<workspacePath>" rev-parse --short HEAD
```

建议提交信息：

- `docs(hugo): publish new post`
- `docs(hugo): revise article structure`
- `chore(hugo): update site configuration`

输出模板：

```text
[阶段B/步骤6] 进行中：检查并提交初始化改动
[阶段B/步骤6] 等待用户：请确认提交信息
[阶段B/步骤6] 系统下一步：提交后进入 Actions 发布验证
```

---

### 7. GitHub Actions 自动部署验证（GitHub Pages）

若用户需要“快速公网可访问”，启用 GitHub Actions 发布。

发布前提醒：

- 可选配置自定义域名（例如 `blog.example.com`）
- 若用户确认启用，必须先完成域名相关文件修改，再触发推送发布

### 7.1 生成工作流文件

写入 `.github/workflows/hugo-pages.yml`，模板见：

`references/github-actions.md`

同时在工作目录写入发布引导文档：

`<workspacePath>/hugo-github-deploy-guide.md`

### 7.2 推送触发部署

```bash
git -C "<workspacePath>" add .github/workflows/hugo-pages.yml
git -C "<workspacePath>" add hugo-github-deploy-guide.md
git -C "<workspacePath>" commit -m "ci(hugo): add GitHub Pages workflow"
git -C "<workspacePath>" push -u origin "<currentBranch>"
```

### 7.2.1 自定义域名文件修改（按需）

```bash
# 1) 修改 Hugo 配置（示例：hugo.toml）
# baseURL = "https://<customDomain>/"

# 2) 写入 CNAME（纯域名，不带协议）
printf '%s\n' "<customDomain>" > "<workspacePath>/static/CNAME"

# 3) 暂存域名配置文件
git -C "<workspacePath>" add hugo.toml
git -C "<workspacePath>" add static/CNAME
```

### 7.3 引导用户开启 Pages

`Settings -> Pages -> Source: GitHub Actions`

### 7.4 记录部署信息

成功后写入状态：

- `deployProvider`: `github-pages`
- `deployWorkflowFile`: `.github/workflows/hugo-pages.yml`
- `deployGuidePath`: `<workspacePath>/hugo-github-deploy-guide.md`
- `customDomain`（如有）
- `domainConfigFiles`（如有，示例：`hugo.toml`、`static/CNAME`）
- `lastDeployUrl`
- `lastDeployStatus`

输出模板：

```text
[阶段B/步骤7] 进行中：配置并验证 GitHub Actions 发布
[阶段B/步骤7] 等待用户：请确认是否启用自定义域名，并在仓库 Settings -> Pages 确认 Source=GitHub Actions
[阶段B/步骤7] 系统下一步：按确认结果修改域名文件后推送触发部署并回传访问 URL
```

## 阶段 C：日常文章发布流程（后续默认）

只关注发布链路，不做内容创作。

### C1. 检测未发布文章

以 `content/` 为范围检查未提交变更：

```bash
git -C "<workspacePath>" status --short -- "content"
```

若有变更，输出“未发布文章提醒”并要求确认：

```text
检测到未发布文章变更，建议先预览确认后再发布。
是否先执行预览？
```

输出模板：

```text
[阶段C/C1] 进行中：检测未发布文章
[阶段C/C1] 等待用户：检测到 <unpublishedArticleCount> 项未发布，是否先预览
[阶段C/C1] 系统下一步：按你的选择执行预览或直接发布
```

### C2. 预览与确认

```bash
hugo server --buildDrafts --bind 127.0.0.1 --port 1313
```

用户确认后继续发布。

输出模板：

```text
[阶段C/C2] 进行中：启动发布前预览
[阶段C/C2] 完成：预览可访问 <lastPreviewUrl>
[阶段C/C2] 下一步：确认提交并发布
```

### C3. 提交与发布

```bash
git -C "<workspacePath>" add content
git -C "<workspacePath>" add .
git -C "<workspacePath>" commit -m "<commitMessage>"
git -C "<workspacePath>" push origin "<currentBranch>"
```

推送后由 GitHub Actions 自动部署。

输出模板：

```text
[阶段C/C3] 进行中：提交并推送触发发布
[阶段C/C3] 完成：提交 <lastCommitHash>，部署状态 <lastDeployStatus>
[阶段C/C3] 下一步：进入状态写回与收尾输出
```

---

## 阶段 D：状态写回与收尾输出

```text
当前工作目录: <workspacePath>
Git 根目录: <gitRoot>
当前分支: <currentBranch>
模板类型: <templateType>
模板名称: <templateName>
模板来源: <templateSource>
预览地址: <lastPreviewUrl>
未发布文章数: <unpublishedArticleCount>
最近提交: <lastCommitHash or N/A>
部署渠道: <deployProvider or N/A>
部署地址: <lastDeployUrl or N/A>
部署状态: <lastDeployStatus or N/A>
状态文件: ~/.openclaw/state/hugo-publisher-state.json
```

固定收尾：

```text
[完成] 当前发布流程已结束
[完成] 如需继续：下一步可直接执行“阶段C 日常发布流程”
```
