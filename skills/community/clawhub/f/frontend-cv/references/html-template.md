# HTML Shell

The bundled renderer uses one shared document shell and swaps theme-specific CSS/layout behavior per preset.

## Shared Structure

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Name - 简历</title>
  <!-- Theme font links -->
  <style>
    /* Theme variables */
    /* Shared print/screen layout */
    /* Theme-specific overrides */
  </style>
</head>
<body>
  <div class="page theme--classic">
    <div class="top-note">更新于 2026年03月</div>

    <header class="resume-header">
      <h1 class="resume-name">Full Name</h1>
      <p class="resume-headline">Role / Focus</p>
      <div class="resume-connections">
        <a class="connection">...</a>
      </div>
    </header>

    <section class="section section--experience">
      <div class="section-heading">
        <h2 class="section-title">工作经历</h2>
      </div>
      <div class="section-body entry-list">
        <article class="entry entry--right-meta">
          <div class="entry-main">
            <div class="entry-title-line"><strong>Title</strong>, Company – Location</div>
            <div class="entry-subtitle">Optional subtitle</div>
            <ul class="highlights">
              <li>Impact bullet</li>
            </ul>
          </div>
          <div class="entry-meta">2023.04 – 至今</div>
        </article>
      </div>
    </section>
  </div>
</body>
</html>
```

## Theme Differences

- `classic`: centered header, blue ruled section titles, right metadata column.
- `modern`: left header, thick blue bar before section titles, left metadata rail.
- `sb2nov`: centered serif header, black rules, italic metadata.
- `engineeringclassic`: left header, lighter blue engineering styling, right metadata column.
- `engineeringresumes`: centered serif header, dense compact spacing, black rules.

## Guidance

- Keep the HTML single-file and self-contained.
- Preserve A4 print fidelity first; screen view is secondary.
- When showing previews, use the exact same renderer path as final export so previews and final output do not drift.
