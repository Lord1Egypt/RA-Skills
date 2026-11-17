## Splitter 分隔面板 beta ​

**URL:** https://element-plus.org/zh-CN/component/splitter

**Contents:**
- Splitter 分隔面板 beta ​
- 基础用法 ​
- 垂直布局 ​
- 可折叠 ​
- 禁用拖动 ​
- 面板大小 ​
- 延迟2.11.0 ​
- Splitter API ​
  - Splitter Attributes ​
  - Splitter Events ​

可将区域水平或垂直分隔，并可自由拖动以调整各个区域的大小。

最基本的用法，如果未传入默认尺寸，将自动平均分配。

配置 collapsible 可提供快速收缩功能。 你可以使用 min 属性来防止折叠后通过拖拽进行扩展。

当任一面板禁用 resizable 时，拖拽功能将被禁用。

v-model:size 可以获取面板的大小。

当启用lazy时，面板大小将不会在拖动时实时更新，只能在拖动结束后更新。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div
    style="height: 250px; box-shadow: var(--el-border-color-light) 0px 0px 10px"
  >
    <el-splitter>
      <el-splitter-panel size="30%">
        <div class="demo-panel">1</div>
      </el-splitter-panel>
      <el-splitter-panel :min="200">
        <div class="demo-panel">2</div>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div
    style="height: 250px; box-shadow: var(--el-border-color-light) 0px 0px 10px"
  >
    <el-splitter layout="vertical">
      <el-splitter-panel>
        <div class="demo-panel">1</div>
      </el-splitter-panel>
      <el-splitter-panel>
        <div class="demo-panel">2</div>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <el-switch
    v-model="isCollapsible"
    active-text="enable"
    inactive-text="disable"
    inline-prompt
    class="mb-2"
  />
  <div
    style="height: 250px; box-shadow: var(--el-border-color-light) 0px 0px 10px"
  >
    <el-splitter>
      <el-splitter-panel :collapsible="isCollapsible" min="50">
        <div class="demo-panel">1</div>
      </el-splitter-panel>
      <el-splitter-panel :collapsible="isCollapsible">
        <div class="demo-panel">2</div>
      </el-splitter-panel>
      <el-splitter-panel>
        <div class="demo-panel">3</div>
      </el-splitter-panel>
      <el-splitter-panel :collapsible="isCollapsible">
        <el-splitter layout="vertical">
          <el-splitter-panel :collapsible="isCollapsible">
            <div class="demo-panel">4</div>
          </el-splitter-panel>
          <el-splitter-panel :collapsible="isCollapsible">
            <div class="demo-panel">5</div>
          </el-splitter-panel>
        </el-splitter>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isCollapsible = ref(true)
</script>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
```

Example 4 (vue):
```vue
<template>
  <el-switch
    v-model="resizable"
    active-text="enable"
    inactive-text="disable"
    inline-prompt
    class="mb-2"
  />
  <div
    style="height: 250px; box-shadow: var(--el-border-color-light) 0px 0px 10px"
  >
    <el-splitter>
      <el-splitter-panel>
        <div class="demo-panel">1</div>
      </el-splitter-panel>
      <el-splitter-panel :resizable="resizable">
        <div class="demo-panel">
          drag {{ resizable ? 'enable' : 'disable' }}
        </div>
      </el-splitter-panel>
      <el-splitter-panel>
        <div class="demo-panel">3</div>
      </el-splitter-panel>
    </el-splitter>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const resizable = ref(false)
</script>

<style scoped>
.demo-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
```

---
