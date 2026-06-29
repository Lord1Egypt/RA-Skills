---
name: "alert"
description: "Alert 警告 -- Element UI Vue2 桌面端组件。Invoke when user needs Alert 警告 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/alert"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/alert#alert-jing-gao) Alert 警告

用于页面中展示重要的提示信息。

### [¶](https://element.eleme.cn/#/zh-CN/component/alert#ji-ben-yong-fa) 基本用法

页面中的非浮层元素，不会自动消失。

成功提示的文案

消息提示的文案

警告提示的文案

错误提示的文案

Alert 组件提供四种主题，由`type`属性指定，默认值为`info`。

```
<template>
  <el-alert
    title="成功提示的文案"
    type="success">
  </el-alert>
  <el-alert
    title="消息提示的文案"
    type="info">
  </el-alert>
  <el-alert
    title="警告提示的文案"
    type="warning">
  </el-alert>
  <el-alert
    title="错误提示的文案"
    type="error">
  </el-alert>
</template>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/alert#zhu-ti) 主题

Alert 组件提供了两个不同的主题：`light`和`dark`。

成功提示的文案

消息提示的文案

警告提示的文案

错误提示的文案

通过设置`effect`属性来改变主题，默认为`light`。

```
<template>
  <el-alert
    title="成功提示的文案"
    type="success"
    effect="dark">
  </el-alert>
  <el-alert
    title="消息提示的文案"
    type="info"
    effect="dark">
  </el-alert>
  <el-alert
    title="警告提示的文案"
    type="warning"
    effect="dark">
  </el-alert>
  <el-alert
    title="错误提示的文案"
    type="error"
    effect="dark">
  </el-alert>
</template>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/alert#zi-ding-yi-guan-bi-an-niu) 自定义关闭按钮

自定义关闭按钮为文字或其他符号。

不可关闭的 alert

自定义 close-text_知道了_

设置了回调的 alert

在 Alert 组件中，你可以设置是否可关闭，关闭按钮的文本以及关闭时的回调函数。`closable`属性决定是否可关闭，接受`boolean`，默认为`true`。你可以设置`close-text`属性来代替右侧的关闭图标，注意：`close-text`必须为文本。设置`close`事件来设置关闭时的回调。

```
<template>
  <el-alert
    title="不可关闭的 alert"
    type="success"
    :closable="false">
  </el-alert>
  <el-alert
    title="自定义 close-text"
    type="info"
    close-text="知道了">
  </el-alert>
  <el-alert
    title="设置了回调的 alert"
    type="warning"
    @close="hello">
  </el-alert>
</template>

<script>
  export default {
    methods: {
      hello() {
        alert('Hello World!');
      }
    }
  }
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/alert#dai-you-icon) 带有 icon

表示某种状态时提升可读性。

成功提示的文案

消息提示的文案

警告提示的文案

错误提示的文案

通过设置`show-icon`属性来显示 Alert 的 icon，这能更有效地向用户展示你的显示意图。

```
<template>
  <el-alert
    title="成功提示的文案"
    type="success"
    show-icon>
  </el-alert>
  <el-alert
    title="消息提示的文案"
    type="info"
    show-icon>
  </el-alert>
  <el-alert
    title="警告提示的文案"
    type="warning"
    show-icon>
  </el-alert>
  <el-alert
    title="错误提示的文案"
    type="error"
    show-icon>
  </el-alert>
</template>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/alert#wen-zi-ju-zhong) 文字居中

使用 `center` 属性让文字水平居中。

成功提示的文案

消息提示的文案

警告提示的文案

错误提示的文案

```
<template>
  <el-alert
    title="成功提示的文案"
    type="success"
    center
    show-icon>
  </el-alert>
  <el-alert
    title="消息提示的文案"
    type="info"
    center
    show-icon>
  </el-alert>
  <el-alert
    title="警告提示的文案"
    type="warning"
    center
    show-icon>
  </el-alert>
  <el-alert
    title="错误提示的文案"
    type="error"
    center
    show-icon>
  </el-alert>
</template>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/alert#dai-you-fu-zhu-xing-wen-zi-jie-shao) 带有辅助性文字介绍

包含标题和内容，解释更详细的警告。

带辅助性文字介绍

这是一句绕口令：黑灰化肥会挥发发灰黑化肥挥发；灰黑化肥会挥发发黑灰化肥发挥。 黑灰化肥会挥发发灰黑化肥黑灰挥发化为灰……

除了必填的`title`属性外，你可以设置`description`属性来帮助你更好地介绍，我们称之为辅助性文字。辅助性文字只能存放单行文本，会自动换行显示。

```
<template>
  <el-alert
    title="带辅助性文字介绍"
    type="success"
    description="这是一句绕口令：黑灰化肥会挥发发灰黑化肥挥发；灰黑化肥会挥发发黑灰化肥发挥。 黑灰化肥会挥发发灰黑化肥黑灰挥发化为灰……">
  </el-alert>
</template>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/alert#dai-you-icon-he-fu-zhu-xing-wen-zi-jie-shao) 带有 icon 和辅助性文字介绍

成功提示的文案

文字说明文字说明文字说明文字说明文字说明文字说明

消息提示的文案

文字说明文字说明文字说明文字说明文字说明文字说明

警告提示的文案

文字说明文字说明文字说明文字说明文字说明文字说明

错误提示的文案

文字说明文字说明文字说明文字说明文字说明文字说明

最后，这是一个同时具有 icon 和辅助性文字的样例。

```
<template>
  <el-alert
    title="成功提示的文案"
    type="success"
    description="文字说明文字说明文字说明文字说明文字说明文字说明"
    show-icon>
  </el-alert>
  <el-alert
    title="消息提示的文案"
    type="info"
    description="文字说明文字说明文字说明文字说明文字说明文字说明"
    show-icon>
  </el-alert>
  <el-alert
    title="警告提示的文案"
    type="warning"
    description="文字说明文字说明文字说明文字说明文字说明文字说明"
    show-icon>
  </el-alert>
  <el-alert
    title="错误提示的文案"
    type="error"
    description="文字说明文字说明文字说明文字说明文字说明文字说明"
    show-icon>
  </el-alert>
</template>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/alert#attributes) Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| title | 标题 | string | — | — |
| type | 主题 | string | success/warning/info/error | info |
| description | 辅助性文字。也可通过默认 slot 传入 | string | — | — |
| closable | 是否可关闭 | boolean | — | true |
| center | 文字是否居中 | boolean | — | true |
| close-text | 关闭按钮自定义文本 | string | — | — |
| show-icon | 是否显示图标 | boolean | — | false |
| effect | 选择提供的主题 | string | light/dark | light |

### [¶](https://element.eleme.cn/#/zh-CN/component/alert#slot) Slot

| Name | Description |
| --- | --- |
| — | 描述 |
| title | 标题的内容 |

### [¶](https://element.eleme.cn/#/zh-CN/component/alert#events) Events

| 事件名称 | 说明 | 回调参数 |
| --- | --- | --- |
| close | 关闭alert时触发的事件 | — |

Statistic 统计数值 Loading 加载


