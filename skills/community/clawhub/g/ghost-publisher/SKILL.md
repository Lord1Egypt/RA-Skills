---
name: ghost-publisher
description: Publish markdown articles to any Ghost 5 CMS site. The first reference implementation of Publisher Interface v1 -- a CMS-agnostic contract for editorial workflows. Handles the full publish pipeline (create, convert markdown to Ghost Lexical, upload feature image, publish) and exposes every interface method (create, update, publish, schedule, delete, upload, get). Works with self-hosted Ghost and Ghost Pro.
version: 1.0.0
emoji: 👻
homepage: https://github.com/MachinesOfDesire/ghost-publisher
metadata:
  openclaw:
    requires:
      env:
        - GHOST_URL
        - GHOST_ADMIN_API_KEY
    primaryEnv: GHOST_ADMIN_API_KEY
---

# Ghost Publisher

Publish markdown articles to any Ghost 5 CMS site. The first reference
implementation of **Publisher Interface v1** -- a CMS-agnostic contract for
editorial workflows that makes "change CMS" a config decision, not a rewrite.

**Companion skills** (all implement the same interface, published separately):
- `ghost-publisher` -- this skill
- `wordpress-publisher` -- planned
- `substack-publisher` -- planned
- `medium-publisher` -- planned

---

## About the interface

This skill implements Publisher Interface v1 in full. The interface spec --
the standard post object schema and the seven required methods -- lives in
[`INTERFACE.md`](INTERFACE.md) at the skill root. Read that file if you are
building a calling agent or another adapter skill. Everything below this
section is Ghost-specific usage.

The short version: your code (or an editorial workflow orchestrator) calls
`publisher.createPost(post)`, `publisher.publishPost(id, opts)` and so on.
The adapter translates the standard post object into Ghost-shaped payloads,
handles JWTs, converts markdown to Ghost Lexical, maps author IDs to Ghost
staff members, and uploads images. None of that leaks into caller code.

---

## Setup

**Required environment variables**

- `GHOST_URL` -- your Ghost site URL, e.g. `https://yoursite.com` or
  `https://yourpub.ghost.io`
- `GHOST_ADMIN_API_KEY` -- Admin API key from a Ghost custom integration.
  Format: `<key_id>:<hex_secret>`

**To get your Admin API key**

1. Go to Ghost Admin -> Settings -> Integrations
2. Click "Add custom integration"
3. Name it (e.g. "OpenClaw Publisher")
4. Copy the Admin API Key -- it is a 24-char key_id, a colon, and a 64-char hex secret (format: `XXXXXXXXXXXXXXXXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)

**Optional config file (`GHOST_PUBLISHER_CONFIG`)**

For non-secret settings (default author, agent-to-staff mapping, newsletter
ID, max image size), point `GHOST_PUBLISHER_CONFIG` at a JSON file:

```json
{
  "default_author_id": "ghost_staff_id",
  "agent_author_map": {
    "staff_1": "ghost_staff_id_1",
    "staff_2": "ghost_staff_id_2"
  },
  "newsletter_id": "ghost_newsletter_id",
  "max_image_size_mb": 2
}
```

The `agent_author_map` lets a caller pass `{"author": "staff_1"}` and have
the adapter resolve it to the right Ghost staff member without the caller
needing to know internal Ghost IDs. Omit the map and everything falls back
to `default_author_id`, or to the integration's default if that is also
unset.

Keep this file out of version control if it contains IDs you do not want
public. No secret keys go in this file -- secrets come from env vars.

---

## Usage

### As a Python module (recommended for agents)

```python
from publisher import GhostPublisher

pub = GhostPublisher()  # reads env vars

post_id = pub.createPost({
    "title": "A quiet argument about obsolescence",
    "excerpt": "Things that still run but no longer serve a purpose.",
    "body_md": open("article.md").read(),
    "tags": ["culture", "criticism"],
    "author": "staff_1",
})

hosted = pub.uploadImage("https://cdn.example.com/hero.jpg", alt="Booth interior")
pub.updatePost(post_id, {"featured_image_url": hosted, "image_alt_text": "Booth interior"})

url = pub.publishPost(post_id, {"send_newsletter": True})
print(f"Live at: {url}")
```

All seven Publisher Interface v1 methods are available on the
`GhostPublisher` instance: `createPost`, `updatePost`, `publishPost`,
`schedulePost`, `deletePost`, `uploadImage`, `getPost`.

### As a CLI

**Full pipeline (most common)**

```bash
python3 publisher.py create-publish article.md \
  --title "Your Article Title" \
  --excerpt "A 1-2 sentence summary for SEO and previews" \
  --tags "ai,economics,analysis" \
  --image-url "https://cdn.example.com/header.jpg" \
  --image-alt "Description of the image" \
  --upload-image \
  --newsletter
```

Remove `--newsletter` to publish without emailing subscribers. Remove
`--upload-image` if the image URL is already on a CDN you trust and you
don't need Ghost's media store to host it.

**Step-by-step**

```bash
# 1. Create a draft (returns post_id)
python3 publisher.py create-draft --title "Title" --excerpt "Summary" --tags "tag1,tag2"

# 2. Inject markdown body
python3 publisher.py update-content <post_id> article.md

# 3. Upload and attach a feature image
python3 publisher.py set-image <post_id> https://cdn.example.com/hero.jpg --alt "Hero image" --upload

# 4. Schedule it, or publish it now
python3 publisher.py schedule <post_id> 2026-05-01T09:00:00Z
python3 publisher.py publish <post_id> --newsletter

# Other interface methods
python3 publisher.py get <post_id>
python3 publisher.py delete <post_id>
python3 publisher.py upload-image ./local.jpg --alt "alt text"
```

---

## Worked example

You are publishing a short essay to a Ghost Pro site with a custom
integration named "OpenClaw Publisher".

**1. Environment**

```bash
export GHOST_URL="https://yourpub.ghost.io"
export GHOST_ADMIN_API_KEY="<your_key_id>:<your_hex_secret>"
```

**2. Write `article.md`**

```markdown
# A quiet argument about obsolescence

Some machines keep running long after they stop serving anyone. The
projector still warms up. The booth still smells of amber lamp and dust.
There is no reel threaded. There is no audience.

## What this piece is about

A meditation on continuity without function -- why certain systems outlive
the problem they were built to solve.
```

**3. Run the pipeline**

```bash
python3 publisher.py create-publish article.md \
  --title "A quiet argument about obsolescence" \
  --excerpt "What certain systems look like after their purpose has gone." \
  --tags "culture,essay" \
  --image-url "https://cdn.example.com/booth.jpg" \
  --image-alt "Close-up of a projector booth interior, no reel loaded" \
  --upload-image
```

**4. Output**

```
[ok] Draft created: 69d12a34ec4a400445c217ce
[ok] Image uploaded: https://yourpub.ghost.io/content/images/2026/04/booth.jpg
[ok] Feature image set
[ok] Published: https://yourpub.ghost.io/quiet-argument-about-obsolescence/
```

That is the full pipeline. The same sequence, called from an editorial
workflow agent against any Publisher Interface v1 adapter, would produce
the same outcome on any CMS.

---

## Markdown formatting supported

- Headings: `# H1` through `#### H4`
- **Bold**, *italic*, ***bold+italic***
- `inline code`
- [Links](https://example.com)
- Bullet lists (`-`, `*`, `+`)
- Numbered lists (`1.`, `2.`)
- Blockquotes (`>`)
- Horizontal rules (`---`)

The skill converts markdown to Ghost 5 Lexical JSON internally. You never
touch the Lexical format directly.

Ghost stores the article title separately from the body. If your markdown
file starts with a `# Title` line, it is stripped automatically before
injection -- the title you pass via `--title` (or the `title` field in a
`createPost` call) is the one that wins.

---

## Editorial standards

**Ghost optimistic concurrency.** Every write fetches `updated_at` first
and passes it back to Ghost. If another writer modifies the post between
your read and your write, Ghost rejects the write. The adapter surfaces
the underlying error -- do not retry blindly.

**JWT expiry.** JWTs are generated fresh for each API call with a 5-minute
expiry. Long-running batch operations do not need to manage tokens.

**Image size cap.** `uploadImage` rejects files over the configured
`max_image_size_mb` (default 2MB) before hitting Ghost. Ghost Pro also has
its own cap; if your image clears this check but Ghost rejects it, raise
the ticket with Ghost Pro support or compress the image first.

**Tags.** Pass tags as plain strings. The adapter asks Ghost to create any
that do not yet exist. Ghost slugs them automatically.

**Author mapping.** If `agent_author_map` is configured, pass the
caller-side identifier (e.g. `"staff_1"`) as `author`. If it is not
configured, the adapter falls back to `default_author_id`, then to the
integration's default author. An unknown `author` does not error -- it
silently falls back. Design your workflow to audit bylines post-publish if
that matters to you.

---

## What this skill is not

- **Not a headless CMS.** Ghost is the CMS; this skill is the plumbing to
  get content into it.
- **Not a markdown renderer.** It converts markdown into Ghost Lexical so
  Ghost can render it. The output lives in Ghost, not here.
- **Not Ghost 4.x compatible.** Ghost 4 used Mobiledoc; this skill targets
  Ghost 5's Lexical format.
- **Not an editorial workflow.** Selecting images, writing copy, scheduling
  cadence -- that belongs to the calling agent or workflow. This skill
  does the publish step and does it well.

---

## License

MIT-0 (MIT No Attribution). Use, modify, redistribute, ship commercially.
No attribution required. See [`LICENSE`](LICENSE).
