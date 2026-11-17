## ColorPickerPanel 颜色选择器面板 beta ​

**URL:** https://element-plus.org/zh-CN/component/color-picker-panel

**Contents:**
- ColorPickerPanel 颜色选择器面板 beta ​
- 基础用法 ​
- 选择透明度 ​
- 预定义颜色 ​
- Border 边框 ​
- 禁用 ​
- API ​
  - 属性 ​
  - 插槽 ​
  - 对外暴露的方法 ​

ColorPickerPanel是ColorPicker的核心组件。

ColorPickerPanel 需要一个字符串类型的变量才能绑定到 v-model。

ColorPickerPanel 支持Alpha 通道选择。 要激活 Alpha 选择，只需添加 "show-alpha" 属性。

默认情况下，边框是默认的，如果你不想要边框请参考示例。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-color-picker-panel v-model="color" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color = ref('#409EFF')
</script>
```

Example 2 (vue):
```vue
<template>
  <el-color-picker-panel v-model="color" show-alpha />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color = ref('rgba(19, 206, 102, 0.8)')
</script>
```

Example 3 (vue):
```vue
<template>
  <el-color-picker-panel
    v-model="color"
    show-alpha
    :predefine="predefineColors"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color = ref('rgba(255, 69, 0, 0.68)')
const predefineColors = [
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
]
</script>
```

Example 4 (vue):
```vue
<template>
  <div ref="containerRef">
    <div class="text-center">No border:</div>
    <el-divider />
    <div class="flex flex-wrap justify-center gap-4">
      <div class="p-5">
        <el-color-picker-panel v-model="value" :border="false" />
      </div>
      <el-divider
        class="h-auto"
        :direction="isNarrow ? 'horizontal' : 'vertical'"
      />
      <el-card>
        <el-color-picker-panel v-model="value" :border="false" />
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useElementSize } from '@vueuse/core'

const value = ref('#ff6900')
const containerRef = ref<HTMLElement>()

const { width } = useElementSize(containerRef)

const isNarrow = computed(() => width.value < 815)
</script>
```

---
