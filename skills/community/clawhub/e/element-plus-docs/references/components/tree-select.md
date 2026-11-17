## TreeSelect 树形选择 ​

**URL:** https://element-plus.org/zh-CN/component/tree-select

**Contents:**
- TreeSelect 树形选择 ​
- 基础用法 ​
- 选择任意级别 ​
- 多选 ​
- 禁用选项 ​
- 可筛选 ​
- 自定义内容 ​
- 懒加载 ​
- 使用 node-key 属性 ​
- API ​

含有下拉菜单的树形选择器，结合了 el-tree 和 el-select 两个组件的功能。

当属性 check-strictly=true 时，任何节点都可以被选择，否则只有子节点可被选择。

当使用 show-checkbox时，由于 check-on-click-node 默认值是 false，这时候只能通过 checkbox 来选中，当然您也可以将其设置成 true，这样点击整个 node 都可以用来完成选择

在使用 show-checkbox 时，因为 check-on-click-leaf 默认值为 true， 最后一个树节点可以通过点击节点进行勾选。

使用关键字筛选或自定义筛选方法。 filterMethod可以自定义数据筛选的方法， filterNodeMethod可以自定义节点数据筛选的方法。

默认情况下，modelValue 会查找 value 键。 对于其他数据结构，必须提供 node-key 才能正常工作。

由于这个组件是el-tree和el-select的结合体，他们的原始属性未被更改，故不在此重复。请跳转查看原组件的相应文档。

在 Tree 和 Select 组件下暴露方法的方式已被 弃用，并将于 3.0.0 中 移除，请在各自的组件层级下使用这些方法：tree 和 select。

**Examples:**

Example 1 (vue):
```vue
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

Example 2 (vue):
```vue
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

Example 3 (vue):
```vue
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

Example 4 (vue):
```vue
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

---
