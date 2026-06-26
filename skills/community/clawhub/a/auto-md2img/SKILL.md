---
name: auto-md2img
emoji: 🖼️
description: Convert Markdown content to images automatically with GitHub styling, full Chinese support, smart pagination, emoji support, and syntax highlighting. Supports height-based pagination and JPEG quality adjustment.
author: OpenClaw Community
version: 1.3.1
license: MIT
tags: ["markdown", "image", "convert", "md2img", "puppeteer", "pagination", "quality", "chinese"]
---

# 🥑 Auto MD2IMG Skill

Automatically converts Markdown content to images for sending in any messaging platform, improving reading experience.

---

## ✨ Features

- 🖼️ Automatically converts Markdown to high-definition images
- 📄 Supports smart pagination, up to 500 lines per page
- 📏 **New: Height-based pagination mode** (line count independent, split by pixel height threshold)
- 🧱 Splits by content blocks, does not cut off headings, code blocks, tables, etc.
- 🔢 Automatically adds page number annotations
- 🀄 Perfect support for Chinese fonts
- 😊 Supports colored Emoji
- 🎨 GitHub-style rendering
- 📸 Auto-detect JPEG/PNG format, supports quality adjustment
- 🔍 Debug mode, output detailed logs and save pagination content
- ⚡ Background browser management, improved performance for repeated conversions
- 🧹 Automatic cache cleaning, privacy protection

---

## 📖 Usage

When you need to reply to users with Markdown formatted content:

### Basic Usage

1. Save Markdown content to a temporary file (or pass string directly)
2. Call `scripts/md_to_png.js` to generate images
3. Send images to users using `<img>` tags
4. Embed paths using corresponding image tags for different messaging platforms
5. Fall back to sending plain text Markdown if image generation fails

### Script Invocation

```bash
# Basic usage
node scripts/md_to_png.js input.md

# Specify output directory
node scripts/md_to_png.js input.md ./output

# Custom lines per page
node scripts/md_to_png.js input.md ./output 300

# Custom JPEG quality (1-100, default 80)
node scripts/md_to_png.js input.md ./output 300 75

# Height-based pagination (custom height threshold in pixels, e.g. 2000px)
node scripts/md_to_png.js input.md ./output --height 2000

# Disable pagination entirely (output single image)
node scripts/md_to_png.js input.md ./output --height 0

# Enable Debug mode (output detailed logs + save pagination content)
node scripts/md_to_png.js input.md ./output --debug
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `inputFile` | string | ✅ | - | Path to input Markdown file |
| `outputDir` | string | ❌ | Current directory | Output image directory |
| `maxLinesPerPage` | number | ❌ | 500 | Maximum lines per page (line-based pagination) |
| `imageQuality` | number | ❌ | 80 | JPEG image quality (1-100) |
| `--height <px>` | number | ❌ | - | Height-based pagination threshold in pixels. ≤0 disables pagination entirely (single output image). Overrides line-based pagination. |
| `--debug` | flag | ❌ | - | Enable Debug mode, output detailed logs and save intermediate pagination content |

---

## 🔧 Configuration

### Font Configuration
- Default fonts: WenQuanYi Micro Hei, WenQuanYi Zen Hei, Noto CJK SC, Noto Color Emoji
- Supports system font fallback

### Output Configuration
- Output resolution: 2x (HD)
- Maximum width: 900px
- Automatically adapts to content height
- PNG format output

### Pagination Configuration
- Default maximum lines per page: 500 (line-based pagination)
- **Height-based pagination**: Split by pixel threshold (`--height` parameter), independent of line count
- Smart splitting by content blocks
- Does not cut off headings, code blocks, quotes, tables, lists
- Disable pagination entirely by setting `--height 0`

### Debug Mode
When enabled with `--debug` flag:
- Outputs detailed processing logs (content block detection, split points, rendering steps)
- Saves intermediate HTML render files for debugging
- Saves raw pagination split content as separate text files
- Includes timing metrics for performance analysis

---

## 📂 Script Paths

`scripts/md_to_png.js` - Main Markdown to image tool

`scripts/md_to_png.js` Functions:
- Reads Markdown files
- Smart content block splitting
- HTML rendering
- Puppeteer screenshot
- Cache cleaning

---

## 🎯 Usage Examples

### Example 1: Simple Conversion

```javascript
import { exec } from 'child_process';
import path from 'path';

const markdownContent = `# Hello World\n\nThis is test content.`;

// Save to temporary file
const tempFile = path.join('/tmp', 'temp.md');
fs.writeFileSync(tempFile, markdownContent);

// Call conversion script
exec(`node scripts/md_to_png.js ${tempFile}`, (error, stdout, stderr) => {
  if (error) {
    console.error('Conversion failed:', error);
    return;
  }
  console.log('Conversion successful:', stdout);
});
```

### Example 2: Usage in Chat Applications

```javascript
// When needing to reply with Markdown content
async function replyWithMarkdown(content, outputDir) {
  try {
    // Call md2img conversion
    const baseName = `reply_${Date.now()}`;
    const files = await convertMarkdown(content, outputDir, baseName);
    
    // Send images using <img> tags
    for (const file of files) {
      await sendMessage(`<img src="${file.path}">`);
    }
  } catch (error) {
    // Fall back to plain text on failure
    await sendMessage(content);
  }
}
```

### Example 3: Height-based Pagination

```bash
# Split by 2000px height, ideal for mobile viewing
node scripts/md_to_png.js long_article.md ./output --height 2000

# No pagination, output single long image
node scripts/md_to_png.js short_note.md ./output --height 0

# JPEG quality adjustment for faster sharing
node scripts/md_to_png.js report.md ./output 500 60 --height 1500
```

### Example 4: Debug Mode

```bash
# Debug mode for troubleshooting conversion issues
node scripts/md_to_png.js problem_content.md ./output --debug
```

---

## 🔒 Security Features

- ✅ Path traversal protection (output directory whitelist)
- ✅ Filename sanitization (illegal character replacement)
- ✅ Content size limit (max 10MB)
- ✅ Line count range validation (10-10000)
- ✅ Configurable cache cleaning policy

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| First browser startup | ~260ms |
| Small document conversion (200 words) | ~2.3s |
| Medium document conversion (2KB) | ~2.6s |
| Large document conversion (5KB) | ~3.6s |
| Repeated conversion performance improvement | 4.5% (single) / 50-70% (batch) |

---

## 🎨 Rendering Effects

Supported Markdown elements:
- ✅ Headings (H1-H6)
- ✅ Text styles (bold, italic, strikethrough, inline code)
- ✅ Code blocks (syntax highlighting)
- ✅ Lists (ordered, unordered)
- ✅ Tables
- ✅ Quote blocks
- ✅ Links
- ✅ Images
- ✅ Emoji

## 🆕 New in v1.3.1

- 📏 Height-based pagination mode (pixel-based splitting, no line count dependency)
- 📸 JPEG quality adjustment (1-100, balance between quality and file size)
- 🔍 Debug mode for troubleshooting conversion issues
- ⚡ 50%+ performance improvement for repeated conversions
- 🧹 More aggressive cache cleaning for better privacy
- 📁 **Auto directory creation**: Automatically creates output directories if they don't exist (no manual setup needed)
- 🐛 Fixed ENOENT error when output directory doesn't exist
- 🐛 Fixed "png screenshots do not support quality" error
- 🐛 Fixed JPEG quality setting not working issue

---

## 🛠️ Tech Stack

- Node.js >= 14
- Puppeteer (headless browser)
- marked (Markdown parsing)
- GitHub style CSS

---

## 📝 Trigger Scenarios

All reply scenarios that require outputting Markdown formatted content:
- Code snippet sharing
- Technical document replies
- Tabular data display
- List organization
- Long text formatting
- Use skill-cn.md when user inputs Chinese

---

## ⚠️ Notes

1. First conversion requires browser startup, slightly slower
2. Recommend enabling `skipCacheClear` configuration for batch conversions
3. Large documents may be split into multiple pages
4. Image files occupy disk space, remember to clean up

---

## Chinese Instructions (中文说明)

### Usage
When you need to reply to users with Markdown formatted content:
1. First save Markdown content to a temporary file (or pass string directly)
2. Call `scripts/md_to_png.js` to generate images
3. Send images to users using `<img>` tags
4. Embed paths using corresponding image tags for different messaging platforms
5. Fall back to sending plain text Markdown if image generation fails

### Script Path
`scripts/md_to_png.js` - Markdown to image tool

### Configuration
- Default fonts: WenQuanYi Micro Hei, WenQuanYi Zen Hei, Noto CJK SC, Noto Color Emoji
- Output resolution: 2x, clearer images
- Maximum width: 900px
- Automatically adapts to content height
- Default maximum lines per page: 500 lines

---

**Auto MD2IMG Skill - Make Markdown replies more beautiful!** 🎉
