---
name: english-daily
description: "Daily English learning with spaced repetition — built-in A1–B2 word bank, new words daily, quiz mode (MCQ/fill-in/spelling), streak tracking, level progression."
keywords: 学英语, 英语单词, 今日单词, 英语练习, 英语学习, 词汇, 测验, 打卡, 连续学习, 进度, 间隔重复, 每日推送, English learning, vocabulary, daily words, quiz, streak, spaced repetition, English practice, CEFR, word bank
license: MIT-0
compatibility:
  platforms:
    - claude-code
    - claude-ai
    - api
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# English Daily

> 私人英语学习助手 — 每日单词 · SRS复习 · 测验打卡 · 进度追踪

## 何时使用

- 用户说"学英语""英语单词""今日单词""英语练习"
- 用户想背单词、做填空、做选择题
- 用户说"测验""我的进度""连续打卡""学习报告"
- 用户说"开启推送""每天推英语单词"

---

## 核心命令（全部纯计算，无文件写入）

档案与学习进度存于原生 **MEMORY.md**，由 Agent 维护。脚本从参数拿到档案字段（等级/每日目标/SRS进度/streak/积分等），做纯计算并**输出更新后的 MEMORY.md 区块**供 Agent 回写。

```bash
# 注册（首次使用）→ 输出 MEMORY.md 档案区块，由 Agent 写入原生记忆
node scripts/register.js <userId> <姓名> [等级 A1/A2/B1/B2] [每日目标 1-20]

# 今日学习（每日推送内容）→ 更新 streak 后输出新的 MEMORY.md 区块
node scripts/daily-push.js <userId> --level <等级> --goal <目标> \
     --progress '<SRS进度JSON>' --streak <n> --longest <n> --last <日期> --points <n>

# 测验练习（纯计算生成题目）
node scripts/quiz.js <userId> [vocab|sentence|mixed] --level <等级> --progress '<SRS进度JSON>'

# 记录测验积分（Claude 在测验完成后调用）→ 更新积分/SRS后输出新的 MEMORY.md 区块
node scripts/quiz.js <userId> --score <正确题数×10> --level <等级> --progress '<SRS进度JSON>' --points <累计积分>

# 查看进度（升级时输出新的 MEMORY.md 区块）
node scripts/progress.js <userId> --name <姓名> --level <等级> --progress '<SRS进度JSON>' --streak <n> --points <n>

# 推送管理（等级/目标作为参数；cron 由 openclaw 运行时管理）
node scripts/push-toggle.js on <userId> --level <等级> --goal <目标> [--morning 08:00] [--channel telegram]
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

---

## 👤 用户档案与进度 (存于原生 MEMORY.md)

本 skill **不向磁盘写任何用户数据**。用户的等级、每日目标、连续学习(streak)、总积分、以及 SRS 单词进度全部保存在 OpenClaw 原生 **MEMORY.md** 中，由 Agent 读写、跨会话保留。

**流程：**

1. 新用户 → 运行 `register.js`，它输出一段 `<!-- english-daily:profile:<userId> -->` markdown 区块。**把该区块写入 MEMORY.md。**
2. 后续每次学习/测验/看进度 → 先**读取 MEMORY.md** 中该区块，把 等级/每日目标/streak/积分/SRS进度(JSON) 作为参数传给脚本。
3. `daily-push.js`（刷新 streak/上次学习）、`quiz.js --score`（累加积分、更新 SRS）、`progress.js`（升级时）会输出**更新后的区块**——用它覆盖 MEMORY.md 中的旧区块。
4. SRS 进度是一段紧凑 JSON，存在区块的「SRS进度」行；传参时原样作为 `--progress '<JSON>'`，勿手动改写。

档案区块格式示例：

```markdown
<!-- english-daily:profile:telegram_123 -->
## 英语学习档案 · 张三
- userId: telegram_123
- 姓名: 张三
- 母语: zh
- 等级: B1 → 目标: B2
- 每日目标: 5 个新单词
- 连续学习: 7天（最长 12天）
- 上次学习: 2026-07-02
- 总积分: 340
- 已学单词: 28
- 推送: 已开启 telegram 08:00
- SRS进度(勿手改): {"apple":{"interval":7,"repetitions":3,"ease":2.5,"nextReview":"2026-07-09","lastQuality":3}}
<!-- /english-daily:profile -->
```

---

## 学习流程

1. **注册** → `register.js` 输出学习档案区块（等级、每日目标），Agent 写入 MEMORY.md
2. **每日学习** → `daily-push.js` 输出今日复习词 + 新词列表，并回写刷新后的档案区块
3. **测验** → `quiz.js` 生成5题（词义选择或句子填空），Claude 逐题互动
4. **记分** → 测验完成后 Claude 调用 `--score`，脚本更新积分/SRS并输出新区块供回写
5. **进度** → `progress.js` 显示连续打卡、掌握词数、升级进度；升级时输出新区块

> 每一步的档案字段都从 MEMORY.md 读出后作为 CLI 参数传入；脚本本身不落盘。

---

## 推送设置

```bash
node scripts/push-toggle.js on <userId> --level B1 --goal 5              # 默认 08:00
node scripts/push-toggle.js on <userId> --level B1 --goal 5 --morning 07:30 --channel feishu
node scripts/push-toggle.js off <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`

推送触发时，cron 消息会让 Agent 先从 MEMORY.md 读出该用户的 SRS 进度与 streak，再运行 `daily-push.js`（等级/每日目标已烘焙进 cron 消息），最后回写刷新后的档案区块。cron 由 openclaw 运行时通过 `__OPENCLAW_CRON_ADD__`/`__OPENCLAW_CRON_RM__` 协议管理，skill 不落盘。

---

## 等级体系

| 等级 | 词汇量 | 升级条件（掌握词数） |
|------|--------|---------------------|
| A1   | ~40词  | 掌握40词 → 升A2      |
| A2   | ~50词  | 掌握90词 → 升B1      |
| B1   | ~40词  | 掌握130词 → 升B2     |
| B2   | ~30词  | 最高等级              |

掌握标准：SRS间隔 ≥ 7天（即多次正确复习）

---

## SRS算法说明

采用简化SM-2间隔重复：
- 质量1（遗忘）/ 质量2（困难）→ 明天复习
- 质量3（掌握）→ 间隔 × 1.5
- 质量4（轻松）→ 间隔 × 2.0
- 最大间隔30天

---

## 🔐 数据与隐私 (Data & Privacy)

- **无文件写入**：所有脚本均为纯计算（生成学习内容/测验题/推送 prompt、更新 streak 与 SRS），**不向磁盘写入任何用户数据**，符合 clawhub 无 `fs` 写入规范。`data/users/*.json` 已列入 `.clawhubignore`，不随 skill 打包。
- **原生记忆**：用户的等级、每日目标、连续学习、积分、SRS 单词进度全部保存在 OpenClaw 原生 `MEMORY.md`，由你本机的 Agent 管理，不经过任何外部服务。
- **删除档案**：删除 MEMORY.md 中对应的 `<!-- english-daily:profile:<userId> -->` 区块即清除该用户的全部学习数据。
- **推送隔离**：`telegram`/`feishu`/`slack`/`discord` 由 openclaw 运行时投递，skill 不调用任何渠道 API、不持有 token。

## 注意事项

- 内置单词库（A1-B2共约160词），`data/wordbank.json`（只读，随 skill 打包）
- 所有脚本仅使用 Node.js 内置模块（path 等），无需 npm install
- 用户ID仅允许字母、数字、连字符、下划线（防路径穿越）
- 用户学习数据为本地敏感数据，请勿随 skill 一并打包或公开分享

---

*Version: 1.1.0 · Updated: 2026-07-02*
