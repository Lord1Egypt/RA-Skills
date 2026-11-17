# Manual JSON examples

Use these **only** for Path B manual fill: `get_template` → `get_template_structure` → `generate_carousel` / `generate_graphic` → `check_job_status`.

Element keys and graphic `label`s must match `get_template_structure` exactly. Drop fields the template does not have; add fields it does.

**Do not use the legacy `carousel` key** (flat `heading` / `description` / `image` on the slide). Always pass `carousel_content` with typed `elements`.

---

## Carousel — `carousel_content`

File: [examples/carousel_content.json](examples/carousel_content.json)

Pass the file contents as `carousel_content` to `generate_carousel` (not wrapped in another `carousel_content` key).

| Field | Type | Notes |
|-------|------|--------|
| `carousel_topic` | string | Optional |
| `intro_slide.elements` | object | First slide. Keys = template slot names |
| `slides[].elements` | object | Middle slides |
| `ending_slide.elements` | object | Last slide |

Each element:

```json
{ "type": "text", "value": "..." }
{ "type": "image", "value": "https://..." }
{ "type": "image", "value": "https://assets.contentdrips.com/loading_gradient.webp", "via": "unsplash", "image_query": "workspace desk" }
```

Carousel element `type` is `"text"` or `"image"` — not `"textbox"`.

---

## Graphic — `content_update`

File: [examples/content_update.json](examples/content_update.json)

Pass the array as `content_update` to `generate_graphic`.

| `type` | Required | Optional |
|--------|----------|----------|
| `textbox` | `label`, `value` | `fontSize`, `fontColor`, `textboxMaxHeight` (`"auto"` or px number) |
| `image` | `label`, `value` (https URL) | `opacity` (0–1) |
| `shape` | `label` | `fill`, `opacity` |

Graphic `type` is `"textbox"`, `"image"`, or `"shape"` — not `"text"`.

---

## Optional branding (both tools)

```json
{
  "name": "Jane Doe",
  "handle": "@janedoe",
  "bio": "Content strategist",
  "website_url": "https://janedoe.com",
  "avatar_image_url": "https://example.com/avatar.jpg"
}
```
