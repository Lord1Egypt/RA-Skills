---
name: "time-picker"
description: "Time Picker 时间选择器 -- Element Plus Vue3 桌面端组件。Invoke when user needs Time Picker 时间选择器 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/time-picker.html"
---

---

# TimePicker 时间选择器 [​](#timepicker-时间选择器)

更新日志待解决

15

用于选择或输入日期

## 任意时间点 [​](#任意时间点)

可以选择任意时间

提供了两种交互方式：默认情况下通过鼠标滚轮进行选择，打开`arrow-control`属性则通过界面上的箭头进行选择。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZXhhbXBsZS1iYXNpY1wiPlxuICAgIDxlbC10aW1lLXBpY2tlciB2LW1vZGVsPVwidmFsdWUxXCIgcGxhY2Vob2xkZXI9XCJBcmJpdHJhcnkgdGltZVwiIC8+XG4gICAgPGVsLXRpbWUtcGlja2VyXG4gICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgIGFycm93LWNvbnRyb2xcbiAgICAgIHBsYWNlaG9sZGVyPVwiQXJiaXRyYXJ5IHRpbWVcIlxuICAgIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKClcbmNvbnN0IHZhbHVlMiA9IHJlZigpXG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLmV4YW1wbGUtYmFzaWMgLmVsLWRhdGUtZWRpdG9yIHtcbiAgbWFyZ2luOiA4cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/time-picker/basic.vue)_

vue

```
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

隐藏源代码

## 限制时间选择范围 [​](#限制时间选择范围)

您也可以限制时间选择范围。

通过 `disabledHours`，`disabledMinutes` 和 `disabledSeconds` 限制可选时间范围。,

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZXhhbXBsZS1iYXNpY1wiPlxuICAgIDxlbC10aW1lLXBpY2tlclxuICAgICAgdi1tb2RlbD1cInZhbHVlMVwiXG4gICAgICA6ZGlzYWJsZWQtaG91cnM9XCJkaXNhYmxlZEhvdXJzXCJcbiAgICAgIDpkaXNhYmxlZC1taW51dGVzPVwiZGlzYWJsZWRNaW51dGVzXCJcbiAgICAgIDpkaXNhYmxlZC1zZWNvbmRzPVwiZGlzYWJsZWRTZWNvbmRzXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiQXJiaXRyYXJ5IHRpbWVcIlxuICAgIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKG5ldyBEYXRlKDIwMTYsIDksIDEwLCAxOCwgMzApKVxuXG5jb25zdCBtYWtlUmFuZ2UgPSAoc3RhcnQ6IG51bWJlciwgZW5kOiBudW1iZXIpID0+IHtcbiAgY29uc3QgcmVzdWx0OiBudW1iZXJbXSA9IFtdXG4gIGZvciAobGV0IGkgPSBzdGFydDsgaSA8PSBlbmQ7IGkrKykge1xuICAgIHJlc3VsdC5wdXNoKGkpXG4gIH1cbiAgcmV0dXJuIHJlc3VsdFxufVxuY29uc3QgZGlzYWJsZWRIb3VycyA9ICgpID0+IHtcbiAgcmV0dXJuIG1ha2VSYW5nZSgwLCAxNikuY29uY2F0KG1ha2VSYW5nZSgxOSwgMjMpKVxufVxuY29uc3QgZGlzYWJsZWRNaW51dGVzID0gKGhvdXI6IG51bWJlcikgPT4ge1xuICBpZiAoaG91ciA9PT0gMTcpIHtcbiAgICByZXR1cm4gbWFrZVJhbmdlKDAsIDI5KVxuICB9XG4gIGlmIChob3VyID09PSAxOCkge1xuICAgIHJldHVybiBtYWtlUmFuZ2UoMzEsIDU5KVxuICB9XG4gIHJldHVybiBbXVxufVxuY29uc3QgZGlzYWJsZWRTZWNvbmRzID0gKGhvdXI6IG51bWJlciwgbWludXRlOiBudW1iZXIpID0+IHtcbiAgaWYgKGhvdXIgPT09IDE4ICYmIG1pbnV0ZSA9PT0gMzApIHtcbiAgICByZXR1cm4gbWFrZVJhbmdlKDEsIDU5KVxuICB9XG4gIHJldHVybiBbXVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5leGFtcGxlLWJhc2ljIC5lbC1kYXRlLWVkaXRvciB7XG4gIG1hcmdpbjogOHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/time-picker/basic-range.vue)_

vue

```
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

隐藏源代码

## 任意时间范围 [​](#任意时间范围)

可选择任意的时间范围

添加`is-range`属性即可选择时间范围。 同样支持 `arrow-control` 属性。

To

To

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1yYW5nZVwiPlxuICAgIDxlbC10aW1lLXBpY2tlclxuICAgICAgdi1tb2RlbD1cInZhbHVlMVwiXG4gICAgICBpcy1yYW5nZVxuICAgICAgcmFuZ2Utc2VwYXJhdG9yPVwiVG9cIlxuICAgICAgc3RhcnQtcGxhY2Vob2xkZXI9XCJTdGFydCB0aW1lXCJcbiAgICAgIGVuZC1wbGFjZWhvbGRlcj1cIkVuZCB0aW1lXCJcbiAgICAvPlxuICAgIDxlbC10aW1lLXBpY2tlclxuICAgICAgdi1tb2RlbD1cInZhbHVlMlwiXG4gICAgICBpcy1yYW5nZVxuICAgICAgYXJyb3ctY29udHJvbFxuICAgICAgcmFuZ2Utc2VwYXJhdG9yPVwiVG9cIlxuICAgICAgc3RhcnQtcGxhY2Vob2xkZXI9XCJTdGFydCB0aW1lXCJcbiAgICAgIGVuZC1wbGFjZWhvbGRlcj1cIkVuZCB0aW1lXCJcbiAgICAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlMSA9IHJlZjxbRGF0ZSwgRGF0ZV0+KFtcbiAgbmV3IERhdGUoMjAxNiwgOSwgMTAsIDgsIDQwKSxcbiAgbmV3IERhdGUoMjAxNiwgOSwgMTAsIDksIDQwKSxcbl0pXG5jb25zdCB2YWx1ZTIgPSByZWY8W0RhdGUsIERhdGVdPihbXG4gIG5ldyBEYXRlKDIwMTYsIDksIDEwLCA4LCA0MCksXG4gIG5ldyBEYXRlKDIwMTYsIDksIDEwLCA5LCA0MCksXG5dKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5kZW1vLXJhbmdlIC5lbC1kYXRlLWVkaXRvciB7XG4gIG1hcmdpbjogOHB4O1xufVxuXG4uZGVtby1yYW5nZSAuZWwtcmFuZ2Utc2VwYXJhdG9yIHtcbiAgYm94LXNpemluZzogY29udGVudC1ib3g7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/time-picker/range.vue)_

vue

```
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

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| model-value / v-model | 绑定值，如果它是数组，长度应该是 2 | `number` / `string` / `object` | '' |
| readonly | 完全只读 | `boolean` | false |
| disabled | 禁用 | `boolean` | false |
| editable | 文本框可输入 | `boolean` | true |
| clearable | 是否显示清除按钮 | `boolean` | true |
| size | 输入框尺寸 | `enum` | — |
| placeholder | 非范围选择时的占位内容 | `string` | '' |
| start-placeholder | 范围选择时开始日期的占位内容 | `string` | — |
| end-placeholder | 范围选择时结束日期的占位内容 | `string` | — |
| is-range | 是否为时间范围选择 | `boolean` | false |
| arrow-control | 是否使用箭头进行时间选择 | `boolean` | false |
| popper-class | TimePicker 下拉框的类名 | `string` | '' |
| popper-style | 为 TimePicke 的下拉菜单自定义样式 | `string` / `object` | — |
| popper-options | 自定义 popper 选项，更多请参考 [popper.js](https://popper.js.org/docs/v2/) | `object` | {} |
| fallback-placements 2.8.4 | Tooltip 可用的 positions 请查看[popper.js 文档](https://popper.js.org/docs/v2/modifiers/flip/#fallbackplacements) | `array` | \['bottom', 'top', 'right', 'left'\] |
| placement 2.8.4 | 下拉框出现的位置 | `展示位置` | bottom |
| range-separator | 选择范围时的分隔符 | `string` | '-' |
| format | 显示在输入框中的格式 | `string` 参考 [日期格式](https://element-plus.org/zh-CN/component/date-picker#date-formats) | — |
| default-value | 可选，选择器打开时默认显示的时间 | `Date` / `array` | — |
| value-format | 可选，绑定值的格式。 不指定则绑定值为 Date 对象 | `string` 参考 [日期格式](https://element-plus.org/zh-CN/component/date-picker#date-formats) | — |
| id | 等价于原生 input `id` 属性 | `string` / `array` | — |
| name | 等价于原生 input `name` 属性 | `string` | '' |
| aria-label a11y 2.7.2 | 等价于原生 input `aria-label` 属性 | `string` | — |
| prefix-icon | 自定义前缀图标 | `string` / `Component` | Clock |
| clear-icon | 自定义清除图标 | `string` / `Component` | CircleClose |
| disabled-hours | 禁止选择部分小时选项 | `Function` | — |
| disabled-minutes | 禁止选择部分分钟选项 | `Function` | — |
| disabled-seconds | 禁止选择部分秒选项 | `Function` | — |
| teleported | 是否将 popover 的下拉列表镜像至 body 元素 | `boolean` | true |
| tabindex | 输入框的 tabindex | `string` / `number` | 0 |
| empty-values 2.7.0 | 组件的空值配置， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `array` | — |
| value-on-clear 2.7.0 | 清空选项的值， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `string` / `number` / `boolean` / `Function` | — |
| save-on-blur 2.13.4 | 当未选择任何值时，是否在获得焦点时自动填充为当前时间。 | `boolean` | true |
| label a11y deprecated | 等价于原生 input `aria-label` 属性 | `string` | — |

### 事件 [​](#事件)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 用户确认选定的值时触发 | `Function` |
| blur | 在组件 Input 失去焦点时触发 | `Function` |
| focus | 在组件 Input 获得焦点时触发 | `Function` |
| clear 2.7.7 | 可清空的模式下用户点击清空按钮时触发 | `Function` |
| visible-change | 当 TimePicker 的下拉列表出现/消失时触发 | `Function` |

### 暴露 [​](#暴露)

| 名称 | 说明 | Type |
| --- | --- | --- |
| focus | 使组件获取焦点 | `Function` |
| blur | 使组件失去焦点 | `Function` |
| handleOpen 2.2.16 | 打开时间选择器弹窗 | `Function` |
| handleClose 2.2.16 | 关闭时间选择器弹窗 | `Function` |

## Type Declarations [​](#type-declarations)

Show declarations

ts

```
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

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/time-picker) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/time-picker.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/time-picker.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/41944818?v=4&size=64)](https://github.com/CherishTheYouth)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/4075314?v=4&size=64)](https://github.com/Giwayume)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/147961575?v=4&size=64)](https://github.com/IceMooncake)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/24540820?v=4&size=64)](https://github.com/catanswer)[![](https://avatars.githubusercontent.com/u/126545033?v=4&size=64)](https://github.com/dhj-l)[![](https://avatars.githubusercontent.com/u/22286818?v=4&size=64)](https://github.com/fratzinger)[![](https://avatars.githubusercontent.com/u/19428473?v=4&size=64)](https://github.com/sheepzh)[![](https://avatars.githubusercontent.com/u/24290011?v=4&size=64)](https://github.com/xingyixiang)[![](https://avatars.githubusercontent.com/u/22910740?v=4&size=64)](https://github.com/StephenKe)[![](https://avatars.githubusercontent.com/u/35426360?v=4&size=64)](https://github.com/Jungzl)[![](https://avatars.githubusercontent.com/u/78132554?v=4&size=64)](https://github.com/momei-LJM)[![](https://avatars.githubusercontent.com/u/7897937?v=4&size=64)](https://github.com/myronliu347)[![](https://avatars.githubusercontent.com/u/81006731?v=4&size=64)](https://github.com/Panzer-Jack)[![](https://avatars.githubusercontent.com/u/57935341?v=4&size=64)](https://github.com/yuchenii)[![](https://avatars.githubusercontent.com/u/55378595?v=4&size=64)](https://github.com/evanryuu)[![](https://avatars.githubusercontent.com/u/86777555?v=4&size=64)](https://github.com/zhengsixsix)[![](https://avatars.githubusercontent.com/u/22659150?v=4&size=64)](https://github.com/ntnyq)[![](https://avatars.githubusercontent.com/u/24601590?v=4&size=64)](https://github.com/konata33)[![](https://avatars.githubusercontent.com/u/32354856?v=4&size=64)](https://github.com/baiwusanyu-c)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/169252980?v=4&size=64)](https://github.com/xiaochenchen-igg-com)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/49087880?v=4&size=64)](https://github.com/pany-ang)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/28811207?v=4&size=64)](https://github.com/fanhefeng)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/48023419?v=4&size=64)](https://github.com/uncledrewzhaopeng)[![](https://avatars.githubusercontent.com/u/25458528?v=4&size=64)](https://github.com/weidehai)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/19464247?v=4&size=64)](https://github.com/lily-elephant)[![](https://avatars.githubusercontent.com/u/22429236?v=4&size=64)](https://github.com/zongzi531)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)

[Switch 开关](https://element-plus.org/zh-CN/component/switch)

[Time Select 时间选择](https://element-plus.org/zh-CN/component/time-select)


