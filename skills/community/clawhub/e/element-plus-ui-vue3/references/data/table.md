---
name: "table"
description: "Table 表格 -- Element Plus Vue3 桌面端组件。Invoke when user needs Table 表格 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/table.html"
---

---

# Table 表格 [​](#table-表格)

更新日志待解决

228

用于展示多条结构类似的数据， 可对数据进行排序、筛选、对比或其他自定义操作。

## 基础表格 [​](#基础表格)

基础的表格展示用法。

当 `el-table` 元素中注入 `data` 对象数组后，在 `el-table-column` 中用 `prop` 属性来对应对象中的键名即可填入数据，用 `label` 属性来定义表格的列名。 可以使用 `width` 属性来定义列宽。

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_1_column_1" width="180"><col name="el-table_1_column_2" width="180"><col name="el-table_1_column_3" width="533"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCI+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTgwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIxODBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiAvPlxuICA8L2VsLXRhYmxlPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IHRhYmxlRGF0YSA9IFtcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAzJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAyJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA0JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/basic.vue)_

vue

```
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

隐藏源代码

## 带斑马纹表格 [​](#带斑马纹表格)

使用带斑马纹的表格，可以更容易区分出不同行的数据。

`stripe` 可以创建带斑马纹的表格。 如果 `true`, 表格将会带有斑马纹。

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_2_column_4" width="180"><col name="el-table_2_column_5" width="180"><col name="el-table_2_column_6" width="533"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_2_column_4 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_2_column_5 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_2_column_6 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row el-table__row--striped"><td colspan="1" rowspan="1" class="el-table_2_column_4 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_2_column_5 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_2_column_6 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_2_column_4 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_2_column_5 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_2_column_6 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row el-table__row--striped"><td colspan="1" rowspan="1" class="el-table_2_column_4 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_2_column_5 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_2_column_6 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHJpcGUgc3R5bGU9XCJ3aWR0aDogMTAwJVwiPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImRhdGVcIiBsYWJlbD1cIkRhdGVcIiB3aWR0aD1cIjE4MFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIHdpZHRoPVwiMTgwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhZGRyZXNzXCIgbGFiZWw9XCJBZGRyZXNzXCIgLz5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5jb25zdCB0YWJsZURhdGEgPSBbXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/striped.vue)_

vue

```
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

隐藏源代码

## 带边框表格 [​](#带边框表格)

默认情况下，Table 组件是不具有竖直方向的边框的， 如果需要，可以使用 `border` 属性，把该属性设置为 `true` 即可启用。

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_3_column_7" width="180"><col name="el-table_3_column_8" width="180"><col name="el-table_3_column_9" width="533"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_3_column_7 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_3_column_8 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_3_column_9 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_3_column_7 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_3_column_8 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_3_column_9 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_3_column_7 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_3_column_8 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_3_column_9 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_3_column_7 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_3_column_8 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_3_column_9 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBib3JkZXIgc3R5bGU9XCJ3aWR0aDogMTAwJVwiPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImRhdGVcIiBsYWJlbD1cIkRhdGVcIiB3aWR0aD1cIjE4MFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIHdpZHRoPVwiMTgwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhZGRyZXNzXCIgbGFiZWw9XCJBZGRyZXNzXCIgLz5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5jb25zdCB0YWJsZURhdGEgPSBbXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/with-border.vue)_

vue

```
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

隐藏源代码

## 带状态表格 [​](#带状态表格)

可将表格内容 highlight 显示，方便区分「成功、信息、警告、危险」等内容。

可以通过指定 Table 组件的 `row-class-name` 属性来为 Table 中的某一行添加 class， 这样就可以自定义每一行的样式了。

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_4_column_10" width="180"><col name="el-table_4_column_11" width="180"><col name="el-table_4_column_12" width="533"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_4_column_10 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_4_column_11 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_4_column_12 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row warning-row"><td colspan="1" rowspan="1" class="el-table_4_column_10 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_4_column_11 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_4_column_12 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_4_column_10 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_4_column_11 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_4_column_12 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row success-row"><td colspan="1" rowspan="1" class="el-table_4_column_10 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_4_column_11 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_4_column_12 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGVcbiAgICA6ZGF0YT1cInRhYmxlRGF0YVwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMTAwJVwiXG4gICAgOnJvdy1jbGFzcy1uYW1lPVwidGFibGVSb3dDbGFzc05hbWVcIlxuICA+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTgwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIxODBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiAvPlxuICA8L2VsLXRhYmxlPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmludGVyZmFjZSBVc2VyIHtcbiAgZGF0ZTogc3RyaW5nXG4gIG5hbWU6IHN0cmluZ1xuICBhZGRyZXNzOiBzdHJpbmdcbn1cblxuY29uc3QgdGFibGVSb3dDbGFzc05hbWUgPSAoe1xuICByb3csXG4gIHJvd0luZGV4LFxufToge1xuICByb3c6IFVzZXJcbiAgcm93SW5kZXg6IG51bWJlclxufSkgPT4ge1xuICBpZiAocm93SW5kZXggPT09IDEpIHtcbiAgICByZXR1cm4gJ3dhcm5pbmctcm93J1xuICB9IGVsc2UgaWYgKHJvd0luZGV4ID09PSAzKSB7XG4gICAgcmV0dXJuICdzdWNjZXNzLXJvdydcbiAgfVxuICByZXR1cm4gJydcbn1cblxuY29uc3QgdGFibGVEYXRhOiBVc2VyW10gPSBbXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG5dXG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLmVsLXRhYmxlIC53YXJuaW5nLXJvdyB7XG4gIC0tZWwtdGFibGUtdHItYmctY29sb3I6IHZhcigtLWVsLWNvbG9yLXdhcm5pbmctbGlnaHQtOSk7XG59XG4uZWwtdGFibGUgLnN1Y2Nlc3Mtcm93IHtcbiAgLS1lbC10YWJsZS10ci1iZy1jb2xvcjogdmFyKC0tZWwtY29sb3Itc3VjY2Vzcy1saWdodC05KTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/with-status.vue)_

vue

```
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

隐藏源代码

## 显示溢出工具提示的表格 [​](#显示溢出工具提示的表格)

当内容太长时，它会分成多行。您可以使用 `show-overflow-tooltip` 将其保留在一行中。

属性 show-overflow-tooltip 接受一个布尔值。 为 `true` 时多余的内容会在 hover 时以 tooltip 的形式显示出来。

|
 |

Date

 |

Name

 |

use show-overflow-tooltip

 |

address

 |
| --- | --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_5_column_13" width="55"><col name="el-table_5_column_14" width="120"><col name="el-table_5_column_15" width="120"><col name="el-table_5_column_16" width="240"><col name="el-table_5_column_17" width="358"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_5_column_13 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-375"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-375"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_5_column_14 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_5_column_15 el-table__cell"><div class="cell">Aleyna Kutzner</div></td><td colspan="1" rowspan="1" class="el-table_5_column_16 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">Lohrbergstr. 86c, Süd Lilli, Saarland</div></td><td colspan="1" rowspan="1" class="el-table_5_column_17 el-table__cell"><div class="cell">Lohrbergstr. 86c, Süd Lilli, Saarland</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_5_column_13 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-376"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-376"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_5_column_14 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_5_column_15 el-table__cell"><div class="cell">Helen Jacobi</div></td><td colspan="1" rowspan="1" class="el-table_5_column_16 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">760 A Street, South Frankfield, Illinois</div></td><td colspan="1" rowspan="1" class="el-table_5_column_17 el-table__cell"><div class="cell">760 A Street, South Frankfield, Illinois</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_5_column_13 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-377"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-377"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_5_column_14 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_5_column_15 el-table__cell"><div class="cell">Brandon Deckert</div></td><td colspan="1" rowspan="1" class="el-table_5_column_16 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">Arnold-Ohletz-Str. 41a, Alt Malinascheid, Thüringen</div></td><td colspan="1" rowspan="1" class="el-table_5_column_17 el-table__cell"><div class="cell">Arnold-Ohletz-Str. 41a, Alt Malinascheid, Thüringen</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_5_column_13 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-378"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-378"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_5_column_14 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_5_column_15 el-table__cell"><div class="cell">Margie Smith</div></td><td colspan="1" rowspan="1" class="el-table_5_column_16 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">23618 Windsor Drive, West Ricardoview, Idaho</div></td><td colspan="1" rowspan="1" class="el-table_5_column_17 el-table__cell"><div class="cell">23618 Windsor Drive, West Ricardoview, Idaho</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCI+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiB0eXBlPVwic2VsZWN0aW9uXCIgd2lkdGg9XCI1NVwiIC8+XG4gICAgPCEtLSBAdnVlLWdlbmVyaWMge1VzZXJ9IC0tPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gbGFiZWw9XCJEYXRlXCIgd2lkdGg9XCIxMjBcIj5cbiAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD1cInNjb3BlXCI+e3sgc2NvcGUucm93LmRhdGUgfX08L3RlbXBsYXRlPlxuICAgIDwvZWwtdGFibGUtY29sdW1uPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcGVydHk9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIxMjBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW5cbiAgICAgIHByb3BlcnR5PVwiYWRkcmVzc1wiXG4gICAgICBsYWJlbD1cInVzZSBzaG93LW92ZXJmbG93LXRvb2x0aXBcIlxuICAgICAgd2lkdGg9XCIyNDBcIlxuICAgICAgc2hvdy1vdmVyZmxvdy10b29sdGlwXG4gICAgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3BlcnR5PVwiYWRkcmVzc1wiIGxhYmVsPVwiYWRkcmVzc1wiIC8+XG4gIDwvZWwtdGFibGU+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW50ZXJmYWNlIFVzZXIge1xuICBkYXRlOiBzdHJpbmdcbiAgbmFtZTogc3RyaW5nXG4gIGFkZHJlc3M6IHN0cmluZ1xufVxuY29uc3QgdGFibGVEYXRhOiBVc2VyW10gPSBbXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ0FsZXluYSBLdXR6bmVyJyxcbiAgICBhZGRyZXNzOiAnTG9ocmJlcmdzdHIuIDg2YywgU8O8ZCBMaWxsaSwgU2FhcmxhbmQnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDMnLFxuICAgIG5hbWU6ICdIZWxlbiBKYWNvYmknLFxuICAgIGFkZHJlc3M6ICc3NjAgQSBTdHJlZXQsIFNvdXRoIEZyYW5rZmllbGQsIElsbGlub2lzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAyJyxcbiAgICBuYW1lOiAnQnJhbmRvbiBEZWNrZXJ0JyxcbiAgICBhZGRyZXNzOiAnQXJub2xkLU9obGV0ei1TdHIuIDQxYSwgQWx0IE1hbGluYXNjaGVpZCwgVGjDvHJpbmdlbicsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ01hcmdpZSBTbWl0aCcsXG4gICAgYWRkcmVzczogJzIzNjE4IFdpbmRzb3IgRHJpdmUsIFdlc3QgUmljYXJkb3ZpZXcsIElkYWhvJyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/show-overflow-tooltip.vue)_

vue

```
<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column type="selection" width="55" />
    <!-- @vue-generic {User} -->
    <el-table-column label="Date" width="120">
      <template #default="scope">{{ scope.row.date }}</template>
    </el-table-column>
    <el-table-column property="name" label="Name" width="120" />
    <el-table-column
      property="address"
      label="use show-overflow-tooltip"
      width="240"
      show-overflow-tooltip
    />
    <el-table-column property="address" label="address" />
  </el-table>
</template>

<script lang="ts" setup>
interface User {
  date: string
  name: string
  address: string
}
const tableData: User[] = [
  {
    date: '2016-05-04',
    name: 'Aleyna Kutzner',
    address: 'Lohrbergstr. 86c, Süd Lilli, Saarland',
  },
  {
    date: '2016-05-03',
    name: 'Helen Jacobi',
    address: '760 A Street, South Frankfield, Illinois',
  },
  {
    date: '2016-05-02',
    name: 'Brandon Deckert',
    address: 'Arnold-Ohletz-Str. 41a, Alt Malinascheid, Thüringen',
  },
  {
    date: '2016-05-01',
    name: 'Margie Smith',
    address: '23618 Windsor Drive, West Ricardoview, Idaho',
  },
]
</script>
```

隐藏源代码

## 固定表头 [​](#固定表头)

纵向内容过多时，可选择固定表头。

只要在 `el-table` 元素中定义了 `height` 属性，即可实现固定表头的表格，而不需要额外的代码。

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_6_column_18" width="180"><col name="el-table_6_column_19" width="180"><col name="el-table_6_column_20" width="533"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_6_column_18 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_6_column_19 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_6_column_20 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_6_column_18 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_6_column_19 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_6_column_20 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_6_column_18 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_6_column_19 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_6_column_20 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_6_column_18 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_6_column_19 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_6_column_20 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_6_column_18 el-table__cell"><div class="cell">2016-05-08</div></td><td colspan="1" rowspan="1" class="el-table_6_column_19 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_6_column_20 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_6_column_18 el-table__cell"><div class="cell">2016-05-06</div></td><td colspan="1" rowspan="1" class="el-table_6_column_19 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_6_column_20 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_6_column_18 el-table__cell"><div class="cell">2016-05-07</div></td><td colspan="1" rowspan="1" class="el-table_6_column_19 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_6_column_20 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBoZWlnaHQ9XCIyNTBcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCI+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTgwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIxODBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiAvPlxuICA8L2VsLXRhYmxlPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IHRhYmxlRGF0YSA9IFtcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAzJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAyJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA0JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA4JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA2JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA3JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/fixed-header.vue)_

vue

```
<template>
  <el-table :data="tableData" height="250" style="width: 100%">
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
  {
    date: '2016-05-08',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-06',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-07',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
]
</script>
```

隐藏源代码

## 固定列 [​](#固定列)

横向内容过多时，可选择固定列。

固定列需要使用 `fixed` 属性，它接受 `Boolean` 值。 如果为 `true`, 列将被左侧固定. 它还接受传入字符串，left 或 right，表示左边固定还是右边固定。

|
Date

 |

Name

 |

State

 |

City

 |

Address

 |

Zip

 |

Operations

 |
| --- | --- | --- | --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 1350px;"><colgroup><col name="el-table_7_column_21" width="150"><col name="el-table_7_column_22" width="120"><col name="el-table_7_column_23" width="120"><col name="el-table_7_column_24" width="120"><col name="el-table_7_column_25" width="600"><col name="el-table_7_column_26" width="120"><col name="el-table_7_column_27" width="120"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_7_column_21 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_7_column_22 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_7_column_23 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_7_column_24 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_7_column_25 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_7_column_26 el-table__cell"><div class="cell">CA 90036</div></td><td colspan="1" rowspan="1" class="el-table_7_column_27 el-table-fixed-column--right is-first-column el-table__cell" style="right: 0px;"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Detail </span></button><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Edit</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_7_column_21 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_7_column_22 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_7_column_23 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_7_column_24 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_7_column_25 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_7_column_26 el-table__cell"><div class="cell">CA 90036</div></td><td colspan="1" rowspan="1" class="el-table_7_column_27 el-table-fixed-column--right is-first-column el-table__cell" style="right: 0px;"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Detail </span></button><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Edit</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_7_column_21 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_7_column_22 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_7_column_23 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_7_column_24 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_7_column_25 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_7_column_26 el-table__cell"><div class="cell">CA 90036</div></td><td colspan="1" rowspan="1" class="el-table_7_column_27 el-table-fixed-column--right is-first-column el-table__cell" style="right: 0px;"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Detail </span></button><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Edit</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_7_column_21 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_7_column_22 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_7_column_23 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_7_column_24 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_7_column_25 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_7_column_26 el-table__cell"><div class="cell">CA 90036</div></td><td colspan="1" rowspan="1" class="el-table_7_column_27 el-table-fixed-column--right is-first-column el-table__cell" style="right: 0px;"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Detail </span></button><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Edit</span></button></div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCI+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBmaXhlZCBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTUwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIxMjBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cInN0YXRlXCIgbGFiZWw9XCJTdGF0ZVwiIHdpZHRoPVwiMTIwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJjaXR5XCIgbGFiZWw9XCJDaXR5XCIgd2lkdGg9XCIxMjBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiB3aWR0aD1cIjYwMFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiemlwXCIgbGFiZWw9XCJaaXBcIiB3aWR0aD1cIjEyMFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBmaXhlZD1cInJpZ2h0XCIgbGFiZWw9XCJPcGVyYXRpb25zXCIgbWluLXdpZHRoPVwiMTIwXCI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ+XG4gICAgICAgIDxlbC1idXR0b24gbGluayB0eXBlPVwicHJpbWFyeVwiIHNpemU9XCJzbWFsbFwiIEBjbGljaz1cImhhbmRsZUNsaWNrXCI+XG4gICAgICAgICAgRGV0YWlsXG4gICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgICA8ZWwtYnV0dG9uIGxpbmsgdHlwZT1cInByaW1hcnlcIiBzaXplPVwic21hbGxcIj5FZGl0PC9lbC1idXR0b24+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtdGFibGUtY29sdW1uPlxuICA8L2VsLXRhYmxlPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IGhhbmRsZUNsaWNrID0gKCkgPT4ge1xuICBjb25zb2xlLmxvZygnY2xpY2snKVxufVxuXG5jb25zdCB0YWJsZURhdGEgPSBbXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgICB0YWc6ICdIb21lJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAyJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICAgIHRhZzogJ09mZmljZScsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgICB0YWc6ICdIb21lJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICAgIHRhZzogJ09mZmljZScsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/fixed-column.vue)_

vue

```
<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column fixed prop="date" label="Date" width="150" />
    <el-table-column prop="name" label="Name" width="120" />
    <el-table-column prop="state" label="State" width="120" />
    <el-table-column prop="city" label="City" width="120" />
    <el-table-column prop="address" label="Address" width="600" />
    <el-table-column prop="zip" label="Zip" width="120" />
    <el-table-column fixed="right" label="Operations" min-width="120">
      <template #default>
        <el-button link type="primary" size="small" @click="handleClick">
          Detail
        </el-button>
        <el-button link type="primary" size="small">Edit</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
const handleClick = () => {
  console.log('click')
}

const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Home',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Office',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Home',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Office',
  },
]
</script>
```

隐藏源代码

## 固定列和表头 [​](#固定列和表头)

当您有大量数据块放入表中，您可以同时固定表头和列。

固定列和表头可以同时使用，只需要将上述两个属性分别设置好即可。

|
Date

 |

Name

 |

State

 |

City

 |

Address

 |

Zip

 |
| --- | --- | --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 1390px;"><colgroup><col name="el-table_8_column_28" width="150"><col name="el-table_8_column_29" width="120"><col name="el-table_8_column_30" width="120"><col name="el-table_8_column_31" width="320"><col name="el-table_8_column_32" width="600"><col name="el-table_8_column_33" width="80"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_8_column_28 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_8_column_29 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_8_column_30 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_8_column_31 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_32 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_33 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_8_column_28 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_8_column_29 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_8_column_30 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_8_column_31 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_32 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_33 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_8_column_28 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_8_column_29 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_8_column_30 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_8_column_31 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_32 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_33 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_8_column_28 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_8_column_29 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_8_column_30 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_8_column_31 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_32 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_33 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_8_column_28 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-08</div></td><td colspan="1" rowspan="1" class="el-table_8_column_29 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_8_column_30 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_8_column_31 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_32 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_33 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_8_column_28 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-06</div></td><td colspan="1" rowspan="1" class="el-table_8_column_29 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_8_column_30 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_8_column_31 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_32 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_33 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_8_column_28 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-07</div></td><td colspan="1" rowspan="1" class="el-table_8_column_29 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_8_column_30 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_8_column_31 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_32 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_8_column_33 el-table__cell"><div class="cell">CA 90036</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCIgaGVpZ2h0PVwiMjUwXCI+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBmaXhlZCBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTUwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIxMjBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cInN0YXRlXCIgbGFiZWw9XCJTdGF0ZVwiIHdpZHRoPVwiMTIwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJjaXR5XCIgbGFiZWw9XCJDaXR5XCIgd2lkdGg9XCIzMjBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiB3aWR0aD1cIjYwMFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiemlwXCIgbGFiZWw9XCJaaXBcIiAvPlxuICA8L2VsLXRhYmxlPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IHRhYmxlRGF0YSA9IFtcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAzJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDInLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ0xvcyBBbmdlbGVzJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB6aXA6ICdDQSA5MDAzNicsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDgnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ0xvcyBBbmdlbGVzJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB6aXA6ICdDQSA5MDAzNicsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA3JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/fixed-column-and-header.vue)_

vue

```
<template>
  <el-table :data="tableData" style="width: 100%" height="250">
    <el-table-column fixed prop="date" label="Date" width="150" />
    <el-table-column prop="name" label="Name" width="120" />
    <el-table-column prop="state" label="State" width="120" />
    <el-table-column prop="city" label="City" width="320" />
    <el-table-column prop="address" label="Address" width="600" />
    <el-table-column prop="zip" label="Zip" />
  </el-table>
</template>

<script lang="ts" setup>
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-08',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-06',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-07',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
]
</script>
```

隐藏源代码

## 流体高度 [​](#流体高度)

当数据量动态变化时，可以为 Table 设置一个最大高度。

通过设置 `max-height` 属性为 `el-table` 指定最大高度。 此时若表格所需的高度大于最大高度，则会显示一个滚动条。

|
Date

 |

Name

 |

State

 |

City

 |

Address

 |

Zip

 |

Operations

 |
| --- | --- | --- | --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 1350px;"><colgroup><col name="el-table_9_column_34" width="150"><col name="el-table_9_column_35" width="120"><col name="el-table_9_column_36" width="120"><col name="el-table_9_column_37" width="120"><col name="el-table_9_column_38" width="600"><col name="el-table_9_column_39" width="120"><col name="el-table_9_column_40" width="120"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_9_column_34 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_9_column_35 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_9_column_36 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_9_column_37 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_9_column_38 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_9_column_39 el-table__cell"><div class="cell">CA 90036</div></td><td colspan="1" rowspan="1" class="el-table_9_column_40 el-table-fixed-column--right is-first-column el-table__cell" style="right: 0px;"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Remove</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_9_column_34 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_9_column_35 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_9_column_36 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_9_column_37 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_9_column_38 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_9_column_39 el-table__cell"><div class="cell">CA 90036</div></td><td colspan="1" rowspan="1" class="el-table_9_column_40 el-table-fixed-column--right is-first-column el-table__cell" style="right: 0px;"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Remove</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_9_column_34 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_9_column_35 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_9_column_36 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_9_column_37 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_9_column_38 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_9_column_39 el-table__cell"><div class="cell">CA 90036</div></td><td colspan="1" rowspan="1" class="el-table_9_column_40 el-table-fixed-column--right is-first-column el-table__cell" style="right: 0px;"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--primary el-button--small is-link"><span class="">Remove</span></button></div></td></tr></tbody></table>

Add Item

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCIgbWF4LWhlaWdodD1cIjI1MFwiPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gZml4ZWQgcHJvcD1cImRhdGVcIiBsYWJlbD1cIkRhdGVcIiB3aWR0aD1cIjE1MFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIHdpZHRoPVwiMTIwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJzdGF0ZVwiIGxhYmVsPVwiU3RhdGVcIiB3aWR0aD1cIjEyMFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiY2l0eVwiIGxhYmVsPVwiQ2l0eVwiIHdpZHRoPVwiMTIwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhZGRyZXNzXCIgbGFiZWw9XCJBZGRyZXNzXCIgd2lkdGg9XCI2MDBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cInppcFwiIGxhYmVsPVwiWmlwXCIgd2lkdGg9XCIxMjBcIiAvPlxuICAgIDwhLS0gQHZ1ZS1nZW5lcmljIHtVbndyYXBSZWY8dHlwZW9mIHRhYmxlRGF0YT5bbnVtYmVyXX0gLS0+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBmaXhlZD1cInJpZ2h0XCIgbGFiZWw9XCJPcGVyYXRpb25zXCIgbWluLXdpZHRoPVwiMTIwXCI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJzY29wZVwiPlxuICAgICAgICA8ZWwtYnV0dG9uXG4gICAgICAgICAgbGlua1xuICAgICAgICAgIHR5cGU9XCJwcmltYXJ5XCJcbiAgICAgICAgICBzaXplPVwic21hbGxcIlxuICAgICAgICAgIEBjbGljay5wcmV2ZW50PVwiZGVsZXRlUm93KHNjb3BlLiRpbmRleClcIlxuICAgICAgICA+XG4gICAgICAgICAgUmVtb3ZlXG4gICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLXRhYmxlLWNvbHVtbj5cbiAgPC9lbC10YWJsZT5cbiAgPGVsLWJ1dHRvbiBjbGFzcz1cIm10LTRcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCIgQGNsaWNrPVwib25BZGRJdGVtXCI+XG4gICAgQWRkIEl0ZW1cbiAgPC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IGRheWpzIGZyb20gJ2RheWpzJ1xuXG5pbXBvcnQgdHlwZSB7IFVud3JhcFJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3Qgbm93ID0gbmV3IERhdGUoKVxuXG5jb25zdCB0YWJsZURhdGEgPSByZWYoW1xuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ0xvcyBBbmdlbGVzJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB6aXA6ICdDQSA5MDAzNicsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAzJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICB9LFxuXSlcblxuY29uc3QgZGVsZXRlUm93ID0gKGluZGV4OiBudW1iZXIpID0+IHtcbiAgdGFibGVEYXRhLnZhbHVlLnNwbGljZShpbmRleCwgMSlcbn1cblxuY29uc3Qgb25BZGRJdGVtID0gKCkgPT4ge1xuICBub3cuc2V0RGF0ZShub3cuZ2V0RGF0ZSgpICsgMSlcbiAgdGFibGVEYXRhLnZhbHVlLnB1c2goe1xuICAgIGRhdGU6IGRheWpzKG5vdykuZm9ybWF0KCdZWVlZLU1NLUREJyksXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/fixed-header-with-fluid-header.vue)_

vue

```
<template>
  <el-table :data="tableData" style="width: 100%" max-height="250">
    <el-table-column fixed prop="date" label="Date" width="150" />
    <el-table-column prop="name" label="Name" width="120" />
    <el-table-column prop="state" label="State" width="120" />
    <el-table-column prop="city" label="City" width="120" />
    <el-table-column prop="address" label="Address" width="600" />
    <el-table-column prop="zip" label="Zip" width="120" />
    <!-- @vue-generic {UnwrapRef<typeof tableData>[number]} -->
    <el-table-column fixed="right" label="Operations" min-width="120">
      <template #default="scope">
        <el-button
          link
          type="primary"
          size="small"
          @click.prevent="deleteRow(scope.$index)"
        >
          Remove
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-button class="mt-4" style="width: 100%" @click="onAddItem">
    Add Item
  </el-button>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

import type { UnwrapRef } from 'vue'

const now = new Date()

const tableData = ref([
  {
    date: '2016-05-01',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-03',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
])

const deleteRow = (index: number) => {
  tableData.value.splice(index, 1)
}

const onAddItem = () => {
  now.setDate(now.getDate() + 1)
  tableData.value.push({
    date: dayjs(now).format('YYYY-MM-DD'),
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  })
}
</script>
```

隐藏源代码

## 多级表头 [​](#多级表头)

数据结构比较复杂的时候，可使用多级表头来展现数据的层次关系。

只需要将el-table-column 放置于el-table-column 中，你可以实现组头。

|
Date

 |

Delivery Info

 |
| --- | --- |
|

Name

 |

Address Info

 |
| --- | --- |
|

State

 |

City

 |

Address

 |

Zip

 |
| --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_10_column_41" width="150"><col name="el-table_10_column_42_column_43" width="120"><col name="el-table_10_column_42_column_44_column_45" width="120"><col name="el-table_10_column_42_column_44_column_46" width="120"><col name="el-table_10_column_42_column_44_column_47" width="263"><col name="el-table_10_column_42_column_44_column_48" width="120"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_10_column_41 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_43 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_45 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_46 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_47 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_48 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_10_column_41 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_43 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_45 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_46 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_47 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_48 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_10_column_41 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_43 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_45 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_46 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_47 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_48 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_10_column_41 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_43 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_45 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_46 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_47 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_48 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_10_column_41 el-table__cell"><div class="cell">2016-05-08</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_43 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_45 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_46 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_47 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_48 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_10_column_41 el-table__cell"><div class="cell">2016-05-06</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_43 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_45 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_46 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_47 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_48 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_10_column_41 el-table__cell"><div class="cell">2016-05-07</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_43 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_45 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_46 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_47 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_10_column_42_column_44_column_48 el-table__cell"><div class="cell">CA 90036</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCI+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTUwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIGxhYmVsPVwiRGVsaXZlcnkgSW5mb1wiPlxuICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIHdpZHRoPVwiMTIwXCIgLz5cbiAgICAgIDxlbC10YWJsZS1jb2x1bW4gbGFiZWw9XCJBZGRyZXNzIEluZm9cIj5cbiAgICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwic3RhdGVcIiBsYWJlbD1cIlN0YXRlXCIgd2lkdGg9XCIxMjBcIiAvPlxuICAgICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJjaXR5XCIgbGFiZWw9XCJDaXR5XCIgd2lkdGg9XCIxMjBcIiAvPlxuICAgICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhZGRyZXNzXCIgbGFiZWw9XCJBZGRyZXNzXCIgLz5cbiAgICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiemlwXCIgbGFiZWw9XCJaaXBcIiB3aWR0aD1cIjEyMFwiIC8+XG4gICAgICA8L2VsLXRhYmxlLWNvbHVtbj5cbiAgICA8L2VsLXRhYmxlLWNvbHVtbj5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5jb25zdCB0YWJsZURhdGEgPSBbXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAyJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDQnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ0xvcyBBbmdlbGVzJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB6aXA6ICdDQSA5MDAzNicsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA4JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDYnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ0xvcyBBbmdlbGVzJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB6aXA6ICdDQSA5MDAzNicsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/grouping-header.vue)_

vue

```
<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="date" label="Date" width="150" />
    <el-table-column label="Delivery Info">
      <el-table-column prop="name" label="Name" width="120" />
      <el-table-column label="Address Info">
        <el-table-column prop="state" label="State" width="120" />
        <el-table-column prop="city" label="City" width="120" />
        <el-table-column prop="address" label="Address" />
        <el-table-column prop="zip" label="Zip" width="120" />
      </el-table-column>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-08',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-06',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-07',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
]
</script>
```

隐藏源代码

## 固定表头 [​](#固定表头-1)

支持固定群组头

组头的属性 `fixed` 由最外层 `el-table-column`决定

|
Date

 |

Name

 |

State

 |

City

 |

Address

 |

Zip

 |
| --- | --- | --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 1390px;"><colgroup><col name="el-table_11_column_49" width="150"><col name="el-table_11_column_50" width="120"><col name="el-table_11_column_51" width="120"><col name="el-table_11_column_52" width="320"><col name="el-table_11_column_53" width="600"><col name="el-table_11_column_54" width="80"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_11_column_49 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_11_column_50 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_11_column_51 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_11_column_52 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_53 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_54 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_11_column_49 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_11_column_50 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_11_column_51 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_11_column_52 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_53 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_54 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_11_column_49 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_11_column_50 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_11_column_51 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_11_column_52 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_53 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_54 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_11_column_49 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_11_column_50 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_11_column_51 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_11_column_52 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_53 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_54 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_11_column_49 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-08</div></td><td colspan="1" rowspan="1" class="el-table_11_column_50 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_11_column_51 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_11_column_52 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_53 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_54 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_11_column_49 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-06</div></td><td colspan="1" rowspan="1" class="el-table_11_column_50 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_11_column_51 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_11_column_52 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_53 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_54 el-table__cell"><div class="cell">CA 90036</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_11_column_49 el-table-fixed-column--left is-last-column el-table__cell" style="left: 0px;"><div class="cell">2016-05-07</div></td><td colspan="1" rowspan="1" class="el-table_11_column_50 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_11_column_51 el-table__cell"><div class="cell">California</div></td><td colspan="1" rowspan="1" class="el-table_11_column_52 el-table__cell"><div class="cell">Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_53 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_11_column_54 el-table__cell"><div class="cell">CA 90036</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCIgaGVpZ2h0PVwiMjUwXCI+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBmaXhlZCBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTUwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIxMjBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cInN0YXRlXCIgbGFiZWw9XCJTdGF0ZVwiIHdpZHRoPVwiMTIwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJjaXR5XCIgbGFiZWw9XCJDaXR5XCIgd2lkdGg9XCIzMjBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiB3aWR0aD1cIjYwMFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiemlwXCIgbGFiZWw9XCJaaXBcIiAvPlxuICA8L2VsLXRhYmxlPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IHRhYmxlRGF0YSA9IFtcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAzJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDInLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ0xvcyBBbmdlbGVzJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB6aXA6ICdDQSA5MDAzNicsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDgnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ0xvcyBBbmdlbGVzJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB6aXA6ICdDQSA5MDAzNicsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA3JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdMb3MgQW5nZWxlcycsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgemlwOiAnQ0EgOTAwMzYnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/fixed-column-and-header.vue)_

vue

```
<template>
  <el-table :data="tableData" style="width: 100%" height="250">
    <el-table-column fixed prop="date" label="Date" width="150" />
    <el-table-column prop="name" label="Name" width="120" />
    <el-table-column prop="state" label="State" width="120" />
    <el-table-column prop="city" label="City" width="320" />
    <el-table-column prop="address" label="Address" width="600" />
    <el-table-column prop="zip" label="Zip" />
  </el-table>
</template>

<script lang="ts" setup>
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-08',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-06',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-07',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
]
</script>
```

隐藏源代码

## 单选 [​](#单选)

选择单行数据时使用色块表示。

Table 组件提供了单选的支持， 只需要配置 `highlight-current-row` 属性即可实现单选。 之后由 `current-change` 事件来管理选中时触发的事件，它会传入 `currentRow`，`oldCurrentRow`。 如果需要显示索引，可以增加一列 `el-table-column`，设置 `type` 属性为 `index` 即可显示从 1 开始的索引号。

|
 |

Date

 |

Name

 |

Address

 |
| --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_12_column_55" width="50"><col name="el-table_12_column_56" width="120"><col name="el-table_12_column_57" width="120"><col name="el-table_12_column_58" width="603"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_12_column_55 el-table__cell"><div class="cell"><div>1</div></div></td><td colspan="1" rowspan="1" class="el-table_12_column_56 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_12_column_57 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_12_column_58 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_12_column_55 el-table__cell"><div class="cell"><div>2</div></div></td><td colspan="1" rowspan="1" class="el-table_12_column_56 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_12_column_57 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_12_column_58 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_12_column_55 el-table__cell"><div class="cell"><div>3</div></div></td><td colspan="1" rowspan="1" class="el-table_12_column_56 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_12_column_57 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_12_column_58 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_12_column_55 el-table__cell"><div class="cell"><div>4</div></div></td><td colspan="1" rowspan="1" class="el-table_12_column_56 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_12_column_57 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_12_column_58 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

Select second rowClear selection

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGVcbiAgICByZWY9XCJzaW5nbGVUYWJsZVJlZlwiXG4gICAgOmRhdGE9XCJ0YWJsZURhdGFcIlxuICAgIGhpZ2hsaWdodC1jdXJyZW50LXJvd1xuICAgIHN0eWxlPVwid2lkdGg6IDEwMCVcIlxuICAgIEBjdXJyZW50LWNoYW5nZT1cImhhbmRsZUN1cnJlbnRDaGFuZ2VcIlxuICA+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiB0eXBlPVwiaW5kZXhcIiB3aWR0aD1cIjUwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3BlcnR5PVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTIwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3BlcnR5PVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIHdpZHRoPVwiMTIwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3BlcnR5PVwiYWRkcmVzc1wiIGxhYmVsPVwiQWRkcmVzc1wiIC8+XG4gIDwvZWwtdGFibGU+XG4gIDxkaXYgc3R5bGU9XCJtYXJnaW4tdG9wOiAyMHB4XCI+XG4gICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJzZXRDdXJyZW50KHRhYmxlRGF0YVsxXSlcIj5TZWxlY3Qgc2Vjb25kIHJvdzwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gQGNsaWNrPVwic2V0Q3VycmVudCgpXCI+Q2xlYXIgc2VsZWN0aW9uPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBUYWJsZUluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbnRlcmZhY2UgVXNlciB7XG4gIGRhdGU6IHN0cmluZ1xuICBuYW1lOiBzdHJpbmdcbiAgYWRkcmVzczogc3RyaW5nXG59XG5cbmNvbnN0IGN1cnJlbnRSb3cgPSByZWYoKVxuY29uc3Qgc2luZ2xlVGFibGVSZWYgPSByZWY8VGFibGVJbnN0YW5jZT4oKVxuXG5jb25zdCBzZXRDdXJyZW50ID0gKHJvdz86IFVzZXIpID0+IHtcbiAgc2luZ2xlVGFibGVSZWYudmFsdWUhLnNldEN1cnJlbnRSb3cocm93KVxufVxuY29uc3QgaGFuZGxlQ3VycmVudENoYW5nZSA9ICh2YWw6IFVzZXIgfCBudWxsKSA9PiB7XG4gIGN1cnJlbnRSb3cudmFsdWUgPSB2YWxcbn1cbmNvbnN0IHRhYmxlRGF0YTogVXNlcltdID0gW1xuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDMnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDInLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDQnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/single-select.vue)_

vue

```
<template>
  <el-table
    ref="singleTableRef"
    :data="tableData"
    highlight-current-row
    style="width: 100%"
    @current-change="handleCurrentChange"
  >
    <el-table-column type="index" width="50" />
    <el-table-column property="date" label="Date" width="120" />
    <el-table-column property="name" label="Name" width="120" />
    <el-table-column property="address" label="Address" />
  </el-table>
  <div style="margin-top: 20px">
    <el-button @click="setCurrent(tableData[1])">Select second row</el-button>
    <el-button @click="setCurrent()">Clear selection</el-button>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TableInstance } from 'element-plus'

interface User {
  date: string
  name: string
  address: string
}

const currentRow = ref()
const singleTableRef = ref<TableInstance>()

const setCurrent = (row?: User) => {
  singleTableRef.value!.setCurrentRow(row)
}
const handleCurrentChange = (val: User | null) => {
  currentRow.value = val
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
```

隐藏源代码

## 多选 [​](#多选)

你也可以选择多行。

在2.8.3 之后， `toggleRowSelection` 支持第三个参数 `ignoreSelectable` 以确定是否忽略可选属性。

实现多选非常简单: 手动添加一个 `el-table-column`，设 `type` 属性为 `selection` 即可；

|
 |

Date

 |

Name

 |

Address

 |
| --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_13_column_59" width="55"><col name="el-table_13_column_60" width="120"><col name="el-table_13_column_61" width="120"><col name="el-table_13_column_62" width="598"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_13_column_59 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox is-disabled" aria-label="Select this row" for="el-id-1024-380"><span class="el-checkbox__input is-disabled"><input class="el-checkbox__original" type="checkbox" disabled="" id="el-id-1024-380"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_13_column_60 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_13_column_61 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_13_column_62 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_13_column_59 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox is-disabled" aria-label="Select this row" for="el-id-1024-381"><span class="el-checkbox__input is-disabled"><input class="el-checkbox__original" type="checkbox" disabled="" id="el-id-1024-381"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_13_column_60 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_13_column_61 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_13_column_62 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_13_column_59 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-382"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-382"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_13_column_60 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_13_column_61 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_13_column_62 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_13_column_59 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-383"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-383"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_13_column_60 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_13_column_61 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_13_column_62 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_13_column_59 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-384"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-384"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_13_column_60 el-table__cell"><div class="cell">2016-05-08</div></td><td colspan="1" rowspan="1" class="el-table_13_column_61 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_13_column_62 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_13_column_59 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-385"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-385"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_13_column_60 el-table__cell"><div class="cell">2016-05-06</div></td><td colspan="1" rowspan="1" class="el-table_13_column_61 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_13_column_62 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_13_column_59 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-386"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-386"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_13_column_60 el-table__cell"><div class="cell">2016-05-07</div></td><td colspan="1" rowspan="1" class="el-table_13_column_61 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_13_column_62 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

Toggle selection status of second and third rows Toggle selection status based on selectable Clear selection

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGVcbiAgICByZWY9XCJtdWx0aXBsZVRhYmxlUmVmXCJcbiAgICA6ZGF0YT1cInRhYmxlRGF0YVwiXG4gICAgcm93LWtleT1cImlkXCJcbiAgICBzdHlsZT1cIndpZHRoOiAxMDAlXCJcbiAgICBAc2VsZWN0aW9uLWNoYW5nZT1cImhhbmRsZVNlbGVjdGlvbkNoYW5nZVwiXG4gID5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHR5cGU9XCJzZWxlY3Rpb25cIiA6c2VsZWN0YWJsZT1cInNlbGVjdGFibGVcIiB3aWR0aD1cIjU1XCIgLz5cbiAgICA8IS0tIEB2dWUtZ2VuZXJpYyB7VXNlcn0gLS0+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBsYWJlbD1cIkRhdGVcIiB3aWR0aD1cIjEyMFwiPlxuICAgICAgPHRlbXBsYXRlICNkZWZhdWx0PVwic2NvcGVcIj57eyBzY29wZS5yb3cuZGF0ZSB9fTwvdGVtcGxhdGU+XG4gICAgPC9lbC10YWJsZS1jb2x1bW4+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wZXJ0eT1cIm5hbWVcIiBsYWJlbD1cIk5hbWVcIiB3aWR0aD1cIjEyMFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wZXJ0eT1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiAvPlxuICA8L2VsLXRhYmxlPlxuICA8ZGl2IHN0eWxlPVwibWFyZ2luLXRvcDogMjBweFwiPlxuICAgIDxlbC1idXR0b24gQGNsaWNrPVwidG9nZ2xlU2VsZWN0aW9uKFt0YWJsZURhdGFbMV0sIHRhYmxlRGF0YVsyXV0pXCI+XG4gICAgICBUb2dnbGUgc2VsZWN0aW9uIHN0YXR1cyBvZiBzZWNvbmQgYW5kIHRoaXJkIHJvd3NcbiAgICA8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIEBjbGljaz1cInRvZ2dsZVNlbGVjdGlvbihbdGFibGVEYXRhWzFdLCB0YWJsZURhdGFbMl1dLCBmYWxzZSlcIj5cbiAgICAgIFRvZ2dsZSBzZWxlY3Rpb24gc3RhdHVzIGJhc2VkIG9uIHNlbGVjdGFibGVcbiAgICA8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIEBjbGljaz1cInRvZ2dsZVNlbGVjdGlvbigpXCI+Q2xlYXIgc2VsZWN0aW9uPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBUYWJsZUluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbnRlcmZhY2UgVXNlciB7XG4gIGlkOiBudW1iZXJcbiAgZGF0ZTogc3RyaW5nXG4gIG5hbWU6IHN0cmluZ1xuICBhZGRyZXNzOiBzdHJpbmdcbn1cblxuY29uc3QgbXVsdGlwbGVUYWJsZVJlZiA9IHJlZjxUYWJsZUluc3RhbmNlPigpXG5jb25zdCBtdWx0aXBsZVNlbGVjdGlvbiA9IHJlZjxVc2VyW10+KFtdKVxuXG5jb25zdCBzZWxlY3RhYmxlID0gKHJvdzogVXNlcikgPT4gIVsxLCAyXS5pbmNsdWRlcyhyb3cuaWQpXG5jb25zdCB0b2dnbGVTZWxlY3Rpb24gPSAocm93cz86IFVzZXJbXSwgaWdub3JlU2VsZWN0YWJsZT86IGJvb2xlYW4pID0+IHtcbiAgaWYgKHJvd3MpIHtcbiAgICByb3dzLmZvckVhY2goKHJvdykgPT4ge1xuICAgICAgbXVsdGlwbGVUYWJsZVJlZi52YWx1ZSEudG9nZ2xlUm93U2VsZWN0aW9uKFxuICAgICAgICByb3csXG4gICAgICAgIHVuZGVmaW5lZCxcbiAgICAgICAgaWdub3JlU2VsZWN0YWJsZVxuICAgICAgKVxuICAgIH0pXG4gIH0gZWxzZSB7XG4gICAgbXVsdGlwbGVUYWJsZVJlZi52YWx1ZSEuY2xlYXJTZWxlY3Rpb24oKVxuICB9XG59XG5jb25zdCBoYW5kbGVTZWxlY3Rpb25DaGFuZ2UgPSAodmFsOiBVc2VyW10pID0+IHtcbiAgbXVsdGlwbGVTZWxlY3Rpb24udmFsdWUgPSB2YWxcbn1cblxuY29uc3QgdGFibGVEYXRhOiBVc2VyW10gPSBbXG4gIHtcbiAgICBpZDogMSxcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBpZDogMixcbiAgICBkYXRlOiAnMjAxNi0wNS0wMicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBpZDogMyxcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBpZDogNCxcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBpZDogNSxcbiAgICBkYXRlOiAnMjAxNi0wNS0wOCcsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBpZDogNixcbiAgICBkYXRlOiAnMjAxNi0wNS0wNicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBpZDogNyxcbiAgICBkYXRlOiAnMjAxNi0wNS0wNycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/multi-select.vue)_

vue

```
<template>
  <el-table
    ref="multipleTableRef"
    :data="tableData"
    row-key="id"
    style="width: 100%"
    @selection-change="handleSelectionChange"
  >
    <el-table-column type="selection" :selectable="selectable" width="55" />
    <!-- @vue-generic {User} -->
    <el-table-column label="Date" width="120">
      <template #default="scope">{{ scope.row.date }}</template>
    </el-table-column>
    <el-table-column property="name" label="Name" width="120" />
    <el-table-column property="address" label="Address" />
  </el-table>
  <div style="margin-top: 20px">
    <el-button @click="toggleSelection([tableData[1], tableData[2]])">
      Toggle selection status of second and third rows
    </el-button>
    <el-button @click="toggleSelection([tableData[1], tableData[2]], false)">
      Toggle selection status based on selectable
    </el-button>
    <el-button @click="toggleSelection()">Clear selection</el-button>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TableInstance } from 'element-plus'

interface User {
  id: number
  date: string
  name: string
  address: string
}

const multipleTableRef = ref<TableInstance>()
const multipleSelection = ref<User[]>([])

const selectable = (row: User) => ![1, 2].includes(row.id)
const toggleSelection = (rows?: User[], ignoreSelectable?: boolean) => {
  if (rows) {
    rows.forEach((row) => {
      multipleTableRef.value!.toggleRowSelection(
        row,
        undefined,
        ignoreSelectable
      )
    })
  } else {
    multipleTableRef.value!.clearSelection()
  }
}
const handleSelectionChange = (val: User[]) => {
  multipleSelection.value = val
}

const tableData: User[] = [
  {
    id: 1,
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 2,
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 3,
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 4,
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 5,
    date: '2016-05-08',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 6,
    date: '2016-05-06',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 7,
    date: '2016-05-07',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
]
</script>
```

隐藏源代码

## 排序 [​](#排序)

对表格进行排序，可快速查找或对比数据。

在列中设置 `sortable` 属性即可实现以该列为基准的排序， 接受一个 `Boolean`，默认为 `false`。 可以通过 Table 的 `default-sort` 属性设置默认的排序列和排序顺序。 可以使用 `sort-method` 或者 `sort-by` 使用自定义的排序规则。 如果需要后端排序，需将 `sortable` 设置为 `custom`，同时在 Table 上监听 `sort-change` 事件， 在事件回调中可以获取当前排序的字段名和排序顺序，从而向接口请求排序后的表格数据。 在本例中，我们还使用了 `formatter` 属性，它用于格式化指定列的值， 接受一个 `Function`，会传入两个参数：`row` 和 `column`， 可以根据自己的需求进行处理。

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_14_column_63" width="180"><col name="el-table_14_column_64" width="180"><col name="el-table_14_column_65" width="533"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_14_column_63 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_14_column_64 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_14_column_65 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_14_column_63 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_14_column_64 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_14_column_65 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_14_column_63 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_14_column_64 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_14_column_65 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_14_column_63 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_14_column_64 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_14_column_65 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGVcbiAgICA6ZGF0YT1cInRhYmxlRGF0YVwiXG4gICAgOmRlZmF1bHQtc29ydD1cInsgcHJvcDogJ2RhdGUnLCBvcmRlcjogJ2Rlc2NlbmRpbmcnIH1cIlxuICAgIHN0eWxlPVwid2lkdGg6IDEwMCVcIlxuICA+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHNvcnRhYmxlIHdpZHRoPVwiMTgwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIxODBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiA6Zm9ybWF0dGVyPVwiZm9ybWF0dGVyXCIgLz5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgdHlwZSB7IFRhYmxlQ29sdW1uQ3R4IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbnRlcmZhY2UgVXNlciB7XG4gIGRhdGU6IHN0cmluZ1xuICBuYW1lOiBzdHJpbmdcbiAgYWRkcmVzczogc3RyaW5nXG59XG5cbmNvbnN0IGZvcm1hdHRlciA9IChyb3c6IFVzZXIsIGNvbHVtbjogVGFibGVDb2x1bW5DdHg8VXNlcj4pID0+IHtcbiAgcmV0dXJuIHJvdy5hZGRyZXNzXG59XG5cbmNvbnN0IHRhYmxlRGF0YTogVXNlcltdID0gW1xuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDMnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDInLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDQnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/sort.vue)_

vue

```
<template>
  <el-table
    :data="tableData"
    :default-sort="{ prop: 'date', order: 'descending' }"
    style="width: 100%"
  >
    <el-table-column prop="date" label="Date" sortable width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" :formatter="formatter" />
  </el-table>
</template>

<script lang="ts" setup>
import type { TableColumnCtx } from 'element-plus'

interface User {
  date: string
  name: string
  address: string
}

const formatter = (row: User, column: TableColumnCtx<User>) => {
  return row.address
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
```

隐藏源代码

## 筛选 [​](#筛选)

对表格进行筛选，可快速查找到自己想看的数据。

在列中设置 `filters` 和 `filter-method` 属性即可开启该列的筛选， filters 是一个数组，`filter-method` 是一个方法，它用于决定某些数据是否显示， 会传入三个参数：`value`, `row` 和 `column`。

reset date filterreset all filters

|
Date

 |

Name

 |

Address

 |

Tag

 |
| --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_15_column_66" width="180"><col name="el-table_15_column_67" width="180"><col name="el-table_15_column_68" width="433"><col name="el-table_15_column_69" width="100"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_15_column_66 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_15_column_67 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_15_column_68 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_15_column_69 el-table__cell"><div class="cell"><span class="el-tag el-tag--primary el-tag--light"><span class="el-tag__content">Home</span></span></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_15_column_66 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_15_column_67 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_15_column_68 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_15_column_69 el-table__cell"><div class="cell"><span class="el-tag el-tag--success el-tag--light"><span class="el-tag__content">Office</span></span></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_15_column_66 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_15_column_67 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_15_column_68 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_15_column_69 el-table__cell"><div class="cell"><span class="el-tag el-tag--primary el-tag--light"><span class="el-tag__content">Home</span></span></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_15_column_66 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_15_column_67 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_15_column_68 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td><td colspan="1" rowspan="1" class="el-table_15_column_69 el-table__cell"><div class="cell"><span class="el-tag el-tag--success el-tag--light"><span class="el-tag__content">Office</span></span></div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIEBjbGljaz1cInJlc2V0RGF0ZUZpbHRlclwiPnJlc2V0IGRhdGUgZmlsdGVyPC9lbC1idXR0b24+XG4gIDxlbC1idXR0b24gQGNsaWNrPVwiY2xlYXJGaWx0ZXJcIj5yZXNldCBhbGwgZmlsdGVyczwvZWwtYnV0dG9uPlxuICA8ZWwtdGFibGUgcmVmPVwidGFibGVSZWZcIiByb3cta2V5PVwiZGF0ZVwiIDpkYXRhPVwidGFibGVEYXRhXCIgc3R5bGU9XCJ3aWR0aDogMTAwJVwiPlxuICAgIDxlbC10YWJsZS1jb2x1bW5cbiAgICAgIHByb3A9XCJkYXRlXCJcbiAgICAgIGxhYmVsPVwiRGF0ZVwiXG4gICAgICBzb3J0YWJsZVxuICAgICAgd2lkdGg9XCIxODBcIlxuICAgICAgY29sdW1uLWtleT1cImRhdGVcIlxuICAgICAgOmZpbHRlcnM9XCJbXG4gICAgICAgIHsgdGV4dDogJzIwMTYtMDUtMDEnLCB2YWx1ZTogJzIwMTYtMDUtMDEnIH0sXG4gICAgICAgIHsgdGV4dDogJzIwMTYtMDUtMDInLCB2YWx1ZTogJzIwMTYtMDUtMDInIH0sXG4gICAgICAgIHsgdGV4dDogJzIwMTYtMDUtMDMnLCB2YWx1ZTogJzIwMTYtMDUtMDMnIH0sXG4gICAgICAgIHsgdGV4dDogJzIwMTYtMDUtMDQnLCB2YWx1ZTogJzIwMTYtMDUtMDQnIH0sXG4gICAgICBdXCJcbiAgICAgIDpmaWx0ZXItbWV0aG9kPVwiZmlsdGVySGFuZGxlclwiXG4gICAgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIxODBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiA6Zm9ybWF0dGVyPVwiZm9ybWF0dGVyXCIgLz5cblxuICAgIDwhLS0gQHZ1ZS1nZW5lcmljIHtVc2VyfSAtLT5cbiAgICA8ZWwtdGFibGUtY29sdW1uXG4gICAgICBwcm9wPVwidGFnXCJcbiAgICAgIGxhYmVsPVwiVGFnXCJcbiAgICAgIHdpZHRoPVwiMTAwXCJcbiAgICAgIDpmaWx0ZXJzPVwiW1xuICAgICAgICB7IHRleHQ6ICdIb21lJywgdmFsdWU6ICdIb21lJyB9LFxuICAgICAgICB7IHRleHQ6ICdPZmZpY2UnLCB2YWx1ZTogJ09mZmljZScgfSxcbiAgICAgIF1cIlxuICAgICAgOmZpbHRlci1tZXRob2Q9XCJmaWx0ZXJUYWdcIlxuICAgICAgZmlsdGVyLXBsYWNlbWVudD1cImJvdHRvbS1lbmRcIlxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD1cInNjb3BlXCI+XG4gICAgICAgIDxlbC10YWdcbiAgICAgICAgICA6dHlwZT1cInNjb3BlLnJvdy50YWcgPT09ICdIb21lJyA/ICdwcmltYXJ5JyA6ICdzdWNjZXNzJ1wiXG4gICAgICAgICAgZGlzYWJsZS10cmFuc2l0aW9uc1xuICAgICAgICAgID57eyBzY29wZS5yb3cudGFnIH19PC9lbC10YWdcbiAgICAgICAgPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLXRhYmxlLWNvbHVtbj5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgVGFibGVDb2x1bW5DdHgsIFRhYmxlSW5zdGFuY2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmludGVyZmFjZSBVc2VyIHtcbiAgZGF0ZTogc3RyaW5nXG4gIG5hbWU6IHN0cmluZ1xuICBhZGRyZXNzOiBzdHJpbmdcbiAgdGFnOiBzdHJpbmdcbn1cblxuY29uc3QgdGFibGVSZWYgPSByZWY8VGFibGVJbnN0YW5jZT4oKVxuXG5jb25zdCByZXNldERhdGVGaWx0ZXIgPSAoKSA9PiB7XG4gIHRhYmxlUmVmLnZhbHVlIS5jbGVhckZpbHRlcihbJ2RhdGUnXSlcbn1cbmNvbnN0IGNsZWFyRmlsdGVyID0gKCkgPT4ge1xuICB0YWJsZVJlZi52YWx1ZSEuY2xlYXJGaWx0ZXIoKVxufVxuY29uc3QgZm9ybWF0dGVyID0gKHJvdzogVXNlciwgY29sdW1uOiBUYWJsZUNvbHVtbkN0eDxVc2VyPikgPT4ge1xuICByZXR1cm4gcm93LmFkZHJlc3Ncbn1cbmNvbnN0IGZpbHRlclRhZyA9ICh2YWx1ZTogc3RyaW5nLCByb3c6IFVzZXIpID0+IHtcbiAgcmV0dXJuIHJvdy50YWcgPT09IHZhbHVlXG59XG5jb25zdCBmaWx0ZXJIYW5kbGVyID0gKFxuICB2YWx1ZTogc3RyaW5nLFxuICByb3c6IFVzZXIsXG4gIGNvbHVtbjogVGFibGVDb2x1bW5DdHg8VXNlcj5cbikgPT4ge1xuICBjb25zdCBwcm9wZXJ0eSA9IGNvbHVtblsncHJvcGVydHknXVxuICByZXR1cm4gcm93W3Byb3BlcnR5XSA9PT0gdmFsdWVcbn1cblxuY29uc3QgdGFibGVEYXRhOiBVc2VyW10gPSBbXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgdGFnOiAnSG9tZScsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgdGFnOiAnT2ZmaWNlJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA0JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB0YWc6ICdIb21lJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB0YWc6ICdPZmZpY2UnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/filter.vue)_

vue

```
<template>
  <el-button @click="resetDateFilter">reset date filter</el-button>
  <el-button @click="clearFilter">reset all filters</el-button>
  <el-table ref="tableRef" row-key="date" :data="tableData" style="width: 100%">
    <el-table-column
      prop="date"
      label="Date"
      sortable
      width="180"
      column-key="date"
      :filters="[
        { text: '2016-05-01', value: '2016-05-01' },
        { text: '2016-05-02', value: '2016-05-02' },
        { text: '2016-05-03', value: '2016-05-03' },
        { text: '2016-05-04', value: '2016-05-04' },
      ]"
      :filter-method="filterHandler"
    />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" :formatter="formatter" />

    <!-- @vue-generic {User} -->
    <el-table-column
      prop="tag"
      label="Tag"
      width="100"
      :filters="[
        { text: 'Home', value: 'Home' },
        { text: 'Office', value: 'Office' },
      ]"
      :filter-method="filterTag"
      filter-placement="bottom-end"
    >
      <template #default="scope">
        <el-tag
          :type="scope.row.tag === 'Home' ? 'primary' : 'success'"
          disable-transitions
          >{{ scope.row.tag }}</el-tag
        >
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TableColumnCtx, TableInstance } from 'element-plus'

interface User {
  date: string
  name: string
  address: string
  tag: string
}

const tableRef = ref<TableInstance>()

const resetDateFilter = () => {
  tableRef.value!.clearFilter(['date'])
}
const clearFilter = () => {
  tableRef.value!.clearFilter()
}
const formatter = (row: User, column: TableColumnCtx<User>) => {
  return row.address
}
const filterTag = (value: string, row: User) => {
  return row.tag === value
}
const filterHandler = (
  value: string,
  row: User,
  column: TableColumnCtx<User>
) => {
  const property = column['property']
  return row[property] === value
}

const tableData: User[] = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
    tag: 'Home',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
    tag: 'Office',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
    tag: 'Home',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
    tag: 'Office',
  },
]
</script>
```

隐藏源代码

## 自定义列模板 [​](#自定义列模板)

自定义列的显示内容，可组合其他组件使用。

通过 `slot` 可以获取到 row, column, $index 和 store（table 内部的状态管理）的数据，用法参考 demo。

|
Date

 |

Name

 |

Operations

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_16_column_70" width="180"><col name="el-table_16_column_71" width="180"><col name="el-table_16_column_72" width="533"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_16_column_70 el-table__cell"><div class="cell"><div style="display: flex; align-items: center;"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a320 320 0 1 0 0-640 320 320 0 0 0 0 640m0 64a384 384 0 1 1 0-768 384 384 0 0 1 0 768"></path><path fill="currentColor" d="M512 320a32 32 0 0 1 32 32l-.512 224a32 32 0 1 1-64 0L480 352a32 32 0 0 1 32-32"></path><path fill="currentColor" d="M448 576a64 64 0 1 0 128 0 64 64 0 1 0-128 0m96-448v128h-64V128h-96a32 32 0 0 1 0-64h256a32 32 0 1 1 0 64z"></path></svg></i><span style="margin-left: 10px;">2016-05-03</span></div></div></td><td colspan="1" rowspan="1" class="el-table_16_column_71 el-table__cell"><div class="cell"><span class="el-tag el-tag--primary el-tag--light el-tooltip__trigger"><span class="el-tag__content">Tom</span></span></div></td><td colspan="1" rowspan="1" class="el-table_16_column_72 el-table__cell"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--small"><span class="">Edit </span></button><button aria-disabled="false" type="button" class="el-button el-button--danger el-button--small"><span class="">Delete</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_16_column_70 el-table__cell"><div class="cell"><div style="display: flex; align-items: center;"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a320 320 0 1 0 0-640 320 320 0 0 0 0 640m0 64a384 384 0 1 1 0-768 384 384 0 0 1 0 768"></path><path fill="currentColor" d="M512 320a32 32 0 0 1 32 32l-.512 224a32 32 0 1 1-64 0L480 352a32 32 0 0 1 32-32"></path><path fill="currentColor" d="M448 576a64 64 0 1 0 128 0 64 64 0 1 0-128 0m96-448v128h-64V128h-96a32 32 0 0 1 0-64h256a32 32 0 1 1 0 64z"></path></svg></i><span style="margin-left: 10px;">2016-05-02</span></div></div></td><td colspan="1" rowspan="1" class="el-table_16_column_71 el-table__cell"><div class="cell"><span class="el-tag el-tag--primary el-tag--light el-tooltip__trigger"><span class="el-tag__content">Tom</span></span></div></td><td colspan="1" rowspan="1" class="el-table_16_column_72 el-table__cell"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--small"><span class="">Edit </span></button><button aria-disabled="false" type="button" class="el-button el-button--danger el-button--small"><span class="">Delete</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_16_column_70 el-table__cell"><div class="cell"><div style="display: flex; align-items: center;"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a320 320 0 1 0 0-640 320 320 0 0 0 0 640m0 64a384 384 0 1 1 0-768 384 384 0 0 1 0 768"></path><path fill="currentColor" d="M512 320a32 32 0 0 1 32 32l-.512 224a32 32 0 1 1-64 0L480 352a32 32 0 0 1 32-32"></path><path fill="currentColor" d="M448 576a64 64 0 1 0 128 0 64 64 0 1 0-128 0m96-448v128h-64V128h-96a32 32 0 0 1 0-64h256a32 32 0 1 1 0 64z"></path></svg></i><span style="margin-left: 10px;">2016-05-04</span></div></div></td><td colspan="1" rowspan="1" class="el-table_16_column_71 el-table__cell"><div class="cell"><span class="el-tag el-tag--primary el-tag--light el-tooltip__trigger"><span class="el-tag__content">Tom</span></span></div></td><td colspan="1" rowspan="1" class="el-table_16_column_72 el-table__cell"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--small"><span class="">Edit </span></button><button aria-disabled="false" type="button" class="el-button el-button--danger el-button--small"><span class="">Delete</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_16_column_70 el-table__cell"><div class="cell"><div style="display: flex; align-items: center;"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a320 320 0 1 0 0-640 320 320 0 0 0 0 640m0 64a384 384 0 1 1 0-768 384 384 0 0 1 0 768"></path><path fill="currentColor" d="M512 320a32 32 0 0 1 32 32l-.512 224a32 32 0 1 1-64 0L480 352a32 32 0 0 1 32-32"></path><path fill="currentColor" d="M448 576a64 64 0 1 0 128 0 64 64 0 1 0-128 0m96-448v128h-64V128h-96a32 32 0 0 1 0-64h256a32 32 0 1 1 0 64z"></path></svg></i><span style="margin-left: 10px;">2016-05-01</span></div></div></td><td colspan="1" rowspan="1" class="el-table_16_column_71 el-table__cell"><div class="cell"><span class="el-tag el-tag--primary el-tag--light el-tooltip__trigger"><span class="el-tag__content">Tom</span></span></div></td><td colspan="1" rowspan="1" class="el-table_16_column_72 el-table__cell"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--small"><span class="">Edit </span></button><button aria-disabled="false" type="button" class="el-button el-button--danger el-button--small"><span class="">Delete</span></button></div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCI+XG4gICAgPCEtLSBAdnVlLWdlbmVyaWMge1VzZXJ9IC0tPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gbGFiZWw9XCJEYXRlXCIgd2lkdGg9XCIxODBcIj5cbiAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD1cInNjb3BlXCI+XG4gICAgICAgIDxkaXYgc3R5bGU9XCJkaXNwbGF5OiBmbGV4OyBhbGlnbi1pdGVtczogY2VudGVyXCI+XG4gICAgICAgICAgPGVsLWljb24+PHRpbWVyIC8+PC9lbC1pY29uPlxuICAgICAgICAgIDxzcGFuIHN0eWxlPVwibWFyZ2luLWxlZnQ6IDEwcHhcIj57eyBzY29wZS5yb3cuZGF0ZSB9fTwvc3Bhbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtdGFibGUtY29sdW1uPlxuICAgIDwhLS0gQHZ1ZS1nZW5lcmljIHtVc2VyfSAtLT5cbiAgICA8ZWwtdGFibGUtY29sdW1uIGxhYmVsPVwiTmFtZVwiIHdpZHRoPVwiMTgwXCI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJzY29wZVwiPlxuICAgICAgICA8ZWwtcG9wb3ZlciBlZmZlY3Q9XCJsaWdodFwiIHRyaWdnZXI9XCJob3ZlclwiIHBsYWNlbWVudD1cInRvcFwiIHdpZHRoPVwiYXV0b1wiPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD5cbiAgICAgICAgICAgIDxkaXY+bmFtZToge3sgc2NvcGUucm93Lm5hbWUgfX08L2Rpdj5cbiAgICAgICAgICAgIDxkaXY+YWRkcmVzczoge3sgc2NvcGUucm93LmFkZHJlc3MgfX08L2Rpdj5cbiAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPlxuICAgICAgICAgICAgPGVsLXRhZz57eyBzY29wZS5yb3cubmFtZSB9fTwvZWwtdGFnPlxuICAgICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgIDwvZWwtcG9wb3Zlcj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC10YWJsZS1jb2x1bW4+XG4gICAgPCEtLSBAdnVlLWdlbmVyaWMge1VzZXJ9IC0tPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gbGFiZWw9XCJPcGVyYXRpb25zXCI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJzY29wZVwiPlxuICAgICAgICA8ZWwtYnV0dG9uIHNpemU9XCJzbWFsbFwiIEBjbGljaz1cImhhbmRsZUVkaXQoc2NvcGUuJGluZGV4LCBzY29wZS5yb3cpXCI+XG4gICAgICAgICAgRWRpdFxuICAgICAgICA8L2VsLWJ1dHRvbj5cbiAgICAgICAgPGVsLWJ1dHRvblxuICAgICAgICAgIHNpemU9XCJzbWFsbFwiXG4gICAgICAgICAgdHlwZT1cImRhbmdlclwiXG4gICAgICAgICAgQGNsaWNrPVwiaGFuZGxlRGVsZXRlKHNjb3BlLiRpbmRleCwgc2NvcGUucm93KVwiXG4gICAgICAgID5cbiAgICAgICAgICBEZWxldGVcbiAgICAgICAgPC9lbC1idXR0b24+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtdGFibGUtY29sdW1uPlxuICA8L2VsLXRhYmxlPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IFRpbWVyIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmludGVyZmFjZSBVc2VyIHtcbiAgZGF0ZTogc3RyaW5nXG4gIG5hbWU6IHN0cmluZ1xuICBhZGRyZXNzOiBzdHJpbmdcbn1cblxuY29uc3QgaGFuZGxlRWRpdCA9IChpbmRleDogbnVtYmVyLCByb3c6IFVzZXIpID0+IHtcbiAgY29uc29sZS5sb2coaW5kZXgsIHJvdylcbn1cbmNvbnN0IGhhbmRsZURlbGV0ZSA9IChpbmRleDogbnVtYmVyLCByb3c6IFVzZXIpID0+IHtcbiAgY29uc29sZS5sb2coaW5kZXgsIHJvdylcbn1cblxuY29uc3QgdGFibGVEYXRhOiBVc2VyW10gPSBbXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/custom-column.vue)_

vue

```
<template>
  <el-table :data="tableData" style="width: 100%">
    <!-- @vue-generic {User} -->
    <el-table-column label="Date" width="180">
      <template #default="scope">
        <div style="display: flex; align-items: center">
          <el-icon><timer /></el-icon>
          <span style="margin-left: 10px">{{ scope.row.date }}</span>
        </div>
      </template>
    </el-table-column>
    <!-- @vue-generic {User} -->
    <el-table-column label="Name" width="180">
      <template #default="scope">
        <el-popover effect="light" trigger="hover" placement="top" width="auto">
          <template #default>
            <div>name: {{ scope.row.name }}</div>
            <div>address: {{ scope.row.address }}</div>
          </template>
          <template #reference>
            <el-tag>{{ scope.row.name }}</el-tag>
          </template>
        </el-popover>
      </template>
    </el-table-column>
    <!-- @vue-generic {User} -->
    <el-table-column label="Operations">
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
          Edit
        </el-button>
        <el-button
          size="small"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)"
        >
          Delete
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import { Timer } from '@element-plus/icons-vue'

interface User {
  date: string
  name: string
  address: string
}

const handleEdit = (index: number, row: User) => {
  console.log(index, row)
}
const handleDelete = (index: number, row: User) => {
  console.log(index, row)
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
```

隐藏源代码

## 自定义表头 [​](#自定义表头)

表头支持自定义。

通过设置 [slot](https://v3.vuejs.org/guide/component-slots.html) 来自定义表头。

|
Date

 |

Name

 |

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_17_column_73" width="299"><col name="el-table_17_column_74" width="297"><col name="el-table_17_column_75" width="297"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_17_column_73 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_17_column_74 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_17_column_75 is-right el-table__cell"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--small"><span class="">Edit </span></button><button aria-disabled="false" type="button" class="el-button el-button--danger el-button--small"><span class="">Delete</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_17_column_73 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_17_column_74 el-table__cell"><div class="cell">John</div></td><td colspan="1" rowspan="1" class="el-table_17_column_75 is-right el-table__cell"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--small"><span class="">Edit </span></button><button aria-disabled="false" type="button" class="el-button el-button--danger el-button--small"><span class="">Delete</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_17_column_73 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_17_column_74 el-table__cell"><div class="cell">Morgan</div></td><td colspan="1" rowspan="1" class="el-table_17_column_75 is-right el-table__cell"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--small"><span class="">Edit </span></button><button aria-disabled="false" type="button" class="el-button el-button--danger el-button--small"><span class="">Delete</span></button></div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_17_column_73 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_17_column_74 el-table__cell"><div class="cell">Jessy</div></td><td colspan="1" rowspan="1" class="el-table_17_column_75 is-right el-table__cell"><div class="cell"><button aria-disabled="false" type="button" class="el-button el-button--small"><span class="">Edit </span></button><button aria-disabled="false" type="button" class="el-button el-button--danger el-button--small"><span class="">Delete</span></button></div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJmaWx0ZXJUYWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCI+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBsYWJlbD1cIkRhdGVcIiBwcm9wPVwiZGF0ZVwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBsYWJlbD1cIk5hbWVcIiBwcm9wPVwibmFtZVwiIC8+XG4gICAgPCEtLSBAdnVlLWdlbmVyaWMge1VzZXJ9IC0tPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gYWxpZ249XCJyaWdodFwiPlxuICAgICAgPHRlbXBsYXRlICNoZWFkZXI+XG4gICAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwic2VhcmNoXCIgc2l6ZT1cInNtYWxsXCIgcGxhY2Vob2xkZXI9XCJUeXBlIHRvIHNlYXJjaFwiIC8+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgPHRlbXBsYXRlICNkZWZhdWx0PVwic2NvcGVcIj5cbiAgICAgICAgPGVsLWJ1dHRvbiBzaXplPVwic21hbGxcIiBAY2xpY2s9XCJoYW5kbGVFZGl0KHNjb3BlLiRpbmRleCwgc2NvcGUucm93KVwiPlxuICAgICAgICAgIEVkaXRcbiAgICAgICAgPC9lbC1idXR0b24+XG4gICAgICAgIDxlbC1idXR0b25cbiAgICAgICAgICBzaXplPVwic21hbGxcIlxuICAgICAgICAgIHR5cGU9XCJkYW5nZXJcIlxuICAgICAgICAgIEBjbGljaz1cImhhbmRsZURlbGV0ZShzY29wZS4kaW5kZXgsIHNjb3BlLnJvdylcIlxuICAgICAgICA+XG4gICAgICAgICAgRGVsZXRlXG4gICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLXRhYmxlLWNvbHVtbj5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBjb21wdXRlZCwgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbnRlcmZhY2UgVXNlciB7XG4gIGRhdGU6IHN0cmluZ1xuICBuYW1lOiBzdHJpbmdcbiAgYWRkcmVzczogc3RyaW5nXG59XG5cbmNvbnN0IHNlYXJjaCA9IHJlZignJylcbmNvbnN0IGZpbHRlclRhYmxlRGF0YSA9IGNvbXB1dGVkKCgpID0+XG4gIHRhYmxlRGF0YS5maWx0ZXIoXG4gICAgKGRhdGEpID0+XG4gICAgICAhc2VhcmNoLnZhbHVlIHx8XG4gICAgICBkYXRhLm5hbWUudG9Mb3dlckNhc2UoKS5pbmNsdWRlcyhzZWFyY2gudmFsdWUudG9Mb3dlckNhc2UoKSlcbiAgKVxuKVxuY29uc3QgaGFuZGxlRWRpdCA9IChpbmRleDogbnVtYmVyLCByb3c6IFVzZXIpID0+IHtcbiAgY29uc29sZS5sb2coaW5kZXgsIHJvdylcbn1cbmNvbnN0IGhhbmRsZURlbGV0ZSA9IChpbmRleDogbnVtYmVyLCByb3c6IFVzZXIpID0+IHtcbiAgY29uc29sZS5sb2coaW5kZXgsIHJvdylcbn1cblxuY29uc3QgdGFibGVEYXRhOiBVc2VyW10gPSBbXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMicsXG4gICAgbmFtZTogJ0pvaG4nLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDQnLFxuICAgIG5hbWU6ICdNb3JnYW4nLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgIG5hbWU6ICdKZXNzeScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/custom-header.vue)_

vue

```
<template>
  <el-table :data="filterTableData" style="width: 100%">
    <el-table-column label="Date" prop="date" />
    <el-table-column label="Name" prop="name" />
    <!-- @vue-generic {User} -->
    <el-table-column align="right">
      <template #header>
        <el-input v-model="search" size="small" placeholder="Type to search" />
      </template>
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
          Edit
        </el-button>
        <el-button
          size="small"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)"
        >
          Delete
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'

interface User {
  date: string
  name: string
  address: string
}

const search = ref('')
const filterTableData = computed(() =>
  tableData.filter(
    (data) =>
      !search.value ||
      data.name.toLowerCase().includes(search.value.toLowerCase())
  )
)
const handleEdit = (index: number, row: User) => {
  console.log(index, row)
}
const handleDelete = (index: number, row: User) => {
  console.log(index, row)
}

const tableData: User[] = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-02',
    name: 'John',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-04',
    name: 'Morgan',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2016-05-01',
    name: 'Jessy',
    address: 'No. 189, Grove St, Los Angeles',
  },
]
</script>
```

隐藏源代码

## 展开行 [​](#展开行)

当行内容过多并且不想显示横向滚动条时，可以使用 Table 展开行功能。

在 2.9.7 版本后，新增了 `preserve-expanded-content` 属性，用于控制折叠时是否在 DOM 中保留已展开的行内容。

通过设置 type="expand" 和 slot 可以开启展开行功能， el-table-column 的模板会被渲染成为展开行的内容，展开行可访问的属性与使用自定义列模板时的 slot 相同。

switch parent border:

switch child border:

preserve expanded:

|
 |

Date

 |

Name

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_18_column_76" width="48"><col name="el-table_18_column_77" width="423"><col name="el-table_18_column_78" width="422"></colgroup><tbody tabindex="-1"><tr class="el-table__row"><td colspan="1" rowspan="1" class="el-table_18_column_76 el-table__expand-column el-table__cell"><div class="cell"><button type="button" aria-label="Expand this row" aria-expanded="false" class="el-table__expand-icon"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></button></div></td><td colspan="1" rowspan="1" class="el-table_18_column_77 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_18_column_78 el-table__cell"><div class="cell">Tom</div></td></tr><tr class="el-table__row"><td colspan="1" rowspan="1" class="el-table_18_column_76 el-table__expand-column el-table__cell"><div class="cell"><button type="button" aria-label="Expand this row" aria-expanded="false" class="el-table__expand-icon"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></button></div></td><td colspan="1" rowspan="1" class="el-table_18_column_77 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_18_column_78 el-table__cell"><div class="cell">Tom</div></td></tr><tr class="el-table__row"><td colspan="1" rowspan="1" class="el-table_18_column_76 el-table__expand-column el-table__cell"><div class="cell"><button type="button" aria-label="Expand this row" aria-expanded="false" class="el-table__expand-icon"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></button></div></td><td colspan="1" rowspan="1" class="el-table_18_column_77 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_18_column_78 el-table__cell"><div class="cell">Tom</div></td></tr><tr class="el-table__row"><td colspan="1" rowspan="1" class="el-table_18_column_76 el-table__expand-column el-table__cell"><div class="cell"><button type="button" aria-label="Expand this row" aria-expanded="false" class="el-table__expand-icon"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></button></div></td><td colspan="1" rowspan="1" class="el-table_18_column_77 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_18_column_78 el-table__cell"><div class="cell">Tom</div></td></tr><tr class="el-table__row"><td colspan="1" rowspan="1" class="el-table_18_column_76 el-table__expand-column el-table__cell"><div class="cell"><button type="button" aria-label="Expand this row" aria-expanded="false" class="el-table__expand-icon"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></button></div></td><td colspan="1" rowspan="1" class="el-table_18_column_77 el-table__cell"><div class="cell">2016-05-08</div></td><td colspan="1" rowspan="1" class="el-table_18_column_78 el-table__cell"><div class="cell">Tom</div></td></tr><tr class="el-table__row"><td colspan="1" rowspan="1" class="el-table_18_column_76 el-table__expand-column el-table__cell"><div class="cell"><button type="button" aria-label="Expand this row" aria-expanded="false" class="el-table__expand-icon"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></button></div></td><td colspan="1" rowspan="1" class="el-table_18_column_77 el-table__cell"><div class="cell">2016-05-06</div></td><td colspan="1" rowspan="1" class="el-table_18_column_78 el-table__cell"><div class="cell">Tom</div></td></tr><tr class="el-table__row"><td colspan="1" rowspan="1" class="el-table_18_column_76 el-table__expand-column el-table__cell"><div class="cell"><button type="button" aria-label="Expand this row" aria-expanded="false" class="el-table__expand-icon"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></button></div></td><td colspan="1" rowspan="1" class="el-table_18_column_77 el-table__cell"><div class="cell">2016-05-07</div></td><td colspan="1" rowspan="1" class="el-table_18_column_78 el-table__cell"><div class="cell">Tom</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICBzd2l0Y2ggcGFyZW50IGJvcmRlcjogPGVsLXN3aXRjaCB2LW1vZGVsPVwicGFyZW50Qm9yZGVyXCIgLz4gc3dpdGNoIGNoaWxkXG4gIGJvcmRlcjogPGVsLXN3aXRjaCB2LW1vZGVsPVwiY2hpbGRCb3JkZXJcIiAvPiBwcmVzZXJ2ZSBleHBhbmRlZDpcbiAgPGVsLXN3aXRjaCB2LW1vZGVsPVwicHJlc2VydmVFeHBhbmRlZFwiIC8+XG4gIDxlbC10YWJsZVxuICAgIDpkYXRhPVwidGFibGVEYXRhXCJcbiAgICA6Ym9yZGVyPVwicGFyZW50Qm9yZGVyXCJcbiAgICA6cHJlc2VydmUtZXhwYW5kZWQtY29udGVudD1cInByZXNlcnZlRXhwYW5kZWRcIlxuICAgIHN0eWxlPVwid2lkdGg6IDEwMCVcIlxuICA+XG4gICAgPCEtLSBAdnVlLWdlbmVyaWMge3R5cGVvZiB0YWJsZURhdGFbbnVtYmVyXX0gLS0+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiB0eXBlPVwiZXhwYW5kXCI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJwcm9wc1wiPlxuICAgICAgICA8ZGl2IG09XCI0XCI+XG4gICAgICAgICAgPHAgbT1cInQtMCBiLTJcIj5TdGF0ZToge3sgcHJvcHMucm93LnN0YXRlIH19PC9wPlxuICAgICAgICAgIDxwIG09XCJ0LTAgYi0yXCI+Q2l0eToge3sgcHJvcHMucm93LmNpdHkgfX08L3A+XG4gICAgICAgICAgPHAgbT1cInQtMCBiLTJcIj5BZGRyZXNzOiB7eyBwcm9wcy5yb3cuYWRkcmVzcyB9fTwvcD5cbiAgICAgICAgICA8cCBtPVwidC0wIGItMlwiPlppcDoge3sgcHJvcHMucm93LnppcCB9fTwvcD5cbiAgICAgICAgICA8aDM+RmFtaWx5PC9oMz5cbiAgICAgICAgICA8ZWwtdGFibGUgOmRhdGE9XCJwcm9wcy5yb3cuZmFtaWx5XCIgOmJvcmRlcj1cImNoaWxkQm9yZGVyXCI+XG4gICAgICAgICAgICA8ZWwtdGFibGUtY29sdW1uIGxhYmVsPVwiTmFtZVwiIHByb3A9XCJuYW1lXCIgLz5cbiAgICAgICAgICAgIDxlbC10YWJsZS1jb2x1bW4gbGFiZWw9XCJTdGF0ZVwiIHByb3A9XCJzdGF0ZVwiIC8+XG4gICAgICAgICAgICA8ZWwtdGFibGUtY29sdW1uIGxhYmVsPVwiQ2l0eVwiIHByb3A9XCJjaXR5XCIgLz5cbiAgICAgICAgICAgIDxlbC10YWJsZS1jb2x1bW4gbGFiZWw9XCJBZGRyZXNzXCIgcHJvcD1cImFkZHJlc3NcIiAvPlxuICAgICAgICAgICAgPGVsLXRhYmxlLWNvbHVtbiBsYWJlbD1cIlppcFwiIHByb3A9XCJ6aXBcIiAvPlxuICAgICAgICAgIDwvZWwtdGFibGU+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLXRhYmxlLWNvbHVtbj5cbiAgICA8ZWwtdGFibGUtY29sdW1uIGxhYmVsPVwiRGF0ZVwiIHByb3A9XCJkYXRlXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIGxhYmVsPVwiTmFtZVwiIHByb3A9XCJuYW1lXCIgLz5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHBhcmVudEJvcmRlciA9IHJlZihmYWxzZSlcbmNvbnN0IGNoaWxkQm9yZGVyID0gcmVmKGZhbHNlKVxuY29uc3QgcHJlc2VydmVFeHBhbmRlZCA9IHJlZihmYWxzZSlcbmNvbnN0IHRhYmxlRGF0YSA9IFtcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAzJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICBhZGRyZXNzOiAnMzY1MCAyMXN0IFN0LCBTYW4gRnJhbmNpc2NvJyxcbiAgICB6aXA6ICdDQSA5NDExNCcsXG4gICAgZmFtaWx5OiBbXG4gICAgICB7XG4gICAgICAgIG5hbWU6ICdKZXJyeScsXG4gICAgICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgYWRkcmVzczogJzM2NTAgMjFzdCBTdCwgU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIHppcDogJ0NBIDk0MTE0JyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIG5hbWU6ICdTcGlrZScsXG4gICAgICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgYWRkcmVzczogJzM2NTAgMjFzdCBTdCwgU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIHppcDogJ0NBIDk0MTE0JyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIG5hbWU6ICdUeWtlJyxcbiAgICAgICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICAgICAgY2l0eTogJ1NhbiBGcmFuY2lzY28nLFxuICAgICAgICBhZGRyZXNzOiAnMzY1MCAyMXN0IFN0LCBTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgemlwOiAnQ0EgOTQxMTQnLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDInLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ1NhbiBGcmFuY2lzY28nLFxuICAgIGFkZHJlc3M6ICczNjUwIDIxc3QgU3QsIFNhbiBGcmFuY2lzY28nLFxuICAgIHppcDogJ0NBIDk0MTE0JyxcbiAgICBmYW1pbHk6IFtcbiAgICAgIHtcbiAgICAgICAgbmFtZTogJ0plcnJ5JyxcbiAgICAgICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICAgICAgY2l0eTogJ1NhbiBGcmFuY2lzY28nLFxuICAgICAgICBhZGRyZXNzOiAnMzY1MCAyMXN0IFN0LCBTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgemlwOiAnQ0EgOTQxMTQnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgbmFtZTogJ1NwaWtlJyxcbiAgICAgICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICAgICAgY2l0eTogJ1NhbiBGcmFuY2lzY28nLFxuICAgICAgICBhZGRyZXNzOiAnMzY1MCAyMXN0IFN0LCBTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgemlwOiAnQ0EgOTQxMTQnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgbmFtZTogJ1R5a2UnLFxuICAgICAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgICAgICBjaXR5OiAnU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIGFkZHJlc3M6ICczNjUwIDIxc3QgU3QsIFNhbiBGcmFuY2lzY28nLFxuICAgICAgICB6aXA6ICdDQSA5NDExNCcsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnU2FuIEZyYW5jaXNjbycsXG4gICAgYWRkcmVzczogJzM2NTAgMjFzdCBTdCwgU2FuIEZyYW5jaXNjbycsXG4gICAgemlwOiAnQ0EgOTQxMTQnLFxuICAgIGZhbWlseTogW1xuICAgICAge1xuICAgICAgICBuYW1lOiAnSmVycnknLFxuICAgICAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgICAgICBjaXR5OiAnU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIGFkZHJlc3M6ICczNjUwIDIxc3QgU3QsIFNhbiBGcmFuY2lzY28nLFxuICAgICAgICB6aXA6ICdDQSA5NDExNCcsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBuYW1lOiAnU3Bpa2UnLFxuICAgICAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgICAgICBjaXR5OiAnU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIGFkZHJlc3M6ICczNjUwIDIxc3QgU3QsIFNhbiBGcmFuY2lzY28nLFxuICAgICAgICB6aXA6ICdDQSA5NDExNCcsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBuYW1lOiAnVHlrZScsXG4gICAgICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgYWRkcmVzczogJzM2NTAgMjFzdCBTdCwgU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIHppcDogJ0NBIDk0MTE0JyxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICBhZGRyZXNzOiAnMzY1MCAyMXN0IFN0LCBTYW4gRnJhbmNpc2NvJyxcbiAgICB6aXA6ICdDQSA5NDExNCcsXG4gICAgZmFtaWx5OiBbXG4gICAgICB7XG4gICAgICAgIG5hbWU6ICdKZXJyeScsXG4gICAgICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgYWRkcmVzczogJzM2NTAgMjFzdCBTdCwgU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIHppcDogJ0NBIDk0MTE0JyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIG5hbWU6ICdTcGlrZScsXG4gICAgICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgYWRkcmVzczogJzM2NTAgMjFzdCBTdCwgU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIHppcDogJ0NBIDk0MTE0JyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIG5hbWU6ICdUeWtlJyxcbiAgICAgICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICAgICAgY2l0eTogJ1NhbiBGcmFuY2lzY28nLFxuICAgICAgICBhZGRyZXNzOiAnMzY1MCAyMXN0IFN0LCBTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgemlwOiAnQ0EgOTQxMTQnLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDgnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ1NhbiBGcmFuY2lzY28nLFxuICAgIGFkZHJlc3M6ICczNjUwIDIxc3QgU3QsIFNhbiBGcmFuY2lzY28nLFxuICAgIHppcDogJ0NBIDk0MTE0JyxcbiAgICBmYW1pbHk6IFtcbiAgICAgIHtcbiAgICAgICAgbmFtZTogJ0plcnJ5JyxcbiAgICAgICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICAgICAgY2l0eTogJ1NhbiBGcmFuY2lzY28nLFxuICAgICAgICBhZGRyZXNzOiAnMzY1MCAyMXN0IFN0LCBTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgemlwOiAnQ0EgOTQxMTQnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgbmFtZTogJ1NwaWtlJyxcbiAgICAgICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICAgICAgY2l0eTogJ1NhbiBGcmFuY2lzY28nLFxuICAgICAgICBhZGRyZXNzOiAnMzY1MCAyMXN0IFN0LCBTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgemlwOiAnQ0EgOTQxMTQnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgbmFtZTogJ1R5a2UnLFxuICAgICAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgICAgICBjaXR5OiAnU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIGFkZHJlc3M6ICczNjUwIDIxc3QgU3QsIFNhbiBGcmFuY2lzY28nLFxuICAgICAgICB6aXA6ICdDQSA5NDExNCcsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnU2FuIEZyYW5jaXNjbycsXG4gICAgYWRkcmVzczogJzM2NTAgMjFzdCBTdCwgU2FuIEZyYW5jaXNjbycsXG4gICAgemlwOiAnQ0EgOTQxMTQnLFxuICAgIGZhbWlseTogW1xuICAgICAge1xuICAgICAgICBuYW1lOiAnSmVycnknLFxuICAgICAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgICAgICBjaXR5OiAnU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIGFkZHJlc3M6ICczNjUwIDIxc3QgU3QsIFNhbiBGcmFuY2lzY28nLFxuICAgICAgICB6aXA6ICdDQSA5NDExNCcsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBuYW1lOiAnU3Bpa2UnLFxuICAgICAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgICAgICBjaXR5OiAnU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIGFkZHJlc3M6ICczNjUwIDIxc3QgU3QsIFNhbiBGcmFuY2lzY28nLFxuICAgICAgICB6aXA6ICdDQSA5NDExNCcsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBuYW1lOiAnVHlrZScsXG4gICAgICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgYWRkcmVzczogJzM2NTAgMjFzdCBTdCwgU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIHppcDogJ0NBIDk0MTE0JyxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA3JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBzdGF0ZTogJ0NhbGlmb3JuaWEnLFxuICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICBhZGRyZXNzOiAnMzY1MCAyMXN0IFN0LCBTYW4gRnJhbmNpc2NvJyxcbiAgICB6aXA6ICdDQSA5NDExNCcsXG4gICAgZmFtaWx5OiBbXG4gICAgICB7XG4gICAgICAgIG5hbWU6ICdKZXJyeScsXG4gICAgICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgYWRkcmVzczogJzM2NTAgMjFzdCBTdCwgU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIHppcDogJ0NBIDk0MTE0JyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIG5hbWU6ICdTcGlrZScsXG4gICAgICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgICAgIGNpdHk6ICdTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgYWRkcmVzczogJzM2NTAgMjFzdCBTdCwgU2FuIEZyYW5jaXNjbycsXG4gICAgICAgIHppcDogJ0NBIDk0MTE0JyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIG5hbWU6ICdUeWtlJyxcbiAgICAgICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICAgICAgY2l0eTogJ1NhbiBGcmFuY2lzY28nLFxuICAgICAgICBhZGRyZXNzOiAnMzY1MCAyMXN0IFN0LCBTYW4gRnJhbmNpc2NvJyxcbiAgICAgICAgemlwOiAnQ0EgOTQxMTQnLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/expandable-row.vue)_

vue

```
<template>
  switch parent border: <el-switch v-model="parentBorder" /> switch child
  border: <el-switch v-model="childBorder" /> preserve expanded:
  <el-switch v-model="preserveExpanded" />
  <el-table
    :data="tableData"
    :border="parentBorder"
    :preserve-expanded-content="preserveExpanded"
    style="width: 100%"
  >
    <!-- @vue-generic {typeof tableData[number]} -->
    <el-table-column type="expand">
      <template #default="props">
        <div m="4">
          <p m="t-0 b-2">State: {{ props.row.state }}</p>
          <p m="t-0 b-2">City: {{ props.row.city }}</p>
          <p m="t-0 b-2">Address: {{ props.row.address }}</p>
          <p m="t-0 b-2">Zip: {{ props.row.zip }}</p>
          <h3>Family</h3>
          <el-table :data="props.row.family" :border="childBorder">
            <el-table-column label="Name" prop="name" />
            <el-table-column label="State" prop="state" />
            <el-table-column label="City" prop="city" />
            <el-table-column label="Address" prop="address" />
            <el-table-column label="Zip" prop="zip" />
          </el-table>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="Date" prop="date" />
    <el-table-column label="Name" prop="name" />
  </el-table>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const parentBorder = ref(false)
const childBorder = ref(false)
const preserveExpanded = ref(false)
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    state: 'California',
    city: 'San Francisco',
    address: '3650 21st St, San Francisco',
    zip: 'CA 94114',
    family: [
      {
        name: 'Jerry',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Spike',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Tyke',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
    ],
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    state: 'California',
    city: 'San Francisco',
    address: '3650 21st St, San Francisco',
    zip: 'CA 94114',
    family: [
      {
        name: 'Jerry',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Spike',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Tyke',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
    ],
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    state: 'California',
    city: 'San Francisco',
    address: '3650 21st St, San Francisco',
    zip: 'CA 94114',
    family: [
      {
        name: 'Jerry',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Spike',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Tyke',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
    ],
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    state: 'California',
    city: 'San Francisco',
    address: '3650 21st St, San Francisco',
    zip: 'CA 94114',
    family: [
      {
        name: 'Jerry',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Spike',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Tyke',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
    ],
  },
  {
    date: '2016-05-08',
    name: 'Tom',
    state: 'California',
    city: 'San Francisco',
    address: '3650 21st St, San Francisco',
    zip: 'CA 94114',
    family: [
      {
        name: 'Jerry',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Spike',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Tyke',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
    ],
  },
  {
    date: '2016-05-06',
    name: 'Tom',
    state: 'California',
    city: 'San Francisco',
    address: '3650 21st St, San Francisco',
    zip: 'CA 94114',
    family: [
      {
        name: 'Jerry',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Spike',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Tyke',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
    ],
  },
  {
    date: '2016-05-07',
    name: 'Tom',
    state: 'California',
    city: 'San Francisco',
    address: '3650 21st St, San Francisco',
    zip: 'CA 94114',
    family: [
      {
        name: 'Jerry',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Spike',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
      {
        name: 'Tyke',
        state: 'California',
        city: 'San Francisco',
        address: '3650 21st St, San Francisco',
        zip: 'CA 94114',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 树形数据与懒加载 [​](#树形数据与懒加载)

支持树类型的数据的显示。 当 row 中包含 `children` 字段时，被视为树形数据。 渲染嵌套数据需要 prop 的 `row-key`。 此外，子行数据可以异步加载。 设置 Table 的`lazy`属性为 true 与加载函数 `load` 。 通过指定 row 中的`hasChildren`字段来指定哪些行是包含子节点。 `children` 与`hasChildren`都可以通过 `tree-props` 配置。

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_19_column_79" width="299"><col name="el-table_19_column_80" width="297"><col name="el-table_19_column_81" width="297"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_19_column_79 el-table__cell"><div class="cell"><span class="el-table__placeholder"></span>2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_19_column_80 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_19_column_81 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_19_column_79 el-table__cell"><div class="cell"><span class="el-table__placeholder"></span>2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_19_column_80 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_19_column_81 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row--level-0 el-table__row"><td colspan="1" rowspan="1" class="el-table_19_column_79 el-table__cell"><div class="cell"><button type="button" aria-label="Collapse this row" aria-expanded="true" class="el-table__expand-icon el-table__expand-icon--expanded"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></button>2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_19_column_80 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_19_column_81 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row--level-1 el-table__row"><td colspan="1" rowspan="1" class="el-table_19_column_79 el-table__cell"><div class="cell"><span class="el-table__indent" style="padding-left: 16px;"></span><span class="el-table__placeholder"></span>2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_19_column_80 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_19_column_81 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row--level-1 el-table__row"><td colspan="1" rowspan="1" class="el-table_19_column_79 el-table__cell"><div class="cell"><span class="el-table__indent" style="padding-left: 16px;"></span><span class="el-table__placeholder"></span>2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_19_column_80 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_19_column_81 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_19_column_79 el-table__cell"><div class="cell"><span class="el-table__placeholder"></span>2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_19_column_80 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_19_column_81 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_20_column_82" width="299"><col name="el-table_20_column_83" width="297"><col name="el-table_20_column_84" width="297"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_20_column_82 el-table__cell"><div class="cell"><span class="el-table__placeholder"></span>2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_20_column_83 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_20_column_84 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_20_column_82 el-table__cell"><div class="cell"><span class="el-table__placeholder"></span>2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_20_column_83 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_20_column_84 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row--level-0 el-table__row"><td colspan="1" rowspan="1" class="el-table_20_column_82 el-table__cell"><div class="cell"><button type="button" aria-label="Expand this row" aria-expanded="false" class="el-table__expand-icon"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></button>2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_20_column_83 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_20_column_84 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_20_column_82 el-table__cell"><div class="cell"><span class="el-table__placeholder"></span>2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_20_column_83 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_20_column_84 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC10YWJsZVxuICAgICAgOmRhdGE9XCJ0YWJsZURhdGFcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMTAwJTsgbWFyZ2luLWJvdHRvbTogMjBweFwiXG4gICAgICByb3cta2V5PVwiaWRcIlxuICAgICAgYm9yZGVyXG4gICAgICBkZWZhdWx0LWV4cGFuZC1hbGxcbiAgICA+XG4gICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJkYXRlXCIgbGFiZWw9XCJEYXRlXCIgc29ydGFibGUgLz5cbiAgICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cIm5hbWVcIiBsYWJlbD1cIk5hbWVcIiBzb3J0YWJsZSAvPlxuICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiYWRkcmVzc1wiIGxhYmVsPVwiQWRkcmVzc1wiIHNvcnRhYmxlIC8+XG4gICAgPC9lbC10YWJsZT5cblxuICAgIDxlbC10YWJsZVxuICAgICAgOmRhdGE9XCJ0YWJsZURhdGExXCJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDEwMCVcIlxuICAgICAgcm93LWtleT1cImlkXCJcbiAgICAgIGJvcmRlclxuICAgICAgbGF6eVxuICAgICAgOmxvYWQ9XCJsb2FkXCJcbiAgICAgIDp0cmVlLXByb3BzPVwieyBjaGlsZHJlbjogJ2NoaWxkcmVuJywgaGFzQ2hpbGRyZW46ICdoYXNDaGlsZHJlbicgfVwiXG4gICAgPlxuICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIC8+XG4gICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgLz5cbiAgICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiAvPlxuICAgIDwvZWwtdGFibGU+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmludGVyZmFjZSBVc2VyIHtcbiAgaWQ6IG51bWJlclxuICBkYXRlOiBzdHJpbmdcbiAgbmFtZTogc3RyaW5nXG4gIGFkZHJlc3M6IHN0cmluZ1xuICBoYXNDaGlsZHJlbj86IGJvb2xlYW5cbiAgY2hpbGRyZW4/OiBVc2VyW11cbn1cblxuY29uc3QgbG9hZCA9IChcbiAgcm93OiBVc2VyLFxuICB0cmVlTm9kZTogdW5rbm93bixcbiAgcmVzb2x2ZTogKGRhdGE6IFVzZXJbXSkgPT4gdm9pZFxuKSA9PiB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIHJlc29sdmUoW1xuICAgICAge1xuICAgICAgICBpZDogMzEsXG4gICAgICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICAgICAgbmFtZTogJ3dhbmd4aWFvaHUnLFxuICAgICAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiAzMixcbiAgICAgICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgICAgICBuYW1lOiAnd2FuZ3hpYW9odScsXG4gICAgICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgICAgfSxcbiAgICBdKVxuICB9LCAxMDAwKVxufVxuXG5jb25zdCB0YWJsZURhdGE6IFVzZXJbXSA9IFtcbiAge1xuICAgIGlkOiAxLFxuICAgIGRhdGU6ICcyMDE2LTA1LTAyJyxcbiAgICBuYW1lOiAnd2FuZ3hpYW9odScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBpZDogMixcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ3dhbmd4aWFvaHUnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgaWQ6IDMsXG4gICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgIG5hbWU6ICd3YW5neGlhb2h1JyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICBpZDogMzEsXG4gICAgICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICAgICAgbmFtZTogJ3dhbmd4aWFvaHUnLFxuICAgICAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiAzMixcbiAgICAgICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgICAgICBuYW1lOiAnd2FuZ3hpYW9odScsXG4gICAgICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgaWQ6IDQsXG4gICAgZGF0ZTogJzIwMTYtMDUtMDMnLFxuICAgIG5hbWU6ICd3YW5neGlhb2h1JyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbl1cblxuY29uc3QgdGFibGVEYXRhMTogVXNlcltdID0gW1xuICB7XG4gICAgaWQ6IDEsXG4gICAgZGF0ZTogJzIwMTYtMDUtMDInLFxuICAgIG5hbWU6ICd3YW5neGlhb2h1JyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGlkOiAyLFxuICAgIGRhdGU6ICcyMDE2LTA1LTA0JyxcbiAgICBuYW1lOiAnd2FuZ3hpYW9odScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBpZDogMyxcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ3dhbmd4aWFvaHUnLFxuICAgIGhhc0NoaWxkcmVuOiB0cnVlLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgaWQ6IDQsXG4gICAgZGF0ZTogJzIwMTYtMDUtMDMnLFxuICAgIG5hbWU6ICd3YW5neGlhb2h1JyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/tree-and-lazy.vue)_

vue

```
<template>
  <div>
    <el-table
      :data="tableData"
      style="width: 100%; margin-bottom: 20px"
      row-key="id"
      border
      default-expand-all
    >
      <el-table-column prop="date" label="Date" sortable />
      <el-table-column prop="name" label="Name" sortable />
      <el-table-column prop="address" label="Address" sortable />
    </el-table>

    <el-table
      :data="tableData1"
      style="width: 100%"
      row-key="id"
      border
      lazy
      :load="load"
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
    >
      <el-table-column prop="date" label="Date" />
      <el-table-column prop="name" label="Name" />
      <el-table-column prop="address" label="Address" />
    </el-table>
  </div>
</template>

<script lang="ts" setup>
interface User {
  id: number
  date: string
  name: string
  address: string
  hasChildren?: boolean
  children?: User[]
}

const load = (
  row: User,
  treeNode: unknown,
  resolve: (data: User[]) => void
) => {
  setTimeout(() => {
    resolve([
      {
        id: 31,
        date: '2016-05-01',
        name: 'wangxiaohu',
        address: 'No. 189, Grove St, Los Angeles',
      },
      {
        id: 32,
        date: '2016-05-01',
        name: 'wangxiaohu',
        address: 'No. 189, Grove St, Los Angeles',
      },
    ])
  }, 1000)
}

const tableData: User[] = [
  {
    id: 1,
    date: '2016-05-02',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 2,
    date: '2016-05-04',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 3,
    date: '2016-05-01',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
    children: [
      {
        id: 31,
        date: '2016-05-01',
        name: 'wangxiaohu',
        address: 'No. 189, Grove St, Los Angeles',
      },
      {
        id: 32,
        date: '2016-05-01',
        name: 'wangxiaohu',
        address: 'No. 189, Grove St, Los Angeles',
      },
    ],
  },
  {
    id: 4,
    date: '2016-05-03',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
  },
]

const tableData1: User[] = [
  {
    id: 1,
    date: '2016-05-02',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 2,
    date: '2016-05-04',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 3,
    date: '2016-05-01',
    name: 'wangxiaohu',
    hasChildren: true,
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 4,
    date: '2016-05-03',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
  },
]
</script>
```

隐藏源代码

## 可选择的树形数据2.8.0 [​](#可选择的树形数据)

当 `treeProps.checkStrictly` 为 true，父节点和子节点的选择状态不再关联， 也就是说，当选择父节点时，它的子节点将不被选择； 当 `treeProps.checkStrictly` 是false，父节点和子节点的选择状态将与子节点的选择状态相关联， 也就是说，当选择父节点时，将选择其所有子节点。

truefalse

|
 |

Date

 |

Name

 |

Address

 |
| --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_21_column_85" width="55"><col name="el-table_21_column_86" width="280"><col name="el-table_21_column_87" width="279"><col name="el-table_21_column_88" width="279"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_21_column_85 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox is-disabled" aria-label="Select this row" for="el-id-1024-391"><span class="el-checkbox__input is-disabled"><input class="el-checkbox__original" type="checkbox" disabled="" id="el-id-1024-391"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_21_column_86 el-table__cell"><div class="cell"><span class="el-table__placeholder"></span>2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_21_column_87 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_21_column_88 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_21_column_85 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-392"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-392"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_21_column_86 el-table__cell"><div class="cell"><span class="el-table__placeholder"></span>2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_21_column_87 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_21_column_88 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row--level-0 el-table__row"><td colspan="1" rowspan="1" class="el-table_21_column_85 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-393"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-393"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_21_column_86 el-table__cell"><div class="cell"><button type="button" aria-label="Collapse this row" aria-expanded="true" class="el-table__expand-icon el-table__expand-icon--expanded"><i class="el-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg></i></button>2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_21_column_87 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_21_column_88 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row--level-1 el-table__row"><td colspan="1" rowspan="1" class="el-table_21_column_85 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox is-disabled" aria-label="Select this row" for="el-id-1024-394"><span class="el-checkbox__input is-disabled"><input class="el-checkbox__original" type="checkbox" disabled="" id="el-id-1024-394"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_21_column_86 el-table__cell"><div class="cell"><span class="el-table__indent" style="padding-left: 16px;"></span><span class="el-table__placeholder"></span>2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_21_column_87 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_21_column_88 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row--level-1 el-table__row"><td colspan="1" rowspan="1" class="el-table_21_column_85 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-395"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-395"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_21_column_86 el-table__cell"><div class="cell"><span class="el-table__indent" style="padding-left: 16px;"></span><span class="el-table__placeholder"></span>2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_21_column_87 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_21_column_88 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row--level-1 el-table__row"><td colspan="1" rowspan="1" class="el-table_21_column_85 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-396"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-396"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_21_column_86 el-table__cell"><div class="cell"><span class="el-table__indent" style="padding-left: 16px;"></span><span class="el-table__placeholder"></span>2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_21_column_87 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_21_column_88 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_21_column_85 el-table-column--selection el-table__cell"><div class="cell"><label class="el-checkbox" aria-label="Select this row" for="el-id-1024-397"><span class="el-checkbox__input"><input class="el-checkbox__original" type="checkbox" id="el-id-1024-397"><span class="el-checkbox__inner"></span></span></label></div></td><td colspan="1" rowspan="1" class="el-table_21_column_86 el-table__cell"><div class="cell"><span class="el-table__placeholder"></span>2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_21_column_87 el-table__cell"><div class="cell">wangxiaohu</div></td><td colspan="1" rowspan="1" class="el-table_21_column_88 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInRyZWVQcm9wcy5jaGVja1N0cmljdGx5XCIgY2xhc3M9XCJtYi0yXCI+XG4gICAgPGVsLXJhZGlvLWJ1dHRvbiA6dmFsdWU9XCJ0cnVlXCIgbGFiZWw9XCJ0cnVlXCIgLz5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIDp2YWx1ZT1cImZhbHNlXCIgbGFiZWw9XCJmYWxzZVwiIC8+XG4gIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDxlbC10YWJsZVxuICAgIDpkYXRhPVwidGFibGVEYXRhXCJcbiAgICA6dHJlZS1wcm9wcz1cInRyZWVQcm9wc1wiXG4gICAgcm93LWtleT1cImlkXCJcbiAgICBkZWZhdWx0LWV4cGFuZC1hbGxcbiAgPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gdHlwZT1cInNlbGVjdGlvblwiIHdpZHRoPVwiNTVcIiA6c2VsZWN0YWJsZT1cInNlbGVjdGFibGVcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImRhdGVcIiBsYWJlbD1cIkRhdGVcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cIm5hbWVcIiBsYWJlbD1cIk5hbWVcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiAvPlxuICA8L2VsLXRhYmxlPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlYWN0aXZlIH0gZnJvbSAndnVlJ1xuXG5pbnRlcmZhY2UgVXNlciB7XG4gIGlkOiBudW1iZXJcbiAgZGF0ZTogc3RyaW5nXG4gIG5hbWU6IHN0cmluZ1xuICBhZGRyZXNzOiBzdHJpbmdcbiAgaGFzQ2hpbGRyZW4/OiBib29sZWFuXG4gIGNoaWxkcmVuPzogVXNlcltdXG59XG5cbmNvbnN0IHRyZWVQcm9wcyA9IHJlYWN0aXZlKHtcbiAgY2hlY2tTdHJpY3RseTogZmFsc2UsXG59KVxuXG5jb25zdCBzZWxlY3RhYmxlID0gKHJvdzogVXNlcikgPT4gIVsxLCAzMV0uaW5jbHVkZXMocm93LmlkKVxuXG5jb25zdCB0YWJsZURhdGE6IFVzZXJbXSA9IFtcbiAge1xuICAgIGlkOiAxLFxuICAgIGRhdGU6ICcyMDE2LTA1LTAyJyxcbiAgICBuYW1lOiAnd2FuZ3hpYW9odScsXG4gICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gIH0sXG4gIHtcbiAgICBpZDogMixcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ3dhbmd4aWFvaHUnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuICB7XG4gICAgaWQ6IDMsXG4gICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgIG5hbWU6ICd3YW5neGlhb2h1JyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICBpZDogMzEsXG4gICAgICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICAgICAgbmFtZTogJ3dhbmd4aWFvaHUnLFxuICAgICAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGlkOiAzMixcbiAgICAgICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgICAgICBuYW1lOiAnd2FuZ3hpYW9odScsXG4gICAgICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgaWQ6IDMzLFxuICAgICAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgICAgIG5hbWU6ICd3YW5neGlhb2h1JyxcbiAgICAgICAgYWRkcmVzczogJ05vLiAxODksIEdyb3ZlIFN0LCBMb3MgQW5nZWxlcycsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICBpZDogNCxcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ3dhbmd4aWFvaHUnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/check-strictly.vue)_

vue

```
<template>
  <el-radio-group v-model="treeProps.checkStrictly" class="mb-2">
    <el-radio-button :value="true" label="true" />
    <el-radio-button :value="false" label="false" />
  </el-radio-group>
  <el-table
    :data="tableData"
    :tree-props="treeProps"
    row-key="id"
    default-expand-all
  >
    <el-table-column type="selection" width="55" :selectable="selectable" />
    <el-table-column prop="date" label="Date" />
    <el-table-column prop="name" label="Name" />
    <el-table-column prop="address" label="Address" />
  </el-table>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

interface User {
  id: number
  date: string
  name: string
  address: string
  hasChildren?: boolean
  children?: User[]
}

const treeProps = reactive({
  checkStrictly: false,
})

const selectable = (row: User) => ![1, 31].includes(row.id)

const tableData: User[] = [
  {
    id: 1,
    date: '2016-05-02',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 2,
    date: '2016-05-04',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
  },
  {
    id: 3,
    date: '2016-05-01',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
    children: [
      {
        id: 31,
        date: '2016-05-01',
        name: 'wangxiaohu',
        address: 'No. 189, Grove St, Los Angeles',
      },
      {
        id: 32,
        date: '2016-05-01',
        name: 'wangxiaohu',
        address: 'No. 189, Grove St, Los Angeles',
      },
      {
        id: 33,
        date: '2016-05-01',
        name: 'wangxiaohu',
        address: 'No. 189, Grove St, Los Angeles',
      },
    ],
  },
  {
    id: 4,
    date: '2016-05-03',
    name: 'wangxiaohu',
    address: 'No. 189, Grove St, Los Angeles',
  },
]
</script>
```

隐藏源代码

## 表尾合计行 [​](#表尾合计行)

若表格展示的是各类数字，可以在表尾显示各列的合计。

将 `show-summary` 设置为`true`就会在表格尾部展示合计行。 默认情况下，对于合计行，第一列不进行数据求合操作，而是显示「合计」二字（可通过`sum-text`配置），其余列会将本列所有数值进行求合操作，并显示出来。 当然，你也可以定义自己的合计逻辑。 使用 `summary-method` 并传入一个方法，返回一个数组，这个数组中的各项就会显示在合计行的各列中，可以是一个 VNode 或 String， 具体可以参考本例中的第二个表格。

|
ID

 |

Name

 |

Amount 1

 |

Amount 2

 |

Amount 3

 |
| --- | --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_22_column_89" width="180"><col name="el-table_22_column_90" width="179"><col name="el-table_22_column_91" width="178"><col name="el-table_22_column_92" width="178"><col name="el-table_22_column_93" width="178"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_22_column_89 el-table__cell"><div class="cell">12987122</div></td><td colspan="1" rowspan="1" class="el-table_22_column_90 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_22_column_91 el-table__cell"><div class="cell">234</div></td><td colspan="1" rowspan="1" class="el-table_22_column_92 el-table__cell"><div class="cell">3.2</div></td><td colspan="1" rowspan="1" class="el-table_22_column_93 el-table__cell"><div class="cell">10</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_22_column_89 el-table__cell"><div class="cell">12987123</div></td><td colspan="1" rowspan="1" class="el-table_22_column_90 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_22_column_91 el-table__cell"><div class="cell">165</div></td><td colspan="1" rowspan="1" class="el-table_22_column_92 el-table__cell"><div class="cell">4.43</div></td><td colspan="1" rowspan="1" class="el-table_22_column_93 el-table__cell"><div class="cell">12</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_22_column_89 el-table__cell"><div class="cell">12987124</div></td><td colspan="1" rowspan="1" class="el-table_22_column_90 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_22_column_91 el-table__cell"><div class="cell">324</div></td><td colspan="1" rowspan="1" class="el-table_22_column_92 el-table__cell"><div class="cell">1.9</div></td><td colspan="1" rowspan="1" class="el-table_22_column_93 el-table__cell"><div class="cell">9</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_22_column_89 el-table__cell"><div class="cell">12987125</div></td><td colspan="1" rowspan="1" class="el-table_22_column_90 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_22_column_91 el-table__cell"><div class="cell">621</div></td><td colspan="1" rowspan="1" class="el-table_22_column_92 el-table__cell"><div class="cell">2.2</div></td><td colspan="1" rowspan="1" class="el-table_22_column_93 el-table__cell"><div class="cell">17</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_22_column_89 el-table__cell"><div class="cell">12987126</div></td><td colspan="1" rowspan="1" class="el-table_22_column_90 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_22_column_91 el-table__cell"><div class="cell">539</div></td><td colspan="1" rowspan="1" class="el-table_22_column_92 el-table__cell"><div class="cell">4.1</div></td><td colspan="1" rowspan="1" class="el-table_22_column_93 el-table__cell"><div class="cell">15</div></td></tr></tbody></table>

<table class="el-table__footer" cellspacing="0" cellpadding="0" border="0" style="width: 893px;"><colgroup><col name="el-table_22_column_89" width="180"><col name="el-table_22_column_90" width="179"><col name="el-table_22_column_91" width="178"><col name="el-table_22_column_92" width="178"><col name="el-table_22_column_93" width="178"></colgroup><tfoot><tr><td colspan="1" rowspan="1" class="el-table__cell el-table_22_column_89 is-leaf"><div class="cell">Sum</div></td><td colspan="1" rowspan="1" class="el-table__cell el-table_22_column_90 is-leaf"><div class="cell"></div></td><td colspan="1" rowspan="1" class="el-table__cell el-table_22_column_91 is-leaf"><div class="cell">1883</div></td><td colspan="1" rowspan="1" class="el-table__cell el-table_22_column_92 is-leaf"><div class="cell">15.83</div></td><td colspan="1" rowspan="1" class="el-table__cell el-table_22_column_93 is-leaf"><div class="cell">63</div></td></tr></tfoot></table>

|
ID

 |

Name

 |

Cost 1 ($)

 |

Cost 2 ($)

 |

Cost 3 ($)

 |
| --- | --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_23_column_94" width="180"><col name="el-table_23_column_95" width="179"><col name="el-table_23_column_96" width="178"><col name="el-table_23_column_97" width="178"><col name="el-table_23_column_98" width="178"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_23_column_94 el-table__cell"><div class="cell">12987122</div></td><td colspan="1" rowspan="1" class="el-table_23_column_95 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_23_column_96 el-table__cell"><div class="cell">234</div></td><td colspan="1" rowspan="1" class="el-table_23_column_97 el-table__cell"><div class="cell">3.2</div></td><td colspan="1" rowspan="1" class="el-table_23_column_98 el-table__cell"><div class="cell">10</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_23_column_94 el-table__cell"><div class="cell">12987123</div></td><td colspan="1" rowspan="1" class="el-table_23_column_95 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_23_column_96 el-table__cell"><div class="cell">165</div></td><td colspan="1" rowspan="1" class="el-table_23_column_97 el-table__cell"><div class="cell">4.43</div></td><td colspan="1" rowspan="1" class="el-table_23_column_98 el-table__cell"><div class="cell">12</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_23_column_94 el-table__cell"><div class="cell">12987124</div></td><td colspan="1" rowspan="1" class="el-table_23_column_95 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_23_column_96 el-table__cell"><div class="cell">324</div></td><td colspan="1" rowspan="1" class="el-table_23_column_97 el-table__cell"><div class="cell">1.9</div></td><td colspan="1" rowspan="1" class="el-table_23_column_98 el-table__cell"><div class="cell">9</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_23_column_94 el-table__cell"><div class="cell">12987125</div></td><td colspan="1" rowspan="1" class="el-table_23_column_95 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_23_column_96 el-table__cell"><div class="cell">621</div></td><td colspan="1" rowspan="1" class="el-table_23_column_97 el-table__cell"><div class="cell">2.2</div></td><td colspan="1" rowspan="1" class="el-table_23_column_98 el-table__cell"><div class="cell">17</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_23_column_94 el-table__cell"><div class="cell">12987126</div></td><td colspan="1" rowspan="1" class="el-table_23_column_95 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_23_column_96 el-table__cell"><div class="cell">539</div></td><td colspan="1" rowspan="1" class="el-table_23_column_97 el-table__cell"><div class="cell">4.1</div></td><td colspan="1" rowspan="1" class="el-table_23_column_98 el-table__cell"><div class="cell">15</div></td></tr></tbody></table>

<table class="el-table__footer" cellspacing="0" cellpadding="0" border="0" style="width: 893px;"><colgroup><col name="el-table_23_column_94" width="180"><col name="el-table_23_column_95" width="179"><col name="el-table_23_column_96" width="178"><col name="el-table_23_column_97" width="178"><col name="el-table_23_column_98" width="178"></colgroup><tfoot><tr><td colspan="1" rowspan="1" class="el-table__cell el-table_23_column_94 is-leaf"><div class="cell"><div style="text-decoration: underline;">Total Cost</div></div></td><td colspan="1" rowspan="1" class="el-table__cell el-table_23_column_95 is-leaf"><div class="cell">N/A</div></td><td colspan="1" rowspan="1" class="el-table__cell el-table_23_column_96 is-leaf"><div class="cell">$ 1883</div></td><td colspan="1" rowspan="1" class="el-table__cell el-table_23_column_97 is-leaf"><div class="cell">$ 15.83</div></td><td colspan="1" rowspan="1" class="el-table__cell el-table_23_column_98 is-leaf"><div class="cell">$ 63</div></td></tr></tfoot></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBib3JkZXIgc2hvdy1zdW1tYXJ5IHN0eWxlPVwid2lkdGg6IDEwMCVcIj5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJpZFwiIGxhYmVsPVwiSURcIiB3aWR0aD1cIjE4MFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiYW1vdW50MVwiIHNvcnRhYmxlIGxhYmVsPVwiQW1vdW50IDFcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFtb3VudDJcIiBzb3J0YWJsZSBsYWJlbD1cIkFtb3VudCAyXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhbW91bnQzXCIgc29ydGFibGUgbGFiZWw9XCJBbW91bnQgM1wiIC8+XG4gIDwvZWwtdGFibGU+XG5cbiAgPGVsLXRhYmxlXG4gICAgOmRhdGE9XCJ0YWJsZURhdGFcIlxuICAgIGJvcmRlclxuICAgIGhlaWdodD1cIjIwMFwiXG4gICAgOnN1bW1hcnktbWV0aG9kPVwiZ2V0U3VtbWFyaWVzXCJcbiAgICBzaG93LXN1bW1hcnlcbiAgICBzdHlsZT1cIndpZHRoOiAxMDAlOyBtYXJnaW4tdG9wOiAyMHB4XCJcbiAgPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImlkXCIgbGFiZWw9XCJJRFwiIHdpZHRoPVwiMTgwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhbW91bnQxXCIgbGFiZWw9XCJDb3N0IDEgKCQpXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhbW91bnQyXCIgbGFiZWw9XCJDb3N0IDIgKCQpXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhbW91bnQzXCIgbGFiZWw9XCJDb3N0IDMgKCQpXCIgLz5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBoIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFZOb2RlIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHR5cGUgeyBUYWJsZUNvbHVtbkN0eCB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW50ZXJmYWNlIFByb2R1Y3Qge1xuICBpZDogc3RyaW5nXG4gIG5hbWU6IHN0cmluZ1xuICBhbW91bnQxOiBzdHJpbmdcbiAgYW1vdW50Mjogc3RyaW5nXG4gIGFtb3VudDM6IG51bWJlclxufVxuXG5pbnRlcmZhY2UgU3VtbWFyeU1ldGhvZFByb3BzPFQgZXh0ZW5kcyBQcm9kdWN0ID0gUHJvZHVjdD4ge1xuICBjb2x1bW5zOiBUYWJsZUNvbHVtbkN0eDxUPltdXG4gIGRhdGE6IFRbXVxufVxuXG5jb25zdCBnZXRTdW1tYXJpZXMgPSAocGFyYW06IFN1bW1hcnlNZXRob2RQcm9wcykgPT4ge1xuICBjb25zdCB7IGNvbHVtbnMsIGRhdGEgfSA9IHBhcmFtXG4gIGNvbnN0IHN1bXM6IChzdHJpbmcgfCBWTm9kZSlbXSA9IFtdXG4gIGNvbHVtbnMuZm9yRWFjaCgoY29sdW1uLCBpbmRleCkgPT4ge1xuICAgIGlmIChpbmRleCA9PT0gMCkge1xuICAgICAgc3Vtc1tpbmRleF0gPSBoKCdkaXYnLCB7IHN0eWxlOiB7IHRleHREZWNvcmF0aW9uOiAndW5kZXJsaW5lJyB9IH0sIFtcbiAgICAgICAgJ1RvdGFsIENvc3QnLFxuICAgICAgXSlcbiAgICAgIHJldHVyblxuICAgIH1cbiAgICBjb25zdCB2YWx1ZXMgPSBkYXRhLm1hcCgoaXRlbSkgPT4gTnVtYmVyKGl0ZW1bY29sdW1uLnByb3BlcnR5XSkpXG4gICAgaWYgKCF2YWx1ZXMuZXZlcnkoKHZhbHVlKSA9PiBOdW1iZXIuaXNOYU4odmFsdWUpKSkge1xuICAgICAgc3Vtc1tpbmRleF0gPSBgJCAke3ZhbHVlcy5yZWR1Y2UoKHByZXYsIGN1cnIpID0+IHtcbiAgICAgICAgY29uc3QgdmFsdWUgPSBOdW1iZXIoY3VycilcbiAgICAgICAgaWYgKCFOdW1iZXIuaXNOYU4odmFsdWUpKSB7XG4gICAgICAgICAgcmV0dXJuIHByZXYgKyBjdXJyXG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgcmV0dXJuIHByZXZcbiAgICAgICAgfVxuICAgICAgfSwgMCl9YFxuICAgIH0gZWxzZSB7XG4gICAgICBzdW1zW2luZGV4XSA9ICdOL0EnXG4gICAgfVxuICB9KVxuXG4gIHJldHVybiBzdW1zXG59XG5cbmNvbnN0IHRhYmxlRGF0YTogUHJvZHVjdFtdID0gW1xuICB7XG4gICAgaWQ6ICcxMjk4NzEyMicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYW1vdW50MTogJzIzNCcsXG4gICAgYW1vdW50MjogJzMuMicsXG4gICAgYW1vdW50MzogMTAsXG4gIH0sXG4gIHtcbiAgICBpZDogJzEyOTg3MTIzJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhbW91bnQxOiAnMTY1JyxcbiAgICBhbW91bnQyOiAnNC40MycsXG4gICAgYW1vdW50MzogMTIsXG4gIH0sXG4gIHtcbiAgICBpZDogJzEyOTg3MTI0JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhbW91bnQxOiAnMzI0JyxcbiAgICBhbW91bnQyOiAnMS45JyxcbiAgICBhbW91bnQzOiA5LFxuICB9LFxuICB7XG4gICAgaWQ6ICcxMjk4NzEyNScsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYW1vdW50MTogJzYyMScsXG4gICAgYW1vdW50MjogJzIuMicsXG4gICAgYW1vdW50MzogMTcsXG4gIH0sXG4gIHtcbiAgICBpZDogJzEyOTg3MTI2JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhbW91bnQxOiAnNTM5JyxcbiAgICBhbW91bnQyOiAnNC4xJyxcbiAgICBhbW91bnQzOiAxNSxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/summary.vue)_

vue

```
<template>
  <el-table :data="tableData" border show-summary style="width: 100%">
    <el-table-column prop="id" label="ID" width="180" />
    <el-table-column prop="name" label="Name" />
    <el-table-column prop="amount1" sortable label="Amount 1" />
    <el-table-column prop="amount2" sortable label="Amount 2" />
    <el-table-column prop="amount3" sortable label="Amount 3" />
  </el-table>

  <el-table
    :data="tableData"
    border
    height="200"
    :summary-method="getSummaries"
    show-summary
    style="width: 100%; margin-top: 20px"
  >
    <el-table-column prop="id" label="ID" width="180" />
    <el-table-column prop="name" label="Name" />
    <el-table-column prop="amount1" label="Cost 1 ($)" />
    <el-table-column prop="amount2" label="Cost 2 ($)" />
    <el-table-column prop="amount3" label="Cost 3 ($)" />
  </el-table>
</template>

<script lang="ts" setup>
import { h } from 'vue'

import type { VNode } from 'vue'
import type { TableColumnCtx } from 'element-plus'

interface Product {
  id: string
  name: string
  amount1: string
  amount2: string
  amount3: number
}

interface SummaryMethodProps<T extends Product = Product> {
  columns: TableColumnCtx<T>[]
  data: T[]
}

const getSummaries = (param: SummaryMethodProps) => {
  const { columns, data } = param
  const sums: (string | VNode)[] = []
  columns.forEach((column, index) => {
    if (index === 0) {
      sums[index] = h('div', { style: { textDecoration: 'underline' } }, [
        'Total Cost',
      ])
      return
    }
    const values = data.map((item) => Number(item[column.property]))
    if (!values.every((value) => Number.isNaN(value))) {
      sums[index] = `$ ${values.reduce((prev, curr) => {
        const value = Number(curr)
        if (!Number.isNaN(value)) {
          return prev + curr
        } else {
          return prev
        }
      }, 0)}`
    } else {
      sums[index] = 'N/A'
    }
  })

  return sums
}

const tableData: Product[] = [
  {
    id: '12987122',
    name: 'Tom',
    amount1: '234',
    amount2: '3.2',
    amount3: 10,
  },
  {
    id: '12987123',
    name: 'Tom',
    amount1: '165',
    amount2: '4.43',
    amount3: 12,
  },
  {
    id: '12987124',
    name: 'Tom',
    amount1: '324',
    amount2: '1.9',
    amount3: 9,
  },
  {
    id: '12987125',
    name: 'Tom',
    amount1: '621',
    amount2: '2.2',
    amount3: 17,
  },
  {
    id: '12987126',
    name: 'Tom',
    amount1: '539',
    amount2: '4.1',
    amount3: 15,
  },
]
</script>
```

隐藏源代码

## 合并行或列 [​](#合并行或列)

多行或多列共用一个数据时，可以合并行或列。

通过给 table 传入`span-method`方法可以实现合并行或列， 方法的参数是一个对象，里面包含当前行 `row`、当前列 `column`、当前行号 `rowIndex`、当前列号 `columnIndex` 四个属性。 该函数可以返回一个包含两个元素的数组，第一个元素代表 `rowspan`，第二个元素代表 `colspan`。 也可以返回一个键名为 `rowspan` 和 `colspan` 的对象。

|
ID

 |

Name

 |

Amount 1

 |

Amount 2

 |

Amount 3

 |
| --- | --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_24_column_99" width="180"><col name="el-table_24_column_100" width="179"><col name="el-table_24_column_101" width="178"><col name="el-table_24_column_102" width="178"><col name="el-table_24_column_103" width="178"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="2" rowspan="1" class="el-table_24_column_99 el-table__cell"><div class="cell">12987122</div></td><td colspan="1" rowspan="1" class="el-table_24_column_101 el-table__cell"><div class="cell">234</div></td><td colspan="1" rowspan="1" class="el-table_24_column_102 el-table__cell"><div class="cell">3.2</div></td><td colspan="1" rowspan="1" class="el-table_24_column_103 el-table__cell"><div class="cell">10</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_24_column_99 el-table__cell"><div class="cell">12987123</div></td><td colspan="1" rowspan="1" class="el-table_24_column_100 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_24_column_101 el-table__cell"><div class="cell">165</div></td><td colspan="1" rowspan="1" class="el-table_24_column_102 el-table__cell"><div class="cell">4.43</div></td><td colspan="1" rowspan="1" class="el-table_24_column_103 el-table__cell"><div class="cell">12</div></td></tr><tr style="" class="el-table__row"><td colspan="2" rowspan="1" class="el-table_24_column_99 el-table__cell"><div class="cell">12987124</div></td><td colspan="1" rowspan="1" class="el-table_24_column_101 el-table__cell"><div class="cell">324</div></td><td colspan="1" rowspan="1" class="el-table_24_column_102 el-table__cell"><div class="cell">1.9</div></td><td colspan="1" rowspan="1" class="el-table_24_column_103 el-table__cell"><div class="cell">9</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_24_column_99 el-table__cell"><div class="cell">12987125</div></td><td colspan="1" rowspan="1" class="el-table_24_column_100 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_24_column_101 el-table__cell"><div class="cell">621</div></td><td colspan="1" rowspan="1" class="el-table_24_column_102 el-table__cell"><div class="cell">2.2</div></td><td colspan="1" rowspan="1" class="el-table_24_column_103 el-table__cell"><div class="cell">17</div></td></tr><tr style="" class="el-table__row"><td colspan="2" rowspan="1" class="el-table_24_column_99 el-table__cell"><div class="cell">12987126</div></td><td colspan="1" rowspan="1" class="el-table_24_column_101 el-table__cell"><div class="cell">539</div></td><td colspan="1" rowspan="1" class="el-table_24_column_102 el-table__cell"><div class="cell">4.1</div></td><td colspan="1" rowspan="1" class="el-table_24_column_103 el-table__cell"><div class="cell">15</div></td></tr></tbody></table>

|
ID

 |

Name

 |

Amount 1

 |

Amount 2

 |

Amount 3

 |
| --- | --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_25_column_104" width="180"><col name="el-table_25_column_105" width="179"><col name="el-table_25_column_106" width="178"><col name="el-table_25_column_107" width="178"><col name="el-table_25_column_108" width="178"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="2" class="el-table_25_column_104 el-table__cell"><div class="cell">12987122</div></td><td colspan="1" rowspan="1" class="el-table_25_column_105 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_25_column_106 el-table__cell"><div class="cell">234</div></td><td colspan="1" rowspan="1" class="el-table_25_column_107 el-table__cell"><div class="cell">3.2</div></td><td colspan="1" rowspan="1" class="el-table_25_column_108 el-table__cell"><div class="cell">10</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_25_column_105 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_25_column_106 el-table__cell"><div class="cell">165</div></td><td colspan="1" rowspan="1" class="el-table_25_column_107 el-table__cell"><div class="cell">4.43</div></td><td colspan="1" rowspan="1" class="el-table_25_column_108 el-table__cell"><div class="cell">12</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="2" class="el-table_25_column_104 el-table__cell"><div class="cell">12987124</div></td><td colspan="1" rowspan="1" class="el-table_25_column_105 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_25_column_106 el-table__cell"><div class="cell">324</div></td><td colspan="1" rowspan="1" class="el-table_25_column_107 el-table__cell"><div class="cell">1.9</div></td><td colspan="1" rowspan="1" class="el-table_25_column_108 el-table__cell"><div class="cell">9</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_25_column_105 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_25_column_106 el-table__cell"><div class="cell">621</div></td><td colspan="1" rowspan="1" class="el-table_25_column_107 el-table__cell"><div class="cell">2.2</div></td><td colspan="1" rowspan="1" class="el-table_25_column_108 el-table__cell"><div class="cell">17</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="2" class="el-table_25_column_104 el-table__cell"><div class="cell">12987126</div></td><td colspan="1" rowspan="1" class="el-table_25_column_105 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_25_column_106 el-table__cell"><div class="cell">539</div></td><td colspan="1" rowspan="1" class="el-table_25_column_107 el-table__cell"><div class="cell">4.1</div></td><td colspan="1" rowspan="1" class="el-table_25_column_108 el-table__cell"><div class="cell">15</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC10YWJsZVxuICAgICAgOmRhdGE9XCJ0YWJsZURhdGFcIlxuICAgICAgOnNwYW4tbWV0aG9kPVwiYXJyYXlTcGFuTWV0aG9kXCJcbiAgICAgIGJvcmRlclxuICAgICAgc3R5bGU9XCJ3aWR0aDogMTAwJVwiXG4gICAgPlxuICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiaWRcIiBsYWJlbD1cIklEXCIgd2lkdGg9XCIxODBcIiAvPlxuICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIC8+XG4gICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhbW91bnQxXCIgc29ydGFibGUgbGFiZWw9XCJBbW91bnQgMVwiIC8+XG4gICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhbW91bnQyXCIgc29ydGFibGUgbGFiZWw9XCJBbW91bnQgMlwiIC8+XG4gICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhbW91bnQzXCIgc29ydGFibGUgbGFiZWw9XCJBbW91bnQgM1wiIC8+XG4gICAgPC9lbC10YWJsZT5cblxuICAgIDxlbC10YWJsZVxuICAgICAgOmRhdGE9XCJ0YWJsZURhdGFcIlxuICAgICAgOnNwYW4tbWV0aG9kPVwib2JqZWN0U3Bhbk1ldGhvZFwiXG4gICAgICBib3JkZXJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDEwMCU7IG1hcmdpbi10b3A6IDIwcHhcIlxuICAgID5cbiAgICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImlkXCIgbGFiZWw9XCJJRFwiIHdpZHRoPVwiMTgwXCIgLz5cbiAgICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cIm5hbWVcIiBsYWJlbD1cIk5hbWVcIiAvPlxuICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiYW1vdW50MVwiIGxhYmVsPVwiQW1vdW50IDFcIiAvPlxuICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiYW1vdW50MlwiIGxhYmVsPVwiQW1vdW50IDJcIiAvPlxuICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiYW1vdW50M1wiIGxhYmVsPVwiQW1vdW50IDNcIiAvPlxuICAgIDwvZWwtdGFibGU+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB0eXBlIHsgVGFibGVDb2x1bW5DdHggfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmludGVyZmFjZSBVc2VyIHtcbiAgaWQ6IHN0cmluZ1xuICBuYW1lOiBzdHJpbmdcbiAgYW1vdW50MTogc3RyaW5nXG4gIGFtb3VudDI6IHN0cmluZ1xuICBhbW91bnQzOiBudW1iZXJcbn1cblxuaW50ZXJmYWNlIFNwYW5NZXRob2RQcm9wcyB7XG4gIHJvdzogVXNlclxuICBjb2x1bW46IFRhYmxlQ29sdW1uQ3R4PFVzZXI+XG4gIHJvd0luZGV4OiBudW1iZXJcbiAgY29sdW1uSW5kZXg6IG51bWJlclxufVxuXG5jb25zdCBhcnJheVNwYW5NZXRob2QgPSAoe1xuICByb3csXG4gIGNvbHVtbixcbiAgcm93SW5kZXgsXG4gIGNvbHVtbkluZGV4LFxufTogU3Bhbk1ldGhvZFByb3BzKSA9PiB7XG4gIGlmIChyb3dJbmRleCAlIDIgPT09IDApIHtcbiAgICBpZiAoY29sdW1uSW5kZXggPT09IDApIHtcbiAgICAgIHJldHVybiBbMSwgMl1cbiAgICB9IGVsc2UgaWYgKGNvbHVtbkluZGV4ID09PSAxKSB7XG4gICAgICByZXR1cm4gWzAsIDBdXG4gICAgfVxuICB9XG59XG5cbmNvbnN0IG9iamVjdFNwYW5NZXRob2QgPSAoe1xuICByb3csXG4gIGNvbHVtbixcbiAgcm93SW5kZXgsXG4gIGNvbHVtbkluZGV4LFxufTogU3Bhbk1ldGhvZFByb3BzKSA9PiB7XG4gIGlmIChjb2x1bW5JbmRleCA9PT0gMCkge1xuICAgIGlmIChyb3dJbmRleCAlIDIgPT09IDApIHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHJvd3NwYW46IDIsXG4gICAgICAgIGNvbHNwYW46IDEsXG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHJvd3NwYW46IDAsXG4gICAgICAgIGNvbHNwYW46IDAsXG4gICAgICB9XG4gICAgfVxuICB9XG59XG5cbmNvbnN0IHRhYmxlRGF0YTogVXNlcltdID0gW1xuICB7XG4gICAgaWQ6ICcxMjk4NzEyMicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYW1vdW50MTogJzIzNCcsXG4gICAgYW1vdW50MjogJzMuMicsXG4gICAgYW1vdW50MzogMTAsXG4gIH0sXG4gIHtcbiAgICBpZDogJzEyOTg3MTIzJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhbW91bnQxOiAnMTY1JyxcbiAgICBhbW91bnQyOiAnNC40MycsXG4gICAgYW1vdW50MzogMTIsXG4gIH0sXG4gIHtcbiAgICBpZDogJzEyOTg3MTI0JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhbW91bnQxOiAnMzI0JyxcbiAgICBhbW91bnQyOiAnMS45JyxcbiAgICBhbW91bnQzOiA5LFxuICB9LFxuICB7XG4gICAgaWQ6ICcxMjk4NzEyNScsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgYW1vdW50MTogJzYyMScsXG4gICAgYW1vdW50MjogJzIuMicsXG4gICAgYW1vdW50MzogMTcsXG4gIH0sXG4gIHtcbiAgICBpZDogJzEyOTg3MTI2JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhbW91bnQxOiAnNTM5JyxcbiAgICBhbW91bnQyOiAnNC4xJyxcbiAgICBhbW91bnQzOiAxNSxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/rowspan-and-colspan.vue)_

vue

```
<template>
  <div>
    <el-table
      :data="tableData"
      :span-method="arraySpanMethod"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="180" />
      <el-table-column prop="name" label="Name" />
      <el-table-column prop="amount1" sortable label="Amount 1" />
      <el-table-column prop="amount2" sortable label="Amount 2" />
      <el-table-column prop="amount3" sortable label="Amount 3" />
    </el-table>

    <el-table
      :data="tableData"
      :span-method="objectSpanMethod"
      border
      style="width: 100%; margin-top: 20px"
    >
      <el-table-column prop="id" label="ID" width="180" />
      <el-table-column prop="name" label="Name" />
      <el-table-column prop="amount1" label="Amount 1" />
      <el-table-column prop="amount2" label="Amount 2" />
      <el-table-column prop="amount3" label="Amount 3" />
    </el-table>
  </div>
</template>

<script lang="ts" setup>
import type { TableColumnCtx } from 'element-plus'

interface User {
  id: string
  name: string
  amount1: string
  amount2: string
  amount3: number
}

interface SpanMethodProps {
  row: User
  column: TableColumnCtx<User>
  rowIndex: number
  columnIndex: number
}

const arraySpanMethod = ({
  row,
  column,
  rowIndex,
  columnIndex,
}: SpanMethodProps) => {
  if (rowIndex % 2 === 0) {
    if (columnIndex === 0) {
      return [1, 2]
    } else if (columnIndex === 1) {
      return [0, 0]
    }
  }
}

const objectSpanMethod = ({
  row,
  column,
  rowIndex,
  columnIndex,
}: SpanMethodProps) => {
  if (columnIndex === 0) {
    if (rowIndex % 2 === 0) {
      return {
        rowspan: 2,
        colspan: 1,
      }
    } else {
      return {
        rowspan: 0,
        colspan: 0,
      }
    }
  }
}

const tableData: User[] = [
  {
    id: '12987122',
    name: 'Tom',
    amount1: '234',
    amount2: '3.2',
    amount3: 10,
  },
  {
    id: '12987123',
    name: 'Tom',
    amount1: '165',
    amount2: '4.43',
    amount3: 12,
  },
  {
    id: '12987124',
    name: 'Tom',
    amount1: '324',
    amount2: '1.9',
    amount3: 9,
  },
  {
    id: '12987125',
    name: 'Tom',
    amount1: '621',
    amount2: '2.2',
    amount3: 17,
  },
  {
    id: '12987126',
    name: 'Tom',
    amount1: '539',
    amount2: '4.1',
    amount3: 15,
  },
]
</script>
```

隐藏源代码

## 自定义索引 [​](#自定义索引)

自定义 `type=index` 列的行号。

通过给 `type=index` 的列传入 index 属性，可以自定义索引。 该属性传入数字时，将作为索引的起始值。 也可以传入一个方法，它提供当前行的行号（从 `0` 开始）作为参数，返回值将作为索引展示。

|
 |

Date

 |

Name

 |

Address

 |
| --- | --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_26_column_109" width="48"><col name="el-table_26_column_110" width="180"><col name="el-table_26_column_111" width="180"><col name="el-table_26_column_112" width="485"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_26_column_109 el-table__cell"><div class="cell"><div>0</div></div></td><td colspan="1" rowspan="1" class="el-table_26_column_110 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_26_column_111 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_26_column_112 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_26_column_109 el-table__cell"><div class="cell"><div>2</div></div></td><td colspan="1" rowspan="1" class="el-table_26_column_110 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_26_column_111 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_26_column_112 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_26_column_109 el-table__cell"><div class="cell"><div>4</div></div></td><td colspan="1" rowspan="1" class="el-table_26_column_110 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_26_column_111 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_26_column_112 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_26_column_109 el-table__cell"><div class="cell"><div>6</div></div></td><td colspan="1" rowspan="1" class="el-table_26_column_110 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_26_column_111 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_26_column_112 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCI+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiB0eXBlPVwiaW5kZXhcIiA6aW5kZXg9XCJpbmRleE1ldGhvZFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTgwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIxODBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiAvPlxuICA8L2VsLXRhYmxlPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IGluZGV4TWV0aG9kID0gKGluZGV4OiBudW1iZXIpID0+IHtcbiAgcmV0dXJuIGluZGV4ICogMlxufVxuY29uc3QgdGFibGVEYXRhID0gW1xuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDMnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ0xvcyBBbmdlbGVzJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB6aXA6ICdDQSA5MDAzNicsXG4gICAgdGFnOiAnSG9tZScsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMicsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgICB0YWc6ICdPZmZpY2UnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDQnLFxuICAgIG5hbWU6ICdUb20nLFxuICAgIHN0YXRlOiAnQ2FsaWZvcm5pYScsXG4gICAgY2l0eTogJ0xvcyBBbmdlbGVzJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgICB6aXA6ICdDQSA5MDAzNicsXG4gICAgdGFnOiAnSG9tZScsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ1RvbScsXG4gICAgc3RhdGU6ICdDYWxpZm9ybmlhJyxcbiAgICBjaXR5OiAnTG9zIEFuZ2VsZXMnLFxuICAgIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxuICAgIHppcDogJ0NBIDkwMDM2JyxcbiAgICB0YWc6ICdPZmZpY2UnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/custom-index.vue)_

vue

```
<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column type="index" :index="indexMethod" />
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" />
  </el-table>
</template>

<script lang="ts" setup>
const indexMethod = (index: number) => {
  return index * 2
}
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Home',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Office',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Home',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
    tag: 'Office',
  },
]
</script>
```

隐藏源代码

## 表格布局 [​](#表格布局)

通过属性 [table-layout](https://developer.mozilla.org/en-US/docs/Web/CSS/table-layout) 可以指定表格中单元格、行和列的布局方式

fixedauto

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_27_column_113" width="299"><col name="el-table_27_column_114" width="297"><col name="el-table_27_column_115" width="297"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_27_column_113 el-table__cell"><div class="cell">2016-05-03</div></td><td colspan="1" rowspan="1" class="el-table_27_column_114 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_27_column_115 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_27_column_113 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_27_column_114 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_27_column_115 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_27_column_113 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_27_column_114 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_27_column_115 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_27_column_113 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_27_column_114 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_27_column_115 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInRhYmxlTGF5b3V0XCIgY2xhc3M9XCJtYi0yXCI+XG4gICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cImZpeGVkXCI+Zml4ZWQ8L2VsLXJhZGlvLWJ1dHRvbj5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwiYXV0b1wiPmF1dG88L2VsLXJhZGlvLWJ1dHRvbj5cbiAgPC9lbC1yYWRpby1ncm91cD5cbiAgPGVsLXRhYmxlIDpkYXRhPVwidGFibGVEYXRhXCIgOnRhYmxlLWxheW91dD1cInRhYmxlTGF5b3V0XCI+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiYWRkcmVzc1wiIGxhYmVsPVwiQWRkcmVzc1wiIC8+XG4gIDwvZWwtdGFibGU+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFRhYmxlSW5zdGFuY2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHRhYmxlTGF5b3V0ID0gcmVmPFRhYmxlSW5zdGFuY2VbJ3RhYmxlTGF5b3V0J10+KCdmaXhlZCcpXG5cbmNvbnN0IHRhYmxlRGF0YSA9IFtcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAzJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAyJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA0JyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICBuYW1lOiAnVG9tJyxcbiAgICBhZGRyZXNzOiAnTm8uIDE4OSwgR3JvdmUgU3QsIExvcyBBbmdlbGVzJyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/table-layout.vue)_

vue

```
<template>
  <el-radio-group v-model="tableLayout" class="mb-2">
    <el-radio-button value="fixed">fixed</el-radio-button>
    <el-radio-button value="auto">auto</el-radio-button>
  </el-radio-group>
  <el-table :data="tableData" :table-layout="tableLayout">
    <el-table-column prop="date" label="Date" />
    <el-table-column prop="name" label="Name" />
    <el-table-column prop="address" label="Address" />
  </el-table>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TableInstance } from 'element-plus'

const tableLayout = ref<TableInstance['tableLayout']>('fixed')

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

隐藏源代码

## Tooltip 自定义 2.9.4 [​](#tooltip-自定义)

您可以使用 `tooltip-formatter` 自定义 Tooltip 提示内容。

|
extends table formatter

 |

formatter object

 |

with vnode

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 720px;"><colgroup><col name="el-table_28_column_116" width="240"><col name="el-table_28_column_117" width="240"><col name="el-table_28_column_118" width="240"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_28_column_116 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">Lohrbergstr. 86c, Süd Lilli, Saarland</div></td><td colspan="1" rowspan="1" class="el-table_28_column_117 el-table__cell"><div class="cell el-tooltip" style="width: 238px;"><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">Office</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">Home</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">Park</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">Garden</span></span></div></td><td colspan="1" rowspan="1" class="el-table_28_column_118 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">https://github.com/element-plus/element-plus/issues</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_28_column_116 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">760 A Street, South Frankfield, Illinois</div></td><td colspan="1" rowspan="1" class="el-table_28_column_117 el-table__cell"><div class="cell el-tooltip" style="width: 238px;"><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">error</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">warning</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">success</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">info</span></span></div></td><td colspan="1" rowspan="1" class="el-table_28_column_118 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">https://github.com/element-plus/element-plus/pulls</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_28_column_116 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">Arnold-Ohletz-Str. 41a, Alt Malinascheid, Thüringen</div></td><td colspan="1" rowspan="1" class="el-table_28_column_117 el-table__cell"><div class="cell el-tooltip" style="width: 238px;"><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">one</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">two</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">three</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">four</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">five</span></span></div></td><td colspan="1" rowspan="1" class="el-table_28_column_118 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">https://github.com/element-plus/element-plus/discussions</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_28_column_116 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">23618 Windsor Drive, West Ricardoview, Idaho</div></td><td colspan="1" rowspan="1" class="el-table_28_column_117 el-table__cell"><div class="cell el-tooltip" style="width: 238px;"><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">blue</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">white</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">dark</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">gray</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">red</span></span><span data-v-90c15426="" class="el-tag el-tag--primary el-tag--light tag-item"><span class="el-tag__content">bright</span></span></div></td><td colspan="1" rowspan="1" class="el-table_28_column_118 el-table__cell"><div class="cell el-tooltip" style="width: 238px;">https://github.com/element-plus/element-plus/actions</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGVcbiAgICA6ZGF0YT1cInRhYmxlRGF0YVwiXG4gICAgc2hvdy1vdmVyZmxvdy10b29sdGlwXG4gICAgOnRvb2x0aXAtZm9ybWF0dGVyPVwidGFibGVSb3dGb3JtYXR0ZXJcIlxuICAgIHN0eWxlPVwid2lkdGg6IDEwMCVcIlxuICA+XG4gICAgPGVsLXRhYmxlLWNvbHVtblxuICAgICAgcHJvcD1cImFkZHJlc3NcIlxuICAgICAgbGFiZWw9XCJleHRlbmRzIHRhYmxlIGZvcm1hdHRlclwiXG4gICAgICB3aWR0aD1cIjI0MFwiXG4gICAgLz5cbiAgICA8IS0tIEB2dWUtZ2VuZXJpYyB7VGFibGVEYXRhfSAtLT5cbiAgICA8ZWwtdGFibGUtY29sdW1uXG4gICAgICBwcm9wPVwidGFnc1wiXG4gICAgICBsYWJlbD1cImZvcm1hdHRlciBvYmplY3RcIlxuICAgICAgd2lkdGg9XCIyNDBcIlxuICAgICAgOnRvb2x0aXAtZm9ybWF0dGVyPVwiKHsgcm93IH0pID0+IHJvdy50YWdzLmpvaW4oJywgJylcIlxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD1cInsgcm93IH1cIj5cbiAgICAgICAgPGVsLXRhZ1xuICAgICAgICAgIHYtZm9yPVwidGFnIGluIHJvdy50YWdzXCJcbiAgICAgICAgICA6a2V5PVwidGFnXCJcbiAgICAgICAgICBjbGFzcz1cInRhZy1pdGVtXCJcbiAgICAgICAgICB0eXBlPVwicHJpbWFyeVwiXG4gICAgICAgID5cbiAgICAgICAgICB7eyB0YWcgfX1cbiAgICAgICAgPC9lbC10YWc+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtdGFibGUtY29sdW1uPlxuICAgIDxlbC10YWJsZS1jb2x1bW5cbiAgICAgIHByb3A9XCJ1cmxcIlxuICAgICAgbGFiZWw9XCJ3aXRoIHZub2RlXCJcbiAgICAgIHdpZHRoPVwiMjQwXCJcbiAgICAgIDp0b29sdGlwLWZvcm1hdHRlcj1cIndpdGhWTm9kZVwiXG4gICAgLz5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBoIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgRWxMaW5rLCB0eXBlIFRhYmxlVG9vbHRpcERhdGEgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbnR5cGUgVGFibGVEYXRhID0ge1xuICBhZGRyZXNzOiBzdHJpbmdcbiAgdGFnczogc3RyaW5nW11cbiAgdXJsOiBzdHJpbmdcbn1cblxuY29uc3QgdGFibGVEYXRhOiBUYWJsZURhdGFbXSA9IFtcbiAge1xuICAgIGFkZHJlc3M6ICdMb2hyYmVyZ3N0ci4gODZjLCBTw7xkIExpbGxpLCBTYWFybGFuZCcsXG4gICAgdGFnczogWydPZmZpY2UnLCAnSG9tZScsICdQYXJrJywgJ0dhcmRlbiddLFxuICAgIHVybDogJ2h0dHBzOi8vZ2l0aHViLmNvbS9lbGVtZW50LXBsdXMvZWxlbWVudC1wbHVzL2lzc3VlcycsXG4gIH0sXG4gIHtcbiAgICBhZGRyZXNzOiAnNzYwIEEgU3RyZWV0LCBTb3V0aCBGcmFua2ZpZWxkLCBJbGxpbm9pcycsXG4gICAgdGFnczogWydlcnJvcicsICd3YXJuaW5nJywgJ3N1Y2Nlc3MnLCAnaW5mbyddLFxuICAgIHVybDogJ2h0dHBzOi8vZ2l0aHViLmNvbS9lbGVtZW50LXBsdXMvZWxlbWVudC1wbHVzL3B1bGxzJyxcbiAgfSxcbiAge1xuICAgIGFkZHJlc3M6ICdBcm5vbGQtT2hsZXR6LVN0ci4gNDFhLCBBbHQgTWFsaW5hc2NoZWlkLCBUaMO8cmluZ2VuJyxcbiAgICB0YWdzOiBbJ29uZScsICd0d28nLCAndGhyZWUnLCAnZm91cicsICdmaXZlJ10sXG4gICAgdXJsOiAnaHR0cHM6Ly9naXRodWIuY29tL2VsZW1lbnQtcGx1cy9lbGVtZW50LXBsdXMvZGlzY3Vzc2lvbnMnLFxuICB9LFxuICB7XG4gICAgYWRkcmVzczogJzIzNjE4IFdpbmRzb3IgRHJpdmUsIFdlc3QgUmljYXJkb3ZpZXcsIElkYWhvJyxcbiAgICB0YWdzOiBbJ2JsdWUnLCAnd2hpdGUnLCAnZGFyaycsICdncmF5JywgJ3JlZCcsICdicmlnaHQnXSxcbiAgICB1cmw6ICdodHRwczovL2dpdGh1Yi5jb20vZWxlbWVudC1wbHVzL2VsZW1lbnQtcGx1cy9hY3Rpb25zJyxcbiAgfSxcbl1cblxuY29uc3QgdGFibGVSb3dGb3JtYXR0ZXIgPSAoZGF0YTogVGFibGVUb29sdGlwRGF0YTxUYWJsZURhdGE+KSA9PiB7XG4gIHJldHVybiBgJHtkYXRhLmNlbGxWYWx1ZX06IHRhYmxlIGZvcm1hdHRlcmBcbn1cblxuY29uc3Qgd2l0aFZOb2RlID0gKGRhdGE6IFRhYmxlVG9vbHRpcERhdGE8VGFibGVEYXRhPikgPT4ge1xuICByZXR1cm4gaChFbExpbmssIHsgdHlwZTogJ3ByaW1hcnknLCBocmVmOiBkYXRhLmNlbGxWYWx1ZSB9LCAoKSA9PlxuICAgIGgoJ3NwYW4nLCBudWxsLCBkYXRhLmNlbGxWYWx1ZSlcbiAgKVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG5wIHtcbiAgbWFyZ2luOiAxMHB4O1xuICBwYWRkaW5nOiAwO1xufVxuLnRhZy1pdGVtICsgLnRhZy1pdGVtIHtcbiAgbWFyZ2luLWxlZnQ6IDVweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/table/tooltip-formatter.vue)_

vue

```
<template>
  <el-table
    :data="tableData"
    show-overflow-tooltip
    :tooltip-formatter="tableRowFormatter"
    style="width: 100%"
  >
    <el-table-column
      prop="address"
      label="extends table formatter"
      width="240"
    />
    <!-- @vue-generic {TableData} -->
    <el-table-column
      prop="tags"
      label="formatter object"
      width="240"
      :tooltip-formatter="({ row }) => row.tags.join(', ')"
    >
      <template #default="{ row }">
        <el-tag
          v-for="tag in row.tags"
          :key="tag"
          class="tag-item"
          type="primary"
        >
          {{ tag }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column
      prop="url"
      label="with vnode"
      width="240"
      :tooltip-formatter="withVNode"
    />
  </el-table>
</template>

<script lang="ts" setup>
import { h } from 'vue'
import { ElLink, type TableTooltipData } from 'element-plus'

type TableData = {
  address: string
  tags: string[]
  url: string
}

const tableData: TableData[] = [
  {
    address: 'Lohrbergstr. 86c, Süd Lilli, Saarland',
    tags: ['Office', 'Home', 'Park', 'Garden'],
    url: 'https://github.com/element-plus/element-plus/issues',
  },
  {
    address: '760 A Street, South Frankfield, Illinois',
    tags: ['error', 'warning', 'success', 'info'],
    url: 'https://github.com/element-plus/element-plus/pulls',
  },
  {
    address: 'Arnold-Ohletz-Str. 41a, Alt Malinascheid, Thüringen',
    tags: ['one', 'two', 'three', 'four', 'five'],
    url: 'https://github.com/element-plus/element-plus/discussions',
  },
  {
    address: '23618 Windsor Drive, West Ricardoview, Idaho',
    tags: ['blue', 'white', 'dark', 'gray', 'red', 'bright'],
    url: 'https://github.com/element-plus/element-plus/actions',
  },
]

const tableRowFormatter = (data: TableTooltipData<TableData>) => {
  return `${data.cellValue}: table formatter`
}

const withVNode = (data: TableTooltipData<TableData>) => {
  return h(ElLink, { type: 'primary', href: data.cellValue }, () =>
    h('span', null, data.cellValue)
  )
}
</script>

<style scoped>
p {
  margin: 10px;
  padding: 0;
}
.tag-item + .tag-item {
  margin-left: 5px;
}
</style>
```

隐藏源代码

## Table API [​](#table-api)

### Table 属性 [​](#table-属性)

| 属性名 | 说明 | 类型 | Default |
| --- | --- | --- | --- |
| data | 表数据 | `array` | \[\] |
| height | table 的高度。 默认为自动高度。 如果 height 为 number 类型，单位 px；如果 height 为 string 类型，则这个高度会设置为 Table 的 style.height 的值，Table 的高度会受控于外部样式。 | `string` / `number` | — |
| max-height | table 的最大高度。 合法的值为数字或者单位为 px 的高度。 | `string` / `number` | — |
| stripe | 是否为斑马纹 table | `boolean` | false |
| border | 是否带有纵向边框 | `boolean` | false |
| size | Table 的尺寸 | `enum` | — |
| fit | 列的宽度是否自撑开 | `boolean` | true |
| show-header | 是否显示表头 | `boolean` | true |
| highlight-current-row | 是否要高亮当前行 | `boolean` | false |
| current-row-key | 当前行的 key，只写属性 | `string` / `number` | — |
| row-class-name | 行的 className 的回调方法，也可以使用字符串为所有行设置一个固定的 className。 | `Function` / `string` | — |
| row-style | 行的 style 的回调方法，也可以使用一个固定的 Object 为所有行设置一样的 Style。 | `Function` / `object` | — |
| cell-class-name | 单元格的 className 的回调方法，也可以使用字符串为所有单元格设置一个固定的 className。 | `Function` / `string` | — |
| cell-style | 单元格的 style 的回调方法，也可以使用一个固定的 Object 为所有单元格设置一样的 Style。 | `Function` / `object` | — |
| header-row-class-name | 表头行的 className 的回调方法，也可以使用字符串为所有表头行设置一个固定的 className。 | `Function` / `string` | — |
| header-row-style | 表头行的 style 的回调方法，也可以使用一个固定的 Object 为所有表头行设置一样的 Style。 | `Function` / `object` | — |
| header-cell-class-name | 表头单元格的 className 的回调方法，也可以使用字符串为所有表头单元格设置一个固定的 className。 | `Function` / `string` | — |
| header-cell-style | 表头单元格的 style 的回调方法，也可以使用一个固定的 Object 为所有表头单元格设置一样的 Style。 | `Function` / `object` | — |
| row-key | 行数据的 Key，用来优化 Table 的渲染； 在使用`reserve-selection`功能与显示树形数据时，该属性是必填的。 类型为 String 时，支持多层访问：`user.info.id`，但不支持 `user.info[0].id`，此种情况请使用 `Function`。 | `Function` / `string` | — |
| empty-text | 空数据时显示的文本内容， 也可以通过 `#empty` 设置 | `string` | No Data |
| default-expand-all | 是否默认展开所有行，当 Table 包含展开行存在或者为树形表格时有效 | `boolean` | false |
| expand-row-keys | 可以通过该属性设置 Table 目前的展开行，需要设置 row-key 属性才能使用，该属性为展开行的 keys 数组。 | `array` | — |
| default-sort | 默认的排序列的 prop 和顺序。 它的 `prop` 属性指定默认的排序的列，`order` 指定默认排序的顺序 | `object` | 如果设置了`prop`，但没有设置 `order`，那么 `order`将被默认设置为ascending |
| tooltip-effect | 溢出的 tooltip 的 `effect` | `enum` | dark |
| tooltip-options 2.2.28 | 溢出 tooltip 的选项，[参见下述 tooltip 组件](https://element-plus.org/zh-CN/component/tooltip.html#attributes) | `object` | `object` |
| append-filter-panel-to 2.8.4 | 挂载到哪个 DOM 元素 | `string` | — |
| show-summary | 是否在表尾显示合计行 | `boolean` | false |
| sum-text | 显示摘要行第一列的文本 | `string` | Sum |
| summary-method | 自定义的合计计算方法 | `Function` | — |
| span-method | 合并行或列的计算方法 | `Function` | — |
| select-on-indeterminate | 在多选表格中，当仅有部分行被选中时，点击表头的多选框时的行为。 若为 true，则选中所有行；若为 false，则取消选择所有行 | `boolean` | true |
| indent | 展示树形数据时，树节点的缩进 | `number` | 16 |
| lazy | 是否懒加载子节点数据 | `boolean` | false |
| load | 加载子节点数据的函数，`lazy` 为 true 时生效 | `Function` | — |
| tree-props | 渲染嵌套数据的配置选项 | `object` | `object` |
| table-layout | 设置表格单元、行和列的布局方式 | `enum` | fixed |
| scrollbar-always-on | 总是显示滚动条 | `boolean` | false |
| show-overflow-tooltip | 是否隐藏额外内容并在单元格悬停时使用 Tooltip 显示它们。这将影响全部列的展示，详请参考[tooltip-options](#table-attributes) | `boolean` / [`object`](#table-attributes) 2.3.7 | — |
| flexible 2.2.1 | 确保主轴的最小尺寸，以便不超过内容 | `boolean` | false |
| scrollbar-tabindex 2.8.3 | body 的滚动条的包裹容器 tabindex | `string` / `number` | — |
| allow-drag-last-column 2.9.2 | 是否允许拖动最后一列 | `boolean` | true |
| tooltip-formatter 2.9.4 | 自定义 `show-overflow-tooltip` 时的 tooltip 内容 | `Function` | — |
| preserve-expanded-content 2.9.7 | 在折叠后是否在DOM中保留展开行内容 | `boolean` | false |
| native-scrollbar 2.10.5 | 是否使用原生滚动条样式 | `boolean` | false |
| row-expandable 2.13.2 | 启用可展开行，当表格具有 type="expand" 列时有效 | `Function` | — |

### Table 事件 [​](#table-事件)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| select | 当用户手动勾选数据行的 Checkbox 时触发的事件 | `Function` |
| select-all | 当用户手动勾选全选 Checkbox 时触发的事件 | `Function` |
| selection-change | 当选择项发生变化时会触发该事件 | `Function` |
| cell-mouse-enter | 当单元格 hover 进入时会触发该事件 | `Function` |
| cell-mouse-leave | 当单元格 hover 退出时会触发该事件 | `Function` |
| cell-click | 当某个单元格被点击时会触发该事件 | `Function` |
| cell-dblclick | 当某个单元格被双击击时会触发该事件 | `Function` |
| cell-contextmenu | 当某个单元格被鼠标右键点击时会触发该事件 | `Function` |
| row-click | 当某一行被点击时会触发该事件 | `Function` |
| row-contextmenu | 当某一行被鼠标右键点击时会触发该事件 | `Function` |
| row-dblclick | 当某一行被双击时会触发该事件 | `Function` |
| header-click | 当某一列的表头被点击时会触发该事件 | `Function` |
| header-contextmenu | 当某一列的表头被鼠标右键点击时触发该事件 | `Function` |
| sort-change | 当表格的排序条件发生变化的时候会触发该事件 | `Function` |
| filter-change | 当表格的过滤条件发生变化的时候会触发该事件 | `Function` |
| current-change | 当表格的当前行发生变化的时候会触发该事件，如果要高亮当前行，请打开表格的 highlight-current-row 属性 | `Function` |
| header-dragend | 当拖动表头改变了列的宽度的时候会触发该事件 | `Function` |
| expand-change | 当用户对某一行展开或者关闭的时候会触发该事件（展开行时，回调的第二个参数为 expandedRows；树形表格时第二参数为 expanded） | `Function` |
| scroll 2.9.0 | 表格被用户滚动后触发 | `Function` |

### Table 插槽 [​](#table-插槽)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | Table-column |
| append | 插入至表格最后一行之后的内容， 如果需要对表格的内容进行无限滚动操作，可能需要用到这个 slot。 若表格有合计行，该 slot 会位于合计行之上。 | — |
| empty | 当数据为空时自定义的内容 | — |

### Table Exposes [​](#table-exposes)

| 方法名 | 说明 | Type |
| --- | --- | --- |
| clearSelection | 用于多选表格，清空用户的选择 | `Function` |
| getSelectionRows | 返回当前选中的行 | `Function` |
| getHalfSelectionRows 2.14.2 | 返回当前半选中的行 | `Function` |
| toggleRowSelection | 用于多选表格，切换某一行的选中状态， 如果使用了第二个参数，则可直接设置这一行选中与否 | `Function` |
| toggleAllSelection | 用于多选表格，切换全选和全不选 | `Function` |
| toggleRowExpansion | 用于可扩展的表格或树表格，如果某行被扩展，则切换。 使用第二个参数，您可以直接设置该行应该被扩展或折叠。 | `Function` |
| setCurrentRow | 用于单选表格，设定某一行为选中行， 如果调用时不加参数，则会取消目前高亮行的选中状态。 | `Function` |
| clearSort | 用于清空排序条件，数据会恢复成未排序的状态 | `Function` |
| clearFilter | 传入由`columnKey` 组成的数组以清除指定列的过滤条件。 如果没有参数，清除所有过滤器 | `Function` |
| doLayout | 对 Table 进行重新布局。 当表格可见性变化时，您可能需要调用此方法以获得正确的布局 | `Function` |
| sort | 手动排序表格。 参数 `prop` 属性指定排序列，`order` 指定排序顺序。 | `Function` |
| scrollTo | 滚动到一组特定坐标 | `Function` |
| setScrollTop | 设置垂直滚动位置 | `Function` |
| setScrollLeft | 设置水平滚动位置 | `Function` |
| columns 2.7.6 | 获取表列的 context | `array` |
| updateKeyChildren 2.8.4 | 适用于 lazy Table, 需要设置 `rowKey`, 更新 key children | `Function` |

## Table-column API [​](#table-column-api)

### Table-column 属性 [​](#table-column-属性)

| 属性名 | 说明 | Type | 默认值 |
| --- | --- | --- | --- |
| type | 对应列的类型。 如果设置了`selection`则显示多选框； 如果设置了 `index` 则显示该行的索引（从 1 开始计算）； 如果设置了 `expand` 则显示为一个可展开的按钮 | `enum` | default |
| index | 如果设置了 `type=index`，可以通过传递 `index` 属性来自定义索引 | `number` / `Function` | — |
| label | 显示的标题 | `string` | — |
| column-key | column 的 key， column 的 key， 如果需要使用 filter-change 事件，则需要此属性标识是哪个 column 的筛选条件 | `string` | — |
| prop | 字段名称 对应列内容的字段名， 也可以使用 `property`属性 | `string` | — |
| width | 对应列的宽度 | `string` / `number` | '' |
| min-width | 对应列的最小宽度， 对应列的最小宽度， 与 `width` 的区别是 `width` 是固定的，`min-width` 会把剩余宽度按比例分配给设置了 `min-width` 的列 | `string` / `number` | '' |
| fixed | 列是否固定在左侧或者右侧。 `true` 表示固定在左侧 | `enum` / `boolean` | false |
| render-header | 列标题 Label 区域渲染使用的 Function | `Function` | — |
| sortable | 对应列是否可以排序， 如果设置为 'custom'，则代表用户希望远程排序，需要监听 Table 的 sort-change 事件 | `boolean` / `string` | false |
| sort-method | 指定数据按照哪个属性进行排序，仅当`sortable`设置为`true`的时候有效。 应该如同 Array.sort 那样返回一个 Number | `Function` | — |
| sort-by | 指定数据按照哪个属性进行排序，仅当 sortable 设置为 true 且没有设置 sort-method 的时候有效。 如果 sort-by 为数组，则先按照第 1 个属性排序，如果第 1 个相等，再按照第 2 个排序，以此类推 | `Function` / `string` / `array` | — |
| sort-orders | 数据在排序时所使用排序策略的轮转顺序，仅当 sortable 为 true 时有效。 需传入一个数组，随着用户点击表头，该列依次按照数组中元素的顺序进行排序 | `object` | \['ascending', 'descending', null\] |
| resizable | 对应列是否可以通过拖动改变宽度（需要在 el-table 上设置 border 属性为真） | `boolean` | true |
| formatter | 用来格式化内容 | `Function` | — |
| show-overflow-tooltip | 当内容过长被隐藏时显示 tooltip | `boolean` / [`object`](#table-attributes) 2.2.28 | undefined |
| align | 对齐方式 | `enum` | left |
| header-align | 表头对齐方式， 若不设置该项，则使用表格的对齐方式 | `enum` | left |
| class-name | 列的 className | `string` | — |
| label-class-name | 当前列标题的自定义类名 | `string` | — |
| selectable | 仅对 type=selection 的列有效，类型为 Function，Function 的返回值用来决定这一行的 CheckBox 是否可以勾选 | `Function` | — |
| reserve-selection | 数据刷新后是否保留选项，仅对 `type=selection` 的列有效， 请注意， 需指定 `row-key` 来让这个功能生效。 | `boolean` | false |
| filters | 数据过滤的选项， 数组格式，数组中的元素需要有 text 和 value 属性。 数组中的每个元素都需要有 text 和 value 属性。 | `array` | ::: |
| filter-placement | 过滤弹出框的定位 | `enum` | — |
| filter-class-name 2.5.0 | 过滤弹出框的 className | `string` | — |
| filter-multiple | 数据过滤的选项是否多选 | `boolean` | true |
| filter-method | 数据过滤使用的方法， 如果是多选的筛选项，对每一条数据会执行多次，任意一次返回 true 就会显示。 | `Function` | ::: |
| filtered-value | 选中的数据过滤项，如果需要自定义表头过滤的渲染方式，可能会需要此属性。 | `array` | — |
| tooltip-formatter 2.9.4 | 使用 `show-overflow-tooltip` 时自定义 tooltip 内容 | `Function` | — |

### Table-column 插槽 [​](#table-column-插槽)

| 插槽名 | 说明 | 类型 |
| --- | --- | --- |
| default | 自定义列的内容 | `object` |
| header | 自定义表头的内容， | `object` |
| filter-icon 2.7.8 | 自定义 filter 图标 | `object` |
| expand 2.10.0 | 展开列的自定义内容 从 v2.13.2 开始支持 `expandable` 属性。 | `object` |

## Type Declarations [​](#type-declarations)

显示类型声明

ts

```
interface Sort {
  prop: string
  order: 'ascending' | 'descending'
  init?: any
  silent?: any
}

interface TreeNode {
  expanded?: boolean
  loading?: boolean
  noLazyChildren?: boolean
  indent?: number
  level?: number
  display?: boolean
}

type DefaultRow = Record<PropertyKey, any>

type TableColumnCtx<T extends DefaultRow = DefaultRow> = {
  id: string
  realWidth: number | null
  type: string
  label: string
  className: string
  labelClassName: string
  property: string
  prop: string
  width?: string | number
  minWidth: string | number
  renderHeader: (data: CI<T>) => VNode
  sortable: boolean | string
  sortMethod: (a: T, b: T) => number
  sortBy: string | ((row: T, index: number, array?: T[]) => string) | string[]
  resizable: boolean
  columnKey: string
  rawColumnKey: string
  align: string
  headerAlign: string
  showOverflowTooltip?: boolean | TableOverflowTooltipOptions
  tooltipFormatter?: TableOverflowTooltipFormatter<T>
  fixed: boolean | string
  formatter: (
    row: T,
    column: TableColumnCtx<T>,
    cellValue: any,
    index: number
  ) => VNode | string
  selectable: (row: T, index: number) => boolean
  reserveSelection: boolean
  filterMethod: FilterMethods<T>
  filteredValue: string[]
  filters: Filters
  filterPlacement: string
  filterMultiple: boolean
  filterClassName: string
  index: number | ((index: number) => number)
  sortOrders: (TableSortOrder | null)[]
  renderCell: (data: any) => VNode | VNode[]
  colSpan: number
  rowSpan: number
  children?: TableColumnCtx<T>[]
  level: number
  filterable: boolean | FilterMethods<T> | Filters
  order: TableSortOrder | null
  isColumnGroup: boolean
  isSubColumn: boolean
  columns: TableColumnCtx<T>[]
  getColumnIndex: () => number
  no: number
  filterOpened?: boolean
  renderFilterIcon?: (scope: any) => VNode
  renderExpand?: (scope: any) => VNode
}
```

## 常见问题解答（FAQ） [​](#常见问题解答-faq)

#### 如何为 `el-table-column` 推断正确的插槽类型？ [​](#如何为-el-table-column-推断正确的插槽类型)

`el-table-column` 是一个泛型组件。 如果 TypeScript 无法从上下文中推断其插槽的行类型，请在 `el-table-column` 前紧挨着添加 Vue 的 `@vue-generic` 指令注释，并显式传入行类型。 更多细节请参考 Vue 文档 [Generics](https://vuejs.org/api/sfc-script-setup.html#generics).

vue

```
<template>
  <el-table :data="tableData">
    <!-- @vue-generic {User} -->
    <el-table-column label="Name">
      <template #default="{ row }">
        {{ row.name }}
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
interface User {
  name: string
  address: string
}

const tableData: User[] = [
  {
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },
]
</script>
```

#### 如何在表格中使用图像预览？ [​](#如何在表格中使用图像预览)

vue

```
<template>
  <el-table-column width="180">
    <template #default="scope">
      <el-image preview-teleported :preview-src-list="srcList" />
    </template>
  </el-table-column>
</template>
```

#### 当使用 DOM 模板时，为什么列没有渲染？ [​](#当使用-dom-模板时-为什么列没有渲染)

典型问题： [#5046](https://github.com/element-plus/element-plus/issues/5046) [#5862](https://github.com/element-plus/element-plus/issues/5862) [#6919](https://github.com/element-plus/element-plus/issues/6919)

这是因为 HTML 定义只允许一些特定元素省略关闭标签，最常见的是 `<input>` 和 `<img>`。 对于任意其他元素，如果你省略了关闭标签，原生的 HTML 解析器会认为你从未关闭打开的标签。

详情请参阅 [Vue 文档](https://vuejs.org/guide/essentials/component-basics.html#self-closing-tags)。

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/table) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/table.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/table.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/24290011?v=4&size=64)](https://github.com/xingyixiang)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/30046649?v=4&size=64)](https://github.com/MrWeilian)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/45098544?v=4&size=64)](https://github.com/tuzixiangs)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/38874640?v=4&size=64)](https://github.com/wNing50)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/59350883?v=4&size=64)](https://github.com/init-qy)[![](https://avatars.githubusercontent.com/u/25472916?v=4&size=64)](https://github.com/wiidede)[![](https://avatars.githubusercontent.com/u/45122329?v=4&size=64)](https://github.com/cokemine)[![](https://avatars.githubusercontent.com/u/46664126?v=4&size=64)](https://github.com/btnkr)[![](https://avatars.githubusercontent.com/u/126545033?v=4&size=64)](https://github.com/dhj-l)[![](https://avatars.githubusercontent.com/u/54931083?v=4&size=64)](https://github.com/wjp980108)[![](https://avatars.githubusercontent.com/u/30883395?v=4&size=64)](https://github.com/webvs2)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/17523626?v=4&size=64)](https://github.com/dowinweb)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/30335393?v=4&size=64)](https://github.com/justwiner)[![](https://avatars.githubusercontent.com/u/67093787?v=4&size=64)](https://github.com/tinyfind)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/31885971?v=4&size=64)](https://github.com/wonderl17)[![](https://avatars.githubusercontent.com/u/26755049?v=4&size=64)](https://github.com/qq282126990)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/9188028?v=4&size=64)](https://github.com/406087475)[![](https://avatars.githubusercontent.com/u/71749650?v=4&size=64)](https://github.com/qeTM)[![](https://avatars.githubusercontent.com/u/45625953?v=4&size=64)](https://github.com/an501920078)[![](https://avatars.githubusercontent.com/u/158829893?v=4&size=64)](https://github.com/JoiePink)[![](https://avatars.githubusercontent.com/u/67700142?v=4&size=64)](https://github.com/vueWorker-x)[![](https://avatars.githubusercontent.com/u/31912749?v=4&size=64)](https://github.com/KeroZhai)[![](https://avatars.githubusercontent.com/u/33254923?v=4&size=64)](https://github.com/yicheny)[![](https://avatars.githubusercontent.com/u/127294190?v=4&size=64)](https://github.com/xuhuaiyu24)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/96716634?v=4&size=64)](https://github.com/ylcjwq)[![](https://avatars.githubusercontent.com/u/45786118?v=4&size=64)](https://github.com/realainov)[![](https://avatars.githubusercontent.com/u/27413795?v=4&size=64)](https://github.com/SpanManX)[![](https://avatars.githubusercontent.com/u/33643257?v=4&size=64)](https://github.com/OFreshman)[![](https://avatars.githubusercontent.com/u/59353463?v=4&size=64)](https://github.com/xiaohe0601)[![](https://avatars.githubusercontent.com/u/59367231?v=4&size=64)](https://github.com/qp666)[![](https://avatars.githubusercontent.com/u/45218946?v=4&size=64)](https://github.com/comp-squirrel)[![](https://avatars.githubusercontent.com/u/82485978?v=4&size=64)](https://github.com/EralChen)[![](https://avatars.githubusercontent.com/u/16640248?v=4&size=64)](https://github.com/chengang4505)[![](https://avatars.githubusercontent.com/u/132551120?v=4&size=64)](https://github.com/YiMo1)[![](https://avatars.githubusercontent.com/u/26403700?v=4&size=64)](https://github.com/blesstosam)[![](https://avatars.githubusercontent.com/u/8591261?v=4&size=64)](https://github.com/zeyongTsai)[![](https://avatars.githubusercontent.com/u/70090558?v=4&size=64)](https://github.com/starryeve)[![](https://avatars.githubusercontent.com/u/48341368?v=4&size=64)](https://github.com/HaceraI)[![](https://avatars.githubusercontent.com/u/204166003?v=4&size=64)](https://github.com/Putia3)[![](https://avatars.githubusercontent.com/u/22910740?v=4&size=64)](https://github.com/StephenKe)[![](https://avatars.githubusercontent.com/u/839559?v=4&size=64)](https://github.com/FrankFang)[![](https://avatars.githubusercontent.com/u/23010875?v=4&size=64)](https://github.com/bartoszrudzinski)[![](https://avatars.githubusercontent.com/u/18254135?v=4&size=64)](https://github.com/zhengbangbo)[![](https://avatars.githubusercontent.com/u/23442840?v=4&size=64)](https://github.com/liunnn1994)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/20264397?v=4&size=64)](https://github.com/Simplifer)[![](https://avatars.githubusercontent.com/u/29966471?v=4&size=64)](https://github.com/tiandaoyi)[![](https://avatars.githubusercontent.com/u/6063358?v=4&size=64)](https://github.com/xxholly32)[![](https://avatars.githubusercontent.com/u/101238421?v=4&size=64)](https://github.com/acyza)[![](https://avatars.githubusercontent.com/u/2098770?v=4&size=64)](https://github.com/liuyutao)[![](https://avatars.githubusercontent.com/u/33687038?v=4&size=64)](https://github.com/guozi9999)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/38490578?v=4&size=64)](https://github.com/yuyinws)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/42139754?v=4&size=64)](https://github.com/zyyv)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/144224541?v=4&size=64)](https://github.com/xixiIBN5100)[![](https://avatars.githubusercontent.com/u/59329360?v=4&size=64)](https://github.com/electroluxcode)[![](https://avatars.githubusercontent.com/u/16920092?v=4&size=64)](https://github.com/LiZheGuang)[![](https://avatars.githubusercontent.com/u/29250746?v=4&size=64)](https://github.com/lxy030988)[![](https://avatars.githubusercontent.com/u/6340506?v=4&size=64)](https://github.com/mdoi2)[![](https://avatars.githubusercontent.com/u/42017165?v=4&size=64)](https://github.com/Mario34)[![](https://avatars.githubusercontent.com/u/13410410?v=4&size=64)](https://github.com/jaa134)[![](https://avatars.githubusercontent.com/u/42532333?v=4&size=64)](https://github.com/ivan0525)[![](https://avatars.githubusercontent.com/u/20083373?v=4&size=64)](https://github.com/Cenavy1019)[![](https://avatars.githubusercontent.com/u/87003751?v=4&size=64)](https://github.com/faga295)[![](https://avatars.githubusercontent.com/u/57086651?v=4&size=64)](https://github.com/Simon-He95)[![](https://avatars.githubusercontent.com/u/46318880?v=4&size=64)](https://github.com/yangliguo7)[![](https://avatars.githubusercontent.com/u/49601167?v=4&size=64)](https://github.com/jianjunyuu)[![](https://avatars.githubusercontent.com/u/169252980?v=4&size=64)](https://github.com/xiaochenchen-igg-com)[![](https://avatars.githubusercontent.com/u/44334858?v=4&size=64)](https://github.com/k713927)[![](https://avatars.githubusercontent.com/u/26833520?v=4&size=64)](https://github.com/josonho)[![](https://avatars.githubusercontent.com/u/1744129?v=4&size=64)](https://github.com/hminghe)[![](https://avatars.githubusercontent.com/u/45614103?v=4&size=64)](https://github.com/kakigakki)[![](https://avatars.githubusercontent.com/u/17698194?v=4&size=64)](https://github.com/nieyuyao)[![](https://avatars.githubusercontent.com/u/15374687?v=4&size=64)](https://github.com/zhangshichun)[![](https://avatars.githubusercontent.com/u/22695767?v=4&size=64)](https://github.com/deepthan)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)[![](https://avatars.githubusercontent.com/u/29143658?v=4&size=64)](https://github.com/HaitaoWang555)

[Skeleton 骨架屏](https://element-plus.org/zh-CN/component/skeleton)

[Virtualized Table 虚拟化表格](https://element-plus.org/zh-CN/component/table-v2)


