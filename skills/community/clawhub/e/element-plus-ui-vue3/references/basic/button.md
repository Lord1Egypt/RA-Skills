---
name: "button"
description: "Button 按钮 -- Element Plus Vue3 桌面端组件。Invoke when user needs Button 按钮 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/button.html"
---

---

# Button 按钮 [​](#button-按钮)

更新日志待解决

18

常用的操作按钮。

## 基础用法 [​](#基础用法)

使用 `type`, `plain`, `round`, `dashed` 和 `circle` 来定义按钮的样式。

DefaultPrimarySuccessInfoWarningDanger

PlainPrimarySuccessInfoWarningDanger

RoundPrimarySuccessInfoWarningDanger

DashedPrimarySuccessInfoWarningDanger

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiYnV0dG9uLWV4YW1wbGVcIj5cbiAgICA8ZGl2IGNsYXNzPVwiYnV0dG9uLXJvd1wiPlxuICAgICAgPGVsLWJ1dHRvbj5EZWZhdWx0PC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCI+UHJpbWFyeTwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwic3VjY2Vzc1wiPlN1Y2Nlc3M8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cImluZm9cIj5JbmZvPC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJ3YXJuaW5nXCI+V2FybmluZzwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwiZGFuZ2VyXCI+RGFuZ2VyPC9lbC1idXR0b24+XG4gICAgPC9kaXY+XG5cbiAgICA8ZGl2IGNsYXNzPVwiYnV0dG9uLXJvd1wiPlxuICAgICAgPGVsLWJ1dHRvbiBwbGFpbj5QbGFpbjwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIHBsYWluPlByaW1hcnk8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInN1Y2Nlc3NcIiBwbGFpbj5TdWNjZXNzPC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJpbmZvXCIgcGxhaW4+SW5mbzwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwid2FybmluZ1wiIHBsYWluPldhcm5pbmc8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cImRhbmdlclwiIHBsYWluPkRhbmdlcjwvZWwtYnV0dG9uPlxuICAgIDwvZGl2PlxuXG4gICAgPGRpdiBjbGFzcz1cImJ1dHRvbi1yb3dcIj5cbiAgICAgIDxlbC1idXR0b24gcm91bmQ+Um91bmQ8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiByb3VuZD5QcmltYXJ5PC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJzdWNjZXNzXCIgcm91bmQ+U3VjY2VzczwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwiaW5mb1wiIHJvdW5kPkluZm88L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cIndhcm5pbmdcIiByb3VuZD5XYXJuaW5nPC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJkYW5nZXJcIiByb3VuZD5EYW5nZXI8L2VsLWJ1dHRvbj5cbiAgICA8L2Rpdj5cblxuICAgIDxkaXYgY2xhc3M9XCJidXR0b24tcm93XCI+XG4gICAgICA8ZWwtYnV0dG9uIGRhc2hlZD5EYXNoZWQ8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBkYXNoZWQ+UHJpbWFyeTwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwic3VjY2Vzc1wiIGRhc2hlZD5TdWNjZXNzPC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJpbmZvXCIgZGFzaGVkPkluZm88L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cIndhcm5pbmdcIiBkYXNoZWQ+V2FybmluZzwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwiZGFuZ2VyXCIgZGFzaGVkPkRhbmdlcjwvZWwtYnV0dG9uPlxuICAgIDwvZGl2PlxuXG4gICAgPGRpdiBjbGFzcz1cImJ1dHRvbi1yb3dcIj5cbiAgICAgIDxlbC1idXR0b24gOmljb249XCJTZWFyY2hcIiBjaXJjbGUgLz5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiA6aWNvbj1cIkVkaXRcIiBjaXJjbGUgLz5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInN1Y2Nlc3NcIiA6aWNvbj1cIkNoZWNrXCIgY2lyY2xlIC8+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJpbmZvXCIgOmljb249XCJNZXNzYWdlXCIgY2lyY2xlIC8+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJ3YXJuaW5nXCIgOmljb249XCJTdGFyXCIgY2lyY2xlIC8+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJkYW5nZXJcIiA6aWNvbj1cIkRlbGV0ZVwiIGNpcmNsZSAvPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQge1xuICBDaGVjayxcbiAgRGVsZXRlLFxuICBFZGl0LFxuICBNZXNzYWdlLFxuICBTZWFyY2gsXG4gIFN0YXIsXG59IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uYnV0dG9uLWV4YW1wbGUge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBnYXA6IDFyZW07XG59XG5cbi5idXR0b24tcm93IHtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC13cmFwOiB3cmFwO1xuICBnYXA6IDFyZW07XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG59XG5cbi5idXR0b24tcm93ID4gKiB7XG4gIG1hcmdpbjogMDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/button/basic.vue)_

vue

```
<template>
  <div class="button-example">
    <div class="button-row">
      <el-button>Default</el-button>
      <el-button type="primary">Primary</el-button>
      <el-button type="success">Success</el-button>
      <el-button type="info">Info</el-button>
      <el-button type="warning">Warning</el-button>
      <el-button type="danger">Danger</el-button>
    </div>

    <div class="button-row">
      <el-button plain>Plain</el-button>
      <el-button type="primary" plain>Primary</el-button>
      <el-button type="success" plain>Success</el-button>
      <el-button type="info" plain>Info</el-button>
      <el-button type="warning" plain>Warning</el-button>
      <el-button type="danger" plain>Danger</el-button>
    </div>

    <div class="button-row">
      <el-button round>Round</el-button>
      <el-button type="primary" round>Primary</el-button>
      <el-button type="success" round>Success</el-button>
      <el-button type="info" round>Info</el-button>
      <el-button type="warning" round>Warning</el-button>
      <el-button type="danger" round>Danger</el-button>
    </div>

    <div class="button-row">
      <el-button dashed>Dashed</el-button>
      <el-button type="primary" dashed>Primary</el-button>
      <el-button type="success" dashed>Success</el-button>
      <el-button type="info" dashed>Info</el-button>
      <el-button type="warning" dashed>Warning</el-button>
      <el-button type="danger" dashed>Danger</el-button>
    </div>

    <div class="button-row">
      <el-button :icon="Search" circle />
      <el-button type="primary" :icon="Edit" circle />
      <el-button type="success" :icon="Check" circle />
      <el-button type="info" :icon="Message" circle />
      <el-button type="warning" :icon="Star" circle />
      <el-button type="danger" :icon="Delete" circle />
    </div>
  </div>
</template>

<script lang="ts" setup>
import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'
</script>

<style scoped>
.button-example {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.button-row > * {
  margin: 0;
}
</style>
```

隐藏源代码

## 禁用状态 [​](#禁用状态)

你可以使用 `disabled` 属性来定义按钮是否被禁用。

使用 `disabled` 属性来控制按钮是否为禁用状态。 该属性接受一个 `Boolean` 类型的值。

DefaultPrimarySuccessInfoWarningDanger

PlainPrimarySuccessInfoWarningDanger

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiYnV0dG9uLWV4YW1wbGVcIj5cbiAgICA8ZGl2IGNsYXNzPVwiYnV0dG9uLXJvd1wiPlxuICAgICAgPGVsLWJ1dHRvbiBkaXNhYmxlZD5EZWZhdWx0PC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgZGlzYWJsZWQ+UHJpbWFyeTwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwic3VjY2Vzc1wiIGRpc2FibGVkPlN1Y2Nlc3M8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cImluZm9cIiBkaXNhYmxlZD5JbmZvPC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJ3YXJuaW5nXCIgZGlzYWJsZWQ+V2FybmluZzwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwiZGFuZ2VyXCIgZGlzYWJsZWQ+RGFuZ2VyPC9lbC1idXR0b24+XG4gICAgPC9kaXY+XG5cbiAgICA8ZGl2IGNsYXNzPVwiYnV0dG9uLXJvd1wiPlxuICAgICAgPGVsLWJ1dHRvbiBwbGFpbiBkaXNhYmxlZD5QbGFpbjwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIHBsYWluIGRpc2FibGVkPlByaW1hcnk8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInN1Y2Nlc3NcIiBwbGFpbiBkaXNhYmxlZD5TdWNjZXNzPC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJpbmZvXCIgcGxhaW4gZGlzYWJsZWQ+SW5mbzwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwid2FybmluZ1wiIHBsYWluIGRpc2FibGVkPldhcm5pbmc8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cImRhbmdlclwiIHBsYWluIGRpc2FibGVkPkRhbmdlcjwvZWwtYnV0dG9uPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG4uYnV0dG9uLWV4YW1wbGUge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBnYXA6IDFyZW07XG59XG5cbi5idXR0b24tcm93IHtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC13cmFwOiB3cmFwO1xuICBnYXA6IDFyZW07XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG59XG5cbi5idXR0b24tcm93ID4gKiB7XG4gIG1hcmdpbjogMDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/button/disabled.vue)_

vue

```
<template>
  <div class="button-example">
    <div class="button-row">
      <el-button disabled>Default</el-button>
      <el-button type="primary" disabled>Primary</el-button>
      <el-button type="success" disabled>Success</el-button>
      <el-button type="info" disabled>Info</el-button>
      <el-button type="warning" disabled>Warning</el-button>
      <el-button type="danger" disabled>Danger</el-button>
    </div>

    <div class="button-row">
      <el-button plain disabled>Plain</el-button>
      <el-button type="primary" plain disabled>Primary</el-button>
      <el-button type="success" plain disabled>Success</el-button>
      <el-button type="info" plain disabled>Info</el-button>
      <el-button type="warning" plain disabled>Warning</el-button>
      <el-button type="danger" plain disabled>Danger</el-button>
    </div>
  </div>
</template>

<style scoped>
.button-example {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.button-row > * {
  margin: 0;
}
</style>
```

隐藏源代码

## 链接按钮 [​](#链接按钮)

WARNING

`type="text"` 已被 **废弃**，将于版本 3.0.0 时 **移除**，请考虑切换至新的 API。

新的 API `link` 于 2.2.1 版本时添加，你可以使用 `type` API 设置链接按钮的主题样式

Basic link button

plainprimarysuccessinfowarningdanger

Disabled link button

plainprimarysuccessinfowarningdanger

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8cD5CYXNpYyBsaW5rIGJ1dHRvbjwvcD5cbiAgPGRpdiBjbGFzcz1cIm1iLTRcIj5cbiAgICA8ZWwtYnV0dG9uXG4gICAgICB2LWZvcj1cImJ1dHRvbiBpbiBidXR0b25zXCJcbiAgICAgIDprZXk9XCJidXR0b24udGV4dFwiXG4gICAgICA6dHlwZT1cImJ1dHRvbi50eXBlXCJcbiAgICAgIGxpbmtcbiAgICA+XG4gICAgICB7eyBidXR0b24udGV4dCB9fVxuICAgIDwvZWwtYnV0dG9uPlxuICA8L2Rpdj5cblxuICA8cD5EaXNhYmxlZCBsaW5rIGJ1dHRvbjwvcD5cbiAgPGRpdj5cbiAgICA8ZWwtYnV0dG9uXG4gICAgICB2LWZvcj1cImJ1dHRvbiBpbiBidXR0b25zXCJcbiAgICAgIDprZXk9XCJidXR0b24udGV4dFwiXG4gICAgICA6dHlwZT1cImJ1dHRvbi50eXBlXCJcbiAgICAgIGxpbmtcbiAgICAgIGRpc2FibGVkXG4gICAgPlxuICAgICAge3sgYnV0dG9uLnRleHQgfX1cbiAgICA8L2VsLWJ1dHRvbj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuY29uc3QgYnV0dG9ucyA9IFtcbiAgeyB0eXBlOiAnJywgdGV4dDogJ3BsYWluJyB9LFxuICB7IHR5cGU6ICdwcmltYXJ5JywgdGV4dDogJ3ByaW1hcnknIH0sXG4gIHsgdHlwZTogJ3N1Y2Nlc3MnLCB0ZXh0OiAnc3VjY2VzcycgfSxcbiAgeyB0eXBlOiAnaW5mbycsIHRleHQ6ICdpbmZvJyB9LFxuICB7IHR5cGU6ICd3YXJuaW5nJywgdGV4dDogJ3dhcm5pbmcnIH0sXG4gIHsgdHlwZTogJ2RhbmdlcicsIHRleHQ6ICdkYW5nZXInIH0sXG5dIGFzIGNvbnN0XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/button/link.vue)_

vue

```
<template>
  <p>Basic link button</p>
  <div class="mb-4">
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      link
    >
      {{ button.text }}
    </el-button>
  </div>

  <p>Disabled link button</p>
  <div>
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      link
      disabled
    >
      {{ button.text }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
const buttons = [
  { type: '', text: 'plain' },
  { type: 'primary', text: 'primary' },
  { type: 'success', text: 'success' },
  { type: 'info', text: 'info' },
  { type: 'warning', text: 'warning' },
  { type: 'danger', text: 'danger' },
] as const
</script>
```

隐藏源代码

## 文字按钮 [​](#文字按钮)

TIP

文字按钮在现在有了全新的设计样式。 2.2.0 如果您想要使用老版样式的按钮，可以考虑使用 [Link](https://element-plus.org/zh-CN/component/link#basic) 组件。

API也已更新，由于 `type` 属性会同时控制按钮的样式， 因此我们通过一个新的 API `text: boolean` 来控制文字按钮。

没有边框和背景色的按钮。

Basic text button

plainprimarysuccessinfowarningdanger

Background color always on

plainprimarysuccessinfowarningdanger

Disabled text button

plainprimarysuccessinfowarningdanger

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8cD5CYXNpYyB0ZXh0IGJ1dHRvbjwvcD5cbiAgPGRpdiBjbGFzcz1cIm1iLTRcIj5cbiAgICA8ZWwtYnV0dG9uXG4gICAgICB2LWZvcj1cImJ1dHRvbiBpbiBidXR0b25zXCJcbiAgICAgIDprZXk9XCJidXR0b24udGV4dFwiXG4gICAgICA6dHlwZT1cImJ1dHRvbi50eXBlXCJcbiAgICAgIHRleHRcbiAgICA+XG4gICAgICB7eyBidXR0b24udGV4dCB9fVxuICAgIDwvZWwtYnV0dG9uPlxuICA8L2Rpdj5cblxuICA8cD5CYWNrZ3JvdW5kIGNvbG9yIGFsd2F5cyBvbjwvcD5cbiAgPGRpdiBjbGFzcz1cIm1iLTRcIj5cbiAgICA8ZWwtYnV0dG9uXG4gICAgICB2LWZvcj1cImJ1dHRvbiBpbiBidXR0b25zXCJcbiAgICAgIDprZXk9XCJidXR0b24udGV4dFwiXG4gICAgICA6dHlwZT1cImJ1dHRvbi50eXBlXCJcbiAgICAgIHRleHRcbiAgICAgIGJnXG4gICAgPlxuICAgICAge3sgYnV0dG9uLnRleHQgfX1cbiAgICA8L2VsLWJ1dHRvbj5cbiAgPC9kaXY+XG5cbiAgPHA+RGlzYWJsZWQgdGV4dCBidXR0b248L3A+XG4gIDxkaXY+XG4gICAgPGVsLWJ1dHRvblxuICAgICAgdi1mb3I9XCJidXR0b24gaW4gYnV0dG9uc1wiXG4gICAgICA6a2V5PVwiYnV0dG9uLnRleHRcIlxuICAgICAgOnR5cGU9XCJidXR0b24udHlwZVwiXG4gICAgICB0ZXh0XG4gICAgICBkaXNhYmxlZFxuICAgID5cbiAgICAgIHt7IGJ1dHRvbi50ZXh0IH19XG4gICAgPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmNvbnN0IGJ1dHRvbnMgPSBbXG4gIHsgdHlwZTogJycsIHRleHQ6ICdwbGFpbicgfSxcbiAgeyB0eXBlOiAncHJpbWFyeScsIHRleHQ6ICdwcmltYXJ5JyB9LFxuICB7IHR5cGU6ICdzdWNjZXNzJywgdGV4dDogJ3N1Y2Nlc3MnIH0sXG4gIHsgdHlwZTogJ2luZm8nLCB0ZXh0OiAnaW5mbycgfSxcbiAgeyB0eXBlOiAnd2FybmluZycsIHRleHQ6ICd3YXJuaW5nJyB9LFxuICB7IHR5cGU6ICdkYW5nZXInLCB0ZXh0OiAnZGFuZ2VyJyB9LFxuXSBhcyBjb25zdFxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/button/text.vue)_

vue

```
<template>
  <p>Basic text button</p>
  <div class="mb-4">
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      text
    >
      {{ button.text }}
    </el-button>
  </div>

  <p>Background color always on</p>
  <div class="mb-4">
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      text
      bg
    >
      {{ button.text }}
    </el-button>
  </div>

  <p>Disabled text button</p>
  <div>
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      text
      disabled
    >
      {{ button.text }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
const buttons = [
  { type: '', text: 'plain' },
  { type: 'primary', text: 'primary' },
  { type: 'success', text: 'success' },
  { type: 'info', text: 'info' },
  { type: 'warning', text: 'warning' },
  { type: 'danger', text: 'danger' },
] as const
</script>
```

隐藏源代码

## 图标按钮 [​](#图标按钮)

使用图标为按钮添加更多的含义。 你也可以单独使用图标不添加文字来节省显示区域占用。

使用 `icon` 属性来为按钮添加图标。 您可以在我们的 Icon 组件中找到所需图标。 通过向右方添加`<i>`标签来添加图标， 你也可以使用自定义图标。

Search Upload

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiA6aWNvbj1cIkVkaXRcIiAvPlxuICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiA6aWNvbj1cIlNoYXJlXCIgLz5cbiAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgOmljb249XCJEZWxldGVcIiAvPlxuICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiA6aWNvbj1cIlNlYXJjaFwiPlNlYXJjaDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIj5cbiAgICAgIFVwbG9hZDxlbC1pY29uIGNsYXNzPVwiZWwtaWNvbi0tcmlnaHRcIj48VXBsb2FkIC8+PC9lbC1pY29uPlxuICAgIDwvZWwtYnV0dG9uPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+XG5pbXBvcnQgeyBEZWxldGUsIEVkaXQsIFNlYXJjaCwgU2hhcmUsIFVwbG9hZCB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/button/icon.vue)_

vue

```
<template>
  <div>
    <el-button type="primary" :icon="Edit" />
    <el-button type="primary" :icon="Share" />
    <el-button type="primary" :icon="Delete" />
    <el-button type="primary" :icon="Search">Search</el-button>
    <el-button type="primary">
      Upload<el-icon class="el-icon--right"><Upload /></el-icon>
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { Delete, Edit, Search, Share, Upload } from '@element-plus/icons-vue'
</script>
```

隐藏源代码

## 按钮组 [​](#按钮组)

以按钮组的方式出现，常用于多项类似操作。

在 2.11.9 中，您可以使用 `direction` 属性。

使用 `<el-button-group>` 对多个按钮分组。

Previous Page Next Page

HorizontalVertical

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uLWdyb3VwIGNsYXNzPVwibWItNFwiPlxuICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiA6aWNvbj1cIkFycm93TGVmdFwiPlByZXZpb3VzIFBhZ2U8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCI+XG4gICAgICBOZXh0IFBhZ2U8ZWwtaWNvbiBjbGFzcz1cImVsLWljb24tLXJpZ2h0XCI+PEFycm93UmlnaHQgLz48L2VsLWljb24+XG4gICAgPC9lbC1idXR0b24+XG4gIDwvZWwtYnV0dG9uLWdyb3VwPlxuICA8YnIgLz5cbiAgPGVsLXJhZGlvLWdyb3VwIHYtbW9kZWw9XCJkaXJlY3Rpb25cIiBjbGFzcz1cIm1iLTJcIj5cbiAgICA8ZWwtcmFkaW8gdmFsdWU9XCJob3Jpem9udGFsXCI+SG9yaXpvbnRhbDwvZWwtcmFkaW8+XG4gICAgPGVsLXJhZGlvIHZhbHVlPVwidmVydGljYWxcIj5WZXJ0aWNhbDwvZWwtcmFkaW8+XG4gIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDxiciAvPlxuXG4gIDxlbC1idXR0b24tZ3JvdXAgOmRpcmVjdGlvbj1cImRpcmVjdGlvblwiPlxuICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiA6aWNvbj1cIkhvdXNlXCIgLz5cbiAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgOmljb249XCJPcGVyYXRpb25cIiAvPlxuICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiA6aWNvbj1cIk5vdGlmaWNhdGlvblwiIC8+XG4gIDwvZWwtYnV0dG9uLWdyb3VwPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7XG4gIEFycm93TGVmdCxcbiAgQXJyb3dSaWdodCxcbiAgSG91c2UsXG4gIE5vdGlmaWNhdGlvbixcbiAgT3BlcmF0aW9uLFxufSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgZGlyZWN0aW9uID0gcmVmPCdob3Jpem9udGFsJyB8ICd2ZXJ0aWNhbCc+KCdob3Jpem9udGFsJylcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/button/group.vue)_

vue

```
<template>
  <el-button-group class="mb-4">
    <el-button type="primary" :icon="ArrowLeft">Previous Page</el-button>
    <el-button type="primary">
      Next Page<el-icon class="el-icon--right"><ArrowRight /></el-icon>
    </el-button>
  </el-button-group>
  <br />
  <el-radio-group v-model="direction" class="mb-2">
    <el-radio value="horizontal">Horizontal</el-radio>
    <el-radio value="vertical">Vertical</el-radio>
  </el-radio-group>
  <br />

  <el-button-group :direction="direction">
    <el-button type="primary" :icon="House" />
    <el-button type="primary" :icon="Operation" />
    <el-button type="primary" :icon="Notification" />
  </el-button-group>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  ArrowLeft,
  ArrowRight,
  House,
  Notification,
  Operation,
} from '@element-plus/icons-vue'

const direction = ref<'horizontal' | 'vertical'>('horizontal')
</script>
```

隐藏源代码

## 加载状态按钮 [​](#加载状态按钮)

点击按钮来加载数据，并向用户反馈加载状态。

通过设置 `loading` 属性为 `true` 来显示加载中状态。

TIP

您可以使用 `loading` 插槽或 `loadingIcon`属性自定义您的loading图标

ps: `loading` 插槽优先级高于`loadingIcon`属性

LoadingLoading

Loading

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgbG9hZGluZz5Mb2FkaW5nPC9lbC1idXR0b24+XG4gIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiA6bG9hZGluZy1pY29uPVwiRWxlbWVcIiBsb2FkaW5nPkxvYWRpbmc8L2VsLWJ1dHRvbj5cbiAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIGxvYWRpbmc+XG4gICAgPHRlbXBsYXRlICNsb2FkaW5nPlxuICAgICAgPGRpdiBjbGFzcz1cImN1c3RvbS1sb2FkaW5nXCI+XG4gICAgICAgIDxzdmcgY2xhc3M9XCJjaXJjdWxhclwiIHZpZXdCb3g9XCItMTAsIC0xMCwgNTAsIDUwXCI+XG4gICAgICAgICAgPHBhdGhcbiAgICAgICAgICAgIGNsYXNzPVwicGF0aFwiXG4gICAgICAgICAgICBkPVwiXG4gICAgICAgICAgICBNIDMwIDE1XG4gICAgICAgICAgICBMIDI4IDE3XG4gICAgICAgICAgICBNIDI1LjYxIDI1LjYxXG4gICAgICAgICAgICBBIDE1IDE1LCAwLCAwLCAxLCAxNSAzMFxuICAgICAgICAgICAgQSAxNSAxNSwgMCwgMSwgMSwgMjcuOTkgNy41XG4gICAgICAgICAgICBMIDE1IDE1XG4gICAgICAgICAgXCJcbiAgICAgICAgICAgIHN0eWxlPVwic3Ryb2tlLXdpZHRoOiA0cHg7IGZpbGw6IHJnYmEoMCwgMCwgMCwgMClcIlxuICAgICAgICAgIC8+XG4gICAgICAgIDwvc3ZnPlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgICBMb2FkaW5nXG4gIDwvZWwtYnV0dG9uPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEVsZW1lIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5lbC1idXR0b24gLmN1c3RvbS1sb2FkaW5nIC5jaXJjdWxhciB7XG4gIG1hcmdpbi1yaWdodDogNnB4O1xuICB3aWR0aDogMThweDtcbiAgaGVpZ2h0OiAxOHB4O1xuICBhbmltYXRpb246IGxvYWRpbmctcm90YXRlIDJzIGxpbmVhciBpbmZpbml0ZTtcbn1cbi5lbC1idXR0b24gLmN1c3RvbS1sb2FkaW5nIC5jaXJjdWxhciAucGF0aCB7XG4gIGFuaW1hdGlvbjogbG9hZGluZy1kYXNoIDEuNXMgZWFzZS1pbi1vdXQgaW5maW5pdGU7XG4gIHN0cm9rZS1kYXNoYXJyYXk6IDkwLCAxNTA7XG4gIHN0cm9rZS1kYXNob2Zmc2V0OiAwO1xuICBzdHJva2Utd2lkdGg6IDI7XG4gIHN0cm9rZTogdmFyKC0tZWwtYnV0dG9uLXRleHQtY29sb3IpO1xuICBzdHJva2UtbGluZWNhcDogcm91bmQ7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/button/loading.vue)_

vue

```
<template>
  <el-button type="primary" loading>Loading</el-button>
  <el-button type="primary" :loading-icon="Eleme" loading>Loading</el-button>
  <el-button type="primary" loading>
    <template #loading>
      <div class="custom-loading">
        <svg class="circular" viewBox="-10, -10, 50, 50">
          <path
            class="path"
            d="
            M 30 15
            L 28 17
            M 25.61 25.61
            A 15 15, 0, 0, 1, 15 30
            A 15 15, 0, 1, 1, 27.99 7.5
            L 15 15
          "
            style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"
          />
        </svg>
      </div>
    </template>
    Loading
  </el-button>
</template>

<script lang="ts" setup>
import { Eleme } from '@element-plus/icons-vue'
</script>

<style scoped>
.el-button .custom-loading .circular {
  margin-right: 6px;
  width: 18px;
  height: 18px;
  animation: loading-rotate 2s linear infinite;
}
.el-button .custom-loading .circular .path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-button-text-color);
  stroke-linecap: round;
}
</style>
```

隐藏源代码

## 调整尺寸 [​](#调整尺寸)

除了默认的大小，按钮组件还提供了几种额外的尺寸可供选择，以便适配不同的场景。

使用 `size` 属性额外配置尺寸，可使用 `large`和`small`两种值。

LargeDefaultSmallSearchSearchSearch

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgaXRlbXMtY2VudGVyIG1iLTRcIj5cbiAgICA8ZWwtYnV0dG9uIHNpemU9XCJsYXJnZVwiPkxhcmdlPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbj5EZWZhdWx0PC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBzaXplPVwic21hbGxcIj5TbWFsbDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gc2l6ZT1cImxhcmdlXCIgOmljb249XCJTZWFyY2hcIj5TZWFyY2g8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIDppY29uPVwiU2VhcmNoXCI+U2VhcmNoPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBzaXplPVwic21hbGxcIiA6aWNvbj1cIlNlYXJjaFwiPlNlYXJjaDwvZWwtYnV0dG9uPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cImZsZXggZmxleC13cmFwIGl0ZW1zLWNlbnRlciBtYi00XCI+XG4gICAgPGVsLWJ1dHRvbiBzaXplPVwibGFyZ2VcIiByb3VuZD5MYXJnZTwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gcm91bmQ+RGVmYXVsdDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gc2l6ZT1cInNtYWxsXCIgcm91bmQ+U21hbGw8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIHNpemU9XCJsYXJnZVwiIDppY29uPVwiU2VhcmNoXCIgcm91bmQ+U2VhcmNoPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiA6aWNvbj1cIlNlYXJjaFwiIHJvdW5kPlNlYXJjaDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gc2l6ZT1cInNtYWxsXCIgOmljb249XCJTZWFyY2hcIiByb3VuZD5TZWFyY2g8L2VsLWJ1dHRvbj5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJmbGV4IGZsZXgtd3JhcCBpdGVtcy1jZW50ZXJcIj5cbiAgICA8ZWwtYnV0dG9uIDppY29uPVwiU2VhcmNoXCIgc2l6ZT1cImxhcmdlXCIgY2lyY2xlIC8+XG4gICAgPGVsLWJ1dHRvbiA6aWNvbj1cIlNlYXJjaFwiIGNpcmNsZSAvPlxuICAgIDxlbC1idXR0b24gOmljb249XCJTZWFyY2hcIiBzaXplPVwic21hbGxcIiBjaXJjbGUgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgU2VhcmNoIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/button/size.vue)_

vue

```
<template>
  <div class="flex flex-wrap items-center mb-4">
    <el-button size="large">Large</el-button>
    <el-button>Default</el-button>
    <el-button size="small">Small</el-button>
    <el-button size="large" :icon="Search">Search</el-button>
    <el-button :icon="Search">Search</el-button>
    <el-button size="small" :icon="Search">Search</el-button>
  </div>
  <div class="flex flex-wrap items-center mb-4">
    <el-button size="large" round>Large</el-button>
    <el-button round>Default</el-button>
    <el-button size="small" round>Small</el-button>
    <el-button size="large" :icon="Search" round>Search</el-button>
    <el-button :icon="Search" round>Search</el-button>
    <el-button size="small" :icon="Search" round>Search</el-button>
  </div>
  <div class="flex flex-wrap items-center">
    <el-button :icon="Search" size="large" circle />
    <el-button :icon="Search" circle />
    <el-button :icon="Search" size="small" circle />
  </div>
</template>

<script setup lang="ts">
import { Search } from '@element-plus/icons-vue'
</script>
```

隐藏源代码

## Tag 2.3.4 [​](#tag)

您可以自定义元素标签。例如，按钮，div，路由链接，nuxt链接。

button

div

[a](https://github.com/element-plus/element-plus)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uPmJ1dHRvbjwvZWwtYnV0dG9uPlxuICA8ZWwtYnV0dG9uIHRhZz1cImRpdlwiIHJvbGU9XCJidXR0b25cIiB0YWJpbmRleD1cIjBcIj5kaXY8L2VsLWJ1dHRvbj5cbiAgPGVsLWJ1dHRvblxuICAgIHR5cGU9XCJwcmltYXJ5XCJcbiAgICB0YWc9XCJhXCJcbiAgICBocmVmPVwiaHR0cHM6Ly9naXRodWIuY29tL2VsZW1lbnQtcGx1cy9lbGVtZW50LXBsdXNcIlxuICAgIHRhcmdldD1cIl9ibGFua1wiXG4gICAgcmVsPVwibm9vcGVuZXIgbm9yZWZlcnJlclwiXG4gID5cbiAgICBhXG4gIDwvZWwtYnV0dG9uPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/button/tag.vue)_

vue

```
<template>
  <el-button>button</el-button>
  <el-button tag="div" role="button" tabindex="0">div</el-button>
  <el-button
    type="primary"
    tag="a"
    href="https://github.com/element-plus/element-plus"
    target="_blank"
    rel="noopener noreferrer"
  >
    a
  </el-button>
</template>
```

隐藏源代码

## 自定义颜色 beta [​](#自定义颜色)

您可以自定义按钮的颜色。

我们将自动计算按钮处于 hover 和 active 状态时的颜色。

自 2.13.7 起，`color` 属性也适用于 `link` 和 `text` 按钮。

DefaultPlainLinkTextText BGDisabled Disabled Plain Disabled Link Disabled Text Disabled Text BG

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGlzRGFyayB9IGZyb20gJ34vY29tcG9zYWJsZXMvZGFyaydcbjwvc2NyaXB0PlxuXG48dGVtcGxhdGU+XG4gIDxkaXY+XG4gICAgPGVsLWJ1dHRvbiBjb2xvcj1cIiM2MjZhZWZcIiA6ZGFyaz1cImlzRGFya1wiPkRlZmF1bHQ8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNvbG9yPVwiIzYyNmFlZlwiIDpkYXJrPVwiaXNEYXJrXCIgcGxhaW4+UGxhaW48L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNvbG9yPVwiIzYyNmFlZlwiIDpkYXJrPVwiaXNEYXJrXCIgbGluaz5MaW5rPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjb2xvcj1cIiM2MjZhZWZcIiA6ZGFyaz1cImlzRGFya1wiIHRleHQ+VGV4dDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY29sb3I9XCIjNjI2YWVmXCIgOmRhcms9XCJpc0RhcmtcIiB0ZXh0IGJnPlRleHQgQkc8L2VsLWJ1dHRvbj5cblxuICAgIDxlbC1idXR0b24gY29sb3I9XCIjNjI2YWVmXCIgOmRhcms9XCJpc0RhcmtcIiBkaXNhYmxlZD5EaXNhYmxlZDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY29sb3I9XCIjNjI2YWVmXCIgOmRhcms9XCJpc0RhcmtcIiBkaXNhYmxlZCBwbGFpbj5cbiAgICAgIERpc2FibGVkIFBsYWluXG4gICAgPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjb2xvcj1cIiM2MjZhZWZcIiA6ZGFyaz1cImlzRGFya1wiIGRpc2FibGVkIGxpbms+XG4gICAgICBEaXNhYmxlZCBMaW5rXG4gICAgPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjb2xvcj1cIiM2MjZhZWZcIiA6ZGFyaz1cImlzRGFya1wiIGRpc2FibGVkIHRleHQ+XG4gICAgICBEaXNhYmxlZCBUZXh0XG4gICAgPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjb2xvcj1cIiM2MjZhZWZcIiA6ZGFyaz1cImlzRGFya1wiIGRpc2FibGVkIHRleHQgYmc+XG4gICAgICBEaXNhYmxlZCBUZXh0IEJHXG4gICAgPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/button/custom.vue)_

vue

```
<script lang="ts" setup>
import { isDark } from '~/composables/dark'
</script>

<template>
  <div>
    <el-button color="#626aef" :dark="isDark">Default</el-button>
    <el-button color="#626aef" :dark="isDark" plain>Plain</el-button>
    <el-button color="#626aef" :dark="isDark" link>Link</el-button>
    <el-button color="#626aef" :dark="isDark" text>Text</el-button>
    <el-button color="#626aef" :dark="isDark" text bg>Text BG</el-button>

    <el-button color="#626aef" :dark="isDark" disabled>Disabled</el-button>
    <el-button color="#626aef" :dark="isDark" disabled plain>
      Disabled Plain
    </el-button>
    <el-button color="#626aef" :dark="isDark" disabled link>
      Disabled Link
    </el-button>
    <el-button color="#626aef" :dark="isDark" disabled text>
      Disabled Text
    </el-button>
    <el-button color="#626aef" :dark="isDark" disabled text bg>
      Disabled Text BG
    </el-button>
  </div>
</template>
```

隐藏源代码

## Button API [​](#button-api)

### Button Attributes [​](#button-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| size | 尺寸 | `enum` | — |
| type | 按钮类型，在设置`color`时，后者优先。 | `enum` | — |
| plain | 是否为朴素按钮 | `boolean` | false |
| text 2.2.0 | 是否为文字按钮 | `boolean` | false |
| bg 2.2.0 | 是否显示文字按钮背景颜色 | `boolean` | false |
| link 2.2.1 | 是否为链接按钮 | `boolean` | false |
| round | 是否为圆角按钮 | `boolean` | false |
| circle | 是否为圆形按钮 | `boolean` | false |
| dashed 2.13.3 | 是否是虚线按钮 | `boolean` | false |
| loading | 是否为加载中状态 | `boolean` | false |
| loading-icon | 自定义加载中状态图标组件 | `string` / `Component` | Loading |
| disabled | 按钮是否为禁用状态 | `boolean` | false |
| icon | 图标组件 | `string` / `Component` | — |
| autofocus | 原生 `autofocus` 属性 | `boolean` | false |
| native-type | 原生 type 属性 | `enum` | button |
| auto-insert-space | 两个中文字符之间自动插入空格(仅当文本长度为 2 且所有字符均为中文时才生效) | `boolean` | false |
| color | 自定义按钮颜色, 并自动计算 `hover` 和 `active` 触发后的颜色 自 2.13.7 起，支持 `link`/`text` 按钮。 | `string` | — |
| dark | dark 模式, 意味着自动设置 `color` 为 dark 模式的颜色 | `boolean` | false |
| tag 2.3.4 | 自定义元素标签 | `string` / `Component` | button |

### Button Slots [​](#button-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |
| loading | 自定义加载中组件 |
| icon | 自定义图标组件 |

### Button Exposes [​](#button-exposes)

| 属性名 | 说明 | 类型 |
| --- | --- | --- |
| ref | 按钮 html 元素 | `object` |
| size | 按钮尺寸 | `object` |
| type | 按钮类型 | `object` |
| disabled | 按钮已禁用 | `object` |
| shouldAddSpace | 是否在两个字符之间插入空格 | `object` |

## ButtonGroup API [​](#buttongroup-api)

### ButtonGroup Attributes [​](#buttongroup-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| size | 用于控制该按钮组内按钮的大小 | `enum` | — |
| type | 用于控制该按钮组内按钮的类型 | `enum` | — |
| direction 2.11.9 | 展示的方向 | `enum` | horizontal |

### ButtonGroup Slots [​](#buttongroup-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义按钮组内容 | Button |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/button) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/button.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/button.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/45122329?v=4&size=64)](https://github.com/cokemine)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/24487727?v=4&size=64)](https://github.com/LostElkByte)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/57352899?v=4&size=64)](https://github.com/VisualYuki)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/41461715?v=4&size=64)](https://github.com/VENI-VIDIVICI)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/30883395?v=4&size=64)](https://github.com/webvs2)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/109908413?v=4&size=64)](https://github.com/sleepyShen1989)[![](https://avatars.githubusercontent.com/u/73946940?v=4&size=64)](https://github.com/jiechen257)[![](https://avatars.githubusercontent.com/u/23433168?v=4&size=64)](https://github.com/hunter-fl)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/102006695?v=4&size=64)](https://github.com/cuongle-hdwebsoft)[![](https://avatars.githubusercontent.com/u/6948318?v=4&size=64)](https://github.com/dreambo8563)[![](https://avatars.githubusercontent.com/u/42372070?v=4&size=64)](https://github.com/Map1en)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/61005888?v=4&size=64)](https://github.com/kuizuo)[![](https://avatars.githubusercontent.com/u/4241620?v=4&size=64)](https://github.com/muhammadcahya)[![](https://avatars.githubusercontent.com/u/191817983?v=4&size=64)](https://github.com/zhuft-moon)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)[![](https://avatars.githubusercontent.com/u/30796346?v=4&size=64)](https://github.com/lyh0371)

[Overview 组件总览](https://element-plus.org/zh-CN/component/overview)

[Border 边框](https://element-plus.org/zh-CN/component/border)


