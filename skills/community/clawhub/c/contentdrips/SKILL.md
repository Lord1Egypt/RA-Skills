---
name: contentdrips
description: >-
  Connect OpenClaw to ContentDrips MCP for social media design and publishing.
  MAIN FLOW: ask AI Design Agent (new blank, or override on a template) vs AI
  carousel/graphic maker (template ID + keep layout, fill topic/URL). Always
  get_template_structure before generate_ai_*. Platforms explicit. Use when
  creating designs, posts, or publishing to LinkedIn/Instagram.
---

# ContentDrips MCP Skill

ContentDrips MCP connects your agent to [ContentDrips](https://contentdrips.com) — create designs, generate AI carousels/graphics, run the AI Design Agent, manage posts, and publish to LinkedIn and Instagram through conversation.

**MCP URL:** `https://mcp.contentdrips.com/mcp`

**Triggers:** contentdrips, carousel, graphic, design, template, social post, LinkedIn, Instagram, schedule post, publish post, AI design agent, my designs, my templates, template categories

---

## Setup (run once)

### 1. Get an API key

1. Log in at [app.contentdrips.com](https://app.contentdrips.com)
2. Go to **Settings → API Tokens**
3. Create a token and copy it

### 2. Register the MCP server in OpenClaw

Export your key, then register the server. Use your actual key in the header (single-quoted JSON does not expand shell variables):

```bash
export CONTENTDRIPS_API_KEY=your_api_key_here

openclaw mcp set contentdrips "{
  \"type\": \"streamable-http\",
  \"url\": \"https://mcp.contentdrips.com/mcp\",
  \"headers\": { \"Authorization\": \"Bearer $CONTENTDRIPS_API_KEY\" }
}"
```

Or paste the key directly: `"Authorization": "Bearer cd_xxxx..."`

### 3. Verify

```bash
openclaw mcp list
```

You should see `contentdrips` with status active. All tools below are then available via MCP.

### 4. Install this skill (optional)

Copy this folder into your OpenClaw workspace:

```bash
mkdir -p ~/.openclaw/workspace/skills/contentdrips
cp -r /path/to/contentdrips-mcp/skills/contentdrips/* ~/.openclaw/workspace/skills/contentdrips/
```

---

## Important URLs

| Resource | URL pattern |
|----------|-------------|
| Edit design | `https://app.contentdrips.com/canvas?template={TEMPLATE_ID}` |
| Edit post | `https://app.contentdrips.com/make-post?id={POST_UUID}` |
| Connect social accounts | `https://app.contentdrips.com/social-accounts` |

Always share these links with the user after creating a design or post.

---

## Agent rules

1. **Workspaces first (always)** — call `get_profiles` before `create_graphic`, `create_post`, `generate_*`, `render_template`, schedule, or publish. If 2+ workspaces, ASK which. Always pass `profile_id`. Never tell the user you lack a profile_id — fetch it.
2. **MAIN FLOW — route by whether they named a template** (template = design = graphic = carousel = infographic):
   - **No ID or name:** AI Design Agent. `get_profiles` → `create_graphic(profile_id)` → `get_brand_styles` (if 2+ ASK which) → `run_ai_design_agent` (pass `reference_image` if they uploaded a picture) → **share the editor link and STOP**.
   - **Has ID or name:** AI maker (keep layout). `get_template` → `get_template_structure` → `generate_ai_carousel` / `generate_ai_graphic` → `check_job_status`.
   - Use Design Agent on an existing template only if they explicitly ask to override/recreate the layout (or recreate from a reference image).
3. **Confirm before publish — platforms matter** — confirm **naming platforms** (e.g. "Publish to LinkedIn only?" / "Publish to Instagram only?"). Set explicit booleans for **only** platforms they named — never add LinkedIn when they asked for Instagram, or Instagram when they asked for LinkedIn.
4. **Confirm before delete** — ask before `delete_graphic` or `delete_post`.
5. **Design synonyms** — "designs", "graphics", "creatives", "templates", "infographics", and "carousels" all map to ContentDrips templates.
6. **Platforms — LinkedIn and Instagram equally** — only schedule/publish to platforms the user explicitly named. LinkedIn-only → `linkedin_publish=true`, `instagram_publish=false`. Instagram-only → opposite. Ask if unclear.
7. **Do not auto-export** — after Design Agent, share `edit_url` only. Call `render_template` → `check_job_status` **only** if they ask to preview, download PNG/PDF, attach to a post, or publish. Never say export is unavailable.
8. **Style + model before Design Agent** — call `get_brand_styles` before every `run_ai_design_agent`. If 2+ saved styles, ASK which to use (or none) — never auto-pick. If exactly 1, use it unless they declined. If Pro is available (`can_use_pro_model`), ASK Basic vs Pro (default Basic). Pass `style_id` and `model`.
9. **Reference images (ChatGPT)** — if the user uploads an image (“recreate this”, “use this as reference”), pass it to `run_ai_design_agent` as `reference_image` (https URL preferred, or data URI). Claude typically cannot pass chat images to MCP.
10. **Post images — two paths only:**
   - ContentDrips exports → `set_post_images` with `export_urls` from `check_job_status`
   - External/user images → `upload_images_to_post` with `image_urls` (prefer URLs over base64; base64 fails above ~4 MB)
11. **Before scheduling/publishing** — call `get_social_accounts` for the profile. If the requested platform is not connected, tell the user to connect at the social-accounts URL above. Do not publish to a different connected platform as a substitute.
12. **Text-only tool output** — share the **Open in editor** link when the user wants to see a design. Do not start a render job just to show them the design.
13. **Custom canvas sizes** — `create_graphic` with `format: "custom"`, `width`, and `height` (100–3000 px). Do not fall back to a preset.
14. **Browse by category** — only when the user asks to show/find templates, or after they chose an existing template and need help picking one.

---

## Tools (28)

### Templates & designs

| Tool | Use when |
|------|----------|
| `get_template_categories` | List public template categories (carousel, quote, LinkedIn, etc.) |
| `search_templates` | Browse/search public templates by `category` and/or `query` keyword |
| `get_my_templates` | List user's designs when they ask to show/pick; never auto-pick for creation |
| `get_template` | Look up one design by ID or name (markdown details + editor link) |
| `get_template_structure` | **Required** before AI maker or manual JSON fill (`generate_carousel` / `generate_graphic`) |
| `create_graphic` | New blank design — first step when creating without a template ID |
| `delete_graphic` | Permanently delete a design |

**`create_graphic` formats:**

| Format | Dimensions |
|--------|------------|
| `square` | 1080 × 1080 |
| `portrait` | 1080 × 1350 |
| `tiktok` | 1080 × 1920 |
| `landscape` | 1920 × 1080 |
| `custom` | any width × height (100–3000 px each) |

For `custom`, always pass `format: "custom"` plus both `width` and `height`. Carousels: set `slides` (default 3).

### AI generation & design

| Tool | Use when |
|------|----------|
| `get_brand_styles` | **Required** before `run_ai_design_agent` — list saved styles + Pro eligibility; ask if 2+ styles or Pro is available |
| `run_ai_design_agent` | New blank layout, or **override** existing design (ask + warn first). Pass `style_id` and `model`. |
| `generate_ai_carousel` | Template ID + new topic/URL — keep carousel layout (after `get_template_structure`) |
| `generate_ai_graphic` | Template ID + new topic/URL — keep graphic layout (after `get_template_structure`) |
| `generate_carousel` | Template ID + manual/LLM `carousel_content` JSON (after `get_template_structure`) |
| `generate_graphic` | Template ID + manual/LLM `content_update` array (after `get_template_structure`) |
| `render_template` | Export current design as PNG/PDF by `template_id` (after Design Agent or any saved design) |
| `check_job_status` | Poll render job → get `export_url`(s) |

### Workspaces & social

| Tool | Use when |
|------|----------|
| `get_profiles` | List workspaces (profiles) |
| `get_social_accounts` | LinkedIn/Instagram connected for a profile |

### Posts

| Tool | Use when |
|------|----------|
| `list_posts` | List by status: draft, scheduled, published, etc. |
| `get_post` | Single post details |
| `create_post` | New draft with caption |
| `update_post` | Edit caption or platform flags |
| `delete_post` | Delete post |

### Post images

| Tool | Use when |
|------|----------|
| `set_post_images` | Attach ContentDrips `export_urls` to a post |
| `upload_images_to_post` | Upload external images (URLs or base64) |
| `remove_images_from_post` | Remove all images from a post |

### Publishing

| Tool | Use when |
|------|----------|
| `schedule_post` | Schedule for future (timezone + platforms) |
| `unschedule_post` | Move scheduled post back to draft |
| `publish_post` | Publish now (requires user confirmation) |

---

## Common workflows

### A. Browse or search public templates

```
get_template_categories()                    → carousel, quote, LinkedIn, etc.
search_templates(category="carousel")        → browse a category
search_templates(query="motivational")       → keyword search
search_templates(category="quote", query="sale")  → combine both
get_template(template_id)                    → details + editor link
```

### B. MAIN FLOW — always ask first

```
No template yet?
  Ask: A) AI Design Agent on NEW blank, OR B) Choose existing template (name/ID)?

Has / chose a template ID?
  Ask explicitly:
    1) AI Design Agent — OVERRIDES existing design with a new AI layout, OR
    2) AI carousel/graphic maker — KEEP layout, fill topic/URL/YouTube/TikTok (recommend for content-fill)

── Path A (Design Agent — no template ID/name) ──
get_profiles → create_graphic(profile_id) → get_brand_styles (ASK if 2+ styles; ask Pro if available)
→ run_ai_design_agent(style_id?, model, reference_image if uploaded) → share edit_url (STOP)
→ render_template only if they ask to preview/download

── Path B maker (template ID or name) ──
get_template → get_template_structure
generate_ai_carousel OR generate_ai_graphic (method=topic|blog|youtube|tiktok_reel)
check_job_status → export_url(s)

── Path B Design Agent (only if they explicitly asked to override/recreate) ──
get_brand_styles → run_ai_design_agent(template_id, style_id?, model, reference_image?) → share edit_url

── Path B manual JSON (full control) ──
get_template → get_template_structure
generate_carousel(carousel_content) OR generate_graphic(content_update)
check_job_status
```

### C. Manual JSON fill (`carousel_content` / `content_update`)

Labels/element keys must match `get_template_structure`. **Do not use the legacy `carousel` key.**

- Carousel → `generate_carousel` with `carousel_content`. Full example: [examples/carousel_content.json](examples/carousel_content.json)
- Graphic → `generate_graphic` with `content_update`. Full example: [examples/content_update.json](examples/content_update.json)
- Format notes: [examples.md](examples.md)

Carousel elements use `{ "type": "text"|"image", "value": "..." }`. Graphic items use `{ "type": "textbox"|"image"|"shape", "label": "...", ... }`.

### D. Generate → post → schedule/publish (platforms explicit)

```
check_job_status → export_urls
create_post(caption, profile_id) → uuid
set_post_images(uuid, export_urls)
get_social_accounts(profile_id)
# LinkedIn only:
publish_post(..., linkedin_publish=true, instagram_publish=false)
# Instagram only:
publish_post(..., linkedin_publish=false, instagram_publish=true)
Ask: "Publish to LinkedIn only?" / "Publish to Instagram only?" — name platforms
```

---

## Example user prompts

- "Create a 3-slide carousel on '3 ways to grow beard'" → **ask** Design Agent vs choose template
- "Make a LinkedIn post about remote work" → **ask** Design Agent vs choose template; publish LinkedIn only
- "Make an Instagram post about 'why remote work is great'" → **ask** Design Agent vs choose template; Instagram only
- "Turn this YouTube into a carousel: [URL]" → **ask** Design Agent vs choose template
- "Fit this blog into a carousel: [URL]" → **ask** Design Agent vs choose template
- "I like this template but new topic X" → ask Design Agent (override) vs maker (keep) → recommend maker → `get_template_structure` → `generate_ai_*`
- "Use template 5821 + this YouTube" → ask override vs maker → recommend maker → structure → `generate_ai_carousel`
- "Publish that post to LinkedIn only" → `linkedin_publish=true`, `instagram_publish=false`
- "Publish that post to Instagram only" → `linkedin_publish=false`, `instagram_publish=true`
- "Show me my designs" / "Show me carousel templates"
- "Get details of template 149900"

---

## Reference

- Manual JSON examples: [examples.md](examples.md), [examples/carousel_content.json](examples/carousel_content.json), [examples/content_update.json](examples/content_update.json)
- Full setup guide for Claude, Cursor, and other MCP clients: `CONTENTDRIPS_MCP_OVERVIEW.md` in the contentdrips-mcp repo.
