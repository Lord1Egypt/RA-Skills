---
name: "date-picker"
description: "Date Picker 日期选择器 -- Element Plus Vue3 桌面端组件。Invoke when user needs Date Picker 日期选择器 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/date-picker.html"
---

---

# DatePicker 日期选择器 [​](#datepicker-日期选择器)

更新日志待解决

66

用于选择或输入日期

## 选择某一天 [​](#选择某一天)

以”日“为基本单位，基础的日期选择控件

基本单位由 `type` 属性指定。 通过 `shortcuts` 配置快捷选项， 通过 `disabledDate` 函数，来设置禁用掉的日期。

largedefaultsmall

Default

Picker with quick options

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInNpemVcIiBhcmlhLWxhYmVsPVwic2l6ZSBjb250cm9sXCIgY2xhc3M9XCJtYi00XCI+XG4gICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cImxhcmdlXCI+bGFyZ2U8L2VsLXJhZGlvLWJ1dHRvbj5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwiZGVmYXVsdFwiPmRlZmF1bHQ8L2VsLXJhZGlvLWJ1dHRvbj5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwic21hbGxcIj5zbWFsbDwvZWwtcmFkaW8tYnV0dG9uPlxuICA8L2VsLXJhZGlvLWdyb3VwPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+RGVmYXVsdDwvc3Bhbj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgICAgdHlwZT1cImRhdGVcIlxuICAgICAgICBwbGFjZWhvbGRlcj1cIlBpY2sgYSBkYXlcIlxuICAgICAgICA6c2l6ZT1cInNpemVcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgIDxzcGFuIGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPlBpY2tlciB3aXRoIHF1aWNrIG9wdGlvbnM8L3NwYW4+XG4gICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgdi1tb2RlbD1cInZhbHVlMlwiXG4gICAgICAgIHR5cGU9XCJkYXRlXCJcbiAgICAgICAgcGxhY2Vob2xkZXI9XCJQaWNrIGEgZGF5XCJcbiAgICAgICAgOmRpc2FibGVkLWRhdGU9XCJkaXNhYmxlZERhdGVcIlxuICAgICAgICA6c2hvcnRjdXRzPVwic2hvcnRjdXRzXCJcbiAgICAgICAgOnNpemU9XCJzaXplXCJcbiAgICAgIC8+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3Qgc2l6ZSA9IHJlZjwnZGVmYXVsdCcgfCAnbGFyZ2UnIHwgJ3NtYWxsJz4oJ2RlZmF1bHQnKVxuXG5jb25zdCB2YWx1ZTEgPSByZWYoJycpXG5jb25zdCB2YWx1ZTIgPSByZWYoJycpXG5cbmNvbnN0IHNob3J0Y3V0cyA9IFtcbiAge1xuICAgIHRleHQ6ICdUb2RheScsXG4gICAgdmFsdWU6IG5ldyBEYXRlKCksXG4gIH0sXG4gIHtcbiAgICB0ZXh0OiAnWWVzdGVyZGF5JyxcbiAgICB2YWx1ZTogKCkgPT4ge1xuICAgICAgY29uc3QgZGF0ZSA9IG5ldyBEYXRlKClcbiAgICAgIGRhdGUuc2V0VGltZShkYXRlLmdldFRpbWUoKSAtIDM2MDAgKiAxMDAwICogMjQpXG4gICAgICByZXR1cm4gZGF0ZVxuICAgIH0sXG4gIH0sXG4gIHtcbiAgICB0ZXh0OiAnQSB3ZWVrIGFnbycsXG4gICAgdmFsdWU6ICgpID0+IHtcbiAgICAgIGNvbnN0IGRhdGUgPSBuZXcgRGF0ZSgpXG4gICAgICBkYXRlLnNldFRpbWUoZGF0ZS5nZXRUaW1lKCkgLSAzNjAwICogMTAwMCAqIDI0ICogNylcbiAgICAgIHJldHVybiBkYXRlXG4gICAgfSxcbiAgfSxcbl1cblxuY29uc3QgZGlzYWJsZWREYXRlID0gKHRpbWU6IERhdGUpID0+IHtcbiAgcmV0dXJuIHRpbWUuZ2V0VGltZSgpID4gRGF0ZS5ub3coKVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1kYXRlLXBpY2tlciB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIHdpZHRoOiAxMDAlO1xuICBwYWRkaW5nOiAwO1xuICBmbGV4LXdyYXA6IHdyYXA7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyIC5ibG9jayB7XG4gIHBhZGRpbmc6IDEuNXJlbSAwO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGJvcmRlci1yaWdodDogc29saWQgMXB4IHZhcigtLWVsLWJvcmRlci1jb2xvcik7XG4gIGZsZXg6IDE7XG4gIG1pbi13aWR0aDogMzAwcHg7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyIC5ibG9jazpsYXN0LWNoaWxkIHtcbiAgYm9yZGVyLXJpZ2h0OiBub25lO1xufVxuXG4uZGVtby1kYXRlLXBpY2tlciAuZGVtb25zdHJhdGlvbiB7XG4gIGRpc3BsYXk6IGJsb2NrO1xuICBjb2xvcjogdmFyKC0tZWwtdGV4dC1jb2xvci1zZWNvbmRhcnkpO1xuICBmb250LXNpemU6IDE0cHg7XG4gIG1hcmdpbi1ib3R0b206IDFyZW07XG59XG5cbkBtZWRpYSBzY3JlZW4gYW5kIChtYXgtd2lkdGg6IDc2OHB4KSB7XG4gIC5kZW1vLWRhdGUtcGlja2VyIC5ibG9jayB7XG4gICAgZmxleDogMCAwIDEwMCU7XG4gICAgcGFkZGluZzogMXJlbSAwO1xuICAgIG1pbi13aWR0aDogYXV0bztcbiAgICBib3JkZXItcmlnaHQ6IG5vbmU7XG4gICAgYm9yZGVyLWJvdHRvbTogc29saWQgMXB4IHZhcigtLWVsLWJvcmRlci1jb2xvcik7XG4gIH1cblxuICAuZGVtby1kYXRlLXBpY2tlciAuYmxvY2s6bGFzdC1jaGlsZCB7XG4gICAgYm9yZGVyLWJvdHRvbTogbm9uZTtcbiAgfVxufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/enter-date.vue)_

vue

```
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

隐藏源代码

## 其他日期单位 [​](#其他日期单位)

通过扩展基础的日期选择，可以选择周、月、年或多个日期

Week

Dates

Year

Years

Month

Months

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJjb250YWluZXJcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5XZWVrPC9zcGFuPlxuICAgICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgICAgICB0eXBlPVwid2Vla1wiXG4gICAgICAgICAgZm9ybWF0PVwiW1dlZWtdIHd3XCJcbiAgICAgICAgICBwbGFjZWhvbGRlcj1cIlBpY2sgYSB3ZWVrXCJcbiAgICAgICAgLz5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzcz1cImJsb2NrXCI+XG4gICAgICAgIDxzcGFuIGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPkRhdGVzPC9zcGFuPlxuICAgICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgICAgICB0eXBlPVwiZGF0ZXNcIlxuICAgICAgICAgIHBsYWNlaG9sZGVyPVwiUGljayBvbmUgb3IgbW9yZSBkYXRlc1wiXG4gICAgICAgIC8+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwiY29udGFpbmVyXCI+XG4gICAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+WWVhcjwvc3Bhbj5cbiAgICAgICAgPGVsLWRhdGUtcGlja2VyXG4gICAgICAgICAgdi1tb2RlbD1cInZhbHVlM1wiXG4gICAgICAgICAgdHlwZT1cInllYXJcIlxuICAgICAgICAgIHBsYWNlaG9sZGVyPVwiUGljayBhIHllYXJcIlxuICAgICAgICAvPlxuICAgICAgPC9kaXY+XG4gICAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+WWVhcnM8L3NwYW4+XG4gICAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICAgIHYtbW9kZWw9XCJ2YWx1ZTRcIlxuICAgICAgICAgIHR5cGU9XCJ5ZWFyc1wiXG4gICAgICAgICAgcGxhY2Vob2xkZXI9XCJQaWNrIG9uZSBvciBtb3JlIHllYXJzXCJcbiAgICAgICAgLz5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJjb250YWluZXJcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5Nb250aDwvc3Bhbj5cbiAgICAgICAgPGVsLWRhdGUtcGlja2VyXG4gICAgICAgICAgdi1tb2RlbD1cInZhbHVlNVwiXG4gICAgICAgICAgdHlwZT1cIm1vbnRoXCJcbiAgICAgICAgICBwbGFjZWhvbGRlcj1cIlBpY2sgYSBtb250aFwiXG4gICAgICAgIC8+XG4gICAgICA8L2Rpdj5cbiAgICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5Nb250aHM8L3NwYW4+XG4gICAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICAgIHYtbW9kZWw9XCJ2YWx1ZTZcIlxuICAgICAgICAgIHR5cGU9XCJtb250aHNcIlxuICAgICAgICAgIHBsYWNlaG9sZGVyPVwiUGljayBvbmUgb3IgbW9yZSBtb250aHNcIlxuICAgICAgICAvPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKCcnKVxuY29uc3QgdmFsdWUyID0gcmVmKCcnKVxuY29uc3QgdmFsdWUzID0gcmVmKCcnKVxuY29uc3QgdmFsdWU0ID0gcmVmKCcnKVxuY29uc3QgdmFsdWU1ID0gcmVmKCcnKVxuY29uc3QgdmFsdWU2ID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1kYXRlLXBpY2tlciB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIHdpZHRoOiAxMDAlO1xuICBwYWRkaW5nOiAwO1xuICBmbGV4LXdyYXA6IHdyYXA7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyIC5jb250YWluZXIge1xuICBmbGV4OiAxO1xuICBtaW4td2lkdGg6IDMwMHB4O1xuICBib3JkZXItcmlnaHQ6IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xufVxuXG4uZGVtby1kYXRlLXBpY2tlciAuY29udGFpbmVyOmxhc3QtY2hpbGQge1xuICBib3JkZXItcmlnaHQ6IG5vbmU7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyIC5ibG9jayB7XG4gIHBhZGRpbmc6IDEuNXJlbSAwO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyIC5jb250YWluZXIgLmJsb2NrOmxhc3QtY2hpbGQge1xuICBib3JkZXItdG9wOiBzb2xpZCAxcHggdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbn1cblxuLmRlbW8tZGF0ZS1waWNrZXIgLmRlbW9uc3RyYXRpb24ge1xuICBkaXNwbGF5OiBibG9jaztcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbiAgZm9udC1zaXplOiAxNHB4O1xuICBtYXJnaW4tYm90dG9tOiAxcmVtO1xufVxuXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA3NjhweCkge1xuICAuZGVtby1kYXRlLXBpY2tlciAuY29udGFpbmVyIHtcbiAgICBmbGV4OiAwIDAgMTAwJTtcbiAgICBtaW4td2lkdGg6IGF1dG87XG4gICAgYm9yZGVyLXJpZ2h0OiBub25lO1xuICAgIGJvcmRlci1ib3R0b206IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICB9XG5cbiAgLmRlbW8tZGF0ZS1waWNrZXIgLmNvbnRhaW5lcjpsYXN0LWNoaWxkIHtcbiAgICBib3JkZXItYm90dG9tOiBub25lO1xuICB9XG5cbiAgLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrIHtcbiAgICBwYWRkaW5nOiAxcmVtIDA7XG4gIH1cblxuICAuZGVtby1kYXRlLXBpY2tlciAuY29udGFpbmVyIC5ibG9jazpsYXN0LWNoaWxkIHtcbiAgICBib3JkZXItdG9wOiBzb2xpZCAxcHggdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbiAgfVxufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/other-measurements.vue)_

vue

```
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

隐藏源代码

## 选择一段时间 [​](#选择一段时间)

你可以通过如下例子来学习如何设置一个日期范围选择器。

在选择日期范围时，默认情况下左右面板会联动。 如果希望两个面板各自独立切换当前月份，可以使用 `unlink-panels` 属性解除联动。

largedefaultsmall

Default

To

With quick options

To

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInNpemVcIiBhcmlhLWxhYmVsPVwic2l6ZSBjb250cm9sXCIgY2xhc3M9XCJtYi00XCI+XG4gICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cImxhcmdlXCI+bGFyZ2U8L2VsLXJhZGlvLWJ1dHRvbj5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwiZGVmYXVsdFwiPmRlZmF1bHQ8L2VsLXJhZGlvLWJ1dHRvbj5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwic21hbGxcIj5zbWFsbDwvZWwtcmFkaW8tYnV0dG9uPlxuICA8L2VsLXJhZGlvLWdyb3VwPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+RGVmYXVsdDwvc3Bhbj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgICAgdHlwZT1cImRhdGVyYW5nZVwiXG4gICAgICAgIHJhbmdlLXNlcGFyYXRvcj1cIlRvXCJcbiAgICAgICAgc3RhcnQtcGxhY2Vob2xkZXI9XCJTdGFydCBkYXRlXCJcbiAgICAgICAgZW5kLXBsYWNlaG9sZGVyPVwiRW5kIGRhdGVcIlxuICAgICAgICA6c2l6ZT1cInNpemVcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgIDxzcGFuIGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPldpdGggcXVpY2sgb3B0aW9uczwvc3Bhbj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgICAgdHlwZT1cImRhdGVyYW5nZVwiXG4gICAgICAgIHVubGluay1wYW5lbHNcbiAgICAgICAgcmFuZ2Utc2VwYXJhdG9yPVwiVG9cIlxuICAgICAgICBzdGFydC1wbGFjZWhvbGRlcj1cIlN0YXJ0IGRhdGVcIlxuICAgICAgICBlbmQtcGxhY2Vob2xkZXI9XCJFbmQgZGF0ZVwiXG4gICAgICAgIDpzaG9ydGN1dHM9XCJzaG9ydGN1dHNcIlxuICAgICAgICA6c2l6ZT1cInNpemVcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBzaXplID0gcmVmPCdkZWZhdWx0JyB8ICdsYXJnZScgfCAnc21hbGwnPignZGVmYXVsdCcpXG5cbmNvbnN0IHZhbHVlMSA9IHJlZignJylcbmNvbnN0IHZhbHVlMiA9IHJlZignJylcblxuY29uc3Qgc2hvcnRjdXRzID0gW1xuICB7XG4gICAgdGV4dDogJ0xhc3Qgd2VlaycsXG4gICAgdmFsdWU6ICgpID0+IHtcbiAgICAgIGNvbnN0IGVuZCA9IG5ldyBEYXRlKClcbiAgICAgIGNvbnN0IHN0YXJ0ID0gbmV3IERhdGUoKVxuICAgICAgc3RhcnQuc2V0VGltZShzdGFydC5nZXRUaW1lKCkgLSAzNjAwICogMTAwMCAqIDI0ICogNylcbiAgICAgIHJldHVybiBbc3RhcnQsIGVuZF1cbiAgICB9LFxuICB9LFxuICB7XG4gICAgdGV4dDogJ0xhc3QgbW9udGgnLFxuICAgIHZhbHVlOiAoKSA9PiB7XG4gICAgICBjb25zdCBlbmQgPSBuZXcgRGF0ZSgpXG4gICAgICBjb25zdCBzdGFydCA9IG5ldyBEYXRlKClcbiAgICAgIHN0YXJ0LnNldFRpbWUoc3RhcnQuZ2V0VGltZSgpIC0gMzYwMCAqIDEwMDAgKiAyNCAqIDMwKVxuICAgICAgcmV0dXJuIFtzdGFydCwgZW5kXVxuICAgIH0sXG4gIH0sXG4gIHtcbiAgICB0ZXh0OiAnTGFzdCAzIG1vbnRocycsXG4gICAgdmFsdWU6ICgpID0+IHtcbiAgICAgIGNvbnN0IGVuZCA9IG5ldyBEYXRlKClcbiAgICAgIGNvbnN0IHN0YXJ0ID0gbmV3IERhdGUoKVxuICAgICAgc3RhcnQuc2V0VGltZShzdGFydC5nZXRUaW1lKCkgLSAzNjAwICogMTAwMCAqIDI0ICogOTApXG4gICAgICByZXR1cm4gW3N0YXJ0LCBlbmRdXG4gICAgfSxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tZGF0ZS1waWNrZXIge1xuICBkaXNwbGF5OiBmbGV4O1xuICB3aWR0aDogMTAwJTtcbiAgcGFkZGluZzogMDtcbiAgZmxleC13cmFwOiB3cmFwO1xufVxuXG4uZGVtby1kYXRlLXBpY2tlciAuYmxvY2sge1xuICBwYWRkaW5nOiAxLjVyZW0gMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBib3JkZXItcmlnaHQ6IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICBmbGV4OiAxO1xuICBtaW4td2lkdGg6IDQwMHB4O1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuXG4uZGVtby1kYXRlLXBpY2tlciAuYmxvY2s6bGFzdC1jaGlsZCB7XG4gIGJvcmRlci1yaWdodDogbm9uZTtcbn1cblxuLmRlbW8tZGF0ZS1waWNrZXIgLmRlbW9uc3RyYXRpb24ge1xuICBkaXNwbGF5OiBibG9jaztcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbiAgZm9udC1zaXplOiAxNHB4O1xuICBtYXJnaW4tYm90dG9tOiAxcmVtO1xufVxuXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiAxMjAwcHgpIHtcbiAgLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrIHtcbiAgICBmbGV4OiAwIDAgMTAwJTtcbiAgICBwYWRkaW5nOiAxcmVtIDA7XG4gICAgbWluLXdpZHRoOiBhdXRvO1xuICAgIGJvcmRlci1yaWdodDogbm9uZTtcbiAgICBib3JkZXItYm90dG9tOiBzb2xpZCAxcHggdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbiAgfVxuXG4gIC5kZW1vLWRhdGUtcGlja2VyIC5ibG9jazpsYXN0LWNoaWxkIHtcbiAgICBib3JkZXItYm90dG9tOiBub25lO1xuICB9XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/date-range.vue)_

vue

```
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

隐藏源代码

## 选择月份范围 [​](#选择月份范围)

你当然还可以选择一个月的范围。

在选择月份范围时，默认情况下左右面板会联动。 如果希望两个面板各自独立切换当前年份，可以使用 `unlink-panels` 属性解除联动。

Default

To

With quick options

To

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+RGVmYXVsdDwvc3Bhbj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgICAgdHlwZT1cIm1vbnRocmFuZ2VcIlxuICAgICAgICByYW5nZS1zZXBhcmF0b3I9XCJUb1wiXG4gICAgICAgIHN0YXJ0LXBsYWNlaG9sZGVyPVwiU3RhcnQgbW9udGhcIlxuICAgICAgICBlbmQtcGxhY2Vob2xkZXI9XCJFbmQgbW9udGhcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgIDxzcGFuIGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPldpdGggcXVpY2sgb3B0aW9uczwvc3Bhbj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgICAgdHlwZT1cIm1vbnRocmFuZ2VcIlxuICAgICAgICB1bmxpbmstcGFuZWxzXG4gICAgICAgIHJhbmdlLXNlcGFyYXRvcj1cIlRvXCJcbiAgICAgICAgc3RhcnQtcGxhY2Vob2xkZXI9XCJTdGFydCBtb250aFwiXG4gICAgICAgIGVuZC1wbGFjZWhvbGRlcj1cIkVuZCBtb250aFwiXG4gICAgICAgIDpzaG9ydGN1dHM9XCJzaG9ydGN1dHNcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZTEgPSByZWYoJycpXG5jb25zdCB2YWx1ZTIgPSByZWYoJycpXG5cbmNvbnN0IHNob3J0Y3V0cyA9IFtcbiAge1xuICAgIHRleHQ6ICdUaGlzIG1vbnRoJyxcbiAgICB2YWx1ZTogW25ldyBEYXRlKCksIG5ldyBEYXRlKCldLFxuICB9LFxuICB7XG4gICAgdGV4dDogJ1RoaXMgeWVhcicsXG4gICAgdmFsdWU6ICgpID0+IHtcbiAgICAgIGNvbnN0IGVuZCA9IG5ldyBEYXRlKClcbiAgICAgIGNvbnN0IHN0YXJ0ID0gbmV3IERhdGUobmV3IERhdGUoKS5nZXRGdWxsWWVhcigpLCAwKVxuICAgICAgcmV0dXJuIFtzdGFydCwgZW5kXVxuICAgIH0sXG4gIH0sXG4gIHtcbiAgICB0ZXh0OiAnTGFzdCA2IG1vbnRocycsXG4gICAgdmFsdWU6ICgpID0+IHtcbiAgICAgIGNvbnN0IGVuZCA9IG5ldyBEYXRlKClcbiAgICAgIGNvbnN0IHN0YXJ0ID0gbmV3IERhdGUoKVxuICAgICAgc3RhcnQuc2V0TW9udGgoc3RhcnQuZ2V0TW9udGgoKSAtIDYpXG4gICAgICByZXR1cm4gW3N0YXJ0LCBlbmRdXG4gICAgfSxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tZGF0ZS1waWNrZXIge1xuICBkaXNwbGF5OiBmbGV4O1xuICB3aWR0aDogMTAwJTtcbiAgcGFkZGluZzogMDtcbiAgZmxleC13cmFwOiB3cmFwO1xufVxuXG4uZGVtby1kYXRlLXBpY2tlciAuYmxvY2sge1xuICBwYWRkaW5nOiAxLjVyZW0gMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBib3JkZXItcmlnaHQ6IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICBmbGV4OiAxO1xuICBtaW4td2lkdGg6IDMwMHB4O1xufVxuXG4uZGVtby1kYXRlLXBpY2tlciAuYmxvY2s6bGFzdC1jaGlsZCB7XG4gIGJvcmRlci1yaWdodDogbm9uZTtcbn1cblxuLmRlbW8tZGF0ZS1waWNrZXIgLmRlbW9uc3RyYXRpb24ge1xuICBkaXNwbGF5OiBibG9jaztcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbiAgZm9udC1zaXplOiAxNHB4O1xuICBtYXJnaW4tYm90dG9tOiAxcmVtO1xufVxuXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA3NjhweCkge1xuICAuZGVtby1kYXRlLXBpY2tlciAuYmxvY2sge1xuICAgIGZsZXg6IDAgMCAxMDAlO1xuICAgIHBhZGRpbmc6IDFyZW0gMDtcbiAgICBtaW4td2lkdGg6IGF1dG87XG4gICAgYm9yZGVyLXJpZ2h0OiBub25lO1xuICAgIGJvcmRlci1ib3R0b206IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICB9XG5cbiAgLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrOmxhc3QtY2hpbGQge1xuICAgIGJvcmRlci1ib3R0b206IG5vbmU7XG4gIH1cbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/month-range.vue)_

vue

```
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

隐藏源代码

## 年份范围2.8.0 [​](#年份范围)

你可以通过如下例子来学习如何设置一个年份范围选择器。

在选择范围时，默认情况下左右面板会联动。 如果希望两个面板各自独立切换当前年份，可以使用 `unlink-panels` 属性解除联动。

Default

To

With quick options

To

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+RGVmYXVsdDwvc3Bhbj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgICAgdHlwZT1cInllYXJyYW5nZVwiXG4gICAgICAgIHJhbmdlLXNlcGFyYXRvcj1cIlRvXCJcbiAgICAgICAgc3RhcnQtcGxhY2Vob2xkZXI9XCJTdGFydCBZZWFyXCJcbiAgICAgICAgZW5kLXBsYWNlaG9sZGVyPVwiRW5kIFllYXJcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgIDxzcGFuIGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPldpdGggcXVpY2sgb3B0aW9uczwvc3Bhbj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgICAgdHlwZT1cInllYXJyYW5nZVwiXG4gICAgICAgIHVubGluay1wYW5lbHNcbiAgICAgICAgcmFuZ2Utc2VwYXJhdG9yPVwiVG9cIlxuICAgICAgICBzdGFydC1wbGFjZWhvbGRlcj1cIlN0YXJ0IFllYXJcIlxuICAgICAgICBlbmQtcGxhY2Vob2xkZXI9XCJFbmQgWWVhclwiXG4gICAgICAgIDpzaG9ydGN1dHM9XCJzaG9ydGN1dHNcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZTEgPSByZWYoKVxuY29uc3QgdmFsdWUyID0gcmVmKClcblxuY29uc3Qgc2hvcnRjdXRzID0gW1xuICB7XG4gICAgdGV4dDogJ1RoaXMgWWVhcicsXG4gICAgdmFsdWU6IFtuZXcgRGF0ZSgpLCBuZXcgRGF0ZSgpXSxcbiAgfSxcbiAge1xuICAgIHRleHQ6ICdMYXN0IDEwIHllYXJzJyxcbiAgICB2YWx1ZTogKCkgPT4ge1xuICAgICAgY29uc3QgZW5kID0gbmV3IERhdGUoKVxuICAgICAgY29uc3Qgc3RhcnQgPSBuZXcgRGF0ZShcbiAgICAgICAgbmV3IERhdGUoKS5zZXRGdWxsWWVhcihuZXcgRGF0ZSgpLmdldEZ1bGxZZWFyKCkgLSAxMClcbiAgICAgIClcbiAgICAgIHJldHVybiBbc3RhcnQsIGVuZF1cbiAgICB9LFxuICB9LFxuICB7XG4gICAgdGV4dDogJ05leHQgNTAgeWVhcnMnLFxuICAgIHZhbHVlOiAoKSA9PiB7XG4gICAgICBjb25zdCBzdGFydCA9IG5ldyBEYXRlKClcbiAgICAgIGNvbnN0IGVuZCA9IG5ldyBEYXRlKFxuICAgICAgICBuZXcgRGF0ZSgpLnNldEZ1bGxZZWFyKG5ldyBEYXRlKCkuZ2V0RnVsbFllYXIoKSArIDUwKVxuICAgICAgKVxuICAgICAgcmV0dXJuIFtzdGFydCwgZW5kXVxuICAgIH0sXG4gIH0sXG5dXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLWRhdGUtcGlja2VyIHtcbiAgZGlzcGxheTogZmxleDtcbiAgd2lkdGg6IDEwMCU7XG4gIHBhZGRpbmc6IDA7XG4gIGZsZXgtd3JhcDogd3JhcDtcbn1cblxuLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrIHtcbiAgcGFkZGluZzogMS41cmVtIDA7XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbiAgYm9yZGVyLXJpZ2h0OiBzb2xpZCAxcHggdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbiAgZmxleDogMTtcbiAgbWluLXdpZHRoOiAzMDBweDtcbn1cblxuLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrOmxhc3QtY2hpbGQge1xuICBib3JkZXItcmlnaHQ6IG5vbmU7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyIC5kZW1vbnN0cmF0aW9uIHtcbiAgZGlzcGxheTogYmxvY2s7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG4gIGZvbnQtc2l6ZTogMTRweDtcbiAgbWFyZ2luLWJvdHRvbTogMXJlbTtcbn1cblxuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogNzY4cHgpIHtcbiAgLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrIHtcbiAgICBmbGV4OiAwIDAgMTAwJTtcbiAgICBwYWRkaW5nOiAxcmVtIDA7XG4gICAgbWluLXdpZHRoOiBhdXRvO1xuICAgIGJvcmRlci1yaWdodDogbm9uZTtcbiAgICBib3JkZXItYm90dG9tOiBzb2xpZCAxcHggdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbiAgfVxuXG4gIC5kZW1vLWRhdGUtcGlja2VyIC5ibG9jazpsYXN0LWNoaWxkIHtcbiAgICBib3JkZXItYm90dG9tOiBub25lO1xuICB9XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/year-range.vue)_

vue

```
<template>
  <div class="demo-date-picker">
    <div class="block">
      <span class="demonstration">Default</span>
      <el-date-picker
        v-model="value1"
        type="yearrange"
        range-separator="To"
        start-placeholder="Start Year"
        end-placeholder="End Year"
      />
    </div>
    <div class="block">
      <span class="demonstration">With quick options</span>
      <el-date-picker
        v-model="value2"
        type="yearrange"
        unlink-panels
        range-separator="To"
        start-placeholder="Start Year"
        end-placeholder="End Year"
        :shortcuts="shortcuts"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref()
const value2 = ref()

const shortcuts = [
  {
    text: 'This Year',
    value: [new Date(), new Date()],
  },
  {
    text: 'Last 10 years',
    value: () => {
      const end = new Date()
      const start = new Date(
        new Date().setFullYear(new Date().getFullYear() - 10)
      )
      return [start, end]
    },
  },
  {
    text: 'Next 50 years',
    value: () => {
      const start = new Date()
      const end = new Date(
        new Date().setFullYear(new Date().getFullYear() + 50)
      )
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

隐藏源代码

## 单个面板 2.14.0 [​](#单个面板)

默认日期选择器范围有两个面板。 如果你想要一个面板设置 `single-panel` 属性。

date range

\-

month range

\-

year range

\-

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+ZGF0ZSByYW5nZTwvc3Bhbj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlciB2LW1vZGVsPVwidmFsdWUxXCIgdHlwZT1cImRhdGVyYW5nZVwiIHNpbmdsZS1wYW5lbCAvPlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+bW9udGggcmFuZ2U8L3NwYW4+XG4gICAgICA8ZWwtZGF0ZS1waWNrZXIgdi1tb2RlbD1cInZhbHVlMlwiIHR5cGU9XCJtb250aHJhbmdlXCIgc2luZ2xlLXBhbmVsIC8+XG4gICAgPC9kaXY+XG4gICAgPGRpdiBjbGFzcz1cImJsb2NrXCI+XG4gICAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj55ZWFyIHJhbmdlPC9zcGFuPlxuICAgICAgPGVsLWRhdGUtcGlja2VyIHYtbW9kZWw9XCJ2YWx1ZTNcIiB0eXBlPVwieWVhcnJhbmdlXCIgc2luZ2xlLXBhbmVsIC8+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKClcbmNvbnN0IHZhbHVlMiA9IHJlZigpXG5jb25zdCB2YWx1ZTMgPSByZWYoKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1kYXRlLXBpY2tlciB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIHdpZHRoOiAxMDAlO1xuICBwYWRkaW5nOiAwO1xuICBmbGV4LXdyYXA6IHdyYXA7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyIC5ibG9jayB7XG4gIHBhZGRpbmc6IDEuNXJlbSAwO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGJvcmRlci1yaWdodDogc29saWQgMXB4IHZhcigtLWVsLWJvcmRlci1jb2xvcik7XG4gIGZsZXg6IDE7XG4gIG1pbi13aWR0aDogMzAwcHg7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyIC5ibG9jazpsYXN0LWNoaWxkIHtcbiAgYm9yZGVyLXJpZ2h0OiBub25lO1xufVxuXG4uZGVtby1kYXRlLXBpY2tlciAuYmxvY2sgOmRlZXAoLmVsLWRhdGUtZWRpdG9yKSB7XG4gIHdpZHRoOiAzMDBweDtcbn1cblxuLmRlbW8tZGF0ZS1waWNrZXIgLmRlbW9uc3RyYXRpb24ge1xuICBkaXNwbGF5OiBibG9jaztcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbiAgZm9udC1zaXplOiAxNHB4O1xuICBtYXJnaW4tYm90dG9tOiAxcmVtO1xuICB3aWR0aDogMTAwJTtcbn1cblxuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogMTIwMHB4KSB7XG4gIC5kZW1vLWRhdGUtcGlja2VyIC5ibG9jayB7XG4gICAgZmxleDogMCAwIDUwJTtcbiAgICBib3JkZXItYm90dG9tOiBzb2xpZCAxcHggdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbiAgfVxuXG4gIC5kZW1vLWRhdGUtcGlja2VyIC5ibG9jazpudGgtY2hpbGQoMm4pIHtcbiAgICBib3JkZXItcmlnaHQ6IG5vbmU7XG4gIH1cblxuICAuZGVtby1kYXRlLXBpY2tlciAuYmxvY2s6bnRoLWxhc3QtY2hpbGQoLW4gKyAyKTpudGgtY2hpbGQoMm4gKyAxKSxcbiAgLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrOmxhc3QtY2hpbGQge1xuICAgIGJvcmRlci1ib3R0b206IG5vbmU7XG4gIH1cbn1cblxuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogNzY4cHgpIHtcbiAgLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrIHtcbiAgICBmbGV4OiAwIDAgMTAwJTtcbiAgICBwYWRkaW5nOiAxcmVtIDA7XG4gICAgbWluLXdpZHRoOiBhdXRvO1xuICAgIGJvcmRlci1yaWdodDogbm9uZTtcbiAgICBib3JkZXItYm90dG9tOiBzb2xpZCAxcHggdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbiAgfVxuXG4gIC5kZW1vLWRhdGUtcGlja2VyIC5ibG9jazpsYXN0LWNoaWxkIHtcbiAgICBib3JkZXItYm90dG9tOiBub25lO1xuICB9XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/single-panel.vue)_

vue

```
<template>
  <div class="demo-date-picker">
    <div class="block">
      <span class="demonstration">date range</span>
      <el-date-picker v-model="value1" type="daterange" single-panel />
    </div>
    <div class="block">
      <span class="demonstration">month range</span>
      <el-date-picker v-model="value2" type="monthrange" single-panel />
    </div>
    <div class="block">
      <span class="demonstration">year range</span>
      <el-date-picker v-model="value3" type="yearrange" single-panel />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref()
const value2 = ref()
const value3 = ref()
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
  display: flex;
  flex-direction: column;
  align-items: center;
}

.demo-date-picker .block:last-child {
  border-right: none;
}

.demo-date-picker .block :deep(.el-date-editor) {
  width: 300px;
}

.demo-date-picker .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 1rem;
  width: 100%;
}

@media screen and (max-width: 1200px) {
  .demo-date-picker .block {
    flex: 0 0 50%;
    border-bottom: solid 1px var(--el-border-color);
  }

  .demo-date-picker .block:nth-child(2n) {
    border-right: none;
  }

  .demo-date-picker .block:nth-last-child(-n + 2):nth-child(2n + 1),
  .demo-date-picker .block:last-child {
    border-bottom: none;
  }
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

隐藏源代码

## 默认值 [​](#默认值)

日期选择器会在用户未选择任何日期的时候默认展示当天的日期。 你也可以使用 `default-value` 来修改这个默认的日期。 请注意该值需要是一个可以解析的 `new Date()` 对象。

如果类型是 `daterange`, `default-value` 则会设置左边窗口的默认值。

date

daterange

\-

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+ZGF0ZTwvc3Bhbj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgICAgdHlwZT1cImRhdGVcIlxuICAgICAgICBwbGFjZWhvbGRlcj1cIlBpY2sgYSBkYXRlXCJcbiAgICAgICAgOmRlZmF1bHQtdmFsdWU9XCJuZXcgRGF0ZSgyMDEwLCA5LCAxKVwiXG4gICAgICAvPlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+ZGF0ZXJhbmdlPC9zcGFuPlxuICAgICAgPGVsLWRhdGUtcGlja2VyXG4gICAgICAgIHYtbW9kZWw9XCJ2YWx1ZTJcIlxuICAgICAgICB0eXBlPVwiZGF0ZXJhbmdlXCJcbiAgICAgICAgc3RhcnQtcGxhY2Vob2xkZXI9XCJTdGFydCBEYXRlXCJcbiAgICAgICAgZW5kLXBsYWNlaG9sZGVyPVwiRW5kIERhdGVcIlxuICAgICAgICA6ZGVmYXVsdC12YWx1ZT1cIltuZXcgRGF0ZSgyMDEwLCA5LCAxKSwgbmV3IERhdGUoMjAxMCwgMTAsIDEpXVwiXG4gICAgICAvPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlMSA9IHJlZignJylcbmNvbnN0IHZhbHVlMiA9IHJlZignJylcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tZGF0ZS1waWNrZXIge1xuICBkaXNwbGF5OiBmbGV4O1xuICB3aWR0aDogMTAwJTtcbiAgcGFkZGluZzogMDtcbiAgZmxleC13cmFwOiB3cmFwO1xufVxuXG4uZGVtby1kYXRlLXBpY2tlciAuYmxvY2sge1xuICBwYWRkaW5nOiAxLjVyZW0gMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBib3JkZXItcmlnaHQ6IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICBmbGV4OiAxO1xuICBtaW4td2lkdGg6IDMwMHB4O1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuXG4uZGVtby1kYXRlLXBpY2tlciAuYmxvY2s6bGFzdC1jaGlsZCB7XG4gIGJvcmRlci1yaWdodDogbm9uZTtcbn1cblxuLmRlbW8tZGF0ZS1waWNrZXIgLmRlbW9uc3RyYXRpb24ge1xuICBkaXNwbGF5OiBibG9jaztcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbiAgZm9udC1zaXplOiAxNHB4O1xuICBtYXJnaW4tYm90dG9tOiAxcmVtO1xufVxuXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA3NjhweCkge1xuICAuZGVtby1kYXRlLXBpY2tlciAuYmxvY2sge1xuICAgIGZsZXg6IDAgMCAxMDAlO1xuICAgIHBhZGRpbmc6IDFyZW0gMDtcbiAgICBtaW4td2lkdGg6IGF1dG87XG4gICAgYm9yZGVyLXJpZ2h0OiBub25lO1xuICAgIGJvcmRlci1ib3R0b206IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICB9XG5cbiAgLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrOmxhc3QtY2hpbGQge1xuICAgIGJvcmRlci1ib3R0b206IG5vbmU7XG4gIH1cbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/default-value.vue)_

vue

```
<template>
  <div class="demo-date-picker">
    <div class="block">
      <span class="demonstration">date</span>
      <el-date-picker
        v-model="value1"
        type="date"
        placeholder="Pick a date"
        :default-value="new Date(2010, 9, 1)"
      />
    </div>
    <div class="block">
      <span class="demonstration">daterange</span>
      <el-date-picker
        v-model="value2"
        type="daterange"
        start-placeholder="Start Date"
        end-placeholder="End Date"
        :default-value="[new Date(2010, 9, 1), new Date(2010, 10, 1)]"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref('')
const value2 = ref('')
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

隐藏源代码

## 日期格式 [​](#日期格式)

使用`format`指定输入框的格式。 使用 `value-format` 指定绑定值的格式。

默认情况下，组件接受并返回`Date`对象。

在 [这里](https://day.js.org/docs/en/display/format#list-of-all-available-formats) 查看 Day.js 支持的所有格式。

WARNING

请一定要注意传入参数的大小写是否正确

Emits Date object

Value:

Use value-format

Value：

Timestamp

Value：

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+RW1pdHMgRGF0ZSBvYmplY3Q8L3NwYW4+XG4gICAgICA8ZGl2IGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPlZhbHVlOiB7eyB2YWx1ZTEgfX08L2Rpdj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgICAgdHlwZT1cImRhdGVcIlxuICAgICAgICBwbGFjZWhvbGRlcj1cIlBpY2sgYSBEYXRlXCJcbiAgICAgICAgZm9ybWF0PVwiWVlZWS9NTS9ERFwiXG4gICAgICAvPlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+VXNlIHZhbHVlLWZvcm1hdDwvc3Bhbj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+VmFsdWXvvJp7eyB2YWx1ZTIgfX08L2Rpdj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgICAgdHlwZT1cImRhdGVcIlxuICAgICAgICBwbGFjZWhvbGRlcj1cIlBpY2sgYSBEYXRlXCJcbiAgICAgICAgZm9ybWF0PVwiWVlZWS9NTS9ERFwiXG4gICAgICAgIHZhbHVlLWZvcm1hdD1cIllZWVktTU0tRERcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgIDxzcGFuIGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPlRpbWVzdGFtcDwvc3Bhbj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+VmFsdWXvvJp7eyB2YWx1ZTMgfX08L2Rpdj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICB2LW1vZGVsPVwidmFsdWUzXCJcbiAgICAgICAgdHlwZT1cImRhdGVcIlxuICAgICAgICBwbGFjZWhvbGRlcj1cIlBpY2sgYSBEYXRlXCJcbiAgICAgICAgZm9ybWF0PVwiWVlZWS9NTS9ERFwiXG4gICAgICAgIHZhbHVlLWZvcm1hdD1cInhcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZTEgPSByZWYoJycpXG5jb25zdCB2YWx1ZTIgPSByZWYoJycpXG5jb25zdCB2YWx1ZTMgPSByZWYoJycpXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLWRhdGUtcGlja2VyIHtcbiAgZGlzcGxheTogZmxleDtcbiAgd2lkdGg6IDEwMCU7XG4gIHBhZGRpbmc6IDA7XG4gIGZsZXgtd3JhcDogd3JhcDtcbn1cblxuLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrIHtcbiAgcGFkZGluZzogMS41cmVtIDA7XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbiAgYm9yZGVyLXJpZ2h0OiBzb2xpZCAxcHggdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbiAgZmxleDogMTtcbiAgbWluLXdpZHRoOiAzMDBweDtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cblxuLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrOmxhc3QtY2hpbGQge1xuICBib3JkZXItcmlnaHQ6IG5vbmU7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyIC5kZW1vbnN0cmF0aW9uIHtcbiAgZGlzcGxheTogYmxvY2s7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG4gIGZvbnQtc2l6ZTogMTRweDtcbiAgbWFyZ2luLWJvdHRvbTogMXJlbTtcbiAgd2lkdGg6IDEwMCU7XG59XG5cbkBtZWRpYSBzY3JlZW4gYW5kIChtYXgtd2lkdGg6IDEyMDBweCkge1xuICAuZGVtby1kYXRlLXBpY2tlciAuYmxvY2sge1xuICAgIGZsZXg6IDAgMCA1MCU7XG4gICAgYm9yZGVyLWJvdHRvbTogc29saWQgMXB4IHZhcigtLWVsLWJvcmRlci1jb2xvcik7XG4gIH1cblxuICAuZGVtby1kYXRlLXBpY2tlciAuYmxvY2s6bnRoLWNoaWxkKDJuKSB7XG4gICAgYm9yZGVyLXJpZ2h0OiBub25lO1xuICB9XG5cbiAgLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrOm50aC1sYXN0LWNoaWxkKC1uICsgMik6bnRoLWNoaWxkKDJuICsgMSksXG4gIC5kZW1vLWRhdGUtcGlja2VyIC5ibG9jazpsYXN0LWNoaWxkIHtcbiAgICBib3JkZXItYm90dG9tOiBub25lO1xuICB9XG59XG5cbkBtZWRpYSBzY3JlZW4gYW5kIChtYXgtd2lkdGg6IDc2OHB4KSB7XG4gIC5kZW1vLWRhdGUtcGlja2VyIC5ibG9jayB7XG4gICAgZmxleDogMCAwIDEwMCU7XG4gICAgcGFkZGluZzogMXJlbSAwO1xuICAgIG1pbi13aWR0aDogYXV0bztcbiAgICBib3JkZXItcmlnaHQ6IG5vbmU7XG4gICAgYm9yZGVyLWJvdHRvbTogc29saWQgMXB4IHZhcigtLWVsLWJvcmRlci1jb2xvcik7XG4gIH1cblxuICAuZGVtby1kYXRlLXBpY2tlciAuYmxvY2s6bGFzdC1jaGlsZCB7XG4gICAgYm9yZGVyLWJvdHRvbTogbm9uZTtcbiAgfVxufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/date-formats.vue)_

vue

```
<template>
  <div class="demo-date-picker">
    <div class="block">
      <span class="demonstration">Emits Date object</span>
      <div class="demonstration">Value: {{ value1 }}</div>
      <el-date-picker
        v-model="value1"
        type="date"
        placeholder="Pick a Date"
        format="YYYY/MM/DD"
      />
    </div>
    <div class="block">
      <span class="demonstration">Use value-format</span>
      <div class="demonstration">Value：{{ value2 }}</div>
      <el-date-picker
        v-model="value2"
        type="date"
        placeholder="Pick a Date"
        format="YYYY/MM/DD"
        value-format="YYYY-MM-DD"
      />
    </div>
    <div class="block">
      <span class="demonstration">Timestamp</span>
      <div class="demonstration">Value：{{ value3 }}</div>
      <el-date-picker
        v-model="value3"
        type="date"
        placeholder="Pick a Date"
        format="YYYY/MM/DD"
        value-format="x"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref('')
const value2 = ref('')
const value3 = ref('')
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
  width: 100%;
}

@media screen and (max-width: 1200px) {
  .demo-date-picker .block {
    flex: 0 0 50%;
    border-bottom: solid 1px var(--el-border-color);
  }

  .demo-date-picker .block:nth-child(2n) {
    border-right: none;
  }

  .demo-date-picker .block:nth-last-child(-n + 2):nth-child(2n + 1),
  .demo-date-picker .block:last-child {
    border-bottom: none;
  }
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

隐藏源代码

## 默认显示日期 [​](#默认显示日期)

在选择日期范围时，你可以指定起始日期和结束日期的默认时间。

默认情况下，开始日期和结束日期的时间部分都是选择日期当日的 `00:00:00`。 通过 `default-time` 可以分别指定开始日期和结束日期的具体时刻。 它接受最多两个日期对象的数组。 其中第一项控制起始日期的具体时刻，第二项控制结束日期的具体时刻。

Component value：

\-

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHA+Q29tcG9uZW50IHZhbHVl77yae3sgdmFsdWUgfX08L3A+XG4gICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgICAgdHlwZT1cImRhdGVyYW5nZVwiXG4gICAgICAgIHN0YXJ0LXBsYWNlaG9sZGVyPVwiU3RhcnQgZGF0ZVwiXG4gICAgICAgIGVuZC1wbGFjZWhvbGRlcj1cIkVuZCBkYXRlXCJcbiAgICAgICAgdmFsdWUtZm9ybWF0PVwiWVlZWS1NTS1ERCBISDptbTpzc1wiXG4gICAgICAgIDpkZWZhdWx0LXRpbWU9XCJkZWZhdWx0VGltZVwiXG4gICAgICAvPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCcnKVxuY29uc3QgZGVmYXVsdFRpbWUgPSByZWY8W0RhdGUsIERhdGVdPihbXG4gIG5ldyBEYXRlKDIwMDAsIDEsIDEsIDAsIDAsIDApLFxuICBuZXcgRGF0ZSgyMDAwLCAyLCAxLCAyMywgNTksIDU5KSxcbl0pXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLWRhdGUtcGlja2VyIHtcbiAgZGlzcGxheTogZmxleDtcbiAgd2lkdGg6IDEwMCU7XG4gIHBhZGRpbmc6IDA7XG4gIGZsZXgtd3JhcDogd3JhcDtcbn1cbi5kZW1vLWRhdGUtcGlja2VyIC5ibG9jayB7XG4gIHBhZGRpbmc6IDMwcHggMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBib3JkZXItcmlnaHQ6IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICBmbGV4OiAxO1xufVxuLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrOmxhc3QtY2hpbGQge1xuICBib3JkZXItcmlnaHQ6IG5vbmU7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/default-time.vue)_

vue

```
<template>
  <div class="demo-date-picker">
    <div class="block">
      <p>Component value：{{ value }}</p>
      <el-date-picker
        v-model="value"
        type="daterange"
        start-placeholder="Start date"
        end-placeholder="End date"
        value-format="YYYY-MM-DD HH:mm:ss"
        :default-time="defaultTime"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
const defaultTime = ref<[Date, Date]>([
  new Date(2000, 1, 1, 0, 0, 0),
  new Date(2000, 2, 1, 23, 59, 59),
])
</script>

<style scoped>
.demo-date-picker {
  display: flex;
  width: 100%;
  padding: 0;
  flex-wrap: wrap;
}
.demo-date-picker .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  flex: 1;
}
.demo-date-picker .block:last-child {
  border-right: none;
}
</style>
```

隐藏源代码

## 设置自定义前缀的内容 [​](#设置自定义前缀的内容)

前缀内容可以被自定义。

当你从其他vue组件或由渲染函数生成的组件中导入组件时, 你可以设置 `prefix-icon` 属性来定制前缀内容

set prefix-icon

_

pre

_

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+c2V0IHByZWZpeC1pY29uPC9zcGFuPlxuICAgICAgPGVsLWRhdGUtcGlja2VyXG4gICAgICAgIHYtbW9kZWw9XCJ2YWx1ZTFcIlxuICAgICAgICB0eXBlPVwiZGF0ZVwiXG4gICAgICAgIHBsYWNlaG9sZGVyPVwiUGljayBhIGRheVwiXG4gICAgICAgIDpwcmVmaXgtaWNvbj1cImN1c3RvbVByZWZpeFwiXG4gICAgICAvPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBoLCByZWYsIHNoYWxsb3dSZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlMSA9IHJlZignJylcblxuY29uc3QgY3VzdG9tUHJlZml4ID0gc2hhbGxvd1JlZih7XG4gIHJlbmRlcigpIHtcbiAgICByZXR1cm4gaCgncCcsICdwcmUnKVxuICB9LFxufSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tZGF0ZS1waWNrZXIge1xuICBkaXNwbGF5OiBmbGV4O1xuICB3aWR0aDogMTAwJTtcbiAgcGFkZGluZzogMDtcbiAgZmxleC13cmFwOiB3cmFwO1xufVxuLmRlbW8tZGF0ZS1waWNrZXIgLmJsb2NrIHtcbiAgcGFkZGluZzogMzBweCAwO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGJvcmRlci1yaWdodDogc29saWQgMXB4IHZhcigtLWVsLWJvcmRlci1jb2xvcik7XG4gIGZsZXg6IDE7XG59XG4uZGVtby1kYXRlLXBpY2tlciAuYmxvY2s6bGFzdC1jaGlsZCB7XG4gIGJvcmRlci1yaWdodDogbm9uZTtcbn1cbi5kZW1vLWRhdGUtcGlja2VyIC5kZW1vbnN0cmF0aW9uIHtcbiAgZGlzcGxheTogYmxvY2s7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG4gIGZvbnQtc2l6ZTogMTRweDtcbiAgbWFyZ2luLWJvdHRvbTogMjBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/custom-prefix-icon.vue)_

vue

```
<template>
  <div class="demo-date-picker">
    <div class="block">
      <span class="demonstration">set prefix-icon</span>
      <el-date-picker
        v-model="value1"
        type="date"
        placeholder="Pick a day"
        :prefix-icon="customPrefix"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { h, ref, shallowRef } from 'vue'

const value1 = ref('')

const customPrefix = shallowRef({
  render() {
    return h('p', 'pre')
  },
})
</script>

<style scoped>
.demo-date-picker {
  display: flex;
  width: 100%;
  padding: 0;
  flex-wrap: wrap;
}
.demo-date-picker .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  flex: 1;
}
.demo-date-picker .block:last-child {
  border-right: none;
}
.demo-date-picker .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
```

隐藏源代码

## 自定义内容 [​](#自定义内容)

弹出框的内容是可以自定义的，在插槽内你可以获取到当前单元格的数据 请注意，自定义内容结构应与默认结构一致，否则可能风格会不一致。

value-on-clear

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlclwiPlxuICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgIHR5cGU9XCJkYXRlXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiUGljayBhIGRheVwiXG4gICAgICBmb3JtYXQ9XCJZWVlZL01NL0REXCJcbiAgICAgIHZhbHVlLWZvcm1hdD1cIllZWVktTU0tRERcIlxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD1cImNlbGxcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImNlbGxcIiA6Y2xhc3M9XCJ7IGN1cnJlbnQ6IGNlbGwuaXNDdXJyZW50IH1cIj5cbiAgICAgICAgICA8c3BhbiBjbGFzcz1cInRleHRcIj57eyBjZWxsLnRleHQgfX08L3NwYW4+XG4gICAgICAgICAgPHNwYW4gdi1pZj1cImlzSG9saWRheShjZWxsKVwiIGNsYXNzPVwiaG9saWRheVwiIC8+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWRhdGUtcGlja2VyPlxuICAgIDxlbC1kYXRlLXBpY2tlciB2LW1vZGVsPVwibW9udGhcIiB0eXBlPVwibW9udGhcIiBwbGFjZWhvbGRlcj1cIlBpY2sgYSBtb250aFwiPlxuICAgICAgPHRlbXBsYXRlICNkZWZhdWx0PVwiY2VsbFwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZWwtZGF0ZS10YWJsZS1jZWxsXCIgOmNsYXNzPVwieyBjdXJyZW50OiBjZWxsLmlzQ3VycmVudCB9XCI+XG4gICAgICAgICAgPHNwYW4gY2xhc3M9XCJlbC1kYXRlLXRhYmxlLWNlbGxfX3RleHRcIj57eyBjZWxsLnRleHQgKyAxIH195pyfPC9zcGFuPlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1kYXRlLXBpY2tlcj5cbiAgICA8ZWwtZGF0ZS1waWNrZXIgdi1tb2RlbD1cInllYXJcIiB0eXBlPVwieWVhclwiIHBsYWNlaG9sZGVyPVwiUGljayBhIHllYXJcIj5cbiAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD1cImNlbGxcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImVsLWRhdGUtdGFibGUtY2VsbFwiIDpjbGFzcz1cInsgY3VycmVudDogY2VsbC5pc0N1cnJlbnQgfVwiPlxuICAgICAgICAgIDxzcGFuIGNsYXNzPVwiZWwtZGF0ZS10YWJsZS1jZWxsX190ZXh0XCI+e3sgY2VsbC50ZXh0ICsgMSB9fXk8L3NwYW4+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWRhdGUtcGlja2VyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCcyMDIxLTEwLTI5JylcbmNvbnN0IG1vbnRoID0gcmVmKCcnKVxuY29uc3QgeWVhciA9IHJlZignJylcbmNvbnN0IGhvbGlkYXlzID0gW1xuICAnMjAyMS0xMC0wMScsXG4gICcyMDIxLTEwLTAyJyxcbiAgJzIwMjEtMTAtMDMnLFxuICAnMjAyMS0xMC0wNCcsXG4gICcyMDIxLTEwLTA1JyxcbiAgJzIwMjEtMTAtMDYnLFxuICAnMjAyMS0xMC0wNycsXG5dXG5cbmNvbnN0IGlzSG9saWRheSA9ICh7IGRheWpzIH0pID0+IHtcbiAgcmV0dXJuIGhvbGlkYXlzLmluY2x1ZGVzKGRheWpzLmZvcm1hdCgnWVlZWS1NTS1ERCcpKVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1kYXRlLXBpY2tlciB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtd3JhcDogd3JhcDtcbiAgZ2FwOiAxcmVtO1xufVxuXG4uZGVtby1kYXRlLXBpY2tlciA+ICoge1xuICBtYXJnaW46IDAgIWltcG9ydGFudDtcbn1cblxuLmNlbGwge1xuICBoZWlnaHQ6IDMwcHg7XG4gIHBhZGRpbmc6IDNweCAwO1xuICBib3gtc2l6aW5nOiBib3JkZXItYm94O1xufVxuXG4uY2VsbCAudGV4dCB7XG4gIHdpZHRoOiAyNHB4O1xuICBoZWlnaHQ6IDI0cHg7XG4gIGRpc3BsYXk6IGJsb2NrO1xuICBtYXJnaW46IDAgYXV0bztcbiAgbGluZS1oZWlnaHQ6IDI0cHg7XG4gIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgbGVmdDogNTAlO1xuICB0cmFuc2Zvcm06IHRyYW5zbGF0ZVgoLTUwJSk7XG4gIGJvcmRlci1yYWRpdXM6IDUwJTtcbn1cblxuLmNlbGwuY3VycmVudCAudGV4dCB7XG4gIGJhY2tncm91bmQ6ICM2MjZhZWY7XG4gIGNvbG9yOiAjZmZmO1xufVxuXG4uY2VsbCAuaG9saWRheSB7XG4gIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgd2lkdGg6IDZweDtcbiAgaGVpZ2h0OiA2cHg7XG4gIGJhY2tncm91bmQ6IHZhcigtLWVsLWNvbG9yLWRhbmdlcik7XG4gIGJvcmRlci1yYWRpdXM6IDUwJTtcbiAgYm90dG9tOiAwcHg7XG4gIGxlZnQ6IDUwJTtcbiAgdHJhbnNmb3JtOiB0cmFuc2xhdGVYKC01MCUpO1xufVxuXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA3NjhweCkge1xuICAuZGVtby1kYXRlLXBpY2tlciB7XG4gICAgZ2FwOiAxLjVyZW07XG4gIH1cbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/custom-content.vue)_

vue

```
<template>
  <div class="demo-date-picker">
    <el-date-picker
      v-model="value"
      type="date"
      placeholder="Pick a day"
      format="YYYY/MM/DD"
      value-format="YYYY-MM-DD"
    >
      <template #default="cell">
        <div class="cell" :class="{ current: cell.isCurrent }">
          <span class="text">{{ cell.text }}</span>
          <span v-if="isHoliday(cell)" class="holiday" />
        </div>
      </template>
    </el-date-picker>
    <el-date-picker v-model="month" type="month" placeholder="Pick a month">
      <template #default="cell">
        <div class="el-date-table-cell" :class="{ current: cell.isCurrent }">
          <span class="el-date-table-cell__text">{{ cell.text + 1 }}期</span>
        </div>
      </template>
    </el-date-picker>
    <el-date-picker v-model="year" type="year" placeholder="Pick a year">
      <template #default="cell">
        <div class="el-date-table-cell" :class="{ current: cell.isCurrent }">
          <span class="el-date-table-cell__text">{{ cell.text + 1 }}y</span>
        </div>
      </template>
    </el-date-picker>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('2021-10-29')
const month = ref('')
const year = ref('')
const holidays = [
  '2021-10-01',
  '2021-10-02',
  '2021-10-03',
  '2021-10-04',
  '2021-10-05',
  '2021-10-06',
  '2021-10-07',
]

const isHoliday = ({ dayjs }) => {
  return holidays.includes(dayjs.format('YYYY-MM-DD'))
}
</script>

<style scoped>
.demo-date-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.demo-date-picker > * {
  margin: 0 !important;
}

.cell {
  height: 30px;
  padding: 3px 0;
  box-sizing: border-box;
}

.cell .text {
  width: 24px;
  height: 24px;
  display: block;
  margin: 0 auto;
  line-height: 24px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 50%;
}

.cell.current .text {
  background: #626aef;
  color: #fff;
}

.cell .holiday {
  position: absolute;
  width: 6px;
  height: 6px;
  background: var(--el-color-danger);
  border-radius: 50%;
  bottom: 0px;
  left: 50%;
  transform: translateX(-50%);
}

@media screen and (max-width: 768px) {
  .demo-date-picker {
    gap: 1.5rem;
  }
}
</style>
```

隐藏源代码

## 自定义图标 2.8.0 [​](#自定义图标)

使用插槽自定义图标。

date

date range

\-

month range

\-

year range

To

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1kYXRlLXBpY2tlci1pY29uXCI+XG4gICAgPGRpdiBjbGFzcz1cImNvbnRhaW5lclwiPlxuICAgICAgPGRpdiBjbGFzcz1cImJsb2NrXCI+XG4gICAgICAgIDxkaXYgY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+ZGF0ZTwvZGl2PlxuICAgICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgICAgICB0eXBlPVwiZGF0ZVwiXG4gICAgICAgICAgcGxhY2Vob2xkZXI9XCJQaWNrIGEgZGF5XCJcbiAgICAgICAgICBmb3JtYXQ9XCJZWVlZL01NL0REXCJcbiAgICAgICAgICB2YWx1ZS1mb3JtYXQ9XCJZWVlZLU1NLUREXCJcbiAgICAgICAgPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjcHJldi1tb250aD5cbiAgICAgICAgICAgIDxlbC1pY29uPjxDYXJldExlZnQgLz48L2VsLWljb24+XG4gICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgICA8dGVtcGxhdGUgI25leHQtbW9udGg+XG4gICAgICAgICAgICA8ZWwtaWNvbj48Q2FyZXRSaWdodCAvPjwvZWwtaWNvbj5cbiAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjcHJldi15ZWFyPlxuICAgICAgICAgICAgPGVsLWljb24+XG4gICAgICAgICAgICAgIDxzdmdcbiAgICAgICAgICAgICAgICB2aWV3Qm94PVwiMCAwIDIwIDIwXCJcbiAgICAgICAgICAgICAgICB2ZXJzaW9uPVwiMS4xXCJcbiAgICAgICAgICAgICAgICB4bWxucz1cImh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnXCJcbiAgICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgIDxnIHN0cm9rZS13aWR0aD1cIjFcIiBmaWxsLXJ1bGU9XCJldmVub2RkXCI+XG4gICAgICAgICAgICAgICAgICA8ZyBmaWxsPVwiY3VycmVudENvbG9yXCI+XG4gICAgICAgICAgICAgICAgICAgIDxwYXRoXG4gICAgICAgICAgICAgICAgICAgICAgZD1cIk04LjczMTcxLDE2Ljc5NDkgQzkuMDMyNjQsMTcuMDc5NSA5LjUwNzMzLDE3LjA2NjMgOS43OTE5NiwxNi43NjU0IEMxMC4wNzY2LDE2LjQ2NDQgMTAuMDYzNCwxNS45ODk3IDkuNzYyNDMsMTUuNzA1MSBMNC41MjMzOSwxMC43NSBMMTcuMjQ3MSwxMC43NSBDMTcuNjYxMywxMC43NSAxNy45OTcxLDEwLjQxNDIgMTcuOTk3MSwxMCBDMTcuOTk3MSw5LjU4NTc5IDE3LjY2MTMsOS4yNSAxNy4yNDcxLDkuMjUgTDQuNTIxMTIsOS4yNSBMOS43NjI0Myw0LjI5Mjc1IEMxMC4wNjM0LDQuMDA4MTIgMTAuMDc2NiwzLjUzMzQzIDkuNzkxOTYsMy4yMzI1IEM5LjUwNzMzLDIuOTMxNTYgOS4wMzI2NCwyLjkxODM0IDguNzMxNzEsMy4yMDI5NyBMMi4zMTQ0OSw5LjI3MjQxIEMyLjE0ODE5LDkuNDI5NyAyLjA0ODE5LDkuNjI5ODEgMi4wMTQ0OCw5LjgzODYgQzIuMDAzMDgsOS44OTA1OCAxLjk5NzA3LDkuOTQ0NTkgMS45OTcwNywxMCBDMS45OTcwNywxMC4wNTc2IDIuMDAzNTYsMTAuMTEzNyAyLjAxNTg1LDEwLjE2NzUgQzIuMDUwODQsMTAuMzczMyAyLjE1MDM5LDEwLjU3MDIgMi4zMTQ0OSwxMC43MjU0IEw4LjczMTcxLDE2Ljc5NDkgWlwiXG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgICA8L2c+XG4gICAgICAgICAgICAgICAgPC9nPlxuICAgICAgICAgICAgICA8L3N2Zz5cbiAgICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjbmV4dC15ZWFyPlxuICAgICAgICAgICAgPGVsLWljb24+XG4gICAgICAgICAgICAgIDxzdmdcbiAgICAgICAgICAgICAgICB2aWV3Qm94PVwiMCAwIDIwIDIwXCJcbiAgICAgICAgICAgICAgICB2ZXJzaW9uPVwiMS4xXCJcbiAgICAgICAgICAgICAgICB4bWxucz1cImh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnXCJcbiAgICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgIDxnIHN0cm9rZS13aWR0aD1cIjFcIiBmaWxsLXJ1bGU9XCJldmVub2RkXCI+XG4gICAgICAgICAgICAgICAgICA8ZyBmaWxsPVwiY3VycmVudENvbG9yXCI+XG4gICAgICAgICAgICAgICAgICAgIDxwYXRoXG4gICAgICAgICAgICAgICAgICAgICAgZD1cIk0xMS4yNjU0LDMuMjA1MTEgQzEwLjk2NDQsMi45MjA0OSAxMC40ODk3LDIuOTMzNzEgMTAuMjA1MSwzLjIzNDY0IEM5LjkyMDQ5LDMuNTM1NTggOS45MzM3MSw0LjAxMDI3IDEwLjIzNDYsNC4yOTQ4OSBMMTUuNDczNyw5LjI1IEwyLjc1LDkuMjUgQzIuMzM1NzksOS4yNSAyLDkuNTg1NzkgMiwxMC4wMDAwMDEyIEMyLDEwLjQxNDIgMi4zMzU3OSwxMC43NSAyLjc1LDEwLjc1IEwxNS40NzYsMTAuNzUgTDEwLjIzNDYsMTUuNzA3MyBDOS45MzM3MSwxNS45OTE5IDkuOTIwNDksMTYuNDY2NiAxMC4yMDUxLDE2Ljc2NzUgQzEwLjQ4OTcsMTcuMDY4NCAxMC45NjQ0LDE3LjA4MTcgMTEuMjY1NCwxNi43OTcgTDE3LjY4MjYsMTAuNzI3NiBDMTcuODQ4OSwxMC41NzAzIDE3Ljk0ODksMTAuMzcwMiAxNy45ODI2LDEwLjE2MTQgQzE3Ljk5NCwxMC4xMDk0IDE4LDEwLjA1NTQgMTgsMTAuMDAwMDAxMiBDMTgsOS45NDI0MSAxNy45OTM1LDkuODg2MzMgMTcuOTgxMiw5LjgzMjQ2IEMxNy45NDYyLDkuNjI2NjcgMTcuODQ2Nyw5LjQyOTc2IDE3LjY4MjYsOS4yNzQ1NSBMMTEuMjY1NCwzLjIwNTExIFpcIlxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICAgPC9nPlxuICAgICAgICAgICAgICAgIDwvZz5cbiAgICAgICAgICAgICAgPC9zdmc+XG4gICAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgPC9lbC1kYXRlLXBpY2tlcj5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzcz1cImxpbmVcIiAvPlxuICAgICAgPGRpdiBjbGFzcz1cImJsb2NrXCI+XG4gICAgICAgIDxkaXYgY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+ZGF0ZSByYW5nZTwvZGl2PlxuICAgICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgICAgICB0eXBlPVwiZGF0ZXJhbmdlXCJcbiAgICAgICAgICBzdGFydC1wbGFjZWhvbGRlcj1cIlN0YXJ0IGRhdGVcIlxuICAgICAgICAgIGVuZC1wbGFjZWhvbGRlcj1cIkVuZCBkYXRlXCJcbiAgICAgICAgICBmb3JtYXQ9XCJZWVlZL01NL0REXCJcbiAgICAgICAgICB2YWx1ZS1mb3JtYXQ9XCJZWVlZLU1NLUREXCJcbiAgICAgICAgICB1bmxpbmstcGFuZWxzXG4gICAgICAgID5cbiAgICAgICAgICA8dGVtcGxhdGUgI3ByZXYtbW9udGg+XG4gICAgICAgICAgICA8ZWwtaWNvbj48Q2FyZXRMZWZ0IC8+PC9lbC1pY29uPlxuICAgICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgICAgPHRlbXBsYXRlICNuZXh0LW1vbnRoPlxuICAgICAgICAgICAgPGVsLWljb24+PENhcmV0UmlnaHQgLz48L2VsLWljb24+XG4gICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgICA8dGVtcGxhdGUgI3ByZXYteWVhcj5cbiAgICAgICAgICAgIDxlbC1pY29uPlxuICAgICAgICAgICAgICA8c3ZnXG4gICAgICAgICAgICAgICAgdmlld0JveD1cIjAgMCAyMCAyMFwiXG4gICAgICAgICAgICAgICAgdmVyc2lvbj1cIjEuMVwiXG4gICAgICAgICAgICAgICAgeG1sbnM9XCJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2Z1wiXG4gICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICA8ZyBzdHJva2Utd2lkdGg9XCIxXCIgZmlsbC1ydWxlPVwiZXZlbm9kZFwiPlxuICAgICAgICAgICAgICAgICAgPGcgZmlsbD1cImN1cnJlbnRDb2xvclwiPlxuICAgICAgICAgICAgICAgICAgICA8cGF0aFxuICAgICAgICAgICAgICAgICAgICAgIGQ9XCJNOC43MzE3MSwxNi43OTQ5IEM5LjAzMjY0LDE3LjA3OTUgOS41MDczMywxNy4wNjYzIDkuNzkxOTYsMTYuNzY1NCBDMTAuMDc2NiwxNi40NjQ0IDEwLjA2MzQsMTUuOTg5NyA5Ljc2MjQzLDE1LjcwNTEgTDQuNTIzMzksMTAuNzUgTDE3LjI0NzEsMTAuNzUgQzE3LjY2MTMsMTAuNzUgMTcuOTk3MSwxMC40MTQyIDE3Ljk5NzEsMTAgQzE3Ljk5NzEsOS41ODU3OSAxNy42NjEzLDkuMjUgMTcuMjQ3MSw5LjI1IEw0LjUyMTEyLDkuMjUgTDkuNzYyNDMsNC4yOTI3NSBDMTAuMDYzNCw0LjAwODEyIDEwLjA3NjYsMy41MzM0MyA5Ljc5MTk2LDMuMjMyNSBDOS41MDczMywyLjkzMTU2IDkuMDMyNjQsMi45MTgzNCA4LjczMTcxLDMuMjAyOTcgTDIuMzE0NDksOS4yNzI0MSBDMi4xNDgxOSw5LjQyOTcgMi4wNDgxOSw5LjYyOTgxIDIuMDE0NDgsOS44Mzg2IEMyLjAwMzA4LDkuODkwNTggMS45OTcwNyw5Ljk0NDU5IDEuOTk3MDcsMTAgQzEuOTk3MDcsMTAuMDU3NiAyLjAwMzU2LDEwLjExMzcgMi4wMTU4NSwxMC4xNjc1IEMyLjA1MDg0LDEwLjM3MzMgMi4xNTAzOSwxMC41NzAyIDIuMzE0NDksMTAuNzI1NCBMOC43MzE3MSwxNi43OTQ5IFpcIlxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICAgPC9nPlxuICAgICAgICAgICAgICAgIDwvZz5cbiAgICAgICAgICAgICAgPC9zdmc+XG4gICAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgICA8dGVtcGxhdGUgI25leHQteWVhcj5cbiAgICAgICAgICAgIDxlbC1pY29uPlxuICAgICAgICAgICAgICA8c3ZnXG4gICAgICAgICAgICAgICAgdmlld0JveD1cIjAgMCAyMCAyMFwiXG4gICAgICAgICAgICAgICAgdmVyc2lvbj1cIjEuMVwiXG4gICAgICAgICAgICAgICAgeG1sbnM9XCJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2Z1wiXG4gICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICA8ZyBzdHJva2Utd2lkdGg9XCIxXCIgZmlsbC1ydWxlPVwiZXZlbm9kZFwiPlxuICAgICAgICAgICAgICAgICAgPGcgZmlsbD1cImN1cnJlbnRDb2xvclwiPlxuICAgICAgICAgICAgICAgICAgICA8cGF0aFxuICAgICAgICAgICAgICAgICAgICAgIGQ9XCJNMTEuMjY1NCwzLjIwNTExIEMxMC45NjQ0LDIuOTIwNDkgMTAuNDg5NywyLjkzMzcxIDEwLjIwNTEsMy4yMzQ2NCBDOS45MjA0OSwzLjUzNTU4IDkuOTMzNzEsNC4wMTAyNyAxMC4yMzQ2LDQuMjk0ODkgTDE1LjQ3MzcsOS4yNSBMMi43NSw5LjI1IEMyLjMzNTc5LDkuMjUgMiw5LjU4NTc5IDIsMTAuMDAwMDAxMiBDMiwxMC40MTQyIDIuMzM1NzksMTAuNzUgMi43NSwxMC43NSBMMTUuNDc2LDEwLjc1IEwxMC4yMzQ2LDE1LjcwNzMgQzkuOTMzNzEsMTUuOTkxOSA5LjkyMDQ5LDE2LjQ2NjYgMTAuMjA1MSwxNi43Njc1IEMxMC40ODk3LDE3LjA2ODQgMTAuOTY0NCwxNy4wODE3IDExLjI2NTQsMTYuNzk3IEwxNy42ODI2LDEwLjcyNzYgQzE3Ljg0ODksMTAuNTcwMyAxNy45NDg5LDEwLjM3MDIgMTcuOTgyNiwxMC4xNjE0IEMxNy45OTQsMTAuMTA5NCAxOCwxMC4wNTU0IDE4LDEwLjAwMDAwMTIgQzE4LDkuOTQyNDEgMTcuOTkzNSw5Ljg4NjMzIDE3Ljk4MTIsOS44MzI0NiBDMTcuOTQ2Miw5LjYyNjY3IDE3Ljg0NjcsOS40Mjk3NiAxNy42ODI2LDkuMjc0NTUgTDExLjI2NTQsMy4yMDUxMSBaXCJcbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICAgIDwvZz5cbiAgICAgICAgICAgICAgICA8L2c+XG4gICAgICAgICAgICAgIDwvc3ZnPlxuICAgICAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgIDwvZWwtZGF0ZS1waWNrZXI+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwiY29udGFpbmVyXCI+XG4gICAgICA8ZGl2IGNsYXNzPVwibGluZVwiIC8+XG4gICAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5tb250aCByYW5nZTwvZGl2PlxuICAgICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgICB2LW1vZGVsPVwidmFsdWUzXCJcbiAgICAgICAgICB0eXBlPVwibW9udGhyYW5nZVwiXG4gICAgICAgICAgc3RhcnQtcGxhY2Vob2xkZXI9XCJTdGFydCBkYXRlXCJcbiAgICAgICAgICBlbmQtcGxhY2Vob2xkZXI9XCJFbmQgZGF0ZVwiXG4gICAgICAgICAgZm9ybWF0PVwiWVlZWS9NTS9ERFwiXG4gICAgICAgICAgdmFsdWUtZm9ybWF0PVwiWVlZWS1NTS1ERFwiXG4gICAgICAgICAgdW5saW5rLXBhbmVsc1xuICAgICAgICA+XG4gICAgICAgICAgPHRlbXBsYXRlICNwcmV2LW1vbnRoPlxuICAgICAgICAgICAgPGVsLWljb24+PENhcmV0TGVmdCAvPjwvZWwtaWNvbj5cbiAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjbmV4dC1tb250aD5cbiAgICAgICAgICAgIDxlbC1pY29uPjxDYXJldFJpZ2h0IC8+PC9lbC1pY29uPlxuICAgICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgICAgPHRlbXBsYXRlICNwcmV2LXllYXI+XG4gICAgICAgICAgICA8ZWwtaWNvbj5cbiAgICAgICAgICAgICAgPHN2Z1xuICAgICAgICAgICAgICAgIHZpZXdCb3g9XCIwIDAgMjAgMjBcIlxuICAgICAgICAgICAgICAgIHZlcnNpb249XCIxLjFcIlxuICAgICAgICAgICAgICAgIHhtbG5zPVwiaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmdcIlxuICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgPGcgc3Ryb2tlLXdpZHRoPVwiMVwiIGZpbGwtcnVsZT1cImV2ZW5vZGRcIj5cbiAgICAgICAgICAgICAgICAgIDxnIGZpbGw9XCJjdXJyZW50Q29sb3JcIj5cbiAgICAgICAgICAgICAgICAgICAgPHBhdGhcbiAgICAgICAgICAgICAgICAgICAgICBkPVwiTTguNzMxNzEsMTYuNzk0OSBDOS4wMzI2NCwxNy4wNzk1IDkuNTA3MzMsMTcuMDY2MyA5Ljc5MTk2LDE2Ljc2NTQgQzEwLjA3NjYsMTYuNDY0NCAxMC4wNjM0LDE1Ljk4OTcgOS43NjI0MywxNS43MDUxIEw0LjUyMzM5LDEwLjc1IEwxNy4yNDcxLDEwLjc1IEMxNy42NjEzLDEwLjc1IDE3Ljk5NzEsMTAuNDE0MiAxNy45OTcxLDEwIEMxNy45OTcxLDkuNTg1NzkgMTcuNjYxMyw5LjI1IDE3LjI0NzEsOS4yNSBMNC41MjExMiw5LjI1IEw5Ljc2MjQzLDQuMjkyNzUgQzEwLjA2MzQsNC4wMDgxMiAxMC4wNzY2LDMuNTMzNDMgOS43OTE5NiwzLjIzMjUgQzkuNTA3MzMsMi45MzE1NiA5LjAzMjY0LDIuOTE4MzQgOC43MzE3MSwzLjIwMjk3IEwyLjMxNDQ5LDkuMjcyNDEgQzIuMTQ4MTksOS40Mjk3IDIuMDQ4MTksOS42Mjk4MSAyLjAxNDQ4LDkuODM4NiBDMi4wMDMwOCw5Ljg5MDU4IDEuOTk3MDcsOS45NDQ1OSAxLjk5NzA3LDEwIEMxLjk5NzA3LDEwLjA1NzYgMi4wMDM1NiwxMC4xMTM3IDIuMDE1ODUsMTAuMTY3NSBDMi4wNTA4NCwxMC4zNzMzIDIuMTUwMzksMTAuNTcwMiAyLjMxNDQ5LDEwLjcyNTQgTDguNzMxNzEsMTYuNzk0OSBaXCJcbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICAgIDwvZz5cbiAgICAgICAgICAgICAgICA8L2c+XG4gICAgICAgICAgICAgIDwvc3ZnPlxuICAgICAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgICAgPHRlbXBsYXRlICNuZXh0LXllYXI+XG4gICAgICAgICAgICA8ZWwtaWNvbj5cbiAgICAgICAgICAgICAgPHN2Z1xuICAgICAgICAgICAgICAgIHZpZXdCb3g9XCIwIDAgMjAgMjBcIlxuICAgICAgICAgICAgICAgIHZlcnNpb249XCIxLjFcIlxuICAgICAgICAgICAgICAgIHhtbG5zPVwiaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmdcIlxuICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgPGcgc3Ryb2tlLXdpZHRoPVwiMVwiIGZpbGwtcnVsZT1cImV2ZW5vZGRcIj5cbiAgICAgICAgICAgICAgICAgIDxnIGZpbGw9XCJjdXJyZW50Q29sb3JcIj5cbiAgICAgICAgICAgICAgICAgICAgPHBhdGhcbiAgICAgICAgICAgICAgICAgICAgICBkPVwiTTExLjI2NTQsMy4yMDUxMSBDMTAuOTY0NCwyLjkyMDQ5IDEwLjQ4OTcsMi45MzM3MSAxMC4yMDUxLDMuMjM0NjQgQzkuOTIwNDksMy41MzU1OCA5LjkzMzcxLDQuMDEwMjcgMTAuMjM0Niw0LjI5NDg5IEwxNS40NzM3LDkuMjUgTDIuNzUsOS4yNSBDMi4zMzU3OSw5LjI1IDIsOS41ODU3OSAyLDEwLjAwMDAwMTIgQzIsMTAuNDE0MiAyLjMzNTc5LDEwLjc1IDIuNzUsMTAuNzUgTDE1LjQ3NiwxMC43NSBMMTAuMjM0NiwxNS43MDczIEM5LjkzMzcxLDE1Ljk5MTkgOS45MjA0OSwxNi40NjY2IDEwLjIwNTEsMTYuNzY3NSBDMTAuNDg5NywxNy4wNjg0IDEwLjk2NDQsMTcuMDgxNyAxMS4yNjU0LDE2Ljc5NyBMMTcuNjgyNiwxMC43Mjc2IEMxNy44NDg5LDEwLjU3MDMgMTcuOTQ4OSwxMC4zNzAyIDE3Ljk4MjYsMTAuMTYxNCBDMTcuOTk0LDEwLjEwOTQgMTgsMTAuMDU1NCAxOCwxMC4wMDAwMDEyIEMxOCw5Ljk0MjQxIDE3Ljk5MzUsOS44ODYzMyAxNy45ODEyLDkuODMyNDYgQzE3Ljk0NjIsOS42MjY2NyAxNy44NDY3LDkuNDI5NzYgMTcuNjgyNiw5LjI3NDU1IEwxMS4yNjU0LDMuMjA1MTEgWlwiXG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgICA8L2c+XG4gICAgICAgICAgICAgICAgPC9nPlxuICAgICAgICAgICAgICA8L3N2Zz5cbiAgICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICA8L2VsLWRhdGUtcGlja2VyPlxuICAgICAgPC9kaXY+XG4gICAgICA8ZGl2IGNsYXNzPVwibGluZVwiIC8+XG4gICAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj55ZWFyIHJhbmdlPC9kaXY+XG4gICAgICAgIDxlbC1kYXRlLXBpY2tlclxuICAgICAgICAgIHYtbW9kZWw9XCJ2YWx1ZTRcIlxuICAgICAgICAgIHR5cGU9XCJ5ZWFycmFuZ2VcIlxuICAgICAgICAgIHJhbmdlLXNlcGFyYXRvcj1cIlRvXCJcbiAgICAgICAgICBzdGFydC1wbGFjZWhvbGRlcj1cIlN0YXJ0IFllYXJcIlxuICAgICAgICAgIGVuZC1wbGFjZWhvbGRlcj1cIkVuZCBZZWFyXCJcbiAgICAgICAgPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjcHJldi15ZWFyPlxuICAgICAgICAgICAgPGVsLWljb24+XG4gICAgICAgICAgICAgIDxzdmdcbiAgICAgICAgICAgICAgICB2aWV3Qm94PVwiMCAwIDIwIDIwXCJcbiAgICAgICAgICAgICAgICB2ZXJzaW9uPVwiMS4xXCJcbiAgICAgICAgICAgICAgICB4bWxucz1cImh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnXCJcbiAgICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgIDxnIHN0cm9rZS13aWR0aD1cIjFcIiBmaWxsLXJ1bGU9XCJldmVub2RkXCI+XG4gICAgICAgICAgICAgICAgICA8ZyBmaWxsPVwiY3VycmVudENvbG9yXCI+XG4gICAgICAgICAgICAgICAgICAgIDxwYXRoXG4gICAgICAgICAgICAgICAgICAgICAgZD1cIk04LjczMTcxLDE2Ljc5NDkgQzkuMDMyNjQsMTcuMDc5NSA5LjUwNzMzLDE3LjA2NjMgOS43OTE5NiwxNi43NjU0IEMxMC4wNzY2LDE2LjQ2NDQgMTAuMDYzNCwxNS45ODk3IDkuNzYyNDMsMTUuNzA1MSBMNC41MjMzOSwxMC43NSBMMTcuMjQ3MSwxMC43NSBDMTcuNjYxMywxMC43NSAxNy45OTcxLDEwLjQxNDIgMTcuOTk3MSwxMCBDMTcuOTk3MSw5LjU4NTc5IDE3LjY2MTMsOS4yNSAxNy4yNDcxLDkuMjUgTDQuNTIxMTIsOS4yNSBMOS43NjI0Myw0LjI5Mjc1IEMxMC4wNjM0LDQuMDA4MTIgMTAuMDc2NiwzLjUzMzQzIDkuNzkxOTYsMy4yMzI1IEM5LjUwNzMzLDIuOTMxNTYgOS4wMzI2NCwyLjkxODM0IDguNzMxNzEsMy4yMDI5NyBMMi4zMTQ0OSw5LjI3MjQxIEMyLjE0ODE5LDkuNDI5NyAyLjA0ODE5LDkuNjI5ODEgMi4wMTQ0OCw5LjgzODYgQzIuMDAzMDgsOS44OTA1OCAxLjk5NzA3LDkuOTQ0NTkgMS45OTcwNywxMCBDMS45OTcwNywxMC4wNTc2IDIuMDAzNTYsMTAuMTEzNyAyLjAxNTg1LDEwLjE2NzUgQzIuMDUwODQsMTAuMzczMyAyLjE1MDM5LDEwLjU3MDIgMi4zMTQ0OSwxMC43MjU0IEw4LjczMTcxLDE2Ljc5NDkgWlwiXG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgICA8L2c+XG4gICAgICAgICAgICAgICAgPC9nPlxuICAgICAgICAgICAgICA8L3N2Zz5cbiAgICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjbmV4dC15ZWFyPlxuICAgICAgICAgICAgPGVsLWljb24+XG4gICAgICAgICAgICAgIDxzdmdcbiAgICAgICAgICAgICAgICB2aWV3Qm94PVwiMCAwIDIwIDIwXCJcbiAgICAgICAgICAgICAgICB2ZXJzaW9uPVwiMS4xXCJcbiAgICAgICAgICAgICAgICB4bWxucz1cImh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnXCJcbiAgICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgIDxnIHN0cm9rZS13aWR0aD1cIjFcIiBmaWxsLXJ1bGU9XCJldmVub2RkXCI+XG4gICAgICAgICAgICAgICAgICA8ZyBmaWxsPVwiY3VycmVudENvbG9yXCI+XG4gICAgICAgICAgICAgICAgICAgIDxwYXRoXG4gICAgICAgICAgICAgICAgICAgICAgZD1cIk0xMS4yNjU0LDMuMjA1MTEgQzEwLjk2NDQsMi45MjA0OSAxMC40ODk3LDIuOTMzNzEgMTAuMjA1MSwzLjIzNDY0IEM5LjkyMDQ5LDMuNTM1NTggOS45MzM3MSw0LjAxMDI3IDEwLjIzNDYsNC4yOTQ4OSBMMTUuNDczNyw5LjI1IEwyLjc1LDkuMjUgQzIuMzM1NzksOS4yNSAyLDkuNTg1NzkgMiwxMC4wMDAwMDEyIEMyLDEwLjQxNDIgMi4zMzU3OSwxMC43NSAyLjc1LDEwLjc1IEwxNS40NzYsMTAuNzUgTDEwLjIzNDYsMTUuNzA3MyBDOS45MzM3MSwxNS45OTE5IDkuOTIwNDksMTYuNDY2NiAxMC4yMDUxLDE2Ljc2NzUgQzEwLjQ4OTcsMTcuMDY4NCAxMC45NjQ0LDE3LjA4MTcgMTEuMjY1NCwxNi43OTcgTDE3LjY4MjYsMTAuNzI3NiBDMTcuODQ4OSwxMC41NzAzIDE3Ljk0ODksMTAuMzcwMiAxNy45ODI2LDEwLjE2MTQgQzE3Ljk5NCwxMC4xMDk0IDE4LDEwLjA1NTQgMTgsMTAuMDAwMDAxMiBDMTgsOS45NDI0MSAxNy45OTM1LDkuODg2MzMgMTcuOTgxMiw5LjgzMjQ2IEMxNy45NDYyLDkuNjI2NjcgMTcuODQ2Nyw5LjQyOTc2IDE3LjY4MjYsOS4yNzQ1NSBMMTEuMjY1NCwzLjIwNTExIFpcIlxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICAgPC9nPlxuICAgICAgICAgICAgICAgIDwvZz5cbiAgICAgICAgICAgICAgPC9zdmc+XG4gICAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgPC9lbC1kYXRlLXBpY2tlcj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBDYXJldExlZnQsIENhcmV0UmlnaHQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKCcnKVxuY29uc3QgdmFsdWUyID0gcmVmKCcnKVxuY29uc3QgdmFsdWUzID0gcmVmKCcnKVxuY29uc3QgdmFsdWU0ID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1kYXRlLXBpY2tlci1pY29uIHtcbiAgZGlzcGxheTogZmxleDtcbiAgd2lkdGg6IDEwMCU7XG4gIHBhZGRpbmc6IDA7XG4gIGZsZXgtd3JhcDogd3JhcDtcbiAgZ2FwOiAxcHg7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyLWljb24gLmNvbnRhaW5lciB7XG4gIGZsZXg6IDE7XG4gIG1pbi13aWR0aDogNDAwcHg7XG4gIGJvcmRlci1yaWdodDogc29saWQgMXB4IHZhcigtLWVsLWJvcmRlci1jb2xvcik7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyLWljb24gLmNvbnRhaW5lcjpsYXN0LWNoaWxkIHtcbiAgYm9yZGVyLXJpZ2h0OiBub25lO1xufVxuXG4uZGVtby1kYXRlLXBpY2tlci1pY29uIC5ibG9jayB7XG4gIHBhZGRpbmc6IDEuNXJlbSAwO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyLWljb24gLmJsb2NrOm5vdCg6Zmlyc3QtY2hpbGQpIHtcbiAgYm9yZGVyLXRvcDogc29saWQgMXB4IHZhcigtLWVsLWJvcmRlci1jb2xvcik7XG59XG5cbi5kZW1vLWRhdGUtcGlja2VyLWljb24gLmRlbW9uc3RyYXRpb24ge1xuICBkaXNwbGF5OiBibG9jaztcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbiAgZm9udC1zaXplOiAxNHB4O1xuICBtYXJnaW4tYm90dG9tOiAxcmVtO1xuICB3aWR0aDogMTAwJTtcbn1cblxuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogMTIwMHB4KSB7XG4gIC5kZW1vLWRhdGUtcGlja2VyLWljb24ge1xuICAgIGdhcDogMDtcbiAgfVxuXG4gIC5kZW1vLWRhdGUtcGlja2VyLWljb24gLmNvbnRhaW5lciB7XG4gICAgZmxleDogMCAwIDEwMCU7XG4gICAgbWluLXdpZHRoOiBhdXRvO1xuICAgIGJvcmRlci1yaWdodDogbm9uZTtcbiAgfVxuXG4gIC5kZW1vLWRhdGUtcGlja2VyLWljb24gLmNvbnRhaW5lcjpub3QoOmxhc3QtY2hpbGQpIHtcbiAgICBib3JkZXItYm90dG9tOiBzb2xpZCAxcHggdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbiAgfVxuXG4gIC5kZW1vLWRhdGUtcGlja2VyLWljb24gLmJsb2NrIHtcbiAgICBwYWRkaW5nOiAxcmVtIDA7XG4gIH1cblxuICAuZGVtby1kYXRlLXBpY2tlci1pY29uIC5ibG9jazpub3QoOmZpcnN0LWNoaWxkKSB7XG4gICAgcG9zaXRpb246IHJlbGF0aXZlO1xuICAgIG1hcmdpbi10b3A6IC0xcHg7XG4gIH1cbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker/custom-icon.vue)_

vue

```
<template>
  <div class="demo-date-picker-icon">
    <div class="container">
      <div class="block">
        <div class="demonstration">date</div>
        <el-date-picker
          v-model="value1"
          type="date"
          placeholder="Pick a day"
          format="YYYY/MM/DD"
          value-format="YYYY-MM-DD"
        >
          <template #prev-month>
            <el-icon><CaretLeft /></el-icon>
          </template>
          <template #next-month>
            <el-icon><CaretRight /></el-icon>
          </template>
          <template #prev-year>
            <el-icon>
              <svg
                viewBox="0 0 20 20"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g stroke-width="1" fill-rule="evenodd">
                  <g fill="currentColor">
                    <path
                      d="M8.73171,16.7949 C9.03264,17.0795 9.50733,17.0663 9.79196,16.7654 C10.0766,16.4644 10.0634,15.9897 9.76243,15.7051 L4.52339,10.75 L17.2471,10.75 C17.6613,10.75 17.9971,10.4142 17.9971,10 C17.9971,9.58579 17.6613,9.25 17.2471,9.25 L4.52112,9.25 L9.76243,4.29275 C10.0634,4.00812 10.0766,3.53343 9.79196,3.2325 C9.50733,2.93156 9.03264,2.91834 8.73171,3.20297 L2.31449,9.27241 C2.14819,9.4297 2.04819,9.62981 2.01448,9.8386 C2.00308,9.89058 1.99707,9.94459 1.99707,10 C1.99707,10.0576 2.00356,10.1137 2.01585,10.1675 C2.05084,10.3733 2.15039,10.5702 2.31449,10.7254 L8.73171,16.7949 Z"
                    />
                  </g>
                </g>
              </svg>
            </el-icon>
          </template>
          <template #next-year>
            <el-icon>
              <svg
                viewBox="0 0 20 20"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g stroke-width="1" fill-rule="evenodd">
                  <g fill="currentColor">
                    <path
                      d="M11.2654,3.20511 C10.9644,2.92049 10.4897,2.93371 10.2051,3.23464 C9.92049,3.53558 9.93371,4.01027 10.2346,4.29489 L15.4737,9.25 L2.75,9.25 C2.33579,9.25 2,9.58579 2,10.0000012 C2,10.4142 2.33579,10.75 2.75,10.75 L15.476,10.75 L10.2346,15.7073 C9.93371,15.9919 9.92049,16.4666 10.2051,16.7675 C10.4897,17.0684 10.9644,17.0817 11.2654,16.797 L17.6826,10.7276 C17.8489,10.5703 17.9489,10.3702 17.9826,10.1614 C17.994,10.1094 18,10.0554 18,10.0000012 C18,9.94241 17.9935,9.88633 17.9812,9.83246 C17.9462,9.62667 17.8467,9.42976 17.6826,9.27455 L11.2654,3.20511 Z"
                    />
                  </g>
                </g>
              </svg>
            </el-icon>
          </template>
        </el-date-picker>
      </div>
      <div class="line" />
      <div class="block">
        <div class="demonstration">date range</div>
        <el-date-picker
          v-model="value2"
          type="daterange"
          start-placeholder="Start date"
          end-placeholder="End date"
          format="YYYY/MM/DD"
          value-format="YYYY-MM-DD"
          unlink-panels
        >
          <template #prev-month>
            <el-icon><CaretLeft /></el-icon>
          </template>
          <template #next-month>
            <el-icon><CaretRight /></el-icon>
          </template>
          <template #prev-year>
            <el-icon>
              <svg
                viewBox="0 0 20 20"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g stroke-width="1" fill-rule="evenodd">
                  <g fill="currentColor">
                    <path
                      d="M8.73171,16.7949 C9.03264,17.0795 9.50733,17.0663 9.79196,16.7654 C10.0766,16.4644 10.0634,15.9897 9.76243,15.7051 L4.52339,10.75 L17.2471,10.75 C17.6613,10.75 17.9971,10.4142 17.9971,10 C17.9971,9.58579 17.6613,9.25 17.2471,9.25 L4.52112,9.25 L9.76243,4.29275 C10.0634,4.00812 10.0766,3.53343 9.79196,3.2325 C9.50733,2.93156 9.03264,2.91834 8.73171,3.20297 L2.31449,9.27241 C2.14819,9.4297 2.04819,9.62981 2.01448,9.8386 C2.00308,9.89058 1.99707,9.94459 1.99707,10 C1.99707,10.0576 2.00356,10.1137 2.01585,10.1675 C2.05084,10.3733 2.15039,10.5702 2.31449,10.7254 L8.73171,16.7949 Z"
                    />
                  </g>
                </g>
              </svg>
            </el-icon>
          </template>
          <template #next-year>
            <el-icon>
              <svg
                viewBox="0 0 20 20"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g stroke-width="1" fill-rule="evenodd">
                  <g fill="currentColor">
                    <path
                      d="M11.2654,3.20511 C10.9644,2.92049 10.4897,2.93371 10.2051,3.23464 C9.92049,3.53558 9.93371,4.01027 10.2346,4.29489 L15.4737,9.25 L2.75,9.25 C2.33579,9.25 2,9.58579 2,10.0000012 C2,10.4142 2.33579,10.75 2.75,10.75 L15.476,10.75 L10.2346,15.7073 C9.93371,15.9919 9.92049,16.4666 10.2051,16.7675 C10.4897,17.0684 10.9644,17.0817 11.2654,16.797 L17.6826,10.7276 C17.8489,10.5703 17.9489,10.3702 17.9826,10.1614 C17.994,10.1094 18,10.0554 18,10.0000012 C18,9.94241 17.9935,9.88633 17.9812,9.83246 C17.9462,9.62667 17.8467,9.42976 17.6826,9.27455 L11.2654,3.20511 Z"
                    />
                  </g>
                </g>
              </svg>
            </el-icon>
          </template>
        </el-date-picker>
      </div>
    </div>
    <div class="container">
      <div class="line" />
      <div class="block">
        <div class="demonstration">month range</div>
        <el-date-picker
          v-model="value3"
          type="monthrange"
          start-placeholder="Start date"
          end-placeholder="End date"
          format="YYYY/MM/DD"
          value-format="YYYY-MM-DD"
          unlink-panels
        >
          <template #prev-month>
            <el-icon><CaretLeft /></el-icon>
          </template>
          <template #next-month>
            <el-icon><CaretRight /></el-icon>
          </template>
          <template #prev-year>
            <el-icon>
              <svg
                viewBox="0 0 20 20"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g stroke-width="1" fill-rule="evenodd">
                  <g fill="currentColor">
                    <path
                      d="M8.73171,16.7949 C9.03264,17.0795 9.50733,17.0663 9.79196,16.7654 C10.0766,16.4644 10.0634,15.9897 9.76243,15.7051 L4.52339,10.75 L17.2471,10.75 C17.6613,10.75 17.9971,10.4142 17.9971,10 C17.9971,9.58579 17.6613,9.25 17.2471,9.25 L4.52112,9.25 L9.76243,4.29275 C10.0634,4.00812 10.0766,3.53343 9.79196,3.2325 C9.50733,2.93156 9.03264,2.91834 8.73171,3.20297 L2.31449,9.27241 C2.14819,9.4297 2.04819,9.62981 2.01448,9.8386 C2.00308,9.89058 1.99707,9.94459 1.99707,10 C1.99707,10.0576 2.00356,10.1137 2.01585,10.1675 C2.05084,10.3733 2.15039,10.5702 2.31449,10.7254 L8.73171,16.7949 Z"
                    />
                  </g>
                </g>
              </svg>
            </el-icon>
          </template>
          <template #next-year>
            <el-icon>
              <svg
                viewBox="0 0 20 20"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g stroke-width="1" fill-rule="evenodd">
                  <g fill="currentColor">
                    <path
                      d="M11.2654,3.20511 C10.9644,2.92049 10.4897,2.93371 10.2051,3.23464 C9.92049,3.53558 9.93371,4.01027 10.2346,4.29489 L15.4737,9.25 L2.75,9.25 C2.33579,9.25 2,9.58579 2,10.0000012 C2,10.4142 2.33579,10.75 2.75,10.75 L15.476,10.75 L10.2346,15.7073 C9.93371,15.9919 9.92049,16.4666 10.2051,16.7675 C10.4897,17.0684 10.9644,17.0817 11.2654,16.797 L17.6826,10.7276 C17.8489,10.5703 17.9489,10.3702 17.9826,10.1614 C17.994,10.1094 18,10.0554 18,10.0000012 C18,9.94241 17.9935,9.88633 17.9812,9.83246 C17.9462,9.62667 17.8467,9.42976 17.6826,9.27455 L11.2654,3.20511 Z"
                    />
                  </g>
                </g>
              </svg>
            </el-icon>
          </template>
        </el-date-picker>
      </div>
      <div class="line" />
      <div class="block">
        <div class="demonstration">year range</div>
        <el-date-picker
          v-model="value4"
          type="yearrange"
          range-separator="To"
          start-placeholder="Start Year"
          end-placeholder="End Year"
        >
          <template #prev-year>
            <el-icon>
              <svg
                viewBox="0 0 20 20"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g stroke-width="1" fill-rule="evenodd">
                  <g fill="currentColor">
                    <path
                      d="M8.73171,16.7949 C9.03264,17.0795 9.50733,17.0663 9.79196,16.7654 C10.0766,16.4644 10.0634,15.9897 9.76243,15.7051 L4.52339,10.75 L17.2471,10.75 C17.6613,10.75 17.9971,10.4142 17.9971,10 C17.9971,9.58579 17.6613,9.25 17.2471,9.25 L4.52112,9.25 L9.76243,4.29275 C10.0634,4.00812 10.0766,3.53343 9.79196,3.2325 C9.50733,2.93156 9.03264,2.91834 8.73171,3.20297 L2.31449,9.27241 C2.14819,9.4297 2.04819,9.62981 2.01448,9.8386 C2.00308,9.89058 1.99707,9.94459 1.99707,10 C1.99707,10.0576 2.00356,10.1137 2.01585,10.1675 C2.05084,10.3733 2.15039,10.5702 2.31449,10.7254 L8.73171,16.7949 Z"
                    />
                  </g>
                </g>
              </svg>
            </el-icon>
          </template>
          <template #next-year>
            <el-icon>
              <svg
                viewBox="0 0 20 20"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g stroke-width="1" fill-rule="evenodd">
                  <g fill="currentColor">
                    <path
                      d="M11.2654,3.20511 C10.9644,2.92049 10.4897,2.93371 10.2051,3.23464 C9.92049,3.53558 9.93371,4.01027 10.2346,4.29489 L15.4737,9.25 L2.75,9.25 C2.33579,9.25 2,9.58579 2,10.0000012 C2,10.4142 2.33579,10.75 2.75,10.75 L15.476,10.75 L10.2346,15.7073 C9.93371,15.9919 9.92049,16.4666 10.2051,16.7675 C10.4897,17.0684 10.9644,17.0817 11.2654,16.797 L17.6826,10.7276 C17.8489,10.5703 17.9489,10.3702 17.9826,10.1614 C17.994,10.1094 18,10.0554 18,10.0000012 C18,9.94241 17.9935,9.88633 17.9812,9.83246 C17.9462,9.62667 17.8467,9.42976 17.6826,9.27455 L11.2654,3.20511 Z"
                    />
                  </g>
                </g>
              </svg>
            </el-icon>
          </template>
        </el-date-picker>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CaretLeft, CaretRight } from '@element-plus/icons-vue'

const value1 = ref('')
const value2 = ref('')
const value3 = ref('')
const value4 = ref('')
</script>

<style scoped>
.demo-date-picker-icon {
  display: flex;
  width: 100%;
  padding: 0;
  flex-wrap: wrap;
  gap: 1px;
}

.demo-date-picker-icon .container {
  flex: 1;
  min-width: 400px;
  border-right: solid 1px var(--el-border-color);
  display: flex;
  flex-direction: column;
}

.demo-date-picker-icon .container:last-child {
  border-right: none;
}

.demo-date-picker-icon .block {
  padding: 1.5rem 0;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.demo-date-picker-icon .block:not(:first-child) {
  border-top: solid 1px var(--el-border-color);
}

.demo-date-picker-icon .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 1rem;
  width: 100%;
}

@media screen and (max-width: 1200px) {
  .demo-date-picker-icon {
    gap: 0;
  }

  .demo-date-picker-icon .container {
    flex: 0 0 100%;
    min-width: auto;
    border-right: none;
  }

  .demo-date-picker-icon .container:not(:last-child) {
    border-bottom: solid 1px var(--el-border-color);
  }

  .demo-date-picker-icon .block {
    padding: 1rem 0;
  }

  .demo-date-picker-icon .block:not(:first-child) {
    position: relative;
    margin-top: -1px;
  }
}
</style>
```

隐藏源代码

更详细的数据类型，请查看下表

ts

```
interface DateCell {
  column: number
  customClass: string | undefined
  disabled: boolean
  end: boolean
  inRange: boolean
  row: number
  selected: Dayjs | undefined
  isCurrent: boolean | undefined
  isSelected: boolean
  renderText: string | undefined
  start: boolean
  text: number
  timestamp: number
  date: Date
  dayjs: Dayjs
  type: 'normal' | 'today' | 'week' | 'next-month' | 'prev-month'
}
```

## 国际化 [​](#国际化)

由于 Element Plus 的默认语言为英语，如果你需要设置其它的语言，请参考[国际化](https://element-plus.org/zh-CN/guide/i18n)文档。

要注意的是：日期相关的文字（月份，每一周的第一天等等）也都是通过国际化来配置的。

## API [​](#api)

### 属性 [​](#属性)

| 属性名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| model-value / v-model | 绑定值，如果是 `range` 选择器，数组长度应为 2 | `number` / `string` / `Date` / `array` | '' |
| readonly | 只读 | `boolean` | false |
| disabled | 禁用 | `boolean` | false |
| size | 输入框尺寸 | `enum` | — |
| editable | 文本框可输入 | `boolean` | true |
| clearable | 是否显示清除按钮 | `boolean` | true |
| placeholder | 非范围选择时的占位内容 | `string` | '' |
| start-placeholder | 范围选择时开始日期的占位内容 | `string` | — |
| end-placeholder | 范围选择时结束日期的占位内容 | `string` | — |
| type | 显示类型 | `enum` | date |
| format | 显示在输入框中的格式 | `string` 参考 [日期格式](#date-formats) | YYYY-MM-DD |
| popper-class | DatePicker 下拉框的类名 | `string` | — |
| popper-style | 弹出内容的自定义样式 | `string` / `object` | — |
| popper-options | 自定义 popper 选项，更多请参考 [popper.js](https://popper.js.org/docs/v2/) | `object` | {} |
| range-separator | 选择范围时的分隔符 | `string` | '-' |
| default-value | 可选，选择器打开时默认显示的时间 | `object` | — |
| default-time | 范围选择时选中日期所使用的当日内具体时刻 | `object` | — |
| value-format | 可选，绑定值的格式。 不指定则绑定值为 Date 对象 | `string` 参考 [日期格式](#date-formats) | — |
| id | 等价于原生 input `id` 属性 | `string` / `array` | — |
| name | 等价于原生 input `name` 属性 | `string` / `array` | '' |
| unlink-panels | 在范围选择器里取消两个日期面板之间的联动 | `boolean` | false |
| single-panel 2.14.0 | 在范围选择器中只显示一个面板 | `boolean` | false |
| prefix-icon | 自定义前缀图标 如果 `type`的值是`TimeLikeType`，那么就是 `Clock`，不然就是 `Calendar` | `string` / `object` | '' |
| clear-icon | 自定义清除图标 | `string` / `object` | `CircleClose` |
| validate-event | 是否触发表单验证 | `boolean` | true |
| disabled-date | 一个用来判断该日期是否被禁用的函数，接受一个 Date 对象作为参数。 应该返回一个 Boolean 值。 | `Function` | — |
| shortcuts | 设置快捷选项，需要传入数组对象 | `array` | \[\] |
| cell-class-name | 设置自定义类名 | `Function` | — |
| teleported | 是否将 date-picker 的下拉列表插入至 body 元素 | `boolean` | true |
| empty-values 2.7.0 | 组件的空值配置， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `array` | — |
| value-on-clear 2.7.0 | 清空选项的值， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `string` / `number` / `boolean` / `Function` | — |
| fallback-placements 2.8.4 | Tooltip 可用的 positions 请查看[popper.js 文档](https://popper.js.org/docs/v2/modifiers/flip/#fallbackplacements) | `array` | \['bottom', 'top', 'right', 'left'\] |
| placement 2.8.4 | 下拉框出现的位置 | `Placement` | bottom |
| show-footer 2.10.5 | 是否显示 footer | `boolean` | true |
| show-confirm 2.11.0 | 是否显示确定按钮 | `boolean` | true |
| show-week-number 2.10.3 | 显示周数(除周外) | `boolean` | 你好 |
| automatic-dropdown 2.11.4 | 该属性决定在输入框获得焦点时日期选择面板是否弹出。 （在 3.0 版本中，默认值将设置为 false） | `boolean` | true |

### 事件 [​](#事件)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当用户确认值或点击外部时触发 | `Function` |
| blur | 在组件 Input 失去焦点时触发 | `Function` |
| focus | 在组件 Input 获得焦点时触发 | `Function` |
| clear 2.7.7 | 当点击清除按钮时触发 | `Function` |
| calendar-change | 在日历所选日期更改时触发 仅用于 `range` | `Function` |
| panel-change | 当日期面板改变时触发。 | `Function` |
| visible-change | 当 DatePicker 的下拉列表出现/消失时触发 | `Function` |

### 插槽 [​](#插槽)

| 名称 | 说明 |
| --- | --- |
| default | 自定义单元格内容 |
| range-separator | 自定义范围分割符内容 |
| prev-month 2.8.0 | 上个月的图标 |
| next-month 2.8.0 | 下个月的图标 |
| prev-year 2.8.0 | 上一年图标 |
| next-year 2.8.0 | 下一年图标 |

### 暴露 [​](#暴露)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| focus | 使组件获取焦点 | `Function` |
| blur 2.8.7 | 使组件失去焦点 | `Function` |
| handleOpen 2.2.16 | 打开日期选择器弹窗 | `Function` |
| handleClose 2.2.16 | 关闭日期选择器弹窗 | `Function` |

## 类型声明 [​](#类型声明)

显示类型声明

ts

```
import type { Options as PopperOptions } from '@popperjs/core'

type TimeLikeType = 'datetime' | 'datetimerange'

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

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/date-picker) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/date-picker.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/date-picker.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/24290011?v=4&size=64)](https://github.com/xingyixiang)[![](https://avatars.githubusercontent.com/u/41944818?v=4&size=64)](https://github.com/CherishTheYouth)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/110156942?v=4&size=64)](https://github.com/a92126)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/22286818?v=4&size=64)](https://github.com/fratzinger)[![](https://avatars.githubusercontent.com/u/45327166?v=4&size=64)](https://github.com/jyp114110)[![](https://avatars.githubusercontent.com/u/54931083?v=4&size=64)](https://github.com/wjp980108)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/54665054?v=4&size=64)](https://github.com/lyric-zemin)[![](https://avatars.githubusercontent.com/u/6340506?v=4&size=64)](https://github.com/mdoi2)[![](https://avatars.githubusercontent.com/u/81006731?v=4&size=64)](https://github.com/Panzer-Jack)[![](https://avatars.githubusercontent.com/u/58782768?v=4&size=64)](https://github.com/dddssw)[![](https://avatars.githubusercontent.com/u/84657208?v=4&size=64)](https://github.com/xiaodong2008)[![](https://avatars.githubusercontent.com/u/31533594?v=4&size=64)](https://github.com/Gnalvin)[![](https://avatars.githubusercontent.com/u/57935341?v=4&size=64)](https://github.com/yuchenii)[![](https://avatars.githubusercontent.com/u/42532333?v=4&size=64)](https://github.com/ivan0525)[![](https://avatars.githubusercontent.com/u/1726061?v=4&size=64)](https://github.com/Justineo)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/18509404?v=4&size=64)](https://github.com/inottn)[![](https://avatars.githubusercontent.com/u/79386745?v=4&size=64)](https://github.com/kamesan012)[![](https://avatars.githubusercontent.com/u/55378595?v=4&size=64)](https://github.com/evanryuu)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/35163869?v=4&size=64)](https://github.com/Brain777777)[![](https://avatars.githubusercontent.com/u/30046649?v=4&size=64)](https://github.com/MrWeilian)[![](https://avatars.githubusercontent.com/u/26035718?v=4&size=64)](https://github.com/SnowingFox)[![](https://avatars.githubusercontent.com/u/17247526?v=4&size=64)](https://github.com/nabaonan)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/49087880?v=4&size=64)](https://github.com/pany-ang)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/25458528?v=4&size=64)](https://github.com/weidehai)[![](https://avatars.githubusercontent.com/u/82928935?v=4&size=64)](https://github.com/verger-guo)[![](https://avatars.githubusercontent.com/u/4075314?v=4&size=64)](https://github.com/Giwayume)[![](https://avatars.githubusercontent.com/u/44187480?v=4&size=64)](https://github.com/banbri)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/35101675?v=4&size=64)](https://github.com/shenX-2021)[![](https://avatars.githubusercontent.com/u/19464247?v=4&size=64)](https://github.com/lily-elephant)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)

[Date Picker Panel 日期选择器面板](https://element-plus.org/zh-CN/component/date-picker-panel)

[DateTime Picker 日期时间选择器](https://element-plus.org/zh-CN/component/datetime-picker)


