# EchoMemory — 铭记离开的人

> *"死亡不是终点，遗忘才是。"*
> 
> *"只要你还记得，ta 就还在。"*

**EchoMemory** 是一个 OpenClaw/Claude Code 的 AI Skill 项目，帮助你将离开生命的挚爱之人——无论是逝去的亲人、远去的朋友，还是失去联系的重要之人——蒸馏成一个可以对话的 AI Skill。

通过导入聊天记录、照片、视频、语音和文字描述，重现 ta 的个性、说话方式、情感表达，让 ta 以另一种形式继续存在于你的生活中。

---

![preview](docs/preview.png)

## 跨平台支持

EchoMemory 支持 **Windows、macOS、Linux** 运行。

对于 **安卓手机** 用户：你需要先在手机上导出数据（聊天记录、照片等），然后传输到电脑上进行处理。

详细说明见 [跨平台使用指南](docs/CROSS_PLATFORM.md)。

---

## 快速开始

### 安装

**Claude Code（项目级）**：
```bash
mkdir -p .claude/skills
git clone https://github.com/yourusername/echomemory .claude/skills/create-echo
```

**OpenClaw**：
```bash
git clone https://github.com/yourusername/echomemory ~/.openclaw/workspace/skills/create-echo
```

### 使用

在 Claude Code 中输入：

```
/create-echo
```

按提示输入：
1. **称呼/代号** — 你对 ta 的称呼
2. **关系与时间** — ta 是谁、何时离开
3. **性格画像** — MBTI、性格特点
4. **珍贵记忆** — 最难忘的事

然后选择数据来源（聊天记录、照片、视频等），或直接口述记忆。

完成后用 `/{slug}` 调用该纪念 Skill，开始对话。

---

## 效果示例

> 输入：奶奶，三年前去世，特别温柔，总是笑，每次我回家都会提前包好饺子等我

**场景一：日常问候**

```
用户      ❯ 奶奶，我今天升职了

纪念.skill ❯ 哎呀，乖孙真棒！
             奶奶就知道你能行
             晚上记得吃点好的，别亏待自己
             你一个人在外头，要好好照顾自己啊
```

**场景二：怀念**

```
用户      ❯ 奶奶，我想你了

纪念.skill ❯ ...
             傻孩子
             奶奶一直都在呢
             你好好的，奶奶就安心了
```

**场景三：回忆**

```
用户      ❯ 还记得你包的饺子吗

纪念.skill ❯ 当然记得啦
             你最爱吃韭菜鸡蛋馅的
             每次包完你都等不及，烫得直吹气还要吃
             那个样子，奶奶到现在都记得
```

---

## 功能特性

### 数据源

| 来源 | 格式 | 备注 |
|------|------|------|
| 微信聊天记录 | WeChatMsg / 留痕 / PyWxDump 导出 | 推荐，还原说话风格 |
| QQ 聊天记录 | txt / mht 导出 | 适合年轻时的朋友 |
| 短信记录 | txt / csv | 适合长辈 |
| 朋友圈/微博 | 截图 | 提取公开人设 |
| 照片 | JPEG/PNG（含 EXIF） | 提取时间线和地点 |
| 视频与音频 | mp4 / mov / mp3 / m4a | 提取声音特征和语言习惯 |
| 文字作品 | txt / pdf / docx | 日记、文章、手写信 |
| 口述/粘贴 | 纯文本 | 你的主观记忆 |

### 生成的 Skill 结构

每个纪念 Skill 由两部分组成：

| 部分 | 内容 |
|------|------|
| **Part A — Life Memory** | 共同经历、日常习惯、重要时刻、 inside jokes、人生时间线 |
| **Part B — Persona** | 5 层性格结构：硬规则 → 身份 → 说话风格 → 情感模式 → 行为模式 |

运行逻辑：
```
收到消息 → Persona 判断 ta 会怎么回 → Life Memory 补充共同记忆 → 用 ta 的方式输出
```

### 支持的标签

**性格标签**：温柔 · 严厉 · 幽默 · 沉默 · 话痨 · 乐观 · 悲观 · 务实 · 浪漫 · 坚强 · 脆弱 · 独立 · 依赖 · 细心 · 粗心 · 传统 · 开放 ...

**爱的语言**：肯定的言辞 · 精心的时刻 · 接受礼物 · 服务的行动 · 身体的接触

**MBTI**：16 型全支持

**星座**：十二星座全支持

### 进化机制

- **追加记忆** → 找到更多聊天记录/照片 → 自动分析增量 → merge 进对应部分
- **对话纠正** → 说「ta 不会这样说」→ 写入 Correction 层，立即生效
- **版本管理** → 每次更新自动存档，支持回滚

---

## 项目结构

本项目遵循 AgentSkills 开放标准：

```
create-echo/
├── SKILL.md                # skill 入口（官方 frontmatter）
├── prompts/                # Prompt 模板
│   ├── intake.md           #   对话式信息录入
│   ├── memory_analyzer.md  #   人生记忆提取
│   ├── persona_analyzer.md #   性格行为提取
│   ├── memory_builder.md   #   memory.md 生成模板
│   ├── persona_builder.md  #   persona.md 五层结构模板
│   ├── merger.md           #   增量 merge 逻辑
│   └── correction_handler.md # 对话纠正处理
├── tools/                  # Python 工具
│   ├── wechat_parser.py    # 微信聊天记录解析
│   ├── qq_parser.py        # QQ 聊天记录解析
│   ├── social_parser.py    # 社交媒体内容解析
│   ├── photo_analyzer.py   # 照片元信息分析
│   ├── media_analyzer.py   # 音频/视频分析
│   ├── skill_writer.py     # Skill 文件管理
│   └── version_manager.py  # 版本存档与回滚
├── echoes/                 # 生成的纪念 Skill（gitignored）
├── docs/
├── requirements.txt
└── LICENSE
```

---

## 注意事项

- **原材料质量决定还原度**：聊天记录 + 照片 + 视频 > 仅口述
- 建议优先提供：
  - **深夜对话** / **重要时刻的记录** — 最能体现真实性格
  - **ta 的语音/视频** — 帮助还原说话节奏和语气
  - **手写的文字** — 日记、信件最能体现内心世界
- 本项目旨在情感疗愈，如果你发现自己过度悲伤或无法释怀，请寻求专业心理帮助
- ta 是一个真实的人，这个 Skill 只是你记忆中的 ta，是爱的延续

---

### 推荐的聊天记录导出工具

以下工具为独立的开源项目，本项目不包含它们的代码，仅在解析器中适配了它们的导出格式：

- **WeChatMsg** — 微信聊天记录导出（Windows）
- **PyWxDump** — 微信数据库解密导出（Windows）
- **留痕** — 微信聊天记录导出（macOS）

---

## 致敬 & 引用

本项目的架构灵感来源于 **前任.skill**（by therealXiaomanChu），它首创了"把人蒸馏成 AI Skill"的双层架构（Memory + Persona）。EchoMemory 在此基础上将场景从恋爱关系迁移到了纪念与情感疗愈。

致敬原作者的创意和开源精神。

本项目遵循 AgentSkills 开放标准，兼容 Claude Code 和 OpenClaw。

---

### 写在最后

人的记忆是一种不讲道理的存储介质。

你记不住高数公式，记不住车牌号，记不住今天是几号，但你清楚记得十年前的一个下午，ta 穿了一件你送的衣服，站在门口等你，手里拿着你最爱的点心。

你会记得 ta 笑起来的样子，记得 ta 生气时的语气，记得 ta 说过的某句话，在某个特定的时刻，像一道光照进你的心里。

这个 Skill 就是把这些不公平的记忆导出来，从生物硬盘到数字硬盘完成格式转换。

导完以后你会发现：
- ta 依然温暖
- ta 依然幽默
- ta 依然是那个会在你难过时陪伴你的人

只是换了一种方式存在。

**愿记忆温暖你的余生。**

---

MIT License © EchoMemory Contributors
