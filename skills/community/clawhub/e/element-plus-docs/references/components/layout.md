## Layout 布局 ​

**URL:** https://element-plus.org/zh-CN/component/layout

**Contents:**
- Layout 布局 ​
- 基础布局 ​
- 分栏间隔 ​
- 混合布局 ​
- 列偏移 ​
- 对齐方式 ​
- 响应式布局 ​
- 基于断点的隐藏类 ​
- Row API ​
  - Row Attributes ​

通过基础的 24 分栏，迅速简便地创建布局。

组件默认使用 Flex 布局，不需要手动设置 type="flex"。

请注意父容器避免使用 inline 相关样式，会导致组件宽度不能撑满。

通过 row 和 col 组件，并通过 col 组件的 span 属性我们就可以自由地组合布局。

行提供 gutter 属性来指定列之间的间距，其默认值为0。

通过基础的 1/24 分栏任意扩展组合形成较为复杂的混合布局。

通过制定 col 组件的 offset 属性可以指定分栏偏移的栏数。

默认使用 flex 布局来对分栏进行灵活的对齐。

您可以通过justify 属性来定义子元素的排版方式，其取值为start、center、end、space-between、space-around或space-evenly。

参照了 Bootstrap 的 响应式设计，预设了五个响应尺寸：xs、sm、md、lg 和 xl。

Element Plus 额外提供了一系列类名，用于在某些条件下隐藏元素。 这些类名可以添加在任何 DOM 元素或自定义组件上。 如果需要，请自行引入以下文件：

**Examples:**

Example 1 (typescript):
```typescript
<template>
  <el-row>
    <el-col :span="24">
      <div class="grid-content ep-bg-purple-dark" />
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="12">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="12">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="8">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="8">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
    <el-col :span="8">
      <div class="grid-content ep-bg-purple" />
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
  </el-row>
</template>

<style>
.el-row {
  margin-bottom: 20px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
```

Example 2 (typescript):
```typescript
<template>
  <el-row :gutter="20">
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
</template>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
```

Example 3 (typescript):
```typescript
<template>
  <el-row :gutter="20">
    <el-col :span="16"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="8"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="8"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="8"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="16"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
</template>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
```

Example 4 (typescript):
```typescript
<template>
  <el-row :gutter="20">
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6" :offset="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="6" :offset="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="6" :offset="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="12" :offset="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
  </el-row>
</template>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
```

---
