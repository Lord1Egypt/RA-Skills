# A4 PDF Templates

Use these as default skeletons for `私人编辑部` when the user wants a quick A4 portrait PDF result with minimal styling. A single-file HTML/CSS document is acceptable as the render source, but the final deliverable should be a PDF.

## Shared print target

Use this baseline in any print-first render source:

```css
@page {
  size: A4 portrait;
  margin: 14mm 12mm 14mm;
}

html, body {
  margin: 0;
  padding: 0;
  background: #f3f0e8;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
  color: #172033;
  line-height: 1.6;
}

.sheet {
  width: 186mm;
  min-height: 269mm;
  margin: 0 auto;
  padding: 0;
}
```

## Template 1: Calm Single Column

Use when:

- the user wants a simple daily brief
- content volume is low
- one-column reading flow matters more than density

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>私人编辑部</title>
  <style>
    @page { size: A4 portrait; margin: 14mm 12mm; }
    body {
      margin: 0;
      background: #f3f0e8;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
      color: #172033;
      line-height: 1.65;
    }
    .sheet { width: 186mm; min-height: 269mm; margin: 0 auto; }
    .masthead { padding: 0 0 6mm; border-bottom: 1.5px solid #172033; }
    .brand { font-size: 22pt; font-weight: 800; }
    .meta { margin-top: 3mm; font-size: 9.5pt; color: #5f6776; }
    .section { margin-top: 6mm; padding: 5mm; background: #fff; border: 1px solid #ddd8cd; border-radius: 4mm; }
    .section h2 { margin: 0 0 3mm; font-size: 14pt; }
    .item + .item { margin-top: 4mm; padding-top: 4mm; border-top: 1px solid #e5e0d5; }
    .item h3 { margin: 0 0 1.5mm; font-size: 11.5pt; }
    .item p { margin: 0; color: #5f6776; font-size: 10pt; }
    .source { margin-top: 2mm; font-size: 8.5pt; }
  </style>
</head>
<body>
  <article class="sheet">
    <header class="masthead">
      <div class="brand">私人编辑部</div>
      <div class="meta">2026.03.17 · 每日简报 · A4 竖版</div>
    </header>

    <section class="section">
      <h2>今天主线</h2>
      <article class="item">
        <h3>主标题</h3>
        <p>一句话摘要。再补一句为什么重要。</p>
        <p class="source">来源：原始链接</p>
      </article>
    </section>
  </article>
</body>
</html>
```

## Template 2: Editorial Two Column

Use when:

- the user wants a publication-like edition
- content naturally splits into two groups
- A4 单页完成度比移动端适配更重要

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>私人编辑部</title>
  <style>
    @page { size: A4 portrait; margin: 12mm; }
    body {
      margin: 0;
      background: #f3f0e8;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
      color: #172033;
      line-height: 1.6;
    }
    .sheet { width: 186mm; min-height: 273mm; margin: 0 auto; }
    .masthead {
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 6mm;
      align-items: end;
      padding-bottom: 5mm;
      border-bottom: 1.5px solid #172033;
    }
    .brand { font-size: 24pt; font-weight: 800; letter-spacing: -0.03em; }
    .summary { font-size: 9.5pt; color: #677083; text-align: right; }
    .grid { display: grid; grid-template-columns: 1.12fr 0.88fr; gap: 5mm; margin-top: 5mm; }
    .column { display: grid; gap: 4mm; align-content: start; }
    .section { background: rgba(255,255,255,0.96); border: 1px solid #ddd7cc; border-radius: 4mm; padding: 4.5mm; }
    .section h2 { margin: 0 0 2.5mm; font-size: 13pt; }
    .lead h3 { margin: 0 0 2mm; font-size: 18pt; line-height: 1.15; }
    .item + .item { margin-top: 3.5mm; padding-top: 3.5mm; border-top: 1px solid #e5dfd5; }
    .item h3 { margin: 0 0 1.5mm; font-size: 11pt; }
    .item p, .lead p { margin: 0; color: #677083; font-size: 9.6pt; }
    .source { margin-top: 1.8mm; font-size: 8.4pt; }
  </style>
</head>
<body>
  <article class="sheet">
    <header class="masthead">
      <div>
        <div class="brand">私人编辑部</div>
        <div>2026.03.17 · PDF Daily Push</div>
      </div>
      <div class="summary">一句话点明本期主线，让读者在 5 秒内知道为什么值得翻这一页。</div>
    </header>

    <main class="grid">
      <div class="column">
        <section class="section lead">
          <h2>今天主线</h2>
          <h3>这里放最强的一条主标题</h3>
          <p>主摘要。再补一句影响或判断。</p>
          <p class="source">来源：原始链接</p>
        </section>
      </div>

      <aside class="column">
        <section class="section">
          <h2>明日关注</h2>
          <article class="item">
            <h3>观察点</h3>
            <p>下一步值得盯什么。</p>
          </article>
        </section>
      </aside>
    </main>
  </article>
</body>
</html>
```

## Template 3: Lead Plus Briefs

Use when:

- one lead story is much stronger than everything else
- the rest should be compressed into fast-scanning briefs
- the page should feel calm rather than busy

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>私人编辑部</title>
  <style>
    @page { size: A4 portrait; margin: 14mm 12mm; }
    body {
      margin: 0;
      background: #f3f0e8;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
      color: #172033;
    }
    .sheet { width: 186mm; min-height: 269mm; margin: 0 auto; }
    .brand { font-size: 22pt; font-weight: 800; }
    .lead { margin-top: 5mm; padding: 6mm; background: #fff; border: 1px solid #e1dbcf; border-radius: 5mm; }
    .lead h1 { margin: 2mm 0 3mm; font-size: 22pt; line-height: 1.1; }
    .lead p, .brief p { margin: 0; color: #647086; font-size: 10pt; line-height: 1.65; }
    .briefs { display: grid; gap: 3.5mm; margin-top: 4mm; }
    .brief { padding: 4mm 4.5mm; background: #fff; border: 1px solid #e1dbcf; border-radius: 4mm; }
    .brief h2 { margin: 0 0 1.5mm; font-size: 11pt; }
    .source { margin-top: 1.8mm; font-size: 8.5pt; }
  </style>
</head>
<body>
  <article class="sheet">
    <header>
      <div class="brand">私人编辑部</div>
      <div>日期 · 主题 · 阅读时长</div>
    </header>

    <section class="lead">
      <div>Lead Story</div>
      <h1>这里放核心主线标题</h1>
      <p>用两到三句话讲清楚今天最重要的变化，以及它为什么值得被读者优先看见。</p>
      <p class="source">来源：原始链接</p>
    </section>

    <section class="briefs">
      <article class="brief">
        <h2>快讯一</h2>
        <p>压缩过的简讯内容。</p>
      </article>
      <article class="brief">
        <h2>明日关注</h2>
        <p>写观察点或下一步追踪方向。</p>
      </article>
    </section>
  </article>
</body>
</html>
```

## Template selection rule

Use these defaults:

1. If the user does not specify layout, start with `Template 2: Editorial Two Column`.
2. If there is only one major theme and few items, use `Template 1` or `Template 3`.
3. If the user wants a calm one-page brief, reduce density before adding more sections.
4. If the user asks for stronger personality, keep the structure and upgrade typography, labels, and section framing before increasing complexity.

## Packaging upgrade rule

If the user wants the result to feel more eye-catching:

1. keep the chosen template
2. add one editorial packaging mode such as `Headliner`, `Signal Board`, or `What It Means`
3. strengthen section labels and lead summary wording
4. keep source links visible for all sourced news items
5. avoid shock-style language, alarmist color choices, and crowded layouts
