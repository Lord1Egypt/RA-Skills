## Select 选择器 ​

**URL:** https://element-plus.org/zh-CN/component/select

**Contents:**
- Select 选择器 ​
- 基础用法 ​
- Options 属性 2.10.5 ​
- 有禁用选项 ​
- 禁用状态 ​
- 可清空 ​
- 尺寸 ​
- 基础多选 ​
- 自定义模板 ​
- 自定义下拉菜单的头部 2.4.3 ​

当选项过多时，使用下拉菜单展示并选择内容。

在版本 2.5.0之后， el-select 的默认宽度更改为 100% 当使用内联形式时，宽度将显示异常。 为了保持显示正常, 您需要手动配置 el-select 的宽度 (如: 例子).

适用广泛的基础单选 v-model 的值为当前被选中的 el-option 的 value 属性值

el-option 基本用法。 您可以通过 props 属性自定义 options 的别名。

在 el-option 中，设定 disabled 值为 true，即可禁用该选项

为 el-select 设置 disabled属性，则整个选择器不可用。

为 el-select 设置 clearable 属性，则可将选择器清空。

使用 size 属性改变选择器大小。 除了默认大小外，还有另外两个选项： large, small。

多选选择器使用 tag 组件来展示已选中的选项。

为 el-select 设置 multiple 属性即可启用多选， 此时 v-model 的值为当前选中值所组成的数组。 默认情况下选中值会以 Tag 组件的形式展现， 你也可以设置 collapse-tags 属性将它们合并为一段文字。 您可以使用 collapse-tags-tooltip 属性来启用鼠标悬停折叠文字以显示具体所选值的行为。

use collapse-tags-tooltip

use max-collapse-tags

将自定义的 HTML 模板插入 el-option 的 slot 中即可。

Use slot to customize the content.

使用 el-option-group 对备选项进行分组，它的 label 属性为分组名

为el-select添加filterable属性即可启用搜索功能。 默认情况下，Select 会找出所有 label 属性包含输入值的选项。 如果希望使用其他的搜索逻辑，可以通过传入一个 filter-method 来实现。 filter-method 为一个 Function，它会在输入值发生变化时调用，参数为当前输入值。

从服务器搜索数据，输入关键字进行查找。为了启用远程搜索，需要将filterable和remote设置为true，同时传入一个remote-method。 remote-method为一个Function，它会在输入值发生变化时调用，参数为当前输入值。 需要注意的是，如果 el-option 是通过 v-for 指令渲染出来的，此时需要为 el-option 添加 key 属性， 且其值需具有唯一性，比如这个例子中的 item.value。

use remote-show-suffix

通过使用 allow-create 属性，用户可以通过输入框创建新项目。 为了使 allow-create 正常工作， filterable 的值必须为 true。 本例还使用了 default-first-option 属性， 在该属性为 true 的情况下，按下回车就可以选中当前选项列表中的第一个选项，无需使用鼠标或键盘方向键进行定位。

如果 Select 的绑定值为对象类型，请务必指定 value-key 作为它的唯一性标识。

通过使用 value-key 属性，可以正确处理带有重复label的数据。 这样虽然label 是重复的，但任可通过 id 来确认唯一性。

selected option's description: no select

将自定义的标签插入 el-select 的 slot 中即可。 collapse-tags, collapse-tags-tooltip, max-collapse-tags 在此模式下不生效.

若想配置如空字符串为有效值而不是空值，可以配置 empty-values 为 [null, undefined].

如果您想要将清空值更改为 null, 请设置 value-on-clear 为 null

suffix-transition 已被 弃用, 并 将会 在2.4.0中删除, 请使用覆盖样式方案。

当将 Tooltip 添加到自定义容器时（通过 append-to 属性），应将容器配置为 position: relative 或 position: absolute，以确保准确定位。 此外，如果需要防止工具提示超出其边界，可以对容器应用 overflow: hidden。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-select v-model="value" placeholder="Select" style="width: 240px">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')

const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
</script>
```

Example 2 (vue):
```vue
<template>
  <el-select
    v-model="value"
    :options="options"
    :props="props"
    placeholder="Select"
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')

const props = {
  value: 'id',
  label: 'label',
  options: 'options',
  disabled: 'disabled',
}

const options = [
  {
    id: 'Option1',
    label: 'Option1',
  },
  {
    id: 'Option2',
    label: 'Option2',
    disabled: true,
  },
  {
    id: 'Option3',
    label: 'Option3',
  },
  {
    id: 'Option4',
    label: 'Option4',
    disabled: true,
  },
  {
    id: 'Option5',
    label: 'Option5',
  },
]
</script>
```

Example 3 (vue):
```vue
<template>
  <el-select v-model="value" placeholder="Select" style="width: 240px">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
      :disabled="item.disabled"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
    disabled: true,
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
</script>
```

Example 4 (vue):
```vue
<template>
  <el-select v-model="value" disabled placeholder="Select" style="width: 240px">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
</script>
```

---
