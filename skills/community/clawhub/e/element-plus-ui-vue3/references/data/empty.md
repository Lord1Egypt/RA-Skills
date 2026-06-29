---
name: "empty"
description: "Empty 空状态 -- Element Plus Vue3 桌面端组件。Invoke when user needs Empty 空状态 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/empty.html"
---

---

# Empty 空状态 [​](#empty-空状态)

更新日志待解决

5

空状态时的占位提示。

## 基础用法 [​](#基础用法)

description

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZW1wdHkgZGVzY3JpcHRpb249XCJkZXNjcmlwdGlvblwiIC8+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/empty/basic-usage.vue)_

vue

```
<template>
  <el-empty description="description" />
</template>
```

隐藏源代码

## 自定义图片 [​](#自定义图片)

通过设置 `image` 属性传入图片 URL。

![](https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png)

No Data

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZW1wdHlcbiAgICBpbWFnZT1cImh0dHBzOi8vc2hhZG93LmVsZW1lY2RuLmNvbS9hcHAvZWxlbWVudC9oYW1idXJnZXIuOWNmN2IwOTEtNTVlOS0xMWU5LWE5NzYtN2Y0ZDBiMDdlZWY2LnBuZ1wiXG4gIC8+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/empty/custom-image.vue)_

vue

```
<template>
  <el-empty
    image="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
  />
</template>
```

隐藏源代码

## 图片尺寸 [​](#图片尺寸)

通过使用 `image-size` 属性来控制图片大小。

No Data

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZW1wdHkgOmltYWdlLXNpemU9XCIyMDBcIiAvPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/empty/image-size.vue)_

vue

```
<template>
  <el-empty :image-size="200" />
</template>
```

隐藏源代码

## 底部内容 [​](#底部内容)

使用默认插槽可在底部插入内容。

No Data

Button

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZW1wdHk+XG4gICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiPkJ1dHRvbjwvZWwtYnV0dG9uPlxuICA8L2VsLWVtcHR5PlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/empty/bottom-content.vue)_

vue

```
<template>
  <el-empty>
    <el-button type="primary">Button</el-button>
  </el-empty>
</template>
```

隐藏源代码

## 自定义样式 [​](#自定义样式)

您可以为empty组件设置自定义样式。 使用 `css/scss` 语言来更改全局或局部颜色。 我们设置了一些全局颜色变量：`--el-empty-fill-color-0`、`--el-empty-fill-color-1`、`--el-empty-fill-color-2`、……、`--el-empty-fill-color-9`。 您可以使用类似 `:root { --el-empty-fill-color-0: red; --el-empty-fill-color-1: blue; }` 等变量。 但通常，如果你想要更改样式，你需要更改所有颜色，因为这些颜色是一个组合。

### 默认变量 [​](#默认变量)

| 变量 | 颜色 |
| --- | --- |
| \--el-empty-fill-color-0 | var(--el-color-white) |
| \--el-empty-fill-color-1 | #fcfcfd |
| \--el-empty-fill-color-2 | #f8f9fb |
| \--el-empty-fill-color-3 | #f7f8fc |
| \--el-empty-fill-color-4 | #eeeff3 |
| \--el-empty-fill-color-5 | #edeef2 |
| \--el-empty-fill-color-6 | #e9ebef |
| \--el-empty-fill-color-7 | #e5e7e9 |
| \--el-empty-fill-color-8 | #e0e3e9 |
| \--el-empty-fill-color-9 | #d5d7de |

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| image | empty 组件的图像地址 | `string` | '' |
| image-size | empty 组件的图像尺寸（宽度） | `number` | — |
| description | empty 组件的描述信息 | `string` | '' |

### 插槽 [​](#插槽)

| 插槽名 | 描述说明 |
| --- | --- |
| default | 作为底部内容的内容 |
| image | 作为图像的内容 |
| description | 作为描述的内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/empty) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/empty.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/empty.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/100674?v=4&size=64)](https://github.com/d--j)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/33497338?v=4&size=64)](https://github.com/MoConWu)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)

[Descriptions 描述列表](https://element-plus.org/zh-CN/component/descriptions)

[Image 图片](https://element-plus.org/zh-CN/component/image)


