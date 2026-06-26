# Scripts CLI Reference

## Runtime Resolution

Resolve `${BUN_X}` in this order:
1. `bun` is installed → use `bun`
2. `npx` available → use `npx -y bun`
3. Neither → halt + explain:
   ```
   Bun runtime required.
   Install: curl -fsSL https://bun.sh/install | bash
   Or via npm: npm install -g bun
   ```

`{baseDir}` = directory containing this SKILL.md.

---

## wechat-api.ts — Article via API

```bash
${BUN_X} {baseDir}/scripts/wechat-api.ts <file.md|file.html> \
  --theme <theme> \
  [--color <color>] \
  [--title <title>] \
  [--summary <summary>] \
  [--author <author>] \
  [--cover <cover_path>] \
  [--account <alias>] \
  [--no-cite]
```

**API endpoint**: `POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN`

**Payload fields**:
- `article_type`: `news` (default) or `newspic`
- `thumb_media_id`: required for `news`
- `need_open_comment`: resolved from config
- `only_fans_can_comment`: resolved from config
- `author`: CLI → frontmatter → EXTEND

**CRITICAL**: Pass the original `.md` file — do NOT pre-convert to HTML. The script handles conversion internally to keep image handling correct.

---

## wechat-article.ts — Article via Browser

```bash
# Markdown input
${BUN_X} {baseDir}/scripts/wechat-article.ts \
  --markdown <file.md> \
  --theme <theme> \
  [--color <color>] \
  [--account <alias>] \
  [--no-cite]

# HTML input
${BUN_X} {baseDir}/scripts/wechat-article.ts \
  --html <file.html> \
  [--account <alias>]
```

Use browser method when:
- API credentials unavailable
- User specifically wants browser flow
- Article needs manual visual confirmation

---

## wechat-browser.ts — Image-text Post (图文/贴图)

```bash
# With markdown + image directory
${BUN_X} {baseDir}/scripts/wechat-browser.ts \
  --markdown <article.md> \
  --images <./images/>

# With explicit title + content + single image
${BUN_X} {baseDir}/scripts/wechat-browser.ts \
  --title "标题" \
  --content "内容" \
  --image <img.png> \
  --submit
```

Supports up to 9 images. No humanization pass for image-text mode.

---

## md-to-wechat.ts — Markdown to WeChat HTML (standalone)

```bash
${BUN_X} {baseDir}/scripts/md-to-wechat.ts <file.md> \
  --theme <theme> \
  [--color <color>] \
  [--output <output.html>]
```

Use when you need the converted HTML without publishing (e.g., for manual review or external paste).

---

## check-permissions.ts — Environment Preflight

```bash
${BUN_X} {baseDir}/scripts/check-permissions.ts
```

Checks:
- Chrome presence
- Chrome profile isolation
- Bun runtime
- macOS Accessibility permissions
- Clipboard copy
- Paste keystroke (Linux: requires `xdotool` or `ydotool`)
- API credentials
- Chrome conflicts (multiple instances)

**Run before first use on a new machine.**

---

## Feature Matrix

| Feature | Image-Text | Article (API) | Article (Browser) |
|---------|:----------:|:-------------:|:-----------------:|
| Plain text input | ✗ | ✓ | ✓ |
| HTML input | ✗ | ✓ | ✓ |
| Markdown input | title+content | ✓ | ✓ |
| Humanization pass | ✗ | ✓ | ✓ |
| WeChat readability cleanup | ✗ | ✓ | ✓ |
| Multiple images | ✓ up to 9 | ✓ inline | ✓ inline |
| Themes | ✗ | ✓ | ✓ |
| Auto-generate metadata | ✗ | ✓ | ✓ |
| Default cover fallback | ✗ | ✓ | ✗ |
| Comment control | ✗ | ✓ | ✗ |
| Requires Chrome | ✓ | ✗ | ✓ |
| Requires API credentials | ✗ | ✓ | ✗ |
| Access token cache | — | ✓ | — |
| Speed | Medium | Fast | Slow |
