---
name: automatic-skill
description: |
  每日 Skill 自动工厂 — 让 openclaw 和 Claude 完全自主地调研、设计、生成、测试并发布全新 skill，全程零人工介入。内置 10 阶段流水线（Research → Design → SEO → Create → Review → Self-Run → Self-Check → Upload → Verify → Final Review），每天凌晨 02:00 自动选题跑完整流程，输出推送到 GitHub 和 clawHub 的生产级 skill。也可手动指定 idea 触发，或单独调用某一阶段进行调试/迭代。支持用自身流水线对已有 skill 做升级、SEO 优化和重新发布。Use it when the user asks to auto-generate a skill, check daily pipeline status, iterate an existing skill, or publish to GitHub and clawHub.
keywords:
  - automatic-skill
  - 自动skill
  - 每日skill
  - skill流水线
  - 技能工厂
  - 自动开发
  - 自动测试
  - 自动发布
  - 元技能
  - skill pipeline
  - skill factory
  - meta skill
  - daily skill
  - auto build skill
  - auto publish skill
  - 自动生成skill
  - 自动制作技能
  - 今日skill
  - 生成新skill
  - skill自动化
  - openclaw skill
  - clawhub publish
  - github skill upload
  - 每日技能推送
  - 10阶段流水线
  - cron skill
  - skill迭代
  - skill升级
  - skill SEO优化
  - self-evolving skill
  - skill自检
  - prompt generator pipeline
  - 零人工介入
  - 自动化内容生产
requirements:
  node: ">=18"
  binaries:
    - name: gh
      required: true
      description: "GitHub CLI — used for auth, repo access, push verification, and PR creation."
    - name: git
      required: true
      description: "Git — used for staging, committing, and pushing skill files."
    - name: clawhub
      required: true
      description: "ClawHub CLI — used for publishing skills to the registry."
    - name: npx
      required: false
      description: "Node package runner — used optionally during skill creation stage."
  env:
    - name: GITHUB_TOKEN
      required: true
      description: "GitHub personal access token with repo write permission (narrowly scoped to a single repo)."
    - name: GITHUB_REPO
      required: true
      description: "Target repository in owner/repo format, e.g. myorg/openclaw-skills"
    - name: CLAWHUB_TOKEN
      required: true
      description: "ClawHub API token for publishing skills to the registry."
    - name: CLAWHUB_OWNER_ID
      required: false
      description: "ClawHub ownerId override. Defaults to the publishing account."
    - name: SKILL_OUTPUT_DIR
      required: false
      description: "Directory where generated skills are written. Defaults to ~/.openclaw/workspace/skills."
    - name: OPENCLAW_NOTIFY_CHANNEL
      required: false
      description: "Notification channel for pipeline failure alerts (e.g. slack://...)."
metadata:
  openclaw:
    homepage: "https://github.com/Cosmofang/automatic-skill"
    author: "Cosmofang"
    runtime:
      node: ">=18"
    permissions:
      - "Reads and writes files in SKILL_OUTPUT_DIR"
      - "Creates GitHub repositories via gh CLI using GITHUB_TOKEN"
      - "Pushes commits to GITHUB_REPO via gh CLI"
      - "Publishes skills to clawHub using CLAWHUB_TOKEN"
      - "Registers cron jobs via openclaw cron (when push-toggle is enabled)"
    env:
      - name: GITHUB_TOKEN
        required: true
        description: "GitHub personal access token — must have 'repo' scope. Scoped to your own repos only. Used by gh CLI to create repos and push commits."
      - name: GITHUB_REPO
        required: true
        description: "Target monorepo in owner/repo format, e.g. yourname/openclaw-skills. Must be a repo you own."
      - name: CLAWHUB_TOKEN
        required: true
        description: "ClawHub API token. Used only to publish skills under your own clawHub account."
      - name: CLAWHUB_OWNER_ID
        required: false
        description: "Your clawHub ownerId. If omitted, defaults to the account associated with CLAWHUB_TOKEN."
      - name: SKILL_OUTPUT_DIR
        required: false
        description: "Where generated skills are written. Defaults to ~/.openclaw/workspace/skills."
      - name: OPENCLAW_NOTIFY_CHANNEL
        required: false
        description: "Notification channel for pipeline failure alerts (e.g. slack://...)."
---

# Automatic Skill — 每日 Skill 自动工厂

> 每天凌晨自动调研 → 设计 → 制作 → 审核 → 自测 → 发布 → 复查，全程无需人工介入（发布阶段使用你自己的 GitHub/clawHub 凭证）

---

## ⚠️ Credentials

**Stages 1–7 use zero credentials.** Only Stage 8 (Upload) and beyond touch your accounts.

| Stage | Action | Credential | What gets written |
|-------|--------|-----------|-------------------|
| 1–7 | Research, Design, SEO, Create, Review, Self-Run, Self-Check | None | Local files only |
| 8a | `gh repo create <owner>/<slug> --public` | `GITHUB_TOKEN` | New public repo on your GitHub account |
| 8b | `git push` to `GITHUB_REPO` | `GITHUB_TOKEN` | New commits to the monorepo you set |
| 8c | `clawhub publish` | `CLAWHUB_TOKEN` | Skill listed publicly under your clawHub account |
| 9–10 | Verify, Final Review | `GITHUB_TOKEN` (read-only `gh api`) | Nothing — read-only checks |
| Cron | Daily auto-run (`push-toggle on`) | None | Registers a local cron job via `openclaw cron` |

**Does NOT:**
- Read, transmit, or log credentials
- Access repos or accounts other than the ones you configure
- Execute network operations from scripts — all network actions go through `gh` CLI and `clawhub` CLI under your control
- Run Stage 8 in `--dry-run` mode (safe for testing entire pipeline without publishing)

**Minimum token scopes:**
- `GITHUB_TOKEN`: fine-grained PAT → single repo → **Contents: Read & write** only
- `CLAWHUB_TOKEN`: keep in shell env (`~/.zshrc`), never commit to any file

---

## Purpose & Capability

automatic-skill 是一个**元技能（meta-skill）**，它的能力是制造其他 skill。

**架构说明（重要）：** 每个阶段脚本是"prompt generator" — 脚本本身不执行任何业务逻辑，只输出结构化 prompt。真正的执行者是 agent（Claude）。网络操作（GitHub push、clawHub publish）均由 agent 调用 `gh` CLI 和 `clawhub` CLI 完成，凭证完全在你的机器上。

**核心能力：**

| 能力 | 说明 |
|------|------|
| 全流水线生成 | 从"想法"到"上线"：Research → Design → SEO → Create → Review → Self-Run → Self-Check → Upload → Verify → Final Review |
| 每日自动选题 | 凌晨 02:00 cron 自动触发，选最高价值 idea，跑完整流程 |
| 手动触发 | 指定 `--idea` 手动选题，或单独跑某一阶段调试 |
| dry-run 模式 | `--dry-run`：执行到 Stage 7 自检后停止，**不发起任何网络操作** |
| 已有 skill 迭代 | 对现有 skill 单独跑 SEO / self-check / upload 阶段进行升级 |

**能力边界（不做的事）：**
- 不直接写 skill 源码（源码由 agent 根据 create 阶段 prompt 生成）
- 不并发生成多个 skill（每次运行产出一个）
- 不访问或修改除 `GITHUB_REPO` 和 `SKILL_OUTPUT_DIR` 以外的任何路径或账号

---

## Instruction Scope

**在 scope 内（会处理）：**
- "帮我自动生成一个 skill" / "skill 流水线跑了没" / "今天出了什么新 skill"
- 手动触发全流水线或单阶段重跑（如"重跑 SEO 阶段"）
- 查看流水线状态和历史日志（`status.js`）
- 开关每日定时任务（`push-toggle on/off`）
- 用 automatic-skill 迭代已有 skill（对现有 skill 升级 / SEO 优化 / 自检 / 上传）

**不在 scope 内（不处理）：**
- 直接编写 skill 源码（源码由 agent 执行 create 阶段 prompt 生成，非 automatic-skill 职责）
- 管理 GitHub 仓库权限、clawHub 账户设置、或任何账户级操作
- 生成非 openclaw skill 格式的内容（普通项目、应用代码等）
- 在未设置 `GITHUB_TOKEN` / `GITHUB_REPO` / `CLAWHUB_TOKEN` 的环境中执行 Stage 8（会提示缺少凭证，不会静默失败）

**凭证缺失时的行为：**
- Stages 1–7：无需凭证，正常运行
- Stage 8 upload：缺少任意必需凭证 → 打印具体缺失变量名 + 配置指引，停止执行（不静默失败）
- `--dry-run`：完整跳过 Stage 8，可安全在无凭证环境测试前七个阶段

---

## Persistence & Privilege

**持久化写入的内容：**

| 路径 | 内容 | 触发条件 |
|------|------|---------|
| `SKILL_OUTPUT_DIR/<slug>/` | 生成的 skill 文件 | Stage 4 Create |
| `data/current-pipeline.json` | 当前流水线运行状态（临时） | 每次流水线运行 |
| `data/pipeline-log.json` | 历次运行历史（追加写入） | Stage 10 Final Review |
| `~/.openclaw/crontab`（或系统 cron） | 每日定时任务条目 | `push-toggle on` 时写入，`off` 时删除 |

**不写入的路径：**
- 不修改 shell 配置文件（`~/.zshrc` 等）
- 不写入 `GITHUB_TOKEN` / `CLAWHUB_TOKEN` 等凭证到任何文件
- 不在 `SKILL_OUTPUT_DIR` 之外创建文件（除 `data/` 目录）

**权限级别：**
- 运行时以当前用户身份执行，不需要 sudo 或提权
- gh CLI 和 clawhub CLI 的权限上限由你配置的 token 范围决定
- 如需撤销所有权限：`push-toggle off`（删除 cron）+ 在 GitHub/clawHub 吊销对应 token

---

## Install Mechanism

### 标准安装（推荐）

从 clawHub 安装到 openclaw workspace：

```bash
clawhub install automatic-skill
# 安装路径：~/.openclaw/workspace/skills/automatic-skill/
```

### 手动安装

从本地源码目录复制：

```bash
cp -r /path/to/automatic-skill ~/.openclaw/workspace/skills/automatic-skill/
```

### 验证安装

```bash
ls ~/.openclaw/workspace/skills/automatic-skill/scripts/
node ~/.openclaw/workspace/skills/automatic-skill/scripts/status.js
# 应输出：No active pipeline run. / pipeline-log.json 状态
```

### 安装后配置

在 shell 环境中设置以下变量（写入 `~/.zshrc` 或 `~/.bashrc`）：

```bash
export GITHUB_TOKEN=<your-github-token>          # repo write scope
export GITHUB_REPO=<owner/repo>                  # e.g. Cosmofang/openclaw-skills
export CLAWHUB_TOKEN=<your-clawhub-token>
export CLAWHUB_OWNER_ID=<your-owner-id>          # optional
export SKILL_OUTPUT_DIR=~/.openclaw/workspace/skills  # optional, this is the default
```

然后验证认证：

```bash
gh auth status        # 应显示 ✓ Logged in
clawhub whoami        # 应返回你的用户名
```

### 启用每日自动运行

```bash
node scripts/push-toggle.js on
# 注册 cron：每天 02:00 自动跑 daily-pipeline.js
```

---

## 何时使用

- 用户说"帮我自动生成一个 skill"/"今天有新 skill 吗"/"skill 流水线跑了没"
- 用户想查看今日生成的 skill 是什么
- 用户想手动触发某一阶段重跑
- 用户想查看生成历史或当前流水线状态
- 用户想用 automatic-skill 迭代/升级/上传某个现有 skill

---

## 🔄 10-Stage Pipeline

| # | Stage | Script | Description |
|---|-------|--------|-------------|
| 1 | Research | `research.js` | Scan trends, identify skill gaps, output Top-3 ideas |
| 2 | Design | `design.js <idea>` | Produce full architecture: file tree, script specs, data schema |
| 3 | SEO | `seo.js` | Optimize display name, tagline, description, 30+ keywords |
| 4 | Create | `create.js` | Generate all files using design + SEO output |
| 5 | Review | `review.js <skill-dir>` | Quality checklist: structure, scripts, content, security |
| 6 | Self-Run | `self-run.js <skill-dir>` | Execute every script, verify zero errors |
| 7 | Self-Check | `self-check.js <skill-dir>` | Validate required fields, file tree, script signatures |
| 7.5 | Safety Check | `scan-check.js <skill-dir>` | Pre-upload credential-safety gate; blocks upload if issues found |
| 8 | Upload | `upload.js <skill-dir>` | Create standalone repo + push monorepo; clawhub publish |
| 9 | Verify | `verify-upload.js <skill-name>` | Confirm live on GitHub and clawHub |
| 10 | Final Review | `final-review.js <skill-name>` | Full report, write to pipeline-log.json |

---

## 📦 Publishing Convention

### Skill Standard Sections

Every skill generated or uploaded by automatic-skill **must** include all five of the following sections in its `SKILL.md`, in this order:

| # | Section | Required content |
|---|---------|-----------------|
| 1 | `## Purpose & Capability` | Core concept + capability table + explicit "Does NOT" boundary |
| 2 | `## Instruction Scope` | In-scope examples + out-of-scope list + behavior on missing credentials |
| 3 | `## Credentials` | Action/Credential/Scope table (or "no credentials required") — no hardcoded tokens |
| 4 | `## Persistence & Privilege` | Paths-written table + "Does NOT write" list + uninstall instructions |
| 5 | `## Install Mechanism` | `clawhub install` command + verification step + env var examples |

Stage 7 (self-check.js) validates all five sections before allowing upload. Missing or empty section = `NEEDS_FIX`.

### GitHub Distribution

Every skill uploaded by automatic-skill **must** have both:

| Destination | Purpose | Command |
|-------------|---------|---------|
| `<owner>/<slug>` (standalone repo) | Users can search and find the skill directly on GitHub | `gh repo create <owner>/<slug> --public` → push skill files |
| `GITHUB_REPO/openclaw/agents/skills/<slug>/` (monorepo) | Registry index — all skills listed in one place | `git add openclaw/agents/skills/<slug>/` → push |

**Stage 8 always runs standalone repo creation first, then monorepo push.**

If the standalone repo already exists, skip creation and force-push the latest files.

---

## 🌐 Language Policy

- **SKILL.md content**: English (default)
- **Conversation with user**: match user's language — Chinese if user writes Chinese
- **JSON logs & reports**: English only

---

## 🛠️ Usage

```bash
# Full pipeline (recommended)
node scripts/pipeline.js                   # auto-select topic, run all stages
node scripts/pipeline.js --idea "daily-poem" # specify topic
node scripts/pipeline.js --dry-run         # run through self-check only, no upload

# Per-stage debug
node scripts/research.js                   # output research prompt
node scripts/design.js "daily-poem"        # output design prompt
node scripts/seo.js --from-pipeline        # output SEO optimization prompt
node scripts/create.js --from-pipeline     # output create prompt
node scripts/review.js /path/skill-dir     # output review prompt
node scripts/self-run.js /path/skill-dir   # output self-run prompt
node scripts/self-check.js /path/skill-dir # output self-check prompt
node scripts/upload.js /path/skill-dir     # output upload prompt (direct push)
node scripts/upload.js --pr /path/skill-dir  # output upload prompt (PR workflow)
node scripts/verify-upload.js skill-name   # output verify prompt (gh api checks)
node scripts/final-review.js skill-name    # output final review prompt

# Status & history
node scripts/status.js                     # current pipeline status
node scripts/status.js --history [N]       # last N runs (default 10)
node scripts/status.js --clear             # clear current pipeline state

# Cron toggle
node scripts/push-toggle.js on             # enable daily 02:00 auto-run
node scripts/push-toggle.js off            # disable
node scripts/push-toggle.js status         # show status
```

---

## ⏰ Cron Setup

```bash
openclaw cron add "0 2 * * *" "cd ~/.openclaw/workspace/skills/automatic-skill && node scripts/daily-pipeline.js"
openclaw cron list
openclaw cron delete <job-id>
```

---

## 📁 File Structure

```
data/
  pipeline-log.json       # append-only history of all pipeline runs
  current-pipeline.json   # transient state during active run
scripts/
  research.js             # stage 1
  design.js               # stage 2
  seo.js                  # stage 3 — SEO optimization
  create.js               # stage 4
  review.js               # stage 5
  self-run.js             # stage 6
  self-check.js           # stage 7
  upload.js               # stage 8
  verify-upload.js        # stage 9
  final-review.js         # stage 10
  pipeline.js             # orchestrator
  daily-pipeline.js       # cron entry point
  status.js               # status query
  push-toggle.js          # cron toggle
```

---

## ⚠️ Notes

1. Required env vars: `GITHUB_TOKEN`, `GITHUB_REPO`, `CLAWHUB_TOKEN`
2. Optional: `CLAWHUB_OWNER_ID` (your clawHub owner ID), `SKILL_OUTPUT_DIR` (default: `~/.openclaw/workspace/skills`)
3. **GitHub operations use the `gh` CLI** (inspired by [steipete/github](https://clawhub.ai/steipete/github)): `gh auth status`, `gh repo view`, `gh api`, `gh pr create`. Install with `brew install gh` and run `gh auth login` before first use.
4. Stage 8 supports `--pr` flag for a PR-based GitHub workflow instead of direct push to main.
5. Stage 9 verifies GitHub state live via `gh api repos/{repo}/contents/{path}` — no `git fetch` needed.
6. **Every skill gets a standalone GitHub repo** (`<owner>/<slug>`) in addition to the monorepo entry — this lets users search and discover skills directly on GitHub
7. On any stage failure the pipeline stops and logs the error — no partial overwrites
8. `--dry-run` stops after self-check, no network operations
9. Full run history in `data/pipeline-log.json`
10. All scripts are prompt generators only — no outbound network requests are made by the scripts themselves

---

## 🧪 Test Run Log (2026-04-04)

First full dry-run results:

| Stage | Status | Notes |
|-------|--------|-------|
| 1 Research | ✅ | Scanned 17 existing skills, identified 5 gaps, selected daily-poem |
| 2 Design | ✅ | Fix: `--from-pipeline` reads from `pipeline.research.selected` not top-level |
| 3 SEO | ✅ | Added in v1.1.0 — produces displayName, tagline, 30+ keywords |
| 4 Create | ✅ | Generated 9 files including 4 scripts |
| 5 Review | ✅ | Score 97/100, 1 warning (empty data array, expected) |
| 6 Self-Run | ✅ | 6 script calls, all passed |
| 7 Self-Check | ✅ | 22/22 checks passed, score 100 |
| 8 Upload | ✅ | dry-run skipped — requires GITHUB_TOKEN / GITHUB_REPO / CLAWHUB_TOKEN |
| 9 Verify | ✅ | dry-run skipped |
| 10 Final Review | ✅ | Archived to pipeline-log.json |

**Environment variables:**
```bash
export GITHUB_TOKEN=<your-token>
export GITHUB_REPO=<owner/repo>
export CLAWHUB_TOKEN=<your-clawhub-token>
export CLAWHUB_OWNER_ID=<your-owner-id>   # optional
export SKILL_OUTPUT_DIR=~/.openclaw/workspace/skills  # optional
```

---

*Version: 1.4.1 · Created: 2026-04-04 · Updated: 2026-04-09*
