---
name: "infinite-scroll"
description: "Infinite Scroll 无限滚动 -- Element Plus Vue3 桌面端组件。Invoke when user needs Infinite Scroll 无限滚动 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/infinite-scroll.html"
---

---

废弃的 directive

我们将不再维护这个 directive。 会在 3.0.0 **被移除**，请使用 [el-scrollbar infinite scroll](https://element-plus.org/zh-CN/component/scrollbar#infinite-scroll) 作为代替。

# Infinite Scroll 无限滚动 [​](#infinite-scroll-无限滚动)

更新日志待解决

3

滚动至底部时，加载更多数据。

## 基础用法 [​](#基础用法)

在要实现滚动加载的列表上添加`v-infinite-scroll`，并赋值相应的加载方法，可实现滚动到底部时自动执行加载方法。

-   1
-   2
-   3
-   4
-   5
-   6

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8dWwgdi1pbmZpbml0ZS1zY3JvbGw9XCJsb2FkXCIgY2xhc3M9XCJpbmZpbml0ZS1saXN0XCIgc3R5bGU9XCJvdmVyZmxvdzogYXV0b1wiPlxuICAgIDxsaSB2LWZvcj1cImkgaW4gY291bnRcIiA6a2V5PVwiaVwiIGNsYXNzPVwiaW5maW5pdGUtbGlzdC1pdGVtXCI+e3sgaSB9fTwvbGk+XG4gIDwvdWw+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBjb3VudCA9IHJlZigwKVxuY29uc3QgbG9hZCA9ICgpID0+IHtcbiAgY291bnQudmFsdWUgKz0gMlxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5pbmZpbml0ZS1saXN0IHtcbiAgaGVpZ2h0OiAzMDBweDtcbiAgcGFkZGluZzogMDtcbiAgbWFyZ2luOiAwO1xuICBsaXN0LXN0eWxlOiBub25lO1xufVxuLmluZmluaXRlLWxpc3QgLmluZmluaXRlLWxpc3QtaXRlbSB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGp1c3RpZnktY29udGVudDogY2VudGVyO1xuICBoZWlnaHQ6IDUwcHg7XG4gIGJhY2tncm91bmQ6IHZhcigtLWVsLWNvbG9yLXByaW1hcnktbGlnaHQtOSk7XG4gIG1hcmdpbjogMTBweDtcbiAgY29sb3I6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xufVxuLmluZmluaXRlLWxpc3QgLmluZmluaXRlLWxpc3QtaXRlbSArIC5saXN0LWl0ZW0ge1xuICBtYXJnaW4tdG9wOiAxMHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/infinite-scroll/basic.vue)_

vue

```
<template>
  <ul v-infinite-scroll="load" class="infinite-list" style="overflow: auto">
    <li v-for="i in count" :key="i" class="infinite-list-item">{{ i }}</li>
  </ul>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const count = ref(0)
const load = () => {
  count.value += 2
}
</script>

<style>
.infinite-list {
  height: 300px;
  padding: 0;
  margin: 0;
  list-style: none;
}
.infinite-list .infinite-list-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  background: var(--el-color-primary-light-9);
  margin: 10px;
  color: var(--el-color-primary);
}
.infinite-list .infinite-list-item + .list-item {
  margin-top: 10px;
}
</style>
```

隐藏源代码

## 禁用加载 [​](#禁用加载)

-   1
-   2
-   3
-   4
-   5
-   6
-   7
-   8
-   9
-   10

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiaW5maW5pdGUtbGlzdC13cmFwcGVyXCIgc3R5bGU9XCJvdmVyZmxvdzogYXV0b1wiPlxuICAgIDx1bFxuICAgICAgdi1pbmZpbml0ZS1zY3JvbGw9XCJsb2FkXCJcbiAgICAgIGNsYXNzPVwibGlzdFwiXG4gICAgICA6aW5maW5pdGUtc2Nyb2xsLWRpc2FibGVkPVwiZGlzYWJsZWRcIlxuICAgID5cbiAgICAgIDxsaSB2LWZvcj1cImkgaW4gY291bnRcIiA6a2V5PVwiaVwiIGNsYXNzPVwibGlzdC1pdGVtXCI+e3sgaSB9fTwvbGk+XG4gICAgPC91bD5cbiAgICA8cCB2LWlmPVwibG9hZGluZ1wiPkxvYWRpbmcuLi48L3A+XG4gICAgPHAgdi1pZj1cIm5vTW9yZVwiPk5vIG1vcmU8L3A+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGNvbXB1dGVkLCByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNvdW50ID0gcmVmKDEwKVxuY29uc3QgbG9hZGluZyA9IHJlZihmYWxzZSlcbmNvbnN0IG5vTW9yZSA9IGNvbXB1dGVkKCgpID0+IGNvdW50LnZhbHVlID49IDIwKVxuY29uc3QgZGlzYWJsZWQgPSBjb21wdXRlZCgoKSA9PiBsb2FkaW5nLnZhbHVlIHx8IG5vTW9yZS52YWx1ZSlcbmNvbnN0IGxvYWQgPSAoKSA9PiB7XG4gIGxvYWRpbmcudmFsdWUgPSB0cnVlXG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGNvdW50LnZhbHVlICs9IDJcbiAgICBsb2FkaW5nLnZhbHVlID0gZmFsc2VcbiAgfSwgMjAwMClcbn1cbjwvc2NyaXB0PlxuXG48c3R5bGU+XG4uaW5maW5pdGUtbGlzdC13cmFwcGVyIHtcbiAgaGVpZ2h0OiAzMDBweDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xufVxuLmluZmluaXRlLWxpc3Qtd3JhcHBlciAubGlzdCB7XG4gIHBhZGRpbmc6IDA7XG4gIG1hcmdpbjogMDtcbiAgbGlzdC1zdHlsZTogbm9uZTtcbn1cblxuLmluZmluaXRlLWxpc3Qtd3JhcHBlciAubGlzdC1pdGVtIHtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XG4gIGhlaWdodDogNTBweDtcbiAgYmFja2dyb3VuZDogdmFyKC0tZWwtY29sb3ItZGFuZ2VyLWxpZ2h0LTkpO1xuICBjb2xvcjogdmFyKC0tZWwtY29sb3ItZGFuZ2VyKTtcbn1cbi5pbmZpbml0ZS1saXN0LXdyYXBwZXIgLmxpc3QtaXRlbSArIC5saXN0LWl0ZW0ge1xuICBtYXJnaW4tdG9wOiAxMHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/infinite-scroll/disable-loading.vue)_

vue

```
<template>
  <div class="infinite-list-wrapper" style="overflow: auto">
    <ul
      v-infinite-scroll="load"
      class="list"
      :infinite-scroll-disabled="disabled"
    >
      <li v-for="i in count" :key="i" class="list-item">{{ i }}</li>
    </ul>
    <p v-if="loading">Loading...</p>
    <p v-if="noMore">No more</p>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'

const count = ref(10)
const loading = ref(false)
const noMore = computed(() => count.value >= 20)
const disabled = computed(() => loading.value || noMore.value)
const load = () => {
  loading.value = true
  setTimeout(() => {
    count.value += 2
    loading.value = false
  }, 2000)
}
</script>

<style>
.infinite-list-wrapper {
  height: 300px;
  text-align: center;
}
.infinite-list-wrapper .list {
  padding: 0;
  margin: 0;
  list-style: none;
}

.infinite-list-wrapper .list-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  background: var(--el-color-danger-light-9);
  color: var(--el-color-danger);
}
.infinite-list-wrapper .list-item + .list-item {
  margin-top: 10px;
}
</style>
```

隐藏源代码

## 指令 [​](#指令)

| 属性 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| v-infinite-scroll | 滚动到底部时，加载更多数据 | `Function` | — |
| infinite-scroll-disabled | 是否禁用 | `boolean` | false |
| infinite-scroll-delay | 节流时延，单位为ms | `number` | 200 |
| infinite-scroll-distance | 触发加载的距离阈值，单位为px | `number` | 0 |
| infinite-scroll-immediate | 是否立即执行加载方法，以防初始状态下内容无法撑满容器。 | `boolean` | true |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/infinite-scroll) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/infinite-scroll.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/infinite-scroll.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/132551120?v=4&size=64)](https://github.com/YiMo1)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/48023419?v=4&size=64)](https://github.com/uncledrewzhaopeng)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)

[Image 图片](https://element-plus.org/zh-CN/component/image)

[Pagination 分页](https://element-plus.org/zh-CN/component/pagination)


