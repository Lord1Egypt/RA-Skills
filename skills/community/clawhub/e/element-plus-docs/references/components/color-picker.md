## ColorPicker 颜色选择器 ​

**URL:** https://element-plus.org/zh-CN/component/color-picker

**Contents:**
- ColorPicker 颜色选择器 ​
- 基础用法 ​
- 选择透明度 ​
- 预定义颜色 ​
- 不同尺寸 ​
- API ​
  - Attributes ​
  - Events ​
  - Exposes ​
- 源代码 ​

使用 v-model 与 Vue 实例中的一个变量进行双向绑定，绑定的变量需要是字符串类型。

ColorPicker 支持普通颜色，也支持带 Alpha 通道的颜色，通过show-alpha属性即可控制是否支持透明度的选择。 要启用 Alpha 选择，只需添加 show-alpha 属性。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="demo-color-block">
    <span class="demonstration">With default value</span>
    <el-color-picker v-model="color1" />
  </div>
  <div class="demo-color-block">
    <span class="demonstration">With no default value</span>
    <el-color-picker v-model="color2" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color1 = ref('#409EFF')
const color2 = ref()
</script>

<style>
.demo-color-block {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}
.demo-color-block .demonstration {
  margin-right: 16px;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <el-color-picker v-model="color" show-alpha />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color = ref('rgba(19, 206, 102, 0.8)')
</script>
```

Example 3 (vue):
```vue
<template>
  <el-color-picker v-model="color" show-alpha :predefine="predefineColors" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color = ref('rgba(255, 69, 0, 0.68)')
const predefineColors = ref([
  '#ff4500',
  '#ff8c00',
  '#ffd700',
  '#90ee90',
  '#00ced1',
  '#1e90ff',
  '#c71585',
  'rgba(255, 69, 0, 0.68)',
  'rgb(255, 120, 0)',
  'hsv(51, 100, 98)',
  'hsva(120, 40, 94, 0.5)',
  'hsl(181, 100%, 37%)',
  'hsla(209, 100%, 56%, 0.73)',
  '#c7158577',
])
</script>
```

Example 4 (vue):
```vue
<template>
  <div class="demo-color-sizes">
    <el-color-picker v-model="color" size="large" />
    <el-color-picker v-model="color" />
    <el-color-picker v-model="color" size="small" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color = ref('#409EFF')
</script>

<style>
.demo-color-sizes .el-color-picker:not(:last-child) {
  margin-right: 16px;
}
</style>
```

---
