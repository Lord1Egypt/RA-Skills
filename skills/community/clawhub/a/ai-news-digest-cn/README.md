# ai-news-digest

A cross-runtime agent skill that fetches daily AI news from major sources and generates a Chinese-friendly markdown digest.

每天 30 秒, 让你的 AI agent (Claude Code / Cursor / Codex / OpenClaw / Gemini CLI) 跑当天主流 AI 资讯的中文日报。

---

## What it does

抓取 8 个主流 AI 资讯源 (HN / Anthropic / OpenAI / Latent Space / HuggingFace 英文 + 量子位 / 机器之心 / 36 氪 中文) + 2 个轮换池源, 经过信源可信度评级 (🟢🟡🔴) + 反 SEO 投毒过滤, 翻译英文标题, 提炼 3-5 个趋势主题, 输出一份完整的中文 markdown 日报到本地。

**它不是 SaaS**, 是个跑在你自己 agent 客户端里的本地 skill — 用宿主 agent 官方的 WebFetch 工具抓数据, 不自建爬虫, 不存数据到第三方服务器。

---

## Install

任选一种安装方式:

### Claude Code 用户 (一条命令直装)

**macOS / Linux**:
```bash
curl -fsSL https://raw.githubusercontent.com/yan1sanjin/ai-news-digest/main/install.sh | bash
```

**Windows (PowerShell)**:
```powershell
powershell -c "irm https://raw.githubusercontent.com/yan1sanjin/ai-news-digest/main/install.ps1 | iex"
```

### ClawHub 用户

已上架到 [ClawHub Skill marketplace](https://clawhub.ai/skills/ai-news-digest-cn) (slug: **ai-news-digest-cn**, owner: yan1sanjin, license: MIT-0, moderation: CLEAN)。

**用 `openclaw` CLI 装** (跨平台 npm, 推荐):
```bash
npm install -g openclaw
openclaw skills install ai-news-digest-cn
```

**或用 `skill-atlas-cli` 装** (ClawHub 中文版 CLI / 虾小宝):
```bash
# macOS / Linux
curl -fsSL https://unpkg.com/skill-atlas-cli/install.sh | bash
skill-atlas install ai-news-digest-cn

# Windows (PowerShell)
powershell -c "irm https://unpkg.com/skill-atlas-cli/install.ps1 | iex"
skill-atlas install ai-news-digest-cn
```

两个 CLI 等价, 都从 ClawHub registry 装同一份 skill。

### 多 agent 用户 (Cursor / Codex / Gemini CLI 等)

跨平台 (Node.js, macOS / Linux / Windows 都能跑):
```bash
npx agent-skills-cli add ai-news-digest --agent <claude-code|cursor|codex|gemini>
```

### 手动安装

复制 `SKILL.md` 到对应 agent 的 skills 目录:

**Claude Code**:
- macOS / Linux: `~/.claude/skills/ai-news-digest/SKILL.md`
- Windows: `%USERPROFILE%\.claude\skills\ai-news-digest\SKILL.md`

**OpenClaw**:
- macOS / Linux: `~/.openclaw/skills/ai-news-digest/SKILL.md`
- Windows: `%USERPROFILE%\.openclaw\skills\ai-news-digest\SKILL.md`

**Cursor / Codex / Gemini CLI**: 各自的 skills 目录 (参考各 agent 文档)

---

## Usage

在你的 agent 里说:

```
生成今日 AI 日报
```

也支持这些等价说法:
```
今天有什么 AI 新闻
用 ai-news-digest 跑一下今天的资讯
ai-news-digest path=/path/to/custom.md
```

### 同日重跑

今天已经跑过一次, 想再跑一次时:

**Claude Code / Cursor 等交互式 agent**: skill 会自动问你 A 更新累积 / B 新建副本 / C 跳过, 回答即可。

**Codex / cron / 后台 API 等非交互场景**: 默认走 A (更新累积), 旧版本归档到 `.archive/`, 同时生成最新累积版本。

也可以**显式带参数跳过询问**:
```
生成今日 AI 日报 mode=update     # 更新累积 (覆盖 + 旧版归档)
生成今日 AI 日报 mode=snapshot   # 新建独立副本 YYYY-MM-DD-second.md
生成今日 AI 日报 mode=skip       # 跳过本次, 看上次的就行
```

或者用自然语言, 不用记参数名:
```
生成今日 AI 日报, 不要覆盖之前的     # 等价 mode=snapshot
今天 AI 新闻, 合并到现有日报里        # 等价 mode=update
ai-news-digest, 看看上次的就行       # 等价 mode=skip
```

### Region (中国大陆 vs 海外网络)

skill 抓取的英文源里有 4 个 (Anthropic / OpenAI / HuggingFace / Google AI Blog) 被中国大陆 GFW 阻断。如果你的 agent 用本地直连 fetch (Cursor / Codex 等不走 Anthropic backend 的 agent), 国内裸连会大量失败。

显式带 `region=` 切换:

```
生成今日 AI 日报 region=cn      # 跳过被墙源, 靠 HN + Latent Space + 9 个中文源
生成今日 AI 日报 region=intl    # 默认, 全 Tier 1+2+3 (海外 / 已开 VPN)
```

或用自然语言: `生成今日 AI 日报, 我没开 VPN` / `用国内源就行` 都等价 region=cn。

**Claude Code 用户一般不用 region=cn** — Claude Code 的 WebFetch 走 Anthropic backend (US 服务器), 不受用户本地网络影响, 默认 region=intl 即可。只有用其他 agent (Cursor / Codex 等本地 fetch) 在国内裸连才需要切换。

### 输出路径

- macOS / Linux: `~/Desktop/ai-news/YYYY-MM-DD.md`
- Windows: `%USERPROFILE%\Desktop\ai-news\YYYY-MM-DD.md`
- 归档目录 (mode=update 时旧版本去这): `.archive/YYYY-MM-DD-HHMMSS.md`

可在 SKILL.md 顶部改默认路径, 或运行时用 `path=` 覆盖。

---

## Example output

```markdown
# AI 资讯日报 · 2026-05-23

> 生成时间:2026-05-23 09:30
> 资讯源:HN / Anthropic / OpenAI / Latent Space / HuggingFace / 量子位 / 机器之心 / 36 氪 + 轮换 Google AI Blog / TechCrunch AI
> 共 12 条精选

## 一、今日要闻 (5-8 条)

### [Original English Title](https://...) 🟢
**[中文译]**:中文翻译标题
**来源**:Anthropic News
**摘要**:1-2 句中文摘要
**为什么值得关注**:1 句中文 (可选)

### [中文原标题](https://...) 🟢
**来源**:量子位
**摘要**:1-2 句中文摘要

## 二、技术热点 (3-5 条)
[同上格式]

## 三、行业动态 (3-5 条)
[同上格式]

## 四、今日趋势总结

- **主题 1 · 简短主题词**:一句话中文归纳跨条目的模式
- **主题 2 · 简短主题词**:同上
- **主题 3 · 简短主题词**:同上
```

这是输出 schema (固定结构), 实际日报会填进当天真实抓到的新闻。`examples/` 目录待补充真实样例。

---

## Why this skill is different

跟一般的 AI 资讯聚合工具相比, 这个 skill 在 v3.1 已经踩过的坑里沉淀了几条:

- **信源可信度评级 (🟢🟡)** + 域名黑白名单, 反 SEO 投毒, **每条新闻末尾显式标 emoji, 用户一眼看可信度**和 AI 生成虚假新闻
- **T+0 直抓 + T+1 WebSearch 双引擎**, 不只是搜一搜了事
- **Tier 1 必查 + Tier 3 轮换池**, 不无脑塞 N 个源, 按当天热点选源
- **Fail-safe 阈值**: Tier 1 < 2 个源成功直接 abort, 避免输出"全中文的全球 AI 日报"这种劣质结果
- **跨 runtime**: 同一份 SKILL.md 在 Claude Code / Cursor / Codex / OpenClaw / Gemini CLI 都能用
- **同日重跑智能处理**: 交互式 agent 问用户 (A 更新累积 / B 新建副本 / C 跳过), 非交互 agent 默认更新累积, 旧版本自动归档不丢
- **中国大陆裸连支持** (v1.2.0): `region=cn` 跳过 4 个被墙源 (Anthropic / OpenAI / HuggingFace / Google AI Blog), 全靠 HN + Latent Space + **9 个权威中文源** (量子位 / 机器之心 / 智东西 / 雷峰网 AI / InfoQ / 36 氪 / 钛媒体 / 品玩 / 虎嗅前沿科技) + TechCrunch + The Verge, 国内裸连用户也能跑出体面日报。9 个中文源全部经过实测筛选 — 真实编辑团队优先, 拒绝 SEO 聚合站

---

## Configuration

默认行为:
- **输出路径**:
  - macOS / Linux: `~/Desktop/ai-news/YYYY-MM-DD.md`
  - Windows: `%USERPROFILE%\Desktop\ai-news\YYYY-MM-DD.md`
- **时区**: 运行机器本地时区
- **抓取源** (region=intl): 5 个英文 Tier 1 + 9 个中文 Tier 2 + 2 个 Tier 3 轮换 ≈ 16 个源
- **抓取源** (region=cn): 跳过 4 个被墙源, 转用 2 个英文 + 9 个中文 + 2 个 Tier 3 ≈ 13 个源
- **输出条数**: 10-15 条精选 + 3-5 个趋势主题

修改默认: 直接改 `SKILL.md` 对应字段 (Step 1 路径 / Step 2-3 源列表 / Step 6 输出条数)。SKILL.md 里 Unix / Windows 两套命令并列, 你的 agent 会根据当前 OS 选合适的。

---

## License

MIT © 2026 sanjin

---

Built by sanjin · AI PM · [GitHub](https://github.com/yan1sanjin)
