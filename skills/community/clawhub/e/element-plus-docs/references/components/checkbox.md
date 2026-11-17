## Checkbox 多选框 ​

**URL:** https://element-plus.org/zh-CN/component/checkbox

**Contents:**
- Checkbox 多选框 ​
- 基础用法 ​
- 禁用状态 ​
- 多选框组 ​
- Options 属性 2.11.2 ​
- 中间状态 ​
- 可选项目数量的限制 ​
- 按钮样式 ​
- 带有边框 ​
- Checkbox API ​

label 作为 value 来使用已经被 废弃, 建议label 只用来表示展示的文字，这个被废弃的用法将会在 3.0.0 版本被移除，请考虑使用新 API 替换.

新的 API value 已在 2.6.0 版本添加，文档中的示例都将使用 value。 如果您使用的版本 低于 2.6.0 并且使用 checkbox-group，请参考：

单独使用可以表示两种状态之间的切换，写在标签中的内容为 checkbox 按钮后的介绍。

checkbox-group元素能把多个 checkbox 管理为一组，只需要在 Group 中使用 v-model 绑定 Array 类型的变量即可。 只有一个选项时的默认值类型为 Boolean，当选中时值为true。 el-checkbox 标签中的内容将成为复选框按钮之后的描述。

适用于多个勾选框绑定到同一个数组的情景，通过是否勾选来表示这一组选项中选中的项。

在 el-checkbox 元素中定义 v-model 绑定变量，单一的 checkbox 中，默认绑定变量的值会是 Boolean，选中为 true。 在 el-checkbox 组件中，value 是选择框的值。 如果该组件下没有被传入内容，那么 label 将会作为 checkbox 按钮后的介绍。 value 也与数组中的元素值相对应。 如果指定的值存在于数组中，就处于选择状态，反之亦然。

基础用法 el-checkbox-group 的快捷示例。 您可以通过 props 属性自定义 options 的别名。

indeterminate 属性用以表示 checkbox 的不确定状态，一般用于实现全选的效果

使用 min 和 max 属性能够限制可以被勾选的项目的数量。

只需要把 el-checkbox 元素替换为 el-checkbox-button 元素即可。 此外，Element Plus 还提供了size属性。

设置border属性可以渲染为带有边框的多选框。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-checkbox-group v-model="checkList">
    <!-- works when >=2.6.0, recommended ✔️ value not work when <2.6.0 ❌ -->
    <el-checkbox label="Option 1" value="Value 1" />
    <!-- works when <2.6.0, deprecated act as value when >=3.0.0 -->
    <el-checkbox label="Option 2 & Value 2" />
  </el-checkbox-group>
</template>
```

Example 2 (vue):
```vue
<template>
  <div>
    <el-checkbox v-model="checked1" label="Option 1" size="large" />
    <el-checkbox v-model="checked2" label="Option 2" size="large" />
  </div>
  <div class="my-2">
    <el-checkbox v-model="checked3" label="Option 1" />
    <el-checkbox v-model="checked4" label="Option 2" />
  </div>
  <div class="mt-2">
    <el-checkbox v-model="checked5" label="Option 1" size="small" />
    <el-checkbox v-model="checked6" label="Option 2" size="small" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked1 = ref(true)
const checked2 = ref(false)
const checked3 = ref(false)
const checked4 = ref(false)
const checked5 = ref(false)
const checked6 = ref(false)
</script>
```

Example 3 (vue):
```vue
<template>
  <el-checkbox v-model="checked1" disabled>Disabled</el-checkbox>
  <el-checkbox v-model="checked2">Not disabled</el-checkbox>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked1 = ref(false)
const checked2 = ref(true)
</script>
```

Example 4 (vue):
```vue
<template>
  <el-checkbox-group v-model="checkList">
    <el-checkbox label="Option A" value="Value A" />
    <el-checkbox label="Option B" value="Value B" />
    <el-checkbox label="Option C" value="Value C" />
    <el-checkbox label="disabled" value="Value disabled" disabled />
    <el-checkbox
      label="selected and disabled"
      value="Value selected and disabled"
      disabled
    />
  </el-checkbox-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checkList = ref(['Value selected and disabled', 'Value A'])
</script>
```

---
