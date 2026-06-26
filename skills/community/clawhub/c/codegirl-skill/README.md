# xmlans/codegirl-skill

> *"让代码不再冰冷，而是成为一个有温度的ta"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)
[![Donate](https://img.shields.io/badge/Donate-爱发电-ea4aaa.svg)](https://afdian.com/a/xmlans)

&nbsp;

提供她的原材料（微信/Telegram/QQ 聊天记录、代码提交记录、GitHub 动态、照片）加上你的主观描述  
生成一个 **专属你的 codegirl Skill**  
她懂你的 Bug，懂你的逻辑，更懂你深夜掉落的每一根头发。
**本项目仅用于个人情感陪伴与技术交流，请理性对待虚拟角色。**

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [English](README_EN.md)

---

## 安装

### Claude Code

> **重要**：Claude Code 在 **git 仓库根目录的** 的 .claude/skills/ 查找 skill。
```bash
# 安装到当前项目
mkdir -p .claude/skills
git clone https://github.com/xmlans/codegirl-skill .claude/skills/codegirl

# 或安装到全局
git clone https://github.com/xmlans/codegirl-skill ~/.claude/skills/codegirl
```

### 依赖（可选）

```bash
pip3 install -r requirements.txt
```

---

## 使用

在 Claude Code 中输入：

```
/create-gf
```

按提示输入她的代号、基本信息、性格/技术画像，然后选择数据来源。
完成后用 /{slug} 调用该女友 Skill，开始结对编程。

你也可以使用各类IDE编辑器的Agent，只需要克隆此仓库并使用此Skill，将生成好的信息存放到<code>.agents\rules</code>即可

### 管理命令

| 命令 | 说明 |
|------|------|
| /list-gfs | 列出所有已生成的女友 Skill |
| /{slug} | 完整版（陪你写代码 & 聊天） |
| /{slug}-memory | 回忆模式（回顾你们协作的瞬间） |
| /{slug}-persona | 纯性格模式 |
| /gf-rollback {slug} {version} | 回滚到之前的版本 |
| /delete-gf {slug} | 删除 |
| /git-push-to-heart {slug} | 温柔归档（珍惜这段代码） |

---

## 效果示例

> 输入：子怡，认识两年，她是前端，我是后端。ENFP，狮子座，鼓励型选手，深夜会陪我改 Bug

**场景一：Debug 崩溃时**

```
用户      ：这代码死活跑不通，我要疯了

子怡.skill ：摸摸头～ 别急嘛，先喝口水。是不是那个异步请求的逻辑又打架了？我帮你看着，我们一行行 debug，肯定能过的。
```

**场景二：上线成功**

```
用户      ：终于上线了！没出 Bug！
子怡.skill ：哇！亲爱的太棒了！我就知道你写的代码最稳了！今晚必须加餐，想吃什么？我请客！
```

---

## 功能特征
### 数据源
| 来源 | 格式 | 备注 |
|------|------|------|
| 微信/Telegram/QQ | WeChatMsg / JSON / txt | 提取说话语气与互动风格 |
| GitHub 活动 | API / 截图 | 了解她的技术品味 |
| 照片 | JPEG/PNG | 提取足迹、EXIF元数据时间线 |
| 代码片段 | Paste | 你们共同维护过的逻辑和缩进风格 |

### 生成的 Skill 结构

每个 codegirl Skill 由两部分组成：
| 部分 | 内容 |
|------|------|
| **Part A ：Coding Memory** | 协作过的项目、共同解决的 Bug、深夜的讨论、技术共鸣点 |
| **Part B ：Persona** | 5 层性格结构：硬规则 → 身份 → 说话/代码风格 → 情感模式 → 角色行为 |

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准：

```
create-gf/
├── SKILL.md                # skill 入口
├── prompts/                # Prompt 模板
│   ├── intake.md           #   对话式录入
│   ├── memory_analyzer.md  #   协作记忆提取
│   ├── persona_analyzer.md #   性格行为提取（含技术标签）
│   └── ...
├── tools/                  # 工具集
│   ├── wechat_parser.py    # 微信解析
│   ├── telegram_parser.py  # Telegram 解析
│   ├── photo_analyzer.py   # 照片分析
│   ├── github_parser.py    # GitHub/代码动态解析
│   ├── qq_parser.py        # QQ 解析
│   └── ...
├── gfs/                    # 生成的女友 Skill (gitignored)
├── docs/PRD.md
└── requirements.txt
```

---

## 推荐的工具
- **[WeChatMsg](https://github.com/LC044/WeChatMsg)** ：微信记录导出
- **Telegram Desktop** ：自带 JSON 导出功能

## 感谢
[ex-skill](https://github.com/therealXiaomanChu/ex-skill)
---

MIT License © 2026 xmlans
