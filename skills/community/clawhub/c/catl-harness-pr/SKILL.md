---
name: catl-harness-pr
version: 0.5.0
description: 【业务龙虾干活前的第一站】蓝标宁德项目任务启动前必读。三步自检：① 已有 skill 吗（表中查）② 已有知识吗（grep harness repo）③ 选对模型吗（调 bluefocus-model-routing）。附清单：模型路由、出图、云存储、抖音/视频号/社媒采集、Wiki 写入等部门已封装 skill。同时提供向 BlueFocusContentUniverse/catl_harness_repo 提交 PR 的完整流程（environment preflight, forced upstream sync, branch naming, commit/PR template, gh/HTTPS+PAT/SSH 认证路径、fork+cross-repo PR 默认模式），以及每日自动总结 + PR + skill 自更新能力（3 条 cron）。触发词：提交到 harness / 推到 GitHub / 发个 PR / harness layer 更新 / 宁德任务 / 宁德 skill / 该用哪个 skill / 选模型 / 节省成本。权威位置：部门 skill 总入口 + harness 仓库入档出口。鉴权/Token 问题联系 @Dr-xiaoming，不要自行改 token。NOT for: 其他项目的通用 GitHub PR、代码仓、非宁德/非蓝标场景。
---

# CATL Harness PR Submission

This skill teaches OpenClaw agents (龙虾) how to submit pull requests to **`BlueFocusContentUniverse/catl_harness_repo`** — the CATL knowledge-engineering harness repo (蓝标内容宇宙组织下，2026-05-08 起取代旧的 `Dr-xiaoming/catl_harness_repo` 个人仓)。 Treat it as **a versioned knowledge base, not a code base**: every PR is a deliberate, sourceable knowledge increment.

## 🛑 业务龙虾任务前 30 秒自检（必读 / Stop-think-act）

**这是这份 skill 最重要的章节**。所有蓝标龙虾在执行任何宁德/项目类任务前，**先停 30 秒走一遍这三步**，再动手：

### Step 1：是不是已经有 skill 干过这事？

下面这些场景**不要重新造**，直接装现成 skill：

| 任务关键词 | 用哪个 skill | 安装命令 |
|---|---|---|
| 提交知识 / 沉淀经验 / 入档仓库 | `catl-harness-pr`（就是当前这个）| `clawhub install catl-harness-pr` |
| 选模型 / 哪个便宜 / 子 agent 模型 / cron 模型 | `bluefocus-model-routing` | `clawhub install bluefocus-model-routing` |
| 出图 / 画一张 / moodboard / 配图 / nano banana | `blueai-nano-banana` | `clawhub install blueai-nano-banana` |
| 上传文件 / 拿公网 URL / 图片云存储 | `blueai-media-storage` | `npx blueai-skills@latest add blueai-media-storage -a openclaw -y` |
| 抖音搜账号 / 关键词 → 账号 + 视频 + 粉丝数 | `blueai-douyin-account-discovery` | `npx blueai-skills@latest add blueai-douyin-account-discovery -a openclaw -y` |
| 微信视频号搜索 / 视频列表 / 评论 / 下载 | `blueai-smd-wechat-channels` | `npx blueai-skills@latest add blueai-smd-wechat-channels -a openclaw -y` |
| 小红书 / 抖音 / B 站 / 微博 / 公众号采集 | `blueai-social-media-data`（底座） | `npx blueai-skills@latest add blueai-social-media-data -a openclaw -y` |
| 飞书 Wiki 写入 / 客户档案沉淀 | `catl-wiki` | （已装）|
| 找现有 skill | `find-skills` | （已装，调 `find-skills` 关键字搜）|

**强行规则**：每次使用上面任意 skill 之前，**必须先 `clawhub update --all` 同步最新版本**。

### Step 2：是不是已经有沉淀过的知识？

如果是宁德 / 客户认知 / 项目方法论相关任务，**先看 `catl_harness_repo` 里有没有相关 layer**，不要从零开始：

```bash
REPO=~/.openclaw/workspace/repos/catl_harness_repo
cd "$REPO" && git pull --ff-only
ls 01-knowledge/ 02-skills/ 03-projects/ 04-daily/ 99-meta/ 2>/dev/null
grep -ri "<关键词>" 01-knowledge/ 02-skills/  # 比如 grep "神行" "安全叙事" "竞品"
```

找到了 → 拿来用，干完后**把增量沉淀回去走 PR**（见 Phase A-E）。
找不到 → 干，干完后**把这次的产物按规范沉淀回去走 PR**。

### Step 3：选对模型，不要烧钱

用 `bluefocus-model-routing` skill 的决策表：

- 编程 / 调试 / 复杂工具调用 → `gpt5.5`
- 长文档 / 中文长文 / 多平台抓取 → `v4pro`
- 子 agent 写文件 / 整理 → `v4flash`
- 日常对话默认 → `sonnet`
- 战略分析 → `opus`（**慎用，贵**）
- 简单脚本能搞定 → 不要用 LLM

**反模式**：所有任务无脑跟主 session 默认 → 子 agent 跟着用 opus → 月成本翻 10 倍。

### 🚦 一句话总结

```
任务来 → ① 已有 skill 吗？ → ② 已有知识吗？ → ③ 选对模型吗？ → 才开始动手
         clawhub update --all   git pull harness repo    bluefocus-model-routing
```

**鉴权 / API key 任何问题** → **联系金明 (@Dr-xiaoming)**，不要自己改 token，不要自己尝试绕过。

---


## Two modes (since v0.3.1)

This skill supports two PR submission modes, **auto-detected by `preflight.sh`**:

| Mode | Used when | How |
|---|---|---|
| **`fork`** (default) | 你的 GitHub 账号对原仓库**没有 write 权限** | Fork → push to fork → cross-repo PR |
| **`legacy`** | 你的 GitHub 账号对原仓库**有 write 权限**（金明本人 / 组织 maintainer） | 直接在原仓库切分支 push → 同仓库 PR |

**探测命令**：`gh api repos/BlueFocusContentUniverse/catl_harness_repo --jq .permissions.push`
- 输出 `true` → legacy 模式
- 输出 `false` 或调用失败 / 没 gh → fork 模式

**强制覆盖**：设 `CATL_HARNESS_PR_MODE=fork` 或 `CATL_HARNESS_PR_MODE=legacy` 环境变量。

> Fork 模式是默认且未来主流。绝大多数龙虾对组织里的 private repo 只有 read 权限，fork + PR 是唯一可行路径。

## Repo facts

- **Upstream URL**: `https://github.com/BlueFocusContentUniverse/catl_harness_repo`
- **Organization**: `BlueFocusContentUniverse` (蓝标内容宇宙)
- **Maintainer**: 佘金明 (`Dr-xiaoming`，GitHub 个人账号) — BlueFocus 宁德时代项目组 产研组 FDE
- **Visibility**: private — 不是每个龙虾的环境都自带访问权，缺 token/SSH 就得先解决认证；fork 出来仍是 private（GitHub 默认行为）
- **Local clone path (convention)**: `~/.openclaw/workspace/repos/catl_harness_repo`
- **Local remote layout (fork mode)**:
  - `origin` → `https://github.com/<your-gh-user>/catl_harness_repo.git` (your fork, push 用)
  - `upstream` → `https://github.com/BlueFocusContentUniverse/catl_harness_repo.git` (read-only sync)
- **Local remote layout (legacy mode)**:
  - `origin` → `https://github.com/BlueFocusContentUniverse/catl_harness_repo.git` (单 remote)
- **Companion**: 飞书 Wiki「宁德时代·客户档案」(see `catl-wiki` skill). Feishu 是协作权威副本，GitHub 是版本/diff/审阅可追溯副本。两边都要同步时：**先 Feishu 定稿，再 PR 到 GitHub**。

## Hard rules (read first, violating any = stop)

1. **每次开始修改前，必须先同步远程到本地**（fork 模式同步 upstream，legacy 模式同步 origin）。不管上次修改离现在多近。见下方 "Phase B: sync"。
2. **永不直推 `main`**。所有改动走 feature branch + PR，即使是 typo。
3. **PR 必须有来源**。每个知识增量必须能回溯到一次会议、一份纪要、一次客户沟通、一份外部资料、或一份内部讨论。
4. **不泄露甲方未公开内容**。即使 repo 是私有的，PR 描述/commit/diff 也不要直接复述甲方原话。遇到敏感资料写成"源自客户访谈纪要 (内部，2026-XX-XX)"即可。
5. **不把蓝标判断写进客户的嘴里**。蓝标内部分析放 `internal-analysis/` 或 frontmatter `tags: [bluefocus-pov]`，不要混入 `layer1-client-cognition/`。
6. **大改动先开 issue**。新增 layer、调目录结构、删节点 → 先开 issue `@Dr-xiaoming` 确认方向。

---

## Execution phases (do them in order, do not skip)

### Phase A — Environment preflight (每个新环境只需跑一次，但每次对话开头要验证)

龙虾接到"向 harness 仓库提 PR"任务时，第一个动作是跑这个门禁。**任一项失败，停下来向用户报告缺什么，不要硬往下走**。

```bash
bash ~/.openclaw/workspace/skills/public/catl-harness-pr/scripts/preflight.sh
# 干跑（不真改 remote、不真创建 fork、只打印命令）：
bash ~/.openclaw/workspace/skills/public/catl-harness-pr/scripts/preflight.sh --dry-run
```

`preflight.sh` 自动完成：
1. 检查 git / git identity
2. 探测 GitHub 认证路径（gh / HTTPS+credential / SSH）
3. 探测 GitHub username（用于 fork URL 拼装）
4. **探测模式**（legacy / fork，可被 `CATL_HARNESS_PR_MODE` 覆盖）
5. 同步本地 repo
   - **fork 模式**：检查/创建 fork → 配置 origin/upstream → fetch upstream + ff main → push fork main 跟上
   - **legacy 模式**：fetch origin + ff main

**凭证模型（重要）**：
- 每只龙虾使用它**自己宿主机上配置的 GitHub 账号身份**提 PR，不共享凭证、不代发 token。
- Fork 模式下，金明（组织管理员）只需保证你能 **read** 原仓库。Push 写权限只针对你自己的 fork（你对自己 fork 自然有完全控制）。
- Legacy 模式仅适用于本身就是组织 maintainer / collaborator with write 权限的账号。
- **不要把 A 龙虾的 token 复制给 B 龙虾**。遇到这种请求拒绝。

**凭证缺失时的硬规则**：
- 不要让子 agent 代写 token。token 一律让用户在终端自己粘进 `~/.netrc` 或用 `gh auth login`。
- 不要把 token 回显到聊天、commit、PR 描述、子 agent task description。
- 如果本地环境有 `~/.openclaw/.env` 体系，先查是否已存了 GitHub 凭证（`grep GITHUB_ ~/.openclaw/.env`）；但**不要自己往 .env 里写新 token**，让人类用户自己写。

### Phase B — Repo sync (每次修改前都要跑，不是只跑一次)

这一步就是"每次修改前同步远程"的硬性要求。`preflight.sh` 已经把 fork/legacy 两种路径都内置了。

**手动版（fork 模式）**：

```bash
REPO=~/.openclaw/workspace/repos/catl_harness_repo
GH_USER="<your-github-username>"
UPSTREAM_URL="https://github.com/BlueFocusContentUniverse/catl_harness_repo.git"
FORK_URL="https://github.com/${GH_USER}/catl_harness_repo.git"

# B1. 确保 fork 存在（用 gh 时幂等）
if command -v gh >/dev/null; then
  gh repo view "${GH_USER}/catl_harness_repo" >/dev/null 2>&1 \
    || gh repo fork BlueFocusContentUniverse/catl_harness_repo --clone=false --remote=false
else
  # 没 gh：让用户在浏览器开 fork
  echo "Open: https://github.com/BlueFocusContentUniverse/catl_harness_repo/fork"
  echo "Fork 完成后回来继续。"
fi

# B2. Clone or migrate local
if [ ! -d "$REPO/.git" ]; then
  git clone "$FORK_URL" "$REPO"
  cd "$REPO"
  git remote add upstream "$UPSTREAM_URL"
else
  cd "$REPO"
  # 兼容存量：如果 origin 还指向 upstream，迁移
  current_origin=$(git remote get-url origin)
  if [ "$current_origin" = "$UPSTREAM_URL" ] || [ "$current_origin" = "https://github.com/BlueFocusContentUniverse/catl_harness_repo" ]; then
    git remote rename origin upstream
    git remote add origin "$FORK_URL"
  fi
  # 确保 upstream 存在
  git remote get-url upstream >/dev/null 2>&1 || git remote add upstream "$UPSTREAM_URL"
fi

# B3. 同步 main: upstream → local → fork
git fetch upstream --prune
git fetch origin --prune
git checkout main
git pull --ff-only upstream main
git push origin main   # 让 fork 的 main 跟上 upstream
```

**手动版（legacy 模式，仅限对原仓库有 write 的账号）**：

```bash
REPO=~/.openclaw/workspace/repos/catl_harness_repo
cd "$REPO"
git fetch origin --prune
git checkout main
git pull --ff-only origin main
```

**关键理解**：Phase B 不是 Phase A 的延续，而是**每次开工前都跑一遍的独立门禁**。即使 10 分钟前刚跑过，也要重跑——别的协作者可能刚刚合了 PR。

### Phase C — Make changes on a feature branch

```bash
# C1. 从最新的 main 切新分支（分支名见 references/branch-naming.md）
git checkout -b layer1/client-cognition-update-20260508

# C2. 进行实际修改 —— 只改 markdown，除非明确要求
# (edit files here)

# C3. 本地 review
git status
git diff --stat
git diff | head -200      # 眼过一遍实际内容

# C4. 如果看到 .DS_Store / IDE 文件 / 个人笔记 / 原始 chat 记录 — 立刻清
# git restore --staged <file>  或  把它加进 .gitignore
```

### Phase D — Commit

```bash
git add <specific-files>   # 不要 git add .，容易带脏文件

git commit -m "layer1(client-cognition): 补充 Q2 神行品牌叙事差异化要点

- 来源: 2026-05-06 虞旸定稿 draft-v2 + 5/3 客户访谈
- 影响范围: layer1/客户认知底座.md 第 3 节
- 审阅人: @Dr-xiaoming"
```

Commit message 规则完整版见 `references/commit-style.md`。必须带「来源 / 影响范围 / 审阅人」三段。

### Phase E — Push & open PR

#### Fork 模式

```bash
# E1. 推送前再 fetch upstream 一次，确认 main 没变化（很快）
git fetch upstream main
behind=$(git rev-list --count HEAD..upstream/main)
if [ "$behind" -gt 0 ]; then
  echo "⚠️  upstream/main 在我干活期间前进了 $behind 个 commit，考虑 rebase："
  echo "   git rebase upstream/main"
fi

# E2. Push feature branch 到自己的 fork（origin）
git push -u origin "$(git branch --show-current)"

# E3. 写 PR body 到 /tmp/pr-body.md（模板见下节）

# E4. 开跨仓库 PR（关键参数：--head <user>:<branch>）
GH_USER="<your-github-username>"
BRANCH=$(git branch --show-current)
if command -v gh >/dev/null; then
  gh pr create \
    --repo BlueFocusContentUniverse/catl_harness_repo \
    --base main \
    --head "${GH_USER}:${BRANCH}" \
    --title "layer1(client-cognition): 补充 Q2 神行品牌叙事差异化" \
    --body-file /tmp/pr-body.md \
    --reviewer Dr-xiaoming
else
  # 没 gh → 浏览器开跨仓库 compare
  echo "请在浏览器打开："
  echo "https://github.com/BlueFocusContentUniverse/catl_harness_repo/compare/main...${GH_USER}:catl_harness_repo:${BRANCH}?expand=1"
  echo "把 /tmp/pr-body.md 的内容粘进 description。"
fi
```

#### Legacy 模式

```bash
# E1. 推送前再 fetch
git fetch origin main
behind=$(git rev-list --count HEAD..origin/main)
if [ "$behind" -gt 0 ]; then
  echo "⚠️  main 在我干活期间前进了 $behind 个 commit，考虑 rebase："
  echo "   git rebase origin/main"
fi

# E2. Push 新分支到原仓库
git push -u origin "$(git branch --show-current)"

# E3. 开同仓库 PR
if command -v gh >/dev/null; then
  gh pr create \
    --title "layer1(client-cognition): 补充 Q2 神行品牌叙事差异化" \
    --body-file /tmp/pr-body.md \
    --base main \
    --reviewer Dr-xiaoming
else
  branch=$(git branch --show-current)
  echo "请在浏览器打开："
  echo "https://github.com/BlueFocusContentUniverse/catl_harness_repo/compare/main...${branch}?expand=1"
fi
```

---

## PR description template

写到 `/tmp/pr-body.md`，是每个 harness PR 的合同：

```markdown
## What
<!-- 一句话说明这次 PR 改了什么。不要写「更新文档」这种废话。 -->

## Why / Source
<!-- 必填。这次知识增量从哪里来？ -->
- 来源类型: [ ] 会议纪要 / [ ] 客户访谈 / [ ] 外部资料 / [ ] 内部讨论 / [ ] 二次提炼 / [ ] 我的判断
- 时间: 2026-XX-XX
- 关联资料: (Feishu 链接 / 文件路径 / 会议名)

## Scope of impact
- 影响 Layer: [ ] L1 客户认知 / [ ] L2 行业认知 / [ ] L3 项目方法论 / [ ] SOP / [ ] 其他
- 下游引用: (列出会用到这份知识的 agent / skill / 任务)

## Sensitive content check
- [ ] 没有甲方原话 / 内部敏感措辞
- [ ] 没有把蓝标主观判断写成「客户立场」
- [ ] 客户/竞品名字处理符合 Layer 1 红线

## Reviewers
- [ ] @Dr-xiaoming (默认必审)
- [ ] (可选) 业务侧第二审阅人
```

Default reviewer 永远是 `@Dr-xiaoming`。第二审阅人仅在跨业务域时加。

---

## After the PR is opened

1. **立刻把 PR URL 回传给用户**。
2. **不要自动 merge**，即使有权限。等人工（金明）review。
3. **收到 review 意见**：在同一分支上追加 commit；不要 force-push，除非明确要求 rebase 清历史。
4. **merge 之后**：如果这份内容同时在飞书 Wiki 存在，确认 Wiki 版本已先于 GitHub 更新——否则 GitHub 就成了单向漂移。
5. **Fork 模式下**：merge 后回本地 `git checkout main && git pull --ff-only upstream main && git push origin main` 把 fork 的 main 同步上来。

---

## 部门已封装 Skills 速查（必读）

蓝标产研组 / 龙虾团队封装的 skills 清单。**每次使用前先向 ClawHub 同步最新版本**：

```bash
clawhub update --all
```

如果使用过程中遇到**鉴权问题**（API key 失效、403、401、token 过期等），**联系金明 (@Dr-xiaoming)**，不要自己尝试改 token。

| Skill | 版本 | 功能 | 安装命令 |
|---|---|---|---|
| `bluefocus-model-routing` | v0.1.0 | **任务前必读**——蓝标场景实战模型路由策略，6 类任务决策表，子 agent / cron / 主 session 三场景细分，含真实失败案例 | `clawhub install bluefocus-model-routing` |
| `blueai-douyin-account-discovery` | v1.0.1 | 抖音关键词搜索 → 账号发现 + 视频列表 + 粉丝数回填（TikHub 底层）| `npx blueai-skills@latest add blueai-douyin-account-discovery -a openclaw -y` |
| `blueai-social-media-data` | unversioned (底座) | 小红书/抖音/B站/微博/微信公众号/视频号 共 10 种模式的数据采集底座，被其他 skill 委托调用 | `npx blueai-skills@latest add blueai-social-media-data -a openclaw -y` |
| `blueai-smd-wechat-channels` | v1.0.0 | 微信视频号专用入口（搜账号/视频列表/评论/搜一搜/下载），依赖 social-media-data 底座 | `npx blueai-skills@latest add blueai-smd-wechat-channels -a openclaw -y` |
| `blueai-media-storage` | 2026-05-21 上线 | 上传本地文件到蓝标云存储（火山/腾讯/阿里/GCP），拿公网 URL，用于项目里直接 src 引用 | `npx blueai-skills@latest add blueai-media-storage -a openclaw -y` |
| `blueai-nano-banana` | v0.1.0 | 调用 BlueAI relay 的 Nano Banana / Gemini image preview 模型生图（Python 一行命令出 PNG，自动读 `~/.openclaw/.env` 里的 `BLUEAI_RELAY_KEY`）| `clawhub install blueai-nano-banana` |

**两套 CLI 区别**：
- `npx blueai-skills@latest ...` → 蓝标内部 BlueAI Skills Market（host: `https://blueai-skills-market.bluemediagroup.cn/`）
- `clawhub ...` → ClawHub 公共/私有 skill 仓

**升级红线**（来自 wechat-channels 官方告警）：
- ❌ 绝对禁止 `npx blueai-skills update`——会替换工作目录代码为软链接，本地修改丢失
- ✅ 用 `clawhub update --all` 走 ClawHub 路径，或对 BlueAI skills 用 `add` 重新安装

---

## When this skill does NOT apply

- **其他 GitHub 项目的 PR** — 用通用 git/gh 知识，不要套用这里的知识工程模板。
- **直接编辑飞书 Wiki / 飞书云文档** — 用 `catl-wiki` 或 `feishu-doc` skill。
- **本地 Obsidian 笔记同步** — 用 `obsidian-openclaw-sync` skill。

---

## Daily Auto-Pipeline (v0.4.0+)

业务龙虾装上 skill 后，自动注册 3 条 cron 实现每日工作总结自动化闭环。

### 三条 Cron

| 时间 | 脚本 | 功能 |
|------|------|------|
| 01:00 | `daily-summarize.sh` | 收集昨日数据 → v4flash 分类 → 脱敏 → 生成 MD → 提交 PR |
| 03:00 | `preflight.sh --sync-only` | 同步 catl_harness_repo 上游 |
| 07:00 | `check-update.sh` | 检查 skill 更新 → 有则飞书通知 |

### 首次安装

```bash
bash ~/.openclaw/workspace/skills/public/catl-harness-pr/scripts/install-cron.sh
```

交互式流程：输入拼音名 → 飞书 open_id → 自动探测 GitHub username → 写入 `.env` → 注册 cron → 提示 `lark-cli auth login --as user`

### 数据流

```
memory/YYYY-MM-DD.md ─┐
飞书消息 (lark-cli)  ─┼─→ filter-catl.py (v4flash) ─→ sanitizer.py (三档) ─→ 04-daily/individual/<pinyin>/YYYY-MM-DD.md ─→ PR
妙记纪要 (lark-cli)  ─┘
```

### 脱敏三档

| 级别 | 行为 | 示例 |
|------|------|------|
| **high** | 拒交，存 `local-only/` | 甲方原话、未公开决策、吐槽客户 |
| **medium** | 替换措辞 + ⚠️ label | 客户偏好、内部讨论 |
| **normal** | 直通 | 普通工作记录 |

详见 `references/sensitivity-rules.md`。

### 手动测试

```bash
# 干跑（不真发 PR）
bash scripts/daily-summarize.sh --dry-run --date 2026-05-14

# 单独测试分类器
python3 scripts/filter-catl.py --dry-run --input "今天修了龙虾的 bug"

# 单独测试脱敏器
python3 scripts/sanitizer.py --input /tmp/test.md --sensitivity medium --dry-run
```

### 故障排查

- daily-summarize 没生成 PR → 检查 `memory/` 是否有日志、`filter-catl.py` 是否判 `is_catl=false`
- 飞书消息拉取失败 → 确认 `lark-cli auth login --as user` 已完成
- PR 创建失败 → 手动跑 `preflight.sh` 检查认证
- Cron 未执行 → `openclaw cron list` + `openclaw cron runs --id <job-id>`

详见 `references/daily-pipeline.md`。

---

## Bundled resources

- `scripts/preflight.sh` — 一键跑 Phase A + Phase B 门禁（双模式自动探测，支持 `--dry-run` 和 `--sync-only`）
- `scripts/setup-fork.sh` — 独立的 fork 创建/远程配置脚本（preflight 会调用，也能单跑）
- `scripts/daily-summarize.sh` — **v0.4.0 新增** 每日自动总结 + PR 主脚本
- `scripts/filter-catl.py` — **v0.4.0 新增** v4flash LLM 二分类器
- `scripts/sanitizer.py` — **v0.4.0 新增** 三档脱敏器
- `scripts/check-update.sh` — **v0.4.0 新增** skill 自更新检查
- `scripts/install-cron.sh` — **v0.4.0 新增** 首次安装向导
- `references/branch-naming.md` — 分支命名规则表
- `references/commit-style.md` — commit message 风格与反模式
- `references/auth-setup.md` — gh / HTTPS+PAT / SSH 三种认证路径详解（fork & legacy 模式 PAT scope 区别）
- `references/repo-layout.md` — 仓库目录结构与知识归类速查
- `references/daily-pipeline.md` — **v0.4.0 新增** cron 详细机制 + 故障排查
- `references/sensitivity-rules.md` — **v0.4.0 新增** 三档脱敏规则案例
- `references/pinyin-naming.md` — **v0.4.0 新增** 拼音命名规则 + 已知清单

---

## CHANGELOG

### v0.5.0 (2026-05-25)

**重大新增：业务龙虾任务前自检流程**

- 新增 SKILL.md 顶部「🛑 业务龙虾任务前 30 秒自检」章节（在 Two modes 之前），强制业务龙虾在执行任务前走「① 已有 skill 吗 → ② 已有知识吗 → ③ 选对模型吗」三步
- 新增 `bluefocus-model-routing` skill 引用，作为 Step 3 模型选择的依据
- 「部门已封装 Skills 速查」表头部加入 `bluefocus-model-routing` 条目
- 鉴权问题统一指向金明（@Dr-xiaoming）

### v0.4.2 (2026-05-25)

- 新增「部门已封装 Skills 速查」章节：列出 5 个部门 skill 的版本、功能描述与安装命令
- 明确「每次使用前先 `clawhub update --all` 同步」的硬性要求
- `blueai-nano-banana` v0.1.0 同步发布到 ClawHub

### v0.4.1 (2026-05-20)

**修复**

- `filter-catl.py` prompt 重写：加 7 个 few-shot 示例、明确 CATL 项目子线范围（ESVL/储能/Tech Day/海外早报/媒体库等）、创建「字面凭证 vs 描述凭证流程」边界。验证集上 5/18 ESVL、5/19 媒体库、5/20 harness 部署全部判对
- `install-cron.sh` 适配 OpenClaw 2026.5.x 的 cron 接口（`--cron`/`--message`/`--session`，旧 flag `--schedule`/`--task-file` 已不可用）

**依赖变动**

- 配套使用 `99-meta/sanitizer/sensitive-terms.v1.1.yaml`（在 catl_harness_repo 里同步发 PR 合入）

### v0.4.0 (2026-05-15)

**新增: Daily Auto-Pipeline**

- 新增 `daily-summarize.sh`: 每日自动收集数据源 → v4flash 分类 → 脱敏 → 生成 MD → 提交 PR
- 新增 `filter-catl.py`: v4flash LLM 二分类器（is_catl / is_toxic / sensitivity）
- 新增 `sanitizer.py`: 三档脱敏器（high 拒交 / medium 替换 / normal 直通）
- 新增 `check-update.sh`: skill 自更新检查 + 飞书通知
- 新增 `install-cron.sh`: 首次安装向导（拼音名 + cron 注册 + lark-cli 认证提示）
- `preflight.sh` 新增 `--sync-only` flag（只跑 Phase B 同步，跳过 Phase A 环境检查）
- 新增 3 个 reference: `daily-pipeline.md`, `sensitivity-rules.md`, `pinyin-naming.md`

**数据源**: memory/YYYY-MM-DD.md + 飞书消息 (lark-cli) + 妙记纪要 (lark-cli)

**输出**: `04-daily/individual/<pinyin>/YYYY-MM-DD.md`，超 50KB 自动切分

### v0.3.1 (2026-05-09)

- 仓库迁移: `Dr-xiaoming/catl_harness_repo` → `BlueFocusContentUniverse/catl_harness_repo`
- 新增 fork 模式（默认），legacy 模式保留
- `preflight.sh` 双模式自动探测
- 新增 `setup-fork.sh` 独立 fork 管理脚本

### v0.3.0 (2026-05-07)

- 初始发布到 ClawHub
- Phase A-E 完整 PR 流程
- 3 个 reference: branch-naming, commit-style, auth-setup
