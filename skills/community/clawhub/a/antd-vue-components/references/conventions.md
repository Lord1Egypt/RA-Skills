# Conventions — learn these once

Patterns shared by **every** ant-design-vue v4 component. Understand this page and the per-component files are just variations on it.

## 1. Install & register

```bash
npm i ant-design-vue@^4.2.6 @ant-design/icons-vue
```

**Global (most common)** — registers all components as `<a-*>`:

```ts
// main.ts
import { createApp } from 'vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'   // base reset — recommended in a normal app
import App from './App.vue'

createApp(App).use(Antd).mount('#app')
```

> v4 injects each component's styles automatically via **CSS-in-JS**, so you don't import per-component CSS. `reset.css` only normalizes base elements (`body`, `h1`, `a`, …). (Inside Slidev you *skip* it — see the `slidev-antd-dashboard` skill — but in a normal app, import it.)

**On-demand** — smaller bundle:

```ts
import { Button, Table } from 'ant-design-vue'
app.use(Button).use(Table)   // still <a-button>, <a-table> (+ their sub-components)
```

**Direct import in one SFC** (no registration) — note the tag is **PascalCase**:

```vue
<script setup>
import { Button } from 'ant-design-vue'
</script>
<template><Button type="primary">OK</Button></template>
```

All examples in this skill assume **global registration** (`<a-button>` style).

## 2. Icons

From `@ant-design/icons-vue`. Three themes per icon: `*Outlined`, `*Filled`, `*TwoTone`.

```vue
<script setup>
import { SearchOutlined, UserOutlined } from '@ant-design/icons-vue'
</script>
<template>
  <a-button type="primary">
    <template #icon><SearchOutlined /></template>
    Search
  </a-button>
  <a-avatar><template #icon><UserOutlined /></template></a-avatar>
</template>
```

Register all globally if you use many: `import * as Icons from '@ant-design/icons-vue'; for (const [k,c] of Object.entries(Icons)) app.component(k,c)` → use `<user-outlined />`.

## 3. Two-way binding: `v-model:<prop>`

Vue replaces React's "value + onChange" with `v-model:<prop>`. The prop name varies by component:

| `v-model:` | Components |
|---|---|
| `value` | Input, Textarea, InputNumber, Select, AutoComplete, Cascader, TreeSelect, DatePicker, RangePicker, TimePicker, Slider, Rate, Mentions, RadioGroup, Segmented, Calendar |
| `checked` | Checkbox, Switch |
| `open` | Modal, Drawer, Dropdown, Tooltip, Popover, Popconfirm |
| `activeKey` | Tabs, Collapse |
| `selectedKeys` / `openKeys` | Menu |
| `current` | Steps, Tour, Pagination |
| `selectedKeys` / `checkedKeys` / `expandedKeys` | Tree |
| `targetKeys` | Transfer |
| `fileList` | Upload |
| `pageSize` | Pagination (alongside `current`) |

> **v4 breaking change:** the old `visible` prop is now **`open`** (Modal/Drawer/Tooltip/Popover/Dropdown/Popconfirm). If you see `visible` in an old example, change it to `open`.

## 4. Events & the React → Vue mapping

Porting from React `antd`? Apply mechanically:

| React `antd` | ant-design-vue |
|---|---|
| `<Button>` … | `<a-button>` (all gain the `a-` prefix) |
| `onChange={fn}` / `onClick` | `@change="fn"` / `@click` |
| `onSearch` / `onSelect` / `onOk` / `onCancel` | `@search` / `@select` / `@ok` / `@cancel` |
| controlled `value` + `onChange` | `v-model:value` |
| controlled `open`/`visible` | `v-model:open` |
| `onFinish` (Form submit) | `@finish` (+ `@finishFailed`) |
| children **render prop** `=> jsx` | a **named/scoped slot** |
| `title={<X/>}` | `<template #title><X/></template>` |
| `columns:[{ render }]` | `#bodyCell` scoped slot |
| `dataSource` | `:data-source` |
| icons from `@ant-design/icons` | `@ant-design/icons-vue` |

## 5. Slots (instead of render props)

- **default** slot = the component's content.
- **named** slots replace render-prop props: `#title`, `#extra`, `#icon`, `#prefix`, `#suffix`, `#addonBefore`/`#addonAfter`, `#description`, `#avatar`, `#tabBarExtraContent`, `#footer`, …
- **scoped** slots pass data out. The big ones:
  - Table: `#bodyCell="{ column, record, index, text }"`, `#headerCell="{ column }"`, `#expandedRowRender="{ record }"`, `#title`, `#footer`.
  - List: `#renderItem="{ item, index }"`.
  - Select / TreeSelect / AutoComplete: `#option="{ value, label }"`.

```vue
<!-- Table cell customization via scoped slot -->
<a-table :columns="columns" :data-source="data" row-key="id">
  <template #bodyCell="{ column, record }">
    <template v-if="column.key === 'status'">
      <a-tag :color="record.active ? 'green' : 'red'">{{ record.active ? 'On' : 'Off' }}</a-tag>
    </template>
  </template>
</a-table>
```

## 6. Forms

**A) Template + rules (declarative):**

```vue
<script setup>
import { reactive } from 'vue'
const form = reactive({ name: '', email: '' })
const rules = {
  name: [{ required: true, message: 'Name is required' }],
  email: [{ type: 'email', message: 'Enter a valid email' }],
}
const onFinish = (values) => console.log('submit', values)
</script>
<template>
  <a-form :model="form" :rules="rules" layout="vertical"
          @finish="onFinish" @finishFailed="(e) => console.log(e)">
    <a-form-item label="Name" name="name"><a-input v-model:value="form.name" /></a-form-item>
    <a-form-item label="Email" name="email"><a-input v-model:value="form.email" /></a-form-item>
    <a-form-item><a-button type="primary" html-type="submit">Submit</a-button></a-form-item>
  </a-form>
</template>
```

- `name` on each `a-form-item` ties it to a `model` key and enables per-field validation.
- `layout`: `horizontal` (default) | `vertical` | `inline`. Control label width with `:label-col` / `:wrapper-col`.

**B) `Form.useForm` (programmatic validate/reset):**

```vue
<script setup>
import { reactive } from 'vue'
import { Form } from 'ant-design-vue'
const model = reactive({ name: '' })
const rules = reactive({ name: [{ required: true, message: 'Required' }] })
const { validate, resetFields, validateInfos } = Form.useForm(model, rules)
const submit = () => validate().then(() => {/* valid */}).catch(() => {/* invalid */})
</script>
```

## 7. Theme & design tokens

```vue
<script setup>
import { theme } from 'ant-design-vue'
const cfg = {
  token: { colorPrimary: '#7c3aed', borderRadius: 8, fontSize: 14 },
  algorithm: theme.defaultAlgorithm,   // theme.darkAlgorithm | theme.compactAlgorithm (combinable in an array)
  components: { Button: { controlHeight: 36 } },  // per-component token overrides
}
</script>
<template>
  <a-config-provider :theme="cfg">
    <a-button type="primary">Themed</a-button>
  </a-config-provider>
</template>
```

Read tokens inside a component: `const { token } = theme.useToken()` → `token.value.colorPrimary`. Dark mode = swap in `theme.darkAlgorithm`; compact = `theme.compactAlgorithm`.

## 8. Imperative feedback: message / notification / Modal

**Static (quick):**

```js
import { message, notification, Modal } from 'ant-design-vue'
message.success('Saved')
notification.open({ message: 'Done', description: 'Export finished', placement: 'topRight' })
Modal.confirm({ title: 'Delete item?', okText: 'Delete', okType: 'danger', onOk: () => {} })
```

**Context-aware (recommended)** — picks up theme/locale; wrap the root in `<a-app>`:

```vue
<!-- App.vue -->
<template><a-app><MyPage /></a-app></template>
```
```vue
<!-- inside MyPage -->
<script setup>
import { App } from 'ant-design-vue'
const { message, modal, notification } = App.useApp()
const save = () => message.success('Saved with app context')
</script>
```

## 9. Locale

```ts
import zhCN from 'ant-design-vue/es/locale/zh_CN'
// <a-config-provider :locale="zhCN"> … </a-config-provider>
```

## 10. Gotchas

- **`open`, not `visible`** (v4).
- **DatePicker/TimePicker use [Day.js](https://day.js.org), not Moment** — values are dayjs objects; format with `valueFormat`/`format`.
- **Table** needs `:columns`, `:data-source`, and a `row-key` (warns without it).
- Customize via **slots**, not render functions, in templates.
- Bind the **right** model prop (`:value` vs `:checked` vs `:open`).
- Static `message`/`Modal` calls render outside your `<a-config-provider>` tree, so they may not see your theme — use `App.useApp()` when that matters.

## Run any example

Every example in this skill is a complete SFC. To try one:

```bash
npm create vite@latest antd-play -- --template vue
cd antd-play
npm i ant-design-vue@^4.2.6 @ant-design/icons-vue
```

`src/main.js`:

```js
import { createApp } from 'vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import App from './App.vue'
createApp(App).use(Antd).mount('#app')
```

Paste an example's `<script setup>` + `<template>` into `src/App.vue`, then `npm run dev`.
