## BCMS Entries

Entries are instances of templates. Each entry typically has:

- `meta`: SEO‑like fields (title, slug, description).
- `content`: localized content fields keyed by language code.

BCMS supports many languages, and both `meta` and `content` can store values per locale.

---

### Creating and editing entries (Dashboard)

To create an entry:

1. Open **Entries** in the sidebar.
2. Select the template you want (e.g. `Blog`).
3. Click **Create new entry**.
4. Fill in meta fields and content, then click **Create**.

To edit an entry:

1. Click the entry in the list.
2. Change meta or content fields.
3. Click **Update**.

You can also **duplicate** an entry from the three‑dot menu next to the Edit button, which creates a new entry with the same values.

To delete an entry, use the same three‑dot menu and choose **Delete**.
Deleted entries go to **Trash**.

---

### Creating entries

- Use `bcms.entry.create(templateName, payload)`.
- Always provide a **unique slug** per template and locale.
- Populate at least one language in `content`.

Example (using status, localized meta and content):

```ts
await bcms.entry.create('blog', {
  statuses: [{ lng: 'en', id: 'published' }],
  meta: [
    {
      lng: 'en',
      data: {
        title: 'Hello world',
        slug: 'hello-world',
      },
    },
  ],
  content: [
    {
      lng: 'en',
      nodes: [
        {
          type: 'paragraph',
          content: [{ type: 'text', text: 'This is my first blog post.' }],
        },
      ],
    },
  ],
});
```

### Reading entries

- Get by ID or slug using helper methods from the SDK (or your own wrapper).
- List all entries of a template and filter by status (e.g. draft/published).

Examples:

```ts
// Get all entries of a template
const blogPosts = await bcms.entry.getAll('blog');

// Get by slug
const onePost = await bcms.entry.getBySlug('hello-world', 'blog');

// Filter by status
const drafts = await bcms.entry.getAllByStatus('blog', 'draft');
```

### Updating and deleting

- Use `bcms.entry.update(templateName, entryId, payload)` for partial updates.
- Use `bcms.entry.delete(templateName, entryId)` to remove content.

Examples:

```ts
await bcms.entry.update('blog', 'entry_id', {
  lng: 'en',
  status: 'draft',
  meta: {
    title: 'Updated title',
  },
  content: [
    {
      type: 'paragraph',
      content: [{ type: 'text', text: 'Updated content goes here.' }],
    },
  ],
});

await bcms.entry.deleteById('entry_id', 'blog');
```

### Multilingual considerations

- Treat each locale as a first‑class variant.
- Avoid copying text between locales automatically; instead, surface missing translations.

---

### Entry statuses

- You can define custom statuses such as `draft`, `ready-for-review`, `published`.
- Editors set statuses via a dropdown in the entry UI.
- In code, statuses are useful for:
  - Previews
  - Staging environments
  - Controlling what appears in production.

Example:

```ts
const drafts = await bcms.entry.getAllByStatus('blog', 'draft');
```

---

### Rendering entry content on the frontend

For React projects, use `<BCMSContentManager />` to render structured content, including widgets:

```tsx
import { BCMSContentManager } from '@thebcms/components-react';
import { bcms } from './client';
import TestimonialsWidget from '@/components/widgets/testimonials';

const page = await bcms.entry.getById('about-us', 'page');

<BCMSContentManager
  items={page.content.en}
  clientConfig={bcms.getConfig()}
  widgetComponents={{
    testimonials: TestimonialsWidget,
  }}
/>;
```

- Primitive nodes (paragraphs, headings, lists) render automatically.
- Widgets are mapped via `widgetComponents`.
- Unhandled widgets result in a **hidden warning element** in the DOM, making it easy to catch missing handlers in development.

For concrete code snippets, check examples in `scripts/manage-entries.ts` and the higher‑level notes in `SKILL.md`.
