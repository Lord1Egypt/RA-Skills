---
name: "alert"
description: "Alert 提示 -- Element Plus Vue3 桌面端组件。Invoke when user needs Alert 提示 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/alert.html"
---

---

# Alert 提示 [​](#alert-提示)

更新日志待解决

0

用于页面中展示重要的提示信息。

## 基础用法 [​](#基础用法)

Alert 组件不属于浮层元素，不会自动消失或关闭。

Alert 组件提供5种类型，由 `type` 属性指定，默认值为 `info`。 `primary` 已被添加到2.9.11。

Primary alert

Success alert

Info alert

Warning alert

Error alert

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIlByaW1hcnkgYWxlcnRcIiB0eXBlPVwicHJpbWFyeVwiIC8+XG4gICAgPGVsLWFsZXJ0IHRpdGxlPVwiU3VjY2VzcyBhbGVydFwiIHR5cGU9XCJzdWNjZXNzXCIgLz5cbiAgICA8ZWwtYWxlcnQgdGl0bGU9XCJJbmZvIGFsZXJ0XCIgdHlwZT1cImluZm9cIiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIldhcm5pbmcgYWxlcnRcIiB0eXBlPVwid2FybmluZ1wiIC8+XG4gICAgPGVsLWFsZXJ0IHRpdGxlPVwiRXJyb3IgYWxlcnRcIiB0eXBlPVwiZXJyb3JcIiAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZWwtYWxlcnQge1xuICBtYXJnaW46IDIwcHggMCAwO1xufVxuLmVsLWFsZXJ0OmZpcnN0LWNoaWxkIHtcbiAgbWFyZ2luOiAwO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/alert/basic.vue)_

vue

```
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

隐藏源代码

## 主题 [​](#主题)

Alert 组件提供了两个不同的主题：`light` 和 `dark`。

通过设置 `effect` 属性来改变主题，默认为 `light`。

Primary alert

Success alert

Info alert

Warning alert

Error alert

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIlByaW1hcnkgYWxlcnRcIiB0eXBlPVwicHJpbWFyeVwiIGVmZmVjdD1cImRhcmtcIiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIlN1Y2Nlc3MgYWxlcnRcIiB0eXBlPVwic3VjY2Vzc1wiIGVmZmVjdD1cImRhcmtcIiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIkluZm8gYWxlcnRcIiB0eXBlPVwiaW5mb1wiIGVmZmVjdD1cImRhcmtcIiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIldhcm5pbmcgYWxlcnRcIiB0eXBlPVwid2FybmluZ1wiIGVmZmVjdD1cImRhcmtcIiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIkVycm9yIGFsZXJ0XCIgdHlwZT1cImVycm9yXCIgZWZmZWN0PVwiZGFya1wiIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlIHNjb3BlZD5cbi5lbC1hbGVydCB7XG4gIG1hcmdpbjogMjBweCAwIDA7XG59XG4uZWwtYWxlcnQ6Zmlyc3QtY2hpbGQge1xuICBtYXJnaW46IDA7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/alert/theme.vue)_

vue

```
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

隐藏源代码

## 自定义关闭按钮 [​](#自定义关闭按钮)

你可以自定义关闭按钮为文字或其他符号。

你可以设置 Alert 组件是否为可关闭状态， 关闭按钮的内容以及关闭时的回调函数同样可以定制。 `closable` 属性决定 Alert 组件是否可关闭， 该属性接受一个 `Boolean`，默认为 `false`。 你可以设置 `close-text` 属性来代替右侧的关闭图标， 需要注意的是 `close-text` 必须是一个字符串。 当 Alert 组件被关闭时会触发 `close` 事件。

Unclosable alert

Customized close text

Gotcha

Alert with callback

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIlVuY2xvc2FibGUgYWxlcnRcIiB0eXBlPVwic3VjY2Vzc1wiIDpjbG9zYWJsZT1cImZhbHNlXCIgLz5cbiAgICA8ZWwtYWxlcnQgdGl0bGU9XCJDdXN0b21pemVkIGNsb3NlIHRleHRcIiB0eXBlPVwiaW5mb1wiIGNsb3NlLXRleHQ9XCJHb3RjaGFcIiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIkFsZXJ0IHdpdGggY2FsbGJhY2tcIiB0eXBlPVwid2FybmluZ1wiIEBjbG9zZT1cImhlbGxvXCIgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuY29uc3QgaGVsbG8gPSAoKSA9PiB7XG4gIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBuby1hbGVydFxuICBhbGVydCgnSGVsbG8gV29ybGQhJylcbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmVsLWFsZXJ0IHtcbiAgbWFyZ2luOiAyMHB4IDAgMDtcbn1cbi5lbC1hbGVydDpmaXJzdC1jaGlsZCB7XG4gIG1hcmdpbjogMDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/alert/close-button.vue)_

vue

```
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

隐藏源代码

## 使用图标 [​](#使用图标)

你可以通过为 Alert 组件添加图标来提高可读性。

通过设置 `show-icon` 属性来显示 Alert 的 icon，这能更有效地向用户展示你的显示意图。 或者你可以使用 `icon` slot 自定义 icon 内容。

Primary alert

Success alert

Info alert

Warning alert

Error alert

Error alert with custom icon

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIlByaW1hcnkgYWxlcnRcIiB0eXBlPVwicHJpbWFyeVwiIHNob3ctaWNvbiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIlN1Y2Nlc3MgYWxlcnRcIiB0eXBlPVwic3VjY2Vzc1wiIHNob3ctaWNvbiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIkluZm8gYWxlcnRcIiB0eXBlPVwiaW5mb1wiIHNob3ctaWNvbiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIldhcm5pbmcgYWxlcnRcIiB0eXBlPVwid2FybmluZ1wiIHNob3ctaWNvbiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIkVycm9yIGFsZXJ0XCIgdHlwZT1cImVycm9yXCIgc2hvdy1pY29uIC8+XG4gICAgPGVsLWFsZXJ0IHRpdGxlPVwiRXJyb3IgYWxlcnQgd2l0aCBjdXN0b20gaWNvblwiIHR5cGU9XCJlcnJvclwiIHNob3ctaWNvbj5cbiAgICAgIDx0ZW1wbGF0ZSAjaWNvbj5cbiAgICAgICAgPEJlbGwgLz5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1hbGVydD5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgQmVsbCB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZWwtYWxlcnQge1xuICBtYXJnaW46IDIwcHggMCAwO1xufVxuLmVsLWFsZXJ0OmZpcnN0LWNoaWxkIHtcbiAgbWFyZ2luOiAwO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/alert/icon.vue)_

vue

```
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

隐藏源代码

## 文字居中 [​](#文字居中)

使用 `center` 属性来让文字水平居中。

Primary alert

Success alert

Info alert

Warning alert

Error alert

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIlByaW1hcnkgYWxlcnRcIiB0eXBlPVwicHJpbWFyeVwiIGNlbnRlciBzaG93LWljb24gLz5cbiAgICA8ZWwtYWxlcnQgdGl0bGU9XCJTdWNjZXNzIGFsZXJ0XCIgdHlwZT1cInN1Y2Nlc3NcIiBjZW50ZXIgc2hvdy1pY29uIC8+XG4gICAgPGVsLWFsZXJ0IHRpdGxlPVwiSW5mbyBhbGVydFwiIHR5cGU9XCJpbmZvXCIgY2VudGVyIHNob3ctaWNvbiAvPlxuICAgIDxlbC1hbGVydCB0aXRsZT1cIldhcm5pbmcgYWxlcnRcIiB0eXBlPVwid2FybmluZ1wiIGNlbnRlciBzaG93LWljb24gLz5cbiAgICA8ZWwtYWxlcnQgdGl0bGU9XCJFcnJvciBhbGVydFwiIHR5cGU9XCJlcnJvclwiIGNlbnRlciBzaG93LWljb24gLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c3R5bGUgc2NvcGVkPlxuLmVsLWFsZXJ0IHtcbiAgbWFyZ2luOiAyMHB4IDAgMDtcbn1cbi5lbC1hbGVydDpmaXJzdC1jaGlsZCB7XG4gIG1hcmdpbjogMDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/alert/center.vue)_

vue

```
<template>
  <div style="max-width: 600px">
    <el-alert title="Primary alert" type="primary" center show-icon />
    <el-alert title="Success alert" type="success" center show-icon />
    <el-alert title="Info alert" type="info" center show-icon />
    <el-alert title="Warning alert" type="warning" center show-icon />
    <el-alert title="Error alert" type="error" center show-icon />
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

隐藏源代码

## 文字描述 [​](#文字描述)

为 Alert 组件添加一个更加详细的描述来使用户了解更多信息。

除了必填的 `title` 属性外，你可以设置 `description` 属性来帮助你更好地介绍，我们称之为辅助性文字。 辅助性文字只能存放文本内容，当内容超出长度限制时会自动换行显示。

With description

This is a description.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiPlxuICAgIDxlbC1hbGVydFxuICAgICAgdGl0bGU9XCJXaXRoIGRlc2NyaXB0aW9uXCJcbiAgICAgIHR5cGU9XCJzdWNjZXNzXCJcbiAgICAgIGRlc2NyaXB0aW9uPVwiVGhpcyBpcyBhIGRlc2NyaXB0aW9uLlwiXG4gICAgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/alert/description.vue)_

vue

```
<template>
  <div style="max-width: 600px">
    <el-alert
      title="With description"
      type="success"
      description="This is a description."
    />
  </div>
</template>
```

隐藏源代码

## 带图标和描述 [​](#带图标和描述)

在最后, 这是一个带有图标和描述的例子。

Primary alert

More text description

Success alert

More text description

Info alert

More text description

Warning alert

More text description

Error alert

More text description

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiPlxuICAgIDxlbC1hbGVydFxuICAgICAgdGl0bGU9XCJQcmltYXJ5IGFsZXJ0XCJcbiAgICAgIHR5cGU9XCJwcmltYXJ5XCJcbiAgICAgIGRlc2NyaXB0aW9uPVwiTW9yZSB0ZXh0IGRlc2NyaXB0aW9uXCJcbiAgICAgIHNob3ctaWNvblxuICAgIC8+XG4gICAgPGVsLWFsZXJ0XG4gICAgICB0aXRsZT1cIlN1Y2Nlc3MgYWxlcnRcIlxuICAgICAgdHlwZT1cInN1Y2Nlc3NcIlxuICAgICAgZGVzY3JpcHRpb249XCJNb3JlIHRleHQgZGVzY3JpcHRpb25cIlxuICAgICAgc2hvdy1pY29uXG4gICAgLz5cbiAgICA8ZWwtYWxlcnRcbiAgICAgIHRpdGxlPVwiSW5mbyBhbGVydFwiXG4gICAgICB0eXBlPVwiaW5mb1wiXG4gICAgICBkZXNjcmlwdGlvbj1cIk1vcmUgdGV4dCBkZXNjcmlwdGlvblwiXG4gICAgICBzaG93LWljb25cbiAgICAvPlxuICAgIDxlbC1hbGVydFxuICAgICAgdGl0bGU9XCJXYXJuaW5nIGFsZXJ0XCJcbiAgICAgIHR5cGU9XCJ3YXJuaW5nXCJcbiAgICAgIGRlc2NyaXB0aW9uPVwiTW9yZSB0ZXh0IGRlc2NyaXB0aW9uXCJcbiAgICAgIHNob3ctaWNvblxuICAgIC8+XG4gICAgPGVsLWFsZXJ0XG4gICAgICB0aXRsZT1cIkVycm9yIGFsZXJ0XCJcbiAgICAgIHR5cGU9XCJlcnJvclwiXG4gICAgICBkZXNjcmlwdGlvbj1cIk1vcmUgdGV4dCBkZXNjcmlwdGlvblwiXG4gICAgICBzaG93LWljb25cbiAgICAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+PC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZWwtYWxlcnQge1xuICBtYXJnaW46IDIwcHggMCAwO1xufVxuLmVsLWFsZXJ0OmZpcnN0LWNoaWxkIHtcbiAgbWFyZ2luOiAwO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/alert/icon-description.vue)_

vue

```
<template>
  <div style="max-width: 600px">
    <el-alert
      title="Primary alert"
      type="primary"
      description="More text description"
      show-icon
    />
    <el-alert
      title="Success alert"
      type="success"
      description="More text description"
      show-icon
    />
    <el-alert
      title="Info alert"
      type="info"
      description="More text description"
      show-icon
    />
    <el-alert
      title="Warning alert"
      type="warning"
      description="More text description"
      show-icon
    />
    <el-alert
      title="Error alert"
      type="error"
      description="More text description"
      show-icon
    />
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.el-alert {
  margin: 20px 0 0;
}
.el-alert:first-child {
  margin: 0;
}
</style>
```

隐藏源代码

## Alert API [​](#alert-api)

### 属性 [​](#属性)

| 名称 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| title | Alert 标题。 | `string` | — |
| type | Alert 类型。 | `enum` | info |
| description | 描述性文本 | `string` | — |
| closable | 是否可以关闭 | `boolean` | true |
| center | 文字是否居中 | ::: | false |
| close-text | 自定义关闭按钮文本 | `string` | — |
| show-icon | 是否显示类型图标 | `boolean` | false |
| effect | 主题样式 | `enum` | light |

### Events [​](#events)

| 名称 | 描述 | 类型 |
| --- | --- | --- |
| close | 关闭 Alert 时触发的事件 | `Function` |

### Slots [​](#slots)

| 名称 | 描述 |
| --- | --- |
| default | Alert 内容描述 |
| title | 标题的内容 |
| icon 2.9.7 | icon 的内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/alert) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/alert.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/alert.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/8479810?v=4&size=64)](https://github.com/xinconan)[![](https://avatars.githubusercontent.com/u/21235555?v=4&size=64)](https://github.com/zhangenming)[![](https://avatars.githubusercontent.com/u/109908413?v=4&size=64)](https://github.com/sleepyShen1989)[![](https://avatars.githubusercontent.com/u/32354856?v=4&size=64)](https://github.com/baiwusanyu-c)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/20987775?v=4&size=64)](https://github.com/cbbfcd)[![](https://avatars.githubusercontent.com/u/134276765?v=4&size=64)](https://github.com/zwgwf)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/36007710?v=4&size=64)](https://github.com/sleepyfive)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)

[Tabs 标签页](https://element-plus.org/zh-CN/component/tabs)

[Dialog 对话框](https://element-plus.org/zh-CN/component/dialog)


