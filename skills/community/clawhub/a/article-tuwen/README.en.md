# Article Tuwen — One-Shot Article to Social Cards

> 📸 Give me raw material, get back a complete set of social cards

[中文](./README.md) | English

---

## ✨ One-Liner

Article Tuwen is a **zero-confirmation, fully automatic** pipeline: feed it URLs, files, or text, and it writes a 4000-word article, renders layouts, screenshots 5-9 social cards (1080×1440), and produces an 800-1000 char compressed text summary. No pauses, no confirmations — end to end.

## 🎯 Problem Solved

- Writing + formatting + screenshotting long-form content is tedious
- Xiaohongshu / WeChat card styles are inconsistent across posts
- Every content piece starts from scratch
- Repeated outputs look too similar

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| **Zero-confirmation pipeline** | 4 phases, fully automatic, no user checkpoints |
| **Diversity rotation** | 8 cover + 8 closing search terms + 5 theme pools, auto-dedup against last 3 runs |
| **Screenshot safety** | Kill stale servers before capture, verify file size to prevent blanks |
| **Font size iron rules** | Body ≥ 30px, auxiliary ≥ 26px, meta ≥ 22px |
| **Density iron rules** | Active composition ≥ 78% canvas height, no center-padding |
| **Dual delivery** | Desktop folder + Feishu cloud sync |

## ⚡ Quick Start

### Trigger

In your AI coding assistant, say:

```
转写成图文
```

Then paste URLs, file paths, or raw text.

### Output Example

```
C:\Users\Administrator\Desktop\mimo公众号配图\
├── p1.png ~ p9.png        # 9 social cards (1080×1440)
├── mimo-article.md         # Long-form source
├── mimo-文字稿.txt          # 800-1000 char compressed text
└── used-images.json        # Image source log
```

Plus a Feishu cloud drive link for mobile access.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Article Tuwen Pipeline                 │
│                                                         │
│  Phase 1          Phase 2          Phase 3          Phase 4          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │ Ingest &  │ →  │ Diversity │ →  │ Render &  │ →  │ Deliver & │   │
│  │ Write     │    │ Check     │    │ Screenshot│    │ Record    │   │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘   │
│                                                         │
│  Input: URL/File/Text        Output: PNG + MD + TXT + Feishu URL  │
└─────────────────────────────────────────────────────────┘
```

### Phase Breakdown

| Phase | Responsibility | Key Actions |
|-------|---------------|-------------|
| **1. Ingest** | Fetch material + write article | WebFetch / Read → 3500-4500 word article |
| **2. Diversity** | Read history.json, rotate cover/closing/theme/layout | 8+8+5 pools, differ from last 3 runs |
| **3. Render** | Assemble HTML → self-check → screenshot → text summary | Font/density rules, kill process before screenshot |
| **4. Deliver** | Desktop folder + Feishu cloud + update history | xcopy + lark-cli |

## 🎨 Themes & Layouts

### Theme Pools

| Category | Available Themes |
|----------|-----------------|
| **Editorial** (business/tech/analysis) | indigo-porcelain, ink-classic, kraft-paper, arctic-dawn, moss-stone |
| **Swiss** (career/tutorials/guides) | copper-oxide, slate-storm, sage-garden, wine-dark-sea, desert-rose |

### Layout Sequences

- First page: fixed M01/M02
- Last page: fixed M15/M16
- Middle pages: M03-M14 + C01-C10 (chart pages)
- No overlap with previous run's first 3 layouts

## ⚙️ Configuration

### history.json

Records each run's parameters, driving diversity rotation:

```json
{
  "runs": [...],
  "rotation": {
    "cover_pool": ["server room", "data center", ...],
    "closing_pool": ["abstract dark", "night city", ...],
    "theme_pool_editorial": ["indigo-porcelain", ...],
    "theme_pool_swiss": ["copper-oxide", ...],
    "next_cover_idx": 3,
    "next_closing_idx": 3,
    "next_theme_idx": 3
  }
}
```

### Font Size Rules

| Element | Minimum Size |
|---------|-------------|
| Body text | ≥ 30px |
| Auxiliary text | ≥ 26px |
| Meta information | ≥ 22px |
| Inner page titles | 52px (unified .h-md) |

### Density Rules

- Active composition ≥ 78% canvas height
- Append callout / data rows / annotation rows when sparse
- Pull Quote pages: no `justify-content: center`

## 📋 Example

**Input:**

```
转写成图文
https://example.com/mimo-release
https://example.com/mimo-benchmark
```

**Output:**

- 9 PNG cards (cover: "data center", theme: "ink-classic")
- mimo-article.md (long-form source)
- mimo-文字稿.txt (compressed text)
- Desktop mimo公众号配图/ folder
- Feishu cloud URL

## ⚠️ Limitations

- Windows only (PowerShell + python + node)
- Depends on xhs-crafter template assets
- Requires Feishu CLI (lark-cli) for cloud sync
- Screenshots depend on local HTTP server + screenshot.js
- No original writing, no video, no plain-text formatting

## 📝 Changelog

See [CHANGELOG.md](./CHANGELOG.md)

## 📄 License

[MIT-0](./LICENSE)
