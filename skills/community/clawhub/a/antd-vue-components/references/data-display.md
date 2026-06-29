# Data Display

Card · Table · Tabs · Descriptions · List · Statistic · Tag · Badge · Avatar · Tooltip · Popover · Segmented · Collapse · Timeline · Tree · Calendar · Carousel · Image · Empty · QRCode · Tour

> Shared patterns in [conventions.md](conventions.md). Table/cell customization uses **scoped slots** (`#bodyCell`).

---

### Card  `<a-card>`

**What:** A bordered content container with optional title, extra actions, cover, and footer actions.

**Variants:** `title` + `#extra`; `:bordered`; `hoverable`; `:loading` (skeleton); `size="small"`; `:tab-list` (inner tabs); `a-card-grid` (grid of cells); `a-card-meta` (`#avatar`/`#title`/`#description`); `#cover`; `:actions`/`#actions`.

**Example:**

```vue
<script setup>
import { EditOutlined, EllipsisOutlined, SettingOutlined } from '@ant-design/icons-vue'
</script>

<template>
  <a-card title="Project Atlas" hoverable style="width:320px">
    <template #extra><a href="#">More</a></template>
    <a-card-meta title="Sprint 12" description="On track · 8 open issues" />
    <template #actions>
      <SettingOutlined key="setting" /><EditOutlined key="edit" /><EllipsisOutlined key="ellipsis" />
    </template>
  </a-card>
</template>
```

**API:** `title` · `:bordered` · `hoverable` · `:loading` · `size` · `:tab-list`/`v-model:activeTabKey`. Slots `#extra` `#cover` `#actions` `#title`.

**Tips:** `:loading` shows a skeleton — handy for async panels. Use `:bordered="false"` on tinted backgrounds; `a-card-grid` for an evenly divided cell grid.

---

### Table  `<a-table>`

**What:** Render rows of data with sorting, filtering, selection, pagination, and expansion.

**Variants:** `:columns` + `:data-source` + `row-key`; `:pagination` (object or `false`); `:row-selection`; `:expandable`; `:scroll="{ x, y }"`; `:loading`; `size` (`small|middle|large`); `sticky`; `:summary` via `#summary`; column features: `sorter`, `filters`/`onFilter`, `fixed`, `width`, `align`, `ellipsis`.

**Example:**

```vue
<script setup>
import { ref, computed } from 'vue'
const columns = [
  { title: 'Name', dataIndex: 'name', key: 'name', sorter: (a, b) => a.name.localeCompare(b.name) },
  { title: 'Dept', dataIndex: 'dept', key: 'dept',
    filters: [{ text: 'Eng', value: 'Eng' }, { text: 'Sales', value: 'Sales' }],
    onFilter: (v, r) => r.dept === v },
  { title: 'Salary', dataIndex: 'salary', key: 'salary', align: 'right', sorter: (a, b) => a.salary - b.salary },
  { title: 'Status', key: 'status' },
]
const data = [
  { id: 1, name: 'Mia', dept: 'Eng', salary: 142000, active: true },
  { id: 2, name: 'Leo', dept: 'Sales', salary: 98000, active: false },
  { id: 3, name: 'Ada', dept: 'Eng', salary: 156000, active: true },
]
const selectedRowKeys = ref([])
const rowSelection = computed(() => ({
  selectedRowKeys: selectedRowKeys.value,
  onChange: (keys) => (selectedRowKeys.value = keys),
}))
</script>

<template>
  <a-table :columns="columns" :data-source="data" row-key="id"
           :row-selection="rowSelection" :pagination="{ pageSize: 5 }" size="middle"
           @change="(pag, filt, sorter) => console.log(pag, filt, sorter)">
    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'status'">
        <a-badge :status="record.active ? 'success' : 'default'" :text="record.active ? 'Active' : 'Inactive'" />
      </template>
    </template>
  </a-table>
</template>
```

**API:** `:columns` · `:data-source` · `row-key` · `:pagination` · `:row-selection` · `:expandable` · `:scroll` · `:loading` · `size` · `sticky`. Scoped slots `#bodyCell` `#headerCell` `#expandedRowRender` `#summary` `#title` `#footer`. Events `@change` (sort/filter/page), `@resizeColumn`.

**Tips:** Always set `row-key`. Put column logic (`sorter`, `filters`, `onFilter`, `width`, `align`) in the **column object**; render custom cells via `#bodyCell`. For wide/tall data use `:scroll="{ x: 1200, y: 400 }"` and `fixed: 'left'/'right'` on key columns.

---

### Tabs  `<a-tabs>`

**What:** Switch between views in the same space.

**Variants:** `type`: `line` (default) · `card` · `editable-card`; `tab-position` (`top|right|bottom|left`); `size`; `centered`; `:items` array or `a-tab-pane` children; `#rightExtra`/`#leftExtra` (tabBarExtraContent); add/remove via `@edit` (editable-card).

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const active = ref('overview')
</script>

<template>
  <a-tabs v-model:activeKey="active">
    <template #rightExtra><a-button size="small">Settings</a-button></template>
    <a-tab-pane key="overview" tab="Overview">Overview content</a-tab-pane>
    <a-tab-pane key="activity" tab="Activity">Activity content</a-tab-pane>
    <a-tab-pane key="members" tab="Members" force-render>Members content</a-tab-pane>
  </a-tabs>

  <a-tabs type="card" style="margin-top:16px">
    <a-tab-pane key="1" tab="Card A">A</a-tab-pane>
    <a-tab-pane key="2" tab="Card B">B</a-tab-pane>
  </a-tabs>
</template>
```

**API:** `v-model:activeKey` · `type` · `tab-position` · `size` · `centered` · `:items`. Pane: `tab` · `force-render` · `disabled`. Events `@change`, `@edit` (editable-card). Slots `#rightExtra` `#leftExtra`.

**Tips:** `force-render` keeps a hidden pane mounted (e.g. to preserve a chart/form). Use `type="card"` for document-like sections; `editable-card` for closable/addable tabs.

---

### Descriptions  `<a-descriptions>`

**What:** A read-only key→value grid for record summaries.

**Variants:** `:column` (number or responsive `{ xs, md, … }`), `bordered`, `size`, `layout` (`horizontal|vertical`), `title`/`#extra`; per item `label`, `:span`.

**Example:**

```vue
<template>
  <a-descriptions title="Order #1042" bordered :column="2" size="small">
    <template #extra><a-button type="primary" size="small">Edit</a-button></template>
    <a-descriptions-item label="Customer">Mia Wong</a-descriptions-item>
    <a-descriptions-item label="Status"><a-badge status="success" text="Paid" /></a-descriptions-item>
    <a-descriptions-item label="Total">$340.00</a-descriptions-item>
    <a-descriptions-item label="Address" :span="2">123 Market St, San Francisco</a-descriptions-item>
  </a-descriptions>
</template>
```

**API:** `:column` · `bordered` · `size` · `layout` · `title`. Item `label` · `:span`. Slots `#extra`.

**Tips:** Use `:span` to make a field stretch across columns. `bordered` reads as a spec sheet; borderless is lighter.

---

### List  `<a-list>`

**What:** Render a collection of items (feed, list, or card grid).

**Variants:** `:data-source` + `#renderItem`; `:grid` (card grid); `item-layout` (`horizontal|vertical`); `:pagination`; `:loading`; `:load-more` (footer); `size`; `bordered`; `#header`/`#footer`; `a-list-item-meta` (`#avatar`/`#title`/`#description`).

**Example:**

```vue
<script setup>
const data = [
  { title: 'Deploy succeeded', desc: 'v2.4.1 · 2m ago' },
  { title: 'New signup', desc: 'acme.com · 1h ago' },
  { title: 'Invoice paid', desc: '$1,200 · 3h ago' },
]
</script>

<template>
  <a-list item-layout="horizontal" :data-source="data" bordered>
    <template #header>Activity</template>
    <template #renderItem="{ item }">
      <a-list-item>
        <a-list-item-meta :title="item.title" :description="item.desc">
          <template #avatar><a-avatar>{{ item.title[0] }}</a-avatar></template>
        </a-list-item-meta>
        <template #actions><a>view</a></template>
      </a-list-item>
    </template>
  </a-list>
</template>
```

**API:** `:data-source` · `:grid` · `item-layout` · `:pagination` · `:loading` · `bordered` · `size`. Slots `#renderItem` `#header` `#footer` `#loadMore`.

**Tips:** Use `:grid="{ gutter: 16, column: 4 }"` to render cards in a grid. Use Table when columns align across rows; List when items are heterogeneous.

---

### Statistic  `<a-statistic>`

**What:** Display a headline number, optionally with prefix/suffix; countdown variant.

**Variants:** `a-statistic` · `a-statistic-countdown` (`:value` = timestamp, `format`); `:precision`, `prefix`/`suffix` (props or slots), `:value-style`, `:loading`.

**Example:**

```vue
<script setup>
import { ArrowUpOutlined } from '@ant-design/icons-vue'
const deadline = Date.now() + 1000 * 60 * 60 * 5
</script>

<template>
  <a-row :gutter="16">
    <a-col :span="8">
      <a-statistic title="Active users" :value="11280" />
    </a-col>
    <a-col :span="8">
      <a-statistic title="Growth" :value="11.28" :precision="2" suffix="%" :value-style="{ color: '#3f8600' }">
        <template #prefix><ArrowUpOutlined /></template>
      </a-statistic>
    </a-col>
    <a-col :span="8">
      <a-statistic-countdown title="Sale ends" :value="deadline" format="HH:mm:ss" />
    </a-col>
  </a-row>
</template>
```

**API:** `title` · `:value` · `:precision` · `prefix`/`suffix` · `:value-style` · `:loading`. Countdown: `:value` (ms timestamp) · `format` · `@finish`.

**Tips:** Color the value via `:value-style` to encode up/down. Pair with `a-card` for KPI tiles (see `slidev-antd-dashboard`).

---

### Tag  `<a-tag>` / `<a-check-tag>`

**What:** Compact labels for status, categories, or selectable filters.

**Variants:** `color` (presets `success|processing|error|warning|default` or named `green|blue|…` or hex); `closable` + `@close`; `bordered`; `#icon`; `a-check-tag` (`v-model:checked` selectable).

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const checked = ref(true)
</script>

<template>
  <a-space wrap>
    <a-tag color="success">success</a-tag>
    <a-tag color="error">error</a-tag>
    <a-tag color="blue">blue</a-tag>
    <a-tag color="#7c3aed">custom</a-tag>
    <a-tag closable @close="(e) => e.preventDefault()">closable</a-tag>
    <a-check-tag v-model:checked="checked">Filter</a-check-tag>
  </a-space>
</template>
```

**API:** `color` · `closable` · `bordered` · `:icon`. Events `@close`. CheckTag: `v-model:checked`, `@change`.

**Tips:** Status presets carry meaning — don't pick colors for variety. `a-check-tag` makes toggleable filter chips.

---

### Badge  `<a-badge>` / `<a-badge-ribbon>`

**What:** A small count or status marker attached to an element; or a corner ribbon.

**Variants:** `:count` (+ `:overflow-count`), `dot`, `status` (`success|processing|error|warning|default`) + `text`, `color`, `:offset`, `:show-zero`; `a-badge-ribbon` (`text`, `placement`, `color`).

**Example:**

```vue
<script setup>
import { BellOutlined } from '@ant-design/icons-vue'
</script>

<template>
  <a-space :size="24">
    <a-badge :count="5"><BellOutlined style="font-size:20px" /></a-badge>
    <a-badge :count="120" :overflow-count="99"><a-avatar shape="square" /></a-badge>
    <a-badge dot><BellOutlined style="font-size:20px" /></a-badge>
    <a-badge status="processing" text="Running" />
  </a-space>

  <a-badge-ribbon text="New" color="red" style="margin-top:16px">
    <a-card size="small" style="width:240px">Card with ribbon</a-card>
  </a-badge-ribbon>
</template>
```

**API:** `:count` · `dot` · `status` · `text` · `color` · `:overflow-count` · `:offset`. Ribbon: `text` · `placement` · `color`.

**Tips:** Standalone `status`+`text` (no child) makes a clean inline status line — common in tables/lists.

---

### Avatar  `<a-avatar>` / `<a-avatar-group>`

**What:** Represent a user/entity with image, icon, or initials.

**Variants:** `size` (number or `large|small|default`), `shape` (`circle|square`), `src`/`srcset`, `#icon`, `alt`; `a-avatar-group` (`:max-count`, `:max-style`, `:size`).

**Example:**

```vue
<script setup>
import { UserOutlined } from '@ant-design/icons-vue'
</script>

<template>
  <a-space>
    <a-avatar><template #icon><UserOutlined /></template></a-avatar>
    <a-avatar style="background:#7c3aed">JW</a-avatar>
    <a-avatar shape="square" :size="48" src="https://i.pravatar.cc/64" />
  </a-space>

  <a-avatar-group :max-count="3" style="margin-top:12px">
    <a-avatar style="background:#f56a00">A</a-avatar>
    <a-avatar style="background:#1677ff">B</a-avatar>
    <a-avatar style="background:#52c41a">C</a-avatar>
    <a-avatar style="background:#999">D</a-avatar>
  </a-avatar-group>
</template>
```

**API:** `size` · `shape` · `src` · `alt`. Slots `#icon`. Group `:max-count` · `:size`.

**Tips:** Provide a fallback (initials in default slot or `#icon`) for when `src` fails. Use `a-avatar-group` for assignee stacks.

---

### Tooltip  `<a-tooltip>` & Popover  `<a-popover>`

**What:** Tooltip = simple text hint; Popover = richer titled content (can hold any markup).

**Variants:** `placement` (12 positions), `trigger` (`hover|focus|click|contextmenu`), `color`, `v-model:open`; Tooltip `title`/`#title`; Popover `title` + `#content`.

**Example:**

```vue
<template>
  <a-space :size="24">
    <a-tooltip title="Refresh data" placement="top">
      <a-button>Hover me</a-button>
    </a-tooltip>

    <a-popover title="Account" trigger="click">
      <template #content>
        <p>Signed in as <b>jane@acme.com</b></p>
        <a-button size="small" danger>Sign out</a-button>
      </template>
      <a-button>Click for popover</a-button>
    </a-popover>
  </a-space>
</template>
```

**API:** `title`/`#title` (Tooltip) · `#content` (Popover) · `placement` · `trigger` · `color` · `v-model:open`.

**Tips:** Tooltip for short labels (icon buttons, truncated text); Popover for small interactive content. Popconfirm (Feedback) is a specialized Popover for confirmations.

---

### Segmented  `<a-segmented>`

**What:** A compact single-select control styled as a connected pill group.

**Variants:** `:options` (`string[]` or `{ label, value, icon, disabled }[]`), `block`, `size`, `#label`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const range = ref('Week')
</script>

<template>
  <a-segmented v-model:value="range" :options="['Day', 'Week', 'Month', 'Year']" />
</template>
```

**API:** `v-model:value` · `:options` · `block` · `size`. Events `@change`. Slot `#label`.

**Tips:** Best for in-card view/time-range switches. For form fields prefer `Radio.Group`; for switching page content use `Tabs`.

---

### Collapse  `<a-collapse>`

**What:** Expandable/collapsible content panels.

**Variants:** `v-model:activeKey`, `accordion` (one open at a time), `ghost`, `:bordered`, `expand-icon-position`, per-panel `header`/`#header`, `#extra`, `collapsible` (`header|icon|disabled`).

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const active = ref(['1'])
</script>

<template>
  <a-collapse v-model:activeKey="active" accordion>
    <a-collapse-panel key="1" header="General">General settings…</a-collapse-panel>
    <a-collapse-panel key="2" header="Security">Security settings…</a-collapse-panel>
    <a-collapse-panel key="3" header="Billing">
      <template #extra><a-tag color="gold">Pro</a-tag></template>
      Billing details…
    </a-collapse-panel>
  </a-collapse>
</template>
```

**API:** `v-model:activeKey` · `accordion` · `ghost` · `:bordered`. Panel `key` · `header` · `#extra` · `collapsible`. Events `@change`.

**Tips:** `ghost` removes the container background for in-page grouping. Use for advanced/optional sections and FAQs.

---

### Timeline  `<a-timeline>`

**What:** A vertical sequence of events.

**Variants:** `mode` (`left|alternate|right`), per-item `color` (`blue|green|red|gray` or hex)/`#dot`, `:pending`, `#label`, `reverse`.

**Example:**

```vue
<template>
  <a-timeline>
    <a-timeline-item color="green">Order placed · 10:24</a-timeline-item>
    <a-timeline-item color="green">Payment captured · 10:25</a-timeline-item>
    <a-timeline-item color="blue">Packed · next day 09:10</a-timeline-item>
    <a-timeline-item color="gray">Awaiting carrier</a-timeline-item>
  </a-timeline>
</template>
```

**API:** `mode` · `:pending` · `reverse`. Item `color` · `#dot` · `#label`. 

**Tips:** Use `mode="alternate"` for a centered, two-sided history. Custom `#dot` (e.g. an icon) to flag a milestone.

---

### Tree  `<a-tree>` / `<a-directory-tree>`

**What:** Hierarchical data with optional checkboxes, selection, and drag-drop.

**Variants:** `:tree-data`; `checkable` (+ `v-model:checkedKeys`); `v-model:selectedKeys`, `v-model:expandedKeys`; `draggable`; `show-line`; `block-node`; `a-directory-tree` (file-explorer style); `#title`, `:field-names`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const checkedKeys = ref(['1-1'])
const expandedKeys = ref(['1'])
const treeData = [
  { title: 'src', key: '1', children: [
    { title: 'components', key: '1-1' }, { title: 'main.ts', key: '1-2' },
  ] },
  { title: 'package.json', key: '2' },
]
</script>

<template>
  <a-tree :tree-data="treeData" checkable
          v-model:checkedKeys="checkedKeys" v-model:expandedKeys="expandedKeys" />
</template>
```

**API:** `:tree-data` · `checkable` · `v-model:checkedKeys` · `v-model:selectedKeys` · `v-model:expandedKeys` · `draggable` · `show-line` · `:field-names`. Events `@check`, `@select`, `@expand`, `@drop`.

**Tips:** `a-directory-tree` adds folder icons & directory behavior. Map non-standard data with `:field-names="{ title, key, children }"`.

---

### Calendar  `<a-calendar>`

**What:** Month/year calendar; full-size panel or compact card.

**Variants:** `v-model:value`, `:fullscreen`, `mode` (`month|year`), `#dateCellRender`/`#monthCellRender` (badges/content per cell), `:valid-range`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
import dayjs from 'dayjs'
const value = ref(dayjs())
const events = { 14: 'Launch', 20: 'Review' }
</script>

<template>
  <div style="width:360px;border:1px solid #eee;border-radius:8px">
    <a-calendar v-model:value="value" :fullscreen="false">
      <template #dateCellRender="{ current }">
        <a-badge v-if="events[current.date()]" status="success" :text="events[current.date()]" />
      </template>
    </a-calendar>
  </div>
</template>
```

**API:** `v-model:value` · `:fullscreen` · `mode` · `:valid-range`. Slots `#dateCellRender` `#monthCellRender` `#headerRender`. Events `@select`, `@panelChange`.

**Tips:** `:fullscreen="false"` fits a card/sidebar. Use cell render slots to show events/heatmaps.

---

### Carousel  `<a-carousel>`

**What:** A rotating slideshow.

**Variants:** `autoplay`, `dots`/`:dot-position`, `effect` (`scrollx|fade`), `:after-change`; imperative `next()/prev()/goTo()` via `ref`.

**Example:**

```vue
<template>
  <a-carousel autoplay effect="fade" style="max-width:480px">
    <div><h3 class="slide">Slide 1</h3></div>
    <div><h3 class="slide">Slide 2</h3></div>
    <div><h3 class="slide">Slide 3</h3></div>
  </a-carousel>
</template>

<style scoped>
.slide { height: 160px; line-height: 160px; text-align: center; color: #fff; background: #364d79; margin: 0; }
</style>
```

**API:** `autoplay` · `dots` · `:dot-position` · `effect`. Methods (via ref): `next`, `prev`, `goTo`.

**Tips:** Each slide must be a single child element. Use sparingly in apps — rotating content is easy to miss.

---

### Image  `<a-image>`

**What:** Image with built-in preview (zoom/rotate) and fallback.

**Variants:** `:width`/`:height`, `:preview` (`false` or `{ src }`), `:fallback`, `:placeholder`, `a-image-preview-group` (gallery).

**Example:**

```vue
<template>
  <a-image :width="200" src="https://picsum.photos/400/300"
           fallback="data:image/png;base64,iVBORw0KGgo=" />

  <a-image-preview-group>
    <a-image :width="80" src="https://picsum.photos/id/10/200" />
    <a-image :width="80" src="https://picsum.photos/id/20/200" />
  </a-image-preview-group>
</template>
```

**API:** `:src` · `:width` · `:preview` · `:fallback` · `:placeholder`. Group wraps multiple images into one previewer.

**Tips:** `:preview="false"` to disable zoom. `:fallback` shows a placeholder on load error.

---

### Empty  `<a-empty>`

**What:** Empty-state placeholder.

**Variants:** `:image` (default / `Empty.PRESENTED_IMAGE_SIMPLE` / custom URL), `#description`, default slot for an action.

**Example:**

```vue
<template>
  <a-empty description="No orders yet">
    <a-button type="primary">Create order</a-button>
  </a-empty>
</template>
```

**API:** `:image` · `#description` · default slot (actions).

**Tips:** Drop inside a Card or a Table's empty area. Add a primary action so the empty state guides the next step.

---

### QRCode  `<a-qrcode>`

**What:** Render a QR code from a value.

**Variants:** `:value`, `:size`, `:icon` (center logo), `status` (`active|expired|loading|scanned`), `:error-level`, `color`/`bg-color`, `:bordered`.

**Example:**

```vue
<template>
  <a-qrcode value="https://antdv.com" :size="140" />
  <a-qrcode value="https://antdv.com" status="expired" :size="140" style="margin-left:16px" />
</template>
```

**API:** `:value` · `:size` · `:icon` · `status` · `:error-level` · `color`. 

**Tips:** Use `status="expired"` (with `@refresh`) for time-limited codes; `:icon` to brand the center.

---

### Tour  `<a-tour>`

**What:** A guided, step-by-step product walkthrough that spotlights elements.

**Variants:** `v-model:open`, `v-model:current`, `:steps` (each: `target`, `title`, `description`, `#cover`), `type` (`default|primary`), `@close`/`@finish`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const open = ref(false)
const btn = ref(null)
const steps = [
  { title: 'Create', description: 'Start a new project here.', target: () => btn.value?.$el ?? btn.value },
]
</script>

<template>
  <a-button ref="btn" type="primary" @click="open = true">Start tour</a-button>
  <a-tour v-model:open="open" :steps="steps" />
</template>
```

**API:** `v-model:open` · `v-model:current` · `:steps`. Step: `target` (fn returning element) · `title` · `description`. Events `@close`, `@finish`, `@change`.

**Tips:** `target` is a function returning the DOM node (use a template ref). Omit `target` for a centered, element-less step.
