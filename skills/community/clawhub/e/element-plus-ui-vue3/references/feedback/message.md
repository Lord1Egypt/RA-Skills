---
name: "message"
description: "Message 消息提示 -- Element Plus Vue3 桌面端组件。Invoke when user needs Message 消息提示 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/message.html"
---

---

# Message 消息提示 [​](#message-消息提示)

更新日志待解决

21

常用于主动操作后的反馈提示。 与 Notification 的区别是后者更多用于系统级通知的被动提醒。

## 基础用法 [​](#基础用法)

默认情况下在顶部显示并在 3 秒后消失。 您可以使用 `placement` 属性控制位置。

Message 在配置上与 Notification 非常类似，所以部分 options 在此不做详尽解释。 文末有 options 列表，可以结合 Notification 的文档理解它们。 Element Plus 注册了一个全局的 `$message`方法用于调用。 Message 可以接收一个字符串或一个 VNode 作为参数，它会被显示为正文内容。

Show message VNode

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3BlblwiPlxuICAgICAgU2hvdyBtZXNzYWdlXG4gICAgPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgOnBsYWluPVwidHJ1ZVwiIEBjbGljaz1cIm9wZW5WblwiPlZOb2RlPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGggfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBFbE1lc3NhZ2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IG9wZW4gPSAoKSA9PiB7XG4gIEVsTWVzc2FnZSgnVGhpcyBpcyBhIG1lc3NhZ2UuJylcbn1cblxuY29uc3Qgb3BlblZuID0gKCkgPT4ge1xuICBFbE1lc3NhZ2Uoe1xuICAgIG1lc3NhZ2U6IGgoJ3AnLCB7IHN0eWxlOiAnbGluZS1oZWlnaHQ6IDE7IGZvbnQtc2l6ZTogMTRweCcgfSwgW1xuICAgICAgaCgnc3BhbicsIG51bGwsICdNZXNzYWdlIGNhbiBiZSAnKSxcbiAgICAgIGgoJ2knLCB7IHN0eWxlOiAnY29sb3I6IHRlYWwnIH0sICdWTm9kZScpLFxuICAgIF0pLFxuICB9KVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message/basic.vue)_

vue

```
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

隐藏源代码

## 不同状态 [​](#不同状态)

用来显示「成功、警告、消息、错误」类的操作反馈。

当需要自定义更多属性时，Message 也可以接收一个对象为参数。 比如，设置 `type` 字段可以定义不同的状态，默认为`info`。 此时正文内容以 `message` 的值传入。 同时，我们也为 Message 的各种 type 注册了方法，可以在不传入 type 字段的情况下像 `open4` 那样直接调用。 `primary` 已被添加到2.9.11。

PrimarySuccessWarningInfoError

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3BlbjVcIj5QcmltYXJ5PC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgOnBsYWluPVwidHJ1ZVwiIEBjbGljaz1cIm9wZW4yXCI+U3VjY2VzczwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY2xhc3M9XCIhbWwtMFwiIDpwbGFpbj1cInRydWVcIiBAY2xpY2s9XCJvcGVuM1wiPldhcm5pbmc8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3BlbjFcIj5JbmZvPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgOnBsYWluPVwidHJ1ZVwiIEBjbGljaz1cIm9wZW40XCI+RXJyb3I8L2VsLWJ1dHRvbj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxNZXNzYWdlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuMSA9ICgpID0+IHtcbiAgRWxNZXNzYWdlKCdUaGlzIGlzIGEgaW5mbyBtZXNzYWdlLicpXG59XG5jb25zdCBvcGVuMiA9ICgpID0+IHtcbiAgRWxNZXNzYWdlKHtcbiAgICBtZXNzYWdlOiAnQ29uZ3JhdHMsIHRoaXMgaXMgYSBzdWNjZXNzIG1lc3NhZ2UuJyxcbiAgICB0eXBlOiAnc3VjY2VzcycsXG4gIH0pXG59XG5jb25zdCBvcGVuMyA9ICgpID0+IHtcbiAgRWxNZXNzYWdlKHtcbiAgICBtZXNzYWdlOiAnV2FybmluZywgdGhpcyBpcyBhIHdhcm5pbmcgbWVzc2FnZS4nLFxuICAgIHR5cGU6ICd3YXJuaW5nJyxcbiAgfSlcbn1cbmNvbnN0IG9wZW40ID0gKCkgPT4ge1xuICBFbE1lc3NhZ2UuZXJyb3IoJ09vcHMsIHRoaXMgaXMgYSBlcnJvciBtZXNzYWdlLicpXG59XG5jb25zdCBvcGVuNSA9ICgpID0+IHtcbiAgRWxNZXNzYWdlLnByaW1hcnkoJ1RoaXMgaXMgYSBwcmltYXJ5IG1lc3NhZ2UuJylcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message/different-types.vue)_

vue

```
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

隐藏源代码

## Plain 2.6.3 [​](#plain)

设置 `plain` 为 plain 背景。

PrimarySuccessWarningInfoError

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3BlbjVcIj5QcmltYXJ5PC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgOnBsYWluPVwidHJ1ZVwiIEBjbGljaz1cIm9wZW4xXCI+U3VjY2VzczwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY2xhc3M9XCIhbWwtMFwiIDpwbGFpbj1cInRydWVcIiBAY2xpY2s9XCJvcGVuMlwiPldhcm5pbmc8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3BlbjNcIj5JbmZvPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgOnBsYWluPVwidHJ1ZVwiIEBjbGljaz1cIm9wZW40XCI+RXJyb3I8L2VsLWJ1dHRvbj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxNZXNzYWdlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuMSA9ICgpID0+IHtcbiAgRWxNZXNzYWdlKHtcbiAgICBtZXNzYWdlOiAnQ29uZ3JhdHMsIHRoaXMgaXMgYSBzdWNjZXNzIG1lc3NhZ2UuJyxcbiAgICB0eXBlOiAnc3VjY2VzcycsXG4gICAgcGxhaW46IHRydWUsXG4gIH0pXG59XG5jb25zdCBvcGVuMiA9ICgpID0+IHtcbiAgRWxNZXNzYWdlKHtcbiAgICBtZXNzYWdlOiAnV2FybmluZywgdGhpcyBpcyBhIHdhcm5pbmcgbWVzc2FnZS4nLFxuICAgIHR5cGU6ICd3YXJuaW5nJyxcbiAgICBwbGFpbjogdHJ1ZSxcbiAgfSlcbn1cbmNvbnN0IG9wZW4zID0gKCkgPT4ge1xuICBFbE1lc3NhZ2Uoe1xuICAgIG1lc3NhZ2U6ICdUaGlzIGlzIGEgaW5mbyBtZXNzYWdlLicsXG4gICAgdHlwZTogJ2luZm8nLFxuICAgIHBsYWluOiB0cnVlLFxuICB9KVxufVxuY29uc3Qgb3BlbjQgPSAoKSA9PiB7XG4gIEVsTWVzc2FnZSh7XG4gICAgbWVzc2FnZTogJ09vcHMsIHRoaXMgaXMgYSBlcnJvciBtZXNzYWdlLicsXG4gICAgdHlwZTogJ2Vycm9yJyxcbiAgICBwbGFpbjogdHJ1ZSxcbiAgfSlcbn1cbmNvbnN0IG9wZW41ID0gKCkgPT4ge1xuICBFbE1lc3NhZ2Uoe1xuICAgIG1lc3NhZ2U6ICdUaGlzIGlzIGEgcHJpbWFyeSBtZXNzYWdlLicsXG4gICAgdHlwZTogJ3ByaW1hcnknLFxuICAgIHBsYWluOiB0cnVlLFxuICB9KVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message/plain.vue)_

vue

```
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

隐藏源代码

## 可关闭的消息提示 [​](#可关闭的消息提示)

可以添加关闭按钮。

默认的 Message 是不可以被人工关闭的。 如果你需要手动关闭功能，你可以把 `showClose` 设置为 true 此外，和 Notification 一样，Message 拥有可控的 `duration`， 默认的关闭时间为 3000 毫秒，当把这个属性的值设置为`0`便表示该消息不会被自动关闭。

PrimarySuccessWarningInfoError Won't close automatically

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3BlbjZcIj5QcmltYXJ5PC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgOnBsYWluPVwidHJ1ZVwiIEBjbGljaz1cIm9wZW4yXCI+U3VjY2VzczwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY2xhc3M9XCIhbWwtMFwiIDpwbGFpbj1cInRydWVcIiBAY2xpY2s9XCJvcGVuM1wiPldhcm5pbmc8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3BlbjFcIj5JbmZvPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgOnBsYWluPVwidHJ1ZVwiIEBjbGljaz1cIm9wZW40XCI+RXJyb3I8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3BlbjVcIj5cbiAgICAgIFdvbid0IGNsb3NlIGF1dG9tYXRpY2FsbHlcbiAgICA8L2VsLWJ1dHRvbj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxNZXNzYWdlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuMSA9ICgpID0+IHtcbiAgRWxNZXNzYWdlKHtcbiAgICBzaG93Q2xvc2U6IHRydWUsXG4gICAgbWVzc2FnZTogJ1RoaXMgaXMgYSBpbmZvIG1lc3NhZ2UuJyxcbiAgfSlcbn1cbmNvbnN0IG9wZW4yID0gKCkgPT4ge1xuICBFbE1lc3NhZ2Uoe1xuICAgIHNob3dDbG9zZTogdHJ1ZSxcbiAgICBtZXNzYWdlOiAnQ29uZ3JhdHMsIHRoaXMgaXMgYSBzdWNjZXNzIG1lc3NhZ2UuJyxcbiAgICB0eXBlOiAnc3VjY2VzcycsXG4gIH0pXG59XG5jb25zdCBvcGVuMyA9ICgpID0+IHtcbiAgRWxNZXNzYWdlKHtcbiAgICBzaG93Q2xvc2U6IHRydWUsXG4gICAgbWVzc2FnZTogJ1dhcm5pbmcsIHRoaXMgaXMgYSB3YXJuaW5nIG1lc3NhZ2UuJyxcbiAgICB0eXBlOiAnd2FybmluZycsXG4gIH0pXG59XG5jb25zdCBvcGVuNCA9ICgpID0+IHtcbiAgRWxNZXNzYWdlKHtcbiAgICBzaG93Q2xvc2U6IHRydWUsXG4gICAgbWVzc2FnZTogJ09vcHMsIHRoaXMgaXMgYSBlcnJvciBtZXNzYWdlLicsXG4gICAgdHlwZTogJ2Vycm9yJyxcbiAgfSlcbn1cbmNvbnN0IG9wZW41ID0gKCkgPT4ge1xuICBFbE1lc3NhZ2Uoe1xuICAgIHNob3dDbG9zZTogdHJ1ZSxcbiAgICBtZXNzYWdlOiAnT29wcywgdGhpcyBpcyBhIG1lc3NhZ2UgdGhhdCBkb2VzIG5vdCBhdXRvbWF0aWNhbGx5IGNsb3NlLicsXG4gICAgZHVyYXRpb246IDAsXG4gIH0pXG59XG5jb25zdCBvcGVuNiA9ICgpID0+IHtcbiAgRWxNZXNzYWdlKHtcbiAgICBzaG93Q2xvc2U6IHRydWUsXG4gICAgbWVzc2FnZTogJ1RoaXMgaXMgYSBwcmltYXJ5IG1lc3NhZ2UuJyxcbiAgICB0eXBlOiAncHJpbWFyeScsXG4gIH0pXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message/closable.vue)_

vue

```
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

隐藏源代码

## 使用 HTML 片段作为正文内容 [​](#使用-html-片段作为正文内容)

`message` 还支持使用 HTML 字符串作为正文内容。

将`dangerouslyUseHTMLString`属性设置为 true,`message` 就会被当作 HTML 片段处理。

Use HTML string

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIDpwbGFpbj1cInRydWVcIiBAY2xpY2s9XCJvcGVuSFRNTFwiPlVzZSBIVE1MIHN0cmluZzwvZWwtYnV0dG9uPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEVsTWVzc2FnZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3Qgb3BlbkhUTUwgPSAoKSA9PiB7XG4gIEVsTWVzc2FnZSh7XG4gICAgZGFuZ2Vyb3VzbHlVc2VIVE1MU3RyaW5nOiB0cnVlLFxuICAgIG1lc3NhZ2U6ICc8c3Ryb25nPlRoaXMgaXMgPGk+SFRNTDwvaT4gc3RyaW5nPC9zdHJvbmc+JyxcbiAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message/raw-html.vue)_

vue

```
<template>
  <el-button :plain="true" @click="openHTML">Use HTML string</el-button>
</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus'

const openHTML = () => {
  ElMessage({
    dangerouslyUseHTMLString: true,
    message: '<strong>This is <i>HTML</i> string</strong>',
  })
}
</script>
```

隐藏源代码

WARNING

`message` 属性虽然支持传入 HTML 片段，但是在网站上动态渲染任意 HTML 是非常危险的，因为容易导致 [XSS 攻击](https://en.wikipedia.org/wiki/Cross-site_scripting)。 因此在 `dangerouslyUseHTMLString` 打开的情况下，请确保 `message` 的内容是可信的，**永远不要**将用户提交的内容赋值给 `message` 属性。

## 分组消息合并 [​](#分组消息合并)

合并相同内容的消息。

设置 `grouping` 为 true，内容相同的 `message` 将被合并。

Show message

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIDpwbGFpbj1cInRydWVcIiBAY2xpY2s9XCJvcGVuXCI+U2hvdyBtZXNzYWdlPC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxNZXNzYWdlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuID0gKCkgPT4ge1xuICBFbE1lc3NhZ2Uoe1xuICAgIG1lc3NhZ2U6ICdUaGlzIGlzIGEgbWVzc2FnZS4nLFxuICAgIGdyb3VwaW5nOiB0cnVlLFxuICAgIHR5cGU6ICdzdWNjZXNzJyxcbiAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message/grouping.vue)_

vue

```
<template>
  <el-button :plain="true" @click="open">Show message</el-button>
</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus'

const open = () => {
  ElMessage({
    message: 'This is a message.',
    grouping: true,
    type: 'success',
  })
}
</script>
```

隐藏源代码

## Placement 2.11.0 [​](#placement)

控制消息出现的位置。 消息可以显示在查看端口的顶部(默认) 或其他位置。

Top Top Left Top Right Bottom Bottom Left Bottom Right

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3Blbk1zZygpXCI+IFRvcCA8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3Blbk1zZygndG9wLWxlZnQnKVwiPlxuICAgICAgVG9wIExlZnRcbiAgICA8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiA6cGxhaW49XCJ0cnVlXCIgQGNsaWNrPVwib3Blbk1zZygndG9wLXJpZ2h0JylcIj5cbiAgICAgIFRvcCBSaWdodFxuICAgIDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY2xhc3M9XCIhbWwtMFwiIDpwbGFpbj1cInRydWVcIiBAY2xpY2s9XCJvcGVuTXNnKCdib3R0b20nKVwiPlxuICAgICAgQm90dG9tXG4gICAgPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgOnBsYWluPVwidHJ1ZVwiIEBjbGljaz1cIm9wZW5Nc2coJ2JvdHRvbS1sZWZ0JylcIj5cbiAgICAgIEJvdHRvbSBMZWZ0XG4gICAgPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgOnBsYWluPVwidHJ1ZVwiIEBjbGljaz1cIm9wZW5Nc2coJ2JvdHRvbS1yaWdodCcpXCI+XG4gICAgICBCb3R0b20gUmlnaHRcbiAgICA8L2VsLWJ1dHRvbj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxNZXNzYWdlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbXBvcnQgdHlwZSB7IE1lc3NhZ2VQbGFjZW1lbnQsIE1lc3NhZ2VUeXBlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5sZXQgdG9wQ291bnQgPSAwXG5sZXQgYm90dG9tQ291bnQgPSAwXG5sZXQgdG9wTGVmdENvdW50ID0gMFxubGV0IHRvcFJpZ2h0Q291bnQgPSAwXG5sZXQgYm90dG9tTGVmdENvdW50ID0gMFxubGV0IGJvdHRvbVJpZ2h0Q291bnQgPSAwXG5cbmNvbnN0IG9wZW5Nc2cgPSAocGxhY2VtZW50OiBNZXNzYWdlUGxhY2VtZW50ID0gJ3RvcCcpID0+IHtcbiAgbGV0IGNvdW50ID0gMFxuICBsZXQgdHlwZTogTWVzc2FnZVR5cGUgPSAnc3VjY2VzcydcblxuICBzd2l0Y2ggKHBsYWNlbWVudCkge1xuICAgIGNhc2UgJ3RvcCc6XG4gICAgICBjb3VudCA9ICsrdG9wQ291bnRcbiAgICAgIHR5cGUgPSAnc3VjY2VzcydcbiAgICAgIGJyZWFrXG4gICAgY2FzZSAnYm90dG9tJzpcbiAgICAgIGNvdW50ID0gKytib3R0b21Db3VudFxuICAgICAgdHlwZSA9ICd3YXJuaW5nJ1xuICAgICAgYnJlYWtcbiAgICBjYXNlICd0b3AtbGVmdCc6XG4gICAgICBjb3VudCA9ICsrdG9wTGVmdENvdW50XG4gICAgICB0eXBlID0gJ2luZm8nXG4gICAgICBicmVha1xuICAgIGNhc2UgJ3RvcC1yaWdodCc6XG4gICAgICBjb3VudCA9ICsrdG9wUmlnaHRDb3VudFxuICAgICAgdHlwZSA9ICdwcmltYXJ5J1xuICAgICAgYnJlYWtcbiAgICBjYXNlICdib3R0b20tbGVmdCc6XG4gICAgICBjb3VudCA9ICsrYm90dG9tTGVmdENvdW50XG4gICAgICB0eXBlID0gJ3dhcm5pbmcnXG4gICAgICBicmVha1xuICAgIGNhc2UgJ2JvdHRvbS1yaWdodCc6XG4gICAgICBjb3VudCA9ICsrYm90dG9tUmlnaHRDb3VudFxuICAgICAgdHlwZSA9ICdlcnJvcidcbiAgICAgIGJyZWFrXG4gIH1cblxuICBFbE1lc3NhZ2Uoe1xuICAgIG1lc3NhZ2U6IGBUaGlzIGlzIGEgbWVzc2FnZSBmcm9tIHRoZSAke3BsYWNlbWVudH0gJHtjb3VudH1gLFxuICAgIHR5cGUsXG4gICAgcGxhY2VtZW50LFxuICB9KVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message/placement.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" :plain="true" @click="openMsg()"> Top </el-button>
    <el-button class="!ml-0" :plain="true" @click="openMsg('top-left')">
      Top Left
    </el-button>
    <el-button class="!ml-0" :plain="true" @click="openMsg('top-right')">
      Top Right
    </el-button>
    <el-button class="!ml-0" :plain="true" @click="openMsg('bottom')">
      Bottom
    </el-button>
    <el-button class="!ml-0" :plain="true" @click="openMsg('bottom-left')">
      Bottom Left
    </el-button>
    <el-button class="!ml-0" :plain="true" @click="openMsg('bottom-right')">
      Bottom Right
    </el-button>
  </div>
</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus'

import type { MessagePlacement, MessageType } from 'element-plus'

let topCount = 0
let bottomCount = 0
let topLeftCount = 0
let topRightCount = 0
let bottomLeftCount = 0
let bottomRightCount = 0

const openMsg = (placement: MessagePlacement = 'top') => {
  let count = 0
  let type: MessageType = 'success'

  switch (placement) {
    case 'top':
      count = ++topCount
      type = 'success'
      break
    case 'bottom':
      count = ++bottomCount
      type = 'warning'
      break
    case 'top-left':
      count = ++topLeftCount
      type = 'info'
      break
    case 'top-right':
      count = ++topRightCount
      type = 'primary'
      break
    case 'bottom-left':
      count = ++bottomLeftCount
      type = 'warning'
      break
    case 'bottom-right':
      count = ++bottomRightCount
      type = 'error'
      break
  }

  ElMessage({
    message: `This is a message from the ${placement} ${count}`,
    type,
    placement,
  })
}
</script>
```

隐藏源代码

## 全局方法 [​](#全局方法)

Element Plus 为 `app.config.globalProperties` 添加了全局方法 `$message`。 因此在 vue 实例中你可以使用当前页面中的调用方式调用 `Message`

## 单独引用 [​](#单独引用)

ts

```
import { ElMessage } from 'element-plus'
```

此时调用方法为 `ElMessage(options)`。 我们也为每个 type 定义了各自的方法，如 `ElMessage.success(options)`。 并且可以调用 `ElMessage.closeAll()` 手动关闭所有实例。

## 应用程序上下文继承 2.0.3 [​](#应用程序上下文继承)

现在 Message 接受一条 `context` 作为消息构造器的第二个参数，允许你将当前应用的上下文注入到 Message 中，这将允许你继承应用程序的所有属性。

你可以像这样使用它：

TIP

如果您全局注册了 ElMessage 组件，它将自动继承应用的上下文环境。

ts

```
import { getCurrentInstance } from 'vue'
import { ElMessage } from 'element-plus'

// 在你的 setup 方法中
const { appContext } = getCurrentInstance()!
ElMessage({}, appContext)
```

## API [​](#api)

### Message 配置项 [​](#message-配置项)

| 名称 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| message | 消息文字 | `string` / `VNode` / `Function` | '' |
| type | 消息类型 | `enum` | info |
| plain 2.6.3 | 是否纯色 | `boolean` | false |
| icon | 自定义图标，该属性会覆盖 `type` 的图标。 | `string` / `Component` | — |
| dangerouslyUseHTMLString | 是否将 message 属性作为 HTML 片段处理 | `boolean` | false |
| customClass | 自定义类名 | `string` | '' |
| duration | 显示时间，单位为毫秒。 设为 0 则不会自动关闭 | `number` | 3000 |
| showClose | 是否显示关闭按钮 | `boolean` | false |
| onClose | 关闭时的回调函数, 参数为被关闭的 message 实例 | `Function` | — |
| offset | 设置到视口边缘的距离（当位置为'top'时为顶部，当位置为'bottom'时为底部） | `number` | 16 |
| placement 2.11.0 | 消息放置位置 | `enum` | top |
| appendTo | 设置 message 的根元素，默认为 `document.body` | `CSSSelector` / `HTMLElement` | — |
| grouping | 合并内容相同的消息，不支持 VNode 类型的消息 | `boolean` | false |
| repeatNum | 重复次数，类似于 Badge 。当和 `grouping` 属性一起使用时作为初始数量使用 | `number` | 1 |

### Message 方法 [​](#message-方法)

调用 `Message` 或 `this.$message` 会返回当前 Message 的实例。 如果需要手动关闭实例，可以调用它的 `close` 方法。

| 名称 | 描述 | 类型 |
| --- | --- | --- |
| close | 关闭当前的 Message | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/message) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/message.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/message.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/47303530?v=4&size=64)](https://github.com/romankaravia)[![](https://avatars.githubusercontent.com/u/71749650?v=4&size=64)](https://github.com/qeTM)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/137589237?v=4&size=64)](https://github.com/zero-years)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/132551120?v=4&size=64)](https://github.com/YiMo1)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/35138018?v=4&size=64)](https://github.com/tuskermanshu)[![](https://avatars.githubusercontent.com/u/49558643?v=4&size=64)](https://github.com/jumtp)[![](https://avatars.githubusercontent.com/u/47104575?v=4&size=64)](https://github.com/linxianxi)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/48512251?v=4&size=64)](https://github.com/lete114)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/31462942?v=4&size=64)](https://github.com/zhazhanitian)[![](https://avatars.githubusercontent.com/u/49446662?v=4&size=64)](https://github.com/codespikey)[![](https://avatars.githubusercontent.com/u/5445667?v=4&size=64)](https://github.com/iceshou)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/134276765?v=4&size=64)](https://github.com/zwgwf)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/191817983?v=4&size=64)](https://github.com/zhuft-moon)[![](https://avatars.githubusercontent.com/u/38075730?v=4&size=64)](https://github.com/c0dedance)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)

[Loading 加载](https://element-plus.org/zh-CN/component/loading)

[Message Box 消息弹出框](https://element-plus.org/zh-CN/component/message-box)


