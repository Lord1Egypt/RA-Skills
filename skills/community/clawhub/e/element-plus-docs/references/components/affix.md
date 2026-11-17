## Affix 固钉 ​

**URL:** https://element-plus.org/zh-CN/component/affix

**Contents:**
- Affix 固钉 ​
- 基础用法 ​
- 指定容器 ​
- 固定位置 ​
- API ​
  - 属性 ​
  - 事件 ​
  - 插槽 ​
  - 暴露 ​
- 源代码 ​

通过设置 offset 属性来改变吸顶距离，默认值为 0。

通过设置 target 属性，让固钉始终保持在容器内， 超过范围则隐藏。

Affix 组件提供 2 个固定的位置参数 top 和 bottom。

通过设置 position 属性来改变固定位置，默认值为 top 。

**Examples:**

Example 1 (typescript):
```typescript
<template>
  <el-affix :offset="120">
    <el-button type="primary">Offset top 120px</el-button>
  </el-affix>
</template>
```

Example 2 (vue):
```vue
<template>
  <div class="affix-container">
    <el-affix target=".affix-container" :offset="80">
      <el-button type="primary">Target container</el-button>
    </el-affix>
  </div>
</template>

<style scoped>
.affix-container {
  text-align: center;
  height: 400px;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
}
</style>
```

Example 3 (typescript):
```typescript
<template>
  <el-affix position="bottom" :offset="20">
    <el-button type="primary">Offset bottom 20px</el-button>
  </el-affix>
</template>
```

---
