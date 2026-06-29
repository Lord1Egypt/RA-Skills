---
name: "slider"
description: "Slider 滑块 -- Element Plus Vue3 桌面端组件。Invoke when user needs Slider 滑块 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/slider.html"
---

---

# Slider 滑块 [​](#slider-滑块)

更新日志待解决

3

通过拖动滑块在一个固定区间内进行选择

## 基础用法 [​](#基础用法)

在拖动滑块时，显示当前值

通过设置绑定值自定义滑块的初始值

Default value

Customized initial value

Hide Tooltip

Format Tooltip

Disabled

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5EZWZhdWx0IHZhbHVlPC9zcGFuPlxuICAgIDxlbC1zbGlkZXIgdi1tb2RlbD1cInZhbHVlMVwiIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5DdXN0b21pemVkIGluaXRpYWwgdmFsdWU8L3NwYW4+XG4gICAgPGVsLXNsaWRlciB2LW1vZGVsPVwidmFsdWUyXCIgLz5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJzbGlkZXItZGVtby1ibG9ja1wiPlxuICAgIDxzcGFuIGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPkhpZGUgVG9vbHRpcDwvc3Bhbj5cbiAgICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJ2YWx1ZTNcIiA6c2hvdy10b29sdGlwPVwiZmFsc2VcIiAvPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cInNsaWRlci1kZW1vLWJsb2NrXCI+XG4gICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+Rm9ybWF0IFRvb2x0aXA8L3NwYW4+XG4gICAgPGVsLXNsaWRlciB2LW1vZGVsPVwidmFsdWU0XCIgOmZvcm1hdC10b29sdGlwPVwiZm9ybWF0VG9vbHRpcFwiIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5EaXNhYmxlZDwvc3Bhbj5cbiAgICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJ2YWx1ZTVcIiBkaXNhYmxlZCAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlMSA9IHJlZigwKVxuY29uc3QgdmFsdWUyID0gcmVmKDApXG5jb25zdCB2YWx1ZTMgPSByZWYoMClcbmNvbnN0IHZhbHVlNCA9IHJlZigwKVxuY29uc3QgdmFsdWU1ID0gcmVmKDApXG5cbmNvbnN0IGZvcm1hdFRvb2x0aXAgPSAodmFsOiBudW1iZXIpID0+IHtcbiAgcmV0dXJuIHZhbCAvIDEwMFxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uc2xpZGVyLWRlbW8tYmxvY2sge1xuICBtYXgtd2lkdGg6IDYwMHB4O1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuLnNsaWRlci1kZW1vLWJsb2NrIC5lbC1zbGlkZXIge1xuICBtYXJnaW4tdG9wOiAwO1xuICBtYXJnaW4tbGVmdDogMTJweDtcbn1cbi5zbGlkZXItZGVtby1ibG9jayAuZGVtb25zdHJhdGlvbiB7XG4gIGZvbnQtc2l6ZTogMTRweDtcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbiAgbGluZS1oZWlnaHQ6IDQ0cHg7XG4gIGZsZXg6IDE7XG4gIG92ZXJmbG93OiBoaWRkZW47XG4gIHRleHQtb3ZlcmZsb3c6IGVsbGlwc2lzO1xuICB3aGl0ZS1zcGFjZTogbm93cmFwO1xuICBtYXJnaW4tYm90dG9tOiAwO1xufVxuLnNsaWRlci1kZW1vLWJsb2NrIC5kZW1vbnN0cmF0aW9uICsgLmVsLXNsaWRlciB7XG4gIGZsZXg6IDAgMCA3MCU7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/slider/basic-usage.vue)_

vue

```
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

隐藏源代码

## 离散值 [​](#离散值)

选项可以是离散的

改变`step`的值可以改变步长， 通过设置 `show-stops` 属性可以显示间断点

Breakpoints not displayed

Breakpoints displayed

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5CcmVha3BvaW50cyBub3QgZGlzcGxheWVkPC9zcGFuPlxuICAgIDxlbC1zbGlkZXIgdi1tb2RlbD1cInZhbHVlMVwiIDpzdGVwPVwiMTBcIiAvPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cInNsaWRlci1kZW1vLWJsb2NrXCI+XG4gICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+QnJlYWtwb2ludHMgZGlzcGxheWVkPC9zcGFuPlxuICAgIDxlbC1zbGlkZXIgdi1tb2RlbD1cInZhbHVlMlwiIDpzdGVwPVwiMTBcIiBzaG93LXN0b3BzIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKDApXG5jb25zdCB2YWx1ZTIgPSByZWYoMClcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLnNsaWRlci1kZW1vLWJsb2NrIHtcbiAgbWF4LXdpZHRoOiA2MDBweDtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cbi5zbGlkZXItZGVtby1ibG9jayAuZWwtc2xpZGVyIHtcbiAgbWFyZ2luLXRvcDogMDtcbiAgbWFyZ2luLWxlZnQ6IDEycHg7XG59XG4uc2xpZGVyLWRlbW8tYmxvY2sgLmRlbW9uc3RyYXRpb24ge1xuICBmb250LXNpemU6IDE0cHg7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG4gIGxpbmUtaGVpZ2h0OiA0NHB4O1xuICBmbGV4OiAxO1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICB0ZXh0LW92ZXJmbG93OiBlbGxpcHNpcztcbiAgd2hpdGUtc3BhY2U6IG5vd3JhcDtcbiAgbWFyZ2luLWJvdHRvbTogMDtcbn1cbi5zbGlkZXItZGVtby1ibG9jayAuZGVtb25zdHJhdGlvbiArIC5lbC1zbGlkZXIge1xuICBmbGV4OiAwIDAgNzAlO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/slider/discrete-values.vue)_

vue

```
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

隐藏源代码

## 带有输入框的滑块 [​](#带有输入框的滑块)

通过输入框输入来改变当前的值。

设置 `show-input` 属性会在右侧显示一个输入框

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJ2YWx1ZVwiIHNob3ctaW5wdXQgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZigwKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uc2xpZGVyLWRlbW8tYmxvY2sge1xuICBtYXgtd2lkdGg6IDYwMHB4O1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuLnNsaWRlci1kZW1vLWJsb2NrIC5lbC1zbGlkZXIge1xuICBtYXJnaW4tdG9wOiAwO1xuICBtYXJnaW4tbGVmdDogMTJweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/slider/slider-with-input-box.vue)_

vue

```
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

隐藏源代码

## 不同尺寸 [​](#不同尺寸)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJ2YWx1ZVwiIHNob3ctaW5wdXQgc2l6ZT1cImxhcmdlXCIgLz5cbiAgICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJ2YWx1ZVwiIHNob3ctaW5wdXQgLz5cbiAgICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJ2YWx1ZVwiIHNob3ctaW5wdXQgc2l6ZT1cInNtYWxsXCIgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZigwKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uc2xpZGVyLWRlbW8tYmxvY2sge1xuICBtYXgtd2lkdGg6IDYwMHB4O1xufVxuXG4uZWwtc2xpZGVyIHtcbiAgbWFyZ2luLXRvcDogMjBweDtcbn1cblxuLmVsLXNsaWRlcjpmaXJzdC1jaGlsZCB7XG4gIG1hcmdpbi10b3A6IDA7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/slider/sizes.vue)_

vue

```
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

隐藏源代码

## 位置 [​](#位置)

您可以自定义 Tooltip 提示的位置。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJ2YWx1ZTFcIiAvPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cInNsaWRlci1kZW1vLWJsb2NrXCI+XG4gICAgPGVsLXNsaWRlciB2LW1vZGVsPVwidmFsdWUyXCIgcGxhY2VtZW50PVwiYm90dG9tXCIgLz5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJzbGlkZXItZGVtby1ibG9ja1wiPlxuICAgIDxlbC1zbGlkZXIgdi1tb2RlbD1cInZhbHVlM1wiIHBsYWNlbWVudD1cInJpZ2h0XCIgLz5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJzbGlkZXItZGVtby1ibG9ja1wiPlxuICAgIDxlbC1zbGlkZXIgdi1tb2RlbD1cInZhbHVlNFwiIHBsYWNlbWVudD1cImxlZnRcIiAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlMSA9IHJlZigwKVxuY29uc3QgdmFsdWUyID0gcmVmKDApXG5jb25zdCB2YWx1ZTMgPSByZWYoMClcbmNvbnN0IHZhbHVlNCA9IHJlZigwKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uc2xpZGVyLWRlbW8tYmxvY2sge1xuICBtYXgtd2lkdGg6IDYwMHB4O1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuLnNsaWRlci1kZW1vLWJsb2NrIC5lbC1zbGlkZXIge1xuICBtYXJnaW4tdG9wOiAwO1xuICBtYXJnaW4tbGVmdDogMTJweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/slider/placement.vue)_

vue

```
<template>
  <div class="slider-demo-block">
    <el-slider v-model="value1" />
  </div>
  <div class="slider-demo-block">
    <el-slider v-model="value2" placement="bottom" />
  </div>
  <div class="slider-demo-block">
    <el-slider v-model="value3" placement="right" />
  </div>
  <div class="slider-demo-block">
    <el-slider v-model="value4" placement="left" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(0)
const value2 = ref(0)
const value3 = ref(0)
const value4 = ref(0)
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

隐藏源代码

## 范围选择 [​](#范围选择)

你还可以选择一个范围值

配置 `range` 属性以激活范围选择模式，该属性的绑定值是一个数组，由最小边界值和最大边界值组成。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJ2YWx1ZVwiIHJhbmdlIHNob3ctc3RvcHMgOm1heD1cIjEwXCIgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZihbNCwgOF0pXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5zbGlkZXItZGVtby1ibG9jayB7XG4gIG1heC13aWR0aDogNjAwcHg7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG59XG4uc2xpZGVyLWRlbW8tYmxvY2sgLmVsLXNsaWRlciB7XG4gIG1hcmdpbi10b3A6IDA7XG4gIG1hcmdpbi1sZWZ0OiAxMnB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/slider/range-selection.vue)_

vue

```
<template>
  <div class="slider-demo-block">
    <el-slider v-model="value" range show-stops :max="10" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref([4, 8])
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

隐藏源代码

## 垂直模式 [​](#垂直模式)

配置 `vertical` 属性为 `true` 启用垂直模式。 在垂直模式下，必须设置 `height` 属性。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJ2YWx1ZVwiIHZlcnRpY2FsIGhlaWdodD1cIjIwMHB4XCIgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZigwKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uc2xpZGVyLWRlbW8tYmxvY2sge1xuICBtYXgtd2lkdGg6IDYwMHB4O1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuLnNsaWRlci1kZW1vLWJsb2NrIC5lbC1zbGlkZXIge1xuICBtYXJnaW4tdG9wOiAwO1xuICBtYXJnaW4tbGVmdDogMTJweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/slider/vertical-mode.vue)_

vue

```
<template>
  <div class="slider-demo-block">
    <el-slider v-model="value" vertical height="200px" />
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

隐藏源代码

## 显示标记 [​](#显示标记)

设置 `marks` 属性可以在滑块上显示标记。

0°C

8°C

37°C

50%

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJ2YWx1ZVwiIHJhbmdlIDptYXJrcz1cIm1hcmtzXCIgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVhY3RpdmUsIHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBDU1NQcm9wZXJ0aWVzIH0gZnJvbSAndnVlJ1xuXG5pbnRlcmZhY2UgTWFyayB7XG4gIHN0eWxlOiBDU1NQcm9wZXJ0aWVzXG4gIGxhYmVsOiBzdHJpbmdcbn1cblxudHlwZSBNYXJrcyA9IFJlY29yZDxudW1iZXIsIE1hcmsgfCBzdHJpbmc+XG5cbmNvbnN0IHZhbHVlID0gcmVmKFszMCwgNjBdKVxuY29uc3QgbWFya3MgPSByZWFjdGl2ZTxNYXJrcz4oe1xuICAwOiAnMMKwQycsXG4gIDg6ICc4wrBDJyxcbiAgMzc6ICczN8KwQycsXG4gIDUwOiB7XG4gICAgc3R5bGU6IHtcbiAgICAgIGNvbG9yOiAnIzE5ODlGQScsXG4gICAgfSxcbiAgICBsYWJlbDogJzUwJScsXG4gIH0sXG59KVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uc2xpZGVyLWRlbW8tYmxvY2sge1xuICBtYXgtd2lkdGg6IDYwMHB4O1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuLnNsaWRlci1kZW1vLWJsb2NrIC5lbC1zbGlkZXIge1xuICBtYXJnaW4tdG9wOiAwO1xuICBtYXJnaW4tbGVmdDogMTJweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/slider/show-marks.vue)_

vue

```
<template>
  <div class="slider-demo-block">
    <el-slider v-model="value" range :marks="marks" />
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

import type { CSSProperties } from 'vue'

interface Mark {
  style: CSSProperties
  label: string
}

type Marks = Record<number, Mark | string>

const value = ref([30, 60])
const marks = reactive<Marks>({
  0: '0°C',
  8: '8°C',
  37: '37°C',
  50: {
    style: {
      color: '#1989FA',
    },
    label: '50%',
  },
})
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

隐藏源代码

## 限制值 2.13.6 [​](#限制值)

设置 `step="mark"` 以将滑块值限制为刻度。

0°C

37°C

100°C

0cm

10cm

25cm

50cm

75cm

100cm

0

13

42

58

89

100

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwic2xpZGVyLWRlbW8tYmxvY2tcIj5cbiAgICA8ZWwtc2xpZGVyXG4gICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgIHZlcnRpY2FsXG4gICAgICBoZWlnaHQ9XCIyMDBweFwiXG4gICAgICA6bWFya3M9XCJtYXJrczFcIlxuICAgICAgcGxhY2VtZW50PVwicmlnaHRcIlxuICAgICAgOmZvcm1hdC10b29sdGlwPVwiKHYpID0+IGAke3Z9wrBDYFwiXG4gICAgICBzdGVwPVwibWFya1wiXG4gICAgLz5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJzbGlkZXItZGVtby1ibG9ja1wiPlxuICAgIDxlbC1zbGlkZXIgdi1tb2RlbD1cInZhbHVlMlwiIDptYXJrcz1cIm1hcmtzMlwiIHN0ZXA9XCJtYXJrXCIgLz5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJzbGlkZXItZGVtby1ibG9ja1wiPlxuICAgIDxlbC1zbGlkZXIgdi1tb2RlbD1cInZhbHVlM1wiIHJhbmdlIDptYXJrcz1cIm1hcmtzM1wiIHN0ZXA9XCJtYXJrXCIgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmLCBzaGFsbG93UmVhY3RpdmUgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgQ1NTUHJvcGVydGllcyB9IGZyb20gJ3Z1ZSdcblxuaW50ZXJmYWNlIE1hcmsge1xuICBzdHlsZTogQ1NTUHJvcGVydGllc1xuICBsYWJlbDogc3RyaW5nXG59XG5cbnR5cGUgTWFya3MgPSBSZWNvcmQ8bnVtYmVyLCBNYXJrIHwgc3RyaW5nPlxuXG5jb25zdCB2YWx1ZTEgPSByZWYoMzcpXG5jb25zdCBtYXJrczEgPSBzaGFsbG93UmVhY3RpdmU8TWFya3M+KHtcbiAgMDogJzDCsEMnLFxuICAzNzogJzM3wrBDJyxcbiAgMTAwOiAnMTAwwrBDJyxcbn0pXG5cbmNvbnN0IHZhbHVlMiA9IHJlZig1MClcbmNvbnN0IG1hcmtzMiA9IHNoYWxsb3dSZWFjdGl2ZTxNYXJrcz4oe1xuICAwOiAnMGNtJyxcbiAgMTA6ICcxMGNtJyxcbiAgMjU6ICcyNWNtJyxcbiAgNTA6ICc1MGNtJyxcbiAgNzU6ICc3NWNtJyxcbiAgMTAwOiAnMTAwY20nLFxufSlcbmNvbnN0IHZhbHVlMyA9IHJlZihbMTMsIDQyXSlcbmNvbnN0IG1hcmtzMyA9IHNoYWxsb3dSZWFjdGl2ZTxNYXJrcz4oe1xuICAwOiAnMCcsXG4gIDEzOiAnMTMnLFxuICA0MjogJzQyJyxcbiAgNTg6ICc1OCcsXG4gIDg5OiAnODknLFxuICAxMDA6ICcxMDAnLFxufSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLnNsaWRlci1kZW1vLWJsb2NrIHtcbiAgbWF4LXdpZHRoOiA2MDBweDtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cbi5zbGlkZXItZGVtby1ibG9jayAuZWwtc2xpZGVyIHtcbiAgbWFyZ2luLXRvcDogMDtcbiAgbWFyZ2luLWxlZnQ6IDEycHg7XG59XG4uc2xpZGVyLWRlbW8tYmxvY2sgKyAuc2xpZGVyLWRlbW8tYmxvY2sge1xuICBtYXJnaW4tdG9wOiAyMHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/slider/restrict-value.vue)_

vue

```
<template>
  <div class="slider-demo-block">
    <el-slider
      v-model="value1"
      vertical
      height="200px"
      :marks="marks1"
      placement="right"
      :format-tooltip="(v) => `${v}°C`"
      step="mark"
    />
  </div>
  <div class="slider-demo-block">
    <el-slider v-model="value2" :marks="marks2" step="mark" />
  </div>
  <div class="slider-demo-block">
    <el-slider v-model="value3" range :marks="marks3" step="mark" />
  </div>
</template>

<script lang="ts" setup>
import { ref, shallowReactive } from 'vue'

import type { CSSProperties } from 'vue'

interface Mark {
  style: CSSProperties
  label: string
}

type Marks = Record<number, Mark | string>

const value1 = ref(37)
const marks1 = shallowReactive<Marks>({
  0: '0°C',
  37: '37°C',
  100: '100°C',
})

const value2 = ref(50)
const marks2 = shallowReactive<Marks>({
  0: '0cm',
  10: '10cm',
  25: '25cm',
  50: '50cm',
  75: '75cm',
  100: '100cm',
})
const value3 = ref([13, 42])
const marks3 = shallowReactive<Marks>({
  0: '0',
  13: '13',
  42: '42',
  58: '58',
  89: '89',
  100: '100',
})
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
.slider-demo-block + .slider-demo-block {
  margin-top: 20px;
}
</style>
```

隐藏源代码

## API [​](#api)

### 属性 [​](#属性)

| 属性名 | 描述 | 类型 | 默认 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `number` / `array` | 0 |
| min | 最小值 | `number` | 0 |
| max | 最大值 | `number` | 100 |
| disabled | 是否禁用 | `boolean` | false |
| step | 步长，可以是数字或 `'mark'` 2.13.6，用于将值限制为刻度。 当设置为 `'mark'` 时，必须设置 `marks` 属性。 | `number` / `string` | 1 |
| show-input | 是否显示输入框，仅在 `range` 为 false 且 `step` 不为 `'mark'` 时生效。 | `boolean` | false |
| show-input-controls | 在显示输入框的情况下，是否显示输入框的控制按钮 | `boolean` | true |
| size | slider 包装器的大小，垂直模式下该属性不可用 | `enum` | default |
| input-size | 输入框的大小，如果设置了 `size` 属性，默认值自动取 `size` | `enum` | default |
| show-stops | 是否显示间断点 | `boolean` | false |
| show-tooltip | 是否显示提示信息 | `boolean` | true |
| format-tooltip | 格式化提示信息 | `Function` | — |
| range | 是否开启选择范围 | `boolean` | false |
| vertical | 垂直模式 | `boolean` | false |
| height | 滑块高度，垂直模式必填 | `string` | — |
| aria-label a11y 2.7.2 | 原生 `aria-label`属性 | `string` | — |
| range-start-label | 当 `range` 为true时，屏幕阅读器标签开始的标记 | `string` | — |
| range-end-label | 当 `range` 为true时，屏幕阅读器标签结尾的标记 | `string` | — |
| format-value-text | 显示屏幕阅读器的 `aria-valuenow` 属性的格式 | `Function` | — |
| tooltip-class | tooltip 的自定义类名 | `string` | — |
| placement | Tooltip 出现的位置 | `enum` | top |
| marks | 标记， key 的类型必须为 `number` 且取值在闭区间 `[min, max]` 内，每个标记可以单独设置样式 | `object` | — |
| validate-event | 输入时是否触发表单的校验 | `boolean` | true |
| persistent 2.9.5 | 当 slider 的 tooltip 处于非活动状态且 `persistent` 为 `false` 时，tooltip 将被销毁。 当 `show-tooltip` 为 `false` 时，`persistent` 将始终为 `false`。 | `boolean` | true |
| label a11y deprecated | 原生 `aria-label`属性 | `string` | — |

### 事件 [​](#事件)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 值改变时触发（使用鼠标拖曳时，只在松开鼠标后触发） | `Function` |
| input | 数据改变时触发（使用鼠标拖曳时，活动过程实时触发） | `Function` |

## 类型声明 [​](#类型声明)

显示类型声明

ts

```
type SliderMarks = Record<number, string | { style: CSSProperties; label: any }>
type Arrayable<T> = T | T[]
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/slider) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/slider.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/slider.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/65441198?v=4&size=64)](https://github.com/tyj-321)[![](https://avatars.githubusercontent.com/u/105651386?v=4&size=64)](https://github.com/heappynd)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/25742988?v=4&size=64)](https://github.com/Geekhyt)[![](https://avatars.githubusercontent.com/u/26035718?v=4&size=64)](https://github.com/SnowingFox)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/1411614?v=4&size=64)](https://github.com/spx443812507)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/90810762?v=4&size=64)](https://github.com/charles-lpd)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/36978416?v=4&size=64)](https://github.com/SimonaliaChen)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/33687038?v=4&size=64)](https://github.com/guozi9999)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/140705167?v=4&size=64)](https://github.com/zhongli-kira)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/24468747?v=4&size=64)](https://github.com/hddhyq)

[Virtualized Select 虚拟化选择器](https://element-plus.org/zh-CN/component/select-v2)

[Switch 开关](https://element-plus.org/zh-CN/component/switch)


