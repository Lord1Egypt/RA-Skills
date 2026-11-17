## Switch 开关 ​

**URL:** https://element-plus.org/zh-CN/component/switch

**Contents:**
- Switch 开关 ​
- 基础用法 ​
- 尺寸 ​
- 文字描述 ​
- 显示自定义图标 ​
- 扩展的 value 类型 ​
- 禁用状态 ​
- 加载状态 ​
- 阻止切换 ​
- 自定义动作图标 2.3.9 ​

表示两种相互对立的状态间的切换，多用于触发「开/关」。

绑定 v-model 到一个 Boolean 类型的变量。 可以使用 --el-switch-on-color 属性与 --el-switch-off-color 属性来设置开关的背景色。

使用active-text属性与inactive-text属性来设置开关的文字描述。 使用 inline-prompt 属性来控制文本是否显示在点内。

使用active-text属性与inactive-text属性来设置开关的文字描述。

使用 inactive-icon 和 active-icon 属性来添加图标。 您可以传递组件名称的字符串（提前注册）或组件本身是一个 SVG Vue 组件。 Element Plus 提供了一套图标，你可以在 icon 找到它们。

使用 inactive-icon 和 active-icon 属性来添加图标。 使用 inline-prompt 属性来控制图标显示在点内。

你可以设置 active-value 和 inactive-value 属性， 它们接受 Boolean、String 或 Number 类型的值。

设置disabled属性，接受一个Boolean，设置true即可禁用。

设置loading属性，接受一个Boolean，设置true即加载中状态。

设置beforeChange属性，若返回 false 或者返回 Promise 且被 reject，则停止切换。

使用 inactive-action-icon 和 active-action-icon 属性来添加图标。

使用 active-action 和 inactive-action 属性来添加图标。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-switch v-model="value1" />
  <el-switch
    v-model="value2"
    class="ml-2"
    style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(true)
const value2 = ref(true)
</script>
```

Example 2 (vue):
```vue
<template>
  <el-switch
    v-model="value"
    size="large"
    active-text="Open"
    inactive-text="Close"
  />
  <br />
  <el-switch v-model="value" active-text="Open" inactive-text="Close" />
  <br />
  <el-switch
    v-model="value"
    size="small"
    active-text="Open"
    inactive-text="Close"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref(true)
</script>
```

Example 3 (vue):
```vue
<template>
  <el-switch
    v-model="value1"
    class="mb-2"
    active-text="Pay by month"
    inactive-text="Pay by year"
  />
  <br />
  <el-switch
    v-model="value2"
    class="mb-2"
    style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
    active-text="Pay by month"
    inactive-text="Pay by year"
  />
  <br />
  <el-switch
    v-model="value3"
    inline-prompt
    active-text="是"
    inactive-text="否"
  />
  <el-switch
    v-model="value4"
    class="ml-2"
    inline-prompt
    style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
    active-text="Y"
    inactive-text="N"
  />
  <el-switch
    v-model="value6"
    class="ml-2"
    width="60"
    inline-prompt
    active-text="超出省略"
    inactive-text="超出省略"
  />
  <el-switch
    v-model="value5"
    class="ml-2"
    inline-prompt
    style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
    active-text="完整展示多个内容"
    inactive-text="多个内容"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(true)
const value2 = ref(true)
const value3 = ref(true)
const value4 = ref(true)
const value5 = ref(true)
const value6 = ref(true)
</script>
```

Example 4 (vue):
```vue
<template>
  <el-switch v-model="value1" :active-icon="Check" :inactive-icon="Close" />
  <br />
  <el-switch
    v-model="value2"
    class="mt-2"
    style="margin-left: 24px"
    inline-prompt
    :active-icon="Check"
    :inactive-icon="Close"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Check, Close } from '@element-plus/icons-vue'

const value1 = ref(true)
const value2 = ref(true)
</script>
```

---
