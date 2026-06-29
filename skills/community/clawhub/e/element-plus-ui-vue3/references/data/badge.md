---
name: "badge"
description: "Badge 标记 -- Element Plus Vue3 桌面端组件。Invoke when user needs Badge 标记 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/badge.html"
---

---

# Badge 徽章 [​](#badge-徽章)

更新日志待解决

2

按钮和图标上的数字或状态标记。

## 基础用法 [​](#基础用法)

可以用来展示新消息的数量。

数量值可接受 Number 或 String。

comments12

replies3

comments1

replies2

custom background1

Click Me

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYmFkZ2UgOnZhbHVlPVwiMTJcIiBjbGFzcz1cIml0ZW1cIj5cbiAgICA8ZWwtYnV0dG9uPmNvbW1lbnRzPC9lbC1idXR0b24+XG4gIDwvZWwtYmFkZ2U+XG4gIDxlbC1iYWRnZSA6dmFsdWU9XCIzXCIgY2xhc3M9XCJpdGVtXCI+XG4gICAgPGVsLWJ1dHRvbj5yZXBsaWVzPC9lbC1idXR0b24+XG4gIDwvZWwtYmFkZ2U+XG4gIDxlbC1iYWRnZSA6dmFsdWU9XCIxXCIgY2xhc3M9XCJpdGVtXCIgdHlwZT1cInByaW1hcnlcIj5cbiAgICA8ZWwtYnV0dG9uPmNvbW1lbnRzPC9lbC1idXR0b24+XG4gIDwvZWwtYmFkZ2U+XG4gIDxlbC1iYWRnZSA6dmFsdWU9XCIyXCIgY2xhc3M9XCJpdGVtXCIgdHlwZT1cIndhcm5pbmdcIj5cbiAgICA8ZWwtYnV0dG9uPnJlcGxpZXM8L2VsLWJ1dHRvbj5cbiAgPC9lbC1iYWRnZT5cbiAgPGVsLWJhZGdlIDp2YWx1ZT1cIjFcIiBjbGFzcz1cIml0ZW1cIiBjb2xvcj1cImdyZWVuXCI+XG4gICAgPGVsLWJ1dHRvbj5jdXN0b20gYmFja2dyb3VuZDwvZWwtYnV0dG9uPlxuICA8L2VsLWJhZGdlPlxuICA8ZWwtZHJvcGRvd24gdHJpZ2dlcj1cImNsaWNrXCI+XG4gICAgPHNwYW4gY2xhc3M9XCJlbC1kcm9wZG93bi1saW5rXCI+XG4gICAgICBDbGljayBNZVxuICAgICAgPGVsLWljb24gY2xhc3M9XCJlbC1pY29uLS1yaWdodFwiPjxjYXJldC1ib3R0b20gLz48L2VsLWljb24+XG4gICAgPC9zcGFuPlxuICAgIDx0ZW1wbGF0ZSAjZHJvcGRvd24+XG4gICAgICA8ZWwtZHJvcGRvd24tbWVudT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gY2xhc3M9XCJjbGVhcmZpeFwiPlxuICAgICAgICAgIGNvbW1lbnRzXG4gICAgICAgICAgPGVsLWJhZGdlIGNsYXNzPVwibWFya1wiIDp2YWx1ZT1cIjEyXCIgLz5cbiAgICAgICAgPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSBjbGFzcz1cImNsZWFyZml4XCI+XG4gICAgICAgICAgcmVwbGllc1xuICAgICAgICAgIDxlbC1iYWRnZSBjbGFzcz1cIm1hcmtcIiA6dmFsdWU9XCIzXCIgLz5cbiAgICAgICAgPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgPC9lbC1kcm9wZG93bi1tZW51PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtZHJvcGRvd24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgQ2FyZXRCb3R0b20gfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLml0ZW0ge1xuICBtYXJnaW4tdG9wOiAxMHB4O1xuICBtYXJnaW4tcmlnaHQ6IDMwcHg7XG59XG5cbi5lbC1kcm9wZG93biB7XG4gIG1hcmdpbi10b3A6IDEuMXJlbTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/badge/basic.vue)_

vue

```
<template>
  <el-badge :value="12" class="item">
    <el-button>comments</el-button>
  </el-badge>
  <el-badge :value="3" class="item">
    <el-button>replies</el-button>
  </el-badge>
  <el-badge :value="1" class="item" type="primary">
    <el-button>comments</el-button>
  </el-badge>
  <el-badge :value="2" class="item" type="warning">
    <el-button>replies</el-button>
  </el-badge>
  <el-badge :value="1" class="item" color="green">
    <el-button>custom background</el-button>
  </el-badge>
  <el-dropdown trigger="click">
    <span class="el-dropdown-link">
      Click Me
      <el-icon class="el-icon--right"><caret-bottom /></el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item class="clearfix">
          comments
          <el-badge class="mark" :value="12" />
        </el-dropdown-item>
        <el-dropdown-item class="clearfix">
          replies
          <el-badge class="mark" :value="3" />
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script lang="ts" setup>
import { CaretBottom } from '@element-plus/icons-vue'
</script>

<style scoped>
.item {
  margin-top: 10px;
  margin-right: 30px;
}

.el-dropdown {
  margin-top: 1.1rem;
}
</style>
```

隐藏源代码

## 最大值 [​](#最大值)

你还可以自定义最大值

由 max 属性定义，接受 Number 值。 请注意，仅在值也是 Number 时起作用。

comments99+

replies10+

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYmFkZ2UgOnZhbHVlPVwiMjAwXCIgOm1heD1cIjk5XCIgY2xhc3M9XCJpdGVtXCI+XG4gICAgPGVsLWJ1dHRvbj5jb21tZW50czwvZWwtYnV0dG9uPlxuICA8L2VsLWJhZGdlPlxuICA8ZWwtYmFkZ2UgOnZhbHVlPVwiMTAwXCIgOm1heD1cIjEwXCIgY2xhc3M9XCJpdGVtXCI+XG4gICAgPGVsLWJ1dHRvbj5yZXBsaWVzPC9lbC1idXR0b24+XG4gIDwvZWwtYmFkZ2U+XG48L3RlbXBsYXRlPlxuXG48c3R5bGUgc2NvcGVkPlxuLml0ZW0ge1xuICBtYXJnaW4tdG9wOiAxMHB4O1xuICBtYXJnaW4tcmlnaHQ6IDQwcHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/badge/max.vue)_

vue

```
<template>
  <el-badge :value="200" :max="99" class="item">
    <el-button>comments</el-button>
  </el-badge>
  <el-badge :value="100" :max="10" class="item">
    <el-button>replies</el-button>
  </el-badge>
</template>

<style scoped>
.item {
  margin-top: 10px;
  margin-right: 40px;
}
</style>
```

隐藏源代码

## 自定义显示内容 [​](#自定义显示内容)

你也可以展示除数字以外你想要展示的任何值。 或者您可以使用 `content` 栏位自定义内容。

当 value 是 String 时，可以显示自定义文字。 或者使用 `content` 插槽。

commentsnew

replieshot

share

99

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYmFkZ2UgdmFsdWU9XCJuZXdcIiBjbGFzcz1cIml0ZW1cIj5cbiAgICA8ZWwtYnV0dG9uPmNvbW1lbnRzPC9lbC1idXR0b24+XG4gIDwvZWwtYmFkZ2U+XG4gIDxlbC1iYWRnZSB2YWx1ZT1cImhvdFwiIGNsYXNzPVwiaXRlbVwiPlxuICAgIDxlbC1idXR0b24+cmVwbGllczwvZWwtYnV0dG9uPlxuICA8L2VsLWJhZGdlPlxuICA8ZWwtYmFkZ2UgdmFsdWU9XCI5OVwiIGNsYXNzPVwiaXRlbVwiPlxuICAgIDxlbC1idXR0b24+c2hhcmU8L2VsLWJ1dHRvbj5cbiAgICA8dGVtcGxhdGUgI2NvbnRlbnQ9XCJ7IHZhbHVlIH1cIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJjdXN0b20tY29udGVudFwiPlxuICAgICAgICA8ZWwtaWNvbj5cbiAgICAgICAgICA8TWVzc2FnZSAvPlxuICAgICAgICA8L2VsLWljb24+XG4gICAgICAgIDxzcGFuPnt7IHZhbHVlIH19PC9zcGFuPlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1iYWRnZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5pdGVtIHtcbiAgbWFyZ2luLXRvcDogMTBweDtcbiAgbWFyZ2luLXJpZ2h0OiA0MHB4O1xufVxuXG4uY3VzdG9tLWNvbnRlbnQge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgZ2FwOiA0cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/badge/customize.vue)_

vue

```
<template>
  <el-badge value="new" class="item">
    <el-button>comments</el-button>
  </el-badge>
  <el-badge value="hot" class="item">
    <el-button>replies</el-button>
  </el-badge>
  <el-badge value="99" class="item">
    <el-button>share</el-button>
    <template #content="{ value }">
      <div class="custom-content">
        <el-icon>
          <Message />
        </el-icon>
        <span>{{ value }}</span>
      </div>
    </template>
  </el-badge>
</template>

<script setup lang="ts">
import { Message } from '@element-plus/icons-vue'
</script>

<style scoped>
.item {
  margin-top: 10px;
  margin-right: 40px;
}

.custom-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
</style>
```

隐藏源代码

## 小红点 [​](#小红点)

通过一个小红点标记来告知用户有新内容。

使用 `is-dot` 属性。 是个布尔值。

query

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYmFkZ2UgaXMtZG90IGNsYXNzPVwiaXRlbVwiPnF1ZXJ5PC9lbC1iYWRnZT5cbiAgPGVsLWJhZGdlIGlzLWRvdCBjbGFzcz1cIml0ZW1cIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwic2hhcmUtYnV0dG9uXCIgOmljb249XCJTaGFyZVwiIHR5cGU9XCJwcmltYXJ5XCIgLz5cbiAgPC9lbC1iYWRnZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBTaGFyZSB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uaXRlbSB7XG4gIG1hcmdpbi10b3A6IDEwcHg7XG4gIG1hcmdpbi1yaWdodDogNDBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/badge/dot.vue)_

vue

```
<template>
  <el-badge is-dot class="item">query</el-badge>
  <el-badge is-dot class="item">
    <el-button class="share-button" :icon="Share" type="primary" />
  </el-badge>
</template>

<script lang="ts" setup>
import { Share } from '@element-plus/icons-vue'
</script>

<style scoped>
.item {
  margin-top: 10px;
  margin-right: 40px;
}
</style>
```

隐藏源代码

## 偏移量 2.7.0 [​](#偏移量)

设置徽章点的偏移，格式是\[左，顶部\]， 代表状态点从左侧和默认位置顶部的偏移。

offset1

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYmFkZ2UgY2xhc3M9XCJpdGVtXCIgOnZhbHVlPVwiMVwiIDpvZmZzZXQ9XCJbMTAsIDVdXCI+XG4gICAgPGVsLWJ1dHRvbj4gb2Zmc2V0PC9lbC1idXR0b24+XG4gIDwvZWwtYmFkZ2U+XG48L3RlbXBsYXRlPlxuXG48c3R5bGUgc2NvcGVkPlxuLml0ZW0ge1xuICBtYXJnaW4tdG9wOiAxMHB4O1xuICBtYXJnaW4tcmlnaHQ6IDMwcHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/badge/offset.vue)_

vue

```
<template>
  <el-badge class="item" :value="1" :offset="[10, 5]">
    <el-button> offset</el-button>
  </el-badge>
</template>

<style scoped>
.item {
  margin-top: 10px;
  margin-right: 30px;
}
</style>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| value | 显示值 | `string` / `number` | '' |
| max | 最大值，超过最大值会显示 `{max}+`。 只有当 value 是数字类型时起作用。 | `number` | 99 |
| is-dot | 是否显示小圆点。 | `boolean` | false |
| hidden | 是否隐藏 Badge。 | `boolean` | false |
| type | badge 类型。 | `enum` | danger |
| show-zero 2.6.0 | 值为零时是否显示 Badge | `boolean` | true |
| color 2.6.3 | 背景色 | `string` |  |
| offset 2.7.0 | badge 的偏移量 | `array` | \[0, 0\] |
| badge-style 2.7.1 | 自定义 badge 样式 | `object` | — |
| badge-class 2.7.1 | 自定义 badge 类名 | `string` | — |

### Slots [​](#slots)

| 插槽名 | 说明 | 类型 |
| --- | --- | --- |
| default | 自定义默认内容 | \- |
| content 2.9.1 | 自定义显示内容 | `object` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/badge) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/badge.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/badge.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/19898669?v=4&size=64)](https://github.com/lxw15337674)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/74746021?v=4&size=64)](https://github.com/xing403)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/66096254?v=4&size=64)](https://github.com/IceyWu)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/134276765?v=4&size=64)](https://github.com/zwgwf)[![](https://avatars.githubusercontent.com/u/2755933?v=4&size=64)](https://github.com/BiosSun)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/39764402?v=4&size=64)](https://github.com/LyyZzzz)[![](https://avatars.githubusercontent.com/u/1532716?v=4&size=64)](https://github.com/godxiaoji)

[Avatar 头像](https://element-plus.org/zh-CN/component/avatar)

[Calendar 日历](https://element-plus.org/zh-CN/component/calendar)


