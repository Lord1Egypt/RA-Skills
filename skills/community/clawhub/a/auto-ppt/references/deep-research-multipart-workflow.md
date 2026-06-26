# Deep-research multipart workflow for Auto-PPT

Use this mode when the user wants any of these:
- 先做成深度研究报告大纲
- 分成 6–10 个专业研究部分
- 每个部分先单独做一份 PDF
- 最后再合并成完整 PPT/PDF
- 先补充 YouTube 视频信息源
- 白板手绘风格 / 视觉惊艳 / 布局多样 / 统一风格
- 参考 `desearch-ppt-1.0.0 2` 的 PPT 风格

## Goal

Given a topic, produce a **high-spreadability deep research deck workflow**:
1. Turn the topic into a 6–10 part professional research outline
2. For each part, gather a few relevant YouTube links first
3. Feed those links plus the part text into NotebookLM as sources
4. Generate one PDF per part in a unified visual style
5. Merge the PDFs at the end
6. If requested, run the postprocess script to produce cleaned PDF + PPTX

## Output shape

Default structure: 6–10 parts.
Each part should feel like one chapter in a serious research report, not random bullets.

Suggested chapter types:
1. 背景与问题定义
2. 市场/行业现状
3. 关键技术或方法演进
4. 典型案例与代表玩家
5. 商业模式/传播逻辑/增长机制
6. 风险、争议与限制
7. 未来趋势与判断
8. 行动建议 / 结论

If the topic needs more granularity, expand to 9–10 parts; if narrower, compress to 6–7.

## Hard rules

- The first step is **not** generating one giant body of text.
- First create a **传播力强的深度研究大纲** with 6–10 parts.
- Each part must have:
  - part title
  - 3–5 key questions
  - the point of that part in the overall narrative
- Keep a single unified style across all parts.
- Style target: **whiteboard sketch / doodle / visual-explainer**, with strong contrast and varied layouts.
- Layouts should vary across parts, but the overall deck must still look like one family.

## YouTube-source rule

Before generating each part's NotebookLM deck:
1. Search YouTube for that part's topic
2. Prefer:
   - official talks
   - conference videos
   - lectures
   - credible creator explainers
   - product demos if relevant
3. Capture 2–5 links per part
4. Paste those links into NotebookLM as sources before or alongside the text

Do not dump a huge list. A few high-signal links are better.

Suggested searches:
- `<topic> overview YouTube`
- `<part title> explained YouTube`
- `<topic> conference talk YouTube`
- `<topic> case study YouTube`

## Narrative design rule

The deck should feel like a publishable deep-research presentation with strong shareability.
That means:
- opening should hook with a sharp framing
- middle sections should move from context -> evidence -> cases -> conflict
- later sections should move to judgment, implications, and next steps
- each part should naturally lead to the next

Think of the final merged deck as one long story, not a folder of unrelated PDFs.

## Unified style rule

Reference style benchmark:
- `/Users/youke/Downloads/desearch-ppt-1.0.0 2`

Desired visual qualities:
- whiteboard hand-drawn feel
- visually surprising but still readable
- mixed layouts, not repetitive left-text-right-image slides
- clear title hierarchy
- use diagrams, arrows, maps, dashboards, split comparisons, timelines
- maintain the same visual language, footer convention, and title rhythm across parts

## Execution workflow

### Step 1: create the 6–10 part outline
Produce a deep-research outline first.
Each part should include:
- `part_num`
- `part_title`
- `role_in_story`
- `key_questions`
- `style_hint`

### Step 2: generate one part at a time
For each part:
1. Search YouTube for that part
2. Collect 2–5 relevant links
3. Write the part text in a NotebookLM-friendly way
4. Keep explicit visual cues in the text so NotebookLM produces varied pages
5. Export one PDF per part

### Step 3: naming convention
Use stable filenames like:
- `主题-01-背景与问题定义.pdf`
- `主题-02-行业现状.pdf`
- `主题-03-技术演进.pdf`

Avoid generic names like `part1.pdf` if the topic is user-facing.

### Step 4: final merge
After all part PDFs are created:
- merge in part order
- if user asked for cleanup, run `postprocess_ppt_outputs.py`

## Token-efficiency guidance

- Do not explain the whole workflow to the user every time.
- When this mode is clearly requested, execute directly.
- Keep SKILL.md short; use this reference only when needed.
- Generate the outline first, then work part-by-part.
- Avoid giant monolithic prompts when part-wise prompts will do.

## Recommended final commands

### Merge ordered PDFs
```bash
bash /Users/youke/.openclaw/workspace/skills/auto-ppt/scripts/merge_pdf_on_desktop.sh 最终研究报告.pdf 主题-01-*.pdf 主题-02-*.pdf
```

### Postprocess after merge
```bash
python3 /Users/youke/.openclaw/workspace/skills/auto-ppt/scripts/postprocess_ppt_outputs.py --output-name 主题_final 主题-01-背景与问题定义.pdf 主题-02-行业现状.pdf 主题-03-技术演进.pdf
```

## What to tell the user at the end

Keep the final reply short:
- how many parts were created
- whether YouTube sources were added
- where the merged PDF/PPTX is
- whether duplicate-page cleanup was applied
