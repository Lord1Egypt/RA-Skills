---
name: generatebot-templates
description: Design and render image templates for social media posts, blog headers, and marketing graphics via the GenerateBot API. Create canvas-based templates with dynamic text, brand colors, logos, and image placeholders, then render them as PNG/JPG. Use when the user wants to create post images, design social media graphics, build branded templates, generate Open Graph images, or render dynamic image content.
emoji: 🎨
homepage: https://generatebot.com
metadata:
  openclaw:
    primaryEnv: GENERATEBOT_API_KEY
    requires:
      env:
        - GENERATEBOT_API_KEY
---

## GenerateBot Templates - Design & Render Post Images

Base URL: `https://generatebot.com/api/v1`

Authentication: Bearer token in the Authorization header.
```
Authorization: Bearer GENERATEBOT_API_KEY
```

All request and response bodies use JSON. Set `Content-Type: application/json`.

---

### Quick Reference

| Action | Method | Path | Credits | Type |
|--------|--------|------|---------|------|
| Create template | POST | /templates | 0 | sync |
| List templates | GET | /templates | 0 | sync |
| Get template | GET | /templates/{id} | 0 | sync |
| Update template | PATCH | /templates/{id} | 0 | sync |
| Delete template | DELETE | /templates/{id} | 0 | sync |
| Render template | POST | /templates/{id}/render | 20 | sync |

---

### System Overview

Templates are canvas JSON documents with dynamic text and image slots. When rendered, the system substitutes placeholder content with real text and images, auto-fits text to its bounding box, and smart-fits images to cover their target areas. The output is a high-quality image (JPEG or PNG) uploaded to CDN.

---

### Canvas JSON Format

#### Top-Level Structure

```json
{
  "version": "5.3.0",
  "objects": [ ... ],
  "clipPath": {
    "type": "rect",
    "version": "5.3.0",
    "left": 0, "top": 0,
    "width": 1080, "height": 1920,
    "fill": "#0a0a0a",
    "scaleX": 1, "scaleY": 1
  }
}
```

- `version`: Always `"5.3.0"`
- `objects`: Ordered array of canvas objects (back-to-front rendering order)
- `clipPath`: Canvas-level clip boundary -- MUST match the `clip` rect dimensions and fill

#### The Clip Rect (Workspace)

Every template MUST have a `clip` rect as its first object. This defines the artboard:

```json
{
  "type": "rect",
  "version": "5.3.0",
  "originX": "left", "originY": "top",
  "left": 0, "top": 0,
  "width": 1080, "height": 1920,
  "fill": "#0a0a0a",
  "stroke": null, "strokeWidth": 0,
  "scaleX": 1, "scaleY": 1,
  "opacity": 1, "visible": true,
  "name": "clip",
  "selectable": false, "hasControls": false
}
```

**Common dimensions:**

| Format | Width | Height | Use Case |
|--------|-------|--------|----------|
| Portrait / Story | 1080 | 1920 | Instagram Stories, LinkedIn Stories |
| Square | 1080 | 1080 | Instagram Feed, LinkedIn Feed |
| Landscape | 1200 | 627 | LinkedIn Articles, Twitter/X |

#### Object Naming Convention

| Pattern | Type | Example | Purpose |
|---------|------|---------|---------|
| `{{key}}` | Dynamic | `{{title}}`, `{{primaryImage}}` | Replaced during rendering |
| Plain name | Static | `gradient_overlay_1`, `accent_line` | Fixed decorative elements |
| `clip` | Workspace | `clip` | Artboard boundary (exactly one) |

#### Image Objects

Image placeholders define where dynamic images appear. The `src` MUST use a 1x1 transparent pixel -- never an empty string.

```json
{
  "type": "image",
  "version": "5.3.0",
  "originX": "left", "originY": "top",
  "left": 0, "top": 0,
  "width": 1200, "height": 800,
  "scaleX": 0.9, "scaleY": 2.4,
  "opacity": 1, "visible": true,
  "name": "{{primaryImage}}",
  "selectable": true, "hasControls": true,
  "src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
  "crossOrigin": "anonymous",
  "filters": []
}
```

**Key rules:**
- `src` MUST be the 1x1 transparent pixel base64 shown above. Empty string `""` causes rendering failures.
- `crossOrigin` MUST be `"anonymous"`
- `filters` MUST be `[]` (empty array)
- `width`/`height` define unscaled dimensions; `scaleX`/`scaleY` scale to visual target size
- The renderer auto-fits the actual image to cover the target area (width*scaleX by height*scaleY)

**Circular image crop (optional):**

```json
{
  "type": "image",
  "name": "{{secondaryImage}}",
  "width": 300, "height": 300,
  "scaleX": 1, "scaleY": 1,
  "src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
  "crossOrigin": "anonymous", "filters": [],
  "clipPath": {
    "type": "circle",
    "version": "5.3.0",
    "radius": 140,
    "left": 0, "top": 0,
    "originX": "center", "originY": "center",
    "fill": "rgb(0,0,0)",
    "inverted": false, "absolutePositioned": false
  }
}
```

#### Textbox Objects

Use large `fontSize` directly -- never use `scaleX`/`scaleY` to size text.

```json
{
  "type": "textbox",
  "version": "5.3.0",
  "originX": "left", "originY": "top",
  "left": 70, "top": 1050,
  "width": 940, "height": 350,
  "fill": "rgba(255, 255, 255, 1)",
  "stroke": null, "strokeWidth": 0,
  "fontSize": 82, "fontFamily": "Arial", "fontWeight": 900,
  "text": "Headline Goes Here in Bold White Text",
  "textAlign": "left", "lineHeight": 1.08, "charSpacing": 0,
  "scaleX": 1, "scaleY": 1,
  "angle": 0, "opacity": 1, "visible": true,
  "name": "{{title}}",
  "selectable": true, "hasControls": true, "editable": true
}
```

**Key rules:**
- `fontSize` MUST be the actual desired size. Do NOT use scaleX/scaleY to enlarge text -- this breaks auto-fit.
- `scaleX` and `scaleY` MUST be `1` on text objects.
- `height` defines the maximum bounding box -- set it generously. The renderer shrinks text to fit.
- `width` defines the text wrapping width.

**Recommended font sizes by role:**

| Role | fontSize | fontWeight | Notes |
|------|----------|------------|-------|
| Title / Headline | 62-82 | 700-900 | Bold, high-impact |
| Description / Body | 32-42 | 400 | Regular weight |
| Label / Tag | 24-28 | 700 | Often with `charSpacing: 80-150` |
| Website / URL | 22-26 | 400-600 | Subtle, lower opacity |
| CTA | 24-28 | 600-700 | Right-aligned or centered |

#### Gradient Overlays

Gradient overlays create dark zones over images where text remains readable. Use a 400x400 base rect, scale it up with `scaleX`/`scaleY`, and flip vertically with `flipY: true` so the solid color sits at the bottom.

```json
{
  "type": "rect",
  "version": "5.3.0",
  "originX": "left", "originY": "top",
  "left": -20, "top": 540,
  "width": 400, "height": 400,
  "fill": {
    "type": "linear",
    "coords": {"x1": 200, "y1": 0, "x2": 200, "y2": 400},
    "colorStops": [
      {"offset": 0, "color": "rgba(0, 0, 0, 1)"},
      {"offset": 0.6, "color": "rgba(0, 0, 0, 0.75)"},
      {"offset": 0.9, "color": "rgba(0, 0, 0, 0)"}
    ],
    "offsetX": 0, "offsetY": 0, "gradientUnits": "pixels"
  },
  "stroke": null, "strokeWidth": 0,
  "scaleX": 2.85, "scaleY": 3.5,
  "flipY": true,
  "opacity": 1, "visible": true,
  "name": "gradient_overlay_1", "selectable": true
}
```

**Best practices:**
- **Stack TWO gradient rects** with slightly different positions and color stop distributions for visual depth
- `flipY: true` makes offset 0 (solid) appear at the bottom, offset 1 (transparent) at the top
- Gradient covers the bottom 60-70% of the canvas; text sits in the fully opaque zone
- Use `left: -20` to ensure full-width coverage after scaling

---

### Template Metadata

Describes which objects are dynamic and how they appear in the editor:

```json
{
  "fields": [
    {
      "key": "title",
      "objectName": "{{title}}",
      "label": "Title",
      "maxLength": 80,
      "required": true,
      "defaultValue": "Headline Goes Here in Bold White Text"
    }
  ],
  "imageSlots": [
    {
      "key": "primaryImage",
      "objectName": "{{primaryImage}}",
      "required": true
    }
  ]
}
```

**Rules:**
- Every `{{key}}` object in canvas JSON MUST have a matching entry in `fields` (text) or `imageSlots` (images)
- `objectName` MUST exactly match the object's `name` including `{{` and `}}`
- Maximum 20 fields, maximum 10 image slots
- `defaultValue` should match the `text` property of the corresponding textbox

**Standard variable names:**

| Key | Type | Purpose | Typical maxLength |
|-----|------|---------|-------------------|
| `title` | field | Main headline | 60-100 |
| `description` | field | Supporting text | 150-250 |
| `label` | field | Category tag (e.g., "BREAKING NEWS") | 20-30 |
| `website` | field | URL or domain | 30 |
| `cta` | field | Call to action (e.g., "Read Below") | 20-30 |
| `primaryImage` | imageSlot | Main hero image | - |
| `secondaryImage` | imageSlot | Supporting image (headshot, logo) | - |

---

### API Reference

#### POST /templates -- Create Template

```json
{
  "name": "News Card Dark",
  "description": "Dark cinematic news card with full-bleed hero image...",
  "category": "linkedin",
  "canvasJson": "{...stringified canvas JSON...}",
  "templateMetadata": {
    "fields": [...],
    "imageSlots": [...]
  }
}
```

**Validation:**
- `name`: 1-200 characters, required
- `description`: max 1000 characters, optional
- `category`: `"linkedin"` | `"instagram"` | `"article"`, required
- `canvasJson`: stringified JSON, max 500KB, must contain a `clip` object
- `templateMetadata.fields`: max 20 items
- `templateMetadata.imageSlots`: max 10 items

**Response (201):**
```json
{
  "success": true,
  "data": {
    "template": {
      "id": "uuid",
      "name": "News Card Dark",
      "description": "...",
      "category": "linkedin",
      "template_metadata": {...},
      "thumbnail_url": null,
      "created_at": "2026-04-10T..."
    }
  }
}
```

#### GET /templates -- List Templates

Query: `?category=linkedin&limit=10&offset=0`

Returns lightweight metadata (no `canvas_json`). Use GET by ID for the full template.

```json
{
  "success": true,
  "data": {
    "templates": [...],
    "pagination": { "total": 12, "limit": 10, "offset": 0, "hasMore": true }
  }
}
```

#### GET /templates/{id} -- Get Template

Returns full template including `canvas_json`.

#### PATCH /templates/{id} -- Update Template

Partial updates. Send only the fields to change (`name`, `category`, `canvasJson`, `templateMetadata`, `isActive`).

#### DELETE /templates/{id} -- Delete Template

Returns `{ "success": true, "data": { "deleted": true } }`.

#### POST /templates/{id}/render -- Render Template (20 credits)

```json
{
  "fields": {
    "title": "Breaking: AI Reaches New Milestone",
    "description": "Researchers announce breakthrough in reasoning capabilities.",
    "label": "TECH NEWS",
    "website": "technews.com"
  },
  "images": {
    "primaryImage": "https://example.com/hero.jpg"
  },
  "outputFormat": "jpeg",
  "quality": 0.9
}
```

- `fields`: key-value pairs matching template field keys (all strings)
- `images`: key-value pairs matching template image slot keys (HTTPS URLs only)
- `outputFormat`: `"jpeg"` (default) or `"png"`
- `quality`: 0.1-1.0, default 0.9

**Response:**
```json
{
  "success": true,
  "data": {
    "imageUrl": "https://generatebot.b-cdn.net/posts/...",
    "width": 1080,
    "height": 1920,
    "creditsConsumed": 20,
    "pipelineRunId": "uuid"
  }
}
```

---

### Text Auto-Fit

The renderer automatically shrinks text to fit within its bounding box:
1. Set `height` generously on textbox objects -- this is the max vertical space
2. Use the actual desired `fontSize` -- the renderer shrinks if text is longer than placeholder
3. Do not rely on `scaleX`/`scaleY` for text sizing -- keep both at `1`
4. Test with long text to verify auto-fit behavior

### Image Smart-Fit

The renderer scales images to cover their target area without distortion:
- Target area = `width * scaleX` by `height * scaleY`
- Image is scaled uniformly to fill (cover) the target area, centered
- Just provide the image URL at render time -- the system handles all sizing

---

### Design Patterns

**Pattern 1: Hero Image with Gradient Overlay (Dark Theme)**
Best for news, dramatic stories. Full-bleed hero image, two stacked gradient rects, bold white title, subtle description, label at top, website/CTA at bottom.

**Pattern 2: Square Card with Accent Line**
Best for feeds. 1080x1080, aggressive gradient, thin vertical accent line, large caps title, no description.

**Pattern 3: Editorial Clean (Light Theme)**
Best for thought leadership. Light background, colored label badge, serif title, hero image in bottom half.

**Pattern 4: Split Dual Image**
Best for comparisons. Two images separated by a colored title band.

---

### Critical Rules

1. Image `src` must NEVER be empty string. Always use: `data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=`
2. Text `scaleX` and `scaleY` must be `1`. Use `fontSize` for sizing.
3. The `clip` rect must be the first object with `name: "clip"`.
4. Canvas-level `clipPath` must match the clip rect's dimensions and fill.
5. Image objects must include `crossOrigin: "anonymous"` and `filters: []`.
6. Gradient overlays use 400x400 base size scaled via `scaleX`/`scaleY`. Never use full canvas dimensions directly.
7. Stack TWO gradient rects for depth -- single gradients look flat.
8. Set generous `height` on textboxes -- this is the auto-fit bounding box.
9. Category must be `"linkedin"`, `"instagram"`, or `"article"`.
10. `canvasJson` max size is 500KB.
11. Every `{{key}}` object must have a matching metadata entry.

### Available Fonts

`Arial, Arial Black, Verdana, Helvetica, Tahoma, Trebuchet MS, Times New Roman, Georgia, Garamond, Courier New, Brush Script MT, Palatino, Bookman, Comic Sans MS, Impact, Lucida Sans Unicode, Geneva, Lucida Console`

### Example: Create and Render a Template

**Step 1: Create**
```bash
curl -X POST https://generatebot.com/api/v1/templates \
  -H "Authorization: Bearer GENERATEBOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "News Card Dark",
    "description": "Dark cinematic news card",
    "category": "linkedin",
    "canvasJson": "{...stringified canvas JSON...}",
    "templateMetadata": {
      "fields": [
        {"key": "title", "objectName": "{{title}}", "label": "Title", "maxLength": 80, "required": true, "defaultValue": "Your Headline"}
      ],
      "imageSlots": [
        {"key": "primaryImage", "objectName": "{{primaryImage}}", "required": true}
      ]
    }
  }'
```

**Step 2: Render (20 credits)**
```bash
curl -X POST https://generatebot.com/api/v1/templates/TEMPLATE_ID/render \
  -H "Authorization: Bearer GENERATEBOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": { "title": "AI Breakthrough Announced Today" },
    "images": { "primaryImage": "https://example.com/hero.jpg" },
    "outputFormat": "jpeg",
    "quality": 0.9
  }'
```

---

### Error Handling

| HTTP Status | Meaning |
|-------------|---------|
| 401 | Invalid or missing API key |
| 402 | Insufficient credits |
| 429 | Rate limit exceeded -- wait and retry |
| 400 | Invalid request body -- check error details |
| 404 | Template not found |

All errors: `{ "error": { "code": "ERROR_CODE", "message": "..." }, "requestId": "..." }`

---

### Other GenerateBot Skills

- **Core Skill** (`generatebot-core`): Search, pipeline, RSS, content CRUD, and credits endpoints.
- **Video Skill** (`generatebot-video`): Detailed video creation tutorial with imageMode reference.
- **Publish Skill** (`generatebot-publish`): Social posting, CMS publishing, enrichment, brand voice, AI images.
- **Workflows Skill** (`generatebot-workflows`): End-to-end workflow patterns and usage mapping.