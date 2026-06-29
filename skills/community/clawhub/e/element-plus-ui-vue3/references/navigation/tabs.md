---
name: "tabs"
description: "Tabs 标签页 -- Element Plus Vue3 桌面端组件。Invoke when user needs Tabs 标签页 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/tabs.html"
---

---

# Tabs 标签页 [​](#tabs-标签页)

更新日志待解决

9

分隔内容上有关联但属于不同类别的数据集合。

## 基础用法 [​](#基础用法)

基础的、简洁的标签页。

Tabs 组件提供了选项卡功能， 默认选中第一个标签页，你也可以通过 `value` 属性来指定当前选中的标签页。

User

Config

Role

Task

User

Config

Role

Task

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFicyB2LW1vZGVsPVwiYWN0aXZlTmFtZVwiIGNsYXNzPVwiZGVtby10YWJzXCIgQHRhYi1jbGljaz1cImhhbmRsZUNsaWNrXCI+XG4gICAgPGVsLXRhYi1wYW5lIGxhYmVsPVwiVXNlclwiIG5hbWU9XCJmaXJzdFwiPlVzZXI8L2VsLXRhYi1wYW5lPlxuICAgIDxlbC10YWItcGFuZSBsYWJlbD1cIkNvbmZpZ1wiIG5hbWU9XCJzZWNvbmRcIj5Db25maWc8L2VsLXRhYi1wYW5lPlxuICAgIDxlbC10YWItcGFuZSBsYWJlbD1cIlJvbGVcIiBuYW1lPVwidGhpcmRcIj5Sb2xlPC9lbC10YWItcGFuZT5cbiAgICA8ZWwtdGFiLXBhbmUgbGFiZWw9XCJUYXNrXCIgbmFtZT1cImZvdXJ0aFwiPlRhc2s8L2VsLXRhYi1wYW5lPlxuICA8L2VsLXRhYnM+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFRhYnNQYW5lQ29udGV4dCB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgYWN0aXZlTmFtZSA9IHJlZignZmlyc3QnKVxuXG5jb25zdCBoYW5kbGVDbGljayA9ICh0YWI6IFRhYnNQYW5lQ29udGV4dCwgZXZlbnQ6IEV2ZW50KSA9PiB7XG4gIGNvbnNvbGUubG9nKHRhYiwgZXZlbnQpXG59XG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLmRlbW8tdGFicyA+IC5lbC10YWJzX19jb250ZW50IHtcbiAgcGFkZGluZzogMzJweDtcbiAgY29sb3I6ICM2Yjc3OGM7XG4gIGZvbnQtc2l6ZTogMzJweDtcbiAgZm9udC13ZWlnaHQ6IDYwMDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tabs/basic.vue)_

vue

```
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

隐藏源代码

## 卡片风格的标签 [​](#卡片风格的标签)

你可以设置具有卡片风格的标签。

只需要设置 `type` 属性为 `card` 就可以使选项卡改变为标签风格。

User

Config

Role

Task

User

Config

Role

Task

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFic1xuICAgIHYtbW9kZWw9XCJhY3RpdmVOYW1lXCJcbiAgICB0eXBlPVwiY2FyZFwiXG4gICAgY2xhc3M9XCJkZW1vLXRhYnNcIlxuICAgIEB0YWItY2xpY2s9XCJoYW5kbGVDbGlja1wiXG4gID5cbiAgICA8ZWwtdGFiLXBhbmUgbGFiZWw9XCJVc2VyXCIgbmFtZT1cImZpcnN0XCI+VXNlcjwvZWwtdGFiLXBhbmU+XG4gICAgPGVsLXRhYi1wYW5lIGxhYmVsPVwiQ29uZmlnXCIgbmFtZT1cInNlY29uZFwiPkNvbmZpZzwvZWwtdGFiLXBhbmU+XG4gICAgPGVsLXRhYi1wYW5lIGxhYmVsPVwiUm9sZVwiIG5hbWU9XCJ0aGlyZFwiPlJvbGU8L2VsLXRhYi1wYW5lPlxuICAgIDxlbC10YWItcGFuZSBsYWJlbD1cIlRhc2tcIiBuYW1lPVwiZm91cnRoXCI+VGFzazwvZWwtdGFiLXBhbmU+XG4gIDwvZWwtdGFicz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgVGFic1BhbmVDb250ZXh0IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBhY3RpdmVOYW1lID0gcmVmKCdmaXJzdCcpXG5cbmNvbnN0IGhhbmRsZUNsaWNrID0gKHRhYjogVGFic1BhbmVDb250ZXh0LCBldmVudDogRXZlbnQpID0+IHtcbiAgY29uc29sZS5sb2codGFiLCBldmVudClcbn1cbjwvc2NyaXB0PlxuXG48c3R5bGU+XG4uZGVtby10YWJzID4gLmVsLXRhYnNfX2NvbnRlbnQge1xuICBwYWRkaW5nOiAzMnB4O1xuICBjb2xvcjogIzZiNzc4YztcbiAgZm9udC1zaXplOiAzMnB4O1xuICBmb250LXdlaWdodDogNjAwO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tabs/card-style.vue)_

vue

```
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

隐藏源代码

## 带有边框的卡片风格 [​](#带有边框的卡片风格)

你还可以设置标签页为带有边框的卡片

将 `type` 设置为 `border-card`。

User

Config

Role

Task

User

Config

Role

Task

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFicyB0eXBlPVwiYm9yZGVyLWNhcmRcIj5cbiAgICA8ZWwtdGFiLXBhbmUgbGFiZWw9XCJVc2VyXCI+VXNlcjwvZWwtdGFiLXBhbmU+XG4gICAgPGVsLXRhYi1wYW5lIGxhYmVsPVwiQ29uZmlnXCI+Q29uZmlnPC9lbC10YWItcGFuZT5cbiAgICA8ZWwtdGFiLXBhbmUgbGFiZWw9XCJSb2xlXCI+Um9sZTwvZWwtdGFiLXBhbmU+XG4gICAgPGVsLXRhYi1wYW5lIGxhYmVsPVwiVGFza1wiPlRhc2s8L2VsLXRhYi1wYW5lPlxuICA8L2VsLXRhYnM+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tabs/border-card.vue)_

vue

```
<template>
  <el-tabs type="border-card">
    <el-tab-pane label="User">User</el-tab-pane>
    <el-tab-pane label="Config">Config</el-tab-pane>
    <el-tab-pane label="Role">Role</el-tab-pane>
    <el-tab-pane label="Task">Task</el-tab-pane>
  </el-tabs>
</template>
```

隐藏源代码

## 标签位置的设置 [​](#标签位置的设置)

可以通过 `tab-position` 设置标签的位置

标签一共有四个方向的设置 `tabPosition="left|right|top|bottom"`

toprightbottomleft

User

Config

Role

Task

User

Config

Role

Task

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInRhYlBvc2l0aW9uXCIgc3R5bGU9XCJtYXJnaW4tYm90dG9tOiAzMHB4XCI+XG4gICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cInRvcFwiPnRvcDwvZWwtcmFkaW8tYnV0dG9uPlxuICAgIDxlbC1yYWRpby1idXR0b24gdmFsdWU9XCJyaWdodFwiPnJpZ2h0PC9lbC1yYWRpby1idXR0b24+XG4gICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cImJvdHRvbVwiPmJvdHRvbTwvZWwtcmFkaW8tYnV0dG9uPlxuICAgIDxlbC1yYWRpby1idXR0b24gdmFsdWU9XCJsZWZ0XCI+bGVmdDwvZWwtcmFkaW8tYnV0dG9uPlxuICA8L2VsLXJhZGlvLWdyb3VwPlxuXG4gIDxlbC10YWJzIDp0YWItcG9zaXRpb249XCJ0YWJQb3NpdGlvblwiIHN0eWxlPVwiaGVpZ2h0OiAyMDBweFwiIGNsYXNzPVwiZGVtby10YWJzXCI+XG4gICAgPGVsLXRhYi1wYW5lIGxhYmVsPVwiVXNlclwiPlVzZXI8L2VsLXRhYi1wYW5lPlxuICAgIDxlbC10YWItcGFuZSBsYWJlbD1cIkNvbmZpZ1wiPkNvbmZpZzwvZWwtdGFiLXBhbmU+XG4gICAgPGVsLXRhYi1wYW5lIGxhYmVsPVwiUm9sZVwiPlJvbGU8L2VsLXRhYi1wYW5lPlxuICAgIDxlbC10YWItcGFuZSBsYWJlbD1cIlRhc2tcIj5UYXNrPC9lbC10YWItcGFuZT5cbiAgPC9lbC10YWJzPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBUYWJzSW5zdGFuY2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHRhYlBvc2l0aW9uID0gcmVmPFRhYnNJbnN0YW5jZVsndGFiUG9zaXRpb24nXT4oJ2xlZnQnKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5kZW1vLXRhYnMgPiAuZWwtdGFic19fY29udGVudCB7XG4gIHBhZGRpbmc6IDMycHg7XG4gIGNvbG9yOiAjNmI3NzhjO1xuICBmb250LXNpemU6IDMycHg7XG4gIGZvbnQtd2VpZ2h0OiA2MDA7XG59XG5cbi5lbC10YWJzLS1yaWdodCAuZWwtdGFic19fY29udGVudCxcbi5lbC10YWJzLS1sZWZ0IC5lbC10YWJzX19jb250ZW50IHtcbiAgaGVpZ2h0OiAxMDAlO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tabs/tab-position.vue)_

vue

```
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

隐藏源代码

## 自定义标签页的内容 [​](#自定义标签页的内容)

可以通过具名插槽来实现自定义标签页的内容

Route

Config

Role

Task

Route

Config

Role

Task

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFicyB0eXBlPVwiYm9yZGVyLWNhcmRcIiBjbGFzcz1cImRlbW8tdGFic1wiPlxuICAgIDxlbC10YWItcGFuZT5cbiAgICAgIDx0ZW1wbGF0ZSAjbGFiZWw+XG4gICAgICAgIDxzcGFuIGNsYXNzPVwiY3VzdG9tLXRhYnMtbGFiZWxcIj5cbiAgICAgICAgICA8ZWwtaWNvbj48Y2FsZW5kYXIgLz48L2VsLWljb24+XG4gICAgICAgICAgPHNwYW4+Um91dGU8L3NwYW4+XG4gICAgICAgIDwvc3Bhbj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgICBSb3V0ZVxuICAgIDwvZWwtdGFiLXBhbmU+XG4gICAgPGVsLXRhYi1wYW5lIGxhYmVsPVwiQ29uZmlnXCI+Q29uZmlnPC9lbC10YWItcGFuZT5cbiAgICA8ZWwtdGFiLXBhbmUgbGFiZWw9XCJSb2xlXCI+Um9sZTwvZWwtdGFiLXBhbmU+XG4gICAgPGVsLXRhYi1wYW5lIGxhYmVsPVwiVGFza1wiPlRhc2s8L2VsLXRhYi1wYW5lPlxuICA8L2VsLXRhYnM+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgQ2FsZW5kYXIgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcbjwvc2NyaXB0PlxuXG48c3R5bGU+XG4uZGVtby10YWJzID4gLmVsLXRhYnNfX2NvbnRlbnQge1xuICBwYWRkaW5nOiAzMnB4O1xuICBjb2xvcjogIzZiNzc4YztcbiAgZm9udC1zaXplOiAzMnB4O1xuICBmb250LXdlaWdodDogNjAwO1xufVxuLmRlbW8tdGFicyAuY3VzdG9tLXRhYnMtbGFiZWwgLmVsLWljb24ge1xuICB2ZXJ0aWNhbC1hbGlnbjogbWlkZGxlO1xufVxuLmRlbW8tdGFicyAuY3VzdG9tLXRhYnMtbGFiZWwgc3BhbiB7XG4gIHZlcnRpY2FsLWFsaWduOiBtaWRkbGU7XG4gIG1hcmdpbi1sZWZ0OiA0cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tabs/custom-tab.vue)_

vue

```
<template>
  <el-tabs type="border-card" class="demo-tabs">
    <el-tab-pane>
      <template #label>
        <span class="custom-tabs-label">
          <el-icon><calendar /></el-icon>
          <span>Route</span>
        </span>
      </template>
      Route
    </el-tab-pane>
    <el-tab-pane label="Config">Config</el-tab-pane>
    <el-tab-pane label="Role">Role</el-tab-pane>
    <el-tab-pane label="Task">Task</el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { Calendar } from '@element-plus/icons-vue'
</script>

<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.demo-tabs .custom-tabs-label .el-icon {
  vertical-align: middle;
}
.demo-tabs .custom-tabs-label span {
  vertical-align: middle;
  margin-left: 4px;
}
</style>
```

隐藏源代码

## 动态增减标签页 [​](#动态增减标签页)

增减标签页按钮只能在选项卡样式的标签页下使用

Tab 1

Tab 2

Tab 1 content

Tab 2 content

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFic1xuICAgIHYtbW9kZWw9XCJlZGl0YWJsZVRhYnNWYWx1ZVwiXG4gICAgdHlwZT1cImNhcmRcIlxuICAgIGVkaXRhYmxlXG4gICAgY2xhc3M9XCJkZW1vLXRhYnNcIlxuICAgIEBlZGl0PVwiaGFuZGxlVGFic0VkaXRcIlxuICA+XG4gICAgPGVsLXRhYi1wYW5lXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gZWRpdGFibGVUYWJzXCJcbiAgICAgIDprZXk9XCJpdGVtLm5hbWVcIlxuICAgICAgOmxhYmVsPVwiaXRlbS50aXRsZVwiXG4gICAgICA6bmFtZT1cIml0ZW0ubmFtZVwiXG4gICAgPlxuICAgICAge3sgaXRlbS5jb250ZW50IH19XG4gICAgPC9lbC10YWItcGFuZT5cbiAgPC9lbC10YWJzPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBUYWJQYW5lTmFtZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxubGV0IHRhYkluZGV4ID0gMlxuY29uc3QgZWRpdGFibGVUYWJzVmFsdWUgPSByZWYoJzInKVxuY29uc3QgZWRpdGFibGVUYWJzID0gcmVmKFtcbiAge1xuICAgIHRpdGxlOiAnVGFiIDEnLFxuICAgIG5hbWU6ICcxJyxcbiAgICBjb250ZW50OiAnVGFiIDEgY29udGVudCcsXG4gIH0sXG4gIHtcbiAgICB0aXRsZTogJ1RhYiAyJyxcbiAgICBuYW1lOiAnMicsXG4gICAgY29udGVudDogJ1RhYiAyIGNvbnRlbnQnLFxuICB9LFxuXSlcblxuY29uc3QgaGFuZGxlVGFic0VkaXQgPSAoXG4gIHRhcmdldE5hbWU6IFRhYlBhbmVOYW1lIHwgdW5kZWZpbmVkLFxuICBhY3Rpb246ICdyZW1vdmUnIHwgJ2FkZCdcbikgPT4ge1xuICBpZiAoYWN0aW9uID09PSAnYWRkJykge1xuICAgIGNvbnN0IG5ld1RhYk5hbWUgPSBgJHsrK3RhYkluZGV4fWBcbiAgICBlZGl0YWJsZVRhYnMudmFsdWUucHVzaCh7XG4gICAgICB0aXRsZTogJ05ldyBUYWInLFxuICAgICAgbmFtZTogbmV3VGFiTmFtZSxcbiAgICAgIGNvbnRlbnQ6ICdOZXcgVGFiIGNvbnRlbnQnLFxuICAgIH0pXG4gICAgZWRpdGFibGVUYWJzVmFsdWUudmFsdWUgPSBuZXdUYWJOYW1lXG4gIH0gZWxzZSBpZiAoYWN0aW9uID09PSAncmVtb3ZlJykge1xuICAgIGNvbnN0IHRhYnMgPSBlZGl0YWJsZVRhYnMudmFsdWVcbiAgICBsZXQgYWN0aXZlTmFtZSA9IGVkaXRhYmxlVGFic1ZhbHVlLnZhbHVlXG4gICAgaWYgKGFjdGl2ZU5hbWUgPT09IHRhcmdldE5hbWUpIHtcbiAgICAgIHRhYnMuZm9yRWFjaCgodGFiLCBpbmRleCkgPT4ge1xuICAgICAgICBpZiAodGFiLm5hbWUgPT09IHRhcmdldE5hbWUpIHtcbiAgICAgICAgICBjb25zdCBuZXh0VGFiID0gdGFic1tpbmRleCArIDFdIHx8IHRhYnNbaW5kZXggLSAxXVxuICAgICAgICAgIGlmIChuZXh0VGFiKSB7XG4gICAgICAgICAgICBhY3RpdmVOYW1lID0gbmV4dFRhYi5uYW1lXG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9KVxuICAgIH1cblxuICAgIGVkaXRhYmxlVGFic1ZhbHVlLnZhbHVlID0gYWN0aXZlTmFtZVxuICAgIGVkaXRhYmxlVGFicy52YWx1ZSA9IHRhYnMuZmlsdGVyKCh0YWIpID0+IHRhYi5uYW1lICE9PSB0YXJnZXROYW1lKVxuICB9XG59XG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLmRlbW8tdGFicyA+IC5lbC10YWJzX19jb250ZW50IHtcbiAgcGFkZGluZzogMzJweDtcbiAgY29sb3I6ICM2Yjc3OGM7XG4gIGZvbnQtc2l6ZTogMzJweDtcbiAgZm9udC13ZWlnaHQ6IDYwMDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tabs/dynamic-tabs.vue)_

vue

```
<template>
  <el-tabs
    v-model="editableTabsValue"
    type="card"
    editable
    class="demo-tabs"
    @edit="handleTabsEdit"
  >
    <el-tab-pane
      v-for="item in editableTabs"
      :key="item.name"
      :label="item.title"
      :name="item.name"
    >
      {{ item.content }}
    </el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TabPaneName } from 'element-plus'

let tabIndex = 2
const editableTabsValue = ref('2')
const editableTabs = ref([
  {
    title: 'Tab 1',
    name: '1',
    content: 'Tab 1 content',
  },
  {
    title: 'Tab 2',
    name: '2',
    content: 'Tab 2 content',
  },
])

const handleTabsEdit = (
  targetName: TabPaneName | undefined,
  action: 'remove' | 'add'
) => {
  if (action === 'add') {
    const newTabName = `${++tabIndex}`
    editableTabs.value.push({
      title: 'New Tab',
      name: newTabName,
      content: 'New Tab content',
    })
    editableTabsValue.value = newTabName
  } else if (action === 'remove') {
    const tabs = editableTabs.value
    let activeName = editableTabsValue.value
    if (activeName === targetName) {
      tabs.forEach((tab, index) => {
        if (tab.name === targetName) {
          const nextTab = tabs[index + 1] || tabs[index - 1]
          if (nextTab) {
            activeName = nextTab.name
          }
        }
      })
    }

    editableTabsValue.value = activeName
    editableTabs.value = tabs.filter((tab) => tab.name !== targetName)
  }
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

隐藏源代码

## 添加按钮自定义图标 2.4.0 [​](#添加按钮自定义图标)

Tab 1

Tab 2

Tab 1 content

Tab 2 content

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiYWRkSWNvblxuPHRlbXBsYXRlPlxuICA8ZWwtdGFic1xuICAgIHYtbW9kZWw9XCJlZGl0YWJsZVRhYnNWYWx1ZVwiXG4gICAgdHlwZT1cImNhcmRcIlxuICAgIGNsYXNzPVwiZGVtby10YWJzXCJcbiAgICBlZGl0YWJsZVxuICAgIEBlZGl0PVwiaGFuZGxlVGFic0VkaXRcIlxuICA+XG4gICAgPHRlbXBsYXRlICNhZGQtaWNvbj5cbiAgICAgIDxlbC1pY29uPjxTZWxlY3QgLz48L2VsLWljb24+XG4gICAgPC90ZW1wbGF0ZT5cbiAgICA8ZWwtdGFiLXBhbmVcbiAgICAgIHYtZm9yPVwiaXRlbSBpbiBlZGl0YWJsZVRhYnNcIlxuICAgICAgOmtleT1cIml0ZW0ubmFtZVwiXG4gICAgICA6bGFiZWw9XCJpdGVtLnRpdGxlXCJcbiAgICAgIDpuYW1lPVwiaXRlbS5uYW1lXCJcbiAgICA+XG4gICAgICB7eyBpdGVtLmNvbnRlbnQgfX1cbiAgICA8L2VsLXRhYi1wYW5lPlxuICA8L2VsLXRhYnM+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgU2VsZWN0IH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmltcG9ydCB0eXBlIHsgVGFiUGFuZU5hbWUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmxldCB0YWJJbmRleCA9IDJcbmNvbnN0IGVkaXRhYmxlVGFic1ZhbHVlID0gcmVmKCcyJylcbmNvbnN0IGVkaXRhYmxlVGFicyA9IHJlZihbXG4gIHtcbiAgICB0aXRsZTogJ1RhYiAxJyxcbiAgICBuYW1lOiAnMScsXG4gICAgY29udGVudDogJ1RhYiAxIGNvbnRlbnQnLFxuICB9LFxuICB7XG4gICAgdGl0bGU6ICdUYWIgMicsXG4gICAgbmFtZTogJzInLFxuICAgIGNvbnRlbnQ6ICdUYWIgMiBjb250ZW50JyxcbiAgfSxcbl0pXG5cbmNvbnN0IGhhbmRsZVRhYnNFZGl0ID0gKFxuICB0YXJnZXROYW1lOiBUYWJQYW5lTmFtZSB8IHVuZGVmaW5lZCxcbiAgYWN0aW9uOiAncmVtb3ZlJyB8ICdhZGQnXG4pID0+IHtcbiAgaWYgKGFjdGlvbiA9PT0gJ2FkZCcpIHtcbiAgICBjb25zdCBuZXdUYWJOYW1lID0gYCR7Kyt0YWJJbmRleH1gXG4gICAgZWRpdGFibGVUYWJzLnZhbHVlLnB1c2goe1xuICAgICAgdGl0bGU6ICdOZXcgVGFiJyxcbiAgICAgIG5hbWU6IG5ld1RhYk5hbWUsXG4gICAgICBjb250ZW50OiAnTmV3IFRhYiBjb250ZW50JyxcbiAgICB9KVxuICAgIGVkaXRhYmxlVGFic1ZhbHVlLnZhbHVlID0gbmV3VGFiTmFtZVxuICB9IGVsc2UgaWYgKGFjdGlvbiA9PT0gJ3JlbW92ZScpIHtcbiAgICBjb25zdCB0YWJzID0gZWRpdGFibGVUYWJzLnZhbHVlXG4gICAgbGV0IGFjdGl2ZU5hbWUgPSBlZGl0YWJsZVRhYnNWYWx1ZS52YWx1ZVxuICAgIGlmIChhY3RpdmVOYW1lID09PSB0YXJnZXROYW1lKSB7XG4gICAgICB0YWJzLmZvckVhY2goKHRhYiwgaW5kZXgpID0+IHtcbiAgICAgICAgaWYgKHRhYi5uYW1lID09PSB0YXJnZXROYW1lKSB7XG4gICAgICAgICAgY29uc3QgbmV4dFRhYiA9IHRhYnNbaW5kZXggKyAxXSB8fCB0YWJzW2luZGV4IC0gMV1cbiAgICAgICAgICBpZiAobmV4dFRhYikge1xuICAgICAgICAgICAgYWN0aXZlTmFtZSA9IG5leHRUYWIubmFtZVxuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfSlcbiAgICB9XG5cbiAgICBlZGl0YWJsZVRhYnNWYWx1ZS52YWx1ZSA9IGFjdGl2ZU5hbWVcbiAgICBlZGl0YWJsZVRhYnMudmFsdWUgPSB0YWJzLmZpbHRlcigodGFiKSA9PiB0YWIubmFtZSAhPT0gdGFyZ2V0TmFtZSlcbiAgfVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5kZW1vLXRhYnMgPiAuZWwtdGFic19fY29udGVudCB7XG4gIHBhZGRpbmc6IDMycHg7XG4gIGNvbG9yOiAjNmI3NzhjO1xuICBmb250LXNpemU6IDMycHg7XG4gIGZvbnQtd2VpZ2h0OiA2MDA7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tabs/customized-add-button-icon.vue)_

vue

```
addIcon
<template>
  <el-tabs
    v-model="editableTabsValue"
    type="card"
    class="demo-tabs"
    editable
    @edit="handleTabsEdit"
  >
    <template #add-icon>
      <el-icon><Select /></el-icon>
    </template>
    <el-tab-pane
      v-for="item in editableTabs"
      :key="item.name"
      :label="item.title"
      :name="item.name"
    >
      {{ item.content }}
    </el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Select } from '@element-plus/icons-vue'

import type { TabPaneName } from 'element-plus'

let tabIndex = 2
const editableTabsValue = ref('2')
const editableTabs = ref([
  {
    title: 'Tab 1',
    name: '1',
    content: 'Tab 1 content',
  },
  {
    title: 'Tab 2',
    name: '2',
    content: 'Tab 2 content',
  },
])

const handleTabsEdit = (
  targetName: TabPaneName | undefined,
  action: 'remove' | 'add'
) => {
  if (action === 'add') {
    const newTabName = `${++tabIndex}`
    editableTabs.value.push({
      title: 'New Tab',
      name: newTabName,
      content: 'New Tab content',
    })
    editableTabsValue.value = newTabName
  } else if (action === 'remove') {
    const tabs = editableTabs.value
    let activeName = editableTabsValue.value
    if (activeName === targetName) {
      tabs.forEach((tab, index) => {
        if (tab.name === targetName) {
          const nextTab = tabs[index + 1] || tabs[index - 1]
          if (nextTab) {
            activeName = nextTab.name
          }
        }
      })
    }

    editableTabsValue.value = activeName
    editableTabs.value = tabs.filter((tab) => tab.name !== targetName)
  }
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

隐藏源代码

## 增加标签页触发器自定义 [​](#增加标签页触发器自定义)

add tab

Tab 1

Tab 2

Tab 1 content

Tab 2 content

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwibWFyZ2luLWJvdHRvbTogMjBweFwiPlxuICAgIDxlbC1idXR0b24gc2l6ZT1cInNtYWxsXCIgQGNsaWNrPVwiYWRkVGFiKGVkaXRhYmxlVGFic1ZhbHVlKVwiPlxuICAgICAgYWRkIHRhYlxuICAgIDwvZWwtYnV0dG9uPlxuICA8L2Rpdj5cbiAgPGVsLXRhYnNcbiAgICB2LW1vZGVsPVwiZWRpdGFibGVUYWJzVmFsdWVcIlxuICAgIHR5cGU9XCJjYXJkXCJcbiAgICBjbGFzcz1cImRlbW8tdGFic1wiXG4gICAgY2xvc2FibGVcbiAgICBAdGFiLXJlbW92ZT1cInJlbW92ZVRhYlwiXG4gID5cbiAgICA8ZWwtdGFiLXBhbmVcbiAgICAgIHYtZm9yPVwiaXRlbSBpbiBlZGl0YWJsZVRhYnNcIlxuICAgICAgOmtleT1cIml0ZW0ubmFtZVwiXG4gICAgICA6bGFiZWw9XCJpdGVtLnRpdGxlXCJcbiAgICAgIDpuYW1lPVwiaXRlbS5uYW1lXCJcbiAgICA+XG4gICAgICB7eyBpdGVtLmNvbnRlbnQgfX1cbiAgICA8L2VsLXRhYi1wYW5lPlxuICA8L2VsLXRhYnM+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFRhYlBhbmVOYW1lIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5sZXQgdGFiSW5kZXggPSAyXG5jb25zdCBlZGl0YWJsZVRhYnNWYWx1ZSA9IHJlZignMicpXG5jb25zdCBlZGl0YWJsZVRhYnMgPSByZWYoW1xuICB7XG4gICAgdGl0bGU6ICdUYWIgMScsXG4gICAgbmFtZTogJzEnLFxuICAgIGNvbnRlbnQ6ICdUYWIgMSBjb250ZW50JyxcbiAgfSxcbiAge1xuICAgIHRpdGxlOiAnVGFiIDInLFxuICAgIG5hbWU6ICcyJyxcbiAgICBjb250ZW50OiAnVGFiIDIgY29udGVudCcsXG4gIH0sXG5dKVxuXG5jb25zdCBhZGRUYWIgPSAodGFyZ2V0TmFtZTogc3RyaW5nKSA9PiB7XG4gIGNvbnN0IG5ld1RhYk5hbWUgPSBgJHsrK3RhYkluZGV4fWBcbiAgZWRpdGFibGVUYWJzLnZhbHVlLnB1c2goe1xuICAgIHRpdGxlOiAnTmV3IFRhYicsXG4gICAgbmFtZTogbmV3VGFiTmFtZSxcbiAgICBjb250ZW50OiAnTmV3IFRhYiBjb250ZW50JyxcbiAgfSlcbiAgZWRpdGFibGVUYWJzVmFsdWUudmFsdWUgPSBuZXdUYWJOYW1lXG59XG5jb25zdCByZW1vdmVUYWIgPSAodGFyZ2V0TmFtZTogVGFiUGFuZU5hbWUpID0+IHtcbiAgY29uc3QgdGFicyA9IGVkaXRhYmxlVGFicy52YWx1ZVxuICBsZXQgYWN0aXZlTmFtZSA9IGVkaXRhYmxlVGFic1ZhbHVlLnZhbHVlXG4gIGlmIChhY3RpdmVOYW1lID09PSB0YXJnZXROYW1lKSB7XG4gICAgdGFicy5mb3JFYWNoKCh0YWIsIGluZGV4KSA9PiB7XG4gICAgICBpZiAodGFiLm5hbWUgPT09IHRhcmdldE5hbWUpIHtcbiAgICAgICAgY29uc3QgbmV4dFRhYiA9IHRhYnNbaW5kZXggKyAxXSB8fCB0YWJzW2luZGV4IC0gMV1cbiAgICAgICAgaWYgKG5leHRUYWIpIHtcbiAgICAgICAgICBhY3RpdmVOYW1lID0gbmV4dFRhYi5uYW1lXG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KVxuICB9XG5cbiAgZWRpdGFibGVUYWJzVmFsdWUudmFsdWUgPSBhY3RpdmVOYW1lXG4gIGVkaXRhYmxlVGFicy52YWx1ZSA9IHRhYnMuZmlsdGVyKCh0YWIpID0+IHRhYi5uYW1lICE9PSB0YXJnZXROYW1lKVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5kZW1vLXRhYnMgPiAuZWwtdGFic19fY29udGVudCB7XG4gIHBhZGRpbmc6IDMycHg7XG4gIGNvbG9yOiAjNmI3NzhjO1xuICBmb250LXNpemU6IDMycHg7XG4gIGZvbnQtd2VpZ2h0OiA2MDA7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tabs/customized-trigger.vue)_

vue

```
<template>
  <div style="margin-bottom: 20px">
    <el-button size="small" @click="addTab(editableTabsValue)">
      add tab
    </el-button>
  </div>
  <el-tabs
    v-model="editableTabsValue"
    type="card"
    class="demo-tabs"
    closable
    @tab-remove="removeTab"
  >
    <el-tab-pane
      v-for="item in editableTabs"
      :key="item.name"
      :label="item.title"
      :name="item.name"
    >
      {{ item.content }}
    </el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TabPaneName } from 'element-plus'

let tabIndex = 2
const editableTabsValue = ref('2')
const editableTabs = ref([
  {
    title: 'Tab 1',
    name: '1',
    content: 'Tab 1 content',
  },
  {
    title: 'Tab 2',
    name: '2',
    content: 'Tab 2 content',
  },
])

const addTab = (targetName: string) => {
  const newTabName = `${++tabIndex}`
  editableTabs.value.push({
    title: 'New Tab',
    name: newTabName,
    content: 'New Tab content',
  })
  editableTabsValue.value = newTabName
}
const removeTab = (targetName: TabPaneName) => {
  const tabs = editableTabs.value
  let activeName = editableTabsValue.value
  if (activeName === targetName) {
    tabs.forEach((tab, index) => {
      if (tab.name === targetName) {
        const nextTab = tabs[index + 1] || tabs[index - 1]
        if (nextTab) {
          activeName = nextTab.name
        }
      }
    })
  }

  editableTabsValue.value = activeName
  editableTabs.value = tabs.filter((tab) => tab.name !== targetName)
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

隐藏源代码

## 默认值2.11.9 [​](#默认值)

User

Config

Role

Task

default-value: third
active:

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFic1xuICAgIHYtbW9kZWw9XCJhY3RpdmVOYW1lXCJcbiAgICBjbGFzcz1cImRlbW8tdGFic1wiXG4gICAgZGVmYXVsdC12YWx1ZT1cInRoaXJkXCJcbiAgICBAdGFiLWNsaWNrPVwiaGFuZGxlQ2xpY2tcIlxuICA+XG4gICAgPGVsLXRhYi1wYW5lXG4gICAgICB2LWZvcj1cInRhYiBpbiB0YWJzXCJcbiAgICAgIDprZXk9XCJ0YWIubmFtZVwiXG4gICAgICA6bGFiZWw9XCJ0YWIubGFiZWxcIlxuICAgICAgOm5hbWU9XCJ0YWIubmFtZVwiXG4gICAgPlxuICAgICAgZGVmYXVsdC12YWx1ZTogdGhpcmRcbiAgICAgIDxiciAvPlxuICAgICAgYWN0aXZlOiB7eyBhY3RpdmVOYW1lIH19XG4gICAgPC9lbC10YWItcGFuZT5cbiAgPC9lbC10YWJzPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBUYWJzUGFuZUNvbnRleHQgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHRhYnMgPSByZWYoW1xuICB7IGxhYmVsOiAnVXNlcicsIG5hbWU6ICdmaXJzdCcgfSxcbiAgeyBsYWJlbDogJ0NvbmZpZycsIG5hbWU6ICdzZWNvbmQnIH0sXG4gIHsgbGFiZWw6ICdSb2xlJywgbmFtZTogJ3RoaXJkJyB9LFxuICB7IGxhYmVsOiAnVGFzaycsIG5hbWU6ICdmb3VydGgnIH0sXG5dKVxuXG5jb25zdCBhY3RpdmVOYW1lID0gcmVmKClcblxuY29uc3QgaGFuZGxlQ2xpY2sgPSAodGFiOiBUYWJzUGFuZUNvbnRleHQsIGV2ZW50OiBFdmVudCkgPT4ge1xuICBjb25zb2xlLmxvZyh0YWIsIGV2ZW50KVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5kZW1vLXRhYnMgPiAuZWwtdGFic19fY29udGVudCB7XG4gIHBhZGRpbmc6IDMycHg7XG4gIGNvbG9yOiAjNmI3NzhjO1xuICBmb250LXNpemU6IDMycHg7XG4gIGZvbnQtd2VpZ2h0OiA2MDA7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tabs/default-value.vue)_

vue

```
<template>
  <el-tabs
    v-model="activeName"
    class="demo-tabs"
    default-value="third"
    @tab-click="handleClick"
  >
    <el-tab-pane
      v-for="tab in tabs"
      :key="tab.name"
      :label="tab.label"
      :name="tab.name"
    >
      default-value: third
      <br />
      active: {{ activeName }}
    </el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TabsPaneContext } from 'element-plus'

const tabs = ref([
  { label: 'User', name: 'first' },
  { label: 'Config', name: 'second' },
  { label: 'Role', name: 'third' },
  { label: 'Task', name: 'fourth' },
])

const activeName = ref()

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

隐藏源代码

## Tabs API [​](#tabs-api)

### Tabs Attributes [​](#tabs-attributes)

| 属性名 | 说明 | 类型 | Default |
| --- | --- | --- | --- |
| model-value / v-model | 绑定值，选中选项卡的 name，默认值是第一个 tab 的 name | `string` / `number` | — |
| default-value 2.11.9 | 在初始渲染时处于激活状态的标签的值。 （避免初始化时变动） | `string` / `number` |  |
| type | 风格类型 | `enum` | '' |
| closable | 标签是否可关闭 | `boolean` | false |
| addable | 标签是否可增加 | `boolean` | false |
| editable | 标签是否同时可增加和关闭 | `boolean` | false |
| tab-position | 选项卡所在位置 | `enum` | top |
| stretch | 标签的宽度是否自撑开 | `boolean` | false |
| before-leave | 切换标签之前的钩子函数， 若返回 `false` 或者返回被 reject 的 `Promise`，则阻止切换。 | `Function` | () => true |
| tabindex 2.11.7 | tabs 的 tabindex | `string` / `number` | 0 |

### Tabs Events [​](#tabs-events)

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| tab-click | tab 被选中时触发 | `Function` |
| tab-change | `activeName` 改变时触发 | `Function` |
| tab-remove | 点击 tab 移除按钮时触发 | `Function` |
| tab-add | 点击 tab 新增按钮时触发 | `Function` |
| edit | 点击 tab 的新增或移除按钮后触发 | `Function` |

### Tabs Slots [​](#tabs-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 默认插槽 | Tab-pane |
| add-icon 2.5.4 | 自定义添加按钮图标 | — |
| addIcon 2.4.0 deprecated | 自定义添加按钮图标 | — |

### Tabs Exposes [​](#tabs-exposes)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| currentName | 当前活动的面板名称 | `object` |
| tabNavRef 2.9.10 | tab-nav 组件实例 | `object` |

## Tab-nav API [​](#tab-nav-api)

### Tab-nav Exposes [​](#tab-nav-exposes)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| scrollToActiveTab | 滚动到活动标签 | `Function` |
| removeFocus | 移除聚焦状态 | `Function` |
| tabListRef 2.9.10 | el\_tabs\_\_nav html 元素 | `object` |
| tabBarRef 2.9.10 | el\_tabs\_\_nav bar 实例 | `object` |

## Tab-bar API [​](#tab-bar-api)

### Tab-bar Exposes [​](#tab-bar-exposes)

| 属性名 | 详情 | 类型 |
| --- | --- | --- |
| ref 2.9.10 | 选项卡根 HTML 元素 | `object` |
| update 2.9.10 | 手动更新标签栏样式的方法，返回更新后的样式 | `Function` |

## Tab-pane API [​](#tab-pane-api)

### Tab-pane Attributes [​](#tab-pane-attributes)

| 名称 | 详情 | Type | 默认值 |
| --- | --- | --- | --- |
| label | 选项卡标题 | `string` | '' |
| disabled | 是否禁用 | `boolean` | false |
| name | 与选项卡绑定值 value 对应的标识符，表示选项卡别名。默认值是tab面板的序列号，如第一个 tab 是 0 | `string` / `number` | — |
| closable | 标签是否可关闭 | `boolean` | false |
| lazy | 标签是否延迟渲染 | `boolean` | false |

### Tab-pane Slots [​](#tab-pane-slots)

| Name | Description |
| --- | --- |
| default | Tab-pane 的内容 |
| label | Tab-pane 的标题内容 |

## 常见问题 [​](#常见问题)

#### 如何使用可排序/可拖动的 tabs？ [​](#如何使用可排序-可拖动的-tabs)

我们已对外暴露了实现该功能所需的必要能力。 您可以查看 [示例](https://tinyurl.com/2jkyw82j) 来用原生的方式实现。 或使用 [SortableJs](https://github.com/SortableJS/Sortable), [示例](https://tinyurl.com/2r8js24y)。

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/tabs) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/tabs.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/tabs.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/33254923?v=4&size=64)](https://github.com/yicheny)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/9784767?v=4&size=64)](https://github.com/maicss)[![](https://avatars.githubusercontent.com/u/8479810?v=4&size=64)](https://github.com/xinconan)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/129492349?v=4&size=64)](https://github.com/Yolo-00)[![](https://avatars.githubusercontent.com/u/42017165?v=4&size=64)](https://github.com/Mario34)[![](https://avatars.githubusercontent.com/u/1532716?v=4&size=64)](https://github.com/godxiaoji)[![](https://avatars.githubusercontent.com/u/48897151?v=4&size=64)](https://github.com/RadiumAg)[![](https://avatars.githubusercontent.com/u/44231913?v=4&size=64)](https://github.com/THUzxj)[![](https://avatars.githubusercontent.com/u/26913795?v=4&size=64)](https://github.com/Lionad-Morotar)[![](https://avatars.githubusercontent.com/u/20185706?v=4&size=64)](https://github.com/xiahouwei)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/45936772?v=4&size=64)](https://github.com/KawaiiZapic)[![](https://avatars.githubusercontent.com/u/1321817?v=4&size=64)](https://github.com/oliverzy)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/34835258?v=4&size=64)](https://github.com/codingories)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/5283258?v=4&size=64)](https://github.com/satrong)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/36768323?v=4&size=64)](https://github.com/bigsnowballhehe)[![](https://avatars.githubusercontent.com/u/53803716?v=4&size=64)](https://github.com/MrpandaLiu)[![](https://avatars.githubusercontent.com/u/36811055?v=4&size=64)](https://github.com/iDestin)[![](https://avatars.githubusercontent.com/u/33464433?v=4&size=64)](https://github.com/cfmj)

[Steps 步骤条](https://element-plus.org/zh-CN/component/steps)

[Alert 提示](https://element-plus.org/zh-CN/component/alert)


