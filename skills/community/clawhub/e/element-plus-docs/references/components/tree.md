## Tree 树形控件 ​

**URL:** https://element-plus.org/zh-CN/component/tree

**Contents:**
- Tree 树形控件 ​
- 基础用法 ​
- 可选择 ​
- 懒加载自定义叶子节点 ​
- 多次懒加载 2.6.3 ​
- 禁用复选框 ​
- 默认展开以及默认选中 ​
- 树节点的选择 ​
- 自定义节点内容 ​
- 自定义节点类名 ​

在使用 show-checkbox 时，因为 check-on-click-leaf 默认值为 true， 最后一个树节点可以通过点击节点进行勾选。

由于在点击节点时才进行该层数据的获取，默认情况下 Tree 无法预知某个节点是否为叶子节点， 所以会为每个节点添加一个下拉按钮，如果节点没有下层数据，则点击后下拉按钮会消失。 同时，你也可以提前告知 Tree 某个节点是否为叶子节点，从而避免在叶子节点前渲染下拉按钮。

加载远程节点数据时，懒加载有时可能失败。 在这种情况下，您可以调用 reject 以保持节点状态，并允许远程加载继续。

在示例中，通过 disabled 设置禁用状态。 相应的复选框已禁用，不能点击。

树节点可以在初始化阶段被设置为展开和选中。

分别通过 default-expanded-keys 和 default-checked-keys 设置默认展开和默认选中的节点。 需要注意的是，此时必须设置 node-key， 其值为节点数据中的一个字段名，该字段在整棵树中是唯一的。

本例展示如何获取和设置选中节点。 获取和设置各有两种方式：通过 node 或通过 key。 如果需要通过 key 来获取或设置，则必须设置 node-key。

节点的内容支持自定义，可以在节点区添加按钮或图标等内容

可以通过两种方法进行树节点内容的自定义：render-content 和 scoped slot。 使用 render-content 指定渲染函数，该函数返回需要的节点区内容即可。 渲染函数的用法请参考 Vue 文档。 使用 scoped slot 会传入两个参数 node 和 data，分别表示当前节点的 Node 对象和当前节点的数据。 注意：由于 JSFiddle 不支持 JSX 语法，所以 render-content 示例无法在那里运行。 但是在实际的项目中，只要正确地配置了相关依赖，就可以正常运行。

使用 props.class 来建立节点的类名。

调用 Tree 实例对象的 filter 方法来过滤树节点。 方法的参数就是过滤关键字。 需要注意的是，此时需要设置 filter-node-method 属性，其值为过滤函数。

通过 draggable 属性可让节点变为可拖拽

Tree 组件有以下方法，均返回当前选中的节点数组

**Examples:**

Example 1 (typescript):
```typescript
<template>
  <el-tree
    style="max-width: 600px"
    :data="data"
    :props="defaultProps"
    @node-click="handleNodeClick"
  />
</template>

<script lang="ts" setup>
interface Tree {
  label: string
  children?: Tree[]
}

const handleNodeClick = (data: Tree) => {
  console.log(data)
}

const data: Tree[] = [
  {
    label: 'Level one 1',
    children: [
      {
        label: 'Level two 1-1',
        children: [
          {
            label: 'Level three 1-1-1',
          },
        ],
      },
    ],
  },
  {
    label: 'Level one 2',
    children: [
      {
        label: 'Level two 2-1',
        children: [
          {
            label: 'Level three 2-1-1',
          },
        ],
      },
      {
        label: 'Level two 2-2',
        children: [
          {
            label: 'Level three 2-2-1',
          },
        ],
      },
    ],
  },
  {
    label: 'Level one 3',
    children: [
      {
        label: 'Level two 3-1',
        children: [
          {
            label: 'Level three 3-1-1',
          },
        ],
      },
      {
        label: 'Level two 3-2',
        children: [
          {
            label: 'Level three 3-2-1',
          },
        ],
      },
    ],
  },
]

const defaultProps = {
  children: 'children',
  label: 'label',
}
</script>
```

Example 2 (typescript):
```typescript
<template>
  <el-tree
    style="max-width: 600px"
    :props="props"
    :load="loadNode"
    lazy
    show-checkbox
    @check-change="handleCheckChange"
  />
</template>

<script lang="ts" setup>
import type { LoadFunction } from 'element-plus'

interface Tree {
  name: string
}

let count = 1
const props = {
  label: 'name',
  children: 'zones',
}

const handleCheckChange = (
  data: Tree,
  checked: boolean,
  indeterminate: boolean
) => {
  console.log(data, checked, indeterminate)
}

const loadNode: LoadFunction = (node, resolve) => {
  if (node.level === 0) {
    return resolve([{ name: 'Root1' }, { name: 'Root2' }])
  }
  if (node.level > 3) return resolve([])

  let hasChild = false
  if (node.data.name === 'region1') {
    hasChild = true
  } else if (node.data.name === 'region2') {
    hasChild = false
  } else {
    hasChild = Math.random() > 0.5
  }

  setTimeout(() => {
    let data: Tree[] = []
    if (hasChild) {
      data = [
        {
          name: `zone${count++}`,
        },
        {
          name: `zone${count++}`,
        },
      ]
    } else {
      data = []
    }

    resolve(data)
  }, 500)
}
</script>
```

Example 3 (typescript):
```typescript
<template>
  <el-tree
    style="max-width: 600px"
    :props="props"
    :load="loadNode"
    lazy
    show-checkbox
  />
</template>

<script lang="ts" setup>
import type { LoadFunction } from 'element-plus'

interface Tree {
  name: string
  leaf?: boolean
}

const props = {
  label: 'name',
  children: 'zones',
  isLeaf: 'leaf',
}

const loadNode: LoadFunction = (node, resolve) => {
  if (node.level === 0) {
    return resolve([{ name: 'region' }])
  }
  if (node.level > 1) return resolve([])

  setTimeout(() => {
    const data: Tree[] = [
      {
        name: 'leaf',
        leaf: true,
      },
      {
        name: 'zone',
      },
    ]

    resolve(data)
  }, 500)
}
</script>
```

Example 4 (typescript):
```typescript
<template>
  <el-tree style="max-width: 600px" :props="props" :load="loadNode" lazy />
</template>

<script lang="ts" setup>
import type { LoadFunction } from 'element-plus'

const props = {
  label: 'name',
  children: 'zones',
  isLeaf: 'leaf',
}

let time = 0
const loadNode: LoadFunction = (node, resolve, reject) => {
  if (node.level === 0) {
    return resolve([{ name: 'region' }])
  }
  time++
  if (node.level >= 1) {
    setTimeout(() => {
      if (time > 3) {
        return resolve([
          { name: 'zone1', leaf: true },
          { name: 'zone2', leaf: true },
          { name: 'zone3', leaf: true },
        ])
      } else {
        return reject()
      }
    }, 3000)
  }
}
</script>
```

---
