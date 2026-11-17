## DatePickerPane 日期选择器面板 beta ​

**URL:** https://element-plus.org/zh-CN/component/date-picker-panel

**Contents:**
- DatePickerPane 日期选择器面板 beta ​
- 选择某一天 ​
- 边框 ​
- 禁用 ​
- 展示类型 ​
- 本地化 ​
- 应用开发接口（API） ​
  - 属性 ​
  - Events ​
  - 插槽 ​

DatePickerPanel是DatePicker的核心组件。

默认情况下，边框是默认的，如果你不想要边框请参考示例。 例如，DatePicker不继承border。

由于 Element Plus 的默认语言为英语，如果你需要设置其它的语言，请参考国际化文档。

要注意的是：日期相关的文字（月份，每一周的第一天等等） 也都进行了本地化配置。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="flex justify-center">
    <el-date-picker-panel v-model="value" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()
</script>
```

Example 2 (vue):
```vue
<template>
  <div
    ref="containerRef"
    :class="['date-picker--example', { 'is-narrow': isNarrow }]"
  >
    <div class="text-center">No border:</div>
    <el-divider />
    <div class="date-picker--flex-container">
      <div class="p-[20px]">
        <el-date-picker-panel v-model="value" :border="false" />
      </div>
      <el-divider
        class="divider"
        :direction="isNarrow ? 'horizontal' : 'vertical'"
      />
      <el-card>
        <el-date-picker-panel v-model="value" :border="false" />
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useElementSize } from '@vueuse/core'

const value = ref()
const containerRef = ref<HTMLElement>()

const { width } = useElementSize(containerRef)

const isNarrow = computed(() => width.value < 815)
</script>

<style scoped>
.date-picker--flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}
.divider {
  height: auto;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <div class="flex flex-col items-center">
    <el-switch
      v-model="disabled"
      active-text="Disabled"
      inactive-text="Enabled"
    />
    <el-date-picker-panel v-model="value" :disabled="disabled" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()
const disabled = ref(true)
</script>
```

Example 4 (typescript):
```typescript
<template>
  <div>
    <div class="flex gap-4">
      <div class="flex flex-col basis-150px gap-1">
        <span>Type:</span>
        <el-select v-model="type">
          <el-option
            v-for="optionType in types"
            :key="optionType"
            :value="optionType"
          />
        </el-select>
      </div>
    </div>
    <el-divider />
    <div class="flex justify-center">
      <el-date-picker-panel v-model="date" :type="type" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

import type { DatePickerType } from 'element-plus'

const date = ref()
const type = ref<DatePickerType>('date')

watch(type, () => {
  date.value = undefined
})

const types: DatePickerType[] = [
  'year',
  'years',
  'month',
  'months',
  'date',
  'dates',
  'week',
  'datetime',
  'datetimerange',
  'daterange',
  'monthrange',
  'yearrange',
]
</script>
```

---
