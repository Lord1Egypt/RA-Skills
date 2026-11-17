## TimePicker 时间选择器 ​

**URL:** https://element-plus.org/zh-CN/component/time-picker

**Contents:**
- TimePicker 时间选择器 ​
- 任意时间点 ​
- 限制时间选择范围 ​
- 任意时间范围 ​
- API ​
  - Attributes ​
  - 事件 ​
  - 暴露 ​
- Type Declarations ​
- 源代码 ​

提供了两种交互方式：默认情况下通过鼠标滚轮进行选择，打开arrow-control属性则通过界面上的箭头进行选择。

通过 disabledHours，disabledMinutes 和 disabledSeconds 限制可选时间范围。,

添加is-range属性即可选择时间范围。 同样支持 arrow-control 属性。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="example-basic">
    <el-time-picker v-model="value1" placeholder="Arbitrary time" />
    <el-time-picker
      v-model="value2"
      arrow-control
      placeholder="Arbitrary time"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref()
const value2 = ref()
</script>

<style>
.example-basic .el-date-editor {
  margin: 8px;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div class="example-basic">
    <el-time-picker
      v-model="value1"
      :disabled-hours="disabledHours"
      :disabled-minutes="disabledMinutes"
      :disabled-seconds="disabledSeconds"
      placeholder="Arbitrary time"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(new Date(2016, 9, 10, 18, 30))

const makeRange = (start: number, end: number) => {
  const result: number[] = []
  for (let i = start; i <= end; i++) {
    result.push(i)
  }
  return result
}
const disabledHours = () => {
  return makeRange(0, 16).concat(makeRange(19, 23))
}
const disabledMinutes = (hour: number) => {
  if (hour === 17) {
    return makeRange(0, 29)
  }
  if (hour === 18) {
    return makeRange(31, 59)
  }
  return []
}
const disabledSeconds = (hour: number, minute: number) => {
  if (hour === 18 && minute === 30) {
    return makeRange(1, 59)
  }
  return []
}
</script>

<style>
.example-basic .el-date-editor {
  margin: 8px;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <div class="demo-range">
    <el-time-picker
      v-model="value1"
      is-range
      range-separator="To"
      start-placeholder="Start time"
      end-placeholder="End time"
    />
    <el-time-picker
      v-model="value2"
      is-range
      arrow-control
      range-separator="To"
      start-placeholder="Start time"
      end-placeholder="End time"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<[Date, Date]>([
  new Date(2016, 9, 10, 8, 40),
  new Date(2016, 9, 10, 9, 40),
])
const value2 = ref<[Date, Date]>([
  new Date(2016, 9, 10, 8, 40),
  new Date(2016, 9, 10, 9, 40),
])
</script>

<style>
.demo-range .el-date-editor {
  margin: 8px;
}

.demo-range .el-range-separator {
  box-sizing: content-box;
}
</style>
```

Example 4 (typescript):
```typescript
type Placement =
  | 'top'
  | 'top-start'
  | 'top-end'
  | 'bottom'
  | 'bottom-start'
  | 'bottom-end'
  | 'left'
  | 'left-start'
  | 'left-end'
  | 'right'
  | 'right-start'
  | 'right-end'
```

---
