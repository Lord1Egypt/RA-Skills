---
name: "divider"
description: "Divider 分割线 -- Element UI Vue2 桌面端组件。Invoke when user needs Divider 分割线 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/divider"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/divider#divider-fen-ge-xian) Divider 分割线

区隔内容的分割线。

### [¶](https://element.eleme.cn/#/zh-CN/component/divider#ji-chu-yong-fa) 基础用法

对不同章节的文本段落进行分割。

青春是一个短暂的美梦, 当你醒来时, 它早已消失无踪

少量的邪恶足以抵消全部高贵的品质, 害得人声名狼藉

```
<template>
  <div>
    <span>青春是一个短暂的美梦, 当你醒来时, 它早已消失无踪</span>
    <el-divider></el-divider>
    <span>少量的邪恶足以抵消全部高贵的品质, 害得人声名狼藉</span>
  </div>
</template>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/divider#she-zhi-wen-an) 设置文案

可以在分割线上自定义文案内容。

头上一片晴天，心中一个想念

少年包青天

饿了别叫妈, 叫饿了么

为了无法计算的价值

阿里云

```
<template>
  <div>
    <span>头上一片晴天，心中一个想念</span>
    <el-divider content-position="left">少年包青天</el-divider>
    <span>饿了别叫妈, 叫饿了么</span>
    <el-divider><i class="el-icon-mobile-phone"></i></el-divider>
    <span>为了无法计算的价值</span>
    <el-divider content-position="right">阿里云</el-divider>
  </div>
</template>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/divider#chui-zhi-fen-ge) 垂直分割

雨纷纷

旧故里

草木深

```
<template>
  <div>
    <span>雨纷纷</span>
    <el-divider direction="vertical"></el-divider>
    <span>旧故里</span>
    <el-divider direction="vertical"></el-divider>
    <span>草木深</span>
  </div>
</template>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/divider#divider-attributes) Divider Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| direction | 设置分割线方向 | string | horizontal / vertical | horizontal |
| content-position | 设置分割线文案的位置 | string | left / right / center | center |

Timeline 时间线 Calendar 日历


