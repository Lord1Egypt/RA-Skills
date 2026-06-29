---
name: "badge"
description: "Badge 标记 -- Element UI Vue2 桌面端组件。Invoke when user needs Badge 标记 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/badge"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/badge#badge-biao-ji) Badge 标记

出现在按钮、图标旁的数字或状态标记。

### [¶](https://element.eleme.cn/#/zh-CN/component/badge#ji-chu-yong-fa) 基础用法

展示新消息数量。

评论12

回复3

评论1

回复2

点我查看

-   评论

    12

-   回复

    3

定义`value`属性，它接受`Number`或者`String`。

```
<el-badge :value="12" class="item">
  <el-button size="small">评论</el-button>
</el-badge>
<el-badge :value="3" class="item">
  <el-button size="small">回复</el-button>
</el-badge>
<el-badge :value="1" class="item" type="primary">
  <el-button size="small">评论</el-button>
</el-badge>
<el-badge :value="2" class="item" type="warning">
  <el-button size="small">回复</el-button>
</el-badge>

<el-dropdown trigger="click">
  <span class="el-dropdown-link">
    点我查看<i class="el-icon-caret-bottom el-icon--right"></i>
  </span>
  <el-dropdown-menu slot="dropdown">
    <el-dropdown-item class="clearfix">
      评论
      <el-badge class="mark" :value="12" />
    </el-dropdown-item>
    <el-dropdown-item class="clearfix">
      回复
      <el-badge class="mark" :value="3" />
    </el-dropdown-item>
  </el-dropdown-menu>
</el-dropdown>

<style>
.item {
  margin-top: 10px;
  margin-right: 40px;
}
</style>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/badge#zui-da-zhi) 最大值

可自定义最大值。

评论99+

回复10+

由`max`属性定义，它接受一个`Number`，需要注意的是，只有当`value`为`Number`时，它才会生效。

```
<el-badge :value="200" :max="99" class="item">
  <el-button size="small">评论</el-button>
</el-badge>
<el-badge :value="100" :max="10" class="item">
  <el-button size="small">回复</el-button>
</el-badge>

<style>
.item {
  margin-top: 10px;
  margin-right: 40px;
}
</style>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/badge#zi-ding-yi-nei-rong) 自定义内容

可以显示数字以外的文本内容。

评论new

回复hot

定义`value`为`String`类型是时可以用于显示自定义文本。

```
<el-badge value="new" class="item">
  <el-button size="small">评论</el-button>
</el-badge>
<el-badge value="hot" class="item">
  <el-button size="small">回复</el-button>
</el-badge>

<style>
.item {
  margin-top: 10px;
  margin-right: 40px;
}
</style>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/badge#xiao-hong-dian) 小红点

以红点的形式标注需要关注的内容。

数据查询

除了数字外，设置`is-dot`属性，它接受一个`Boolean`。

```
<el-badge is-dot class="item">数据查询</el-badge>
<el-badge is-dot class="item">
  <el-button class="share-button" icon="el-icon-share" type="primary"></el-button>
</el-badge>

<style>
.item {
  margin-top: 10px;
  margin-right: 40px;
}
</style>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/badge#attributes) Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| value | 显示值 | string, number | — | — |
| max | 最大值，超过最大值会显示 '{max}+'，要求 value 是 Number 类型 | number | — | — |
| is-dot | 小圆点 | boolean | — | false |
| hidden | 隐藏 badge | boolean | — | false |
| type | 类型 | string | primary / success / warning / danger / info | — |

Pagination 分页 Avatar 头像


