---
name: antd-vue-components
description: Learn and look up how to use any ant-design-vue (Vue 3) component — its variants, runnable examples, Vue 3 SFC code, and key props/events/slots. Use when the user asks how to use an ant-design-vue component (a-table, a-form, a-select, a-menu, a-modal, …), wants a component's variants/examples/Vue 3 code, is porting a UI from React antd to Vue, or is learning ant-design-vue. Target is ant-design-vue v4 (Vue 3), NOT React antd.
---

# ant-design-vue components — learning reference

A study & lookup guide for **every `ant-design-vue` v4 (Vue 3)** component. For each component you get: **what it's for · its variants · a runnable Vue 3 SFC example · key props/events/slots · tips**.

## Read first

- This targets **`ant-design-vue` v4.2.x on Vue 3**. Globally-registered components use the **`a-` prefix** (`<a-button>`, `<a-table>`). It is **not** React `antd` — props/events/slots differ (see conventions).
- **Start with [references/conventions.md](references/conventions.md)** — the patterns shared by *all* components (registration, icons, `v-model:*`, events, slots, forms, theme, imperative APIs, and how to run any example). Learn these once and every component below makes sense.

## How to help someone learn a component

When asked "how do I use `<component>`?" (or for its variants/examples/code):

1. **Find it** in the index below and open that category file in `references/`.
2. **Present in this order:** one-line *what* → *variants* (the forms it ships in) → a **minimal runnable Vue 3 SFC** → *key API* (props/events/slots) → *tips* and when to pick it over a sibling.
3. **Match the level:** beginners get the minimal example first; then layer on variants/edge cases. Porting from React → point them at the React→Vue mapping in conventions.md.
4. **Always use Vue 3 idioms:** `v-model:value`/`v-model:checked`/`v-model:open`/…, `@change` events, and **named/scoped slots** (never React render-props or `onChange`).
5. **To run it:** give the Vite quickstart in [conventions.md](references/conventions.md#run-any-example), or offer to scaffold a playground.

## Component index

| Category | File | Components |
|---|---|---|
| **Conventions** (read first) | [conventions.md](references/conventions.md) | registration · icons · `v-model:*` · events · slots · forms · theme/tokens · message/Modal/notification · run-any-example |
| **General** | [general.md](references/general.md) | Button · FloatButton · Typography · Icon |
| **Layout** | [layout.md](references/layout.md) | Divider · Flex · Grid (Row/Col) · Layout · Space |
| **Navigation** | [navigation.md](references/navigation.md) | Anchor · Breadcrumb · Dropdown · Menu · Pagination · Steps |
| **Data Entry** | [data-entry.md](references/data-entry.md) | AutoComplete · Cascader · Checkbox · DatePicker · Form · Input · InputNumber · Mentions · Radio · Rate · Select · Slider · Switch · TimePicker · Transfer · TreeSelect · Upload |
| **Data Display** | [data-display.md](references/data-display.md) | Avatar · Badge · Calendar · Card · Carousel · Collapse · Descriptions · Empty · Image · List · Popover · QRCode · Segmented · Statistic · Table · Tabs · Tag · Timeline · Tooltip · Tour · Tree |
| **Feedback** | [feedback.md](references/feedback.md) | Alert · Drawer · Message · Modal · Notification · Popconfirm · Progress · Result · Skeleton · Spin · Watermark |
| **Other / system** | [other.md](references/other.md) | Affix · App · ConfigProvider · theme tokens · util |

## Per-component entry shape

Every component in the category files follows the same template, so studying is uniform:

```
### Name  `<a-name>`
What:     one sentence.
Variants: the meaningful forms (size/type/mode/shape/state …).
Example:  a complete <script setup> + <template> SFC you can paste & run.
API:      key props · events · slots (the ones you actually use).
Tips:     gotchas + "use this vs <sibling>".
```

## Related

- Building **dashboards in Slidev** with these components? Use the **`slidev-antd-dashboard`** skill — it covers the Slidev integration, layout shell, and dashboard composition rules. This skill is the general-purpose component learning reference.
- Official docs (authoritative API): <https://antdv.com/components/overview>.
