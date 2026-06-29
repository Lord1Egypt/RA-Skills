# General

Button · FloatButton · Typography · Icon

> Shared patterns (registration, icons, events, slots) live in [conventions.md](conventions.md).

---

### Button  `<a-button>`

**What:** Trigger an action or navigation.

**Variants:**
- `type`: `primary` · `default` · `dashed` · `text` · `link`
- state/modifier: `danger`, `ghost`, `disabled`, `loading`, `block` (full width)
- `size`: `large` · `middle` · `small`
- `shape`: `default` · `circle` · `round`
- with icon (`#icon` slot), icon-only (`shape="circle"`), `html-type="submit"` for forms

**Example:**

```vue
<script setup>
import { ref } from 'vue'
import { SearchOutlined, PlusOutlined } from '@ant-design/icons-vue'
const loading = ref(false)
const run = () => { loading.value = true; setTimeout(() => (loading.value = false), 1200) }
</script>

<template>
  <a-space wrap>
    <a-button type="primary">Primary</a-button>
    <a-button>Default</a-button>
    <a-button type="dashed">Dashed</a-button>
    <a-button type="text">Text</a-button>
    <a-button type="link">Link</a-button>
    <a-button type="primary" danger>Danger</a-button>
    <a-button type="primary" :loading="loading" @click="run">
      <template #icon><SearchOutlined /></template>
      Search
    </a-button>
    <a-button type="primary" shape="circle">
      <template #icon><PlusOutlined /></template>
    </a-button>
    <a-button type="primary" size="large" round>Large round</a-button>
    <a-button type="primary" block>Block</a-button>
  </a-space>
</template>
```

**API:** props `type` · `danger` · `ghost` · `size` · `shape` · `loading` · `disabled` · `block` · `href`/`target` (renders `<a>`) · `html-type`. Events: `@click`. Slots: default (label), `#icon`.

**Tips:** Keep **≤1 `primary`** per region; use `default`/`text`/`link` for secondary actions. Group buttons with `<a-space>`. For a submit button inside `<a-form>`, use `html-type="submit"`.

---

### FloatButton  `<a-float-button>`

**What:** A button pinned to a corner of the viewport (FAB), optionally expanding into a menu; includes back-to-top.

**Variants:** single `a-float-button` · `a-float-button-group` (with `trigger="hover|click"` to expand) · `a-back-top`. `type`: `primary`/`default`; `shape`: `circle`/`square`; with `#icon`, `tooltip`, `badge`, `href`.

**Example:**

```vue
<script setup>
import { QuestionOutlined, CustomerServiceOutlined, CommentOutlined, SyncOutlined } from '@ant-design/icons-vue'
</script>

<template>
  <!-- single -->
  <a-float-button tooltip="Help" :style="{ right: '24px', bottom: '24px' }">
    <template #icon><QuestionOutlined /></template>
  </a-float-button>

  <!-- expanding group -->
  <a-float-button-group trigger="hover" type="primary" :style="{ right: '24px', bottom: '96px' }">
    <template #icon><CustomerServiceOutlined /></template>
    <a-float-button><template #icon><CommentOutlined /></template></a-float-button>
    <a-float-button><template #icon><SyncOutlined /></template></a-float-button>
  </a-float-button-group>

  <a-back-top />
</template>
```

**API:** `type` · `shape` · `tooltip` · `:badge` · `href`. Group: `trigger`, `#icon` (collapsed icon). Events `@click`.

**Tips:** Position via the `style` `right`/`bottom`. Use for one persistent global action (new, help, support) — not as a primary toolbar.

---

### Typography  `<a-typography-*>`

**What:** Text with semantic styles plus copy/edit/ellipsis interactions.

**Variants:**
- elements: `a-typography-title` (`:level="1..5"`) · `a-typography-text` · `a-typography-paragraph` · `a-typography-link`
- semantic `type`: `secondary` · `success` · `warning` · `danger`
- modifiers: `strong`, `italic`, `underline`, `delete`, `mark`, `code`, `keyboard`
- interactions: `:ellipsis` (`true` or `{ rows, expandable, tooltip }`), `:copyable`, `:editable`

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const editable = ref('Click the pencil to edit me')
</script>

<template>
  <a-typography-title :level="3">Heading level 3</a-typography-title>
  <a-typography-text type="success">Success</a-typography-text>
  <a-typography-text type="danger" delete>Removed</a-typography-text>
  <a-typography-text code>npm run dev</a-typography-text>
  <a-typography-text :copyable="{ text: 'copied value' }">Copy me</a-typography-text>
  <a-typography-paragraph v-model:content="editable" :editable="true" />
  <a-typography-paragraph :ellipsis="{ rows: 2, expandable: true, symbol: 'more' }">
    A long paragraph that will be clamped to two lines with an inline “more” toggle…
  </a-typography-paragraph>
  <a-typography-link href="https://antdv.com" target="_blank">antdv.com</a-typography-link>
</template>
```

**API:** `:level` (Title) · `type` · `:ellipsis` · `:copyable` · `:editable` · `:content`/`v-model:content` (editable). Slots: default content.

**Tips:** Prefer Typography over raw `<h1>/<p>` when you want truncation, copy, or inline edit. For table/inline truncation, `:ellipsis="{ tooltip: true }"` shows the full text on hover.

---

### Icon  (`@ant-design/icons-vue`)

**What:** SVG icons used standalone or inside components' `#icon` slots.

**Variants:** three themes per name — `*Outlined`, `*Filled`, `*TwoTone` (e.g. `HeartOutlined` / `HeartFilled` / `HeartTwoTone`). Props: `spin`, `:rotate`, `two-tone-color` (TwoTone only), size/color via CSS `font-size`/`color`.

**Example:**

```vue
<script setup>
import { HeartTwoTone, LoadingOutlined, SettingFilled, SmileOutlined } from '@ant-design/icons-vue'
</script>

<template>
  <SmileOutlined :style="{ fontSize: '24px', color: '#1677ff' }" />
  <SettingFilled spin />
  <LoadingOutlined />
  <HeartTwoTone two-tone-color="#eb2f96" />
</template>
```

**API:** `spin` · `:rotate` (deg) · `two-tone-color`. Style/size with inline `font-size` & `color`.

**Tips:** Inside other components use the **`#icon` slot** (Button, Avatar, Menu items, Tag, Result, …). For brand/custom SVGs, `createFromIconfontCN({ scriptUrl })` builds an `<icon-font>` component. Don't mix icon sets — stay within `@ant-design/icons-vue` for visual consistency.
