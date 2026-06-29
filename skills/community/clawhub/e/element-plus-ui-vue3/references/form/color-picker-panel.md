---
name: "color-picker-panel"
description: "ColorPickerPanel 颜色选择器面板 -- Element Plus Vue3 桌面端组件。Invoke when user needs ColorPickerPanel 颜色选择器面板 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/color-picker-panel.html"
---

---

# ColorPickerPanel 颜色选择器面板 beta [​](#colorpickerpanel-颜色选择器面板)

更新日志待解决

0

`ColorPickerPanel`是`ColorPicker`的核心组件。

## 基础用法 [​](#基础用法)

ColorPickerPanel 需要一个字符串类型的变量才能绑定到 v-model。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY29sb3ItcGlja2VyLXBhbmVsIHYtbW9kZWw9XCJjb2xvclwiIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBjb2xvciA9IHJlZignIzQwOUVGRicpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/color-picker-panel/basic.vue)_

vue

```
<template>
  <el-color-picker-panel v-model="color" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color = ref('#409EFF')
</script>
```

隐藏源代码

## 选择透明度 [​](#选择透明度)

ColorPickerPanel 支持Alpha 通道选择。 要激活 Alpha 选择，只需添加 "show-alpha" 属性。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY29sb3ItcGlja2VyLXBhbmVsIHYtbW9kZWw9XCJjb2xvclwiIHNob3ctYWxwaGEgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNvbG9yID0gcmVmKCdyZ2JhKDE5LCAyMDYsIDEwMiwgMC44KScpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/color-picker-panel/alpha.vue)_

vue

```
<template>
  <el-color-picker-panel v-model="color" show-alpha />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color = ref('rgba(19, 206, 102, 0.8)')
</script>
```

隐藏源代码

## 预定义颜色 [​](#预定义颜色)

颜色选择板支持预定义的颜色选项

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY29sb3ItcGlja2VyLXBhbmVsXG4gICAgdi1tb2RlbD1cImNvbG9yXCJcbiAgICBzaG93LWFscGhhXG4gICAgOnByZWRlZmluZT1cInByZWRlZmluZUNvbG9yc1wiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBjb2xvciA9IHJlZigncmdiYSgyNTUsIDY5LCAwLCAwLjY4KScpXG5jb25zdCBwcmVkZWZpbmVDb2xvcnMgPSBbXG4gICcjZmY0NTAwJyxcbiAgJyNmZjhjMDAnLFxuICAnI2ZmZDcwMCcsXG4gICcjOTBlZTkwJyxcbiAgJyMwMGNlZDEnLFxuICAnIzFlOTBmZicsXG4gICcjYzcxNTg1JyxcbiAgJ3JnYmEoMjU1LCA2OSwgMCwgMC42OCknLFxuICAncmdiKDI1NSwgMTIwLCAwKScsXG4gICdoc3YoNTEsIDEwMCwgOTgpJyxcbiAgJ2hzdmEoMTIwLCA0MCwgOTQsIDAuNSknLFxuICAnaHNsKDE4MSwgMTAwJSwgMzclKScsXG4gICdoc2xhKDIwOSwgMTAwJSwgNTYlLCAwLjczKScsXG4gICcjYzcxNTg1NzcnLFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/color-picker-panel/predefined-color.vue)_

vue

```
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

隐藏源代码

## Border 边框 [​](#border-边框)

默认情况下，边框是默认的，如果你不想要边框请参考示例。

No border:

TS

JS

_[](https://element-plus.run/?extra_packages=%40vueuse%2Fcore#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHJlZj1cImNvbnRhaW5lclJlZlwiPlxuICAgIDxkaXYgY2xhc3M9XCJ0ZXh0LWNlbnRlclwiPk5vIGJvcmRlcjo8L2Rpdj5cbiAgICA8ZWwtZGl2aWRlciAvPlxuICAgIDxkaXYgY2xhc3M9XCJmbGV4IGZsZXgtd3JhcCBqdXN0aWZ5LWNlbnRlciBnYXAtNFwiPlxuICAgICAgPGRpdiBjbGFzcz1cInAtNVwiPlxuICAgICAgICA8ZWwtY29sb3ItcGlja2VyLXBhbmVsIHYtbW9kZWw9XCJ2YWx1ZVwiIDpib3JkZXI9XCJmYWxzZVwiIC8+XG4gICAgICA8L2Rpdj5cbiAgICAgIDxlbC1kaXZpZGVyXG4gICAgICAgIGNsYXNzPVwiaC1hdXRvXCJcbiAgICAgICAgOmRpcmVjdGlvbj1cImlzTmFycm93ID8gJ2hvcml6b250YWwnIDogJ3ZlcnRpY2FsJ1wiXG4gICAgICAvPlxuICAgICAgPGVsLWNhcmQ+XG4gICAgICAgIDxlbC1jb2xvci1waWNrZXItcGFuZWwgdi1tb2RlbD1cInZhbHVlXCIgOmJvcmRlcj1cImZhbHNlXCIgLz5cbiAgICAgIDwvZWwtY2FyZD5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgY29tcHV0ZWQsIHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IHVzZUVsZW1lbnRTaXplIH0gZnJvbSAnQHZ1ZXVzZS9jb3JlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZignI2ZmNjkwMCcpXG5jb25zdCBjb250YWluZXJSZWYgPSByZWY8SFRNTEVsZW1lbnQ+KClcblxuY29uc3QgeyB3aWR0aCB9ID0gdXNlRWxlbWVudFNpemUoY29udGFpbmVyUmVmKVxuXG5jb25zdCBpc05hcnJvdyA9IGNvbXB1dGVkKCgpID0+IHdpZHRoLnZhbHVlIDwgODE1KVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/color-picker-panel/border.vue)_

vue

```
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

隐藏源代码

## 禁用 [​](#禁用)

"禁用"属性决定颜色选择器是否完全禁用。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY29sb3ItcGlja2VyLXBhbmVsXG4gICAgdi1tb2RlbD1cImNvbG9yXCJcbiAgICBkaXNhYmxlZFxuICAgIHNob3ctYWxwaGFcbiAgICA6cHJlZGVmaW5lPVwicHJlZGVmaW5lQ29sb3JzXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNvbG9yID0gcmVmKCcjZmY2OTAwJylcbmNvbnN0IHByZWRlZmluZUNvbG9ycyA9IFtcbiAgJyNmZjQ1MDAnLFxuICAnI2ZmOGMwMCcsXG4gICcjZmZkNzAwJyxcbiAgJyM5MGVlOTAnLFxuICAnIzAwY2VkMScsXG4gICcjMWU5MGZmJyxcbiAgJyNjNzE1ODUnLFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/color-picker-panel/disabled.vue)_

vue

```
<template>
  <el-color-picker-panel
    v-model="color"
    disabled
    show-alpha
    :predefine="predefineColors"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const color = ref('#ff6900')
const predefineColors = [
  '#ff4500',
  '#ff8c00',
  '#ffd700',
  '#90ee90',
  '#00ced1',
  '#1e90ff',
  '#c71585',
]
</script>
```

隐藏源代码

## API [​](#api)

### 属性 [​](#属性)

| 方法名 | 详情 | 事件参数 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 绑定值 | `string` | — |
| border | 颜色选择器面板是否有边框 | `boolean` | true |
| disabled | 是否禁用 | `boolean` | false |
| show-alpha | 是否显示 alpha 滑块 | `boolean` | false |
| color-format | 写入 v-model 的颜色的格式 | `enum` | `enum` |
| predefine | 预定义颜色 | `array` | — |
| validate-event 2.11.7 | 是否触发表单验证 | `boolean` | true |
| hue-slider-class 2.13.6 | 类名将会传递给 hue-slider | `object` | ::: |
| hue-slider-style 2.13.6 | 样式将会传递给 hue-slider | `string` / `object` | ::: |

### 插槽 [​](#插槽)

| 方法名 | 详情 |
| --- | --- |
| footer | 输入框之后要附加的内容 |

### 对外暴露的方法 [​](#对外暴露的方法)

| 方法名 | 详情 | 事件参数 |
| --- | --- | --- |
| color | 当前色彩对象 | `object` |
| inputRef | 自定义 input ref | `object` |
| update 2.11.4 | 更新子组件 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/color-picker-panel) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/color-picker-panel.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/color-picker-panel.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/62818957?v=4&size=64)](https://github.com/ZacharyBear)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/1472924?v=4&size=64)](https://github.com/hdwills)

[Checkbox 多选框](https://element-plus.org/zh-CN/component/checkbox)

[Color Picker 颜色选择器](https://element-plus.org/zh-CN/component/color-picker)


