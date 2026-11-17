## Avatar 头像 ​

**URL:** https://element-plus.org/zh-CN/component/avatar

**Contents:**
- Avatar 头像 ​
- 基础用法 ​
- 展示类型 ​
- 回退行为 ​
- 适应容器 ​
- 头像组 2.13.1 ​
- Avatar API ​
  - Avatar 属性 ​
  - Avatar 事件 ​
  - Avatar 插槽 ​

Avatar 组件可以用来代表人物或对象， 支持使用图片、图标或者文字作为 Avatar。

使用 shape 和 size 属性来设置 Avatar 的形状和大小。

支持使用图片，图标或者文字作为 Avatar。

当使用图片作为用户头像时，设置该图片如何在容器中展示。与 object-fit 属性一致

使用标签 <el-avatar-group> 来分组您的头像。

use collapse-class and collapse-style

use max-collapse-avatars

use collapse-avatars-tooltip

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-row class="demo-avatar demo-basic">
    <el-col :lg="12" :md="12">
      <div class="sub-title">circle</div>
      <div class="demo-basic--circle">
        <div class="block">
          <el-avatar :size="50" :src="circleUrl" />
        </div>
        <div v-for="size in sizeList" :key="size" class="block">
          <el-avatar :size="size" :src="circleUrl" />
        </div>
      </div>
    </el-col>
    <el-col :lg="12" :md="12">
      <div class="sub-title">square</div>
      <div class="demo-basic--circle">
        <div class="block">
          <el-avatar shape="square" :size="50" :src="squareUrl" />
        </div>
        <div v-for="size in sizeList" :key="size" class="block">
          <el-avatar shape="square" :size="size" :src="squareUrl" />
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { reactive, toRefs } from 'vue'

const state = reactive({
  circleUrl:
    'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
  squareUrl:
    'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
  sizeList: ['small', '', 'large'] as const,
})

const { circleUrl, squareUrl, sizeList } = toRefs(state)
</script>

<style scoped>
.demo-basic {
  text-align: center;
}
.demo-basic .sub-title {
  margin-bottom: 10px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
.demo-basic .demo-basic--circle,
.demo-basic .demo-basic--square {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.demo-basic .block:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}
.demo-basic .block {
  flex: 1;
}
.demo-basic .el-col:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}
@media screen and (max-width: 992px) {
  .demo-basic .el-col:not(:last-child) {
    border-right: none;
  }
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div class="demo-type">
    <div>
      <el-avatar :icon="UserFilled" />
    </div>
    <div>
      <el-avatar
        src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
      />
    </div>
    <div>
      <el-avatar> user </el-avatar>
    </div>
  </div>
</template>

<script setup lang="ts">
import { UserFilled } from '@element-plus/icons-vue'
</script>

<style scoped>
.demo-type {
  display: flex;
}
.demo-type > div {
  flex: 1;
  text-align: center;
}

.demo-type > div:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}
</style>
```

Example 3 (typescript):
```typescript
<template>
  <div class="demo-type">
    <el-avatar :size="60" src="https://empty" @error="errorHandler">
      <img
        src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"
      />
    </el-avatar>
  </div>
</template>

<script lang="ts" setup>
const errorHandler = () => true
</script>
```

Example 4 (vue):
```vue
<template>
  <div class="demo-fit">
    <div v-for="fit in fits" :key="fit" class="block">
      <span class="title">{{ fit }}</span>
      <el-avatar shape="square" :size="100" :fit="fit" :src="url" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, toRefs } from 'vue'

import type { CSSProperties } from 'vue'

const state = reactive({
  fits: [
    'fill',
    'contain',
    'cover',
    'none',
    'scale-down',
  ] as CSSProperties['object-fit'][],
  url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
})

const { fits, url } = toRefs(state)
</script>

<style scoped>
.demo-fit {
  display: flex;
  text-align: center;
  justify-content: space-between;
}
.demo-fit .block {
  flex: 1;
  display: flex;
  flex-direction: column;
  flex-grow: 0;
}

.demo-fit .title {
  margin-bottom: 10px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
</style>
```

---
