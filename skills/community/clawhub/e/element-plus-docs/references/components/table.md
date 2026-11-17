## Table 表格 ​

**URL:** https://element-plus.org/zh-CN/component/table

**Contents:**
- Table 表格 ​
- 基础表格 ​
- 带斑马纹表格 ​
- 带边框表格 ​
- 带状态表格 ​
- 显示溢出工具提示的表格 ​
- 固定表头 ​
- 固定列 ​
- 固定列和表头 ​
- 流体高度 ​

用于展示多条结构类似的数据， 可对数据进行排序、筛选、对比或其他自定义操作。

当 el-table 元素中注入 data 对象数组后，在 el-table-column 中用 prop 属性来对应对象中的键名即可填入数据，用 label 属性来定义表格的列名。 可以使用 width 属性来定义列宽。

使用带斑马纹的表格，可以更容易区分出不同行的数据。

stripe 可以创建带斑马纹的表格。 如果 true, 表格将会带有斑马纹。

默认情况下，Table 组件是不具有竖直方向的边框的， 如果需要，可以使用 border 属性，把该属性设置为 true 即可启用。

可将表格内容 highlight 显示，方便区分「成功、信息、警告、危险」等内容。

可以通过指定 Table 组件的 row-class-name 属性来为 Table 中的某一行添加 class， 这样就可以自定义每一行的样式了。

当内容太长时，它会分成多行。您可以使用 show-overflow-tooltip 将其保留在一行中。

属性 show-overflow-tooltip 接受一个布尔值。 为 true 时多余的内容会在 hover 时以 tooltip 的形式显示出来。

只要在 el-table 元素中定义了 height 属性，即可实现固定表头的表格，而不需要额外的代码。

固定列需要使用 fixed 属性，它接受 Boolean 值。 如果为 true, 列将被左侧固定. 它还接受传入字符串，left 或 right，表示左边固定还是右边固定。

当您有大量数据块放入表中，您可以同时固定表头和列。

固定列和表头可以同时使用，只需要将上述两个属性分别设置好即可。

当数据量动态变化时，可以为 Table 设置一个最大高度。

通过设置 max-height 属性为 el-table 指定最大高度。 此时若表格所需的高度大于最大高度，则会显示一个滚动条。

数据结构比较复杂的时候，可使用多级表头来展现数据的层次关系。

只需要将el-table-column 放置于el-table-column 中，你可以实现组头。

组头的属性 fixed 由最外层 el-table-column决定

Table 组件提供了单选的支持， 只需要配置 highlight-current-row 属性即可实现单选。 之后由 current-change 事件来管理选中时触发的事件，它会传入 currentRow，oldCurrentRow。 如果需要显示索引，可以增加一列 el-table-column，设置 type 属性为 index 即可显示从 1 开始的索引号。

在2.8.3 之后， toggleRowSelection 支持第三个参数 ignoreSelectable 以确定是否忽略可选属性。

实现多选非常简单: 手动添加一个 el-table-column，设 type 属性为 selection 即可；

在列中设置 sortable 属性即可实现以该列为基准的排序， 接受一个 Boolean，默认为 false。 可以通过 Table 的 default-sort 属性设置默认的排序列和排序顺序。 可以使用 sort-method 或者 sort-by 使用自定义的排序规则。 如果需要后端排序，需将 sortable 设置为 custom，同时在 Table 上监听 sort-change 事件， 在事件回调中可以获取当前排序的字段名和排序顺序，从而向接口请求排序后的表格数据。 在本例中，我们还使用了 formatter 属性，它用于格式化指定列的值， 接受一个 Function，会传入两个参数：row 和 column， 可以根据自己的需求进行处理。

对表格进行筛选，可快速查找到自己想看的数据。

在列中设置 filters 和 filter-method 属性即可开启该列的筛选， filters 是一个数组，filter-method 是一个方法，它用于决定某些数据是否显示， 会传入三个参数：value, row 和 column。

通过 slot 可以获取到 row, column, $index 和 store（table 内部的状态管理）的数据，用法参考 demo。

当行内容过多并且不想显示横向滚动条时，可以使用 Table 展开行功能。

在 2.9.7 版本后，新增了 preserve-expanded-content 属性，用于控制折叠时是否在 DOM 中保留已展开的行内容。

通过设置 type="expand" 和 slot 可以开启展开行功能， el-table-column 的模板会被渲染成为展开行的内容，展开行可访问的属性与使用自定义列模板时的 slot 相同。

支持树类型的数据的显示。 当 row 中包含 children 字段时，被视为树形数据。 渲染嵌套数据需要 prop 的 row-key。 此外，子行数据可以异步加载。 设置 Table 的lazy属性为 true 与加载函数 load 。 通过指定 row 中的hasChildren字段来指定哪些行是包含子节点。 children 与hasChildren都可以通过 tree-props 配置。

当 treeProps.checkStrictly 为 true，父节点和子节点的选择状态不再关联， 也就是说，当选择父节点时，它的子节点将不被选择； 当 treeProps.checkStrictly 是false，父节点和子节点的选择状态将与子节点的选择状态相关联， 也就是说，当选择父节点时，将选择其所有子节点。

若表格展示的是各类数字，可以在表尾显示各列的合计。

将 show-summary 设置为true就会在表格尾部展示合计行。 默认情况下，对于合计行，第一列不进行数据求合操作，而是显示「合计」二字（可通过sum-text配置），其余列会将本列所有数值进行求合操作，并显示出来。 当然，你也可以定义自己的合计逻辑。 使用 summary-method 并传入一个方法，返回一个数组，这个数组中的各项就会显示在合计行的各列中，可以是一个 VNode 或 String， 具体可以参考本例中的第二个表格。

多行或多列共用一个数据时，可以合并行或列。

通过给 table 传入span-method方法可以实现合并行或列， 方法的参数是一个对象，里面包含当前行 row、当前列 column、当前行号 rowIndex、当前列号 columnIndex 四个属性。 该函数可以返回一个包含两个元素的数组，第一个元素代表 rowspan，第二个元素代表 colspan。 也可以返回一个键名为 rowspan 和 colspan 的对象。

通过给 type=index 的列传入 index 属性，可以自定义索引。 该属性传入数字时，将作为索引的起始值。 也可以传入一个方法，它提供当前行的行号（从 0 开始）作为参数，返回值将作为索引展示。

通过属性 table-layout 可以指定表格中单元格、行和列的布局方式

您可以使用 tooltip-formatter 自定义 Tooltip 提示内容。

el-table-column 是一个泛型组件。 如果 TypeScript 无法从上下文中推断其插槽的行类型，请在 el-table-column 前紧挨着添加 Vue 的 @vue-generic 指令注释，并显式传入行类型。 更多细节请参考 Vue 文档 Generics.

典型问题： #5046 #5862 #6919

这是因为 HTML 定义只允许一些特定元素省略关闭标签，最常见的是 <input> 和 <img>。 对于任意其他元素，如果你省略了关闭标签，原生的 HTML 解析器会认为你从未关闭打开的标签。

**Examples:**

Example 1 (typescript):
```typescript
<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" />
  </el-table>
</template>

<script lang="ts" setup>
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
]
</script>
```

Example 2 (typescript):
```typescript
<template>
  <el-table :data="tableData" stripe style="width: 100%">
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" />
  </el-table>
</template>

<script lang="ts" setup>
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
]
</script>
```

Example 3 (typescript):
```typescript
<template>
  <el-table :data="tableData" border style="width: 100%">
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" />
  </el-table>
</template>

<script lang="ts" setup>
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
]
</script>
```

Example 4 (typescript):
```typescript
<template>
  <el-table
    :data="tableData"
    style="width: 100%"
    :row-class-name="tableRowClassName"
  >
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" />
  </el-table>
</template>

<script lang="ts" setup>
interface User {
  date: string
  name: string
  address: string
}

const tableRowClassName = ({
  row,
  rowIndex,
}: {
  row: User
  rowIndex: number
}) => {
  if (rowIndex === 1) {
    return 'warning-row'
  } else if (rowIndex === 3) {
    return 'success-row'
  }
  return ''
}

const tableData: User[] = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
]
</script>

<style>
.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>
```

---
