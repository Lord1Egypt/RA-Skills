## Link 链接 ​

**URL:** https://element-plus.org/zh-CN/component/link

**Contents:**
- Link 链接 ​
- 基础用法 ​
- 禁用状态 ​
- 下划线 ​
- 图标 ​
- Link API ​
  - Attributes ​
  - Slots ​
- 源代码 ​
- 贡献者 ​

安全警告 href prop 将会直接渲染到 <a> 标签内部。 如果你传递类似 javascript:alert(1) 这样的值或恶意 URL，可能会导致 XSS 或开放重定向漏洞。

属性 boolean 值 将在 3.0.0 版本中被移除，请考虑切换至新的 API。

从 2.9.9 开始，你可以使用 'always' | 'hover' | 'never' 来控制是否显示下划线。 文档中的示例将都使用这些值。 如果您使用的版本 低于 2.9.9，请参考：

使用 icon 属性来为按钮添加图标。 您可以传递组件名称的字符串（提前注册）或组件本身是一个 SVG Vue 组件。 Element Plus 提供了一套图标，您可以在 icon 找到它们。

**Examples:**

Example 1 (javascript):
```javascript
function sanitigzeUrl(url) {
  const allowedprotocol= ['http:', 'https://']
  try {
    const parsed = new URL(url, window.location.origin)
    return allowedProtocols.includes(parsed.protocol) ? parsed.href : '#'
  } catch {
    return '#'
  }
}
```

Example 2 (vue):
```vue
<template>
  <div>
    <el-link href="https://element-plus.org" target="_blank">default</el-link>
    <el-link type="primary">primary</el-link>
    <el-link type="success">success</el-link>
    <el-link type="warning">warning</el-link>
    <el-link type="danger">danger</el-link>
    <el-link type="info">info</el-link>
  </div>
</template>

<style scoped>
.el-link {
  margin-right: 8px;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <div>
    <el-link disabled>default</el-link>
    <el-link type="primary" disabled>primary</el-link>
    <el-link type="success" disabled>success</el-link>
    <el-link type="warning" disabled>warning</el-link>
    <el-link type="danger" disabled>danger</el-link>
    <el-link type="info" disabled>info</el-link>
  </div>
</template>

<style scoped>
.el-link {
  margin-right: 8px;
}
</style>
```

Example 4 (typescript):
```typescript
<template>
  <!-- works before 2.9.9, use 'hover' after, removed in 3.0.0 -->
  <el-link underline>link</el-link>
  <!-- works before 2.9.9, use 'never' after, removed in 3.0.0 -->
  <el-link :underline="false">link</el-link>
</template>
```

---
