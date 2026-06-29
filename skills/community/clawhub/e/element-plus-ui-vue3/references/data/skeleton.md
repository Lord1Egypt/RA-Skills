---
name: "skeleton"
description: "Skeleton 骨架屏 -- Element Plus Vue3 桌面端组件。Invoke when user needs Skeleton 骨架屏 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/skeleton.html"
---

---

# Skeleton 骨架屏 [​](#skeleton-骨架屏)

更新日志待解决

1

在需要等待加载内容的位置设置一个骨架屏，某些场景下比 Loading 的视觉效果更好。

## 基础用法 [​](#基础用法)

基础的骨架效果。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2tlbGV0b24gLz5cbiAgPGJyIC8+XG4gIDxlbC1za2VsZXRvbiBzdHlsZT1cIi0tZWwtc2tlbGV0b24tY2lyY2xlLXNpemU6IDEwMHB4XCI+XG4gICAgPHRlbXBsYXRlICN0ZW1wbGF0ZT5cbiAgICAgIDxlbC1za2VsZXRvbi1pdGVtIHZhcmlhbnQ9XCJjaXJjbGVcIiAvPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtc2tlbGV0b24+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/skeleton/basic-usage.vue)_

vue

```
<template>
  <el-skeleton />
  <br />
  <el-skeleton style="--el-skeleton-circle-size: 100px">
    <template #template>
      <el-skeleton-item variant="circle" />
    </template>
  </el-skeleton>
</template>
```

隐藏源代码

## 更多参数 [​](#更多参数)

可以配置骨架屏段落数量，以便更接近真实渲染效果。显示的数量会比传入的数量多 1，首行会被渲染一个长度 33% 的段首。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2tlbGV0b24gOnJvd3M9XCI1XCIgLz5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/skeleton/configurable-rows.vue)_

vue

```
<template>
  <el-skeleton :rows="5" />
</template>
```

隐藏源代码

## 动画效果 [​](#动画效果)

我们提供了一个开关标志，表明是否显示加载动画， 调用 `animated` 如果真是这样，所有的 `el-skeleton` 的子节点将显示动画。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2tlbGV0b24gOnJvd3M9XCI1XCIgYW5pbWF0ZWQgLz5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/skeleton/animation.vue)_

vue

```
<template>
  <el-skeleton :rows="5" animated />
</template>
```

隐藏源代码

## 自定义样式 [​](#自定义样式)

Element Plus 提供的排版模式有时候并不满足要求，当您想要用自己定义的模板时，可以通过一个具名 Slot `template` 来自己设定模板。

我们提供了不同的模板单元可供使用，具体可选值请看 API 详细描述。 另外，在构建您自己自定义的骨架时，您应该尽可能更接近于真正的DOM。 避免DOM因高度差而发生抖动。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2tlbGV0b24gc3R5bGU9XCJ3aWR0aDogMjQwcHhcIj5cbiAgICA8dGVtcGxhdGUgI3RlbXBsYXRlPlxuICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cImltYWdlXCIgc3R5bGU9XCJ3aWR0aDogMjQwcHg7IGhlaWdodDogMjQwcHhcIiAvPlxuICAgICAgPGRpdiBzdHlsZT1cInBhZGRpbmc6IDE0cHhcIj5cbiAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cInBcIiBzdHlsZT1cIndpZHRoOiA1MCVcIiAvPlxuICAgICAgICA8ZGl2XG4gICAgICAgICAgc3R5bGU9XCJcbiAgICAgICAgICAgIGRpc3BsYXk6IGZsZXg7XG4gICAgICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyO1xuICAgICAgICAgICAganVzdGlmeS1pdGVtczogc3BhY2UtYmV0d2VlbjtcbiAgICAgICAgICBcIlxuICAgICAgICA+XG4gICAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cInRleHRcIiBzdHlsZT1cIm1hcmdpbi1yaWdodDogMTZweFwiIC8+XG4gICAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cInRleHRcIiBzdHlsZT1cIndpZHRoOiAzMCVcIiAvPlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtc2tlbGV0b24+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/skeleton/customized-template.vue)_

vue

```
<template>
  <el-skeleton style="width: 240px">
    <template #template>
      <el-skeleton-item variant="image" style="width: 240px; height: 240px" />
      <div style="padding: 14px">
        <el-skeleton-item variant="p" style="width: 50%" />
        <div
          style="
            display: flex;
            align-items: center;
            justify-items: space-between;
          "
        >
          <el-skeleton-item variant="text" style="margin-right: 16px" />
          <el-skeleton-item variant="text" style="width: 30%" />
        </div>
      </div>
    </template>
  </el-skeleton>
</template>
```

隐藏源代码

## 加载状态 [​](#加载状态)

当 `Loading` 结束之后，我们往往需要显示真实的 UI， 可以通过 `loading` 属性的值来控制是否显示加载后的 DOM。 也可以通过具名插槽 `default` 来构建 loading 结束之后需要展示的真实 DOM 元素结构。

Switch Loading

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgZGlyZWN0aW9uPVwidmVydGljYWxcIiBhbGlnbm1lbnQ9XCJmbGV4LXN0YXJ0XCI+XG4gICAgPGRpdj5cbiAgICAgIDxsYWJlbCBzdHlsZT1cIm1hcmdpbi1yaWdodDogMTZweFwiPlN3aXRjaCBMb2FkaW5nPC9sYWJlbD5cbiAgICAgIDxlbC1zd2l0Y2ggdi1tb2RlbD1cImxvYWRpbmdcIiAvPlxuICAgIDwvZGl2PlxuICAgIDxlbC1za2VsZXRvbiBzdHlsZT1cIndpZHRoOiAyNDBweFwiIDpsb2FkaW5nPVwibG9hZGluZ1wiIGFuaW1hdGVkPlxuICAgICAgPHRlbXBsYXRlICN0ZW1wbGF0ZT5cbiAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cImltYWdlXCIgc3R5bGU9XCJ3aWR0aDogMjQwcHg7IGhlaWdodDogMjQwcHhcIiAvPlxuICAgICAgICA8ZGl2IHN0eWxlPVwicGFkZGluZzogMTRweFwiPlxuICAgICAgICAgIDxlbC1za2VsZXRvbi1pdGVtIHZhcmlhbnQ9XCJoM1wiIHN0eWxlPVwid2lkdGg6IDUwJVwiIC8+XG4gICAgICAgICAgPGRpdlxuICAgICAgICAgICAgc3R5bGU9XCJcbiAgICAgICAgICAgICAgZGlzcGxheTogZmxleDtcbiAgICAgICAgICAgICAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAgICAgICAgICAgICAganVzdGlmeS1pdGVtczogc3BhY2UtYmV0d2VlbjtcbiAgICAgICAgICAgICAgbWFyZ2luLXRvcDogMTZweDtcbiAgICAgICAgICAgICAgaGVpZ2h0OiAxNnB4O1xuICAgICAgICAgICAgXCJcbiAgICAgICAgICA+XG4gICAgICAgICAgICA8ZWwtc2tlbGV0b24taXRlbSB2YXJpYW50PVwidGV4dFwiIHN0eWxlPVwibWFyZ2luLXJpZ2h0OiAxNnB4XCIgLz5cbiAgICAgICAgICAgIDxlbC1za2VsZXRvbi1pdGVtIHZhcmlhbnQ9XCJ0ZXh0XCIgc3R5bGU9XCJ3aWR0aDogMzAlXCIgLz5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgPHRlbXBsYXRlICNkZWZhdWx0PlxuICAgICAgICA8ZWwtY2FyZCA6Ym9keS1zdHlsZT1cInsgcGFkZGluZzogJzBweCcsIG1hcmdpbkJvdHRvbTogJzFweCcgfVwiPlxuICAgICAgICAgIDxpbWdcbiAgICAgICAgICAgIHNyYz1cImh0dHBzOi8vc2hhZG93LmVsZW1lY2RuLmNvbS9hcHAvZWxlbWVudC9oYW1idXJnZXIuOWNmN2IwOTEtNTVlOS0xMWU5LWE5NzYtN2Y0ZDBiMDdlZWY2LnBuZ1wiXG4gICAgICAgICAgICBjbGFzcz1cImltYWdlXCJcbiAgICAgICAgICAvPlxuICAgICAgICAgIDxkaXYgc3R5bGU9XCJwYWRkaW5nOiAxNHB4XCI+XG4gICAgICAgICAgICA8c3Bhbj5EZWxpY2lvdXMgaGFtYnVyZ2VyPC9zcGFuPlxuICAgICAgICAgICAgPGRpdiBjbGFzcz1cImJvdHRvbSBjYXJkLWhlYWRlclwiPlxuICAgICAgICAgICAgICA8ZGl2IGNsYXNzPVwidGltZVwiPnt7IGN1cnJlbnREYXRlIH19PC9kaXY+XG4gICAgICAgICAgICAgIDxlbC1idXR0b24gdGV4dCBjbGFzcz1cImJ1dHRvblwiPk9wZXJhdGlvbiBidXR0b248L2VsLWJ1dHRvbj5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2VsLWNhcmQ+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtc2tlbGV0b24+XG4gIDwvZWwtc3BhY2U+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBsb2FkaW5nID0gcmVmKHRydWUpXG5jb25zdCBjdXJyZW50RGF0ZSA9IG5ldyBEYXRlKCkudG9EYXRlU3RyaW5nKClcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/skeleton/loading-state.vue)_

vue

```
<template>
  <el-space direction="vertical" alignment="flex-start">
    <div>
      <label style="margin-right: 16px">Switch Loading</label>
      <el-switch v-model="loading" />
    </div>
    <el-skeleton style="width: 240px" :loading="loading" animated>
      <template #template>
        <el-skeleton-item variant="image" style="width: 240px; height: 240px" />
        <div style="padding: 14px">
          <el-skeleton-item variant="h3" style="width: 50%" />
          <div
            style="
              display: flex;
              align-items: center;
              justify-items: space-between;
              margin-top: 16px;
              height: 16px;
            "
          >
            <el-skeleton-item variant="text" style="margin-right: 16px" />
            <el-skeleton-item variant="text" style="width: 30%" />
          </div>
        </div>
      </template>
      <template #default>
        <el-card :body-style="{ padding: '0px', marginBottom: '1px' }">
          <img
            src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
            class="image"
          />
          <div style="padding: 14px">
            <span>Delicious hamburger</span>
            <div class="bottom card-header">
              <div class="time">{{ currentDate }}</div>
              <el-button text class="button">Operation button</el-button>
            </div>
          </div>
        </el-card>
      </template>
    </el-skeleton>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const loading = ref(true)
const currentDate = new Date().toDateString()
</script>
```

隐藏源代码

## 渲染多条数据 [​](#渲染多条数据)

大多时候, 骨架屏都被用来渲染列表, 当我们需要在从服务器获取数据的时候来渲染一个假的 UI。 利用 `count` 这个属性就能控制渲染多少条假的数据在页面上

TIP

我们不推荐在浏览器中渲染过多的虚假 UI 元素，这样会消耗更多时间销毁骨架元素，从而引起性能问题。 为了用户体验，请尽量将 `count` 值保持在小一点的数值。

Click me to reload

![](https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg)

Deer

Wed Jun 24 2026

Operation button

![](https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg)

Horse

Wed Jun 24 2026

Operation button

![](https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg)

Mountain Lion

Wed Jun 24 2026

Operation button

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2Ugc3R5bGU9XCJ3aWR0aDogMTAwJVwiIGZpbGw+XG4gICAgPGRpdj5cbiAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwic2V0TG9hZGluZ1wiPkNsaWNrIG1lIHRvIHJlbG9hZDwvZWwtYnV0dG9uPlxuICAgIDwvZGl2PlxuICAgIDxlbC1za2VsZXRvblxuICAgICAgc3R5bGU9XCJkaXNwbGF5OiBmbGV4OyBnYXA6IDhweFwiXG4gICAgICA6bG9hZGluZz1cImxvYWRpbmdcIlxuICAgICAgYW5pbWF0ZWRcbiAgICAgIDpjb3VudD1cIjNcIlxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjdGVtcGxhdGU+XG4gICAgICAgIDxkaXYgc3R5bGU9XCJmbGV4OiAxXCI+XG4gICAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cImltYWdlXCIgc3R5bGU9XCJoZWlnaHQ6IDI0MHB4XCIgLz5cbiAgICAgICAgICA8ZGl2IHN0eWxlPVwicGFkZGluZzogMTRweFwiPlxuICAgICAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cImgzXCIgc3R5bGU9XCJ3aWR0aDogNTAlXCIgLz5cbiAgICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgICAgc3R5bGU9XCJcbiAgICAgICAgICAgICAgICBkaXNwbGF5OiBmbGV4O1xuICAgICAgICAgICAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gICAgICAgICAgICAgICAganVzdGlmeS1pdGVtczogc3BhY2UtYmV0d2VlbjtcbiAgICAgICAgICAgICAgICBtYXJnaW4tdG9wOiAxNnB4O1xuICAgICAgICAgICAgICAgIGhlaWdodDogMTZweDtcbiAgICAgICAgICAgICAgXCJcbiAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cInRleHRcIiBzdHlsZT1cIm1hcmdpbi1yaWdodDogMTZweFwiIC8+XG4gICAgICAgICAgICAgIDxlbC1za2VsZXRvbi1pdGVtIHZhcmlhbnQ9XCJ0ZXh0XCIgc3R5bGU9XCJ3aWR0aDogMzAlXCIgLz5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ+XG4gICAgICAgIDxlbC1jYXJkXG4gICAgICAgICAgdi1mb3I9XCJpdGVtIGluIGxpc3RzXCJcbiAgICAgICAgICA6a2V5PVwiaXRlbS5uYW1lXCJcbiAgICAgICAgICA6Ym9keS1zdHlsZT1cInsgcGFkZGluZzogJzBweCcsIG1hcmdpbkJvdHRvbTogJzFweCcgfVwiXG4gICAgICAgID5cbiAgICAgICAgICA8aW1nXG4gICAgICAgICAgICA6c3JjPVwiaXRlbS5pbWdVcmxcIlxuICAgICAgICAgICAgY2xhc3M9XCJpbWFnZSBtdWx0aS1jb250ZW50XCJcbiAgICAgICAgICAgIHN0eWxlPVwibWF4LXdpZHRoOiAxMDAlXCJcbiAgICAgICAgICAvPlxuICAgICAgICAgIDxkaXYgc3R5bGU9XCJwYWRkaW5nOiAxNHB4XCI+XG4gICAgICAgICAgICA8c3Bhbj57eyBpdGVtLm5hbWUgfX08L3NwYW4+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzPVwiYm90dG9tIGNhcmQtaGVhZGVyXCI+XG4gICAgICAgICAgICAgIDxkaXYgY2xhc3M9XCJ0aW1lXCI+e3sgY3VycmVudERhdGUgfX08L2Rpdj5cbiAgICAgICAgICAgICAgPGVsLWJ1dHRvbiB0ZXh0IGNsYXNzPVwiYnV0dG9uXCI+T3BlcmF0aW9uIGJ1dHRvbjwvZWwtYnV0dG9uPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZWwtY2FyZD5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1za2VsZXRvbj5cbiAgPC9lbC1zcGFjZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBvbk1vdW50ZWQsIHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW50ZXJmYWNlIExpc3RJdGVtIHtcbiAgaW1nVXJsOiBzdHJpbmdcbiAgbmFtZTogc3RyaW5nXG59XG5cbmNvbnN0IGxvYWRpbmcgPSByZWYodHJ1ZSlcbmNvbnN0IGxpc3RzID0gcmVmPExpc3RJdGVtW10+KFtdKVxuY29uc3QgY3VycmVudERhdGUgPSBuZXcgRGF0ZSgpLnRvRGF0ZVN0cmluZygpXG5cbmNvbnN0IHNldExvYWRpbmcgPSAoKSA9PiB7XG4gIGxvYWRpbmcudmFsdWUgPSB0cnVlXG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGxvYWRpbmcudmFsdWUgPSBmYWxzZVxuICB9LCAyMDAwKVxufVxuXG5vbk1vdW50ZWQoKCkgPT4ge1xuICBsb2FkaW5nLnZhbHVlID0gZmFsc2VcbiAgbGlzdHMudmFsdWUgPSBbXG4gICAge1xuICAgICAgaW1nVXJsOlxuICAgICAgICAnaHR0cHM6Ly9mdXNzMTAuZWxlbWVjZG4uY29tL2EvM2YvMzMwMmU1OGY5YTE4MWQyNTA5ZjNkYzBmYTY4YjBqcGVnLmpwZWcnLFxuICAgICAgbmFtZTogJ0RlZXInLFxuICAgIH0sXG4gICAge1xuICAgICAgaW1nVXJsOlxuICAgICAgICAnaHR0cHM6Ly9mdXNzMTAuZWxlbWVjZG4uY29tLzEvMzQvMTlhYTk4YjFmY2IyNzgxYzRmYmEzM2Q4NTA1NDlqcGVnLmpwZWcnLFxuICAgICAgbmFtZTogJ0hvcnNlJyxcbiAgICB9LFxuICAgIHtcbiAgICAgIGltZ1VybDpcbiAgICAgICAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8wLzZmL2UzNWZmMzc1ODEyZTZiMDAyMGI2YjRlOGY5NTgzanBlZy5qcGVnJyxcbiAgICAgIG5hbWU6ICdNb3VudGFpbiBMaW9uJyxcbiAgICB9LFxuICBdXG59KVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/skeleton/rendering-with-data.vue)_

vue

```
<template>
  <el-space style="width: 100%" fill>
    <div>
      <el-button @click="setLoading">Click me to reload</el-button>
    </div>
    <el-skeleton
      style="display: flex; gap: 8px"
      :loading="loading"
      animated
      :count="3"
    >
      <template #template>
        <div style="flex: 1">
          <el-skeleton-item variant="image" style="height: 240px" />
          <div style="padding: 14px">
            <el-skeleton-item variant="h3" style="width: 50%" />
            <div
              style="
                display: flex;
                align-items: center;
                justify-items: space-between;
                margin-top: 16px;
                height: 16px;
              "
            >
              <el-skeleton-item variant="text" style="margin-right: 16px" />
              <el-skeleton-item variant="text" style="width: 30%" />
            </div>
          </div>
        </div>
      </template>
      <template #default>
        <el-card
          v-for="item in lists"
          :key="item.name"
          :body-style="{ padding: '0px', marginBottom: '1px' }"
        >
          <img
            :src="item.imgUrl"
            class="image multi-content"
            style="max-width: 100%"
          />
          <div style="padding: 14px">
            <span>{{ item.name }}</span>
            <div class="bottom card-header">
              <div class="time">{{ currentDate }}</div>
              <el-button text class="button">Operation button</el-button>
            </div>
          </div>
        </el-card>
      </template>
    </el-skeleton>
  </el-space>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

interface ListItem {
  imgUrl: string
  name: string
}

const loading = ref(true)
const lists = ref<ListItem[]>([])
const currentDate = new Date().toDateString()

const setLoading = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 2000)
}

onMounted(() => {
  loading.value = false
  lists.value = [
    {
      imgUrl:
        'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
      name: 'Deer',
    },
    {
      imgUrl:
        'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
      name: 'Horse',
    },
    {
      imgUrl:
        'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
      name: 'Mountain Lion',
    },
  ]
})
</script>
```

隐藏源代码

## 防止渲染抖动 [​](#防止渲染抖动)

有的时候，API 的请求回来的特别快，往往骨架占位刚刚被渲染，真实的数据就已经回来了，用户的界面会突然一闪， 此时为了避免这种情况，就需要通过 `throttle` 属性来避免这个问题。

TIP

2.8.8版本里， `throtle` 属性支持两个值： `number` 和 `object`。 当通过 `number`时，它相当于 `{leading: xxx}`，控制骨架屏幕显示的节奏。 当然，您也可以通过传递 `{trailing: xxx}` 来控制骨架屏消失的节奏。

Switch Loading

![](https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png)

Delicious hamburger

Wed Jun 24 2026

operation button

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgZGlyZWN0aW9uPVwidmVydGljYWxcIiBhbGlnbm1lbnQ9XCJmbGV4LXN0YXJ0XCI+XG4gICAgPGRpdj5cbiAgICAgIDxsYWJlbCBzdHlsZT1cIm1hcmdpbi1yaWdodDogMTZweFwiPlN3aXRjaCBMb2FkaW5nPC9sYWJlbD5cbiAgICAgIDxlbC1zd2l0Y2ggdi1tb2RlbD1cImxvYWRpbmdcIiAvPlxuICAgIDwvZGl2PlxuICAgIDxlbC1za2VsZXRvblxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgOmxvYWRpbmc9XCJsb2FkaW5nXCJcbiAgICAgIGFuaW1hdGVkXG4gICAgICA6dGhyb3R0bGU9XCI1MDBcIlxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjdGVtcGxhdGU+XG4gICAgICAgIDxlbC1za2VsZXRvbi1pdGVtIHZhcmlhbnQ9XCJpbWFnZVwiIHN0eWxlPVwid2lkdGg6IDI0MHB4OyBoZWlnaHQ6IDI2NXB4XCIgLz5cbiAgICAgICAgPGRpdiBzdHlsZT1cInBhZGRpbmc6IDE0cHhcIj5cbiAgICAgICAgICA8ZWwtc2tlbGV0b24taXRlbSB2YXJpYW50PVwiaDNcIiBzdHlsZT1cIndpZHRoOiA1MCVcIiAvPlxuICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgIHN0eWxlPVwiXG4gICAgICAgICAgICAgIGRpc3BsYXk6IGZsZXg7XG4gICAgICAgICAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gICAgICAgICAgICAgIGp1c3RpZnktaXRlbXM6IHNwYWNlLWJldHdlZW47XG4gICAgICAgICAgICAgIG1hcmdpbi10b3A6IDE2cHg7XG4gICAgICAgICAgICAgIGhlaWdodDogMTZweDtcbiAgICAgICAgICAgIFwiXG4gICAgICAgICAgPlxuICAgICAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cInRleHRcIiBzdHlsZT1cIm1hcmdpbi1yaWdodDogMTZweFwiIC8+XG4gICAgICAgICAgICA8ZWwtc2tlbGV0b24taXRlbSB2YXJpYW50PVwidGV4dFwiIHN0eWxlPVwid2lkdGg6IDMwJVwiIC8+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD5cbiAgICAgICAgPGVsLWNhcmQgOmJvZHktc3R5bGU9XCJ7IHBhZGRpbmc6ICcwcHgnLCBtYXJnaW5Cb3R0b206ICcxcHgnIH1cIj5cbiAgICAgICAgICA8aW1nXG4gICAgICAgICAgICBzcmM9XCJodHRwczovL3NoYWRvdy5lbGVtZWNkbi5jb20vYXBwL2VsZW1lbnQvaGFtYnVyZ2VyLjljZjdiMDkxLTU1ZTktMTFlOS1hOTc2LTdmNGQwYjA3ZWVmNi5wbmdcIlxuICAgICAgICAgICAgY2xhc3M9XCJpbWFnZVwiXG4gICAgICAgICAgLz5cbiAgICAgICAgICA8ZGl2IHN0eWxlPVwicGFkZGluZzogMTRweFwiPlxuICAgICAgICAgICAgPHNwYW4+RGVsaWNpb3VzIGhhbWJ1cmdlcjwvc3Bhbj5cbiAgICAgICAgICAgIDxkaXYgY2xhc3M9XCJib3R0b20gY2FyZC1oZWFkZXJcIj5cbiAgICAgICAgICAgICAgPGRpdiBjbGFzcz1cInRpbWVcIj57eyBjdXJyZW50RGF0ZSB9fTwvZGl2PlxuICAgICAgICAgICAgICA8ZWwtYnV0dG9uIHRleHQgY2xhc3M9XCJidXR0b25cIj5vcGVyYXRpb24gYnV0dG9uPC9lbC1idXR0b24+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9lbC1jYXJkPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLXNrZWxldG9uPlxuICA8L2VsLXNwYWNlPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgbG9hZGluZyA9IHJlZihmYWxzZSlcbmNvbnN0IGN1cnJlbnREYXRlID0gbmV3IERhdGUoKS50b0RhdGVTdHJpbmcoKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/skeleton/avoiding-rendering-bouncing.vue)_

vue

```
<template>
  <el-space direction="vertical" alignment="flex-start">
    <div>
      <label style="margin-right: 16px">Switch Loading</label>
      <el-switch v-model="loading" />
    </div>
    <el-skeleton
      style="width: 240px"
      :loading="loading"
      animated
      :throttle="500"
    >
      <template #template>
        <el-skeleton-item variant="image" style="width: 240px; height: 265px" />
        <div style="padding: 14px">
          <el-skeleton-item variant="h3" style="width: 50%" />
          <div
            style="
              display: flex;
              align-items: center;
              justify-items: space-between;
              margin-top: 16px;
              height: 16px;
            "
          >
            <el-skeleton-item variant="text" style="margin-right: 16px" />
            <el-skeleton-item variant="text" style="width: 30%" />
          </div>
        </div>
      </template>
      <template #default>
        <el-card :body-style="{ padding: '0px', marginBottom: '1px' }">
          <img
            src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
            class="image"
          />
          <div style="padding: 14px">
            <span>Delicious hamburger</span>
            <div class="bottom card-header">
              <div class="time">{{ currentDate }}</div>
              <el-button text class="button">operation button</el-button>
            </div>
          </div>
        </el-card>
      </template>
    </el-skeleton>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const loading = ref(false)
const currentDate = new Date().toDateString()
</script>
```

隐藏源代码

## 初始渲染加载 2.8.8 [​](#初始渲染加载)

当初始值为 loading: true 时，您可以设置 `throttle: {initVal: true, leading: xxx}` 来控制初始骨架屏的即时显示，而无需进行节流。

Switch Loading

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgZGlyZWN0aW9uPVwidmVydGljYWxcIiBhbGlnbm1lbnQ9XCJmbGV4LXN0YXJ0XCI+XG4gICAgPGRpdj5cbiAgICAgIDxsYWJlbCBzdHlsZT1cIm1hcmdpbi1yaWdodDogMTZweFwiPlN3aXRjaCBMb2FkaW5nPC9sYWJlbD5cbiAgICAgIDxlbC1zd2l0Y2ggdi1tb2RlbD1cImxvYWRpbmdcIiAvPlxuICAgIDwvZGl2PlxuICAgIDxlbC1za2VsZXRvblxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgOmxvYWRpbmc9XCJsb2FkaW5nXCJcbiAgICAgIGFuaW1hdGVkXG4gICAgICA6dGhyb3R0bGU9XCJ7IGxlYWRpbmc6IDUwMCwgaW5pdFZhbDogdHJ1ZSB9XCJcbiAgICA+XG4gICAgICA8dGVtcGxhdGUgI3RlbXBsYXRlPlxuICAgICAgICA8ZWwtc2tlbGV0b24taXRlbSB2YXJpYW50PVwiaW1hZ2VcIiBzdHlsZT1cIndpZHRoOiAyNDBweDsgaGVpZ2h0OiAyNjVweFwiIC8+XG4gICAgICAgIDxkaXYgc3R5bGU9XCJwYWRkaW5nOiAxNHB4XCI+XG4gICAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cImgzXCIgc3R5bGU9XCJ3aWR0aDogNTAlXCIgLz5cbiAgICAgICAgICA8ZGl2XG4gICAgICAgICAgICBzdHlsZT1cIlxuICAgICAgICAgICAgICBkaXNwbGF5OiBmbGV4O1xuICAgICAgICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyO1xuICAgICAgICAgICAgICBqdXN0aWZ5LWl0ZW1zOiBzcGFjZS1iZXR3ZWVuO1xuICAgICAgICAgICAgICBtYXJnaW4tdG9wOiAxNnB4O1xuICAgICAgICAgICAgICBoZWlnaHQ6IDE2cHg7XG4gICAgICAgICAgICBcIlxuICAgICAgICAgID5cbiAgICAgICAgICAgIDxlbC1za2VsZXRvbi1pdGVtIHZhcmlhbnQ9XCJ0ZXh0XCIgc3R5bGU9XCJtYXJnaW4tcmlnaHQ6IDE2cHhcIiAvPlxuICAgICAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cInRleHRcIiBzdHlsZT1cIndpZHRoOiAzMCVcIiAvPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ+XG4gICAgICAgIDxlbC1jYXJkIDpib2R5LXN0eWxlPVwieyBwYWRkaW5nOiAnMHB4JywgbWFyZ2luQm90dG9tOiAnMXB4JyB9XCI+XG4gICAgICAgICAgPGltZ1xuICAgICAgICAgICAgc3JjPVwiaHR0cHM6Ly9zaGFkb3cuZWxlbWVjZG4uY29tL2FwcC9lbGVtZW50L2hhbWJ1cmdlci45Y2Y3YjA5MS01NWU5LTExZTktYTk3Ni03ZjRkMGIwN2VlZjYucG5nXCJcbiAgICAgICAgICAgIGNsYXNzPVwiaW1hZ2VcIlxuICAgICAgICAgIC8+XG4gICAgICAgICAgPGRpdiBzdHlsZT1cInBhZGRpbmc6IDE0cHhcIj5cbiAgICAgICAgICAgIDxzcGFuPkRlbGljaW91cyBoYW1idXJnZXI8L3NwYW4+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzPVwiYm90dG9tIGNhcmQtaGVhZGVyXCI+XG4gICAgICAgICAgICAgIDxkaXYgY2xhc3M9XCJ0aW1lXCI+e3sgY3VycmVudERhdGUgfX08L2Rpdj5cbiAgICAgICAgICAgICAgPGVsLWJ1dHRvbiB0ZXh0IGNsYXNzPVwiYnV0dG9uXCI+b3BlcmF0aW9uIGJ1dHRvbjwvZWwtYnV0dG9uPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZWwtY2FyZD5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1za2VsZXRvbj5cbiAgPC9lbC1zcGFjZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGxvYWRpbmcgPSByZWYodHJ1ZSlcbmNvbnN0IGN1cnJlbnREYXRlID0gbmV3IERhdGUoKS50b0RhdGVTdHJpbmcoKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/skeleton/initial-rendering-loading.vue)_

vue

```
<template>
  <el-space direction="vertical" alignment="flex-start">
    <div>
      <label style="margin-right: 16px">Switch Loading</label>
      <el-switch v-model="loading" />
    </div>
    <el-skeleton
      style="width: 240px"
      :loading="loading"
      animated
      :throttle="{ leading: 500, initVal: true }"
    >
      <template #template>
        <el-skeleton-item variant="image" style="width: 240px; height: 265px" />
        <div style="padding: 14px">
          <el-skeleton-item variant="h3" style="width: 50%" />
          <div
            style="
              display: flex;
              align-items: center;
              justify-items: space-between;
              margin-top: 16px;
              height: 16px;
            "
          >
            <el-skeleton-item variant="text" style="margin-right: 16px" />
            <el-skeleton-item variant="text" style="width: 30%" />
          </div>
        </div>
      </template>
      <template #default>
        <el-card :body-style="{ padding: '0px', marginBottom: '1px' }">
          <img
            src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
            class="image"
          />
          <div style="padding: 14px">
            <span>Delicious hamburger</span>
            <div class="bottom card-header">
              <div class="time">{{ currentDate }}</div>
              <el-button text class="button">operation button</el-button>
            </div>
          </div>
        </el-card>
      </template>
    </el-skeleton>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const loading = ref(true)
const currentDate = new Date().toDateString()
</script>
```

隐藏源代码

## 切换显示/隐藏时避免渲染抖动 2.8.8 [​](#切换显示-隐藏时避免渲染抖动)

TIP

您可以设置 `throttle: {initVal: true, leading: xxx, trailing: xxx}`，以控制骨架效果的初始显示，并使切换加载状态时骨架效果的过渡更加平滑。

有时，当加载状态切换显示或隐藏时，您可能希望业务组件的渲染更加平滑。 您可以设置 `throttle: {leading: xxx, trailing: xxx}` 来控制渲染抖动。

Switch Loading

![](https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png)

Delicious hamburger

Wed Jun 24 2026

operation button

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgZGlyZWN0aW9uPVwidmVydGljYWxcIiBhbGlnbm1lbnQ9XCJmbGV4LXN0YXJ0XCI+XG4gICAgPGRpdj5cbiAgICAgIDxsYWJlbCBzdHlsZT1cIm1hcmdpbi1yaWdodDogMTZweFwiPlN3aXRjaCBMb2FkaW5nPC9sYWJlbD5cbiAgICAgIDxlbC1zd2l0Y2ggdi1tb2RlbD1cImxvYWRpbmdcIiAvPlxuICAgIDwvZGl2PlxuICAgIDxlbC1za2VsZXRvblxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgOmxvYWRpbmc9XCJsb2FkaW5nXCJcbiAgICAgIGFuaW1hdGVkXG4gICAgICA6dGhyb3R0bGU9XCJ7IGxlYWRpbmc6IDUwMCwgdHJhaWxpbmc6IDUwMCwgaW5pdFZhbDogdHJ1ZSB9XCJcbiAgICA+XG4gICAgICA8dGVtcGxhdGUgI3RlbXBsYXRlPlxuICAgICAgICA8ZWwtc2tlbGV0b24taXRlbSB2YXJpYW50PVwiaW1hZ2VcIiBzdHlsZT1cIndpZHRoOiAyNDBweDsgaGVpZ2h0OiAyNjVweFwiIC8+XG4gICAgICAgIDxkaXYgc3R5bGU9XCJwYWRkaW5nOiAxNHB4XCI+XG4gICAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cImgzXCIgc3R5bGU9XCJ3aWR0aDogNTAlXCIgLz5cbiAgICAgICAgICA8ZGl2XG4gICAgICAgICAgICBzdHlsZT1cIlxuICAgICAgICAgICAgICBkaXNwbGF5OiBmbGV4O1xuICAgICAgICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyO1xuICAgICAgICAgICAgICBqdXN0aWZ5LWl0ZW1zOiBzcGFjZS1iZXR3ZWVuO1xuICAgICAgICAgICAgICBtYXJnaW4tdG9wOiAxNnB4O1xuICAgICAgICAgICAgICBoZWlnaHQ6IDE2cHg7XG4gICAgICAgICAgICBcIlxuICAgICAgICAgID5cbiAgICAgICAgICAgIDxlbC1za2VsZXRvbi1pdGVtIHZhcmlhbnQ9XCJ0ZXh0XCIgc3R5bGU9XCJtYXJnaW4tcmlnaHQ6IDE2cHhcIiAvPlxuICAgICAgICAgICAgPGVsLXNrZWxldG9uLWl0ZW0gdmFyaWFudD1cInRleHRcIiBzdHlsZT1cIndpZHRoOiAzMCVcIiAvPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ+XG4gICAgICAgIDxlbC1jYXJkIDpib2R5LXN0eWxlPVwieyBwYWRkaW5nOiAnMHB4JywgbWFyZ2luQm90dG9tOiAnMXB4JyB9XCI+XG4gICAgICAgICAgPGltZ1xuICAgICAgICAgICAgc3JjPVwiaHR0cHM6Ly9zaGFkb3cuZWxlbWVjZG4uY29tL2FwcC9lbGVtZW50L2hhbWJ1cmdlci45Y2Y3YjA5MS01NWU5LTExZTktYTk3Ni03ZjRkMGIwN2VlZjYucG5nXCJcbiAgICAgICAgICAgIGNsYXNzPVwiaW1hZ2VcIlxuICAgICAgICAgIC8+XG4gICAgICAgICAgPGRpdiBzdHlsZT1cInBhZGRpbmc6IDE0cHhcIj5cbiAgICAgICAgICAgIDxzcGFuPkRlbGljaW91cyBoYW1idXJnZXI8L3NwYW4+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzPVwiYm90dG9tIGNhcmQtaGVhZGVyXCI+XG4gICAgICAgICAgICAgIDxkaXYgY2xhc3M9XCJ0aW1lXCI+e3sgY3VycmVudERhdGUgfX08L2Rpdj5cbiAgICAgICAgICAgICAgPGVsLWJ1dHRvbiB0ZXh0IGNsYXNzPVwiYnV0dG9uXCI+b3BlcmF0aW9uIGJ1dHRvbjwvZWwtYnV0dG9uPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZWwtY2FyZD5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1za2VsZXRvbj5cbiAgPC9lbC1zcGFjZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGxvYWRpbmcgPSByZWYoZmFsc2UpXG5jb25zdCBjdXJyZW50RGF0ZSA9IG5ldyBEYXRlKCkudG9EYXRlU3RyaW5nKClcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/skeleton/leading-trailing-without-bouncing.vue)_

vue

```
<template>
  <el-space direction="vertical" alignment="flex-start">
    <div>
      <label style="margin-right: 16px">Switch Loading</label>
      <el-switch v-model="loading" />
    </div>
    <el-skeleton
      style="width: 240px"
      :loading="loading"
      animated
      :throttle="{ leading: 500, trailing: 500, initVal: true }"
    >
      <template #template>
        <el-skeleton-item variant="image" style="width: 240px; height: 265px" />
        <div style="padding: 14px">
          <el-skeleton-item variant="h3" style="width: 50%" />
          <div
            style="
              display: flex;
              align-items: center;
              justify-items: space-between;
              margin-top: 16px;
              height: 16px;
            "
          >
            <el-skeleton-item variant="text" style="margin-right: 16px" />
            <el-skeleton-item variant="text" style="width: 30%" />
          </div>
        </div>
      </template>
      <template #default>
        <el-card :body-style="{ padding: '0px', marginBottom: '1px' }">
          <img
            src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
            class="image"
          />
          <div style="padding: 14px">
            <span>Delicious hamburger</span>
            <div class="bottom card-header">
              <div class="time">{{ currentDate }}</div>
              <el-button text class="button">operation button</el-button>
            </div>
          </div>
        </el-card>
      </template>
    </el-skeleton>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const loading = ref(false)
const currentDate = new Date().toDateString()
</script>
```

隐藏源代码

## [​](#)

## Skeleton API [​](#skeleton-api)

### Skeleton Attributes [​](#skeleton-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| animated | 是否使用动画 | `boolean` | false |
| count | 渲染多少个 template, 建议使用尽可能小的数字 | `number` | 1 |
| loading | 是否显示加载结束后的 DOM 结构 | `boolean` | false |
| rows | 骨架屏段落数量 | `number` | 3 |
| throttle | 渲染延迟（以毫秒为单位） 数字代表延迟显示, 也可以设置为延迟隐藏, 例如 `{ leading: 500, trailing: 500 }` 当需要控制初始加载值时，您可以设置 `{ initVal: true }` | `number` / `object` | 0 |

### Skeleton Slots [​](#skeleton-slots)

| 插槽名 | 说明 | 事件参数 |
| --- | --- | --- |
| default | 真正渲染的DOM | `object` |
| template | 渲染 skeleton 模板的内容 | `object` |

## SkeletonItem API [​](#skeletonitem-api)

### SkeletonItem Attributes [​](#skeletonitem-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| variant | 当前渲染 skeleton 类型 | `enum` | text |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/skeleton) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/skeleton.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/skeleton.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/137589237?v=4&size=64)](https://github.com/zero-years)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/15872986?v=4&size=64)](https://github.com/chenweiyi)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/20543158?v=4&size=64)](https://github.com/porcelainHeart)[![](https://avatars.githubusercontent.com/u/65892539?v=4&size=64)](https://github.com/xionkq)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)

[Result 结果](https://element-plus.org/zh-CN/component/result)

[Table 表格](https://element-plus.org/zh-CN/component/table)


