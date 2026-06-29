# Feedback

Alert · Modal · Drawer · Message · Notification · Popconfirm · Progress · Result · Skeleton · Spin · Watermark

> Shared patterns in [conventions.md](conventions.md). v4 uses **`v-model:open`** (not `visible`) for Modal/Drawer. `message`/`notification`/`Modal.confirm` are imperative — see [conventions §8](conventions.md#8-imperative-feedback-message--notification--modal).

---

### Alert  `<a-alert>`

**What:** An inline status/announcement banner.

**Variants:** `type` (`success|info|warning|error`), `message` (+ `description`), `show-icon`, `closable`, `banner` (full-width, top), `#action`, `#icon`.

**Example:**

```vue
<template>
  <a-space direction="vertical" style="width:100%">
    <a-alert type="success" message="Saved successfully" show-icon />
    <a-alert type="warning" message="Quota almost reached"
             description="You've used 90% of your plan's API calls." show-icon closable />
    <a-alert type="error" message="Payment failed" banner>
      <template #action><a-button size="small" danger>Retry</a-button></template>
    </a-alert>
  </a-space>
</template>
```

**API:** `type` · `message` · `description` · `show-icon` · `closable` · `banner`. Slots `#action` `#icon` `#description`. Events `@close`.

**Tips:** `banner` for page-top notices; `description` turns it into a richer multi-line block.

---

### Modal  `<a-modal>`

**What:** A focused dialog overlay.

**Variants:** declarative `a-modal` (`v-model:open`) or imperative `Modal.confirm/info/success/error/warning(...)`. Props: `title`, `:width`, `:footer` (`null` to hide), `:confirm-loading`, `centered`, `:mask-closable`, `ok-text`/`cancel-text`, `#footer`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
import { Modal } from 'ant-design-vue'
const open = ref(false)
const loading = ref(false)
const ok = () => { loading.value = true; setTimeout(() => { loading.value = false; open.value = false }, 800) }
const confirmDelete = () =>
  Modal.confirm({ title: 'Delete project?', content: 'This cannot be undone.',
                  okText: 'Delete', okType: 'danger', onOk: () => console.log('deleted') })
</script>

<template>
  <a-space>
    <a-button type="primary" @click="open = true">Open modal</a-button>
    <a-button danger @click="confirmDelete">Confirm dialog</a-button>
  </a-space>

  <a-modal v-model:open="open" title="Edit profile" :confirm-loading="loading" @ok="ok">
    <a-form layout="vertical"><a-form-item label="Name"><a-input /></a-form-item></a-form>
  </a-modal>
</template>
```

**API:** `v-model:open` · `title` · `:width` · `:footer` · `:confirm-loading` · `centered` · `:mask-closable`. Events `@ok`, `@cancel`. Slots default, `#title`, `#footer`. Static: `Modal.confirm/info/success/error/warning`.

**Tips:** Use the static `Modal.confirm` for quick confirmations; the component form for forms/custom footers. `:footer="null"` to fully customize.

---

### Drawer  `<a-drawer>`

**What:** A panel that slides in from an edge — good for details/edit without losing page context.

**Variants:** `placement` (`right|left|top|bottom`), `:width`/`:height`, `v-model:open`, `:mask`, `#extra`, `#footer`, nested drawers.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const open = ref(false)
</script>

<template>
  <a-button type="primary" @click="open = true">Open drawer</a-button>
  <a-drawer v-model:open="open" title="Order details" placement="right" :width="420">
    <template #extra><a-button type="primary">Save</a-button></template>
    <a-descriptions :column="1" bordered size="small">
      <a-descriptions-item label="Customer">Mia Wong</a-descriptions-item>
      <a-descriptions-item label="Total">$340.00</a-descriptions-item>
    </a-descriptions>
  </a-drawer>
</template>
```

**API:** `v-model:open` · `placement` · `:width`/`:height` · `:mask` · `:closable`. Slots default, `#title`, `#extra`, `#footer`. Events `@close`.

**Tips:** Use Drawer for larger detail/edit (many fields); Modal for short, focused tasks.

---

### Message  (`message` API)

**What:** A lightweight, auto-dismissing global toast.

**Variants:** `success` · `error` · `info` · `warning` · `loading`; `message.open({...})`; returns a closer (e.g. to end a `loading`).

**Example:**

```vue
<script setup>
import { message } from 'ant-design-vue'
const save = () => {
  const close = message.loading('Saving…', 0)
  setTimeout(() => { close(); message.success('Saved') }, 1000)
}
</script>

<template><a-button type="primary" @click="save">Save</a-button></template>
```

**API:** `message.success/error/info/warning/loading(content, duration)` · `message.open(config)`. Config: `content`, `duration`, `icon`, `key`.

**Tips:** Prefer `App.useApp().message` so toasts inherit your theme ([conventions §8](conventions.md#8-imperative-feedback-message--notification--modal)). Use `key` to update an existing message in place.

---

### Notification  (`notification` API)

**What:** A larger, corner notification with title + description; stays longer than a message.

**Variants:** `success/info/warning/error/open`; `placement` (`topRight|topLeft|bottomRight|bottomLeft`), `duration`, `btn`, `icon`, `key`.

**Example:**

```vue
<script setup>
import { notification } from 'ant-design-vue'
const notify = () =>
  notification.open({ message: 'Deployment finished', description: 'v2.4.1 is live in production.',
                      placement: 'bottomRight', duration: 4 })
</script>

<template><a-button @click="notify">Notify</a-button></template>
```

**API:** `notification.open/success/error/info/warning(config)`. Config: `message`, `description`, `placement`, `duration`, `btn`, `icon`, `key`.

**Tips:** Use for async/system events that warrant detail; use `message` for brief action feedback.

---

### Popconfirm  `<a-popconfirm>`

**What:** An inline confirmation bubble anchored to its trigger (lighter than a Modal).

**Variants:** `title` (+ `description`), `ok-text`/`cancel-text`, `ok-type`, `#icon`, `placement`, `@confirm`/`@cancel`.

**Example:**

```vue
<script setup>
import { message } from 'ant-design-vue'
</script>

<template>
  <a-popconfirm title="Delete this row?" description="This can't be undone."
                ok-text="Delete" ok-type="danger" cancel-text="Keep"
                @confirm="() => message.success('Deleted')">
    <a-button danger>Delete</a-button>
  </a-popconfirm>
</template>
```

**API:** `title` · `description` · `ok-text` · `cancel-text` · `ok-type` · `placement`. Events `@confirm`, `@cancel`. Slot: default (trigger).

**Tips:** Ideal for destructive **row** actions in tables. Use a full Modal when the confirmation needs more explanation or inputs.

---

### Progress  `<a-progress>`

**What:** Show completion of a task or a value vs. target.

**Variants:** `type` (`line|circle|dashboard`), `:percent`, `status` (`success|exception|active|normal`), `:steps`, `:stroke-color` (string or gradient), `size`, `:show-info`, `:gap-degree` (dashboard).

**Example:**

```vue
<template>
  <a-space :size="32" align="center">
    <a-progress :percent="72" :stroke-color="{ '0%': '#108ee9', '100%': '#87d068' }" style="width:200px" />
    <a-progress type="circle" :percent="90" :width="80" />
    <a-progress type="dashboard" :percent="68" status="active" />
    <a-progress :percent="100" status="success" :steps="5" style="width:200px" />
  </a-space>
</template>
```

**API:** `type` · `:percent` · `status` · `:steps` · `:stroke-color` · `size` · `:show-info`.

**Tips:** `type="dashboard"` for a gauge look in KPI cards. Pass a gradient object to `:stroke-color`.

---

### Result  `<a-result>`

**What:** A full-panel feedback page for an operation outcome.

**Variants:** `status` (`success|error|info|warning|404|403|500`), `title`, `sub-title`, `#extra` (actions), `#icon`.

**Example:**

```vue
<template>
  <a-result status="success" title="Payment successful" sub-title="Order #1042 · $340.00">
    <template #extra>
      <a-button type="primary">View order</a-button>
      <a-button>Back home</a-button>
    </template>
  </a-result>
</template>
```

**API:** `status` · `title` · `sub-title`. Slots `#extra` `#icon` `#subTitle`.

**Tips:** Use the numeric statuses (`404/403/500`) for error pages. Always give a next-step action in `#extra`.

---

### Skeleton  `<a-skeleton>`

**What:** Placeholder shimmer while content loads.

**Variants:** `a-skeleton` (`:loading`, `active`, `:avatar`, `:title`, `:paragraph={ rows }`) · `a-skeleton-button` · `a-skeleton-input` · `a-skeleton-image` · `a-skeleton-avatar`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const loading = ref(true)
</script>

<template>
  <a-button size="small" @click="loading = !loading">Toggle</a-button>
  <a-skeleton :loading="loading" active avatar :paragraph="{ rows: 3 }" style="margin-top:12px">
    <a-card><a-card-meta title="Loaded title" description="Real content shows when loading is false." /></a-card>
  </a-skeleton>
</template>
```

**API:** `:loading` · `active` · `:avatar` · `:title` · `:paragraph`. Sub-components for individual element placeholders.

**Tips:** Wrap real content in the default slot and flip `:loading` — it swaps automatically. `active` adds the shimmer animation.

---

### Spin  `<a-spin>`

**What:** A loading spinner, optionally wrapping a region.

**Variants:** `:spinning`, `tip`, `:delay`, `size` (`small|default|large`), `#indicator` (custom spinner), wrap content as default slot.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const loading = ref(true)
</script>

<template>
  <a-spin :spinning="loading" tip="Loading…">
    <a-alert type="info" message="Content behind the spinner" description="Dims while spinning." />
  </a-spin>
</template>
```

**API:** `:spinning` · `tip` · `:delay` · `size`. Slots default (wrapped content), `#indicator`.

**Tips:** `:delay` avoids flicker on fast loads. For skeletons of known shape, prefer `Skeleton`; Spin is best for indeterminate waits.

---

### Watermark  `<a-watermark>`

**What:** Overlay repeating text/image watermark on its content.

**Variants:** `:content` (string or array of lines), `:font` (`{ color, fontSize }`), `:gap`, `:offset`, `:width`/`:height`, `:rotate`, `image`.

**Example:**

```vue
<template>
  <a-watermark :content="['Acme Inc', 'Confidential']" :font="{ color: 'rgba(0,0,0,.12)' }">
    <div style="height:240px;padding:16px">Protected content area…</div>
  </a-watermark>
</template>
```

**API:** `:content` · `:font` · `:gap` · `:offset` · `:rotate` · `image`.

**Tips:** Use for confidential/demo screens. It resists casual removal but isn't true DRM.
