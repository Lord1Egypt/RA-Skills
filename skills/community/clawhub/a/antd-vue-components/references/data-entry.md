# Data Entry

Input · InputNumber · Select · AutoComplete · Cascader · TreeSelect · DatePicker · TimePicker · Checkbox · Radio · Switch · Slider · Rate · Mentions · Upload · Transfer · Form

> Shared patterns (especially `v-model:*`, events, Form) in [conventions.md](conventions.md). Inputs bind with `v-model:value`; Checkbox/Switch with `v-model:checked`.

---

### Input  `<a-input>` (+ Password / Search / Textarea / Group)

**What:** Single-line (and multi-line) text entry.

**Variants:** `a-input` · `a-input-password` · `a-input-search` (with `@search`, `enter-button`) · `a-textarea` (`:rows`, `:auto-size`) · `a-input-group` (compact/joined). Modifiers: `allow-clear`, `:maxlength`, `show-count`, `size`, `disabled`, `status="error|warning"`, `#prefix`/`#suffix`/`#addonBefore`/`#addonAfter`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
import { UserOutlined } from '@ant-design/icons-vue'
const name = ref(''); const pwd = ref(''); const bio = ref('')
</script>

<template>
  <a-space direction="vertical" style="width:320px">
    <a-input v-model:value="name" placeholder="Username" allow-clear>
      <template #prefix><UserOutlined /></template>
    </a-input>
    <a-input addon-before="https://" addon-after=".com" default-value="mysite" />
    <a-input-password v-model:value="pwd" placeholder="Password" />
    <a-input-search placeholder="Search" enter-button @search="(v) => console.log(v)" />
    <a-textarea v-model:value="bio" :rows="3" show-count :maxlength="120" />
  </a-space>
</template>
```

**API:** `v-model:value` · `allow-clear` · `:maxlength` · `show-count` · `size` · `status`. Slots: `#prefix` `#suffix` `#addonBefore` `#addonAfter`. Events `@change`, `@pressEnter`, (`@search` on Search).

**Tips:** Use `status="error"` for standalone validation; inside `<a-form-item>` validation is automatic. `a-input-search` with `enter-button` is the filter-bar search box.

---

### InputNumber  `<a-input-number>`

**What:** Numeric input with stepper, bounds, and formatting.

**Variants:** `:min`/`:max`/`:step`, `:precision`, `:formatter`/`:parser` (currency, %, thousands), `addon-before`/`addon-after`, `string` mode (big numbers), `size`, `status`, `:controls`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const price = ref(1999)
</script>

<template>
  <a-input-number
    v-model:value="price"
    :min="0" :max="100000" :step="100"
    :formatter="(v) => `$ ${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')"
    :parser="(v) => v.replace(/\$\s?|(,*)/g, '')"
    style="width: 200px"
  />
</template>
```

**API:** `v-model:value` · `:min` · `:max` · `:step` · `:precision` · `:formatter` · `:parser` · `string`. Events `@change`, `@pressEnter`.

**Tips:** Use `string` mode to avoid float precision issues with large/decimal values. `:formatter`/`:parser` come as a pair.

---

### Select  `<a-select>`

**What:** Choose one or many options from a dropdown.

**Variants:** `mode`: single (default) · `multiple` · `tags` (free entry) · `combobox`. Plus `show-search`, `:filter-option`, `:options` (vs `a-select-option` children), `allow-clear`, `:loading`, `label-in-value`, `:field-names`, `:max-tag-count`, `:option-filter-prop`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const single = ref('lucy')
const many = ref(['a'])
const options = [
  { value: 'jack', label: 'Jack' },
  { value: 'lucy', label: 'Lucy' },
  { value: 'tom', label: 'Tom', disabled: true },
]
</script>

<template>
  <a-space direction="vertical" style="width:320px">
    <a-select v-model:value="single" :options="options" style="width:100%" />
    <a-select v-model:value="many" mode="multiple" :max-tag-count="2" style="width:100%"
              :options="[{value:'a',label:'Apple'},{value:'b',label:'Banana'},{value:'c',label:'Cherry'}]" />
    <a-select show-search placeholder="Search…" style="width:100%"
              :filter-option="(input, opt) => opt.label.toLowerCase().includes(input.toLowerCase())"
              :options="options" />
  </a-space>
</template>
```

**API:** `v-model:value` · `mode` · `:options` · `show-search` · `:filter-option` · `allow-clear` · `:loading` · `label-in-value` · `:field-names`. Events `@change`, `@search`, `@select`, `@deselect`. Slots `#option`, `#suffixIcon`, `#dropdownRender`.

**Tips:** Prefer `:options` over child tags for dynamic data. `mode="tags"` lets users add new values; `combobox` is autocomplete-like. Use `:field-names="{ label, value, options }"` to map non-standard data keys.

---

### AutoComplete  `<a-auto-complete>`

**What:** A text input with a suggestion dropdown you control as the user types.

**Variants:** `:options`, `@search` to refresh them, `:filter-option`, `backfill`, wrap a custom `a-input`/`a-textarea` in the default slot.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const value = ref('')
const options = ref([])
const onSearch = (text) => {
  options.value = !text ? [] : ['gmail.com', 'outlook.com', 'yahoo.com'].map((d) => ({ value: `${text}@${d}` }))
}
</script>

<template>
  <a-auto-complete v-model:value="value" :options="options" style="width:280px"
                   placeholder="Type an email" @search="onSearch" />
</template>
```

**API:** `v-model:value` · `:options` · `:filter-option` · `backfill`. Events `@search`, `@select`, `@change`. Slots: default (custom input), `#option`.

**Tips:** Use AutoComplete for **free-text with hints**; use Select (`show-search`) when the value must be one of a fixed set.

---

### Cascader  `<a-cascader>`

**What:** Select a value from a multi-level hierarchy (region, category).

**Variants:** `:options` (nested `children`), `show-search`, `change-on-select` (allow non-leaf), `multiple`, `:field-names`, `#displayRender`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const value = ref([])
const options = [
  { value: 'us', label: 'USA', children: [
    { value: 'ca', label: 'California', children: [{ value: 'sf', label: 'San Francisco' }] },
  ] },
  { value: 'jp', label: 'Japan', children: [{ value: 'tk', label: 'Tokyo' }] },
]
</script>

<template>
  <a-cascader v-model:value="value" :options="options" placeholder="Pick a location"
              show-search style="width:280px" />
</template>
```

**API:** `v-model:value` (array path) · `:options` · `show-search` · `change-on-select` · `multiple` · `:field-names`. Events `@change`.

**Tips:** `v-model:value` is the **path array** (`['us','ca','sf']`). Use `change-on-select` to allow selecting an intermediate node.

---

### TreeSelect  `<a-tree-select>`

**What:** Like Select, but options form a tree; supports checkable multi-select.

**Variants:** `:tree-data`, `tree-checkable`, `multiple`, `show-search`, `tree-default-expand-all`, `:field-names`, `tree-node-filter-prop`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const value = ref()
const treeData = [
  { label: 'Engineering', value: 'eng', children: [
    { label: 'Frontend', value: 'fe' }, { label: 'Backend', value: 'be' },
  ] },
  { label: 'Design', value: 'design' },
]
</script>

<template>
  <a-tree-select v-model:value="value" :tree-data="treeData" tree-default-expand-all
                 allow-clear placeholder="Pick a team" style="width:280px" />
</template>
```

**API:** `v-model:value` · `:tree-data` · `tree-checkable` · `multiple` · `show-search` · `:field-names`. Events `@change`, `@select`.

**Tips:** Add `tree-checkable` for multi-select with parent/child propagation. Map custom keys with `:field-names="{ label, value, children }"`.

---

### DatePicker  `<a-date-picker>` / `<a-range-picker>`

**What:** Pick a date, date-time, or range. **Values are [Day.js](https://day.js.org) objects** in v4.

**Variants:** `a-date-picker` · `a-range-picker`; `picker`: `date|week|month|quarter|year`; `show-time`; `format` / `value-format` (string output); `:disabled-date`; `:presets`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
import dayjs from 'dayjs'
const day = ref()
const range = ref()
</script>

<template>
  <a-space direction="vertical">
    <a-date-picker v-model:value="day" />
    <a-date-picker picker="month" placeholder="Pick a month" />
    <a-date-picker show-time format="YYYY-MM-DD HH:mm" placeholder="Date & time" />
    <a-range-picker v-model:value="range"
      :presets="[
        { label: 'Last 7 days', value: [dayjs().add(-7,'d'), dayjs()] },
        { label: 'This month', value: [dayjs().startOf('month'), dayjs()] },
      ]" />
    <a-date-picker value-format="YYYY-MM-DD" @change="(d, s) => console.log(s)" />
  </a-space>
</template>
```

**API:** `v-model:value` · `picker` · `show-time` · `format` · `value-format` · `:disabled-date` · `:presets`. Events `@change`, `@ok` (with time).

**Tips:** Use `value-format` to get/set plain strings instead of dayjs objects. `:disabled-date="(cur) => cur && cur > dayjs().endOf('day')"` blocks future dates. Configure dayjs locale/plugins if you need non-default behavior.

---

### TimePicker  `<a-time-picker>`

**What:** Pick a time of day (dayjs value).

**Variants:** `format` (`HH:mm:ss`), `use12-hours`, `:minute-step`/`:second-step`, `:disabled-hours`, `a-time-range-picker`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const t = ref()
</script>

<template>
  <a-time-picker v-model:value="t" format="HH:mm" :minute-step="15" />
</template>
```

**API:** `v-model:value` · `format` · `use12-hours` · `:minute-step`. Events `@change`.

**Tips:** Same dayjs/`value-format` rules as DatePicker. For date + time together, prefer `<a-date-picker show-time>`.

---

### Checkbox  `<a-checkbox>` / `<a-checkbox-group>`

**What:** Boolean toggles; groups for multi-select.

**Variants:** single `a-checkbox` (`v-model:checked`, `indeterminate`) · `a-checkbox-group` (`v-model:value`, `:options`). Classic "check all" uses `indeterminate`.

**Example:**

```vue
<script setup>
import { ref, computed } from 'vue'
const all = ['Email', 'SMS', 'Push']
const checked = ref(['Email'])
const checkAll = computed({
  get: () => checked.value.length === all.length,
  set: (v) => (checked.value = v ? [...all] : []),
})
const indeterminate = computed(() => checked.value.length > 0 && checked.value.length < all.length)
</script>

<template>
  <a-checkbox v-model:checked="checkAll" :indeterminate="indeterminate">All channels</a-checkbox>
  <a-divider type="vertical" />
  <a-checkbox-group v-model:value="checked" :options="all" />
</template>
```

**API:** Checkbox `v-model:checked` · `indeterminate` · `disabled`. Group `v-model:value` · `:options`. Events `@change`.

**Tips:** Single checkbox = `v-model:checked` (boolean); group = `v-model:value` (array).

---

### Radio  `<a-radio-group>`

**What:** Pick exactly one option.

**Variants:** `a-radio` (dots) or `a-radio-button` (segmented); `option-type="button"` + `button-style="solid|outline"`; `:options` array; `size`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const view = ref('list')
const plan = ref('pro')
</script>

<template>
  <a-radio-group v-model:value="view">
    <a-radio value="list">List</a-radio>
    <a-radio value="grid">Grid</a-radio>
  </a-radio-group>

  <a-radio-group v-model:value="plan" option-type="button" button-style="solid" style="margin-left:16px">
    <a-radio-button value="free">Free</a-radio-button>
    <a-radio-button value="pro">Pro</a-radio-button>
    <a-radio-button value="team">Team</a-radio-button>
  </a-radio-group>
</template>
```

**API:** Group `v-model:value` · `:options` · `option-type` · `button-style` · `size`. Events `@change`.

**Tips:** For a compact toolbar toggle, also consider `Segmented` (Data Display). Radio is the form-field idiom for one-of-many.

---

### Switch  `<a-switch>`

**What:** An instant on/off toggle.

**Variants:** `checked-children`/`un-checked-children` (labels), `size="small"`, `:loading`, `disabled`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const on = ref(true)
</script>

<template>
  <a-switch v-model:checked="on" checked-children="On" un-checked-children="Off" />
  <a-switch size="small" style="margin-left:12px" />
  <a-switch :loading="true" style="margin-left:12px" />
</template>
```

**API:** `v-model:checked` · `checked-children` · `un-checked-children` · `:loading` · `size` · `disabled`. Events `@change`.

**Tips:** Switch applies **immediately**; for choices that need a Save step, use Checkbox/Radio in a form.

---

### Slider  `<a-slider>`

**What:** Pick a number (or range) by dragging.

**Variants:** `range`, `:min`/`:max`/`:step`, `:marks`, `vertical`, `dots`, `:tooltip="{ formatter }"`, `:included`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const one = ref(30)
const span = ref([20, 60])
const marks = { 0: '0°', 50: '50°', 100: { style: { color: '#f50' }, label: '100°' } }
</script>

<template>
  <a-slider v-model:value="one" :marks="marks" />
  <a-slider v-model:value="span" range :tooltip="{ formatter: (v) => `${v}%` }" />
</template>
```

**API:** `v-model:value` · `range` · `:min`/`:max`/`:step` · `:marks` · `vertical` · `:tooltip`. Events `@change`, `@afterChange`.

**Tips:** `range` makes the value a `[min, max]` array. Use `:marks` for labeled stops.

---

### Rate  `<a-rate>`

**What:** Star (or custom glyph) rating.

**Variants:** `:count`, `allow-half`, `allow-clear`, `#character` (custom glyph), `disabled`, `:tooltips`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
import { HeartOutlined } from '@ant-design/icons-vue'
const score = ref(2.5)
</script>

<template>
  <a-rate v-model:value="score" allow-half />
  <a-rate :count="5" style="margin-left:16px">
    <template #character><HeartOutlined /></template>
  </a-rate>
</template>
```

**API:** `v-model:value` · `:count` · `allow-half` · `allow-clear` · `:tooltips`. Slots `#character`. Events `@change`.

**Tips:** `allow-half` enables 0.5 steps. Provide `:tooltips="['Bad', …]"` for accessibility/clarity.

---

### Mentions  `<a-mentions>`

**What:** Textarea with `@`-style mention suggestions.

**Variants:** `:options` (v4) or `a-mentions-option` children, `prefix` (`@`, `#`, or array), `split`, `:filter-option`, `:rows`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const value = ref('Hi @')
const options = [{ value: 'mia' }, { value: 'leo' }, { value: 'ada' }]
</script>

<template>
  <a-mentions v-model:value="value" :options="options" :rows="3"
              placeholder="Type @ to mention" />
</template>
```

**API:** `v-model:value` · `:options` · `prefix` · `split` · `:filter-option`. Events `@change`, `@search`, `@select`.

**Tips:** Use `:prefix="['@', '#']"` to support both mentions and tags in one box.

---

### Upload  `<a-upload>` / `<a-upload-dragger>`

**What:** File selection/upload with a managed file list.

**Variants:** `a-upload` (button/picture) · `a-upload-dragger` (drop zone). `list-type`: `text|picture|picture-card`; `:max-count`, `multiple`, `accept`, `:before-upload` (return `false` to skip auto-upload), `:custom-request`, `directory`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
import { UploadOutlined, InboxOutlined } from '@ant-design/icons-vue'
const fileList = ref([])
// keep files locally instead of POSTing automatically:
const beforeUpload = () => false
</script>

<template>
  <a-upload v-model:file-list="fileList" :before-upload="beforeUpload" :max-count="3">
    <a-button><template #icon><UploadOutlined /></template>Select files</a-button>
  </a-upload>

  <a-upload-dragger v-model:file-list="fileList" :before-upload="beforeUpload" multiple style="margin-top:12px">
    <p class="ant-upload-drag-icon"><InboxOutlined /></p>
    <p class="ant-upload-text">Click or drag files to upload</p>
  </a-upload-dragger>
</template>
```

**API:** `v-model:file-list` (or `:file-list` + `@change`) · `list-type` · `:max-count` · `multiple` · `accept` · `:before-upload` · `:custom-request` · `action` (upload URL). Events `@change`, `@preview`, `@remove`.

**Tips:** Return `false` from `:before-upload` to manage files yourself (no auto-POST). Use `list-type="picture-card"` for image galleries/avatars. Provide `action` (URL) or `:custom-request` for real uploads.

---

### Transfer  `<a-transfer>`

**What:** Move items between two lists (assign/unassign).

**Variants:** `:data-source`, `v-model:target-keys`, `:titles`, `show-search`, `:render`, `:list-style`, `one-way`, `:selected-keys`.

**Example:**

```vue
<script setup>
import { ref } from 'vue'
const data = Array.from({ length: 8 }, (_, i) => ({ key: String(i), title: `Item ${i}` }))
const targetKeys = ref(['1', '3'])
</script>

<template>
  <a-transfer
    :data-source="data"
    v-model:target-keys="targetKeys"
    :titles="['Available', 'Assigned']"
    :render="(item) => item.title"
    show-search
  />
</template>
```

**API:** `:data-source` · `v-model:target-keys` · `:titles` · `show-search` · `:render` · `one-way`. Events `@change`, `@search`.

**Tips:** Each item needs a unique `key`. Great for permission/column/role assignment.

---

### Form  `<a-form>` / `<a-form-item>`

**What:** Layout, data binding, and validation for a set of inputs. (Base validation example + `Form.useForm` are in [conventions.md §6](conventions.md#6-forms).)

**Variants:** `layout`: `horizontal|vertical|inline`; label sizing via `:label-col`/`:wrapper-col`; `validate-trigger`; per-item `:rules`, `has-feedback`, `validate-status`/`help` (manual); dynamic field lists; `:disabled` (whole form).

**Example (layouts + dynamic rows):**

```vue
<script setup>
import { reactive } from 'vue'
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue'
const form = reactive({ project: '', tags: [{ value: '' }] })
const addTag = () => form.tags.push({ value: '' })
const removeTag = (i) => form.tags.splice(i, 1)
const onFinish = (v) => console.log(v)
</script>

<template>
  <a-form :model="form" layout="vertical" @finish="onFinish" style="max-width:480px">
    <a-form-item label="Project" name="project" :rules="[{ required: true, message: 'Required' }]">
      <a-input v-model:value="form.project" />
    </a-form-item>

    <a-form-item label="Tags">
      <div v-for="(tag, i) in form.tags" :key="i" style="display:flex;gap:8px;margin-bottom:8px">
        <a-input v-model:value="tag.value" placeholder="tag" />
        <a-button type="text" danger @click="removeTag(i)"><MinusCircleOutlined /></a-button>
      </div>
      <a-button type="dashed" block @click="addTag"><PlusOutlined /> Add tag</a-button>
    </a-form-item>

    <a-form-item>
      <a-button type="primary" html-type="submit">Save</a-button>
    </a-form-item>
  </a-form>
</template>
```

**API:** Form `:model` · `:rules` · `layout` · `:label-col`/`:wrapper-col` · `validate-trigger` · `@finish`/`@finishFailed`. Item `name` · `label` · `:rules` · `validate-status` · `help` · `has-feedback`.

**Tips:** `name` must match a `model` key for per-field validation. `layout="inline"` for filter bars, `vertical` for create/edit. For programmatic validation use `Form.useForm`. Submit via a `html-type="submit"` button + `@finish`.
