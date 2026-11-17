## Watermark 水印 ​

**URL:** https://element-plus.org/zh-CN/component/watermark

**Contents:**
- Watermark 水印 ​
- 基础用法 ​
- 多行水印 ​
- 图片水印 ​
- 自定义配置 ​
- Element Plus
- A Vue 3 based component library for designers and developers
- API ​
  - 属性 ​
  - Font ​

使用 content设置一个字符串数组来指定多行文本水印内容

通过 image 指定图像地址。 为了确保图像清晰展示而不是被拉伸，请设置宽度和高度，建议使用至少两倍的宽度和高度的图片来保证显示效果。

**Examples:**

Example 1 (vue):
```vue
<script setup lang="ts">
import { reactive, watch } from 'vue'
import { isDark } from '~/composables/dark'

const font = reactive({
  color: 'rgba(0, 0, 0, .15)',
})

watch(
  isDark,
  () => {
    font.color = isDark.value
      ? 'rgba(255, 255, 255, .15)'
      : 'rgba(0, 0, 0, .15)'
  },
  {
    immediate: true,
  }
)
</script>

<template>
  <el-watermark :font="font">
    <div style="height: 500px" />
  </el-watermark>
</template>
```

Example 2 (vue):
```vue
<script setup lang="ts">
import { reactive, watch } from 'vue'
import { isDark } from '~/composables/dark'

const font = reactive({
  color: 'rgba(0, 0, 0, .15)',
})

watch(
  isDark,
  () => {
    font.color = isDark.value
      ? 'rgba(255, 255, 255, .15)'
      : 'rgba(0, 0, 0, .15)'
  },
  {
    immediate: true,
  }
)
</script>

<template>
  <el-watermark :font="font" :content="['Element+', 'Element Plus']">
    <div style="height: 500px" />
  </el-watermark>
</template>
```

Example 3 (typescript):
```typescript
<template>
  <el-watermark
    :width="130"
    :height="30"
    image="https://element-plus.org/images/element-plus-logo.svg"
  >
    <div style="height: 500px" />
  </el-watermark>
</template>
```

Example 4 (vue):
```vue
<script setup lang="ts">
import { reactive, watch } from 'vue'
import { isDark } from '~/composables/dark'

const config = reactive({
  content: 'Element Plus',
  font: {
    fontSize: 16,
    color: 'rgba(0, 0, 0, 0.15)',
  },
  zIndex: -1,
  rotate: -22,
  gap: [100, 100] as [number, number],
  offset: [] as unknown as [number, number],
})

watch(
  isDark,
  (value) => {
    config.font.color = value
      ? 'rgba(255, 255, 255, .15)'
      : 'rgba(0, 0, 0, .15)'
  },
  { immediate: true }
)
</script>

<template>
  <div class="wrapper">
    <el-watermark
      class="watermark"
      :content="config.content"
      :font="config.font"
      :z-index="config.zIndex"
      :rotate="config.rotate"
      :gap="config.gap"
      :offset="config.offset"
    >
      <div class="watermark-container">
        <h1>Element Plus</h1>
        <h2>A Vue 3 based component library for designers and developers</h2>
        <img src="/images/hamburger.png" alt="示例图片" />
      </div>
    </el-watermark>
    <el-form
      class="form"
      :model="config"
      label-position="top"
      label-width="50px"
    >
      <el-form-item label="Content">
        <el-input v-model="config.content" />
      </el-form-item>
      <el-form-item label="Color">
        <el-color-picker v-model="config.font.color" show-alpha />
      </el-form-item>
      <el-form-item label="FontSize">
        <el-slider v-model="config.font.fontSize" />
      </el-form-item>
      <el-form-item label="zIndex">
        <el-slider v-model="config.zIndex" />
      </el-form-item>
      <el-form-item label="Rotate">
        <el-slider v-model="config.rotate" :min="-180" :max="180" />
      </el-form-item>
      <el-form-item label="Gap">
        <el-space>
          <el-input-number v-model="config.gap[0]" controls-position="right" />
          <el-input-number v-model="config.gap[1]" controls-position="right" />
        </el-space>
      </el-form-item>
      <el-form-item label="Offset">
        <el-space>
          <el-input-number
            v-model="config.offset[0]"
            placeholder="offsetLeft"
            controls-position="right"
          />
          <el-input-number
            v-model="config.offset[1]"
            placeholder="offsetTop"
            controls-position="right"
          />
        </el-space>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.wrapper {
  display: flex;
}
.watermark {
  display: flex;
  flex: auto;
}
.watermark-container {
  flex: auto;
}
.form {
  width: 330px;
  margin-left: 20px;
  border-left: 1px solid #eee;
  padding-left: 20px;
}

img {
  z-index: 10;
  width: 100%;
  max-width: 300px;
  position: relative;
}
</style>
```

---
