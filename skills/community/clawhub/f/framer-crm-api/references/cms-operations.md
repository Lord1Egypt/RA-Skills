# CMS Operations Reference

Complete reference for all CMS read/write operations via the Framer Server API.

---

## Connecting

```javascript
import { connect } from "framer-api"
import "dotenv/config" // if using dotenv

const framer = await connect(process.env.FRAMER_PROJECT_URL, process.env.FRAMER_API_KEY)
```

Always wrap operations in try/finally to ensure disconnect:

```javascript
try {
  // operations...
} finally {
  framer.disconnect()
}
```

---

## Collections

### List all collections

```javascript
const collections = await framer.getCollections()
for (const col of collections) {
  console.log(`${col.name} (${col.id}) — managed by: ${col.managedBy}`)
}
```

**Properties on a Collection:**
- `id` — unique ID
- `name` — display name
- `managedBy` — `"user"` | `"thisPlugin"` | `"anotherPlugin"`
- `slugFieldName` — name of the slug field (user collections only)
- `readonly` — whether modifications are blocked

### Get a single collection

```javascript
const col = await framer.getCollection("WB2ZX44Cx")
```

### Create a new collection

```javascript
const newCol = await framer.createCollection("My Articles")
```

This creates an empty collection. Add fields next.

### Add fields to a collection

```javascript
const fields = await newCol.addFields([
  { type: "string", name: "Title" },
  { type: "string", name: "Slug" },
  { type: "formattedText", name: "Content" },
  { type: "string", name: "Meta Description" },
  { type: "image", name: "Thumbnail" },
  { type: "date", name: "Published At" },
  { type: "boolean", name: "Featured" },
  { type: "number", name: "Read Time" },
  { type: "enum", name: "Status", cases: [{ name: "Draft" }, { name: "Published" }, { name: "Archived" }] },
])
```

**Supported field types for creation:** `string`, `number`, `boolean`, `date`, `image`, `file`, `link`, `formattedText`, `color`, `enum`, `collectionReference`, `multiCollectionReference`.

### Remove fields

```javascript
await collection.removeFields(["fieldId1", "fieldId2"])
```

### Reorder fields

```javascript
await collection.setFieldOrder(["fieldId3", "fieldId1", "fieldId2"])
```

---

## Items

### Get all items in a collection

```javascript
const items = await collection.getItems()
for (const item of items) {
  console.log(item.id, item.slug, item.draft)
  // item.fieldData is keyed by field ID
}
```

**Properties on a CollectionItem:**
- `id` — unique item ID
- `slug` — URL slug (unique within collection)
- `draft` — `true` if unpublished draft
- `fieldData` — object keyed by field ID, each value has `{ type, value }`

### Resolve field names to IDs

Always do this before creating/updating items:

```javascript
const fields = await collection.getFields()
const fieldMap = Object.fromEntries(fields.map(f => [f.name, f]))

// Now use fieldMap["Title"].id, fieldMap["Content"].id, etc.
```

### Create a new item

```javascript
const fields = await collection.getFields()
const fieldMap = Object.fromEntries(fields.map(f => [f.name, f]))

await collection.addItems([{
  slug: "my-new-article",
  fieldData: {
    [fieldMap["Title"].id]: { type: "string", value: "My New Article" },
    [fieldMap["Content"].id]: { type: "formattedText", value: "<h2>Hello</h2><p>World</p>" },
    [fieldMap["Meta Description"].id]: { type: "string", value: "A test article" },
  }
}])
```

### Update an existing item

Two approaches:

**Via setAttributes (recommended for single items):**

```javascript
const items = await collection.getItems()
const item = items.find(i => i.slug === "my-article")

const updated = await item.setAttributes({
  slug: "my-updated-article",  // optional: change slug
  fieldData: {
    [titleField.id]: { type: "string", value: "Updated Title" },
  }
})
```

`setAttributes` returns the updated item, or `null` if the item was deleted before the update.

**Via addItems with matching ID (upsert):**

```javascript
await collection.addItems([{
  id: existingItem.id,  // match by ID = update
  slug: "updated-slug",
  fieldData: { ... }
}])
```

### Delete items

**Single item:**
```javascript
await item.remove()
```

**Bulk delete:**
```javascript
await collection.removeItems(["itemId1", "itemId2", "itemId3"])
```

### Reorder items

```javascript
const items = await collection.getItems()
const reversed = items.map(i => i.id).reverse()
await collection.setItemOrder(reversed)
```

---

## Images

### Upload an image from URL

```javascript
const asset = await framer.uploadImage("https://example.com/photo.jpg")
// Returns: { id: "abc.jpg", url: "https://framerusercontent.com/images/abc.jpg", thumbnailUrl: "..." }
```

### Set image on a CMS item

```javascript
const asset = await framer.uploadImage("https://example.com/photo.jpg")

await item.setAttributes({
  fieldData: {
    [thumbnailField.id]: {
      type: "image",
      value: asset.url  // Use the full framerusercontent.com URL
    }
  }
})
```

**Important:** Pass `asset.url` (the full URL string), not the asset object or ID.

---

## Full article push example

Complete pattern for pushing an article to an existing collection:

```javascript
import { connect } from "framer-api"

const framer = await connect(projectUrl, apiKey)

try {
  // 1. Find the collection
  const collections = await framer.getCollections()
  const blog = collections.find(c => c.name === "Blog")

  // 2. Get field definitions
  const fields = await blog.getFields()
  const f = Object.fromEntries(fields.map(f => [f.name, f]))

  // 3. Upload thumbnail
  const thumb = await framer.uploadImage("https://example.com/thumb.jpg")

  // 4. Create the item
  await blog.addItems([{
    slug: "how-to-use-framer-api",
    fieldData: {
      [f["Title"].id]: { type: "string", value: "How to Use the Framer API" },
      [f["Content"].id]: { type: "formattedText", value: "<h2>Getting Started</h2><p>...</p>" },
      [f["Thumbnail"].id]: { type: "image", value: thumb.url },
      [f["Meta Description"].id]: { type: "string", value: "Learn how to..." },
    }
  }])

  // 5. Publish preview
  const result = await framer.publish()
  console.log("Preview:", result.hostnames)

  // 6. Deploy (only after user confirmation!)
  // await framer.deploy(result.deployment.id)
} finally {
  framer.disconnect()
}
```

---

## Plugin data (key-value storage)

Store arbitrary metadata on collections or items:

```javascript
// Set
await collection.setPluginData("lastSync", new Date().toISOString())

// Get
const lastSync = await collection.getPluginData("lastSync")

// List keys
const keys = await collection.getPluginDataKeys()

// Delete
await collection.setPluginData("lastSync", null)
```

Works on both `Collection` and `CollectionItem` objects.

---

## Error handling

Common errors and how to handle them:

| Error | Cause | Fix |
|-------|-------|-----|
| Connection refused | Invalid project URL or API key | Re-check credentials |
| Collection not found | Wrong ID or name | Call `getCollections()` to see available |
| Read-only collection | Collection managed by plugin (`managedBy: "thisPlugin"`) | Can only modify `"user"` collections |
| Field not found | Using field name instead of ID | Resolve via `getFields()` first |
| Duplicate slug | Slug already exists in collection | Use a unique slug or update by ID |
| Plan limitation | Feature requires paid plan (e.g., redirects) | Upgrade Framer plan |
