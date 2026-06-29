---
name: "image"
description: "Image 图片 -- Element Plus Vue3 桌面端组件。Invoke when user needs Image 图片 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/image.html"
---

---

# Image 图片 [​](#image-图片)

更新日志待解决

5

图片容器，在保留所有原生 img 的特性下，支持懒加载，自定义占位、加载失败等

## 基础用法 [​](#基础用法)

可通过`fit`确定图片如何适应到容器框，同原生 [object-fit](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit)。

fill

![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

contain

![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

cover

![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

none

![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

scale-down

![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbWFnZVwiPlxuICAgIDxkaXYgdi1mb3I9XCJmaXQgaW4gZml0c1wiIDprZXk9XCJmaXRcIiBjbGFzcz1cImJsb2NrXCI+XG4gICAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj57eyBmaXQgfX08L3NwYW4+XG4gICAgICA8ZWwtaW1hZ2Ugc3R5bGU9XCJ3aWR0aDogMTAwcHg7IGhlaWdodDogMTAwcHhcIiA6c3JjPVwidXJsXCIgOmZpdD1cImZpdFwiIC8+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB0eXBlIHsgSW1hZ2VQcm9wcyB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgZml0cyA9IFtcbiAgJ2ZpbGwnLFxuICAnY29udGFpbicsXG4gICdjb3ZlcicsXG4gICdub25lJyxcbiAgJ3NjYWxlLWRvd24nLFxuXSBhcyBJbWFnZVByb3BzWydmaXQnXVtdXG5jb25zdCB1cmwgPVxuICAnaHR0cHM6Ly9mdXNzMTAuZWxlbWVjZG4uY29tL2UvNWQvNGE3MzFhOTA1OTRhNGFmNTQ0YzBjMjU5NDExNzFqcGVnLmpwZWcnXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLWltYWdlIC5ibG9jayB7XG4gIHBhZGRpbmc6IDMwcHggMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBib3JkZXItcmlnaHQ6IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICBkaXNwbGF5OiBpbmxpbmUtYmxvY2s7XG4gIHdpZHRoOiAyMCU7XG4gIG1pbi13aWR0aDogMTAwcHg7XG4gIGJveC1zaXppbmc6IGJvcmRlci1ib3g7XG4gIHZlcnRpY2FsLWFsaWduOiB0b3A7XG59XG4uZGVtby1pbWFnZSAuYmxvY2s6bGFzdC1jaGlsZCB7XG4gIGJvcmRlci1yaWdodDogbm9uZTtcbn1cbi5kZW1vLWltYWdlIC5kZW1vbnN0cmF0aW9uIHtcbiAgZGlzcGxheTogYmxvY2s7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG4gIGZvbnQtc2l6ZTogMTRweDtcbiAgbWFyZ2luLWJvdHRvbTogMjBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/image/basic-usage.vue)_

vue

```
<template>
  <div class="demo-image">
    <div v-for="fit in fits" :key="fit" class="block">
      <span class="demonstration">{{ fit }}</span>
      <el-image style="width: 100px; height: 100px" :src="url" :fit="fit" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { ImageProps } from 'element-plus'

const fits = [
  'fill',
  'contain',
  'cover',
  'none',
  'scale-down',
] as ImageProps['fit'][]
const url =
  'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
</script>

<style scoped>
.demo-image .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 20%;
  min-width: 100px;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image .block:last-child {
  border-right: none;
}
.demo-image .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
```

隐藏源代码

## 占位内容 [​](#占位内容)

可通过`slot = placeholder`可自定义占位内容

Default

![](https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg)

Custom

![](https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg)

Loading...

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbWFnZV9fcGxhY2Vob2xkZXJcIj5cbiAgICA8ZGl2IGNsYXNzPVwiYmxvY2tcIj5cbiAgICAgIDxzcGFuIGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPkRlZmF1bHQ8L3NwYW4+XG4gICAgICA8ZWwtaW1hZ2UgOnNyYz1cInNyY1wiIC8+XG4gICAgPC9kaXY+XG4gICAgPGRpdiBjbGFzcz1cImJsb2NrXCI+XG4gICAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5DdXN0b208L3NwYW4+XG4gICAgICA8ZWwtaW1hZ2UgOnNyYz1cInNyY1wiPlxuICAgICAgICA8dGVtcGxhdGUgI3BsYWNlaG9sZGVyPlxuICAgICAgICAgIDxkaXYgY2xhc3M9XCJpbWFnZS1zbG90XCI+TG9hZGluZzxzcGFuIGNsYXNzPVwiZG90XCI+Li4uPC9zcGFuPjwvZGl2PlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgPC9lbC1pbWFnZT5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuY29uc3Qgc3JjID1cbiAgJ2h0dHBzOi8vY3ViZS5lbGVtZWNkbi5jb20vNi85NC80ZDNlYTUzYzA4NGJhZDY5MzFhNTZkNTE1OGE0OGpwZWcuanBlZydcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8taW1hZ2VfX3BsYWNlaG9sZGVyIC5ibG9jayB7XG4gIHBhZGRpbmc6IDMwcHggMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBib3JkZXItcmlnaHQ6IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICBkaXNwbGF5OiBpbmxpbmUtYmxvY2s7XG4gIHdpZHRoOiA0OSU7XG4gIGJveC1zaXppbmc6IGJvcmRlci1ib3g7XG4gIHZlcnRpY2FsLWFsaWduOiB0b3A7XG59XG4uZGVtby1pbWFnZV9fcGxhY2Vob2xkZXIgLmRlbW9uc3RyYXRpb24ge1xuICBkaXNwbGF5OiBibG9jaztcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbiAgZm9udC1zaXplOiAxNHB4O1xuICBtYXJnaW4tYm90dG9tOiAyMHB4O1xufVxuLmRlbW8taW1hZ2VfX3BsYWNlaG9sZGVyIC5lbC1pbWFnZSB7XG4gIHBhZGRpbmc6IDAgNXB4O1xuICBtYXgtd2lkdGg6IDMwMHB4O1xuICBtYXgtaGVpZ2h0OiAyMDBweDtcbn1cblxuLmRlbW8taW1hZ2VfX3BsYWNlaG9sZGVyLmltYWdlLXNsb3Qge1xuICBkaXNwbGF5OiBmbGV4O1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAgd2lkdGg6IDEwMCU7XG4gIGhlaWdodDogMTAwJTtcbiAgYmFja2dyb3VuZDogdmFyKC0tZWwtZmlsbC1jb2xvci1saWdodCk7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG4gIGZvbnQtc2l6ZTogMTRweDtcbn1cbi5kZW1vLWltYWdlX19wbGFjZWhvbGRlciAuZG90IHtcbiAgYW5pbWF0aW9uOiBkb3QgMnMgaW5maW5pdGUgc3RlcHMoMywgc3RhcnQpO1xuICBvdmVyZmxvdzogaGlkZGVuO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/image/placeholder.vue)_

vue

```
<template>
  <div class="demo-image__placeholder">
    <div class="block">
      <span class="demonstration">Default</span>
      <el-image :src="src" />
    </div>
    <div class="block">
      <span class="demonstration">Custom</span>
      <el-image :src="src">
        <template #placeholder>
          <div class="image-slot">Loading<span class="dot">...</span></div>
        </template>
      </el-image>
    </div>
  </div>
</template>

<script lang="ts" setup>
const src =
  'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg'
</script>

<style scoped>
.demo-image__placeholder .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 49%;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image__placeholder .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
.demo-image__placeholder .el-image {
  padding: 0 5px;
  max-width: 300px;
  max-height: 200px;
}

.demo-image__placeholder.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 14px;
}
.demo-image__placeholder .dot {
  animation: dot 2s infinite steps(3, start);
  overflow: hidden;
}
</style>
```

隐藏源代码

## 加载失败 [​](#加载失败)

通过 `slot = error` and `slot = viewer-error`自定义图像加载错误时的内容。

FAILED

![](https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg)

preview controlled

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbWFnZV9fZXJyb3JcIiBmbGV4IGdhcC0yPlxuICAgIDxlbC1pbWFnZSAvPlxuICAgIDxlbC1pbWFnZT5cbiAgICAgIDx0ZW1wbGF0ZSAjZXJyb3I+XG4gICAgICAgIDxkaXYgY2xhc3M9XCJpbWFnZS12aWV3ZXItc2xvdCBpbWFnZS1zbG90XCI+XG4gICAgICAgICAgPGVsLWljb24+PGljb24tcGljdHVyZSAvPjwvZWwtaWNvbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtaW1hZ2U+XG4gICAgPGVsLWltYWdlIDpzcmM9XCJ1cmxcIiA6cHJldmlldy1zcmMtbGlzdD1cInNyY0xpc3RcIiBzaG93LXByb2dyZXNzPlxuICAgICAgPHRlbXBsYXRlICN2aWV3ZXItZXJyb3I9XCJ7IGFjdGl2ZUluZGV4LCBzcmMgfVwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiaW1hZ2Utc2xvdCB2aWV3ZXItZXJyb3JcIj5cbiAgICAgICAgICA8ZWwtaWNvbj48aWNvbi1waWN0dXJlIC8+PC9lbC1pY29uPlxuICAgICAgICAgIDxzcGFuPlxuICAgICAgICAgICAgdGhpcyBpcyB2aWV3ZXItZXJyb3Igc2xvdC4gY3VycmVudCBpbmRleDoge3sgYWN0aXZlSW5kZXggfX0uIHNyYzpcbiAgICAgICAgICAgIHt7IHNyYyB9fVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtaW1hZ2U+XG4gICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJzaG93UHJldmlldyA9IHRydWVcIj4gcHJldmlldyBjb250cm9sbGVkIDwvZWwtYnV0dG9uPlxuXG4gICAgPGVsLWltYWdlLXZpZXdlclxuICAgICAgdi1pZj1cInNob3dQcmV2aWV3XCJcbiAgICAgIHNob3ctcHJvZ3Jlc3NcbiAgICAgIDp1cmwtbGlzdD1cInNyY0xpc3RcIlxuICAgICAgQGNsb3NlPVwic2hvd1ByZXZpZXcgPSBmYWxzZVwiXG4gICAgPlxuICAgICAgPHRlbXBsYXRlICN2aWV3ZXItZXJyb3I9XCJ7IGFjdGl2ZUluZGV4LCBzcmMgfVwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiaW1hZ2Utc2xvdCB2aWV3ZXItZXJyb3JcIj5cbiAgICAgICAgICA8ZWwtaWNvbj48aWNvbi1waWN0dXJlIC8+PC9lbC1pY29uPlxuICAgICAgICAgIDxzcGFuPlxuICAgICAgICAgICAgdGhpcyBpcyB2aWV3ZXItZXJyb3Igc2xvdC4gY3VycmVudCBpbmRleDoge3sgYWN0aXZlSW5kZXggfX0uIHNyYzpcbiAgICAgICAgICAgIHt7IHNyYyB9fVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtaW1hZ2Utdmlld2VyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBQaWN0dXJlIGFzIEljb25QaWN0dXJlIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IHNob3dQcmV2aWV3ID0gcmVmKGZhbHNlKVxuXG5jb25zdCBzcmNMaXN0ID0gW1xuICAnaHR0cHM6Ly9mdXNzMTAuZWxlbWVjZG4uY29tL2EvM2YvMzMwMmU1OGY5YTE4MWQyNTA5ZjNkYzBmYTY4YjBqcGVnLmpwZWcnLFxuICAnaHR0cHM6Ly9lcnJvclNyYycsXG5dXG5jb25zdCB1cmwgPVxuICAnaHR0cHM6Ly9mdXNzMTAuZWxlbWVjZG4uY29tL2EvM2YvMzMwMmU1OGY5YTE4MWQyNTA5ZjNkYzBmYTY4YjBqcGVnLmpwZWcnXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLWltYWdlX19lcnJvciAuZWwtaW1hZ2Uge1xuICBtYXgtd2lkdGg6IDMwMHB4O1xuICBtYXgtaGVpZ2h0OiAyMDBweDtcbiAgd2lkdGg6IDEwMCU7XG59XG5cbi5kZW1vLWltYWdlX19lcnJvciAuaW1hZ2Utc2xvdCB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGp1c3RpZnktY29udGVudDogY2VudGVyO1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBmb250LXNpemU6IDMwcHg7XG4gIGhlaWdodDogMjAwcHg7XG4gIGJhY2tncm91bmQ6ICNmZmY7XG59XG4uZGVtby1pbWFnZV9fZXJyb3IgLmltYWdlLXNsb3QgLmVsLWljb24ge1xuICBmb250LXNpemU6IDMwcHg7XG59XG4uaW1hZ2Utdmlld2VyLXNsb3Qge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1lbC1maWxsLWNvbG9yLWxpZ2h0KTtcbn1cbi52aWV3ZXItZXJyb3Ige1xuICBjb2xvcjogIzAwMDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/image/load-failed.vue)_

vue

```
<template>
  <div class="demo-image__error" flex gap-2>
    <el-image />
    <el-image>
      <template #error>
        <div class="image-viewer-slot image-slot">
          <el-icon><icon-picture /></el-icon>
        </div>
      </template>
    </el-image>
    <el-image :src="url" :preview-src-list="srcList" show-progress>
      <template #viewer-error="{ activeIndex, src }">
        <div class="image-slot viewer-error">
          <el-icon><icon-picture /></el-icon>
          <span>
            this is viewer-error slot. current index: {{ activeIndex }}. src:
            {{ src }}
          </span>
        </div>
      </template>
    </el-image>
    <el-button @click="showPreview = true"> preview controlled </el-button>

    <el-image-viewer
      v-if="showPreview"
      show-progress
      :url-list="srcList"
      @close="showPreview = false"
    >
      <template #viewer-error="{ activeIndex, src }">
        <div class="image-slot viewer-error">
          <el-icon><icon-picture /></el-icon>
          <span>
            this is viewer-error slot. current index: {{ activeIndex }}. src:
            {{ src }}
          </span>
        </div>
      </template>
    </el-image-viewer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Picture as IconPicture } from '@element-plus/icons-vue'

const showPreview = ref(false)

const srcList = [
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
  'https://errorSrc',
]
const url =
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg'
</script>

<style scoped>
.demo-image__error .el-image {
  max-width: 300px;
  max-height: 200px;
  width: 100%;
}

.demo-image__error .image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-size: 30px;
  height: 200px;
  background: #fff;
}
.demo-image__error .image-slot .el-icon {
  font-size: 30px;
}
.image-viewer-slot {
  background: var(--el-fill-color-light);
}
.viewer-error {
  color: #000;
}
</style>
```

隐藏源代码

## 懒加载 [​](#懒加载)

TIP

浏览器原生支持的 `loading`属性在 2.2.3版本加入。 您可以使用 `loading="lazy"` 替换之前的`lazy= true`。

如果当前浏览器支持原生图片延迟加载，则先使用原生能力，否则将使用滚动监听实现相同效果。

可通过`lazy`开启懒加载功能， 当图片滚动到可视范围内才会加载。 可通过 `scroll-container` 来设置滚动容器， 若未定义，则为最近一个 overflow 值为 auto 或 scroll 的父元素。

![](https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg)

![](https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbWFnZV9fbGF6eVwiPlxuICAgIDxlbC1pbWFnZSB2LWZvcj1cInVybCBpbiB1cmxzXCIgOmtleT1cInVybFwiIDpzcmM9XCJ1cmxcIiBsYXp5IC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IHVybHMgPSBbXG4gICdodHRwczovL2Z1c3MxMC5lbGVtZWNkbi5jb20vYS8zZi8zMzAyZTU4ZjlhMTgxZDI1MDlmM2RjMGZhNjhiMGpwZWcuanBlZycsXG4gICdodHRwczovL2Z1c3MxMC5lbGVtZWNkbi5jb20vMS8zNC8xOWFhOThiMWZjYjI3ODFjNGZiYTMzZDg1MDU0OWpwZWcuanBlZycsXG4gICdodHRwczovL2Z1c3MxMC5lbGVtZWNkbi5jb20vMC82Zi9lMzVmZjM3NTgxMmU2YjAwMjBiNmI0ZThmOTU4M2pwZWcuanBlZycsXG4gICdodHRwczovL2Z1c3MxMC5lbGVtZWNkbi5jb20vOS9iYi9lMjc4NThlOTczZjVkN2QzOTA0ODM1ZjQ2YWJiZGpwZWcuanBlZycsXG4gICdodHRwczovL2Z1c3MxMC5lbGVtZWNkbi5jb20vZC9lNi9jNGQ5M2EzODA1YjNjZTNmMzIzZjc5NzRlNmY3OGpwZWcuanBlZycsXG4gICdodHRwczovL2Z1c3MxMC5lbGVtZWNkbi5jb20vMy8yOC9iYmY4OTNmNzkyZjAzYTU0NDA4YjNiN2E3ZWJmMGpwZWcuanBlZycsXG4gICdodHRwczovL2Z1c3MxMC5lbGVtZWNkbi5jb20vMi8xMS82NTM1YmNmYjI2ZTRjNzliNDhkZGRlNDRmNGI2ZmpwZWcuanBlZycsXG5dXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLWltYWdlX19sYXp5IHtcbiAgaGVpZ2h0OiA0MDBweDtcbiAgb3ZlcmZsb3cteTogYXV0bztcbn1cbi5kZW1vLWltYWdlX19sYXp5IC5lbC1pbWFnZSB7XG4gIGRpc3BsYXk6IGJsb2NrO1xuICBtaW4taGVpZ2h0OiAyMDBweDtcbiAgbWFyZ2luLWJvdHRvbTogMTBweDtcbn1cbi5kZW1vLWltYWdlX19sYXp5IC5lbC1pbWFnZTpsYXN0LWNoaWxkIHtcbiAgbWFyZ2luLWJvdHRvbTogMDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/image/lazy-load.vue)_

vue

```
<template>
  <div class="demo-image__lazy">
    <el-image v-for="url in urls" :key="url" :src="url" lazy />
  </div>
</template>

<script lang="ts" setup>
const urls = [
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
  'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
  'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
  'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
  'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
  'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
  'https://fuss10.elemecdn.com/2/11/6535bcfb26e4c79b48ddde44f4b6fjpeg.jpeg',
]
</script>

<style scoped>
.demo-image__lazy {
  height: 400px;
  overflow-y: auto;
}
.demo-image__lazy .el-image {
  display: block;
  min-height: 200px;
  margin-bottom: 10px;
}
.demo-image__lazy .el-image:last-child {
  margin-bottom: 0;
}
</style>
```

隐藏源代码

## 图片预览 [​](#图片预览)

可通过 `previewSrcList` 开启预览大图的功能。 你可以通过 `initial-index` 初始化第一张预览图片的位置。 默认初始位置为 0。

![](https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbWFnZV9fcHJldmlld1wiPlxuICAgIDxlbC1pbWFnZVxuICAgICAgc3R5bGU9XCJ3aWR0aDogMTAwcHg7IGhlaWdodDogMTAwcHhcIlxuICAgICAgOnNyYz1cInVybFwiXG4gICAgICA6em9vbS1yYXRlPVwiMS4yXCJcbiAgICAgIDptYXgtc2NhbGU9XCI3XCJcbiAgICAgIDptaW4tc2NhbGU9XCIwLjJcIlxuICAgICAgOnByZXZpZXctc3JjLWxpc3Q9XCJzcmNMaXN0XCJcbiAgICAgIHNob3ctcHJvZ3Jlc3NcbiAgICAgIDppbml0aWFsLWluZGV4PVwiNFwiXG4gICAgICBmaXQ9XCJjb3ZlclwiXG4gICAgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuY29uc3QgdXJsID1cbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9hLzNmLzMzMDJlNThmOWExODFkMjUwOWYzZGMwZmE2OGIwanBlZy5qcGVnJ1xuY29uc3Qgc3JjTGlzdCA9IFtcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9hLzNmLzMzMDJlNThmOWExODFkMjUwOWYzZGMwZmE2OGIwanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8xLzM0LzE5YWE5OGIxZmNiMjc4MWM0ZmJhMzNkODUwNTQ5anBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8wLzZmL2UzNWZmMzc1ODEyZTZiMDAyMGI2YjRlOGY5NTgzanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS85L2JiL2UyNzg1OGU5NzNmNWQ3ZDM5MDQ4MzVmNDZhYmJkanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9kL2U2L2M0ZDkzYTM4MDViM2NlM2YzMjNmNzk3NGU2Zjc4anBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8zLzI4L2JiZjg5M2Y3OTJmMDNhNTQ0MDhiM2I3YTdlYmYwanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8yLzExLzY1MzViY2ZiMjZlNGM3OWI0OGRkZGU0NGY0YjZmanBlZy5qcGVnJyxcbl1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8taW1hZ2VfX2Vycm9yIC5pbWFnZS1zbG90IHtcbiAgZm9udC1zaXplOiAzMHB4O1xufVxuLmRlbW8taW1hZ2VfX2Vycm9yIC5pbWFnZS1zbG90IC5lbC1pY29uIHtcbiAgZm9udC1zaXplOiAzMHB4O1xufVxuLmRlbW8taW1hZ2VfX2Vycm9yIC5lbC1pbWFnZSB7XG4gIHdpZHRoOiAxMDAlO1xuICBoZWlnaHQ6IDIwMHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/image/image-preview.vue)_

vue

```
<template>
  <div class="demo-image__preview">
    <el-image
      style="width: 100px; height: 100px"
      :src="url"
      :zoom-rate="1.2"
      :max-scale="7"
      :min-scale="0.2"
      :preview-src-list="srcList"
      show-progress
      :initial-index="4"
      fit="cover"
    />
  </div>
</template>

<script lang="ts" setup>
const url =
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg'
const srcList = [
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
  'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
  'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
  'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
  'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
  'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
  'https://fuss10.elemecdn.com/2/11/6535bcfb26e4c79b48ddde44f4b6fjpeg.jpeg',
]
</script>

<style scoped>
.demo-image__error .image-slot {
  font-size: 30px;
}
.demo-image__error .image-slot .el-icon {
  font-size: 30px;
}
.demo-image__error .el-image {
  width: 100%;
  height: 200px;
}
</style>
```

隐藏源代码

## 手动打开预览 2.9.4 [​](#手动打开预览)

openPreview with showPreview method

![](https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg)

preview controlled

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtMTJcIj5cbiAgICA8ZGl2IGNsYXNzPVwiZ3JpZCBnYXAtM1wiPlxuICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJoYW5kbGVDbGlja1wiPlxuICAgICAgICBvcGVuUHJldmlldyB3aXRoIHNob3dQcmV2aWV3IG1ldGhvZFxuICAgICAgPC9lbC1idXR0b24+XG4gICAgICA8ZWwtaW1hZ2VcbiAgICAgICAgcmVmPVwiaW1hZ2VSZWZcIlxuICAgICAgICBzdHlsZT1cIndpZHRoOiAxMDBweDsgaGVpZ2h0OiAxMDBweFwiXG4gICAgICAgIDpzcmM9XCJ1cmxcIlxuICAgICAgICBzaG93LXByb2dyZXNzXG4gICAgICAgIDpwcmV2aWV3LXNyYy1saXN0PVwic3JjTGlzdFwiXG4gICAgICAgIGZpdD1cImNvdmVyXCJcbiAgICAgIC8+XG4gICAgPC9kaXY+XG4gICAgPGRpdj5cbiAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwic2hvd1ByZXZpZXcgPSB0cnVlXCI+IHByZXZpZXcgY29udHJvbGxlZCA8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1pbWFnZS12aWV3ZXJcbiAgICAgICAgdi1pZj1cInNob3dQcmV2aWV3XCJcbiAgICAgICAgOnVybC1saXN0PVwic3JjTGlzdFwiXG4gICAgICAgIHNob3ctcHJvZ3Jlc3NcbiAgICAgICAgOmluaXRpYWwtaW5kZXg9XCI0XCJcbiAgICAgICAgQGNsb3NlPVwic2hvd1ByZXZpZXcgPSBmYWxzZVwiXG4gICAgICAvPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgSW1hZ2VJbnN0YW5jZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgdXJsID1cbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9hLzNmLzMzMDJlNThmOWExODFkMjUwOWYzZGMwZmE2OGIwanBlZy5qcGVnJ1xuY29uc3Qgc3JjTGlzdCA9IFtcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9hLzNmLzMzMDJlNThmOWExODFkMjUwOWYzZGMwZmE2OGIwanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8xLzM0LzE5YWE5OGIxZmNiMjc4MWM0ZmJhMzNkODUwNTQ5anBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8wLzZmL2UzNWZmMzc1ODEyZTZiMDAyMGI2YjRlOGY5NTgzanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS85L2JiL2UyNzg1OGU5NzNmNWQ3ZDM5MDQ4MzVmNDZhYmJkanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9kL2U2L2M0ZDkzYTM4MDViM2NlM2YzMjNmNzk3NGU2Zjc4anBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8zLzI4L2JiZjg5M2Y3OTJmMDNhNTQ0MDhiM2I3YTdlYmYwanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8yLzExLzY1MzViY2ZiMjZlNGM3OWI0OGRkZGU0NGY0YjZmanBlZy5qcGVnJyxcbl1cblxuY29uc3QgaW1hZ2VSZWYgPSByZWY8SW1hZ2VJbnN0YW5jZT4oKVxuY29uc3Qgc2hvd1ByZXZpZXcgPSByZWYoZmFsc2UpXG5cbmNvbnN0IGhhbmRsZUNsaWNrID0gKCkgPT4ge1xuICBpbWFnZVJlZi52YWx1ZSEuc2hvd1ByZXZpZXcoKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/image/manually-preview.vue)_

vue

```
<template>
  <div class="flex gap-12">
    <div class="grid gap-3">
      <el-button @click="handleClick">
        openPreview with showPreview method
      </el-button>
      <el-image
        ref="imageRef"
        style="width: 100px; height: 100px"
        :src="url"
        show-progress
        :preview-src-list="srcList"
        fit="cover"
      />
    </div>
    <div>
      <el-button @click="showPreview = true"> preview controlled </el-button>
      <el-image-viewer
        v-if="showPreview"
        :url-list="srcList"
        show-progress
        :initial-index="4"
        @close="showPreview = false"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { ImageInstance } from 'element-plus'

const url =
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg'
const srcList = [
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
  'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
  'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
  'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
  'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
  'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
  'https://fuss10.elemecdn.com/2/11/6535bcfb26e4c79b48ddde44f4b6fjpeg.jpeg',
]

const imageRef = ref<ImageInstance>()
const showPreview = ref(false)

const handleClick = () => {
  imageRef.value!.showPreview()
}
</script>
```

隐藏源代码

## 自定义工具栏2.9.4 [​](#自定义工具栏)

可通过 `toolbar` 插槽自定义工具栏内容，自版本 2.9.7 起，插槽中添加了 `setActiveItem` 方法，用于根据索引切换图片。

![](https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbWFnZV9fY3VzdG9tLXRvb2xiYXJcIj5cbiAgICA8ZWwtaW1hZ2VcbiAgICAgIHN0eWxlPVwid2lkdGg6IDEwMHB4OyBoZWlnaHQ6IDEwMHB4XCJcbiAgICAgIDpzcmM9XCJ1cmxcIlxuICAgICAgOnByZXZpZXctc3JjLWxpc3Q9XCJzcmNMaXN0XCJcbiAgICAgIGZpdD1cImNvdmVyXCJcbiAgICAgIHNob3ctcHJvZ3Jlc3NcbiAgICA+XG4gICAgICA8dGVtcGxhdGVcbiAgICAgICAgI3Rvb2xiYXI9XCJ7IGFjdGlvbnMsIHByZXYsIG5leHQsIHJlc2V0LCBhY3RpdmVJbmRleCwgc2V0QWN0aXZlSXRlbSB9XCJcbiAgICAgID5cbiAgICAgICAgPGVsLWljb24gQGNsaWNrPVwicHJldlwiPjxCYWNrIC8+PC9lbC1pY29uPlxuICAgICAgICA8ZWwtaWNvbiBAY2xpY2s9XCJuZXh0XCI+PFJpZ2h0IC8+PC9lbC1pY29uPlxuICAgICAgICA8ZWwtaWNvbiBAY2xpY2s9XCJzZXRBY3RpdmVJdGVtKHNyY0xpc3QubGVuZ3RoIC0gMSlcIj5cbiAgICAgICAgICA8REFycm93UmlnaHQgLz5cbiAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICA8ZWwtaWNvbiBAY2xpY2s9XCJhY3Rpb25zKCd6b29tT3V0JylcIj48Wm9vbU91dCAvPjwvZWwtaWNvbj5cbiAgICAgICAgPGVsLWljb25cbiAgICAgICAgICBAY2xpY2s9XCJhY3Rpb25zKCd6b29tSW4nLCB7IGVuYWJsZVRyYW5zaXRpb246IGZhbHNlLCB6b29tUmF0ZTogMiB9KVwiXG4gICAgICAgID5cbiAgICAgICAgICA8Wm9vbUluIC8+XG4gICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgPGVsLWljb25cbiAgICAgICAgICBAY2xpY2s9XCJcbiAgICAgICAgICAgIGFjdGlvbnMoJ2Nsb2Nrd2lzZScsIHsgcm90YXRlRGVnOiAxODAsIGVuYWJsZVRyYW5zaXRpb246IGZhbHNlIH0pXG4gICAgICAgICAgXCJcbiAgICAgICAgPlxuICAgICAgICAgIDxSZWZyZXNoUmlnaHQgLz5cbiAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICA8ZWwtaWNvbiBAY2xpY2s9XCJhY3Rpb25zKCdhbnRpY2xvY2t3aXNlJylcIj48UmVmcmVzaExlZnQgLz48L2VsLWljb24+XG4gICAgICAgIDxlbC1pY29uIEBjbGljaz1cInJlc2V0XCI+PFJlZnJlc2ggLz48L2VsLWljb24+XG4gICAgICAgIDxlbC1pY29uIEBjbGljaz1cImRvd25sb2FkKGFjdGl2ZUluZGV4KVwiPjxEb3dubG9hZCAvPjwvZWwtaWNvbj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1pbWFnZT5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxJY29uIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuaW1wb3J0IHtcbiAgQmFjayxcbiAgREFycm93UmlnaHQsXG4gIERvd25sb2FkLFxuICBSZWZyZXNoLFxuICBSZWZyZXNoTGVmdCxcbiAgUmVmcmVzaFJpZ2h0LFxuICBSaWdodCxcbiAgWm9vbUluLFxuICBab29tT3V0LFxufSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgdXJsID1cbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9hLzNmLzMzMDJlNThmOWExODFkMjUwOWYzZGMwZmE2OGIwanBlZy5qcGVnJ1xuY29uc3Qgc3JjTGlzdCA9IFtcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9hLzNmLzMzMDJlNThmOWExODFkMjUwOWYzZGMwZmE2OGIwanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8xLzM0LzE5YWE5OGIxZmNiMjc4MWM0ZmJhMzNkODUwNTQ5anBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8wLzZmL2UzNWZmMzc1ODEyZTZiMDAyMGI2YjRlOGY5NTgzanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS85L2JiL2UyNzg1OGU5NzNmNWQ3ZDM5MDQ4MzVmNDZhYmJkanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9kL2U2L2M0ZDkzYTM4MDViM2NlM2YzMjNmNzk3NGU2Zjc4anBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8zLzI4L2JiZjg5M2Y3OTJmMDNhNTQ0MDhiM2I3YTdlYmYwanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8yLzExLzY1MzViY2ZiMjZlNGM3OWI0OGRkZGU0NGY0YjZmanBlZy5qcGVnJyxcbl1cblxuY29uc3QgZG93bmxvYWQgPSAoaW5kZXg6IG51bWJlcikgPT4ge1xuICBjb25zdCB1cmwgPSBzcmNMaXN0W2luZGV4XVxuICBjb25zdCBzdWZmaXggPSB1cmwuc2xpY2UodXJsLmxhc3RJbmRleE9mKCcuJykpXG4gIGNvbnN0IGZpbGVuYW1lID0gRGF0ZS5ub3coKSArIHN1ZmZpeFxuXG4gIGZldGNoKHVybClcbiAgICAudGhlbigocmVzcG9uc2UpID0+IHJlc3BvbnNlLmJsb2IoKSlcbiAgICAudGhlbigoYmxvYikgPT4ge1xuICAgICAgY29uc3QgYmxvYlVybCA9IFVSTC5jcmVhdGVPYmplY3RVUkwobmV3IEJsb2IoW2Jsb2JdKSlcbiAgICAgIGNvbnN0IGxpbmsgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdhJylcbiAgICAgIGxpbmsuaHJlZiA9IGJsb2JVcmxcbiAgICAgIGxpbmsuZG93bmxvYWQgPSBmaWxlbmFtZVxuICAgICAgZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChsaW5rKVxuICAgICAgbGluay5jbGljaygpXG4gICAgICBVUkwucmV2b2tlT2JqZWN0VVJMKGJsb2JVcmwpXG4gICAgICBsaW5rLnJlbW92ZSgpXG4gICAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/image/custom-toolbar.vue)_

vue

```
<template>
  <div class="demo-image__custom-toolbar">
    <el-image
      style="width: 100px; height: 100px"
      :src="url"
      :preview-src-list="srcList"
      fit="cover"
      show-progress
    >
      <template
        #toolbar="{ actions, prev, next, reset, activeIndex, setActiveItem }"
      >
        <el-icon @click="prev"><Back /></el-icon>
        <el-icon @click="next"><Right /></el-icon>
        <el-icon @click="setActiveItem(srcList.length - 1)">
          <DArrowRight />
        </el-icon>
        <el-icon @click="actions('zoomOut')"><ZoomOut /></el-icon>
        <el-icon
          @click="actions('zoomIn', { enableTransition: false, zoomRate: 2 })"
        >
          <ZoomIn />
        </el-icon>
        <el-icon
          @click="
            actions('clockwise', { rotateDeg: 180, enableTransition: false })
          "
        >
          <RefreshRight />
        </el-icon>
        <el-icon @click="actions('anticlockwise')"><RefreshLeft /></el-icon>
        <el-icon @click="reset"><Refresh /></el-icon>
        <el-icon @click="download(activeIndex)"><Download /></el-icon>
      </template>
    </el-image>
  </div>
</template>

<script lang="ts" setup>
import { ElIcon } from 'element-plus'
import {
  Back,
  DArrowRight,
  Download,
  Refresh,
  RefreshLeft,
  RefreshRight,
  Right,
  ZoomIn,
  ZoomOut,
} from '@element-plus/icons-vue'

const url =
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg'
const srcList = [
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
  'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
  'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
  'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
  'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
  'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
  'https://fuss10.elemecdn.com/2/11/6535bcfb26e4c79b48ddde44f4b6fjpeg.jpeg',
]

const download = (index: number) => {
  const url = srcList[index]
  const suffix = url.slice(url.lastIndexOf('.'))
  const filename = Date.now() + suffix

  fetch(url)
    .then((response) => response.blob())
    .then((blob) => {
      const blobUrl = URL.createObjectURL(new Blob([blob]))
      const link = document.createElement('a')
      link.href = blobUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      URL.revokeObjectURL(blobUrl)
      link.remove()
    })
}
</script>
```

隐藏源代码

## 自定义进度条 2.9.4 [​](#自定义进度条)

可通过 `show-progress` 控制是否在预览图片时显示进度条。 自版本 2.9.8 起，进度条会在使用 `progress` 插槽时显示。

![](https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbWFnZV9fY3VzdG9tLXRvb2xiYXJcIj5cbiAgICA8ZWwtaW1hZ2VcbiAgICAgIHN0eWxlPVwid2lkdGg6IDEwMHB4OyBoZWlnaHQ6IDEwMHB4XCJcbiAgICAgIDpzcmM9XCJ1cmxcIlxuICAgICAgOnByZXZpZXctc3JjLWxpc3Q9XCJzcmNMaXN0XCJcbiAgICAgIGZpdD1cImNvdmVyXCJcbiAgICA+XG4gICAgICA8dGVtcGxhdGUgI3Byb2dyZXNzPVwieyBhY3RpdmVJbmRleCwgdG90YWwgfVwiPlxuICAgICAgICA8c3Bhbj57eyBhY3RpdmVJbmRleCArIDEgKyAnLScgKyB0b3RhbCB9fTwvc3Bhbj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1pbWFnZT5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuY29uc3QgdXJsID1cbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9hLzNmLzMzMDJlNThmOWExODFkMjUwOWYzZGMwZmE2OGIwanBlZy5qcGVnJ1xuY29uc3Qgc3JjTGlzdCA9IFtcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9hLzNmLzMzMDJlNThmOWExODFkMjUwOWYzZGMwZmE2OGIwanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8xLzM0LzE5YWE5OGIxZmNiMjc4MWM0ZmJhMzNkODUwNTQ5anBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8wLzZmL2UzNWZmMzc1ODEyZTZiMDAyMGI2YjRlOGY5NTgzanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS85L2JiL2UyNzg1OGU5NzNmNWQ3ZDM5MDQ4MzVmNDZhYmJkanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS9kL2U2L2M0ZDkzYTM4MDViM2NlM2YzMjNmNzk3NGU2Zjc4anBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8zLzI4L2JiZjg5M2Y3OTJmMDNhNTQ0MDhiM2I3YTdlYmYwanBlZy5qcGVnJyxcbiAgJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8yLzExLzY1MzViY2ZiMjZlNGM3OWI0OGRkZGU0NGY0YjZmanBlZy5qcGVnJyxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/image/custom-progress.vue)_

vue

```
<template>
  <div class="demo-image__custom-toolbar">
    <el-image
      style="width: 100px; height: 100px"
      :src="url"
      :preview-src-list="srcList"
      fit="cover"
    >
      <template #progress="{ activeIndex, total }">
        <span>{{ activeIndex + 1 + '-' + total }}</span>
      </template>
    </el-image>
  </div>
</template>

<script lang="ts" setup>
const url =
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg'
const srcList = [
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
  'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
  'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
  'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
  'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
  'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
  'https://fuss10.elemecdn.com/2/11/6535bcfb26e4c79b48ddde44f4b6fjpeg.jpeg',
]
</script>
```

隐藏源代码

## Image API [​](#image-api)

### Image Attributes [​](#image-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| src | 图片源地址，同原生属性一致 | `string` | '' |
| fit | 确定图片如何适应容器框，同原生 [object-fit](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit) | `enum` | '' |
| hide-on-click-modal | 当开启 preview 功能时，是否可以通过点击遮罩层关闭 preview | `boolean` | false |
| loading 2.2.3 | 浏览器加载图像的策略，和 [浏览器原生](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-loading)能力一致 | `enum` | — |
| lazy | 是否使用懒加载 | `boolean` | false |
| scroll-container | 开启懒加载功能后，监听 scroll 事件的容器 默认情况下，开启懒加载功能后，监听 scroll 事件的容器 | `string` / `object` | — |
| alt | 原生属性 `alt` | `string` | — |
| referrerpolicy | 原生属性 [referrerPolicy](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/referrerPolicy)。 | `string` | — |
| crossorigin | 原生属性 [crossorigin](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin) | `enum` | — |
| preview-src-list | 开启图片预览功能 | `array` | \[\] |
| z-index | 设置图片预览的 z-index | `number` | — |
| initial-index | 初始预览图像索引，小于 `url-list` 的长度 | `number` | 0 |
| close-on-press-escape | 是否可以通过按下 ESC 关闭 Image Viewer | `boolean` | true |
| preview-teleported | image-viewer 是否插入至 body 元素上。 嵌套的父元素属性会发生修改时应该将此属性设置为 `true` | `boolean` | false |
| infinite | 是否可以无限循环预览 | `boolean` | true |
| zoom-rate | 图像查看器缩放事件的缩放速率。 | `number` | 1.2 |
| scale 2.11.3 | 预览图像缩放。 | `number` | 1 |
| min-scale 2.4.0 | 图像查看器缩放事件的最小缩放比例 | `number` | 0.2 |
| max-scale 2.4.0 | 图像查看器缩放事件的最大缩放比例 | `number` | 7 |
| show-progress 2.9.4 | 是否在预览图片时显示进度条 | `boolean` | false |

### Image Events [​](#image-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| load | 图片加载成功触发 | `Function` |
| error | 图片加载失败触发 | `Function` |
| switch | 切换图像时触发。 | `Function` |
| close | 当点击 X 按钮或者在`hide-on-click-modal`为 true 时点击遮罩层时触发 | `Function` |
| show | 当 Viewer 显示时触发 | `Function` |

### Image Slots [​](#image-slots)

| 插槽名 | 说明 | 类型 |
| --- | --- | --- |
| placeholder | 当图像尚未加载时，自定义的占位符内容 | \- |
| error | 自定义图像加载失败的内容 | \- |
| [\[image viewer slots\](#image-viewer-slots)](#image-viewer-slots) | 当你允许大的图像预览时，可以使用图像预览的插槽。 | \- |

### Image Exposes [​](#image-exposes)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| showPreview 2.9.4 | 手动打开大图预览 | `Function` |

## Image Viewer API [​](#image-viewer-api)

### Image Viewer Attributes [​](#image-viewer-attributes)

| 事件名 | 说明 | Type | 默认值 |
| --- | --- | --- | --- |
| url-list | 用于预览的图片链接列表 | `array` | \[\] |
| z-index | 预览时遮罩层的 z-index | `number` / `string` | — |
| initial-index | 初始预览图像索引，小于 `url-list` 的长度 | `number` | 0 |
| infinite | 是否可以无限循环预览 | `boolean` | true |
| hide-on-click-modal | 是否可以通过点击遮罩层关闭预览 | `boolean` | false |
| teleported | image 自身是否插入至 body 元素上。 嵌套的父元素属性会发生修改时应该将此属性设置为 `true` | `boolean` | false |
| zoom-rate 2.2.27 | 图像查看器缩放事件的缩放速率。 | `number` | 1.2 |
| scale 2.11.3 | 预览图像缩放。 | `number` | 1 |
| min-scale 2.4.0 | 图像查看器缩放事件的最小缩放比例 | `number` | 0.2 |
| max-scale 2.4.0 | 图像查看器缩放事件的最大缩放比例 | `number` | 7 |
| close-on-press-escape | 是否可以通过按下 ESC 关闭 Image Viewer | `boolean` | true |
| show-progress 2.9.4 | 是否显示预览图片的进度条内容 | `boolean` | false |

### Image Viewer Events [​](#image-viewer-events)

| Name | 说明 | 类型 |
| --- | --- | --- |
| close | 当点击 X 按钮或者在`hide-on-click-modal`为 true 时点击遮罩层时触发 | `Function` |
| error 2.11.3 | 图片加载失败触发 | `Function` |
| switch | 切换图像时触发。 | `Function` |
| rotate 2.3.13 | 旋转图像时触发。 | `Function` |

### Image Viewer Slots [​](#image-viewer-slots)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| viewer | 自定义内容 | \- |
| progress 2.9.4 | 自定义进度内容 (优先级高于 `show-progress` prop) | `object` |
| toolbar 2.9.4 | 自定义工具栏内容 | `object` |
| viewer-error 2.11.3 | 自定义图像加载失败的内容 | `object` |

### Image Viewer Exposes [​](#image-viewer-exposes)

| Name | Description | Type |
| --- | --- | --- |
| setActiveItem | 手动切换图片 | `Function` |

## 类型声明 [​](#类型声明)

Show declarations

ts

```
type ImageViewerAction = 'zoomIn' | 'zoomOut' | 'clockwise' | 'anticlockwise'
type ImageViewerActionOptions = {
  enableTransition?: boolean
  zoomRate?: number
  rotateDeg?: number
}
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/image) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/image.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/image.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/24540820?v=4&size=64)](https://github.com/catanswer)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/55419399?v=4&size=64)](https://github.com/declanchiu)[![](https://avatars.githubusercontent.com/u/33775809?v=4&size=64)](https://github.com/besscroft)[![](https://avatars.githubusercontent.com/u/63360587?v=4&size=64)](https://github.com/wkasunsampath)[![](https://avatars.githubusercontent.com/u/66096254?v=4&size=64)](https://github.com/IceyWu)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/27653885?v=4&size=64)](https://github.com/cicada-ah)[![](https://avatars.githubusercontent.com/u/49704630?v=4&size=64)](https://github.com/ljf1834)[![](https://avatars.githubusercontent.com/u/16984236?v=4&size=64)](https://github.com/JiatLn)[![](https://avatars.githubusercontent.com/u/26266181?v=4&size=64)](https://github.com/wydingez)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/8347286?v=4&size=64)](https://github.com/holynewbie)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/27729870?v=4&size=64)](https://github.com/zycoJamie)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)[![](https://avatars.githubusercontent.com/u/96148681?v=4&size=64)](https://github.com/cregis0073)[![](https://avatars.githubusercontent.com/u/442927?v=4&size=64)](https://github.com/EstebanFuentealba)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/27677166?v=4&size=64)](https://github.com/hickiy)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/57179957?v=4&size=64)](https://github.com/yeonjulee1005)[![](https://avatars.githubusercontent.com/u/1836701?v=4&size=64)](https://github.com/HADB)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/75007029?v=4&size=64)](https://github.com/yj-liuzepeng)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)

[Empty 空状态](https://element-plus.org/zh-CN/component/empty)

[Infinite Scroll 无限滚动](https://element-plus.org/zh-CN/component/infinite-scroll)


