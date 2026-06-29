# Campus Morning Brief / 校园晨报

A reusable bilingual AI-agent skill for creating concise, personalized, and source-backed morning briefs for students.

一个面向学生的通用双语 AI Agent Skill，用于生成简洁、个性化且可追溯来源的校园晨报。

[ClawHub Skill / ClawHub 技能页](https://clawhub.ai/skills/campus-morning-brief) ·
[Version / 版本 1.0.3](https://clawhub.ai/skills/campus-morning-brief) ·
[MIT License / MIT 许可证](LICENSE)

![Campus Morning Brief preview / 校园晨报效果图](assets/campus-morning-brief-preview.jpg)

## Why this skill / 为什么需要它

Most news digests are written for adults and are too long, too broad, or unsuitable for a student's morning routine. This skill turns current weather, verified news, interests, study guidance, and reminders into a brief that can be read in three to five minutes.

多数资讯摘要面向成年人，篇幅过长、范围过宽，也不适合学生早晨阅读。本 Skill 将实时天气、经核验的新闻、个人兴趣、学习方法和提醒事项整理成一份可在三到五分钟内读完的晨报。

## Features / 主要能力

- Personalized by city, timezone, age group, language, and interests. / 按城市、时区、年龄段、语言和兴趣进行个性化。
- Current weather with clothing and campus-safety advice. / 提供实时天气、穿衣建议和校园安全提示。
- Source-backed general and interest news. / 提供可追溯来源的综合新闻与兴趣资讯。
- Age-appropriate filtering and calm wording. / 进行适龄内容过滤，并使用平实表达。
- Bilingual quote, study method, reminders, and action anchor. / 包含双语名言、学习方法、提醒事项和行动锚点。
- Structured JSON validation plus Markdown and HTML rendering. / 支持结构化 JSON 校验以及 Markdown、HTML 渲染。
- No third-party Python runtime dependencies. / Python 运行时不依赖第三方包。

## Install from ClawHub / 从 ClawHub 安装

```bash
clawhub install campus-morning-brief
```

ClawHub page / 商店页面：<https://clawhub.ai/skills/campus-morning-brief>

## Quick start / 快速开始

Ask your agent to use the skill with a prompt such as:

可以使用类似下面的提示词调用 Skill：

```text
Use $campus-morning-brief to create today's morning brief for a
middle-school student in Beijing who likes science and football.

使用 $campus-morning-brief，为一名居住在北京、喜欢科学和足球的
初中生生成今天的校园晨报。
```

The skill guides the agent to:

Skill 会引导 Agent：

1. Resolve the student profile and local date. / 确定学生配置和当地日期。
2. Research current weather and source-backed news. / 调研实时天气和有来源依据的新闻。
3. Build and validate a structured `brief.json`. / 构建并校验结构化 `brief.json`。
4. Render Markdown, HTML, and metadata. / 渲染 Markdown、HTML 和元数据。
5. Deliver or print only after authorization. / 仅在获得授权后发送或打印。

## Render an existing payload / 渲染已有数据

Use the portable profile example in [`references/config.example.json`](references/config.example.json) and build a payload matching [`references/brief.schema.json`](references/brief.schema.json). Then run:

参考 [`references/config.example.json`](references/config.example.json) 中的通用配置，并构建符合 [`references/brief.schema.json`](references/brief.schema.json) 的数据，然后执行：

```bash
python3 scripts/render_brief.py brief.json --output-dir output
```

Generated files / 生成文件：

```text
output/
├── morning-brief.md
├── morning-brief.html
└── metadata.json
```

## Content and safety / 内容与安全

- Current information must be fetched instead of recalled from model memory. / 时效内容必须实时获取，不得依赖模型记忆。
- Every news item must include its publisher, date, and direct URL. / 每条新闻必须包含发布机构、日期和直达链接。
- Graphic violence, sexual content, gambling, self-harm details, rumors, disguised advertising, and age-inappropriate material are excluded. / 排除血腥暴力、色情、赌博、自伤细节、谣言、软性广告和不适龄内容。
- Credentials, private schedules, delivery identifiers, and generated issues stay outside the Skill directory. / 凭据、私人日程、投递标识和历史晨报不得放入 Skill 目录。
- Sending, posting, or printing requires explicit authorization unless an existing automation already grants it. / 除非现有自动化已经授权，否则发送、发布或打印前必须明确确认。

See [`SKILL.md`](SKILL.md) for the complete workflow and [`references/content-guidelines.md`](references/content-guidelines.md) for bilingual editorial guidance.

完整工作流程见 [`SKILL.md`](SKILL.md)，双语编辑规范见 [`references/content-guidelines.md`](references/content-guidelines.md)。

## Repository structure / 仓库结构

```text
campus-morning-brief/
├── SKILL.md                         # Agent workflow / Agent 工作流程
├── agents/openai.yaml               # Skill UI metadata / 界面元数据
├── references/
│   ├── brief.schema.json            # Output schema / 输出规范
│   ├── config.example.json          # Portable profile / 通用配置
│   └── content-guidelines.md        # Editorial rules / 编辑规范
├── scripts/render_brief.py          # Validator and renderer / 校验与渲染
└── tests/                            # Tests and fixtures / 测试与样例
```

## Development / 开发与测试

```bash
python3 -S -B -m unittest discover -s tests -v
python3 scripts/render_brief.py tests/fixtures/valid.json --output-dir output
```

## Contributing / 参与贡献

Contributions are welcome, especially improvements to student-safe content rules, structured payload validation, rendering quality, and bilingual documentation.

欢迎参与贡献，尤其是学生适用的内容安全规则、结构化数据校验、渲染质量和双语文档。

- Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. / 提交 PR 前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
- Report reproducible problems with [GitHub Issues](https://github.com/my12121-beep/campus-morning-brief/issues). / 可通过 [GitHub Issues](https://github.com/my12121-beep/campus-morning-brief/issues) 反馈可复现问题。
- Use [GitHub Discussions](https://github.com/my12121-beep/campus-morning-brief/discussions) for ideas, examples, and usage questions. / 可在 [GitHub Discussions](https://github.com/my12121-beep/campus-morning-brief/discussions) 讨论想法、样例和使用问题。
- If this skill helps your workflow, starring the repository and sharing the ClawHub page helps other developers find it. / 如果这个 Skill 对你有帮助，给仓库 Star 并分享 ClawHub 页面能帮助其他开发者发现它。

## Discoverability / 曝光与发现

This repository is published as a public GitHub project and a ClawHub skill. Useful entry points:

本仓库同时作为公开 GitHub 项目和 ClawHub Skill 发布。常用入口：

- GitHub: <https://github.com/my12121-beep/campus-morning-brief>
- ClawHub: <https://clawhub.ai/skills/campus-morning-brief>
- Release: <https://github.com/my12121-beep/campus-morning-brief/releases/tag/v1.0.3>
- Promotion kit / 推广文案：[PROMOTION.md](PROMOTION.md)

## Links / 相关链接

- [ClawHub Skill / ClawHub 技能页](https://clawhub.ai/skills/campus-morning-brief)
- [GitHub repository / GitHub 仓库](https://github.com/my12121-beep/campus-morning-brief)
- [GitHub Discussions / GitHub 讨论区](https://github.com/my12121-beep/campus-morning-brief/discussions)
- [Promotion kit / 推广文案](PROMOTION.md)
- [Report an issue / 提交问题](https://github.com/my12121-beep/campus-morning-brief/issues)

## License / 许可证

[MIT](LICENSE)
