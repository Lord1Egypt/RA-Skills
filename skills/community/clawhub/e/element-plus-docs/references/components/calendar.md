## Calendar 日历 ​

**URL:** https://element-plus.org/zh-CN/component/calendar

**Contents:**
- Calendar 日历 ​
- 基础用法 ​
- 控制器类型 2.13.1 ​
- 自定义内容 ​
- 范围 ​
- 自定义日历头部 ​
- 国际化 ​
- API ​
  - Attributes ​
  - Slots ​

设置 value 来指定当前显示的月份。 如果 value 未指定，则显示当月。 value 支持 v-model 双向绑定。

您可以设置日历头部的控制器类型。 设置 select时，您可以使用 formatter 自定义 label。

通过设置名为 date-cell 的 scoped-slot 来自定义日历单元格中显示的内容。 在 scoped-slot 可以获取到 date（当前单元格的日期）, data（包括 type，isSelected，day 属性）。 详情解释参考下方的 API 文档。

设置 range 属性指定日历的显示范围。 开始时间必须是周起始日，结束时间必须是周结束日，且时间跨度不能超过两个月。

由于 Element Plus 的默认语言为英语，如果你需要设置其它的语言，请参考国际化文档。

要注意的是：日期相关的文字（月份，每一周的第一天等等）也都是通过国际化来配置的。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-calendar v-model="value" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref(new Date())
</script>
```

Example 2 (vue):
```vue
<template>
  <el-radio-group v-model="controllerType">
    <el-radio-button label="select" value="select" />
    <el-radio-button label="button" value="button" />
  </el-radio-group>

  <el-calendar v-model="value" :controller-type="controllerType" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const controllerType = ref<'select' | 'button'>('select')
const value = ref(new Date())
</script>
```

Example 3 (typescript):
```typescript
<template>
  <el-calendar>
    <template #date-cell="{ data }">
      <p :class="data.isSelected ? 'is-selected' : ''">
        {{ data.day.split('-').slice(1).join('-') }}
        {{ data.isSelected ? '✔️' : '' }}
      </p>
    </template>
  </el-calendar>
</template>

<style>
.is-selected {
  color: #1989fa;
}
</style>
```

Example 4 (typescript):
```typescript
<template>
  <el-calendar :range="[new Date(2019, 2, 4), new Date(2019, 2, 24)]" />
</template>
```

---
