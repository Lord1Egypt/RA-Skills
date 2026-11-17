## Empty 空状态 ​

**URL:** https://element-plus.org/zh-CN/component/empty

**Contents:**
- Empty 空状态 ​
- 基础用法 ​
- 自定义图片 ​
- 图片尺寸 ​
- 底部内容 ​
- 自定义样式 ​
  - 默认变量 ​
- API ​
  - Attributes ​
  - 插槽 ​

通过设置 image 属性传入图片 URL。

通过使用 image-size 属性来控制图片大小。

您可以为empty组件设置自定义样式。 使用 css/scss 语言来更改全局或局部颜色。 我们设置了一些全局颜色变量：--el-empty-fill-color-0、--el-empty-fill-color-1、--el-empty-fill-color-2、……、--el-empty-fill-color-9。 您可以使用类似 :root { --el-empty-fill-color-0: red; --el-empty-fill-color-1: blue; } 等变量。 但通常，如果你想要更改样式，你需要更改所有颜色，因为这些颜色是一个组合。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-empty description="description" />
</template>
```

Example 2 (vue):
```vue
<template>
  <el-empty
    image="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
  />
</template>
```

Example 3 (vue):
```vue
<template>
  <el-empty :image-size="200" />
</template>
```

Example 4 (vue):
```vue
<template>
  <el-empty>
    <el-button type="primary">Button</el-button>
  </el-empty>
</template>
```

---
