---
name: "progress"
description: "Progress 进度条 -- Element Plus Vue3 桌面端组件。Invoke when user needs Progress 进度条 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/progress.html"
---

---

# Progress 进度条 [​](#progress-进度条)

更新日志待解决

1

用于展示操作进度，告知用户当前状态和预期。

## 直线进度条 [​](#直线进度条)

Progress 组件设置 `percentage` 属性即可，表示进度条对应的百分比。 该属性**必填**，并且必须在 `0-100` 的范围内。 你可以通过设置 `format` 来自定义文字显示的格式。

50%

Full

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1wcm9ncmVzc1wiPlxuICAgIDxlbC1wcm9ncmVzcyA6cGVyY2VudGFnZT1cIjUwXCIgLz5cbiAgICA8ZWwtcHJvZ3Jlc3MgOnBlcmNlbnRhZ2U9XCIxMDBcIiA6Zm9ybWF0PVwiZm9ybWF0XCIgLz5cbiAgICA8ZWwtcHJvZ3Jlc3MgOnBlcmNlbnRhZ2U9XCIxMDBcIiBzdGF0dXM9XCJzdWNjZXNzXCIgLz5cbiAgICA8ZWwtcHJvZ3Jlc3MgOnBlcmNlbnRhZ2U9XCIxMDBcIiBzdGF0dXM9XCJ3YXJuaW5nXCIgLz5cbiAgICA8ZWwtcHJvZ3Jlc3MgOnBlcmNlbnRhZ2U9XCI1MFwiIHN0YXR1cz1cImV4Y2VwdGlvblwiIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IGZvcm1hdCA9IChwZXJjZW50YWdlKSA9PiAocGVyY2VudGFnZSA9PT0gMTAwID8gJ0Z1bGwnIDogYCR7cGVyY2VudGFnZX0lYClcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tcHJvZ3Jlc3MgLmVsLXByb2dyZXNzLS1saW5lIHtcbiAgbWFyZ2luLWJvdHRvbTogMTVweDtcbiAgbWF4LXdpZHRoOiA2MDBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/progress/linear-progress-bar.vue)_

vue

```
<template>
  <div class="demo-progress">
    <el-progress :percentage="50" />
    <el-progress :percentage="100" :format="format" />
    <el-progress :percentage="100" status="success" />
    <el-progress :percentage="100" status="warning" />
    <el-progress :percentage="50" status="exception" />
  </div>
</template>

<script lang="ts" setup>
const format = (percentage) => (percentage === 100 ? 'Full' : `${percentage}%`)
</script>

<style scoped>
.demo-progress .el-progress--line {
  margin-bottom: 15px;
  max-width: 600px;
}
</style>
```

隐藏源代码

## 进度条内显示百分比标识 [​](#进度条内显示百分比标识)

百分比不占用额外空间，适用于文件上传等场景。

Progress 组件可通过 `stroke-width` 属性更改进度条的高度，并可通过 `text-inside` 属性来改变进度条内部的文字。

70%

100%

80%

50%

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1wcm9ncmVzc1wiPlxuICAgIDxlbC1wcm9ncmVzcyA6dGV4dC1pbnNpZGU9XCJ0cnVlXCIgOnN0cm9rZS13aWR0aD1cIjI2XCIgOnBlcmNlbnRhZ2U9XCI3MFwiIC8+XG4gICAgPGVsLXByb2dyZXNzXG4gICAgICA6dGV4dC1pbnNpZGU9XCJ0cnVlXCJcbiAgICAgIDpzdHJva2Utd2lkdGg9XCIyNFwiXG4gICAgICA6cGVyY2VudGFnZT1cIjEwMFwiXG4gICAgICBzdGF0dXM9XCJzdWNjZXNzXCJcbiAgICAvPlxuICAgIDxlbC1wcm9ncmVzc1xuICAgICAgOnRleHQtaW5zaWRlPVwidHJ1ZVwiXG4gICAgICA6c3Ryb2tlLXdpZHRoPVwiMjJcIlxuICAgICAgOnBlcmNlbnRhZ2U9XCI4MFwiXG4gICAgICBzdGF0dXM9XCJ3YXJuaW5nXCJcbiAgICAvPlxuICAgIDxlbC1wcm9ncmVzc1xuICAgICAgOnRleHQtaW5zaWRlPVwidHJ1ZVwiXG4gICAgICA6c3Ryb2tlLXdpZHRoPVwiMjBcIlxuICAgICAgOnBlcmNlbnRhZ2U9XCI1MFwiXG4gICAgICBzdGF0dXM9XCJleGNlcHRpb25cIlxuICAgIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLXByb2dyZXNzIC5lbC1wcm9ncmVzcy0tbGluZSB7XG4gIG1hcmdpbi1ib3R0b206IDE1cHg7XG4gIG1heC13aWR0aDogNjAwcHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/progress/internal-percentage.vue)_

vue

```
<template>
  <div class="demo-progress">
    <el-progress :text-inside="true" :stroke-width="26" :percentage="70" />
    <el-progress
      :text-inside="true"
      :stroke-width="24"
      :percentage="100"
      status="success"
    />
    <el-progress
      :text-inside="true"
      :stroke-width="22"
      :percentage="80"
      status="warning"
    />
    <el-progress
      :text-inside="true"
      :stroke-width="20"
      :percentage="50"
      status="exception"
    />
  </div>
</template>

<style scoped>
.demo-progress .el-progress--line {
  margin-bottom: 15px;
  max-width: 600px;
}
</style>
```

隐藏源代码

## 自定义进度条的颜色 [​](#自定义进度条的颜色)

可以通过 `color` 属性来设置进度条的颜色。 该属性可以接受十六进制颜色值，函数和数组。

20%

20%

20%

20%

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1wcm9ncmVzc1wiPlxuICAgIDxlbC1wcm9ncmVzcyA6cGVyY2VudGFnZT1cInBlcmNlbnRhZ2VcIiA6Y29sb3I9XCJjdXN0b21Db2xvclwiIC8+XG5cbiAgICA8ZWwtcHJvZ3Jlc3MgOnBlcmNlbnRhZ2U9XCJwZXJjZW50YWdlXCIgOmNvbG9yPVwiY3VzdG9tQ29sb3JNZXRob2RcIiAvPlxuXG4gICAgPGVsLXByb2dyZXNzIDpwZXJjZW50YWdlPVwicGVyY2VudGFnZVwiIDpjb2xvcj1cImN1c3RvbUNvbG9yc1wiIC8+XG4gICAgPGVsLXByb2dyZXNzIDpwZXJjZW50YWdlPVwicGVyY2VudGFnZVwiIDpjb2xvcj1cImN1c3RvbUNvbG9yc1wiIC8+XG4gICAgPGRpdj5cbiAgICAgIDxlbC1idXR0b24tZ3JvdXA+XG4gICAgICAgIDxlbC1idXR0b24gOmljb249XCJNaW51c1wiIEBjbGljaz1cImRlY3JlYXNlXCIgLz5cbiAgICAgICAgPGVsLWJ1dHRvbiA6aWNvbj1cIlBsdXNcIiBAY2xpY2s9XCJpbmNyZWFzZVwiIC8+XG4gICAgICA8L2VsLWJ1dHRvbi1ncm91cD5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgTWludXMsIFBsdXMgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgcGVyY2VudGFnZSA9IHJlZigyMClcbmNvbnN0IGN1c3RvbUNvbG9yID0gcmVmKCcjNDA5ZWZmJylcblxuY29uc3QgY3VzdG9tQ29sb3JzID0gW1xuICB7IGNvbG9yOiAnI2Y1NmM2YycsIHBlcmNlbnRhZ2U6IDIwIH0sXG4gIHsgY29sb3I6ICcjZTZhMjNjJywgcGVyY2VudGFnZTogNDAgfSxcbiAgeyBjb2xvcjogJyM1Y2I4N2EnLCBwZXJjZW50YWdlOiA2MCB9LFxuICB7IGNvbG9yOiAnIzE5ODlmYScsIHBlcmNlbnRhZ2U6IDgwIH0sXG4gIHsgY29sb3I6ICcjNmY3YWQzJywgcGVyY2VudGFnZTogMTAwIH0sXG5dXG5cbmNvbnN0IGN1c3RvbUNvbG9yTWV0aG9kID0gKHBlcmNlbnRhZ2U6IG51bWJlcikgPT4ge1xuICBpZiAocGVyY2VudGFnZSA8IDMwKSB7XG4gICAgcmV0dXJuICcjOTA5Mzk5J1xuICB9XG4gIGlmIChwZXJjZW50YWdlIDwgNzApIHtcbiAgICByZXR1cm4gJyNlNmEyM2MnXG4gIH1cbiAgcmV0dXJuICcjNjdjMjNhJ1xufVxuY29uc3QgaW5jcmVhc2UgPSAoKSA9PiB7XG4gIHBlcmNlbnRhZ2UudmFsdWUgKz0gMTBcbiAgaWYgKHBlcmNlbnRhZ2UudmFsdWUgPiAxMDApIHtcbiAgICBwZXJjZW50YWdlLnZhbHVlID0gMTAwXG4gIH1cbn1cbmNvbnN0IGRlY3JlYXNlID0gKCkgPT4ge1xuICBwZXJjZW50YWdlLnZhbHVlIC09IDEwXG4gIGlmIChwZXJjZW50YWdlLnZhbHVlIDwgMCkge1xuICAgIHBlcmNlbnRhZ2UudmFsdWUgPSAwXG4gIH1cbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tcHJvZ3Jlc3MgLmVsLXByb2dyZXNzLS1saW5lIHtcbiAgbWFyZ2luLWJvdHRvbTogMTVweDtcbiAgbWF4LXdpZHRoOiA2MDBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/progress/custom-color.vue)_

vue

```
<template>
  <div class="demo-progress">
    <el-progress :percentage="percentage" :color="customColor" />

    <el-progress :percentage="percentage" :color="customColorMethod" />

    <el-progress :percentage="percentage" :color="customColors" />
    <el-progress :percentage="percentage" :color="customColors" />
    <div>
      <el-button-group>
        <el-button :icon="Minus" @click="decrease" />
        <el-button :icon="Plus" @click="increase" />
      </el-button-group>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Minus, Plus } from '@element-plus/icons-vue'

const percentage = ref(20)
const customColor = ref('#409eff')

const customColors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 },
]

const customColorMethod = (percentage: number) => {
  if (percentage < 30) {
    return '#909399'
  }
  if (percentage < 70) {
    return '#e6a23c'
  }
  return '#67c23a'
}
const increase = () => {
  percentage.value += 10
  if (percentage.value > 100) {
    percentage.value = 100
  }
}
const decrease = () => {
  percentage.value -= 10
  if (percentage.value < 0) {
    percentage.value = 0
  }
}
</script>

<style scoped>
.demo-progress .el-progress--line {
  margin-bottom: 15px;
  max-width: 600px;
}
</style>
```

隐藏源代码

## 环形进度条 [​](#环形进度条)

Progress 组件可通过 `type` 属性来指定使用环形进度条，在环形进度条中，还可以通过 `width` 属性来设置其大小。

0%

25%

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1wcm9ncmVzc1wiPlxuICAgIDxlbC1wcm9ncmVzcyB0eXBlPVwiY2lyY2xlXCIgOnBlcmNlbnRhZ2U9XCIwXCIgLz5cbiAgICA8ZWwtcHJvZ3Jlc3MgdHlwZT1cImNpcmNsZVwiIDpwZXJjZW50YWdlPVwiMjVcIiAvPlxuICAgIDxlbC1wcm9ncmVzcyB0eXBlPVwiY2lyY2xlXCIgOnBlcmNlbnRhZ2U9XCIxMDBcIiBzdGF0dXM9XCJzdWNjZXNzXCIgLz5cbiAgICA8ZWwtcHJvZ3Jlc3MgdHlwZT1cImNpcmNsZVwiIDpwZXJjZW50YWdlPVwiNzBcIiBzdGF0dXM9XCJ3YXJuaW5nXCIgLz5cbiAgICA8ZWwtcHJvZ3Jlc3MgdHlwZT1cImNpcmNsZVwiIDpwZXJjZW50YWdlPVwiNTBcIiBzdGF0dXM9XCJleGNlcHRpb25cIiAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1wcm9ncmVzcyAuZWwtcHJvZ3Jlc3MtLWNpcmNsZSB7XG4gIG1hcmdpbi1yaWdodDogMTVweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/progress/circular-progress-bar.vue)_

vue

```
<template>
  <div class="demo-progress">
    <el-progress type="circle" :percentage="0" />
    <el-progress type="circle" :percentage="25" />
    <el-progress type="circle" :percentage="100" status="success" />
    <el-progress type="circle" :percentage="70" status="warning" />
    <el-progress type="circle" :percentage="50" status="exception" />
  </div>
</template>

<style scoped>
.demo-progress .el-progress--circle {
  margin-right: 15px;
}
</style>
```

隐藏源代码

## 仪表盘形进度条 [​](#仪表盘形进度条)

您也可以指定 `type` 属性到 `dashboard` 使用控制面板进度栏。

10%

70%

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1wcm9ncmVzc1wiPlxuICAgIDxlbC1wcm9ncmVzcyB0eXBlPVwiZGFzaGJvYXJkXCIgOnBlcmNlbnRhZ2U9XCJwZXJjZW50YWdlXCIgOmNvbG9yPVwiY29sb3JzXCIgLz5cbiAgICA8ZWwtcHJvZ3Jlc3MgdHlwZT1cImRhc2hib2FyZFwiIDpwZXJjZW50YWdlPVwicGVyY2VudGFnZTJcIiA6Y29sb3I9XCJjb2xvcnNcIiAvPlxuICAgIDxkaXY+XG4gICAgICA8ZWwtYnV0dG9uLWdyb3VwPlxuICAgICAgICA8ZWwtYnV0dG9uIDppY29uPVwiTWludXNcIiBAY2xpY2s9XCJkZWNyZWFzZVwiIC8+XG4gICAgICAgIDxlbC1idXR0b24gOmljb249XCJQbHVzXCIgQGNsaWNrPVwiaW5jcmVhc2VcIiAvPlxuICAgICAgPC9lbC1idXR0b24tZ3JvdXA+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IG9uTW91bnRlZCwgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgTWludXMsIFBsdXMgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgcGVyY2VudGFnZSA9IHJlZigxMClcbmNvbnN0IHBlcmNlbnRhZ2UyID0gcmVmKDApXG5cbmNvbnN0IGNvbG9ycyA9IFtcbiAgeyBjb2xvcjogJyNmNTZjNmMnLCBwZXJjZW50YWdlOiAyMCB9LFxuICB7IGNvbG9yOiAnI2U2YTIzYycsIHBlcmNlbnRhZ2U6IDQwIH0sXG4gIHsgY29sb3I6ICcjNWNiODdhJywgcGVyY2VudGFnZTogNjAgfSxcbiAgeyBjb2xvcjogJyMxOTg5ZmEnLCBwZXJjZW50YWdlOiA4MCB9LFxuICB7IGNvbG9yOiAnIzZmN2FkMycsIHBlcmNlbnRhZ2U6IDEwMCB9LFxuXVxuXG5jb25zdCBpbmNyZWFzZSA9ICgpID0+IHtcbiAgcGVyY2VudGFnZS52YWx1ZSArPSAxMFxuICBpZiAocGVyY2VudGFnZS52YWx1ZSA+IDEwMCkge1xuICAgIHBlcmNlbnRhZ2UudmFsdWUgPSAxMDBcbiAgfVxufVxuY29uc3QgZGVjcmVhc2UgPSAoKSA9PiB7XG4gIHBlcmNlbnRhZ2UudmFsdWUgLT0gMTBcbiAgaWYgKHBlcmNlbnRhZ2UudmFsdWUgPCAwKSB7XG4gICAgcGVyY2VudGFnZS52YWx1ZSA9IDBcbiAgfVxufVxub25Nb3VudGVkKCgpID0+IHtcbiAgc2V0SW50ZXJ2YWwoKCkgPT4ge1xuICAgIHBlcmNlbnRhZ2UyLnZhbHVlID0gKHBlcmNlbnRhZ2UyLnZhbHVlICUgMTAwKSArIDEwXG4gIH0sIDUwMClcbn0pXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLXByb2dyZXNzIC5lbC1wcm9ncmVzcy0tbGluZSB7XG4gIG1hcmdpbi1ib3R0b206IDE1cHg7XG4gIG1heC13aWR0aDogNjAwcHg7XG59XG4uZGVtby1wcm9ncmVzcyAuZWwtcHJvZ3Jlc3MtLWNpcmNsZSB7XG4gIG1hcmdpbi1yaWdodDogMTVweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/progress/dashboard-progress-bar.vue)_

vue

```
<template>
  <div class="demo-progress">
    <el-progress type="dashboard" :percentage="percentage" :color="colors" />
    <el-progress type="dashboard" :percentage="percentage2" :color="colors" />
    <div>
      <el-button-group>
        <el-button :icon="Minus" @click="decrease" />
        <el-button :icon="Plus" @click="increase" />
      </el-button-group>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { Minus, Plus } from '@element-plus/icons-vue'

const percentage = ref(10)
const percentage2 = ref(0)

const colors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 },
]

const increase = () => {
  percentage.value += 10
  if (percentage.value > 100) {
    percentage.value = 100
  }
}
const decrease = () => {
  percentage.value -= 10
  if (percentage.value < 0) {
    percentage.value = 0
  }
}
onMounted(() => {
  setInterval(() => {
    percentage2.value = (percentage2.value % 100) + 10
  }, 500)
})
</script>

<style scoped>
.demo-progress .el-progress--line {
  margin-bottom: 15px;
  max-width: 600px;
}
.demo-progress .el-progress--circle {
  margin-right: 15px;
}
</style>
```

隐藏源代码

## 自定义内容 [​](#自定义内容)

通过默认插槽添加自定义内容。

Content

Content

80%Progressing

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1wcm9ncmVzc1wiPlxuICAgIDxlbC1wcm9ncmVzcyA6cGVyY2VudGFnZT1cIjUwXCI+XG4gICAgICA8ZWwtYnV0dG9uIHRleHQ+Q29udGVudDwvZWwtYnV0dG9uPlxuICAgIDwvZWwtcHJvZ3Jlc3M+XG4gICAgPGVsLXByb2dyZXNzXG4gICAgICA6dGV4dC1pbnNpZGU9XCJ0cnVlXCJcbiAgICAgIDpzdHJva2Utd2lkdGg9XCIyMFwiXG4gICAgICA6cGVyY2VudGFnZT1cIjUwXCJcbiAgICAgIHN0YXR1cz1cImV4Y2VwdGlvblwiXG4gICAgPlxuICAgICAgPHNwYW4+Q29udGVudDwvc3Bhbj5cbiAgICA8L2VsLXByb2dyZXNzPlxuICAgIDxlbC1wcm9ncmVzcyB0eXBlPVwiY2lyY2xlXCIgOnBlcmNlbnRhZ2U9XCIxMDBcIiBzdGF0dXM9XCJzdWNjZXNzXCI+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJzdWNjZXNzXCIgOmljb249XCJDaGVja1wiIGNpcmNsZSAvPlxuICAgIDwvZWwtcHJvZ3Jlc3M+XG4gICAgPGVsLXByb2dyZXNzIHR5cGU9XCJkYXNoYm9hcmRcIiA6cGVyY2VudGFnZT1cIjgwXCI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJ7IHBlcmNlbnRhZ2UgfVwiPlxuICAgICAgICA8c3BhbiBjbGFzcz1cInBlcmNlbnRhZ2UtdmFsdWVcIj57eyBwZXJjZW50YWdlIH19JTwvc3Bhbj5cbiAgICAgICAgPHNwYW4gY2xhc3M9XCJwZXJjZW50YWdlLWxhYmVsXCI+UHJvZ3Jlc3Npbmc8L3NwYW4+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtcHJvZ3Jlc3M+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IENoZWNrIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5wZXJjZW50YWdlLXZhbHVlIHtcbiAgZGlzcGxheTogYmxvY2s7XG4gIG1hcmdpbi10b3A6IDEwcHg7XG4gIGZvbnQtc2l6ZTogMjhweDtcbn1cbi5wZXJjZW50YWdlLWxhYmVsIHtcbiAgZGlzcGxheTogYmxvY2s7XG4gIG1hcmdpbi10b3A6IDEwcHg7XG4gIGZvbnQtc2l6ZTogMTJweDtcbn1cbi5kZW1vLXByb2dyZXNzIC5lbC1wcm9ncmVzcy0tbGluZSB7XG4gIG1hcmdpbi1ib3R0b206IDE1cHg7XG4gIG1heC13aWR0aDogNjAwcHg7XG59XG4uZGVtby1wcm9ncmVzcyAuZWwtcHJvZ3Jlc3MtLWNpcmNsZSB7XG4gIG1hcmdpbi1yaWdodDogMTVweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/progress/customized-content.vue)_

vue

```
<template>
  <div class="demo-progress">
    <el-progress :percentage="50">
      <el-button text>Content</el-button>
    </el-progress>
    <el-progress
      :text-inside="true"
      :stroke-width="20"
      :percentage="50"
      status="exception"
    >
      <span>Content</span>
    </el-progress>
    <el-progress type="circle" :percentage="100" status="success">
      <el-button type="success" :icon="Check" circle />
    </el-progress>
    <el-progress type="dashboard" :percentage="80">
      <template #default="{ percentage }">
        <span class="percentage-value">{{ percentage }}%</span>
        <span class="percentage-label">Progressing</span>
      </template>
    </el-progress>
  </div>
</template>

<script lang="ts" setup>
import { Check } from '@element-plus/icons-vue'
</script>

<style scoped>
.percentage-value {
  display: block;
  margin-top: 10px;
  font-size: 28px;
}
.percentage-label {
  display: block;
  margin-top: 10px;
  font-size: 12px;
}
.demo-progress .el-progress--line {
  margin-bottom: 15px;
  max-width: 600px;
}
.demo-progress .el-progress--circle {
  margin-right: 15px;
}
</style>
```

隐藏源代码

## 动画进度条 [​](#动画进度条)

使用 `indeterminate` 属性来设置不确定的进度， `duration` 来控制动画持续时间。

50%

Full

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1wcm9ncmVzc1wiPlxuICAgIDxlbC1wcm9ncmVzcyA6cGVyY2VudGFnZT1cIjUwXCIgOmluZGV0ZXJtaW5hdGU9XCJ0cnVlXCIgLz5cbiAgICA8ZWwtcHJvZ3Jlc3MgOnBlcmNlbnRhZ2U9XCIxMDBcIiA6Zm9ybWF0PVwiZm9ybWF0XCIgOmluZGV0ZXJtaW5hdGU9XCJ0cnVlXCIgLz5cbiAgICA8ZWwtcHJvZ3Jlc3NcbiAgICAgIDpwZXJjZW50YWdlPVwiMTAwXCJcbiAgICAgIHN0YXR1cz1cInN1Y2Nlc3NcIlxuICAgICAgOmluZGV0ZXJtaW5hdGU9XCJ0cnVlXCJcbiAgICAgIDpkdXJhdGlvbj1cIjVcIlxuICAgIC8+XG4gICAgPGVsLXByb2dyZXNzXG4gICAgICA6cGVyY2VudGFnZT1cIjEwMFwiXG4gICAgICBzdGF0dXM9XCJ3YXJuaW5nXCJcbiAgICAgIDppbmRldGVybWluYXRlPVwidHJ1ZVwiXG4gICAgICA6ZHVyYXRpb249XCIxXCJcbiAgICAvPlxuICAgIDxlbC1wcm9ncmVzcyA6cGVyY2VudGFnZT1cIjUwXCIgc3RhdHVzPVwiZXhjZXB0aW9uXCIgOmluZGV0ZXJtaW5hdGU9XCJ0cnVlXCIgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuY29uc3QgZm9ybWF0ID0gKHBlcmNlbnRhZ2UpID0+IChwZXJjZW50YWdlID09PSAxMDAgPyAnRnVsbCcgOiBgJHtwZXJjZW50YWdlfSVgKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1wcm9ncmVzcyAuZWwtcHJvZ3Jlc3MtLWxpbmUge1xuICBtYXJnaW4tYm90dG9tOiAxNXB4O1xuICBtYXgtd2lkdGg6IDYwMHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/progress/indeterminate-progress.vue)_

vue

```
<template>
  <div class="demo-progress">
    <el-progress :percentage="50" :indeterminate="true" />
    <el-progress :percentage="100" :format="format" :indeterminate="true" />
    <el-progress
      :percentage="100"
      status="success"
      :indeterminate="true"
      :duration="5"
    />
    <el-progress
      :percentage="100"
      status="warning"
      :indeterminate="true"
      :duration="1"
    />
    <el-progress :percentage="50" status="exception" :indeterminate="true" />
  </div>
</template>

<script lang="ts" setup>
const format = (percentage) => (percentage === 100 ? 'Full' : `${percentage}%`)
</script>

<style scoped>
.demo-progress .el-progress--line {
  margin-bottom: 15px;
  max-width: 600px;
}
</style>
```

隐藏源代码

## 条纹进度条 [​](#条纹进度条)

通过设置 `striped` 属性获取条纹进度条。 也可以使用 `striped-flow` 属性来使条纹流动起来。 使用`duration` 属性来控制条纹流动的速度。

50%

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1wcm9ncmVzc1wiPlxuICAgIDxlbC1wcm9ncmVzcyA6cGVyY2VudGFnZT1cIjUwXCIgOnN0cm9rZS13aWR0aD1cIjE1XCIgc3RyaXBlZCAvPlxuICAgIDxlbC1wcm9ncmVzc1xuICAgICAgOnBlcmNlbnRhZ2U9XCIzMFwiXG4gICAgICA6c3Ryb2tlLXdpZHRoPVwiMTVcIlxuICAgICAgc3RhdHVzPVwid2FybmluZ1wiXG4gICAgICBzdHJpcGVkXG4gICAgICBzdHJpcGVkLWZsb3dcbiAgICAvPlxuICAgIDxlbC1wcm9ncmVzc1xuICAgICAgOnBlcmNlbnRhZ2U9XCIxMDBcIlxuICAgICAgOnN0cm9rZS13aWR0aD1cIjE1XCJcbiAgICAgIHN0YXR1cz1cInN1Y2Nlc3NcIlxuICAgICAgc3RyaXBlZFxuICAgICAgc3RyaXBlZC1mbG93XG4gICAgICA6ZHVyYXRpb249XCIxMFwiXG4gICAgLz5cbiAgICA8ZWwtcHJvZ3Jlc3NcbiAgICAgIDpwZXJjZW50YWdlPVwicGVyY2VudGFnZVwiXG4gICAgICA6c3Ryb2tlLXdpZHRoPVwiMTVcIlxuICAgICAgc3RhdHVzPVwiZXhjZXB0aW9uXCJcbiAgICAgIHN0cmlwZWRcbiAgICAgIHN0cmlwZWQtZmxvd1xuICAgICAgOmR1cmF0aW9uPVwiZHVyYXRpb25cIlxuICAgIC8+XG4gICAgPGVsLWJ1dHRvbi1ncm91cD5cbiAgICAgIDxlbC1idXR0b24gOmljb249XCJNaW51c1wiIEBjbGljaz1cImRlY3JlYXNlXCIgLz5cbiAgICAgIDxlbC1idXR0b24gOmljb249XCJQbHVzXCIgQGNsaWNrPVwiaW5jcmVhc2VcIiAvPlxuICAgIDwvZWwtYnV0dG9uLWdyb3VwPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBjb21wdXRlZCwgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgTWludXMsIFBsdXMgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgcGVyY2VudGFnZSA9IHJlZjxudW1iZXI+KDcwKVxuY29uc3QgZHVyYXRpb24gPSBjb21wdXRlZCgoKSA9PiBNYXRoLmZsb29yKHBlcmNlbnRhZ2UudmFsdWUgLyAxMCkpXG5cbmNvbnN0IGluY3JlYXNlID0gKCkgPT4ge1xuICBwZXJjZW50YWdlLnZhbHVlICs9IDEwXG4gIGlmIChwZXJjZW50YWdlLnZhbHVlID4gMTAwKSB7XG4gICAgcGVyY2VudGFnZS52YWx1ZSA9IDEwMFxuICB9XG59XG5jb25zdCBkZWNyZWFzZSA9ICgpID0+IHtcbiAgcGVyY2VudGFnZS52YWx1ZSAtPSAxMFxuICBpZiAocGVyY2VudGFnZS52YWx1ZSA8IDApIHtcbiAgICBwZXJjZW50YWdlLnZhbHVlID0gMFxuICB9XG59XG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLXByb2dyZXNzIC5lbC1wcm9ncmVzcy0tbGluZSB7XG4gIG1hcmdpbi1ib3R0b206IDE1cHg7XG4gIG1heC13aWR0aDogNjAwcHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/progress/striped-progress.vue)_

vue

```
<template>
  <div class="demo-progress">
    <el-progress :percentage="50" :stroke-width="15" striped />
    <el-progress
      :percentage="30"
      :stroke-width="15"
      status="warning"
      striped
      striped-flow
    />
    <el-progress
      :percentage="100"
      :stroke-width="15"
      status="success"
      striped
      striped-flow
      :duration="10"
    />
    <el-progress
      :percentage="percentage"
      :stroke-width="15"
      status="exception"
      striped
      striped-flow
      :duration="duration"
    />
    <el-button-group>
      <el-button :icon="Minus" @click="decrease" />
      <el-button :icon="Plus" @click="increase" />
    </el-button-group>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { Minus, Plus } from '@element-plus/icons-vue'

const percentage = ref<number>(70)
const duration = computed(() => Math.floor(percentage.value / 10))

const increase = () => {
  percentage.value += 10
  if (percentage.value > 100) {
    percentage.value = 100
  }
}
const decrease = () => {
  percentage.value -= 10
  if (percentage.value < 0) {
    percentage.value = 0
  }
}
</script>

<style scoped>
.demo-progress .el-progress--line {
  margin-bottom: 15px;
  max-width: 600px;
}
</style>
```

隐藏源代码

## API [​](#api)

### 属性 [​](#属性)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| percentage required | percentage | `number` | 0 |
| type | 进度条类型 | `enum` | line |
| stroke-width | 进度条的宽度 | `number` | 6 |
| text-inside | 进度条显示文字内置在进度条内（仅 `type` 为 'line' 时可用） | `boolean` | false |
| status | 进度条当前状态 | `enum` | — |
| indeterminate | 是否为动画进度条 | `boolean` | false |
| duration | 控制动画进度条速度和条纹进度条流动速度 | `number` | 3 |
| color | 进度条背景色 （会覆盖 `status` 状态颜色） | `string` / `function` / `Array` | '' |
| width | 环形进度条画布宽度（只在 type 为 circle 或 dashboard 时可用） | `number` | 126 |
| show-text | 是否显示进度条文字内容 | `boolean` | true |
| stroke-linecap | circle/dashboard 类型路径两端的形状 | `enum` | round |
| format | 指定进度条文字内容 | `Function` | — |
| striped 2.3.4 | 在进度条上增加条纹 | `boolean` | false |
| striped-flow 2.3.4 | 让进度条上的条纹流动起来 | `boolean` | false |

### Slots [​](#slots)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| default | 自定义内容 | `object` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/progress) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/progress.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/progress.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/82307113?v=4&size=64)](https://github.com/754664196)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/9958583?v=4&size=64)](https://github.com/Otto-J)[![](https://avatars.githubusercontent.com/u/12029924?v=4&size=64)](https://github.com/rottenpen)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/33799081?v=4&size=64)](https://github.com/wuyadan)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/50621078?v=4&size=64)](https://github.com/HYzihong)

[Pagination 分页](https://element-plus.org/zh-CN/component/pagination)

[Result 结果](https://element-plus.org/zh-CN/component/result)


