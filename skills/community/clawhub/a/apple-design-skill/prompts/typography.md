# Typography Engine

This module defines the multi-language font system for Apple-style UI generation. It provides font stacks for five language environments, a type scale, and detailed spacing rules. All typographic tokens reference `design-tokens.md` for weight, letter-spacing, and line-height values.

> **Usage:** Detect the user's language from their prompt, select the matching font stack, and apply the corresponding CSS. Always include the Google Fonts `<link>` tags as a fallback for environments where Apple system fonts are unavailable.

---

## 1. Multi-Language Font Stacks

Each language environment defines a `display` stack (for headings), a `text` stack (for body copy), and a Google Fonts open-source fallback.

```json
{
  "fontStacks": {
    "en": {
      "display": "'SF Pro Display', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
      "text": "'SF Pro Text', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
      "fallback_google": "'Inter', sans-serif"
    },
    "zh-CN": {
      "display": "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
      "text": "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
      "fallback_google": "'Noto Sans SC', sans-serif"
    },
    "zh-TW": {
      "display": "'PingFang TC', 'Hiragino Sans CNS', 'Microsoft JhengHei', sans-serif",
      "text": "'PingFang TC', 'Hiragino Sans CNS', 'Microsoft JhengHei', sans-serif",
      "fallback_google": "'Noto Sans TC', sans-serif"
    },
    "ja": {
      "display": "'Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'Yu Gothic', 'Meiryo', sans-serif",
      "text": "'Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'Yu Gothic', 'Meiryo', sans-serif",
      "fallback_google": "'Noto Sans JP', sans-serif"
    },
    "ko": {
      "display": "'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif",
      "text": "'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif",
      "fallback_google": "'Noto Sans KR', sans-serif"
    }
  }
}
```

### Applying font stacks in CSS

Use CSS custom properties so the correct stack is injected once and referenced everywhere.

**English (en):**

```css
:root[lang="en"], :root:lang(en) {
  --apple-font-display: 'SF Pro Display', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
  --apple-font-text: 'SF Pro Text', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
}
```

**Simplified Chinese (zh-CN):**

```css
:root[lang="zh-CN"], :root:lang(zh-CN) {
  --apple-font-display: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  --apple-font-text: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
}
```

**Traditional Chinese (zh-TW):**

```css
:root[lang="zh-TW"], :root:lang(zh-TW) {
  --apple-font-display: 'PingFang TC', 'Hiragino Sans CNS', 'Microsoft JhengHei', sans-serif;
  --apple-font-text: 'PingFang TC', 'Hiragino Sans CNS', 'Microsoft JhengHei', sans-serif;
}
```

**Japanese (ja):**

```css
:root[lang="ja"], :root:lang(ja) {
  --apple-font-display: 'Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'Yu Gothic', 'Meiryo', sans-serif;
  --apple-font-text: 'Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'Yu Gothic', 'Meiryo', sans-serif;
}
```

**Korean (ko):**

```css
:root[lang="ko"], :root:lang(ko) {
  --apple-font-display: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
  --apple-font-text: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
}
```

---

## 2. Google Fonts Fallback

When Apple system fonts are unavailable (Linux, older Windows, web-only environments), load these open-source alternatives via Google Fonts. Always include the appropriate `<link>` tags in generated HTML.

| Language | System Font | Google Fonts Alternative |
|----------|------------|--------------------------|
| en | SF Pro Display / Text | Inter |
| zh-CN | PingFang SC | Noto Sans SC |
| zh-TW | PingFang TC | Noto Sans TC |
| ja | Hiragino Sans | Noto Sans JP |
| ko | Apple SD Gothic Neo | Noto Sans KR |

### Google Fonts `<link>` tags

Include only the tags needed for the detected language. For multi-language pages, combine them.

```html
<!-- English fallback -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Simplified Chinese fallback -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Traditional Chinese fallback -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Japanese fallback -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Korean fallback -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
```

When Google Fonts are loaded, append them to the font stack so they act as the final named fallback before the generic `sans-serif`:

```css
/* Example: English with Google Fonts fallback */
:root[lang="en"] {
  --apple-font-display: 'SF Pro Display', 'Helvetica Neue', 'Helvetica', 'Arial', 'Inter', sans-serif;
  --apple-font-text: 'SF Pro Text', 'Helvetica Neue', 'Helvetica', 'Arial', 'Inter', sans-serif;
}
```

---

## 3. Font Size Scale

The type scale follows Apple's convention: oversized hero headlines, clear subtitles, comfortable body text, and compact captions.

```css
:root {
  /* Hero / large display headings: 48px – 80px */
  --apple-font-size-hero: 56px;
  --apple-font-size-hero-min: 48px;
  --apple-font-size-hero-max: 80px;

  /* Subtitles / section headings: 24px – 32px */
  --apple-font-size-subtitle: 28px;
  --apple-font-size-subtitle-min: 24px;
  --apple-font-size-subtitle-max: 32px;

  /* Body text: 17px – 21px */
  --apple-font-size-body: 17px;
  --apple-font-size-body-min: 17px;
  --apple-font-size-body-max: 21px;

  /* Caption / auxiliary text: 12px – 14px */
  --apple-font-size-caption: 12px;
  --apple-font-size-caption-min: 12px;
  --apple-font-size-caption-max: 14px;
}
```

### Responsive sizing

Scale hero and subtitle sizes down on smaller viewports:

```css
h1, .hero-headline {
  font-family: var(--apple-font-display);
  font-size: var(--apple-font-size-hero-min);       /* mobile default */
  font-weight: var(--apple-weight-title-bold);       /* 700 from design-tokens.md */
  line-height: var(--apple-leading-title);           /* 1.1 from design-tokens.md */
  letter-spacing: var(--apple-tracking-en-title);    /* -0.015em from design-tokens.md */
}

@media (min-width: 734px) {
  h1, .hero-headline {
    font-size: var(--apple-font-size-hero);          /* 56px */
  }
}

@media (min-width: 1068px) {
  h1, .hero-headline {
    font-size: var(--apple-font-size-hero-max);      /* 80px */
  }
}
```

---

## 4. Letter Spacing

Letter spacing differs by language and text role. These tokens are defined in `design-tokens.md` and referenced here for context.

| Context | Token | Value | Notes |
|---------|-------|-------|-------|
| Chinese headings | `--apple-tracking-zh-title` | 0.04em | Slightly open for CJK legibility |
| English headings (default) | `--apple-tracking-en-title` | -0.015em | Tight, editorial feel |
| English headings (tight) | `--apple-tracking-en-title-tight` | -0.02em | Maximum tightness |
| English headings (loose) | `--apple-tracking-en-title-loose` | 0.01em | Slightly open for short words |
| Body text | `--apple-tracking-body` | 0em | Normal tracking |

**Rule:** When the detected language is `zh-CN`, `zh-TW`, or `ja`, apply `--apple-tracking-zh-title` to headings. For `en` and `ko`, apply `--apple-tracking-en-title`.

---

## 5. Line Height

Line height tokens are defined in `design-tokens.md`. The rules below specify when to use each value.

| Context | Token | Value | Notes |
|---------|-------|-------|-------|
| Headings (default) | `--apple-leading-title` | 1.1 | Compact multi-line headlines |
| Headings (tight) | `--apple-leading-title-tight` | 1.05 | Single-line hero text |
| Headings (loose) | `--apple-leading-title-loose` | 1.15 | Multi-line subtitles |
| Body text (default) | `--apple-leading-body` | 1.53 | Comfortable reading |
| Body text (tight) | `--apple-leading-body-tight` | 1.5 | Compact paragraphs |
| Body text (loose) | `--apple-leading-body-loose` | 1.58 | Long-form content |

**Rule:** Headings always use `--apple-leading-title` (range 1.05–1.15). Body text always uses `--apple-leading-body` (range 1.5–1.58).

---

## 6. Font Weight

Font weight tokens are defined in `design-tokens.md`. Apply them as follows:

| Context | Token | Value | Notes |
|---------|-------|-------|-------|
| Hero headlines (English) | `--apple-weight-title-bold` | 700 | Standard bold for Latin scripts |
| Hero headlines (Chinese/CJK) | `--apple-weight-title-black` | 900 | **Extra-black for CJK hero text — this is critical.** Apple's Chinese site uses very heavy weights for impact. |
| Section headings (English) | `--apple-weight-title` | 600 | Semibold |
| Section headings (Chinese/CJK) | `--apple-weight-title-heavy` | 800 | Heavy weight for CJK section headings |
| Body text | `--apple-weight-body` | 400 | Regular |
| Emphasized body | `--apple-weight-body-medium` | 500 | Medium |

### CJK Font Weight Override Rule

**CRITICAL:** When the detected language is `zh-CN`, `zh-TW`, `ja`, or `ko`, you MUST increase heading font weights:

- Hero headlines (h1): use `font-weight: 900` (`--apple-weight-title-black`)
- Section headings (h2): use `font-weight: 800` (`--apple-weight-title-heavy`)
- Feature card titles (h3): use `font-weight: 700` (`--apple-weight-title-bold`)

This is because CJK fonts at weight 600-700 appear visually thinner than their Latin counterparts. Apple's own Chinese site compensates by using heavier weights. The result should feel bold, professional, and full of energy — not thin or weak.

```css
/* CJK font weight overrides — apply when lang is zh-CN, zh-TW, ja, or ko */
:root:lang(zh-CN) h1, :root:lang(zh-TW) h1, :root:lang(ja) h1, :root:lang(ko) h1,
[lang="zh-CN"] h1, [lang="zh-TW"] h1, [lang="ja"] h1, [lang="ko"] h1 {
  font-weight: 900; /* --apple-weight-title-black */
}

:root:lang(zh-CN) h2, :root:lang(zh-TW) h2, :root:lang(ja) h2, :root:lang(ko) h2,
[lang="zh-CN"] h2, [lang="zh-TW"] h2, [lang="ja"] h2, [lang="ko"] h2 {
  font-weight: 800; /* --apple-weight-title-heavy */
}
```

Also ensure Google Fonts fallback loads the heavy weights:

```html
<!-- Simplified Chinese fallback — include weight 900 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
```

**Rule:** For English, title weights range from 600 to 700. For CJK languages, title weights range from 700 to 900. Body weights are always 400–500 regardless of language.

---

## 7. Language Detection Logic

When generating Apple-style UI, follow this procedure to select the correct typographic settings:

### Detection rules

1. **Examine the user's prompt language.** If the user writes in a specific language, use that language's font stack.
2. **Check for explicit `lang` attribute requests.** If the user specifies a language code (e.g., "use zh-CN"), apply that directly.
3. **Character-based detection fallback:**
   - If the text contains CJK Unified Ideographs (U+4E00–U+9FFF):
     - Check for Simplified Chinese indicators (simplified-only characters or explicit zh-CN context) → use `zh-CN`
     - Check for Traditional Chinese indicators (traditional-only characters or explicit zh-TW context) → use `zh-TW`
     - If ambiguous, default to `zh-CN`
   - If the text contains Hiragana (U+3040–U+309F) or Katakana (U+30A0–U+30FF) → use `ja`
   - If the text contains Hangul (U+AC00–U+D7AF) → use `ko`
   - Otherwise → use `en`
4. **Default:** If language cannot be determined, fall back to `en`.

### Application procedure

Once the language is detected:

1. Set the `lang` attribute on the `<html>` element: `<html lang="detected-language">`.
2. Inject the corresponding font stack CSS custom properties from Section 1.
3. Include the matching Google Fonts `<link>` tag from Section 2.
4. Apply the correct letter-spacing token:
   - `zh-CN`, `zh-TW`, `ja` → `--apple-tracking-zh-title` for headings
   - `en`, `ko` → `--apple-tracking-en-title` for headings
5. All other typographic tokens (size, weight, line-height) are language-independent — apply them uniformly.

### Multi-language pages

For pages that mix languages (e.g., English headings with Chinese body text):

- Set the primary `lang` on `<html>` based on the dominant language.
- Use `lang` attributes on individual elements to override: `<p lang="zh-CN">中文段落</p>`.
- Load Google Fonts for all languages present on the page.
- Apply font-stack overrides at the element level using scoped CSS or inline styles.

---

## Quick Reference

| Property | Headings | Body |
|----------|----------|------|
| Font size | 48–80px (hero), 24–32px (subtitle) | 17–21px (body), 12–14px (caption) |
| Font weight | 600–700 | 400–500 |
| Line height | 1.05–1.15 | 1.5–1.58 |
| Letter spacing (en) | -0.02em to 0.01em | 0em |
| Letter spacing (zh/ja) | 0.04em | 0em |
