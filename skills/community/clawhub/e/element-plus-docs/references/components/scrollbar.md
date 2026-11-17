## Scrollbar 滚动条 ​

**URL:** https://element-plus.org/zh-CN/component/scrollbar

**Contents:**
- Scrollbar 滚动条 ​
- 基础用法 ​
- 横向滚动 ​
- 最大高度 ​
- 手动滚动 ​
- 无限滚动2.10.0 ​
- API ​
  - Attributes ​
  - Events ​
  - Slots ​

通过 height 属性设置滚动条高度，若不设置则根据父容器高度自适应。

当元素宽度大于滚动条宽度时，会显示横向滚动条。

通过使用 setScrollTop 与 setScrollLeft 方法，可以手动控制滚动条滚动。

end-reached 是在滚动条到达底部时触发的。 它可以用作无限滚动。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-scrollbar height="400px">
    <p v-for="item in 20" :key="item" class="scrollbar-demo-item">{{ item }}</p>
  </el-scrollbar>
</template>

<style scoped>
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
</style>
```

Example 2 (vue):
```vue
<template>
  <el-scrollbar>
    <div class="scrollbar-flex-content">
      <p v-for="item in 50" :key="item" class="scrollbar-demo-item">
        {{ item }}
      </p>
    </div>
  </el-scrollbar>
</template>

<style scoped>
.scrollbar-flex-content {
  display: flex;
  width: fit-content;
}
.scrollbar-demo-item {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-danger-light-9);
  color: var(--el-color-danger);
}
</style>
```

Example 3 (vue):
```vue
<template>
  <el-button @click="add">Add Item</el-button>
  <el-button @click="onDelete">Delete Item</el-button>
  <el-scrollbar max-height="400px">
    <p v-for="item in count" :key="item" class="scrollbar-demo-item">
      {{ item }}
    </p>
  </el-scrollbar>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const count = ref(3)

const add = () => {
  count.value++
}
const onDelete = () => {
  if (count.value > 0) {
    count.value--
  }
}
</script>

<style scoped>
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
</style>
```

Example 4 (vue):
```vue
<template>
  <el-scrollbar ref="scrollbarRef" height="400px" always @scroll="scroll">
    <div ref="innerRef">
      <p v-for="item in 20" :key="item" class="scrollbar-demo-item">
        {{ item }}
      </p>
    </div>
  </el-scrollbar>

  <el-slider
    v-model="value"
    :max="max"
    :format-tooltip="formatTooltip"
    @input="inputSlider"
  />
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

import type { ScrollbarInstance } from 'element-plus'

type Arrayable<T> = T | T[]

const max = ref(0)
const value = ref(0)
const innerRef = ref<HTMLDivElement>()
const scrollbarRef = ref<ScrollbarInstance>()

onMounted(() => {
  max.value = innerRef.value!.clientHeight - 380
})

const inputSlider = (value: Arrayable<number>) => {
  scrollbarRef.value!.setScrollTop(value as number)
}
const scroll = ({ scrollTop }: { scrollTop: number }) => {
  value.value = scrollTop
}
const formatTooltip = (value: number) => `${value} px`
</script>

<style scoped>
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
.el-slider {
  margin-top: 20px;
}
</style>
```

---
