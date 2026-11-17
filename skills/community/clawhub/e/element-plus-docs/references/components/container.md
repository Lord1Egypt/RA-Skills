## Container 布局容器 ​

**URL:** https://element-plus.org/zh-CN/component/container

**Contents:**
- Container 布局容器 ​
- 常见页面布局 ​
- 例子 ​
- Container API ​
  - Container Attributes ​
  - Container Slots ​
- Header API ​
  - Header Attributes ​
  - Header Slots ​
- Aside API ​

用于布局的容器组件，方便快速搭建页面的基本结构：

<el-container>：外层容器。 当子元素中包含 <el-header> 或 <el-footer> 时，全部子元素会垂直上下排列， 否则会水平左右排列。

以上组件采用了 flex 布局，使用前请确定目标浏览器是否兼容。 此外， <el-container>的直接子元素必须是后四个组件中的一个或多个。 后四个组件的父元素必须是一个 <el-container>

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="common-layout">
    <el-container>
      <el-header>Header</el-header>
      <el-main>Main</el-main>
    </el-container>
  </div>
</template>
```

Example 2 (vue):
```vue
<template>
  <div class="common-layout">
    <el-container>
      <el-header>Header</el-header>
      <el-main>Main</el-main>
      <el-footer>Footer</el-footer>
    </el-container>
  </div>
</template>
```

Example 3 (vue):
```vue
<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px">Aside</el-aside>
      <el-main>Main</el-main>
      <el-aside width="200px">Aside</el-aside>
    </el-container>
  </div>
</template>
```

Example 4 (vue):
```vue
<template>
  <div class="common-layout">
    <el-container>
      <el-header>Header</el-header>
      <el-container>
        <el-aside width="200px">Aside</el-aside>
        <el-main>Main</el-main>
      </el-container>
    </el-container>
  </div>
</template>
```

---
