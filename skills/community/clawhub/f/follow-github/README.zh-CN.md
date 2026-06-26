**[English](README.md)** | 中文

# Follow GitHub

> 你的个性化 GitHub 摘要 —— 每日或每周一份，推到你的消息通道或邮箱。

一个追踪三类内容并重整成易读摘要的 skill：

1. **你关注的人** —— 新建的仓库、star 过的项目、维护的仓库发布新版本
2. **GitHub Trending** —— 当下 GitHub 的热门仓库，可按语言过滤
3. **新兴热门项目** —— 最近冒出来、star 增长快的新仓库

数据**实时**从 GitHub API 和 `github.com/trending` 获取。没有中央服务器、没有第三方
数据管道 —— 只是你自己的 token 直接请求 GitHub。

灵感来自 [follow-builders](https://github.com/zarazhangrui/follow-builders)。

## 快速开始

如果你是 OpenClaw / ClawHub 用户：

```bash
openclaw skills install follow-github
```

然后开一个对话，说 `配置 follow-github` 或 `set up follow-github`。

## 你会得到什么

一份每日或每周的 GitHub 摘要，可按环境通过以下渠道送达：

- OpenClaw 对话内直接送达
- Telegram 机器人消息
- Resend 邮件
- 终端内按需获取

你可以配置：

- 要包含哪些内容流：Following、Trending、Hot New Projects
- Trending / Hot 的语言过滤
- 摘要语言：英文、中文、双语
- 发送频率、时间、时区和投递渠道

## 输出示例

```markdown
# GitHub 速递 — 2026-04-20

## 你关注的人

**karpathy**
- star 了 unslothai/unsloth — 2-5x 更快的 LLM 微调 [Python] ★ 18.4k
- 新建了 karpathy/llm-c — 纯 C 实现的 LLM 训练 [C]

3 个你关注的人 star 了 anthropics/claude-cookbook
（levie、simonw、swyx）

## Trending

- forrestchang/andrej-karpathy-skills — 一个 CLAUDE.md 优化 Claude Code
  [Markdown] +45k ★ 本周
- NousResearch/hermes-agent — 会成长的 agent [Python] +38k ★

## 新兴项目

- multica-ai/multica — 开源的 managed agents 平台
  [TypeScript] ★ 17.2k（9 天前创建）
```

语言、语气、章节顺序、过滤条件 —— 首次配置后全部**可通过对话调整**。

## 更多安装方式

根据你使用的 agent 选一种。

### 方式 1：ClawHub（OpenClaw 用户最简）

```bash
openclaw skills install follow-github
```

然后开一个对话，说 "配置 follow-github" —— skill 会带你走完交互式引导。

### 方式 2：Claude Code

```bash
# 用户级（所有项目都能用）
git clone https://github.com/Miraclemin/follow-github ~/.claude/skills/follow-github

# 或 项目级（仅当前项目）
git clone https://github.com/Miraclemin/follow-github .claude/skills/follow-github
```

Claude Code 会自动发现这些目录下的 skill。开一个新会话，说 "配置 follow-github"。

### 方式 3：Codex CLI（或其他 agent）

Codex 没有一级 skill 机制，当成"参考文档 + 可执行脚本"使用：

```bash
git clone https://github.com/Miraclemin/follow-github ~/agents/follow-github
cd ~/agents/follow-github/scripts && npm install
```

然后让你的 agent 读 `SKILL.md`——可以在 `AGENTS.md` / 系统提示里引用它，或者直接说：

```bash
# Codex 里
"读一下 ~/agents/follow-github/SKILL.md 并按照里面的说明执行"
```

### 方式 4：手动（适用任何环境）

```bash
git clone https://github.com/Miraclemin/follow-github
cd follow-github/scripts && npm install
node prepare-digest.js   # 输出原始 JSON（需要先配置）
```

---

## 首次运行

Skill 会引导你走一个 10 步的交互式配置：

| 步骤 | 询问内容 |
|---|---|
| 1 | 介绍（无需输入） |
| 2 | 你的 GitHub 用户名 |
| 3 | 一个 GitHub PAT（有引导） |
| 4 | 要哪些内容流（任意组合） |
| 5 | 语言过滤（如 Python、Rust —— 或不限） |
| 6 | 频率和时间（日/周 + 时区） |
| 7 | 投递方式（OpenClaw 会自动检测） |
| 8 | 摘要语言（中/英/双语） |
| 9 | 自动注册 cron 任务 |
| 10 | 立刻发一份样例摘要让你反馈 |

偏好写入 `~/.follow-github/config.json`；token 存到 `~/.follow-github/.env`
（不会被提交，除了 GitHub API 不发往任何地方）。

### 投递方式

首次配置时也会一起设置投递渠道：

- **OpenClaw**：走 OpenClaw 内建消息通道
- **Telegram**：使用你自己的 bot token 和 chat ID
- **Email**：使用你自己的 Resend API key 和邮箱地址
- **按需获取**：不自动投递，需要时手动让 agent 生成

对 Claude Code、Codex CLI 这类非持久 agent，若想定时收到摘要，推荐配置
Telegram 或 Email。

### Telegram 配置

如果你选 Telegram，agent 应该这样引导用户：

1. 打开 Telegram，搜索 `@BotFather`
2. 发送 `/newbot`
3. 设置 bot 名称和一个以 `bot` 结尾的用户名
4. 复制 BotFather 返回的 token
5. 先和这个 bot 聊天，随便发一条消息
6. 把 token 存到 `~/.follow-github/.env` 的 `TELEGRAM_BOT_TOKEN`
7. 用下面命令取 chat ID：

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result'][0]['message']['chat']['id'])" 2>/dev/null || echo "No messages found — send a message to your bot first"
```

### Email 配置

如果你选 Email，agent 应该这样引导用户：

1. 到 https://resend.com 注册一个免费账号
2. 在 Resend 后台创建 API key
3. 存到 `~/.follow-github/.env` 的 `RESEND_API_KEY`
4. 在 `config.delivery.email` 写入收件邮箱

### GitHub Token 配置

引导会带你走，这里仅供参考：

1. 打开 https://github.com/settings/personal-access-tokens/new（fine-grained token）
2. **Repository access**：Public Repositories (read-only)
3. **Permissions**：`Metadata: Read` 即可（默认勾上）
4. 复制 token（以 `github_pat_` 开头），引导时粘贴

---

## 通过对话定制

配置完成后，直接对话：

| 你说 | 会发生什么 |
|---|---|
| "改成日报" | `config.frequency` → `daily`，cron 重新注册 |
| "只看 Rust" | `config.languages` → `["rust"]` |
| "去掉 trending" | `config.sources.trending` → `false` |
| "摘要短一点" | 编辑 `~/.follow-github/prompts/summarize-*.md` |
| "语气更口语化" | 编辑 `~/.follow-github/prompts/digest-intro.md` |
| "显示我的设置" | 读取并展示 config.json |
| "恢复默认 prompt" | 删除你的自定义 prompt |

你的自定义 prompt 放在 `~/.follow-github/prompts/`，会**覆盖**默认版本 —— skill
升级不会冲掉你的个性化。

---

## 架构

```
GitHub API (实时)              ──┐
github.com/trending 爬虫       ──┼──▶ prepare-digest.js (本地)
GitHub Search API (实时)        ──┘              │
                                                  ▼ JSON blob
                                            LLM (你的 agent)
                                                  │  按 prompts 重整
                                                  ▼
                                        deliver.js ──▶ stdout / Telegram / 邮箱
```

**三级 prompt 优先级**：
1. `~/.follow-github/prompts/*.md` —— 你的定制（最高优先级）
2. `<remoteUrl>/*.md` —— 可选的远端更新（`config.prompts.remoteUrl` 配置）
3. `./prompts/*.md` —— skill 自带默认（兜底）

**去重** 通过 `~/.follow-github/state.json` 实现 —— 每条事件或新仓库在 30 天内只出现一次。

**无中央 feed** —— 和 `follow-builders` 不同，每个用户跑自己的抓取。好处：零基建，
不用维护服务器、GitHub Actions 或 API key 池。

---

## 配置文件格式

```json
{
  "platform": "openclaw",
  "github": { "username": "your-handle" },
  "sources": {
    "following": true,
    "trending": true,
    "hot": true
  },
  "languages": ["python", "typescript"],
  "frequency": "weekly",
  "weeklyDay": "monday",
  "deliveryTime": "09:00",
  "timezone": "Asia/Shanghai",
  "delivery": { "method": "stdout" },
  "digestLanguage": "zh",
  "prompts": { "remoteUrl": null },
  "onboardingComplete": true
}
```

所有字段都可以通过对话修改 —— 你不需要手动改这个文件。

---

## 依赖

- Node.js 18+（使用原生 `fetch`）
- 一个 GitHub PAT（只读公开仓库权限即可）
- 可选：`openclaw` CLI、Claude Code、或任何支持 LLM 的 CLI agent
- 若在 OpenClaw 之外做定时投递：Telegram bot token 或 Resend API key

---

## 许可证

MIT —— 见 [LICENSE](./LICENSE)。

## 隐私

- GitHub token 存在 `~/.follow-github/.env`，不在仓库里
- Telegram / Resend 密钥如果使用，也只存本地 `~/.follow-github/.env`
- 用户偏好和去重状态保存在 `~/.follow-github/`
- 仓库只抓取公开 GitHub 数据，以及你自己的 GitHub API 请求

---

## 相关

- [follow-builders](https://github.com/zarazhangrui/follow-builders) —— 本项目灵感来源，
  追踪 AI builders 的 X 动态和 YouTube 播客
- [ClawHub](https://clawhub.ai) —— OpenClaw 的 skill 注册中心

English: [README.md](./README.md)
