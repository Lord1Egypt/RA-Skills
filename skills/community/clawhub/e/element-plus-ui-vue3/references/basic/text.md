---
name: "text"
description: "Text 文本 -- Element Plus Vue3 桌面端组件。Invoke when user needs Text 文本 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/text.html"
---

---

# Text [​](#text)

更新日志待解决

6

文本的常见操作

## 基础用法 [​](#基础用法)

由 `type` 属性来选择 Text 的类型。

DefaultPrimarySuccessInfoWarningDanger

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGV4dCBjbGFzcz1cIm14LTFcIj5EZWZhdWx0PC9lbC10ZXh0PlxuICA8ZWwtdGV4dCBjbGFzcz1cIm14LTFcIiB0eXBlPVwicHJpbWFyeVwiPlByaW1hcnk8L2VsLXRleHQ+XG4gIDxlbC10ZXh0IGNsYXNzPVwibXgtMVwiIHR5cGU9XCJzdWNjZXNzXCI+U3VjY2VzczwvZWwtdGV4dD5cbiAgPGVsLXRleHQgY2xhc3M9XCJteC0xXCIgdHlwZT1cImluZm9cIj5JbmZvPC9lbC10ZXh0PlxuICA8ZWwtdGV4dCBjbGFzcz1cIm14LTFcIiB0eXBlPVwid2FybmluZ1wiPldhcm5pbmc8L2VsLXRleHQ+XG4gIDxlbC10ZXh0IGNsYXNzPVwibXgtMVwiIHR5cGU9XCJkYW5nZXJcIj5EYW5nZXI8L2VsLXRleHQ+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/text/basic.vue)_

vue

```
<template>
  <el-text class="mx-1">Default</el-text>
  <el-text class="mx-1" type="primary">Primary</el-text>
  <el-text class="mx-1" type="success">Success</el-text>
  <el-text class="mx-1" type="info">Info</el-text>
  <el-text class="mx-1" type="warning">Warning</el-text>
  <el-text class="mx-1" type="danger">Danger</el-text>
</template>
```

隐藏源代码

## 尺寸 [​](#尺寸)

使用 `size` 属性配置尺寸，可选的尺寸大小有: `large`, `default` 或 `small`

LargeDefaultSmall

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGV4dCBjbGFzcz1cIm14LTFcIiBzaXplPVwibGFyZ2VcIj5MYXJnZTwvZWwtdGV4dD5cbiAgPGVsLXRleHQgY2xhc3M9XCJteC0xXCI+RGVmYXVsdDwvZWwtdGV4dD5cbiAgPGVsLXRleHQgY2xhc3M9XCJteC0xXCIgc2l6ZT1cInNtYWxsXCI+U21hbGw8L2VsLXRleHQ+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/text/sizes.vue)_

vue

```
<template>
  <el-text class="mx-1" size="large">Large</el-text>
  <el-text class="mx-1">Default</el-text>
  <el-text class="mx-1" size="small">Small</el-text>
</template>
```

隐藏源代码

## 省略 [​](#省略)

通过 `truncated` 属性，在文本超过视图或最大宽度设置时展示省略符。 通过 `line-clamp` 属性控制多行的样式

Self element set width 100px

Squeezed by parent element

The -webkit-line-clamp CSS property
allows limiting of the contents of
a block to the specified number of lines.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGV4dCBjbGFzcz1cInctMTUwcHggbWItMlwiIHRydW5jYXRlZD5cbiAgICBTZWxmIGVsZW1lbnQgc2V0IHdpZHRoIDEwMHB4XG4gIDwvZWwtdGV4dD5cbiAgPGVsLXJvdyBjbGFzcz1cInctMTUwcHggbWItMlwiPlxuICAgIDxlbC10ZXh0IHRydW5jYXRlZD5TcXVlZXplZCBieSBwYXJlbnQgZWxlbWVudDwvZWwtdGV4dD5cbiAgPC9lbC1yb3c+XG4gIDxlbC10ZXh0IGxpbmUtY2xhbXA9XCIyXCI+XG4gICAgVGhlIC13ZWJraXQtbGluZS1jbGFtcCBDU1MgcHJvcGVydHk8YnIgLz5cbiAgICBhbGxvd3MgbGltaXRpbmcgb2YgdGhlIGNvbnRlbnRzIG9mPGJyIC8+XG4gICAgYSBibG9jayB0byB0aGUgc3BlY2lmaWVkIG51bWJlciBvZiBsaW5lcy5cbiAgPC9lbC10ZXh0PlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/text/truncated.vue)_

vue

```
<template>
  <el-text class="w-150px mb-2" truncated>
    Self element set width 100px
  </el-text>
  <el-row class="w-150px mb-2">
    <el-text truncated>Squeezed by parent element</el-text>
  </el-row>
  <el-text line-clamp="2">
    The -webkit-line-clamp CSS property<br />
    allows limiting of the contents of<br />
    a block to the specified number of lines.
  </el-text>
</template>
```

隐藏源代码

## 覆盖 [​](#覆盖)

使用属性 `tag` 覆盖元素

span

This is a paragraph.

**Bold**

_Italic_

This is subscript

This is superscript

Inserted

~~Deleted~~

Marked

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgZGlyZWN0aW9uPVwidmVydGljYWxcIj5cbiAgICA8ZWwtdGV4dD5zcGFuPC9lbC10ZXh0PlxuICAgIDxlbC10ZXh0IHRhZz1cInBcIj5UaGlzIGlzIGEgcGFyYWdyYXBoLjwvZWwtdGV4dD5cbiAgICA8ZWwtdGV4dCB0YWc9XCJiXCI+Qm9sZDwvZWwtdGV4dD5cbiAgICA8ZWwtdGV4dCB0YWc9XCJpXCI+SXRhbGljPC9lbC10ZXh0PlxuICAgIDxlbC10ZXh0PlxuICAgICAgVGhpcyBpc1xuICAgICAgPGVsLXRleHQgdGFnPVwic3ViXCIgc2l6ZT1cInNtYWxsXCI+c3Vic2NyaXB0PC9lbC10ZXh0PlxuICAgIDwvZWwtdGV4dD5cbiAgICA8ZWwtdGV4dD5cbiAgICAgIFRoaXMgaXNcbiAgICAgIDxlbC10ZXh0IHRhZz1cInN1cFwiIHNpemU9XCJzbWFsbFwiPnN1cGVyc2NyaXB0PC9lbC10ZXh0PlxuICAgIDwvZWwtdGV4dD5cbiAgICA8ZWwtdGV4dCB0YWc9XCJpbnNcIj5JbnNlcnRlZDwvZWwtdGV4dD5cbiAgICA8ZWwtdGV4dCB0YWc9XCJkZWxcIj5EZWxldGVkPC9lbC10ZXh0PlxuICAgIDxlbC10ZXh0IHRhZz1cIm1hcmtcIj5NYXJrZWQ8L2VsLXRleHQ+XG4gIDwvZWwtc3BhY2U+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/text/override.vue)_

vue

```
<template>
  <el-space direction="vertical">
    <el-text>span</el-text>
    <el-text tag="p">This is a paragraph.</el-text>
    <el-text tag="b">Bold</el-text>
    <el-text tag="i">Italic</el-text>
    <el-text>
      This is
      <el-text tag="sub" size="small">subscript</el-text>
    </el-text>
    <el-text>
      This is
      <el-text tag="sup" size="small">superscript</el-text>
    </el-text>
    <el-text tag="ins">Inserted</el-text>
    <el-text tag="del">Deleted</el-text>
    <el-text tag="mark">Marked</el-text>
  </el-space>
</template>
```

隐藏源代码

## 混合使用 [​](#混合使用)

混合使用 Text 组件

Element-Plus

Rate

This is text mixed icon and component Button

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgZGlyZWN0aW9uPVwidmVydGljYWxcIj5cbiAgICA8ZWwtdGV4dD5cbiAgICAgIDxlbC1pY29uPlxuICAgICAgICA8RWxlbWVudFBsdXMgLz5cbiAgICAgIDwvZWwtaWNvbj5cbiAgICAgIEVsZW1lbnQtUGx1c1xuICAgIDwvZWwtdGV4dD5cbiAgICA8ZWwtcm93PlxuICAgICAgPGVsLXRleHQ+UmF0ZTwvZWwtdGV4dD5cbiAgICAgIDxlbC1yYXRlIGNsYXNzPVwibWwtMVwiIC8+XG4gICAgPC9lbC1yb3c+XG4gICAgPGVsLXRleHQ+XG4gICAgICBUaGlzIGlzIHRleHQgbWl4ZWQgaWNvblxuICAgICAgPGVsLWljb24+XG4gICAgICAgIDxCZWxsIC8+XG4gICAgICA8L2VsLWljb24+XG4gICAgICBhbmQgY29tcG9uZW50XG4gICAgICA8ZWwtYnV0dG9uPkJ1dHRvbjwvZWwtYnV0dG9uPlxuICAgIDwvZWwtdGV4dD5cbiAgPC9lbC1zcGFjZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBCZWxsLCBFbGVtZW50UGx1cyB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/text/mixed.vue)_

vue

```
<template>
  <el-space direction="vertical">
    <el-text>
      <el-icon>
        <ElementPlus />
      </el-icon>
      Element-Plus
    </el-text>
    <el-row>
      <el-text>Rate</el-text>
      <el-rate class="ml-1" />
    </el-row>
    <el-text>
      This is text mixed icon
      <el-icon>
        <Bell />
      </el-icon>
      and component
      <el-button>Button</el-button>
    </el-text>
  </el-space>
</template>

<script lang="ts" setup>
import { Bell, ElementPlus } from '@element-plus/icons-vue'
</script>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 描述 | 类型 | 默认值 |
| --- | --- | --- | --- |
| type | 类型 | `enum` | — |
| size | 大小 | `enum` | default |
| truncated | 显示省略号 | `boolean` | false |
| line-clamp 2.4.0 | 最大行数 | `string` / `number` | — |
| tag | 自定义元素标签 | `string` | span |

### Slots [​](#slots)

| 名称 | 详情 |
| --- | --- |
| default | 默认内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/text) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/text.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/text.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)

[Link 链接](https://element-plus.org/zh-CN/component/link)

[Scrollbar 滚动条](https://element-plus.org/zh-CN/component/scrollbar)


