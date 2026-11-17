## Alert 提示 ​

**URL:** https://element-plus.org/zh-CN/component/alert

**Contents:**
- Alert 提示 ​
- 基础用法 ​
- 主题 ​
- 自定义关闭按钮 ​
- 使用图标 ​
- 文字居中 ​
- 文字描述 ​
- 带图标和描述 ​
- Alert API ​
  - 属性 ​

Alert 组件不属于浮层元素，不会自动消失或关闭。

Alert 组件提供5种类型，由 type 属性指定，默认值为 info。 primary 已被添加到2.9.11。

Alert 组件提供了两个不同的主题：light 和 dark。

通过设置 effect 属性来改变主题，默认为 light。

你可以设置 Alert 组件是否为可关闭状态， 关闭按钮的内容以及关闭时的回调函数同样可以定制。 closable 属性决定 Alert 组件是否可关闭， 该属性接受一个 Boolean，默认为 false。 你可以设置 close-text 属性来代替右侧的关闭图标， 需要注意的是 close-text 必须是一个字符串。 当 Alert 组件被关闭时会触发 close 事件。

你可以通过为 Alert 组件添加图标来提高可读性。

通过设置 show-icon 属性来显示 Alert 的 icon，这能更有效地向用户展示你的显示意图。 或者你可以使用 icon slot 自定义 icon 内容。

使用 center 属性来让文字水平居中。

为 Alert 组件添加一个更加详细的描述来使用户了解更多信息。

除了必填的 title 属性外，你可以设置 description 属性来帮助你更好地介绍，我们称之为辅助性文字。 辅助性文字只能存放文本内容，当内容超出长度限制时会自动换行显示。

This is a description.

More text description

More text description

More text description

More text description

More text description

**Examples:**

Example 1 (vue):
```vue
<template>
  <div style="max-width: 600px">
    <el-alert title="Primary alert" type="primary" />
    <el-alert title="Success alert" type="success" />
    <el-alert title="Info alert" type="info" />
    <el-alert title="Warning alert" type="warning" />
    <el-alert title="Error alert" type="error" />
  </div>
</template>

<style scoped>
.el-alert {
  margin: 20px 0 0;
}
.el-alert:first-child {
  margin: 0;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div style="max-width: 600px">
    <el-alert title="Primary alert" type="primary" effect="dark" />
    <el-alert title="Success alert" type="success" effect="dark" />
    <el-alert title="Info alert" type="info" effect="dark" />
    <el-alert title="Warning alert" type="warning" effect="dark" />
    <el-alert title="Error alert" type="error" effect="dark" />
  </div>
</template>

<style scoped>
.el-alert {
  margin: 20px 0 0;
}
.el-alert:first-child {
  margin: 0;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <div style="max-width: 600px">
    <el-alert title="Unclosable alert" type="success" :closable="false" />
    <el-alert title="Customized close text" type="info" close-text="Gotcha" />
    <el-alert title="Alert with callback" type="warning" @close="hello" />
  </div>
</template>

<script lang="ts" setup>
const hello = () => {
  // eslint-disable-next-line no-alert
  alert('Hello World!')
}
</script>

<style scoped>
.el-alert {
  margin: 20px 0 0;
}
.el-alert:first-child {
  margin: 0;
}
</style>
```

Example 4 (vue):
```vue
<template>
  <div style="max-width: 600px">
    <el-alert title="Primary alert" type="primary" show-icon />
    <el-alert title="Success alert" type="success" show-icon />
    <el-alert title="Info alert" type="info" show-icon />
    <el-alert title="Warning alert" type="warning" show-icon />
    <el-alert title="Error alert" type="error" show-icon />
    <el-alert title="Error alert with custom icon" type="error" show-icon>
      <template #icon>
        <Bell />
      </template>
    </el-alert>
  </div>
</template>

<script lang="ts" setup>
import { Bell } from '@element-plus/icons-vue'
</script>

<style scoped>
.el-alert {
  margin: 20px 0 0;
}
.el-alert:first-child {
  margin: 0;
}
</style>
```

---
