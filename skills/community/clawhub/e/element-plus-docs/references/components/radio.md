## Radio 单选框 ​

**URL:** https://element-plus.org/zh-CN/component/radio

**Contents:**
- Radio 单选框 ​
- 基础用法 ​
- 禁用状态 ​
- 单选框组 ​
- 带有边框 ​
- Options 属性 2.11.2 ​
- 单选按钮 ​
- Radio API ​
  - Radio Attributes ​
  - Radio Events ​

label 作为 value 来使用已经被 废弃, 建议label 只用来表示展示的文字，这个被废弃的用法将会在 3.0.0 版本被移除，请考虑使用新 API 替换.

新的 API value 已在 2.6.0 版本添加，文档中的示例都将使用 value。 如果您使用的版本 低于 2.6.0，请参考：

单选框不应该有太多的可选项， 如果你有很多的可选项你应该使用选择框而不是单选框。

要使用 Radio 组件，只需要设置v-model绑定变量， 选中意味着变量的值为相应 Radio value属性的值， value可以是String、Number 或 Boolean。

disabled 属性可以用来控制单选框的禁用状态。

你只需要为单选框设置 disabled 属性就能控制其禁用状态。

结合el-radio-group元素和子元素el-radio可以实现单选组， 为 el-radio-group 绑定 v-model，再为 每一个 el-radio 设置好 label 属性即可， 另外，还可以通过 change 事件来响应变化，它会传入一个参数 value 来表示改变之后的值。

设置 border 属性为 true 可以渲染为带有边框的单选框。

基础用法 el-radio-group 的快捷示例。 您可以通过 props 属性自定义 options 的别名。

只需要把 el-radio 元素换成 el-radio-button 元素即可， :::demo 您可以使用 填充 和 文本颜色 设置按钮的样式。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-radio-group v-model="radio1">
    <!-- works when >=2.6.0, recommended ✔️ not work when <2.6.0 ❌ -->
    <el-radio value="Value 1">Option 1</el-radio>
    <!-- works when <2.6.0, deprecated act as value when >=3.0.0 -->
    <el-radio label="Label 2 & Value 2">Option 2</el-radio>
  </el-radio-group>
</template>
```

Example 2 (vue):
```vue
<template>
  <div class="mb-2 ml-4">
    <el-radio-group v-model="radio1">
      <el-radio value="1" size="large">Option 1</el-radio>
      <el-radio value="2" size="large">Option 2</el-radio>
    </el-radio-group>
  </div>
  <div class="my-2 ml-4">
    <el-radio-group v-model="radio2">
      <el-radio value="1">Option 1</el-radio>
      <el-radio value="2">Option 2</el-radio>
    </el-radio-group>
  </div>
  <div class="my-4 ml-4">
    <el-radio-group v-model="radio3">
      <el-radio value="1" size="small">Option 1</el-radio>
      <el-radio value="2" size="small">Option 2</el-radio>
    </el-radio-group>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const radio1 = ref('1')
const radio2 = ref('1')
const radio3 = ref('1')
</script>
```

Example 3 (vue):
```vue
<template>
  <el-radio v-model="radio" disabled value="disabled">Option A</el-radio>
  <el-radio v-model="radio" disabled value="selected and disabled">
    Option B
  </el-radio>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const radio = ref('selected and disabled')
</script>
```

Example 4 (vue):
```vue
<template>
  <el-radio-group v-model="radio">
    <el-radio :value="3">Option A</el-radio>
    <el-radio :value="6">Option B</el-radio>
    <el-radio :value="9">Option C</el-radio>
  </el-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const radio = ref(3)
</script>
```

---
