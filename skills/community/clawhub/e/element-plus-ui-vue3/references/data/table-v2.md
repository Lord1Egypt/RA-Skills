---
name: "table-v2"
description: "Virtualized Table 虚拟化表格 -- Element Plus Vue3 桌面端组件。Invoke when user needs Virtualized Table 虚拟化表格 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/table-v2.html"
---

---

# Virtualized Table 虚拟化表格 beta [​](#virtualized-table-虚拟化表格)

更新日志待解决

48

在前端开发领域，表格一直都是一个高频出现的组件，尤其是在中后台和数据分析场景。 但是，对于 [Table V1](https://element-plus.org/zh-CN/component/table)来说，当一屏里超过 1000 条数据记录时，就会出现卡顿等性能问题，体验不是很好。

通过虚拟化表格组件，超大数据渲染将不再是一个头疼的问题。

TIP

该组件**仍在测试中**，生产环境使用可能有风险。 若您发现了 bug 或问题，请于 [GitHub](https://github.com/element-plus/element-plus/issues) 报告给我们以便修复。 同时，有一些 API 并未在此文档中提及，因为部分还没有开发完全，因此我们不在此提及。

**即使**虚拟化的表格是高效的，但是当数据负载过大时，**网络**和**内存容量**也会成为您应用程序的瓶颈。 因此请牢记，虚拟化表格永远不是最完美的解决方案，请考虑数据分页、过滤器等优化方案。

## 基础用法 [​](#基础用法)

让我们演示虚拟化表的性能，用10列和1 000行渲染一个基本示例。

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOndpZHRoPVwiNzAwXCJcbiAgICA6aGVpZ2h0PVwiNDAwXCJcbiAgICBmaXhlZFxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IGdlbmVyYXRlQ29sdW1ucyA9IChsZW5ndGggPSAxMCwgcHJlZml4ID0gJ2NvbHVtbi0nLCBwcm9wcz86IGFueSkgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIGNvbHVtbkluZGV4KSA9PiAoe1xuICAgIC4uLnByb3BzLFxuICAgIGtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICBkYXRhS2V5OiBgJHtwcmVmaXh9JHtjb2x1bW5JbmRleH1gLFxuICAgIHRpdGxlOiBgQ29sdW1uICR7Y29sdW1uSW5kZXh9YCxcbiAgICB3aWR0aDogMTUwLFxuICB9KSlcblxuY29uc3QgZ2VuZXJhdGVEYXRhID0gKFxuICBjb2x1bW5zOiBSZXR1cm5UeXBlPHR5cGVvZiBnZW5lcmF0ZUNvbHVtbnM+LFxuICBsZW5ndGggPSAyMDAsXG4gIHByZWZpeCA9ICdyb3ctJ1xuKSA9PlxuICBBcnJheS5mcm9tKHsgbGVuZ3RoIH0pLm1hcCgoXywgcm93SW5kZXgpID0+IHtcbiAgICByZXR1cm4gY29sdW1ucy5yZWR1Y2UoXG4gICAgICAocm93RGF0YSwgY29sdW1uLCBjb2x1bW5JbmRleCkgPT4ge1xuICAgICAgICByb3dEYXRhW2NvbHVtbi5kYXRhS2V5XSA9IGBSb3cgJHtyb3dJbmRleH0gLSBDb2wgJHtjb2x1bW5JbmRleH1gXG4gICAgICAgIHJldHVybiByb3dEYXRhXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogYCR7cHJlZml4fSR7cm93SW5kZXh9YCxcbiAgICAgICAgcGFyZW50SWQ6IG51bGwsXG4gICAgICB9XG4gICAgKVxuICB9KVxuXG5jb25zdCBjb2x1bW5zID0gZ2VuZXJhdGVDb2x1bW5zKDEwKVxuY29uc3QgZGF0YSA9IGdlbmVyYXRlRGF0YShjb2x1bW5zLCAxMDAwKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/basic.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :width="700"
    :height="400"
    fixed
  />
</template>

<script lang="ts" setup>
const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = generateData(columns, 1000)
</script>
```

隐藏源代码

## 自动调整大小 [​](#自动调整大小)

如果不想手动向表格传递 `width` 和 `height` 属性，可以使用 AutoResizer 对表格组件进行封装。 这会自动为你更新宽度和高度。

尝试调整您的浏览器大小来看看它是如何工作的。

TIP

由于 `AutoResizer` 组件的默认高度是 100%，所以请确保该组件的父元素**拥有固定的高度值**。 或者，您可以通过将 `style` 属性传递到 `AutoResizer` 来定义它。

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwiaGVpZ2h0OiA0MDBweFwiPlxuICAgIDxlbC1hdXRvLXJlc2l6ZXI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJ7IGhlaWdodCwgd2lkdGggfVwiPlxuICAgICAgICA8ZWwtdGFibGUtdjJcbiAgICAgICAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgICAgICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgICAgICAgOndpZHRoPVwid2lkdGhcIlxuICAgICAgICAgIDpoZWlnaHQ9XCJoZWlnaHRcIlxuICAgICAgICAgIGZpeGVkXG4gICAgICAgIC8+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtYXV0by1yZXNpemVyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5jb25zdCBnZW5lcmF0ZUNvbHVtbnMgPSAobGVuZ3RoID0gMTAsIHByZWZpeCA9ICdjb2x1bW4tJywgcHJvcHM/OiBhbnkpID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCBjb2x1bW5JbmRleCkgPT4gKHtcbiAgICAuLi5wcm9wcyxcbiAgICBrZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgZGF0YUtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICB0aXRsZTogYENvbHVtbiAke2NvbHVtbkluZGV4fWAsXG4gICAgd2lkdGg6IDE1MCxcbiAgfSkpXG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9IChcbiAgY29sdW1uczogUmV0dXJuVHlwZTx0eXBlb2YgZ2VuZXJhdGVDb2x1bW5zPixcbiAgbGVuZ3RoID0gMjAwLFxuICBwcmVmaXggPSAncm93LSdcbikgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIHJvd0luZGV4KSA9PiB7XG4gICAgcmV0dXJuIGNvbHVtbnMucmVkdWNlKFxuICAgICAgKHJvd0RhdGEsIGNvbHVtbiwgY29sdW1uSW5kZXgpID0+IHtcbiAgICAgICAgcm93RGF0YVtjb2x1bW4uZGF0YUtleV0gPSBgUm93ICR7cm93SW5kZXh9IC0gQ29sICR7Y29sdW1uSW5kZXh9YFxuICAgICAgICByZXR1cm4gcm93RGF0YVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IGAke3ByZWZpeH0ke3Jvd0luZGV4fWAsXG4gICAgICAgIHBhcmVudElkOiBudWxsLFxuICAgICAgfVxuICAgIClcbiAgfSlcblxuY29uc3QgY29sdW1ucyA9IGdlbmVyYXRlQ29sdW1ucygxMClcbmNvbnN0IGRhdGEgPSBnZW5lcmF0ZURhdGEoY29sdW1ucywgMjAwKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/auto-resizer.vue)_

vue

```
<template>
  <div style="height: 400px">
    <el-auto-resizer>
      <template #default="{ height, width }">
        <el-table-v2
          :columns="columns"
          :data="data"
          :width="width"
          :height="height"
          fixed
        />
      </template>
    </el-auto-resizer>
  </div>
</template>

<script lang="ts" setup>
const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = generateData(columns, 200)
</script>
```

隐藏源代码

## 自定义单元格渲染器 [​](#customize-cell-renderer)

当然，您可以根据您的需要呈现表格单元格。 这是如何自定义您的单元格的简单例子。

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Name

Operations

2020/10/01

2020/10/01

2020/10/01

2020/10/01

2020/10/01

2020/10/01

2020/10/01

2020/10/01

2020/10/01

Date

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOndpZHRoPVwiNzAwXCJcbiAgICA6aGVpZ2h0PVwiNDAwXCJcbiAgICBmaXhlZFxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHN4XCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgZGF5anMgZnJvbSAnZGF5anMnXG5pbXBvcnQge1xuICBFbEJ1dHRvbixcbiAgRWxJY29uLFxuICBFbFRhZyxcbiAgRWxUb29sdGlwLFxuICBUYWJsZVYyRml4ZWREaXIsXG59IGZyb20gJ2VsZW1lbnQtcGx1cydcbmltcG9ydCB7IFRpbWVyIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmltcG9ydCB0eXBlIHsgQ29sdW1uIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5sZXQgaWQgPSAwXG5cbmNvbnN0IGRhdGFHZW5lcmF0b3IgPSAoKSA9PiAoe1xuICBpZDogYHJhbmRvbS1pZC0keysraWR9YCxcbiAgbmFtZTogJ1RvbScsXG4gIGRhdGU6ICcyMDIwLTEwLTEnLFxufSlcblxuY29uc3QgY29sdW1uczogQ29sdW1uPGFueT5bXSA9IFtcbiAge1xuICAgIGtleTogJ2RhdGUnLFxuICAgIHRpdGxlOiAnRGF0ZScsXG4gICAgZGF0YUtleTogJ2RhdGUnLFxuICAgIHdpZHRoOiAxNTAsXG4gICAgZml4ZWQ6IFRhYmxlVjJGaXhlZERpci5MRUZULFxuICAgIGNlbGxSZW5kZXJlcjogKHsgY2VsbERhdGE6IGRhdGUgfSkgPT4gKFxuICAgICAgPEVsVG9vbHRpcCBjb250ZW50PXtkYXlqcyhkYXRlKS5mb3JtYXQoJ1lZWVkvTU0vREQnKX0+XG4gICAgICAgIHtcbiAgICAgICAgICA8c3BhbiBjbGFzcz1cImZsZXggaXRlbXMtY2VudGVyXCI+XG4gICAgICAgICAgICA8RWxJY29uIGNsYXNzPVwibXItM1wiPlxuICAgICAgICAgICAgICA8VGltZXIgLz5cbiAgICAgICAgICAgIDwvRWxJY29uPlxuICAgICAgICAgICAge2RheWpzKGRhdGUpLmZvcm1hdCgnWVlZWS9NTS9ERCcpfVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgfVxuICAgICAgPC9FbFRvb2x0aXA+XG4gICAgKSxcbiAgfSxcbiAge1xuICAgIGtleTogJ25hbWUnLFxuICAgIHRpdGxlOiAnTmFtZScsXG4gICAgZGF0YUtleTogJ25hbWUnLFxuICAgIHdpZHRoOiAxNTAsXG4gICAgYWxpZ246ICdjZW50ZXInLFxuICAgIGNlbGxSZW5kZXJlcjogKHsgY2VsbERhdGE6IG5hbWUgfSkgPT4gPEVsVGFnPntuYW1lfTwvRWxUYWc+LFxuICB9LFxuICB7XG4gICAga2V5OiAnb3BlcmF0aW9ucycsXG4gICAgdGl0bGU6ICdPcGVyYXRpb25zJyxcbiAgICBjZWxsUmVuZGVyZXI6ICgpID0+IChcbiAgICAgIDw+XG4gICAgICAgIDxFbEJ1dHRvbiBzaXplPVwic21hbGxcIj5FZGl0PC9FbEJ1dHRvbj5cbiAgICAgICAgPEVsQnV0dG9uIHNpemU9XCJzbWFsbFwiIHR5cGU9XCJkYW5nZXJcIj5cbiAgICAgICAgICBEZWxldGVcbiAgICAgICAgPC9FbEJ1dHRvbj5cbiAgICAgIDwvPlxuICAgICksXG4gICAgd2lkdGg6IDE1MCxcbiAgICBhbGlnbjogJ2NlbnRlcicsXG4gIH0sXG5dXG5cbmNvbnN0IGRhdGEgPSByZWYoQXJyYXkuZnJvbSh7IGxlbmd0aDogMjAwIH0pLm1hcChkYXRhR2VuZXJhdG9yKSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/cell-templating.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :width="700"
    :height="400"
    fixed
  />
</template>

<script lang="tsx" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'
import {
  ElButton,
  ElIcon,
  ElTag,
  ElTooltip,
  TableV2FixedDir,
} from 'element-plus'
import { Timer } from '@element-plus/icons-vue'

import type { Column } from 'element-plus'

let id = 0

const dataGenerator = () => ({
  id: `random-id-${++id}`,
  name: 'Tom',
  date: '2020-10-1',
})

const columns: Column<any>[] = [
  {
    key: 'date',
    title: 'Date',
    dataKey: 'date',
    width: 150,
    fixed: TableV2FixedDir.LEFT,
    cellRenderer: ({ cellData: date }) => (
      <ElTooltip content={dayjs(date).format('YYYY/MM/DD')}>
        {
          <span class="flex items-center">
            <ElIcon class="mr-3">
              <Timer />
            </ElIcon>
            {dayjs(date).format('YYYY/MM/DD')}
          </span>
        }
      </ElTooltip>
    ),
  },
  {
    key: 'name',
    title: 'Name',
    dataKey: 'name',
    width: 150,
    align: 'center',
    cellRenderer: ({ cellData: name }) => <ElTag>{name}</ElTag>,
  },
  {
    key: 'operations',
    title: 'Operations',
    cellRenderer: () => (
      <>
        <ElButton size="small">Edit</ElButton>
        <ElButton size="small" type="danger">
          Delete
        </ElButton>
      </>
    ),
    width: 150,
    align: 'center',
  },
]

const data = ref(Array.from({ length: 200 }).map(dataGenerator))
</script>
```

隐藏源代码

## 带有选择的表格 [​](#带有选择的表格)

使用自定义的单元格渲染来给表格组件添加选择的能力。

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 0 - Col 10

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 1 - Col 10

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 2 - Col 10

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 3 - Col 10

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 4 - Col 10

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 5 - Col 10

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 6 - Col 10

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 7 - Col 10

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Row 8 - Col 10

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwiaGVpZ2h0OiA0MDBweFwiPlxuICAgIDxlbC1hdXRvLXJlc2l6ZXI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJ7IGhlaWdodCwgd2lkdGggfVwiPlxuICAgICAgICA8ZWwtdGFibGUtdjJcbiAgICAgICAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgICAgICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgICAgICAgOndpZHRoPVwid2lkdGhcIlxuICAgICAgICAgIDpoZWlnaHQ9XCJoZWlnaHRcIlxuICAgICAgICAgIGZpeGVkXG4gICAgICAgIC8+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtYXV0by1yZXNpemVyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzeFwiIHNldHVwPlxuaW1wb3J0IHsgcmVmLCB1bnJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsQ2hlY2tib3gsIHVzZUxvY2FsZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW1wb3J0IHR5cGUgeyBGdW5jdGlvbmFsQ29tcG9uZW50IH0gZnJvbSAndnVlJ1xuaW1wb3J0IHR5cGUgeyBDaGVja2JveFZhbHVlVHlwZSwgQ29sdW1uIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG50eXBlIFNlbGVjdGlvbkNlbGxQcm9wcyA9IHtcbiAgdmFsdWU6IGJvb2xlYW5cbiAgaW50ZXJtZWRpYXRlPzogYm9vbGVhblxuICBhcmlhTGFiZWw/OiBzdHJpbmdcbiAgb25DaGFuZ2U6ICh2YWx1ZTogQ2hlY2tib3hWYWx1ZVR5cGUpID0+IHZvaWRcbn1cblxuY29uc3QgeyB0IH0gPSB1c2VMb2NhbGUoKVxuXG5jb25zdCBTZWxlY3Rpb25DZWxsOiBGdW5jdGlvbmFsQ29tcG9uZW50PFNlbGVjdGlvbkNlbGxQcm9wcz4gPSAoe1xuICB2YWx1ZSxcbiAgaW50ZXJtZWRpYXRlID0gZmFsc2UsXG4gIGFyaWFMYWJlbCxcbiAgb25DaGFuZ2UsXG59KSA9PiB7XG4gIHJldHVybiAoXG4gICAgPEVsQ2hlY2tib3hcbiAgICAgIG9uQ2hhbmdlPXtvbkNoYW5nZX1cbiAgICAgIG1vZGVsVmFsdWU9e3ZhbHVlfVxuICAgICAgYXJpYUxhYmVsPXthcmlhTGFiZWx9XG4gICAgICBpbmRldGVybWluYXRlPXtpbnRlcm1lZGlhdGV9XG4gICAgLz5cbiAgKVxufVxuXG5jb25zdCBnZW5lcmF0ZUNvbHVtbnMgPSAobGVuZ3RoID0gMTAsIHByZWZpeCA9ICdjb2x1bW4tJywgcHJvcHM/OiBhbnkpID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCBjb2x1bW5JbmRleCkgPT4gKHtcbiAgICAuLi5wcm9wcyxcbiAgICBrZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgZGF0YUtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICB0aXRsZTogYENvbHVtbiAke2NvbHVtbkluZGV4fWAsXG4gICAgd2lkdGg6IDE1MCxcbiAgfSkpXG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9IChcbiAgY29sdW1uczogUmV0dXJuVHlwZTx0eXBlb2YgZ2VuZXJhdGVDb2x1bW5zPixcbiAgbGVuZ3RoID0gMjAwLFxuICBwcmVmaXggPSAncm93LSdcbikgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIHJvd0luZGV4KSA9PiB7XG4gICAgcmV0dXJuIGNvbHVtbnMucmVkdWNlKFxuICAgICAgKHJvd0RhdGEsIGNvbHVtbiwgY29sdW1uSW5kZXgpID0+IHtcbiAgICAgICAgcm93RGF0YVtjb2x1bW4uZGF0YUtleV0gPSBgUm93ICR7cm93SW5kZXh9IC0gQ29sICR7Y29sdW1uSW5kZXh9YFxuICAgICAgICByZXR1cm4gcm93RGF0YVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IGAke3ByZWZpeH0ke3Jvd0luZGV4fWAsXG4gICAgICAgIGNoZWNrZWQ6IGZhbHNlLFxuICAgICAgICBwYXJlbnRJZDogbnVsbCxcbiAgICAgIH1cbiAgICApXG4gIH0pXG5cbmNvbnN0IGNvbHVtbnM6IENvbHVtbjxhbnk+W10gPSBnZW5lcmF0ZUNvbHVtbnMoMTApXG5jb2x1bW5zLnVuc2hpZnQoe1xuICBrZXk6ICdzZWxlY3Rpb24nLFxuICB3aWR0aDogNTAsXG4gIGNlbGxSZW5kZXJlcjogKHsgcm93RGF0YSB9KSA9PiB7XG4gICAgY29uc3Qgb25DaGFuZ2UgPSAodmFsdWU6IENoZWNrYm94VmFsdWVUeXBlKSA9PiAocm93RGF0YS5jaGVja2VkID0gdmFsdWUpXG4gICAgcmV0dXJuIChcbiAgICAgIDxTZWxlY3Rpb25DZWxsXG4gICAgICAgIHZhbHVlPXtyb3dEYXRhLmNoZWNrZWR9XG4gICAgICAgIGFyaWFMYWJlbD17dCgnZWwudGFibGUuc2VsZWN0Um93TGFiZWwnKX1cbiAgICAgICAgb25DaGFuZ2U9e29uQ2hhbmdlfVxuICAgICAgLz5cbiAgICApXG4gIH0sXG5cbiAgaGVhZGVyQ2VsbFJlbmRlcmVyOiAoKSA9PiB7XG4gICAgY29uc3QgX2RhdGEgPSB1bnJlZihkYXRhKVxuICAgIGNvbnN0IG9uQ2hhbmdlID0gKHZhbHVlOiBDaGVja2JveFZhbHVlVHlwZSkgPT5cbiAgICAgIChkYXRhLnZhbHVlID0gX2RhdGEubWFwKChyb3cpID0+IHtcbiAgICAgICAgcm93LmNoZWNrZWQgPSB2YWx1ZVxuICAgICAgICByZXR1cm4gcm93XG4gICAgICB9KSlcbiAgICBjb25zdCBhbGxTZWxlY3RlZCA9IF9kYXRhLmV2ZXJ5KChyb3cpID0+IHJvdy5jaGVja2VkKVxuICAgIGNvbnN0IGNvbnRhaW5zQ2hlY2tlZCA9IF9kYXRhLnNvbWUoKHJvdykgPT4gcm93LmNoZWNrZWQpXG5cbiAgICByZXR1cm4gKFxuICAgICAgPFNlbGVjdGlvbkNlbGxcbiAgICAgICAgdmFsdWU9e2FsbFNlbGVjdGVkfVxuICAgICAgICBpbnRlcm1lZGlhdGU9e2NvbnRhaW5zQ2hlY2tlZCAmJiAhYWxsU2VsZWN0ZWR9XG4gICAgICAgIGFyaWFMYWJlbD17dCgnZWwudGFibGUuc2VsZWN0QWxsTGFiZWwnKX1cbiAgICAgICAgb25DaGFuZ2U9e29uQ2hhbmdlfVxuICAgICAgLz5cbiAgICApXG4gIH0sXG59KVxuXG5jb25zdCBkYXRhID0gcmVmKGdlbmVyYXRlRGF0YShjb2x1bW5zLCAyMDApKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/selection.vue)_

vue

```
<template>
  <div style="height: 400px">
    <el-auto-resizer>
      <template #default="{ height, width }">
        <el-table-v2
          :columns="columns"
          :data="data"
          :width="width"
          :height="height"
          fixed
        />
      </template>
    </el-auto-resizer>
  </div>
</template>

<script lang="tsx" setup>
import { ref, unref } from 'vue'
import { ElCheckbox, useLocale } from 'element-plus'

import type { FunctionalComponent } from 'vue'
import type { CheckboxValueType, Column } from 'element-plus'

type SelectionCellProps = {
  value: boolean
  intermediate?: boolean
  ariaLabel?: string
  onChange: (value: CheckboxValueType) => void
}

const { t } = useLocale()

const SelectionCell: FunctionalComponent<SelectionCellProps> = ({
  value,
  intermediate = false,
  ariaLabel,
  onChange,
}) => {
  return (
    <ElCheckbox
      onChange={onChange}
      modelValue={value}
      ariaLabel={ariaLabel}
      indeterminate={intermediate}
    />
  )
}

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        checked: false,
        parentId: null,
      }
    )
  })

const columns: Column<any>[] = generateColumns(10)
columns.unshift({
  key: 'selection',
  width: 50,
  cellRenderer: ({ rowData }) => {
    const onChange = (value: CheckboxValueType) => (rowData.checked = value)
    return (
      <SelectionCell
        value={rowData.checked}
        ariaLabel={t('el.table.selectRowLabel')}
        onChange={onChange}
      />
    )
  },

  headerCellRenderer: () => {
    const _data = unref(data)
    const onChange = (value: CheckboxValueType) =>
      (data.value = _data.map((row) => {
        row.checked = value
        return row
      }))
    const allSelected = _data.every((row) => row.checked)
    const containsChecked = _data.some((row) => row.checked)

    return (
      <SelectionCell
        value={allSelected}
        intermediate={containsChecked && !allSelected}
        ariaLabel={t('el.table.selectAllLabel')}
        onChange={onChange}
      />
    )
  },
})

const data = ref(generateData(columns, 200))
</script>
```

隐藏源代码

## 可编辑单元格 [​](#可编辑单元格)

类似上面添加筛选框的方法，我们可以用同样的方法实现可编辑单元格。

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Editable Column

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwiaGVpZ2h0OiA0MDBweFwiPlxuICAgIDxlbC1hdXRvLXJlc2l6ZXI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJ7IGhlaWdodCwgd2lkdGggfVwiPlxuICAgICAgICA8ZWwtdGFibGUtdjJcbiAgICAgICAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgICAgICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgICAgICAgOndpZHRoPVwid2lkdGhcIlxuICAgICAgICAgIDpoZWlnaHQ9XCJoZWlnaHRcIlxuICAgICAgICAgIGZpeGVkXG4gICAgICAgIC8+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtYXV0by1yZXNpemVyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzeFwiIHNldHVwPlxuaW1wb3J0IHsgcmVmLCB3aXRoS2V5cyB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsSW5wdXQgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmltcG9ydCB0eXBlIHsgRnVuY3Rpb25hbENvbXBvbmVudCB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB0eXBlIHsgQ29sdW1uLCBJbnB1dEluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG50eXBlIFNlbGVjdGlvbkNlbGxQcm9wcyA9IHtcbiAgdmFsdWU6IHN0cmluZ1xuICBpbnRlcm1lZGlhdGU/OiBib29sZWFuXG4gIG9uQ2hhbmdlOiAodmFsdWU6IHN0cmluZykgPT4gdm9pZFxuICBvbkJsdXI6ICgpID0+IHZvaWRcbiAgb25LZXlkb3duRW50ZXI6ICgpID0+IHZvaWRcbiAgZm9yd2FyZFJlZjogKGVsOiBJbnB1dEluc3RhbmNlKSA9PiB2b2lkXG59XG5cbmNvbnN0IElucHV0Q2VsbDogRnVuY3Rpb25hbENvbXBvbmVudDxTZWxlY3Rpb25DZWxsUHJvcHM+ID0gKHtcbiAgdmFsdWUsXG4gIG9uQ2hhbmdlLFxuICBvbkJsdXIsXG4gIG9uS2V5ZG93bkVudGVyLFxuICBmb3J3YXJkUmVmLFxufSkgPT4ge1xuICByZXR1cm4gKFxuICAgIDxFbElucHV0XG4gICAgICByZWY9e2ZvcndhcmRSZWYgYXMgYW55fVxuICAgICAgb25JbnB1dD17b25DaGFuZ2V9XG4gICAgICBvbkJsdXI9e29uQmx1cn1cbiAgICAgIG9uS2V5ZG93bj17d2l0aEtleXMob25LZXlkb3duRW50ZXIsIFsnZW50ZXInXSl9XG4gICAgICBtb2RlbFZhbHVlPXt2YWx1ZX1cbiAgICAvPlxuICApXG59XG5cbmNvbnN0IGdlbmVyYXRlQ29sdW1ucyA9IChsZW5ndGggPSAxMCwgcHJlZml4ID0gJ2NvbHVtbi0nLCBwcm9wcz86IGFueSkgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIGNvbHVtbkluZGV4KSA9PiAoe1xuICAgIC4uLnByb3BzLFxuICAgIGtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICBkYXRhS2V5OiBgJHtwcmVmaXh9JHtjb2x1bW5JbmRleH1gLFxuICAgIHRpdGxlOiBgQ29sdW1uICR7Y29sdW1uSW5kZXh9YCxcbiAgICB3aWR0aDogMTUwLFxuICB9KSlcblxuY29uc3QgZ2VuZXJhdGVEYXRhID0gKFxuICBjb2x1bW5zOiBSZXR1cm5UeXBlPHR5cGVvZiBnZW5lcmF0ZUNvbHVtbnM+LFxuICBsZW5ndGggPSAyMDAsXG4gIHByZWZpeCA9ICdyb3ctJ1xuKSA9PlxuICBBcnJheS5mcm9tKHsgbGVuZ3RoIH0pLm1hcCgoXywgcm93SW5kZXgpID0+IHtcbiAgICByZXR1cm4gY29sdW1ucy5yZWR1Y2UoXG4gICAgICAocm93RGF0YSwgY29sdW1uLCBjb2x1bW5JbmRleCkgPT4ge1xuICAgICAgICByb3dEYXRhW2NvbHVtbi5kYXRhS2V5XSA9IGBSb3cgJHtyb3dJbmRleH0gLSBDb2wgJHtjb2x1bW5JbmRleH1gXG4gICAgICAgIHJldHVybiByb3dEYXRhXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogYCR7cHJlZml4fSR7cm93SW5kZXh9YCxcbiAgICAgICAgZWRpdGluZzogZmFsc2UsXG4gICAgICAgIHBhcmVudElkOiBudWxsLFxuICAgICAgfVxuICAgIClcbiAgfSlcblxuY29uc3QgY29sdW1uczogQ29sdW1uPGFueT5bXSA9IGdlbmVyYXRlQ29sdW1ucygxMClcbmNvbHVtbnNbMF0gPSB7XG4gIC4uLmNvbHVtbnNbMF0sXG4gIHRpdGxlOiAnRWRpdGFibGUgQ29sdW1uJyxcbiAgY2VsbFJlbmRlcmVyOiAoeyByb3dEYXRhLCBjb2x1bW4gfSkgPT4ge1xuICAgIGNvbnN0IG9uQ2hhbmdlID0gKHZhbHVlOiBzdHJpbmcpID0+IHtcbiAgICAgIHJvd0RhdGFbY29sdW1uLmRhdGFLZXkhXSA9IHZhbHVlXG4gICAgfVxuICAgIGNvbnN0IG9uRW50ZXJFZGl0TW9kZSA9ICgpID0+IHtcbiAgICAgIHJvd0RhdGEuZWRpdGluZyA9IHRydWVcbiAgICB9XG5cbiAgICBjb25zdCBvbkV4aXRFZGl0TW9kZSA9ICgpID0+IChyb3dEYXRhLmVkaXRpbmcgPSBmYWxzZSlcbiAgICBjb25zdCBpbnB1dCA9IHJlZigpXG4gICAgY29uc3Qgc2V0UmVmID0gKGVsKSA9PiB7XG4gICAgICBpbnB1dC52YWx1ZSA9IGVsXG4gICAgICBpZiAoZWwpIHtcbiAgICAgICAgZWwuZm9jdXM/LigpXG4gICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIHJvd0RhdGEuZWRpdGluZyA/IChcbiAgICAgIDxJbnB1dENlbGxcbiAgICAgICAgZm9yd2FyZFJlZj17c2V0UmVmfVxuICAgICAgICB2YWx1ZT17cm93RGF0YVtjb2x1bW4uZGF0YUtleSFdfVxuICAgICAgICBvbkNoYW5nZT17b25DaGFuZ2V9XG4gICAgICAgIG9uQmx1cj17b25FeGl0RWRpdE1vZGV9XG4gICAgICAgIG9uS2V5ZG93bkVudGVyPXtvbkV4aXRFZGl0TW9kZX1cbiAgICAgIC8+XG4gICAgKSA6IChcbiAgICAgIDxkaXYgY2xhc3M9XCJ0YWJsZS12Mi1pbmxpbmUtZWRpdGluZy10cmlnZ2VyXCIgb25DbGljaz17b25FbnRlckVkaXRNb2RlfT5cbiAgICAgICAge3Jvd0RhdGFbY29sdW1uLmRhdGFLZXkhXX1cbiAgICAgIDwvZGl2PlxuICAgIClcbiAgfSxcbn1cblxuY29uc3QgZGF0YSA9IHJlZihnZW5lcmF0ZURhdGEoY29sdW1ucywgMjAwKSlcbjwvc2NyaXB0PlxuXG48c3R5bGU+XG4udGFibGUtdjItaW5saW5lLWVkaXRpbmctdHJpZ2dlciB7XG4gIGJvcmRlcjogMXB4IHRyYW5zcGFyZW50IGRvdHRlZDtcbiAgcGFkZGluZzogNHB4O1xufVxuXG4udGFibGUtdjItaW5saW5lLWVkaXRpbmctdHJpZ2dlcjpob3ZlciB7XG4gIGJvcmRlci1jb2xvcjogdmFyKC0tZWwtY29sb3ItcHJpbWFyeSk7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/inline-editing.vue)_

vue

```
<template>
  <div style="height: 400px">
    <el-auto-resizer>
      <template #default="{ height, width }">
        <el-table-v2
          :columns="columns"
          :data="data"
          :width="width"
          :height="height"
          fixed
        />
      </template>
    </el-auto-resizer>
  </div>
</template>

<script lang="tsx" setup>
import { ref, withKeys } from 'vue'
import { ElInput } from 'element-plus'

import type { FunctionalComponent } from 'vue'
import type { Column, InputInstance } from 'element-plus'

type SelectionCellProps = {
  value: string
  intermediate?: boolean
  onChange: (value: string) => void
  onBlur: () => void
  onKeydownEnter: () => void
  forwardRef: (el: InputInstance) => void
}

const InputCell: FunctionalComponent<SelectionCellProps> = ({
  value,
  onChange,
  onBlur,
  onKeydownEnter,
  forwardRef,
}) => {
  return (
    <ElInput
      ref={forwardRef as any}
      onInput={onChange}
      onBlur={onBlur}
      onKeydown={withKeys(onKeydownEnter, ['enter'])}
      modelValue={value}
    />
  )
}

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        editing: false,
        parentId: null,
      }
    )
  })

const columns: Column<any>[] = generateColumns(10)
columns[0] = {
  ...columns[0],
  title: 'Editable Column',
  cellRenderer: ({ rowData, column }) => {
    const onChange = (value: string) => {
      rowData[column.dataKey!] = value
    }
    const onEnterEditMode = () => {
      rowData.editing = true
    }

    const onExitEditMode = () => (rowData.editing = false)
    const input = ref()
    const setRef = (el) => {
      input.value = el
      if (el) {
        el.focus?.()
      }
    }

    return rowData.editing ? (
      <InputCell
        forwardRef={setRef}
        value={rowData[column.dataKey!]}
        onChange={onChange}
        onBlur={onExitEditMode}
        onKeydownEnter={onExitEditMode}
      />
    ) : (
      <div class="table-v2-inline-editing-trigger" onClick={onEnterEditMode}>
        {rowData[column.dataKey!]}
      </div>
    )
  },
}

const data = ref(generateData(columns, 200))
</script>

<style>
.table-v2-inline-editing-trigger {
  border: 1px transparent dotted;
  padding: 4px;
}

.table-v2-inline-editing-trigger:hover {
  border-color: var(--el-color-primary);
}
</style>
```

隐藏源代码

## 带状态的表格 [​](#带状态的表格)

可将表格内容 highlight 显示，方便区分「成功、信息、警告、危险」等内容。

要自定义行的外观，请使用 `row-class-name` 属性。 举个例子，每10行会自动添加 `bg-blue-200` 类名，每5行会添加 `bg-red-100` 类名。

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Tom

EditDelete

Name

Operations

2020/10/01

2020/10/01

2020/10/01

2020/10/01

2020/10/01

2020/10/01

2020/10/01

2020/10/01

2020/10/01

Date

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOnJvdy1jbGFzcz1cInJvd0NsYXNzXCJcbiAgICA6d2lkdGg9XCI3MDBcIlxuICAgIDpoZWlnaHQ9XCI0MDBcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHN4XCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgZGF5anMgZnJvbSAnZGF5anMnXG5pbXBvcnQge1xuICBFbEJ1dHRvbixcbiAgRWxJY29uLFxuICBFbFRhZyxcbiAgRWxUb29sdGlwLFxuICBUYWJsZVYyRml4ZWREaXIsXG59IGZyb20gJ2VsZW1lbnQtcGx1cydcbmltcG9ydCB7IFRpbWVyIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmltcG9ydCB0eXBlIHsgQ29sdW1uLCBSb3dDbGFzc05hbWVHZXR0ZXIgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmxldCBpZCA9IDBcblxuY29uc3QgZGF0YUdlbmVyYXRvciA9ICgpID0+ICh7XG4gIGlkOiBgcmFuZG9tLWlkLSR7KytpZH1gLFxuICBuYW1lOiAnVG9tJyxcbiAgZGF0ZTogJzIwMjAtMTAtMScsXG59KVxuXG5jb25zdCBjb2x1bW5zOiBDb2x1bW48YW55PltdID0gW1xuICB7XG4gICAga2V5OiAnZGF0ZScsXG4gICAgdGl0bGU6ICdEYXRlJyxcbiAgICBkYXRhS2V5OiAnZGF0ZScsXG4gICAgd2lkdGg6IDE1MCxcbiAgICBmaXhlZDogVGFibGVWMkZpeGVkRGlyLkxFRlQsXG4gICAgY2VsbFJlbmRlcmVyOiAoeyBjZWxsRGF0YTogZGF0ZSB9KSA9PiAoXG4gICAgICA8RWxUb29sdGlwIGNvbnRlbnQ9e2RheWpzKGRhdGUpLmZvcm1hdCgnWVlZWS9NTS9ERCcpfT5cbiAgICAgICAge1xuICAgICAgICAgIDxzcGFuIGNsYXNzPVwiZmxleCBpdGVtcy1jZW50ZXJcIj5cbiAgICAgICAgICAgIDxFbEljb24gY2xhc3M9XCJtci0zXCI+XG4gICAgICAgICAgICAgIDxUaW1lciAvPlxuICAgICAgICAgICAgPC9FbEljb24+XG4gICAgICAgICAgICB7ZGF5anMoZGF0ZSkuZm9ybWF0KCdZWVlZL01NL0REJyl9XG4gICAgICAgICAgPC9zcGFuPlxuICAgICAgICB9XG4gICAgICA8L0VsVG9vbHRpcD5cbiAgICApLFxuICB9LFxuICB7XG4gICAga2V5OiAnbmFtZScsXG4gICAgdGl0bGU6ICdOYW1lJyxcbiAgICBkYXRhS2V5OiAnbmFtZScsXG4gICAgd2lkdGg6IDE1MCxcbiAgICBhbGlnbjogJ2NlbnRlcicsXG4gICAgY2VsbFJlbmRlcmVyOiAoeyBjZWxsRGF0YTogbmFtZSB9KSA9PiA8RWxUYWc+e25hbWV9PC9FbFRhZz4sXG4gIH0sXG4gIHtcbiAgICBrZXk6ICdvcGVyYXRpb25zJyxcbiAgICB0aXRsZTogJ09wZXJhdGlvbnMnLFxuICAgIGNlbGxSZW5kZXJlcjogKCkgPT4gKFxuICAgICAgPD5cbiAgICAgICAgPEVsQnV0dG9uIHNpemU9XCJzbWFsbFwiPkVkaXQ8L0VsQnV0dG9uPlxuICAgICAgICA8RWxCdXR0b24gc2l6ZT1cInNtYWxsXCIgdHlwZT1cImRhbmdlclwiPlxuICAgICAgICAgIERlbGV0ZVxuICAgICAgICA8L0VsQnV0dG9uPlxuICAgICAgPC8+XG4gICAgKSxcbiAgICB3aWR0aDogMTUwLFxuICAgIGFsaWduOiAnY2VudGVyJyxcbiAgICBmbGV4R3JvdzogMSxcbiAgfSxcbl1cblxuY29uc3QgZGF0YSA9IHJlZihBcnJheS5mcm9tKHsgbGVuZ3RoOiAyMDAgfSkubWFwKGRhdGFHZW5lcmF0b3IpKVxuXG5jb25zdCByb3dDbGFzcyA9ICh7IHJvd0luZGV4IH06IFBhcmFtZXRlcnM8Um93Q2xhc3NOYW1lR2V0dGVyPGFueT4+WzBdKSA9PiB7XG4gIGlmIChyb3dJbmRleCAlIDEwID09PSA1KSB7XG4gICAgcmV0dXJuICdiZy1yZWQtMTAwJ1xuICB9IGVsc2UgaWYgKHJvd0luZGV4ICUgMTAgPT09IDApIHtcbiAgICByZXR1cm4gJ2JnLWJsdWUtMjAwJ1xuICB9XG4gIHJldHVybiAnJ1xufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/row-class.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :row-class="rowClass"
    :width="700"
    :height="400"
  />
</template>

<script lang="tsx" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'
import {
  ElButton,
  ElIcon,
  ElTag,
  ElTooltip,
  TableV2FixedDir,
} from 'element-plus'
import { Timer } from '@element-plus/icons-vue'

import type { Column, RowClassNameGetter } from 'element-plus'

let id = 0

const dataGenerator = () => ({
  id: `random-id-${++id}`,
  name: 'Tom',
  date: '2020-10-1',
})

const columns: Column<any>[] = [
  {
    key: 'date',
    title: 'Date',
    dataKey: 'date',
    width: 150,
    fixed: TableV2FixedDir.LEFT,
    cellRenderer: ({ cellData: date }) => (
      <ElTooltip content={dayjs(date).format('YYYY/MM/DD')}>
        {
          <span class="flex items-center">
            <ElIcon class="mr-3">
              <Timer />
            </ElIcon>
            {dayjs(date).format('YYYY/MM/DD')}
          </span>
        }
      </ElTooltip>
    ),
  },
  {
    key: 'name',
    title: 'Name',
    dataKey: 'name',
    width: 150,
    align: 'center',
    cellRenderer: ({ cellData: name }) => <ElTag>{name}</ElTag>,
  },
  {
    key: 'operations',
    title: 'Operations',
    cellRenderer: () => (
      <>
        <ElButton size="small">Edit</ElButton>
        <ElButton size="small" type="danger">
          Delete
        </ElButton>
      </>
    ),
    width: 150,
    align: 'center',
    flexGrow: 1,
  },
]

const data = ref(Array.from({ length: 200 }).map(dataGenerator))

const rowClass = ({ rowIndex }: Parameters<RowClassNameGetter<any>>[0]) => {
  if (rowIndex % 10 === 5) {
    return 'bg-red-100'
  } else if (rowIndex % 10 === 0) {
    return 'bg-blue-200'
  }
  return ''
}
</script>
```

隐藏源代码

## 表格行的粘性布局 [​](#表格行的粘性布局)

您可以简单地使用 `fixed-data` 属性来实现将某些行固定到表格的头部。

您可以根据滚动事件动态设置粘性行，如这个示例所示。

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwidGFibGVEYXRhXCJcbiAgICA6Zml4ZWQtZGF0YT1cImZpeGVkRGF0YVwiXG4gICAgOndpZHRoPVwiNzAwXCJcbiAgICA6aGVpZ2h0PVwiNDAwXCJcbiAgICA6cm93LWNsYXNzPVwicm93Q2xhc3NcIlxuICAgIGZpeGVkXG4gICAgQHNjcm9sbD1cIm9uU2Nyb2xsXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBjb21wdXRlZCwgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBnZW5lcmF0ZUNvbHVtbnMgPSAobGVuZ3RoID0gMTAsIHByZWZpeCA9ICdjb2x1bW4tJywgcHJvcHM/OiBhbnkpID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCBjb2x1bW5JbmRleCkgPT4gKHtcbiAgICAuLi5wcm9wcyxcbiAgICBrZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgZGF0YUtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICB0aXRsZTogYENvbHVtbiAke2NvbHVtbkluZGV4fWAsXG4gICAgd2lkdGg6IDE1MCxcbiAgfSkpXG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9IChcbiAgY29sdW1uczogUmV0dXJuVHlwZTx0eXBlb2YgZ2VuZXJhdGVDb2x1bW5zPixcbiAgbGVuZ3RoID0gMjAwLFxuICBwcmVmaXggPSAncm93LSdcbikgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIHJvd0luZGV4KSA9PiB7XG4gICAgcmV0dXJuIGNvbHVtbnMucmVkdWNlKFxuICAgICAgKHJvd0RhdGEsIGNvbHVtbiwgY29sdW1uSW5kZXgpID0+IHtcbiAgICAgICAgcm93RGF0YVtjb2x1bW4uZGF0YUtleV0gPSBgUm93ICR7cm93SW5kZXh9IC0gQ29sICR7Y29sdW1uSW5kZXh9YFxuICAgICAgICByZXR1cm4gcm93RGF0YVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IGAke3ByZWZpeH0ke3Jvd0luZGV4fWAsXG4gICAgICAgIHBhcmVudElkOiBudWxsLFxuICAgICAgfVxuICAgIClcbiAgfSlcblxuY29uc3QgY29sdW1ucyA9IGdlbmVyYXRlQ29sdW1ucygxMClcbmNvbnN0IGRhdGEgPSBnZW5lcmF0ZURhdGEoY29sdW1ucywgMjAwKVxuXG5jb25zdCByb3dDbGFzcyA9ICh7IHJvd0luZGV4IH0pID0+IHtcbiAgaWYgKHJvd0luZGV4IDwgMCB8fCAocm93SW5kZXggKyAxKSAlIDUgPT09IDApIHJldHVybiAnc3RpY2t5LXJvdydcbn1cblxuY29uc3Qgc3RpY2t5SW5kZXggPSByZWYoMClcblxuY29uc3QgZml4ZWREYXRhID0gY29tcHV0ZWQoKCkgPT5cbiAgZGF0YS5zbGljZShzdGlja3lJbmRleC52YWx1ZSwgc3RpY2t5SW5kZXgudmFsdWUgKyAxKVxuKVxuXG5jb25zdCB0YWJsZURhdGEgPSBjb21wdXRlZCgoKSA9PiB7XG4gIHJldHVybiBkYXRhLnNsaWNlKDEpXG59KVxuXG5jb25zdCBvblNjcm9sbCA9ICh7IHNjcm9sbFRvcCB9KSA9PiB7XG4gIHN0aWNreUluZGV4LnZhbHVlID0gTWF0aC5mbG9vcihzY3JvbGxUb3AgLyAyNTApICogNVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5lbC1lbC10YWJsZS12Ml9fZml4ZWQtaGVhZGVyLXJvdyB7XG4gIGJhY2tncm91bmQtY29sb3I6IHZhcigtLWVsLWNvbG9yLXByaW1hcnktbGlnaHQtNSk7XG4gIGZvbnQtd2VpZ2h0OiBib2xkO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/sticky-rows.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="tableData"
    :fixed-data="fixedData"
    :width="700"
    :height="400"
    :row-class="rowClass"
    fixed
    @scroll="onScroll"
  />
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = generateData(columns, 200)

const rowClass = ({ rowIndex }) => {
  if (rowIndex < 0 || (rowIndex + 1) % 5 === 0) return 'sticky-row'
}

const stickyIndex = ref(0)

const fixedData = computed(() =>
  data.slice(stickyIndex.value, stickyIndex.value + 1)
)

const tableData = computed(() => {
  return data.slice(1)
})

const onScroll = ({ scrollTop }) => {
  stickyIndex.value = Math.floor(scrollTop / 250) * 5
}
</script>

<style>
.el-el-table-v2__fixed-header-row {
  background-color: var(--el-color-primary-light-5);
  font-weight: bold;
}
</style>
```

隐藏源代码

## 固定列表格 [​](#固定列表格)

如果您想要有列粘贴左侧或右侧的某种原因。 您可以通过向表中添加特殊属性来实现这一点。

您可以设置该行的 `fixed` 属性为 `true` （代表`FixedDir.LEFT`）、`FixedDir.LEFT` 或 `FixedDir.RIGHT`

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Row 0 - Col 0

Row 0 - Col 1

Row 1 - Col 0

Row 1 - Col 1

Row 2 - Col 0

Row 2 - Col 1

Row 3 - Col 0

Row 3 - Col 1

Row 4 - Col 0

Row 4 - Col 1

Row 5 - Col 0

Row 5 - Col 1

Row 6 - Col 0

Row 6 - Col 1

Row 7 - Col 0

Row 7 - Col 1

Row 8 - Col 0

Row 8 - Col 1

Column 0

Column 1

Row 0 - Col 9

Row 1 - Col 9

Row 2 - Col 9

Row 3 - Col 9

Row 4 - Col 9

Row 5 - Col 9

Row 6 - Col 9

Row 7 - Col 9

Row 8 - Col 9

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOnNvcnQtYnk9XCJzb3J0QnlcIlxuICAgIDp3aWR0aD1cIjcwMFwiXG4gICAgOmhlaWdodD1cIjQwMFwiXG4gICAgZml4ZWRcbiAgICBAY29sdW1uLXNvcnQ9XCJvblNvcnRcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IFRhYmxlVjJGaXhlZERpciwgVGFibGVWMlNvcnRPcmRlciB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW1wb3J0IHR5cGUgeyBTb3J0QnkgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGdlbmVyYXRlQ29sdW1ucyA9IChsZW5ndGggPSAxMCwgcHJlZml4ID0gJ2NvbHVtbi0nLCBwcm9wcz86IGFueSkgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIGNvbHVtbkluZGV4KSA9PiAoe1xuICAgIC4uLnByb3BzLFxuICAgIGtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICBkYXRhS2V5OiBgJHtwcmVmaXh9JHtjb2x1bW5JbmRleH1gLFxuICAgIHRpdGxlOiBgQ29sdW1uICR7Y29sdW1uSW5kZXh9YCxcbiAgICB3aWR0aDogMTUwLFxuICB9KSlcblxuY29uc3QgZ2VuZXJhdGVEYXRhID0gKFxuICBjb2x1bW5zOiBSZXR1cm5UeXBlPHR5cGVvZiBnZW5lcmF0ZUNvbHVtbnM+LFxuICBsZW5ndGggPSAyMDAsXG4gIHByZWZpeCA9ICdyb3ctJ1xuKSA9PlxuICBBcnJheS5mcm9tKHsgbGVuZ3RoIH0pLm1hcCgoXywgcm93SW5kZXgpID0+IHtcbiAgICByZXR1cm4gY29sdW1ucy5yZWR1Y2UoXG4gICAgICAocm93RGF0YSwgY29sdW1uLCBjb2x1bW5JbmRleCkgPT4ge1xuICAgICAgICByb3dEYXRhW2NvbHVtbi5kYXRhS2V5XSA9IGBSb3cgJHtyb3dJbmRleH0gLSBDb2wgJHtjb2x1bW5JbmRleH1gXG4gICAgICAgIHJldHVybiByb3dEYXRhXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogYCR7cHJlZml4fSR7cm93SW5kZXh9YCxcbiAgICAgICAgcGFyZW50SWQ6IG51bGwsXG4gICAgICB9XG4gICAgKVxuICB9KVxuXG5jb25zdCBjb2x1bW5zID0gZ2VuZXJhdGVDb2x1bW5zKDEwKVxubGV0IGRhdGEgPSBnZW5lcmF0ZURhdGEoY29sdW1ucywgMjAwKVxuXG5jb2x1bW5zWzBdLmZpeGVkID0gdHJ1ZVxuY29sdW1uc1sxXS5maXhlZCA9IFRhYmxlVjJGaXhlZERpci5MRUZUXG5jb2x1bW5zWzldLmZpeGVkID0gVGFibGVWMkZpeGVkRGlyLlJJR0hUXG5cbmZvciAobGV0IGkgPSAwOyBpIDwgMzsgaSsrKSBjb2x1bW5zW2ldLnNvcnRhYmxlID0gdHJ1ZVxuXG5jb25zdCBzb3J0QnkgPSByZWY8U29ydEJ5Pih7XG4gIGtleTogJ2NvbHVtbi0wJyxcbiAgb3JkZXI6IFRhYmxlVjJTb3J0T3JkZXIuQVNDLFxufSlcblxuY29uc3Qgb25Tb3J0ID0gKF9zb3J0Qnk6IFNvcnRCeSkgPT4ge1xuICBkYXRhID0gZGF0YS5yZXZlcnNlKClcbiAgc29ydEJ5LnZhbHVlID0gX3NvcnRCeVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/fixed-columns.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :sort-by="sortBy"
    :width="700"
    :height="400"
    fixed
    @column-sort="onSort"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { TableV2FixedDir, TableV2SortOrder } from 'element-plus'

import type { SortBy } from 'element-plus'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
let data = generateData(columns, 200)

columns[0].fixed = true
columns[1].fixed = TableV2FixedDir.LEFT
columns[9].fixed = TableV2FixedDir.RIGHT

for (let i = 0; i < 3; i++) columns[i].sortable = true

const sortBy = ref<SortBy>({
  key: 'column-0',
  order: TableV2SortOrder.ASC,
})

const onSort = (_sortBy: SortBy) => {
  data = data.reverse()
  sortBy.value = _sortBy
}
</script>
```

隐藏源代码

## 表头分组 [​](#表头分组)

正如这个示例，通过自定义表头渲染以将表头分组。

TIP

在这种情况下，我们使用了 `JSX` 功能，这个功能在playground上不被支持。 您可以在本地环境或在线集成开发环境（如 `codesandbox` ）中试用它们。

建议您使用 JSX 使用您的表格组件，因为它包含 VNode 操作。

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 0 - Col 10

Row 0 - Col 11

Row 0 - Col 12

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 1 - Col 10

Row 1 - Col 11

Row 1 - Col 12

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 2 - Col 10

Row 2 - Col 11

Row 2 - Col 12

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 3 - Col 10

Row 3 - Col 11

Row 3 - Col 12

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 4 - Col 10

Row 4 - Col 11

Row 4 - Col 12

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 5 - Col 10

Row 5 - Col 11

Row 5 - Col 12

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 6 - Col 10

Row 6 - Col 11

Row 6 - Col 12

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 7 - Col 10

Row 7 - Col 11

Row 7 - Col 12

Group width 400

Group width 400

Group width 200

Group width 200

Group width 200

Group width 200

Group width 200

Group width 200

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

Column 10

Column 11

Column 12

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Group width 300

Group width 200

Group width 100

Column 0

Column 1

Column 2

Row 0 - Col 13

Row 0 - Col 14

Row 1 - Col 13

Row 1 - Col 14

Row 2 - Col 13

Row 2 - Col 14

Row 3 - Col 13

Row 3 - Col 14

Row 4 - Col 13

Row 4 - Col 14

Row 5 - Col 13

Row 5 - Col 14

Row 6 - Col 13

Row 6 - Col 14

Row 7 - Col 13

Row 7 - Col 14

Group width 200

Group width 200

Column 13

Column 14

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICBmaXhlZFxuICAgIDpjb2x1bW5zPVwiZml4ZWRDb2x1bW5zXCJcbiAgICA6ZGF0YT1cImRhdGFcIlxuICAgIDpoZWFkZXItaGVpZ2h0PVwiWzUwLCA0MCwgNTBdXCJcbiAgICA6aGVhZGVyLWNsYXNzPVwiaGVhZGVyQ2xhc3NcIlxuICAgIDp3aWR0aD1cIjcwMFwiXG4gICAgOmhlaWdodD1cIjQwMFwiXG4gID5cbiAgICA8dGVtcGxhdGUgI2hlYWRlcj1cInByb3BzXCI+XG4gICAgICA8Y3VzdG9taXplZC1oZWFkZXIgdi1iaW5kPVwicHJvcHNcIiAvPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtdGFibGUtdjI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c3hcIiBzZXR1cD5cbmltcG9ydCB7IFRhYmxlVjJGaXhlZERpciwgVGFibGVWMlBsYWNlaG9sZGVyIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbXBvcnQgdHlwZSB7IEZ1bmN0aW9uYWxDb21wb25lbnQgfSBmcm9tICd2dWUnXG5pbXBvcnQgdHlwZSB7XG4gIEhlYWRlckNsYXNzTmFtZUdldHRlcixcbiAgVGFibGVWMkN1c3RvbWl6ZWRIZWFkZXJTbG90UGFyYW0sXG59IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgZ2VuZXJhdGVDb2x1bW5zID0gKGxlbmd0aCA9IDEwLCBwcmVmaXggPSAnY29sdW1uLScsIHByb3BzPzogYW55KSA9PlxuICBBcnJheS5mcm9tKHsgbGVuZ3RoIH0pLm1hcCgoXywgY29sdW1uSW5kZXgpID0+ICh7XG4gICAgLi4ucHJvcHMsXG4gICAga2V5OiBgJHtwcmVmaXh9JHtjb2x1bW5JbmRleH1gLFxuICAgIGRhdGFLZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgdGl0bGU6IGBDb2x1bW4gJHtjb2x1bW5JbmRleH1gLFxuICAgIHdpZHRoOiAxNTAsXG4gIH0pKVxuXG5jb25zdCBnZW5lcmF0ZURhdGEgPSAoXG4gIGNvbHVtbnM6IFJldHVyblR5cGU8dHlwZW9mIGdlbmVyYXRlQ29sdW1ucz4sXG4gIGxlbmd0aCA9IDIwMCxcbiAgcHJlZml4ID0gJ3Jvdy0nXG4pID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCByb3dJbmRleCkgPT4ge1xuICAgIHJldHVybiBjb2x1bW5zLnJlZHVjZShcbiAgICAgIChyb3dEYXRhLCBjb2x1bW4sIGNvbHVtbkluZGV4KSA9PiB7XG4gICAgICAgIHJvd0RhdGFbY29sdW1uLmRhdGFLZXldID0gYFJvdyAke3Jvd0luZGV4fSAtIENvbCAke2NvbHVtbkluZGV4fWBcbiAgICAgICAgcmV0dXJuIHJvd0RhdGFcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiBgJHtwcmVmaXh9JHtyb3dJbmRleH1gLFxuICAgICAgICBwYXJlbnRJZDogbnVsbCxcbiAgICAgIH1cbiAgICApXG4gIH0pXG5jb25zdCBjb2x1bW5zID0gZ2VuZXJhdGVDb2x1bW5zKDE1KVxuY29uc3QgZGF0YSA9IGdlbmVyYXRlRGF0YShjb2x1bW5zLCAyMDApXG5cbmNvbnN0IGZpeGVkQ29sdW1ucyA9IGNvbHVtbnMubWFwKChjb2x1bW4sIGNvbHVtbkluZGV4KSA9PiB7XG4gIGxldCBmaXhlZDogVGFibGVWMkZpeGVkRGlyIHwgdW5kZWZpbmVkID0gdW5kZWZpbmVkXG4gIGlmIChjb2x1bW5JbmRleCA8IDMpIGZpeGVkID0gVGFibGVWMkZpeGVkRGlyLkxFRlRcbiAgaWYgKGNvbHVtbkluZGV4ID4gMTIpIGZpeGVkID0gVGFibGVWMkZpeGVkRGlyLlJJR0hUXG4gIHJldHVybiB7IC4uLmNvbHVtbiwgZml4ZWQsIHdpZHRoOiAxMDAgfVxufSlcblxuY29uc3QgQ3VzdG9taXplZEhlYWRlcjogRnVuY3Rpb25hbENvbXBvbmVudDxcbiAgVGFibGVWMkN1c3RvbWl6ZWRIZWFkZXJTbG90UGFyYW1cbj4gPSAoeyBjZWxscywgY29sdW1ucywgaGVhZGVySW5kZXggfSkgPT4ge1xuICBpZiAoaGVhZGVySW5kZXggPT09IDIpIHJldHVybiBjZWxsc1xuXG4gIGNvbnN0IGdyb3VwQ2VsbHMgPSBbXSBhcyB0eXBlb2YgY2VsbHNcbiAgbGV0IHdpZHRoID0gMFxuICBsZXQgaWR4ID0gMFxuXG4gIGNvbHVtbnMuZm9yRWFjaCgoY29sdW1uLCBjb2x1bW5JbmRleCkgPT4ge1xuICAgIGlmIChjb2x1bW4ucGxhY2Vob2xkZXJTaWduID09PSBUYWJsZVYyUGxhY2Vob2xkZXIpXG4gICAgICBncm91cENlbGxzLnB1c2goY2VsbHNbY29sdW1uSW5kZXhdKVxuICAgIGVsc2Uge1xuICAgICAgd2lkdGggKz0gY2VsbHNbY29sdW1uSW5kZXhdLnByb3BzIS5jb2x1bW4ud2lkdGhcbiAgICAgIGlkeCsrXG5cbiAgICAgIGNvbnN0IG5leHRDb2x1bW4gPSBjb2x1bW5zW2NvbHVtbkluZGV4ICsgMV1cbiAgICAgIGlmIChcbiAgICAgICAgY29sdW1uSW5kZXggPT09IGNvbHVtbnMubGVuZ3RoIC0gMSB8fFxuICAgICAgICBuZXh0Q29sdW1uLnBsYWNlaG9sZGVyU2lnbiA9PT0gVGFibGVWMlBsYWNlaG9sZGVyIHx8XG4gICAgICAgIGlkeCA9PT0gKGhlYWRlckluZGV4ID09PSAwID8gNCA6IDIpXG4gICAgICApIHtcbiAgICAgICAgZ3JvdXBDZWxscy5wdXNoKFxuICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgIGNsYXNzPVwiZmxleCBpdGVtcy1jZW50ZXIganVzdGlmeS1jZW50ZXIgY3VzdG9tLWhlYWRlci1jZWxsXCJcbiAgICAgICAgICAgIHJvbGU9XCJjb2x1bW5oZWFkZXJcIlxuICAgICAgICAgICAgc3R5bGU9e3tcbiAgICAgICAgICAgICAgLi4uY2VsbHNbY29sdW1uSW5kZXhdLnByb3BzIS5zdHlsZSxcbiAgICAgICAgICAgICAgd2lkdGg6IGAke3dpZHRofXB4YCxcbiAgICAgICAgICAgIH19XG4gICAgICAgICAgPlxuICAgICAgICAgICAgR3JvdXAgd2lkdGgge3dpZHRofVxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICApXG4gICAgICAgIHdpZHRoID0gMFxuICAgICAgICBpZHggPSAwXG4gICAgICB9XG4gICAgfVxuICB9KVxuICByZXR1cm4gZ3JvdXBDZWxsc1xufVxuXG5jb25zdCBoZWFkZXJDbGFzcyA9ICh7XG4gIGhlYWRlckluZGV4LFxufTogUGFyYW1ldGVyczxIZWFkZXJDbGFzc05hbWVHZXR0ZXI8YW55Pj5bMF0pID0+IHtcbiAgaWYgKGhlYWRlckluZGV4ID09PSAxKSByZXR1cm4gJ2VsLXByaW1hcnktY29sb3InXG4gIHJldHVybiAnJ1xufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5lbC1lbC10YWJsZS12Ml9faGVhZGVyLXJvdyAuY3VzdG9tLWhlYWRlci1jZWxsIHtcbiAgYm9yZGVyLXJpZ2h0OiAxcHggc29saWQgdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbn1cblxuLmVsLWVsLXRhYmxlLXYyX19oZWFkZXItcm93IC5jdXN0b20taGVhZGVyLWNlbGw6bGFzdC1jaGlsZCB7XG4gIGJvcmRlci1yaWdodDogbm9uZTtcbn1cblxuLmVsLXByaW1hcnktY29sb3Ige1xuICBiYWNrZ3JvdW5kLWNvbG9yOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgY29sb3I6IHZhcigtLWVsLWNvbG9yLXdoaXRlKTtcbiAgZm9udC1zaXplOiAxNHB4O1xuICBmb250LXdlaWdodDogYm9sZDtcbn1cblxuLmVsLXByaW1hcnktY29sb3IgLmN1c3RvbS1oZWFkZXItY2VsbCB7XG4gIHBhZGRpbmc6IDAgNHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/grouping-header.vue)_

vue

```
<template>
  <el-table-v2
    fixed
    :columns="fixedColumns"
    :data="data"
    :header-height="[50, 40, 50]"
    :header-class="headerClass"
    :width="700"
    :height="400"
  >
    <template #header="props">
      <customized-header v-bind="props" />
    </template>
  </el-table-v2>
</template>

<script lang="tsx" setup>
import { TableV2FixedDir, TableV2Placeholder } from 'element-plus'

import type { FunctionalComponent } from 'vue'
import type {
  HeaderClassNameGetter,
  TableV2CustomizedHeaderSlotParam,
} from 'element-plus'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })
const columns = generateColumns(15)
const data = generateData(columns, 200)

const fixedColumns = columns.map((column, columnIndex) => {
  let fixed: TableV2FixedDir | undefined = undefined
  if (columnIndex < 3) fixed = TableV2FixedDir.LEFT
  if (columnIndex > 12) fixed = TableV2FixedDir.RIGHT
  return { ...column, fixed, width: 100 }
})

const CustomizedHeader: FunctionalComponent<
  TableV2CustomizedHeaderSlotParam
> = ({ cells, columns, headerIndex }) => {
  if (headerIndex === 2) return cells

  const groupCells = [] as typeof cells
  let width = 0
  let idx = 0

  columns.forEach((column, columnIndex) => {
    if (column.placeholderSign === TableV2Placeholder)
      groupCells.push(cells[columnIndex])
    else {
      width += cells[columnIndex].props!.column.width
      idx++

      const nextColumn = columns[columnIndex + 1]
      if (
        columnIndex === columns.length - 1 ||
        nextColumn.placeholderSign === TableV2Placeholder ||
        idx === (headerIndex === 0 ? 4 : 2)
      ) {
        groupCells.push(
          <div
            class="flex items-center justify-center custom-header-cell"
            role="columnheader"
            style={{
              ...cells[columnIndex].props!.style,
              width: `${width}px`,
            }}
          >
            Group width {width}
          </div>
        )
        width = 0
        idx = 0
      }
    }
  })
  return groupCells
}

const headerClass = ({
  headerIndex,
}: Parameters<HeaderClassNameGetter<any>>[0]) => {
  if (headerIndex === 1) return 'el-primary-color'
  return ''
}
</script>

<style>
.el-el-table-v2__header-row .custom-header-cell {
  border-right: 1px solid var(--el-border-color);
}

.el-el-table-v2__header-row .custom-header-cell:last-child {
  border-right: none;
}

.el-primary-color {
  background-color: var(--el-color-primary);
  color: var(--el-color-white);
  font-size: 14px;
  font-weight: bold;
}

.el-primary-color .custom-header-cell {
  padding: 0 4px;
}
</style>
```

隐藏源代码

## 过滤器 [​](#过滤器)

虚拟表格提供自定义页眉渲染器以创建自定义标题。 然后我们可以利用这些来渲染过滤器。

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

Row 0 - Col 0

Row 0 - Col 1

Row 1 - Col 0

Row 1 - Col 1

Row 2 - Col 0

Row 2 - Col 1

Row 3 - Col 0

Row 3 - Col 1

Row 4 - Col 0

Row 4 - Col 1

Row 5 - Col 0

Row 5 - Col 1

Row 6 - Col 0

Row 6 - Col 1

Row 7 - Col 0

Row 7 - Col 1

Row 8 - Col 0

Row 8 - Col 1

Column 0

Column 1

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICBmaXhlZFxuICAgIDpjb2x1bW5zPVwiZml4ZWRDb2x1bW5zXCJcbiAgICA6ZGF0YT1cImRhdGFcIlxuICAgIDp3aWR0aD1cIjcwMFwiXG4gICAgOmhlaWdodD1cIjQwMFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c3hcIiBzZXR1cD5cbmltcG9ydCB7IGNvbXB1dGVkLCByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQge1xuICBFbEJ1dHRvbixcbiAgRWxDaGVja2JveCxcbiAgRWxJY29uLFxuICBFbFBvcG92ZXIsXG4gIFRhYmxlVjJGaXhlZERpcixcbiAgdXNlTG9jYWxlLFxufSBmcm9tICdlbGVtZW50LXBsdXMnXG5pbXBvcnQgeyBGaWx0ZXIgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuaW1wb3J0IHR5cGUgeyBIZWFkZXJDZWxsU2xvdFByb3BzIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBnZW5lcmF0ZUNvbHVtbnMgPSAobGVuZ3RoID0gMTAsIHByZWZpeCA9ICdjb2x1bW4tJywgcHJvcHM/OiBhbnkpID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCBjb2x1bW5JbmRleCkgPT4gKHtcbiAgICAuLi5wcm9wcyxcbiAgICBrZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgZGF0YUtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICB0aXRsZTogYENvbHVtbiAke2NvbHVtbkluZGV4fWAsXG4gICAgd2lkdGg6IDE1MCxcbiAgfSkpXG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9IChcbiAgY29sdW1uczogUmV0dXJuVHlwZTx0eXBlb2YgZ2VuZXJhdGVDb2x1bW5zPixcbiAgbGVuZ3RoID0gMjAwLFxuICBwcmVmaXggPSAncm93LSdcbikgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIHJvd0luZGV4KSA9PiB7XG4gICAgcmV0dXJuIGNvbHVtbnMucmVkdWNlKFxuICAgICAgKHJvd0RhdGEsIGNvbHVtbiwgY29sdW1uSW5kZXgpID0+IHtcbiAgICAgICAgcm93RGF0YVtjb2x1bW4uZGF0YUtleV0gPSBgUm93ICR7cm93SW5kZXh9IC0gQ29sICR7Y29sdW1uSW5kZXh9YFxuICAgICAgICByZXR1cm4gcm93RGF0YVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IGAke3ByZWZpeH0ke3Jvd0luZGV4fWAsXG4gICAgICAgIHBhcmVudElkOiBudWxsLFxuICAgICAgfVxuICAgIClcbiAgfSlcbmNvbnN0IGNvbHVtbnMgPSBnZW5lcmF0ZUNvbHVtbnMoMTApXG5jb25zdCBkYXRhID0gcmVmKGdlbmVyYXRlRGF0YShjb2x1bW5zLCAyMDApKVxuXG5jb25zdCB7IHQgfSA9IHVzZUxvY2FsZSgpXG5jb25zdCBzaG91bGRGaWx0ZXIgPSByZWYoZmFsc2UpXG5jb25zdCBwb3BvdmVyUmVmID0gcmVmKClcblxuY29uc3QgYXJpYUxhYmVsID0gY29tcHV0ZWQoKCkgPT4ge1xuICByZXR1cm4gdCgnZWwudGFibGUuZmlsdGVyTGFiZWwnLCB7IGNvbHVtbjogY29sdW1uc1swXS50aXRsZSB9KVxufSlcblxuY29uc3Qgb25GaWx0ZXIgPSAoKSA9PiB7XG4gIHBvcG92ZXJSZWYudmFsdWUuaGlkZSgpXG4gIGlmIChzaG91bGRGaWx0ZXIudmFsdWUpIHtcbiAgICBkYXRhLnZhbHVlID0gZ2VuZXJhdGVEYXRhKGNvbHVtbnMsIDEwMCwgJ2ZpbHRlcmVkLScpXG4gIH0gZWxzZSB7XG4gICAgZGF0YS52YWx1ZSA9IGdlbmVyYXRlRGF0YShjb2x1bW5zLCAyMDApXG4gIH1cbn1cblxuY29uc3Qgb25SZXNldCA9ICgpID0+IHtcbiAgc2hvdWxkRmlsdGVyLnZhbHVlID0gZmFsc2VcbiAgb25GaWx0ZXIoKVxufVxuXG5jb25zdCBoYW5kbGVTaG93UG9wb3ZlciA9ICgpID0+IHtcbiAgY29uc3QgYnV0dG9uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLmVsLXRhYmxlLXYyX19kZW1vLWZpbHRlciBidXR0b24nKVxuICA7KGJ1dHRvbiBhcyBIVE1MRWxlbWVudCk/LmZvY3VzKClcbn1cblxuY29sdW1uc1swXS5oZWFkZXJDZWxsUmVuZGVyZXIgPSAocHJvcHM6IEhlYWRlckNlbGxTbG90UHJvcHMpID0+IHtcbiAgcmV0dXJuIChcbiAgICA8ZGl2IGNsYXNzPVwiZmxleCBpdGVtcy1jZW50ZXIganVzdGlmeS1jZW50ZXJcIj5cbiAgICAgIDxzcGFuIGNsYXNzPVwibXItMiB0ZXh0LXhzXCI+e3Byb3BzLmNvbHVtbi50aXRsZX08L3NwYW4+XG4gICAgICA8RWxQb3BvdmVyXG4gICAgICAgIHJlZj17cG9wb3ZlclJlZn1cbiAgICAgICAgdHJpZ2dlcj1cImNsaWNrXCJcbiAgICAgICAgd2lkdGg9ezIwMH1cbiAgICAgICAgb25BZnRlci1lbnRlcj17aGFuZGxlU2hvd1BvcG92ZXJ9XG4gICAgICA+XG4gICAgICAgIHt7XG4gICAgICAgICAgZGVmYXVsdDogKCkgPT4gKFxuICAgICAgICAgICAgPGRpdiBjbGFzcz1cImZpbHRlci13cmFwcGVyXCI+XG4gICAgICAgICAgICAgIDxkaXYgY2xhc3M9XCJmaWx0ZXItZ3JvdXBcIj5cbiAgICAgICAgICAgICAgICA8RWxDaGVja2JveCB2LW1vZGVsPXtzaG91bGRGaWx0ZXIudmFsdWV9PlxuICAgICAgICAgICAgICAgICAgRmlsdGVyIFRleHRcbiAgICAgICAgICAgICAgICA8L0VsQ2hlY2tib3g+XG4gICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICA8ZGl2IGNsYXNzPVwiZWwtdGFibGUtdjJfX2RlbW8tZmlsdGVyXCI+XG4gICAgICAgICAgICAgICAgPEVsQnV0dG9uIHRleHQgb25DbGljaz17b25GaWx0ZXJ9PlxuICAgICAgICAgICAgICAgICAgQ29uZmlybVxuICAgICAgICAgICAgICAgIDwvRWxCdXR0b24+XG4gICAgICAgICAgICAgICAgPEVsQnV0dG9uIHRleHQgb25DbGljaz17b25SZXNldH0+XG4gICAgICAgICAgICAgICAgICBSZXNldFxuICAgICAgICAgICAgICAgIDwvRWxCdXR0b24+XG4gICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgKSxcbiAgICAgICAgICByZWZlcmVuY2U6ICgpID0+IChcbiAgICAgICAgICAgIDxidXR0b25cbiAgICAgICAgICAgICAgdHlwZT1cImJ1dHRvblwiXG4gICAgICAgICAgICAgIGFyaWEtbGFiZWw9e2FyaWFMYWJlbC52YWx1ZX1cbiAgICAgICAgICAgICAgY2xhc3M9XCJlbC10YWJsZS12Ml9fZGVtby1maWx0ZXItYnRuXCJcbiAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgPEVsSWNvbiBzaXplPXsxNH0+XG4gICAgICAgICAgICAgICAgPEZpbHRlciAvPlxuICAgICAgICAgICAgICA8L0VsSWNvbj5cbiAgICAgICAgICAgIDwvYnV0dG9uPlxuICAgICAgICAgICksXG4gICAgICAgIH19XG4gICAgICA8L0VsUG9wb3Zlcj5cbiAgICA8L2Rpdj5cbiAgKVxufVxuXG5jb25zdCBmaXhlZENvbHVtbnMgPSBjb2x1bW5zLm1hcCgoY29sdW1uLCBjb2x1bW5JbmRleCkgPT4ge1xuICBsZXQgZml4ZWQ6IFRhYmxlVjJGaXhlZERpciB8IHVuZGVmaW5lZCA9IHVuZGVmaW5lZFxuICBpZiAoY29sdW1uSW5kZXggPCAyKSBmaXhlZCA9IFRhYmxlVjJGaXhlZERpci5MRUZUXG4gIGlmIChjb2x1bW5JbmRleCA+IDkpIGZpeGVkID0gVGFibGVWMkZpeGVkRGlyLlJJR0hUXG4gIHJldHVybiB7IC4uLmNvbHVtbiwgZml4ZWQsIHdpZHRoOiAxMDAgfVxufSlcbjwvc2NyaXB0PlxuXG48c3R5bGU+XG4uZWwtdGFibGUtdjJfX2RlbW8tZmlsdGVyIHtcbiAgYm9yZGVyLXRvcDogdmFyKC0tZWwtYm9yZGVyKTtcbiAgbWFyZ2luOiAxMnB4IC0xMnB4IC0xMnB4O1xuICBwYWRkaW5nOiAwIDEycHg7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGp1c3RpZnktY29udGVudDogc3BhY2UtYmV0d2Vlbjtcbn1cbi5lbC10YWJsZS12Ml9fZGVtby1maWx0ZXItYnRuIHtcbiAgZGlzcGxheTogZmxleDtcbiAgY3Vyc29yOiBwb2ludGVyO1xuICBwYWRkaW5nOiAwO1xuICBtYXJnaW46IDA7XG4gIGJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50O1xuICBhcHBlYXJhbmNlOiBub25lO1xuICBib3JkZXI6IG5vbmU7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/filter.vue)_

vue

```
<template>
  <el-table-v2
    fixed
    :columns="fixedColumns"
    :data="data"
    :width="700"
    :height="400"
  />
</template>

<script lang="tsx" setup>
import { computed, ref } from 'vue'
import {
  ElButton,
  ElCheckbox,
  ElIcon,
  ElPopover,
  TableV2FixedDir,
  useLocale,
} from 'element-plus'
import { Filter } from '@element-plus/icons-vue'

import type { HeaderCellSlotProps } from 'element-plus'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })
const columns = generateColumns(10)
const data = ref(generateData(columns, 200))

const { t } = useLocale()
const shouldFilter = ref(false)
const popoverRef = ref()

const ariaLabel = computed(() => {
  return t('el.table.filterLabel', { column: columns[0].title })
})

const onFilter = () => {
  popoverRef.value.hide()
  if (shouldFilter.value) {
    data.value = generateData(columns, 100, 'filtered-')
  } else {
    data.value = generateData(columns, 200)
  }
}

const onReset = () => {
  shouldFilter.value = false
  onFilter()
}

const handleShowPopover = () => {
  const button = document.querySelector('.el-table-v2__demo-filter button')
  ;(button as HTMLElement)?.focus()
}

columns[0].headerCellRenderer = (props: HeaderCellSlotProps) => {
  return (
    <div class="flex items-center justify-center">
      <span class="mr-2 text-xs">{props.column.title}</span>
      <ElPopover
        ref={popoverRef}
        trigger="click"
        width={200}
        onAfter-enter={handleShowPopover}
      >
        {{
          default: () => (
            <div class="filter-wrapper">
              <div class="filter-group">
                <ElCheckbox v-model={shouldFilter.value}>
                  Filter Text
                </ElCheckbox>
              </div>
              <div class="el-table-v2__demo-filter">
                <ElButton text onClick={onFilter}>
                  Confirm
                </ElButton>
                <ElButton text onClick={onReset}>
                  Reset
                </ElButton>
              </div>
            </div>
          ),
          reference: () => (
            <button
              type="button"
              aria-label={ariaLabel.value}
              class="el-table-v2__demo-filter-btn"
            >
              <ElIcon size={14}>
                <Filter />
              </ElIcon>
            </button>
          ),
        }}
      </ElPopover>
    </div>
  )
}

const fixedColumns = columns.map((column, columnIndex) => {
  let fixed: TableV2FixedDir | undefined = undefined
  if (columnIndex < 2) fixed = TableV2FixedDir.LEFT
  if (columnIndex > 9) fixed = TableV2FixedDir.RIGHT
  return { ...column, fixed, width: 100 }
})
</script>

<style>
.el-table-v2__demo-filter {
  border-top: var(--el-border);
  margin: 12px -12px -12px;
  padding: 0 12px;
  display: flex;
  justify-content: space-between;
}
.el-table-v2__demo-filter-btn {
  display: flex;
  cursor: pointer;
  padding: 0;
  margin: 0;
  background-color: transparent;
  appearance: none;
  border: none;
}
</style>
```

隐藏源代码

## 可排序表格 [​](#可排序表格)

您可以使用排序状态来对表格进行排序。

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOnNvcnQtYnk9XCJzb3J0U3RhdGVcIlxuICAgIDp3aWR0aD1cIjcwMFwiXG4gICAgOmhlaWdodD1cIjQwMFwiXG4gICAgZml4ZWRcbiAgICBAY29sdW1uLXNvcnQ9XCJvblNvcnRcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IFRhYmxlVjJTb3J0T3JkZXIgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmltcG9ydCB0eXBlIHsgU29ydEJ5IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBnZW5lcmF0ZUNvbHVtbnMgPSAobGVuZ3RoID0gMTAsIHByZWZpeCA9ICdjb2x1bW4tJywgcHJvcHM/OiBhbnkpID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCBjb2x1bW5JbmRleCkgPT4gKHtcbiAgICAuLi5wcm9wcyxcbiAgICBrZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgZGF0YUtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICB0aXRsZTogYENvbHVtbiAke2NvbHVtbkluZGV4fWAsXG4gICAgd2lkdGg6IDE1MCxcbiAgfSkpXG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9IChcbiAgY29sdW1uczogUmV0dXJuVHlwZTx0eXBlb2YgZ2VuZXJhdGVDb2x1bW5zPixcbiAgbGVuZ3RoID0gMjAwLFxuICBwcmVmaXggPSAncm93LSdcbikgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIHJvd0luZGV4KSA9PiB7XG4gICAgcmV0dXJuIGNvbHVtbnMucmVkdWNlKFxuICAgICAgKHJvd0RhdGEsIGNvbHVtbiwgY29sdW1uSW5kZXgpID0+IHtcbiAgICAgICAgcm93RGF0YVtjb2x1bW4uZGF0YUtleV0gPSBgUm93ICR7cm93SW5kZXh9IC0gQ29sICR7Y29sdW1uSW5kZXh9YFxuICAgICAgICByZXR1cm4gcm93RGF0YVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IGAke3ByZWZpeH0ke3Jvd0luZGV4fWAsXG4gICAgICAgIHBhcmVudElkOiBudWxsLFxuICAgICAgfVxuICAgIClcbiAgfSlcblxuY29uc3QgY29sdW1ucyA9IGdlbmVyYXRlQ29sdW1ucygxMClcbmxldCBkYXRhID0gZ2VuZXJhdGVEYXRhKGNvbHVtbnMsIDIwMClcblxuY29sdW1uc1swXS5zb3J0YWJsZSA9IHRydWVcblxuY29uc3Qgc29ydFN0YXRlID0gcmVmPFNvcnRCeT4oe1xuICBrZXk6ICdjb2x1bW4tMCcsXG4gIG9yZGVyOiBUYWJsZVYyU29ydE9yZGVyLkFTQyxcbn0pXG5cbmNvbnN0IG9uU29ydCA9IChzb3J0Qnk6IFNvcnRCeSkgPT4ge1xuICBjb25zb2xlLmxvZyhzb3J0QnkpXG4gIGRhdGEgPSBkYXRhLnJldmVyc2UoKVxuICBzb3J0U3RhdGUudmFsdWUgPSBzb3J0Qnlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/sort.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :sort-by="sortState"
    :width="700"
    :height="400"
    fixed
    @column-sort="onSort"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { TableV2SortOrder } from 'element-plus'

import type { SortBy } from 'element-plus'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
let data = generateData(columns, 200)

columns[0].sortable = true

const sortState = ref<SortBy>({
  key: 'column-0',
  order: TableV2SortOrder.ASC,
})

const onSort = (sortBy: SortBy) => {
  console.log(sortBy)
  data = data.reverse()
  sortState.value = sortBy
}
</script>
```

隐藏源代码

## 受控的排序 [​](#受控的排序)

您可以在需要时定义多个可排序的列。 请记住，当您在定义了多个可排序的列时， UI 可能会显得有些奇怪，因为用户不知道哪一列被排序。

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICB2LW1vZGVsOnNvcnQtc3RhdGU9XCJzb3J0U3RhdGVcIlxuICAgIDpjb2x1bW5zPVwiY29sdW1uc1wiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgICA6d2lkdGg9XCI3MDBcIlxuICAgIDpoZWlnaHQ9XCI0MDBcIlxuICAgIGZpeGVkXG4gICAgQGNvbHVtbi1zb3J0PVwib25Tb3J0XCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBUYWJsZVYyU29ydE9yZGVyIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbXBvcnQgdHlwZSB7IFNvcnRCeSwgU29ydFN0YXRlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBnZW5lcmF0ZUNvbHVtbnMgPSAobGVuZ3RoID0gMTAsIHByZWZpeCA9ICdjb2x1bW4tJywgcHJvcHM/OiBhbnkpID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCBjb2x1bW5JbmRleCkgPT4gKHtcbiAgICAuLi5wcm9wcyxcbiAgICBrZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgZGF0YUtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICB0aXRsZTogYENvbHVtbiAke2NvbHVtbkluZGV4fWAsXG4gICAgd2lkdGg6IDE1MCxcbiAgfSkpXG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9IChcbiAgY29sdW1uczogUmV0dXJuVHlwZTx0eXBlb2YgZ2VuZXJhdGVDb2x1bW5zPixcbiAgbGVuZ3RoID0gMjAwLFxuICBwcmVmaXggPSAncm93LSdcbikgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIHJvd0luZGV4KSA9PiB7XG4gICAgcmV0dXJuIGNvbHVtbnMucmVkdWNlKFxuICAgICAgKHJvd0RhdGEsIGNvbHVtbiwgY29sdW1uSW5kZXgpID0+IHtcbiAgICAgICAgcm93RGF0YVtjb2x1bW4uZGF0YUtleV0gPSBgUm93ICR7cm93SW5kZXh9IC0gQ29sICR7Y29sdW1uSW5kZXh9YFxuICAgICAgICByZXR1cm4gcm93RGF0YVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IGAke3ByZWZpeH0ke3Jvd0luZGV4fWAsXG4gICAgICAgIHBhcmVudElkOiBudWxsLFxuICAgICAgfVxuICAgIClcbiAgfSlcblxuY29uc3QgY29sdW1ucyA9IGdlbmVyYXRlQ29sdW1ucygxMClcbmNvbnN0IGRhdGEgPSByZWYoZ2VuZXJhdGVEYXRhKGNvbHVtbnMsIDIwMCkpXG5cbmNvbHVtbnNbMF0uc29ydGFibGUgPSB0cnVlXG5jb2x1bW5zWzFdLnNvcnRhYmxlID0gdHJ1ZVxuXG5jb25zdCBzb3J0U3RhdGUgPSByZWY8U29ydFN0YXRlPih7XG4gICdjb2x1bW4tMCc6IFRhYmxlVjJTb3J0T3JkZXIuREVTQyxcbiAgJ2NvbHVtbi0xJzogVGFibGVWMlNvcnRPcmRlci5BU0MsXG59KVxuXG5jb25zdCBvblNvcnQgPSAoeyBrZXksIG9yZGVyIH06IFNvcnRCeSkgPT4ge1xuICBzb3J0U3RhdGUudmFsdWVba2V5XSA9IG9yZGVyXG4gIGRhdGEudmFsdWUgPSBkYXRhLnZhbHVlLnJldmVyc2UoKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/controlled-sort.vue)_

vue

```
<template>
  <el-table-v2
    v-model:sort-state="sortState"
    :columns="columns"
    :data="data"
    :width="700"
    :height="400"
    fixed
    @column-sort="onSort"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { TableV2SortOrder } from 'element-plus'

import type { SortBy, SortState } from 'element-plus'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = ref(generateData(columns, 200))

columns[0].sortable = true
columns[1].sortable = true

const sortState = ref<SortState>({
  'column-0': TableV2SortOrder.DESC,
  'column-1': TableV2SortOrder.ASC,
})

const onSort = ({ key, order }: SortBy) => {
  sortState.value[key] = order
  data.value = data.value.reverse()
}
</script>
```

隐藏源代码

## 高亮显示鼠标悬停单元格 [​](#高亮显示鼠标悬停单元格)

当处理一个大的列表时，很容易丢失当前行的轨迹和您正在访问的一列。 在这种情况下，使用这个功能可能很有帮助。

1

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 0 - Col 10

2

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 1 - Col 10

3

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 2 - Col 10

4

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 3 - Col 10

5

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 4 - Col 10

6

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 5 - Col 10

7

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 6 - Col 10

8

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 7 - Col 10

9

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Row 8 - Col 10

Row No.

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwiaGVpZ2h0OiA0MDBweFwiPlxuICAgIDxlbC1hdXRvLXJlc2l6ZXI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJ7IGhlaWdodCwgd2lkdGggfVwiPlxuICAgICAgICA8ZWwtdGFibGUtdjJcbiAgICAgICAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgICAgICAgIDpjZWxsLXByb3BzPVwiY2VsbFByb3BzXCJcbiAgICAgICAgICA6Y2xhc3M9XCJrbHNcIlxuICAgICAgICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgICAgICAgOndpZHRoPVwid2lkdGhcIlxuICAgICAgICAgIDpoZWlnaHQ9XCJoZWlnaHRcIlxuICAgICAgICAvPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWF1dG8tcmVzaXplcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBnZW5lcmF0ZUNvbHVtbnMgPSAobGVuZ3RoID0gMTAsIHByZWZpeCA9ICdjb2x1bW4tJywgcHJvcHM/OiBhbnkpID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCBjb2x1bW5JbmRleCkgPT4gKHtcbiAgICAuLi5wcm9wcyxcbiAgICBrZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgZGF0YUtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICB0aXRsZTogYENvbHVtbiAke2NvbHVtbkluZGV4fWAsXG4gICAgd2lkdGg6IDE1MCxcbiAgfSkpXG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9IChcbiAgY29sdW1uczogUmV0dXJuVHlwZTx0eXBlb2YgZ2VuZXJhdGVDb2x1bW5zPixcbiAgbGVuZ3RoID0gMjAwLFxuICBwcmVmaXggPSAncm93LSdcbikgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIHJvd0luZGV4KSA9PiB7XG4gICAgcmV0dXJuIGNvbHVtbnMucmVkdWNlKFxuICAgICAgKHJvd0RhdGEsIGNvbHVtbiwgY29sdW1uSW5kZXgpID0+IHtcbiAgICAgICAgcm93RGF0YVtjb2x1bW4uZGF0YUtleV0gPSBgUm93ICR7cm93SW5kZXh9IC0gQ29sICR7Y29sdW1uSW5kZXh9YFxuICAgICAgICByZXR1cm4gcm93RGF0YVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IGAke3ByZWZpeH0ke3Jvd0luZGV4fWAsXG4gICAgICAgIHBhcmVudElkOiBudWxsLFxuICAgICAgfVxuICAgIClcbiAgfSlcblxuY29uc3QgY29sdW1ucyA9IGdlbmVyYXRlQ29sdW1ucygxMClcbmNvbHVtbnMudW5zaGlmdCh7XG4gIGtleTogJ2NvbHVtbi1uLTEnLFxuICB3aWR0aDogNTAsXG4gIHRpdGxlOiAnUm93IE5vLicsXG4gIGNlbGxSZW5kZXJlcjogKHsgcm93SW5kZXggfSkgPT4gYCR7cm93SW5kZXggKyAxfWAsXG4gIGFsaWduOiAnY2VudGVyJyxcbn0pXG5jb25zdCBkYXRhID0gZ2VuZXJhdGVEYXRhKGNvbHVtbnMsIDIwMClcblxuY29uc3QgY2VsbFByb3BzID0gKHsgY29sdW1uSW5kZXggfSkgPT4ge1xuICBjb25zdCBrZXkgPSBgaG92ZXJpbmctY29sLSR7Y29sdW1uSW5kZXh9YFxuICByZXR1cm4ge1xuICAgIFsnZGF0YS1rZXknXToga2V5LFxuICAgIG9uTW91c2VlbnRlcjogKCkgPT4ge1xuICAgICAga2xzLnZhbHVlID0ga2V5XG4gICAgfSxcbiAgICBvbk1vdXNlbGVhdmU6ICgpID0+IHtcbiAgICAgIGtscy52YWx1ZSA9ICcnXG4gICAgfSxcbiAgfVxufVxuXG5jb25zdCBrbHMgPSByZWY8c3RyaW5nPignJylcbjwvc2NyaXB0PlxuXG48c3R5bGU+XG4uaG92ZXJpbmctY29sLTAgW2RhdGEta2V5PSdob3ZlcmluZy1jb2wtMCddLFxuLmhvdmVyaW5nLWNvbC0xIFtkYXRhLWtleT0naG92ZXJpbmctY29sLTEnXSxcbi5ob3ZlcmluZy1jb2wtMiBbZGF0YS1rZXk9J2hvdmVyaW5nLWNvbC0yJ10sXG4uaG92ZXJpbmctY29sLTMgW2RhdGEta2V5PSdob3ZlcmluZy1jb2wtMyddLFxuLmhvdmVyaW5nLWNvbC00IFtkYXRhLWtleT0naG92ZXJpbmctY29sLTQnXSxcbi5ob3ZlcmluZy1jb2wtNSBbZGF0YS1rZXk9J2hvdmVyaW5nLWNvbC01J10sXG4uaG92ZXJpbmctY29sLTYgW2RhdGEta2V5PSdob3ZlcmluZy1jb2wtNiddLFxuLmhvdmVyaW5nLWNvbC03IFtkYXRhLWtleT0naG92ZXJpbmctY29sLTcnXSxcbi5ob3ZlcmluZy1jb2wtOCBbZGF0YS1rZXk9J2hvdmVyaW5nLWNvbC04J10sXG4uaG92ZXJpbmctY29sLTkgW2RhdGEta2V5PSdob3ZlcmluZy1jb2wtOSddLFxuLmhvdmVyaW5nLWNvbC0xMCBbZGF0YS1rZXk9J2hvdmVyaW5nLWNvbC0xMCddIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tZWwtdGFibGUtcm93LWhvdmVyLWJnLWNvbG9yKTtcbn1cblxuW2RhdGEta2V5PSdob3ZlcmluZy1jb2wtMCddIHtcbiAgZm9udC13ZWlnaHQ6IGJvbGQ7XG4gIHVzZXItc2VsZWN0OiBub25lO1xuICBwb2ludGVyLWV2ZW50czogbm9uZTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/cross-hovering.vue)_

vue

```
<template>
  <div style="height: 400px">
    <el-auto-resizer>
      <template #default="{ height, width }">
        <el-table-v2
          :columns="columns"
          :cell-props="cellProps"
          :class="kls"
          :data="data"
          :width="width"
          :height="height"
        />
      </template>
    </el-auto-resizer>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
columns.unshift({
  key: 'column-n-1',
  width: 50,
  title: 'Row No.',
  cellRenderer: ({ rowIndex }) => `${rowIndex + 1}`,
  align: 'center',
})
const data = generateData(columns, 200)

const cellProps = ({ columnIndex }) => {
  const key = `hovering-col-${columnIndex}`
  return {
    ['data-key']: key,
    onMouseenter: () => {
      kls.value = key
    },
    onMouseleave: () => {
      kls.value = ''
    },
  }
}

const kls = ref<string>('')
</script>

<style>
.hovering-col-0 [data-key='hovering-col-0'],
.hovering-col-1 [data-key='hovering-col-1'],
.hovering-col-2 [data-key='hovering-col-2'],
.hovering-col-3 [data-key='hovering-col-3'],
.hovering-col-4 [data-key='hovering-col-4'],
.hovering-col-5 [data-key='hovering-col-5'],
.hovering-col-6 [data-key='hovering-col-6'],
.hovering-col-7 [data-key='hovering-col-7'],
.hovering-col-8 [data-key='hovering-col-8'],
.hovering-col-9 [data-key='hovering-col-9'],
.hovering-col-10 [data-key='hovering-col-10'] {
  background: var(--el-table-row-hover-bg-color);
}

[data-key='hovering-col-0'] {
  font-weight: bold;
  user-select: none;
  pointer-events: none;
}
</style>
```

隐藏源代码

## 横跨列 [​](#横跨列)

虚拟化表格没有使用内置的 `table` 元素，故 `colspan` 和 `rowspan` 与 [TableV1](https://element-plus.org/zh-CN/component/table) 比较略有不同。 然而，通过定制的行渲染器，这些功能仍然可以实现。 在本节中，我们将演示如何实现这一点。

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjIgZml4ZWQgOmNvbHVtbnM9XCJjb2x1bW5zXCIgOmRhdGE9XCJkYXRhXCIgOndpZHRoPVwiNzAwXCIgOmhlaWdodD1cIjQwMFwiPlxuICAgIDx0ZW1wbGF0ZSAjcm93PVwicHJvcHNcIj5cbiAgICAgIDxSb3cgdi1iaW5kPVwicHJvcHNcIiAvPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtdGFibGUtdjI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgY2xvbmVWTm9kZSB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgZ2VuZXJhdGVDb2x1bW5zID0gKGxlbmd0aCA9IDEwLCBwcmVmaXggPSAnY29sdW1uLScsIHByb3BzPzogYW55KSA9PlxuICBBcnJheS5mcm9tKHsgbGVuZ3RoIH0pLm1hcCgoXywgY29sdW1uSW5kZXgpID0+ICh7XG4gICAgLi4ucHJvcHMsXG4gICAga2V5OiBgJHtwcmVmaXh9JHtjb2x1bW5JbmRleH1gLFxuICAgIGRhdGFLZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgdGl0bGU6IGBDb2x1bW4gJHtjb2x1bW5JbmRleH1gLFxuICAgIHdpZHRoOiAxNTAsXG4gIH0pKVxuXG5jb25zdCBnZW5lcmF0ZURhdGEgPSAoXG4gIGNvbHVtbnM6IFJldHVyblR5cGU8dHlwZW9mIGdlbmVyYXRlQ29sdW1ucz4sXG4gIGxlbmd0aCA9IDIwMCxcbiAgcHJlZml4ID0gJ3Jvdy0nXG4pID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCByb3dJbmRleCkgPT4ge1xuICAgIHJldHVybiBjb2x1bW5zLnJlZHVjZShcbiAgICAgIChyb3dEYXRhLCBjb2x1bW4sIGNvbHVtbkluZGV4KSA9PiB7XG4gICAgICAgIHJvd0RhdGFbY29sdW1uLmRhdGFLZXldID0gYFJvdyAke3Jvd0luZGV4fSAtIENvbCAke2NvbHVtbkluZGV4fWBcbiAgICAgICAgcmV0dXJuIHJvd0RhdGFcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiBgJHtwcmVmaXh9JHtyb3dJbmRleH1gLFxuICAgICAgICBwYXJlbnRJZDogbnVsbCxcbiAgICAgIH1cbiAgICApXG4gIH0pXG5cbmNvbnN0IGNvbHVtbnMgPSBnZW5lcmF0ZUNvbHVtbnMoMTApXG5jb25zdCBkYXRhID0gZ2VuZXJhdGVEYXRhKGNvbHVtbnMsIDIwMClcblxuY29uc3QgY29sU3BhbkluZGV4ID0gMVxuY29sdW1uc1tjb2xTcGFuSW5kZXhdLmNvbFNwYW4gPSAoeyByb3dJbmRleCB9KSA9PiAocm93SW5kZXggJSA0KSArIDFcbmNvbHVtbnNbY29sU3BhbkluZGV4XS5hbGlnbiA9ICdjZW50ZXInXG5cbmNvbnN0IFJvdyA9ICh7IHJvd0RhdGEsIHJvd0luZGV4LCBjZWxscywgY29sdW1ucyB9KSA9PiB7XG4gIGNvbnN0IGNvbFNwYW4gPSBjb2x1bW5zW2NvbFNwYW5JbmRleF0uY29sU3Bhbih7IHJvd0RhdGEsIHJvd0luZGV4IH0pXG4gIGlmIChjb2xTcGFuID4gMSkge1xuICAgIGxldCB3aWR0aCA9IE51bWJlci5wYXJzZUludChjZWxsc1tjb2xTcGFuSW5kZXhdLnByb3BzLnN0eWxlLndpZHRoKVxuICAgIGZvciAobGV0IGkgPSAxOyBpIDwgY29sU3BhbjsgaSsrKSB7XG4gICAgICB3aWR0aCArPSBOdW1iZXIucGFyc2VJbnQoY2VsbHNbY29sU3BhbkluZGV4ICsgaV0ucHJvcHMuc3R5bGUud2lkdGgpXG4gICAgICBjZWxsc1tjb2xTcGFuSW5kZXggKyBpXSA9IG51bGxcbiAgICB9XG4gICAgY29uc3Qgc3R5bGUgPSB7XG4gICAgICAuLi5jZWxsc1tjb2xTcGFuSW5kZXhdLnByb3BzLnN0eWxlLFxuICAgICAgd2lkdGg6IGAke3dpZHRofXB4YCxcbiAgICAgIGJhY2tncm91bmRDb2xvcjogJ3ZhcigtLWVsLWNvbG9yLXByaW1hcnktbGlnaHQtMyknLFxuICAgIH1cbiAgICBjZWxsc1tjb2xTcGFuSW5kZXhdID0gY2xvbmVWTm9kZShjZWxsc1tjb2xTcGFuSW5kZXhdLCB7IHN0eWxlIH0pXG4gIH1cblxuICByZXR1cm4gY2VsbHNcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/colspan.vue)_

vue

```
<template>
  <el-table-v2 fixed :columns="columns" :data="data" :width="700" :height="400">
    <template #row="props">
      <Row v-bind="props" />
    </template>
  </el-table-v2>
</template>

<script lang="ts" setup>
import { cloneVNode } from 'vue'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = generateData(columns, 200)

const colSpanIndex = 1
columns[colSpanIndex].colSpan = ({ rowIndex }) => (rowIndex % 4) + 1
columns[colSpanIndex].align = 'center'

const Row = ({ rowData, rowIndex, cells, columns }) => {
  const colSpan = columns[colSpanIndex].colSpan({ rowData, rowIndex })
  if (colSpan > 1) {
    let width = Number.parseInt(cells[colSpanIndex].props.style.width)
    for (let i = 1; i < colSpan; i++) {
      width += Number.parseInt(cells[colSpanIndex + i].props.style.width)
      cells[colSpanIndex + i] = null
    }
    const style = {
      ...cells[colSpanIndex].props.style,
      width: `${width}px`,
      backgroundColor: 'var(--el-color-primary-light-3)',
    }
    cells[colSpanIndex] = cloneVNode(cells[colSpanIndex], { style })
  }

  return cells
}
</script>
```

隐藏源代码

## 纵跨行 [​](#纵跨行)

既然我们已经提到了 [Colspan](#colspan)，那跨行（row span）也是没有问题的。 它与colspan略有不同，但是基本原理是一样的。

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjIgZml4ZWQgOmNvbHVtbnM9XCJjb2x1bW5zXCIgOmRhdGE9XCJkYXRhXCIgOndpZHRoPVwiNzAwXCIgOmhlaWdodD1cIjQwMFwiPlxuICAgIDx0ZW1wbGF0ZSAjcm93PVwicHJvcHNcIj5cbiAgICAgIDxSb3cgdi1iaW5kPVwicHJvcHNcIiAvPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtdGFibGUtdjI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgY2xvbmVWTm9kZSB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgZ2VuZXJhdGVDb2x1bW5zID0gKGxlbmd0aCA9IDEwLCBwcmVmaXggPSAnY29sdW1uLScsIHByb3BzPzogYW55KSA9PlxuICBBcnJheS5mcm9tKHsgbGVuZ3RoIH0pLm1hcCgoXywgY29sdW1uSW5kZXgpID0+ICh7XG4gICAgLi4ucHJvcHMsXG4gICAga2V5OiBgJHtwcmVmaXh9JHtjb2x1bW5JbmRleH1gLFxuICAgIGRhdGFLZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgdGl0bGU6IGBDb2x1bW4gJHtjb2x1bW5JbmRleH1gLFxuICAgIHdpZHRoOiAxNTAsXG4gIH0pKVxuXG5jb25zdCBnZW5lcmF0ZURhdGEgPSAoXG4gIGNvbHVtbnM6IFJldHVyblR5cGU8dHlwZW9mIGdlbmVyYXRlQ29sdW1ucz4sXG4gIGxlbmd0aCA9IDIwMCxcbiAgcHJlZml4ID0gJ3Jvdy0nXG4pID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCByb3dJbmRleCkgPT4ge1xuICAgIHJldHVybiBjb2x1bW5zLnJlZHVjZShcbiAgICAgIChyb3dEYXRhLCBjb2x1bW4sIGNvbHVtbkluZGV4KSA9PiB7XG4gICAgICAgIHJvd0RhdGFbY29sdW1uLmRhdGFLZXldID0gYFJvdyAke3Jvd0luZGV4fSAtIENvbCAke2NvbHVtbkluZGV4fWBcbiAgICAgICAgcmV0dXJuIHJvd0RhdGFcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiBgJHtwcmVmaXh9JHtyb3dJbmRleH1gLFxuICAgICAgICBwYXJlbnRJZDogbnVsbCxcbiAgICAgIH1cbiAgICApXG4gIH0pXG5cbmNvbnN0IGNvbHVtbnMgPSBnZW5lcmF0ZUNvbHVtbnMoMTApXG5jb25zdCBkYXRhID0gZ2VuZXJhdGVEYXRhKGNvbHVtbnMsIDIwMClcblxuY29uc3Qgcm93U3BhbkluZGV4ID0gMFxuY29sdW1uc1tyb3dTcGFuSW5kZXhdLnJvd1NwYW4gPSAoeyByb3dJbmRleCB9KSA9PlxuICByb3dJbmRleCAlIDIgPT09IDAgJiYgcm93SW5kZXggPD0gZGF0YS5sZW5ndGggLSAyID8gMiA6IDFcblxuY29uc3QgUm93ID0gKHsgcm93RGF0YSwgcm93SW5kZXgsIGNlbGxzLCBjb2x1bW5zIH0pID0+IHtcbiAgY29uc3Qgcm93U3BhbiA9IGNvbHVtbnNbcm93U3BhbkluZGV4XS5yb3dTcGFuKHsgcm93RGF0YSwgcm93SW5kZXggfSlcbiAgaWYgKHJvd1NwYW4gPiAxKSB7XG4gICAgY29uc3QgY2VsbCA9IGNlbGxzW3Jvd1NwYW5JbmRleF1cbiAgICBjb25zdCBzdHlsZSA9IHtcbiAgICAgIC4uLmNlbGwucHJvcHMuc3R5bGUsXG4gICAgICBiYWNrZ3JvdW5kQ29sb3I6ICd2YXIoLS1lbC1jb2xvci1wcmltYXJ5LWxpZ2h0LTMpJyxcbiAgICAgIGhlaWdodDogYCR7cm93U3BhbiAqIDUwIC0gMX1weGAsXG4gICAgICBhbGlnblNlbGY6ICdmbGV4LXN0YXJ0JyxcbiAgICAgIHpJbmRleDogMSxcbiAgICB9XG4gICAgY2VsbHNbcm93U3BhbkluZGV4XSA9IGNsb25lVk5vZGUoY2VsbCwgeyBzdHlsZSB9KVxuICB9XG4gIHJldHVybiBjZWxsc1xufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/rowspan.vue)_

vue

```
<template>
  <el-table-v2 fixed :columns="columns" :data="data" :width="700" :height="400">
    <template #row="props">
      <Row v-bind="props" />
    </template>
  </el-table-v2>
</template>

<script lang="ts" setup>
import { cloneVNode } from 'vue'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = generateData(columns, 200)

const rowSpanIndex = 0
columns[rowSpanIndex].rowSpan = ({ rowIndex }) =>
  rowIndex % 2 === 0 && rowIndex <= data.length - 2 ? 2 : 1

const Row = ({ rowData, rowIndex, cells, columns }) => {
  const rowSpan = columns[rowSpanIndex].rowSpan({ rowData, rowIndex })
  if (rowSpan > 1) {
    const cell = cells[rowSpanIndex]
    const style = {
      ...cell.props.style,
      backgroundColor: 'var(--el-color-primary-light-3)',
      height: `${rowSpan * 50 - 1}px`,
      alignSelf: 'flex-start',
      zIndex: 1,
    }
    cells[rowSpanIndex] = cloneVNode(cell, { style })
  }
  return cells
}
</script>
```

隐藏源代码

## 同时跨行和跨列 [​](#同时跨行和跨列)

我们当然可以同时使用横跨列与纵跨行来满足您的业务需求！

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 1

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 1

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 1

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 1

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjIgZml4ZWQgOmNvbHVtbnM9XCJjb2x1bW5zXCIgOmRhdGE9XCJkYXRhXCIgOndpZHRoPVwiNzAwXCIgOmhlaWdodD1cIjQwMFwiPlxuICAgIDx0ZW1wbGF0ZSAjcm93PVwicHJvcHNcIj5cbiAgICAgIDxSb3cgdi1iaW5kPVwicHJvcHNcIiAvPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtdGFibGUtdjI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c3hcIiBzZXR1cD5cbmltcG9ydCB7IGNsb25lVk5vZGUgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGdlbmVyYXRlQ29sdW1ucyA9IChsZW5ndGggPSAxMCwgcHJlZml4ID0gJ2NvbHVtbi0nLCBwcm9wcz86IGFueSkgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIGNvbHVtbkluZGV4KSA9PiAoe1xuICAgIC4uLnByb3BzLFxuICAgIGtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICBkYXRhS2V5OiBgJHtwcmVmaXh9JHtjb2x1bW5JbmRleH1gLFxuICAgIHRpdGxlOiBgQ29sdW1uICR7Y29sdW1uSW5kZXh9YCxcbiAgICB3aWR0aDogMTUwLFxuICB9KSlcblxuY29uc3QgZ2VuZXJhdGVEYXRhID0gKFxuICBjb2x1bW5zOiBSZXR1cm5UeXBlPHR5cGVvZiBnZW5lcmF0ZUNvbHVtbnM+LFxuICBsZW5ndGggPSAyMDAsXG4gIHByZWZpeCA9ICdyb3ctJ1xuKSA9PlxuICBBcnJheS5mcm9tKHsgbGVuZ3RoIH0pLm1hcCgoXywgcm93SW5kZXgpID0+IHtcbiAgICByZXR1cm4gY29sdW1ucy5yZWR1Y2UoXG4gICAgICAocm93RGF0YSwgY29sdW1uLCBjb2x1bW5JbmRleCkgPT4ge1xuICAgICAgICByb3dEYXRhW2NvbHVtbi5kYXRhS2V5XSA9IGBSb3cgJHtyb3dJbmRleH0gLSBDb2wgJHtjb2x1bW5JbmRleH1gXG4gICAgICAgIHJldHVybiByb3dEYXRhXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogYCR7cHJlZml4fSR7cm93SW5kZXh9YCxcbiAgICAgICAgcGFyZW50SWQ6IG51bGwsXG4gICAgICB9XG4gICAgKVxuICB9KVxuXG5jb25zdCBjb2x1bW5zID0gZ2VuZXJhdGVDb2x1bW5zKDEwKVxuY29uc3QgZGF0YSA9IGdlbmVyYXRlRGF0YShjb2x1bW5zLCAyMDApXG5cbmNvbnN0IGNvbFNwYW5JbmRleCA9IDFcbmNvbHVtbnNbY29sU3BhbkluZGV4XS5jb2xTcGFuID0gKHsgcm93SW5kZXggfSkgPT4gKHJvd0luZGV4ICUgNCkgKyAxXG5jb2x1bW5zW2NvbFNwYW5JbmRleF0uYWxpZ24gPSAnY2VudGVyJ1xuXG5jb25zdCByb3dTcGFuSW5kZXggPSAwXG5jb2x1bW5zW3Jvd1NwYW5JbmRleF0ucm93U3BhbiA9ICh7IHJvd0luZGV4IH0pID0+XG4gIHJvd0luZGV4ICUgMiA9PT0gMCAmJiByb3dJbmRleCA8PSBkYXRhLmxlbmd0aCAtIDIgPyAyIDogMVxuXG5jb25zdCBSb3cgPSAoeyByb3dEYXRhLCByb3dJbmRleCwgY2VsbHMsIGNvbHVtbnMgfSkgPT4ge1xuICBjb25zdCBjb2xTcGFuID0gY29sdW1uc1tjb2xTcGFuSW5kZXhdLmNvbFNwYW4oeyByb3dEYXRhLCByb3dJbmRleCB9KVxuICBpZiAoY29sU3BhbiA+IDEpIHtcbiAgICBsZXQgd2lkdGggPSBOdW1iZXIucGFyc2VJbnQoY2VsbHNbY29sU3BhbkluZGV4XS5wcm9wcy5zdHlsZS53aWR0aClcbiAgICBmb3IgKGxldCBpID0gMTsgaSA8IGNvbFNwYW47IGkrKykge1xuICAgICAgd2lkdGggKz0gTnVtYmVyLnBhcnNlSW50KGNlbGxzW2NvbFNwYW5JbmRleCArIGldLnByb3BzLnN0eWxlLndpZHRoKVxuICAgICAgY2VsbHNbY29sU3BhbkluZGV4ICsgaV0gPSBudWxsXG4gICAgfVxuICAgIGNvbnN0IHN0eWxlID0ge1xuICAgICAgLi4uY2VsbHNbY29sU3BhbkluZGV4XS5wcm9wcy5zdHlsZSxcbiAgICAgIHdpZHRoOiBgJHt3aWR0aH1weGAsXG4gICAgICBiYWNrZ3JvdW5kQ29sb3I6ICd2YXIoLS1lbC1jb2xvci1wcmltYXJ5LWxpZ2h0LTMpJyxcbiAgICB9XG4gICAgY2VsbHNbY29sU3BhbkluZGV4XSA9IGNsb25lVk5vZGUoY2VsbHNbY29sU3BhbkluZGV4XSwgeyBzdHlsZSB9KVxuICB9XG5cbiAgY29uc3Qgcm93U3BhbiA9IGNvbHVtbnNbcm93U3BhbkluZGV4XS5yb3dTcGFuKHsgcm93RGF0YSwgcm93SW5kZXggfSlcbiAgaWYgKHJvd1NwYW4gPiAxKSB7XG4gICAgY29uc3QgY2VsbCA9IGNlbGxzW3Jvd1NwYW5JbmRleF1cbiAgICBjb25zdCBzdHlsZSA9IHtcbiAgICAgIC4uLmNlbGwucHJvcHMuc3R5bGUsXG4gICAgICBiYWNrZ3JvdW5kQ29sb3I6ICd2YXIoLS1lbC1jb2xvci1kYW5nZXItbGlnaHQtMyknLFxuICAgICAgaGVpZ2h0OiBgJHtyb3dTcGFuICogNTB9cHhgLFxuICAgICAgYWxpZ25TZWxmOiAnZmxleC1zdGFydCcsXG4gICAgICB6SW5kZXg6IDEsXG4gICAgfVxuICAgIGNlbGxzW3Jvd1NwYW5JbmRleF0gPSBjbG9uZVZOb2RlKGNlbGwsIHsgc3R5bGUgfSlcbiAgfSBlbHNlIHtcbiAgICBjb25zdCBzdHlsZSA9IGNlbGxzW3Jvd1NwYW5JbmRleF0ucHJvcHMuc3R5bGVcbiAgICAvLyBvdmVycmlkZSB0aGUgY2VsbCBoZXJlIGZvciBjcmVhdGluZyBhIHB1cmUgbm9kZSB3aXRob3V0IHBvbGx1dGUgdGhlIHN0eWxlXG4gICAgY2VsbHNbcm93U3BhbkluZGV4XSA9IChcbiAgICAgIDxkaXYgc3R5bGU9e3sgLi4uc3R5bGUsIHdpZHRoOiBgJHtzdHlsZS53aWR0aH1weGAgfX0gLz5cbiAgICApXG4gIH1cbiAgcmV0dXJuIGNlbGxzXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/spans.vue)_

vue

```
<template>
  <el-table-v2 fixed :columns="columns" :data="data" :width="700" :height="400">
    <template #row="props">
      <Row v-bind="props" />
    </template>
  </el-table-v2>
</template>

<script lang="tsx" setup>
import { cloneVNode } from 'vue'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = generateData(columns, 200)

const colSpanIndex = 1
columns[colSpanIndex].colSpan = ({ rowIndex }) => (rowIndex % 4) + 1
columns[colSpanIndex].align = 'center'

const rowSpanIndex = 0
columns[rowSpanIndex].rowSpan = ({ rowIndex }) =>
  rowIndex % 2 === 0 && rowIndex <= data.length - 2 ? 2 : 1

const Row = ({ rowData, rowIndex, cells, columns }) => {
  const colSpan = columns[colSpanIndex].colSpan({ rowData, rowIndex })
  if (colSpan > 1) {
    let width = Number.parseInt(cells[colSpanIndex].props.style.width)
    for (let i = 1; i < colSpan; i++) {
      width += Number.parseInt(cells[colSpanIndex + i].props.style.width)
      cells[colSpanIndex + i] = null
    }
    const style = {
      ...cells[colSpanIndex].props.style,
      width: `${width}px`,
      backgroundColor: 'var(--el-color-primary-light-3)',
    }
    cells[colSpanIndex] = cloneVNode(cells[colSpanIndex], { style })
  }

  const rowSpan = columns[rowSpanIndex].rowSpan({ rowData, rowIndex })
  if (rowSpan > 1) {
    const cell = cells[rowSpanIndex]
    const style = {
      ...cell.props.style,
      backgroundColor: 'var(--el-color-danger-light-3)',
      height: `${rowSpan * 50}px`,
      alignSelf: 'flex-start',
      zIndex: 1,
    }
    cells[rowSpanIndex] = cloneVNode(cell, { style })
  } else {
    const style = cells[rowSpanIndex].props.style
    // override the cell here for creating a pure node without pollute the style
    cells[rowSpanIndex] = (
      <div style={{ ...style, width: `${style.width}px` }} />
    )
  }
  return cells
}
</script>
```

隐藏源代码

## 树形数据 [​](#树形数据)

虚拟表也可以在树状结构中呈现数据。 点击箭头图标，你可以展开或折叠树节点。

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Row 0 - Col 0

Row 0 - Col 1

Row 1 - Col 0

Row 1 - Col 1

Row 2 - Col 0

Row 2 - Col 1

Row 3 - Col 0

Row 3 - Col 1

Row 4 - Col 0

Row 4 - Col 1

Row 5 - Col 0

Row 5 - Col 1

Row 6 - Col 0

Row 6 - Col 1

Row 7 - Col 0

Row 7 - Col 1

Row 8 - Col 0

Row 8 - Col 1

Column 0

Column 1

Row 0 - Col 9

Row 1 - Col 9

Row 2 - Col 9

Row 3 - Col 9

Row 4 - Col 9

Row 5 - Col 9

Row 6 - Col 9

Row 7 - Col 9

Row 8 - Col 9

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICB2LW1vZGVsOmV4cGFuZGVkLXJvdy1rZXlzPVwiZXhwYW5kZWRSb3dLZXlzXCJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwidHJlZURhdGFcIlxuICAgIDp3aWR0aD1cIjcwMFwiXG4gICAgOmV4cGFuZC1jb2x1bW4ta2V5PVwiZXhwYW5kQ29sdW1uS2V5XCJcbiAgICA6aGVpZ2h0PVwiNDAwXCJcbiAgICBmaXhlZFxuICAgIEByb3ctZXhwYW5kPVwib25Sb3dFeHBhbmRlZFwiXG4gICAgQGV4cGFuZGVkLXJvd3MtY2hhbmdlPVwib25FeHBhbmRlZFJvd3NDaGFuZ2VcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGNvbXB1dGVkLCByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBUYWJsZVYyRml4ZWREaXIgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmltcG9ydCB0eXBlIHsgRXhwYW5kZWRSb3dzQ2hhbmdlSGFuZGxlciwgUm93RXhwYW5kSGFuZGxlciB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgZ2VuZXJhdGVDb2x1bW5zID0gKGxlbmd0aCA9IDEwLCBwcmVmaXggPSAnY29sdW1uLScsIHByb3BzPzogYW55KSA9PlxuICBBcnJheS5mcm9tKHsgbGVuZ3RoIH0pLm1hcCgoXywgY29sdW1uSW5kZXgpID0+ICh7XG4gICAgLi4ucHJvcHMsXG4gICAga2V5OiBgJHtwcmVmaXh9JHtjb2x1bW5JbmRleH1gLFxuICAgIGRhdGFLZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgdGl0bGU6IGBDb2x1bW4gJHtjb2x1bW5JbmRleH1gLFxuICAgIHdpZHRoOiAxNTAsXG4gIH0pKVxuXG5jb25zdCBnZW5lcmF0ZURhdGEgPSAoXG4gIGNvbHVtbnM6IFJldHVyblR5cGU8dHlwZW9mIGdlbmVyYXRlQ29sdW1ucz4sXG4gIGxlbmd0aCA9IDIwMCxcbiAgcHJlZml4ID0gJ3Jvdy0nXG4pID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCByb3dJbmRleCkgPT4ge1xuICAgIHJldHVybiBjb2x1bW5zLnJlZHVjZShcbiAgICAgIChyb3dEYXRhLCBjb2x1bW4sIGNvbHVtbkluZGV4KSA9PiB7XG4gICAgICAgIHJvd0RhdGFbY29sdW1uLmRhdGFLZXldID0gYFJvdyAke3Jvd0luZGV4fSAtIENvbCAke2NvbHVtbkluZGV4fWBcbiAgICAgICAgcmV0dXJuIHJvd0RhdGFcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiBgJHtwcmVmaXh9JHtyb3dJbmRleH1gLFxuICAgICAgICBwYXJlbnRJZDogbnVsbCxcbiAgICAgIH1cbiAgICApXG4gIH0pXG5cbmNvbnN0IGNvbHVtbnMgPSBnZW5lcmF0ZUNvbHVtbnMoMTApLm1hcCgoY29sdW1uLCBjb2x1bW5JbmRleCkgPT4ge1xuICBsZXQgZml4ZWQhOiBUYWJsZVYyRml4ZWREaXJcbiAgaWYgKGNvbHVtbkluZGV4IDwgMikgZml4ZWQgPSBUYWJsZVYyRml4ZWREaXIuTEVGVFxuICBpZiAoY29sdW1uSW5kZXggPiA4KSBmaXhlZCA9IFRhYmxlVjJGaXhlZERpci5SSUdIVFxuICByZXR1cm4geyAuLi5jb2x1bW4sIGZpeGVkIH1cbn0pXG5cbmNvbnN0IGRhdGEgPSBnZW5lcmF0ZURhdGEoY29sdW1ucywgMjAwKVxuXG5jb25zdCBleHBhbmRDb2x1bW5LZXkgPSAnY29sdW1uLTAnXG5cbi8vIGFkZCBzb21lIHN1YiBpdGVtc1xuZm9yIChsZXQgaSA9IDA7IGkgPCA1MDsgaSsrKSB7XG4gIGRhdGEucHVzaChcbiAgICB7XG4gICAgICAuLi5kYXRhWzBdLFxuICAgICAgaWQ6IGAke2RhdGFbMF0uaWR9LXN1Yi0ke2l9YCxcbiAgICAgIHBhcmVudElkOiBkYXRhWzBdLmlkLFxuICAgICAgW2V4cGFuZENvbHVtbktleV06IGBTdWIgJHtpfWAsXG4gICAgfSxcbiAgICB7XG4gICAgICAuLi5kYXRhWzJdLFxuICAgICAgaWQ6IGAke2RhdGFbMl0uaWR9LXN1Yi0ke2l9YCxcbiAgICAgIHBhcmVudElkOiBkYXRhWzJdLmlkLFxuICAgICAgW2V4cGFuZENvbHVtbktleV06IGBTdWIgJHtpfWAsXG4gICAgfSxcbiAgICB7XG4gICAgICAuLi5kYXRhWzJdLFxuICAgICAgaWQ6IGAke2RhdGFbMl0uaWR9LXN1Yi1zdWItJHtpfWAsXG4gICAgICBwYXJlbnRJZDogYCR7ZGF0YVsyXS5pZH0tc3ViLSR7aX1gLFxuICAgICAgW2V4cGFuZENvbHVtbktleV06IGBTdWItU3ViICR7aX1gLFxuICAgIH1cbiAgKVxufVxuXG5mdW5jdGlvbiB1bmZsYXR0ZW4oXG4gIGRhdGE6IFJldHVyblR5cGU8dHlwZW9mIGdlbmVyYXRlRGF0YT4sXG4gIHJvb3RJZCA9IG51bGwsXG4gIGRhdGFLZXkgPSAnaWQnLFxuICBwYXJlbnRLZXkgPSAncGFyZW50SWQnXG4pIHtcbiAgY29uc3QgdHJlZTogYW55W10gPSBbXVxuICBjb25zdCBjaGlsZHJlbk1hcCA9IHt9XG5cbiAgZm9yIChjb25zdCBkYXR1bSBvZiBkYXRhKSB7XG4gICAgY29uc3QgaXRlbSA9IHsgLi4uZGF0dW0gfVxuICAgIGNvbnN0IGlkID0gaXRlbVtkYXRhS2V5XVxuICAgIGNvbnN0IHBhcmVudElkID0gaXRlbVtwYXJlbnRLZXldXG5cbiAgICBpZiAoQXJyYXkuaXNBcnJheShpdGVtLmNoaWxkcmVuKSkge1xuICAgICAgY2hpbGRyZW5NYXBbaWRdID0gaXRlbS5jaGlsZHJlbi5jb25jYXQoY2hpbGRyZW5NYXBbaWRdIHx8IFtdKVxuICAgIH0gZWxzZSBpZiAoIWNoaWxkcmVuTWFwW2lkXSkge1xuICAgICAgY2hpbGRyZW5NYXBbaWRdID0gW11cbiAgICB9XG4gICAgaXRlbS5jaGlsZHJlbiA9IGNoaWxkcmVuTWFwW2lkXVxuXG4gICAgaWYgKHBhcmVudElkICE9PSB1bmRlZmluZWQgJiYgcGFyZW50SWQgIT09IHJvb3RJZCkge1xuICAgICAgaWYgKCFjaGlsZHJlbk1hcFtwYXJlbnRJZF0pIGNoaWxkcmVuTWFwW3BhcmVudElkXSA9IFtdXG4gICAgICBjaGlsZHJlbk1hcFtwYXJlbnRJZF0ucHVzaChpdGVtKVxuICAgIH0gZWxzZSB7XG4gICAgICB0cmVlLnB1c2goaXRlbSlcbiAgICB9XG4gIH1cblxuICByZXR1cm4gdHJlZVxufVxuXG5jb25zdCB0cmVlRGF0YSA9IGNvbXB1dGVkKCgpID0+IHVuZmxhdHRlbihkYXRhKSlcblxuY29uc3QgZXhwYW5kZWRSb3dLZXlzID0gcmVmPHN0cmluZ1tdPihbXSlcblxuY29uc3Qgb25Sb3dFeHBhbmRlZCA9ICh7IGV4cGFuZGVkIH06IFBhcmFtZXRlcnM8Um93RXhwYW5kSGFuZGxlcj5bMF0pID0+IHtcbiAgY29uc29sZS5sb2coJ0V4cGFuZGVkOicsIGV4cGFuZGVkKVxufVxuXG5jb25zdCBvbkV4cGFuZGVkUm93c0NoYW5nZSA9IChcbiAgZXhwYW5kZWRLZXlzOiBQYXJhbWV0ZXJzPEV4cGFuZGVkUm93c0NoYW5nZUhhbmRsZXI+WzBdXG4pID0+IHtcbiAgY29uc29sZS5sb2coZXhwYW5kZWRLZXlzKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/tree-data.vue)_

vue

```
<template>
  <el-table-v2
    v-model:expanded-row-keys="expandedRowKeys"
    :columns="columns"
    :data="treeData"
    :width="700"
    :expand-column-key="expandColumnKey"
    :height="400"
    fixed
    @row-expand="onRowExpanded"
    @expanded-rows-change="onExpandedRowsChange"
  />
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { TableV2FixedDir } from 'element-plus'

import type { ExpandedRowsChangeHandler, RowExpandHandler } from 'element-plus'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10).map((column, columnIndex) => {
  let fixed!: TableV2FixedDir
  if (columnIndex < 2) fixed = TableV2FixedDir.LEFT
  if (columnIndex > 8) fixed = TableV2FixedDir.RIGHT
  return { ...column, fixed }
})

const data = generateData(columns, 200)

const expandColumnKey = 'column-0'

// add some sub items
for (let i = 0; i < 50; i++) {
  data.push(
    {
      ...data[0],
      id: `${data[0].id}-sub-${i}`,
      parentId: data[0].id,
      [expandColumnKey]: `Sub ${i}`,
    },
    {
      ...data[2],
      id: `${data[2].id}-sub-${i}`,
      parentId: data[2].id,
      [expandColumnKey]: `Sub ${i}`,
    },
    {
      ...data[2],
      id: `${data[2].id}-sub-sub-${i}`,
      parentId: `${data[2].id}-sub-${i}`,
      [expandColumnKey]: `Sub-Sub ${i}`,
    }
  )
}

function unflatten(
  data: ReturnType<typeof generateData>,
  rootId = null,
  dataKey = 'id',
  parentKey = 'parentId'
) {
  const tree: any[] = []
  const childrenMap = {}

  for (const datum of data) {
    const item = { ...datum }
    const id = item[dataKey]
    const parentId = item[parentKey]

    if (Array.isArray(item.children)) {
      childrenMap[id] = item.children.concat(childrenMap[id] || [])
    } else if (!childrenMap[id]) {
      childrenMap[id] = []
    }
    item.children = childrenMap[id]

    if (parentId !== undefined && parentId !== rootId) {
      if (!childrenMap[parentId]) childrenMap[parentId] = []
      childrenMap[parentId].push(item)
    } else {
      tree.push(item)
    }
  }

  return tree
}

const treeData = computed(() => unflatten(data))

const expandedRowKeys = ref<string[]>([])

const onRowExpanded = ({ expanded }: Parameters<RowExpandHandler>[0]) => {
  console.log('Expanded:', expanded)
}

const onExpandedRowsChange = (
  expandedKeys: Parameters<ExpandedRowsChangeHandler>[0]
) => {
  console.log(expandedKeys)
}
</script>
```

隐藏源代码

## 动态高度行 [​](#动态高度行)

虚拟表能够呈现具有动态高度的行数。 如果您正在处理数据并不确定内容大小， 此功能对于调整到内容高度的渲染行是理想的。 要启用此功能，请传递 `estimated-row-height` 属性。 估计高度越接近实际内容，渲染体验就越顺。

TIP

每行高度在渲染过程中动态测量。 因此，如果您试图显示大量数据， UI **可能会** 抖动。

Tom

Eius optio fugiat.

EditDelete

Tom

Corrupti doloremque a quos vero delectus consequatur.

EditDelete

Tom

Eius optio fugiat.

EditDelete

Name

Description

Operations

random-200

random-199

random-198

random-197

random-196

random-195

random-194

random-193

random-192

random-191

random-190

Id

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOnNvcnQtYnk9XCJzb3J0XCJcbiAgICA6ZXN0aW1hdGVkLXJvdy1oZWlnaHQ9XCI0MFwiXG4gICAgOndpZHRoPVwiNzAwXCJcbiAgICA6aGVpZ2h0PVwiNDAwXCJcbiAgICBmaXhlZFxuICAgIEBjb2x1bW4tc29ydD1cIm9uQ29sdW1uU29ydFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c3hcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7XG4gIEVsQnV0dG9uLFxuICBFbFRhZyxcbiAgVGFibGVWMkZpeGVkRGlyLFxuICBUYWJsZVYyU29ydE9yZGVyLFxufSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmltcG9ydCB0eXBlIHsgQ29sdW1uLCBTb3J0QnkgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGxvbmdUZXh0ID1cbiAgJ1F1YWVyYXQgaXBzYW0gbmVjZXNzaXRhdGlidXMgZXVtIHF1aWJ1c2RhbSBlc3QgaWQgdm9sdXB0YXRlbSBjdW1xdWUgbW9sbGl0aWEuJ1xuY29uc3QgbWlkVGV4dCA9ICdDb3JydXB0aSBkb2xvcmVtcXVlIGEgcXVvcyB2ZXJvIGRlbGVjdHVzIGNvbnNlcXVhdHVyLidcbmNvbnN0IHNob3J0VGV4dCA9ICdFaXVzIG9wdGlvIGZ1Z2lhdC4nXG5cbmNvbnN0IHRleHRMaXN0ID0gW3Nob3J0VGV4dCwgbWlkVGV4dCwgbG9uZ1RleHRdXG5cbi8vIGdlbmVyYXRlIHJhbmRvbSBudW1iZXIgaW4gcmFuZ2UgMCB0byAyXG5cbmxldCBpZCA9IDBcblxuY29uc3QgZGF0YUdlbmVyYXRvciA9ICgpID0+ICh7XG4gIGlkOiBgcmFuZG9tLSR7KytpZH1gLFxuICBuYW1lOiAnVG9tJyxcbiAgZGF0ZTogJzIwMTYtMDUtMDMnLFxuICBkZXNjcmlwdGlvbjogdGV4dExpc3RbTWF0aC5mbG9vcihNYXRoLnJhbmRvbSgpICogMyldLFxufSlcblxuY29uc3QgY29sdW1uczogQ29sdW1uPGFueT5bXSA9IFtcbiAge1xuICAgIGtleTogJ2lkJyxcbiAgICB0aXRsZTogJ0lkJyxcbiAgICBkYXRhS2V5OiAnaWQnLFxuICAgIHdpZHRoOiAxNTAsXG4gICAgc29ydGFibGU6IHRydWUsXG4gICAgZml4ZWQ6IFRhYmxlVjJGaXhlZERpci5MRUZULFxuICB9LFxuICB7XG4gICAga2V5OiAnbmFtZScsXG4gICAgdGl0bGU6ICdOYW1lJyxcbiAgICBkYXRhS2V5OiAnbmFtZScsXG4gICAgd2lkdGg6IDE1MCxcbiAgICBhbGlnbjogJ2NlbnRlcicsXG4gICAgY2VsbFJlbmRlcmVyOiAoeyBjZWxsRGF0YTogbmFtZSB9KSA9PiA8RWxUYWc+e25hbWV9PC9FbFRhZz4sXG4gIH0sXG4gIHtcbiAgICBrZXk6ICdkZXNjcmlwdGlvbicsXG4gICAgdGl0bGU6ICdEZXNjcmlwdGlvbicsXG4gICAgZGF0YUtleTogJ2Rlc2NyaXB0aW9uJyxcbiAgICB3aWR0aDogMTUwLFxuICAgIGNlbGxSZW5kZXJlcjogKHsgY2VsbERhdGE6IGRlc2NyaXB0aW9uIH0pID0+IChcbiAgICAgIDxkaXYgc3R5bGU9XCJwYWRkaW5nOiAxMHB4IDA7XCI+e2Rlc2NyaXB0aW9ufTwvZGl2PlxuICAgICksXG4gIH0sXG4gIHtcbiAgICBrZXk6ICdvcGVyYXRpb25zJyxcbiAgICB0aXRsZTogJ09wZXJhdGlvbnMnLFxuICAgIGNlbGxSZW5kZXJlcjogKCkgPT4gKFxuICAgICAgPD5cbiAgICAgICAgPEVsQnV0dG9uIHNpemU9XCJzbWFsbFwiPkVkaXQ8L0VsQnV0dG9uPlxuICAgICAgICA8RWxCdXR0b24gc2l6ZT1cInNtYWxsXCIgdHlwZT1cImRhbmdlclwiPlxuICAgICAgICAgIERlbGV0ZVxuICAgICAgICA8L0VsQnV0dG9uPlxuICAgICAgPC8+XG4gICAgKSxcbiAgICB3aWR0aDogMTUwLFxuICAgIGFsaWduOiAnY2VudGVyJyxcbiAgfSxcbl1cbmNvbnN0IGRhdGEgPSByZWYoXG4gIEFycmF5LmZyb20oeyBsZW5ndGg6IDIwMCB9KVxuICAgIC5tYXAoZGF0YUdlbmVyYXRvcilcbiAgICAuc29ydCgoYSwgYikgPT4gKGEubmFtZSA+IGIubmFtZSA/IDEgOiAtMSkpXG4pXG5cbmNvbnN0IHNvcnQgPSByZWY8U29ydEJ5Pih7IGtleTogJ25hbWUnLCBvcmRlcjogVGFibGVWMlNvcnRPcmRlci5BU0MgfSlcblxuY29uc3Qgb25Db2x1bW5Tb3J0ID0gKHNvcnRCeTogU29ydEJ5KSA9PiB7XG4gIGNvbnN0IG9yZGVyID0gc29ydEJ5Lm9yZGVyID09PSAnYXNjJyA/IDEgOiAtMVxuICBjb25zdCBkYXRhQ2xvbmUgPSBbLi4uZGF0YS52YWx1ZV1cbiAgZGF0YUNsb25lLnNvcnQoKGEsIGIpID0+IChhW3NvcnRCeS5rZXldID4gYltzb3J0Qnkua2V5XSA/IG9yZGVyIDogLW9yZGVyKSlcbiAgc29ydC52YWx1ZSA9IHNvcnRCeVxuICBkYXRhLnZhbHVlID0gZGF0YUNsb25lXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/dynamic-height.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :sort-by="sort"
    :estimated-row-height="40"
    :width="700"
    :height="400"
    fixed
    @column-sort="onColumnSort"
  />
</template>

<script lang="tsx" setup>
import { ref } from 'vue'
import {
  ElButton,
  ElTag,
  TableV2FixedDir,
  TableV2SortOrder,
} from 'element-plus'

import type { Column, SortBy } from 'element-plus'

const longText =
  'Quaerat ipsam necessitatibus eum quibusdam est id voluptatem cumque mollitia.'
const midText = 'Corrupti doloremque a quos vero delectus consequatur.'
const shortText = 'Eius optio fugiat.'

const textList = [shortText, midText, longText]

// generate random number in range 0 to 2

let id = 0

const dataGenerator = () => ({
  id: `random-${++id}`,
  name: 'Tom',
  date: '2016-05-03',
  description: textList[Math.floor(Math.random() * 3)],
})

const columns: Column<any>[] = [
  {
    key: 'id',
    title: 'Id',
    dataKey: 'id',
    width: 150,
    sortable: true,
    fixed: TableV2FixedDir.LEFT,
  },
  {
    key: 'name',
    title: 'Name',
    dataKey: 'name',
    width: 150,
    align: 'center',
    cellRenderer: ({ cellData: name }) => <ElTag>{name}</ElTag>,
  },
  {
    key: 'description',
    title: 'Description',
    dataKey: 'description',
    width: 150,
    cellRenderer: ({ cellData: description }) => (
      <div style="padding: 10px 0;">{description}</div>
    ),
  },
  {
    key: 'operations',
    title: 'Operations',
    cellRenderer: () => (
      <>
        <ElButton size="small">Edit</ElButton>
        <ElButton size="small" type="danger">
          Delete
        </ElButton>
      </>
    ),
    width: 150,
    align: 'center',
  },
]
const data = ref(
  Array.from({ length: 200 })
    .map(dataGenerator)
    .sort((a, b) => (a.name > b.name ? 1 : -1))
)

const sort = ref<SortBy>({ key: 'name', order: TableV2SortOrder.ASC })

const onColumnSort = (sortBy: SortBy) => {
  const order = sortBy.order === 'asc' ? 1 : -1
  const dataClone = [...data.value]
  dataClone.sort((a, b) => (a[sortBy.key] > b[sortBy.key] ? order : -order))
  sort.value = sortBy
  data.value = dataClone
}
</script>
```

隐藏源代码

## 可展开的附加信息 [​](#可展开的附加信息)

使用动态高度渲染，您也可以在表格中显示详细的视图。

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOmVzdGltYXRlZC1yb3ctaGVpZ2h0PVwiNTBcIlxuICAgIDpleHBhbmQtY29sdW1uLWtleT1cImNvbHVtbnNbMF0ua2V5XCJcbiAgICA6d2lkdGg9XCI3MDBcIlxuICAgIDpoZWlnaHQ9XCI0MDBcIlxuICA+XG4gICAgPHRlbXBsYXRlICNyb3c9XCJwcm9wc1wiPlxuICAgICAgPFJvdyB2LWJpbmQ9XCJwcm9wc1wiIC8+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC10YWJsZS12Mj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzeFwiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBkZXRhaWxlZFRleHQgPSBgVmVsaXQgc2VkIGFzcGVybmF0dXIgdGVtcG9yYS4gTmF0dXMgY29uc2VxdWF0dXIgb2ZmaWNpaXMgZGljdGEgdmVsIGFzc3VtZW5kYS5cbkl0YXF1ZSBlc3QgdGVtcG9yaWJ1cyBtaW51cyBxdWlzLiBJcHN1bSBjb21tb2RpYWIgcG9ycm8gdmVsIHZvbHVwdGFzIGlsbHVtLlxuUXVpIHF1YW0gbnVsbGEgZXQgZG9sb3JlIGF1dGVtIGl0YXF1ZSBlc3QuXG5JZCBjb25zZXF1YXR1ciBpcHN1bSBlYSBmdWdhIGV0IG9kaXQgZWxpZ2VuZGkgaW1wZWRpdC5cbk1haW9yZXMgb2ZmaWNpaXMgb2NjYWVjYXRpIGV0IG1hZ25hbSBldCBzYXBpZW50ZSBlc3QgdmVsaXQgc3VudC5cbk5vbiBldCB0ZW1wb3JlIHRlbXBvcmlidXMuIEV4Y2VwdHVyaSBldCBxdW9zLiBNaW51cyBkaXN0aW5jdGlvIGF1dC5cblZvbHVwdGF0ZW0gZWEgZXhjZXB0dXJpIG9tbmlzIHZlbC4gTm9uIGFwZXJpYW0gc2l0IHNlZCBsYWJvcmlvc2FtIGVhcXVlIG9tbmlzIGRlbGVuaXRpLlxuRXN0IG1vbGVzdGlhZSBvbW5pcyBub24gZXQgbnVsbGEgcmVwdWRpYW5kYWUgZnVnYSBzaXQuYFxuXG5jb25zdCBnZW5lcmF0ZUNvbHVtbnMgPSAobGVuZ3RoID0gMTAsIHByZWZpeCA9ICdjb2x1bW4tJywgcHJvcHM/OiBhbnkpID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCBjb2x1bW5JbmRleCkgPT4gKHtcbiAgICAuLi5wcm9wcyxcbiAgICBrZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgZGF0YUtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICB0aXRsZTogYENvbHVtbiAke2NvbHVtbkluZGV4fWAsXG4gICAgd2lkdGg6IDE1MCxcbiAgfSkpXG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9IChcbiAgY29sdW1uczogUmV0dXJuVHlwZTx0eXBlb2YgZ2VuZXJhdGVDb2x1bW5zPixcbiAgbGVuZ3RoID0gMjAwLFxuICBwcmVmaXggPSAncm93LSdcbikgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIHJvd0luZGV4KSA9PiB7XG4gICAgcmV0dXJuIGNvbHVtbnMucmVkdWNlKFxuICAgICAgKHJvd0RhdGEsIGNvbHVtbiwgY29sdW1uSW5kZXgpID0+IHtcbiAgICAgICAgcm93RGF0YVtjb2x1bW4uZGF0YUtleV0gPSBgUm93ICR7cm93SW5kZXh9IC0gQ29sICR7Y29sdW1uSW5kZXh9YFxuICAgICAgICByZXR1cm4gcm93RGF0YVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IGAke3ByZWZpeH0ke3Jvd0luZGV4fWAsXG4gICAgICAgIHBhcmVudElkOiBudWxsLFxuICAgICAgfVxuICAgIClcbiAgfSlcblxuY29uc3QgY29sdW1ucyA9IGdlbmVyYXRlQ29sdW1ucygxMClcbmNvbnN0IGRhdGEgPSByZWYoXG4gIGdlbmVyYXRlRGF0YShjb2x1bW5zLCAyMDApLm1hcCgoZGF0YSkgPT4ge1xuICAgIGRhdGEuY2hpbGRyZW4gPSBbXG4gICAgICB7XG4gICAgICAgIGlkOiBgJHtkYXRhLmlkfS1kZXRhaWwtY29udGVudGAsXG4gICAgICAgIGRldGFpbDogZGV0YWlsZWRUZXh0LFxuICAgICAgfSxcbiAgICBdXG4gICAgcmV0dXJuIGRhdGFcbiAgfSlcbilcblxuY29uc3QgUm93ID0gKHsgY2VsbHMsIHJvd0RhdGEgfSkgPT4ge1xuICBpZiAocm93RGF0YS5kZXRhaWwpIHJldHVybiA8ZGl2IGNsYXNzPVwicC02XCI+e3Jvd0RhdGEuZGV0YWlsfTwvZGl2PlxuICByZXR1cm4gY2VsbHNcbn1cblxuUm93LmluaGVyaXRBdHRycyA9IGZhbHNlXG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLmVsLXRhYmxlLXYyX19yb3ctZGVwdGgtMCB7XG4gIGhlaWdodDogNTBweDtcbn1cblxuLmVsLXRhYmxlLXYyX19jZWxsLXRleHQge1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICB0ZXh0LW92ZXJmbG93OiBlbGxpcHNpcztcbiAgd2hpdGUtc3BhY2U6IG5vd3JhcDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/detailed-view.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :estimated-row-height="50"
    :expand-column-key="columns[0].key"
    :width="700"
    :height="400"
  >
    <template #row="props">
      <Row v-bind="props" />
    </template>
  </el-table-v2>
</template>

<script lang="tsx" setup>
import { ref } from 'vue'

const detailedText = `Velit sed aspernatur tempora. Natus consequatur officiis dicta vel assumenda.
Itaque est temporibus minus quis. Ipsum commodiab porro vel voluptas illum.
Qui quam nulla et dolore autem itaque est.
Id consequatur ipsum ea fuga et odit eligendi impedit.
Maiores officiis occaecati et magnam et sapiente est velit sunt.
Non et tempore temporibus. Excepturi et quos. Minus distinctio aut.
Voluptatem ea excepturi omnis vel. Non aperiam sit sed laboriosam eaque omnis deleniti.
Est molestiae omnis non et nulla repudiandae fuga sit.`

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = ref(
  generateData(columns, 200).map((data) => {
    data.children = [
      {
        id: `${data.id}-detail-content`,
        detail: detailedText,
      },
    ]
    return data
  })
)

const Row = ({ cells, rowData }) => {
  if (rowData.detail) return <div class="p-6">{rowData.detail}</div>
  return cells
}

Row.inheritAttrs = false
</script>

<style>
.el-table-v2__row-depth-0 {
  height: 50px;
}

.el-table-v2__cell-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
```

隐藏源代码

## 自定义页脚 [​](#自定义页脚)

自定义表格 footer， 通常用来展示一些汇总数据和信息。

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Row 9 - Col 0

Row 9 - Col 1

Row 9 - Col 2

Row 9 - Col 3

Row 9 - Col 4

Row 9 - Col 5

Row 9 - Col 6

Row 9 - Col 7

Row 9 - Col 8

Row 9 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

Display a message in the footer

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOnJvdy1oZWlnaHQ9XCI0MFwiXG4gICAgOndpZHRoPVwiNzAwXCJcbiAgICA6aGVpZ2h0PVwiNDAwXCJcbiAgICA6Zm9vdGVyLWhlaWdodD1cIjUwXCJcbiAgICBmaXhlZFxuICA+XG4gICAgPHRlbXBsYXRlICNmb290ZXJcbiAgICAgID48ZGl2XG4gICAgICAgIGNsYXNzPVwiZmxleCBpdGVtcy1jZW50ZXJcIlxuICAgICAgICBzdHlsZT1cIlxuICAgICAgICAgIGp1c3RpZnktY29udGVudDogY2VudGVyO1xuICAgICAgICAgIGhlaWdodDogMTAwJTtcbiAgICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5LWxpZ2h0LTcpO1xuICAgICAgICBcIlxuICAgICAgPlxuICAgICAgICBEaXNwbGF5IGEgbWVzc2FnZSBpbiB0aGUgZm9vdGVyXG4gICAgICA8L2Rpdj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLXRhYmxlLXYyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IGdlbmVyYXRlQ29sdW1ucyA9IChsZW5ndGggPSAxMCwgcHJlZml4ID0gJ2NvbHVtbi0nLCBwcm9wcz86IGFueSkgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIGNvbHVtbkluZGV4KSA9PiAoe1xuICAgIC4uLnByb3BzLFxuICAgIGtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICBkYXRhS2V5OiBgJHtwcmVmaXh9JHtjb2x1bW5JbmRleH1gLFxuICAgIHRpdGxlOiBgQ29sdW1uICR7Y29sdW1uSW5kZXh9YCxcbiAgICB3aWR0aDogMTUwLFxuICB9KSlcblxuY29uc3QgZ2VuZXJhdGVEYXRhID0gKFxuICBjb2x1bW5zOiBSZXR1cm5UeXBlPHR5cGVvZiBnZW5lcmF0ZUNvbHVtbnM+LFxuICBsZW5ndGggPSAyMDAsXG4gIHByZWZpeCA9ICdyb3ctJ1xuKSA9PlxuICBBcnJheS5mcm9tKHsgbGVuZ3RoIH0pLm1hcCgoXywgcm93SW5kZXgpID0+IHtcbiAgICByZXR1cm4gY29sdW1ucy5yZWR1Y2UoXG4gICAgICAocm93RGF0YSwgY29sdW1uLCBjb2x1bW5JbmRleCkgPT4ge1xuICAgICAgICByb3dEYXRhW2NvbHVtbi5kYXRhS2V5XSA9IGBSb3cgJHtyb3dJbmRleH0gLSBDb2wgJHtjb2x1bW5JbmRleH1gXG4gICAgICAgIHJldHVybiByb3dEYXRhXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBpZDogYCR7cHJlZml4fSR7cm93SW5kZXh9YCxcbiAgICAgICAgcGFyZW50SWQ6IG51bGwsXG4gICAgICB9XG4gICAgKVxuICB9KVxuXG5jb25zdCBjb2x1bW5zID0gZ2VuZXJhdGVDb2x1bW5zKDEwKVxuY29uc3QgZGF0YSA9IGdlbmVyYXRlRGF0YShjb2x1bW5zLCAyMDApXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/footer.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :row-height="40"
    :width="700"
    :height="400"
    :footer-height="50"
    fixed
  >
    <template #footer
      ><div
        class="flex items-center"
        style="
          justify-content: center;
          height: 100%;
          background-color: var(--el-color-primary-light-7);
        "
      >
        Display a message in the footer
      </div>
    </template>
  </el-table-v2>
</template>

<script lang="ts" setup>
const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = generateData(columns, 200)
</script>
```

隐藏源代码

## 自定义空元素渲染器 [​](#自定义空元素渲染器)

渲染自定义的空元素。

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

No Data

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwiW11cIlxuICAgIDpyb3ctaGVpZ2h0PVwiNDBcIlxuICAgIDp3aWR0aD1cIjcwMFwiXG4gICAgOmhlaWdodD1cIjQwMFwiXG4gICAgOmZvb3Rlci1oZWlnaHQ9XCI1MFwiXG4gID5cbiAgICA8dGVtcGxhdGUgI2VtcHR5PlxuICAgICAgPGRpdiBjbGFzcz1cImZsZXggaXRlbXMtY2VudGVyIGp1c3RpZnktY2VudGVyIGgtMTAwJVwiPlxuICAgICAgICA8ZWwtZW1wdHkgLz5cbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtdGFibGUtdjI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c3hcIiBzZXR1cD5cbmNvbnN0IGdlbmVyYXRlQ29sdW1ucyA9IChsZW5ndGggPSAxMCwgcHJlZml4ID0gJ2NvbHVtbi0nLCBwcm9wcz86IGFueSkgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIGNvbHVtbkluZGV4KSA9PiAoe1xuICAgIC4uLnByb3BzLFxuICAgIGtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICBkYXRhS2V5OiBgJHtwcmVmaXh9JHtjb2x1bW5JbmRleH1gLFxuICAgIHRpdGxlOiBgQ29sdW1uICR7Y29sdW1uSW5kZXh9YCxcbiAgICB3aWR0aDogMTUwLFxuICB9KSlcblxuY29uc3QgY29sdW1ucyA9IGdlbmVyYXRlQ29sdW1ucygxMClcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/empty.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="[]"
    :row-height="40"
    :width="700"
    :height="400"
    :footer-height="50"
  >
    <template #empty>
      <div class="flex items-center justify-center h-100%">
        <el-empty />
      </div>
    </template>
  </el-table-v2>
</template>

<script lang="tsx" setup>
const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const columns = generateColumns(10)
</script>
```

隐藏源代码

## 浮动遮罩层 [​](#浮动遮罩层)

当您想要显示加载指示器之类的浮动元素，可以通过渲染一个浮动在表格之上的遮罩层来实现。

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Row 9 - Col 0

Row 9 - Col 1

Row 9 - Col 2

Row 9 - Col 3

Row 9 - Col 4

Row 9 - Col 5

Row 9 - Col 6

Row 9 - Col 7

Row 9 - Col 8

Row 9 - Col 9

Row 10 - Col 0

Row 10 - Col 1

Row 10 - Col 2

Row 10 - Col 3

Row 10 - Col 4

Row 10 - Col 5

Row 10 - Col 6

Row 10 - Col 7

Row 10 - Col 8

Row 10 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUtdjJcbiAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgOnJvdy1oZWlnaHQ9XCI0MFwiXG4gICAgOndpZHRoPVwiNzAwXCJcbiAgICA6aGVpZ2h0PVwiNDAwXCJcbiAgPlxuICAgIDx0ZW1wbGF0ZSAjb3ZlcmxheT5cbiAgICAgIDxkaXZcbiAgICAgICAgY2xhc3M9XCJlbC1sb2FkaW5nLW1hc2tcIlxuICAgICAgICBzdHlsZT1cImRpc3BsYXk6IGZsZXg7IGFsaWduLWl0ZW1zOiBjZW50ZXI7IGp1c3RpZnktY29udGVudDogY2VudGVyXCJcbiAgICAgID5cbiAgICAgICAgPGVsLWljb24gY2xhc3M9XCJpcy1sb2FkaW5nXCIgY29sb3I9XCJ2YXIoLS1lbC1jb2xvci1wcmltYXJ5KVwiIDpzaXplPVwiMjZcIj5cbiAgICAgICAgICA8bG9hZGluZy1pY29uIC8+XG4gICAgICAgIDwvZWwtaWNvbj5cbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtdGFibGUtdjI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgTG9hZGluZyBhcyBMb2FkaW5nSWNvbiB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5jb25zdCBnZW5lcmF0ZUNvbHVtbnMgPSAobGVuZ3RoID0gMTAsIHByZWZpeCA9ICdjb2x1bW4tJywgcHJvcHM/OiBhbnkpID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCBjb2x1bW5JbmRleCkgPT4gKHtcbiAgICAuLi5wcm9wcyxcbiAgICBrZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgZGF0YUtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICB0aXRsZTogYENvbHVtbiAke2NvbHVtbkluZGV4fWAsXG4gICAgd2lkdGg6IDE1MCxcbiAgfSkpXG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9IChcbiAgY29sdW1uczogUmV0dXJuVHlwZTx0eXBlb2YgZ2VuZXJhdGVDb2x1bW5zPixcbiAgbGVuZ3RoID0gMjAwLFxuICBwcmVmaXggPSAncm93LSdcbikgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIHJvd0luZGV4KSA9PiB7XG4gICAgcmV0dXJuIGNvbHVtbnMucmVkdWNlKFxuICAgICAgKHJvd0RhdGEsIGNvbHVtbiwgY29sdW1uSW5kZXgpID0+IHtcbiAgICAgICAgcm93RGF0YVtjb2x1bW4uZGF0YUtleV0gPSBgUm93ICR7cm93SW5kZXh9IC0gQ29sICR7Y29sdW1uSW5kZXh9YFxuICAgICAgICByZXR1cm4gcm93RGF0YVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IGAke3ByZWZpeH0ke3Jvd0luZGV4fWAsXG4gICAgICAgIHBhcmVudElkOiBudWxsLFxuICAgICAgfVxuICAgIClcbiAgfSlcblxuY29uc3QgY29sdW1ucyA9IGdlbmVyYXRlQ29sdW1ucygxMClcbmNvbnN0IGRhdGEgPSBnZW5lcmF0ZURhdGEoY29sdW1ucywgMjAwKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5leGFtcGxlLXNob3djYXNlIC5lbC10YWJsZS12Ml9fb3ZlcmxheSB7XG4gIHotaW5kZXg6IDk7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/overlay.vue)_

vue

```
<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :row-height="40"
    :width="700"
    :height="400"
  >
    <template #overlay>
      <div
        class="el-loading-mask"
        style="display: flex; align-items: center; justify-content: center"
      >
        <el-icon class="is-loading" color="var(--el-color-primary)" :size="26">
          <loading-icon />
        </el-icon>
      </div>
    </template>
  </el-table-v2>
</template>

<script lang="ts" setup>
import { Loading as LoadingIcon } from '@element-plus/icons-vue'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = generateData(columns, 200)
</script>

<style>
.example-showcase .el-table-v2__overlay {
  z-index: 9;
}
</style>
```

隐藏源代码

## 手动滚动 [​](#手动滚动)

使用 Table V2 暴露的方法可以进行手动或编程式的滚动到指定的偏移量或者行。

TIP

`scrollToRow` 的第二个参数代表滚动策略，计算了要滚动的位置，其默认值是 `auto`。 如果你想要滚动到某个特定位置，你可以自己定义战略。 可用的选项是 `"auto" | "center" | "end" | "start" | "smart"`

`smart` 和`auto` 之间的区别是， `auto` 是 `smart` 滚动策略的子集。

Scroll pixels

Scroll rows

Scroll by pixels Scroll by rows

Row 0 - Col 0

Row 0 - Col 1

Row 0 - Col 2

Row 0 - Col 3

Row 0 - Col 4

Row 0 - Col 5

Row 0 - Col 6

Row 0 - Col 7

Row 0 - Col 8

Row 0 - Col 9

Row 1 - Col 0

Row 1 - Col 1

Row 1 - Col 2

Row 1 - Col 3

Row 1 - Col 4

Row 1 - Col 5

Row 1 - Col 6

Row 1 - Col 7

Row 1 - Col 8

Row 1 - Col 9

Row 2 - Col 0

Row 2 - Col 1

Row 2 - Col 2

Row 2 - Col 3

Row 2 - Col 4

Row 2 - Col 5

Row 2 - Col 6

Row 2 - Col 7

Row 2 - Col 8

Row 2 - Col 9

Row 3 - Col 0

Row 3 - Col 1

Row 3 - Col 2

Row 3 - Col 3

Row 3 - Col 4

Row 3 - Col 5

Row 3 - Col 6

Row 3 - Col 7

Row 3 - Col 8

Row 3 - Col 9

Row 4 - Col 0

Row 4 - Col 1

Row 4 - Col 2

Row 4 - Col 3

Row 4 - Col 4

Row 4 - Col 5

Row 4 - Col 6

Row 4 - Col 7

Row 4 - Col 8

Row 4 - Col 9

Row 5 - Col 0

Row 5 - Col 1

Row 5 - Col 2

Row 5 - Col 3

Row 5 - Col 4

Row 5 - Col 5

Row 5 - Col 6

Row 5 - Col 7

Row 5 - Col 8

Row 5 - Col 9

Row 6 - Col 0

Row 6 - Col 1

Row 6 - Col 2

Row 6 - Col 3

Row 6 - Col 4

Row 6 - Col 5

Row 6 - Col 6

Row 6 - Col 7

Row 6 - Col 8

Row 6 - Col 9

Row 7 - Col 0

Row 7 - Col 1

Row 7 - Col 2

Row 7 - Col 3

Row 7 - Col 4

Row 7 - Col 5

Row 7 - Col 6

Row 7 - Col 7

Row 7 - Col 8

Row 7 - Col 9

Row 8 - Col 0

Row 8 - Col 1

Row 8 - Col 2

Row 8 - Col 3

Row 8 - Col 4

Row 8 - Col 5

Row 8 - Col 6

Row 8 - Col 7

Row 8 - Col 8

Row 8 - Col 9

Column 0

Column 1

Column 2

Column 3

Column 4

Column 5

Column 6

Column 7

Column 8

Column 9

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibWItNCBmbGV4IGl0ZW1zLWNlbnRlclwiPlxuICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJTY3JvbGwgcGl4ZWxzXCIgY2xhc3M9XCJtci00XCI+XG4gICAgICA8ZWwtaW5wdXQgdi1tb2RlbD1cInNjcm9sbERlbHRhXCIgLz5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiU2Nyb2xsIHJvd3NcIj5cbiAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwic2Nyb2xsUm93c1wiIC8+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibWItNCBmbGV4IGl0ZW1zLWNlbnRlclwiPlxuICAgIDxlbC1idXR0b24gQGNsaWNrPVwic2Nyb2xsQnlQaXhlbHNcIj4gU2Nyb2xsIGJ5IHBpeGVscyA8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIEBjbGljaz1cInNjcm9sbEJ5Um93c1wiPiBTY3JvbGwgYnkgcm93cyA8L2VsLWJ1dHRvbj5cbiAgPC9kaXY+XG4gIDxkaXYgc3R5bGU9XCJoZWlnaHQ6IDQwMHB4XCI+XG4gICAgPGVsLWF1dG8tcmVzaXplcj5cbiAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD1cInsgaGVpZ2h0LCB3aWR0aCB9XCI+XG4gICAgICAgIDxlbC10YWJsZS12MlxuICAgICAgICAgIHJlZj1cInRhYmxlUmVmXCJcbiAgICAgICAgICA6Y29sdW1ucz1cImNvbHVtbnNcIlxuICAgICAgICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgICAgICAgOndpZHRoPVwid2lkdGhcIlxuICAgICAgICAgIDpoZWlnaHQ9XCJoZWlnaHRcIlxuICAgICAgICAgIGZpeGVkXG4gICAgICAgIC8+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtYXV0by1yZXNpemVyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgVGFibGVWMkluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBnZW5lcmF0ZUNvbHVtbnMgPSAobGVuZ3RoID0gMTAsIHByZWZpeCA9ICdjb2x1bW4tJywgcHJvcHM/OiBhbnkpID0+XG4gIEFycmF5LmZyb20oeyBsZW5ndGggfSkubWFwKChfLCBjb2x1bW5JbmRleCkgPT4gKHtcbiAgICAuLi5wcm9wcyxcbiAgICBrZXk6IGAke3ByZWZpeH0ke2NvbHVtbkluZGV4fWAsXG4gICAgZGF0YUtleTogYCR7cHJlZml4fSR7Y29sdW1uSW5kZXh9YCxcbiAgICB0aXRsZTogYENvbHVtbiAke2NvbHVtbkluZGV4fWAsXG4gICAgd2lkdGg6IDE1MCxcbiAgfSkpXG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9IChcbiAgY29sdW1uczogUmV0dXJuVHlwZTx0eXBlb2YgZ2VuZXJhdGVDb2x1bW5zPixcbiAgbGVuZ3RoID0gMjAwLFxuICBwcmVmaXggPSAncm93LSdcbikgPT5cbiAgQXJyYXkuZnJvbSh7IGxlbmd0aCB9KS5tYXAoKF8sIHJvd0luZGV4KSA9PiB7XG4gICAgcmV0dXJuIGNvbHVtbnMucmVkdWNlKFxuICAgICAgKHJvd0RhdGEsIGNvbHVtbiwgY29sdW1uSW5kZXgpID0+IHtcbiAgICAgICAgcm93RGF0YVtjb2x1bW4uZGF0YUtleV0gPSBgUm93ICR7cm93SW5kZXh9IC0gQ29sICR7Y29sdW1uSW5kZXh9YFxuICAgICAgICByZXR1cm4gcm93RGF0YVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IGAke3ByZWZpeH0ke3Jvd0luZGV4fWAsXG4gICAgICAgIHBhcmVudElkOiBudWxsLFxuICAgICAgfVxuICAgIClcbiAgfSlcblxuY29uc3QgY29sdW1ucyA9IGdlbmVyYXRlQ29sdW1ucygxMClcbmNvbnN0IGRhdGEgPSBnZW5lcmF0ZURhdGEoY29sdW1ucywgMjAwKVxuY29uc3QgdGFibGVSZWYgPSByZWY8VGFibGVWMkluc3RhbmNlPigpXG5jb25zdCBzY3JvbGxEZWx0YSA9IHJlZigyMDApXG5jb25zdCBzY3JvbGxSb3dzID0gcmVmKDEwKVxuXG5mdW5jdGlvbiBzY3JvbGxCeVBpeGVscygpIHtcbiAgdGFibGVSZWYudmFsdWU/LnNjcm9sbFRvVG9wKHNjcm9sbERlbHRhLnZhbHVlKVxufVxuXG5mdW5jdGlvbiBzY3JvbGxCeVJvd3MoKSB7XG4gIHRhYmxlUmVmLnZhbHVlPy5zY3JvbGxUb1JvdyhzY3JvbGxSb3dzLnZhbHVlKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table-v2/manual-scroll.vue)_

vue

```
<template>
  <div class="mb-4 flex items-center">
    <el-form-item label="Scroll pixels" class="mr-4">
      <el-input v-model="scrollDelta" />
    </el-form-item>
    <el-form-item label="Scroll rows">
      <el-input v-model="scrollRows" />
    </el-form-item>
  </div>
  <div class="mb-4 flex items-center">
    <el-button @click="scrollByPixels"> Scroll by pixels </el-button>
    <el-button @click="scrollByRows"> Scroll by rows </el-button>
  </div>
  <div style="height: 400px">
    <el-auto-resizer>
      <template #default="{ height, width }">
        <el-table-v2
          ref="tableRef"
          :columns="columns"
          :data="data"
          :width="width"
          :height="height"
          fixed
        />
      </template>
    </el-auto-resizer>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TableV2Instance } from 'element-plus'

const generateColumns = (length = 10, prefix = 'column-', props?: any) =>
  Array.from({ length }).map((_, columnIndex) => ({
    ...props,
    key: `${prefix}${columnIndex}`,
    dataKey: `${prefix}${columnIndex}`,
    title: `Column ${columnIndex}`,
    width: 150,
  }))

const generateData = (
  columns: ReturnType<typeof generateColumns>,
  length = 200,
  prefix = 'row-'
) =>
  Array.from({ length }).map((_, rowIndex) => {
    return columns.reduce(
      (rowData, column, columnIndex) => {
        rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
        return rowData
      },
      {
        id: `${prefix}${rowIndex}`,
        parentId: null,
      }
    )
  })

const columns = generateColumns(10)
const data = generateData(columns, 200)
const tableRef = ref<TableV2Instance>()
const scrollDelta = ref(200)
const scrollRows = ref(10)

function scrollByPixels() {
  tableRef.value?.scrollToTop(scrollDelta.value)
}

function scrollByRows() {
  tableRef.value?.scrollToRow(scrollRows.value)
}
</script>
```

隐藏源代码

## TableV2 API [​](#tablev2-api)

### TableV2 Attributes [​](#tablev2-attributes)

| 属性名 | 描述说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| cache | 为了更好的渲染效果预先多加载的行数 | `number` | 2 |
| estimated-row-height | 渲染动态的单元格的预估高度 | `number` | — |
| header-class | header 部分的自定义 class 名 | `string` / Function<[HeaderClassGetter](#typings)\> | — |
| header-props | header 部分的自定义 props 名 | `object` / Function<[HeaderPropsGetter](#typings)\> | — |
| header-cell-props | header cell 部分的自定义 props 名 | `object` / Function<[HeaderCellPropsGetter](#typings)\> | — |
| header-height | Header 的高度由`height`设置。 如果传入数组，它会使 header row 等于数组长度 | `number`/ `number[]` | 50 |
| footer-height | Footer 部分的高度，当传入值时，这部分将被计算入 table 的高度里 | `number` | 0 |
| row-class | row wrapper 部分的自定义 class 名 | `string` / Function<[RowClassGetter](#typings)\> | — |
| row-key | 每行的 key 值，如果不提供，将使用索引 index 代替 | `string` / `Symbol` / `number` | id |
| row-props | row component 部分的自定义 class 名 | `object` / Function<[RowPropsGetter](#typings)\> | — |
| row-height | 每行的高度, 用于计算表的总高度 | `number` | 50 |
| row-event-handlers | 当每行添加了一系列事件处理器时触发 | `object`<[RowEventHandlers](#typings)\> | — |
| cell-props | 每个单元格 cell 的自定义 props (除了 header cell 以外) | `object` / Function<[CellPropsGetter](#typings)\> | — |
| columns | 列 column 的配置数组 | [Column\[\]](#column-attribute) | — |
| data | 要在表中渲染的数据数组 | [Data\[\]](#typings) | \[\] |
| data-getter | 一个自定义方法从数据源获取数据 | Function<[DataGetter<T>](#typings)\> | — |
| fixed-data | 渲染行在表格主内容上方和 header 下方区域的数据 | `object`<[Data](#typings)\> | — |
| expand-column-key | 列的 key 来标记哪个行可以被展开 | `string` | — |
| expanded-row-keys | 存放行展开状态的 key 的数组，可以和 `v-model` 搭配使用 | [KeyType\[\]](#typings) | — |
| default-expanded-row-keys | 默认展开的行的 key 的数组, **这个数据不是响应式的** | [KeyType\[\]](#typings) | — |
| class | 表格的类名称，将应用于表格的全部的三个部分 (左、右、主) | `string` / `array` / `object` | — |
| fixed | 单元格宽度是自适应还是固定 | `boolean` | false |
| width required | 表格的宽度 | `number` | — |
| height required | 表格的高度 | `number` | — |
| max-height | 表格的最大高度 | `number` | — |
| indent-size | 树形表的水平缩进 | `number` | 12 |
| h-scrollbar-size | 配置表格的水平滚动条大小，防止水平和垂直滚动条重叠。 | `number` | 6 |
| v-scrollbar-size | 配置表格的垂直滚动条大小，防止水平和垂直滚动条重叠。 | `number` | 6 |
| scrollbar-always-on | 如果开启，滚动条将一直显示，反之只会在鼠标经过时显示。 | `boolean` | false |
| sort-by | 排序方式 | `object`<[SortBy](#typings)\> | {} |
| sort-state | 多个排序 | `object`<[SortState](#typings)\> | undefined |

### TableV2 Slots [​](#tablev2-slots)

| 插槽名 | 事件参数 |
| --- | --- |
| cell | `object`<[CellSlotProps](#typings)\> |
| header | `object`<[HeaderSlotProps](#typings)\> |
| header-cell | `object`<[HeaderCellSlotProps](#typings)\> |
| row | `object`<[RowSlotProps](#typings)\> |
| footer | — |
| empty | — |
| overlay | — |

### TableV2 Events [​](#tablev2-events)

| 事件名 | 描述 | 参数 |
| --- | --- | --- |
| column-sort | 列排序时调用 | `object`<[ColumnSortParam](#typings)\> |
| expanded-rows-change | 行展开状态改变时触发 | [KeyType\[\]](#typings) |
| end-reached | 到达表格末尾时触发。 回调包含剩余距离，它通常是滚动条高度。 | `Function` |
| scroll | 表格被用户滚动后触发 | `object`<[ScrollParams](#typings)\> |
| rows-rendered | 当行被渲染后触发 | `object`<[RowsRenderedParams](#typings)\> |
| row-expand | 点击箭头图标展开/折叠树节点时触发 | `object`<[RowExpandParams](#typings)\> |

### TableV2 Exposes [​](#tablev2-exposes)

| Method | 描述 | 参数 |
| --- | --- | --- |
| scrollTo | 滚动到给定位置 | `Function` |
| scrollToLeft | 滚动到给定的水平位置 | `Function` |
| scrollToTop | 滚动到给定的垂直位置 | `Function` |
| scrollToRow | 使用给定的滚动策略滚动至指定行 | `Function` |

TIP

请注意：这些是 `JavaScript` 对象，所以您 **不能使用** 短横线命名法（kebab-case）来处理这些属性

### Column Attribute [​](#column-attribute)

| 属性名 | 描述 | 类型 | 默认值 |
| --- | --- | --- | --- |
| align | 表格单元格内容对齐方式 | [Alignment](https://github.com/element-plus/element-plus/blob/b92b22932758f0ddea98810ae248f6ca62f77e25/packages/components/table-v2/src/constants.ts#L6) | left |
| class | 列的类名 | `string` | — |
| key | 唯一标志 | [KeyType](#typings) | — |
| dataKey | data 的唯一标志符 | [KeyType](#typings) | — |
| fixed | 固定列位置 | `boolean` / [FixedDir](https://github.com/element-plus/element-plus/blob/b92b22932758f0ddea98810ae248f6ca62f77e25/packages/components/table-v2/src/constants.ts#L11) | false |
| flexGrow | CSS 属性 flex grow, 仅当不是固定表时才生效 | `number` | 0 |
| flexShrink | CSS 属性 flex shrink, 仅当不是固定表时才生效 | `number` | 1 |
| headerClass | 自定义 header 头部类名 | `string` | — |
| hidden | 此列是否不可见 | `boolean` | — |
| style | 自定义列单元格的类名，将会与 gird 单元格合并 | `object` | — |
| sortable | 设置列是否可排序 | `boolean` | — |
| title | Header 头部单元格中的默认文本 | `string` | — |
| maxWidth | 列的最大宽度 | `number` | — |
| minWidth | 列的最小宽度 | `number` | — |
| width required | 列宽度 | `number` | — |
| cellRenderer | 自定义单元格渲染器 | `VueComponent` / (props: [CellRenderProps](#typings)) => VNode | — |
| headerCellRenderer | 自定义头部渲染器 | `VueComponent` / (props: [HeaderRenderProps](#typings)) => VNode | — |

## Typings [​](#typings)

显示类型声明

ts

```
type HeaderClassGetter = (param: {
  columns: Column<any>[]
  headerIndex: number
}) => string

type HeaderPropsGetter = (param: {
  columns: Column<any>[]
  headerIndex: number
}) => Record<string, any>

type HeaderCellPropsGetter = (param: {
  columns: Column<any>[]
  column: Column<any>
  columnIndex: number
  headerIndex: number
  style: CSSProperties
}) => Record<string, any>

type RowClassGetter = (param: {
  columns: Column<any>[]
  rowData: any
  rowIndex: number
}) => string

type RowPropsGetter = (param: {
  columns: Column<any>[]
  rowData: any
  rowIndex: number
}) => Record<string, any>

type CellPropsGetter = (param: {
  column: Column<any>
  columns: Column<any>[]
  columnIndex: number
  cellData: any
  rowData: any
  rowIndex: number
}) => void

type DataGetterParams<T> = {
  columns: Column<T>[]
  column: Column<T>
  columnIndex: number
} & RowCommonParams

type DataGetter<T> = (params: DataGetterParams<T>) => T

type CellRenderProps<T> = {
  cellData: T
  column: Column<T>
  columns: Column<T>[]
  columnIndex: number
  rowData: any
  rowIndex: number
}

type HeaderRenderProps<T> = {
  column: Column<T>
  columns: Column<T>[]
  columnIndex: number
  headerIndex: number
}

type ScrollParams = {
  xAxisScrollDir: 'forward' | 'backward'
  scrollLeft: number
  yAxisScrollDir: 'forward' | 'backward'
  scrollTop: number
}

type CellSlotProps<T> = {
  column: Column<T>
  columns: Column<T>[]
  columnIndex: number
  depth: number
  style: CSSProperties
  rowData: any
  rowIndex: number
  isScrolling: boolean
  expandIconProps?:
    | {
        rowData: any
        rowIndex: number
        onExpand: (expand: boolean) => void
      }
    | undefined
}

type HeaderSlotProps = {
  cells: VNode[]
  columns: Column<any>[]
  headerIndex: number
}

type HeaderCellSlotProps = {
  class: string
  columns: Column<any>[]
  column: Column<any>
  columnIndex: number
  headerIndex: number
  style: CSSProperties
  headerCellProps?: any
  sortBy: SortBy
  sortState?: SortState | undefined
  onColumnSorted: (e: MouseEvent) => void
}

type RowCommonParams = {
  rowData: any
  rowIndex: number
}

type RowEventHandlerParams = {
  rowKey: KeyType
  event: Event
} & RowCommonParams

type RowEventHandler = (params: RowEventHandlerParams) => void
type RowEventHandlers = {
  onClick?: RowEventHandler
  onContextmenu?: RowEventHandler
  onDblclick?: RowEventHandler
  onMouseenter?: RowEventHandler
  onMouseleave?: RowEventHandler
}

type RowsRenderedParams = {
  rowCacheStart: number
  rowCacheEnd: number
  rowVisibleStart: number
  rowVisibleEnd: number
}

type RowSlotProps = {
  columns: Column<any>[]
  rowData: any
  columnIndex: number
  rowIndex: number
  data: any
  key: number | string
  isScrolling?: boolean
  style: CSSProperties
}

type RowExpandParams = {
  expanded: boolean
  rowKey: KeyType
} & RowCommonParams

type Data = {
  [key: KeyType]: any
  children?: Array<any>
}

type FixedData = Data

type KeyType = string | number | symbol

type ColumnSortParam<T> = { column: Column<T>; key: KeyType; order: SortOrder }

enum SortOrder {
  ASC = 'asc',
  DESC = 'desc',
}

enum Alignment {
  LEFT = 'left',
  CENTER = 'center',
  RIGHT = 'right',
}

type SortBy = { key: KeyType; Order: SortOrder }
type SortState = Record<KeyType, SortOrder>
```

## 常见问题 [​](#常见问题)

#### 如何在第一列中渲染带复选框的列表？ [​](#如何在第一列中渲染带复选框的列表)

由于可以自己定义单元格渲染器，您可以根据示例 [自定义单元格渲染器](#customize-cell-renderer) 代码来渲染 `checkbox`，并自行管理其状态。

#### 为什么虚拟化表提供的功能较 [TableV1](https://element-plus.org/zh-CN/component/table) 少？ [​](#为什么虚拟化表提供的功能较-tablev1-少)

对于虚拟化表格，我们打算减少一些功能，让用户根据需求自行实现。 整合过多的功能会让组件的代码变得难以维护，且对于大多数用户来说，基础功能就已足够。 一些主要的功能尚未开发。 我们很希望听从您的意见。 进入 [Discord](https://discord.com/invite/gXK9XNzW3X) 持续关注.

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/table-v2) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/table-v2.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/table-v2.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/33254923?v=4&size=64)](https://github.com/yicheny)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/132551120?v=4&size=64)](https://github.com/YiMo1)[![](https://avatars.githubusercontent.com/u/80318503?v=4&size=64)](https://github.com/YancyZhang30)[![](https://avatars.githubusercontent.com/u/35426360?v=4&size=64)](https://github.com/Jungzl)[![](https://avatars.githubusercontent.com/u/60510247?v=4&size=64)](https://github.com/Whbbit1999)[![](https://avatars.githubusercontent.com/u/30046649?v=4&size=64)](https://github.com/MrWeilian)[![](https://avatars.githubusercontent.com/u/169252980?v=4&size=64)](https://github.com/xiaochenchen-igg-com)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/22515951?v=4&size=64)](https://github.com/webfansplz)[![](https://avatars.githubusercontent.com/u/17539193?v=4&size=64)](https://github.com/gaoyia)[![](https://avatars.githubusercontent.com/u/32761502?v=4&size=64)](https://github.com/kimverchan)[![](https://avatars.githubusercontent.com/u/134276765?v=4&size=64)](https://github.com/zwgwf)[![](https://avatars.githubusercontent.com/u/93197952?v=4&size=64)](https://github.com/Mutter45)[![](https://avatars.githubusercontent.com/u/32960305?v=4&size=64)](https://github.com/KimYangOfCat)[![](https://avatars.githubusercontent.com/u/48878568?v=4&size=64)](https://github.com/SignDawn)[![](https://avatars.githubusercontent.com/u/24557533?v=4&size=64)](https://github.com/gb853940223)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/78799103?v=4&size=64)](https://github.com/kankan-web)[![](https://avatars.githubusercontent.com/u/75007029?v=4&size=64)](https://github.com/yj-liuzepeng)[![](https://avatars.githubusercontent.com/u/83541965?v=4&size=64)](https://github.com/MilesTails01)[![](https://avatars.githubusercontent.com/u/62194324?v=4&size=64)](https://github.com/onishi-kohei)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)

[Table 表格](https://element-plus.org/zh-CN/component/table)

[Tag 标签](https://element-plus.org/zh-CN/component/tag)


