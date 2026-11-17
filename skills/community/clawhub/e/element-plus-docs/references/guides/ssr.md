## 服务端渲染 (SSR) ​

**URL:** https://element-plus.org/zh-CN/guide/ssr

**Contents:**
- 服务端渲染 (SSR) ​
- 提供一个ID ​
- 配置 ZIndex ​
- Teleports ​
  - 在挂载时渲染 Teleport ​
  - 注入 Teleport 标记 ​
  - Contents
    - 链接
    - 社区

当使用 Element Plus 在 SSR 场景下开发时，您需要在 SSR 期间进行特殊处理，以避免水合错误。

对于Nuxt 用户，我们提供的 Nuxt 模块 已经包含了对这些问题的处理方案。 您只需要安装它就可以了。

提供的值用于生成 ElementPlus 中的唯一ID。 因为不同的 IDs 容易发生SSR中的水合率错误， 为了确保服务器端和客户端生成相同的ID， 我们需要将 ID_injection_key 注入到 Vue。

当您使用SSR进行开发时，您可能会遇到 z-index 引起的水合错误。 在这种情况下，我们建议注入一个初始值以避免这种错误。

Teleport 被元素加元件中的多个组件内部使用 (例如) ElDialog, ElDrawer, ElTooltip, ElDropdown, ElSelect, ElDatePicker ...)，所以在SSR期间需要特殊处理。

一个较容易的解决办法是有条件渲染挂载上的 Teleport 。

例如，在Nuxt中使用 ClientOnly 这个组件。

另一种方式是将传送标记注入到你的 HTML 页面末尾的正确位置。

您需要注入靠近 <body> 标签的传送标记。

如果您修改了 Namespace 或 append-to 属性，您需要调整 #el-popper-container- 值。

**Examples:**

Example 1 (sql):
```sql
// irrelevant code omitted
import { createApp } from 'vue'
import { ID_INJECTION_KEY } from 'element-plus'
import App from './App.vue'

const app = createApp(App)
app.provide(ID_INJECTION_KEY, {
  prefix: 1024,
  current: 0,
})
```

Example 2 (sql):
```sql
// irrelevant code omitted
import { createApp } from 'vue'
import { ZINDEX_INJECTION_KEY } from 'element-plus'
import App from './App.vue'

const app = createApp(App)
app.provide(ZINDEX_INJECTION_KEY, { current: 0 })
```

Example 3 (unknown):
```unknown
<client-only>
  <el-tooltip content="the tooltip content">
    <el-button>tooltip</el-button>
  </el-tooltip>
</client-only>
```

Example 4 (vue):
```vue
<script setup>
import { ref } from 'vue'

const isClient = ref(false)

onMounted(() => {
  isClient.value = true
})
</script>

<template>
  <el-tooltip v-if="isClient" content="the tooltip content">
    <el-button>tooltip</el-button>
  </el-tooltip>
</template>
```

---
