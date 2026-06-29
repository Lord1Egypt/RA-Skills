---
name: "pagination"
description: "Pagination 分页 -- Element Plus Vue3 桌面端组件。Invoke when user needs Pagination 分页 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/pagination.html"
---

---

# Pagination 分页 [​](#pagination-分页)

更新日志待解决

9

当数据量过多时，使用分页分解数据。

## 基础用法 [​](#基础用法)

设置`layout`，表示需要显示的内容，用逗号分隔，布局元素会依次显示。 分页元素包括：`prev`（跳转到上一页的按钮）、`next`（跳转到下一页的按钮）、`pager`（页码列表）、`jumper`（跳转输入框）、`total`（总条目数）、`sizes`（用于设置每页条数的选择器）以及 `->`（该符号之后的所有元素将被靠右对齐）。

When you have few pages

-   1
-   2
-   3
-   4
-   5

When you have more than 7 pages

-   1
-   2
-   3
-   4
-   5
-   6

-   100

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZXhhbXBsZS1wYWdpbmF0aW9uLWJsb2NrXCI+XG4gICAgPGRpdiBjbGFzcz1cImV4YW1wbGUtZGVtb25zdHJhdGlvblwiPldoZW4geW91IGhhdmUgZmV3IHBhZ2VzPC9kaXY+XG4gICAgPGVsLXBhZ2luYXRpb24gbGF5b3V0PVwicHJldiwgcGFnZXIsIG5leHRcIiA6dG90YWw9XCI1MFwiIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwiZXhhbXBsZS1wYWdpbmF0aW9uLWJsb2NrXCI+XG4gICAgPGRpdiBjbGFzcz1cImV4YW1wbGUtZGVtb25zdHJhdGlvblwiPldoZW4geW91IGhhdmUgbW9yZSB0aGFuIDcgcGFnZXM8L2Rpdj5cbiAgICA8ZWwtcGFnaW5hdGlvbiBsYXlvdXQ9XCJwcmV2LCBwYWdlciwgbmV4dFwiIDp0b3RhbD1cIjEwMDBcIiAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZXhhbXBsZS1wYWdpbmF0aW9uLWJsb2NrICsgLmV4YW1wbGUtcGFnaW5hdGlvbi1ibG9jayB7XG4gIG1hcmdpbi10b3A6IDEwcHg7XG59XG4uZXhhbXBsZS1wYWdpbmF0aW9uLWJsb2NrIC5leGFtcGxlLWRlbW9uc3RyYXRpb24ge1xuICBtYXJnaW4tYm90dG9tOiAxNnB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/pagination/basic-usage.vue)_

vue

```
<template>
  <div class="example-pagination-block">
    <div class="example-demonstration">When you have few pages</div>
    <el-pagination layout="prev, pager, next" :total="50" />
  </div>
  <div class="example-pagination-block">
    <div class="example-demonstration">When you have more than 7 pages</div>
    <el-pagination layout="prev, pager, next" :total="1000" />
  </div>
</template>

<style scoped>
.example-pagination-block + .example-pagination-block {
  margin-top: 10px;
}
.example-pagination-block .example-demonstration {
  margin-bottom: 16px;
}
</style>
```

隐藏源代码

## 设置最大页码按钮数 [​](#设置最大页码按钮数)

默认情况下，当总页数超过 7 页时，Pagination 会折叠多余的页码按钮。 通过 `pager-count` 属性可以设置最大页码按钮数。

-   1
-   2
-   3
-   4
-   5
-   6
-   7
-   8
-   9
-   10

-   50

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcGFnaW5hdGlvblxuICAgIDpwYWdlLXNpemU9XCIyMFwiXG4gICAgOnBhZ2VyLWNvdW50PVwiMTFcIlxuICAgIGxheW91dD1cInByZXYsIHBhZ2VyLCBuZXh0XCJcbiAgICA6dG90YWw9XCIxMDAwXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/pagination/number-of-pagers.vue)_

vue

```
<template>
  <el-pagination
    :page-size="20"
    :pager-count="11"
    layout="prev, pager, next"
    :total="1000"
  />
</template>
```

隐藏源代码

## 带有背景色的分页 [​](#带有背景色的分页)

设置`background`属性可以为分页按钮添加背景色。

-   1
-   2
-   3
-   4
-   5
-   6

-   100

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcGFnaW5hdGlvbiBiYWNrZ3JvdW5kIGxheW91dD1cInByZXYsIHBhZ2VyLCBuZXh0XCIgOnRvdGFsPVwiMTAwMFwiIC8+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/pagination/background-color.vue)_

vue

```
<template>
  <el-pagination background layout="prev, pager, next" :total="1000" />
</template>
```

隐藏源代码

## 小型分页 [​](#小型分页)

在空间有限的情况下，可以使用简单的小型分页。

通过`size`更改大小 这是个 `small`的例子

-   1
-   2
-   3
-   4
-   5

-   1
-   2
-   3
-   4
-   5

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcGFnaW5hdGlvbiBzaXplPVwic21hbGxcIiBsYXlvdXQ9XCJwcmV2LCBwYWdlciwgbmV4dFwiIDp0b3RhbD1cIjUwXCIgLz5cbiAgPGVsLXBhZ2luYXRpb25cbiAgICBzaXplPVwic21hbGxcIlxuICAgIGJhY2tncm91bmRcbiAgICBsYXlvdXQ9XCJwcmV2LCBwYWdlciwgbmV4dFwiXG4gICAgOnRvdGFsPVwiNTBcIlxuICAgIGNsYXNzPVwibXQtNFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/pagination/small-pagination.vue)_

vue

```
<template>
  <el-pagination size="small" layout="prev, pager, next" :total="50" />
  <el-pagination
    size="small"
    background
    layout="prev, pager, next"
    :total="50"
    class="mt-4"
  />
</template>
```

隐藏源代码

## 当只有一页时隐藏分页 [​](#当只有一页时隐藏分页)

当只有一页时，通过设置 `hide-on-single-page` 属性来隐藏分页。

* * *

-   1

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1zd2l0Y2ggdi1tb2RlbD1cInZhbHVlXCIgLz5cbiAgICA8aHIgY2xhc3M9XCJteS00XCIgLz5cbiAgICA8ZWwtcGFnaW5hdGlvblxuICAgICAgOmhpZGUtb24tc2luZ2xlLXBhZ2U9XCJ2YWx1ZVwiXG4gICAgICA6dG90YWw9XCI1XCJcbiAgICAgIGxheW91dD1cInByZXYsIHBhZ2VyLCBuZXh0XCJcbiAgICAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKGZhbHNlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/pagination/auto-hide-pagination.vue)_

vue

```
<template>
  <div>
    <el-switch v-model="value" />
    <hr class="my-4" />
    <el-pagination
      :hide-on-single-page="value"
      :total="5"
      layout="prev, pager, next"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref(false)
</script>
```

隐藏源代码

## 附加功能 [​](#附加功能)

根据场景需要，可以添加其他功能模块。

此示例是一个完整的用例。 使用了 `size-change` 和 `current-change` 事件来处理页码大小和当前页变动时候触发的事件。 `page-sizes`接受一个整数类型的数组，数组元素为展示的选择每页显示个数的选项，`[100, 200, 300, 400]` 表示四个选项，每页显示 100 个，200 个，300 个或者 400 个。

defaultlargesmall

background:

disabled:

* * *

Total item count

Total 1000

-   1

-   3
-   4
-   5
-   6
-   7

-   10

Change page size

100/page

-   1

-   3
-   4
-   5
-   6
-   7

-   10

Jump to

-   1

-   3
-   4
-   5
-   6
-   7

-   10

Go to

All combined

Total 400

100/page

-   1
-   2
-   3
-   4

Go to

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBpdGVtcy1jZW50ZXIgbWItNFwiPlxuICAgIDxlbC1yYWRpby1ncm91cCB2LW1vZGVsPVwic2l6ZVwiIGNsYXNzPVwibXItNFwiPlxuICAgICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cImRlZmF1bHRcIj5kZWZhdWx0PC9lbC1yYWRpby1idXR0b24+XG4gICAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwibGFyZ2VcIj5sYXJnZTwvZWwtcmFkaW8tYnV0dG9uPlxuXG4gICAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwic21hbGxcIj5zbWFsbDwvZWwtcmFkaW8tYnV0dG9uPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gICAgPGRpdj5cbiAgICAgIGJhY2tncm91bmQ6XG4gICAgICA8ZWwtc3dpdGNoIHYtbW9kZWw9XCJiYWNrZ3JvdW5kXCIgY2xhc3M9XCJtbC0yXCIgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwibWwtNFwiPlxuICAgICAgZGlzYWJsZWQ6IDxlbC1zd2l0Y2ggdi1tb2RlbD1cImRpc2FibGVkXCIgY2xhc3M9XCJtbC0yXCIgLz5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG5cbiAgPGhyIGNsYXNzPVwibXktNFwiIC8+XG5cbiAgPGRpdiBjbGFzcz1cImRlbW8tcGFnaW5hdGlvbi1ibG9ja1wiPlxuICAgIDxkaXYgY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+VG90YWwgaXRlbSBjb3VudDwvZGl2PlxuICAgIDxlbC1wYWdpbmF0aW9uXG4gICAgICB2LW1vZGVsOmN1cnJlbnQtcGFnZT1cImN1cnJlbnRQYWdlMVwiXG4gICAgICA6cGFnZS1zaXplPVwiMTAwXCJcbiAgICAgIDpzaXplPVwic2l6ZVwiXG4gICAgICA6ZGlzYWJsZWQ9XCJkaXNhYmxlZFwiXG4gICAgICA6YmFja2dyb3VuZD1cImJhY2tncm91bmRcIlxuICAgICAgbGF5b3V0PVwidG90YWwsIHByZXYsIHBhZ2VyLCBuZXh0XCJcbiAgICAgIDp0b3RhbD1cIjEwMDBcIlxuICAgICAgQHNpemUtY2hhbmdlPVwiaGFuZGxlU2l6ZUNoYW5nZVwiXG4gICAgICBAY3VycmVudC1jaGFuZ2U9XCJoYW5kbGVDdXJyZW50Q2hhbmdlXCJcbiAgICAvPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cImRlbW8tcGFnaW5hdGlvbi1ibG9ja1wiPlxuICAgIDxkaXYgY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+Q2hhbmdlIHBhZ2Ugc2l6ZTwvZGl2PlxuICAgIDxlbC1wYWdpbmF0aW9uXG4gICAgICB2LW1vZGVsOmN1cnJlbnQtcGFnZT1cImN1cnJlbnRQYWdlMlwiXG4gICAgICB2LW1vZGVsOnBhZ2Utc2l6ZT1cInBhZ2VTaXplMlwiXG4gICAgICA6cGFnZS1zaXplcz1cIlsxMDAsIDIwMCwgMzAwLCA0MDBdXCJcbiAgICAgIDpzaXplPVwic2l6ZVwiXG4gICAgICA6ZGlzYWJsZWQ9XCJkaXNhYmxlZFwiXG4gICAgICA6YmFja2dyb3VuZD1cImJhY2tncm91bmRcIlxuICAgICAgbGF5b3V0PVwic2l6ZXMsIHByZXYsIHBhZ2VyLCBuZXh0XCJcbiAgICAgIDp0b3RhbD1cIjEwMDBcIlxuICAgICAgQHNpemUtY2hhbmdlPVwiaGFuZGxlU2l6ZUNoYW5nZVwiXG4gICAgICBAY3VycmVudC1jaGFuZ2U9XCJoYW5kbGVDdXJyZW50Q2hhbmdlXCJcbiAgICAvPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cImRlbW8tcGFnaW5hdGlvbi1ibG9ja1wiPlxuICAgIDxkaXYgY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+SnVtcCB0bzwvZGl2PlxuICAgIDxlbC1wYWdpbmF0aW9uXG4gICAgICB2LW1vZGVsOmN1cnJlbnQtcGFnZT1cImN1cnJlbnRQYWdlM1wiXG4gICAgICB2LW1vZGVsOnBhZ2Utc2l6ZT1cInBhZ2VTaXplM1wiXG4gICAgICA6c2l6ZT1cInNpemVcIlxuICAgICAgOmRpc2FibGVkPVwiZGlzYWJsZWRcIlxuICAgICAgOmJhY2tncm91bmQ9XCJiYWNrZ3JvdW5kXCJcbiAgICAgIGxheW91dD1cInByZXYsIHBhZ2VyLCBuZXh0LCBqdW1wZXJcIlxuICAgICAgOnRvdGFsPVwiMTAwMFwiXG4gICAgICBAc2l6ZS1jaGFuZ2U9XCJoYW5kbGVTaXplQ2hhbmdlXCJcbiAgICAgIEBjdXJyZW50LWNoYW5nZT1cImhhbmRsZUN1cnJlbnRDaGFuZ2VcIlxuICAgIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwiZGVtby1wYWdpbmF0aW9uLWJsb2NrXCI+XG4gICAgPGRpdiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5BbGwgY29tYmluZWQ8L2Rpdj5cbiAgICA8ZWwtcGFnaW5hdGlvblxuICAgICAgdi1tb2RlbDpjdXJyZW50LXBhZ2U9XCJjdXJyZW50UGFnZTRcIlxuICAgICAgdi1tb2RlbDpwYWdlLXNpemU9XCJwYWdlU2l6ZTRcIlxuICAgICAgOnBhZ2Utc2l6ZXM9XCJbMTAwLCAyMDAsIDMwMCwgNDAwXVwiXG4gICAgICA6c2l6ZT1cInNpemVcIlxuICAgICAgOmRpc2FibGVkPVwiZGlzYWJsZWRcIlxuICAgICAgOmJhY2tncm91bmQ9XCJiYWNrZ3JvdW5kXCJcbiAgICAgIGxheW91dD1cInRvdGFsLCBzaXplcywgcHJldiwgcGFnZXIsIG5leHQsIGp1bXBlclwiXG4gICAgICA6dG90YWw9XCI0MDBcIlxuICAgICAgQHNpemUtY2hhbmdlPVwiaGFuZGxlU2l6ZUNoYW5nZVwiXG4gICAgICBAY3VycmVudC1jaGFuZ2U9XCJoYW5kbGVDdXJyZW50Q2hhbmdlXCJcbiAgICAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgQ29tcG9uZW50U2l6ZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgY3VycmVudFBhZ2UxID0gcmVmKDUpXG5jb25zdCBjdXJyZW50UGFnZTIgPSByZWYoNSlcbmNvbnN0IGN1cnJlbnRQYWdlMyA9IHJlZig1KVxuY29uc3QgY3VycmVudFBhZ2U0ID0gcmVmKDQpXG5jb25zdCBwYWdlU2l6ZTIgPSByZWYoMTAwKVxuY29uc3QgcGFnZVNpemUzID0gcmVmKDEwMClcbmNvbnN0IHBhZ2VTaXplNCA9IHJlZigxMDApXG5jb25zdCBzaXplID0gcmVmPENvbXBvbmVudFNpemU+KCdkZWZhdWx0JylcbmNvbnN0IGJhY2tncm91bmQgPSByZWYoZmFsc2UpXG5jb25zdCBkaXNhYmxlZCA9IHJlZihmYWxzZSlcblxuY29uc3QgaGFuZGxlU2l6ZUNoYW5nZSA9ICh2YWw6IG51bWJlcikgPT4ge1xuICBjb25zb2xlLmxvZyhgJHt2YWx9IGl0ZW1zIHBlciBwYWdlYClcbn1cbmNvbnN0IGhhbmRsZUN1cnJlbnRDaGFuZ2UgPSAodmFsOiBudW1iZXIpID0+IHtcbiAgY29uc29sZS5sb2coYGN1cnJlbnQgcGFnZTogJHt2YWx9YClcbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tcGFnaW5hdGlvbi1ibG9jayArIC5kZW1vLXBhZ2luYXRpb24tYmxvY2sge1xuICBtYXJnaW4tdG9wOiAxMHB4O1xufVxuLmRlbW8tcGFnaW5hdGlvbi1ibG9jayAuZGVtb25zdHJhdGlvbiB7XG4gIG1hcmdpbi1ib3R0b206IDE2cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/pagination/more-elements.vue)_

vue

```
<template>
  <div class="flex items-center mb-4">
    <el-radio-group v-model="size" class="mr-4">
      <el-radio-button value="default">default</el-radio-button>
      <el-radio-button value="large">large</el-radio-button>

      <el-radio-button value="small">small</el-radio-button>
    </el-radio-group>
    <div>
      background:
      <el-switch v-model="background" class="ml-2" />
    </div>
    <div class="ml-4">
      disabled: <el-switch v-model="disabled" class="ml-2" />
    </div>
  </div>

  <hr class="my-4" />

  <div class="demo-pagination-block">
    <div class="demonstration">Total item count</div>
    <el-pagination
      v-model:current-page="currentPage1"
      :page-size="100"
      :size="size"
      :disabled="disabled"
      :background="background"
      layout="total, prev, pager, next"
      :total="1000"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
  <div class="demo-pagination-block">
    <div class="demonstration">Change page size</div>
    <el-pagination
      v-model:current-page="currentPage2"
      v-model:page-size="pageSize2"
      :page-sizes="[100, 200, 300, 400]"
      :size="size"
      :disabled="disabled"
      :background="background"
      layout="sizes, prev, pager, next"
      :total="1000"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
  <div class="demo-pagination-block">
    <div class="demonstration">Jump to</div>
    <el-pagination
      v-model:current-page="currentPage3"
      v-model:page-size="pageSize3"
      :size="size"
      :disabled="disabled"
      :background="background"
      layout="prev, pager, next, jumper"
      :total="1000"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
  <div class="demo-pagination-block">
    <div class="demonstration">All combined</div>
    <el-pagination
      v-model:current-page="currentPage4"
      v-model:page-size="pageSize4"
      :page-sizes="[100, 200, 300, 400]"
      :size="size"
      :disabled="disabled"
      :background="background"
      layout="total, sizes, prev, pager, next, jumper"
      :total="400"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { ComponentSize } from 'element-plus'

const currentPage1 = ref(5)
const currentPage2 = ref(5)
const currentPage3 = ref(5)
const currentPage4 = ref(4)
const pageSize2 = ref(100)
const pageSize3 = ref(100)
const pageSize4 = ref(100)
const size = ref<ComponentSize>('default')
const background = ref(false)
const disabled = ref(false)

const handleSizeChange = (val: number) => {
  console.log(`${val} items per page`)
}
const handleCurrentChange = (val: number) => {
  console.log(`current page: ${val}`)
}
</script>

<style scoped>
.demo-pagination-block + .demo-pagination-block {
  margin-top: 10px;
}
.demo-pagination-block .demonstration {
  margin-bottom: 16px;
}
</style>
```

隐藏源代码

## API [​](#api)

### 属性 [​](#属性)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| size 2.7.6 | 分页大小 | `enum` | 'default' |
| background | 是否为分页按钮添加背景色 | `boolean` | false |
| page-size / v-model:page-size | 每页显示条目个数 | `number` | — |
| default-page-size | 每页默认的条目个数，不设置时默认为10 | `number` | — |
| total | 总条目数 | `number` | — |
| page-count | 总页数， `total` 和 `page-count` 设置任意一个就可以达到显示页码的功能；如果要支持 `page-sizes` 的更改，则需要使用 `total` 属性 | `number` | — |
| pager-count | 设置最大页码按钮数。 页码按钮的数量，当总页数超过该值时会折叠 | `number` | 7 |
| current-page / v-model:current-page | 当前页数 | `number` | — |
| default-current-page | 当前页数的默认初始值，不设置时默认为 1 | `number` | — |
| layout | 组件布局，子组件名用逗号分隔 | `string` | prev, pager, next, jumper, ->, total |
| page-sizes | 每页显示个数选择器的选项设置 | `array` | \[10, 20, 30, 40, 50, 100\] |
| append-size-to 2.8.4 | 下拉框挂载到哪个 DOM 元素 | `string` | — |
| popper-class | 每页显示个数选择器的下拉框类名 | `string` | '' |
| popper-style 2.11.5 | 每页显示个数选择器的下拉框样式 | `string` / `object` | aaa |
| prev-text | 替代图标显示的上一页文字 | `string` | '' |
| prev-icon | 上一页的图标， 比 `prev-text` 优先级更高 | `string` / `Component` | ArrowLeft |
| next-text | 替代图标显示的下一页文字 | `string` | '' |
| next-icon | 下一页的图标， 比 `next-text` 优先级更低 | `string` / `Component` | ArrowRight |
| disabled | 是否禁用分页 | `boolean` | false |
| teleported 2.3.13 | 是否将下拉菜单teleport至 body | `boolean` | true |
| hide-on-single-page | 只有一页时是否隐藏 | `boolean` | false |
| small deprecated | 是否使用小型分页样式 | `boolean` | false |

WARNING

我们现在会检查一些不合理的用法，如果发现分页器未显示，可以核对是否违反以下情形：

-   `total` 和 `page-count` 必须传一个，不然组件无法判断总页数；优先使用 `page-count`;
-   如果传入了 `current-page`，必须监听 `current-page` 变更的事件（`@update:current-page`），否则分页切换不起作用；
-   如果传入了 `page-size`，且布局包含 page-size 选择器（即 `layout` 包含 `sizes`），必须监听 `page-size` 变更的事件（`@update:page-size`），否则分页大小的变化将不起作用。

### 事件 [​](#事件)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| size-change | `page-size` 改变时触发 | `Function` |
| current-change | `current-page` 改变时触发 | `Function` |
| change 2.4.4 | `current-page` 或 `page-size` 更改时触发 | `Function` |
| prev-click | 用户点击上一页按钮改变当前页时触发 | `Function` |
| next-click | 用户点击下一页按钮改变当前页时触发 | `Function` |

WARNING

以上事件不推荐使用（但由于兼容的原因仍然支持，在以后的版本中将会被删除）；如果要监听 current-page 和 page-size 的改变，使用 `v-model` 双向绑定是个更好的选择。

### 插槽 [​](#插槽)

| 名称 | 说明 |
| --- | --- |
| default | 自定义内容 设置文案，需要在 `layout` 中列出 `slot` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/pagination) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/pagination.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/pagination.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/5559812?v=4&size=64)](https://github.com/metanas)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/30883395?v=4&size=64)](https://github.com/webvs2)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/3898898?v=4&size=64)](https://github.com/ioslh)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/35400818?v=4&size=64)](https://github.com/ToyCat93)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/24290011?v=4&size=64)](https://github.com/xingyixiang)[![](https://avatars.githubusercontent.com/u/37095891?v=4&size=64)](https://github.com/boomboy4)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/20925158?v=4&size=64)](https://github.com/fzq1998)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/134276765?v=4&size=64)](https://github.com/zwgwf)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/10475770?v=4&size=64)](https://github.com/DarkHighness)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/20411966?v=4&size=64)](https://github.com/SorrowX)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/26358323?v=4&size=64)](https://github.com/wangyuhuiever)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)[![](https://avatars.githubusercontent.com/u/105651386?v=4&size=64)](https://github.com/heappynd)[![](https://avatars.githubusercontent.com/u/35426360?v=4&size=64)](https://github.com/Jungzl)

[Infinite Scroll 无限滚动](https://element-plus.org/zh-CN/component/infinite-scroll)

[Progress 进度条](https://element-plus.org/zh-CN/component/progress)


