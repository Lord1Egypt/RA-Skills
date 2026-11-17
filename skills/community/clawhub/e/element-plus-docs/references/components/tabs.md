## Tabs 标签页 ​

**URL:** https://element-plus.org/zh-CN/component/tabs

**Contents:**
- Tabs 标签页 ​
- 基础用法 ​
- 卡片风格的标签 ​
- 带有边框的卡片风格 ​
- 标签位置的设置 ​
- 自定义标签页的内容 ​
- 动态增减标签页 ​
- 添加按钮自定义图标 2.4.0 ​
- 增加标签页触发器自定义 ​
- 默认值2.11.9 ​

分隔内容上有关联但属于不同类别的数据集合。

Tabs 组件提供了选项卡功能， 默认选中第一个标签页，你也可以通过 value 属性来指定当前选中的标签页。

只需要设置 type 属性为 card 就可以使选项卡改变为标签风格。

将 type 设置为 border-card。

可以通过 tab-position 设置标签的位置

标签一共有四个方向的设置 tabPosition="left|right|top|bottom"

增减标签页按钮只能在选项卡样式的标签页下使用

我们已对外暴露了实现该功能所需的必要能力。 您可以查看 示例 来用原生的方式实现。 或使用 SortableJs, 示例。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
    <el-tab-pane label="User" name="first">User</el-tab-pane>
    <el-tab-pane label="Config" name="second">Config</el-tab-pane>
    <el-tab-pane label="Role" name="third">Role</el-tab-pane>
    <el-tab-pane label="Task" name="fourth">Task</el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TabsPaneContext } from 'element-plus'

const activeName = ref('first')

const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event)
}
</script>

<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <el-tabs
    v-model="activeName"
    type="card"
    class="demo-tabs"
    @tab-click="handleClick"
  >
    <el-tab-pane label="User" name="first">User</el-tab-pane>
    <el-tab-pane label="Config" name="second">Config</el-tab-pane>
    <el-tab-pane label="Role" name="third">Role</el-tab-pane>
    <el-tab-pane label="Task" name="fourth">Task</el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TabsPaneContext } from 'element-plus'

const activeName = ref('first')

const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event)
}
</script>

<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <el-tabs type="border-card">
    <el-tab-pane label="User">User</el-tab-pane>
    <el-tab-pane label="Config">Config</el-tab-pane>
    <el-tab-pane label="Role">Role</el-tab-pane>
    <el-tab-pane label="Task">Task</el-tab-pane>
  </el-tabs>
</template>
```

Example 4 (vue):
```vue
<template>
  <el-radio-group v-model="tabPosition" style="margin-bottom: 30px">
    <el-radio-button value="top">top</el-radio-button>
    <el-radio-button value="right">right</el-radio-button>
    <el-radio-button value="bottom">bottom</el-radio-button>
    <el-radio-button value="left">left</el-radio-button>
  </el-radio-group>

  <el-tabs :tab-position="tabPosition" style="height: 200px" class="demo-tabs">
    <el-tab-pane label="User">User</el-tab-pane>
    <el-tab-pane label="Config">Config</el-tab-pane>
    <el-tab-pane label="Role">Role</el-tab-pane>
    <el-tab-pane label="Task">Task</el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TabsInstance } from 'element-plus'

const tabPosition = ref<TabsInstance['tabPosition']>('left')
</script>

<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.el-tabs--right .el-tabs__content,
.el-tabs--left .el-tabs__content {
  height: 100%;
}
</style>
```

---
