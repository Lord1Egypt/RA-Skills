# easy-image Workplace Image Generation Assistant

> Simple description → Professional prompt → High-quality image

## Features

### 1. Smart Translation

Automatically translates simple descriptions into professional prompts. Built-in **13 domain templates** covering **500+ professional prompts**.

**Web search enabled by default** for real-time information:
- Mention brands/products → Auto-search latest designs
- Mention characters/figures → Auto-search accurate appearances
- Mention style references → Auto-search visual examples

```
Input:  "Blue tech-style PPT cover"
Output: modern tech presentation cover, deep blue gradient background (#0a1929 to #1565c0),
        minimalist geometric elements, professional corporate style, 16:9 aspect ratio...
```

Supported domains: PPT graphics, marketing posters, product photography, scene photos, report illustrations, social media, avatars, badges, stickers, intro graphics, flowcharts, UI prototypes, exploded diagrams

### 2. Guided Completion

Intelligently identifies missing information, asks only essential questions, quickly generates professional-grade images.

| User Input | System Response |
|------------|-----------------|
| "Make me a product photo" | "Sure, what product?" |
| "Wireless earbuds" | "Got it, white background or scene shot?" |
| "White" | → Generate directly |

### 3. Multi-Platform Support

Supports 6 major image generation platforms, switch with one command:

| Platform | Command |
|----------|---------|
| Jiekou AI | "use Jiekou" |
| Novita | "switch to Novita" |
| PPIO | "use PPIO" |
| OpenRouter | "switch to OpenRouter" |
| WaveSpeed | "use WaveSpeed" |
| Google Imagen | "switch to Google" |

### 4. Personal Prompt Library

Say "save" when satisfied, auto-accumulates to personal library, prioritizes reuse for similar future requests.

```
"This looks great, save it" → Saved to ~/.easy-image-skill/my-prompts.md
Next time "make a similar product photo" → Auto-match and reuse
```

---

## Quick Start

### Installation

```bash
# Install via OpenClaw
claw install easy-image
```

### First-time Setup

Auto-enters setup guide on first use (~30 seconds):

1. **Select platform** → Default: Jiekou AI
2. **Configure API Key** → `my key is sk-xxx`
3. **Set save path** → Default: ~/Downloads
4. **Choose frequent scenes** → Optional, optimizes recommendations

Start generating after setup is complete.

---

## Internals

### Interaction Flow

```
User Input → Intent Recognition → Info Completion → Template Matching → Prompt Assembly → API Call → Save & Display
```

### Intent Recognition

| Element | Examples |
|---------|----------|
| Scene | PPT, poster, product photo... |
| Channel | Xiaohongshu→3:4, WeChat Moments→1:1, PPT→16:9 |
| Subject | Product name, person, scene description |
| Style | Tech, minimal, vintage... |

### Matching Logic

```
Priority: Personal Library (similarity>0.3) > Domain Templates > Default
```

Personal library matching: Scene match + keyword overlap calculation, silent reuse when similarity exceeds threshold.

### Model Selection

| Condition | Model |
|-----------|-------|
| Default | Gemini 3.1 Flash + Grounding (web search) |
| Complex composition / 8K HD | Gemini 3 Pro |
| Pure abstract description | Gemini 3.1 Flash (no search) |

---

**easy-image** — Let professionals focus on content, not prompt engineering
