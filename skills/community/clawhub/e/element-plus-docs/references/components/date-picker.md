## DatePicker 日期选择器 ​

**URL:** https://element-plus.org/zh-CN/component/date-picker

**Contents:**
- DatePicker 日期选择器 ​
- 选择某一天 ​
- 其他日期单位 ​
- 选择一段时间 ​
- 选择月份范围 ​
- 年份范围2.8.0 ​
- 单个面板 2.14.0 ​
- 默认值 ​
- 日期格式 ​
- 默认显示日期 ​

基本单位由 type 属性指定。 通过 shortcuts 配置快捷选项， 通过 disabledDate 函数，来设置禁用掉的日期。

通过扩展基础的日期选择，可以选择周、月、年或多个日期

你可以通过如下例子来学习如何设置一个日期范围选择器。

在选择日期范围时，默认情况下左右面板会联动。 如果希望两个面板各自独立切换当前月份，可以使用 unlink-panels 属性解除联动。

在选择月份范围时，默认情况下左右面板会联动。 如果希望两个面板各自独立切换当前年份，可以使用 unlink-panels 属性解除联动。

你可以通过如下例子来学习如何设置一个年份范围选择器。

在选择范围时，默认情况下左右面板会联动。 如果希望两个面板各自独立切换当前年份，可以使用 unlink-panels 属性解除联动。

默认日期选择器范围有两个面板。 如果你想要一个面板设置 single-panel 属性。

日期选择器会在用户未选择任何日期的时候默认展示当天的日期。 你也可以使用 default-value 来修改这个默认的日期。 请注意该值需要是一个可以解析的 new Date() 对象。

如果类型是 daterange, default-value 则会设置左边窗口的默认值。

使用format指定输入框的格式。 使用 value-format 指定绑定值的格式。

在 这里 查看 Day.js 支持的所有格式。

在选择日期范围时，你可以指定起始日期和结束日期的默认时间。

默认情况下，开始日期和结束日期的时间部分都是选择日期当日的 00:00:00。 通过 default-time 可以分别指定开始日期和结束日期的具体时刻。 它接受最多两个日期对象的数组。 其中第一项控制起始日期的具体时刻，第二项控制结束日期的具体时刻。

当你从其他vue组件或由渲染函数生成的组件中导入组件时, 你可以设置 prefix-icon 属性来定制前缀内容

弹出框的内容是可以自定义的，在插槽内你可以获取到当前单元格的数据 请注意，自定义内容结构应与默认结构一致，否则可能风格会不一致。

由于 Element Plus 的默认语言为英语，如果你需要设置其它的语言，请参考国际化文档。

要注意的是：日期相关的文字（月份，每一周的第一天等等）也都是通过国际化来配置的。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-radio-group v-model="size" aria-label="size control" class="mb-4">
    <el-radio-button value="large">large</el-radio-button>
    <el-radio-button value="default">default</el-radio-button>
    <el-radio-button value="small">small</el-radio-button>
  </el-radio-group>
  <div class="demo-date-picker">
    <div class="block">
      <span class="demonstration">Default</span>
      <el-date-picker
        v-model="value1"
        type="date"
        placeholder="Pick a day"
        :size="size"
      />
    </div>
    <div class="block">
      <span class="demonstration">Picker with quick options</span>
      <el-date-picker
        v-model="value2"
        type="date"
        placeholder="Pick a day"
        :disabled-date="disabledDate"
        :shortcuts="shortcuts"
        :size="size"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const size = ref<'default' | 'large' | 'small'>('default')

const value1 = ref('')
const value2 = ref('')

const shortcuts = [
  {
    text: 'Today',
    value: new Date(),
  },
  {
    text: 'Yesterday',
    value: () => {
      const date = new Date()
      date.setTime(date.getTime() - 3600 * 1000 * 24)
      return date
    },
  },
  {
    text: 'A week ago',
    value: () => {
      const date = new Date()
      date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
      return date
    },
  },
]

const disabledDate = (time: Date) => {
  return time.getTime() > Date.now()
}
</script>

<style scoped>
.demo-date-picker {
  display: flex;
  width: 100%;
  padding: 0;
  flex-wrap: wrap;
}

.demo-date-picker .block {
  padding: 1.5rem 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  flex: 1;
  min-width: 300px;
}

.demo-date-picker .block:last-child {
  border-right: none;
}

.demo-date-picker .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 1rem;
}

@media screen and (max-width: 768px) {
  .demo-date-picker .block {
    flex: 0 0 100%;
    padding: 1rem 0;
    min-width: auto;
    border-right: none;
    border-bottom: solid 1px var(--el-border-color);
  }

  .demo-date-picker .block:last-child {
    border-bottom: none;
  }
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div class="demo-date-picker">
    <div class="container">
      <div class="block">
        <span class="demonstration">Week</span>
        <el-date-picker
          v-model="value1"
          type="week"
          format="[Week] ww"
          placeholder="Pick a week"
        />
      </div>
      <div class="block">
        <span class="demonstration">Dates</span>
        <el-date-picker
          v-model="value2"
          type="dates"
          placeholder="Pick one or more dates"
        />
      </div>
    </div>
    <div class="container">
      <div class="block">
        <span class="demonstration">Year</span>
        <el-date-picker
          v-model="value3"
          type="year"
          placeholder="Pick a year"
        />
      </div>
      <div class="block">
        <span class="demonstration">Years</span>
        <el-date-picker
          v-model="value4"
          type="years"
          placeholder="Pick one or more years"
        />
      </div>
    </div>
    <div class="container">
      <div class="block">
        <span class="demonstration">Month</span>
        <el-date-picker
          v-model="value5"
          type="month"
          placeholder="Pick a month"
        />
      </div>
      <div class="block">
        <span class="demonstration">Months</span>
        <el-date-picker
          v-model="value6"
          type="months"
          placeholder="Pick one or more months"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref('')
const value2 = ref('')
const value3 = ref('')
const value4 = ref('')
const value5 = ref('')
const value6 = ref('')
</script>

<style scoped>
.demo-date-picker {
  display: flex;
  width: 100%;
  padding: 0;
  flex-wrap: wrap;
}

.demo-date-picker .container {
  flex: 1;
  min-width: 300px;
  border-right: solid 1px var(--el-border-color);
}

.demo-date-picker .container:last-child {
  border-right: none;
}

.demo-date-picker .block {
  padding: 1.5rem 0;
  text-align: center;
}

.demo-date-picker .container .block:last-child {
  border-top: solid 1px var(--el-border-color);
}

.demo-date-picker .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 1rem;
}

@media screen and (max-width: 768px) {
  .demo-date-picker .container {
    flex: 0 0 100%;
    min-width: auto;
    border-right: none;
    border-bottom: solid 1px var(--el-border-color);
  }

  .demo-date-picker .container:last-child {
    border-bottom: none;
  }

  .demo-date-picker .block {
    padding: 1rem 0;
  }

  .demo-date-picker .container .block:last-child {
    border-top: solid 1px var(--el-border-color);
  }
}
</style>
```

Example 3 (vue):
```vue
<template>
  <el-radio-group v-model="size" aria-label="size control" class="mb-4">
    <el-radio-button value="large">large</el-radio-button>
    <el-radio-button value="default">default</el-radio-button>
    <el-radio-button value="small">small</el-radio-button>
  </el-radio-group>
  <div class="demo-date-picker">
    <div class="block">
      <span class="demonstration">Default</span>
      <el-date-picker
        v-model="value1"
        type="daterange"
        range-separator="To"
        start-placeholder="Start date"
        end-placeholder="End date"
        :size="size"
      />
    </div>
    <div class="block">
      <span class="demonstration">With quick options</span>
      <el-date-picker
        v-model="value2"
        type="daterange"
        unlink-panels
        range-separator="To"
        start-placeholder="Start date"
        end-placeholder="End date"
        :shortcuts="shortcuts"
        :size="size"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const size = ref<'default' | 'large' | 'small'>('default')

const value1 = ref('')
const value2 = ref('')

const shortcuts = [
  {
    text: 'Last week',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    },
  },
  {
    text: 'Last month',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    },
  },
  {
    text: 'Last 3 months',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    },
  },
]
</script>

<style scoped>
.demo-date-picker {
  display: flex;
  width: 100%;
  padding: 0;
  flex-wrap: wrap;
}

.demo-date-picker .block {
  padding: 1.5rem 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  flex: 1;
  min-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.demo-date-picker .block:last-child {
  border-right: none;
}

.demo-date-picker .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 1rem;
}

@media screen and (max-width: 1200px) {
  .demo-date-picker .block {
    flex: 0 0 100%;
    padding: 1rem 0;
    min-width: auto;
    border-right: none;
    border-bottom: solid 1px var(--el-border-color);
  }

  .demo-date-picker .block:last-child {
    border-bottom: none;
  }
}
</style>
```

Example 4 (vue):
```vue
<template>
  <div class="demo-date-picker">
    <div class="block">
      <span class="demonstration">Default</span>
      <el-date-picker
        v-model="value1"
        type="monthrange"
        range-separator="To"
        start-placeholder="Start month"
        end-placeholder="End month"
      />
    </div>
    <div class="block">
      <span class="demonstration">With quick options</span>
      <el-date-picker
        v-model="value2"
        type="monthrange"
        unlink-panels
        range-separator="To"
        start-placeholder="Start month"
        end-placeholder="End month"
        :shortcuts="shortcuts"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref('')
const value2 = ref('')

const shortcuts = [
  {
    text: 'This month',
    value: [new Date(), new Date()],
  },
  {
    text: 'This year',
    value: () => {
      const end = new Date()
      const start = new Date(new Date().getFullYear(), 0)
      return [start, end]
    },
  },
  {
    text: 'Last 6 months',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setMonth(start.getMonth() - 6)
      return [start, end]
    },
  },
]
</script>

<style scoped>
.demo-date-picker {
  display: flex;
  width: 100%;
  padding: 0;
  flex-wrap: wrap;
}

.demo-date-picker .block {
  padding: 1.5rem 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  flex: 1;
  min-width: 300px;
}

.demo-date-picker .block:last-child {
  border-right: none;
}

.demo-date-picker .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 1rem;
}

@media screen and (max-width: 768px) {
  .demo-date-picker .block {
    flex: 0 0 100%;
    padding: 1rem 0;
    min-width: auto;
    border-right: none;
    border-bottom: solid 1px var(--el-border-color);
  }

  .demo-date-picker .block:last-child {
    border-bottom: none;
  }
}
</style>
```

---
