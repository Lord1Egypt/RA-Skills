---
name: "transitions"
description: "内置过渡动画 -- Element Plus Vue3 桌面端组件。Invoke when user needs 内置过渡动画 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/guide/transitions.html"
---

---

# 内置过渡动画 [​](#内置过渡动画)

Element Plus 内应用在部分组件的过渡动画，你也可以直接使用。 在使用之前，请阅读 [官方的过渡组件文档](https://vuejs.org/guide/built-ins/transition.html)。

## Fade 淡入淡出 [​](#fade-淡入淡出)

提供 `el-fade-in-linear` 和 `el-fade-in` 两种效果。

Click Me

.el-fade-in-linear

.el-fade-in

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1idXR0b24gQGNsaWNrPVwic2hvdyA9ICFzaG93XCI+Q2xpY2sgTWU8L2VsLWJ1dHRvbj5cblxuICAgIDxkaXYgY2xhc3M9XCJmYWRlLWNvbnRhaW5lclwiPlxuICAgICAgPHRyYW5zaXRpb24gbmFtZT1cImVsLWZhZGUtaW4tbGluZWFyXCI+XG4gICAgICAgIDxkaXYgdi1zaG93PVwic2hvd1wiIGNsYXNzPVwidHJhbnNpdGlvbi1ib3hcIj4uZWwtZmFkZS1pbi1saW5lYXI8L2Rpdj5cbiAgICAgIDwvdHJhbnNpdGlvbj5cbiAgICAgIDx0cmFuc2l0aW9uIG5hbWU9XCJlbC1mYWRlLWluXCI+XG4gICAgICAgIDxkaXYgdi1zaG93PVwic2hvd1wiIGNsYXNzPVwidHJhbnNpdGlvbi1ib3hcIj4uZWwtZmFkZS1pbjwvZGl2PlxuICAgICAgPC90cmFuc2l0aW9uPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHNob3cgPSByZWYodHJ1ZSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmZhZGUtY29udGFpbmVyIHtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC13cmFwOiB3cmFwO1xuICBnYXA6IDE2cHg7XG4gIG1pbi1oZWlnaHQ6IDEwMHB4O1xuICBtYXJnaW4tdG9wOiAyMHB4O1xufVxuXG4udHJhbnNpdGlvbi1ib3gge1xuICB3aWR0aDogMjAwcHg7XG4gIGhlaWdodDogMTAwcHg7XG4gIGJvcmRlci1yYWRpdXM6IHZhcigtLWVsLWJvcmRlci1yYWRpdXMtYmFzZSk7XG4gIGJhY2tncm91bmQtY29sb3I6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGNvbG9yOiAjZmZmO1xuICBwYWRkaW5nOiA0MHB4IDIwcHg7XG4gIGJveC1zaXppbmc6IGJvcmRlci1ib3g7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/transitions/fade.vue)_

vue

```
<template>
  <div>
    <el-button @click="show = !show">Click Me</el-button>

    <div class="fade-container">
      <transition name="el-fade-in-linear">
        <div v-show="show" class="transition-box">.el-fade-in-linear</div>
      </transition>
      <transition name="el-fade-in">
        <div v-show="show" class="transition-box">.el-fade-in</div>
      </transition>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const show = ref(true)
</script>

<style scoped>
.fade-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  min-height: 100px;
  margin-top: 20px;
}

.transition-box {
  width: 200px;
  height: 100px;
  border-radius: var(--el-border-radius-base);
  background-color: var(--el-color-primary);
  text-align: center;
  color: #fff;
  padding: 40px 20px;
  box-sizing: border-box;
}
</style>
```

隐藏源代码

## Zoom 缩放 [​](#zoom-缩放)

`el-zoom-in-left`, `el-zoom-in-center`, `el-zoom-in-top` and `el-zoom-in-bottom` are provided.

Click Me

.el-zoom-in-left

.el-zoom-in-center

.el-zoom-in-top

.el-zoom-in-bottom

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1idXR0b24gQGNsaWNrPVwic2hvdyA9ICFzaG93XCI+Q2xpY2sgTWU8L2VsLWJ1dHRvbj5cblxuICAgIDxkaXYgY2xhc3M9XCJ0cmFuc2l0aW9uLWNvbnRhaW5lclwiPlxuICAgICAgPHRyYW5zaXRpb24gbmFtZT1cImVsLXpvb20taW4tbGVmdFwiPlxuICAgICAgICA8ZGl2IHYtc2hvdz1cInNob3dcIiBjbGFzcz1cInRyYW5zaXRpb24tYm94XCI+LmVsLXpvb20taW4tbGVmdDwvZGl2PlxuICAgICAgPC90cmFuc2l0aW9uPlxuXG4gICAgICA8dHJhbnNpdGlvbiBuYW1lPVwiZWwtem9vbS1pbi1jZW50ZXJcIj5cbiAgICAgICAgPGRpdiB2LXNob3c9XCJzaG93XCIgY2xhc3M9XCJ0cmFuc2l0aW9uLWJveFwiPi5lbC16b29tLWluLWNlbnRlcjwvZGl2PlxuICAgICAgPC90cmFuc2l0aW9uPlxuXG4gICAgICA8dHJhbnNpdGlvbiBuYW1lPVwiZWwtem9vbS1pbi10b3BcIj5cbiAgICAgICAgPGRpdiB2LXNob3c9XCJzaG93XCIgY2xhc3M9XCJ0cmFuc2l0aW9uLWJveFwiPi5lbC16b29tLWluLXRvcDwvZGl2PlxuICAgICAgPC90cmFuc2l0aW9uPlxuXG4gICAgICA8dHJhbnNpdGlvbiBuYW1lPVwiZWwtem9vbS1pbi1ib3R0b21cIj5cbiAgICAgICAgPGRpdiB2LXNob3c9XCJzaG93XCIgY2xhc3M9XCJ0cmFuc2l0aW9uLWJveFwiPi5lbC16b29tLWluLWJvdHRvbTwvZGl2PlxuICAgICAgPC90cmFuc2l0aW9uPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHNob3cgPSByZWYodHJ1ZSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLnRyYW5zaXRpb24tY29udGFpbmVyIHtcbiAgZGlzcGxheTogZmxleDtcbiAgbWFyZ2luLXRvcDogMjBweDtcbiAgbWluLWhlaWdodDogMTAwcHg7XG4gIGZsZXgtd3JhcDogd3JhcDtcbiAgZ2FwOiAxNnB4O1xufVxuXG4udHJhbnNpdGlvbi1ib3gge1xuICB3aWR0aDogMjAwcHg7XG4gIGhlaWdodDogMTAwcHg7XG4gIGJvcmRlci1yYWRpdXM6IHZhcigtLWVsLWJvcmRlci1yYWRpdXMtYmFzZSk7XG4gIGJhY2tncm91bmQtY29sb3I6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGNvbG9yOiAjZmZmO1xuICBwYWRkaW5nOiAyMHB4O1xuICBib3gtc2l6aW5nOiBib3JkZXItYm94O1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgd29yZC1icmVhazogYnJlYWstd29yZDtcbiAgZm9udC1zaXplOiAxNHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/transitions/zoom.vue)_

vue

```
<template>
  <div>
    <el-button @click="show = !show">Click Me</el-button>

    <div class="transition-container">
      <transition name="el-zoom-in-left">
        <div v-show="show" class="transition-box">.el-zoom-in-left</div>
      </transition>

      <transition name="el-zoom-in-center">
        <div v-show="show" class="transition-box">.el-zoom-in-center</div>
      </transition>

      <transition name="el-zoom-in-top">
        <div v-show="show" class="transition-box">.el-zoom-in-top</div>
      </transition>

      <transition name="el-zoom-in-bottom">
        <div v-show="show" class="transition-box">.el-zoom-in-bottom</div>
      </transition>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const show = ref(true)
</script>

<style scoped>
.transition-container {
  display: flex;
  margin-top: 20px;
  min-height: 100px;
  flex-wrap: wrap;
  gap: 16px;
}

.transition-box {
  width: 200px;
  height: 100px;
  border-radius: var(--el-border-radius-base);
  background-color: var(--el-color-primary);
  text-align: center;
  color: #fff;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  word-break: break-word;
  font-size: 14px;
}
</style>
```

隐藏源代码

## Collapse 折叠面板 [​](#collapse-折叠面板)

使用 `el-collapse-transition` 组件实现折叠展开效果。

Click Me

el-collapse-transition

el-collapse-transition

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1idXR0b24gQGNsaWNrPVwic2hvdyA9ICFzaG93XCI+Q2xpY2sgTWU8L2VsLWJ1dHRvbj5cblxuICAgIDxkaXYgc3R5bGU9XCJtYXJnaW4tdG9wOiAyMHB4OyBoZWlnaHQ6IDIxMHB4XCI+XG4gICAgICA8ZWwtY29sbGFwc2UtdHJhbnNpdGlvbj5cbiAgICAgICAgPGRpdiB2LXNob3c9XCJzaG93XCI+XG4gICAgICAgICAgPGRpdiBjbGFzcz1cInRyYW5zaXRpb24tYm94XCI+ZWwtY29sbGFwc2UtdHJhbnNpdGlvbjwvZGl2PlxuICAgICAgICAgIDxkaXYgY2xhc3M9XCJ0cmFuc2l0aW9uLWJveCBtdC1bMTBweF1cIj5lbC1jb2xsYXBzZS10cmFuc2l0aW9uPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jb2xsYXBzZS10cmFuc2l0aW9uPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHNob3cgPSByZWYodHJ1ZSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLnRyYW5zaXRpb24tYm94IHtcbiAgd2lkdGg6IDIwMHB4O1xuICBoZWlnaHQ6IDEwMHB4O1xuICBib3JkZXItcmFkaXVzOiB2YXIoLS1lbC1ib3JkZXItcmFkaXVzLWJhc2UpO1xuICBiYWNrZ3JvdW5kLWNvbG9yOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBjb2xvcjogI2ZmZjtcbiAgcGFkZGluZzogNDBweCAyMHB4O1xuICBib3gtc2l6aW5nOiBib3JkZXItYm94O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/transitions/collapse.vue)_

vue

```
<template>
  <div>
    <el-button @click="show = !show">Click Me</el-button>

    <div style="margin-top: 20px; height: 210px">
      <el-collapse-transition>
        <div v-show="show">
          <div class="transition-box">el-collapse-transition</div>
          <div class="transition-box mt-[10px]">el-collapse-transition</div>
        </div>
      </el-collapse-transition>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const show = ref(true)
</script>

<style scoped>
.transition-box {
  width: 200px;
  height: 100px;
  border-radius: var(--el-border-radius-base);
  background-color: var(--el-color-primary);
  text-align: center;
  color: #fff;
  padding: 40px 20px;
  box-sizing: border-box;
}
</style>
```

隐藏源代码

## 按需导入 [​](#按需导入)

main.ts

ts

```
// collapse
import { ElCollapseTransition } from 'element-plus'
// fade/zoom
import 'element-plus/theme-chalk/base.css'
import App from './App.vue'

const app = createApp(App)
app.component(ElCollapseTransition.name, ElCollapseTransition)
```

[SSR](https://element-plus.org/zh-CN/guide/ssr)

[更新日志](https://element-plus.org/zh-CN/guide/changelog)


