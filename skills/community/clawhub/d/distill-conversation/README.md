# Alembic — 对话蒸馏器

[![EN](https://img.shields.io/badge/lang-English-blue.svg)](./README.en.md)
[![CN](https://img.shields.io/badge/lang-中文-red.svg)](./README.md)

> **把你和 AI 的对话，炼成可以反复回看的知识笔记。**

你和 ChatGPT 聊了两小时，搞懂了一个概念。三天后，你只记得「好像聊过」。

Alembic 解决的就是这个问题：它从你的 **大模型对话** 中，自动提取关键词、过滤噪声、按第一性原理重组，输出一篇**结构化的知识笔记**——不是对话摘要，而是你日后回看就能秒懂的「知识结晶」。

> **许可（License）**
> 本仓库代码以 **MIT License** 发布。详见 [LICENSE](./LICENSE) 文件。

---

## 它做了什么

```
                    ┌─────────────┐
  ChatGPT 链接 ──→  │             │  ──→  关键词1.md（结构化知识笔记）
  或粘贴文本   ──→  │   Alembic   │  ──→  关键词2.md（结构化知识笔记）
  + 可选关键词 ──→  │             │  ──→  ...
                    └─────────────┘
```

1. **自动解析** ChatGPT 共享链接（逆向 React Server Component 序列化格式）
2. **提取关键词** — 对话中认知增量最大的概念（≤ 3 个，尽可能少）
3. **蒸馏知识** — 第一性原理导向、问题驱动、取精华去糟粕
4. **输出笔记** — 干净的 Markdown，可直接存入 Obsidian vault 或任意目录

---

## 快速开始

### 安装

```bash
# 方式一：直接复制
cp -r distill-conversation ~/.claude/skills/distill-conversation

# 方式二：克隆 + 软链接
git clone https://github.com/yaoyuyang/distill-conversation.git
ln -s $(pwd)/distill-conversation ~/.claude/skills/distill-conversation
```

### 依赖

| 依赖 | 说明 |
|------|------|
| **Claude Code** | 需支持 skills 功能 |
| **Python 3.6+** | 仅标准库，零额外依赖 |

> **不需要 curl**。v0.3.0 起已改用 Python 标准库 `urllib.request` 进行网络请求。

### 环境变量（可选）

| 变量 | 说明 |
|------|------|
| `OBSIDIAN_VAULT_PATH` | Obsidian vault 路径。设置后，笔记默认输出到 `$OBSIDIAN_VAULT_PATH/00.Inbox/`。未设置时输出到当前工作目录。 |

---

## 使用方法

在 Claude Code 中：

```bash
# 从 ChatGPT 共享链接蒸馏（自动提取关键词）
/distill-conversation https://chatgpt.com/share/xxxxx

# 指定关键词（只整理你关心的部分）
/distill-conversation https://chatgpt.com/share/xxxxx 哈希值

# 指定输出目录
/distill-conversation https://chatgpt.com/share/xxxxx --output-dir ~/notes/inbox

# 直接粘贴对话文本
/distill-conversation
（然后粘贴对话内容）
```

### 输出目录优先级

1. `--output-dir` 参数（最高优先）
2. `$OBSIDIAN_VAULT_PATH/00.Inbox/`（环境变量已设置时）
3. 当前工作目录（最终回退）

### Obsidian 用户推荐用法

```bash
# 设置 vault 路径（加到 shell profile 中）
export OBSIDIAN_VAULT_PATH="$HOME/ObsidianVault"

# 之后直接使用，笔记自动进入 Inbox
/distill-conversation https://chatgpt.com/share/xxxxx
```

---

## 蒸馏原则

| 原则 | 说明 |
|------|------|
| **第一性原理** | 从「它本质是什么 / 为什么存在」出发，不罗列结论 |
| **问题驱动** | 每篇笔记回答一个核心问题 |
| **取精华去糟粕** | 保留洞见和正确结论，丢弃试探、跑题、寒暄 |
| **融合你的思考** | 保留你的追问逻辑和理解路径 |
| **结构化** | 是什么 → 为什么 → 怎么理解 → 关键细节 |

---

## 输出笔记结构

```markdown
---
tags: [领域, 子分类, 对话蒸馏]
created: 2026-04-05
source: https://chatgpt.com/share/xxxxx
---
# 关键词标题
> 核心问题：一句话概括这篇笔记要回答什么

## 本质定义        ← 一句话定义 + 直觉理解
## 为什么重要      ← 它解决了什么根本问题
## 核心机制        ← 笔记主体（灵活组织）
## 关键细节        ← 边界条件、常见误区、实用技巧
## 我的理解路径    ← 你在对话中的思维转折
## 相关概念        ← Wiki-links
## 参考来源        ← 对话链接 + 外部资料
```

---

## 实际案例

### 输入

```
/distill-conversation https://chatgpt.com/share/69d11ccd-4a20-8330-adb9-2a39f1dbfbc9
```

一段 4 轮、约 8000 字的对话，用户问了「Rust 和 C++ 在量化研究中的区别」。

### Alembic 自动识别

- **关键词**：`量化场景下的语言选型(Rust vs C++ vs Python)`（1 个，整段对话围绕同一主题）
- **冲突检查**：vault 中无同名笔记

### 输出（节选）

> 完整文件见 [`examples/量化场景下的语言选型(Rust vs C++ vs Python).md`](./examples/量化场景下的语言选型(Rust%20vs%20C++%20vs%20Python).md)

8000 字的原始对话 → 一篇约 1500 字的结构化笔记。噪声被过滤了 80%+，核心洞见全部保留。

---

## 安全说明

- **域名白名单**：解析器只允许访问 `chatgpt.com` 和 `chat.openai.com` 的共享链接，其他 URL 在请求前即被拒绝
- **无第三方传输**：所有处理在本地完成，不会将数据发送到任何第三方服务器
- **纯标准库**：网络请求使用 Python `urllib.request`，无 subprocess 调用，无 `shell=True`
- **仅写指定目录**：笔记只写入用户指定的输出目录
- **离线模式**：不希望联网时，可以直接粘贴对话文本（模式 B），或使用 `--html` 参数传入本地 HTML 文件

---

## 常见问题排查

| 问题 | 排查建议 |
|------|----------|
| 解析返回 0 条消息 | ChatGPT 前端格式可能已更新，解析器会输出警告信息。检查链接是否为有效的公开共享链接。 |
| "不支持的 URL 格式" | 确认 URL 格式为 `https://chatgpt.com/share/<uuid>`。不支持对话主页面链接。 |
| "下载的页面内容过短" | 链接可能已失效或被取消共享。尝试在浏览器中打开确认。 |
| 未找到 `OBSIDIAN_VAULT_PATH` | 使用 `--output-dir` 显式指定输出目录，或在 shell profile 中设置该环境变量。 |
| 网络超时 | 检查网络连接，或改用模式 B（粘贴文本）/ 本地 HTML。 |

---

## 文件结构

```
distill-conversation/
├── SKILL.md                          # Skill 定义（Claude Code 读取）
├── scripts/
│   └── parse_chatgpt_share.py        # ChatGPT 共享链接解析器（纯标准库）
├── examples/
│   └── 量化场景下的语言选型(...).md    # 实际蒸馏案例
├── README.md                         # 中文说明（本文件）
├── README.en.md                      # English README
└── LICENSE                           # MIT
```

## ChatGPT 解析器原理

ChatGPT 共享页面使用 **React Server Component (RSC/Flight)** 序列化格式——一种非标准的流式编码：

- 字符串被 interned（`"user"` 和 `"assistant"` 各只出现一次）
- 后续引用通过数字 ID 指向 interned 的角色
- 数据通常被双重转义（嵌套在 JSON 字符串中）

解析器自动处理所有这些情况，并在格式变化时给出明确警告。

## 已知限制

- **ChatGPT 格式依赖**：RSC 格式可能随 ChatGPT 更新而变化，解析器会在失败时明确提示
- **短消息丢失**：少于 20 字的 user 消息偶尔可能被跳过（不影响蒸馏结果）
- **仅支持 ChatGPT 链接**：其他 LLM 请直接粘贴对话文本

---

## 命名说明

- **Skill ID / slug**: `distill-conversation`
- **展示名**: Alembic（炼金术中的蒸馏器，比喻从对话中蒸馏知识）
- **功能描述**: Conversation Distiller / 对话蒸馏器
