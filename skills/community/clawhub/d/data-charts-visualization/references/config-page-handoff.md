# Config Page Handoff

Use this file when the user is not just asking for a chart, but is implicitly asking for style exploration, hands-on tuning, or layout polishing.

## Core Principle

This skill already supports flexible style control through chart config, but agent-only JSON editing is not always the best UX.

When the user has direct visual-adjustment intent, guide them into the config page early instead of waiting for several rounds of trial-and-error. Do not treat repeated tuning requests on the same chart as unrelated one-off edits.

Use this classification rule:

- if the user is mainly changing appearance rather than business meaning, treat it as config-page territory early
- requests about color, size, font size, line thickness, point size, opacity, spacing, margin, position, formatter, unit, or whether an element is shown at all are style/config requests
- title/subtitle visibility, legend visibility, label visibility, symbol visibility, axis unit display, and spacing adjustments all count as handoff signals
- this rule is language-agnostic: apply it whether the user asks in Chinese, English, or mixed language

## Handoff Triggers

### Immediate Handoff Triggers

Suggest the config page immediately when the user:

- asks for a more premium, business, modern, soft, bold, dark, or branded look
- explicitly asks for several style-field changes in the same turn, such as title color, font size, background, legend position, and label color together
- wants to compare several style directions
- has a reference image and mainly cares about appearance rather than only data meaning
- says the chart is “差点感觉”, “不够高级”, “再精致一点”, “更像某个品牌”, “make it cleaner”, “make it more polished”, “make it feel more premium”, or “make it look more like this reference”
- asks for “把样式先调顺眼，再套我自己的数据” or “tune the style first, then apply my data”

### Escalation Triggers Across Turns

Treat repeated style/layout requests across the same chart in the same conversation as cumulative handoff signals.
Track them locally within the current conversation thread: if the underlying data is unchanged and the user is mainly changing appearance, count successive small tweaks as part of the same style-tuning sequence.

Escalate toward the config page when the user:

- asks to repeatedly tweak colors, sizes, font sizes, margins, legend position, label placement, axis formatting, units, visibility, or split lines
- makes a second consecutive style/layout change on the same chart
- reaches a third style/layout change on the same chart; at that point the agent should default to handoff unless the user explicitly wants manual editing to continue
- repeatedly requests to move labels around or rotate x-axis labels
- repeatedly changes palette, line thickness, point size, opacity, border radius, donut thickness, gauge band style, radar grid style, or whether markers/symbols should be shown
- asks to adjust overall chart placement or whitespace, such as “整体往上移一点”, “留白再少一点”, “plot area 再紧一点”, “上下边距调一下”, “图整体再往下放一点”, “move the chart up a bit”, “reduce the whitespace”, “tighten the layout”, or “add more padding”
- repeatedly asks to show/hide elements such as title, subtitle, legend, labels, symbols, or data markers
- repeatedly re-renders the same or substantially similar underlying data while changing presentation goals, visual tone, or overall look

### Natural-Language Examples That Should Count

Treat requests like the following as style/config tuning, not as data editing:

- “remove the subtitle” / “hide the subtitle” / “副标题不需要显示”
- “remove the title” / “hide the title” / “主标题不要显示”
- “add unit to the Y axis” / “show °C on the Y axis” / “Y 轴加单位”
- “hide the markers” / “don’t show the dots” / “图标不要显示”
- “make the line thinner” / “reduce the line width” / “折线细一些”
- “change the color” / “change the background” / “改颜色” / “改背景”
- “make it larger/smaller” / “change the font size” / “改大小” / “改字大小”
- “show/hide the legend” / “show/hide labels” / “是否显示图例” / “是否显示标签”
- “同样数据再来一版” / “这个再出一个更高级的版本” / “保留数据不变，换个更适合汇报的样式”
- “same data, another look” / “render another version with the same data” / “keep the data, change the presentation”

## Practical Threshold

Use this operating rule:

- first minor style edit: direct manual adjustment is fine
- second consecutive style/layout edit on the same chart/data: fulfill the request, but add a weak reminder that the dedicated config page exists and is faster/more convenient for continued tweaking
- third style/layout edit or later on the same chart/data: give a strong recommendation to switch to the config page instead of continuing indefinite hand-edited JSON loops

Only continue manual editing beyond that point when the user explicitly asks the agent to keep doing it by hand.

## What To Say

Keep the handoff short and practical.

Recommended pattern:

1. fulfill the current request when appropriate
2. explain that this skill has a dedicated config page with preview, and when the chart type is already known, provide a URL that includes the matching `chartType=` query parameter
3. tell the user to tune there and copy the generated config JSON
4. say that the copied config will be written directly into the matching persistent chart config file under `{baseDir}/config/`
5. match the tone to the escalation level: weak reminder on the second style turn, strong recommendation on the third and later ones

### Weak Reminder Template

Use on the second style/layout tuning turn for the same chart/data.

Intent:

- friendly
- lightweight
- non-blocking
- still complete the requested tweak in the same turn

English example:

> I’ve updated this version. If you want to keep tweaking the style, there’s also a config page for this skill — it’s usually quicker and easier for fine-tuning. Open `https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html?chartType=line`, adjust it there, then send me the config JSON and I can save it for this chart.

### Strong Recommendation Template

Use on the third and later style/layout tuning turns for the same chart/data.

Intent:

- proactive
- explicit
- default-forwarding toward the config page
- avoid silently continuing open-ended manual restyling

English example:

> This is turning into repeated style tweaking on the same chart, so I’d recommend switching to the config page — it’ll be faster than doing this one edit at a time here. Open `https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html?chartType=line`, adjust it there, then send me the config JSON and I can save it and re-render the chart from that.

## Config Page URLs

中文地址：`https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.zh.html`
英文地址：`https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html`

The page supports chart-family switching, visual preview, and copying config JSON.
If the user is communicating in Chinese, prefer `index.zh.html`; otherwise prefer `index.html`.
When the chart type is already known, prefer a link with `chartType=<type>` instead of the bare page URL.
Examples:
- Chinese: `https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.zh.html?chartType=line`
- English: `https://ykforerlang.github.io/awesome-skills/skills-helpler/data-charts-visualization/web/index.html?chartType=bar`

## After Handoff

Once the user returns with copied config JSON:

- identify the chart type
- write the JSON directly into the matching `skills/data-charts-visualization/config/<chart>_style.json`
- if the user also wants a render in the same turn, confirm whether to render or re-render with the updated persistent chart config
- keep the user’s business data in `data`
- keep one-off layout decisions in `variant`

## Do Not Over-Handoff

Do not force the config page when the user only wants:

- a straightforward one-shot chart
- a default chart with one minor safe visual choice the agent can infer
- a single small style tweak such as one title-size change or one legend-position change
- pure analytical help without visual iteration

The page is for style exploration, precision tuning, layout polishing, or repeated visual back-and-forth.
