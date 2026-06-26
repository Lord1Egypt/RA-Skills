---
name: framer-cms
description: >
  Framer CMS management via the Server API — list, create, read, update, and delete CMS collections and items,
  upload images, publish previews, deploy to production, and manage project assets, all without opening Framer.
  Use when the user asks to manage Framer CMS content, publish a Framer site, push articles to Framer,
  update CMS items, upload images to Framer, create collections, sync content, or automate any Framer workflow.
  Trigger on: "framer", "framer cms", "framer publish", "framer deploy", "framer collection", "framer article",
  "push to framer", "upload to framer", "framer api", "framer server api", "cms item", "cms collection",
  "publish site", "deploy site", "framer preview", "framer image", "framer content".
  Do NOT trigger for: Framer design/layout work, Framer Motion animation library, building Framer plugins.
metadata:
  openclaw:
    requires:
      env:
        - FRAMER_PROJECT_URL
        - FRAMER_API_KEY
      bins:
        - node
        - npm
    primaryEnv: FRAMER_API_KEY
---

# Framer CMS — Server API Skill

Manage Framer CMS content programmatically via the `framer-api` npm package. Push articles, upload images, create collections, and publish/deploy — all from the terminal, no Framer app needed.

## First-time setup (onboarding)

If this is the first time the user uses this skill in a project, run the onboarding flow described in `references/onboarding.md`.

**Quick check:** Look for `FRAMER_PROJECT_URL` and `FRAMER_API_KEY` in the user's `.env` file or environment. If missing, onboard.

---

## How it works

This skill uses the **Framer Server API** (`framer-api` npm package) which connects to Framer projects via WebSocket using an API key. It provides full CMS CRUD, image uploads, publishing, and deployment.

**Important:** The `framer-api` package must be installed in the project. If not present, run:

```bash
npm i framer-api
```

All operations use **ES module scripts** (`.mjs` files) with this connection pattern:

```javascript
import { connect } from "framer-api"

// IMPORTANT: API key is passed as a plain string (2nd argument), NOT as {apiKey: "..."}
const framer = await connect(process.env.FRAMER_PROJECT_URL, process.env.FRAMER_API_KEY)
try {
  // ... operations ...
} finally {
  await framer.disconnect()
}
```

---

## Available operations

### CMS Collections

| Operation | Method | Notes |
|-----------|--------|-------|
| List collections | `framer.getCollections()` | Returns all CMS collections |
| Get one collection | `framer.getCollection(id)` | By collection ID |
| Create collection | `framer.createCollection(name)` | Creates empty collection |
| Get fields | `collection.getFields()` | Field definitions (name, type, id) |
| Add fields | `collection.addFields([{type, name}])` | Add new fields to collection |
| Remove fields | `collection.removeFields([fieldId])` | Delete fields by ID |
| Reorder fields | `collection.setFieldOrder([fieldIds])` | Set field display order |

### CMS Items (articles, entries)

| Operation | Method | Notes |
|-----------|--------|-------|
| List items | `collection.getItems()` | All items with field data |
| Create items | `collection.addItems([{slug, fieldData}])` | Create new items. Returns `undefined` — re-fetch with `getItems()` to get IDs |
| Update item fields | `item.setAttributes({ fieldData: { [fieldId]: {type, value} } })` | **MUST wrap in `fieldData:`** — without it, values are silently ignored |
| Update item slug/draft | `item.setAttributes({ slug: "new", draft: false })` | Slug and draft are set directly (NOT inside fieldData) |
| Delete item | `item.remove()` | Single item |
| Bulk delete | `collection.removeItems([itemIds])` | Multiple items |
| Reorder items | `collection.setItemOrder([itemIds])` | Set display order |

### ⚠️ Critical: How to update CMS item fields

The `setAttributes` method has a **non-obvious API design** — field values MUST be wrapped in a `fieldData` key:

```javascript
// ✅ CORRECT — fields wrapped in fieldData
await item.setAttributes({
  fieldData: {
    [titleFieldId]: { type: "string", value: "New Title" }
  }
})

// ❌ WRONG — silently ignored, no error thrown
await item.setAttributes({
  [titleFieldId]: { type: "string", value: "New Title" }
})

// ❌ WRONG — also silently ignored
await item.setAttributes({
  [titleFieldId]: "New Title"
})
```

**Partial updates work:** Only specified fields are changed. Other fields are preserved.

**Non-field attributes** (slug, draft) go directly on the object, NOT inside fieldData:
```javascript
await item.setAttributes({ slug: "new-slug", draft: false })
```

### Field data format

When creating/updating items, field data is keyed by **field ID** (not name):

```javascript
const fields = await collection.getFields()
const titleField = fields.find(f => f.name === "Title")

await collection.addItems([{
  slug: "my-article",
  fieldData: {
    [titleField.id]: { type: "string", value: "My Article Title" },
  }
}])
```

**Supported field types and their value format:**

| Type | Value format | Example |
|------|-------------|---------|
| `string` | `string` | `{ type: "string", value: "Hello" }` |
| `number` | `number` | `{ type: "number", value: 42 }` |
| `boolean` | `boolean` | `{ type: "boolean", value: true }` |
| `date` | `string` (UTC ISO) | `{ type: "date", value: "2026-04-06T00:00:00Z" }` |
| `formattedText` | `string` (HTML) | `{ type: "formattedText", value: "<h2>Title</h2><p>Text</p>" }` |
| `link` | `string` (URL) | `{ type: "link", value: "https://example.com" }` |
| `image` | `ImageAsset` object | See image upload section |
| `enum` | `string` (case name) | `{ type: "enum", value: "Published" }` |
| `color` | `string` (hex/rgba) | `{ type: "color", value: "#FF0000" }` |
| `file` | `FileAsset` object | Similar to image |
| `collectionReference` | `string` (item ID) | `{ type: "collectionReference", value: "itemId123" }` |
| `multiCollectionReference` | `string[]` | `{ type: "multiCollectionReference", value: ["id1","id2"] }` |

### Images

Upload images from public URLs, then use the returned asset in CMS items:

```javascript
const asset = await framer.uploadImage("https://example.com/photo.jpg")
// asset = { id, url, thumbnailUrl }

await item.setAttributes({
  fieldData: {
    [thumbnailField.id]: { type: "image", value: asset.url }
  }
})
```

### Publishing & deployment

```javascript
// Create a preview deployment
const result = await framer.publish()
// result = { deployment: { id }, hostnames: [...] }

// Promote preview to production
await framer.deploy(result.deployment.id)
```

**Always ask the user before deploying to production.** Publishing a preview is safe; deploying is live.

### Project info & changes

```javascript
await framer.getProjectInfo()       // { id, name, apiVersion1Id }
await framer.getCurrentUser()       // { id, name, avatar }
await framer.getPublishInfo()       // Current deployment status
await framer.getChangedPaths()      // { added, removed, modified }
await framer.getChangeContributors() // Contributor UUIDs
await framer.getDeployments()       // All deployment history
```

### Other operations

| Operation | Method | Notes |
|-----------|--------|-------|
| Color styles | `getColorStyles()`, `createColorStyle()` | Design tokens |
| Text styles | `getTextStyles()`, `createTextStyle()` | Typography tokens |
| Code files | `getCodeFiles()`, `createCodeFile(name, code)` | Custom code overrides |
| Custom code | `getCustomCode()` | Head/body code injection |
| Fonts | `getFonts()` | Project fonts |
| Locales | `getLocales()`, `getDefaultLocale()` | i18n |
| Pages | `createWebPage(path)`, `removeNode(id)` | Page management |
| Screenshots | `screenshot(nodeId, options)` | PNG buffer of any node |
| Redirects | `addRedirects([{from, to}])` | Requires paid plan |
| Node tree | `getNode(id)`, `getChildren(id)`, `getParent(id)` | DOM traversal |

---

## Common workflows

### Push a new article to CMS

See `references/cms-operations.md` for the full pattern including field resolution, image upload, and error handling.

### Bulk update articles

```javascript
const items = await collection.getItems()
for (const item of items) {
  await item.setAttributes({
    fieldData: {
      [metaField.id]: { type: "string", value: generateMeta(item) }
    }
  })
}
```

### Publish after CMS changes

```javascript
const changes = await framer.getChangedPaths()
if (changes.added.length || changes.modified.length || changes.removed.length) {
  const result = await framer.publish()
  console.log("Preview:", result.hostnames)
  // Ask user before: await framer.deploy(result.deployment.id)
}
```

---

## Important notes

- **API key scope:** Each key is bound to one project. For multiple Framer sites, store multiple keys.
- **WebSocket connection:** The `connect()` call opens a persistent WebSocket. Always call `disconnect()` when done, or use `using framer = await connect(...)` for auto-cleanup.
- **Field IDs, not names:** CMS operations use field IDs. Always call `getFields()` first and resolve names to IDs.
- **Image fields:** Pass the full `framerusercontent.com` URL from `uploadImage()`, not the asset ID.
- **Proxy methods:** Most methods (getCollections, publish, etc.) are proxied — they don't appear in `Object.keys(framer)` but work correctly.
- **Rate limits:** No documented rate limits, but avoid hammering. Add small delays for bulk operations (100+ items).
- **`formattedText` fields:** Accept standard HTML (h1-h6, p, ul, ol, li, a, strong, em, img, blockquote, pre, code, table, etc.).
- **Draft items:** Items can have `draft: true` — drafts are excluded from publishing.
- **Blog Posts collection:** Collections managed by `"thisPlugin"` are read-only via the API. Only `"user"` managed collections can be modified.
