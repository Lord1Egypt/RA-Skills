# Layout

Divider · Flex · Grid (Row/Col) · Layout · Space

> Shared patterns in [conventions.md](conventions.md).

---

### Grid  `<a-row>` / `<a-col>`

**What:** A 24-column responsive grid — the backbone of most page layouts.

**Variants:**
- Row: `:gutter` (number, `[h, v]`, or responsive object), `justify` (`start|end|center|space-around|space-between|space-evenly`), `align` (`top|middle|bottom`), `wrap`
- Col: `:span` (1–24), `:offset`, `:push`/`:pull`, `:order`, `flex`
- responsive per breakpoint on Col: `:xs :sm :md :lg :xl :xxl` (number or `{ span, offset }`)

**Example:**

```vue
<template>
  <a-row :gutter="[16, 16]">
    <a-col :span="6" v-for="n in 4" :key="n">
      <div class="box">span 6</div>
    </a-col>
    <a-col :xs="24" :md="16"><div class="box">md 16 / xs 24</div></a-col>
    <a-col :xs="24" :md="8"><div class="box">md 8 / xs 24</div></a-col>
  </a-row>
</template>

<style scoped>
.box { background: #e6f4ff; border: 1px solid #91caff; border-radius: 6px; padding: 12px; text-align: center; }
</style>
```

**API:** Row `:gutter` · `justify` · `align` · `wrap`. Col `:span` · `:offset` · `:order` · `flex` · breakpoint props.

**Tips:** Spacing between columns is `:gutter` — don't add margins. Use breakpoint props for responsive reflow. For simple one-dimensional spacing, reach for `Flex` or `Space` instead.

---

### Flex  `<a-flex>`

**What:** A thin wrapper over CSS flexbox (added in v4.2) for quick 1-D layouts without writing styles.

**Variants:** `vertical`, `justify` (flex-* values), `align`, `:gap` (`small|middle|large` or number), `wrap`.

**Example:**

```vue
<template>
  <a-flex justify="space-between" align="center" :gap="middle" style="border:1px solid #eee;padding:12px">
    <a-typography-title :level="5" style="margin:0">Toolbar</a-typography-title>
    <a-flex :gap="8">
      <a-button>Cancel</a-button>
      <a-button type="primary">Save</a-button>
    </a-flex>
  </a-flex>
</template>
```

**API:** `vertical` · `justify` · `align` · `:gap` · `wrap` · `:flex`.

**Tips:** Use Flex for header bars / alignment; use Grid when you need a responsive column system; use Space for evenly-gapped inline runs.

---

### Space  `<a-space>`

**What:** Consistent gaps between inline (or stacked) children — the idiomatic alternative to margin hacks.

**Variants:** `direction` (`horizontal|vertical`), `:size` (`small|middle|large` or number or `[h,v]`), `align`, `wrap`, `#split` slot (a separator between items).

**Example:**

```vue
<template>
  <a-space>
    <a-button>One</a-button><a-button>Two</a-button><a-button>Three</a-button>
  </a-space>

  <a-space :size="16" wrap style="margin-top:12px">
    <a-tag>tag a</a-tag><a-tag>tag b</a-tag><a-tag>tag c</a-tag>
  </a-space>

  <a-space direction="vertical" style="width:100%;margin-top:12px">
    <a-input placeholder="row 1" />
    <a-input placeholder="row 2" />
  </a-space>

  <a-space :size="8" style="margin-top:12px">
    <span>Edit</span><template #split><a-divider type="vertical" /></template><span>Delete</span>
  </a-space>
</template>
```

**API:** `direction` · `:size` · `align` · `wrap`. Slots: default, `#split`.

**Tips:** Best tool for button rows, tag runs, and action links (`Edit | Delete` via `#split`). For full layout structure use Grid/Flex.

---

### Divider  `<a-divider>`

**What:** A separator line between sections, optionally with text; or a vertical rule inline.

**Variants:** `type` (`horizontal|vertical`), `orientation` (`left|center|right` for text), `dashed`, `:plain`.

**Example:**

```vue
<template>
  <p>Section one.</p>
  <a-divider />
  <a-divider orientation="left">Settings</a-divider>
  <p>Section two.</p>
  <span>A</span><a-divider type="vertical" /><span>B</span><a-divider type="vertical" /><span>C</span>
</template>
```

**API:** `type` · `orientation` · `dashed` · `:plain`. Slot: default (label).

**Tips:** `type="vertical"` for inline separators (pair with `<a-space>`). Keep dividers sparse — too many fragment a page.

---

### Layout  `<a-layout>`

**What:** Page scaffolding: header / sider / content / footer regions, with a collapsible sider.

**Variants:** `a-layout` (add `has-sider` when a sider is a direct child) · `a-layout-header` · `a-layout-sider` (`collapsible`, `v-model:collapsed`, `:width`, `:collapsed-width`, `breakpoint`, `theme="dark|light"`, `reverse-arrow`) · `a-layout-content` · `a-layout-footer`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const collapsed = ref(false)
</script>

<template>
  <a-layout style="height: 320px">
    <a-layout-sider v-model:collapsed="collapsed" collapsible theme="dark">
      <div style="height:40px;margin:12px;background:rgba(255,255,255,.2);border-radius:6px" />
      <a-menu theme="dark" mode="inline" :selected-keys="['1']">
        <a-menu-item key="1">Dashboard</a-menu-item>
        <a-menu-item key="2">Reports</a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background:#fff;padding:0 16px">Header</a-layout-header>
      <a-layout-content style="margin:16px">Content area</a-layout-content>
      <a-layout-footer style="text-align:center">Footer</a-layout-footer>
    </a-layout>
  </a-layout>
</template>
```

**API:** Sider: `v-model:collapsed` · `collapsible` · `:width` · `:collapsed-width` · `breakpoint` · `theme` · `@collapse`. Layout: `has-sider`.

**Tips:** Nest a `<a-layout>` (header+content+footer) beside the sider, as above. Put the navigation `<a-menu mode="inline">` inside the sider. For full admin shells and dashboard composition, see the `slidev-antd-dashboard` skill.
