---
name: "notification"
description: "Notification 通知 -- Element Plus Vue3 桌面端组件。Invoke when user needs Notification 通知 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/notification.html"
---

---

# Notification 通知 [​](#notification-通知)

更新日志待解决

2

悬浮出现在页面角落，显示全局的通知提醒消息。

## 基础用法 [​](#基础用法)

Element Plus 注册了 `$notify` 方法并且它接受一个 Object 作为其参数。 在最简单的情况下，你可以通过设置 `title` 和 `message` 属性来设置通知的标题和正文内容。 默认情况下，通知在4500毫秒后自动关闭，但你可以通过设置 `duration` 属性来自定义通知的展示时间。 如果你将它设置为 `0`，那么通知将不会自动关闭。 需要注意的是 `duration` 接收一个 `Number`，单位为毫秒。

Closes automatically Won't close automatically

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuMVwiPlxuICAgICAgQ2xvc2VzIGF1dG9tYXRpY2FsbHlcbiAgICA8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuMlwiPlxuICAgICAgV29uJ3QgY2xvc2UgYXV0b21hdGljYWxseVxuICAgIDwvZWwtYnV0dG9uPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBoIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgRWxOb3RpZmljYXRpb24gfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IG9wZW4xID0gKCkgPT4ge1xuICBFbE5vdGlmaWNhdGlvbih7XG4gICAgdGl0bGU6ICdUaXRsZScsXG4gICAgbWVzc2FnZTogaCgnaScsIHsgc3R5bGU6ICdjb2xvcjogdGVhbCcgfSwgJ1RoaXMgaXMgYSByZW1pbmRlcicpLFxuICB9KVxufVxuXG5jb25zdCBvcGVuMiA9ICgpID0+IHtcbiAgRWxOb3RpZmljYXRpb24oe1xuICAgIHRpdGxlOiAnUHJvbXB0JyxcbiAgICBtZXNzYWdlOiAnVGhpcyBpcyBhIG1lc3NhZ2UgdGhhdCBkb2VzIG5vdCBhdXRvbWF0aWNhbGx5IGNsb3NlJyxcbiAgICBkdXJhdGlvbjogMCxcbiAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/notification/basic.vue)_

vue

```
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

隐藏源代码

## 不同类型的通知 [​](#不同类型的通知)

我们提供了四种不同类型的提醒框：success、warning、info 和error。

Element Plus 为 Notification 组件准备了5种通知类型：`primary`,`success`, `warning`, `info`, `error`。 他们可以设置 `type` 字段来修改，除上述的四个值之外的值会被忽略。 同时，我们也为 Notification 的各种 type 注册了单独的方法，可以在不传入 `type` 字段的情况下像 `open3` 和 `open4` 那样直接调用。 `primary` 已被添加到2.9.11。

PrimarySuccessWarningInfoError

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuNVwiPlByaW1hcnk8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuMVwiPlN1Y2Nlc3M8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuMlwiPldhcm5pbmc8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuM1wiPkluZm88L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuNFwiPkVycm9yPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEVsTm90aWZpY2F0aW9uIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuMSA9ICgpID0+IHtcbiAgRWxOb3RpZmljYXRpb24oe1xuICAgIHRpdGxlOiAnU3VjY2VzcycsXG4gICAgbWVzc2FnZTogJ1RoaXMgaXMgYSBzdWNjZXNzIG1lc3NhZ2UnLFxuICAgIHR5cGU6ICdzdWNjZXNzJyxcbiAgfSlcbn1cblxuY29uc3Qgb3BlbjIgPSAoKSA9PiB7XG4gIEVsTm90aWZpY2F0aW9uKHtcbiAgICB0aXRsZTogJ1dhcm5pbmcnLFxuICAgIG1lc3NhZ2U6ICdUaGlzIGlzIGEgd2FybmluZyBtZXNzYWdlJyxcbiAgICB0eXBlOiAnd2FybmluZycsXG4gIH0pXG59XG5cbmNvbnN0IG9wZW4zID0gKCkgPT4ge1xuICBFbE5vdGlmaWNhdGlvbih7XG4gICAgdGl0bGU6ICdJbmZvJyxcbiAgICBtZXNzYWdlOiAnVGhpcyBpcyBhbiBpbmZvIG1lc3NhZ2UnLFxuICAgIHR5cGU6ICdpbmZvJyxcbiAgfSlcbn1cblxuY29uc3Qgb3BlbjQgPSAoKSA9PiB7XG4gIEVsTm90aWZpY2F0aW9uKHtcbiAgICB0aXRsZTogJ0Vycm9yJyxcbiAgICBtZXNzYWdlOiAnVGhpcyBpcyBhbiBlcnJvciBtZXNzYWdlJyxcbiAgICB0eXBlOiAnZXJyb3InLFxuICB9KVxufVxuXG5jb25zdCBvcGVuNSA9ICgpID0+IHtcbiAgRWxOb3RpZmljYXRpb24oe1xuICAgIHRpdGxlOiAnUHJpbWFyeScsXG4gICAgbWVzc2FnZTogJ1RoaXMgaXMgYSBwcmltYXJ5IG1lc3NhZ2UnLFxuICAgIHR5cGU6ICdwcmltYXJ5JyxcbiAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/notification/different-types.vue)_

vue

```
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

隐藏源代码

## 自定义消息弹出的位置 [​](#自定义消息弹出的位置)

可以让 Notification 从屏幕四角中的任意一角弹出

使用 `position` 属性设置 Notification 的弹出位置， 支持四个选项：`top-right`、`top-left`、`bottom-right` 和 `bottom-left`， 默认为 `top-right`。

Top Right Bottom Right Bottom Left Top Left

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuMVwiPiBUb3AgUmlnaHQgPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgcGxhaW4gQGNsaWNrPVwib3BlbjJcIj4gQm90dG9tIFJpZ2h0IDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY2xhc3M9XCIhbWwtMFwiIHBsYWluIEBjbGljaz1cIm9wZW4zXCI+IEJvdHRvbSBMZWZ0IDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY2xhc3M9XCIhbWwtMFwiIHBsYWluIEBjbGljaz1cIm9wZW40XCI+IFRvcCBMZWZ0IDwvZWwtYnV0dG9uPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBFbE5vdGlmaWNhdGlvbiB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3Qgb3BlbjEgPSAoKSA9PiB7XG4gIEVsTm90aWZpY2F0aW9uKHtcbiAgICB0aXRsZTogJ0N1c3RvbSBQb3NpdGlvbicsXG4gICAgbWVzc2FnZTogXCJJJ20gYXQgdGhlIHRvcCByaWdodCBjb3JuZXJcIixcbiAgfSlcbn1cblxuY29uc3Qgb3BlbjIgPSAoKSA9PiB7XG4gIEVsTm90aWZpY2F0aW9uKHtcbiAgICB0aXRsZTogJ0N1c3RvbSBQb3NpdGlvbicsXG4gICAgbWVzc2FnZTogXCJJJ20gYXQgdGhlIGJvdHRvbSByaWdodCBjb3JuZXJcIixcbiAgICBwb3NpdGlvbjogJ2JvdHRvbS1yaWdodCcsXG4gIH0pXG59XG5cbmNvbnN0IG9wZW4zID0gKCkgPT4ge1xuICBFbE5vdGlmaWNhdGlvbih7XG4gICAgdGl0bGU6ICdDdXN0b20gUG9zaXRpb24nLFxuICAgIG1lc3NhZ2U6IFwiSSdtIGF0IHRoZSBib3R0b20gbGVmdCBjb3JuZXJcIixcbiAgICBwb3NpdGlvbjogJ2JvdHRvbS1sZWZ0JyxcbiAgfSlcbn1cblxuY29uc3Qgb3BlbjQgPSAoKSA9PiB7XG4gIEVsTm90aWZpY2F0aW9uKHtcbiAgICB0aXRsZTogJ0N1c3RvbSBQb3NpdGlvbicsXG4gICAgbWVzc2FnZTogXCJJJ20gYXQgdGhlIHRvcCBsZWZ0IGNvcm5lclwiLFxuICAgIHBvc2l0aW9uOiAndG9wLWxlZnQnLFxuICB9KVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/notification/positioning.vue)_

vue

```
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

隐藏源代码

## 有位置偏移的通知栏 [​](#有位置偏移的通知栏)

能够设置偏移量来使 Notification 偏移默认位置。

Notification 提供设置偏移量的功能，通过设置 `offset` 字段，可以使弹出的消息距屏幕边缘偏移一段距离。 注意在同一时刻，每一个的 Notification 实例应当具有一个相同的偏移量。

Notification with offset

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj4gTm90aWZpY2F0aW9uIHdpdGggb2Zmc2V0IDwvZWwtYnV0dG9uPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEVsTm90aWZpY2F0aW9uIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuID0gKCkgPT4ge1xuICBFbE5vdGlmaWNhdGlvbi5zdWNjZXNzKHtcbiAgICB0aXRsZTogJ1N1Y2Nlc3MnLFxuICAgIG1lc3NhZ2U6ICdUaGlzIGlzIGEgc3VjY2VzcyBtZXNzYWdlJyxcbiAgICBvZmZzZXQ6IDEwMCxcbiAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/notification/offsetting.vue)_

vue

```
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

隐藏源代码

## 使用 HTML 片段作为正文内容 [​](#使用-html-片段作为正文内容)

`message` 支持传入 HTML 字符串来作为正文内容。

将 `dangerouslyUseHTMLString` 属性设置为 true，`message` 属性就会被当作 HTML 片段处理。

Use HTML String

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj4gVXNlIEhUTUwgU3RyaW5nIDwvZWwtYnV0dG9uPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEVsTm90aWZpY2F0aW9uIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuID0gKCkgPT4ge1xuICBFbE5vdGlmaWNhdGlvbih7XG4gICAgdGl0bGU6ICdIVE1MIFN0cmluZycsXG4gICAgZGFuZ2Vyb3VzbHlVc2VIVE1MU3RyaW5nOiB0cnVlLFxuICAgIG1lc3NhZ2U6ICc8c3Ryb25nPlRoaXMgaXMgPGk+SFRNTDwvaT4gc3RyaW5nPC9zdHJvbmc+JyxcbiAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/notification/raw-html.vue)_

vue

```
<template>
  <el-button plain @click="open"> Use HTML String </el-button>
</template>

<script lang="ts" setup>
import { ElNotification } from 'element-plus'

const open = () => {
  ElNotification({
    title: 'HTML String',
    dangerouslyUseHTMLString: true,
    message: '<strong>This is <i>HTML</i> string</strong>',
  })
}
</script>
```

隐藏源代码

WARNING

`message` 属性虽然支持传入 HTML 片段，但是在网站上动态渲染任意 HTML 是非常危险的，因为容易导致 [XSS 攻击](https://en.wikipedia.org/wiki/Cross-site_scripting)。 因此在 `dangerouslyUseHTMLString` 打开的情况下，请确保 `message` 的内容是可信的，**永远不要**将用户提交的内容赋值给 `message` 属性。

## 函数形式的 message 2.9.0 [​](#函数形式的-message)

`message` 可以是 VNode。

在2.9.0之后， `message` 支持返回值为 VNode的函数。

Common VNodeDynamic props

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuXCI+Q29tbW9uIFZOb2RlPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgcGxhaW4gQGNsaWNrPVwib3BlbjFcIj5EeW5hbWljIHByb3BzPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGgsIHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsTm90aWZpY2F0aW9uLCBFbFN3aXRjaCB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3Qgb3BlbiA9ICgpID0+IHtcbiAgRWxOb3RpZmljYXRpb24oe1xuICAgIHRpdGxlOiAnVXNlIFZub2RlJyxcbiAgICBtZXNzYWdlOiBoKCdwJywgbnVsbCwgW1xuICAgICAgaCgnc3BhbicsIG51bGwsICdNZXNzYWdlIGNhbiBiZSAnKSxcbiAgICAgIGgoJ2knLCB7IHN0eWxlOiAnY29sb3I6IHRlYWwnIH0sICdWTm9kZScpLFxuICAgIF0pLFxuICB9KVxufVxuXG5jb25zdCBvcGVuMSA9ICgpID0+IHtcbiAgY29uc3QgY2hlY2tlZCA9IHJlZjxib29sZWFuIHwgc3RyaW5nIHwgbnVtYmVyPihmYWxzZSlcbiAgRWxOb3RpZmljYXRpb24oe1xuICAgIHRpdGxlOiAnVXNlIFZub2RlJyxcbiAgICAvLyBTaG91bGQgcGFzcyBhIGZ1bmN0aW9uIGlmIFZOb2RlIGNvbnRhaW5zIGR5bmFtaWMgcHJvcHNcbiAgICBtZXNzYWdlOiAoKSA9PlxuICAgICAgaChFbFN3aXRjaCwge1xuICAgICAgICBtb2RlbFZhbHVlOiBjaGVja2VkLnZhbHVlLFxuICAgICAgICAnb25VcGRhdGU6bW9kZWxWYWx1ZSc6ICh2YWw6IGJvb2xlYW4gfCBzdHJpbmcgfCBudW1iZXIpID0+IHtcbiAgICAgICAgICBjaGVja2VkLnZhbHVlID0gdmFsXG4gICAgICAgIH0sXG4gICAgICB9KSxcbiAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/notification/use-vnode.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" plain @click="open">Common VNode</el-button>
    <el-button class="!ml-0" plain @click="open1">Dynamic props</el-button>
  </div>
</template>

<script lang="ts" setup>
import { h, ref } from 'vue'
import { ElNotification, ElSwitch } from 'element-plus'

const open = () => {
  ElNotification({
    title: 'Use Vnode',
    message: h('p', null, [
      h('span', null, 'Message can be '),
      h('i', { style: 'color: teal' }, 'VNode'),
    ]),
  })
}

const open1 = () => {
  const checked = ref<boolean | string | number>(false)
  ElNotification({
    title: 'Use Vnode',
    // Should pass a function if VNode contains dynamic props
    message: () =>
      h(ElSwitch, {
        modelValue: checked.value,
        'onUpdate:modelValue': (val: boolean | string | number) => {
          checked.value = val
        },
      }),
  })
}
</script>
```

隐藏源代码

## 隐藏关闭按钮 [​](#隐藏关闭按钮)

通知的关闭按钮可以被设置为隐藏。

将 `showClose` 属性设置为 `false` 即可隐藏关闭按钮。

Hide close button

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj4gSGlkZSBjbG9zZSBidXR0b24gPC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxOb3RpZmljYXRpb24gfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IG9wZW4gPSAoKSA9PiB7XG4gIEVsTm90aWZpY2F0aW9uLnN1Y2Nlc3Moe1xuICAgIHRpdGxlOiAnSW5mbycsXG4gICAgbWVzc2FnZTogJ1RoaXMgaXMgYSBtZXNzYWdlIHdpdGhvdXQgY2xvc2UgYnV0dG9uJyxcbiAgICBzaG93Q2xvc2U6IGZhbHNlLFxuICB9KVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/notification/no-close.vue)_

vue

```
<template>
  <el-button plain @click="open"> Hide close button </el-button>
</template>

<script lang="ts" setup>
import { ElNotification } from 'element-plus'

const open = () => {
  ElNotification.success({
    title: 'Info',
    message: 'This is a message without close button',
    showClose: false,
  })
}
</script>
```

隐藏源代码

## 全局方法 [​](#全局方法)

Element Plus 为 `app.config.globalProperties` 添加了全局方法 `$notify`。 因此在 Vue instance 中可以采用本页面中的方式调用 `Notification`。

## 单独引用 [​](#单独引用)

javascript

```
import { ElNotification } from 'element-plus'
import { CloseBold } from '@element-plus/icons-vue'

ElNotification({
  title: 'Title',
  message: 'This is a message',
  closeIcon: CloseBold,
})
```

你可以在对应的处理函数内调用 `ElNotification(options)` 来呼出通知栏。 我们也提前定义了多个 type 的单独调用方法，如 `ElNotification.success(options)`。 当你需要关闭页面上所有的通知栏的时候，可以调用 `ElNotification.closeAll()` 来关闭所有的实例。 在 2.10.5 版本中，你可以通过调用 `ElNotification.updateOffsets(position)` 手动更新所有通知实例在特定方向上的偏移量。

## 应用程序上下文继承 \> 2.0.4 [​](#应用程序上下文继承-2-0-4)

现在 Notification 接受一条 `context` 作为消息构造器的第二个参数，允许你将当前应用的上下文注入到 Notification 中，这将允许你继承应用程序的所有属性。

你可以像这样使用它：

TIP

如果您全局注册了 ElNotification 组件，它将自动继承应用的上下文环境。

ts

```
import { getCurrentInstance } from 'vue'
import { ElNotification } from 'element-plus'

// 在你的 setup 方法中
const { appContext } = getCurrentInstance()!
ElNotification({}, appContext)
```

## API [​](#api)

### 配置项 [​](#配置项)

| 名称 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| title | title | `string` | '' |
| message | 通知栏正文内容 | `string` / `VNode` / `Function` | '' |
| dangerouslyUseHTMLString | 是否将 message 属性作为 HTML 片段处理 | `boolean` | false |
| type | 通知的类型 | `enum` | '' |
| icon | 自定义图标。 若设置了 `type`，则 `icon` 会被覆盖 | `string` / `Component` | — |
| customClass | 自定义类名 | `string` | '' |
| duration | 显示时间, 单位为毫秒。 值为 0 则不会自动关闭 | `number` | 4500 |
| position | 自定义弹出位置 | `enum` | top-right |
| showClose | 是否显示关闭按钮 | `boolean` | true |
| onClose | 关闭时的回调函数 | `Function` | — |
| onClick | 点击 Notification 时的回调函数 | `Function` | — |
| offset | 相对屏幕顶部的偏移量 偏移的距离，在同一时刻，所有的 Notification 实例应当具有一个相同的偏移量 | `number` | 0 |
| appendTo | 设置 notification 的根元素，默认为 `document.body` | `CSSSelector` / `HTMLElement` | — |
| zIndex | 初始 zIndex | `number` | 0 |
| closeIcon 2.9.8 | 自定义关闭图标 | `string` / `Component` | Close |

### 方法 [​](#方法)

`Notification` 和 `this.$notify` 都返回当前的 Notification 实例。 如果需要手动关闭实例，可以调用它的 `close` 方法。

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| close | 关闭当前的 Notification | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/notification) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/notification.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/notification.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/14144811?v=4&size=64)](https://github.com/cn-xufei)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/132551120?v=4&size=64)](https://github.com/YiMo1)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/31533594?v=4&size=64)](https://github.com/Gnalvin)[![](https://avatars.githubusercontent.com/u/10301686?v=4&size=64)](https://github.com/acfinity)[![](https://avatars.githubusercontent.com/u/169252980?v=4&size=64)](https://github.com/xiaochenchen-igg-com)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/49446662?v=4&size=64)](https://github.com/codespikey)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/15535177?v=4&size=64)](https://github.com/liuzi6612)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/32129111?v=4&size=64)](https://github.com/Vgbire)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/57524062?v=4&size=64)](https://github.com/Ther-su)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)

[Message Box 消息弹出框](https://element-plus.org/zh-CN/component/message-box)

[Popconfirm 气泡确认框](https://element-plus.org/zh-CN/component/popconfirm)


