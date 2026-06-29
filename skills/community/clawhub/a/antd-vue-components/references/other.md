# Other / system

ConfigProvider · App · theme tokens · Affix · util

> ConfigProvider, theme, and the imperative-API context are introduced in [conventions.md](conventions.md) (§7–§8). This page is the component-focused reference.

---

### ConfigProvider  `<a-config-provider>`

**What:** App-wide configuration: theme tokens/algorithm, default component size, locale, text direction, and popup mounting.

**Variants / key props:**
- `:theme="{ token, algorithm, components }"` — design tokens, dark/compact algorithm, per-component overrides
- `component-size` (`small|middle|large`) — default size for all controls
- `:locale` — i18n pack (e.g. `zh_CN`)
- `direction` (`ltr|rtl`)
- `:get-popup-container` — where overlays (dropdown/select/tooltip) mount; useful inside scaled/scrolling containers
- `:auto-insert-space-in-button`, `prefix-cls`

**Example:**

```vue
<script setup>
import { theme } from 'ant-design-vue'
const dark = {
  algorithm: theme.darkAlgorithm,
  token: { colorPrimary: '#13c2c2', borderRadius: 6 },
}
</script>

<template>
  <a-config-provider :theme="dark" component-size="small">
    <div style="padding:16px;background:#141414">
      <a-button type="primary">Dark + compact</a-button>
      <a-input style="width:160px;margin-left:8px" placeholder="small size" />
    </div>
  </a-config-provider>
</template>
```

**Tips:** Nesting is allowed — inner providers override outer. Combine algorithms in an array: `algorithm: [theme.darkAlgorithm, theme.compactAlgorithm]`. Use `:get-popup-container="(node) => node.parentNode"` when dropdowns must stay inside a scrolling/transformed box.

---

### theme tokens  (`import { theme } from 'ant-design-vue'`)

**What:** The design-token system powering ConfigProvider theming.

**Pieces:**
- **Algorithms:** `theme.defaultAlgorithm` · `theme.darkAlgorithm` · `theme.compactAlgorithm` (combine in an array).
- **`theme.useToken()`** — read resolved tokens inside a component:

```vue
<script setup>
import { theme } from 'ant-design-vue'
const { token } = theme.useToken()
// token.value.colorPrimary, token.value.borderRadius, token.value.colorBgContainer, …
</script>
<template>
  <div :style="{ background: token.colorPrimaryBg, padding: token.padding + 'px', borderRadius: token.borderRadius + 'px' }">
    Themed with live tokens
  </div>
</template>
```

- **Token layers:** *seed* (e.g. `colorPrimary`, `borderRadius`, `fontSize`) → *map* (derived scales) → *alias* (`colorBgContainer`, `colorTextSecondary`, …). Override seeds in `:theme.token`.
- **Per-component overrides:** `:theme="{ components: { Button: { colorPrimary: '#f50' }, Table: { headerBg: '#fafafa' } } }"`.

**Tips:** Prefer tokens over hard-coded colors in custom markup so it tracks light/dark automatically. `useToken` must run in a component under a ConfigProvider (the default app counts).

---

### App  `<a-app>`

**What:** A context wrapper that (1) provides theme/locale-aware `message`/`notification`/`modal` via `App.useApp()`, and (2) supplies base reset styles to its subtree.

**Example:**

```vue
<!-- App.vue: wrap once near the root -->
<template>
  <a-config-provider :theme="{ token: { colorPrimary: '#7c3aed' } }">
    <a-app><MainView /></a-app>
  </a-config-provider>
</template>
```
```vue
<!-- any descendant -->
<script setup>
import { App } from 'ant-design-vue'
const { message, modal, notification } = App.useApp()
const go = () => message.success('Uses app theme + context')
</script>
<template><a-button @click="go">Notify</a-button></template>
```

**Tips:** Use `App.useApp()` instead of the static `message`/`Modal` imports when you want feedback to inherit theme/locale and live inside the Vue tree. Wrap the app **inside** ConfigProvider so context picks up your theme.

---

### Affix  `<a-affix>`

**What:** Pin an element to the viewport (or a container) as the page scrolls.

**Variants:** `:offset-top`, `:offset-bottom`, `:target` (scroll container fn), `@change`.

**Example:**

```vue
<template>
  <a-affix :offset-top="16">
    <a-button type="primary">Sticks 16px from top</a-button>
  </a-affix>
</template>
```

**API:** `:offset-top` · `:offset-bottom` · `:target`. Events `@change` (fires when affixed state flips).

**Tips:** Use for sticky toolbars/anchors. For sticky **table headers**, prefer the Table's own `sticky` / `:scroll` instead.

---

### util / global config

**What:** Odds and ends beyond components.

- **`message`/`notification` global config:** `message.config({ top: '64px', duration: 2, maxCount: 3 })`, `notification.config({ placement: 'bottomRight' })`.
- **Static theming for imperative APIs:** when using static `Modal.confirm`/`message` outside `<a-app>`, configure once via the app's `ConfigProvider` static config, or switch to `App.useApp()` (preferred).
- **Version check:** `import { version } from 'ant-design-vue'` — handy to confirm you're on v4.x.

**Tips:** Most "utilities" you need are actually the imperative APIs (`message`/`notification`/`Modal`) in [conventions §8](conventions.md#8-imperative-feedback-message--notification--modal) and the `theme` tokens above.
