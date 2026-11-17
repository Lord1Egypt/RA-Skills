## Input Number 数字输入框 ​

**URL:** https://element-plus.org/zh-CN/component/input-number

**Contents:**
- Input Number 数字输入框 ​
- 基础用法 ​
- 禁用状态 ​
- 步进 ​
- 严格步进 ​
- 精度 ​
- 不同的输入框尺寸 ​
- 按钮位置 ​
- 自定义图标 2.6.3 ​
- 带前缀和后缀2.8.4 ​

要使用它，只需要在 <el-input-number> 元素中使用 v-model 绑定变量即可，变量的初始值即为默认值。

当输入无效的字符串到输入框时，由于错误，输入值将把 NaN 导入到上层

disabled属性接受一个 Boolean，设置为true即可禁用整个组件。 ，如果你只需要控制数值在某一范围内，可以设置 min 属性和 max 属性， 默认情况下，最小值是 Number.MIN_SAFE_INTEGER。

step-strictly属性接受一个Boolean。 如果这个属性被设置为 true，则只能输入步进的倍数。

设置 precision 属性可以控制数值精度，接收一个 Number。

precision 的值必须是一个非负整数，并且不能小于 step 的小数位数。

使用 size 属性额外配置尺寸，可选的尺寸大小为：large 或 small

设置 controls-position 属性可以控制按钮位置。

使用 decrease-icon 和 increase-icon 设置自定义图标。

为了确保精度，输入的数值被限制在 Number.MIN_SAFE_INTEGER 到 Number.MAX_SAFE_INTEGER 之间。

使用 formatter 来显示值，通常会同时配合 parser 一起使用。

当设置了 formatter 时，内部输入框的 type 会变为 text，从而允许输入非数字字符。 组件内部使用 Number.parseFloat 处理输入：解析成功时，将解析后的数值写入 model-value；当解析结果为 NaN 时，将 model-value 设为 null。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-input-number v-model="num" :min="1" :max="10" @change="handleChange" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(1)
const handleChange = (value: number | undefined) => {
  console.log(value)
}
</script>
```

Example 2 (vue):
```vue
<template>
  <el-input-number v-model="num" :disabled="true" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(1)
</script>
```

Example 3 (vue):
```vue
<template>
  <el-input-number v-model="num" :step="2" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(5)
</script>
```

Example 4 (vue):
```vue
<template>
  <el-input-number v-model="num" :step="2" step-strictly />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(2)
</script>
```

---
