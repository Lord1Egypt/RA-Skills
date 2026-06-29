---
name: "time-select"
description: "Time Select 时间选择 -- Element Plus Vue3 桌面端组件。Invoke when user needs Time Select 时间选择 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/time-select.html"
---

---

# TimeSelect 时间选择 [​](#timeselect-时间选择)

更新日志待解决

3

用于选择或输入日期

可用时间范围是 00:00-23:59

## 固定时间点 [​](#固定时间点)

提供几个固定的时间点供用户选择

使用 `el-time-select` 标签，然后通过`start`、`end`和`step`指定起始时间，结束时间和步长。

Select time

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGltZS1zZWxlY3RcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICBzdGFydD1cIjA4OjMwXCJcbiAgICBzdGVwPVwiMDA6MTVcIlxuICAgIGVuZD1cIjE4OjMwXCJcbiAgICBwbGFjZWhvbGRlcj1cIlNlbGVjdCB0aW1lXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/time-select/basic.vue)_

vue

```
<template>
  <el-time-select
    v-model="value"
    style="width: 240px"
    start="08:30"
    step="00:15"
    end="18:30"
    placeholder="Select time"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
</script>
```

隐藏源代码

## 时间格式 [​](#时间格式)

使用 `format` 属性来控制时间格式 (小时以及分钟)。

在 [这里](https://day.js.org/docs/zh-CN/display/format) 查看 Day.js 支持的 format 参数。

WARNING

请一定要注意传入参数的大小写是否正确

Select time

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGltZS1zZWxlY3RcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICBzdGFydD1cIjAwOjAwXCJcbiAgICBzdGVwPVwiMDA6MzBcIlxuICAgIGVuZD1cIjIzOjU5XCJcbiAgICBwbGFjZWhvbGRlcj1cIlNlbGVjdCB0aW1lXCJcbiAgICBmb3JtYXQ9XCJoaDptbSBBXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/time-select/time-formats.vue)_

vue

```
<template>
  <el-time-select
    v-model="value"
    style="width: 240px"
    start="00:00"
    step="00:30"
    end="23:59"
    placeholder="Select time"
    format="hh:mm A"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
</script>
```

隐藏源代码

## 固定时间范围 [​](#固定时间范围)

如果先选中了开始（或结束）时间，则结束（或开始）时间的状态也将会随之改变。

Start time

End time

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby10aW1lLXJhbmdlIGZsZXggZmxleC13cmFwIGdhcC00XCI+XG4gICAgPGVsLXRpbWUtc2VsZWN0XG4gICAgICB2LW1vZGVsPVwic3RhcnRUaW1lXCJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAgIDptYXgtdGltZT1cImVuZFRpbWVcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJTdGFydCB0aW1lXCJcbiAgICAgIHN0YXJ0PVwiMDg6MzBcIlxuICAgICAgc3RlcD1cIjAwOjE1XCJcbiAgICAgIGVuZD1cIjE4OjMwXCJcbiAgICAvPlxuICAgIDxlbC10aW1lLXNlbGVjdFxuICAgICAgdi1tb2RlbD1cImVuZFRpbWVcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgOm1pbi10aW1lPVwic3RhcnRUaW1lXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiRW5kIHRpbWVcIlxuICAgICAgc3RhcnQ9XCIwODozMFwiXG4gICAgICBzdGVwPVwiMDA6MTVcIlxuICAgICAgZW5kPVwiMTg6MzBcIlxuICAgIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3Qgc3RhcnRUaW1lID0gcmVmKCcnKVxuY29uc3QgZW5kVGltZSA9IHJlZignJylcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/time-select/time-range.vue)_

vue

```
<template>
  <div class="demo-time-range flex flex-wrap gap-4">
    <el-time-select
      v-model="startTime"
      style="width: 240px"
      :max-time="endTime"
      placeholder="Start time"
      start="08:30"
      step="00:15"
      end="18:30"
    />
    <el-time-select
      v-model="endTime"
      style="width: 240px"
      :min-time="startTime"
      placeholder="End time"
      start="08:30"
      step="00:15"
      end="18:30"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const startTime = ref('')
const endTime = ref('')
</script>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `string` | — |
| disabled | 禁用状态 | `boolean` | false |
| editable | 文本框可输入 | `boolean` | true |
| clearable | 是否显示清除按钮 | `boolean` | true |
| include-end-time 2.9.3 | 是否在选项中包含`end` | `boolean` | false |
| size | 输入框尺寸 | `enum` | default |
| placeholder | 非范围选择时的占位内容 | `string` | — |
| name 2.13.3 | 原生属性 | `string` | — |
| effect | Tooltip 主题，内置了 `dark` / `light` 两种主题 | `string` / `enum` | light |
| prefix-icon | 自定义前缀图标 | `string` / `Component` | Clock |
| clear-icon | 自定义清除图标 | `string` / `Component` | CircleClose |
| start | 开始时间 | `string` | 09:00 |
| end | 结束时间 | `string` | 18:00 |
| step | 间隔时间 | `string` | 00:30 |
| min-time | 最早时间点，早于该时间的时间段将被禁用 | `string` | — |
| max-time | 最晚时间点，晚于该时间的时间段将被禁用 | `string` | — |
| format | 设置时间格式 | `string` see [formats](https://day.js.org/docs/en/display/format#list-of-all-available-formats) | HH:mm |
| empty-values 2.7.0 | 组件的空值配置， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `array` | — |
| value-on-clear 2.7.0 | 清空选项的值， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `string` / `number` / `boolean` / `Function` | — |
| popper-class 2.11.4 | 为 TimeSelect 下拉面板设置自定义类名 | `string` | '' |
| popper-style 2.11.4 | 为 TimeSelect 下拉面板设置自定义样式 | `string` / `object` | — |

### Events [​](#events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 用户确认选定的值时触发 | `Function` |
| blur | 在组件 Input 失去焦点时触发 | `Function` |
| focus | 在组件 Input 获得焦点时触发 | `Function` |
| clear 2.7.7 | 可清空的单选模式下用户点击清空按钮时触发 | `Function` |

### Exposes [​](#exposes)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| focus | 使 input 获取焦点 | `Function` |
| blur | 使 input 失去焦点 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/time-select) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/time-select.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/time-select.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/33687038?v=4&size=64)](https://github.com/guozi9999)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/19790546?v=4&size=64)](https://github.com/cleaverlove)[![](https://avatars.githubusercontent.com/u/47178158?v=4&size=64)](https://github.com/Aaron-zon)[![](https://avatars.githubusercontent.com/u/33000154?v=4&size=64)](https://github.com/l-x-f)[![](https://avatars.githubusercontent.com/u/58846658?v=4&size=64)](https://github.com/JiuRanYa)[![](https://avatars.githubusercontent.com/u/102006695?v=4&size=64)](https://github.com/cuongle-hdwebsoft)[![](https://avatars.githubusercontent.com/u/5559812?v=4&size=64)](https://github.com/metanas)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/17247526?v=4&size=64)](https://github.com/nabaonan)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)

[Time Picker 时间选择器](https://element-plus.org/zh-CN/component/time-picker)

[Transfer 穿梭框](https://element-plus.org/zh-CN/component/transfer)


