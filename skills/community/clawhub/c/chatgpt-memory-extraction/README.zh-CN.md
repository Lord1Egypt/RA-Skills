[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md)

# ChatGPT 记忆提取 🧠✨

一个 [OpenClaw](https://github.com/openclaw/openclaw) 技能，帮你把和 ChatGPT 聊了好久好久的那些对话，变成一份**有条理、能检索的个人记忆档案**～

## 这个小工具的由来

我和 ChatGPT 聊了三年多，积累了 500+ 个对话、6万多条消息。里面有我读过的论文、学到的知识、做过的决定、经历过的开心和难过、遇到的人——可是它们全都锁在一堆巨大的 JSON 文件里，想回顾的时候根本找不到 😢

所以就做了这个小工具，它可以帮你把 ChatGPT 的导出数据，一步步整理成按时间线排列的记忆档案，还会顺便帮你提取人物关系、学习轨迹、重要事件这些信息。

而且整理好的记忆档案不只能用来回顾——你可以把它喂给你的 OpenClaw 或者任何其他 AI 助手，**让它从第一天起就真正了解你**。再也不用每次换一个新的 AI 就重新做一遍详细的自我介绍了，那样真的很花时间 😅

## 能做些什么呢

- 📦 **自动提取**：一个 Python 小脚本帮你把 JSON 转成人能读的文本文件，按年份和季度分好类
- 📖 **深度整理**：引导 AI 逐个对话认真阅读（不是扫一眼标题就概括哦），写成结构化的季度时间线
- 👥 **人物档案**：提取对话里出现的每个人，给他们建一份独立的小档案
- 🎯 **主题提炼**：学术成长、情感时刻、生活变化、技能学习——按主题帮你汇总好

## 一句真心话

说实话，AI 在处理大量文本的时候**真的很容易偷懒**😅 这是我踩了好多坑之后才总结出来的教训。所以这个技能里内置了一套质量规则，专门对付 AI 的各种偷工减料（比如只看开头几条消息就开始概括、写"XX条消息讨论了各种话题"这种敷衍话、说"已更新文件"但其实根本没改……）。

不过即使有了这些规则，**还是建议你亲自看看 AI 整理出来的东西**。每做完一个季度就检查一下，发现不对就让它重来。最好的效果来自你和 AI 的配合，而不是完全交给它就不管啦～

## 怎么用

### 1. 安装

```bash
# 通过 ClawHub
npx clawhub install chatgpt-memory-extraction

# 或从 GitHub 手动安装
git clone https://github.com/cyresearch/chatgpt-memory-extraction.git ~/.openclaw/workspace/skills/chatgpt-memory-extraction
```

### 2. 导出你的 ChatGPT 数据

打开 [ChatGPT](https://chat.openai.com) → 设置 → 数据控制 → 导出数据 → 确认

> ⏳ 导出可能要等**几个小时甚至一两天**哦，数据多的话会更久。好了之后 OpenAI 会发邮件通知你～

### 3. 开始整理吧！

跟你的 OpenClaw 助手说：

> "我导出了 ChatGPT 的数据，帮我整理成记忆档案吧"

它会带着你一步步来：提取 → 逐季度阅读 → 写时间线 → 你来审核 → 提取人物和主题 🌱

## 整理出来长什么样

```
memory/
├── timeline/{year}/Q{1-4}.md   # 按季度的时间线（最核心的文件～）
├── people/{category}/*.md       # 人物档案
├── topics/*.md                  # 按主题的记录
├── meta/extraction-log.md       # 进度追踪
└── raw/{year}_Q{n}/             # 原始对话文本（方便回头验证）
```

## 需要准备什么

- [OpenClaw](https://github.com/openclaw/openclaw)
- Python 3.8+
- 你的 ChatGPT 数据导出文件（从 OpenAI 下载的 `.zip`）

## License

MIT — 见 [LICENSE](LICENSE)
