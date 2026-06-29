---
name: "border"
description: "Border 边框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Border 边框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/border.html"
---

---

# Border 边框 [​](#border-边框)

我们对边框进行统一规范，可用于按钮、卡片、弹窗等组件里。

## 边框样式 [​](#边框样式)

我们提供了以下几种边框样式，以供选择。

<table class="demo-border" data-v-fc2962eb=""><tbody data-v-fc2962eb=""><tr data-v-fc2962eb=""><td class="text" data-v-fc2962eb="">Name</td><td class="text" data-v-fc2962eb="">Thickness</td><td class="line" data-v-fc2962eb="">Demo</td></tr><tr data-v-fc2962eb=""><td class="text" data-v-fc2962eb="">Solid</td><td class="text" data-v-fc2962eb="">1px</td><td class="line" data-v-fc2962eb=""><div data-v-fc2962eb=""></div></td></tr><tr data-v-fc2962eb=""><td class="text" data-v-fc2962eb="">Dashed</td><td class="text" data-v-fc2962eb="">2px</td><td class="line" data-v-fc2962eb=""><div class="dashed" data-v-fc2962eb=""></div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8dGFibGUgY2xhc3M9XCJkZW1vLWJvcmRlclwiPlxuICAgIDx0Ym9keT5cbiAgICAgIDx0cj5cbiAgICAgICAgPHRkIGNsYXNzPVwidGV4dFwiPk5hbWU8L3RkPlxuICAgICAgICA8dGQgY2xhc3M9XCJ0ZXh0XCI+VGhpY2tuZXNzPC90ZD5cbiAgICAgICAgPHRkIGNsYXNzPVwibGluZVwiPkRlbW88L3RkPlxuICAgICAgPC90cj5cbiAgICAgIDx0cj5cbiAgICAgICAgPHRkIGNsYXNzPVwidGV4dFwiPlNvbGlkPC90ZD5cbiAgICAgICAgPHRkIGNsYXNzPVwidGV4dFwiPjFweDwvdGQ+XG4gICAgICAgIDx0ZCBjbGFzcz1cImxpbmVcIj5cbiAgICAgICAgICA8ZGl2IC8+XG4gICAgICAgIDwvdGQ+XG4gICAgICA8L3RyPlxuICAgICAgPHRyPlxuICAgICAgICA8dGQgY2xhc3M9XCJ0ZXh0XCI+RGFzaGVkPC90ZD5cbiAgICAgICAgPHRkIGNsYXNzPVwidGV4dFwiPjJweDwvdGQ+XG4gICAgICAgIDx0ZCBjbGFzcz1cImxpbmVcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzPVwiZGFzaGVkXCIgLz5cbiAgICAgICAgPC90ZD5cbiAgICAgIDwvdHI+XG4gICAgPC90Ym9keT5cbiAgPC90YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1ib3JkZXIgLnRleHQge1xuICB3aWR0aDogMTUlO1xufVxuLmRlbW8tYm9yZGVyIC5saW5lIHtcbiAgd2lkdGg6IDcwJTtcbn1cbi5kZW1vLWJvcmRlciAubGluZSBkaXYge1xuICB3aWR0aDogMTAwJTtcbiAgaGVpZ2h0OiAwO1xuICBib3JkZXItdG9wOiAxcHggc29saWQgdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbn1cbi5kZW1vLWJvcmRlciAubGluZSAuZGFzaGVkIHtcbiAgYm9yZGVyLXRvcDogMnB4IGRhc2hlZCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/border/border.vue)_

vue

```
<template>
  <table class="demo-border">
    <tbody>
      <tr>
        <td class="text">Name</td>
        <td class="text">Thickness</td>
        <td class="line">Demo</td>
      </tr>
      <tr>
        <td class="text">Solid</td>
        <td class="text">1px</td>
        <td class="line">
          <div />
        </td>
      </tr>
      <tr>
        <td class="text">Dashed</td>
        <td class="text">2px</td>
        <td class="line">
          <div class="dashed" />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.demo-border .text {
  width: 15%;
}
.demo-border .line {
  width: 70%;
}
.demo-border .line div {
  width: 100%;
  height: 0;
  border-top: 1px solid var(--el-border-color);
}
.demo-border .line .dashed {
  border-top: 2px dashed var(--el-border-color);
}
</style>
```

隐藏源代码

## 圆角 [​](#圆角)

我们提供了以下几种圆角样式，以供选择。

No Radius

`border-radius: "0px"`

Small Radius

`border-radius: 2px`

Large Radius

`border-radius: 4px`

Round Radius

`border-radius: 20px`

TS

JS

_[](https://element-plus.run/?extra_packages=%40vueuse%2Fcore#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IDpndXR0ZXI9XCIxMlwiIGNsYXNzPVwiZGVtby1yYWRpdXNcIj5cbiAgICA8ZWwtY29sXG4gICAgICB2LWZvcj1cIihyYWRpdXMsIGkpIGluIHJhZGl1c0dyb3VwXCJcbiAgICAgIDprZXk9XCJpXCJcbiAgICAgIDpzcGFuPVwiNlwiXG4gICAgICA6eHM9XCJ7IHNwYW46IDEyIH1cIlxuICAgID5cbiAgICAgIDxkaXYgY2xhc3M9XCJ0aXRsZVwiPnt7IHJhZGl1cy5uYW1lIH19PC9kaXY+XG4gICAgICA8ZGl2IGNsYXNzPVwidmFsdWVcIj5cbiAgICAgICAgPGNvZGU+XG4gICAgICAgICAgYm9yZGVyLXJhZGl1czpcbiAgICAgICAgICB7e1xuICAgICAgICAgICAgcmFkaXVzLnR5cGVcbiAgICAgICAgICAgICAgPyB1c2VDc3NWYXIoYC0tZWwtYm9yZGVyLXJhZGl1cy0ke3JhZGl1cy50eXBlfWApXG4gICAgICAgICAgICAgIDogJ1wiMHB4XCInXG4gICAgICAgICAgfX1cbiAgICAgICAgPC9jb2RlPlxuICAgICAgPC9kaXY+XG4gICAgICA8ZGl2XG4gICAgICAgIGNsYXNzPVwicmFkaXVzXCJcbiAgICAgICAgOnN0eWxlPVwie1xuICAgICAgICAgIGJvcmRlclJhZGl1czogcmFkaXVzLnR5cGVcbiAgICAgICAgICAgID8gYHZhcigtLWVsLWJvcmRlci1yYWRpdXMtJHtyYWRpdXMudHlwZX0pYFxuICAgICAgICAgICAgOiAnJyxcbiAgICAgICAgfVwiXG4gICAgICAvPlxuICAgIDwvZWwtY29sPlxuICA8L2VsLXJvdz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyB1c2VDc3NWYXIgfSBmcm9tICdAdnVldXNlL2NvcmUnXG5cbmNvbnN0IHJhZGl1c0dyb3VwID0gcmVmKFtcbiAge1xuICAgIG5hbWU6ICdObyBSYWRpdXMnLFxuICAgIHR5cGU6ICcnLFxuICB9LFxuICB7XG4gICAgbmFtZTogJ1NtYWxsIFJhZGl1cycsXG4gICAgdHlwZTogJ3NtYWxsJyxcbiAgfSxcbiAge1xuICAgIG5hbWU6ICdMYXJnZSBSYWRpdXMnLFxuICAgIHR5cGU6ICdiYXNlJyxcbiAgfSxcbiAge1xuICAgIG5hbWU6ICdSb3VuZCBSYWRpdXMnLFxuICAgIHR5cGU6ICdyb3VuZCcsXG4gIH0sXG5dKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1yYWRpdXMgLnRpdGxlIHtcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3ItcmVndWxhcik7XG4gIGZvbnQtc2l6ZTogMThweDtcbiAgbWFyZ2luOiAxMHB4IDA7XG59XG4uZGVtby1yYWRpdXMgLnZhbHVlIHtcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3ItcHJpbWFyeSk7XG4gIGZvbnQtc2l6ZTogMTZweDtcbiAgbWFyZ2luOiAxMHB4IDA7XG59XG4uZGVtby1yYWRpdXMgLnJhZGl1cyB7XG4gIGhlaWdodDogNDBweDtcbiAgd2lkdGg6IDcwJTtcbiAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbiAgYm9yZGVyLXJhZGl1czogMDtcbiAgbWFyZ2luLXRvcDogMjBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/border/radius.vue)_

vue

```
<template>
  <el-row :gutter="12" class="demo-radius">
    <el-col
      v-for="(radius, i) in radiusGroup"
      :key="i"
      :span="6"
      :xs="{ span: 12 }"
    >
      <div class="title">{{ radius.name }}</div>
      <div class="value">
        <code>
          border-radius:
          {{
            radius.type
              ? useCssVar(`--el-border-radius-${radius.type}`)
              : '"0px"'
          }}
        </code>
      </div>
      <div
        class="radius"
        :style="{
          borderRadius: radius.type
            ? `var(--el-border-radius-${radius.type})`
            : '',
        }"
      />
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useCssVar } from '@vueuse/core'

const radiusGroup = ref([
  {
    name: 'No Radius',
    type: '',
  },
  {
    name: 'Small Radius',
    type: 'small',
  },
  {
    name: 'Large Radius',
    type: 'base',
  },
  {
    name: 'Round Radius',
    type: 'round',
  },
])
</script>

<style scoped>
.demo-radius .title {
  color: var(--el-text-color-regular);
  font-size: 18px;
  margin: 10px 0;
}
.demo-radius .value {
  color: var(--el-text-color-primary);
  font-size: 16px;
  margin: 10px 0;
}
.demo-radius .radius {
  height: 40px;
  width: 70%;
  border: 1px solid var(--el-border-color);
  border-radius: 0;
  margin-top: 20px;
}
</style>
```

隐藏源代码

## 阴影 [​](#阴影)

我们提供了以下几种投影样式，以供选择。

Basic Shadow`--el-box-shadow`

Light Shadow`--el-box-shadow-light`

Lighter Shadow`--el-box-shadow-lighter`

Dark Shadow`--el-box-shadow-dark`

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBqdXN0aWZ5LWJldHdlZW4gaXRlbXMtY2VudGVyIGZsZXgtd3JhcFwiPlxuICAgIDxkaXZcbiAgICAgIHYtZm9yPVwiKHNoYWRvdywgaSkgaW4gc2hhZG93R3JvdXBcIlxuICAgICAgOmtleT1cImlcIlxuICAgICAgY2xhc3M9XCJmbGV4IGZsZXgtY29sIGp1c3RpZnktY2VudGVyIGl0ZW1zLWNlbnRlclwiXG4gICAgICBtPVwiYXV0b1wiXG4gICAgICB3PVwiNDZcIlxuICAgID5cbiAgICAgIDxkaXZcbiAgICAgICAgY2xhc3M9XCJpbmxpbmUtZmxleFwiXG4gICAgICAgIGg9XCIzMFwiXG4gICAgICAgIHc9XCIzMFwiXG4gICAgICAgIG09XCIyXCJcbiAgICAgICAgOnN0eWxlPVwie1xuICAgICAgICAgIGJveFNoYWRvdzogYHZhcigke2dldENzc1Zhck5hbWUoc2hhZG93LnR5cGUpfSlgLFxuICAgICAgICB9XCJcbiAgICAgIC8+XG4gICAgICA8c3BhbiBwPVwieS00XCIgY2xhc3M9XCJkZW1vLXNoYWRvdy10ZXh0XCIgdGV4dD1cInNtXCI+XG4gICAgICAgIHt7IHNoYWRvdy5uYW1lIH19XG4gICAgICA8L3NwYW4+XG4gICAgICA8Y29kZSB0ZXh0PVwieHNcIj5cbiAgICAgICAge3sgZ2V0Q3NzVmFyTmFtZShzaGFkb3cudHlwZSkgfX1cbiAgICAgIDwvY29kZT5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBzaGFkb3dHcm91cCA9IHJlZihbXG4gIHtcbiAgICBuYW1lOiAnQmFzaWMgU2hhZG93JyxcbiAgICB0eXBlOiAnJyxcbiAgfSxcbiAge1xuICAgIG5hbWU6ICdMaWdodCBTaGFkb3cnLFxuICAgIHR5cGU6ICdsaWdodCcsXG4gIH0sXG4gIHtcbiAgICBuYW1lOiAnTGlnaHRlciBTaGFkb3cnLFxuICAgIHR5cGU6ICdsaWdodGVyJyxcbiAgfSxcbiAge1xuICAgIG5hbWU6ICdEYXJrIFNoYWRvdycsXG4gICAgdHlwZTogJ2RhcmsnLFxuICB9LFxuXSlcblxuY29uc3QgZ2V0Q3NzVmFyTmFtZSA9ICh0eXBlOiBzdHJpbmcpID0+IHtcbiAgcmV0dXJuIGAtLWVsLWJveC1zaGFkb3cke3R5cGUgPyAnLScgOiAnJ30ke3R5cGV9YFxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/border/shadow.vue)_

vue

```
<template>
  <div class="flex justify-between items-center flex-wrap">
    <div
      v-for="(shadow, i) in shadowGroup"
      :key="i"
      class="flex flex-col justify-center items-center"
      m="auto"
      w="46"
    >
      <div
        class="inline-flex"
        h="30"
        w="30"
        m="2"
        :style="{
          boxShadow: `var(${getCssVarName(shadow.type)})`,
        }"
      />
      <span p="y-4" class="demo-shadow-text" text="sm">
        {{ shadow.name }}
      </span>
      <code text="xs">
        {{ getCssVarName(shadow.type) }}
      </code>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const shadowGroup = ref([
  {
    name: 'Basic Shadow',
    type: '',
  },
  {
    name: 'Light Shadow',
    type: 'light',
  },
  {
    name: 'Lighter Shadow',
    type: 'lighter',
  },
  {
    name: 'Dark Shadow',
    type: 'dark',
  },
])

const getCssVarName = (type: string) => {
  return `--el-box-shadow${type ? '-' : ''}${type}`
}
</script>
```

隐藏源代码

## 源代码 [​](#源代码)

[文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/border.md)

[Button 按钮](https://element-plus.org/zh-CN/component/button)

[Color 色彩](https://element-plus.org/zh-CN/component/color)


