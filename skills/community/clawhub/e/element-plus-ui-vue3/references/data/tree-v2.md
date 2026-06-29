---
name: "tree-v2"
description: "Virtualized Tree 虚拟化树形控件 -- Element Plus Vue3 桌面端组件。Invoke when user needs Virtualized Tree 虚拟化树形控件 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/tree-v2.html"
---

---

#

Tree V2 虚拟化树形控件beta

[​](#tree-v2-虚拟化树形控件)

更新日志待解决

17

不论你的数据量多大，虚拟树都能毫无压力地处理。

## 基础用法 [​](#基础用法)

基础的树形结构展示

node-1

node-2

node-3

node-4

node-5

node-6

node-7

node-8

node-9

node-10

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS12MlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgOmhlaWdodD1cIjIwMFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW50ZXJmYWNlIFRyZWUge1xuICBpZDogc3RyaW5nXG4gIGxhYmVsOiBzdHJpbmdcbiAgY2hpbGRyZW4/OiBUcmVlW11cbn1cblxuY29uc3QgZ2V0S2V5ID0gKHByZWZpeDogc3RyaW5nLCBpZDogbnVtYmVyKSA9PiB7XG4gIHJldHVybiBgJHtwcmVmaXh9LSR7aWR9YFxufVxuXG5jb25zdCBjcmVhdGVEYXRhID0gKFxuICBtYXhEZWVwOiBudW1iZXIsXG4gIG1heENoaWxkcmVuOiBudW1iZXIsXG4gIG1pbk5vZGVzTnVtYmVyOiBudW1iZXIsXG4gIGRlZXAgPSAxLFxuICBrZXkgPSAnbm9kZSdcbik6IFRyZWVbXSA9PiB7XG4gIGxldCBpZCA9IDBcbiAgcmV0dXJuIEFycmF5LmZyb20oeyBsZW5ndGg6IG1pbk5vZGVzTnVtYmVyIH0pXG4gICAgLmZpbGwoZGVlcClcbiAgICAubWFwKCgpID0+IHtcbiAgICAgIGNvbnN0IGNoaWxkcmVuTnVtYmVyID1cbiAgICAgICAgZGVlcCA9PT0gbWF4RGVlcCA/IDAgOiBNYXRoLnJvdW5kKE1hdGgucmFuZG9tKCkgKiBtYXhDaGlsZHJlbilcbiAgICAgIGNvbnN0IG5vZGVLZXkgPSBnZXRLZXkoa2V5LCArK2lkKVxuICAgICAgcmV0dXJuIHtcbiAgICAgICAgaWQ6IG5vZGVLZXksXG4gICAgICAgIGxhYmVsOiBub2RlS2V5LFxuICAgICAgICBjaGlsZHJlbjogY2hpbGRyZW5OdW1iZXJcbiAgICAgICAgICA/IGNyZWF0ZURhdGEobWF4RGVlcCwgbWF4Q2hpbGRyZW4sIGNoaWxkcmVuTnVtYmVyLCBkZWVwICsgMSwgbm9kZUtleSlcbiAgICAgICAgICA6IHVuZGVmaW5lZCxcbiAgICAgIH1cbiAgICB9KVxufVxuXG5jb25zdCBwcm9wcyA9IHtcbiAgdmFsdWU6ICdpZCcsXG4gIGxhYmVsOiAnbGFiZWwnLFxuICBjaGlsZHJlbjogJ2NoaWxkcmVuJyxcbn1cbmNvbnN0IGRhdGEgPSBjcmVhdGVEYXRhKDQsIDMwLCA0MClcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-v2/basic.vue)_

vue

```
<template>
  <el-tree-v2
    style="max-width: 600px"
    :data="data"
    :props="props"
    :height="200"
  />
</template>

<script lang="ts" setup>
interface Tree {
  id: string
  label: string
  children?: Tree[]
}

const getKey = (prefix: string, id: number) => {
  return `${prefix}-${id}`
}

const createData = (
  maxDeep: number,
  maxChildren: number,
  minNodesNumber: number,
  deep = 1,
  key = 'node'
): Tree[] => {
  let id = 0
  return Array.from({ length: minNodesNumber })
    .fill(deep)
    .map(() => {
      const childrenNumber =
        deep === maxDeep ? 0 : Math.round(Math.random() * maxChildren)
      const nodeKey = getKey(key, ++id)
      return {
        id: nodeKey,
        label: nodeKey,
        children: childrenNumber
          ? createData(maxDeep, maxChildren, childrenNumber, deep + 1, nodeKey)
          : undefined,
      }
    })
}

const props = {
  value: 'id',
  label: 'label',
  children: 'children',
}
const data = createData(4, 30, 40)
</script>
```

隐藏源代码

## 可选择的虚拟树 [​](#可选择的虚拟树)

适用于需要选择层级时使用。

node-1

node-2

node-3

node-4

node-5

node-6

node-7

node-8

node-9

node-10

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS12MlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgc2hvdy1jaGVja2JveFxuICAgIDpoZWlnaHQ9XCIyMDBcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmludGVyZmFjZSBUcmVlIHtcbiAgaWQ6IHN0cmluZ1xuICBsYWJlbDogc3RyaW5nXG4gIGNoaWxkcmVuPzogVHJlZVtdXG59XG5cbmNvbnN0IGdldEtleSA9IChwcmVmaXg6IHN0cmluZywgaWQ6IG51bWJlcikgPT4ge1xuICByZXR1cm4gYCR7cHJlZml4fS0ke2lkfWBcbn1cblxuY29uc3QgY3JlYXRlRGF0YSA9IChcbiAgbWF4RGVlcDogbnVtYmVyLFxuICBtYXhDaGlsZHJlbjogbnVtYmVyLFxuICBtaW5Ob2Rlc051bWJlcjogbnVtYmVyLFxuICBkZWVwID0gMSxcbiAga2V5ID0gJ25vZGUnXG4pOiBUcmVlW10gPT4ge1xuICBsZXQgaWQgPSAwXG4gIHJldHVybiBBcnJheS5mcm9tKHsgbGVuZ3RoOiBtaW5Ob2Rlc051bWJlciB9KVxuICAgIC5maWxsKGRlZXApXG4gICAgLm1hcCgoKSA9PiB7XG4gICAgICBjb25zdCBjaGlsZHJlbk51bWJlciA9XG4gICAgICAgIGRlZXAgPT09IG1heERlZXAgPyAwIDogTWF0aC5yb3VuZChNYXRoLnJhbmRvbSgpICogbWF4Q2hpbGRyZW4pXG4gICAgICBjb25zdCBub2RlS2V5ID0gZ2V0S2V5KGtleSwgKytpZClcbiAgICAgIHJldHVybiB7XG4gICAgICAgIGlkOiBub2RlS2V5LFxuICAgICAgICBsYWJlbDogbm9kZUtleSxcbiAgICAgICAgY2hpbGRyZW46IGNoaWxkcmVuTnVtYmVyXG4gICAgICAgICAgPyBjcmVhdGVEYXRhKG1heERlZXAsIG1heENoaWxkcmVuLCBjaGlsZHJlbk51bWJlciwgZGVlcCArIDEsIG5vZGVLZXkpXG4gICAgICAgICAgOiB1bmRlZmluZWQsXG4gICAgICB9XG4gICAgfSlcbn1cblxuY29uc3QgcHJvcHMgPSB7XG4gIHZhbHVlOiAnaWQnLFxuICBsYWJlbDogJ2xhYmVsJyxcbiAgY2hpbGRyZW46ICdjaGlsZHJlbicsXG59XG5jb25zdCBkYXRhID0gY3JlYXRlRGF0YSg0LCAzMCwgNDApXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-v2/selectable.vue)_

vue

```
<template>
  <el-tree-v2
    style="max-width: 600px"
    :data="data"
    :props="props"
    show-checkbox
    :height="200"
  />
</template>

<script lang="ts" setup>
interface Tree {
  id: string
  label: string
  children?: Tree[]
}

const getKey = (prefix: string, id: number) => {
  return `${prefix}-${id}`
}

const createData = (
  maxDeep: number,
  maxChildren: number,
  minNodesNumber: number,
  deep = 1,
  key = 'node'
): Tree[] => {
  let id = 0
  return Array.from({ length: minNodesNumber })
    .fill(deep)
    .map(() => {
      const childrenNumber =
        deep === maxDeep ? 0 : Math.round(Math.random() * maxChildren)
      const nodeKey = getKey(key, ++id)
      return {
        id: nodeKey,
        label: nodeKey,
        children: childrenNumber
          ? createData(maxDeep, maxChildren, childrenNumber, deep + 1, nodeKey)
          : undefined,
      }
    })
}

const props = {
  value: 'id',
  label: 'label',
  children: 'children',
}
const data = createData(4, 30, 40)
</script>
```

隐藏源代码

WARNING

在使用 show-checkbox 时，因为 `check-on-click-leaf` 默认值为 true， 最后一个树节点可以通过点击节点进行勾选。

## 禁用复选框 [​](#禁用复选框)

节点的复选框可以设置为禁用。

在示例中，属性在 defaultProps 中声明了 `disabled`，一些节点被设置为 `disabled：true`。 相应的复选框已禁用，不能点击。

node-1

node-2

node-3

node-4

node-5

node-6

node-7

node-8

node-9

node-10

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS12MlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgc2hvdy1jaGVja2JveFxuICAgIDpoZWlnaHQ9XCIyMDBcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmludGVyZmFjZSBUcmVlIHtcbiAgaWQ6IHN0cmluZ1xuICBsYWJlbDogc3RyaW5nXG4gIGNoaWxkcmVuPzogVHJlZVtdXG4gIGRpc2FibGVkOiBib29sZWFuXG59XG5cbmNvbnN0IGdldEtleSA9IChwcmVmaXg6IHN0cmluZywgaWQ6IG51bWJlcikgPT4ge1xuICByZXR1cm4gYCR7cHJlZml4fS0ke2lkfWBcbn1cblxuY29uc3QgY3JlYXRlRGF0YSA9IChcbiAgbWF4RGVlcDogbnVtYmVyLFxuICBtYXhDaGlsZHJlbjogbnVtYmVyLFxuICBtaW5Ob2Rlc051bWJlcjogbnVtYmVyLFxuICBkZWVwID0gMSxcbiAga2V5ID0gJ25vZGUnXG4pOiBUcmVlW10gPT4ge1xuICBsZXQgaWQgPSAwXG4gIHJldHVybiBBcnJheS5mcm9tKHsgbGVuZ3RoOiBtaW5Ob2Rlc051bWJlciB9KVxuICAgIC5maWxsKGRlZXApXG4gICAgLm1hcCgoKSA9PiB7XG4gICAgICBjb25zdCBjaGlsZHJlbk51bWJlciA9XG4gICAgICAgIGRlZXAgPT09IG1heERlZXAgPyAwIDogTWF0aC5yb3VuZChNYXRoLnJhbmRvbSgpICogbWF4Q2hpbGRyZW4pXG4gICAgICBjb25zdCBub2RlS2V5ID0gZ2V0S2V5KGtleSwgKytpZClcbiAgICAgIHJldHVybiB7XG4gICAgICAgIGlkOiBub2RlS2V5LFxuICAgICAgICBsYWJlbDogbm9kZUtleSxcbiAgICAgICAgY2hpbGRyZW46IGNoaWxkcmVuTnVtYmVyXG4gICAgICAgICAgPyBjcmVhdGVEYXRhKG1heERlZXAsIG1heENoaWxkcmVuLCBjaGlsZHJlbk51bWJlciwgZGVlcCArIDEsIG5vZGVLZXkpXG4gICAgICAgICAgOiB1bmRlZmluZWQsXG4gICAgICAgIGRpc2FibGVkOiBub2RlS2V5LmluY2x1ZGVzKCcyJyksXG4gICAgICB9XG4gICAgfSlcbn1cblxuY29uc3QgcHJvcHMgPSB7XG4gIHZhbHVlOiAnaWQnLFxuICBsYWJlbDogJ2xhYmVsJyxcbiAgY2hpbGRyZW46ICdjaGlsZHJlbicsXG4gIGRpc2FibGVkOiAnZGlzYWJsZWQnLFxufVxuY29uc3QgZGF0YSA9IGNyZWF0ZURhdGEoNCwgMzAsIDQwKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-v2/disabled.vue)_

vue

```
<template>
  <el-tree-v2
    style="max-width: 600px"
    :data="data"
    :props="props"
    show-checkbox
    :height="200"
  />
</template>

<script lang="ts" setup>
interface Tree {
  id: string
  label: string
  children?: Tree[]
  disabled: boolean
}

const getKey = (prefix: string, id: number) => {
  return `${prefix}-${id}`
}

const createData = (
  maxDeep: number,
  maxChildren: number,
  minNodesNumber: number,
  deep = 1,
  key = 'node'
): Tree[] => {
  let id = 0
  return Array.from({ length: minNodesNumber })
    .fill(deep)
    .map(() => {
      const childrenNumber =
        deep === maxDeep ? 0 : Math.round(Math.random() * maxChildren)
      const nodeKey = getKey(key, ++id)
      return {
        id: nodeKey,
        label: nodeKey,
        children: childrenNumber
          ? createData(maxDeep, maxChildren, childrenNumber, deep + 1, nodeKey)
          : undefined,
        disabled: nodeKey.includes('2'),
      }
    })
}

const props = {
  value: 'id',
  label: 'label',
  children: 'children',
  disabled: 'disabled',
}
const data = createData(4, 30, 40)
</script>
```

隐藏源代码

## 默认扩展和默认检查 [​](#默认扩展和默认检查)

树节点可以在初始化阶段被设置为展开或选中。

分别通过 `default-expanded-keys` 和 `default-checked-keys` 设置默认展开和默认选中的节点。

node-1

node-1-1

node-1-2

node-1-3

node-1-4

node-1-5

node-1-6

node-1-7

node-1-8

node-1-9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS12MlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6aGVpZ2h0PVwiMjAwXCJcbiAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgc2hvdy1jaGVja2JveFxuICAgIDpkZWZhdWx0LWNoZWNrZWQta2V5cz1cImRlZmF1bHRDaGVja2VkS2V5c1wiXG4gICAgOmRlZmF1bHQtZXhwYW5kZWQta2V5cz1cImRlZmF1bHRFeHBhbmRlZEtleXNcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW50ZXJmYWNlIFRyZWUge1xuICBpZDogc3RyaW5nXG4gIGxhYmVsOiBzdHJpbmdcbiAgY2hpbGRyZW4/OiBUcmVlW11cbn1cblxuY29uc3QgZ2V0S2V5ID0gKHByZWZpeDogc3RyaW5nLCBpZDogbnVtYmVyKSA9PiB7XG4gIHJldHVybiBgJHtwcmVmaXh9LSR7aWR9YFxufVxuXG5jb25zdCBjcmVhdGVEYXRhID0gKFxuICBtYXhEZWVwOiBudW1iZXIsXG4gIG1heENoaWxkcmVuOiBudW1iZXIsXG4gIG1pbk5vZGVzTnVtYmVyOiBudW1iZXIsXG4gIGRlZXAgPSAxLFxuICBrZXkgPSAnbm9kZSdcbik6IFRyZWVbXSA9PiB7XG4gIGxldCBpZCA9IDBcbiAgcmV0dXJuIEFycmF5LmZyb20oeyBsZW5ndGg6IG1pbk5vZGVzTnVtYmVyIH0pXG4gICAgLmZpbGwoZGVlcClcbiAgICAubWFwKCgpID0+IHtcbiAgICAgIGNvbnN0IGNoaWxkcmVuTnVtYmVyID1cbiAgICAgICAgZGVlcCA9PT0gbWF4RGVlcCA/IDAgOiBNYXRoLnJvdW5kKE1hdGgucmFuZG9tKCkgKiBtYXhDaGlsZHJlbilcbiAgICAgIGNvbnN0IG5vZGVLZXkgPSBnZXRLZXkoa2V5LCArK2lkKVxuICAgICAgcmV0dXJuIHtcbiAgICAgICAgaWQ6IG5vZGVLZXksXG4gICAgICAgIGxhYmVsOiBub2RlS2V5LFxuICAgICAgICBjaGlsZHJlbjogY2hpbGRyZW5OdW1iZXJcbiAgICAgICAgICA/IGNyZWF0ZURhdGEobWF4RGVlcCwgbWF4Q2hpbGRyZW4sIGNoaWxkcmVuTnVtYmVyLCBkZWVwICsgMSwgbm9kZUtleSlcbiAgICAgICAgICA6IHVuZGVmaW5lZCxcbiAgICAgIH1cbiAgICB9KVxufVxuXG5jb25zdCBwcm9wcyA9IHtcbiAgdmFsdWU6ICdpZCcsXG4gIGxhYmVsOiAnbGFiZWwnLFxuICBjaGlsZHJlbjogJ2NoaWxkcmVuJyxcbn1cbmNvbnN0IGRhdGEgPSBjcmVhdGVEYXRhKDQsIDMwLCA0MClcbmNvbnN0IGNoZWNrZWRLZXlzOiBzdHJpbmdbXSA9IFtdXG5jb25zdCBleHBhbmVkS2V5czogc3RyaW5nW10gPSBbXVxuZm9yIChjb25zdCBkYXR1bSBvZiBkYXRhKSB7XG4gIGNvbnN0IGNoaWxkcmVuID0gZGF0dW0uY2hpbGRyZW5cbiAgaWYgKGNoaWxkcmVuKSB7XG4gICAgZXhwYW5lZEtleXMucHVzaChkYXR1bS5pZClcbiAgICBjaGVja2VkS2V5cy5wdXNoKGNoaWxkcmVuWzBdLmlkKVxuICAgIGJyZWFrXG4gIH1cbn1cblxuY29uc3QgZGVmYXVsdENoZWNrZWRLZXlzID0gcmVmKGNoZWNrZWRLZXlzKVxuY29uc3QgZGVmYXVsdEV4cGFuZGVkS2V5cyA9IHJlZihleHBhbmVkS2V5cylcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-v2/default-state.vue)_

vue

```
<template>
  <el-tree-v2
    style="max-width: 600px"
    :data="data"
    :height="200"
    :props="props"
    show-checkbox
    :default-checked-keys="defaultCheckedKeys"
    :default-expanded-keys="defaultExpandedKeys"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Tree {
  id: string
  label: string
  children?: Tree[]
}

const getKey = (prefix: string, id: number) => {
  return `${prefix}-${id}`
}

const createData = (
  maxDeep: number,
  maxChildren: number,
  minNodesNumber: number,
  deep = 1,
  key = 'node'
): Tree[] => {
  let id = 0
  return Array.from({ length: minNodesNumber })
    .fill(deep)
    .map(() => {
      const childrenNumber =
        deep === maxDeep ? 0 : Math.round(Math.random() * maxChildren)
      const nodeKey = getKey(key, ++id)
      return {
        id: nodeKey,
        label: nodeKey,
        children: childrenNumber
          ? createData(maxDeep, maxChildren, childrenNumber, deep + 1, nodeKey)
          : undefined,
      }
    })
}

const props = {
  value: 'id',
  label: 'label',
  children: 'children',
}
const data = createData(4, 30, 40)
const checkedKeys: string[] = []
const expanedKeys: string[] = []
for (const datum of data) {
  const children = datum.children
  if (children) {
    expanedKeys.push(datum.id)
    checkedKeys.push(children[0].id)
    break
  }
}

const defaultCheckedKeys = ref(checkedKeys)
const defaultExpandedKeys = ref(expanedKeys)
</script>
```

隐藏源代码

## 自定义节点内容 [​](#自定义节点内容)

节点的内容支持自定义，可以在节点区添加按钮或图标等内容

\[ElementPlus\]node-1

\[ElementPlus\]node-2

\[ElementPlus\]node-3

\[ElementPlus\]node-4

\[ElementPlus\]node-5

\[ElementPlus\]node-6

\[ElementPlus\]node-7

\[ElementPlus\]node-8

\[ElementPlus\]node-9

\[ElementPlus\]node-10

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS12MlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgOmhlaWdodD1cIjIwMFwiXG4gID5cbiAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJ7IG5vZGUgfVwiPlxuICAgICAgPGVsLWljb24gY2xhc3M9XCJlbC1pY29uLS1sZWZ0XCI+XG4gICAgICAgIDxEb2N1bWVudCB2LWlmPVwibm9kZS5pc0xlYWZcIiAvPlxuICAgICAgICA8Rm9sZGVyIHYtZWxzZS1pZj1cIiFub2RlLmV4cGFuZGVkXCIgLz5cbiAgICAgICAgPEZvbGRlck9wZW5lZCB2LWVsc2UgLz5cbiAgICAgIDwvZWwtaWNvbj5cbiAgICAgIDxzcGFuIGNsYXNzPVwicHJlZml4XCIgOmNsYXNzPVwieyAnaXMtbGVhZic6IG5vZGUuaXNMZWFmIH1cIlxuICAgICAgICA+W0VsZW1lbnRQbHVzXTwvc3BhblxuICAgICAgPlxuICAgICAgPHNwYW4+e3sgbm9kZS5sYWJlbCB9fTwvc3Bhbj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLXRyZWUtdjI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRG9jdW1lbnQsIEZvbGRlciwgRm9sZGVyT3BlbmVkIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmludGVyZmFjZSBUcmVlIHtcbiAgaWQ6IHN0cmluZ1xuICBsYWJlbDogc3RyaW5nXG4gIGNoaWxkcmVuPzogVHJlZVtdXG59XG5cbmNvbnN0IGdldEtleSA9IChwcmVmaXg6IHN0cmluZywgaWQ6IG51bWJlcikgPT4ge1xuICByZXR1cm4gYCR7cHJlZml4fS0ke2lkfWBcbn1cblxuY29uc3QgY3JlYXRlRGF0YSA9IChcbiAgbWF4RGVlcDogbnVtYmVyLFxuICBtYXhDaGlsZHJlbjogbnVtYmVyLFxuICBtaW5Ob2Rlc051bWJlcjogbnVtYmVyLFxuICBkZWVwID0gMSxcbiAga2V5ID0gJ25vZGUnXG4pOiBUcmVlW10gPT4ge1xuICBsZXQgaWQgPSAwXG4gIHJldHVybiBBcnJheS5mcm9tKHsgbGVuZ3RoOiBtaW5Ob2Rlc051bWJlciB9KVxuICAgIC5maWxsKGRlZXApXG4gICAgLm1hcCgoKSA9PiB7XG4gICAgICBjb25zdCBjaGlsZHJlbk51bWJlciA9XG4gICAgICAgIGRlZXAgPT09IG1heERlZXAgPyAwIDogTWF0aC5yb3VuZChNYXRoLnJhbmRvbSgpICogbWF4Q2hpbGRyZW4pXG4gICAgICBjb25zdCBub2RlS2V5ID0gZ2V0S2V5KGtleSwgKytpZClcbiAgICAgIHJldHVybiB7XG4gICAgICAgIGlkOiBub2RlS2V5LFxuICAgICAgICBsYWJlbDogbm9kZUtleSxcbiAgICAgICAgY2hpbGRyZW46IGNoaWxkcmVuTnVtYmVyXG4gICAgICAgICAgPyBjcmVhdGVEYXRhKG1heERlZXAsIG1heENoaWxkcmVuLCBjaGlsZHJlbk51bWJlciwgZGVlcCArIDEsIG5vZGVLZXkpXG4gICAgICAgICAgOiB1bmRlZmluZWQsXG4gICAgICB9XG4gICAgfSlcbn1cblxuY29uc3QgcHJvcHMgPSB7XG4gIHZhbHVlOiAnaWQnLFxuICBsYWJlbDogJ2xhYmVsJyxcbiAgY2hpbGRyZW46ICdjaGlsZHJlbicsXG59XG5jb25zdCBkYXRhID0gY3JlYXRlRGF0YSg0LCAzMCwgNDApXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5wcmVmaXgge1xuICBjb2xvcjogdmFyKC0tZWwtY29sb3ItcHJpbWFyeSk7XG4gIG1hcmdpbi1yaWdodDogMTBweDtcbn1cbi5wcmVmaXguaXMtbGVhZiB7XG4gIGNvbG9yOiB2YXIoLS1lbC1jb2xvci1zdWNjZXNzKTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-v2/custom-node.vue)_

vue

```
<template>
  <el-tree-v2
    style="max-width: 600px"
    :data="data"
    :props="props"
    :height="200"
  >
    <template #default="{ node }">
      <el-icon class="el-icon--left">
        <Document v-if="node.isLeaf" />
        <Folder v-else-if="!node.expanded" />
        <FolderOpened v-else />
      </el-icon>
      <span class="prefix" :class="{ 'is-leaf': node.isLeaf }"
        >[ElementPlus]</span
      >
      <span>{{ node.label }}</span>
    </template>
  </el-tree-v2>
</template>

<script lang="ts" setup>
import { Document, Folder, FolderOpened } from '@element-plus/icons-vue'

interface Tree {
  id: string
  label: string
  children?: Tree[]
}

const getKey = (prefix: string, id: number) => {
  return `${prefix}-${id}`
}

const createData = (
  maxDeep: number,
  maxChildren: number,
  minNodesNumber: number,
  deep = 1,
  key = 'node'
): Tree[] => {
  let id = 0
  return Array.from({ length: minNodesNumber })
    .fill(deep)
    .map(() => {
      const childrenNumber =
        deep === maxDeep ? 0 : Math.round(Math.random() * maxChildren)
      const nodeKey = getKey(key, ++id)
      return {
        id: nodeKey,
        label: nodeKey,
        children: childrenNumber
          ? createData(maxDeep, maxChildren, childrenNumber, deep + 1, nodeKey)
          : undefined,
      }
    })
}

const props = {
  value: 'id',
  label: 'label',
  children: 'children',
}
const data = createData(4, 30, 40)
</script>

<style scoped>
.prefix {
  color: var(--el-color-primary);
  margin-right: 10px;
}
.prefix.is-leaf {
  color: var(--el-color-success);
}
</style>
```

隐藏源代码

## 自定义节点类 2.9.0 [​](#自定义节点类)

节点的类名支持自定义。

Level one 1

Level one 2

Level one 3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS12MlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICBzaG93LWNoZWNrYm94XG4gICAgOmV4cGFuZC1vbi1jbGljay1ub2RlPVwiZmFsc2VcIlxuICAgIDpwcm9wcz1cInsgY2xhc3M6IGN1c3RvbU5vZGVDbGFzcyB9XCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgdHlwZSB7IFRyZWVOb2RlLCBUcmVlTm9kZURhdGEgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmludGVyZmFjZSBUcmVlIHtcbiAgaWQ/OiBzdHJpbmdcbiAgdmFsdWU/OiBzdHJpbmdcbiAgbGFiZWw/OiBzdHJpbmdcbiAgaXNQZW51bHRpbWF0ZT86IGJvb2xlYW5cbiAgY2hpbGRyZW4/OiBUcmVlW11cbn1cblxuY29uc3QgY3VzdG9tTm9kZUNsYXNzID0gKHsgaXNQZW51bHRpbWF0ZSB9OiBUcmVlTm9kZURhdGEsIG5vZGU6IFRyZWVOb2RlKSA9PlxuICBpc1BlbnVsdGltYXRlID8gJ2lzLXBlbnVsdGltYXRlJyA6ICcnXG5cbmNvbnN0IGRhdGE6IFRyZWVbXSA9IFtcbiAge1xuICAgIGlkOiAnMScsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgaWQ6ICc0JyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMS0xJyxcbiAgICAgICAgaXNQZW51bHRpbWF0ZTogdHJ1ZSxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBpZDogJzknLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAxLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBpZDogJzEwJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMS0xLTInLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICBpZDogJzInLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDInLFxuICAgIGlzUGVudWx0aW1hdGU6IHRydWUsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgaWQ6ICc1JyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0xJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiAnNicsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDItMicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICBpZDogJzMnLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDMnLFxuICAgIGlzUGVudWx0aW1hdGU6IHRydWUsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgaWQ6ICc3JyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0xJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiAnOCcsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDMtMicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbjpkZWVwKC5pcy1wZW51bHRpbWF0ZSAuZWwtdHJlZS1ub2RlX19sYWJlbCkge1xuICBjb2xvcjogIzYyNmFlZjtcbiAgZm9udC13ZWlnaHQ6IDYwMDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-v2/custom-node-class.vue)_

vue

```
<template>
  <el-tree-v2
    style="max-width: 600px"
    :data="data"
    show-checkbox
    :expand-on-click-node="false"
    :props="{ class: customNodeClass }"
  />
</template>

<script lang="ts" setup>
import type { TreeNode, TreeNodeData } from 'element-plus'

interface Tree {
  id?: string
  value?: string
  label?: string
  isPenultimate?: boolean
  children?: Tree[]
}

const customNodeClass = ({ isPenultimate }: TreeNodeData, node: TreeNode) =>
  isPenultimate ? 'is-penultimate' : ''

const data: Tree[] = [
  {
    id: '1',
    label: 'Level one 1',
    children: [
      {
        id: '4',
        label: 'Level two 1-1',
        isPenultimate: true,
        children: [
          {
            id: '9',
            label: 'Level three 1-1-1',
          },
          {
            id: '10',
            label: 'Level three 1-1-2',
          },
        ],
      },
    ],
  },
  {
    id: '2',
    label: 'Level one 2',
    isPenultimate: true,
    children: [
      {
        id: '5',
        label: 'Level two 2-1',
      },
      {
        id: '6',
        label: 'Level two 2-2',
      },
    ],
  },
  {
    id: '3',
    label: 'Level one 3',
    isPenultimate: true,
    children: [
      {
        id: '7',
        label: 'Level two 3-1',
      },
      {
        id: '8',
        label: 'Level two 3-2',
      },
    ],
  },
]
</script>

<style scoped>
:deep(.is-penultimate .el-tree-node__label) {
  color: #626aef;
  font-weight: 600;
}
</style>
```

隐藏源代码

## 自定义图标 2.10.3 [​](#自定义图标)

您可以自定义不同节点状态的图标。 树节点暴露了 `expanded` 属性和 `isLeaf` 属性，允许你根据节点的状态动态渲染不同的图标：叶子节点、展开的节点或折叠的节点。

node-1

node-2

node-3

node-4

node-5

node-6

node-7

node-8

node-9

node-10

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZS12MlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgOmhlaWdodD1cIjIwMFwiXG4gID5cbiAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJ7IG5vZGUgfVwiPlxuICAgICAgPGVsLWljb24gY2xhc3M9XCJub2RlLWljb25cIiA6Y2xhc3M9XCJ7ICdpcy1sZWFmJzogbm9kZS5pc0xlYWYgfVwiPlxuICAgICAgICA8RG9jdW1lbnQgdi1pZj1cIm5vZGUuaXNMZWFmXCIgLz5cbiAgICAgICAgPEZvbGRlciB2LWVsc2UtaWY9XCIhbm9kZS5leHBhbmRlZFwiIC8+XG4gICAgICAgIDxGb2xkZXJPcGVuZWQgdi1lbHNlIC8+XG4gICAgICA8L2VsLWljb24+XG4gICAgICA8c3Bhbj57eyBub2RlLmxhYmVsIH19PC9zcGFuPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtdHJlZS12Mj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBEb2N1bWVudCwgRm9sZGVyLCBGb2xkZXJPcGVuZWQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuaW50ZXJmYWNlIFRyZWUge1xuICBpZDogc3RyaW5nXG4gIGxhYmVsOiBzdHJpbmdcbiAgY2hpbGRyZW4/OiBUcmVlW11cbn1cblxuY29uc3QgZ2V0S2V5ID0gKHByZWZpeDogc3RyaW5nLCBpZDogbnVtYmVyKSA9PiB7XG4gIHJldHVybiBgJHtwcmVmaXh9LSR7aWR9YFxufVxuXG5jb25zdCBjcmVhdGVEYXRhID0gKFxuICBtYXhEZWVwOiBudW1iZXIsXG4gIG1heENoaWxkcmVuOiBudW1iZXIsXG4gIG1pbk5vZGVzTnVtYmVyOiBudW1iZXIsXG4gIGRlZXAgPSAxLFxuICBrZXkgPSAnbm9kZSdcbik6IFRyZWVbXSA9PiB7XG4gIGxldCBpZCA9IDBcbiAgcmV0dXJuIEFycmF5LmZyb20oeyBsZW5ndGg6IG1pbk5vZGVzTnVtYmVyIH0pXG4gICAgLmZpbGwoZGVlcClcbiAgICAubWFwKCgpID0+IHtcbiAgICAgIGNvbnN0IGNoaWxkcmVuTnVtYmVyID1cbiAgICAgICAgZGVlcCA9PT0gbWF4RGVlcCA/IDAgOiBNYXRoLnJvdW5kKE1hdGgucmFuZG9tKCkgKiBtYXhDaGlsZHJlbilcbiAgICAgIGNvbnN0IG5vZGVLZXkgPSBnZXRLZXkoa2V5LCArK2lkKVxuICAgICAgcmV0dXJuIHtcbiAgICAgICAgaWQ6IG5vZGVLZXksXG4gICAgICAgIGxhYmVsOiBub2RlS2V5LFxuICAgICAgICBjaGlsZHJlbjogY2hpbGRyZW5OdW1iZXJcbiAgICAgICAgICA/IGNyZWF0ZURhdGEobWF4RGVlcCwgbWF4Q2hpbGRyZW4sIGNoaWxkcmVuTnVtYmVyLCBkZWVwICsgMSwgbm9kZUtleSlcbiAgICAgICAgICA6IHVuZGVmaW5lZCxcbiAgICAgIH1cbiAgICB9KVxufVxuXG5jb25zdCBwcm9wcyA9IHtcbiAgdmFsdWU6ICdpZCcsXG4gIGxhYmVsOiAnbGFiZWwnLFxuICBjaGlsZHJlbjogJ2NoaWxkcmVuJyxcbn1cbmNvbnN0IGRhdGEgPSBjcmVhdGVEYXRhKDQsIDMwLCA0MClcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLm5vZGUtaWNvbiB7XG4gIG1hcmdpbi1yaWdodDogNXB4O1xuICBjb2xvcjogdmFyKC0tZWwtY29sb3Itd2FybmluZyk7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-v2/custom-icon.vue)_

vue

```
<template>
  <el-tree-v2
    style="max-width: 600px"
    :data="data"
    :props="props"
    :height="200"
  >
    <template #default="{ node }">
      <el-icon class="node-icon" :class="{ 'is-leaf': node.isLeaf }">
        <Document v-if="node.isLeaf" />
        <Folder v-else-if="!node.expanded" />
        <FolderOpened v-else />
      </el-icon>
      <span>{{ node.label }}</span>
    </template>
  </el-tree-v2>
</template>

<script lang="ts" setup>
import { Document, Folder, FolderOpened } from '@element-plus/icons-vue'

interface Tree {
  id: string
  label: string
  children?: Tree[]
}

const getKey = (prefix: string, id: number) => {
  return `${prefix}-${id}`
}

const createData = (
  maxDeep: number,
  maxChildren: number,
  minNodesNumber: number,
  deep = 1,
  key = 'node'
): Tree[] => {
  let id = 0
  return Array.from({ length: minNodesNumber })
    .fill(deep)
    .map(() => {
      const childrenNumber =
        deep === maxDeep ? 0 : Math.round(Math.random() * maxChildren)
      const nodeKey = getKey(key, ++id)
      return {
        id: nodeKey,
        label: nodeKey,
        children: childrenNumber
          ? createData(maxDeep, maxChildren, childrenNumber, deep + 1, nodeKey)
          : undefined,
      }
    })
}

const props = {
  value: 'id',
  label: 'label',
  children: 'children',
}
const data = createData(4, 30, 40)
</script>

<style scoped>
.node-icon {
  margin-right: 5px;
  color: var(--el-color-warning);
}
</style>
```

隐藏源代码

## 树节点过滤 2.9.1 [​](#树节点过滤)

`filter-method` 方法只有在版本 `2.9.1` 之后才能接受第三个参数。 树节点是可以被过滤的

在需要对节点进行过滤时，调用 Tree 实例的 `filter` 方法， 参数为关键字。 需要注意的是，此时需要设置 `filter-method`，值为过滤函数。

node-1

node-2

node-3

node-4

node-5

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwicXVlcnlcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBlbnRlciBrZXl3b3JkXCJcbiAgICBAaW5wdXQ9XCJvblF1ZXJ5Q2hhbmdlZFwiXG4gIC8+XG4gIDxlbC10cmVlLXYyXG4gICAgcmVmPVwidHJlZVJlZlwiXG4gICAgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCJcbiAgICA6ZGF0YT1cImRhdGFcIlxuICAgIDpwcm9wcz1cInByb3BzXCJcbiAgICA6ZmlsdGVyLW1ldGhvZD1cImZpbHRlck1ldGhvZFwiXG4gICAgOmhlaWdodD1cIjIwMFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFRyZWVOb2RlRGF0YSwgVHJlZVYySW5zdGFuY2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmludGVyZmFjZSBUcmVlIHtcbiAgaWQ6IHN0cmluZ1xuICBsYWJlbDogc3RyaW5nXG4gIGNoaWxkcmVuPzogVHJlZVtdXG59XG5cbmNvbnN0IGdldEtleSA9IChwcmVmaXg6IHN0cmluZywgaWQ6IG51bWJlcikgPT4gYCR7cHJlZml4fS0ke2lkfWBcblxuY29uc3QgY3JlYXRlRGF0YSA9IChcbiAgbWF4RGVlcDogbnVtYmVyLFxuICBtYXhDaGlsZHJlbjogbnVtYmVyLFxuICBtaW5Ob2Rlc051bWJlcjogbnVtYmVyLFxuICBkZWVwID0gMSxcbiAga2V5ID0gJ25vZGUnXG4pOiBUcmVlW10gPT4ge1xuICBsZXQgaWQgPSAwXG4gIHJldHVybiBBcnJheS5mcm9tKHsgbGVuZ3RoOiBtaW5Ob2Rlc051bWJlciB9KVxuICAgIC5maWxsKGRlZXApXG4gICAgLm1hcCgoKSA9PiB7XG4gICAgICBjb25zdCBjaGlsZHJlbk51bWJlciA9XG4gICAgICAgIGRlZXAgPT09IG1heERlZXAgPyAwIDogTWF0aC5yb3VuZChNYXRoLnJhbmRvbSgpICogbWF4Q2hpbGRyZW4pXG4gICAgICBjb25zdCBub2RlS2V5ID0gZ2V0S2V5KGtleSwgKytpZClcbiAgICAgIHJldHVybiB7XG4gICAgICAgIGlkOiBub2RlS2V5LFxuICAgICAgICBsYWJlbDogbm9kZUtleSxcbiAgICAgICAgY2hpbGRyZW46IGNoaWxkcmVuTnVtYmVyXG4gICAgICAgICAgPyBjcmVhdGVEYXRhKG1heERlZXAsIG1heENoaWxkcmVuLCBjaGlsZHJlbk51bWJlciwgZGVlcCArIDEsIG5vZGVLZXkpXG4gICAgICAgICAgOiB1bmRlZmluZWQsXG4gICAgICB9XG4gICAgfSlcbn1cblxuY29uc3QgcXVlcnkgPSByZWYoJycpXG5jb25zdCB0cmVlUmVmID0gcmVmPFRyZWVWMkluc3RhbmNlPigpXG5jb25zdCBkYXRhID0gY3JlYXRlRGF0YSg0LCAzMCwgNSlcbmNvbnN0IHByb3BzID0ge1xuICB2YWx1ZTogJ2lkJyxcbiAgbGFiZWw6ICdsYWJlbCcsXG4gIGNoaWxkcmVuOiAnY2hpbGRyZW4nLFxufVxuXG5jb25zdCBvblF1ZXJ5Q2hhbmdlZCA9IChxdWVyeTogc3RyaW5nKSA9PiB7XG4gIHRyZWVSZWYudmFsdWUhLmZpbHRlcihxdWVyeSlcbn1cbmNvbnN0IGZpbHRlck1ldGhvZCA9IChxdWVyeTogc3RyaW5nLCBub2RlOiBUcmVlTm9kZURhdGEpID0+XG4gIG5vZGUubGFiZWwhLmluY2x1ZGVzKHF1ZXJ5KVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree-v2/filter.vue)_

vue

```
<template>
  <el-input
    v-model="query"
    style="width: 240px"
    placeholder="Please enter keyword"
    @input="onQueryChanged"
  />
  <el-tree-v2
    ref="treeRef"
    style="max-width: 600px"
    :data="data"
    :props="props"
    :filter-method="filterMethod"
    :height="200"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TreeNodeData, TreeV2Instance } from 'element-plus'

interface Tree {
  id: string
  label: string
  children?: Tree[]
}

const getKey = (prefix: string, id: number) => `${prefix}-${id}`

const createData = (
  maxDeep: number,
  maxChildren: number,
  minNodesNumber: number,
  deep = 1,
  key = 'node'
): Tree[] => {
  let id = 0
  return Array.from({ length: minNodesNumber })
    .fill(deep)
    .map(() => {
      const childrenNumber =
        deep === maxDeep ? 0 : Math.round(Math.random() * maxChildren)
      const nodeKey = getKey(key, ++id)
      return {
        id: nodeKey,
        label: nodeKey,
        children: childrenNumber
          ? createData(maxDeep, maxChildren, childrenNumber, deep + 1, nodeKey)
          : undefined,
      }
    })
}

const query = ref('')
const treeRef = ref<TreeV2Instance>()
const data = createData(4, 30, 5)
const props = {
  value: 'id',
  label: 'label',
  children: 'children',
}

const onQueryChanged = (query: string) => {
  treeRef.value!.filter(query)
}
const filterMethod = (query: string, node: TreeNodeData) =>
  node.label!.includes(query)
</script>
```

隐藏源代码

## TreeV2 API [​](#treev2-api)

### TreeV2 Attributes [​](#treev2-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| data | 展示数据 | `array` | — |
| empty-text | 内容为空的时候展示的文本 | `string` | — |
| [props](#props) | 配置选项，具体看下表 | `object` | — |
| highlight-current | 是否高亮当前选中节点 | `boolean` | false |
| expand-on-click-node | 是否在点击节点的时候展开或者收缩节点， 默认值为 true，如果为 false，则只有点箭头图标的时候才会展开或者收缩节点 | `boolean` | true |
| check-on-click-node | 是否在点击节点的时候选中节点，默认值为 false，即只有在点击复选框时才会选中节点 | `boolean` | false |
| check-on-click-leaf 2.9.6 | 点击叶节点(最后一个子节点)时是否检查或取消节点 | `boolean` | true |
| default-expanded-keys | 默认展开的节点的 key 的数组 | `array` | — |
| show-checkbox | 节点是否可被选择 | `boolean` | false |
| check-strictly | 在显示复选框的情况下，是否严格的遵循父子不互相关联的做法，默认为 false | `boolean` | false |
| default-checked-keys | 默认勾选的节点的 key 的数组 | `array` | — |
| current-node-key | 当前选中的节点 | `string` / `number` | — |
| filter-method | 对树节点进行筛选时执行的方法，返回 true 表示这个节点可以显示， 返回 `false` 则表示这个节点会被隐藏 | `Function` | — |
| indent | 相邻级节点间的水平缩进，单位为像素 | `number` | 16 |
| icon | 自定义树节点图标组件 | `string` / `Component` | — |
| item-size 2.2.33 | 自定义树节点的高度 | `number` | 26 |
| scrollbar-always-on 2.10.4 | 总是显示滚动条 | `boolean` | false |
| height | tree 的高度 | `number` | 200 |

### props [​](#props)

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| value | 每个树节点用来作为唯一标识的属性，在整棵树中应该是唯一的 | `string` | id |
| label | 指定节点标签为节点对象的某个属性值 | `string` | label |
| children | 指定子树为节点对象的某个属性值 | `string` | children |
| disabled | 指定节点选择框是否禁用为节点对象的某个属性值 | `string` | disabled |
| class 2.9.0 | 自定义节点类名 | `string` / `Function` | — |

### TreeV2 Exposes [​](#treev2-exposes)

`Tree` 组件有以下方法，均返回当前选中的节点数组

| 方法 | 说明 | 参数 |
| --- | --- | --- |
| filter | 过滤所有树节点，过滤后的节点将被隐藏 | `(query: string)` |
| getCheckedNodes | 如果节点可以被选中，(`show-checkbox` 为 `true`), 本方法将返回当前选中节点的数组 | `(leafOnly: boolean)` |
| getCheckedKeys | 若节点可用被选中 (`show-checkbox` 为 `true`), 它将返回当前选中节点 key 的数组 | `(leafOnly: boolean)` |
| setCheckedKeys | 通过 keys 设置目前勾选的节点 | `(keys: TreeKey[])` |
| setChecked | 设置节点是否被选中，`deep`（2.14.0 新增）表示是否递归选中/取消选中子节点。 | `(key: TreeKey, checked: boolean, deep?: boolean)` |
| setExpandedKeys | 设置当前展开的节点 | `(keys: TreeKey[])` |
| getHalfCheckedNodes | 如果节点可用被选中 (`show-checkbox` 为 `true`), 它将返回当前半选中的节点组成的数组 | — |
| getHalfCheckedKeys | 若节点可被选中(`show-checkbox` 为 `true`)，则返回目前半选中的节点的 key 所组成的数组 | — |
| getCurrentKey | 获取当前被选中节点的 key，若没有节点被选中则返回 `undefined` | — |
| getCurrentNode | 获取当前被选中节点的 data，若没有节点被选中则返回 `undefined` | — |
| setCurrentKey | 通过 key 设置某个节点的当前选中状态 | `(key: TreeKey)` |
| getNode | 通过 key 或 data 获取节点 | `(data: TreeKey | TreeNodeData)` |
| expandNode | 展开指定节点 | `(node: TreeNode)` |
| collapseNode | 折叠指定节点 | `(node: TreeNode)` |
| setData | 当数据量非常庞大的时候，总是使用响应式数据将导致性能表现不佳，所以我们提供一种显式设置的方式来避免此种情况 | `(data: TreeData)` |
| scrollTo 2.8.0 | 滚动到给定位置 | `(offset: number)` |
| scrollToNode 2.8.0 | 使用给定的滚动策略滚动至指定位置 | `(key: TreeKey, strategy?: auto | smart | center | start | end)` |

### TreeV2 Events [​](#treev2-events)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| node-click | 当节点被点击的时候触发 | `(data: TreeNodeData, node: TreeNode, e: MouseEvent)` |
| node-drop 2.8.3 | 拖放到节点时触发器 | `(data: TreeNodeData, node: TreeNode, e: DragEvent)` |
| node-contextmenu | 当某一节点被鼠标右键点击时会触发该事件 | `(e: Event, data: TreeNodeData, node: TreeNode)` |
| check-change | 当复选框被点击的时候触发 | `(data: TreeNodeData, checked: boolean)` |
| check | 点击节点复选框之后触发 | `(data: TreeNodeData, info: { checkedKeys: TreeKey[],checkedNodes: TreeData, halfCheckedKeys: TreeKey[], halfCheckedNodes: TreeData,})` |
| current-change | 当前选中节点变化时触发的事件 | `(data: TreeNodeData, node: TreeNode)` |
| node-expand | 节点被展开时触发的事件 | `(data: TreeNodeData, node: TreeNode)` |
| node-collapse | 节点被关闭时触发的事件 | `(data: TreeNodeData, node: TreeNode)` |

### TreeV2 Slots [​](#treev2-slots)

| 插槽名 | 描述 | Type |
| --- | --- | --- |
| default | 自定义树节点的内容。 | `object` |
| empty 2.9.0 | 当数据为空时自定义的内容 | — |

## 类型声明 [​](#类型声明)

Show declarations

ts

```
type TreeNodeData = Record<string, any>
type TreeKey = string | number
type TreeData = TreeNodeData[]

interface TreeNode {
  key: TreeKey
  level: number
  parent?: TreeNode
  children?: TreeNode[]
  data: TreeNodeData
  disabled?: boolean
  label?: string
  isLeaf?: boolean
  expanded?: boolean
  isEffectivelyChecked?: boolean
}
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/tree-v2) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/tree-v2.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/24290011?v=4&size=64)](https://github.com/xingyixiang)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/75007029?v=4&size=64)](https://github.com/yj-liuzepeng)[![](https://avatars.githubusercontent.com/u/59350883?v=4&size=64)](https://github.com/init-qy)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/33687038?v=4&size=64)](https://github.com/guozi9999)[![](https://avatars.githubusercontent.com/u/53589602?v=4&size=64)](https://github.com/l246804)[![](https://avatars.githubusercontent.com/u/16463481?v=4&size=64)](https://github.com/hellomrbigshot)[![](https://avatars.githubusercontent.com/u/54931083?v=4&size=64)](https://github.com/wjp980108)[![](https://avatars.githubusercontent.com/u/69580637?v=4&size=64)](https://github.com/jevin98)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/14892120?v=4&size=64)](https://github.com/scvzerng)[![](https://avatars.githubusercontent.com/u/33497338?v=4&size=64)](https://github.com/MoConWu)[![](https://avatars.githubusercontent.com/u/35138018?v=4&size=64)](https://github.com/tuskermanshu)[![](https://avatars.githubusercontent.com/u/47178158?v=4&size=64)](https://github.com/Aaron-zon)[![](https://avatars.githubusercontent.com/u/159113473?v=4&size=64)](https://github.com/huangjw1997)[![](https://avatars.githubusercontent.com/u/26035718?v=4&size=64)](https://github.com/SnowingFox)[![](https://avatars.githubusercontent.com/u/5389932?v=4&size=64)](https://github.com/muuyao)[![](https://avatars.githubusercontent.com/u/77471461?v=4&size=64)](https://github.com/qinhuangdaoooo)[![](https://avatars.githubusercontent.com/u/22515951?v=4&size=64)](https://github.com/webfansplz)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/9244703?v=4&size=64)](https://github.com/JobinJia)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/49394793?v=4&size=64)](https://github.com/bxh1071)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/49453941?v=4&size=64)](https://github.com/maxime-bc)[![](https://avatars.githubusercontent.com/u/38248854?v=4&size=64)](https://github.com/Yueyanc)

[Tree 树形控件](https://element-plus.org/zh-CN/component/tree)

[Statistic 统计组件](https://element-plus.org/zh-CN/component/statistic)


