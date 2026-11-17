## Text ​

**URL:** https://element-plus.org/zh-CN/component/text

**Contents:**
- Text ​
- 基础用法 ​
- 尺寸 ​
- 省略 ​
- 覆盖 ​
- 混合使用 ​
- API ​
  - Attributes ​
  - Slots ​
- 源代码 ​

由 type 属性来选择 Text 的类型。

使用 size 属性配置尺寸，可选的尺寸大小有: large, default 或 small

通过 truncated 属性，在文本超过视图或最大宽度设置时展示省略符。 通过 line-clamp 属性控制多行的样式

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-text class="mx-1">Default</el-text>
  <el-text class="mx-1" type="primary">Primary</el-text>
  <el-text class="mx-1" type="success">Success</el-text>
  <el-text class="mx-1" type="info">Info</el-text>
  <el-text class="mx-1" type="warning">Warning</el-text>
  <el-text class="mx-1" type="danger">Danger</el-text>
</template>
```

Example 2 (vue):
```vue
<template>
  <el-text class="mx-1" size="large">Large</el-text>
  <el-text class="mx-1">Default</el-text>
  <el-text class="mx-1" size="small">Small</el-text>
</template>
```

Example 3 (jsx):
```jsx
<template>
  <el-text class="w-150px mb-2" truncated>
    Self element set width 100px
  </el-text>
  <el-row class="w-150px mb-2">
    <el-text truncated>Squeezed by parent element</el-text>
  </el-row>
  <el-text line-clamp="2">
    The -webkit-line-clamp CSS property<br />
    allows limiting of the contents of<br />
    a block to the specified number of lines.
  </el-text>
</template>
```

Example 4 (vue):
```vue
<template>
  <el-space direction="vertical">
    <el-text>span</el-text>
    <el-text tag="p">This is a paragraph.</el-text>
    <el-text tag="b">Bold</el-text>
    <el-text tag="i">Italic</el-text>
    <el-text>
      This is
      <el-text tag="sub" size="small">subscript</el-text>
    </el-text>
    <el-text>
      This is
      <el-text tag="sup" size="small">superscript</el-text>
    </el-text>
    <el-text tag="ins">Inserted</el-text>
    <el-text tag="del">Deleted</el-text>
    <el-text tag="mark">Marked</el-text>
  </el-space>
</template>
```

---
