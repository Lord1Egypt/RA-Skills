---
name: "carousel"
description: "Carousel 走马灯 -- Element Plus Vue3 桌面端组件。Invoke when user needs Carousel 走马灯 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/carousel.html"
---

---

# Carousel 走马灯 [​](#carousel-走马灯)

更新日志待解决

7

在有限空间内，循环播放同一类型的图片、文字等内容

## 基础用法 [​](#基础用法)

结合使用 `el-carousel` 和 `el-carousel-item` 标签就得到了一个走马灯。 每一个页面的内容是完全可定制的，把你想要展示的内容放在 `el-carousel-item` 标签内。 默认情况下，在鼠标 hover 底部的指示器时就会触发切换。 通过设置 `trigger` 属性为 `click`，可以达到点击触发的效果。

Switch when indicator is hovered (default)

### 1

### 2

### 3

### 4

Switch when indicator is clicked

### 1

### 2

### 3

### 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiYmxvY2sgdGV4dC1jZW50ZXJcIj5cbiAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5cbiAgICAgIFN3aXRjaCB3aGVuIGluZGljYXRvciBpcyBob3ZlcmVkIChkZWZhdWx0KVxuICAgIDwvc3Bhbj5cbiAgICA8ZWwtY2Fyb3VzZWwgaGVpZ2h0PVwiMTUwcHhcIj5cbiAgICAgIDxlbC1jYXJvdXNlbC1pdGVtIHYtZm9yPVwiaXRlbSBpbiA0XCIgOmtleT1cIml0ZW1cIj5cbiAgICAgICAgPGgzIGNsYXNzPVwic21hbGwganVzdGlmeS1jZW50ZXJcIiB0ZXh0PVwiMnhsXCI+e3sgaXRlbSB9fTwvaDM+XG4gICAgICA8L2VsLWNhcm91c2VsLWl0ZW0+XG4gICAgPC9lbC1jYXJvdXNlbD5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJibG9jayB0ZXh0LWNlbnRlclwiIG09XCJ0LTRcIj5cbiAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5Td2l0Y2ggd2hlbiBpbmRpY2F0b3IgaXMgY2xpY2tlZDwvc3Bhbj5cbiAgICA8ZWwtY2Fyb3VzZWwgdHJpZ2dlcj1cImNsaWNrXCIgaGVpZ2h0PVwiMTUwcHhcIj5cbiAgICAgIDxlbC1jYXJvdXNlbC1pdGVtIHYtZm9yPVwiaXRlbSBpbiA0XCIgOmtleT1cIml0ZW1cIj5cbiAgICAgICAgPGgzIGNsYXNzPVwic21hbGwganVzdGlmeS1jZW50ZXJcIiB0ZXh0PVwiMnhsXCI+e3sgaXRlbSB9fTwvaDM+XG4gICAgICA8L2VsLWNhcm91c2VsLWl0ZW0+XG4gICAgPC9lbC1jYXJvdXNlbD5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW9uc3RyYXRpb24ge1xuICBjb2xvcjogdmFyKC0tZWwtdGV4dC1jb2xvci1zZWNvbmRhcnkpO1xufVxuXG4uZWwtY2Fyb3VzZWxfX2l0ZW0gaDMge1xuICBjb2xvcjogIzQ3NTY2OTtcbiAgb3BhY2l0eTogMC43NTtcbiAgbGluZS1oZWlnaHQ6IDE1MHB4O1xuICBtYXJnaW46IDA7XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbn1cblxuLmVsLWNhcm91c2VsX19pdGVtOm50aC1jaGlsZCgybikge1xuICBiYWNrZ3JvdW5kLWNvbG9yOiAjOTlhOWJmO1xufVxuXG4uZWwtY2Fyb3VzZWxfX2l0ZW06bnRoLWNoaWxkKDJuICsgMSkge1xuICBiYWNrZ3JvdW5kLWNvbG9yOiAjZDNkY2U2O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/carousel/basic.vue)_

vue

```
<template>
  <div class="block text-center">
    <span class="demonstration">
      Switch when indicator is hovered (default)
    </span>
    <el-carousel height="150px">
      <el-carousel-item v-for="item in 4" :key="item">
        <h3 class="small justify-center" text="2xl">{{ item }}</h3>
      </el-carousel-item>
    </el-carousel>
  </div>
  <div class="block text-center" m="t-4">
    <span class="demonstration">Switch when indicator is clicked</span>
    <el-carousel trigger="click" height="150px">
      <el-carousel-item v-for="item in 4" :key="item">
        <h3 class="small justify-center" text="2xl">{{ item }}</h3>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<style scoped>
.demonstration {
  color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

隐藏源代码

## 动态模糊 2.6.0 [​](#动态模糊)

添加动态模糊以给走马灯注入活力和流畅性。

启用动态模糊增强了走马灯的活力和流畅性。 `motion-blur` 的默认值是 `false`，手动激活此功能即可提供视觉感受上的提升。

Motion blur the switch (default)

### 1

### 2

### 3

### 4

Vertical effect

### 1

### 2

### 3

### 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiYmxvY2sgdGV4dC1jZW50ZXJcIj5cbiAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5Nb3Rpb24gYmx1ciB0aGUgc3dpdGNoIChkZWZhdWx0KTwvc3Bhbj5cbiAgICA8ZWwtY2Fyb3VzZWwgaGVpZ2h0PVwiMjAwcHhcIiBtb3Rpb24tYmx1cj5cbiAgICAgIDxlbC1jYXJvdXNlbC1pdGVtIHYtZm9yPVwiaXRlbSBpbiA0XCIgOmtleT1cIml0ZW1cIj5cbiAgICAgICAgPGgzIGNsYXNzPVwic21hbGwganVzdGlmeS1jZW50ZXJcIiB0ZXh0PVwiMnhsXCI+e3sgaXRlbSB9fTwvaDM+XG4gICAgICA8L2VsLWNhcm91c2VsLWl0ZW0+XG4gICAgPC9lbC1jYXJvdXNlbD5cbiAgPC9kaXY+XG4gIDxwIGNsYXNzPVwidGV4dC1jZW50ZXIgZGVtb25zdHJhdGlvblwiPlZlcnRpY2FsIGVmZmVjdDwvcD5cbiAgPGVsLWNhcm91c2VsXG4gICAgaGVpZ2h0PVwiMjAwcHhcIlxuICAgIGRpcmVjdGlvbj1cInZlcnRpY2FsXCJcbiAgICBtb3Rpb24tYmx1clxuICAgIDphdXRvcGxheT1cImZhbHNlXCJcbiAgPlxuICAgIDxlbC1jYXJvdXNlbC1pdGVtIHYtZm9yPVwiaXRlbSBpbiA0XCIgOmtleT1cIml0ZW1cIj5cbiAgICAgIDxoMyB0ZXh0PVwiMnhsXCIganVzdGlmeT1cImNlbnRlclwiPnt7IGl0ZW0gfX08L2gzPlxuICAgIDwvZWwtY2Fyb3VzZWwtaXRlbT5cbiAgPC9lbC1jYXJvdXNlbD5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtb25zdHJhdGlvbiB7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG59XG5cbi5lbC1jYXJvdXNlbF9faXRlbSBoMyB7XG4gIGNvbG9yOiAjNDc1NjY5O1xuICBvcGFjaXR5OiAwLjc1O1xuICBsaW5lLWhlaWdodDogMjAwcHg7XG4gIG1hcmdpbjogMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xufVxuXG4uZWwtY2Fyb3VzZWxfX2l0ZW06bnRoLWNoaWxkKDJuKSB7XG4gIGJhY2tncm91bmQtY29sb3I6ICM5OWE5YmY7XG59XG5cbi5lbC1jYXJvdXNlbF9faXRlbTpudGgtY2hpbGQoMm4gKyAxKSB7XG4gIGJhY2tncm91bmQtY29sb3I6ICNkM2RjZTY7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/carousel/motion-blur.vue)_

vue

```
<template>
  <div class="block text-center">
    <span class="demonstration">Motion blur the switch (default)</span>
    <el-carousel height="200px" motion-blur>
      <el-carousel-item v-for="item in 4" :key="item">
        <h3 class="small justify-center" text="2xl">{{ item }}</h3>
      </el-carousel-item>
    </el-carousel>
  </div>
  <p class="text-center demonstration">Vertical effect</p>
  <el-carousel
    height="200px"
    direction="vertical"
    motion-blur
    :autoplay="false"
  >
    <el-carousel-item v-for="item in 4" :key="item">
      <h3 text="2xl" justify="center">{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.demonstration {
  color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

隐藏源代码

## 指示器 [​](#指示器)

可以将指示器的显示位置设置在容器外部

`indicator-position` 属性定义了指示器的位置。 默认情况下，它会显示在走马灯内部，设置为 `outside` 则会显示在外部；设置为 `none` 则不会显示指示器。

### 1

### 2

### 3

### 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2Fyb3VzZWwgaW5kaWNhdG9yLXBvc2l0aW9uPVwib3V0c2lkZVwiPlxuICAgIDxlbC1jYXJvdXNlbC1pdGVtIHYtZm9yPVwiaXRlbSBpbiA0XCIgOmtleT1cIml0ZW1cIj5cbiAgICAgIDxoMyB0ZXh0PVwiMnhsXCIganVzdGlmeT1cImNlbnRlclwiPnt7IGl0ZW0gfX08L2gzPlxuICAgIDwvZWwtY2Fyb3VzZWwtaXRlbT5cbiAgPC9lbC1jYXJvdXNlbD5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZWwtY2Fyb3VzZWxfX2l0ZW0gaDMge1xuICBkaXNwbGF5OiBmbGV4O1xuICBjb2xvcjogIzQ3NTY2OTtcbiAgb3BhY2l0eTogMC43NTtcbiAgbGluZS1oZWlnaHQ6IDMwMHB4O1xuICBtYXJnaW46IDA7XG59XG5cbi5lbC1jYXJvdXNlbF9faXRlbTpudGgtY2hpbGQoMm4pIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogIzk5YTliZjtcbn1cblxuLmVsLWNhcm91c2VsX19pdGVtOm50aC1jaGlsZCgybiArIDEpIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogI2QzZGNlNjtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/carousel/indicator.vue)_

vue

```
<template>
  <el-carousel indicator-position="outside">
    <el-carousel-item v-for="item in 4" :key="item">
      <h3 text="2xl" justify="center">{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.el-carousel__item h3 {
  display: flex;
  color: #475669;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

隐藏源代码

## 切换箭头 [​](#切换箭头)

可以设置切换箭头的显示时机

`arrow` 属性定义了切换箭头的显示时机。 默认情况下，切换箭头只有在鼠标 hover 到走马灯上时才会显示。 若将 `arrow` 设置为 `always`，则会一直显示；设置为 `never`，则会一直隐藏。

### 1

### 2

### 3

### 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2Fyb3VzZWwgOmludGVydmFsPVwiNTAwMFwiIGFycm93PVwiYWx3YXlzXCI+XG4gICAgPGVsLWNhcm91c2VsLWl0ZW0gdi1mb3I9XCJpdGVtIGluIDRcIiA6a2V5PVwiaXRlbVwiPlxuICAgICAgPGgzIHRleHQ9XCIyeGxcIiBqdXN0aWZ5PVwiY2VudGVyXCI+e3sgaXRlbSB9fTwvaDM+XG4gICAgPC9lbC1jYXJvdXNlbC1pdGVtPlxuICA8L2VsLWNhcm91c2VsPlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlIHNjb3BlZD5cbi5lbC1jYXJvdXNlbF9faXRlbSBoMyB7XG4gIGNvbG9yOiAjNDc1NjY5O1xuICBvcGFjaXR5OiAwLjc1O1xuICBsaW5lLWhlaWdodDogMzAwcHg7XG4gIG1hcmdpbjogMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xufVxuXG4uZWwtY2Fyb3VzZWxfX2l0ZW06bnRoLWNoaWxkKDJuKSB7XG4gIGJhY2tncm91bmQtY29sb3I6ICM5OWE5YmY7XG59XG5cbi5lbC1jYXJvdXNlbF9faXRlbTpudGgtY2hpbGQoMm4gKyAxKSB7XG4gIGJhY2tncm91bmQtY29sb3I6ICNkM2RjZTY7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/carousel/arrows.vue)_

vue

```
<template>
  <el-carousel :interval="5000" arrow="always">
    <el-carousel-item v-for="item in 4" :key="item">
      <h3 text="2xl" justify="center">{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

隐藏源代码

## 自动高度 [​](#自动高度)

当 `carousel` 的 `height` 设置为 `auto`时， `carousel` 的高度将根据子内容的高度自动设置

each carousel-item has a different height

### height 100px

### height 200px

### height 300px

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiYmxvY2sgdGV4dC1jZW50ZXJcIiBzdHlsZT1cImhlaWdodDogMzAwcHhcIj5cbiAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5lYWNoIGNhcm91c2VsLWl0ZW0gaGFzIGEgZGlmZmVyZW50IGhlaWdodDwvc3Bhbj5cbiAgICA8ZWwtY2Fyb3VzZWwgaGVpZ2h0PVwiYXV0b1wiIGF1dG9wbGF5PlxuICAgICAgPGVsLWNhcm91c2VsLWl0ZW0gc3R5bGU9XCJoZWlnaHQ6IDEwMHB4XCI+XG4gICAgICAgIDxoMyBjbGFzcz1cInNtYWxsIGp1c3RpZnktY2VudGVyXCIgdGV4dD1cIjJ4bFwiPmhlaWdodCAxMDBweDwvaDM+XG4gICAgICA8L2VsLWNhcm91c2VsLWl0ZW0+XG4gICAgICA8ZWwtY2Fyb3VzZWwtaXRlbSBzdHlsZT1cImhlaWdodDogMjAwcHhcIj5cbiAgICAgICAgPGgzIGNsYXNzPVwic21hbGwganVzdGlmeS1jZW50ZXJcIiB0ZXh0PVwiMnhsXCI+aGVpZ2h0IDIwMHB4PC9oMz5cbiAgICAgIDwvZWwtY2Fyb3VzZWwtaXRlbT5cbiAgICAgIDxlbC1jYXJvdXNlbC1pdGVtIHN0eWxlPVwiaGVpZ2h0OiAzMDBweFwiPlxuICAgICAgICA8aDMgY2xhc3M9XCJzbWFsbCBqdXN0aWZ5LWNlbnRlclwiIHRleHQ9XCIyeGxcIj5oZWlnaHQgMzAwcHg8L2gzPlxuICAgICAgPC9lbC1jYXJvdXNlbC1pdGVtPlxuICAgIDwvZWwtY2Fyb3VzZWw+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlIHNjb3BlZD5cbi5jYXJvdXNlbC1pdGVtIHtcbiAgY29sb3I6ICM0NzU2Njk7XG4gIG9wYWNpdHk6IDAuNzU7XG4gIG1hcmdpbjogMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xufVxuXG4uZWwtY2Fyb3VzZWxfX2l0ZW0gaDMge1xuICBjb2xvcjogIzQ3NTY2OTtcbiAgb3BhY2l0eTogMC43NTtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAgbWFyZ2luOiAwO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGhlaWdodDogMTAwJTtcbn1cblxuLmVsLWNhcm91c2VsX19pdGVtOm50aC1jaGlsZCgybikge1xuICBiYWNrZ3JvdW5kLWNvbG9yOiAjOTlhOWJmO1xufVxuXG4uZWwtY2Fyb3VzZWxfX2l0ZW06bnRoLWNoaWxkKDJuICsgMSkge1xuICBiYWNrZ3JvdW5kLWNvbG9yOiAjZDNkY2U2O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/carousel/auto-height.vue)_

vue

```
<template>
  <div class="block text-center" style="height: 300px">
    <span class="demonstration">each carousel-item has a different height</span>
    <el-carousel height="auto" autoplay>
      <el-carousel-item style="height: 100px">
        <h3 class="small justify-center" text="2xl">height 100px</h3>
      </el-carousel-item>
      <el-carousel-item style="height: 200px">
        <h3 class="small justify-center" text="2xl">height 200px</h3>
      </el-carousel-item>
      <el-carousel-item style="height: 300px">
        <h3 class="small justify-center" text="2xl">height 300px</h3>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<style scoped>
.carousel-item {
  color: #475669;
  opacity: 0.75;
  margin: 0;
  text-align: center;
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  display: flex;
  align-items: center;
  margin: 0;
  text-align: center;
  height: 100%;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

隐藏源代码

## 卡片模式 [​](#卡片模式)

当页面宽度方向空间空余，但高度方向空间匮乏时，可使用卡片风格

将 `type` 属性设置为 `card` 即可启用卡片模式。 从交互上来说，卡片模式和一般模式的最大区别在于，卡片模式可以通过直接点击两侧的幻灯片进行切换。

### 1

### 2

### 3

### 4

### 5

### 6

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2Fyb3VzZWwgOmludGVydmFsPVwiNDAwMFwiIHR5cGU9XCJjYXJkXCIgaGVpZ2h0PVwiMjAwcHhcIj5cbiAgICA8ZWwtY2Fyb3VzZWwtaXRlbSB2LWZvcj1cIml0ZW0gaW4gNlwiIDprZXk9XCJpdGVtXCI+XG4gICAgICA8aDMgdGV4dD1cIjJ4bFwiIGp1c3RpZnk9XCJjZW50ZXJcIj57eyBpdGVtIH19PC9oMz5cbiAgICA8L2VsLWNhcm91c2VsLWl0ZW0+XG4gIDwvZWwtY2Fyb3VzZWw+XG48L3RlbXBsYXRlPlxuXG48c3R5bGUgc2NvcGVkPlxuLmVsLWNhcm91c2VsX19pdGVtIGgzIHtcbiAgY29sb3I6ICM0NzU2Njk7XG4gIG9wYWNpdHk6IDAuNzU7XG4gIGxpbmUtaGVpZ2h0OiAyMDBweDtcbiAgbWFyZ2luOiAwO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG59XG5cbi5lbC1jYXJvdXNlbF9faXRlbTpudGgtY2hpbGQoMm4pIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogIzk5YTliZjtcbn1cblxuLmVsLWNhcm91c2VsX19pdGVtOm50aC1jaGlsZCgybiArIDEpIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogI2QzZGNlNjtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/carousel/card.vue)_

vue

```
<template>
  <el-carousel :interval="4000" type="card" height="200px">
    <el-carousel-item v-for="item in 6" :key="item">
      <h3 text="2xl" justify="center">{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

隐藏源代码

## 垂直排列 [​](#垂直排列)

默认情况下，方向 `direction` 为 水平 `horizontal`。 通过设置 `direction` 为 `vertical` 来让走马灯在垂直方向上显示。

normal vertical layout

### 1

### 2

### 3

### 4

card vertical layout

### 1

### 2

### 3

### 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8cCBjbGFzcz1cInRleHQtY2VudGVyIGRlbW9uc3RyYXRpb25cIj5ub3JtYWwgdmVydGljYWwgbGF5b3V0PC9wPlxuICA8ZWwtY2Fyb3VzZWwgaGVpZ2h0PVwiMjAwcHhcIiBkaXJlY3Rpb249XCJ2ZXJ0aWNhbFwiIDphdXRvcGxheT1cImZhbHNlXCI+XG4gICAgPGVsLWNhcm91c2VsLWl0ZW0gdi1mb3I9XCJpdGVtIGluIDRcIiA6a2V5PVwiaXRlbVwiPlxuICAgICAgPGgzIHRleHQ9XCIyeGxcIiBqdXN0aWZ5PVwiY2VudGVyXCI+e3sgaXRlbSB9fTwvaDM+XG4gICAgPC9lbC1jYXJvdXNlbC1pdGVtPlxuICA8L2VsLWNhcm91c2VsPlxuICA8cCBjbGFzcz1cInRleHQtY2VudGVyIGRlbW9uc3RyYXRpb25cIj5jYXJkIHZlcnRpY2FsIGxheW91dDwvcD5cbiAgPGVsLWNhcm91c2VsXG4gICAgaGVpZ2h0PVwiNDAwcHhcIlxuICAgIGRpcmVjdGlvbj1cInZlcnRpY2FsXCJcbiAgICB0eXBlPVwiY2FyZFwiXG4gICAgOmF1dG9wbGF5PVwiZmFsc2VcIlxuICA+XG4gICAgPGVsLWNhcm91c2VsLWl0ZW0gdi1mb3I9XCJpdGVtIGluIDRcIiA6a2V5PVwiaXRlbVwiPlxuICAgICAgPGgzIHRleHQ9XCIyeGxcIiBqdXN0aWZ5PVwiY2VudGVyXCI+e3sgaXRlbSB9fTwvaDM+XG4gICAgPC9lbC1jYXJvdXNlbC1pdGVtPlxuICA8L2VsLWNhcm91c2VsPlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlIHNjb3BlZD5cbi5lbC1jYXJvdXNlbF9faXRlbSBoMyB7XG4gIGNvbG9yOiAjNDc1NjY5O1xuICBvcGFjaXR5OiAwLjc1O1xuICBsaW5lLWhlaWdodDogMjAwcHg7XG4gIG1hcmdpbjogMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xufVxuXG4uZWwtY2Fyb3VzZWxfX2l0ZW06bnRoLWNoaWxkKDJuKSB7XG4gIGJhY2tncm91bmQtY29sb3I6ICM5OWE5YmY7XG59XG5cbi5lbC1jYXJvdXNlbF9faXRlbTpudGgtY2hpbGQoMm4gKyAxKSB7XG4gIGJhY2tncm91bmQtY29sb3I6ICNkM2RjZTY7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/carousel/vertical.vue)_

vue

```
<template>
  <p class="text-center demonstration">normal vertical layout</p>
  <el-carousel height="200px" direction="vertical" :autoplay="false">
    <el-carousel-item v-for="item in 4" :key="item">
      <h3 text="2xl" justify="center">{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>
  <p class="text-center demonstration">card vertical layout</p>
  <el-carousel
    height="400px"
    direction="vertical"
    type="card"
    :autoplay="false"
  >
    <el-carousel-item v-for="item in 4" :key="item">
      <h3 text="2xl" justify="center">{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

隐藏源代码

## Carousel API [​](#carousel-api)

### Carousel Attributes [​](#carousel-attributes)

| 属性名 | 说明 | 类型 | Default |
| --- | --- | --- | --- |
| height | carousel 的高度 | `string` | '' |
| initial-index | 初始状态激活的幻灯片的索引，从 0 开始 | `number` | 0 |
| trigger | 指示器的触发方式 | `enum` | hover |
| autoplay | 是否自动切换 | `boolean` | true |
| interval | 自动切换的时间间隔，单位为毫秒 | `number` | 3000 |
| indicator-position | 指示器的位置 | `enum` | '' |
| arrow | 切换箭头的显示时机 | `enum` | hover |
| type | carousel 的类型 | `enum` | '' |
| card-scale 2.7.8 | 当 type 为 card时，二级卡的缩放大小 | `number` | 0.83 |
| loop | 是否循环显示 | `boolean` | true |
| direction | 展示的方向 | `enum` | horizontal |
| pause-on-hover | 鼠标悬浮时暂停自动切换 | `boolean` | true |
| motion-blur 2.6.0 | 添加动态模糊以给走马灯注入活力和流畅性。 | `boolean` | false |

### Carousel Events [​](#carousel-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当前展示的幻灯片切换时触发，它有两个参数， 一个是新幻灯片的索引，另一个是旧幻灯片的索引 | `Function` |

### Carousel Slots [​](#carousel-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | Carousel-Item |

### Carousel Exposes [​](#carousel-exposes)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| activeIndex 2.7.8 | 当前幻灯片的索引 | `number` |
| setActiveItem | 手动切换幻灯片，传入需要切换的幻灯片的索引，从 0 开始；或相应 `el-carousel-item` 的 `name` 属性值 | `Function` |
| prev | 切换至上一张幻灯片 | `Function` |
| next | 切换至下一张幻灯片 | `Function` |

## Carousel-Item API [​](#carousel-item-api)

### Carousel-Item Attributes [​](#carousel-item-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| name | 幻灯片的名字，可用作 `setActiveItem` 的参数 | `string` | '' |
| label | 该幻灯片所对应指示器的文本 | `string` / `number` | '' |

### Carousel-Item Slots [​](#carousel-item-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/carousel) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/carousel.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/carousel.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/69580637?v=4&size=64)](https://github.com/jevin98)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/78132554?v=4&size=64)](https://github.com/momei-LJM)[![](https://avatars.githubusercontent.com/u/26403700?v=4&size=64)](https://github.com/blesstosam)[![](https://avatars.githubusercontent.com/u/44160015?v=4&size=64)](https://github.com/JedediahXu)[![](https://avatars.githubusercontent.com/u/31238760?v=4&size=64)](https://github.com/cloydlau)[![](https://avatars.githubusercontent.com/u/102006695?v=4&size=64)](https://github.com/cuongle-hdwebsoft)[![](https://avatars.githubusercontent.com/u/30046649?v=4&size=64)](https://github.com/MrWeilian)[![](https://avatars.githubusercontent.com/u/73547598?v=4&size=64)](https://github.com/SaberA1ter)[![](https://avatars.githubusercontent.com/u/26755049?v=4&size=64)](https://github.com/qq282126990)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/39959340?v=4&size=64)](https://github.com/yonghui-wang)[![](https://avatars.githubusercontent.com/u/134276765?v=4&size=64)](https://github.com/zwgwf)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/45936772?v=4&size=64)](https://github.com/KawaiiZapic)[![](https://avatars.githubusercontent.com/u/2755933?v=4&size=64)](https://github.com/BiosSun)[![](https://avatars.githubusercontent.com/u/36007710?v=4&size=64)](https://github.com/sleepyfive)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/33687038?v=4&size=64)](https://github.com/guozi9999)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)

[Card 卡片](https://element-plus.org/zh-CN/component/card)

[Collapse 折叠面板](https://element-plus.org/zh-CN/component/collapse)


