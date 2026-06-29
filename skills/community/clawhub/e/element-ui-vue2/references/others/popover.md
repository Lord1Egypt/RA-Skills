---
name: "popover"
description: "Popover 弹出框 -- Element UI Vue2 桌面端组件。Invoke when user needs Popover 弹出框 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/popover"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/popover#popover-dan-chu-kuang) Popover 弹出框

### [¶](https://element.eleme.cn/#/zh-CN/component/popover#ji-chu-yong-fa) 基础用法

Popover 的属性与 Tooltip 很类似，它们都是基于`Vue-popper`开发的，因此对于重复属性，请参考 Tooltip 的文档，在此文档中不做详尽解释。

标题

这是一段内容,这是一段内容,这是一段内容,这是一段内容。

hover 激活

标题

这是一段内容,这是一段内容,这是一段内容,这是一段内容。

click 激活 focus 激活

标题

这是一段内容,这是一段内容,这是一段内容,这是一段内容。

手动激活

`trigger`属性用于设置何时触发 Popover，支持四种触发方式：`hover`，`click`，`focus` 和 `manual`。对于触发 Popover 的元素，有两种写法：使用 `slot="reference"` 的具名插槽，或使用自定义指令`v-popover`指向 Popover 的索引`ref`。

```
<template>
  <el-popover
    placement="top-start"
    title="标题"
    width="200"
    trigger="hover"
    content="这是一段内容,这是一段内容,这是一段内容,这是一段内容。">
    <el-button slot="reference">hover 激活</el-button>
  </el-popover>

  <el-popover
    placement="bottom"
    title="标题"
    width="200"
    trigger="click"
    content="这是一段内容,这是一段内容,这是一段内容,这是一段内容。">
    <el-button slot="reference">click 激活</el-button>
  </el-popover>

  <el-popover
    ref="popover"
    placement="right"
    title="标题"
    width="200"
    trigger="focus"
    content="这是一段内容,这是一段内容,这是一段内容,这是一段内容。">
  </el-popover>
  <el-button v-popover:popover>focus 激活</el-button>

  <el-popover
    placement="bottom"
    title="标题"
    width="200"
    trigger="manual"
    content="这是一段内容,这是一段内容,这是一段内容,这是一段内容。"
    v-model="visible">
    <el-button slot="reference" @click="visible = !visible">手动激活</el-button>
  </el-popover>
</template>

<script>
  export default {
    data() {
      return {
        visible: false
      };
    }
  };
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/popover#qian-tao-xin-xi) 嵌套信息

可以在 Popover 中嵌套多种类型信息，以下为嵌套表格的例子。

|
日期

 |

姓名

 |

地址

 |
| --- | --- | --- |

<table cellspacing="0" cellpadding="0" border="0" class="el-table__body" style="width: 550px;"><colgroup><col name="el-table_1_column_1" width="150"><col name="el-table_1_column_2" width="100"><col name="el-table_1_column_3" width="300"></colgroup><tbody><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-04</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-01</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-03</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr></tbody></table>

click 激活

利用分发取代`content`属性

```
<el-popover
  placement="right"
  width="400"
  trigger="click">
  <el-table :data="gridData">
    <el-table-column width="150" property="date" label="日期"></el-table-column>
    <el-table-column width="100" property="name" label="姓名"></el-table-column>
    <el-table-column width="300" property="address" label="地址"></el-table-column>
  </el-table>
  <el-button slot="reference">click 激活</el-button>
</el-popover>

<script>
  export default {
    data() {
      return {
        gridData: [{
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-04',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-01',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }]
      };
    }
  };
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/popover#qian-tao-cao-zuo) 嵌套操作

当然，你还可以嵌套操作，这相比 Dialog 更为轻量：

这是一段内容这是一段内容确定删除吗？

取消 确定

删除

```
<el-popover
  placement="top"
  width="160"
  v-model="visible">
  <p>这是一段内容这是一段内容确定删除吗？</p>
  <div style="text-align: right; margin: 0">
    <el-button size="mini" type="text" @click="visible = false">取消</el-button>
    <el-button type="primary" size="mini" @click="visible = false">确定</el-button>
  </div>
  <el-button slot="reference">删除</el-button>
</el-popover>

<script>
  export default {
    data() {
      return {
        visible: false,
      };
    }
  }
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/popover#attributes) Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| trigger | 触发方式 | String | click/focus/hover/manual | click |
| title | 标题 | String | — | — |
| content | 显示的内容，也可以通过 `slot` 传入 DOM | String | — | — |
| width | 宽度 | String, Number | — | 最小宽度 150px |
| placement | 出现位置 | String | top/top-start/top-end/bottom/bottom-start/bottom-end/left/left-start/left-end/right/right-start/right-end | bottom |
| disabled | Popover 是否可用 | Boolean | — | false |
| value / v-model | 状态是否可见 | Boolean | — | false |
| offset | 出现位置的偏移量 | Number | — | 0 |
| transition | 定义渐变动画 | String | — | fade-in-linear |
| visible-arrow | 是否显示 Tooltip 箭头，更多参数可见[Vue-popper](https://github.com/element-component/vue-popper) | Boolean | — | true |
| popper-options | [popper.js](https://popper.js.org/docs/v2/) 的参数 | Object | 参考 [popper.js](https://popper.js.org/docs/v2/) 文档 | `{ boundariesElement: 'body', gpuAcceleration: false }` |
| popper-class | 为 popper 添加类名 | String | — | — |
| open-delay | 触发方式为 hover 时的显示延迟，单位为毫秒 | Number | — | — |
| close-delay | 触发方式为 hover 时的隐藏延迟，单位为毫秒 | number | — | 200 |
| tabindex | Popover 组件的 [tabindex](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/tabindex) | number | — | 0 |

### [¶](https://element.eleme.cn/#/zh-CN/component/popover#slot) Slot

| 参数 | 说明 |
| --- | --- |
| — | Popover 内嵌 HTML 文本 |
| reference | 触发 Popover 显示的 HTML 元素 |

### [¶](https://element.eleme.cn/#/zh-CN/component/popover#events) Events

| 事件名称 | 说明 | 回调参数 |
| --- | --- | --- |
| show | 显示时触发 | — |
| after-enter | 显示动画播放完毕后触发 | — |
| hide | 隐藏时触发 | — |
| after-leave | 隐藏动画播放完毕后触发 | — |

Tooltip 文字提示 Popconfirm 气泡确认框


