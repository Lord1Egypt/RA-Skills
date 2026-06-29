---
name: "breadcrumb"
description: "Breadcrumb 面包屑 -- Element Plus Vue3 桌面端组件。Invoke when user needs Breadcrumb 面包屑 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/breadcrumb.html"
---

---

# Breadcrumb 面包屑 [​](#breadcrumb-面包屑)

更新日志待解决

0

显示当前页面的路径，快速返回之前的任意页面。

## 基础用法 [​](#基础用法)

在 `el-breadcrumb` 中使用 `el-breadcrumb-item` 标签表示从首页开始的每一级。 该组件接受一个 `String` 类型的参数 `separator`来作为分隔符。 默认值为 '/'。

homepage/[promotion management](https://element-plus.org/)/promotion list/promotion detail/

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnJlYWRjcnVtYiBzZXBhcmF0b3I9XCIvXCI+XG4gICAgPGVsLWJyZWFkY3J1bWItaXRlbSA6dG89XCJ7IHBhdGg6ICcvJyB9XCI+aG9tZXBhZ2U8L2VsLWJyZWFkY3J1bWItaXRlbT5cbiAgICA8ZWwtYnJlYWRjcnVtYi1pdGVtPlxuICAgICAgPGEgaHJlZj1cIi9cIj5wcm9tb3Rpb24gbWFuYWdlbWVudDwvYT5cbiAgICA8L2VsLWJyZWFkY3J1bWItaXRlbT5cbiAgICA8ZWwtYnJlYWRjcnVtYi1pdGVtPnByb21vdGlvbiBsaXN0PC9lbC1icmVhZGNydW1iLWl0ZW0+XG4gICAgPGVsLWJyZWFkY3J1bWItaXRlbT5wcm9tb3Rpb24gZGV0YWlsPC9lbC1icmVhZGNydW1iLWl0ZW0+XG4gIDwvZWwtYnJlYWRjcnVtYj5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/breadcrumb/basic.vue)_

vue

```
<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item :to="{ path: '/' }">homepage</el-breadcrumb-item>
    <el-breadcrumb-item>
      <a href="/">promotion management</a>
    </el-breadcrumb-item>
    <el-breadcrumb-item>promotion list</el-breadcrumb-item>
    <el-breadcrumb-item>promotion detail</el-breadcrumb-item>
  </el-breadcrumb>
</template>
```

隐藏源代码

## 图标分隔符 [​](#图标分隔符)

通过设置 `separator-class` 可使用相应的 `iconfont` 作为分隔符，注意这将使 `separator` 失效。

homepagepromotion managementpromotion listpromotion detail

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnJlYWRjcnVtYiA6c2VwYXJhdG9yLWljb249XCJBcnJvd1JpZ2h0XCI+XG4gICAgPGVsLWJyZWFkY3J1bWItaXRlbSA6dG89XCJ7IHBhdGg6ICcvJyB9XCI+aG9tZXBhZ2U8L2VsLWJyZWFkY3J1bWItaXRlbT5cbiAgICA8ZWwtYnJlYWRjcnVtYi1pdGVtPnByb21vdGlvbiBtYW5hZ2VtZW50PC9lbC1icmVhZGNydW1iLWl0ZW0+XG4gICAgPGVsLWJyZWFkY3J1bWItaXRlbT5wcm9tb3Rpb24gbGlzdDwvZWwtYnJlYWRjcnVtYi1pdGVtPlxuICAgIDxlbC1icmVhZGNydW1iLWl0ZW0+cHJvbW90aW9uIGRldGFpbDwvZWwtYnJlYWRjcnVtYi1pdGVtPlxuICA8L2VsLWJyZWFkY3J1bWI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgQXJyb3dSaWdodCB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/breadcrumb/icon.vue)_

vue

```
<template>
  <el-breadcrumb :separator-icon="ArrowRight">
    <el-breadcrumb-item :to="{ path: '/' }">homepage</el-breadcrumb-item>
    <el-breadcrumb-item>promotion management</el-breadcrumb-item>
    <el-breadcrumb-item>promotion list</el-breadcrumb-item>
    <el-breadcrumb-item>promotion detail</el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script lang="ts" setup>
import { ArrowRight } from '@element-plus/icons-vue'
</script>
```

隐藏源代码

## Breadcrumb API [​](#breadcrumb-api)

### Breadcrumb Attributes [​](#breadcrumb-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| separator | 分隔符 | `string` | / |
| separator-icon | 图标分隔符的组件或组件名 | `string` / `Component` | — |

### Breadcrumb Slots [​](#breadcrumb-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | Breadcrumb Item |

## BreadcrumbItem API [​](#breadcrumbitem-api)

### BreadcrumbItem Attributes [​](#breadcrumbitem-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| to | 路由跳转目标，同 `vue-router` 的 `to` 属性 | `string` / `object` | '' |
| replace | 如果设置该属性为 `true`, 导航将不会留下历史记录 | `boolean` | false |

### BreadcrumbItem Slots [​](#breadcrumbitem-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/breadcrumb) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/breadcrumb.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/breadcrumb.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/42489652?v=4&size=64)](https://github.com/GGupzHH)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)

[Backtop 回到顶部](https://element-plus.org/zh-CN/component/backtop)

[Dropdown 下拉菜单](https://element-plus.org/zh-CN/component/dropdown)


