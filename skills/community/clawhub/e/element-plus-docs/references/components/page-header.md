## Page Header 页头 ​

**URL:** https://element-plus.org/zh-CN/component/page-header.html

**Contents:**
- Page Header 页头 ​
- 完整示例 ​
- 基础用法 ​
- 自定义图标 ​
- 无图标 ​
- 面包屑导航 ​
- 额外操作部分 ​
- 主要内容 ​
- 组件插槽结构 ​
- API ​

如果页面的路径比较简单，推荐使用页头组件而非面包屑组件。

Element Plus team uses weekly release strategy under normal circumstance, but critical bug fixes would require hotfix so the actual release number could be more than 1 per week.

默认图标可能无法满足您的需求，您可以通过设置icon属性来自定义图标，示例如下。

有时，页面全是元素，您可能不想展示页面上方的图标，您可以设置icon属性值为""来去除它。

使用页头组件，您可以通过添加插槽 breadcrumb 来设置面包屑路由导航。

头部可能会变得很复杂，您可以在头部添加更多的区块，以允许丰富的交互。

有时我们想让页头显示一些协同响应内容，我们可以使用 default 插槽。

**Examples:**

Example 1 (typescript):
```typescript
<template>
  <div aria-label="A complete example of page header">
    <el-page-header @back="onBack">
      <template #breadcrumb>
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: './page-header.html' }">
            homepage
          </el-breadcrumb-item>
          <el-breadcrumb-item>
            <a href="./page-header.html">route 1</a>
          </el-breadcrumb-item>
          <el-breadcrumb-item>route 2</el-breadcrumb-item>
        </el-breadcrumb>
      </template>
      <template #content>
        <div class="flex items-center">
          <el-avatar
            class="mr-3"
            :size="32"
            src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
          />
          <span class="text-large font-600 mr-3"> Title </span>
          <span
            class="text-sm mr-2"
            style="color: var(--el-text-color-regular)"
          >
            Sub title
          </span>
          <el-tag>Default</el-tag>
        </div>
      </template>
      <template #extra>
        <div class="flex items-center">
          <el-button>Print</el-button>
          <el-button type="primary" class="ml-2">Edit</el-button>
        </div>
      </template>

      <el-descriptions :column="3" size="small" class="mt-4">
        <el-descriptions-item label="Username">
          kooriookami
        </el-descriptions-item>
        <el-descriptions-item label="Telephone">
          18100000000
        </el-descriptions-item>
        <el-descriptions-item label="Place">Suzhou</el-descriptions-item>
        <el-descriptions-item label="Remarks">
          <el-tag size="small">School</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Address">
          No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
        </el-descriptions-item>
      </el-descriptions>
      <p class="mt-4 text-sm">
        Element Plus team uses <b>weekly</b> release strategy under normal
        circumstance, but critical bug fixes would require hotfix so the actual
        release number <b>could be</b> more than 1 per week.
      </p>
    </el-page-header>
  </div>
</template>

<script setup lang="ts">
import { ElNotification as notify } from 'element-plus'

const onBack = () => {
  notify('Back')
}
</script>
```

Example 2 (javascript):
```javascript
<template>
  <el-page-header @back="goBack">
    <template #content>
      <span class="text-large font-600 mr-3"> Title </span>
    </template>
  </el-page-header>
</template>

<script lang="ts" setup>
const goBack = () => {
  console.log('go back')
}
</script>
```

Example 3 (typescript):
```typescript
<template>
  <el-page-header :icon="ArrowLeft">
    <template #content>
      <span class="text-large font-600 mr-3"> Title </span>
    </template>
  </el-page-header>
</template>

<script lang="ts" setup>
import { ArrowLeft } from '@element-plus/icons-vue'
</script>
```

Example 4 (vue):
```vue
<template>
  <el-page-header icon="">
    <template #content>
      <span class="text-large font-600 mr-3"> Title </span>
    </template>
  </el-page-header>
</template>
```

---
