---
name: "menu"
description: "Menu 菜单 -- Element Plus Vue3 桌面端组件。Invoke when user needs Menu 菜单 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/menu.html"
---

---

# Menu 菜单 [​](#menu-菜单)

更新日志待解决

60

为网站提供导航功能的菜单。

TIP

如果您想要覆盖el-menu的默认高度, 您可以使用下列CSS

css

```
.el-menu--horizontal {
  --el-menu-horizontal-height: 100px;
}
```

## 顶栏 [​](#顶栏)

顶部栏菜单可以在各种场景中使用。

导航菜单默认为垂直模式，通过将 mode 属性设置为 horizontal 来使导航菜单变更为水平模式。 另外，在菜单中通过 sub-menu 组件可以生成二级菜单。 Menu 还提供了`background-color`、`text-color`和`active-text-color`，分别用于设置菜单的背景色、菜单的文字颜色和当前激活菜单的文字颜色。

-   Processing Center
-   Workspace

-   Info
-   Orders

-   Processing Center
-   Workspace

-   Info
-   Orders

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtbWVudVxuICAgIDpkZWZhdWx0LWFjdGl2ZT1cImFjdGl2ZUluZGV4XCJcbiAgICBjbGFzcz1cImVsLW1lbnUtZGVtb1wiXG4gICAgbW9kZT1cImhvcml6b250YWxcIlxuICAgIEBzZWxlY3Q9XCJoYW5kbGVTZWxlY3RcIlxuICA+XG4gICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjFcIj5Qcm9jZXNzaW5nIENlbnRlcjwvZWwtbWVudS1pdGVtPlxuICAgIDxlbC1zdWItbWVudSBpbmRleD1cIjJcIj5cbiAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+V29ya3NwYWNlPC90ZW1wbGF0ZT5cbiAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTFcIj5pdGVtIG9uZTwvZWwtbWVudS1pdGVtPlxuICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjItMlwiPml0ZW0gdHdvPC9lbC1tZW51LWl0ZW0+XG4gICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMi0zXCI+aXRlbSB0aHJlZTwvZWwtbWVudS1pdGVtPlxuICAgICAgPGVsLXN1Yi1tZW51IGluZGV4PVwiMi00XCI+XG4gICAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+aXRlbSBmb3VyPC90ZW1wbGF0ZT5cbiAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjItNC0xXCI+aXRlbSBvbmU8L2VsLW1lbnUtaXRlbT5cbiAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjItNC0yXCI+aXRlbSB0d288L2VsLW1lbnUtaXRlbT5cbiAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjItNC0zXCI+aXRlbSB0aHJlZTwvZWwtbWVudS1pdGVtPlxuICAgICAgPC9lbC1zdWItbWVudT5cbiAgICA8L2VsLXN1Yi1tZW51PlxuICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIzXCIgZGlzYWJsZWQ+SW5mbzwvZWwtbWVudS1pdGVtPlxuICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCI0XCI+T3JkZXJzPC9lbC1tZW51LWl0ZW0+XG4gIDwvZWwtbWVudT5cbiAgPGRpdiBjbGFzcz1cImgtNlwiIC8+XG4gIDxlbC1tZW51XG4gICAgOmRlZmF1bHQtYWN0aXZlPVwiYWN0aXZlSW5kZXgyXCJcbiAgICBjbGFzcz1cImVsLW1lbnUtZGVtb1wiXG4gICAgbW9kZT1cImhvcml6b250YWxcIlxuICAgIGJhY2tncm91bmQtY29sb3I9XCIjNTQ1YzY0XCJcbiAgICB0ZXh0LWNvbG9yPVwiI2ZmZlwiXG4gICAgYWN0aXZlLXRleHQtY29sb3I9XCIjZmZkMDRiXCJcbiAgICBAc2VsZWN0PVwiaGFuZGxlU2VsZWN0XCJcbiAgPlxuICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIxXCI+UHJvY2Vzc2luZyBDZW50ZXI8L2VsLW1lbnUtaXRlbT5cbiAgICA8ZWwtc3ViLW1lbnUgaW5kZXg9XCIyXCI+XG4gICAgICA8dGVtcGxhdGUgI3RpdGxlPldvcmtzcGFjZTwvdGVtcGxhdGU+XG4gICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMi0xXCI+aXRlbSBvbmU8L2VsLW1lbnUtaXRlbT5cbiAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTJcIj5pdGVtIHR3bzwvZWwtbWVudS1pdGVtPlxuICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjItM1wiPml0ZW0gdGhyZWU8L2VsLW1lbnUtaXRlbT5cbiAgICAgIDxlbC1zdWItbWVudSBpbmRleD1cIjItNFwiPlxuICAgICAgICA8dGVtcGxhdGUgI3RpdGxlPml0ZW0gZm91cjwvdGVtcGxhdGU+XG4gICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTQtMVwiPml0ZW0gb25lPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTQtMlwiPml0ZW0gdHdvPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTQtM1wiPml0ZW0gdGhyZWU8L2VsLW1lbnUtaXRlbT5cbiAgICAgIDwvZWwtc3ViLW1lbnU+XG4gICAgPC9lbC1zdWItbWVudT5cbiAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiM1wiIGRpc2FibGVkPkluZm88L2VsLW1lbnUtaXRlbT5cbiAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiNFwiPk9yZGVyczwvZWwtbWVudS1pdGVtPlxuICA8L2VsLW1lbnU+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBhY3RpdmVJbmRleCA9IHJlZignMScpXG5jb25zdCBhY3RpdmVJbmRleDIgPSByZWYoJzEnKVxuY29uc3QgaGFuZGxlU2VsZWN0ID0gKGtleTogc3RyaW5nLCBrZXlQYXRoOiBzdHJpbmdbXSkgPT4ge1xuICBjb25zb2xlLmxvZyhrZXksIGtleVBhdGgpXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/menu/basic.vue)_

vue

```
<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
  >
    <el-menu-item index="1">Processing Center</el-menu-item>
    <el-sub-menu index="2">
      <template #title>Workspace</template>
      <el-menu-item index="2-1">item one</el-menu-item>
      <el-menu-item index="2-2">item two</el-menu-item>
      <el-menu-item index="2-3">item three</el-menu-item>
      <el-sub-menu index="2-4">
        <template #title>item four</template>
        <el-menu-item index="2-4-1">item one</el-menu-item>
        <el-menu-item index="2-4-2">item two</el-menu-item>
        <el-menu-item index="2-4-3">item three</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-menu-item index="3" disabled>Info</el-menu-item>
    <el-menu-item index="4">Orders</el-menu-item>
  </el-menu>
  <div class="h-6" />
  <el-menu
    :default-active="activeIndex2"
    class="el-menu-demo"
    mode="horizontal"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
    @select="handleSelect"
  >
    <el-menu-item index="1">Processing Center</el-menu-item>
    <el-sub-menu index="2">
      <template #title>Workspace</template>
      <el-menu-item index="2-1">item one</el-menu-item>
      <el-menu-item index="2-2">item two</el-menu-item>
      <el-menu-item index="2-3">item three</el-menu-item>
      <el-sub-menu index="2-4">
        <template #title>item four</template>
        <el-menu-item index="2-4-1">item one</el-menu-item>
        <el-menu-item index="2-4-2">item two</el-menu-item>
        <el-menu-item index="2-4-3">item three</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-menu-item index="3" disabled>Info</el-menu-item>
    <el-menu-item index="4">Orders</el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeIndex = ref('1')
const activeIndex2 = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>
```

隐藏源代码

## 左右 [​](#左右)

您可以将菜单项放置在左边或右边。

-   ![Element logo](https://element-plus.org/images/element-plus-logo.svg)
-   Processing Center
-   Workspace

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtbWVudVxuICAgIDpkZWZhdWx0LWFjdGl2ZT1cImFjdGl2ZUluZGV4XCJcbiAgICBjbGFzcz1cImVsLW1lbnUtZGVtb1wiXG4gICAgbW9kZT1cImhvcml6b250YWxcIlxuICAgIDplbGxpcHNpcz1cImZhbHNlXCJcbiAgICBAc2VsZWN0PVwiaGFuZGxlU2VsZWN0XCJcbiAgPlxuICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIwXCI+XG4gICAgICA8aW1nXG4gICAgICAgIHN0eWxlPVwid2lkdGg6IDEwMHB4XCJcbiAgICAgICAgc3JjPVwiL2ltYWdlcy9lbGVtZW50LXBsdXMtbG9nby5zdmdcIlxuICAgICAgICBhbHQ9XCJFbGVtZW50IGxvZ29cIlxuICAgICAgLz5cbiAgICA8L2VsLW1lbnUtaXRlbT5cbiAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMVwiPlByb2Nlc3NpbmcgQ2VudGVyPC9lbC1tZW51LWl0ZW0+XG4gICAgPGVsLXN1Yi1tZW51IGluZGV4PVwiMlwiPlxuICAgICAgPHRlbXBsYXRlICN0aXRsZT5Xb3Jrc3BhY2U8L3RlbXBsYXRlPlxuICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjItMVwiPml0ZW0gb25lPC9lbC1tZW51LWl0ZW0+XG4gICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMi0yXCI+aXRlbSB0d288L2VsLW1lbnUtaXRlbT5cbiAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTNcIj5pdGVtIHRocmVlPC9lbC1tZW51LWl0ZW0+XG4gICAgICA8ZWwtc3ViLW1lbnUgaW5kZXg9XCIyLTRcIj5cbiAgICAgICAgPHRlbXBsYXRlICN0aXRsZT5pdGVtIGZvdXI8L3RlbXBsYXRlPlxuICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMi00LTFcIj5pdGVtIG9uZTwvZWwtbWVudS1pdGVtPlxuICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMi00LTJcIj5pdGVtIHR3bzwvZWwtbWVudS1pdGVtPlxuICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMi00LTNcIj5pdGVtIHRocmVlPC9lbC1tZW51LWl0ZW0+XG4gICAgICA8L2VsLXN1Yi1tZW51PlxuICAgIDwvZWwtc3ViLW1lbnU+XG4gIDwvZWwtbWVudT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGFjdGl2ZUluZGV4ID0gcmVmKCcxJylcbmNvbnN0IGhhbmRsZVNlbGVjdCA9IChrZXk6IHN0cmluZywga2V5UGF0aDogc3RyaW5nW10pID0+IHtcbiAgY29uc29sZS5sb2coa2V5LCBrZXlQYXRoKVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZWwtbWVudS0taG9yaXpvbnRhbCA+IC5lbC1tZW51LWl0ZW06bnRoLWNoaWxkKDEpIHtcbiAgbWFyZ2luLXJpZ2h0OiBhdXRvO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/menu/left-and-right.vue)_

vue

```
<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false"
    @select="handleSelect"
  >
    <el-menu-item index="0">
      <img
        style="width: 100px"
        src="/images/element-plus-logo.svg"
        alt="Element logo"
      />
    </el-menu-item>
    <el-menu-item index="1">Processing Center</el-menu-item>
    <el-sub-menu index="2">
      <template #title>Workspace</template>
      <el-menu-item index="2-1">item one</el-menu-item>
      <el-menu-item index="2-2">item two</el-menu-item>
      <el-menu-item index="2-3">item three</el-menu-item>
      <el-sub-menu index="2-4">
        <template #title>item four</template>
        <el-menu-item index="2-4-1">item one</el-menu-item>
        <el-menu-item index="2-4-2">item two</el-menu-item>
        <el-menu-item index="2-4-3">item three</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style scoped>
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}
</style>
```

隐藏源代码

## 侧栏 [​](#侧栏)

垂直菜单，可内嵌子菜单。

通过 el-menu-item-group 组件可以实现菜单进行分组，分组名可以通过 title 属性直接设定，也可以通过具名 slot 来设定。

##### Default colors

-   Navigator One

    -   Group One

        -   item one
        -   item two
    -   Group Two

        -   item three
    -   item four

        -   item one
-   Navigator Two
-   Navigator Three
-   Navigator Four

##### Custom colors

-   Navigator One

    -   Group One

        -   item one
        -   item two
    -   Group Two

        -   item three
    -   item four

        -   item one
-   Navigator Two
-   Navigator Three
-   Navigator Four

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IGNsYXNzPVwidGFjXCI+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjEyXCI+XG4gICAgICA8aDUgY2xhc3M9XCJtYi0yXCI+RGVmYXVsdCBjb2xvcnM8L2g1PlxuICAgICAgPGVsLW1lbnVcbiAgICAgICAgZGVmYXVsdC1hY3RpdmU9XCIyXCJcbiAgICAgICAgY2xhc3M9XCJlbC1tZW51LXZlcnRpY2FsLWRlbW9cIlxuICAgICAgICBAb3Blbj1cImhhbmRsZU9wZW5cIlxuICAgICAgICBAY2xvc2U9XCJoYW5kbGVDbG9zZVwiXG4gICAgICA+XG4gICAgICAgIDxlbC1zdWItbWVudSBpbmRleD1cIjFcIj5cbiAgICAgICAgICA8dGVtcGxhdGUgI3RpdGxlPlxuICAgICAgICAgICAgPGVsLWljb24+PGxvY2F0aW9uIC8+PC9lbC1pY29uPlxuICAgICAgICAgICAgPHNwYW4+TmF2aWdhdG9yIE9uZTwvc3Bhbj5cbiAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICAgIDxlbC1tZW51LWl0ZW0tZ3JvdXAgdGl0bGU9XCJHcm91cCBPbmVcIj5cbiAgICAgICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIxLTFcIj5pdGVtIG9uZTwvZWwtbWVudS1pdGVtPlxuICAgICAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjEtMlwiPml0ZW0gdHdvPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgICAgPC9lbC1tZW51LWl0ZW0tZ3JvdXA+XG4gICAgICAgICAgPGVsLW1lbnUtaXRlbS1ncm91cCB0aXRsZT1cIkdyb3VwIFR3b1wiPlxuICAgICAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjEtM1wiPml0ZW0gdGhyZWU8L2VsLW1lbnUtaXRlbT5cbiAgICAgICAgICA8L2VsLW1lbnUtaXRlbS1ncm91cD5cbiAgICAgICAgICA8ZWwtc3ViLW1lbnUgaW5kZXg9XCIxLTRcIj5cbiAgICAgICAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+aXRlbSBmb3VyPC90ZW1wbGF0ZT5cbiAgICAgICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIxLTQtMVwiPml0ZW0gb25lPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgICAgPC9lbC1zdWItbWVudT5cbiAgICAgICAgPC9lbC1zdWItbWVudT5cbiAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjJcIj5cbiAgICAgICAgICA8ZWwtaWNvbj48aWNvbi1tZW51IC8+PC9lbC1pY29uPlxuICAgICAgICAgIDxzcGFuPk5hdmlnYXRvciBUd288L3NwYW4+XG4gICAgICAgIDwvZWwtbWVudS1pdGVtPlxuICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiM1wiIGRpc2FibGVkPlxuICAgICAgICAgIDxlbC1pY29uPjxkb2N1bWVudCAvPjwvZWwtaWNvbj5cbiAgICAgICAgICA8c3Bhbj5OYXZpZ2F0b3IgVGhyZWU8L3NwYW4+XG4gICAgICAgIDwvZWwtbWVudS1pdGVtPlxuICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiNFwiPlxuICAgICAgICAgIDxlbC1pY29uPjxzZXR0aW5nIC8+PC9lbC1pY29uPlxuICAgICAgICAgIDxzcGFuPk5hdmlnYXRvciBGb3VyPC9zcGFuPlxuICAgICAgICA8L2VsLW1lbnUtaXRlbT5cbiAgICAgIDwvZWwtbWVudT5cbiAgICA8L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpzcGFuPVwiMTJcIj5cbiAgICAgIDxoNSBjbGFzcz1cIm1iLTJcIj5DdXN0b20gY29sb3JzPC9oNT5cbiAgICAgIDxlbC1tZW51XG4gICAgICAgIGFjdGl2ZS10ZXh0LWNvbG9yPVwiI2ZmZDA0YlwiXG4gICAgICAgIGJhY2tncm91bmQtY29sb3I9XCIjNTQ1YzY0XCJcbiAgICAgICAgY2xhc3M9XCJlbC1tZW51LXZlcnRpY2FsLWRlbW9cIlxuICAgICAgICBkZWZhdWx0LWFjdGl2ZT1cIjJcIlxuICAgICAgICB0ZXh0LWNvbG9yPVwiI2ZmZlwiXG4gICAgICAgIEBvcGVuPVwiaGFuZGxlT3BlblwiXG4gICAgICAgIEBjbG9zZT1cImhhbmRsZUNsb3NlXCJcbiAgICAgID5cbiAgICAgICAgPGVsLXN1Yi1tZW51IGluZGV4PVwiMVwiPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+XG4gICAgICAgICAgICA8ZWwtaWNvbj48bG9jYXRpb24gLz48L2VsLWljb24+XG4gICAgICAgICAgICA8c3Bhbj5OYXZpZ2F0b3IgT25lPC9zcGFuPlxuICAgICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgICAgPGVsLW1lbnUtaXRlbS1ncm91cCB0aXRsZT1cIkdyb3VwIE9uZVwiPlxuICAgICAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjEtMVwiPml0ZW0gb25lPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMS0yXCI+aXRlbSB0d288L2VsLW1lbnUtaXRlbT5cbiAgICAgICAgICA8L2VsLW1lbnUtaXRlbS1ncm91cD5cbiAgICAgICAgICA8ZWwtbWVudS1pdGVtLWdyb3VwIHRpdGxlPVwiR3JvdXAgVHdvXCI+XG4gICAgICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMS0zXCI+aXRlbSB0aHJlZTwvZWwtbWVudS1pdGVtPlxuICAgICAgICAgIDwvZWwtbWVudS1pdGVtLWdyb3VwPlxuICAgICAgICAgIDxlbC1zdWItbWVudSBpbmRleD1cIjEtNFwiPlxuICAgICAgICAgICAgPHRlbXBsYXRlICN0aXRsZT5pdGVtIGZvdXI8L3RlbXBsYXRlPlxuICAgICAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjEtNC0xXCI+aXRlbSBvbmU8L2VsLW1lbnUtaXRlbT5cbiAgICAgICAgICA8L2VsLXN1Yi1tZW51PlxuICAgICAgICA8L2VsLXN1Yi1tZW51PlxuICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMlwiPlxuICAgICAgICAgIDxlbC1pY29uPjxpY29uLW1lbnUgLz48L2VsLWljb24+XG4gICAgICAgICAgPHNwYW4+TmF2aWdhdG9yIFR3bzwvc3Bhbj5cbiAgICAgICAgPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIzXCIgZGlzYWJsZWQ+XG4gICAgICAgICAgPGVsLWljb24+PGRvY3VtZW50IC8+PC9lbC1pY29uPlxuICAgICAgICAgIDxzcGFuPk5hdmlnYXRvciBUaHJlZTwvc3Bhbj5cbiAgICAgICAgPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCI0XCI+XG4gICAgICAgICAgPGVsLWljb24+PHNldHRpbmcgLz48L2VsLWljb24+XG4gICAgICAgICAgPHNwYW4+TmF2aWdhdG9yIEZvdXI8L3NwYW4+XG4gICAgICAgIDwvZWwtbWVudS1pdGVtPlxuICAgICAgPC9lbC1tZW51PlxuICAgIDwvZWwtY29sPlxuICA8L2VsLXJvdz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQge1xuICBEb2N1bWVudCxcbiAgTWVudSBhcyBJY29uTWVudSxcbiAgTG9jYXRpb24sXG4gIFNldHRpbmcsXG59IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5jb25zdCBoYW5kbGVPcGVuID0gKGtleTogc3RyaW5nLCBrZXlQYXRoOiBzdHJpbmdbXSkgPT4ge1xuICBjb25zb2xlLmxvZyhrZXksIGtleVBhdGgpXG59XG5jb25zdCBoYW5kbGVDbG9zZSA9IChrZXk6IHN0cmluZywga2V5UGF0aDogc3RyaW5nW10pID0+IHtcbiAgY29uc29sZS5sb2coa2V5LCBrZXlQYXRoKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/menu/vertical.vue)_

vue

```
<template>
  <el-row class="tac">
    <el-col :span="12">
      <h5 class="mb-2">Default colors</h5>
      <el-menu
        default-active="2"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-sub-menu index="1">
          <template #title>
            <el-icon><location /></el-icon>
            <span>Navigator One</span>
          </template>
          <el-menu-item-group title="Group One">
            <el-menu-item index="1-1">item one</el-menu-item>
            <el-menu-item index="1-2">item two</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="Group Two">
            <el-menu-item index="1-3">item three</el-menu-item>
          </el-menu-item-group>
          <el-sub-menu index="1-4">
            <template #title>item four</template>
            <el-menu-item index="1-4-1">item one</el-menu-item>
          </el-sub-menu>
        </el-sub-menu>
        <el-menu-item index="2">
          <el-icon><icon-menu /></el-icon>
          <span>Navigator Two</span>
        </el-menu-item>
        <el-menu-item index="3" disabled>
          <el-icon><document /></el-icon>
          <span>Navigator Three</span>
        </el-menu-item>
        <el-menu-item index="4">
          <el-icon><setting /></el-icon>
          <span>Navigator Four</span>
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col :span="12">
      <h5 class="mb-2">Custom colors</h5>
      <el-menu
        active-text-color="#ffd04b"
        background-color="#545c64"
        class="el-menu-vertical-demo"
        default-active="2"
        text-color="#fff"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-sub-menu index="1">
          <template #title>
            <el-icon><location /></el-icon>
            <span>Navigator One</span>
          </template>
          <el-menu-item-group title="Group One">
            <el-menu-item index="1-1">item one</el-menu-item>
            <el-menu-item index="1-2">item two</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="Group Two">
            <el-menu-item index="1-3">item three</el-menu-item>
          </el-menu-item-group>
          <el-sub-menu index="1-4">
            <template #title>item four</template>
            <el-menu-item index="1-4-1">item one</el-menu-item>
          </el-sub-menu>
        </el-sub-menu>
        <el-menu-item index="2">
          <el-icon><icon-menu /></el-icon>
          <span>Navigator Two</span>
        </el-menu-item>
        <el-menu-item index="3" disabled>
          <el-icon><document /></el-icon>
          <span>Navigator Three</span>
        </el-menu-item>
        <el-menu-item index="4">
          <el-icon><setting /></el-icon>
          <span>Navigator Four</span>
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>
```

隐藏源代码

## Collapse 折叠面板 [​](#collapse-折叠面板)

垂直导航菜单可以被折叠

expandcollapse

-   Navigator One

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cImlzQ29sbGFwc2VcIiBzdHlsZT1cIm1hcmdpbi1ib3R0b206IDIwcHhcIj5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIDp2YWx1ZT1cImZhbHNlXCI+ZXhwYW5kPC9lbC1yYWRpby1idXR0b24+XG4gICAgPGVsLXJhZGlvLWJ1dHRvbiA6dmFsdWU9XCJ0cnVlXCI+Y29sbGFwc2U8L2VsLXJhZGlvLWJ1dHRvbj5cbiAgPC9lbC1yYWRpby1ncm91cD5cbiAgPGVsLW1lbnVcbiAgICBkZWZhdWx0LWFjdGl2ZT1cIjJcIlxuICAgIGNsYXNzPVwiZWwtbWVudS12ZXJ0aWNhbC1kZW1vXCJcbiAgICA6Y29sbGFwc2U9XCJpc0NvbGxhcHNlXCJcbiAgICBAb3Blbj1cImhhbmRsZU9wZW5cIlxuICAgIEBjbG9zZT1cImhhbmRsZUNsb3NlXCJcbiAgPlxuICAgIDxlbC1zdWItbWVudSBpbmRleD1cIjFcIj5cbiAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+XG4gICAgICAgIDxlbC1pY29uPjxsb2NhdGlvbiAvPjwvZWwtaWNvbj5cbiAgICAgICAgPHNwYW4+TmF2aWdhdG9yIE9uZTwvc3Bhbj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8ZWwtbWVudS1pdGVtLWdyb3VwPlxuICAgICAgICA8dGVtcGxhdGUgI3RpdGxlPjxzcGFuPkdyb3VwIE9uZTwvc3Bhbj48L3RlbXBsYXRlPlxuICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMS0xXCI+aXRlbSBvbmU8L2VsLW1lbnUtaXRlbT5cbiAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjEtMlwiPml0ZW0gdHdvPC9lbC1tZW51LWl0ZW0+XG4gICAgICA8L2VsLW1lbnUtaXRlbS1ncm91cD5cbiAgICAgIDxlbC1tZW51LWl0ZW0tZ3JvdXAgdGl0bGU9XCJHcm91cCBUd29cIj5cbiAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjEtM1wiPml0ZW0gdGhyZWU8L2VsLW1lbnUtaXRlbT5cbiAgICAgIDwvZWwtbWVudS1pdGVtLWdyb3VwPlxuICAgICAgPGVsLXN1Yi1tZW51IGluZGV4PVwiMS00XCI+XG4gICAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+PHNwYW4+aXRlbSBmb3VyPC9zcGFuPjwvdGVtcGxhdGU+XG4gICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIxLTQtMVwiPml0ZW0gb25lPC9lbC1tZW51LWl0ZW0+XG4gICAgICA8L2VsLXN1Yi1tZW51PlxuICAgIDwvZWwtc3ViLW1lbnU+XG4gICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjJcIj5cbiAgICAgIDxlbC1pY29uPjxpY29uLW1lbnUgLz48L2VsLWljb24+XG4gICAgICA8dGVtcGxhdGUgI3RpdGxlPk5hdmlnYXRvciBUd288L3RlbXBsYXRlPlxuICAgIDwvZWwtbWVudS1pdGVtPlxuICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIzXCIgZGlzYWJsZWQ+XG4gICAgICA8ZWwtaWNvbj48ZG9jdW1lbnQgLz48L2VsLWljb24+XG4gICAgICA8dGVtcGxhdGUgI3RpdGxlPk5hdmlnYXRvciBUaHJlZTwvdGVtcGxhdGU+XG4gICAgPC9lbC1tZW51LWl0ZW0+XG4gICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjRcIj5cbiAgICAgIDxlbC1pY29uPjxzZXR0aW5nIC8+PC9lbC1pY29uPlxuICAgICAgPHRlbXBsYXRlICN0aXRsZT5OYXZpZ2F0b3IgRm91cjwvdGVtcGxhdGU+XG4gICAgPC9lbC1tZW51LWl0ZW0+XG4gIDwvZWwtbWVudT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQge1xuICBEb2N1bWVudCxcbiAgTWVudSBhcyBJY29uTWVudSxcbiAgTG9jYXRpb24sXG4gIFNldHRpbmcsXG59IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5jb25zdCBpc0NvbGxhcHNlID0gcmVmKHRydWUpXG5jb25zdCBoYW5kbGVPcGVuID0gKGtleTogc3RyaW5nLCBrZXlQYXRoOiBzdHJpbmdbXSkgPT4ge1xuICBjb25zb2xlLmxvZyhrZXksIGtleVBhdGgpXG59XG5jb25zdCBoYW5kbGVDbG9zZSA9IChrZXk6IHN0cmluZywga2V5UGF0aDogc3RyaW5nW10pID0+IHtcbiAgY29uc29sZS5sb2coa2V5LCBrZXlQYXRoKVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5lbC1tZW51LXZlcnRpY2FsLWRlbW86bm90KC5lbC1tZW51LS1jb2xsYXBzZSkge1xuICB3aWR0aDogMjAwcHg7XG4gIG1pbi1oZWlnaHQ6IDQwMHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/menu/collapse.vue)_

vue

```
<template>
  <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
    <el-radio-button :value="false">expand</el-radio-button>
    <el-radio-button :value="true">collapse</el-radio-button>
  </el-radio-group>
  <el-menu
    default-active="2"
    class="el-menu-vertical-demo"
    :collapse="isCollapse"
    @open="handleOpen"
    @close="handleClose"
  >
    <el-sub-menu index="1">
      <template #title>
        <el-icon><location /></el-icon>
        <span>Navigator One</span>
      </template>
      <el-menu-item-group>
        <template #title><span>Group One</span></template>
        <el-menu-item index="1-1">item one</el-menu-item>
        <el-menu-item index="1-2">item two</el-menu-item>
      </el-menu-item-group>
      <el-menu-item-group title="Group Two">
        <el-menu-item index="1-3">item three</el-menu-item>
      </el-menu-item-group>
      <el-sub-menu index="1-4">
        <template #title><span>item four</span></template>
        <el-menu-item index="1-4-1">item one</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-menu-item index="2">
      <el-icon><icon-menu /></el-icon>
      <template #title>Navigator Two</template>
    </el-menu-item>
    <el-menu-item index="3" disabled>
      <el-icon><document /></el-icon>
      <template #title>Navigator Three</template>
    </el-menu-item>
    <el-menu-item index="4">
      <el-icon><setting /></el-icon>
      <template #title>Navigator Four</template>
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'

const isCollapse = ref(true)
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>
```

隐藏源代码

## 弹出层偏移量 2.4.4 [​](#弹出层偏移量)

当提供了 popperOffset 配置，会覆盖 Menu 的 `popper-offset`.

-   Processing Center
-   Workspace

-   Override Popper Offset

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtbWVudVxuICAgIGVsbGlwc2lzXG4gICAgY2xhc3M9XCJlbC1tZW51LXBvcHBlci1kZW1vXCJcbiAgICBtb2RlPVwiaG9yaXpvbnRhbFwiXG4gICAgOnBvcHBlci1vZmZzZXQ9XCIxNlwiXG4gICAgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCJcbiAgPlxuICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIxXCI+UHJvY2Vzc2luZyBDZW50ZXI8L2VsLW1lbnUtaXRlbT5cbiAgICA8ZWwtc3ViLW1lbnUgaW5kZXg9XCIyXCI+XG4gICAgICA8dGVtcGxhdGUgI3RpdGxlPldvcmtzcGFjZTwvdGVtcGxhdGU+XG4gICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMi0xXCI+aXRlbSBvbmU8L2VsLW1lbnUtaXRlbT5cbiAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTJcIj5pdGVtIHR3bzwvZWwtbWVudS1pdGVtPlxuICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjItM1wiPml0ZW0gdGhyZWU8L2VsLW1lbnUtaXRlbT5cbiAgICAgIDxlbC1zdWItbWVudSBpbmRleD1cIjItNFwiPlxuICAgICAgICA8dGVtcGxhdGUgI3RpdGxlPml0ZW0gZm91cjwvdGVtcGxhdGU+XG4gICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTQtMVwiPml0ZW0gb25lPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTQtMlwiPml0ZW0gdHdvPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTQtM1wiPml0ZW0gdGhyZWU8L2VsLW1lbnUtaXRlbT5cbiAgICAgIDwvZWwtc3ViLW1lbnU+XG4gICAgPC9lbC1zdWItbWVudT5cbiAgICA8ZWwtc3ViLW1lbnUgaW5kZXg9XCIzXCIgOnBvcHBlci1vZmZzZXQ9XCI4XCI+XG4gICAgICA8dGVtcGxhdGUgI3RpdGxlPk92ZXJyaWRlIFBvcHBlciBPZmZzZXQ8L3RlbXBsYXRlPlxuICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjMtMVwiPml0ZW0gb25lPC9lbC1tZW51LWl0ZW0+XG4gICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMy0yXCI+aXRlbSB0d288L2VsLW1lbnUtaXRlbT5cbiAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIzLTNcIj5pdGVtIHRocmVlPC9lbC1tZW51LWl0ZW0+XG4gICAgICA8ZWwtc3ViLW1lbnUgaW5kZXg9XCIzLTRcIiA6cG9wcGVyLW9mZnNldD1cIjIwXCI+XG4gICAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+b3ZlcnJpZGUgY2hpbGQ8L3RlbXBsYXRlPlxuICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMy00LTFcIj5pdGVtIG9uZTwvZWwtbWVudS1pdGVtPlxuICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMy00LTJcIj5pdGVtIHR3bzwvZWwtbWVudS1pdGVtPlxuICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMy00LTNcIj5pdGVtIHRocmVlPC9lbC1tZW51LWl0ZW0+XG4gICAgICA8L2VsLXN1Yi1tZW51PlxuICAgIDwvZWwtc3ViLW1lbnU+XG4gICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjRcIiBkaXNhYmxlZD5JbmZvPC9lbC1tZW51LWl0ZW0+XG4gICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjVcIj5PcmRlcnM8L2VsLW1lbnUtaXRlbT5cbiAgPC9lbC1tZW51PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/menu/popper-offset.vue)_

vue

```
<template>
  <el-menu
    ellipsis
    class="el-menu-popper-demo"
    mode="horizontal"
    :popper-offset="16"
    style="max-width: 600px"
  >
    <el-menu-item index="1">Processing Center</el-menu-item>
    <el-sub-menu index="2">
      <template #title>Workspace</template>
      <el-menu-item index="2-1">item one</el-menu-item>
      <el-menu-item index="2-2">item two</el-menu-item>
      <el-menu-item index="2-3">item three</el-menu-item>
      <el-sub-menu index="2-4">
        <template #title>item four</template>
        <el-menu-item index="2-4-1">item one</el-menu-item>
        <el-menu-item index="2-4-2">item two</el-menu-item>
        <el-menu-item index="2-4-3">item three</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-sub-menu index="3" :popper-offset="8">
      <template #title>Override Popper Offset</template>
      <el-menu-item index="3-1">item one</el-menu-item>
      <el-menu-item index="3-2">item two</el-menu-item>
      <el-menu-item index="3-3">item three</el-menu-item>
      <el-sub-menu index="3-4" :popper-offset="20">
        <template #title>override child</template>
        <el-menu-item index="3-4-1">item one</el-menu-item>
        <el-menu-item index="3-4-2">item two</el-menu-item>
        <el-menu-item index="3-4-3">item three</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-menu-item index="4" disabled>Info</el-menu-item>
    <el-menu-item index="5">Orders</el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup></script>
```

隐藏源代码

## 菜单 API [​](#菜单-api)

### Menu Attributes [​](#menu-attributes)

| 属性名 | 说明 | 类型 | Default |
| --- | --- | --- | --- |
| mode | 菜单展示模式 | `enum` | vertical |
| collapse | 是否水平折叠收起菜单（仅在 mode 为 vertical 时可用） | `boolean` | false |
| ellipsis | 是否省略多余的子项（仅在横向模式生效） | `boolean` | true |
| ellipsis-icon 2.4.4 | 自定义省略图标 (仅在水平模式下可用) | `string` / `Component` | — |
| popper-offset 2.4.4 | 弹出层的偏移量(对所有子菜单有效) | `number` | 6 |
| default-active | 页面加载时默认激活菜单的 index | `string` | '' |
| default-openeds | 默认打开的 sub-menu 的 index 的数组 | `array` | \[\] |
| unique-opened | 是否只保持一个子菜单的展开 | `boolean` | false |
| menu-trigger | 子菜单打开的触发方式，只在 `mode` 为 horizontal 时有效。 | `enum` | hover |
| router | 是否启用 `vue-router` 模式。 启用该模式会在激活导航时以 index 作为 path 进行路由跳转 使用 `default-active` 来设置加载时的激活项。 | `boolean` | false |
| collapse-transition | 是否开启折叠动画 | `boolean` | true |
| popper-effect 2.2.26 | Tooltip 主题，内置了 `dark` / `light` 两种主题，当菜单折叠时生效。 | `enum` / `string` | dark |
| close-on-click-outside 2.4.4 | 可选，单击外部时是否折叠菜单 | `boolean` | false |
| popper-class 2.5.0 | 用于所有弹出菜单和标题提示的自定义类名 | `string` | — |
| popper-style 2.11.5 | 用于所有弹出菜单和标题提示的自定义样式 | `string` / `object` | — |
| show-timeout 2.5.0 | 菜单出现前的延迟 | `number` | 300 |
| hide-timeout 2.5.0 | 菜单消失前的延迟 | `number` | 300 |
| background-color deprecated | 菜单的背景颜色 (十六进制格式) (推荐在样式类中使用 `--el-menu-bg-color`) | `string` | #ffffff |
| text-color deprecated | 菜单的文字颜色 (十六进制格式) (推荐在样式类中使用 `--el-menu-text-color`) | `string` | #303133 |
| active-text-color deprecated | 活动菜单项的文本颜色（十六进制格式）（推荐使用 css var `--el-menu-active-color`） | `string` | #409eff |
| persistent 2.9.5 | 当菜单处于非活动状态且 `persistent` 为 `false` 时，下拉菜单将被销毁 | `boolean` | true |

### Menu Events [​](#menu-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| select | 菜单激活回调 | `Function` |
| open | sub-menu 展开的回调 | `Function` |
| close | sub-menu 收起的回调 | `Function` |

### Menu Slots [​](#menu-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | SubMenu / Menu-Item / Menu-Item-Group |

### Menu Exposes [​](#menu-exposes)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| open | 打开一个特定的子菜单，参数是要打开的子菜单的索引 | `Function` |
| close | 关闭一个特定的子菜单，参数是要关闭子菜单的索引 | `Function` |
| handleResize | 手动触发菜单宽度重新计算 | `Function` |
| updateActiveIndex 2.9.8 | 通过索引激活指定菜单 | `Function` |

## SubMenu API [​](#submenu-api)

### SubMenu Attributes [​](#submenu-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| index required | 唯一标志 | `string` | — |
| popper-class | 为 popper 添加类名 | `string` | — |
| popper-style 2.11.5 | 为 popper 添加自定义样式 | `string` / `object` | — |
| show-timeout | 子菜单出现之前的延迟，(继承 menu 的 `show-timeout` 配置) | `number` | — |
| hide-timeout | 子菜单消失之前的延迟，(继承 menu 的 `hide-timeout` 配置) | `number` | — |
| disabled | 是否禁用 | `boolean` | false |
| teleported | 是否将弹出菜单挂载到 body 上，第一级SubMenu默认值为 true，其他SubMenus 的值为 false | `boolean` | undefined |
| popper-offset | 弹出窗口的偏移量 (覆盖 `popper`的菜单) | `number` | — |
| expand-close-icon | 父菜单展开且子菜单关闭时的图标， `expand-close-icon` 和 `expand-open-icon` 需要一起配置才能生效 | `string` / `Component` | — |
| expand-open-icon | 父菜单展开且子菜单打开时的图标， `expand-open-icon` 和 `expand-close-icon` 需要一起配置才能生效 | `string` / `Component` | — |
| collapse-close-icon | 父菜单收起且子菜单关闭时的图标， `collapse-close-icon` 和 `collapse-open-icon` 需要一起配置才能生效 | `string` / `Component` | — |
| collapse-open-icon | 父菜单收起且子菜单打开时的图标， `collapse-open-icon` 和 `collapse-close-icon` 需要一起配置才能生效 | `string` / `Component` | — |

### SubMenu Slots [​](#submenu-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | SubMenu / Menu-Item / Menu-Item-Group |
| title | 自定义标题内容 | — |

## Menu-Item API [​](#menu-item-api)

### Menu-Item Attributes [​](#menu-item-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| index required | 唯一标志 | `string` | — |
| route | Vue Route 路由位置参数 | `string` / `object` | — |
| disabled | 是否禁用 | `boolean` | false |

### Menu-Item Events [​](#menu-item-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| click | 点击菜单项时回调函数, 参数为菜单项实例 | `Function` |

### Menu-Item Slots [​](#menu-item-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |
| title | 自定义标题内容 |

## Menu-Item-Group API [​](#menu-item-group-api)

### Menu-Item-Group Attributes [​](#menu-item-group-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| title | 组标题 | `string` | — |

### Menu-Item-Group Slots [​](#menu-item-group-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 默认插槽内容 | Menu-Item |
| title | 自定义组标题内容 | — |

## 类型声明 [​](#类型声明)

显示类型声明

ts

```
/**
 * @param index index of activated menu
 * @param indexPath index path of activated menu
 * @param item the selected menu item
 * @param routerResult result returned by `vue-router` if `router` is enabled
 */
type MenuSelectEvent = (
  index: string,
  indexPath: string[],
  item: MenuItemClicked,
  routerResult?: Promise<void | NavigationFailure>
) => void

/**
 * @param index index of expanded sub-menu
 * @param indexPath index path of expanded sub-menu
 */
type MenuOpenEvent = (index: string, indexPath: string[]) => void

/**
 * @param index index of collapsed sub-menu
 * @param indexPath index path of collapsed sub-menu
 */
type MenuCloseEvent = (index: string, indexPath: string[]) => void

interface MenuItemRegistered {
  index: string
  indexPath: string[]
  active: boolean
}

interface MenuItemClicked {
  index: string
  indexPath: string[]
  route?: RouteLocationRaw
}
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/menu) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/menu.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/menu.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/17698194?v=4&size=64)](https://github.com/nieyuyao)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/41532842?v=4&size=64)](https://github.com/feiyuOL)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/59312002?v=4&size=64)](https://github.com/meet-student)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/30396440?v=4&size=64)](https://github.com/wen-lun)[![](https://avatars.githubusercontent.com/u/19513904?v=4&size=64)](https://github.com/ShirleyYoung19)[![](https://avatars.githubusercontent.com/u/148513444?v=4&size=64)](https://github.com/ikkkp)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/102006695?v=4&size=64)](https://github.com/cuongle-hdwebsoft)[![](https://avatars.githubusercontent.com/u/26295849?v=4&size=64)](https://github.com/CeceWall)[![](https://avatars.githubusercontent.com/u/36811055?v=4&size=64)](https://github.com/iDestin)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/19643456?v=4&size=64)](https://github.com/ParkerFiend)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)[![](https://avatars.githubusercontent.com/u/63504321?v=4&size=64)](https://github.com/Lucky-Ya-Q)[![](https://avatars.githubusercontent.com/u/87300515?v=4&size=64)](https://github.com/WindBearr)[![](https://avatars.githubusercontent.com/u/49601167?v=4&size=64)](https://github.com/jianjunyuu)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/26268346?v=4&size=64)](https://github.com/Jimmyzm)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/15604293?v=4&size=64)](https://github.com/Liiked)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/9036838?v=4&size=64)](https://github.com/jiankian)[![](https://avatars.githubusercontent.com/u/45283723?v=4&size=64)](https://github.com/oliver139)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/58544605?v=4&size=64)](https://github.com/dan-sotnik)[![](https://avatars.githubusercontent.com/u/128784464?v=4&size=64)](https://github.com/super622)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/16005946?v=4&size=64)](https://github.com/jpenna)[![](https://avatars.githubusercontent.com/u/63645337?v=4&size=64)](https://github.com/baboon-king)

[Dropdown 下拉菜单](https://element-plus.org/zh-CN/component/dropdown)

[Page Header 页头](https://element-plus.org/zh-CN/component/page-header)


