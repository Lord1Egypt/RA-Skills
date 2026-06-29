---
name: "breadcrumb"
description: "Breadcrumb 面包屑 -- Element UI Vue2 桌面端组件。Invoke when user needs Breadcrumb 面包屑 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/breadcrumb"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/breadcrumb#breadcrumb-mian-bao-xie) Breadcrumb 面包屑

显示当前页面的路径，快速返回之前的任意页面。

### [¶](https://element.eleme.cn/#/zh-CN/component/breadcrumb#ji-chu-yong-fa) 基础用法

适用广泛的基础用法。

首页/ [活动管理](https://element.eleme.cn/)/ 活动列表/ 活动详情/

在`el-breadcrumb`中使用`el-breadcrumb-item`标签表示从首页开始的每一级。Element 提供了一个`separator`属性，在`el-breadcrumb`标签中设置它来决定分隔符，它只能是字符串，默认为斜杠`/`。

```
<el-breadcrumb separator="/">
  <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
  <el-breadcrumb-item><a href="/">活动管理</a></el-breadcrumb-item>
  <el-breadcrumb-item>活动列表</el-breadcrumb-item>
  <el-breadcrumb-item>活动详情</el-breadcrumb-item>
</el-breadcrumb>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/breadcrumb#tu-biao-fen-ge-fu) 图标分隔符

首页 活动管理 活动列表 活动详情

通过设置 `separator-class` 可使用相应的 `iconfont` 作为分隔符，注意这将使 `separator` 设置失效

```
<el-breadcrumb separator-class="el-icon-arrow-right">
  <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
  <el-breadcrumb-item>活动管理</el-breadcrumb-item>
  <el-breadcrumb-item>活动列表</el-breadcrumb-item>
  <el-breadcrumb-item>活动详情</el-breadcrumb-item>
</el-breadcrumb>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/breadcrumb#breadcrumb-attributes) Breadcrumb Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| separator | 分隔符 | string | — | 斜杠'/' |
| separator-class | 图标分隔符 class | string | — | \- |

### [¶](https://element.eleme.cn/#/zh-CN/component/breadcrumb#breadcrumb-item-attributes) Breadcrumb Item Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| to | 路由跳转对象，同 `vue-router` 的 `to` | string/object | — | — |
| replace | 在使用 to 进行路由跳转时，启用 replace 将不会向 history 添加新记录 | boolean | — | false |

Tabs 标签页 PageHeader 页头


