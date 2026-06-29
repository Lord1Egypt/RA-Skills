## BCMS Templates

Templates define content types (for example `Blog`, `Page`, `Author`).
They describe which properties an entry will have, including meta fields and content fields.

You can think of a template as a blueprint for entries such as Blog, Project, Author, Testimonial, or Product.

---

### Creating and editing templates (Dashboard)

- Open **Templates** in the BCMS sidebar and click **Create New Template**.
- Give the template a **singular, descriptive title** such as `Blog` (not `Blogs`).
  - The label influences UI phrases like “Add new Blog”.
- Optionally add a **description** used only inside the CMS to document processes, usage notes, or internal guidelines.
- Later, use **Edit template** to rename, update the description, or adjust fields.

### Naming and modelling guidelines

- Use **singular, descriptive names** (`blog`, not `blogs`).
- Use **groups** for reusable clusters of fields (e.g. SEO, author info).
- Prefer **smaller, composable templates** over one giant template.

---

### Adding properties to a template

In the dashboard, properties are dragged from the **Property list** into the template.
Each property can be:

- Single or array (allow multiple values)
- Required or optional

Common property types:

- **String** – short plain text (titles, slugs, labels)
- **Rich text** – formatted content for body text
- **Number** – prices, rankings, counts
- **Boolean** – flags like featured/published/visible
- **Date** – publish dates or event times
- **Enumeration** – predefined options (e.g. `Blog | News | Guide`)
- **Media** – images, PDFs and other files from the media library
- **Group pointer** – reusable group of fields (e.g. SEO or SocialLink)
- **Entry pointer** – reference to entries from another template (e.g. Author, Category)

You can reorder fields, mark them as required, and allow multiple values where appropriate.

#### Entry pointers

Entry pointers link entries between templates (e.g. a `Blog` entry referencing an `Author` entry).
Use them whenever you need a real relationship instead of copying text.

#### Groups in templates

Groups are mini-templates reused across templates and widgets.
Typical examples:

- SEO block (meta title, meta description, social image)
- Address block
- Testimonial item

Use **Group pointer** fields to embed these reusable structures.

---

### Template settings and IDs

Under template settings you can:

- Rename or delete the template.
- Change field labels or add/remove fields.
- Ensure API keys have the correct access to this template in **Project settings → API keys**.

The **template ID** (or name) is used in SDK calls such as `bcms.entry.create('blog', ...)`.
You can read it from the template’s URL or via the SDK.

---

### Common operations (SDK)

- **List all templates**

  ```ts
  const templates = await bcms.template.getAll();
  ```

- **Get a template by ID or name**

  ```ts
  const tplById = await bcms.template.getById('templateId');
  const blogTpl = await bcms.template.getOne('blog');
  ```

- **Update a template**

  ```ts
  await bcms.template.update('templateId', {
    label: 'Updated name',
    desc: 'Updated description',
    // fields...
  });
  ```

- **Delete a template**

  ```ts
  await bcms.template.deleteById('templateId');
  ```

- **Find where a template is used**

  ```ts
  await bcms.template.whereIsItUsed('templateId');
  ```

When refactoring templates:

- Track where groups and widgets are used before deletion.
- Plan migrations for existing entries (consider temporary compatibility fields).

---

### Deleting templates – impact and precautions

- Deleting a template removes it from the dashboard and can affect:
  - Entries based on that template.
  - Entry pointers or widgets that reference those entries.
- Before deleting, inspect usage via:
  - The dashboard (entries list)
  - `template.whereIsItUsed` / `group.whereIsItUsed` / `widget.whereIsItUsed`

Where possible, prefer **schema evolution** (adding/replacing fields) over hard deletion on production projects.

---

See the main `SKILL.md` and BCMS docs for more modelling examples and patterns.
