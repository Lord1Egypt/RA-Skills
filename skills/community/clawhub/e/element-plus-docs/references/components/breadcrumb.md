## Breadcrumb 面包屑 ​

**URL:** https://element-plus.org/zh-CN/component/breadcrumb

**Contents:**
- Breadcrumb 面包屑 ​
- 基础用法 ​
- 图标分隔符 ​
- Breadcrumb API ​
  - Breadcrumb Attributes ​
  - Breadcrumb Slots ​
- BreadcrumbItem API ​
  - BreadcrumbItem Attributes ​
  - BreadcrumbItem Slots ​
- 源代码 ​

显示当前页面的路径，快速返回之前的任意页面。

在 el-breadcrumb 中使用 el-breadcrumb-item 标签表示从首页开始的每一级。 该组件接受一个 String 类型的参数 separator来作为分隔符。 默认值为 '/'。

通过设置 separator-class 可使用相应的 iconfont 作为分隔符，注意这将使 separator 失效。

**Examples:**

Example 1 (typescript):
```typescript
<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item :to="{ path: '/' }">homepage</el-breadcrumb-item>
    <el-breadcrumb-item>
      <a href="/">promotion management</a>
    </el-breadcrumb-item>
    <el-breadcrumb-item>promotion list</el-breadcrumb-item>
    <el-breadcrumb-item>promotion detail</el-breadcrumb-item>
  </el-breadcrumb>
</template>
```

Example 2 (typescript):
```typescript
<template>
  <el-breadcrumb :separator-icon="ArrowRight">
    <el-breadcrumb-item :to="{ path: '/' }">homepage</el-breadcrumb-item>
    <el-breadcrumb-item>promotion management</el-breadcrumb-item>
    <el-breadcrumb-item>promotion list</el-breadcrumb-item>
    <el-breadcrumb-item>promotion detail</el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script lang="ts" setup>
import { ArrowRight } from '@element-plus/icons-vue'
</script>
```

---
