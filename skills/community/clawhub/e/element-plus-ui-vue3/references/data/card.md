---
name: "card"
description: "Card 卡片 -- Element Plus Vue3 桌面端组件。Invoke when user needs Card 卡片 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/card.html"
---

---

# Card 卡片 [​](#card-卡片)

更新日志待解决

2

将信息聚合在卡片容器中展示。

## 基础用法 [​](#基础用法)

卡片包含标题，内容以及操作区域。

Card 组件由 `header` `body` 和 `footer`组成。 `header` 和 `footer`是可选的，其内容取决于一个具名的 slot。

Card name

List item 1

List item 2

List item 3

List item 4

Footer content

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FyZCBzdHlsZT1cIm1heC13aWR0aDogNDgwcHhcIj5cbiAgICA8dGVtcGxhdGUgI2hlYWRlcj5cbiAgICAgIDxkaXYgY2xhc3M9XCJjYXJkLWhlYWRlclwiPlxuICAgICAgICA8c3Bhbj5DYXJkIG5hbWU8L3NwYW4+XG4gICAgICA8L2Rpdj5cbiAgICA8L3RlbXBsYXRlPlxuICAgIDxwIHYtZm9yPVwibyBpbiA0XCIgOmtleT1cIm9cIiBjbGFzcz1cInRleHQgaXRlbVwiPnt7ICdMaXN0IGl0ZW0gJyArIG8gfX08L3A+XG4gICAgPHRlbXBsYXRlICNmb290ZXI+Rm9vdGVyIGNvbnRlbnQ8L3RlbXBsYXRlPlxuICA8L2VsLWNhcmQ+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/card/basic.vue)_

vue

```
<template>
  <el-card style="max-width: 480px">
    <template #header>
      <div class="card-header">
        <span>Card name</span>
      </div>
    </template>
    <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
    <template #footer>Footer content</template>
  </el-card>
</template>
```

隐藏源代码

## 简单卡片 [​](#简单卡片)

卡片可以只有内容区域。

List item 1

List item 2

List item 3

List item 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FyZCBzdHlsZT1cIm1heC13aWR0aDogNDgwcHhcIj5cbiAgICA8cCB2LWZvcj1cIm8gaW4gNFwiIDprZXk9XCJvXCIgY2xhc3M9XCJ0ZXh0IGl0ZW1cIj57eyAnTGlzdCBpdGVtICcgKyBvIH19PC9wPlxuICA8L2VsLWNhcmQ+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/card/simple.vue)_

vue

```
<template>
  <el-card style="max-width: 480px">
    <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
  </el-card>
</template>
```

隐藏源代码

## 有图片内容的卡片 [​](#有图片内容的卡片)

可配置定义更丰富的内容展示。

配置 `body-style` 属性来自定义 `body` 部分的样式。

Yummy hamburger

![](https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FyZCBzdHlsZT1cIm1heC13aWR0aDogNDgwcHhcIj5cbiAgICA8dGVtcGxhdGUgI2hlYWRlcj5ZdW1teSBoYW1idXJnZXI8L3RlbXBsYXRlPlxuICAgIDxpbWdcbiAgICAgIHNyYz1cImh0dHBzOi8vc2hhZG93LmVsZW1lY2RuLmNvbS9hcHAvZWxlbWVudC9oYW1idXJnZXIuOWNmN2IwOTEtNTVlOS0xMWU5LWE5NzYtN2Y0ZDBiMDdlZWY2LnBuZ1wiXG4gICAgICBzdHlsZT1cIndpZHRoOiAxMDAlXCJcbiAgICAvPlxuICA8L2VsLWNhcmQ+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/card/with-images.vue)_

vue

```
<template>
  <el-card style="max-width: 480px">
    <template #header>Yummy hamburger</template>
    <img
      src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
      style="width: 100%"
    />
  </el-card>
</template>
```

隐藏源代码

## 带有阴影效果的卡片 [​](#带有阴影效果的卡片)

你可以定义什么时候展示卡片的阴影效果。

通过 `shadow` 属性设置卡片阴影出现的时机。 该属性的值可以是：`always`、`hover` 或 `never`。

Always

Hover

Never

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTRcIj5cbiAgICA8ZWwtY2FyZCBzdHlsZT1cIndpZHRoOiA0ODBweFwiIHNoYWRvdz1cImFsd2F5c1wiPkFsd2F5czwvZWwtY2FyZD5cbiAgICA8ZWwtY2FyZCBzdHlsZT1cIndpZHRoOiA0ODBweFwiIHNoYWRvdz1cImhvdmVyXCI+SG92ZXI8L2VsLWNhcmQ+XG4gICAgPGVsLWNhcmQgc3R5bGU9XCJ3aWR0aDogNDgwcHhcIiBzaGFkb3c9XCJuZXZlclwiPk5ldmVyPC9lbC1jYXJkPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/card/shadow.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-4">
    <el-card style="width: 480px" shadow="always">Always</el-card>
    <el-card style="width: 480px" shadow="hover">Hover</el-card>
    <el-card style="width: 480px" shadow="never">Never</el-card>
  </div>
</template>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| header | 卡片的标题 你既可以通过设置 header 来修改标题，也可以通过 `slot#header` 传入 DOM 节点 | `string` | — |
| footer 2.4.3 | 卡片页脚。 你既可以通过设置 footer 来修改卡片底部内容，也可以通过 `slot#footer` 传入 DOM 节点 | `string` | — |
| body-style | body 的 CSS 样式 | `object` | — |
| header-class 2.9.8 | card header 的自定义类名 | `string` | — |
| body-class 2.3.10 | body 的自定义类名 | `string` | — |
| footer-class 2.9.8 | footer 的自定义类名 | `string` | — |
| shadow | 卡片阴影显示时机 | `enum` | always |

### Slots [​](#slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |
| header | 卡片标题内容 |
| footer | 卡片页脚内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/card) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/card.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/card.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/140705167?v=4&size=64)](https://github.com/zhongli-kira)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/87003751?v=4&size=64)](https://github.com/faga295)[![](https://avatars.githubusercontent.com/u/110730129?v=4&size=64)](https://github.com/uxuip)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/30256102?v=4&size=64)](https://github.com/leon-kfd)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/75007029?v=4&size=64)](https://github.com/yj-liuzepeng)[![](https://avatars.githubusercontent.com/u/101238421?v=4&size=64)](https://github.com/acyza)[![](https://avatars.githubusercontent.com/u/22659150?v=4&size=64)](https://github.com/ntnyq)

[Calendar 日历](https://element-plus.org/zh-CN/component/calendar)

[Carousel 走马灯](https://element-plus.org/zh-CN/component/carousel)


