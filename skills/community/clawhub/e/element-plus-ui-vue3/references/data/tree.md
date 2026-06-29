---
name: "tree"
description: "Tree 树形控件 -- Element Plus Vue3 桌面端组件。Invoke when user needs Tree 树形控件 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/tree.html"
---

---

# Tree 树形控件 [​](#tree-树形控件)

更新日志待解决

77

用清晰的层级结构展示信息，可展开或折叠。

## 基础用法 [​](#基础用法)

基础的树形结构展示

Level one 1

Level one 2

Level one 3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZVxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6cHJvcHM9XCJkZWZhdWx0UHJvcHNcIlxuICAgIEBub2RlLWNsaWNrPVwiaGFuZGxlTm9kZUNsaWNrXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbnRlcmZhY2UgVHJlZSB7XG4gIGxhYmVsOiBzdHJpbmdcbiAgY2hpbGRyZW4/OiBUcmVlW11cbn1cblxuY29uc3QgaGFuZGxlTm9kZUNsaWNrID0gKGRhdGE6IFRyZWUpID0+IHtcbiAgY29uc29sZS5sb2coZGF0YSlcbn1cblxuY29uc3QgZGF0YTogVHJlZVtdID0gW1xuICB7XG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMS0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDEtMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMicsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDItMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDItMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMycsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuXG5jb25zdCBkZWZhdWx0UHJvcHMgPSB7XG4gIGNoaWxkcmVuOiAnY2hpbGRyZW4nLFxuICBsYWJlbDogJ2xhYmVsJyxcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/basic.vue)_

vue

```
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

隐藏源代码

## 可选择 [​](#可选择)

适用于需要选择层级时使用。

本例还展示了动态加载节点数据的方法。

Root1

Root2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZVxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOnByb3BzPVwicHJvcHNcIlxuICAgIDpsb2FkPVwibG9hZE5vZGVcIlxuICAgIGxhenlcbiAgICBzaG93LWNoZWNrYm94XG4gICAgQGNoZWNrLWNoYW5nZT1cImhhbmRsZUNoZWNrQ2hhbmdlXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgdHlwZSB7IExvYWRGdW5jdGlvbiB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW50ZXJmYWNlIFRyZWUge1xuICBuYW1lOiBzdHJpbmdcbn1cblxubGV0IGNvdW50ID0gMVxuY29uc3QgcHJvcHMgPSB7XG4gIGxhYmVsOiAnbmFtZScsXG4gIGNoaWxkcmVuOiAnem9uZXMnLFxufVxuXG5jb25zdCBoYW5kbGVDaGVja0NoYW5nZSA9IChcbiAgZGF0YTogVHJlZSxcbiAgY2hlY2tlZDogYm9vbGVhbixcbiAgaW5kZXRlcm1pbmF0ZTogYm9vbGVhblxuKSA9PiB7XG4gIGNvbnNvbGUubG9nKGRhdGEsIGNoZWNrZWQsIGluZGV0ZXJtaW5hdGUpXG59XG5cbmNvbnN0IGxvYWROb2RlOiBMb2FkRnVuY3Rpb24gPSAobm9kZSwgcmVzb2x2ZSkgPT4ge1xuICBpZiAobm9kZS5sZXZlbCA9PT0gMCkge1xuICAgIHJldHVybiByZXNvbHZlKFt7IG5hbWU6ICdSb290MScgfSwgeyBuYW1lOiAnUm9vdDInIH1dKVxuICB9XG4gIGlmIChub2RlLmxldmVsID4gMykgcmV0dXJuIHJlc29sdmUoW10pXG5cbiAgbGV0IGhhc0NoaWxkID0gZmFsc2VcbiAgaWYgKG5vZGUuZGF0YS5uYW1lID09PSAncmVnaW9uMScpIHtcbiAgICBoYXNDaGlsZCA9IHRydWVcbiAgfSBlbHNlIGlmIChub2RlLmRhdGEubmFtZSA9PT0gJ3JlZ2lvbjInKSB7XG4gICAgaGFzQ2hpbGQgPSBmYWxzZVxuICB9IGVsc2Uge1xuICAgIGhhc0NoaWxkID0gTWF0aC5yYW5kb20oKSA+IDAuNVxuICB9XG5cbiAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgbGV0IGRhdGE6IFRyZWVbXSA9IFtdXG4gICAgaWYgKGhhc0NoaWxkKSB7XG4gICAgICBkYXRhID0gW1xuICAgICAgICB7XG4gICAgICAgICAgbmFtZTogYHpvbmUke2NvdW50Kyt9YCxcbiAgICAgICAgfSxcbiAgICAgICAge1xuICAgICAgICAgIG5hbWU6IGB6b25lJHtjb3VudCsrfWAsXG4gICAgICAgIH0sXG4gICAgICBdXG4gICAgfSBlbHNlIHtcbiAgICAgIGRhdGEgPSBbXVxuICAgIH1cblxuICAgIHJlc29sdmUoZGF0YSlcbiAgfSwgNTAwKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/selectable.vue)_

vue

```
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

隐藏源代码

WARNING

在使用 show-checkbox 时，因为 `check-on-click-leaf` 默认值为 true， 最后一个树节点可以通过点击节点进行勾选。

## 懒加载自定义叶子节点 [​](#懒加载自定义叶子节点)

由于在点击节点时才进行该层数据的获取，默认情况下 Tree 无法预知某个节点是否为叶子节点， 所以会为每个节点添加一个下拉按钮，如果节点没有下层数据，则点击后下拉按钮会消失。 同时，你也可以提前告知 Tree 某个节点是否为叶子节点，从而避免在叶子节点前渲染下拉按钮。

region

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZVxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOnByb3BzPVwicHJvcHNcIlxuICAgIDpsb2FkPVwibG9hZE5vZGVcIlxuICAgIGxhenlcbiAgICBzaG93LWNoZWNrYm94XG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHR5cGUgeyBMb2FkRnVuY3Rpb24gfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmludGVyZmFjZSBUcmVlIHtcbiAgbmFtZTogc3RyaW5nXG4gIGxlYWY/OiBib29sZWFuXG59XG5cbmNvbnN0IHByb3BzID0ge1xuICBsYWJlbDogJ25hbWUnLFxuICBjaGlsZHJlbjogJ3pvbmVzJyxcbiAgaXNMZWFmOiAnbGVhZicsXG59XG5cbmNvbnN0IGxvYWROb2RlOiBMb2FkRnVuY3Rpb24gPSAobm9kZSwgcmVzb2x2ZSkgPT4ge1xuICBpZiAobm9kZS5sZXZlbCA9PT0gMCkge1xuICAgIHJldHVybiByZXNvbHZlKFt7IG5hbWU6ICdyZWdpb24nIH1dKVxuICB9XG4gIGlmIChub2RlLmxldmVsID4gMSkgcmV0dXJuIHJlc29sdmUoW10pXG5cbiAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgY29uc3QgZGF0YTogVHJlZVtdID0gW1xuICAgICAge1xuICAgICAgICBuYW1lOiAnbGVhZicsXG4gICAgICAgIGxlYWY6IHRydWUsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBuYW1lOiAnem9uZScsXG4gICAgICB9LFxuICAgIF1cblxuICAgIHJlc29sdmUoZGF0YSlcbiAgfSwgNTAwKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/custom-leaf.vue)_

vue

```
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

隐藏源代码

## 多次懒加载 2.6.3 [​](#多次懒加载)

加载远程节点数据时，懒加载有时可能失败。 在这种情况下，您可以调用 reject 以保持节点状态，并允许远程加载继续。

region

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZSBzdHlsZT1cIm1heC13aWR0aDogNjAwcHhcIiA6cHJvcHM9XCJwcm9wc1wiIDpsb2FkPVwibG9hZE5vZGVcIiBsYXp5IC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHR5cGUgeyBMb2FkRnVuY3Rpb24gfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHByb3BzID0ge1xuICBsYWJlbDogJ25hbWUnLFxuICBjaGlsZHJlbjogJ3pvbmVzJyxcbiAgaXNMZWFmOiAnbGVhZicsXG59XG5cbmxldCB0aW1lID0gMFxuY29uc3QgbG9hZE5vZGU6IExvYWRGdW5jdGlvbiA9IChub2RlLCByZXNvbHZlLCByZWplY3QpID0+IHtcbiAgaWYgKG5vZGUubGV2ZWwgPT09IDApIHtcbiAgICByZXR1cm4gcmVzb2x2ZShbeyBuYW1lOiAncmVnaW9uJyB9XSlcbiAgfVxuICB0aW1lKytcbiAgaWYgKG5vZGUubGV2ZWwgPj0gMSkge1xuICAgIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgaWYgKHRpbWUgPiAzKSB7XG4gICAgICAgIHJldHVybiByZXNvbHZlKFtcbiAgICAgICAgICB7IG5hbWU6ICd6b25lMScsIGxlYWY6IHRydWUgfSxcbiAgICAgICAgICB7IG5hbWU6ICd6b25lMicsIGxlYWY6IHRydWUgfSxcbiAgICAgICAgICB7IG5hbWU6ICd6b25lMycsIGxlYWY6IHRydWUgfSxcbiAgICAgICAgXSlcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiByZWplY3QoKVxuICAgICAgfVxuICAgIH0sIDMwMDApXG4gIH1cbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/multiple-times-load.vue)_

vue

```
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

隐藏源代码

## 禁用复选框 [​](#禁用复选框)

节点的复选框可以设置为禁用。

在示例中，通过 disabled 设置禁用状态。 相应的复选框已禁用，不能点击。

Level one 1

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZVxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6cHJvcHM9XCJkZWZhdWx0UHJvcHNcIlxuICAgIHNob3ctY2hlY2tib3hcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5jb25zdCBkZWZhdWx0UHJvcHMgPSB7XG4gIGNoaWxkcmVuOiAnY2hpbGRyZW4nLFxuICBsYWJlbDogJ2xhYmVsJyxcbiAgZGlzYWJsZWQ6ICdkaXNhYmxlZCcsXG59XG5cbmNvbnN0IGRhdGEgPSBbXG4gIHtcbiAgICBpZDogMSxcbiAgICBsYWJlbDogJ0xldmVsIG9uZSAxJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICBpZDogMyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBpZDogNCxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMy0xLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgaWQ6IDUsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMS0yJyxcbiAgICAgICAgICAgIGRpc2FibGVkOiB0cnVlLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogMixcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0yJyxcbiAgICAgICAgZGlzYWJsZWQ6IHRydWUsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgaWQ6IDYsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGlkOiA3LFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAzLTItMicsXG4gICAgICAgICAgICBkaXNhYmxlZDogdHJ1ZSxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/disabled.vue)_

vue

```
<template>
  <el-tree
    style="max-width: 600px"
    :data="data"
    :props="defaultProps"
    show-checkbox
  />
</template>

<script lang="ts" setup>
const defaultProps = {
  children: 'children',
  label: 'label',
  disabled: 'disabled',
}

const data = [
  {
    id: 1,
    label: 'Level one 1',
    children: [
      {
        id: 3,
        label: 'Level two 2-1',
        children: [
          {
            id: 4,
            label: 'Level three 3-1-1',
          },
          {
            id: 5,
            label: 'Level three 3-1-2',
            disabled: true,
          },
        ],
      },
      {
        id: 2,
        label: 'Level two 2-2',
        disabled: true,
        children: [
          {
            id: 6,
            label: 'Level three 3-2-1',
          },
          {
            id: 7,
            label: 'Level three 3-2-2',
            disabled: true,
          },
        ],
      },
    ],
  },
]
</script>
```

隐藏源代码

## 默认展开以及默认选中 [​](#默认展开以及默认选中)

树节点可以在初始化阶段被设置为展开和选中。

分别通过 `default-expanded-keys` 和 `default-checked-keys` 设置默认展开和默认选中的节点。 需要注意的是，此时必须设置 `node-key`， 其值为节点数据中的一个字段名，该字段在整棵树中是唯一的。

Level one 1

Level one 2

Level two 2-1

Level two 2-2

Level one 3

Level two 3-1

Level two 3-2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZVxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICBzaG93LWNoZWNrYm94XG4gICAgbm9kZS1rZXk9XCJpZFwiXG4gICAgOmRlZmF1bHQtZXhwYW5kZWQta2V5cz1cIlsyLCAzXVwiXG4gICAgOmRlZmF1bHQtY2hlY2tlZC1rZXlzPVwiWzVdXCJcbiAgICA6cHJvcHM9XCJkZWZhdWx0UHJvcHNcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IGRlZmF1bHRQcm9wcyA9IHtcbiAgY2hpbGRyZW46ICdjaGlsZHJlbicsXG4gIGxhYmVsOiAnbGFiZWwnLFxufVxuY29uc3QgZGF0YSA9IFtcbiAge1xuICAgIGlkOiAxLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDEnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIGlkOiA0LFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAxLTEnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGlkOiA5LFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAxLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBpZDogMTAsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDEtMS0yJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgaWQ6IDIsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMicsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgaWQ6IDUsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDItMScsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogNixcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0yJyxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIGlkOiAzLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDMnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIGlkOiA3LFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAzLTEnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IDgsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDMtMicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/default-state.vue)_

vue

```
<template>
  <el-tree
    style="max-width: 600px"
    :data="data"
    show-checkbox
    node-key="id"
    :default-expanded-keys="[2, 3]"
    :default-checked-keys="[5]"
    :props="defaultProps"
  />
</template>

<script lang="ts" setup>
const defaultProps = {
  children: 'children',
  label: 'label',
}
const data = [
  {
    id: 1,
    label: 'Level one 1',
    children: [
      {
        id: 4,
        label: 'Level two 1-1',
        children: [
          {
            id: 9,
            label: 'Level three 1-1-1',
          },
          {
            id: 10,
            label: 'Level three 1-1-2',
          },
        ],
      },
    ],
  },
  {
    id: 2,
    label: 'Level one 2',
    children: [
      {
        id: 5,
        label: 'Level two 2-1',
      },
      {
        id: 6,
        label: 'Level two 2-2',
      },
    ],
  },
  {
    id: 3,
    label: 'Level one 3',
    children: [
      {
        id: 7,
        label: 'Level two 3-1',
      },
      {
        id: 8,
        label: 'Level two 3-2',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 树节点的选择 [​](#树节点的选择)

本例展示如何获取和设置选中节点。 获取和设置各有两种方式：通过 node 或通过 key。 如果需要通过 key 来获取或设置，则必须设置 `node-key`。

Level one 1

Level two 1-1

Level three 1-1-1

Level three 1-1-2

Level one 2

Level two 2-1

Level two 2-2

Level one 3

Level two 3-1

Level two 3-2

get by nodeget by keyset by nodeset by keyreset

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZVxuICAgIHJlZj1cInRyZWVSZWZcIlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICBzaG93LWNoZWNrYm94XG4gICAgZGVmYXVsdC1leHBhbmQtYWxsXG4gICAgbm9kZS1rZXk9XCJpZFwiXG4gICAgaGlnaGxpZ2h0LWN1cnJlbnRcbiAgICA6cHJvcHM9XCJkZWZhdWx0UHJvcHNcIlxuICAvPlxuXG4gIDxkaXYgY2xhc3M9XCJmbGV4IGZsZXgtd3JhcCBnYXAtMSBtdC0yXCI+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgQGNsaWNrPVwiZ2V0Q2hlY2tlZE5vZGVzXCI+Z2V0IGJ5IG5vZGU8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBAY2xpY2s9XCJnZXRDaGVja2VkS2V5c1wiPmdldCBieSBrZXk8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBAY2xpY2s9XCJzZXRDaGVja2VkTm9kZXNcIj5zZXQgYnkgbm9kZTwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY2xhc3M9XCIhbWwtMFwiIEBjbGljaz1cInNldENoZWNrZWRLZXlzXCI+c2V0IGJ5IGtleTwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY2xhc3M9XCIhbWwtMFwiIEBjbGljaz1cInJlc2V0Q2hlY2tlZFwiPnJlc2V0PC9lbC1idXR0b24+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBSZW5kZXJDb250ZW50Q29udGV4dCwgVHJlZUluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbnRlcmZhY2UgVHJlZSB7XG4gIGlkOiBudW1iZXJcbiAgbGFiZWw6IHN0cmluZ1xuICBjaGlsZHJlbj86IFRyZWVbXVxufVxudHlwZSBOb2RlID0gUmVuZGVyQ29udGVudENvbnRleHRbJ25vZGUnXVxuXG5jb25zdCB0cmVlUmVmID0gcmVmPFRyZWVJbnN0YW5jZT4oKVxuXG5jb25zdCBnZXRDaGVja2VkTm9kZXMgPSAoKSA9PiB7XG4gIGNvbnNvbGUubG9nKHRyZWVSZWYudmFsdWUhLmdldENoZWNrZWROb2RlcyhmYWxzZSwgZmFsc2UpKVxufVxuY29uc3QgZ2V0Q2hlY2tlZEtleXMgPSAoKSA9PiB7XG4gIGNvbnNvbGUubG9nKHRyZWVSZWYudmFsdWUhLmdldENoZWNrZWRLZXlzKGZhbHNlKSlcbn1cbmNvbnN0IHNldENoZWNrZWROb2RlcyA9ICgpID0+IHtcbiAgdHJlZVJlZi52YWx1ZSEuc2V0Q2hlY2tlZE5vZGVzKFxuICAgIFtcbiAgICAgIHtcbiAgICAgICAgaWQ6IDUsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDItMScsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogOSxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAxLTEtMScsXG4gICAgICB9LFxuICAgIF0gYXMgTm9kZVtdLFxuICAgIGZhbHNlXG4gIClcbn1cbmNvbnN0IHNldENoZWNrZWRLZXlzID0gKCkgPT4ge1xuICB0cmVlUmVmLnZhbHVlIS5zZXRDaGVja2VkS2V5cyhbM10sIGZhbHNlKVxufVxuY29uc3QgcmVzZXRDaGVja2VkID0gKCkgPT4ge1xuICB0cmVlUmVmLnZhbHVlIS5zZXRDaGVja2VkS2V5cyhbXSwgZmFsc2UpXG59XG5cbmNvbnN0IGRlZmF1bHRQcm9wcyA9IHtcbiAgY2hpbGRyZW46ICdjaGlsZHJlbicsXG4gIGxhYmVsOiAnbGFiZWwnLFxufVxuXG5jb25zdCBkYXRhOiBUcmVlW10gPSBbXG4gIHtcbiAgICBpZDogMSxcbiAgICBsYWJlbDogJ0xldmVsIG9uZSAxJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICBpZDogNCxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMS0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBpZDogOSxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMS0xLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgaWQ6IDEwLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAxLTEtMicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIGlkOiAyLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDInLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIGlkOiA1LFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAyLTEnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IDYsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDItMicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICBpZDogMyxcbiAgICBsYWJlbDogJ0xldmVsIG9uZSAzJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICBpZDogNyxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0xJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiA4LFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAzLTInLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/checking-tree.vue)_

vue

```
<template>
  <el-tree
    ref="treeRef"
    style="max-width: 600px"
    :data="data"
    show-checkbox
    default-expand-all
    node-key="id"
    highlight-current
    :props="defaultProps"
  />

  <div class="flex flex-wrap gap-1 mt-2">
    <el-button class="!ml-0" @click="getCheckedNodes">get by node</el-button>
    <el-button class="!ml-0" @click="getCheckedKeys">get by key</el-button>
    <el-button class="!ml-0" @click="setCheckedNodes">set by node</el-button>
    <el-button class="!ml-0" @click="setCheckedKeys">set by key</el-button>
    <el-button class="!ml-0" @click="resetChecked">reset</el-button>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { RenderContentContext, TreeInstance } from 'element-plus'

interface Tree {
  id: number
  label: string
  children?: Tree[]
}
type Node = RenderContentContext['node']

const treeRef = ref<TreeInstance>()

const getCheckedNodes = () => {
  console.log(treeRef.value!.getCheckedNodes(false, false))
}
const getCheckedKeys = () => {
  console.log(treeRef.value!.getCheckedKeys(false))
}
const setCheckedNodes = () => {
  treeRef.value!.setCheckedNodes(
    [
      {
        id: 5,
        label: 'Level two 2-1',
      },
      {
        id: 9,
        label: 'Level three 1-1-1',
      },
    ] as Node[],
    false
  )
}
const setCheckedKeys = () => {
  treeRef.value!.setCheckedKeys([3], false)
}
const resetChecked = () => {
  treeRef.value!.setCheckedKeys([], false)
}

const defaultProps = {
  children: 'children',
  label: 'label',
}

const data: Tree[] = [
  {
    id: 1,
    label: 'Level one 1',
    children: [
      {
        id: 4,
        label: 'Level two 1-1',
        children: [
          {
            id: 9,
            label: 'Level three 1-1-1',
          },
          {
            id: 10,
            label: 'Level three 1-1-2',
          },
        ],
      },
    ],
  },
  {
    id: 2,
    label: 'Level one 2',
    children: [
      {
        id: 5,
        label: 'Level two 2-1',
      },
      {
        id: 6,
        label: 'Level two 2-2',
      },
    ],
  },
  {
    id: 3,
    label: 'Level one 3',
    children: [
      {
        id: 7,
        label: 'Level two 3-1',
      },
      {
        id: 8,
        label: 'Level two 3-2',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 自定义节点内容 [​](#自定义节点内容)

节点的内容支持自定义，可以在节点区添加按钮或图标等内容

可以通过两种方法进行树节点内容的自定义：`render-content` 和 scoped slot。 使用 `render-content` 指定渲染函数，该函数返回需要的节点区内容即可。 渲染函数的用法请参考 Vue 文档。 使用 scoped slot 会传入两个参数 `node` 和 `data`，分别表示当前节点的 Node 对象和当前节点的数据。 注意：由于 JSFiddle 不支持 JSX 语法，所以 `render-content` 示例无法在那里运行。 但是在实际的项目中，只要正确地配置了相关依赖，就可以正常运行。

Using render-content

Level one 1

AppendDelete

Level two 1-1

AppendDelete

Level three 1-1-1

AppendDelete

Level three 1-1-2

AppendDelete

Level one 2

AppendDelete

Level two 2-1

AppendDelete

Level two 2-2

AppendDelete

Level one 3

AppendDelete

Level two 3-1

AppendDelete

Level two 3-2

AppendDelete

Using scoped slot

Level one 1

Append Delete

Level two 1-1

Append Delete

Level three 1-1-1

Append Delete

Level three 1-1-2

Append Delete

Level one 2

Append Delete

Level two 2-1

Append Delete

Level two 2-2

Append Delete

Level one 3

Append Delete

Level two 3-1

Append Delete

Level two 3-2

Append Delete

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY3VzdG9tLXRyZWUtY29udGFpbmVyXCI+XG4gICAgPHA+VXNpbmcgcmVuZGVyLWNvbnRlbnQ8L3A+XG4gICAgPGVsLXRyZWVcbiAgICAgIHJlZj1cInRyZWVSZWYxXCJcbiAgICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgICA6ZGF0YT1cImRhdGFTb3VyY2VcIlxuICAgICAgc2hvdy1jaGVja2JveFxuICAgICAgbm9kZS1rZXk9XCJpZFwiXG4gICAgICBkZWZhdWx0LWV4cGFuZC1hbGxcbiAgICAgIDpleHBhbmQtb24tY2xpY2stbm9kZT1cImZhbHNlXCJcbiAgICAgIDpyZW5kZXItY29udGVudD1cInJlbmRlckNvbnRlbnRcIlxuICAgIC8+XG4gICAgPHA+VXNpbmcgc2NvcGVkIHNsb3Q8L3A+XG4gICAgPGVsLXRyZWVcbiAgICAgIHJlZj1cInRyZWVSZWYyXCJcbiAgICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgICA6ZGF0YT1cImRhdGFTb3VyY2VcIlxuICAgICAgc2hvdy1jaGVja2JveFxuICAgICAgbm9kZS1rZXk9XCJpZFwiXG4gICAgICBkZWZhdWx0LWV4cGFuZC1hbGxcbiAgICAgIDpleHBhbmQtb24tY2xpY2stbm9kZT1cImZhbHNlXCJcbiAgICA+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJ7IG5vZGUsIGRhdGEgfVwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiY3VzdG9tLXRyZWUtbm9kZVwiPlxuICAgICAgICAgIDxzcGFuPnt7IG5vZGUubGFiZWwgfX08L3NwYW4+XG4gICAgICAgICAgPGRpdj5cbiAgICAgICAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBsaW5rIEBjbGljaz1cImFwcGVuZChkYXRhKVwiPlxuICAgICAgICAgICAgICBBcHBlbmRcbiAgICAgICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgICAgICAgPGVsLWJ1dHRvblxuICAgICAgICAgICAgICBzdHlsZT1cIm1hcmdpbi1sZWZ0OiA0cHhcIlxuICAgICAgICAgICAgICB0eXBlPVwiZGFuZ2VyXCJcbiAgICAgICAgICAgICAgbGlua1xuICAgICAgICAgICAgICBAY2xpY2s9XCJyZW1vdmUobm9kZSwgZGF0YSlcIlxuICAgICAgICAgICAgPlxuICAgICAgICAgICAgICBEZWxldGVcbiAgICAgICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC10cmVlPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBFbEJ1dHRvbiB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW1wb3J0IHR5cGUge1xuICBSZW5kZXJDb250ZW50Q29udGV4dCxcbiAgUmVuZGVyQ29udGVudEZ1bmN0aW9uLFxuICBUcmVlSW5zdGFuY2UsXG59IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW50ZXJmYWNlIFRyZWUge1xuICBpZDogbnVtYmVyXG4gIGxhYmVsOiBzdHJpbmdcbiAgY2hpbGRyZW4/OiBUcmVlW11cbn1cbnR5cGUgTm9kZSA9IFJlbmRlckNvbnRlbnRDb250ZXh0Wydub2RlJ11cbnR5cGUgRGF0YSA9IFJlbmRlckNvbnRlbnRDb250ZXh0WydkYXRhJ11cblxubGV0IGlkID0gMTAwMFxuY29uc3QgdHJlZVJlZjEgPSByZWY8VHJlZUluc3RhbmNlPigpXG5jb25zdCB0cmVlUmVmMiA9IHJlZjxUcmVlSW5zdGFuY2U+KClcblxuY29uc3QgYXBwZW5kID0gKGRhdGE6IERhdGEpID0+IHtcbiAgY29uc3QgbmV3Q2hpbGQgPSB7IGlkOiBpZCsrLCBsYWJlbDogJ3Rlc3R0ZXN0JywgY2hpbGRyZW46IFtdIH1cbiAgdHJlZVJlZjEudmFsdWU/LmFwcGVuZChuZXdDaGlsZCwgZGF0YSlcbiAgdHJlZVJlZjIudmFsdWU/LmFwcGVuZChuZXdDaGlsZCwgZGF0YSlcbn1cblxuY29uc3QgcmVtb3ZlID0gKG5vZGU6IE5vZGUsIGRhdGE6IERhdGEpID0+IHtcbiAgdHJlZVJlZjEudmFsdWU/LnJlbW92ZShkYXRhKVxuICB0cmVlUmVmMi52YWx1ZT8ucmVtb3ZlKGRhdGEpXG59XG5cbmNvbnN0IHJlbmRlckNvbnRlbnQ6IFJlbmRlckNvbnRlbnRGdW5jdGlvbiA9IChoLCB7IG5vZGUsIGRhdGEgfSkgPT4ge1xuICByZXR1cm4gaChcbiAgICAnZGl2JyxcbiAgICB7XG4gICAgICBjbGFzczogJ2N1c3RvbS10cmVlLW5vZGUnLFxuICAgIH0sXG4gICAgW1xuICAgICAgaCgnc3BhbicsIG51bGwsIG5vZGUubGFiZWwpLFxuICAgICAgaCgnZGl2JywgbnVsbCwgW1xuICAgICAgICBoKFxuICAgICAgICAgIEVsQnV0dG9uLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHR5cGU6ICdwcmltYXJ5JyxcbiAgICAgICAgICAgIGxpbms6IHRydWUsXG4gICAgICAgICAgICBvbkNsaWNrOiAoKSA9PiBhcHBlbmQoZGF0YSksXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBkZWZhdWx0OiAoKSA9PiAnQXBwZW5kJyxcbiAgICAgICAgICB9XG4gICAgICAgICksXG4gICAgICAgIGgoXG4gICAgICAgICAgRWxCdXR0b24sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdHlwZTogJ2RhbmdlcicsXG4gICAgICAgICAgICBsaW5rOiB0cnVlLFxuICAgICAgICAgICAgc3R5bGU6ICdtYXJnaW4tbGVmdDogNHB4JyxcbiAgICAgICAgICAgIG9uQ2xpY2s6ICgpID0+IHJlbW92ZShub2RlLCBkYXRhKSxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGRlZmF1bHQ6ICgpID0+ICdEZWxldGUnLFxuICAgICAgICAgIH1cbiAgICAgICAgKSxcbiAgICAgIF0pLFxuICAgIF1cbiAgKVxufVxuXG5jb25zdCBkYXRhU291cmNlID0gcmVmPFRyZWVbXT4oW1xuICB7XG4gICAgaWQ6IDEsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgaWQ6IDQsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDEtMScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgaWQ6IDksXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDEtMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGlkOiAxMCxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMS0xLTInLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICBpZDogMixcbiAgICBsYWJlbDogJ0xldmVsIG9uZSAyJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICBpZDogNSxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0xJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiA2LFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAyLTInLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgaWQ6IDMsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMycsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgaWQ6IDcsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDMtMScsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogOCxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0yJyxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbl0pXG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLmN1c3RvbS10cmVlLW5vZGUge1xuICBmbGV4OiAxO1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47XG4gIGZvbnQtc2l6ZTogMTRweDtcbiAgcGFkZGluZy1yaWdodDogOHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/customized-node.vue)_

vue

```
<template>
  <div class="custom-tree-container">
    <p>Using render-content</p>
    <el-tree
      ref="treeRef1"
      style="max-width: 600px"
      :data="dataSource"
      show-checkbox
      node-key="id"
      default-expand-all
      :expand-on-click-node="false"
      :render-content="renderContent"
    />
    <p>Using scoped slot</p>
    <el-tree
      ref="treeRef2"
      style="max-width: 600px"
      :data="dataSource"
      show-checkbox
      node-key="id"
      default-expand-all
      :expand-on-click-node="false"
    >
      <template #default="{ node, data }">
        <div class="custom-tree-node">
          <span>{{ node.label }}</span>
          <div>
            <el-button type="primary" link @click="append(data)">
              Append
            </el-button>
            <el-button
              style="margin-left: 4px"
              type="danger"
              link
              @click="remove(node, data)"
            >
              Delete
            </el-button>
          </div>
        </div>
      </template>
    </el-tree>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElButton } from 'element-plus'

import type {
  RenderContentContext,
  RenderContentFunction,
  TreeInstance,
} from 'element-plus'

interface Tree {
  id: number
  label: string
  children?: Tree[]
}
type Node = RenderContentContext['node']
type Data = RenderContentContext['data']

let id = 1000
const treeRef1 = ref<TreeInstance>()
const treeRef2 = ref<TreeInstance>()

const append = (data: Data) => {
  const newChild = { id: id++, label: 'testtest', children: [] }
  treeRef1.value?.append(newChild, data)
  treeRef2.value?.append(newChild, data)
}

const remove = (node: Node, data: Data) => {
  treeRef1.value?.remove(data)
  treeRef2.value?.remove(data)
}

const renderContent: RenderContentFunction = (h, { node, data }) => {
  return h(
    'div',
    {
      class: 'custom-tree-node',
    },
    [
      h('span', null, node.label),
      h('div', null, [
        h(
          ElButton,
          {
            type: 'primary',
            link: true,
            onClick: () => append(data),
          },
          {
            default: () => 'Append',
          }
        ),
        h(
          ElButton,
          {
            type: 'danger',
            link: true,
            style: 'margin-left: 4px',
            onClick: () => remove(node, data),
          },
          {
            default: () => 'Delete',
          }
        ),
      ]),
    ]
  )
}

const dataSource = ref<Tree[]>([
  {
    id: 1,
    label: 'Level one 1',
    children: [
      {
        id: 4,
        label: 'Level two 1-1',
        children: [
          {
            id: 9,
            label: 'Level three 1-1-1',
          },
          {
            id: 10,
            label: 'Level three 1-1-2',
          },
        ],
      },
    ],
  },
  {
    id: 2,
    label: 'Level one 2',
    children: [
      {
        id: 5,
        label: 'Level two 2-1',
      },
      {
        id: 6,
        label: 'Level two 2-2',
      },
    ],
  },
  {
    id: 3,
    label: 'Level one 3',
    children: [
      {
        id: 7,
        label: 'Level two 3-1',
      },
      {
        id: 8,
        label: 'Level two 3-2',
      },
    ],
  },
])
</script>

<style>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>
```

隐藏源代码

## 自定义节点类名 [​](#自定义节点类名)

节点的类名支持自定义。

使用 `props.class` 来建立节点的类名。

Level one 1

Level two 1-1

Level three 1-1-1

Level three 1-1-2

Level one 2

Level two 2-1

Level two 2-2

Level one 3

Level two 3-1

Level two 3-2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY3VzdG9tLXRyZWUtbm9kZS1jb250YWluZXJcIj5cbiAgICA8ZWwtdHJlZVxuICAgICAgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCJcbiAgICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgICBzaG93LWNoZWNrYm94XG4gICAgICBub2RlLWtleT1cImlkXCJcbiAgICAgIGRlZmF1bHQtZXhwYW5kLWFsbFxuICAgICAgOmV4cGFuZC1vbi1jbGljay1ub2RlPVwiZmFsc2VcIlxuICAgICAgOnByb3BzPVwieyBjbGFzczogY3VzdG9tTm9kZUNsYXNzIH1cIlxuICAgIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB0eXBlIHsgVHJlZU5vZGVEYXRhIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbnRlcmZhY2UgVHJlZSB7XG4gIGlkOiBudW1iZXJcbiAgbGFiZWw6IHN0cmluZ1xuICBpc1BlbnVsdGltYXRlPzogYm9vbGVhblxuICBjaGlsZHJlbj86IFRyZWVbXVxufVxuXG5jb25zdCBjdXN0b21Ob2RlQ2xhc3MgPSAoeyBpc1BlbnVsdGltYXRlIH06IFRyZWVOb2RlRGF0YSkgPT5cbiAgaXNQZW51bHRpbWF0ZSA/ICdpcy1wZW51bHRpbWF0ZScgOiAnJ1xuXG5jb25zdCBkYXRhOiBUcmVlW10gPSBbXG4gIHtcbiAgICBpZDogMSxcbiAgICBsYWJlbDogJ0xldmVsIG9uZSAxJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICBpZDogNCxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMS0xJyxcbiAgICAgICAgaXNQZW51bHRpbWF0ZTogdHJ1ZSxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBpZDogOSxcbiAgICAgICAgICAgIGxhYmVsOiAnTGV2ZWwgdGhyZWUgMS0xLTEnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgaWQ6IDEwLFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAxLTEtMicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIGlkOiAyLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDInLFxuICAgIGlzUGVudWx0aW1hdGU6IHRydWUsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgaWQ6IDUsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDItMScsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogNixcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0yJyxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIGlkOiAzLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDMnLFxuICAgIGlzUGVudWx0aW1hdGU6IHRydWUsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgaWQ6IDcsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDMtMScsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogOCxcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0yJyxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuXG48c3R5bGU+XG4uaXMtcGVudWx0aW1hdGUgPiAuZWwtdHJlZS1ub2RlX19jb250ZW50IC5lbC10cmVlLW5vZGVfX2xhYmVsIHtcbiAgY29sb3I6ICM2MjZhZWY7XG59XG4uaXMtcGVudWx0aW1hdGUgPiAuZWwtdHJlZS1ub2RlX19jaGlsZHJlbiA+IGRpdiB7XG4gIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgbWFyZ2luLXJpZ2h0OiA0cHg7XG5cbiAgJjpub3QoOmZpcnN0LWNoaWxkKSAuZWwtdHJlZS1ub2RlX19jb250ZW50IHtcbiAgICBwYWRkaW5nLWxlZnQ6IDBweCAhaW1wb3J0YW50O1xuICB9XG4gIC5lbC10cmVlLW5vZGVfX2NvbnRlbnQge1xuICAgIHBhZGRpbmctcmlnaHQ6IDE2cHg7XG4gIH1cbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/custom-node-class.vue)_

vue

```
<template>
  <div class="custom-tree-node-container">
    <el-tree
      style="max-width: 600px"
      :data="data"
      show-checkbox
      node-key="id"
      default-expand-all
      :expand-on-click-node="false"
      :props="{ class: customNodeClass }"
    />
  </div>
</template>

<script lang="ts" setup>
import type { TreeNodeData } from 'element-plus'

interface Tree {
  id: number
  label: string
  isPenultimate?: boolean
  children?: Tree[]
}

const customNodeClass = ({ isPenultimate }: TreeNodeData) =>
  isPenultimate ? 'is-penultimate' : ''

const data: Tree[] = [
  {
    id: 1,
    label: 'Level one 1',
    children: [
      {
        id: 4,
        label: 'Level two 1-1',
        isPenultimate: true,
        children: [
          {
            id: 9,
            label: 'Level three 1-1-1',
          },
          {
            id: 10,
            label: 'Level three 1-1-2',
          },
        ],
      },
    ],
  },
  {
    id: 2,
    label: 'Level one 2',
    isPenultimate: true,
    children: [
      {
        id: 5,
        label: 'Level two 2-1',
      },
      {
        id: 6,
        label: 'Level two 2-2',
      },
    ],
  },
  {
    id: 3,
    label: 'Level one 3',
    isPenultimate: true,
    children: [
      {
        id: 7,
        label: 'Level two 3-1',
      },
      {
        id: 8,
        label: 'Level two 3-2',
      },
    ],
  },
]
</script>

<style>
.is-penultimate > .el-tree-node__content .el-tree-node__label {
  color: #626aef;
}
.is-penultimate > .el-tree-node__children > div {
  display: inline-block;
  margin-right: 4px;

  &:not(:first-child) .el-tree-node__content {
    padding-left: 0px !important;
  }
  .el-tree-node__content {
    padding-right: 16px;
  }
}
</style>
```

隐藏源代码

## 树节点过滤 [​](#树节点过滤)

树节点是可以被过滤的

调用 Tree 实例对象的 `filter` 方法来过滤树节点。 方法的参数就是过滤关键字。 需要注意的是，此时需要设置 `filter-node-method` 属性，其值为过滤函数。

Level one 1

Level two 1-1

Level three 1-1-1

Level three 1-1-2

Level one 2

Level two 2-1

Level two 2-2

Level one 3

Level two 3-1

Level two 3-2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwiZmlsdGVyVGV4dFwiXG4gICAgY2xhc3M9XCJ3LTYwIG1iLTJcIlxuICAgIHBsYWNlaG9sZGVyPVwiRmlsdGVyIGtleXdvcmRcIlxuICAvPlxuXG4gIDxlbC10cmVlXG4gICAgcmVmPVwidHJlZVJlZlwiXG4gICAgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCJcbiAgICBjbGFzcz1cImZpbHRlci10cmVlXCJcbiAgICA6ZGF0YT1cImRhdGFcIlxuICAgIDpwcm9wcz1cImRlZmF1bHRQcm9wc1wiXG4gICAgZGVmYXVsdC1leHBhbmQtYWxsXG4gICAgOmZpbHRlci1ub2RlLW1ldGhvZD1cImZpbHRlck5vZGVcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiwgd2F0Y2ggfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgRmlsdGVyTm9kZU1ldGhvZEZ1bmN0aW9uLCBUcmVlSW5zdGFuY2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmludGVyZmFjZSBUcmVlIHtcbiAgW2tleTogc3RyaW5nXTogYW55XG59XG5cbmNvbnN0IGZpbHRlclRleHQgPSByZWYoJycpXG5jb25zdCB0cmVlUmVmID0gcmVmPFRyZWVJbnN0YW5jZT4oKVxuXG5jb25zdCBkZWZhdWx0UHJvcHMgPSB7XG4gIGNoaWxkcmVuOiAnY2hpbGRyZW4nLFxuICBsYWJlbDogJ2xhYmVsJyxcbn1cblxud2F0Y2goZmlsdGVyVGV4dCwgKHZhbCkgPT4ge1xuICB0cmVlUmVmLnZhbHVlIS5maWx0ZXIodmFsKVxufSlcblxuY29uc3QgZmlsdGVyTm9kZTogRmlsdGVyTm9kZU1ldGhvZEZ1bmN0aW9uID0gKHZhbHVlOiBzdHJpbmcsIGRhdGE6IFRyZWUpID0+IHtcbiAgaWYgKCF2YWx1ZSkgcmV0dXJuIHRydWVcbiAgcmV0dXJuIGRhdGEubGFiZWwuaW5jbHVkZXModmFsdWUpXG59XG5cbmNvbnN0IGRhdGE6IFRyZWVbXSA9IFtcbiAge1xuICAgIGlkOiAxLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDEnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIGlkOiA0LFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAxLTEnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGlkOiA5LFxuICAgICAgICAgICAgbGFiZWw6ICdMZXZlbCB0aHJlZSAxLTEtMScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBpZDogMTAsXG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDEtMS0yJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgaWQ6IDIsXG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMicsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgaWQ6IDUsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDItMScsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogNixcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0yJyxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIGlkOiAzLFxuICAgIGxhYmVsOiAnTGV2ZWwgb25lIDMnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIGlkOiA3LFxuICAgICAgICBsYWJlbDogJ0xldmVsIHR3byAzLTEnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IDgsXG4gICAgICAgIGxhYmVsOiAnTGV2ZWwgdHdvIDMtMicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/filtering.vue)_

vue

```
<template>
  <el-input
    v-model="filterText"
    class="w-60 mb-2"
    placeholder="Filter keyword"
  />

  <el-tree
    ref="treeRef"
    style="max-width: 600px"
    class="filter-tree"
    :data="data"
    :props="defaultProps"
    default-expand-all
    :filter-node-method="filterNode"
  />
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

import type { FilterNodeMethodFunction, TreeInstance } from 'element-plus'

interface Tree {
  [key: string]: any
}

const filterText = ref('')
const treeRef = ref<TreeInstance>()

const defaultProps = {
  children: 'children',
  label: 'label',
}

watch(filterText, (val) => {
  treeRef.value!.filter(val)
})

const filterNode: FilterNodeMethodFunction = (value: string, data: Tree) => {
  if (!value) return true
  return data.label.includes(value)
}

const data: Tree[] = [
  {
    id: 1,
    label: 'Level one 1',
    children: [
      {
        id: 4,
        label: 'Level two 1-1',
        children: [
          {
            id: 9,
            label: 'Level three 1-1-1',
          },
          {
            id: 10,
            label: 'Level three 1-1-2',
          },
        ],
      },
    ],
  },
  {
    id: 2,
    label: 'Level one 2',
    children: [
      {
        id: 5,
        label: 'Level two 2-1',
      },
      {
        id: 6,
        label: 'Level two 2-2',
      },
    ],
  },
  {
    id: 3,
    label: 'Level one 3',
    children: [
      {
        id: 7,
        label: 'Level two 3-1',
      },
      {
        id: 8,
        label: 'Level two 3-2',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 手风琴模式 [​](#手风琴模式)

对于同一级的节点，每次只能展开一个

Level one 1

Level one 2

Level one 3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZVxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6cHJvcHM9XCJkZWZhdWx0UHJvcHNcIlxuICAgIGFjY29yZGlvblxuICAgIEBub2RlLWNsaWNrPVwiaGFuZGxlTm9kZUNsaWNrXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbnRlcmZhY2UgVHJlZSB7XG4gIGxhYmVsOiBzdHJpbmdcbiAgY2hpbGRyZW4/OiBUcmVlW11cbn1cblxuY29uc3QgaGFuZGxlTm9kZUNsaWNrID0gKGRhdGE6IFRyZWUpID0+IHtcbiAgY29uc29sZS5sb2coZGF0YSlcbn1cblxuY29uc3QgZGF0YTogVHJlZVtdID0gW1xuICB7XG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMS0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDEtMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMicsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDItMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDItMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMycsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuY29uc3QgZGVmYXVsdFByb3BzID0ge1xuICBjaGlsZHJlbjogJ2NoaWxkcmVuJyxcbiAgbGFiZWw6ICdsYWJlbCcsXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/accordion.vue)_

vue

```
<template>
  <el-tree
    style="max-width: 600px"
    :data="data"
    :props="defaultProps"
    accordion
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

隐藏源代码

## 可拖拽节点 [​](#可拖拽节点)

通过 `draggable` 属性可让节点变为可拖拽

Level one 1

Level two 1-1

Level three 1-1-1

Level one 2

Level two 2-1

Level three 2-1-1

Level two 2-2

Level three 2-2-1

Level one 3

Level two 3-1

Level three 3-1-1

Level two 3-2

Level three 3-2-1

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJlZVxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOmFsbG93LWRyb3A9XCJhbGxvd0Ryb3BcIlxuICAgIDphbGxvdy1kcmFnPVwiYWxsb3dEcmFnXCJcbiAgICA6ZGF0YT1cImRhdGFcIlxuICAgIGRyYWdnYWJsZVxuICAgIGRlZmF1bHQtZXhwYW5kLWFsbFxuICAgIG5vZGUta2V5PVwiaWRcIlxuICAgIEBub2RlLWRyYWctc3RhcnQ9XCJoYW5kbGVEcmFnU3RhcnRcIlxuICAgIEBub2RlLWRyYWctZW50ZXI9XCJoYW5kbGVEcmFnRW50ZXJcIlxuICAgIEBub2RlLWRyYWctbGVhdmU9XCJoYW5kbGVEcmFnTGVhdmVcIlxuICAgIEBub2RlLWRyYWctb3Zlcj1cImhhbmRsZURyYWdPdmVyXCJcbiAgICBAbm9kZS1kcmFnLWVuZD1cImhhbmRsZURyYWdFbmRcIlxuICAgIEBub2RlLWRyb3A9XCJoYW5kbGVEcm9wXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgdHlwZSB7XG4gIEFsbG93RHJvcFR5cGUsXG4gIE5vZGVEcm9wVHlwZSxcbiAgUmVuZGVyQ29udGVudENvbnRleHQsXG59IGZyb20gJ2VsZW1lbnQtcGx1cydcblxudHlwZSBOb2RlID0gUmVuZGVyQ29udGVudENvbnRleHRbJ25vZGUnXVxuXG5jb25zdCBoYW5kbGVEcmFnU3RhcnQgPSAobm9kZTogTm9kZSwgZXY6IERyYWdFdmVudCkgPT4ge1xuICBjb25zb2xlLmxvZygnZHJhZyBzdGFydCcsIG5vZGUpXG59XG5jb25zdCBoYW5kbGVEcmFnRW50ZXIgPSAoZHJhZ2dpbmdOb2RlOiBOb2RlLCBkcm9wTm9kZTogTm9kZSwgZXY6IERyYWdFdmVudCkgPT4ge1xuICBjb25zb2xlLmxvZygndHJlZSBkcmFnIGVudGVyOicsIGRyb3BOb2RlLmxhYmVsKVxufVxuY29uc3QgaGFuZGxlRHJhZ0xlYXZlID0gKGRyYWdnaW5nTm9kZTogTm9kZSwgZHJvcE5vZGU6IE5vZGUsIGV2OiBEcmFnRXZlbnQpID0+IHtcbiAgY29uc29sZS5sb2coJ3RyZWUgZHJhZyBsZWF2ZTonLCBkcm9wTm9kZS5sYWJlbClcbn1cbmNvbnN0IGhhbmRsZURyYWdPdmVyID0gKGRyYWdnaW5nTm9kZTogTm9kZSwgZHJvcE5vZGU6IE5vZGUsIGV2OiBEcmFnRXZlbnQpID0+IHtcbiAgY29uc29sZS5sb2coJ3RyZWUgZHJhZyBvdmVyOicsIGRyb3BOb2RlLmxhYmVsKVxufVxuY29uc3QgaGFuZGxlRHJhZ0VuZCA9IChcbiAgZHJhZ2dpbmdOb2RlOiBOb2RlLFxuICBkcm9wTm9kZTogTm9kZSB8IG51bGwsXG4gIGRyb3BUeXBlOiBOb2RlRHJvcFR5cGUsXG4gIGV2OiBEcmFnRXZlbnRcbikgPT4ge1xuICBjb25zb2xlLmxvZygndHJlZSBkcmFnIGVuZDonLCBkcm9wTm9kZSAmJiBkcm9wTm9kZS5sYWJlbCwgZHJvcFR5cGUpXG59XG5jb25zdCBoYW5kbGVEcm9wID0gKFxuICBkcmFnZ2luZ05vZGU6IE5vZGUsXG4gIGRyb3BOb2RlOiBOb2RlLFxuICBkcm9wVHlwZTogRXhjbHVkZTxOb2RlRHJvcFR5cGUsICdub25lJz4sXG4gIGV2OiBEcmFnRXZlbnRcbikgPT4ge1xuICBjb25zb2xlLmxvZygndHJlZSBkcm9wOicsIGRyb3BOb2RlLmxhYmVsLCBkcm9wVHlwZSlcbn1cbmNvbnN0IGFsbG93RHJvcCA9IChkcmFnZ2luZ05vZGU6IE5vZGUsIGRyb3BOb2RlOiBOb2RlLCB0eXBlOiBBbGxvd0Ryb3BUeXBlKSA9PiB7XG4gIGlmIChkcm9wTm9kZS5kYXRhLmxhYmVsID09PSAnTGV2ZWwgdHdvIDMtMScpIHtcbiAgICByZXR1cm4gdHlwZSAhPT0gJ2lubmVyJ1xuICB9IGVsc2Uge1xuICAgIHJldHVybiB0cnVlXG4gIH1cbn1cbmNvbnN0IGFsbG93RHJhZyA9IChkcmFnZ2luZ05vZGU6IE5vZGUpID0+IHtcbiAgcmV0dXJuICFkcmFnZ2luZ05vZGUuZGF0YS5sYWJlbC5pbmNsdWRlcygnTGV2ZWwgdGhyZWUgMy0xLTEnKVxufVxuXG5jb25zdCBkYXRhID0gW1xuICB7XG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMS0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDEtMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMicsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDItMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMi0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDItMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdMZXZlbCBvbmUgMycsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0xJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMS0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6ICdMZXZlbCB0d28gMy0yJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBsYWJlbDogJ0xldmVsIHRocmVlIDMtMi0xJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tree/draggable.vue)_

vue

```
<template>
  <el-tree
    style="max-width: 600px"
    :allow-drop="allowDrop"
    :allow-drag="allowDrag"
    :data="data"
    draggable
    default-expand-all
    node-key="id"
    @node-drag-start="handleDragStart"
    @node-drag-enter="handleDragEnter"
    @node-drag-leave="handleDragLeave"
    @node-drag-over="handleDragOver"
    @node-drag-end="handleDragEnd"
    @node-drop="handleDrop"
  />
</template>

<script lang="ts" setup>
import type {
  AllowDropType,
  NodeDropType,
  RenderContentContext,
} from 'element-plus'

type Node = RenderContentContext['node']

const handleDragStart = (node: Node, ev: DragEvent) => {
  console.log('drag start', node)
}
const handleDragEnter = (draggingNode: Node, dropNode: Node, ev: DragEvent) => {
  console.log('tree drag enter:', dropNode.label)
}
const handleDragLeave = (draggingNode: Node, dropNode: Node, ev: DragEvent) => {
  console.log('tree drag leave:', dropNode.label)
}
const handleDragOver = (draggingNode: Node, dropNode: Node, ev: DragEvent) => {
  console.log('tree drag over:', dropNode.label)
}
const handleDragEnd = (
  draggingNode: Node,
  dropNode: Node | null,
  dropType: NodeDropType,
  ev: DragEvent
) => {
  console.log('tree drag end:', dropNode && dropNode.label, dropType)
}
const handleDrop = (
  draggingNode: Node,
  dropNode: Node,
  dropType: Exclude<NodeDropType, 'none'>,
  ev: DragEvent
) => {
  console.log('tree drop:', dropNode.label, dropType)
}
const allowDrop = (draggingNode: Node, dropNode: Node, type: AllowDropType) => {
  if (dropNode.data.label === 'Level two 3-1') {
    return type !== 'inner'
  } else {
    return true
  }
}
const allowDrag = (draggingNode: Node) => {
  return !draggingNode.data.label.includes('Level three 3-1-1')
}

const data = [
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
</script>
```

隐藏源代码

## Tree API [​](#tree-api)

### 属性 [​](#属性)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| data | 展示数据 | `array` | — |
| empty-text | 内容为空的时候展示的文本 | `string` | — |
| node-key | 每个树节点用来作为唯一标识的属性，整棵树应该是唯一的 | `string` | — |
| [props](#props) | 配置选项，具体看下表 | `object` | — |
| render-after-expand | 是否在第一次展开某个树节点后才渲染其子节点 | `boolean` | true |
| load | 加载子树数据的方法，仅当 lazy 属性为true 时生效 | `Function` | — |
| render-content | 树节点的内容区的渲染 Function | `Function` | — |
| highlight-current | 是否高亮当前选中节点，默认值是 false。 | `boolean` | false |
| default-expand-all | 是否默认展开所有节点 | `boolean` | false |
| expand-on-click-node | 是否在点击节点的时候展开或者收缩节点， 默认值为 true，如果为 false，则只有点箭头图标的时候才会展开或者收缩节点。 | `boolean` | true |
| check-on-click-node | 是否在点击节点的时候选中节点，默认值为 false，即只有在点击复选框时才会选中节点。 | `boolean` | false |
| check-on-click-leaf 2.9.6 | 点击叶节点(最后一个子节点)时是否选中或取消选中节点。 | `boolean` | true |
| auto-expand-parent | 展开子节点的时候是否自动展开父节点 | `boolean` | true |
| default-expanded-keys | 默认展开的节点的 key 的数组 | `array` | — |
| show-checkbox | 节点是否可被选择 | `boolean` | false |
| check-strictly | 在显示复选框的情况下，是否严格的遵循父子不互相关联的做法，默认为 false | `boolean` | false |
| default-checked-keys | 默认勾选的节点的 key 的数组 | `array` | — |
| current-node-key | 当前选中的节点 | `string` / `number` | — |
| filter-node-method | 对树节点进行筛选时执行的方法， 返回 `false` 则表示这个节点会被隐藏 | `Function` | — |
| accordion | 是否每次只打开一个同级树节点展开 | `boolean` | false |
| indent | 相邻级节点间的水平缩进，单位为像素 | `number` | 18 |
| icon | 自定义树节点图标组件 | `string` / `Component` | — |
| lazy | 是否懒加载子节点，需与 load 方法结合使用 | `boolean` | false |
| draggable | 是否开启拖拽节点功能 | `boolean` | false |
| allow-drag | 判断节点能否被拖拽 如果返回 `false` ，节点不能被拖动 | `Function` | — |
| allow-drop | 拖拽时判定目标节点能否成为拖动目标位置。 如果返回 `false` ，拖动节点不能被拖放到目标节点。 `type` 参数有三种情况：'prev'、'inner' 和 'next'，分别表示放置在目标节点前、插入至目标节点和放置在目标节点后 | `Function` | — |

### Props [​](#props)

| Props | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| label | 指定节点标签为节点对象的某个属性值 | `string` / `Function` | — |
| children | 指定子树为节点对象的某个属性值 | `string` | — |
| disabled | 指定节点选择框是否禁用为节点对象的某个属性值 | `string` / `Function` | — |
| isLeaf | 指定节点是否为叶子节点，仅在指定了 lazy 属性的情况下生效 | `string` / `Function` | — |
| class | 自定义节点类名 | `string` / `Function` | — |

### 对外暴露的方法 [​](#对外暴露的方法)

`Tree` 组件有以下方法，均返回当前选中的节点数组

| 方法 | 说明 | 回调参数 |
| --- | --- | --- |
| filter | 过滤所有树节点，过滤后的节点将被隐藏 | 接收一个参数并指定为 filter-node-method 属性的第一个参数 |
| updateKeyChildren | 为节点设置新数据，只有当设置 `node-key` 属性的时候才可用 | (key, data) 接收两个参数: 1. 节点的 key 2. 新数据 |
| getCheckedNodes | 如果节点可以被选中，(`show-checkbox` 为 `true`), 本方法将返回当前选中节点的数组 | (leafOnly, includeHalfChecked) 接收两个布尔类型参数: 1. 默认值为 `false`. 若参数为 `true`, 它将返回当前选中节点的子节点 2. 默认值为 `false`. 如果参数为 `true`, 返回值包含半选中节点数据 |
| setCheckedNodes | 设置目前选中的节点，使用此方法必须设置 `node-key` 属性 | (nodes, leafOnly) 接收两个参数: 1. 要选中的节点对象构成的数组 2. 布尔类型的值 如果设置为 `true`，将只设置选中的叶子节点状态。 默认值是 `false`. |
| getCheckedKeys | 若节点可用被选中 (`show-checkbox` 为 `true`), 它将返回当前选中节点 key 的数组 | (leafOnly) 接收一个布尔类型参数，默认为 `false`. 若参数为 `true`, 它将返回当前选中节点的子节点 |
| setCheckedKeys | 设置目前选中的节点，使用此方法必须设置 `node-key` 属性 | (keys, leafOnly) 接收两个参数: 1. 一个需要被选中的多节点 key 的数组 2. 布尔类型的值 如果设置为 `true`，将只设置选中的叶子节点状态。 默认值是 `false`. |
| setChecked | 设置节点是否被选中, 使用此方法必须设置 `node-key` 属性 | (key/data, checked, deep) 接收三个参数: 1. 要选中的节点的 key 或者数据 2. 一个布尔类型参数表明是否选中. 3. 一个布尔类型参数，用于指示是否递归选中/取消选中子节点（自 2.14.0 起，无论 `check-strictly` 设置如何，该行为均有效）。 |
| getHalfCheckedNodes | 如果节点可用被选中 (`show-checkbox` 为 `true`), 它将返回当前半选中的节点组成的数组 | — |
| getHalfCheckedKeys | 若节点可被选中(`show-checkbox` 为 `true`)，则返回目前半选中的节点的 key 所组成的数组 | — |
| getCurrentKey | 返回当前被选中节点的数据 (如果没有则返回 null) | — |
| getCurrentNode | 返回当前被选中节点的数据 (如果没有则返回 null) | — |
| setCurrentKey | 通过 key 设置某个节点的当前选中状态，使用此方法必须设置 `node-key` 属性 | (key, shouldAutoExpandParent=true) 1. 待被选节点的 key， 如果为 `null`, 取消当前选中的节点 2. 是否展开父节点 |
| setCurrentNode | 设置节点为选中状态，使用此方法必须设置 `node-key` 属性 | (node, shouldAutoExpandParent=true) 1. 待被选中的节点 2. 是否展开父节点 |
| getNode | 根据 data 或者 key 拿到 Tree 组件中的 node | (data) 节点的 data 或 key |
| remove | 删除 Tree 中的一个节点，使用此方法必须设置 node-key 属性 | (data) 要删除的节点的 data 或者 node 对象 |
| append | 为 Tree 中的一个节点追加一个子节点 | (data, parentNode) 1. 要追加的子节点的 data 2. 父节点的 data, key 或 node |
| insertBefore | 在 Tree 中给定节点前插入一个节点 | (data, refNode) 1. 要增加的节点的 data 2. 参考节点的 data, key 或 node |
| insertAfter | 在 Tree 中给定节点后插入一个节点 | (data, refNode) 1. 要增加的节点的 data 2. 参考节点的 data, key 或 node |

### 事件 [​](#事件)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| node-click | 当节点被点击的时候触发 | 四个参数：对应于节点点击的节点对象，TreeNode 的 `node` 属性, TreeNode和事件对象 |
| node-contextmenu | 当某一节点被鼠标右键点击时会触发该事件 | 共四个参数，依次为：event、传递给 `data` 属性的数组中该节点所对应的对象、节点对应的 Node、节点组件本身。 |
| check-change | 当复选框被点击的时候触发 | 共三个参数，依次为：传递给 data 属性的数组中该节点所对应的对象、节点本身是否被选中、节点的子树中是否有被选中的节点 |
| check | 点击节点复选框之后触发 | 共两个参数，依次为：传递给 data 属性的数组中该节点所对应的对象、树目前的选中状态对象，包含 checkedNodes、checkedKeys、halfCheckedNodes、halfCheckedKeys 四个属性 |
| current-change | 当前选中节点变化时触发的事件 | 共两个参数，依次为：当前节点的数据，当前节点的 Node 对象 |
| node-expand | 节点被展开时触发的事件 | 共三个参数，依次为：传递给 `data` 属性的数组中该节点所对应的对象、节点对应的 Node、节点组件本身 |
| node-collapse | 节点被关闭时触发的事件 | 共三个参数，依次为：传递给 `data` 属性的数组中该节点所对应的对象、节点对应的 Node、节点组件本身 |
| node-drag-start | 节点开始拖拽时触发的事件 | 共两个参数，依次为：被拖拽节点对应的 Node、event |
| node-drag-enter | 拖拽进入其他节点时触发的事件 | 共三个参数，依次为：被拖拽节点对应的 Node、所进入节点对应的 Node、event |
| node-drag-leave | 拖拽离开某个节点时触发的事件 | 共三个参数，依次为：被拖拽节点对应的 Node、所离开节点对应的 Node、event |
| node-drag-over | 在拖拽节点时触发的事件（类似浏览器的 mouseover 事件） | 共三个参数，依次为：被拖拽节点对应的 Node、当前进入节点对应的 Node、event |
| node-drag-end | 拖拽结束时（可能未成功）触发的事件 | 共四个参数，依次为：被拖拽节点对应的 Node、结束拖拽时最后进入的节点（可能为空）、被拖拽节点的放置位置（before、after、inner）、event |
| node-drop | 拖拽成功完成时触发的事件 | 共四个参数，依次为：被拖拽节点对应的 Node、结束拖拽时最后进入的节点、被拖拽节点的放置位置（before、after、inner）、event |

### 插槽 [​](#插槽)

| 插槽名 | 描述 | Type |
| --- | --- | --- |
| default | 自定义树节点的内容。 | `object` |
| empty 2.3.4 | 当数据为空时自定义的内容 | — |

## 类型声明 [​](#类型声明)

Show declarations

ts

```
interface RootTreeType {
  root: Ref<Node>
  // ...
}

// UnwrapRef<RootTreeType['root']> => Node
type Node = {
  canFocus: boolean
  checked: boolean
  childNodes: Node[]
  data: TreeNodeData
  expanded: boolean
  id: number
  indeterminate: boolean
  isCurrent: boolean
  isEffectivelyChecked: boolean
  isLeaf?: boolean
  isLeafByUser?: boolean
  level: number
  loaded: boolean
  loading: boolean
  parent: Node | null
  store: TreeStore
  text: string | null
  visible: boolean
}

// TreeNodeData => Tree / TreeOptionProps
// Tree type is your prop type.
// TreeOptionProps is default prop type
interface TreeOptionProps {
  children?: string
  label?: string | ((data: TreeNodeData, node: Node) => string)
  disabled?: string | ((data: TreeNodeData, node: Node) => boolean)
  isLeaf?: string | ((data: TreeNodeData, node: Node) => boolean)
  class?: (
    data: TreeNodeData,
    node: Node
  ) => string | { [key: string]: boolean }
}
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/tree) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/tree.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/tree.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/27413795?v=4&size=64)](https://github.com/SpanManX)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/59350883?v=4&size=64)](https://github.com/init-qy)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/36940267?v=4&size=64)](https://github.com/gaoxuan-haxibiao)[![](https://avatars.githubusercontent.com/u/75007029?v=4&size=64)](https://github.com/yj-liuzepeng)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/32807958?v=4&size=64)](https://github.com/zhiyuanzmj)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/283908624?v=4&size=64)](https://github.com/ruguoba)[![](https://avatars.githubusercontent.com/u/53589602?v=4&size=64)](https://github.com/l246804)[![](https://avatars.githubusercontent.com/u/15535177?v=4&size=64)](https://github.com/liuzi6612)[![](https://avatars.githubusercontent.com/u/24290011?v=4&size=64)](https://github.com/xingyixiang)[![](https://avatars.githubusercontent.com/u/14892120?v=4&size=64)](https://github.com/scvzerng)[![](https://avatars.githubusercontent.com/u/16952163?v=4&size=64)](https://github.com/ben-lau)[![](https://avatars.githubusercontent.com/u/110156942?v=4&size=64)](https://github.com/a92126)[![](https://avatars.githubusercontent.com/u/78132554?v=4&size=64)](https://github.com/momei-LJM)[![](https://avatars.githubusercontent.com/u/57086651?v=4&size=64)](https://github.com/Simon-He95)[![](https://avatars.githubusercontent.com/u/34467508?v=4&size=64)](https://github.com/kaedeair)[![](https://avatars.githubusercontent.com/u/22884361?v=4&size=64)](https://github.com/Alixhan)[![](https://avatars.githubusercontent.com/u/65433954?v=4&size=64)](https://github.com/inside5545)[![](https://avatars.githubusercontent.com/u/41944818?v=4&size=64)](https://github.com/CherishTheYouth)[![](https://avatars.githubusercontent.com/u/54665054?v=4&size=64)](https://github.com/lyric-zemin)[![](https://avatars.githubusercontent.com/u/105651386?v=4&size=64)](https://github.com/heappynd)[![](https://avatars.githubusercontent.com/u/26755049?v=4&size=64)](https://github.com/qq282126990)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/54560462?v=4&size=64)](https://github.com/matto49)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/49394793?v=4&size=64)](https://github.com/bxh1071)[![](https://avatars.githubusercontent.com/u/15629755?v=4&size=64)](https://github.com/Nullaha)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/23442840?v=4&size=64)](https://github.com/liunnn1994)[![](https://avatars.githubusercontent.com/u/1687298?v=4&size=64)](https://github.com/greper)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/52314078?v=4&size=64)](https://github.com/vaebe)[![](https://avatars.githubusercontent.com/u/38553985?v=4&size=64)](https://github.com/lequangdongg)[![](https://avatars.githubusercontent.com/u/38248854?v=4&size=64)](https://github.com/Yueyanc)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/48074435?v=4&size=64)](https://github.com/ElsaOOo)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)[![](https://avatars.githubusercontent.com/u/22695767?v=4&size=64)](https://github.com/deepthan)

[Tour 漫游式引导](https://element-plus.org/zh-CN/component/tour)

[Virtualized Tree 虚拟化树形控件](https://element-plus.org/zh-CN/component/tree-v2)


