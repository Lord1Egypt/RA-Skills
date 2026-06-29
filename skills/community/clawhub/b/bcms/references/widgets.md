## BCMS Widgets

Widgets are reusable content blocks embedded inside rich‑text fields.
They are useful for callouts, banners, or CTA sections reused across many pages.

Key points:

- Design widgets for reusability and clear content boundaries.
- Use them to keep templates simpler while still supporting flexible layouts.

Important notes:

- Use `bcms.widget.getAll()` and `bcms.widget.whereIsItUsed(widgetId)` to inspect usage.
- Widgets are **not deletable via SDK**; removal must be done in the BCMS dashboard.

---

### Creating and editing widgets (Dashboard)

To create a widget:

1. Go to **Widgets** in the sidebar.
2. Click **Create new widget**.
3. Enter a label and optional description.

To edit a widget:

- Click the widget you want to update.
- Modify label, description, or properties.

After defining a widget, you can insert it into entry content fields from the rich‑text editor.

---

### Adding properties to a widget

Widgets can contain the same kinds of properties as templates and groups:

- String, number, boolean, date
- Rich text
- Media
- Group pointers
- Entry pointers

These fields become the widget’s configuration when an editor inserts it into content.

---

### Deleting widgets – impact and limitations

To delete a widget:

1. Open the widget.
2. Click **Edit widget**.
3. Click **Delete widget** and confirm.

Important:

- Deleting a widget removes it from all entries that use it.
- There is **no SDK method** to delete widgets; deletion is manual in the dashboard.
- Always check where a widget is used before deleting to avoid breaking live pages.

You can inspect usage programmatically:

```ts
const usage = await bcms.widget.whereIsItUsed('widget_id');
console.log(usage);
```

---

### Type‑safe widget usage

BCMS automatically generates TypeScript types for widgets, templates and groups.
You can import widget types from `@bcms-types/ts`:

```tsx
import type { TestimonialsWidget } from '@bcms-types/ts';

const Testimonials = ({ data }: { data: TestimonialsWidget }) => {
  return (
    <section>
      {data.testimonials.map((t) => (
        <blockquote key={t.quote}>
          <p>{t.quote}</p>
          <footer>— {t.name}</footer>
        </blockquote>
      ))}
    </section>
  );
};
```

This ensures compile‑time safety when accessing widget properties.

---

### Rendering widgets with `BCMSContentManager`

For React:

```tsx
import { BCMSContentManager } from '@thebcms/components-react';
import { bcms } from './client';
import Testimonials from '@/components/widgets/testimonials';

const page = await bcms.entry.getById('about-us', 'page');

<BCMSContentManager
  items={page.content.en}
  clientConfig={bcms.getConfig()}
  widgetComponents={{
    testimonials: Testimonials,
  }}
/>;
```

- `BCMSContentManager` renders rich‑text, images, and widgets.
- Widgets are matched by **key** in `widgetComponents`; keys must match widget names (usually lower‑case).
- If a widget is not handled, BCMS renders a hidden warning element:

```html
<div
  style="display: none;"
  data-bcms-widget-error="Widget testimonials is not handled"
>
  Widget testimonials is not handled
</div>
```

You can also use the `nodeParser` prop for fully custom rendering when necessary.

---

Consult the BCMS documentation for widget configuration options and limitations.
