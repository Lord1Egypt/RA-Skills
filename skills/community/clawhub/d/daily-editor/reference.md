# Reference

## Product framing

`私人编辑部` should feel like a compact publication, not a feed reader.

Good framing:

- curated daily push
- private editorial desk
- selective one-page brief
- calm A4 PDF edition

Avoid framing it as:

- raw crawler output
- full news archive
- generic portal homepage
- outrage-driven content stream

## Safety framing

The edition should be safe, harmless, and easy to circulate internally or personally.

Preferred tone:

- calm
- factual
- restrained
- useful

Avoid:

- alarmist phrasing
- graphic or explicit detail
- glamorizing harmful behavior
- edgy packaging for its own sake

## Good section patterns

### Standard daily edition

- Lead
- Section A
- Section B
- Watchlist

### Professional morning brief

- Top line
- Markets / business
- Technology / AI
- Calendar / what to watch

### Personal hybrid edition

- External world
- Core topic
- Personal notes
- Tomorrow

### Games / culture edition

- Lead story
- Platform moves
- Releases / content
- Industry signals
- Watchlist

## Density guide

### Light

- 4 to 6 items
- one strong lead
- ideal for premium-feeling one-page PDFs

### Standard

- 6 to 12 items
- best default for daily push

### Dense

- 12 to 16 items
- use only if the user explicitly wants a packed brief
- compress weaker items into short briefs

## PDF heuristics

Default page composition:

```html
<body>
  <article class="sheet">
    <header class="masthead">...</header>
    <main>
      <section class="lead">...</section>
      <section class="domain-section">...</section>
      <section class="domain-section">...</section>
      <aside class="watchlist">...</aside>
    </main>
    <footer>...</footer>
  </article>
</body>
```

Print-first rules:

- prefer A4 portrait
- keep margins generous enough for print
- avoid overlong sections that force awkward page breaks
- make the first page complete even if the edition spills to a second page
- use one restrained accent color

## Editorial packaging modes

If the user wants a result that feels less plain, use one of these framing modes.

### Headliner

- each section opens with a clear editorial line
- supporting items are shorter and more compressed
- good for premium daily push tone

### Signal Board

- classify items as strong signal, weak signal, and noise
- useful for finance, AI, business, and industry monitoring

### Tension Map

- frame the day around competing forces carefully
- examples: platform vs publisher, growth vs pressure, convenience vs regulation
- avoid theatrical conflict language

### What It Means

- add a compact implication line after each news item
- good when the audience wants interpretation, not just recap

### Three-second scan

- begin each section with one sentence that a reader can skim instantly
- ideal for one-page PDF briefs

Use packaging through copy and structure first. Do not rely on decoration alone.

## Source link policy

For sourced news items, include the original link whenever available.

Recommended pattern inside cards:

```html
<p class="source">
  来源：<a href="https://example.com">Xbox Wire</a>
</p>
```

Guidelines:

- Prefer the original publisher or primary report over summaries of summaries.
- Use a human-readable source label.
- Preserve clean reading flow; source links should support the item, not dominate it.
- If the PDF renderer preserves links, keep them clickable.

## Preview workflow

When PDF is the deliverable, validate the page visually before final delivery when possible.

Recommended order:

1. Save the artifact as a local `.pdf` file.
2. If the PDF comes from HTML/CSS, preview the render source when faster.
3. Check spacing, overflow, weak hierarchy, broken cards, and page breaks.
4. Confirm source labels are readable and not too small.

## Editorial heuristics

When choosing what leads the edition, prefer:

1. structural change over small update
2. forward implication over isolated event
3. cross-domain relevance over niche trivia
4. one strong lead over many equal leads
5. calm clarity over dramatic escalation

## Naming heuristics for sections

Prefer section names that read like an issue, not a menu.

Good:

- 今天主线
- 市场脉搏
- 平台动向
- 关键产品
- 今日观察
- 明日关注

Weak:

- 新闻1
- 科技栏目
- 其他
- 杂项

## Custom section handling

If the user gives raw topics like:

- finance
- games
- AI
- personal notes

You may transform them into:

- 市场脉搏
- 游戏工业
- AI 新动向
- 编辑手记

Keep the meaning, improve the editorial voice, and keep the phrasing safe and neutral.
