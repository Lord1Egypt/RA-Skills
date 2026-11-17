## Notification 通知 ​

**URL:** https://element-plus.org/zh-CN/component/notification

**Contents:**
- Notification 通知 ​
- 基础用法 ​
- 不同类型的通知 ​
- 自定义消息弹出的位置 ​
- 有位置偏移的通知栏 ​
- 使用 HTML 片段作为正文内容 ​
- 函数形式的 message 2.9.0 ​
- 隐藏关闭按钮 ​
- 全局方法 ​
- 单独引用 ​

悬浮出现在页面角落，显示全局的通知提醒消息。

Element Plus 注册了 $notify 方法并且它接受一个 Object 作为其参数。 在最简单的情况下，你可以通过设置 title 和 message 属性来设置通知的标题和正文内容。 默认情况下，通知在4500毫秒后自动关闭，但你可以通过设置 duration 属性来自定义通知的展示时间。 如果你将它设置为 0，那么通知将不会自动关闭。 需要注意的是 duration 接收一个 Number，单位为毫秒。

我们提供了四种不同类型的提醒框：success、warning、info 和error。

Element Plus 为 Notification 组件准备了5种通知类型：primary,success, warning, info, error。 他们可以设置 type 字段来修改，除上述的四个值之外的值会被忽略。 同时，我们也为 Notification 的各种 type 注册了单独的方法，可以在不传入 type 字段的情况下像 open3 和 open4 那样直接调用。 primary 已被添加到2.9.11。

可以让 Notification 从屏幕四角中的任意一角弹出

使用 position 属性设置 Notification 的弹出位置， 支持四个选项：top-right、top-left、bottom-right 和 bottom-left， 默认为 top-right。

能够设置偏移量来使 Notification 偏移默认位置。

Notification 提供设置偏移量的功能，通过设置 offset 字段，可以使弹出的消息距屏幕边缘偏移一段距离。 注意在同一时刻，每一个的 Notification 实例应当具有一个相同的偏移量。

message 支持传入 HTML 字符串来作为正文内容。

将 dangerouslyUseHTMLString 属性设置为 true，message 属性就会被当作 HTML 片段处理。

message 属性虽然支持传入 HTML 片段，但是在网站上动态渲染任意 HTML 是非常危险的，因为容易导致 XSS 攻击。 因此在 dangerouslyUseHTMLString 打开的情况下，请确保 message 的内容是可信的，永远不要将用户提交的内容赋值给 message 属性。

在2.9.0之后， message 支持返回值为 VNode的函数。

将 showClose 属性设置为 false 即可隐藏关闭按钮。

Element Plus 为 app.config.globalProperties 添加了全局方法 $notify。 因此在 Vue instance 中可以采用本页面中的方式调用 Notification。

你可以在对应的处理函数内调用 ElNotification(options) 来呼出通知栏。 我们也提前定义了多个 type 的单独调用方法，如 ElNotification.success(options)。 当你需要关闭页面上所有的通知栏的时候，可以调用 ElNotification.closeAll() 来关闭所有的实例。 在 2.10.5 版本中，你可以通过调用 ElNotification.updateOffsets(position) 手动更新所有通知实例在特定方向上的偏移量。

现在 Notification 接受一条 context 作为消息构造器的第二个参数，允许你将当前应用的上下文注入到 Notification 中，这将允许你继承应用程序的所有属性。

如果您全局注册了 ElNotification 组件，它将自动继承应用的上下文环境。

Notification 和 this.$notify 都返回当前的 Notification 实例。 如果需要手动关闭实例，可以调用它的 close 方法。

**Examples:**

Example 1 (jsx):
```jsx
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" plain @click="open1">
      Closes automatically
    </el-button>
    <el-button class="!ml-0" plain @click="open2">
      Won't close automatically
    </el-button>
  </div>
</template>

<script lang="ts" setup>
import { h } from 'vue'
import { ElNotification } from 'element-plus'

const open1 = () => {
  ElNotification({
    title: 'Title',
    message: h('i', { style: 'color: teal' }, 'This is a reminder'),
  })
}

const open2 = () => {
  ElNotification({
    title: 'Prompt',
    message: 'This is a message that does not automatically close',
    duration: 0,
  })
}
</script>
```

Example 2 (jsx):
```jsx
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" plain @click="open5">Primary</el-button>
    <el-button class="!ml-0" plain @click="open1">Success</el-button>
    <el-button class="!ml-0" plain @click="open2">Warning</el-button>
    <el-button class="!ml-0" plain @click="open3">Info</el-button>
    <el-button class="!ml-0" plain @click="open4">Error</el-button>
  </div>
</template>

<script lang="ts" setup>
import { ElNotification } from 'element-plus'

const open1 = () => {
  ElNotification({
    title: 'Success',
    message: 'This is a success message',
    type: 'success',
  })
}

const open2 = () => {
  ElNotification({
    title: 'Warning',
    message: 'This is a warning message',
    type: 'warning',
  })
}

const open3 = () => {
  ElNotification({
    title: 'Info',
    message: 'This is an info message',
    type: 'info',
  })
}

const open4 = () => {
  ElNotification({
    title: 'Error',
    message: 'This is an error message',
    type: 'error',
  })
}

const open5 = () => {
  ElNotification({
    title: 'Primary',
    message: 'This is a primary message',
    type: 'primary',
  })
}
</script>
```

Example 3 (jsx):
```jsx
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" plain @click="open1"> Top Right </el-button>
    <el-button class="!ml-0" plain @click="open2"> Bottom Right </el-button>
    <el-button class="!ml-0" plain @click="open3"> Bottom Left </el-button>
    <el-button class="!ml-0" plain @click="open4"> Top Left </el-button>
  </div>
</template>

<script lang="ts" setup>
import { ElNotification } from 'element-plus'

const open1 = () => {
  ElNotification({
    title: 'Custom Position',
    message: "I'm at the top right corner",
  })
}

const open2 = () => {
  ElNotification({
    title: 'Custom Position',
    message: "I'm at the bottom right corner",
    position: 'bottom-right',
  })
}

const open3 = () => {
  ElNotification({
    title: 'Custom Position',
    message: "I'm at the bottom left corner",
    position: 'bottom-left',
  })
}

const open4 = () => {
  ElNotification({
    title: 'Custom Position',
    message: "I'm at the top left corner",
    position: 'top-left',
  })
}
</script>
```

Example 4 (jsx):
```jsx
<template>
  <el-button plain @click="open"> Notification with offset </el-button>
</template>

<script lang="ts" setup>
import { ElNotification } from 'element-plus'

const open = () => {
  ElNotification.success({
    title: 'Success',
    message: 'This is a success message',
    offset: 100,
  })
}
</script>
```

---
