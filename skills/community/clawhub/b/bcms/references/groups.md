## BCMS Groups

Groups are reusable building blocks made up of multiple properties.
They help you organise and nest structured content in templates and widgets.

A group is like a mini‑template defined once and reused anywhere:

- Inside templates
- Inside widgets
- Inside other groups (nested groups)

Typical use cases:

- FAQs
- Social links
- Testimonials
- Reusable SEO blocks

---

### Creating and editing groups (Dashboard)

To create a group:

1. Navigate to **Groups** in the sidebar.
2. Click **Create New Group**.
3. Set a label and optional description.
4. Add properties by dragging field types into the group builder.

To edit a group:

- Click the group name to open it.
- Use **Edit Group** to rename or change the description.
- Modify properties directly in the builder.

---

### Adding properties to a group

Groups can contain most property types, including:

- String
- Media
- Rich text
- Boolean
- Number
- Date
- Entry pointer
- Other groups (nested groups)

Each property becomes part of the group definition and is reused wherever the group appears.
Groups can also be made **repeatable** (arrays), ideal for:

- Testimonials
- Steps in a guide
- Feature lists
- FAQ items

---

### Groups in templates, widgets, and other groups

Groups can be referenced almost anywhere:

- **Templates** – shared structures used across all entries of a template.
- **Widgets** – modular content blocks needing structured fields.
- **Other groups** – nested reusable patterns.

This encourages:

- Less duplication of fields
- More consistent data shapes
- Easier type‑safe rendering in frontends

---

### Type‑safe usage in code

BCMS generates TypeScript types for all groups.
You can import and use these types from `@bcms-types/ts`:

```tsx
import type { TestimonialGroup } from '@bcms-types/ts';

type Props = {
  data: TestimonialGroup[];
};

export const Testimonials = ({ data }: Props) => (
  <section>
    {data.map((testimonial) => (
      <blockquote key={testimonial.quote}>
        <p>{testimonial.quote}</p>
        <footer>— {testimonial.name}</footer>
      </blockquote>
    ))}
  </section>
);
```

---

### Example: group inside a template

Imagine a `Team Member` template where each member has multiple social links.

- Create a `SocialLink` group with `platform`, `url`, and `icon`.
- Add the group to the template as a repeatable field.

In code:

```ts
import { bcms } from '@/bcms';
import type { TeamMemberEntryMetaItem } from '@bcms-types/ts';

const entry = await bcms.entry.getById<TeamMemberEntryMetaItem>(
  'team-member-slug',
  'team-member',
);

entry.meta.social_links.forEach((link) => {
  console.log(link.platform, link.url);
});
```

---

Common operations:

- `bcms.group.getAll()`
- `bcms.group.whereIsItUsed(groupId)`

Examples:

```ts
// Get all groups
const groups = await bcms.group.getAll();

// Get a single group
const group = await bcms.group.getById('group_id');

// Find where a group is used
const usage = await bcms.group.whereIsItUsed('group_id');
console.log(usage);
```

---

### Deleting groups – impact and precautions

Deleting a group removes it from:

- Templates that reference it
- Widgets that reference it
- Other groups that nest it

Always use `group.whereIsItUsed` or the dashboard UI to inspect usage before deleting, especially in production.

---

Refer to the official BCMS docs for the latest API surface and additional examples.
