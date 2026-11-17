## Virtualized Select 虚拟化选择器 ​

**URL:** https://element-plus.org/zh-CN/component/select-v2

**Contents:**
- Virtualized Select 虚拟化选择器 ​
- 背景 ​
- 基础用法 ​
- 多选 ​
- 尺寸 ​
- 隐藏多余标签的多选 ​
- 可过滤的多选 ​
- 禁用选择器本身或选项 ​
- 给选项进行分组 ​
- 一键清除 ​

这个组件目前在测试当中，如果在使用中发现任何漏洞和问题，请在 GitHub 中提交 issue 以便我们进行处理。

在某些使用情况下，单个选择器可能最终加载数万行数据。 将这么多的数据渲染至 DOM 中可能会给浏览器带来负担，从而造成性能问题。 为了更好的用户和开发者体验，我们决定添加此组件。

使用 size 属性改变选择器大小。 除了默认大小外，还有另外两个选项： large, small。

默认情况下选中值会以 Tag 的形式展现，你也可以设置collapse-tags属性将它们合并为一段文字。 您可以使用 collapse-tags-tooltip 属性来启用鼠标悬停折叠文字以显示具体所选值的行为。

use collapse-tags-tooltip

use max-collapse-tags

当选项太多时，你可以使用 filterable 选项来启用过滤功能来找到所需的选项。

您可以选择禁用 Select 或者 Select 中的某个选项。

只要数据格式满足特定要求，我们就可以按照自己的意愿为选项进行分组。

我们可以同时清除所有选定的选项。此设定也适用于单选。

我们也可以通过自定义模板来渲染自己想要的选项内容。

通过使用 allow-create 属性，用户可以通过输入框创建新项目。 为了使 allow-create 正常工作， filterable 的值必须为 true。 本例还使用了 default-first-option 属性， 在该属性为 true 的情况下，按下回车就可以选中当前选项列表中的第一个选项，无需使用鼠标或键盘方向键进行定位。

最好在使用 allow-create 属性的同时设置 :reserve-keyword="false"。

set reserve-keyword false

从服务器搜索数据，输入关键字进行查找。为了启用远程搜索，需要将filterable和remote设置为true，同时传入一个remote-method。 remote-method为一个Function，它会在输入值发生变化时调用，参数为当前输入值。

use remote-show-suffix

当 options.value 是一个对象时，您应该为它设置一个唯一的标识名称

在 2.4.0 之前，value-key既用作所选对象的唯一值，也用作options中表示值的对应 key。 现在 value-key 仅作为所选对象的唯一值使用，选项中值的 key 是 props.value.

当您的 options 格式不同于默认格式 您可以通过 props 属性自定义 options

将自定义的标签插入 el-select 的 slot 中即可。 collapse-tags, collapse-tags-tooltip, max-collapse-tags 在此模式下不生效.

若想配置如空字符串为有效值而不是空值，可以配置 empty-values 为 [null, undefined].

如果您想要将清空值更改为 null, 请设置 value-on-clear 为 null

下拉框的宽度默认根据label的值计算。 如果通过default slot自定义下拉框选项，选项中显示的文本可能与label的值不相等，从而导致计算错误。 在这种情况下，可以通过设置fit-input-width属性为一个数字来固定其宽度。

当将 Tooltip 添加到自定义容器时（通过 append-to 属性），应将容器配置为 position: relative 或 position: absolute，以确保准确定位。 此外，如果需要防止工具提示超出其边界，可以对容器应用 overflow: hidden。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-select-v2
    v-model="value"
    :options="options"
    placeholder="Please select"
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref()
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>
```

Example 2 (vue):
```vue
<template>
  <el-select-v2
    v-model="value"
    :options="options"
    placeholder="Please select"
    style="width: 240px"
    multiple
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref([])
const options = ref(
  Array.from({ length: 1000 }).map((_, idx) => ({
    value: `Option ${idx + 1}`,
    label: `${initials[idx % 10]}${idx}`,
  }))
)
</script>
```

Example 3 (vue):
```vue
<template>
  <div class="flex flex-wrap gap-4 items-center">
    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      size="large"
      style="width: 240px"
    />
    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
    />
    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      size="small"
      style="width: 240px"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref()
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>

<style scoped>
.example-showcase .el-select-v2 {
  margin-right: 20px;
}
</style>
```

Example 4 (vue):
```vue
<template>
  <div class="m-4">
    <p>use collapse-tags</p>
    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
      multiple
      collapse-tags
    />
  </div>
  <div class="m-4">
    <p>use collapse-tags-tooltip</p>
    <el-select-v2
      v-model="value2"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
      multiple
      collapse-tags
      collapse-tags-tooltip
    />
  </div>
  <div class="m-4">
    <p>use max-collapse-tags</p>
    <el-select-v2
      v-model="value3"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
      multiple
      collapse-tags
      collapse-tags-tooltip
      :max-collapse-tags="3"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref([])
const value2 = ref([])
const value3 = ref([])
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>
```

---
