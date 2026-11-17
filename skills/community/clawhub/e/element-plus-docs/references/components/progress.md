## Progress 进度条 ​

**URL:** https://element-plus.org/zh-CN/component/progress

**Contents:**
- Progress 进度条 ​
- 直线进度条 ​
- 进度条内显示百分比标识 ​
- 自定义进度条的颜色 ​
- 环形进度条 ​
- 仪表盘形进度条 ​
- 自定义内容 ​
- 动画进度条 ​
- 条纹进度条 ​
- API ​

用于展示操作进度，告知用户当前状态和预期。

Progress 组件设置 percentage 属性即可，表示进度条对应的百分比。 该属性必填，并且必须在 0-100 的范围内。 你可以通过设置 format 来自定义文字显示的格式。

百分比不占用额外空间，适用于文件上传等场景。

Progress 组件可通过 stroke-width 属性更改进度条的高度，并可通过 text-inside 属性来改变进度条内部的文字。

可以通过 color 属性来设置进度条的颜色。 该属性可以接受十六进制颜色值，函数和数组。

Progress 组件可通过 type 属性来指定使用环形进度条，在环形进度条中，还可以通过 width 属性来设置其大小。

您也可以指定 type 属性到 dashboard 使用控制面板进度栏。

使用 indeterminate 属性来设置不确定的进度， duration 来控制动画持续时间。

通过设置 striped 属性获取条纹进度条。 也可以使用 striped-flow 属性来使条纹流动起来。 使用duration 属性来控制条纹流动的速度。

**Examples:**

Example 1 (vue):
```vue
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

Example 2 (vue):
```vue
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

Example 3 (vue):
```vue
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

Example 4 (vue):
```vue
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

---
