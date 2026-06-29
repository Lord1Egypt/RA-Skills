---
name: "avatar"
description: "Avatar 头像 -- Element Plus Vue3 桌面端组件。Invoke when user needs Avatar 头像 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/avatar.html"
---

---

# Avatar 头像 [​](#avatar-头像)

更新日志待解决

0

Avatar 组件可以用来代表人物或对象， 支持使用图片、图标或者文字作为 Avatar。

## 基础用法 [​](#基础用法)

使用 `shape` 和 `size` 属性来设置 Avatar 的形状和大小。

circle

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)

square

![](https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png)

![](https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png)

![](https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png)

![](https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IGNsYXNzPVwiZGVtby1hdmF0YXIgZGVtby1iYXNpY1wiPlxuICAgIDxlbC1jb2wgOmxnPVwiMTJcIiA6bWQ9XCIxMlwiPlxuICAgICAgPGRpdiBjbGFzcz1cInN1Yi10aXRsZVwiPmNpcmNsZTwvZGl2PlxuICAgICAgPGRpdiBjbGFzcz1cImRlbW8tYmFzaWMtLWNpcmNsZVwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgICAgICA8ZWwtYXZhdGFyIDpzaXplPVwiNTBcIiA6c3JjPVwiY2lyY2xlVXJsXCIgLz5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgdi1mb3I9XCJzaXplIGluIHNpemVMaXN0XCIgOmtleT1cInNpemVcIiBjbGFzcz1cImJsb2NrXCI+XG4gICAgICAgICAgPGVsLWF2YXRhciA6c2l6ZT1cInNpemVcIiA6c3JjPVwiY2lyY2xlVXJsXCIgLz5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpsZz1cIjEyXCIgOm1kPVwiMTJcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJzdWItdGl0bGVcIj5zcXVhcmU8L2Rpdj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkZW1vLWJhc2ljLS1jaXJjbGVcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImJsb2NrXCI+XG4gICAgICAgICAgPGVsLWF2YXRhciBzaGFwZT1cInNxdWFyZVwiIDpzaXplPVwiNTBcIiA6c3JjPVwic3F1YXJlVXJsXCIgLz5cbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXYgdi1mb3I9XCJzaXplIGluIHNpemVMaXN0XCIgOmtleT1cInNpemVcIiBjbGFzcz1cImJsb2NrXCI+XG4gICAgICAgICAgPGVsLWF2YXRhciBzaGFwZT1cInNxdWFyZVwiIDpzaXplPVwic2l6ZVwiIDpzcmM9XCJzcXVhcmVVcmxcIiAvPlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZWwtY29sPlxuICA8L2VsLXJvdz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWFjdGl2ZSwgdG9SZWZzIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBzdGF0ZSA9IHJlYWN0aXZlKHtcbiAgY2lyY2xlVXJsOlxuICAgICdodHRwczovL2N1YmUuZWxlbWVjZG4uY29tLzMvN2MvM2VhNmJlZWM2NDM2OWMyNjQyYjkyYzY3MjZmMWVwbmcucG5nJyxcbiAgc3F1YXJlVXJsOlxuICAgICdodHRwczovL2N1YmUuZWxlbWVjZG4uY29tLzkvYzIvZjBlZThhM2M3Yzk2MzhhNTQ5NDAzODI1NjhjOWRwbmcucG5nJyxcbiAgc2l6ZUxpc3Q6IFsnc21hbGwnLCAnJywgJ2xhcmdlJ10gYXMgY29uc3QsXG59KVxuXG5jb25zdCB7IGNpcmNsZVVybCwgc3F1YXJlVXJsLCBzaXplTGlzdCB9ID0gdG9SZWZzKHN0YXRlKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1iYXNpYyB7XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbn1cbi5kZW1vLWJhc2ljIC5zdWItdGl0bGUge1xuICBtYXJnaW4tYm90dG9tOiAxMHB4O1xuICBmb250LXNpemU6IDE0cHg7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG59XG4uZGVtby1iYXNpYyAuZGVtby1iYXNpYy0tY2lyY2xlLFxuLmRlbW8tYmFzaWMgLmRlbW8tYmFzaWMtLXNxdWFyZSB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGp1c3RpZnktY29udGVudDogc3BhY2UtYmV0d2VlbjtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cbi5kZW1vLWJhc2ljIC5ibG9jazpub3QoOmxhc3QtY2hpbGQpIHtcbiAgYm9yZGVyLXJpZ2h0OiAxcHggc29saWQgdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbn1cbi5kZW1vLWJhc2ljIC5ibG9jayB7XG4gIGZsZXg6IDE7XG59XG4uZGVtby1iYXNpYyAuZWwtY29sOm5vdCg6bGFzdC1jaGlsZCkge1xuICBib3JkZXItcmlnaHQ6IDFweCBzb2xpZCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xufVxuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogOTkycHgpIHtcbiAgLmRlbW8tYmFzaWMgLmVsLWNvbDpub3QoOmxhc3QtY2hpbGQpIHtcbiAgICBib3JkZXItcmlnaHQ6IG5vbmU7XG4gIH1cbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/avatar/basic.vue)_

vue

```
<template>
  <el-row class="demo-avatar demo-basic">
    <el-col :lg="12" :md="12">
      <div class="sub-title">circle</div>
      <div class="demo-basic--circle">
        <div class="block">
          <el-avatar :size="50" :src="circleUrl" />
        </div>
        <div v-for="size in sizeList" :key="size" class="block">
          <el-avatar :size="size" :src="circleUrl" />
        </div>
      </div>
    </el-col>
    <el-col :lg="12" :md="12">
      <div class="sub-title">square</div>
      <div class="demo-basic--circle">
        <div class="block">
          <el-avatar shape="square" :size="50" :src="squareUrl" />
        </div>
        <div v-for="size in sizeList" :key="size" class="block">
          <el-avatar shape="square" :size="size" :src="squareUrl" />
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { reactive, toRefs } from 'vue'

const state = reactive({
  circleUrl:
    'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
  squareUrl:
    'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
  sizeList: ['small', '', 'large'] as const,
})

const { circleUrl, squareUrl, sizeList } = toRefs(state)
</script>

<style scoped>
.demo-basic {
  text-align: center;
}
.demo-basic .sub-title {
  margin-bottom: 10px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
.demo-basic .demo-basic--circle,
.demo-basic .demo-basic--square {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.demo-basic .block:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}
.demo-basic .block {
  flex: 1;
}
.demo-basic .el-col:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}
@media screen and (max-width: 992px) {
  .demo-basic .el-col:not(:last-child) {
    border-right: none;
  }
}
</style>
```

隐藏源代码

## 展示类型 [​](#展示类型)

支持使用图片，图标或者文字作为 Avatar。

![](https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png)

user

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby10eXBlXCI+XG4gICAgPGRpdj5cbiAgICAgIDxlbC1hdmF0YXIgOmljb249XCJVc2VyRmlsbGVkXCIgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2PlxuICAgICAgPGVsLWF2YXRhclxuICAgICAgICBzcmM9XCJodHRwczovL2N1YmUuZWxlbWVjZG4uY29tLzAvODgvMDNiMGQzOTU4M2Y0ODIwNjc2OGE3NTM0ZTU1YmNwbmcucG5nXCJcbiAgICAgIC8+XG4gICAgPC9kaXY+XG4gICAgPGRpdj5cbiAgICAgIDxlbC1hdmF0YXI+IHVzZXIgPC9lbC1hdmF0YXI+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IFVzZXJGaWxsZWQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tdHlwZSB7XG4gIGRpc3BsYXk6IGZsZXg7XG59XG4uZGVtby10eXBlID4gZGl2IHtcbiAgZmxleDogMTtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xufVxuXG4uZGVtby10eXBlID4gZGl2Om5vdCg6bGFzdC1jaGlsZCkge1xuICBib3JkZXItcmlnaHQ6IDFweCBzb2xpZCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/avatar/types.vue)_

vue

```
<template>
  <div class="demo-type">
    <div>
      <el-avatar :icon="UserFilled" />
    </div>
    <div>
      <el-avatar
        src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
      />
    </div>
    <div>
      <el-avatar> user </el-avatar>
    </div>
  </div>
</template>

<script setup lang="ts">
import { UserFilled } from '@element-plus/icons-vue'
</script>

<style scoped>
.demo-type {
  display: flex;
}
.demo-type > div {
  flex: 1;
  text-align: center;
}

.demo-type > div:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}
</style>
```

隐藏源代码

## 回退行为 [​](#回退行为)

图片加载失败时的回退行为。

![](https://empty/)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby10eXBlXCI+XG4gICAgPGVsLWF2YXRhciA6c2l6ZT1cIjYwXCIgc3JjPVwiaHR0cHM6Ly9lbXB0eVwiIEBlcnJvcj1cImVycm9ySGFuZGxlclwiPlxuICAgICAgPGltZ1xuICAgICAgICBzcmM9XCJodHRwczovL2N1YmUuZWxlbWVjZG4uY29tL2UvZmQvMGZjN2QyMDUzMmZkYWY3NjlhMjU2ODM2MTc3MTFwbmcucG5nXCJcbiAgICAgIC8+XG4gICAgPC9lbC1hdmF0YXI+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IGVycm9ySGFuZGxlciA9ICgpID0+IHRydWVcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/avatar/fallback.vue)_

vue

```
<template>
  <div class="demo-type">
    <el-avatar :size="60" src="https://empty" @error="errorHandler">
      <img
        src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"
      />
    </el-avatar>
  </div>
</template>

<script lang="ts" setup>
const errorHandler = () => true
</script>
```

隐藏源代码

## 适应容器 [​](#适应容器)

当使用图片作为用户头像时，设置该图片如何在容器中展示。与 [object-fit](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit) 属性一致

fill![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

contain![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

cover![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

none![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

scale-down![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1maXRcIj5cbiAgICA8ZGl2IHYtZm9yPVwiZml0IGluIGZpdHNcIiA6a2V5PVwiZml0XCIgY2xhc3M9XCJibG9ja1wiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJ0aXRsZVwiPnt7IGZpdCB9fTwvc3Bhbj5cbiAgICAgIDxlbC1hdmF0YXIgc2hhcGU9XCJzcXVhcmVcIiA6c2l6ZT1cIjEwMFwiIDpmaXQ9XCJmaXRcIiA6c3JjPVwidXJsXCIgLz5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVhY3RpdmUsIHRvUmVmcyB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBDU1NQcm9wZXJ0aWVzIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBzdGF0ZSA9IHJlYWN0aXZlKHtcbiAgZml0czogW1xuICAgICdmaWxsJyxcbiAgICAnY29udGFpbicsXG4gICAgJ2NvdmVyJyxcbiAgICAnbm9uZScsXG4gICAgJ3NjYWxlLWRvd24nLFxuICBdIGFzIENTU1Byb3BlcnRpZXNbJ29iamVjdC1maXQnXVtdLFxuICB1cmw6ICdodHRwczovL2Z1c3MxMC5lbGVtZWNkbi5jb20vZS81ZC80YTczMWE5MDU5NGE0YWY1NDRjMGMyNTk0MTE3MWpwZWcuanBlZycsXG59KVxuXG5jb25zdCB7IGZpdHMsIHVybCB9ID0gdG9SZWZzKHN0YXRlKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1maXQge1xuICBkaXNwbGF5OiBmbGV4O1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGp1c3RpZnktY29udGVudDogc3BhY2UtYmV0d2Vlbjtcbn1cbi5kZW1vLWZpdCAuYmxvY2sge1xuICBmbGV4OiAxO1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBmbGV4LWdyb3c6IDA7XG59XG5cbi5kZW1vLWZpdCAudGl0bGUge1xuICBtYXJnaW4tYm90dG9tOiAxMHB4O1xuICBmb250LXNpemU6IDE0cHg7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/avatar/fit.vue)_

vue

```
<template>
  <div class="demo-fit">
    <div v-for="fit in fits" :key="fit" class="block">
      <span class="title">{{ fit }}</span>
      <el-avatar shape="square" :size="100" :fit="fit" :src="url" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, toRefs } from 'vue'

import type { CSSProperties } from 'vue'

const state = reactive({
  fits: [
    'fill',
    'contain',
    'cover',
    'none',
    'scale-down',
  ] as CSSProperties['object-fit'][],
  url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
})

const { fits, url } = toRefs(state)
</script>

<style scoped>
.demo-fit {
  display: flex;
  text-align: center;
  justify-content: space-between;
}
.demo-fit .block {
  flex: 1;
  display: flex;
  flex-direction: column;
  flex-grow: 0;
}

.demo-fit .title {
  margin-bottom: 10px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
</style>
```

隐藏源代码

## 头像组 2.13.1 [​](#头像组)

显示为头像组

使用标签 `<el-avatar-group>` 来分组您的头像。

default

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)

use collapse-avatars

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)\+ 4

use collapse-class and collapse-style

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)\+ 4

use max-collapse-avatars

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)\+ 2

use collapse-avatars-tooltip

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)\+ 2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+ZGVmYXVsdDwvcD5cbiAgICA8ZWwtYXZhdGFyLWdyb3VwPlxuICAgICAgPGVsLWF2YXRhciB2LWZvcj1cIm51bWJlciBpbiA1XCIgOmtleT1cIm51bWJlclwiIDpzcmM9XCJjaXJjbGVVcmxcIiAvPlxuICAgIDwvZWwtYXZhdGFyLWdyb3VwPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cIm0tNFwiPlxuICAgIDxwPnVzZSBjb2xsYXBzZS1hdmF0YXJzPC9wPlxuICAgIDxlbC1hdmF0YXItZ3JvdXAgY29sbGFwc2UtYXZhdGFycz5cbiAgICAgIDxlbC1hdmF0YXIgdi1mb3I9XCJudW1iZXIgaW4gNVwiIDprZXk9XCJudW1iZXJcIiA6c3JjPVwiY2lyY2xlVXJsXCIgLz5cbiAgICA8L2VsLWF2YXRhci1ncm91cD5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJtLTRcIj5cbiAgICA8cD51c2UgY29sbGFwc2UtY2xhc3MgYW5kIGNvbGxhcHNlLXN0eWxlPC9wPlxuICAgIDxlbC1hdmF0YXItZ3JvdXBcbiAgICAgIGNvbGxhcHNlLWF2YXRhcnNcbiAgICAgIDpjb2xsYXBzZS1zdHlsZT1cInsgJ2JhY2tncm91bmQtY29sb3InOiAnI2Q5ZWNmZicgfVwiXG4gICAgICBjb2xsYXBzZS1jbGFzcz1cIm15LWNvbGxhcHNlLWF2YXRhclwiXG4gICAgPlxuICAgICAgPGVsLWF2YXRhciB2LWZvcj1cIm51bWJlciBpbiA1XCIgOmtleT1cIm51bWJlclwiIDpzcmM9XCJjaXJjbGVVcmxcIiAvPlxuICAgIDwvZWwtYXZhdGFyLWdyb3VwPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cIm0tNFwiPlxuICAgIDxwPnVzZSBtYXgtY29sbGFwc2UtYXZhdGFyczwvcD5cbiAgICA8ZWwtYXZhdGFyLWdyb3VwIGNvbGxhcHNlLWF2YXRhcnMgOm1heC1jb2xsYXBzZS1hdmF0YXJzPVwiM1wiPlxuICAgICAgPGVsLWF2YXRhciB2LWZvcj1cIm51bWJlciBpbiA1XCIgOmtleT1cIm51bWJlclwiIDpzcmM9XCJjaXJjbGVVcmxcIiAvPlxuICAgIDwvZWwtYXZhdGFyLWdyb3VwPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cIm0tNFwiPlxuICAgIDxwPnVzZSBjb2xsYXBzZS1hdmF0YXJzLXRvb2x0aXA8L3A+XG4gICAgPGVsLWF2YXRhci1ncm91cFxuICAgICAgY29sbGFwc2UtYXZhdGFyc1xuICAgICAgOm1heC1jb2xsYXBzZS1hdmF0YXJzPVwiM1wiXG4gICAgICBjb2xsYXBzZS1hdmF0YXJzLXRvb2x0aXBcbiAgICA+XG4gICAgICA8ZWwtYXZhdGFyIHYtZm9yPVwibnVtYmVyIGluIDVcIiA6a2V5PVwibnVtYmVyXCIgOnNyYz1cImNpcmNsZVVybFwiIC8+XG4gICAgPC9lbC1hdmF0YXItZ3JvdXA+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IGNpcmNsZVVybCA9XG4gICdodHRwczovL2N1YmUuZWxlbWVjZG4uY29tLzMvN2MvM2VhNmJlZWM2NDM2OWMyNjQyYjkyYzY3MjZmMWVwbmcucG5nJ1xuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5teS1jb2xsYXBzZS1hdmF0YXIge1xuICBjb2xvcjogIzQwOWVmZjtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/avatar/group.vue)_

vue

```
<template>
  <div class="m-4">
    <p>default</p>
    <el-avatar-group>
      <el-avatar v-for="number in 5" :key="number" :src="circleUrl" />
    </el-avatar-group>
  </div>
  <div class="m-4">
    <p>use collapse-avatars</p>
    <el-avatar-group collapse-avatars>
      <el-avatar v-for="number in 5" :key="number" :src="circleUrl" />
    </el-avatar-group>
  </div>
  <div class="m-4">
    <p>use collapse-class and collapse-style</p>
    <el-avatar-group
      collapse-avatars
      :collapse-style="{ 'background-color': '#d9ecff' }"
      collapse-class="my-collapse-avatar"
    >
      <el-avatar v-for="number in 5" :key="number" :src="circleUrl" />
    </el-avatar-group>
  </div>
  <div class="m-4">
    <p>use max-collapse-avatars</p>
    <el-avatar-group collapse-avatars :max-collapse-avatars="3">
      <el-avatar v-for="number in 5" :key="number" :src="circleUrl" />
    </el-avatar-group>
  </div>
  <div class="m-4">
    <p>use collapse-avatars-tooltip</p>
    <el-avatar-group
      collapse-avatars
      :max-collapse-avatars="3"
      collapse-avatars-tooltip
    >
      <el-avatar v-for="number in 5" :key="number" :src="circleUrl" />
    </el-avatar-group>
  </div>
</template>

<script lang="ts" setup>
const circleUrl =
  'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
</script>

<style>
.my-collapse-avatar {
  color: #409eff;
}
</style>
```

隐藏源代码

## Avatar API [​](#avatar-api)

### Avatar 属性 [​](#avatar-属性)

| 名称 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| icon | 设置 Avatar 的图标类型，具体参考 Icon 组件 | `string` / `Component` | — |
| size | Avatar 大小 | `number` / `enum` | — |
| shape | Avatar 形状 | `enum` | — |
| src | Avatar 图片的源地址 | `string` | — |
| src-set | 图片 Avatar 的原生 `srcset` 属性 | `string` | string |
| alt | 图片 Avatar 的原生 `alt` 属性 | `string` | — |
| fit | 当展示类型为图片的时候，设置图片如何适应容器 | `enum` | cover |

### Avatar 事件 [​](#avatar-事件)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| error | 图片加载失败时触发 | `Function` |

### Avatar 插槽 [​](#avatar-插槽)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义头像展示内容 |

## AvatarGroup API 2.13.1 [​](#avatargroup-api)

### AvatarGroup Attributes [​](#avatargroup-attributes)

| 方法名 | 详情 | Type | 默认 |
| --- | --- | --- | --- |
| size | 控制头像组中的头像大小 | `number` / `enum` | — |
| shape | 控制头像组中的头像形状 | `enum` | — |
| collapse-avatars | 是否折叠头像 | `boolean` | false |
| collapse-avatars-tooltip | 是否在鼠标悬停折叠头像的文字时显示所有折叠头像。 若要使用此功能， `collapse-avatars` 必须为 true | `boolean` | false |
| max-collapse-avatars | 需要显示的头像的最大数量 若要使用此功能， `collapse-avatars` 必须为 true | `number` | 1 |
| effect | tooltip 主题，内置了 `dark` / `light` 两种 | `enum` / `string` | light |
| placement | tooltip 的位置 | `enum` | top |
| popper-class | tooltip 的自定义类名 | `string` | '' |
| popper-style | tooltip 的自定义样式 | `string` / `object` | — |
| collapse-class | collapse-avatar 的自定义类名 | `string` | '' |
| collapse-style | collapse-avatar 的自定义样式 | `string` / `object` | — |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/avatar) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/avatar.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/avatar.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)[![](https://avatars.githubusercontent.com/u/49899455?v=4&size=64)](https://github.com/zhuige)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/75007029?v=4&size=64)](https://github.com/yj-liuzepeng)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)

[Upload 上传器](https://element-plus.org/zh-CN/component/upload)

[Badge 徽章](https://element-plus.org/zh-CN/component/badge)


