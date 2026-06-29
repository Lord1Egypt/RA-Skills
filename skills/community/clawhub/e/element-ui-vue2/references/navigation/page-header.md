---
name: "page-header"
description: "PageHeader 页头 -- Element UI Vue2 桌面端组件。Invoke when user needs PageHeader 页头 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/page-header"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/page-header#pageheader-ye-tou) PageHeader 页头

如果页面的路径比较简单，推荐使用页头组件而非面包屑组件。

### [¶](https://element.eleme.cn/#/zh-CN/component/page-header#ji-chu) 基础

返回

详情页面

```
<el-page-header @back="goBack" content="详情页面">
</el-page-header>

<script>
  export default {
    methods: {
      goBack() {
        console.log('go back');
      }
    }
  }
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/page-header#attributes) Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| title | 标题 | string | — | 返回 |
| content | 内容 | string | — | — |

### [¶](https://element.eleme.cn/#/zh-CN/component/page-header#events) Events

| 事件名称 | 说明 | 回调参数 |
| --- | --- | --- |
| back | 点击左侧区域触发 | — |

### [¶](https://element.eleme.cn/#/zh-CN/component/page-header#slots) Slots

| 事件名称 | 说明 |
| --- | --- |
| title | 标题内容 |
| content | 内容 |

Breadcrumb 面包屑 Dropdown 下拉菜单


