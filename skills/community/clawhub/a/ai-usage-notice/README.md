# ai-usage-notice

**为 AI 直接输出的成品默认添加「AI 使用说明」的规范 skill——项目 README 开头 + 文章文末双默认位置，法律依据、施加方式、例外边界完整齐备。**

**A skill that mandates an "AI Usage Notice" on AI-produced deliverables — a visible notice on the project page or at the end of an article, backed by legal requirements, with clear placement rules, alternatives, and exceptions.**

[中文](#中文) | [English](#english)

---

## 中文

### 这是什么

一套「AI 生成内容标识」的落地规范，依据《生成式人工智能服务管理暂行办法》与《人工智能生成合成内容标识办法》（2025-09-01 施行）整理，适用于所有由 AI 直接输出的成品：

- **规则核心**：凡 AI 直接输出的成品（代码项目/网站/应用/脚本文档/文章/教程等），默认附带 AI 使用说明，除非用户明确说"不加"。
- **两种默认施加方式**：项目 → 在「项目介绍处」标明；文章/文档 → 在「结尾处」注明。
- **声明要素清单**：明确"AI 生成 / AI 辅助生成"措辞 + 生成时间 + 一句使用注意。
- **备选方式**：文件头部注释、`NOTICE.md` 独立声明文件、平台内置"AI 生成"标识、交付时口头说明。
- **例外与边界**：用户说"不加"就不加也不追问；用户主导的长期产品代码库由用户自己决定。
- 附带法律背景说明与活文档更新协议。

### 安装

```bash
git clone https://github.com/mowenQWQ/ai-usage-notice.git
cp ai-usage-notice/SKILL.md /path/to/your/agent/skills/ai-usage-notice/
```

适用于支持 Skill 格式的 AI 编码助手（Claude Code / CodeBuddy / OpenClaw 等），按 description 关键词自动触发。

---

## English

### What is this

A practical standard for labeling AI-generated content, grounded in China's *Interim Measures for Generative AI Services* and the *AI-Generated Synthetic Content Labeling Measures* (effective 2025-09-01). Applies to every deliverable produced directly by AI:

- **Core rule**: every AI-produced deliverable (code project / website / app / script / article / tutorial) carries an AI usage notice by default — unless the user explicitly opts out.
- **Two default placements**: projects → a visible statement near the project description; articles/documents → a note at the end.
- **Required elements**: honest "AI-generated / AI-assisted" wording + generation date + a one-line usage caution.
- **Alternatives**: file-header comments, a standalone `NOTICE.md`, platform AI labels, verbal disclosure at delivery.
- **Exceptions**: "no notice" when the user says so (no nagging); user-owned long-term products are the user's call.
- Includes the legal background and a living-document update protocol.

### Install

```bash
git clone https://github.com/mowenQWQ/ai-usage-notice.git
cp ai-usage-notice/SKILL.md /path/to/your/agent/skills/ai-usage-notice/
```

---

## License

MIT — see [LICENSE](LICENSE).

---

## 🤖 AI 使用声明 / AI Usage Disclosure

本项目在开发与维护过程中使用了 AI 编程助手（Claude / Anthropic）辅助代码编写、文档整理与问题排查；核心决策、内容审核与最终发布由维护者完成。

This project was developed and maintained with the assistance of an AI coding assistant (Claude / Anthropic) for coding, documentation, and troubleshooting. Core decisions, content review, and final releases are made by the maintainer.