---
name: docker-image-sync
label: Docker官网镜像拉取能力
description: |
  Sync Docker Hub images to CNB.tool registry via GitHub Actions, solving domestic Docker pull failures for OpenClaw.

  Use when:
  - User needs to pull Docker images but direct access to hub.docker.com is blocked
  - OpenClaw fails to pull Docker images automatically
  - Setting up a Docker mirror using CNB + GitHub Actions proxy

  ───────────────────────────────

  使用 Github Action 同步 Docker 镜像至 cnb.tool 制品库，解决国内拉取镜像失败问题，从而解决 openclaw 自动拉取镜像失败的问题。

  适用场景：
  - 无法直连 hub.docker.com，需要通过 CNB 代理拉取镜像
  - OpenClaw 自动拉取 Docker 镜像失败
  - 通过 GitHub Actions + CNB 构建 Docker 镜像中转服务
---

# Docker官网镜像拉取能力

**使用 Github Action 同步Docker 镜像至cnb.tool 制品库，解决国内拉取镜像失败问题，从而解决 openclaw 自动拉取镜像失败的问题。**

**技能介绍:https://github.com/lufei4/docker-image-sync**

## 前置条件（必选）

- **GitHub CLI（`gh`）**：登录检测、Fork 仓库、设置 Secrets、监控 Actions 状态
  - 安装：`brew install gh`（macOS）或 [github.com/cli](https://cli.github.com)
  - 需登录：`gh auth login`
- **Docker CLI（`docker`）**：登录 CNB 制品库、推送和拉取镜像
  - 安装：`brew install docker` 或从 [docker.com](https://docs.docker.com/desktop/install/linux-install/)

## 工作原理

当无法直连 `hub.docker.com` 时，通过 GitHub Actions 代理中转：

1. 修改 GitHub 仓库 `images.txt`，**清空已有记录，只写入目标镜像**
2. 推送触发 GitHub Actions 同步到 CNB
3. 等待 Actions 完成
4. 从 CNB 拉取镜像到本地

## 🚀 安装流程

技能安装后，请按以下步骤操作：

### 第一步：GitHub 登录检测 & 创建私有仓库

运行以下命令检测 GitHub 登录状态：

```bash
bash ~/.openclaw/workspace/skills/cnb-image-sync/cnb-pull.sh --check
```

- **已登录** → 自动创建私有仓库 `cnb-docker-sync`（**默认私有，不会暴露镜像名**）
- **未登录** → 运行 `gh auth login` 在终端登录，或提供 GitHub Personal Access Token 给 openclaw

> Token 获取路径：GitHub → Settings → Developer settings → Personal access tokens → Generate new token
>
> **推荐方式（不过用户手）：**
> 运行 `gh auth login`，走设备码流程登录，token 自动由 `gh` 管理，无需用户复制粘贴
>
> **如果必须提供 Token（细粒度最小权限）：**
> 创建 Fine-grained Personal Access Token，限制到**仅 `cnb-docker-sync` 仓库**，权限：
> - `Contents: read and write`（读写仓库，触发 workflow）
> - `Secrets: read and write`（设置 Repository Secrets）
> - `Workflows: read and write`（触发 Actions）
> **不要**给 `repo` 全部范围，只给这一个仓库

### 第二步：注册 CNB 账号并创建制品仓库

#### 2.1 注册 CNB 账号

访问 [cnb.cool](https://cnb.cool/)，使用微信账号登录（支持扫码登录）。

![CNB 登录页面](https://github.com/lufei4/docker-image-sync/raw/main/img.png)

#### 2.2 创建仓库

登录后，按以下路径操作：

1. 点击页面**右上角头像**
2. 选择**我的仓库**
3. 点击**创建仓库**按钮，填写仓库名称（可使用中文），类型选择 **Docker**

![进入我的仓库](https://github.com/lufei4/docker-image-sync/raw/main/img_1.png)

创建完成后，进入仓库列表：

![仓库列表](https://github.com/lufei4/docker-image-sync/raw/main/img_2.png)

#### 2.3 获取 CNB 参数（关键步骤）

仓库创建完成后，进入仓库管理页，选择刚创建的仓库 → **制品** → **使用指引**（或**操作指引**）。

点击**使用指引**，找到**了解更多**，这里包含本技能所需的 CNB 参数：

![使用指引-了解更多](https://github.com/lufei4/docker-image-sync/raw/main/img_3.png)

同时在仓库页面点击**操作指引**，可以看到推送和拉取命令，其中有两个关键信息需要记录：

![操作指引](https://github.com/lufei4/docker-image-sync/raw/main/img_4.png)

| 参数 | 对应信息 | 说明 |
|------|----------|------|
| `CNB_REGISTRY` | 仓库地址 | 固定值，如 `docker.cnb.cool` |
| `CNB_REPO_SLUG` | 命名空间 | 格式 `用户名/仓库名`，需转为小写，如 `lufei123/lufei-docker` |

#### 2.4 获取 CNB_TOKEN

在制品库页面，找到**访问令牌**或 **Access Token** 配置，创建一个访问令牌（用于拉取凭证）。

### 第三步：提供参数给 openclaw

准备好以下 4 个参数后，**直接回复我这些值**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `CNB_TOKEN` | CNB 访问令牌 | `8B76Bopie1d966fVDMgJnhFRepZ` |
| `CNB_REGISTRY` | CNB 仓库地址（固定值） | `docker.cnb.cool` |
| `CNB_REPO_SLUG` | CNB 命名空间（小写） | `lufei123/lufei-docker` |
| `CNB_GITHUB_REPO` | 私有仓库地址（格式：`你的GitHub用户名/cnb-docker-sync`） | `你的GitHub用户名/cnb-docker-sync` |

**openclaw 收到后会帮你完成以下操作：**

1. 写入 `~/.openclaw/.env`（注意：请保持该文件可信，`chmod 600 ~/.openclaw/.env`）
2. 自动创建私有仓库 `你的用户名/cnb-docker-sync`（如不存在）
3. 将 **内嵌的 GitHub Actions workflow** 推送到你的私有仓库（workflow 代码来自技能制品，透明可查）
4. 将 `CNB_REGISTRY`、`CNB_REPO_SLUG_LOWERCASE`、`CNB_TOKEN` 设置到私有仓库的 Repository Secrets

> ⚠️ 私有仓库默认不会暴露镜像名，这是相比 Fork 方案的关键改进

### 第四步：测试验证

参数配置完成后，openclaw 自动拉取 `postgres:latest` 进行测试，通过后汇报结果。

## 安全特性

- ✅ **`.env` 安全加载**：使用 IFS 逐行解析，仅提取需要的变量，无 shell source，避免注入
- ✅ **workflow 内嵌**：GitHub Actions workflow 代码来自技能制品（非外部仓库），透明可查
- ✅ **默认私有仓库**：GitHub 仓库默认为私有，镜像名不会暴露在公开历史记录中
- ✅ **最小权限 Token**：推荐使用 `gh auth login` 登录（不过用户手），或创建细粒度最小权限 Token
- ✅ **环境变量文件保护**：建议 `chmod 600 ~/.openclaw/.env`

## 使用方式

```bash
bash ~/.openclaw/workspace/skills/cnb-image-sync/cnb-pull.sh <镜像名>[:标签]
```

**示例：**

```bash
bash ~/.openclaw/workspace/skills/cnb-image-sync/cnb-pull.sh mongo:latest
bash ~/.openclaw/workspace/skills/cnb-image-sync/cnb-pull.sh nginx:1.25
bash ~/.openclaw/workspace/skills/cnb-image-sync/cnb-pull.sh redis:7-alpine
```

## 关键特性

- **images.txt 始终只有一个镜像**：每次拉取时清空已有记录，只写入目标镜像
- **自动重试**：优先尝试直接从 CNB 拉取（镜像已存在时），失败则走代理中转
- **等待 Actions**：代理模式下等待 GitHub Actions 完成（约 1-3 分钟）
- **不污染 Git 历史**：拉取完成后清空 images.txt，不推送清理
- **彩色输出**：绿色 info、黄色 warn、红色 error

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `CNB_TOKEN` | CNB 访问令牌（必填） | — |
| `CNB_REGISTRY` | CNB 镜像仓库地址 | `docker.cnb.cool` |
| `CNB_REPO_SLUG` | CNB 目标仓库（必填，需小写） | — |
| `CNB_GITHUB_REPO` | GitHub 代理仓库（必填） | — |

## 疑难排除

| 问题 | 解决方案 |
|------|----------|
| `gh: command not found` | 安装 GitHub CLI：`brew install gh` |
| GitHub Actions 失败 | 检查 Repository Secrets 是否正确配置 |
| 拉取超时 | 稍后重试，CNB 制品同步有延迟 |
| 仓库不存在 | 确认 CNB_REPO_SLUG 与制品库命名空间完全一致 |

---

# Docker Image Sync via CNB

**Sync Docker Hub images to CNB.tool registry via GitHub Actions, solving domestic Docker pull failures and enabling OpenClaw to auto-pull images without issues.**

## Prerequisites (Required)

- **GitHub CLI (`gh`)**: Login detection, Fork repo, set Secrets, monitor Actions
  - Install: `brew install gh` (macOS) or [github.com/cli](https://cli.github.com)
  - Login: `gh auth login`
- **Docker CLI (`docker`)**: Login to CNB registry, push and pull images
  - Install: `brew install docker` or from [docker.com](https://docs.docker.com/desktop/install/linux-install/)

## How It Works

When `hub.docker.com` is unreachable, this skill proxies through GitHub Actions:

1. Modify `images.txt` in the GitHub repo — **clear all entries, write only the target image**
2. Push to trigger GitHub Actions sync to CNB
3. Wait for Actions completion
4. Pull the image from CNB to local

## 🚀 Installation

### Step 1 — GitHub Login Check & Create Private Repo

```bash
bash ~/.openclaw/workspace/skills/cnb-image-sync/cnb-pull.sh --check
```

- **Logged in** → Automatically creates private repo `cnb-docker-sync` (**private by default, image names not exposed**)
- **Not logged in** → Run `gh auth login` in terminal, or provide a GitHub Personal Access Token to openclaw

> Token path: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
>
> **Recommended (token never touches user input):**
> Run `gh auth login` — device flow, token managed by `gh`, no copy-paste needed
>
> **If you must provide a Token (fine-grained, minimal scope):**
> Create a Fine-grained Personal Access Token limited to the **`cnb-docker-sync` repo only**, permissions:
> - `Contents: read and write` (commit/push to trigger workflow)
> - `Secrets: read and write` (set Repository Secrets)
> - `Workflows: read and write` (trigger Actions)
> **Do NOT** grant full `repo` scope — limit to this single repository only

### Step 2 — Register CNB Account & Create Registry

#### 2.1 Register CNB Account

Visit [cnb.cool](https://cnb.cool/), sign in with your Alibaba Cloud account (supports QR code login).

![CNB Login](https://github.com/lufei4/docker-image-sync/raw/main/img.png)

#### 2.2 Create a Registry

1. Click your **avatar** (top-right)
2. Select **我的仓库** (My Repositories)
3. Click **创建仓库** (Create Repository), fill in a name, choose type **Docker**

![My Repositories](https://github.com/lufei4/docker-image-sync/raw/main/img_1.png)

![Registry List](https://github.com/lufei4/docker-image-sync/raw/main/img_2.png)

#### 2.3 Get CNB Parameters (Key Step)

After creating the registry, go to: your repository → **制品** (Artifacts) → **使用指引** (Usage Guide) or **操作指引** (Operations Guide).

Click **了解更多** (Learn More) — this contains the CNB parameters needed by this skill:

![Usage Guide — Learn More](https://github.com/lufei4/docker-image-sync/raw/main/img_3.png)

Also in the repository page, click **操作指引** (Operations Guide) to see push/pull commands. Record these two values:

![Operations Guide](https://github.com/lufei4/docker-image-sync/raw/main/img_4.png)

| Parameter | Maps to | Notes |
|-----------|---------|-------|
| `CNB_REGISTRY` | Registry address | Fixed value, e.g. `docker.cnb.cool` |
| `CNB_REPO_SLUG` | Namespace | Format `username/repo-name`, lowercase, e.g. `lufei123/lufei-docker` |

#### 2.4 Get CNB_TOKEN

In the CNB registry page, find **访问令牌** (Access Token) configuration, create an access token for pull authentication.

### Step 3 — Provide Parameters to openclaw

Reply with these 4 values:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `CNB_TOKEN` | CNB access token | `8B76Bopie1d966fVDMgJnhFRepZ` |
| `CNB_REGISTRY` | CNB registry address (fixed value) | `docker.cnb.cool` |
| `CNB_REPO_SLUG` | CNB namespace (lowercase) | `lufei123/lufei-docker` |
| `CNB_GITHUB_REPO` | Private repo address (format: `your-github-username/cnb-docker-sync`) | `your-github-username/cnb-docker-sync` |

**openclaw will automatically:**

1. Write to `~/.openclaw/.env` (please keep this file trusted — run `chmod 600 ~/.openclaw/.env`)
2. Auto-create private repo `your-username/cnb-docker-sync` (if not exists)
3. Push the **bundled GitHub Actions workflow** to your private repo (workflow code comes from skill artifacts, transparent and inspectable)
4. Set `CNB_REGISTRY`, `CNB_REPO_SLUG_LOWERCASE`, `CNB_TOKEN` as Repository Secrets in the private repo

> ⚠️ Private repos do not expose image names in public history — this is the key improvement over the fork approach

### Step 4 — Test Verification

openclaw automatically pulls `postgres:latest` to verify the setup, then reports the result.

## Security Features

- ✅ **Secure `.env` loading**: Uses IFS line-by-line parsing, extracts only needed variables, no shell source, injection-safe
- ✅ **Bundled workflow**: GitHub Actions workflow code comes from skill artifacts (not external repo), transparent and inspectable
- ✅ **Private repo by default**: GitHub repo is private by default, image names are not exposed in public history
- ✅ **Minimal-scope token**: Recommends `gh auth login` (token never exposed in chat), or create fine-grained minimal-scope Token
- ✅ **Environment file protection**: Recommend `chmod 600 ~/.openclaw/.env`

## Usage

```bash
bash ~/.openclaw/workspace/skills/cnb-image-sync/cnb-pull.sh <image>[:tag]
```

**Examples:**

```bash
bash ~/.openclaw/workspace/skills/cnb-image-sync/cnb-pull.sh mongo:latest
bash ~/.openclaw/workspace/skills/cnb-image-sync/cnb-pull.sh nginx:1.25
bash ~/.openclaw/workspace/skills/cnb-image-sync/cnb-pull.sh redis:7-alpine
```

## Key Features

- **images.txt always contains only one image**: Clears existing entries before each pull
- **Auto retry**: Tries direct CNB pull first (works when image already exists), falls back to proxy
- **Waits for Actions**: Waits for GitHub Actions completion (~1-3 min) in proxy mode
- **No Git history pollution**: Clears `images.txt` locally after pull without pushing
- **Colorized output**: Green info, yellow warn, red error

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CNB_TOKEN` | CNB access token (required) | — |
| `CNB_REGISTRY` | CNB registry address | `docker.cnb.cool` |
| `CNB_REPO_SLUG` | CNB target repo (required, lowercase) | — |
| `CNB_GITHUB_REPO` | GitHub proxy repo (required) | — |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `gh: command not found` | Install GitHub CLI: `brew install gh` |
| GitHub Actions failed | Check Repository Secrets configuration |
| Pull timeout | Retry later — CNB sync may have delay |
| Repository not found | Verify `CNB_REPO_SLUG` matches the registry namespace exactly |