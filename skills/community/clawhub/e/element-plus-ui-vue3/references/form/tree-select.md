---
name: "tree-select"
description: "TreeSelect 树形选择 -- Element Plus Vue3 桌面端组件。Invoke when user needs TreeSelect 树形选择 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/tree-select.html"
---

---

# TreeSelect 树形选择 [​](#treeselect-树形选择)

更新日志待解决

22

含有下拉菜单的树形选择器，结合了 `el-tree` 和 `el-select` 两个组件的功能。

## 基础用法 [​](#基础用法)

树状选择器

Select

show checkbox:

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS1zZWxlY3RcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOnJlbmRlci1hZnRlci1leHBhbmQ9XCJmYWxzZVwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAvPlxuICA8ZWwtZGl2aWRlciAvPlxuICBzaG93IGNoZWNrYm94OlxuICA8ZWwtdHJlZS1zZWxlY3RcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOnJlbmRlci1hZnRlci1leHBhbmQ9XCJmYWxzZVwiXG4gICAgc2hvdy1jaGVja2JveFxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKClcblxuY29uc3QgZGF0YSA9IFtcbiAge1xuICAgIHZhbHVlOiAnMScsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICcxLTEnLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAxLTEnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMS0xLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAxLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnMicsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMicsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICcyLTEnLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAyLTEnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMi0xLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAyLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnMi0yJyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJzItMi0xJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMi0yLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJzMnLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDMnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnMy0xJyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJzMtMS0xJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMy0xLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJzMtMicsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDMtMicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICczLTItMScsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-select/basic.vue)_

vue

```
<template>
  <el-tree-select
    v-model="value"
    :data="data"
    :render-after-expand="false"
    style="width: 240px"
  />
  <el-divider />
  show checkbox:
  <el-tree-select
    v-model="value"
    :data="data"
    :render-after-expand="false"
    show-checkbox
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()

const data = [
  {
    value: '1',
    label: 'Level one 1',
    children: [
      {
        value: '1-1',
        label: 'Level two 1-1',
        children: [
          {
            value: '1-1-1',
            label: 'Level three 1-1-1',
          },
        ],
      },
    ],
  },
  {
    value: '2',
    label: 'Level one 2',
    children: [
      {
        value: '2-1',
        label: 'Level two 2-1',
        children: [
          {
            value: '2-1-1',
            label: 'Level three 2-1-1',
          },
        ],
      },
      {
        value: '2-2',
        label: 'Level two 2-2',
        children: [
          {
            value: '2-2-1',
            label: 'Level three 2-2-1',
          },
        ],
      },
    ],
  },
  {
    value: '3',
    label: 'Level one 3',
    children: [
      {
        value: '3-1',
        label: 'Level two 3-1',
        children: [
          {
            value: '3-1-1',
            label: 'Level three 3-1-1',
          },
        ],
      },
      {
        value: '3-2',
        label: 'Level two 3-2',
        children: [
          {
            value: '3-2-1',
            label: 'Level three 3-2-1',
          },
        ],
      },
    ],
  },
]
</script>
```

隐藏源代码

## 选择任意级别 [​](#选择任意级别)

当属性 `check-strictly=true` 时，任何节点都可以被选择，否则只有子节点可被选择。

TIP

当使用 `show-checkbox`时，由于 `check-on-click-node` 默认值是 false，这时候只能通过 checkbox 来选中，当然您也可以将其设置成 true，这样点击整个 node 都可以用来完成选择

Select

show checkbox:

Select

show checkbox with \`check-on-click-node\`:

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS1zZWxlY3RcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgY2hlY2stc3RyaWN0bHlcbiAgICA6cmVuZGVyLWFmdGVyLWV4cGFuZD1cImZhbHNlXCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gIC8+XG4gIDxlbC1kaXZpZGVyIC8+XG4gIHNob3cgY2hlY2tib3g6XG4gIDxlbC10cmVlLXNlbGVjdFxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICBjaGVjay1zdHJpY3RseVxuICAgIDpyZW5kZXItYWZ0ZXItZXhwYW5kPVwiZmFsc2VcIlxuICAgIHNob3ctY2hlY2tib3hcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gIC8+XG4gIDxlbC1kaXZpZGVyIC8+XG4gIHNob3cgY2hlY2tib3ggd2l0aCBgY2hlY2stb24tY2xpY2stbm9kZWA6XG4gIDxlbC10cmVlLXNlbGVjdFxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICBjaGVjay1zdHJpY3RseVxuICAgIDpyZW5kZXItYWZ0ZXItZXhwYW5kPVwiZmFsc2VcIlxuICAgIHNob3ctY2hlY2tib3hcbiAgICBjaGVjay1vbi1jbGljay1ub2RlXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoKVxuXG5jb25zdCBkYXRhID0gW1xuICB7XG4gICAgdmFsdWU6ICcxJyxcbiAgICBsYWJlbDogJ0xldmVsIG9uZSAxJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJzEtMScsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDEtMScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICcxLTEtMScsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDEtMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICcyJyxcbiAgICBsYWJlbDogJ0xldmVsIG9uZSAyJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJzItMScsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDItMScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICcyLTEtMScsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDItMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICcyLTInLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAyLTInLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMi0yLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAyLTItMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnMycsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMycsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICczLTEnLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAzLTEnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMy0xLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAzLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnMy0yJyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJzMtMi0xJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMy0yLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-select/check-strictly.vue)_

vue

```
<template>
  <el-tree-select
    v-model="value"
    :data="data"
    check-strictly
    :render-after-expand="false"
    style="width: 240px"
  />
  <el-divider />
  show checkbox:
  <el-tree-select
    v-model="value"
    :data="data"
    check-strictly
    :render-after-expand="false"
    show-checkbox
    style="width: 240px"
  />
  <el-divider />
  show checkbox with `check-on-click-node`:
  <el-tree-select
    v-model="value"
    :data="data"
    check-strictly
    :render-after-expand="false"
    show-checkbox
    check-on-click-node
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()

const data = [
  {
    value: '1',
    label: 'Level one 1',
    children: [
      {
        value: '1-1',
        label: 'Level two 1-1',
        children: [
          {
            value: '1-1-1',
            label: 'Level three 1-1-1',
          },
        ],
      },
    ],
  },
  {
    value: '2',
    label: 'Level one 2',
    children: [
      {
        value: '2-1',
        label: 'Level two 2-1',
        children: [
          {
            value: '2-1-1',
            label: 'Level three 2-1-1',
          },
        ],
      },
      {
        value: '2-2',
        label: 'Level two 2-2',
        children: [
          {
            value: '2-2-1',
            label: 'Level three 2-2-1',
          },
        ],
      },
    ],
  },
  {
    value: '3',
    label: 'Level one 3',
    children: [
      {
        value: '3-1',
        label: 'Level two 3-1',
        children: [
          {
            value: '3-1-1',
            label: 'Level three 3-1-1',
          },
        ],
      },
      {
        value: '3-2',
        label: 'Level two 3-2',
        children: [
          {
            value: '3-2-1',
            label: 'Level three 3-2-1',
          },
        ],
      },
    ],
  },
]
</script>
```

隐藏源代码

WARNING

在使用 show-checkbox 时，因为 `check-on-click-leaf` 默认值为 true， 最后一个树节点可以通过点击节点进行勾选。

## 多选 [​](#多选)

通过点击或复选框选择多个选项。

Select

show checkbox:

Select

show checkbox with \`check-strictly\`:

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS1zZWxlY3RcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgbXVsdGlwbGVcbiAgICA6cmVuZGVyLWFmdGVyLWV4cGFuZD1cImZhbHNlXCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gIC8+XG4gIDxlbC1kaXZpZGVyIC8+XG4gIHNob3cgY2hlY2tib3g6XG4gIDxlbC10cmVlLXNlbGVjdFxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICBtdWx0aXBsZVxuICAgIDpyZW5kZXItYWZ0ZXItZXhwYW5kPVwiZmFsc2VcIlxuICAgIHNob3ctY2hlY2tib3hcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gIC8+XG4gIDxlbC1kaXZpZGVyIC8+XG4gIHNob3cgY2hlY2tib3ggd2l0aCBgY2hlY2stc3RyaWN0bHlgOlxuICA8ZWwtdHJlZS1zZWxlY3RcbiAgICB2LW1vZGVsPVwidmFsdWVTdHJpY3RseVwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICBtdWx0aXBsZVxuICAgIDpyZW5kZXItYWZ0ZXItZXhwYW5kPVwiZmFsc2VcIlxuICAgIHNob3ctY2hlY2tib3hcbiAgICBjaGVjay1zdHJpY3RseVxuICAgIGNoZWNrLW9uLWNsaWNrLW5vZGVcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZigpXG5jb25zdCB2YWx1ZVN0cmljdGx5ID0gcmVmKClcblxuY29uc3QgZGF0YSA9IFtcbiAge1xuICAgIHZhbHVlOiAnMScsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICcxLTEnLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAxLTEnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMS0xLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAxLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnMicsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMicsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICcyLTEnLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAyLTEnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMi0xLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAyLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnMi0yJyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJzItMi0xJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMi0yLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJzMnLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDMnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnMy0xJyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJzMtMS0xJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMy0xLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJzMtMicsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDMtMicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICczLTItMScsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-select/multiple.vue)_

vue

```
<template>
  <el-tree-select
    v-model="value"
    :data="data"
    multiple
    :render-after-expand="false"
    style="width: 240px"
  />
  <el-divider />
  show checkbox:
  <el-tree-select
    v-model="value"
    :data="data"
    multiple
    :render-after-expand="false"
    show-checkbox
    style="width: 240px"
  />
  <el-divider />
  show checkbox with `check-strictly`:
  <el-tree-select
    v-model="valueStrictly"
    :data="data"
    multiple
    :render-after-expand="false"
    show-checkbox
    check-strictly
    check-on-click-node
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()
const valueStrictly = ref()

const data = [
  {
    value: '1',
    label: 'Level one 1',
    children: [
      {
        value: '1-1',
        label: 'Level two 1-1',
        children: [
          {
            value: '1-1-1',
            label: 'Level three 1-1-1',
          },
        ],
      },
    ],
  },
  {
    value: '2',
    label: 'Level one 2',
    children: [
      {
        value: '2-1',
        label: 'Level two 2-1',
        children: [
          {
            value: '2-1-1',
            label: 'Level three 2-1-1',
          },
        ],
      },
      {
        value: '2-2',
        label: 'Level two 2-2',
        children: [
          {
            value: '2-2-1',
            label: 'Level three 2-2-1',
          },
        ],
      },
    ],
  },
  {
    value: '3',
    label: 'Level one 3',
    children: [
      {
        value: '3-1',
        label: 'Level two 3-1',
        children: [
          {
            value: '3-1-1',
            label: 'Level three 3-1-1',
          },
        ],
      },
      {
        value: '3-2',
        label: 'Level two 3-2',
        children: [
          {
            value: '3-2-1',
            label: 'Level three 3-2-1',
          },
        ],
      },
    ],
  },
]
</script>
```

隐藏源代码

## 禁用选项 [​](#禁用选项)

使用 disabled 字段禁用选项。

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS1zZWxlY3Qgdi1tb2RlbD1cInZhbHVlXCIgOmRhdGE9XCJkYXRhXCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIiAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoKVxuXG5jb25zdCBkYXRhID0gW1xuICB7XG4gICAgdmFsdWU6ICcxJyxcbiAgICBsYWJlbDogJ0xldmVsIG9uZSAxJyxcbiAgICBkaXNhYmxlZDogdHJ1ZSxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJzEtMScsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDEtMScsXG4gICAgICAgIGRpc2FibGVkOiB0cnVlLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGRpc2FibGVkOiB0cnVlLFxuICAgICAgICAgICAgdmFsdWU6ICcxLTEtMScsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDEtMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICcyJyxcbiAgICBsYWJlbDogJ0xldmVsIG9uZSAyJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJzItMScsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDItMScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICcyLTEtMScsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDItMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICcyLTInLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAyLTInLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMi0yLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAyLTItMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnMycsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMycsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICczLTEnLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAzLTEnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMy0xLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAzLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnMy0yJyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJzMtMi0xJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMy0yLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-select/disabled.vue)_

vue

```
<template>
  <el-tree-select v-model="value" :data="data" style="width: 240px" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()

const data = [
  {
    value: '1',
    label: 'Level one 1',
    disabled: true,
    children: [
      {
        value: '1-1',
        label: 'Level two 1-1',
        disabled: true,
        children: [
          {
            disabled: true,
            value: '1-1-1',
            label: 'Level three 1-1-1',
          },
        ],
      },
    ],
  },
  {
    value: '2',
    label: 'Level one 2',
    children: [
      {
        value: '2-1',
        label: 'Level two 2-1',
        children: [
          {
            value: '2-1-1',
            label: 'Level three 2-1-1',
          },
        ],
      },
      {
        value: '2-2',
        label: 'Level two 2-2',
        children: [
          {
            value: '2-2-1',
            label: 'Level three 2-2-1',
          },
        ],
      },
    ],
  },
  {
    value: '3',
    label: 'Level one 3',
    children: [
      {
        value: '3-1',
        label: 'Level two 3-1',
        children: [
          {
            value: '3-1-1',
            label: 'Level three 3-1-1',
          },
        ],
      },
      {
        value: '3-2',
        label: 'Level two 3-2',
        children: [
          {
            value: '3-2-1',
            label: 'Level three 3-2-1',
          },
        ],
      },
    ],
  },
]
</script>
```

隐藏源代码

## 可筛选 [​](#可筛选)

使用关键字筛选或自定义筛选方法。 `filterMethod`可以自定义数据筛选的方法， `filterNodeMethod`可以自定义节点数据筛选的方法。

Select

filter method:

Select

filter node method:

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS1zZWxlY3RcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgZmlsdGVyYWJsZVxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgLz5cbiAgPGVsLWRpdmlkZXIgLz5cbiAgZmlsdGVyIG1ldGhvZDpcbiAgPGVsLXRyZWUtc2VsZWN0XG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICA6ZGF0YT1cImRhdGFcIlxuICAgIDpmaWx0ZXItbWV0aG9kPVwiZmlsdGVyTWV0aG9kXCJcbiAgICBmaWx0ZXJhYmxlXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAvPlxuICA8ZWwtZGl2aWRlciAvPlxuICBmaWx0ZXIgbm9kZSBtZXRob2Q6XG4gIDxlbC10cmVlLXNlbGVjdFxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6ZmlsdGVyLW5vZGUtbWV0aG9kPVwiZmlsdGVyTm9kZU1ldGhvZFwiXG4gICAgZmlsdGVyYWJsZVxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKClcblxuY29uc3Qgc291cmNlRGF0YSA9IFtcbiAge1xuICAgIHZhbHVlOiAnMScsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICcxLTEnLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAxLTEnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMS0xLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAxLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnMicsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMicsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICcyLTEnLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAyLTEnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMi0xLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAyLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnMi0yJyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJzItMi0xJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMi0yLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJzMnLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDMnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnMy0xJyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJzMtMS0xJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMy0xLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJzMtMicsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDMtMicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICczLTItMScsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuY29uc3QgZGF0YSA9IHJlZihzb3VyY2VEYXRhKVxuXG5jb25zdCBmaWx0ZXJNZXRob2QgPSAodmFsdWUpID0+IHtcbiAgZGF0YS52YWx1ZSA9IFsuLi5zb3VyY2VEYXRhXS5maWx0ZXIoKGl0ZW0pID0+IGl0ZW0ubGFiZWwuaW5jbHVkZXModmFsdWUpKVxufVxuXG5jb25zdCBmaWx0ZXJOb2RlTWV0aG9kID0gKHZhbHVlLCBkYXRhKSA9PiBkYXRhLmxhYmVsLmluY2x1ZGVzKHZhbHVlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-select/filterable.vue)_

vue

```
<template>
  <el-tree-select
    v-model="value"
    :data="data"
    filterable
    style="width: 240px"
  />
  <el-divider />
  filter method:
  <el-tree-select
    v-model="value"
    :data="data"
    :filter-method="filterMethod"
    filterable
    style="width: 240px"
  />
  <el-divider />
  filter node method:
  <el-tree-select
    v-model="value"
    :data="data"
    :filter-node-method="filterNodeMethod"
    filterable
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()

const sourceData = [
  {
    value: '1',
    label: 'Level one 1',
    children: [
      {
        value: '1-1',
        label: 'Level two 1-1',
        children: [
          {
            value: '1-1-1',
            label: 'Level three 1-1-1',
          },
        ],
      },
    ],
  },
  {
    value: '2',
    label: 'Level one 2',
    children: [
      {
        value: '2-1',
        label: 'Level two 2-1',
        children: [
          {
            value: '2-1-1',
            label: 'Level three 2-1-1',
          },
        ],
      },
      {
        value: '2-2',
        label: 'Level two 2-2',
        children: [
          {
            value: '2-2-1',
            label: 'Level three 2-2-1',
          },
        ],
      },
    ],
  },
  {
    value: '3',
    label: 'Level one 3',
    children: [
      {
        value: '3-1',
        label: 'Level two 3-1',
        children: [
          {
            value: '3-1-1',
            label: 'Level three 3-1-1',
          },
        ],
      },
      {
        value: '3-2',
        label: 'Level two 3-2',
        children: [
          {
            value: '3-2-1',
            label: 'Level three 3-2-1',
          },
        ],
      },
    ],
  },
]
const data = ref(sourceData)

const filterMethod = (value) => {
  data.value = [...sourceData].filter((item) => item.label.includes(value))
}

const filterNodeMethod = (value, data) => data.label.includes(value)
</script>
```

隐藏源代码

## 自定义内容 [​](#自定义内容)

自定义树节点的内容。

Select

use render content:

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS1zZWxlY3Qgdi1tb2RlbD1cInZhbHVlXCIgOmRhdGE9XCJkYXRhXCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIj5cbiAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJ7IGRhdGE6IHsgbGFiZWwgfSB9XCI+XG4gICAgICB7eyBsYWJlbCB9fTxzcGFuIHN0eWxlPVwiY29sb3I6IGdyYXlcIj4oc3VmZml4KTwvc3Bhbj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLXRyZWUtc2VsZWN0PlxuICA8ZWwtZGl2aWRlciAvPlxuICB1c2UgcmVuZGVyIGNvbnRlbnQ6XG4gIDxlbC10cmVlLXNlbGVjdFxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6cmVuZGVyLWNvbnRlbnQ9XCJyZW5kZXJDb250ZW50XCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZigpXG5cbmNvbnN0IHJlbmRlckNvbnRlbnQgPSAoaCwgeyBkYXRhIH0pID0+IHtcbiAgcmV0dXJuIGgoXG4gICAgJ3NwYW4nLFxuICAgIHtcbiAgICAgIHN0eWxlOiB7XG4gICAgICAgIGNvbG9yOiAnIzYyNkFFRicsXG4gICAgICB9LFxuICAgIH0sXG4gICAgZGF0YS5sYWJlbFxuICApXG59XG5cbmNvbnN0IGRhdGEgPSBbXG4gIHtcbiAgICB2YWx1ZTogJzEnLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDEnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnMS0xJyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMS0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJzEtMS0xJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMS0xLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJzInLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDInLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnMi0xJyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJzItMS0xJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMi0xLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJzItMicsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDItMicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICcyLTItMScsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDItMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICczJyxcbiAgICBsYWJlbDogJ0xldmVsIG9uZSAzJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJzMtMScsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDMtMScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICczLTEtMScsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICczLTInLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAzLTInLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnMy0yLTEnLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAzLTItMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-select/slots.vue)_

vue

```
<template>
  <el-tree-select v-model="value" :data="data" style="width: 240px">
    <template #default="{ data: { label } }">
      {{ label }}<span style="color: gray">(suffix)</span>
    </template>
  </el-tree-select>
  <el-divider />
  use render content:
  <el-tree-select
    v-model="value"
    :data="data"
    :render-content="renderContent"
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()

const renderContent = (h, { data }) => {
  return h(
    'span',
    {
      style: {
        color: '#626AEF',
      },
    },
    data.label
  )
}

const data = [
  {
    value: '1',
    label: 'Level one 1',
    children: [
      {
        value: '1-1',
        label: 'Level two 1-1',
        children: [
          {
            value: '1-1-1',
            label: 'Level three 1-1-1',
          },
        ],
      },
    ],
  },
  {
    value: '2',
    label: 'Level one 2',
    children: [
      {
        value: '2-1',
        label: 'Level two 2-1',
        children: [
          {
            value: '2-1-1',
            label: 'Level three 2-1-1',
          },
        ],
      },
      {
        value: '2-2',
        label: 'Level two 2-2',
        children: [
          {
            value: '2-2-1',
            label: 'Level three 2-2-1',
          },
        ],
      },
    ],
  },
  {
    value: '3',
    label: 'Level one 3',
    children: [
      {
        value: '3-1',
        label: 'Level two 3-1',
        children: [
          {
            value: '3-1-1',
            label: 'Level three 3-1-1',
          },
        ],
      },
      {
        value: '3-2',
        label: 'Level two 3-2',
        children: [
          {
            value: '3-2-1',
            label: 'Level three 3-2-1',
          },
        ],
      },
    ],
  },
]
</script>
```

隐藏源代码

## 懒加载 [​](#懒加载)

树节点懒加载，更加适合于数据量大的列表。

Select

2.2.26 show lazy load label:

lazy load node5

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS1zZWxlY3RcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIGxhenlcbiAgICA6bG9hZD1cImxvYWRcIlxuICAgIDpwcm9wcz1cInByb3BzXCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gIC8+XG4gIDxlbC1kaXZpZGVyIC8+XG4gIDxWZXJzaW9uVGFnIHZlcnNpb249XCIyLjIuMjZcIiAvPiBzaG93IGxhenkgbG9hZCBsYWJlbDpcbiAgPGVsLXRyZWUtc2VsZWN0XG4gICAgdi1tb2RlbD1cInZhbHVlMlwiXG4gICAgbGF6eVxuICAgIDpsb2FkPVwibG9hZFwiXG4gICAgOnByb3BzPVwicHJvcHNcIlxuICAgIDpjYWNoZS1kYXRhPVwiY2FjaGVEYXRhXCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZigpXG5jb25zdCB2YWx1ZTIgPSByZWYoNSlcblxuY29uc3QgY2FjaGVEYXRhID0gW3sgdmFsdWU6IDUsIGxhYmVsOiAnbGF6eSBsb2FkIG5vZGU1JyB9XVxuXG5jb25zdCBwcm9wcyA9IHtcbiAgbGFiZWw6ICdsYWJlbCcsXG4gIGNoaWxkcmVuOiAnY2hpbGRyZW4nLFxuICBpc0xlYWY6ICdpc0xlYWYnLFxufVxuXG5sZXQgaWQgPSAwXG5cbmNvbnN0IGxvYWQgPSAobm9kZSwgcmVzb2x2ZSkgPT4ge1xuICBpZiAobm9kZS5pc0xlYWYpIHJldHVybiByZXNvbHZlKFtdKVxuXG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIHJlc29sdmUoW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogKytpZCxcbiAgICAgICAgbGFiZWw6IGBsYXp5IGxvYWQgbm9kZSR7aWR9YCxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiArK2lkLFxuICAgICAgICBsYWJlbDogYGxhenkgbG9hZCBub2RlJHtpZH1gLFxuICAgICAgICBpc0xlYWY6IHRydWUsXG4gICAgICB9LFxuICAgIF0pXG4gIH0sIDQwMClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-select/lazy.vue)_

vue

```
<template>
  <el-tree-select
    v-model="value"
    lazy
    :load="load"
    :props="props"
    style="width: 240px"
  />
  <el-divider />
  <VersionTag version="2.2.26" /> show lazy load label:
  <el-tree-select
    v-model="value2"
    lazy
    :load="load"
    :props="props"
    :cache-data="cacheData"
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()
const value2 = ref(5)

const cacheData = [{ value: 5, label: 'lazy load node5' }]

const props = {
  label: 'label',
  children: 'children',
  isLeaf: 'isLeaf',
}

let id = 0

const load = (node, resolve) => {
  if (node.isLeaf) return resolve([])

  setTimeout(() => {
    resolve([
      {
        value: ++id,
        label: `lazy load node${id}`,
      },
      {
        value: ++id,
        label: `lazy load node${id}`,
        isLeaf: true,
      },
    ])
  }, 400)
}
</script>
```

隐藏源代码

## 使用 node-key 属性 [​](#使用-node-key-属性)

默认情况下，`modelValue` 会查找 `value` 键。 对于其他数据结构，必须提供 `node-key` 才能正常工作。

TIP

1.  `node-key` 在整个树中应该是唯一的。
2.  `value-key` 与 `node-key` 具有相同的目标。
3.  与 select 组件相反，tree-select 不能检索对象值。

value-on-clear

Level two 1-1

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS1zZWxlY3RcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICA6ZGF0YT1cImRhdGFcIlxuICAgIG5vZGUta2V5PVwiaWRcIlxuICAgIHNob3ctY2hlY2tib3hcbiAgICBtdWx0aXBsZVxuICAgIGRlZmF1bHQtZXhwYW5kLWFsbFxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoWzJdKVxuY29uc3QgZGF0YSA9IFtcbiAge1xuICAgIGlkOiAxLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDEnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIGlkOiAyLFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAxLTEnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IDMsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDEtMicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-select/node-key.vue)_

vue

```
<template>
  <el-tree-select
    v-model="value"
    style="width: 240px"
    :data="data"
    node-key="id"
    show-checkbox
    multiple
    default-expand-all
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref([2])
const data = [
  {
    id: 1,
    label: 'Level one 1',
    children: [
      {
        id: 2,
        label: 'Level two 1-1',
      },
      {
        id: 3,
        label: 'Level two 1-2',
      },
    ],
  },
]
</script>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

由于这个组件是`el-tree`和`el-select`的结合体，他们的原始属性未被更改，故不在此重复。请跳转查看原组件的相应文档。

| 属性 | 对外暴露的方法 | 事件 | 插槽 |
| --- | --- | --- | --- |
| [tree](https://element-plus.org/zh-CN/component/tree#attributes) | [tree](https://element-plus.org/zh-CN/component/tree#exposes) | [tree](https://element-plus.org/zh-CN/component/tree#events) | [tree](https://element-plus.org/zh-CN/component/tree#slots) |
| [select](https://element-plus.org/zh-CN/component/select#select-attributes) | [select](https://element-plus.org/zh-CN/component/select#select-exposes) | [select](https://element-plus.org/zh-CN/component/select#select-events) | [select](https://element-plus.org/zh-CN/component/select#select-slots) |

#### Own Attributes [​](#own-attributes)

| 属性名 | 详情 | 类型 | 默认值 |
| --- | --- | --- | --- |
| cache-data 2.2.26 | 懒加载节点的缓存数据，结构与数据相同，用于获取未加载数据的标签 | `array` | \[\] |

### 对外暴露的方法 [​](#对外暴露的方法)

WARNING

在 Tree 和 Select 组件下暴露方法的方式已被 **弃用**，并将于 3.0.0 中 **移除**，请在各自的组件层级下使用这些方法：`tree` 和 `select`。

| 事件名 | 详情 | Type |
| --- | --- | --- |
| treeRef 2.11.3 | Tree 组件实例 | `TreeInstance` |
| selectRef 2.11.3 | Select 组件实例 | `SelectInstance` |
| filter deprecated | 过滤所有树节点，过滤后的节点将被隐藏 | 接收一个参数并指定为 filter-node-method 属性的第一个参数 |
| updateKeyChildren deprecated | 为节点设置新数据，只有当设置 `node-key` 属性的时候才可用 | (key, data) 接收两个参数: 1. 节点的 key 2. 新数据 |
| getCheckedNodes deprecated | 如果节点可以被选中，(`show-checkbox` 为 `true`), 本方法将返回当前选中节点的数组 | (leafOnly, includeHalfChecked) 接收两个布尔类型参数: 1. 默认值为 `false`. 若参数为 `true`, 它将返回当前选中节点的子节点 2. 默认值为 `false`. 如果参数为 `true`, 返回值包含半选中节点数据 |
| setCheckedNodes deprecated | 设置目前选中的节点，使用此方法必须设置 `node-key` 属性 | 要选中的节点构成的数组 |
| getCheckedKeys deprecated | 若节点可用被选中 (`show-checkbox` 为 `true`), 它将返回当前选中节点 key 的数组 | (leafOnly) 接收一个布尔类型参数，默认为 `false`. 若参数为 `true`, 它将返回当前选中节点的子节点 |
| setCheckedKeys deprecated | 设置目前选中的节点，使用此方法必须设置 `node-key` 属性 | (keys, leafOnly) 接收两个参数: 1. 一个需要被选中的多节点 key 的数组 2. 布尔类型的值 如果设置为 `true`，将只设置选中的叶子节点状态。 默认值是 `false`. |
| setChecked deprecated | 设置节点是否被选中, 使用此方法必须设置 `node-key` 属性 | (key/data, checked, deep) 接收三个参数: 1. 要选中的节点的 key 或者数据 2. 一个布尔类型参数表明是否选中. 3. 一个布尔类型参数，用于指示是否递归选中/取消选中子节点（自 2.14.0 起，无论 `check-strictly` 设置如何，该行为均有效）。 |
| getHalfCheckedNodes deprecated | 如果节点可用被选中 (`show-checkbox` 为 `true`), 它将返回当前半选中的节点组成的数组 | ::: |
| getHalfCheckedKeys deprecated | 若节点可被选中(`show-checkbox` 为 `true`)，则返回目前半选中的节点的 key 所组成的数组 | ::: |
| getCurrentKey deprecated | 返回当前被选中节点的数据 (如果没有则返回 null) | ::: |
| getCurrentNode deprecated | 返回当前被选中节点的数据 (如果没有则返回 null) | ::: |
| setCurrentKey deprecated | 通过 key 设置某个节点的当前选中状态，使用此方法必须设置 `node-key` 属性 | (key, shouldAutoExpandParent=true) 1. 待被选节点的 key， 如果为 `null`, 取消当前选中的节点 2. 是否展开父节点 |
| setCurrentNode deprecated | 设置节点为选中状态，使用此方法必须设置 `node-key` 属性 | (node, shouldAutoExpandParent=true) 1. 待被选中的节点 2. 是否展开父节点 |
| getNode deprecated | 根据 data 或者 key 拿到 Tree 组件中的 node | (data) 节点的 data 或 key |
| remove deprecated | 删除 Tree 中的一个节点，使用此方法必须设置 node-key 属性 | (data) 要删除的节点的 data 或者 node 对象 |
| append deprecated | 为 Tree 中的一个节点追加一个子节点 | (data, parentNode) 1. 要追加的子节点的 data 2. 父节点的 data, key 或 node |
| insertBefore deprecated | 在 Tree 中给定节点前插入一个节点 | (data, refNode) 1. 要增加的节点的 data 2. 参考节点的 data, key 或 node |
| insertAfter deprecated | 在 Tree 中给定节点后插入一个节点 | (data, refNode) 1. 要增加的节点的 data 2. 参考节点的 data, key 或 node |
| focus deprecated | 使选择器的输入框获取焦点 | `Function` |
| blur deprecated | 使选择器的输入框失去焦点，并隐藏下拉框 | `Function` |
| selectedLabel 2.8.5 deprecated | 获取当前选中的标签 | `object` |

## 类型声明 [​](#类型声明)

显示类型声明

ts

```
type CacheOption = {
  value: string | number | boolean | object
  currentLabel: string | number
  isDisabled: boolean
}
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/tree-select) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/tree-select.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/tree-select.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/20787785?v=4&size=64)](https://github.com/yujinpan)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/33254923?v=4&size=64)](https://github.com/yicheny)[![](https://avatars.githubusercontent.com/u/27413795?v=4&size=64)](https://github.com/SpanManX)[![](https://avatars.githubusercontent.com/u/24290011?v=4&size=64)](https://github.com/xingyixiang)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/36940267?v=4&size=64)](https://github.com/gaoxuan-haxibiao)[![](https://avatars.githubusercontent.com/u/27912232?v=4&size=64)](https://github.com/Fuphoenixes)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/16463481?v=4&size=64)](https://github.com/hellomrbigshot)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/36811055?v=4&size=64)](https://github.com/iDestin)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/54303040?v=4&size=64)](https://github.com/7086cmd)[![](https://avatars.githubusercontent.com/u/48147837?v=4&size=64)](https://github.com/kcmeven)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/53589602?v=4&size=64)](https://github.com/l246804)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)

[Transfer 穿梭框](https://element-plus.org/zh-CN/component/transfer)

[Upload 上传器](https://element-plus.org/zh-CN/component/upload)


