# Easy Image Skill Architecture

## Project File Structure

```
easy-image-skill/
├── SKILL.md                          # Main entry file (core flow definition)
├── docs/
│   └── architecture.md               # This document (architecture overview)
└── references/
    ├── model-selection.md            # Smart model selection rules
    ├── glossary.md                   # Professional terminology dictionary (300+ entries)
    ├── platforms/                    # Platform API configurations (6 platforms)
    │   ├── jiekou.md                 # Jiekou AI (Recommended for China)
    │   ├── novita.md                 # Novita
    │   ├── ppio.md                   # PPIO Cloud
    │   ├── openrouter.md             # OpenRouter
    │   ├── wavespeed.md              # WaveSpeed
    │   └── google.md                 # Google Imagen
    └── templates/                    # Domain templates (12 scenes)
        ├── ppt-slides.md             # PPT Graphics
        ├── marketing-poster.md       # Marketing Posters
        ├── product-photo.md          # Product Photos
        ├── scene-photo.md            # Scene Photos
        ├── report-illustration.md    # Report Illustrations
        ├── social-media-grid.md      # Social Media Grid
        ├── avatar.md                 # Avatar Design
        ├── badge-id.md               # Badge/ID Design
        ├── emoji-sticker.md          # Emoji/Sticker Design
        ├── intro-graphic.md          # Introduction Graphics
        ├── flowchart.md              # Flowcharts
        └── ui-prototype.md           # UI Prototypes
```

---

## Complete Request Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              User Input                                      │
│                    "Generate a latest iPhone 16 product photo"              │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 0: First-time Check                                                   │
│  ├─ Check if ~/.easy-image-skill/config.json exists                         │
│  ├─ Not exists → Start setup flow (select platform, config Key, save path)  │
│  └─ Exists → Continue execution                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 1: Smart Recognition                                                  │
│  ├─ Scene: Product photo                                                    │
│  ├─ Subject: iPhone 16                                                      │
│  ├─ Timeliness: latest ✓                                                    │
│  └─ Brand name: iPhone ✓                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 2: Check Personal Library                                             │
│  ├─ Query ~/.easy-image-skill/my-prompts.md                                 │
│  ├─ Match scene + keyword similarity                                        │
│  ├─ Match found (score > 0.3) → Silently reuse personal library template    │
│  └─ No match → Use public template references/templates/product-photo.md    │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 3: Check Information Completeness                                     │
│  ├─ Scene: Product photo ✓                                                  │
│  ├─ Subject: iPhone 16 ✓                                                    │
│  ├─ Size: Default 1:1 (product photo standard)                              │
│  └─ Information complete → Proceed to Step 4                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 4: Silent Translation                                                 │
│  ├─ Load template: references/templates/product-photo.md                    │
│  ├─ Query dictionary: references/glossary.md                                │
│  ├─ Select style preset: Clean/Minimal                                      │
│  └─ Assemble prompt:                                                        │
│     "clean professional product photography of iPhone 16,                   │
│      minimal white background, centered composition..."                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 5: Smart Model Selection                 Ref: references/model-selection.md │
│  ├─ Detected brand name "iPhone" → Trigger web search                       │
│  ├─ Detected timeliness "latest" → Confirm web search                       │
│  ├─ Select model: Gemini 3.1 Flash Image                                    │
│  └─ Enable Grounding: search_types = ["web", "image"]                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 6: Call API                              Ref: references/platforms/*.md │
│  ├─ Read config: ~/.easy-image-skill/config.json → platform = "jiekou"      │
│  ├─ Read Key: ~/.jiekou/config.json → api_key                               │
│  ├─ Construct request:                                                      │
│  │   {                                                                      │
│  │     "prompt": "clean professional product photography...",               │
│  │     "size": "1K",                                                        │
│  │     "aspect_ratio": "1:1",                                               │
│  │     "tools": [{"google_search": {"search_types": ["web", "image"]}}]     │
│  │   }                                                                      │
│  ├─ Send to: https://api.jiekou.ai/v3/gemini-3.1-flash-image-text-to-image  │
│  └─ Timeout: 300 seconds                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 7: Save and Display Result                                            │
│  ├─ Handle response (Base64 / URL)                                          │
│  ├─ Filename: product_iphone16_20260316_143052.png                          │
│  ├─ Save to: ~/Downloads/ (user configured path)                            │
│  └─ Display image + Ask if satisfied                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 8: Handle User Feedback                                               │
│  ├─ "satisfied" / "save it" → Save to personal library                      │
│  ├─ "change color" → Enter adjustment flow                                  │
│  └─ "no thanks" → End                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Module Responsibilities

### SKILL.md (Main Controller)
- Define 8-step execution flow
- First-time setup logic
- Intent recognition rules
- Adjustment flow
- Error handling

### references/model-selection.md (Model Selector)
- Web search trigger conditions (brand names, timeliness, reference descriptions)
- High-quality model trigger conditions (complex composition, professional photography, high-quality requirements)
- Priority rules: Web search > Complex composition > Default
- Keyword matching algorithm

### references/platforms/*.md (API Adapters)
- Platform-specific API Endpoints
- Request/Response formats
- Web search parameters (different per platform)
- Error code handling
- Timeout configuration (unified 300 seconds)

### references/templates/*.md (Prompt Templates)
- Scene default parameters (aspect ratio, style)
- Core element definitions
- Style presets (4-6 per scene)
- Prompt templates (with variable placeholders)

### references/glossary.md (Terminology Dictionary)
- English terminology
- Professional term translations
- 8 categories with 300+ entries

---

## Model Selection Decision Tree

```
User Prompt
    │
    ▼
┌─────────────────────────┐
│ Contains brand name?     │  iPhone, Nike, Huawei, Tesla...
│ Contains timeliness?     │  latest, trending, 2026...
│ Contains reference desc? │  like..., official style, realistic...
└─────────────────────────┘
    │
    ├─ YES (any match) ─────────────────────────────────────┐
    │                                                       ▼
    │                            ┌──────────────────────────────────────┐
    │                            │ Gemini 3.1 Flash Image + Grounding   │
    │                            │ • Enable Google Search               │
    │                            │ • search_types: ["web"] or           │
    │                            │   ["web", "image"] (for products)    │
    │                            └──────────────────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Contains complex comp?   │  multiple people, large scene, panorama...
│ (≥2 keywords)           │
│ Contains pro photo?      │  studio, commercial photography...
│ Contains high quality?   │  ultra HD, 8K, perfect, ultimate...
└─────────────────────────┘
    │
    ├─ YES (≥2 keywords match) ─────────────────────────────┐
    │                                                       ▼
    │                            ┌──────────────────────────────────────┐
    │                            │ Gemini 3 Pro Image                   │
    │                            │ • Highest image quality              │
    │                            │ • Excellent complex composition      │
    │                            │ • No web search support              │
    │                            └──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ Default Model                        │
│ Gemini 3.1 Flash Image (no Grounding)│
│ • Fast generation                    │
│ • General use cases                  │
└──────────────────────────────────────┘
```

---

## Configuration Files

```
User Config Directory
├── ~/.easy-image-skill/
│   ├── config.json          # Main config (platform, save path, frequent scenes)
│   └── my-prompts.md        # Personal prompt library
│
└── ~/.{platform}/
    └── config.json          # Platform API Key config

Main Config Example:
{
  "platform": "jiekou",
  "save_path": "~/Downloads",
  "frequent_scenes": ["product-photo", "ppt-slides"]
}

Platform Config Example:
{
  "api_key": "sk-xxx",
  "base_url": "https://api.jiekou.ai",
  "default_model": "gemini-3.1-flash-image",
  "timeout": 300,
  "enable_grounding": true
}
```

---

## Grounding Parameters by Platform

| Platform | Parameter Name | Enable Method |
|----------|---------------|---------------|
| Google | `tools` | `[{"google_search": {}}]` |
| Jiekou | `tools` | `[{"google_search": {"search_types": ["web", "image"]}}]` |
| OpenRouter | `plugins` | `[{"id": "web", "config": {"engine": "native"}}]` |
| Novita | `grounding` | `{"enabled": true, "search_types": ["web"]}` |
| PPIO | `search_grounding` | `{"enabled": true, "types": ["web"]}` |
| WaveSpeed | `web_search` | `{"enabled": true, "types": ["web"]}` |

---

## Data Flow

```
                    ┌─────────────────┐
                    │   User Input    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │   Scene     │  │   Subject   │  │   Style     │
    │ Recognition │  │ Extraction  │  │ Detection   │
    └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   Personal Library      │
              │   Matching              │
              │ ~/.easy-image-skill/    │
              │    my-prompts.md        │
              └───────────┬─────────────┘
                          │
            ┌─────────────┴─────────────┐
            │ Match               No Match │
            ▼                           ▼
    ┌───────────────┐          ┌───────────────┐
    │  Reuse        │          │  Load Public  │
    │  Personal     │          │  Template     │
    │  Library      │          │  references/  │
    │               │          │  templates/   │
    └───────┬───────┘          └───────┬───────┘
            │                          │
            └────────────┬─────────────┘
                         │
                         ▼
              ┌─────────────────────────┐
              │   Terminology           │
              │   Translation           │
              │  references/glossary.md │
              └───────────┬─────────────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │   Smart Model           │
              │   Selection             │
              │ references/             │
              │   model-selection.md    │
              └───────────┬─────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │ 3.1 Flash│     │ 3 Pro   │     │ 3.1 Flash│
    │+Grounding│     │(Quality)│     │(Default) │
    └────┬────┘     └────┬────┘     └────┬────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
              ┌─────────────────────────┐
              │   Platform API Call     │
              │  references/platforms/  │
              │      {platform}.md      │
              └───────────┬─────────────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │   Save & Display        │
              │   {save_path}/{file}    │
              └─────────────────────────┘
```

---

## Consistency Checklist

| Item | SKILL.md | platforms/*.md | Status |
|------|----------|----------------|--------|
| Timeout | 300 seconds | 300 seconds | ✅ Consistent |
| Default model | Gemini 3.1 Flash Image | Gemini 3.1 Flash Image | ✅ Consistent |
| Web search default | Enable as needed | enable_grounding: true | ✅ Consistent |
| Supported platforms | 6 | 6 files | ✅ Consistent |
| Template count | 12 | 12 files | ✅ Consistent |
| Poll interval | 2 seconds | - | ✅ |
| File naming | {scene}_{brief}_{timestamp}.png | - | ✅ |
