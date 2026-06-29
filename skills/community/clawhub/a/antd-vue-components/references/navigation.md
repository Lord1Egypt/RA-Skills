# Navigation

Anchor · Breadcrumb · Dropdown · Menu · Pagination · Steps

> Shared patterns in [conventions.md](conventions.md).

---

### Menu  `<a-menu>`

**What:** The primary navigation list — vertical sidebar, inline tree, or horizontal bar.

**Variants:**
- `mode`: `inline` (collapsible tree in a sider) · `vertical` (fly-out) · `horizontal` (top bar)
- `theme`: `light` · `dark`
- state: `v-model:selectedKeys`, `v-model:openKeys`, `inline-collapsed`, `selectable`, `multiple`
- items: **slot form** (`a-menu-item`, `a-sub-menu`, `a-menu-item-group`, `a-menu-divider`) **or** `:items` array

**Example (slot form):**

```vue
<script setup>
import { ref } from 'vue'
import { MailOutlined, AppstoreOutlined, SettingOutlined } from '@ant-design/icons-vue'
const selectedKeys = ref(['inbox'])
const openKeys = ref(['mail'])
</script>

<template>
  <a-menu v-model:selectedKeys="selectedKeys" v-model:openKeys="openKeys"
          mode="inline" style="width:240px">
    <a-sub-menu key="mail">
      <template #icon><MailOutlined /></template>
      <template #title>Mail</template>
      <a-menu-item key="inbox">Inbox</a-menu-item>
      <a-menu-item key="sent">Sent</a-menu-item>
    </a-sub-menu>
    <a-menu-item-group title="Workspace">
      <a-menu-item key="apps"><template #icon><AppstoreOutlined /></template>Apps</a-menu-item>
    </a-menu-item-group>
    <a-menu-divider />
    <a-menu-item key="settings"><template #icon><SettingOutlined /></template>Settings</a-menu-item>
  </a-menu>
</template>
```

> Same menu via `:items="[{ key:'mail', icon: () => h(MailOutlined), label:'Mail', children:[…] }]"` — the array form needs `h()` render functions for icons (`import { h } from 'vue'`). The slot form is more readable.

**API:** `mode` · `theme` · `v-model:selectedKeys` · `v-model:openKeys` · `inline-collapsed` · `:items` · `trigger-sub-menu-action`. Events: `@click="({ key }) => …"`, `@select`, `@openChange`.

**Tips:** Icons on top-level items only. Keep depth ≤2 (push deeper structure into Tabs). For full nav/IA design rules, see the `slidev-antd-dashboard` skill's `navigation.md`.

---

### Dropdown  `<a-dropdown>`

**What:** A floating menu attached to a trigger element.

**Variants:** `a-dropdown` (overlay via `#overlay` or `:menu`) · `a-dropdown-button` (button + caret). `trigger`: `hover` (default) · `click` · `contextmenu`. `placement`, `arrow`, `v-model:open`, `disabled`.

**Example:**

```vue
<script setup>
import { DownOutlined } from '@ant-design/icons-vue'
const onClick = ({ key }) => console.log('chose', key)
</script>

<template>
  <a-dropdown :trigger="['click']">
    <a-button>Actions <DownOutlined /></a-button>
    <template #overlay>
      <a-menu @click="onClick">
        <a-menu-item key="edit">Edit</a-menu-item>
        <a-menu-item key="dup">Duplicate</a-menu-item>
        <a-menu-divider />
        <a-menu-item key="del" danger>Delete</a-menu-item>
      </a-menu>
    </template>
  </a-dropdown>

  <a-dropdown-button style="margin-left:12px">
    Submit
    <template #overlay><a-menu><a-menu-item key="draft">Save draft</a-menu-item></a-menu></template>
  </a-dropdown-button>
</template>
```

**API:** `trigger` · `placement` · `arrow` · `v-model:open` · `disabled`. Slots: default (trigger), `#overlay`.

**Tips:** Use for **actions** (a menu); for arbitrary hover content use `Popover`. The trigger element is the default slot; the menu goes in `#overlay`.

---

### Breadcrumb  `<a-breadcrumb>`

**What:** Shows the current location in a hierarchy.

**Variants:** `a-breadcrumb-item` children or `:items` array; custom `separator`; items with icons; an item with a dropdown `#overlay`.

**Example:**

```vue
<script setup>
import { HomeOutlined } from '@ant-design/icons-vue'
</script>

<template>
  <a-breadcrumb>
    <a-breadcrumb-item href="/"><HomeOutlined /></a-breadcrumb-item>
    <a-breadcrumb-item href="/orders">Orders</a-breadcrumb-item>
    <a-breadcrumb-item>Refund #1042</a-breadcrumb-item>
  </a-breadcrumb>

  <a-breadcrumb separator=">" style="margin-top:8px">
    <a-breadcrumb-item>Home</a-breadcrumb-item>
    <a-breadcrumb-item>Library</a-breadcrumb-item>
  </a-breadcrumb>
</template>
```

**API:** `separator` · `:items`. Item: `href` · `#overlay` (dropdown). 

**Tips:** Last segment = current page (not a link). Mirror the menu path and the page title wording.

---

### Pagination  `<a-pagination>`

**What:** Page through large data sets.

**Variants:** `v-model:current` + `v-model:pageSize`; `:total`; `show-size-changer`; `show-quick-jumper`; `simple`; `size="small"`; `:show-total`; `disabled`; `:page-size-options`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const current = ref(1)
const pageSize = ref(10)
</script>

<template>
  <a-pagination
    v-model:current="current"
    v-model:page-size="pageSize"
    :total="385"
    show-size-changer
    show-quick-jumper
    :show-total="(total, range) => `${range[0]}-${range[1]} of ${total}`"
    @change="(p, s) => console.log(p, s)"
  />
  <a-pagination simple :total="50" style="margin-top:12px" />
</template>
```

**API:** `v-model:current` · `v-model:pageSize` · `:total` · `show-size-changer` · `show-quick-jumper` · `simple` · `size` · `:show-total`. Events `@change`, `@showSizeChange`.

**Tips:** Most tables embed pagination via `<a-table :pagination="{…}">`, so you rarely use `a-pagination` standalone except for lists/galleries.

---

### Steps  `<a-steps>`

**What:** Show progress through a sequence of stages.

**Variants:** `direction` (`horizontal|vertical`), `size="small"`, `type` (`default|navigation|inline`), `:percent` (on current step), `progress-dot`, `label-placement`; per `a-step`: `title`, `sub-title`, `description`, `status` (`wait|process|finish|error`), `:icon`, `disabled`. Clickable via `v-model:current` + `@change`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const current = ref(1)
</script>

<template>
  <a-steps v-model:current="current" @change="(c) => current = c">
    <a-step title="Cart" description="Review items" />
    <a-step title="Payment" description="Enter card" />
    <a-step title="Done" description="Confirmation" />
  </a-steps>

  <a-space style="margin-top:16px">
    <a-button :disabled="current === 0" @click="current--">Prev</a-button>
    <a-button type="primary" :disabled="current === 2" @click="current++">Next</a-button>
  </a-space>

  <a-steps :current="1" direction="vertical" size="small" status="error" style="margin-top:24px">
    <a-step title="Submitted" />
    <a-step title="Validation failed" />
    <a-step title="Published" />
  </a-steps>
</template>
```

**API:** `v-model:current` · `direction` · `size` · `type` · `:percent` · `progress-dot` · `status`. Step: `title` · `sub-title` · `description` · `status` · `:icon`. Events `@change`.

**Tips:** Use Steps for **ordered** flows (wizards, fulfillment). For non-ordered view switching use Tabs/Segmented. Set a step's `status="error"` to flag a failed stage.

---

### Anchor  `<a-anchor>`

**What:** In-page jump links that highlight the section currently in view.

**Variants:** `:items` array (v4) or `a-anchor-link` children; `direction` (`vertical|horizontal`); `:affix`; `:target-offset`; `:get-container` (for a scroll container).

**Example:**

```vue
<script setup>
const items = [
  { key: 'profile', href: '#profile', title: 'Profile' },
  { key: 'security', href: '#security', title: 'Security' },
  { key: 'billing', href: '#billing', title: 'Billing' },
]
</script>

<template>
  <a-row :gutter="16">
    <a-col :span="18">
      <section id="profile" style="height:200px">Profile…</section>
      <section id="security" style="height:200px">Security…</section>
      <section id="billing" style="height:200px">Billing…</section>
    </a-col>
    <a-col :span="6"><a-anchor :items="items" :affix="false" /></a-col>
  </a-row>
</template>
```

**API:** `:items` · `direction` · `:affix` · `:target-offset` · `:get-container`. Events `@change`, `@click`.

**Tips:** For long single-page settings/docs. If the page scrolls inside a container (not the window), pass `:get-container`.
