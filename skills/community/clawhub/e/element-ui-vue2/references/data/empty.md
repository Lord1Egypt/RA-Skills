---
name: "empty"
description: "Empty 空状态 -- Element UI Vue2 桌面端组件。Invoke when user needs Empty 空状态 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/empty"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/empty#empty-kong-zhuang-tai) Empty 空状态

空状态时的占位提示。

### [¶](https://element.eleme.cn/#/zh-CN/component/empty#ji-chu-yong-fa) 基础用法

描述文字

```
<el-empty description="描述文字"></el-empty>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/empty#zi-ding-yi-tu-pian) 自定义图片

通过设置 `image` 属性传入图片 URL。

![](https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png)

暂无数据

```
<el-empty image="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"></el-empty>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/empty#tu-pian-chi-cun) 图片尺寸

通过设置 `image-size` 属性来控制图片大小。

暂无数据

```
<el-empty :image-size="200"></el-empty>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/empty#di-bu-nei-rong) 底部内容

使用默认插槽可在底部插入内容。

暂无数据

按钮

```
<el-empty>
  <el-button type="primary">按钮</el-button>
</el-empty>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/empty#empty-attributes) Empty Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| image | 图片地址 | string | — | — |
| image-size | 图片大小（宽度） | number | — | — |
| description | 文本描述 | string | — | — |

### [¶](https://element.eleme.cn/#/zh-CN/component/empty#empty-slots) Empty Slots

| Name | 说明 |
| --- | --- |
| default | 自定义底部内容 |
| image | 自定义图片 |
| description | 自定义描述文字 |

Skeleton 骨架屏 Descriptions 描述列表


