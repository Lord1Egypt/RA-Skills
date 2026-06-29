---
name: "color-picker"
description: "Color Picker 颜色选择器 -- Element Plus Vue3 桌面端组件。Invoke when user needs Color Picker 颜色选择器 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/color-picker.html"
---

---

# ColorPicker 颜色选择器 [​](#colorpicker-颜色选择器)

更新日志待解决

4

用于颜色选择，支持多种格式。

## 基础用法 [​](#基础用法)

使用 v-model 与 Vue 实例中的一个变量进行双向绑定，绑定的变量需要是字符串类型。

With default value

With no default value

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1jb2xvci1ibG9ja1wiPlxuICAgIDxzcGFuIGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPldpdGggZGVmYXVsdCB2YWx1ZTwvc3Bhbj5cbiAgICA8ZWwtY29sb3ItcGlja2VyIHYtbW9kZWw9XCJjb2xvcjFcIiAvPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cImRlbW8tY29sb3ItYmxvY2tcIj5cbiAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5XaXRoIG5vIGRlZmF1bHQgdmFsdWU8L3NwYW4+XG4gICAgPGVsLWNvbG9yLXBpY2tlciB2LW1vZGVsPVwiY29sb3IyXCIgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBjb2xvcjEgPSByZWYoJyM0MDlFRkYnKVxuY29uc3QgY29sb3IyID0gcmVmKClcbjwvc2NyaXB0PlxuXG48c3R5bGU+XG4uZGVtby1jb2xvci1ibG9jayB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIG1hcmdpbi1ib3R0b206IDE2cHg7XG59XG4uZGVtby1jb2xvci1ibG9jayAuZGVtb25zdHJhdGlvbiB7XG4gIG1hcmdpbi1yaWdodDogMTZweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/color-picker/basic.vue)_

vue

```
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

隐藏源代码

## 选择透明度 [​](#选择透明度)

ColorPicker 支持普通颜色，也支持带 Alpha 通道的颜色，通过`show-alpha`属性即可控制是否支持透明度的选择。 要启用 Alpha 选择，只需添加 `show-alpha` 属性。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY29sb3ItcGlja2VyIHYtbW9kZWw9XCJjb2xvclwiIHNob3ctYWxwaGEgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNvbG9yID0gcmVmKCdyZ2JhKDE5LCAyMDYsIDEwMiwgMC44KScpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/color-picker/alpha.vue)_

vue

```
<template>
  <el-color-picker v-model="color" show-alpha />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color = ref('rgba(19, 206, 102, 0.8)')
</script>
```

隐藏源代码

## 预定义颜色 [​](#预定义颜色)

ColorPicker 支持预定义颜色

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY29sb3ItcGlja2VyIHYtbW9kZWw9XCJjb2xvclwiIHNob3ctYWxwaGEgOnByZWRlZmluZT1cInByZWRlZmluZUNvbG9yc1wiIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBjb2xvciA9IHJlZigncmdiYSgyNTUsIDY5LCAwLCAwLjY4KScpXG5jb25zdCBwcmVkZWZpbmVDb2xvcnMgPSByZWYoW1xuICAnI2ZmNDUwMCcsXG4gICcjZmY4YzAwJyxcbiAgJyNmZmQ3MDAnLFxuICAnIzkwZWU5MCcsXG4gICcjMDBjZWQxJyxcbiAgJyMxZTkwZmYnLFxuICAnI2M3MTU4NScsXG4gICdyZ2JhKDI1NSwgNjksIDAsIDAuNjgpJyxcbiAgJ3JnYigyNTUsIDEyMCwgMCknLFxuICAnaHN2KDUxLCAxMDAsIDk4KScsXG4gICdoc3ZhKDEyMCwgNDAsIDk0LCAwLjUpJyxcbiAgJ2hzbCgxODEsIDEwMCUsIDM3JSknLFxuICAnaHNsYSgyMDksIDEwMCUsIDU2JSwgMC43MyknLFxuICAnI2M3MTU4NTc3Jyxcbl0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/color-picker/predefined-color.vue)_

vue

```
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

隐藏源代码

## 不同尺寸 [​](#不同尺寸)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1jb2xvci1zaXplc1wiPlxuICAgIDxlbC1jb2xvci1waWNrZXIgdi1tb2RlbD1cImNvbG9yXCIgc2l6ZT1cImxhcmdlXCIgLz5cbiAgICA8ZWwtY29sb3ItcGlja2VyIHYtbW9kZWw9XCJjb2xvclwiIC8+XG4gICAgPGVsLWNvbG9yLXBpY2tlciB2LW1vZGVsPVwiY29sb3JcIiBzaXplPVwic21hbGxcIiAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNvbG9yID0gcmVmKCcjNDA5RUZGJylcbjwvc2NyaXB0PlxuXG48c3R5bGU+XG4uZGVtby1jb2xvci1zaXplcyAuZWwtY29sb3ItcGlja2VyOm5vdCg6bGFzdC1jaGlsZCkge1xuICBtYXJnaW4tcmlnaHQ6IDE2cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/color-picker/sizes.vue)_

vue

```
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

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `string` | — |
| disabled | 是否禁用 | `boolean` | false |
| clearable 2.13.1 | 文本框可输入 | `boolean` | true |
| size | 尺寸 | `enum` | — |
| show-alpha | 是否支持透明度选择 | `boolean` | false |
| color-format | 写入 v-model 的颜色的格式 | `enum` | `enum` |
| popper-class | ColorPicker 下拉框的类名 | `string` / `object` | '' |
| popper-style 2.11.4 | ColorPicker 下拉面板的自定义样式 | `string` / `object` | — |
| predefine | 预定义颜色 | `array` | — |
| validate-event | 输入时是否触发表单的校验 | `boolean` | true |
| tabindex | ColorPicker 的 tabindex | `string` / `number` | 0 |
| aria-label a11y 2.7.2 | ColorPicker 的 aria-label | `string` | — |
| empty-values 2.10.3 | 组件的空值配置， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `array` | — |
| value-on-clear 2.10.3 | 清空选项的值， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `string` / `number` / `boolean` / `Function` | — |
| id | ColorPicker 的 id | `string` | — |
| teleported 2.7.2 | 是否将 popover 的下拉列表渲染至 body 下 | `boolean` | true |
| label a11y deprecated | ColorPicker 的 aria-label | `string` | — |
| persistent 2.10.5 | 当颜色选择器未激活且 persistent 为 false 时，颜色面板将被销毁。 | `boolean` | true |
| append-to 2.10.5 | 挂载到哪个 DOM 元素 | `CSSSelector` / `HTMLElement` | \- |

### Events [​](#events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当绑定值变化时触发 | `Function` |
| active-change | 面板中当前显示的颜色发生改变时触发 | `Function` |
| focus 2.4.0 | 当获得焦点时触发 | `Function` |
| blur 2.4.0 | 当失去焦点时触发 | `Function` |
| clear 2.13.1 | 当点击清除按钮时触发 | `Function` |

### Exposes [​](#exposes)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| color | 当前色彩对象 | `object` |
| show 2.3.3 | 手动显示颜色选择器 | `Function` |
| hide 2.3.3 | 手动隐藏颜色选择器 | `Function` |
| focus 2.3.13 | 使 picker 获得焦点 | `Function` |
| blur 2.3.13 | 使 picker 失去焦点 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/color-picker) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/color-picker.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/color-picker.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/83899365?v=4&size=64)](https://github.com/chensuifengran)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/31885971?v=4&size=64)](https://github.com/wonderl17)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/111559907?v=4&size=64)](https://github.com/JCL206312)[![](https://avatars.githubusercontent.com/u/26516275?v=4&size=64)](https://github.com/zhanghaifeng213)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/78132554?v=4&size=64)](https://github.com/momei-LJM)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/47178158?v=4&size=64)](https://github.com/Aaron-zon)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/3360879?v=4&size=64)](https://github.com/xiterjia)[![](https://avatars.githubusercontent.com/u/25458528?v=4&size=64)](https://github.com/weidehai)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/17247526?v=4&size=64)](https://github.com/nabaonan)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)

[ColorPickerPanel 颜色选择器面板](https://element-plus.org/zh-CN/component/color-picker-panel)

[Date Picker Panel 日期选择器面板](https://element-plus.org/zh-CN/component/date-picker-panel)


