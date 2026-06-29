---
name: "link"
description: "Link 文字链接 -- Element UI Vue2 桌面端组件。Invoke when user needs Link 文字链接 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/link"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/link#link-wen-zi-lian-jie) Link 文字链接

文字超链接

### [¶](https://element.eleme.cn/#/zh-CN/component/link#ji-chu-yong-fa) 基础用法

基础的文字链接用法。

[默认链接](https://element.eleme.io/) 主要链接 成功链接 警告链接 危险链接 信息链接

```
<div>
  <el-link href="https://element.eleme.io" target="_blank">默认链接</el-link>
  <el-link type="primary">主要链接</el-link>
  <el-link type="success">成功链接</el-link>
  <el-link type="warning">警告链接</el-link>
  <el-link type="danger">危险链接</el-link>
  <el-link type="info">信息链接</el-link>
</div>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/link#jin-yong-zhuang-tai) 禁用状态

文字链接不可用状态。

默认链接 主要链接 成功链接 警告链接 危险链接 信息链接

```
<div>
  <el-link disabled>默认链接</el-link>
  <el-link type="primary" disabled>主要链接</el-link>
  <el-link type="success" disabled>成功链接</el-link>
  <el-link type="warning" disabled>警告链接</el-link>
  <el-link type="danger" disabled>危险链接</el-link>
  <el-link type="info" disabled>信息链接</el-link>
</div>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/link#xia-hua-xian) 下划线

文字链接下划线。

无下划线 有下划线

```
<div>
  <el-link :underline="false">无下划线</el-link>
  <el-link>有下划线</el-link>
</div>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/link#tu-biao) 图标

带图标的文字链接可增强辨识度。

编辑 查看

```
<div>
  <el-link icon="el-icon-edit">编辑</el-link>
  <el-link>查看<i class="el-icon-view el-icon--right"></i> </el-link>
</div>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/link#attributes) Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| type | 类型 | string | primary / success / warning / danger / info | default |
| underline | 是否下划线 | boolean | — | true |
| disabled | 是否禁用状态 | boolean | — | false |
| href | 原生 href 属性 | string | — | \- |
| icon | 图标类名 | string | — | \- |

Button 按钮 Radio 单选框


