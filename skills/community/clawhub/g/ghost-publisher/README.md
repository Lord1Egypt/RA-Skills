# Ghost Publisher

> Publish markdown to any Ghost 5 site. The first reference implementation of Publisher Interface v1.

A ClawHub skill that turns "publish this article" into one call. Handles the
Ghost-specific mess (JWTs, Lexical JSON, optimistic concurrency, image
uploads, newsletter triggers) so callers can stay focused on what they are
publishing, not how.

It is also the first implementation of **Publisher Interface v1** -- a
CMS-agnostic contract. Target the interface in your code and swap CMS with
a config change, not a rewrite. The interface spec lives in
[`INTERFACE.md`](INTERFACE.md).

---

## What this looks like

```python
from publisher import GhostPublisher

pub = GhostPublisher()  # reads GHOST_URL, GHOST_ADMIN_API_KEY

post_id = pub.createPost({
    "title": "A quiet argument about obsolescence",
    "excerpt": "Things that still run but no longer serve a purpose.",
    "body_md": open("article.md").read(),
    "tags": ["culture", "criticism"],
    "author": "staff_1",
})

hero = pub.uploadImage("https://cdn.example.com/hero.jpg", alt="Booth interior")
pub.updatePost(post_id, {"featured_image_url": hero, "image_alt_text": "Booth interior"})

url = pub.publishPost(post_id, {"send_newsletter": True})
```

All seven Publisher Interface v1 methods are available on the `GhostPublisher`
class: `createPost`, `updatePost`, `publishPost`, `schedulePost`,
`deletePost`, `uploadImage`, `getPost`.

---

## Install

```bash
openclaw skill install ghost-publisher
```

Set your Ghost credentials:

```bash
export GHOST_URL="https://yoursite.com"
export GHOST_ADMIN_API_KEY="<key_id>:<hex_secret>"
```

Get `GHOST_ADMIN_API_KEY` from Ghost Admin -> Settings -> Integrations ->
Add custom integration. Works with both self-hosted Ghost and Ghost Pro.

---

## Commands

Full pipeline, one call:

```bash
python3 publisher.py create-publish article.md \
  --title "Your title" \
  --excerpt "1-2 sentence summary" \
  --tags "tag1,tag2" \
  --image-url "https://cdn.example.com/hero.jpg" \
  --image-alt "Description" \
  --upload-image \
  --newsletter
```

Step-by-step:

| Command | Purpose |
|---|---|
| `create-draft` | Create a new draft, returns post_id |
| `update-content <id> <file.md>` | Inject markdown body |
| `set-image <id> <url> [--alt] [--upload]` | Set feature image |
| `publish <id> [--newsletter]` | Transition to published |
| `schedule <id> <iso-datetime>` | Transition to scheduled |
| `delete <id>` | Delete a post |
| `get <id>` | Fetch a post as JSON (standard schema) |
| `upload-image <url-or-path> [--alt]` | Upload to Ghost media, print URL |
| `create-publish <file.md> ...` | Full pipeline in one call |

Run `python3 publisher.py <command> --help` for every option.

---

## Configuration

Secrets come from environment variables. Non-secret settings come from a
JSON config file.

| Variable | Purpose |
|---|---|
| `GHOST_URL` | Your Ghost site URL (required) |
| `GHOST_ADMIN_API_KEY` | Admin API key from a custom integration (required) |
| `GHOST_PUBLISHER_CONFIG` | Path to optional JSON config file |

Example `ghost-publisher.config.json`:

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

`agent_author_map` lets callers pass a caller-side identifier (an agent ID,
a byline slug, anything) as the `author` field in a standard post object.
The adapter resolves it to a Ghost staff ID. Unknown authors silently fall
back to `default_author_id`, then to the integration's default.

---

## How to use this

**If you are writing an editorial agent or workflow:** target
`GhostPublisher` (or, better, the Publisher Interface v1 contract) rather
than Ghost's Admin API directly. Your agent stays CMS-independent. When
`wordpress-publisher` or `substack-publisher` ships, you swap one import.

**If you are publishing ad-hoc:** use the CLI. `create-publish` is the
one-shot command and handles every step of the pipeline (draft -> content
-> image upload -> publish) in a single invocation.

**If you are building another adapter skill:** read
[`INTERFACE.md`](INTERFACE.md) for the v1 contract and
[`publisher.py`](publisher.py) for a reference implementation. The
standard-post-object to backend-post-object translation lives in
`_standard_to_ghost()` and `_ghost_to_standard()` -- that is the pattern
to mirror for whatever CMS you are adapting.

---

## Companion skills

| Skill | Status |
|---|---|
| `ghost-publisher` | This skill (v1.0.0) |
| `wordpress-publisher` | Planned |
| `substack-publisher` | Planned |
| `medium-publisher` | Planned |

All four implement the same interface. Shipping adapters as separate skills
means installers bring only what they need -- a Ghost-only publication
does not install the WordPress adapter -- and makes it easy for third
parties to ship their own adapters for CMSes we do not cover.

---

## What this is not

- **Not a headless CMS.** Ghost is the CMS. This skill is the plumbing.
- **Not Ghost 4.x compatible.** Ghost 4 used Mobiledoc; this targets Ghost
  5's Lexical format.
- **Not an editorial workflow.** Selecting images, writing copy, pacing
  releases -- that is the calling agent's job. This skill does the publish
  step.

---

## License

MIT-0 (MIT No Attribution) -- the [mandatory license](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)
for all ClawHub skills. Use, modify, redistribute, ship commercially -- no
attribution required.
