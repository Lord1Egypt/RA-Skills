# art-critique.skill

通过 **对话式艺术评论** 帮助你推进作品发展的 Agent Skill。不是打分，也不是替你改作品，而是用外部视角激发创意。

适用于支持 [Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) 的运行环境（如 Claude Code、Cursor 等）。

### 能做什么

- 对进行中或已完成的作品获得反馈：直观感受、表达逻辑、接下来可以实验什么。
- 按方面逐轮讨论（概念、形式、材料、语境等），结束时留下整场对话的笔记。
- 在确实贴合作品时，引入艺术理论、其他作品或背景信息——包括作品引用、挪用或重演某类熟悉图像的情况。
- 支持 **图像、文本、音频、视频、装置或混合** 媒介；也可发送 **自录演示+讲解短视频**（Agent 会区分「画面所见」与「口播所说」，并先完成接入笔记再开始讨论）。建议：约 3 分钟内、画面清晰、口播与展示同步，录完再发送。

可以说：*帮我 critique 一下*、*review 我的作品*、*你对这件作品有什么感受* 等。

### 使用

安装后让 Agent 能读取 skill 根目录下的 `SKILL.md`（路径因运行环境而异）。每次新 critique 会在工作目录创建**独立 session 文件夹**（如 `art-critique-sessions/2026-06-07_作品名_143022/`），同天同作品多次 session 用时间戳区分，不会覆盖旧笔记；可选索引见 `art-critique-sessions/_index.md`。

**输入建议（超出时 Agent 会请你精简）：** 图像 ≤5 张；视频 1 条（作品 ≤5 分钟，演示+讲解 ≤3 分钟）；文本约 8000 字内。视频请先说明是「作品本身」还是「边展示边讲解」。

### 自定义

**更换评论框架** — 评论框架是解读作品的指导方法。默认框架：`references/note-frameworks/four-steps.md`（视觉/静态）。音频/视频/表演：`time-based-media.md`。使用其他框架：在 `references/note-frameworks/` 添加文件，并在 `SKILL.md` 中指明参考文件路径。

**扩展知识库** — 知识库是 Agent 联想时的自定义信息来源之一。从 `references/templates/` 复制模板到 `references/library/cases/`、`theories/` 或 `contexts/`，用散文填写正文，并在 frontmatter 写一行 `summary`。无需更新其他索引。作者日后可能会更新知识库来进一步提升 skill 专业度。

---

An agent skill for **dialogue-based art critique**: an outside perspective through feeling and open questions, not grading or telling you what to fix.

Compatible with agents that load [Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) (e.g. Claude Code, Cursor).

### What you can use it for

- Get feedback on a work-in-progress or finished piece — what lands, what confuses, what to experiment next.
- Walk through a work one aspect at a time (concept, form, material, context…) and leave with written notes from the session.
- Enrich the conversation with art theory, other works, or background when it actually fits the piece — including when the work quotes or restages something familiar.
- Critique **image, text, audio, video, installation, or mixed** work — including a **short self-recorded demo with narration** (the agent separates what it sees from what you say, and completes an ingest pass before dialogue). Tip: keep it under ~3 minutes, well lit, show and speak in sync, send when recording is finished.

Say things like: *critique this*, *help me review my artwork*, *what do you feel about this piece*.

### Setup

Install so your agent can see `SKILL.md` at the skill root (path depends on the runtime). Each new critique gets its own session folder (e.g. `art-critique-sessions/2026-06-07_work-slug_143022/`); same work on the same day uses a new timestamp so earlier notes are not overwritten. Optional index: `art-critique-sessions/_index.md`.

**Input guidelines (agent will ask you to trim if over):** up to 5 images; 1 video (work ≤5 min, demo+talk ≤3 min); text ~8,000 words. For video, say whether the clip IS the work or a walkthrough with narration.

### Customize

**Replace the critique framework** — Default first-reading method: `references/note-frameworks/four-steps.md` (visual/static). For audio/video/performance: `time-based-media.md`. To use another method: add a file under `references/note-frameworks/` and note its path in `SKILL.md`. 

**Extend the knowledge library** — Copy a template from `references/templates/` into `references/library/cases/`, `theories/`, or `contexts/`. Fill in plain prose and a one-line `summary` in the frontmatter. Author may update the library later to improve this skill.
