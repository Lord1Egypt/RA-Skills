## 内置过渡动画 ​

**URL:** https://element-plus.org/zh-CN/guide/transitions

**Contents:**
- 内置过渡动画 ​
- Fade 淡入淡出 ​
- Zoom 缩放 ​
- Collapse 折叠面板 ​
- 按需导入 ​
  - Contents
    - 链接
    - 社区

Element Plus 内应用在部分组件的过渡动画，你也可以直接使用。 在使用之前，请阅读 官方的过渡组件文档。

提供 el-fade-in-linear 和 el-fade-in 两种效果。

el-zoom-in-left, el-zoom-in-center, el-zoom-in-top and el-zoom-in-bottom are provided.

使用 el-collapse-transition 组件实现折叠展开效果。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div>
    <el-button @click="show = !show">Click Me</el-button>

    <div class="fade-container">
      <transition name="el-fade-in-linear">
        <div v-show="show" class="transition-box">.el-fade-in-linear</div>
      </transition>
      <transition name="el-fade-in">
        <div v-show="show" class="transition-box">.el-fade-in</div>
      </transition>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const show = ref(true)
</script>

<style scoped>
.fade-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  min-height: 100px;
  margin-top: 20px;
}

.transition-box {
  width: 200px;
  height: 100px;
  border-radius: var(--el-border-radius-base);
  background-color: var(--el-color-primary);
  text-align: center;
  color: #fff;
  padding: 40px 20px;
  box-sizing: border-box;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div>
    <el-button @click="show = !show">Click Me</el-button>

    <div class="transition-container">
      <transition name="el-zoom-in-left">
        <div v-show="show" class="transition-box">.el-zoom-in-left</div>
      </transition>

      <transition name="el-zoom-in-center">
        <div v-show="show" class="transition-box">.el-zoom-in-center</div>
      </transition>

      <transition name="el-zoom-in-top">
        <div v-show="show" class="transition-box">.el-zoom-in-top</div>
      </transition>

      <transition name="el-zoom-in-bottom">
        <div v-show="show" class="transition-box">.el-zoom-in-bottom</div>
      </transition>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const show = ref(true)
</script>

<style scoped>
.transition-container {
  display: flex;
  margin-top: 20px;
  min-height: 100px;
  flex-wrap: wrap;
  gap: 16px;
}

.transition-box {
  width: 200px;
  height: 100px;
  border-radius: var(--el-border-radius-base);
  background-color: var(--el-color-primary);
  text-align: center;
  color: #fff;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  word-break: break-word;
  font-size: 14px;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <div>
    <el-button @click="show = !show">Click Me</el-button>

    <div style="margin-top: 20px; height: 210px">
      <el-collapse-transition>
        <div v-show="show">
          <div class="transition-box">el-collapse-transition</div>
          <div class="transition-box mt-[10px]">el-collapse-transition</div>
        </div>
      </el-collapse-transition>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const show = ref(true)
</script>

<style scoped>
.transition-box {
  width: 200px;
  height: 100px;
  border-radius: var(--el-border-radius-base);
  background-color: var(--el-color-primary);
  text-align: center;
  color: #fff;
  padding: 40px 20px;
  box-sizing: border-box;
}
</style>
```

Example 4 (sql):
```sql
// collapse
import { ElCollapseTransition } from 'element-plus'
// fade/zoom
import 'element-plus/theme-chalk/base.css'
import App from './App.vue'

const app = createApp(App)
app.component(ElCollapseTransition.name, ElCollapseTransition)
```

---
