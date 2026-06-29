---
name: "container"
description: "Container 布局容器 -- Element UI Vue2 桌面端组件。Invoke when user needs Container 布局容器 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/container"
---

---

-   [更新日志](#/zh-CN/component/changelog)
-   [Element React](https://elemefe.github.io/element-react/)
-   [Element Angular](https://element-angular.faas.ele.me/)
-   开发指南
    -   [安装](#/zh-CN/component/installation)
    -   [快速上手](#/zh-CN/component/quickstart)
    -   [国际化](#/zh-CN/component/i18n)
    -   [自定义主题](#/zh-CN/component/custom-theme)
    -   [内置过渡动画](#/zh-CN/component/transition)
-   组件

    Basic

    -   [Layout 布局](#/zh-CN/component/layout)
    -   [Container 布局容器](#/zh-CN/component/container)
    -   [Color 色彩](#/zh-CN/component/color)
    -   [Typography 字体](#/zh-CN/component/typography)
    -   [Border 边框](#/zh-CN/component/border)
    -   [Icon 图标](#/zh-CN/component/icon)
    -   [Button 按钮](#/zh-CN/component/button)
    -   [Link 文字链接](#/zh-CN/component/link)

    Form

    -   [Radio 单选框](#/zh-CN/component/radio)
    -   [Checkbox 多选框](#/zh-CN/component/checkbox)
    -   [Input 输入框](#/zh-CN/component/input)
    -   [InputNumber 计数器](#/zh-CN/component/input-number)
    -   [Select 选择器](#/zh-CN/component/select)
    -   [Cascader 级联选择器](#/zh-CN/component/cascader)
    -   [Switch 开关](#/zh-CN/component/switch)
    -   [Slider 滑块](#/zh-CN/component/slider)
    -   [TimePicker 时间选择器](#/zh-CN/component/time-picker)
    -   [DatePicker 日期选择器](#/zh-CN/component/date-picker)
    -   [DateTimePicker 日期时间选择器](#/zh-CN/component/datetime-picker)
    -   [Upload 上传](#/zh-CN/component/upload)
    -   [Rate 评分](#/zh-CN/component/rate)
    -   [ColorPicker 颜色选择器](#/zh-CN/component/color-picker)
    -   [Transfer 穿梭框](#/zh-CN/component/transfer)
    -   [Form 表单](#/zh-CN/component/form)

    Data

    -   [Table 表格](#/zh-CN/component/table)
    -   [Tag 标签](#/zh-CN/component/tag)
    -   [Progress 进度条](#/zh-CN/component/progress)
    -   [Tree 树形控件](#/zh-CN/component/tree)
    -   [Pagination 分页](#/zh-CN/component/pagination)
    -   [Badge 标记](#/zh-CN/component/badge)
    -   [Avatar 头像](#/zh-CN/component/avatar)
    -   [Skeleton 骨架屏](#/zh-CN/component/skeleton)
    -   [Empty 空状态](#/zh-CN/component/empty)
    -   [Descriptions 描述列表](#/zh-CN/component/descriptions)
    -   [Result 结果](#/zh-CN/component/result)
    -   [Statistic 统计数值](#/zh-CN/component/statistic)

    Notice

    -   [Alert 警告](#/zh-CN/component/alert)
    -   [Loading 加载](#/zh-CN/component/loading)
    -   [Message 消息提示](#/zh-CN/component/message)
    -   [MessageBox 弹框](#/zh-CN/component/message-box)
    -   [Notification 通知](#/zh-CN/component/notification)

    Navigation

    -   [NavMenu 导航菜单](#/zh-CN/component/menu)
    -   [Tabs 标签页](#/zh-CN/component/tabs)
    -   [Breadcrumb 面包屑](#/zh-CN/component/breadcrumb)
    -   [PageHeader 页头](#/zh-CN/component/page-header)
    -   [Dropdown 下拉菜单](#/zh-CN/component/dropdown)
    -   [Steps 步骤条](#/zh-CN/component/steps)

    Others

    -   [Dialog 对话框](#/zh-CN/component/dialog)
    -   [Tooltip 文字提示](#/zh-CN/component/tooltip)
    -   [Popover 弹出框](#/zh-CN/component/popover)
    -   [Popconfirm 气泡确认框](#/zh-CN/component/popconfirm)
    -   [Card 卡片](#/zh-CN/component/card)
    -   [Carousel 走马灯](#/zh-CN/component/carousel)
    -   [Collapse 折叠面板](#/zh-CN/component/collapse)
    -   [Timeline 时间线](#/zh-CN/component/timeline)
    -   [Divider 分割线](#/zh-CN/component/divider)
    -   [Calendar 日历](#/zh-CN/component/calendar)
    -   [Image 图片](#/zh-CN/component/image)
    -   [Backtop 回到顶部](#/zh-CN/component/backtop)
    -   [InfiniteScroll 无限滚动](#/zh-CN/component/infiniteScroll)
    -   [Drawer 抽屉](#/zh-CN/component/drawer)

## [¶](https://element.eleme.cn/#/zh-CN/component/container#container-bu-ju-rong-qi) Container 布局容器

用于布局的容器组件，方便快速搭建页面的基本结构：

`<el-container>`：外层容器。当子元素中包含 `<el-header>` 或 `<el-footer>` 时，全部子元素会垂直上下排列，否则会水平左右排列。

`<el-header>`：顶栏容器。

`<el-aside>`：侧边栏容器。

`<el-main>`：主要区域容器。

`<el-footer>`：底栏容器。

以上组件采用了 flex 布局，使用前请确定目标浏览器是否兼容。此外，`<el-container>` 的子元素只能是后四者，后四者的父元素也只能是 `<el-container>`。

### [¶](https://element.eleme.cn/#/zh-CN/component/container#chang-jian-ye-mian-bu-ju) 常见页面布局

Main

Main

Main

Main

Main

Main

Main

```
<el-container>
  <el-header>Header</el-header>
  <el-main>Main</el-main>
</el-container>

<el-container>
  <el-header>Header</el-header>
  <el-main>Main</el-main>
  <el-footer>Footer</el-footer>
</el-container>

<el-container>
  <el-aside width="200px">Aside</el-aside>
  <el-main>Main</el-main>
</el-container>

<el-container>
  <el-header>Header</el-header>
  <el-container>
    <el-aside width="200px">Aside</el-aside>
    <el-main>Main</el-main>
  </el-container>
</el-container>

<el-container>
  <el-header>Header</el-header>
  <el-container>
    <el-aside width="200px">Aside</el-aside>
    <el-container>
      <el-main>Main</el-main>
      <el-footer>Footer</el-footer>
    </el-container>
  </el-container>
</el-container>

<el-container>
  <el-aside width="200px">Aside</el-aside>
  <el-container>
    <el-header>Header</el-header>
    <el-main>Main</el-main>
  </el-container>
</el-container>

<el-container>
  <el-aside width="200px">Aside</el-aside>
  <el-container>
    <el-header>Header</el-header>
    <el-main>Main</el-main>
    <el-footer>Footer</el-footer>
  </el-container>
</el-container>

<style>
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/container#shi-li) 实例

|
日期

 |

姓名

 |

地址

 |
| --- | --- | --- |

<table cellspacing="0" cellpadding="0" border="0" class="el-table__body" style="width: 578px;"><colgroup><col name="el-table_1_column_1" width="140"><col name="el-table_1_column_2" width="120"><col name="el-table_1_column_3" width="318"></colgroup><tbody><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr><tr class="el-table__row"><td rowspan="1" colspan="1" class="el-table_1_column_1   el-table__cell"><div class="cell">2016-05-02</div></td><td rowspan="1" colspan="1" class="el-table_1_column_2   el-table__cell"><div class="cell">王小虎</div></td><td rowspan="1" colspan="1" class="el-table_1_column_3   el-table__cell"><div class="cell">上海市普陀区金沙江路 1518 弄</div></td></tr></tbody></table>

```
<el-container style="height: 500px; border: 1px solid #eee">
  <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
    <el-menu :default-openeds="['1', '3']">
      <el-submenu index="1">
        <template slot="title"><i class="el-icon-message"></i>导航一</template>
        <el-menu-item-group>
          <template slot="title">分组一</template>
          <el-menu-item index="1-1">选项1</el-menu-item>
          <el-menu-item index="1-2">选项2</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="分组2">
          <el-menu-item index="1-3">选项3</el-menu-item>
        </el-menu-item-group>
        <el-submenu index="1-4">
          <template slot="title">选项4</template>
          <el-menu-item index="1-4-1">选项4-1</el-menu-item>
        </el-submenu>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-menu"></i>导航二</template>
        <el-menu-item-group>
          <template slot="title">分组一</template>
          <el-menu-item index="2-1">选项1</el-menu-item>
          <el-menu-item index="2-2">选项2</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="分组2">
          <el-menu-item index="2-3">选项3</el-menu-item>
        </el-menu-item-group>
        <el-submenu index="2-4">
          <template slot="title">选项4</template>
          <el-menu-item index="2-4-1">选项4-1</el-menu-item>
        </el-submenu>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title"><i class="el-icon-setting"></i>导航三</template>
        <el-menu-item-group>
          <template slot="title">分组一</template>
          <el-menu-item index="3-1">选项1</el-menu-item>
          <el-menu-item index="3-2">选项2</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="分组2">
          <el-menu-item index="3-3">选项3</el-menu-item>
        </el-menu-item-group>
        <el-submenu index="3-4">
          <template slot="title">选项4</template>
          <el-menu-item index="3-4-1">选项4-1</el-menu-item>
        </el-submenu>
      </el-submenu>
    </el-menu>
  </el-aside>

  <el-container>
    <el-header style="text-align: right; font-size: 12px">
      <el-dropdown>
        <i class="el-icon-setting" style="margin-right: 15px"></i>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>查看</el-dropdown-item>
          <el-dropdown-item>新增</el-dropdown-item>
          <el-dropdown-item>删除</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <span>王小虎</span>
    </el-header>

    <el-main>
      <el-table :data="tableData">
        <el-table-column prop="date" label="日期" width="140">
        </el-table-column>
        <el-table-column prop="name" label="姓名" width="120">
        </el-table-column>
        <el-table-column prop="address" label="地址">
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
</el-container>

<style>
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }

  .el-aside {
    color: #333;
  }
</style>

<script>
  export default {
    data() {
      const item = {
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      };
      return {
        tableData: Array(20).fill(item)
      }
    }
  };
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/container#container-attributes) Container Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| direction | 子元素的排列方向 | string | horizontal / vertical | 子元素中有 `el-header` 或 `el-footer` 时为 vertical，否则为 horizontal |

### [¶](https://element.eleme.cn/#/zh-CN/component/container#header-attributes) Header Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| height | 顶栏高度 | string | — | 60px |

### [¶](https://element.eleme.cn/#/zh-CN/component/container#aside-attributes) Aside Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| width | 侧边栏宽度 | string | — | 300px |

### [¶](https://element.eleme.cn/#/zh-CN/component/container#footer-attributes) Footer Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| height | 底栏高度 | string | — | 60px |

Layout 布局 Color 色彩


