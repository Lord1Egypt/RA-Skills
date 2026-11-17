## Message 消息提示 ​

**URL:** https://element-plus.org/zh-CN/component/message

**Contents:**
- Message 消息提示 ​
- 基础用法 ​
- 不同状态 ​
- Plain 2.6.3 ​
- 可关闭的消息提示 ​
- 使用 HTML 片段作为正文内容 ​
- 分组消息合并 ​
- Placement 2.11.0 ​
- 全局方法 ​
- 单独引用 ​

常用于主动操作后的反馈提示。 与 Notification 的区别是后者更多用于系统级通知的被动提醒。

默认情况下在顶部显示并在 3 秒后消失。 您可以使用 placement 属性控制位置。

Message 在配置上与 Notification 非常类似，所以部分 options 在此不做详尽解释。 文末有 options 列表，可以结合 Notification 的文档理解它们。 Element Plus 注册了一个全局的 $message方法用于调用。 Message 可以接收一个字符串或一个 VNode 作为参数，它会被显示为正文内容。

用来显示「成功、警告、消息、错误」类的操作反馈。

当需要自定义更多属性时，Message 也可以接收一个对象为参数。 比如，设置 type 字段可以定义不同的状态，默认为info。 此时正文内容以 message 的值传入。 同时，我们也为 Message 的各种 type 注册了方法，可以在不传入 type 字段的情况下像 open4 那样直接调用。 primary 已被添加到2.9.11。

默认的 Message 是不可以被人工关闭的。 如果你需要手动关闭功能，你可以把 showClose 设置为 true 此外，和 Notification 一样，Message 拥有可控的 duration， 默认的关闭时间为 3000 毫秒，当把这个属性的值设置为0便表示该消息不会被自动关闭。

message 还支持使用 HTML 字符串作为正文内容。

将dangerouslyUseHTMLString属性设置为 true,message 就会被当作 HTML 片段处理。

message 属性虽然支持传入 HTML 片段，但是在网站上动态渲染任意 HTML 是非常危险的，因为容易导致 XSS 攻击。 因此在 dangerouslyUseHTMLString 打开的情况下，请确保 message 的内容是可信的，永远不要将用户提交的内容赋值给 message 属性。

设置 grouping 为 true，内容相同的 message 将被合并。

控制消息出现的位置。 消息可以显示在查看端口的顶部(默认) 或其他位置。

Element Plus 为 app.config.globalProperties 添加了全局方法 $message。 因此在 vue 实例中你可以使用当前页面中的调用方式调用 Message

此时调用方法为 ElMessage(options)。 我们也为每个 type 定义了各自的方法，如 ElMessage.success(options)。 并且可以调用 ElMessage.closeAll() 手动关闭所有实例。

现在 Message 接受一条 context 作为消息构造器的第二个参数，允许你将当前应用的上下文注入到 Message 中，这将允许你继承应用程序的所有属性。

如果您全局注册了 ElMessage 组件，它将自动继承应用的上下文环境。

调用 Message 或 this.$message 会返回当前 Message 的实例。 如果需要手动关闭实例，可以调用它的 close 方法。

**Examples:**

Example 1 (typescript):
```typescript
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" :plain="true" @click="open">
      Show message
    </el-button>
    <el-button class="!ml-0" :plain="true" @click="openVn">VNode</el-button>
  </div>
</template>

<script lang="ts" setup>
import { h } from 'vue'
import { ElMessage } from 'element-plus'

const open = () => {
  ElMessage('This is a message.')
}

const openVn = () => {
  ElMessage({
    message: h('p', { style: 'line-height: 1; font-size: 14px' }, [
      h('span', null, 'Message can be '),
      h('i', { style: 'color: teal' }, 'VNode'),
    ]),
  })
}
</script>
```

Example 2 (typescript):
```typescript
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" :plain="true" @click="open5">Primary</el-button>
    <el-button class="!ml-0" :plain="true" @click="open2">Success</el-button>
    <el-button class="!ml-0" :plain="true" @click="open3">Warning</el-button>
    <el-button class="!ml-0" :plain="true" @click="open1">Info</el-button>
    <el-button class="!ml-0" :plain="true" @click="open4">Error</el-button>
  </div>
</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus'

const open1 = () => {
  ElMessage('This is a info message.')
}
const open2 = () => {
  ElMessage({
    message: 'Congrats, this is a success message.',
    type: 'success',
  })
}
const open3 = () => {
  ElMessage({
    message: 'Warning, this is a warning message.',
    type: 'warning',
  })
}
const open4 = () => {
  ElMessage.error('Oops, this is a error message.')
}
const open5 = () => {
  ElMessage.primary('This is a primary message.')
}
</script>
```

Example 3 (typescript):
```typescript
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" :plain="true" @click="open5">Primary</el-button>
    <el-button class="!ml-0" :plain="true" @click="open1">Success</el-button>
    <el-button class="!ml-0" :plain="true" @click="open2">Warning</el-button>
    <el-button class="!ml-0" :plain="true" @click="open3">Info</el-button>
    <el-button class="!ml-0" :plain="true" @click="open4">Error</el-button>
  </div>
</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus'

const open1 = () => {
  ElMessage({
    message: 'Congrats, this is a success message.',
    type: 'success',
    plain: true,
  })
}
const open2 = () => {
  ElMessage({
    message: 'Warning, this is a warning message.',
    type: 'warning',
    plain: true,
  })
}
const open3 = () => {
  ElMessage({
    message: 'This is a info message.',
    type: 'info',
    plain: true,
  })
}
const open4 = () => {
  ElMessage({
    message: 'Oops, this is a error message.',
    type: 'error',
    plain: true,
  })
}
const open5 = () => {
  ElMessage({
    message: 'This is a primary message.',
    type: 'primary',
    plain: true,
  })
}
</script>
```

Example 4 (typescript):
```typescript
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" :plain="true" @click="open6">Primary</el-button>
    <el-button class="!ml-0" :plain="true" @click="open2">Success</el-button>
    <el-button class="!ml-0" :plain="true" @click="open3">Warning</el-button>
    <el-button class="!ml-0" :plain="true" @click="open1">Info</el-button>
    <el-button class="!ml-0" :plain="true" @click="open4">Error</el-button>
    <el-button class="!ml-0" :plain="true" @click="open5">
      Won't close automatically
    </el-button>
  </div>
</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus'

const open1 = () => {
  ElMessage({
    showClose: true,
    message: 'This is a info message.',
  })
}
const open2 = () => {
  ElMessage({
    showClose: true,
    message: 'Congrats, this is a success message.',
    type: 'success',
  })
}
const open3 = () => {
  ElMessage({
    showClose: true,
    message: 'Warning, this is a warning message.',
    type: 'warning',
  })
}
const open4 = () => {
  ElMessage({
    showClose: true,
    message: 'Oops, this is a error message.',
    type: 'error',
  })
}
const open5 = () => {
  ElMessage({
    showClose: true,
    message: 'Oops, this is a message that does not automatically close.',
    duration: 0,
  })
}
const open6 = () => {
  ElMessage({
    showClose: true,
    message: 'This is a primary message.',
    type: 'primary',
  })
}
</script>
```

---
