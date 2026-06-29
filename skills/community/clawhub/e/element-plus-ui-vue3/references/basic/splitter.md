---
name: "splitter"
description: "Splitter 分隔面板 -- Element Plus Vue3 桌面端组件。Invoke when user needs Splitter 分隔面板 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/splitter.html"
---

---

# Splitter 分隔面板 beta [​](#splitter-分隔面板)

更新日志待解决

5

可将区域水平或垂直分隔，并可自由拖动以调整各个区域的大小。

## 基础用法 [​](#基础用法)

最基本的用法，如果未传入默认尺寸，将自动平均分配。

1

2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2XG4gICAgc3R5bGU9XCJoZWlnaHQ6IDI1MHB4OyBib3gtc2hhZG93OiB2YXIoLS1lbC1ib3JkZXItY29sb3ItbGlnaHQpIDBweCAwcHggMTBweFwiXG4gID5cbiAgICA8ZWwtc3BsaXR0ZXI+XG4gICAgICA8ZWwtc3BsaXR0ZXItcGFuZWwgc2l6ZT1cIjMwJVwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZGVtby1wYW5lbFwiPjE8L2Rpdj5cbiAgICAgIDwvZWwtc3BsaXR0ZXItcGFuZWw+XG4gICAgICA8ZWwtc3BsaXR0ZXItcGFuZWwgOm1pbj1cIjIwMFwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZGVtby1wYW5lbFwiPjI8L2Rpdj5cbiAgICAgIDwvZWwtc3BsaXR0ZXItcGFuZWw+XG4gICAgPC9lbC1zcGxpdHRlcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tcGFuZWwge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgaGVpZ2h0OiAxMDAlO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/splitter/basic.vue)_

vue

```
<template>
  <div
    style="height: 250px; box-shadow: var(--el-border-color-light) 0px 0px 10px"
  >
    <el-splitter>
      <el-splitter-panel size="30%">
        <div class="demo-panel">1</div>
      </el-splitter-panel>
      <el-splitter-panel :min="200">
        <div class="demo-panel">2</div>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
```

隐藏源代码

## 垂直布局 [​](#垂直布局)

使用垂直方向。

1

2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2XG4gICAgc3R5bGU9XCJoZWlnaHQ6IDI1MHB4OyBib3gtc2hhZG93OiB2YXIoLS1lbC1ib3JkZXItY29sb3ItbGlnaHQpIDBweCAwcHggMTBweFwiXG4gID5cbiAgICA8ZWwtc3BsaXR0ZXIgbGF5b3V0PVwidmVydGljYWxcIj5cbiAgICAgIDxlbC1zcGxpdHRlci1wYW5lbD5cbiAgICAgICAgPGRpdiBjbGFzcz1cImRlbW8tcGFuZWxcIj4xPC9kaXY+XG4gICAgICA8L2VsLXNwbGl0dGVyLXBhbmVsPlxuICAgICAgPGVsLXNwbGl0dGVyLXBhbmVsPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZGVtby1wYW5lbFwiPjI8L2Rpdj5cbiAgICAgIDwvZWwtc3BsaXR0ZXItcGFuZWw+XG4gICAgPC9lbC1zcGxpdHRlcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tcGFuZWwge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgaGVpZ2h0OiAxMDAlO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/splitter/vertical.vue)_

vue

```
<template>
  <div
    style="height: 250px; box-shadow: var(--el-border-color-light) 0px 0px 10px"
  >
    <el-splitter layout="vertical">
      <el-splitter-panel>
        <div class="demo-panel">1</div>
      </el-splitter-panel>
      <el-splitter-panel>
        <div class="demo-panel">2</div>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
```

隐藏源代码

## 可折叠 [​](#可折叠)

配置 `collapsible` 可提供快速收缩功能。 你可以使用 `min` 属性来防止折叠后通过拖拽进行扩展。

enable

1

2

3

4

5

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoXG4gICAgdi1tb2RlbD1cImlzQ29sbGFwc2libGVcIlxuICAgIGFjdGl2ZS10ZXh0PVwiZW5hYmxlXCJcbiAgICBpbmFjdGl2ZS10ZXh0PVwiZGlzYWJsZVwiXG4gICAgaW5saW5lLXByb21wdFxuICAgIGNsYXNzPVwibWItMlwiXG4gIC8+XG4gIDxkaXZcbiAgICBzdHlsZT1cImhlaWdodDogMjUwcHg7IGJveC1zaGFkb3c6IHZhcigtLWVsLWJvcmRlci1jb2xvci1saWdodCkgMHB4IDBweCAxMHB4XCJcbiAgPlxuICAgIDxlbC1zcGxpdHRlcj5cbiAgICAgIDxlbC1zcGxpdHRlci1wYW5lbCA6Y29sbGFwc2libGU9XCJpc0NvbGxhcHNpYmxlXCIgbWluPVwiNTBcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImRlbW8tcGFuZWxcIj4xPC9kaXY+XG4gICAgICA8L2VsLXNwbGl0dGVyLXBhbmVsPlxuICAgICAgPGVsLXNwbGl0dGVyLXBhbmVsIDpjb2xsYXBzaWJsZT1cImlzQ29sbGFwc2libGVcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImRlbW8tcGFuZWxcIj4yPC9kaXY+XG4gICAgICA8L2VsLXNwbGl0dGVyLXBhbmVsPlxuICAgICAgPGVsLXNwbGl0dGVyLXBhbmVsPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZGVtby1wYW5lbFwiPjM8L2Rpdj5cbiAgICAgIDwvZWwtc3BsaXR0ZXItcGFuZWw+XG4gICAgICA8ZWwtc3BsaXR0ZXItcGFuZWwgOmNvbGxhcHNpYmxlPVwiaXNDb2xsYXBzaWJsZVwiPlxuICAgICAgICA8ZWwtc3BsaXR0ZXIgbGF5b3V0PVwidmVydGljYWxcIj5cbiAgICAgICAgICA8ZWwtc3BsaXR0ZXItcGFuZWwgOmNvbGxhcHNpYmxlPVwiaXNDb2xsYXBzaWJsZVwiPlxuICAgICAgICAgICAgPGRpdiBjbGFzcz1cImRlbW8tcGFuZWxcIj40PC9kaXY+XG4gICAgICAgICAgPC9lbC1zcGxpdHRlci1wYW5lbD5cbiAgICAgICAgICA8ZWwtc3BsaXR0ZXItcGFuZWwgOmNvbGxhcHNpYmxlPVwiaXNDb2xsYXBzaWJsZVwiPlxuICAgICAgICAgICAgPGRpdiBjbGFzcz1cImRlbW8tcGFuZWxcIj41PC9kaXY+XG4gICAgICAgICAgPC9lbC1zcGxpdHRlci1wYW5lbD5cbiAgICAgICAgPC9lbC1zcGxpdHRlcj5cbiAgICAgIDwvZWwtc3BsaXR0ZXItcGFuZWw+XG4gICAgPC9lbC1zcGxpdHRlcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBpc0NvbGxhcHNpYmxlID0gcmVmKHRydWUpXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLXBhbmVsIHtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XG4gIGhlaWdodDogMTAwJTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/splitter/collapsible.vue)_

vue

```
<template>
  <el-switch
    v-model="isCollapsible"
    active-text="enable"
    inactive-text="disable"
    inline-prompt
    class="mb-2"
  />
  <div
    style="height: 250px; box-shadow: var(--el-border-color-light) 0px 0px 10px"
  >
    <el-splitter>
      <el-splitter-panel :collapsible="isCollapsible" min="50">
        <div class="demo-panel">1</div>
      </el-splitter-panel>
      <el-splitter-panel :collapsible="isCollapsible">
        <div class="demo-panel">2</div>
      </el-splitter-panel>
      <el-splitter-panel>
        <div class="demo-panel">3</div>
      </el-splitter-panel>
      <el-splitter-panel :collapsible="isCollapsible">
        <el-splitter layout="vertical">
          <el-splitter-panel :collapsible="isCollapsible">
            <div class="demo-panel">4</div>
          </el-splitter-panel>
          <el-splitter-panel :collapsible="isCollapsible">
            <div class="demo-panel">5</div>
          </el-splitter-panel>
        </el-splitter>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isCollapsible = ref(true)
</script>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
```

隐藏源代码

## 禁用拖动 [​](#禁用拖动)

当任一面板禁用 `resizable` 时，拖拽功能将被禁用。

disable

1

drag disable

3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoXG4gICAgdi1tb2RlbD1cInJlc2l6YWJsZVwiXG4gICAgYWN0aXZlLXRleHQ9XCJlbmFibGVcIlxuICAgIGluYWN0aXZlLXRleHQ9XCJkaXNhYmxlXCJcbiAgICBpbmxpbmUtcHJvbXB0XG4gICAgY2xhc3M9XCJtYi0yXCJcbiAgLz5cbiAgPGRpdlxuICAgIHN0eWxlPVwiaGVpZ2h0OiAyNTBweDsgYm94LXNoYWRvdzogdmFyKC0tZWwtYm9yZGVyLWNvbG9yLWxpZ2h0KSAwcHggMHB4IDEwcHhcIlxuICA+XG4gICAgPGVsLXNwbGl0dGVyPlxuICAgICAgPGVsLXNwbGl0dGVyLXBhbmVsPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZGVtby1wYW5lbFwiPjE8L2Rpdj5cbiAgICAgIDwvZWwtc3BsaXR0ZXItcGFuZWw+XG4gICAgICA8ZWwtc3BsaXR0ZXItcGFuZWwgOnJlc2l6YWJsZT1cInJlc2l6YWJsZVwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZGVtby1wYW5lbFwiPlxuICAgICAgICAgIGRyYWcge3sgcmVzaXphYmxlID8gJ2VuYWJsZScgOiAnZGlzYWJsZScgfX1cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2VsLXNwbGl0dGVyLXBhbmVsPlxuICAgICAgPGVsLXNwbGl0dGVyLXBhbmVsPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZGVtby1wYW5lbFwiPjM8L2Rpdj5cbiAgICAgIDwvZWwtc3BsaXR0ZXItcGFuZWw+XG4gICAgPC9lbC1zcGxpdHRlcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCByZXNpemFibGUgPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLXBhbmVsIHtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XG4gIGhlaWdodDogMTAwJTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/splitter/disableDrag.vue)_

vue

```
<template>
  <el-switch
    v-model="resizable"
    active-text="enable"
    inactive-text="disable"
    inline-prompt
    class="mb-2"
  />
  <div
    style="height: 250px; box-shadow: var(--el-border-color-light) 0px 0px 10px"
  >
    <el-splitter>
      <el-splitter-panel>
        <div class="demo-panel">1</div>
      </el-splitter-panel>
      <el-splitter-panel :resizable="resizable">
        <div class="demo-panel">
          drag {{ resizable ? 'enable' : 'disable' }}
        </div>
      </el-splitter-panel>
      <el-splitter-panel>
        <div class="demo-panel">3</div>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const resizable = ref(false)
</script>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
```

隐藏源代码

## 面板大小 [​](#面板大小)

`v-model:size` 可以获取面板的大小。

1

100px

3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2XG4gICAgc3R5bGU9XCJoZWlnaHQ6IDI1MHB4OyBib3gtc2hhZG93OiB2YXIoLS1lbC1ib3JkZXItY29sb3ItbGlnaHQpIDBweCAwcHggMTBweFwiXG4gID5cbiAgICA8ZWwtc3BsaXR0ZXJcbiAgICAgIEByZXNpemUtc3RhcnQ9XCJoYW5kbGVSZXNpemVTdGFydFwiXG4gICAgICBAcmVzaXplLWVuZD1cImhhbmRsZVJlc2l6ZUVuZFwiXG4gICAgICBAcmVzaXplPVwiaGFuZGxlUmVzaXplXCJcbiAgICA+XG4gICAgICA8ZWwtc3BsaXR0ZXItcGFuZWw+XG4gICAgICAgIDxkaXYgY2xhc3M9XCJkZW1vLXBhbmVsXCI+MTwvZGl2PlxuICAgICAgPC9lbC1zcGxpdHRlci1wYW5lbD5cbiAgICAgIDxlbC1zcGxpdHRlci1wYW5lbCB2LW1vZGVsOnNpemU9XCJzaXplXCIgOm1heD1cIjIwMFwiIDptaW49XCI1MFwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZGVtby1wYW5lbFwiPnt7IHNpemUgfX1weDwvZGl2PlxuICAgICAgPC9lbC1zcGxpdHRlci1wYW5lbD5cbiAgICAgIDxlbC1zcGxpdHRlci1wYW5lbD5cbiAgICAgICAgPGRpdiBjbGFzcz1cImRlbW8tcGFuZWxcIj4zPC9kaXY+XG4gICAgICA8L2VsLXNwbGl0dGVyLXBhbmVsPlxuICAgIDwvZWwtc3BsaXR0ZXI+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3Qgc2l6ZSA9IHJlZigxMDApXG5cbmNvbnN0IGhhbmRsZVJlc2l6ZVN0YXJ0ID0gKGluZGV4OiBudW1iZXIsIHNpemVzOiBudW1iZXJbXSkgPT4ge1xuICBjb25zb2xlLmxvZygncmVzaXplU3RhcnQnLCBpbmRleCwgc2l6ZXMpXG59XG5cbmNvbnN0IGhhbmRsZVJlc2l6ZSA9IChpbmRleDogbnVtYmVyLCBzaXplczogbnVtYmVyW10pID0+IHtcbiAgY29uc29sZS5sb2coJ3Jlc2l6ZScsIGluZGV4LCBzaXplcylcbn1cblxuY29uc3QgaGFuZGxlUmVzaXplRW5kID0gKGluZGV4OiBudW1iZXIsIHNpemVzOiBudW1iZXJbXSkgPT4ge1xuICBjb25zb2xlLmxvZygncmVzaXplRW5kJywgaW5kZXgsIHNpemVzKVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1wYW5lbCB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGp1c3RpZnktY29udGVudDogY2VudGVyO1xuICBoZWlnaHQ6IDEwMCU7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/splitter/size.vue)_

vue

```
<template>
  <div
    style="height: 250px; box-shadow: var(--el-border-color-light) 0px 0px 10px"
  >
    <el-splitter
      @resize-start="handleResizeStart"
      @resize-end="handleResizeEnd"
      @resize="handleResize"
    >
      <el-splitter-panel>
        <div class="demo-panel">1</div>
      </el-splitter-panel>
      <el-splitter-panel v-model:size="size" :max="200" :min="50">
        <div class="demo-panel">{{ size }}px</div>
      </el-splitter-panel>
      <el-splitter-panel>
        <div class="demo-panel">3</div>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const size = ref(100)

const handleResizeStart = (index: number, sizes: number[]) => {
  console.log('resizeStart', index, sizes)
}

const handleResize = (index: number, sizes: number[]) => {
  console.log('resize', index, sizes)
}

const handleResizeEnd = (index: number, sizes: number[]) => {
  console.log('resizeEnd', index, sizes)
}
</script>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
```

隐藏源代码

## 延迟2.11.0 [​](#延迟)

当启用`lazy`时，面板大小将不会在拖动时实时更新，只能在拖动结束后更新。

1

2

3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2XG4gICAgc3R5bGU9XCJoZWlnaHQ6IDI1MHB4OyBib3gtc2hhZG93OiB2YXIoLS1lbC1ib3JkZXItY29sb3ItbGlnaHQpIDBweCAwcHggMTBweFwiXG4gID5cbiAgICA8ZWwtc3BsaXR0ZXIgbGF6eT5cbiAgICAgIDxlbC1zcGxpdHRlci1wYW5lbCBjb2xsYXBzaWJsZSBtaW49XCI1MFwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZGVtby1wYW5lbFwiPjE8L2Rpdj5cbiAgICAgIDwvZWwtc3BsaXR0ZXItcGFuZWw+XG4gICAgICA8ZWwtc3BsaXR0ZXItcGFuZWwgY29sbGFwc2libGU+XG4gICAgICAgIDxkaXYgY2xhc3M9XCJkZW1vLXBhbmVsXCI+MjwvZGl2PlxuICAgICAgPC9lbC1zcGxpdHRlci1wYW5lbD5cbiAgICAgIDxlbC1zcGxpdHRlci1wYW5lbCBjb2xsYXBzaWJsZT5cbiAgICAgICAgPGRpdiBjbGFzcz1cImRlbW8tcGFuZWxcIj4zPC9kaXY+XG4gICAgICA8L2VsLXNwbGl0dGVyLXBhbmVsPlxuICAgIDwvZWwtc3BsaXR0ZXI+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLXBhbmVsIHtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XG4gIGhlaWdodDogMTAwJTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/splitter/lazy.vue)_

vue

```
<template>
  <div
    style="height: 250px; box-shadow: var(--el-border-color-light) 0px 0px 10px"
  >
    <el-splitter lazy>
      <el-splitter-panel collapsible min="50">
        <div class="demo-panel">1</div>
      </el-splitter-panel>
      <el-splitter-panel collapsible>
        <div class="demo-panel">2</div>
      </el-splitter-panel>
      <el-splitter-panel collapsible>
        <div class="demo-panel">3</div>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
```

隐藏源代码

## Splitter API [​](#splitter-api)

### Splitter Attributes [​](#splitter-attributes)

| 名称 | 详情 | 类型 | 默认值 |
| --- | --- | --- | --- |
| layout | 分隔面板的布局方向 | `enum` | horizontal |
| lazy 2.11.0 | 是否使用懒加载 | `boolean` | false |

### Splitter Events [​](#splitter-events)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| resize-start | 开始调整面板大小时触发，`index` 是拖拽条的索引。 | `Function` |
| resize | 调整面板大小时触发，`index` 是拖拽条的索引。 | `Function` |
| resize-end | 面板调整大小结束时触发，`index` 是拖拽条的索引。 | `Function` |
| collapse 2.10.3 | 当面板折叠时触发，`index` 是拖拽条的索引。 | `Function` |

## SplitterPanel API [​](#splitterpanel-api)

### SplitterPanel Attributes [​](#splitterpanel-attributes)

| 名称 | 描述 | 类型 | 默认值 |
| --- | --- | --- | --- |
| size / v-model:size | 面板大小(像素或百分比) | `string` / `number` | \- |
| min | 面板最小尺寸(像素或百分比) | `string` / `number` | \- |
| max | 面板的最大尺寸(像素或百分比) | `string` / `number` | \- |
| resizable | 是否可以调整面板大小 | `boolean` | true |
| collapsible | 面板是否可折叠。 | `boolean` | false |

### SplitterPanel Events [​](#splitterpanel-events)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| update:size | 当面板大小改变时触发 | `Function` |

### SplitterPanel Slots [​](#splitterpanel-slots)

| 插槽名 | 详情 |
| --- | --- |
| default | 面板的默认内容 |
| start-collapsible | 自定义起始折叠按钮的内容 |
| end-collapsible | 结束可折叠按钮的自定义内容 |

### SplitterPanel Exposes [​](#splitterpanel-exposes)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| splitterPanelRef 2.11.9 | SplitterPanel html 元素 | `object` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/splitter) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/splitter.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/splitter.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/25793232?v=4&size=64)](https://github.com/Bigpawn)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/31533594?v=4&size=64)](https://github.com/Gnalvin)[![](https://avatars.githubusercontent.com/u/20151622?v=4&size=64)](https://github.com/william-xue)

[Space 间距](https://element-plus.org/zh-CN/component/space)

[Typography 排版](https://element-plus.org/zh-CN/component/typography)


