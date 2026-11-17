## Pagination 分页 ​

**URL:** https://element-plus.org/zh-CN/component/pagination

**Contents:**
- Pagination 分页 ​
- 基础用法 ​
- 设置最大页码按钮数 ​
- 带有背景色的分页 ​
- 小型分页 ​
- 当只有一页时隐藏分页 ​
- 附加功能 ​
- API ​
  - 属性 ​
  - 事件 ​

设置layout，表示需要显示的内容，用逗号分隔，布局元素会依次显示。 分页元素包括：prev（跳转到上一页的按钮）、next（跳转到下一页的按钮）、pager（页码列表）、jumper（跳转输入框）、total（总条目数）、sizes（用于设置每页条数的选择器）以及 ->（该符号之后的所有元素将被靠右对齐）。

默认情况下，当总页数超过 7 页时，Pagination 会折叠多余的页码按钮。 通过 pager-count 属性可以设置最大页码按钮数。

设置background属性可以为分页按钮添加背景色。

在空间有限的情况下，可以使用简单的小型分页。

通过size更改大小 这是个 small的例子

当只有一页时，通过设置 hide-on-single-page 属性来隐藏分页。

此示例是一个完整的用例。 使用了 size-change 和 current-change 事件来处理页码大小和当前页变动时候触发的事件。 page-sizes接受一个整数类型的数组，数组元素为展示的选择每页显示个数的选项，[100, 200, 300, 400] 表示四个选项，每页显示 100 个，200 个，300 个或者 400 个。

我们现在会检查一些不合理的用法，如果发现分页器未显示，可以核对是否违反以下情形：

以上事件不推荐使用（但由于兼容的原因仍然支持，在以后的版本中将会被删除）；如果要监听 current-page 和 page-size 的改变，使用 v-model 双向绑定是个更好的选择。

**Examples:**

Example 1 (vue):
```vue
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

Example 2 (typescript):
```typescript
<template>
  <el-pagination
    :page-size="20"
    :pager-count="11"
    layout="prev, pager, next"
    :total="1000"
  />
</template>
```

Example 3 (typescript):
```typescript
<template>
  <el-pagination background layout="prev, pager, next" :total="1000" />
</template>
```

Example 4 (typescript):
```typescript
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

---
