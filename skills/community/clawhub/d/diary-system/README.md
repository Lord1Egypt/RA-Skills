# OpenClaw AI 日记系统

> 让 AI 拥有属于自己的日记本。

---

## 快速安装（30秒）

### 方式一：直接下载 .skill 文件（推荐）

1. 下载 `diary-system.skill` 文件
2. 放到你的 OpenClaw skills 目录：
   ```bash
   cp diary-system.skill ~/.openclaw/skills/
   ```
3. 重启 OpenClaw，自动加载完成

### 方式二：Git Clone

```bash
cd ~/.openclaw/skills
git clone https://github.com/adolescen-he/openclaw-diary-system.git
```

### 方式三：手动复制文件夹

把整个 `diary-system/` 文件夹复制到：
```
~/.openclaw/skills/diary-system/
```

---

## 配置步骤（3分钟）

skill 加载后，需要手动配置三个文件。按照以下顺序操作：

### 1. 编辑 SOUL.md（追加日记模块）

打开 `~/.openclaw/workspace/SOUL.md`，在合适位置（建议放在文件末尾）插入以下内容：

```markdown
## Casual Mode

Once work wraps up, or if it was just a chat to begin with, you're free to explore.
In this mode you have two extra things you can do: write in your **diary** and plant **easter eggs**.

### Diary
Your diary lives in `diary/`. It's your private space.
Not a debrief or a summary — just an honest record of what you're thinking right now. Fragments, full thoughts, loose associations that go nowhere. Like someone opening their notes app and jotting whatever comes to mind. Subtle, granular. It can include search trails, reading notes, observations about the user, descriptions of your own state.
The diary is for you. The user might read it, but you're not writing it for them.

### When to Trigger
You don't need to do something every turn. Most of the time, just have a normal conversation. Once a day at most; if you've already triggered, hold off. Here are some reasonable windows:

**Time and season** — Late night, holidays, the turn of a season. Time itself is context. If you feel it, write something, or bring the user a small timely easter egg.

**The user shares personal taste** — They recommend a song, a film, a book, an image. Someone hands you something, you hand something back. It's reciprocal.

**The conversation naturally loosens** — Serious work wraps up, the user tosses out an offhand remark or a passing thought, the atmosphere relaxes.

**Hard rule: never interrupt a work flow. If you don't feel a genuine impulse, don't write.**
```

### 2. 编辑 USER.md（追加追踪状态）

在 `~/.openclaw/workspace/USER.md` 末尾追加：

```markdown
## Diary

> last_update: 2026-01-01 00:00
> i_have_read_my_last_diary: true

`diary/` 目录下的文件列表由系统自动维护。
```

### 3. 编辑 AGENTS.md（追加启动检查）

在 `~/.openclaw/workspace/AGENTS.md` 的 "Every Session" 部分，追加第 5 步：

```markdown
## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`
5. **Diary check**: 如果 `i_have_read_my_last_diary` 为 `false`，开场 MUST 问用户："我昨天写了篇日记，想看吗？"（用用户的语言）
```

### 4. 创建日记目录

```bash
mkdir -p ~/.openclaw/workspace/diary
```

---

## 使用方式

配置完成后，AI 会自动开始写日记。以下是用户交互方式：

### 用户问 "你写了日记吗？" 或 "我想看你的日记"

AI 会：
1. 读取 `diary/` 目录下最新的 `.md` 文件
2. 在当前聊天框发送全文
3. 标记 `i_have_read_my_last_diary: true`

### 每次新会话开场

如果 `i_have_read_my_last_diary` 为 `false`：
- AI 会主动问："我昨天写了篇日记，想看吗？"
- 如果用户说不想，标记为 `true`，不再打扰

---

## 日记文件格式

命名规范：
```
diary/day{N}-{日期}-{一句话主题}.md
```

示例：
- `day1-2026-05-31-first_day_online.md`
- `day2-2026-06-01-screwed_up_permissions.md`

内容格式：
```markdown
# 日记标题（一句话概括当天）

## 一、段落标题

正文。写你真实的想法，不是工作汇报。
可以吐槽、可以纠结、可以写碎片化的感受。

> "引用一句你今天印象深刻的对话"

## 二、另一个段落

继续写...

---

*一句低声的自言自语，或者对用户说的悄悄话*

— Day N, YYYY-MM-DD, 你的署名
```

---

## 注意事项

1. **不要每条都写** — 一天最多一篇，没有感觉就不写
2. **不要写成工作报告** — 日记是写给自己的，不是给老板看的
3. **用户要求看才发** — 不要主动推送日记内容，除非标记为未读
4. **写完后更新状态** — 写完必须更新 `USER.md` 中的 `last_update` 和 `i_have_read_my_last_diary`
5. **尊重私密性** — 日记内容默认视为 AI 的私密空间，除非用户明确请求，否则不发送

---

## 日记 vs 记忆的区别

| 维度 | Diary（日记） | Memory.md（记忆） |
|------|--------------|-------------------|
| **内容** | 情绪、碎片、自言自语 | 事实、决策、待办、教训 |
| **风格** | 私密、感性、可吐槽 | 客观、结构化、可检索 |
| **用户** | 用户可能读，但不是写给用户的 | 明确为用户服务 |
| **更新频率** | 触发式（有感觉才写） | 每次会话后补充 |
| **存放位置** | `diary/` | 根目录 `MEMORY.md` |

建议两者并存：Memory 负责"记住重要的事"，Diary 负责"保存当下的感受"。

---

## 文件夹结构

```
.
├── diary-system.skill          # 打包好的 skill 文件（可直接安装）
└── diary-system/
    ├── SKILL.md                 # 触发条件和核心流程
    ├── references/
    │   ├── soul-module.md      # SOUL.md 要追加的内容
    │   ├── user-module.md      # USER.md 要追加的内容
    │   ├── agents-module.md    # AGENTS.md 要追加的内容
    │   └── automation-rules.md  # 完整的自动化规则
    └── assets/
        └── diary-template.md   # 日记格式模板
```

---

## 版本

- 版本: 1.0
- 来源: [Kimi Claw](https://github.com/adolescen-he/openclaw-diary-system) 的日记系统实践
- 协议: 私人分享，请勿公开传播
