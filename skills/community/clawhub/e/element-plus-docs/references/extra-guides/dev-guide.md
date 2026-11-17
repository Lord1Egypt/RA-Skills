## 本地开发 ​

**URL:** https://element-plus.org/zh-CN/guide/dev-guide

**Contents:**
- 本地开发 ​
- 启动项目 ​
- 网站预览 ​
- 本地开发 ​
- 以下命令在开发过程中也很有用 ​
  - 生成组件模板 ​
  - 同步语言文件 ​
  - Contents
    - 链接
    - 社区

该项目将启动网站，网站内你可以预览全部现有组件

根据需要修改 App.vue 文件让开发过程顺利进行

将在 packages/components/awesome 和 packages/components/awesome-button 目录下生成组件模板。

将把 en.ts 语言文件中的新字段同步到其他语言文件，并添加注释 // to be translated。

**Examples:**

Example 1 (unknown):
```unknown
pnpm docs:dev
```

Example 2 (jsx):
```jsx
<template>
  <ComponentYouAreDeveloping />
</template>

<script setup lang="ts">
// make sure this component is registered in @element-plus/components
</script>
```

Example 3 (markdown):
```markdown
pnpm gen <component-name>
# eg.
pnpm gen awesome
pnpm gen awesome-button
```

Example 4 (unknown):
```unknown
pnpm locale:sync
```

---
