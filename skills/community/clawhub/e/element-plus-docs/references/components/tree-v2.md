## Tree V2 虚拟化树形控件beta ​

**URL:** https://element-plus.org/zh-CN/component/tree-v2

**Contents:**
- Tree V2 虚拟化树形控件beta ​
- 基础用法 ​
- 可选择的虚拟树 ​
- 禁用复选框 ​
- 默认扩展和默认检查 ​
- 自定义节点内容 ​
- 自定义节点类 2.9.0 ​
- 自定义图标 2.10.3 ​
- 树节点过滤 2.9.1 ​
- TreeV2 API ​

不论你的数据量多大，虚拟树都能毫无压力地处理。

在使用 show-checkbox 时，因为 check-on-click-leaf 默认值为 true， 最后一个树节点可以通过点击节点进行勾选。

在示例中，属性在 defaultProps 中声明了 disabled，一些节点被设置为 disabled：true。 相应的复选框已禁用，不能点击。

树节点可以在初始化阶段被设置为展开或选中。

分别通过 default-expanded-keys 和 default-checked-keys 设置默认展开和默认选中的节点。

节点的内容支持自定义，可以在节点区添加按钮或图标等内容

您可以自定义不同节点状态的图标。 树节点暴露了 expanded 属性和 isLeaf 属性，允许你根据节点的状态动态渲染不同的图标：叶子节点、展开的节点或折叠的节点。

filter-method 方法只有在版本 2.9.1 之后才能接受第三个参数。 树节点是可以被过滤的

在需要对节点进行过滤时，调用 Tree 实例的 filter 方法， 参数为关键字。 需要注意的是，此时需要设置 filter-method，值为过滤函数。

Tree 组件有以下方法，均返回当前选中的节点数组

**Examples:**

Example 1 (typescript):
```typescript
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

Example 2 (typescript):
```typescript
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

Example 3 (typescript):
```typescript
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

Example 4 (typescript):
```typescript
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

---
