---
name: campus-morning-brief
description: Create a concise, age-appropriate, personalized daily campus morning brief with local weather, verified current news, a bilingual quote, study guidance, reminders, and a concrete action prompt. Use when a user asks for a 校园晨报、学生晨报、school morning brief、printable student daily digest，或面向儿童、青少年、班级和家庭的自动晨间简报。
---

# Campus Morning Brief / 校园晨报

Generate a source-backed brief that a student can finish in three to five minutes. Keep personal settings in an external config and fetched content in structured JSON so the workflow remains reusable and auditable.

生成一份有来源依据、可在三到五分钟内读完的学生晨报。将个人设置保存在外部配置中，并以结构化 JSON 保存采集内容，使流程可复用、可审计。

## Workflow / 工作流程

### 1. Resolve the profile / 确定用户配置

- Read an existing profile when supplied. Otherwise collect or infer the display name, city, timezone, age group, language, interests, reminders, and output directory.
- Use neutral defaults for omitted optional fields. Never invent private facts, school names, schedules, or health information.
- Follow [references/config.example.json](references/config.example.json) for the portable profile format.

- 用户提供配置时直接读取；否则收集或合理推断显示名称、城市、时区、年龄段、语言、兴趣、提醒事项和输出目录。
- 对缺失的可选字段使用中性默认值。不得虚构隐私信息、学校名称、课程安排或健康信息。
- 通用配置格式见 [references/config.example.json](references/config.example.json)。

### 2. Establish the issue date / 确定晨报日期

- Use the profile timezone, not the host timezone, for “today.” State the exact calendar date in the output.
- 以配置中的时区而非主机时区确定“今天”，并在输出中写明完整日期。

### 3. Research current content / 调研时效内容

- Fetch current local weather and news; do not rely on model memory.
- Prefer primary or authoritative sources. Cross-check claims affecting safety.
- Select news published within the last 72 hours when possible. If only older coverage is available, disclose its date instead of presenting it as new.
- Preserve the direct URL, publisher, and publication date for every news item.
- Exclude graphic violence, sexual content, gambling, self-harm details, sensational rumors, disguised advertising, and age-inappropriate material.

- 实时获取当地天气与新闻，不依赖模型记忆。
- 优先采用第一方或权威来源；涉及安全的内容须交叉核验。
- 尽量选择过去 72 小时内发布的新闻。只能采用较早报道时，应明确原始日期，不得包装成最新消息。
- 每条新闻必须保留直达链接、发布机构和发布日期。
- 排除血腥暴力、色情、赌博、自伤细节、耸动谣言、软性广告及不适龄内容。

### 4. Build the payload / 构建内容数据

- Follow [references/content-guidelines.md](references/content-guidelines.md).
- Produce JSON matching [references/brief.schema.json](references/brief.schema.json).
- Summarize in original wording; do not copy article passages. Separate reported facts from advice or interpretation.

- 遵循 [references/content-guidelines.md](references/content-guidelines.md)。
- 生成符合 [references/brief.schema.json](references/brief.schema.json) 的 JSON。
- 使用原创表述进行摘要，不复制报道段落；明确区分报道事实、建议和解读。

### 5. Validate and render / 校验并渲染

Save the payload as `brief.json`, then run:

将数据保存为 `brief.json`，然后执行：

```bash
python3 scripts/render_brief.py brief.json --output-dir output
```

The script validates the payload and writes `morning-brief.md`, `morning-brief.html`, and `metadata.json` without third-party Python packages. Treat validation failures as content errors and fix the payload instead of bypassing validation.

脚本不依赖第三方 Python 包，会校验数据并生成 `morning-brief.md`、`morning-brief.html` 和 `metadata.json`。校验失败应视为内容错误，应修正数据，不得绕过校验。

### 6. Inspect the result / 检查结果

- Confirm the HTML has no clipping or overflow when a browser or screenshot tool is available.
- Confirm every current-events item has a working source URL.
- Confirm names, dates, weather location, and reminders match the profile.
- Render validated HTML to PDF or PNG with the environment's browser, PDF, or screenshot capability when needed; do not make PDF/PNG a hard dependency.

- 有浏览器或截图工具时，检查 HTML 是否存在裁切或溢出。
- 确认每条时事内容都包含可访问的来源链接。
- 确认姓名、日期、天气地点和提醒事项与配置一致。
- 需要 PDF 或 PNG 时，使用当前环境的浏览器、PDF 或截图能力处理已校验的 HTML；不要将 PDF/PNG 设为硬依赖。

### 7. Deliver only when requested / 仅在明确要求时投递

- Keep delivery separate from generation.
- Ask before sending, posting, or printing unless an existing automation explicitly authorizes it.
- Return output paths and a compact source list.

- 将内容生成与投递分离。
- 除非现有自动化已明确授权，否则发送、发布或打印前必须确认。
- 返回输出路径和精简来源列表。

## Automation Mode / 自动化模式

For an established scheduled automation, execute end to end without interactive checkpoints. Fail with a nonzero exit code or structured error when required data is missing. Never silently reuse yesterday's weather or present stale news as current.

由已建立的定时自动化调用时，可不中途确认并完整执行。缺少必要数据时，应返回非零退出码或结构化错误。不得静默复用昨日天气，也不得把过期新闻呈现为最新内容。

## Output Standard / 输出标准

- Fit the core brief on one A4 page at normal print scale. / 核心内容在正常打印比例下应适配一张 A4 纸。
- Target three to five minutes of reading. / 阅读时长控制在三到五分钟。
- Use calm, concrete, age-appropriate language. / 使用平实、具体且符合年龄段的语言。
- Include sources in both the payload and rendered output. / 数据和渲染结果均须保留来源。
- Keep credentials, private schedules, generated issues, and delivery identifiers outside the skill directory. / 凭据、私人日程、历史晨报和投递标识不得放入 Skill 目录。
