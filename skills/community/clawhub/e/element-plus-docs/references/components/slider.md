## Slider 滑块 ​

**URL:** https://element-plus.org/zh-CN/component/slider

**Contents:**
- Slider 滑块 ​
- 基础用法 ​
- 离散值 ​
- 带有输入框的滑块 ​
- 不同尺寸 ​
- 位置 ​
- 范围选择 ​
- 垂直模式 ​
- 显示标记 ​
- 限制值 2.13.6 ​

改变step的值可以改变步长， 通过设置 show-stops 属性可以显示间断点

设置 show-input 属性会在右侧显示一个输入框

您可以自定义 Tooltip 提示的位置。

配置 range 属性以激活范围选择模式，该属性的绑定值是一个数组，由最小边界值和最大边界值组成。

配置 vertical 属性为 true 启用垂直模式。 在垂直模式下，必须设置 height 属性。

设置 marks 属性可以在滑块上显示标记。

设置 step="mark" 以将滑块值限制为刻度。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="slider-demo-block">
    <span class="demonstration">Default value</span>
    <el-slider v-model="value1" />
  </div>
  <div class="slider-demo-block">
    <span class="demonstration">Customized initial value</span>
    <el-slider v-model="value2" />
  </div>
  <div class="slider-demo-block">
    <span class="demonstration">Hide Tooltip</span>
    <el-slider v-model="value3" :show-tooltip="false" />
  </div>
  <div class="slider-demo-block">
    <span class="demonstration">Format Tooltip</span>
    <el-slider v-model="value4" :format-tooltip="formatTooltip" />
  </div>
  <div class="slider-demo-block">
    <span class="demonstration">Disabled</span>
    <el-slider v-model="value5" disabled />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(0)
const value2 = ref(0)
const value3 = ref(0)
const value4 = ref(0)
const value5 = ref(0)

const formatTooltip = (val: number) => {
  return val / 100
}
</script>

<style scoped>
.slider-demo-block {
  max-width: 600px;
  display: flex;
  align-items: center;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}
.slider-demo-block .demonstration {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 70%;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div class="slider-demo-block">
    <span class="demonstration">Breakpoints not displayed</span>
    <el-slider v-model="value1" :step="10" />
  </div>
  <div class="slider-demo-block">
    <span class="demonstration">Breakpoints displayed</span>
    <el-slider v-model="value2" :step="10" show-stops />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(0)
const value2 = ref(0)
</script>

<style scoped>
.slider-demo-block {
  max-width: 600px;
  display: flex;
  align-items: center;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}
.slider-demo-block .demonstration {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 70%;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <div class="slider-demo-block">
    <el-slider v-model="value" show-input />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref(0)
</script>

<style scoped>
.slider-demo-block {
  max-width: 600px;
  display: flex;
  align-items: center;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}
</style>
```

Example 4 (vue):
```vue
<template>
  <div class="slider-demo-block">
    <el-slider v-model="value" show-input size="large" />
    <el-slider v-model="value" show-input />
    <el-slider v-model="value" show-input size="small" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref(0)
</script>

<style scoped>
.slider-demo-block {
  max-width: 600px;
}

.el-slider {
  margin-top: 20px;
}

.el-slider:first-child {
  margin-top: 0;
}
</style>
```

---
