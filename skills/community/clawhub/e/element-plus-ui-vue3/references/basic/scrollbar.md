---
name: "scrollbar"
description: "Scrollbar 滚动条 -- Element Plus Vue3 桌面端组件。Invoke when user needs Scrollbar 滚动条 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/scrollbar.html"
---

---

# Scrollbar 滚动条 [​](#scrollbar-滚动条)

更新日志待解决

22

用于替换浏览器原生滚动条。

## 基础用法 [​](#基础用法)

通过 `height` 属性设置滚动条高度，若不设置则根据父容器高度自适应。

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2Nyb2xsYmFyIGhlaWdodD1cIjQwMHB4XCI+XG4gICAgPHAgdi1mb3I9XCJpdGVtIGluIDIwXCIgOmtleT1cIml0ZW1cIiBjbGFzcz1cInNjcm9sbGJhci1kZW1vLWl0ZW1cIj57eyBpdGVtIH19PC9wPlxuICA8L2VsLXNjcm9sbGJhcj5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG4uc2Nyb2xsYmFyLWRlbW8taXRlbSB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGp1c3RpZnktY29udGVudDogY2VudGVyO1xuICBoZWlnaHQ6IDUwcHg7XG4gIG1hcmdpbjogMTBweDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBib3JkZXItcmFkaXVzOiA0cHg7XG4gIGJhY2tncm91bmQ6IHZhcigtLWVsLWNvbG9yLXByaW1hcnktbGlnaHQtOSk7XG4gIGNvbG9yOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/scrollbar/basic-usage.vue)_

vue

```
<template>
  <el-scrollbar height="400px">
    <p v-for="item in 20" :key="item" class="scrollbar-demo-item">{{ item }}</p>
  </el-scrollbar>
</template>

<style scoped>
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
</style>
```

隐藏源代码

## 横向滚动 [​](#横向滚动)

当元素宽度大于滚动条宽度时，会显示横向滚动条。

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2Nyb2xsYmFyPlxuICAgIDxkaXYgY2xhc3M9XCJzY3JvbGxiYXItZmxleC1jb250ZW50XCI+XG4gICAgICA8cCB2LWZvcj1cIml0ZW0gaW4gNTBcIiA6a2V5PVwiaXRlbVwiIGNsYXNzPVwic2Nyb2xsYmFyLWRlbW8taXRlbVwiPlxuICAgICAgICB7eyBpdGVtIH19XG4gICAgICA8L3A+XG4gICAgPC9kaXY+XG4gIDwvZWwtc2Nyb2xsYmFyPlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlIHNjb3BlZD5cbi5zY3JvbGxiYXItZmxleC1jb250ZW50IHtcbiAgZGlzcGxheTogZmxleDtcbiAgd2lkdGg6IGZpdC1jb250ZW50O1xufVxuLnNjcm9sbGJhci1kZW1vLWl0ZW0ge1xuICBmbGV4LXNocmluazogMDtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XG4gIHdpZHRoOiAxMDBweDtcbiAgaGVpZ2h0OiA1MHB4O1xuICBtYXJnaW46IDEwcHg7XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbiAgYm9yZGVyLXJhZGl1czogNHB4O1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1lbC1jb2xvci1kYW5nZXItbGlnaHQtOSk7XG4gIGNvbG9yOiB2YXIoLS1lbC1jb2xvci1kYW5nZXIpO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/scrollbar/horizontal-scroll.vue)_

vue

```
<template>
  <el-scrollbar>
    <div class="scrollbar-flex-content">
      <p v-for="item in 50" :key="item" class="scrollbar-demo-item">
        {{ item }}
      </p>
    </div>
  </el-scrollbar>
</template>

<style scoped>
.scrollbar-flex-content {
  display: flex;
  width: fit-content;
}
.scrollbar-demo-item {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-danger-light-9);
  color: var(--el-color-danger);
}
</style>
```

隐藏源代码

## 最大高度 [​](#最大高度)

当元素高度超过最大高度，才会显示滚动条。

Add ItemDelete Item

1

2

3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIEBjbGljaz1cImFkZFwiPkFkZCBJdGVtPC9lbC1idXR0b24+XG4gIDxlbC1idXR0b24gQGNsaWNrPVwib25EZWxldGVcIj5EZWxldGUgSXRlbTwvZWwtYnV0dG9uPlxuICA8ZWwtc2Nyb2xsYmFyIG1heC1oZWlnaHQ9XCI0MDBweFwiPlxuICAgIDxwIHYtZm9yPVwiaXRlbSBpbiBjb3VudFwiIDprZXk9XCJpdGVtXCIgY2xhc3M9XCJzY3JvbGxiYXItZGVtby1pdGVtXCI+XG4gICAgICB7eyBpdGVtIH19XG4gICAgPC9wPlxuICA8L2VsLXNjcm9sbGJhcj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNvdW50ID0gcmVmKDMpXG5cbmNvbnN0IGFkZCA9ICgpID0+IHtcbiAgY291bnQudmFsdWUrK1xufVxuY29uc3Qgb25EZWxldGUgPSAoKSA9PiB7XG4gIGlmIChjb3VudC52YWx1ZSA+IDApIHtcbiAgICBjb3VudC52YWx1ZS0tXG4gIH1cbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLnNjcm9sbGJhci1kZW1vLWl0ZW0ge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgaGVpZ2h0OiA1MHB4O1xuICBtYXJnaW46IDEwcHg7XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbiAgYm9yZGVyLXJhZGl1czogNHB4O1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5LWxpZ2h0LTkpO1xuICBjb2xvcjogdmFyKC0tZWwtY29sb3ItcHJpbWFyeSk7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/scrollbar/max-height.vue)_

vue

```
<template>
  <el-button @click="add">Add Item</el-button>
  <el-button @click="onDelete">Delete Item</el-button>
  <el-scrollbar max-height="400px">
    <p v-for="item in count" :key="item" class="scrollbar-demo-item">
      {{ item }}
    </p>
  </el-scrollbar>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const count = ref(3)

const add = () => {
  count.value++
}
const onDelete = () => {
  if (count.value > 0) {
    count.value--
  }
}
</script>

<style scoped>
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
</style>
```

隐藏源代码

## 手动滚动 [​](#手动滚动)

通过使用 `setScrollTop` 与 `setScrollLeft` 方法，可以手动控制滚动条滚动。

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2Nyb2xsYmFyIHJlZj1cInNjcm9sbGJhclJlZlwiIGhlaWdodD1cIjQwMHB4XCIgYWx3YXlzIEBzY3JvbGw9XCJzY3JvbGxcIj5cbiAgICA8ZGl2IHJlZj1cImlubmVyUmVmXCI+XG4gICAgICA8cCB2LWZvcj1cIml0ZW0gaW4gMjBcIiA6a2V5PVwiaXRlbVwiIGNsYXNzPVwic2Nyb2xsYmFyLWRlbW8taXRlbVwiPlxuICAgICAgICB7eyBpdGVtIH19XG4gICAgICA8L3A+XG4gICAgPC9kaXY+XG4gIDwvZWwtc2Nyb2xsYmFyPlxuXG4gIDxlbC1zbGlkZXJcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIDptYXg9XCJtYXhcIlxuICAgIDpmb3JtYXQtdG9vbHRpcD1cImZvcm1hdFRvb2x0aXBcIlxuICAgIEBpbnB1dD1cImlucHV0U2xpZGVyXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBvbk1vdW50ZWQsIHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBTY3JvbGxiYXJJbnN0YW5jZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxudHlwZSBBcnJheWFibGU8VD4gPSBUIHwgVFtdXG5cbmNvbnN0IG1heCA9IHJlZigwKVxuY29uc3QgdmFsdWUgPSByZWYoMClcbmNvbnN0IGlubmVyUmVmID0gcmVmPEhUTUxEaXZFbGVtZW50PigpXG5jb25zdCBzY3JvbGxiYXJSZWYgPSByZWY8U2Nyb2xsYmFySW5zdGFuY2U+KClcblxub25Nb3VudGVkKCgpID0+IHtcbiAgbWF4LnZhbHVlID0gaW5uZXJSZWYudmFsdWUhLmNsaWVudEhlaWdodCAtIDM4MFxufSlcblxuY29uc3QgaW5wdXRTbGlkZXIgPSAodmFsdWU6IEFycmF5YWJsZTxudW1iZXI+KSA9PiB7XG4gIHNjcm9sbGJhclJlZi52YWx1ZSEuc2V0U2Nyb2xsVG9wKHZhbHVlIGFzIG51bWJlcilcbn1cbmNvbnN0IHNjcm9sbCA9ICh7IHNjcm9sbFRvcCB9OiB7IHNjcm9sbFRvcDogbnVtYmVyIH0pID0+IHtcbiAgdmFsdWUudmFsdWUgPSBzY3JvbGxUb3Bcbn1cbmNvbnN0IGZvcm1hdFRvb2x0aXAgPSAodmFsdWU6IG51bWJlcikgPT4gYCR7dmFsdWV9IHB4YFxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uc2Nyb2xsYmFyLWRlbW8taXRlbSB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGp1c3RpZnktY29udGVudDogY2VudGVyO1xuICBoZWlnaHQ6IDUwcHg7XG4gIG1hcmdpbjogMTBweDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBib3JkZXItcmFkaXVzOiA0cHg7XG4gIGJhY2tncm91bmQ6IHZhcigtLWVsLWNvbG9yLXByaW1hcnktbGlnaHQtOSk7XG4gIGNvbG9yOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbn1cbi5lbC1zbGlkZXIge1xuICBtYXJnaW4tdG9wOiAyMHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/scrollbar/manual-scroll.vue)_

vue

```
<template>
  <el-scrollbar ref="scrollbarRef" height="400px" always @scroll="scroll">
    <div ref="innerRef">
      <p v-for="item in 20" :key="item" class="scrollbar-demo-item">
        {{ item }}
      </p>
    </div>
  </el-scrollbar>

  <el-slider
    v-model="value"
    :max="max"
    :format-tooltip="formatTooltip"
    @input="inputSlider"
  />
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

import type { ScrollbarInstance } from 'element-plus'

type Arrayable<T> = T | T[]

const max = ref(0)
const value = ref(0)
const innerRef = ref<HTMLDivElement>()
const scrollbarRef = ref<ScrollbarInstance>()

onMounted(() => {
  max.value = innerRef.value!.clientHeight - 380
})

const inputSlider = (value: Arrayable<number>) => {
  scrollbarRef.value!.setScrollTop(value as number)
}
const scroll = ({ scrollTop }: { scrollTop: number }) => {
  value.value = scrollTop
}
const formatTooltip = (value: number) => `${value} px`
</script>

<style scoped>
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
.el-slider {
  margin-top: 20px;
}
</style>
```

隐藏源代码

## 无限滚动2.10.0 [​](#无限滚动)

`end-reached` 是在滚动条到达底部时触发的。 它可以用作无限滚动。

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2Nyb2xsYmFyIGhlaWdodD1cIjQwMHB4XCIgQGVuZC1yZWFjaGVkPVwibG9hZE1vcmVcIj5cbiAgICA8cCB2LWZvcj1cIml0ZW0gaW4gbnVtXCIgOmtleT1cIml0ZW1cIiBjbGFzcz1cInNjcm9sbGJhci1kZW1vLWl0ZW1cIj5cbiAgICAgIHt7IGl0ZW0gfX1cbiAgICA8L3A+XG4gIDwvZWwtc2Nyb2xsYmFyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBTY3JvbGxiYXJEaXJlY3Rpb24gfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IG51bSA9IHJlZigzMClcblxuY29uc3QgbG9hZE1vcmUgPSAoZGlyZWN0aW9uOiBTY3JvbGxiYXJEaXJlY3Rpb24pID0+IHtcbiAgaWYgKGRpcmVjdGlvbiA9PT0gJ2JvdHRvbScpIHtcbiAgICBudW0udmFsdWUgKz0gNVxuICB9XG59XG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5zY3JvbGxiYXItZGVtby1pdGVtIHtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XG4gIGhlaWdodDogNTBweDtcbiAgbWFyZ2luOiAxMHB4O1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIGJvcmRlci1yYWRpdXM6IDRweDtcbiAgYmFja2dyb3VuZDogdmFyKC0tZWwtY29sb3ItcHJpbWFyeS1saWdodC05KTtcbiAgY29sb3I6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xufVxuLmVsLXNsaWRlciB7XG4gIG1hcmdpbi10b3A6IDIwcHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/scrollbar/infinite-scroll.vue)_

vue

```
<template>
  <el-scrollbar height="400px" @end-reached="loadMore">
    <p v-for="item in num" :key="item" class="scrollbar-demo-item">
      {{ item }}
    </p>
  </el-scrollbar>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { ScrollbarDirection } from 'element-plus'

const num = ref(30)

const loadMore = (direction: ScrollbarDirection) => {
  if (direction === 'bottom') {
    num.value += 5
  }
}
</script>

<style scoped>
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
.el-slider {
  margin-top: 20px;
}
</style>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| height | 滚动条高度 | `string` / `number` | — |
| max-height | 滚动条最大高度 | `string` / `number` | — |
| native | 是否使用原生滚动条样式 | `boolean` | false |
| wrap-style | 包裹容器的自定义样式 | `string` / `object` | — |
| wrap-class | 包裹容器的自定义类名 | `string` | — |
| view-style | 视图的自定义样式 | `string` / `object` | — |
| view-class | 视图的自定义类名 | `string` | — |
| noresize | 不响应容器尺寸变化，如果容器尺寸不会发生变化，最好设置它可以优化性能 | `boolean` | false |
| tag | 视图的元素标签 | `string` | div |
| always | 滚动条总是显示 | `boolean` | false |
| min-size | 滚动条最小尺寸 | `number` | 20 |
| id 2.4.0 | 视图ID | `string` | — |
| role 2.4.0 a11y | 视图的角色 | `string` | — |
| aria-label 2.4.0 a11y | 视图的 aria-label | `string` | — |
| aria-orientation 2.4.0 a11y | 视图的 aria-orientation | `enum` | — |
| tabindex 2.8.3 | 容器的tabindex | `number` / `string` | — |
| distance 2.10.5 | 触发到达底部事件的距离（像素） | `number` | 0 |

### Events [​](#events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| scroll | 当触发滚动事件时，返回滚动的距离 | `Function` |
| end-reached 2.10.0 | 触发滚动结束时的触发器 | `Function` |

### Slots [​](#slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

### Exposes [​](#exposes)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| handleScroll | 触发滚动事件 | `Function` |
| scrollTo | 滚动到一组特定坐标 | `Function` |
| setScrollTop | 设置滚动条到顶部的距离 | `Function` |
| setScrollLeft | 设置滚动条到左边的距离 | `Function` |
| update | 手动更新滚动条状态 | `Function` |
| wrapRef | 滚动条包裹的 ref 对象 | `object` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/scrollbar) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/scrollbar.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/scrollbar.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/62818957?v=4&size=64)](https://github.com/ZacharyBear)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/33646534?v=4&size=64)](https://github.com/SevenDreamYang)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/24290011?v=4&size=64)](https://github.com/xingyixiang)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)

[Text 文本](https://element-plus.org/zh-CN/component/text)

[Space 间距](https://element-plus.org/zh-CN/component/space)


