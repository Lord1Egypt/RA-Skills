## Badge 徽章 ​

**URL:** https://element-plus.org/zh-CN/component/badge

**Contents:**
- Badge 徽章 ​
- 基础用法 ​
- 最大值 ​
- 自定义显示内容 ​
- 小红点 ​
- 偏移量 2.7.0 ​
- API ​
  - Attributes ​
  - Slots ​
- 源代码 ​

数量值可接受 Number 或 String。

由 max 属性定义，接受 Number 值。 请注意，仅在值也是 Number 时起作用。

你也可以展示除数字以外你想要展示的任何值。 或者您可以使用 content 栏位自定义内容。

当 value 是 String 时，可以显示自定义文字。 或者使用 content 插槽。

设置徽章点的偏移，格式是[左，顶部]， 代表状态点从左侧和默认位置顶部的偏移。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-badge :value="12" class="item">
    <el-button>comments</el-button>
  </el-badge>
  <el-badge :value="3" class="item">
    <el-button>replies</el-button>
  </el-badge>
  <el-badge :value="1" class="item" type="primary">
    <el-button>comments</el-button>
  </el-badge>
  <el-badge :value="2" class="item" type="warning">
    <el-button>replies</el-button>
  </el-badge>
  <el-badge :value="1" class="item" color="green">
    <el-button>custom background</el-button>
  </el-badge>
  <el-dropdown trigger="click">
    <span class="el-dropdown-link">
      Click Me
      <el-icon class="el-icon--right"><caret-bottom /></el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item class="clearfix">
          comments
          <el-badge class="mark" :value="12" />
        </el-dropdown-item>
        <el-dropdown-item class="clearfix">
          replies
          <el-badge class="mark" :value="3" />
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script lang="ts" setup>
import { CaretBottom } from '@element-plus/icons-vue'
</script>

<style scoped>
.item {
  margin-top: 10px;
  margin-right: 30px;
}

.el-dropdown {
  margin-top: 1.1rem;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <el-badge :value="200" :max="99" class="item">
    <el-button>comments</el-button>
  </el-badge>
  <el-badge :value="100" :max="10" class="item">
    <el-button>replies</el-button>
  </el-badge>
</template>

<style scoped>
.item {
  margin-top: 10px;
  margin-right: 40px;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <el-badge value="new" class="item">
    <el-button>comments</el-button>
  </el-badge>
  <el-badge value="hot" class="item">
    <el-button>replies</el-button>
  </el-badge>
  <el-badge value="99" class="item">
    <el-button>share</el-button>
    <template #content="{ value }">
      <div class="custom-content">
        <el-icon>
          <Message />
        </el-icon>
        <span>{{ value }}</span>
      </div>
    </template>
  </el-badge>
</template>

<script setup lang="ts">
import { Message } from '@element-plus/icons-vue'
</script>

<style scoped>
.item {
  margin-top: 10px;
  margin-right: 40px;
}

.custom-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
</style>
```

Example 4 (vue):
```vue
<template>
  <el-badge is-dot class="item">query</el-badge>
  <el-badge is-dot class="item">
    <el-button class="share-button" :icon="Share" type="primary" />
  </el-badge>
</template>

<script lang="ts" setup>
import { Share } from '@element-plus/icons-vue'
</script>

<style scoped>
.item {
  margin-top: 10px;
  margin-right: 40px;
}
</style>
```

---
