# Publisher Interface v1

A CMS-agnostic contract for publishing long-form content. This interface is
independent of any single CMS. Reference implementations ship as separate
ClawHub skills, one per CMS, named `{cms}-publisher`:

- `ghost-publisher` — this skill (Ghost 5.x, the first reference implementation)
- `wordpress-publisher` — planned
- `substack-publisher` — planned
- `medium-publisher` — planned

An Editorial Workflow Orchestrator (or any calling agent) targets this
interface rather than any specific CMS. Swapping CMS becomes a config change,
not a code change.

---

## The standard post object

Every method that accepts or returns a post uses this schema. Fields marked
optional may be omitted or set to `null`. Adapters SHOULD silently ignore
fields their backing CMS does not support, rather than error.

```json
{
  "title": "Full article title",
  "seo_title": "60 chars max, optional",
  "excerpt": "1-2 sentence summary for SEO and previews",
  "body_md": "Markdown body (CommonMark, with a few extensions; see below)",
  "tags": ["tag1", "tag2"],
  "author": "agent_id_or_staff_slug",
  "status": "draft | scheduled | published",
  "scheduled_at": "ISO 8601 timestamp, or null",
  "featured_image_url": "https://... or null",
  "image_alt_text": "string describing the feature image",
  "send_newsletter": false,
  "story_id": "caller-owned correlation ID, opaque to the adapter",
  "canonical_url": "optional, for cross-posts",
  "custom_fields": {}
}
```

### Field notes

- **`body_md`** — CommonMark with headings (#-####), bold, italic, bold+italic,
  inline code, links, bullet lists, numbered lists, blockquotes, and
  horizontal rules. Adapters convert to their CMS's native format (Ghost
  Lexical JSON, WordPress Gutenberg blocks, etc.).
- **`tags`** — plain strings. Adapters create tags that do not yet exist on
  the destination CMS.
- **`author`** — a caller-side identifier (agent ID, byline slug). Adapters
  map it to a CMS-specific staff/user ID via a configurable
  `agent_author_map`. If no mapping is found, adapters fall back to the
  integration's default author.
- **`status`** — one of three states. `scheduled` requires `scheduled_at`.
- **`send_newsletter`** — only honored at publish time, and only by adapters
  whose CMS has a newsletter concept. Ignored otherwise.
- **`custom_fields`** — an escape hatch for CMS-specific metadata the
  interface does not standardize. Keys and values are adapter-defined.

---

## Required methods

All seven methods are required. Signatures here use JavaScript-like notation
for readability; implementations may use whatever language is natural (this
reference implementation is Python).

```
publisher.createPost(post)             -> post_id
publisher.updatePost(id, fields)       -> updated post object
publisher.publishPost(id, opts)        -> post_url
publisher.schedulePost(id, datetime)   -> confirmation { id, status, scheduled_at }
publisher.deletePost(id)               -> confirmation { id, deleted: true }
publisher.uploadImage(url_or_path, alt)-> hosted_image_url
publisher.getPost(id)                  -> post object
```

### `createPost(post)`

Creates a new post in draft state by default. Accepts the full standard post
object. Adapters SHOULD accept partial objects (at minimum `title` is
required). Returns the CMS-assigned post ID as a string.

### `updatePost(id, fields)`

Patches an existing post. `fields` is a partial standard post object —
only the included keys are updated. Returns the full updated post object.
Adapters MUST honor the destination CMS's concurrency controls (e.g. Ghost's
`updated_at` optimistic lock).

### `publishPost(id, opts)`

Transitions a post to `published`. `opts` is an optional object:

```json
{ "send_newsletter": true }
```

Returns the public URL of the now-live post.

### `schedulePost(id, datetime)`

Transitions a post to `scheduled` with `scheduled_at = datetime`. `datetime`
MUST be an ISO 8601 string in the future. Returns a confirmation object with
the scheduled timestamp.

### `deletePost(id)`

Deletes a post. Returns a confirmation `{ "id": "...", "deleted": true }`.

### `uploadImage(url_or_path, alt)`

Uploads an image to the CMS's media store. Accepts either a remote URL (the
adapter fetches it) or a local file path. `alt` is the alt text to associate
with the image when the CMS supports it. Returns the hosted URL on the CMS's
media CDN.

Adapters MAY enforce a max file size (the Ghost adapter rejects images over
the configured `max_image_size_mb`, default 2MB).

### `getPost(id)`

Returns the full standard post object for an existing post. Adapters
translate their native representation back to the standard schema.

---

## Configuration

Adapters draw runtime configuration from environment variables for secrets
and an optional JSON config file for non-secret settings (author mappings,
defaults). The reference Ghost adapter uses:

- `GHOST_URL` — the Ghost site base URL
- `GHOST_ADMIN_API_KEY` — the admin API key, format `<key_id>:<hex_secret>`
- `GHOST_PUBLISHER_CONFIG` — optional path to a JSON config file with
  `default_author_id`, `agent_author_map`, `newsletter_id`, `max_image_size_mb`

Other adapters follow the same pattern with their own environment variable
names.

---

## Versioning

This is Publisher Interface **v1**. Breaking changes bump to v2 and the
interface document is re-published under a new URL. Adapters declare the
interface version they implement in their SKILL.md frontmatter.

Non-breaking additions (new optional fields, new optional methods) are
allowed within v1.
