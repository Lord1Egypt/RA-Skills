---
name: "backtop"
description: "Backtop 回到顶部 -- Element Plus Vue3 桌面端组件。Invoke when user needs Backtop 回到顶部 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/backtop.html"
---

---

# Backtop 回到顶部 [​](#backtop-回到顶部)

更新日志待解决

1

返回页面顶部的操作按钮。

## 基础用法 [​](#基础用法)

通过滑动来查看容器右下角的按钮。

Scroll down to see the bottom-right button.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICBTY3JvbGwgZG93biB0byBzZWUgdGhlIGJvdHRvbS1yaWdodCBidXR0b24uXG4gIDxlbC1iYWNrdG9wIDpyaWdodD1cIjEwMFwiIDpib3R0b209XCIxMDBcIiAvPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/backtop/basic.vue)_

vue

```
<template>
  Scroll down to see the bottom-right button.
  <el-backtop :right="100" :bottom="100" />
</template>
```

隐藏源代码

## 自定义内容 [​](#自定义内容)

显示区域被固定为 40px \* 40px 的区域，其中的内容可支持自定义。

Scroll down to see the bottom-right button.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICBTY3JvbGwgZG93biB0byBzZWUgdGhlIGJvdHRvbS1yaWdodCBidXR0b24uXG4gIDxlbC1iYWNrdG9wIDpib3R0b209XCIxMDBcIj5cbiAgICA8ZGl2XG4gICAgICBzdHlsZT1cIlxuICAgICAgICBoZWlnaHQ6IDEwMCU7XG4gICAgICAgIHdpZHRoOiAxMDAlO1xuICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiB2YXIoLS1lbC1iZy1jb2xvci1vdmVybGF5KTtcbiAgICAgICAgYm94LXNoYWRvdzogdmFyKC0tZWwtYm94LXNoYWRvdy1saWdodGVyKTtcbiAgICAgICAgdGV4dC1hbGlnbjogY2VudGVyO1xuICAgICAgICBsaW5lLWhlaWdodDogNDBweDtcbiAgICAgICAgY29sb3I6ICMxOTg5ZmE7XG4gICAgICBcIlxuICAgID5cbiAgICAgIFVQXG4gICAgPC9kaXY+XG4gIDwvZWwtYmFja3RvcD5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/backtop/custom.vue)_

vue

```
<template>
  Scroll down to see the bottom-right button.
  <el-backtop :bottom="100">
    <div
      style="
        height: 100%;
        width: 100%;
        background-color: var(--el-bg-color-overlay);
        box-shadow: var(--el-box-shadow-lighter);
        text-align: center;
        line-height: 40px;
        color: #1989fa;
      "
    >
      UP
    </div>
  </el-backtop>
</template>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 名称 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| target | 触发滚动的对象 | `string` | — |
| visibility-height | 滚动高度达到此参数值才出现 | `number` | 200 |
| right | 控制其显示位置，距离页面右边距 | `number` | 40 |
| bottom | 控制其显示位置，距离页面底部距离 | `number` | 40 |

### Events [​](#events)

| 名称 | 说明 | 回调参数 |
| --- | --- | --- |
| click | 点击按钮触发的事件 | `Function` |

### Slots [​](#slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/backtop) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/backtop.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/backtop.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/59350883?v=4&size=64)](https://github.com/init-qy)[![](https://avatars.githubusercontent.com/u/5701072?v=4&size=64)](https://github.com/Naeemo)[![](https://avatars.githubusercontent.com/u/110765073?v=4&size=64)](https://github.com/fwr220807)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)

[Anchor 锚点](https://element-plus.org/zh-CN/component/anchor)

[Breadcrumb 面包屑](https://element-plus.org/zh-CN/component/breadcrumb)


