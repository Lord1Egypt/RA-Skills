## Virtualized Table 虚拟化表格 beta ​

**URL:** https://element-plus.org/zh-CN/component/table-v2

**Contents:**
- Virtualized Table 虚拟化表格 beta ​
- 基础用法 ​
- 自动调整大小 ​
- 自定义单元格渲染器 ​
- 带有选择的表格 ​
- 可编辑单元格 ​
- 带状态的表格 ​
- 表格行的粘性布局 ​
- 固定列表格 ​
- 表头分组 ​

在前端开发领域，表格一直都是一个高频出现的组件，尤其是在中后台和数据分析场景。 但是，对于 Table V1来说，当一屏里超过 1000 条数据记录时，就会出现卡顿等性能问题，体验不是很好。

通过虚拟化表格组件，超大数据渲染将不再是一个头疼的问题。

该组件仍在测试中，生产环境使用可能有风险。 若您发现了 bug 或问题，请于 GitHub 报告给我们以便修复。 同时，有一些 API 并未在此文档中提及，因为部分还没有开发完全，因此我们不在此提及。

即使虚拟化的表格是高效的，但是当数据负载过大时，网络和内存容量也会成为您应用程序的瓶颈。 因此请牢记，虚拟化表格永远不是最完美的解决方案，请考虑数据分页、过滤器等优化方案。

让我们演示虚拟化表的性能，用10列和1 000行渲染一个基本示例。

如果不想手动向表格传递 width 和 height 属性，可以使用 AutoResizer 对表格组件进行封装。 这会自动为你更新宽度和高度。

尝试调整您的浏览器大小来看看它是如何工作的。

由于 AutoResizer 组件的默认高度是 100%，所以请确保该组件的父元素拥有固定的高度值。 或者，您可以通过将 style 属性传递到 AutoResizer 来定义它。

当然，您可以根据您的需要呈现表格单元格。 这是如何自定义您的单元格的简单例子。

使用自定义的单元格渲染来给表格组件添加选择的能力。

类似上面添加筛选框的方法，我们可以用同样的方法实现可编辑单元格。

可将表格内容 highlight 显示，方便区分「成功、信息、警告、危险」等内容。

要自定义行的外观，请使用 row-class-name 属性。 举个例子，每10行会自动添加 bg-blue-200 类名，每5行会添加 bg-red-100 类名。

您可以简单地使用 fixed-data 属性来实现将某些行固定到表格的头部。

您可以根据滚动事件动态设置粘性行，如这个示例所示。

如果您想要有列粘贴左侧或右侧的某种原因。 您可以通过向表中添加特殊属性来实现这一点。

您可以设置该行的 fixed 属性为 true （代表FixedDir.LEFT）、FixedDir.LEFT 或 FixedDir.RIGHT

正如这个示例，通过自定义表头渲染以将表头分组。

在这种情况下，我们使用了 JSX 功能，这个功能在playground上不被支持。 您可以在本地环境或在线集成开发环境（如 codesandbox ）中试用它们。

建议您使用 JSX 使用您的表格组件，因为它包含 VNode 操作。

虚拟表格提供自定义页眉渲染器以创建自定义标题。 然后我们可以利用这些来渲染过滤器。

您可以在需要时定义多个可排序的列。 请记住，当您在定义了多个可排序的列时， UI 可能会显得有些奇怪，因为用户不知道哪一列被排序。

当处理一个大的列表时，很容易丢失当前行的轨迹和您正在访问的一列。 在这种情况下，使用这个功能可能很有帮助。

虚拟化表格没有使用内置的 table 元素，故 colspan 和 rowspan 与 TableV1 比较略有不同。 然而，通过定制的行渲染器，这些功能仍然可以实现。 在本节中，我们将演示如何实现这一点。

既然我们已经提到了 Colspan，那跨行（row span）也是没有问题的。 它与colspan略有不同，但是基本原理是一样的。

我们当然可以同时使用横跨列与纵跨行来满足您的业务需求！

虚拟表也可以在树状结构中呈现数据。 点击箭头图标，你可以展开或折叠树节点。

虚拟表能够呈现具有动态高度的行数。 如果您正在处理数据并不确定内容大小， 此功能对于调整到内容高度的渲染行是理想的。 要启用此功能，请传递 estimated-row-height 属性。 估计高度越接近实际内容，渲染体验就越顺。

每行高度在渲染过程中动态测量。 因此，如果您试图显示大量数据， UI 可能会 抖动。

使用动态高度渲染，您也可以在表格中显示详细的视图。

自定义表格 footer， 通常用来展示一些汇总数据和信息。

当您想要显示加载指示器之类的浮动元素，可以通过渲染一个浮动在表格之上的遮罩层来实现。

使用 Table V2 暴露的方法可以进行手动或编程式的滚动到指定的偏移量或者行。

scrollToRow 的第二个参数代表滚动策略，计算了要滚动的位置，其默认值是 auto。 如果你想要滚动到某个特定位置，你可以自己定义战略。 可用的选项是 "auto" | "center" | "end" | "start" | "smart"

smart 和auto 之间的区别是， auto 是 smart 滚动策略的子集。

请注意：这些是 JavaScript 对象，所以您 不能使用 短横线命名法（kebab-case）来处理这些属性

由于可以自己定义单元格渲染器，您可以根据示例 自定义单元格渲染器 代码来渲染 checkbox，并自行管理其状态。

对于虚拟化表格，我们打算减少一些功能，让用户根据需求自行实现。 整合过多的功能会让组件的代码变得难以维护，且对于大多数用户来说，基础功能就已足够。 一些主要的功能尚未开发。 我们很希望听从您的意见。 进入 Discord 持续关注.

**Examples:**

Example 1 (json):
```json
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

Example 2 (json):
```json
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

Example 3 (jsx):
```jsx
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

Example 4 (typescript):
```typescript
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

---
