## Image 图片 ​

**URL:** https://element-plus.org/zh-CN/component/image

**Contents:**
- Image 图片 ​
- 基础用法 ​
- 占位内容 ​
- 加载失败 ​
- 懒加载 ​
- 图片预览 ​
- 手动打开预览 2.9.4 ​
- 自定义工具栏2.9.4 ​
- 自定义进度条 2.9.4 ​
- Image API ​

图片容器，在保留所有原生 img 的特性下，支持懒加载，自定义占位、加载失败等

可通过fit确定图片如何适应到容器框，同原生 object-fit。

可通过slot = placeholder可自定义占位内容

通过 slot = error and slot = viewer-error自定义图像加载错误时的内容。

浏览器原生支持的 loading属性在 2.2.3版本加入。 您可以使用 loading="lazy" 替换之前的lazy= true。

如果当前浏览器支持原生图片延迟加载，则先使用原生能力，否则将使用滚动监听实现相同效果。

可通过lazy开启懒加载功能， 当图片滚动到可视范围内才会加载。 可通过 scroll-container 来设置滚动容器， 若未定义，则为最近一个 overflow 值为 auto 或 scroll 的父元素。

可通过 previewSrcList 开启预览大图的功能。 你可以通过 initial-index 初始化第一张预览图片的位置。 默认初始位置为 0。

可通过 toolbar 插槽自定义工具栏内容，自版本 2.9.7 起，插槽中添加了 setActiveItem 方法，用于根据索引切换图片。

可通过 show-progress 控制是否在预览图片时显示进度条。 自版本 2.9.8 起，进度条会在使用 progress 插槽时显示。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="demo-image">
    <div v-for="fit in fits" :key="fit" class="block">
      <span class="demonstration">{{ fit }}</span>
      <el-image style="width: 100px; height: 100px" :src="url" :fit="fit" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { ImageProps } from 'element-plus'

const fits = [
  'fill',
  'contain',
  'cover',
  'none',
  'scale-down',
] as ImageProps['fit'][]
const url =
  'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
</script>

<style scoped>
.demo-image .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 20%;
  min-width: 100px;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image .block:last-child {
  border-right: none;
}
.demo-image .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div class="demo-image__placeholder">
    <div class="block">
      <span class="demonstration">Default</span>
      <el-image :src="src" />
    </div>
    <div class="block">
      <span class="demonstration">Custom</span>
      <el-image :src="src">
        <template #placeholder>
          <div class="image-slot">Loading<span class="dot">...</span></div>
        </template>
      </el-image>
    </div>
  </div>
</template>

<script lang="ts" setup>
const src =
  'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg'
</script>

<style scoped>
.demo-image__placeholder .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 49%;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image__placeholder .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
.demo-image__placeholder .el-image {
  padding: 0 5px;
  max-width: 300px;
  max-height: 200px;
}

.demo-image__placeholder.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 14px;
}
.demo-image__placeholder .dot {
  animation: dot 2s infinite steps(3, start);
  overflow: hidden;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <div class="demo-image__error" flex gap-2>
    <el-image />
    <el-image>
      <template #error>
        <div class="image-viewer-slot image-slot">
          <el-icon><icon-picture /></el-icon>
        </div>
      </template>
    </el-image>
    <el-image :src="url" :preview-src-list="srcList" show-progress>
      <template #viewer-error="{ activeIndex, src }">
        <div class="image-slot viewer-error">
          <el-icon><icon-picture /></el-icon>
          <span>
            this is viewer-error slot. current index: {{ activeIndex }}. src:
            {{ src }}
          </span>
        </div>
      </template>
    </el-image>
    <el-button @click="showPreview = true"> preview controlled </el-button>

    <el-image-viewer
      v-if="showPreview"
      show-progress
      :url-list="srcList"
      @close="showPreview = false"
    >
      <template #viewer-error="{ activeIndex, src }">
        <div class="image-slot viewer-error">
          <el-icon><icon-picture /></el-icon>
          <span>
            this is viewer-error slot. current index: {{ activeIndex }}. src:
            {{ src }}
          </span>
        </div>
      </template>
    </el-image-viewer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Picture as IconPicture } from '@element-plus/icons-vue'

const showPreview = ref(false)

const srcList = [
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
  'https://errorSrc',
]
const url =
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg'
</script>

<style scoped>
.demo-image__error .el-image {
  max-width: 300px;
  max-height: 200px;
  width: 100%;
}

.demo-image__error .image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-size: 30px;
  height: 200px;
  background: #fff;
}
.demo-image__error .image-slot .el-icon {
  font-size: 30px;
}
.image-viewer-slot {
  background: var(--el-fill-color-light);
}
.viewer-error {
  color: #000;
}
</style>
```

Example 4 (vue):
```vue
<template>
  <div class="demo-image__lazy">
    <el-image v-for="url in urls" :key="url" :src="url" lazy />
  </div>
</template>

<script lang="ts" setup>
const urls = [
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
  'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
  'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
  'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
  'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
  'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
  'https://fuss10.elemecdn.com/2/11/6535bcfb26e4c79b48ddde44f4b6fjpeg.jpeg',
]
</script>

<style scoped>
.demo-image__lazy {
  height: 400px;
  overflow-y: auto;
}
.demo-image__lazy .el-image {
  display: block;
  min-height: 200px;
  margin-bottom: 10px;
}
.demo-image__lazy .el-image:last-child {
  margin-bottom: 0;
}
</style>
```

---
