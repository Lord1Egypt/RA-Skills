## Properties in BCMS

In BCMS, properties (also known as inputs) are the smallest building blocks used to define content structure.
They are combined in **Groups**, **Widgets**, and **Templates** to define flexible and structured content types.

Each property type represents a specific kind of input field – like text, number, image, or relationship to other content.

You can configure each property as:

- **Single or array** – one value or many values.
- **Required or optional** – whether editors must fill it in to save an entry.

---

## Basic property types

### String

A basic text input that accepts any character.

- Appears as a single‑line text field.
- Good for titles, slugs, or short descriptions.

```json
{
  "title": "Hello World"
}
```

**Options**

- Array: Yes
- Required: Optional

---

## Rich text

A content editor with formatting: headings, bold, italic, links, lists, etc.

- Good for content bodies that allow formatting.

```json
{
  "body": [
    {
      "type": "paragraph",
      "value": "This is a paragraph."
    }
  ]
}
```

**Options**

- Array: Yes
- Required: Optional

You can pass rich‑text content to `BCMSContentManager` like this:

```tsx
<BCMSContentManager
  items={myRichTextInput.nodes}
  clientConfig={bcms.getConfig()}
/>;
```

`BCMSContentManager` will automatically resolve paragraphs, lists, and other nodes into HTML,
and it can also render widgets when configured.

---

## Number

Accepts any numeric value, including decimals.

- Appears as a number input field.
- Useful for prices, rankings, or metrics.

```json
{
  "price": 19.99
}
```

**Options**

- Array: Yes
- Required: Optional

---

## Date

Date‑time picker that returns a timestamp (in milliseconds).

- Good for scheduling events, publishing content, or tracking deadlines.

```json
{
  "publishedAt": 1712926400000
}
```

**Options**

- Array: Yes
- Required: Optional

---

## Boolean

A simple toggle input: `true` or `false`.

- Appears as a switch in the editor.
- Ideal for flags like `featured`, `published`, or `visible`.

```json
{
  "featured": true
}
```

**Options**

- Array: Yes
- Required: Optional

---

## Enumeration

Predefined list of selectable options shown as a dropdown.

- Helps enforce consistency (e.g. category: `Blog`, `News`, `Guide`).
- You define the choices when setting up the property.

```json
{
  "category": "Blog"
}
```

**Options**

- Array: Yes
- Required: Optional

---

## Relational property types

### Entry pointer

Lets editors select one or more entries from another template.

- Often used for building relationships between content.
- Example: “Recommended Articles” → list of entries from the `Blog` template.

```json
{
  "relatedPosts": [
    "entry-id-1",
    "entry-id-2"
  ]
}
```

**Options**

- Array: Yes
- Required: Optional

---

### Group pointer

Lets you embed a group of properties inside the current template or widget.

- Reuses custom‑defined input structures.
- Example: a `Testimonial` group with `name`, `quote`, and `avatar`.

```json
{
  "testimonials": [
    {
      "name": "Jane",
      "quote": "Great service!"
    }
  ]
}
```

**Options**

- Array: Yes
- Required: Optional

See `references/groups.md` for more on working with groups.

---

### Media

File picker that connects to the Media Library.

- Allows selecting images, videos, or files.
- Used often in hero sections, product images, downloads, etc.

```json
{
  "image": {
    "_id": "media-id",
    "name": "hero.jpg"
  }
}
```

**Options**

- Array: Yes
- Required: Optional

See `references/media.md` for more on working with media.

---

## Visual and upcoming properties

### Color picker (coming soon)

Will allow selecting color values in HEX or RGB.

---

### Tags (coming soon)

Planned support for assigning free‑form labels or keywords to entries.

---

## Best practices

- Use arrays when multiple values make sense, such as feature lists or image galleries.
- Keep required fields minimal so content editors are not blocked.
- Use **Groups** for repeatable structures, and **Widgets** for reusable layouts across templates.
- Prefer **entry pointers** over duplicating text when linking content.

---

## Example use in a template

Consider a `Blog Post` template with these properties:

- `title` (built‑in, String)
- `slug` (built‑in, String)
- `publishedAt` (Date)
- `author` (Group pointer)
- `coverImage` (Media)
- `relatedPosts` (Entry pointer, array)

This structure lets editors create rich blog posts with consistent data:

- Titles and slugs for routing and SEO.
- A publish date for scheduling and sorting.
- A reusable `Author` group for bios and avatars.
- A `coverImage` for hero visuals.
- `relatedPosts` to cross‑link content without duplication.

