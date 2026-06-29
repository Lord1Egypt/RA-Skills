---
name: "container"
description: "Container 布局容器 -- Element Plus Vue3 桌面端组件。Invoke when user needs Container 布局容器 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/container.html"
---

---

# Container 布局容器 [​](#container-布局容器)

更新日志待解决

3

用于布局的容器组件，方便快速搭建页面的基本结构：

`<el-container>`：外层容器。 当子元素中包含 `<el-header>` 或 `<el-footer>` 时，全部子元素会垂直上下排列， 否则会水平左右排列。

`<el-header>`：顶栏容器。

`<el-aside>`：侧边栏容器。

`<el-main>`：主要区域容器。

`<el-footer>`：底栏容器。

TIP

以上组件采用了 flex 布局，使用前请确定目标浏览器是否兼容。 此外， `<el-container>`的直接子元素必须是后四个组件中的一个或多个。 后四个组件的父元素必须是一个 `<el-container>`

## 常见页面布局 [​](#常见页面布局)

Main

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY29tbW9uLWxheW91dFwiPlxuICAgIDxlbC1jb250YWluZXI+XG4gICAgICA8ZWwtaGVhZGVyPkhlYWRlcjwvZWwtaGVhZGVyPlxuICAgICAgPGVsLW1haW4+TWFpbjwvZWwtbWFpbj5cbiAgICA8L2VsLWNvbnRhaW5lcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/container/layout-hm.vue)_

vue

```
<template>
  <div class="common-layout">
    <el-container>
      <el-header>Header</el-header>
      <el-main>Main</el-main>
    </el-container>
  </div>
</template>
```

隐藏源代码

Main

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY29tbW9uLWxheW91dFwiPlxuICAgIDxlbC1jb250YWluZXI+XG4gICAgICA8ZWwtaGVhZGVyPkhlYWRlcjwvZWwtaGVhZGVyPlxuICAgICAgPGVsLW1haW4+TWFpbjwvZWwtbWFpbj5cbiAgICAgIDxlbC1mb290ZXI+Rm9vdGVyPC9lbC1mb290ZXI+XG4gICAgPC9lbC1jb250YWluZXI+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/container/layout-hmf.vue)_

vue

```
<template>
  <div class="common-layout">
    <el-container>
      <el-header>Header</el-header>
      <el-main>Main</el-main>
      <el-footer>Footer</el-footer>
    </el-container>
  </div>
</template>
```

隐藏源代码

Main

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY29tbW9uLWxheW91dFwiPlxuICAgIDxlbC1jb250YWluZXI+XG4gICAgICA8ZWwtYXNpZGUgd2lkdGg9XCIyMDBweFwiPkFzaWRlPC9lbC1hc2lkZT5cbiAgICAgIDxlbC1tYWluPk1haW48L2VsLW1haW4+XG4gICAgICA8ZWwtYXNpZGUgd2lkdGg9XCIyMDBweFwiPkFzaWRlPC9lbC1hc2lkZT5cbiAgICA8L2VsLWNvbnRhaW5lcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/container/layout-am.vue)_

vue

```
<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px">Aside</el-aside>
      <el-main>Main</el-main>
      <el-aside width="200px">Aside</el-aside>
    </el-container>
  </div>
</template>
```

隐藏源代码

Main

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY29tbW9uLWxheW91dFwiPlxuICAgIDxlbC1jb250YWluZXI+XG4gICAgICA8ZWwtaGVhZGVyPkhlYWRlcjwvZWwtaGVhZGVyPlxuICAgICAgPGVsLWNvbnRhaW5lcj5cbiAgICAgICAgPGVsLWFzaWRlIHdpZHRoPVwiMjAwcHhcIj5Bc2lkZTwvZWwtYXNpZGU+XG4gICAgICAgIDxlbC1tYWluPk1haW48L2VsLW1haW4+XG4gICAgICA8L2VsLWNvbnRhaW5lcj5cbiAgICA8L2VsLWNvbnRhaW5lcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/container/layout-ham.vue)_

vue

```
<template>
  <div class="common-layout">
    <el-container>
      <el-header>Header</el-header>
      <el-container>
        <el-aside width="200px">Aside</el-aside>
        <el-main>Main</el-main>
      </el-container>
    </el-container>
  </div>
</template>
```

隐藏源代码

Main

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY29tbW9uLWxheW91dFwiPlxuICAgIDxlbC1jb250YWluZXI+XG4gICAgICA8ZWwtaGVhZGVyPkhlYWRlcjwvZWwtaGVhZGVyPlxuICAgICAgPGVsLWNvbnRhaW5lcj5cbiAgICAgICAgPGVsLWFzaWRlIHdpZHRoPVwiMjAwcHhcIj5Bc2lkZTwvZWwtYXNpZGU+XG4gICAgICAgIDxlbC1jb250YWluZXI+XG4gICAgICAgICAgPGVsLW1haW4+TWFpbjwvZWwtbWFpbj5cbiAgICAgICAgICA8ZWwtZm9vdGVyPkZvb3RlcjwvZWwtZm9vdGVyPlxuICAgICAgICA8L2VsLWNvbnRhaW5lcj5cbiAgICAgIDwvZWwtY29udGFpbmVyPlxuICAgIDwvZWwtY29udGFpbmVyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/container/layout-hamf.vue)_

vue

```
<template>
  <div class="common-layout">
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
  </div>
</template>
```

隐藏源代码

Main

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY29tbW9uLWxheW91dFwiPlxuICAgIDxlbC1jb250YWluZXI+XG4gICAgICA8ZWwtYXNpZGUgd2lkdGg9XCIyMDBweFwiPkFzaWRlPC9lbC1hc2lkZT5cbiAgICAgIDxlbC1jb250YWluZXI+XG4gICAgICAgIDxlbC1oZWFkZXI+SGVhZGVyPC9lbC1oZWFkZXI+XG4gICAgICAgIDxlbC1tYWluPk1haW48L2VsLW1haW4+XG4gICAgICA8L2VsLWNvbnRhaW5lcj5cbiAgICA8L2VsLWNvbnRhaW5lcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/container/layout-ahm.vue)_

vue

```
<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px">Aside</el-aside>
      <el-container>
        <el-header>Header</el-header>
        <el-main>Main</el-main>
      </el-container>
    </el-container>
  </div>
</template>
```

隐藏源代码

Main

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY29tbW9uLWxheW91dFwiPlxuICAgIDxlbC1jb250YWluZXI+XG4gICAgICA8ZWwtYXNpZGUgd2lkdGg9XCIyMDBweFwiPkFzaWRlPC9lbC1hc2lkZT5cbiAgICAgIDxlbC1jb250YWluZXI+XG4gICAgICAgIDxlbC1oZWFkZXI+SGVhZGVyPC9lbC1oZWFkZXI+XG4gICAgICAgIDxlbC1tYWluPk1haW48L2VsLW1haW4+XG4gICAgICAgIDxlbC1mb290ZXI+Rm9vdGVyPC9lbC1mb290ZXI+XG4gICAgICA8L2VsLWNvbnRhaW5lcj5cbiAgICA8L2VsLWNvbnRhaW5lcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/container/layout-ahmf.vue)_

vue

```
<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px">Aside</el-aside>
      <el-container>
        <el-header>Header</el-header>
        <el-main>Main</el-main>
        <el-footer>Footer</el-footer>
      </el-container>
    </el-container>
  </div>
</template>
```

隐藏源代码

## 例子 [​](#例子)

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 693px;"><colgroup><col name="el-table_1_column_1" width="140"><col name="el-table_1_column_2" width="120"><col name="el-table_1_column_3" width="433"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">Tom</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No. 189, Grove St, Los Angeles</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY29udGFpbmVyIGNsYXNzPVwibGF5b3V0LWNvbnRhaW5lci1kZW1vXCIgc3R5bGU9XCJoZWlnaHQ6IDUwMHB4XCI+XG4gICAgPGVsLWFzaWRlIHdpZHRoPVwiMjAwcHhcIj5cbiAgICAgIDxlbC1zY3JvbGxiYXI+XG4gICAgICAgIDxlbC1tZW51IDpkZWZhdWx0LW9wZW5lZHM9XCJbJzEnLCAnMyddXCI+XG4gICAgICAgICAgPGVsLXN1Yi1tZW51IGluZGV4PVwiMVwiPlxuICAgICAgICAgICAgPHRlbXBsYXRlICN0aXRsZT5cbiAgICAgICAgICAgICAgPGVsLWljb24+PG1lc3NhZ2UgLz48L2VsLWljb24+TmF2aWdhdG9yIE9uZVxuICAgICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgICAgIDxlbC1tZW51LWl0ZW0tZ3JvdXA+XG4gICAgICAgICAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+R3JvdXAgMTwvdGVtcGxhdGU+XG4gICAgICAgICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIxLTFcIj5PcHRpb24gMTwvZWwtbWVudS1pdGVtPlxuICAgICAgICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMS0yXCI+T3B0aW9uIDI8L2VsLW1lbnUtaXRlbT5cbiAgICAgICAgICAgIDwvZWwtbWVudS1pdGVtLWdyb3VwPlxuICAgICAgICAgICAgPGVsLW1lbnUtaXRlbS1ncm91cCB0aXRsZT1cIkdyb3VwIDJcIj5cbiAgICAgICAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjEtM1wiPk9wdGlvbiAzPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgICAgICA8L2VsLW1lbnUtaXRlbS1ncm91cD5cbiAgICAgICAgICAgIDxlbC1zdWItbWVudSBpbmRleD1cIjEtNFwiPlxuICAgICAgICAgICAgICA8dGVtcGxhdGUgI3RpdGxlPk9wdGlvbjQ8L3RlbXBsYXRlPlxuICAgICAgICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMS00LTFcIj5PcHRpb24gNC0xPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgICAgICA8L2VsLXN1Yi1tZW51PlxuICAgICAgICAgIDwvZWwtc3ViLW1lbnU+XG4gICAgICAgICAgPGVsLXN1Yi1tZW51IGluZGV4PVwiMlwiPlxuICAgICAgICAgICAgPHRlbXBsYXRlICN0aXRsZT5cbiAgICAgICAgICAgICAgPGVsLWljb24+PGljb24tbWVudSAvPjwvZWwtaWNvbj5OYXZpZ2F0b3IgVHdvXG4gICAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICAgICAgPGVsLW1lbnUtaXRlbS1ncm91cD5cbiAgICAgICAgICAgICAgPHRlbXBsYXRlICN0aXRsZT5Hcm91cCAxPC90ZW1wbGF0ZT5cbiAgICAgICAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjItMVwiPk9wdGlvbiAxPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIyLTJcIj5PcHRpb24gMjwvZWwtbWVudS1pdGVtPlxuICAgICAgICAgICAgPC9lbC1tZW51LWl0ZW0tZ3JvdXA+XG4gICAgICAgICAgICA8ZWwtbWVudS1pdGVtLWdyb3VwIHRpdGxlPVwiR3JvdXAgMlwiPlxuICAgICAgICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMi0zXCI+T3B0aW9uIDM8L2VsLW1lbnUtaXRlbT5cbiAgICAgICAgICAgIDwvZWwtbWVudS1pdGVtLWdyb3VwPlxuICAgICAgICAgICAgPGVsLXN1Yi1tZW51IGluZGV4PVwiMi00XCI+XG4gICAgICAgICAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+T3B0aW9uIDQ8L3RlbXBsYXRlPlxuICAgICAgICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMi00LTFcIj5PcHRpb24gNC0xPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgICAgICA8L2VsLXN1Yi1tZW51PlxuICAgICAgICAgIDwvZWwtc3ViLW1lbnU+XG4gICAgICAgICAgPGVsLXN1Yi1tZW51IGluZGV4PVwiM1wiPlxuICAgICAgICAgICAgPHRlbXBsYXRlICN0aXRsZT5cbiAgICAgICAgICAgICAgPGVsLWljb24+PHNldHRpbmcgLz48L2VsLWljb24+TmF2aWdhdG9yIFRocmVlXG4gICAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICAgICAgPGVsLW1lbnUtaXRlbS1ncm91cD5cbiAgICAgICAgICAgICAgPHRlbXBsYXRlICN0aXRsZT5Hcm91cCAxPC90ZW1wbGF0ZT5cbiAgICAgICAgICAgICAgPGVsLW1lbnUtaXRlbSBpbmRleD1cIjMtMVwiPk9wdGlvbiAxPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgICAgICAgIDxlbC1tZW51LWl0ZW0gaW5kZXg9XCIzLTJcIj5PcHRpb24gMjwvZWwtbWVudS1pdGVtPlxuICAgICAgICAgICAgPC9lbC1tZW51LWl0ZW0tZ3JvdXA+XG4gICAgICAgICAgICA8ZWwtbWVudS1pdGVtLWdyb3VwIHRpdGxlPVwiR3JvdXAgMlwiPlxuICAgICAgICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMy0zXCI+T3B0aW9uIDM8L2VsLW1lbnUtaXRlbT5cbiAgICAgICAgICAgIDwvZWwtbWVudS1pdGVtLWdyb3VwPlxuICAgICAgICAgICAgPGVsLXN1Yi1tZW51IGluZGV4PVwiMy00XCI+XG4gICAgICAgICAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+T3B0aW9uIDQ8L3RlbXBsYXRlPlxuICAgICAgICAgICAgICA8ZWwtbWVudS1pdGVtIGluZGV4PVwiMy00LTFcIj5PcHRpb24gNC0xPC9lbC1tZW51LWl0ZW0+XG4gICAgICAgICAgICA8L2VsLXN1Yi1tZW51PlxuICAgICAgICAgIDwvZWwtc3ViLW1lbnU+XG4gICAgICAgIDwvZWwtbWVudT5cbiAgICAgIDwvZWwtc2Nyb2xsYmFyPlxuICAgIDwvZWwtYXNpZGU+XG5cbiAgICA8ZWwtY29udGFpbmVyPlxuICAgICAgPGVsLWhlYWRlciBzdHlsZT1cInRleHQtYWxpZ246IHJpZ2h0OyBmb250LXNpemU6IDEycHhcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cInRvb2xiYXJcIj5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24+XG4gICAgICAgICAgICA8ZWwtaWNvbiBzdHlsZT1cIm1hcmdpbi1yaWdodDogOHB4OyBtYXJnaW4tdG9wOiAxcHhcIj5cbiAgICAgICAgICAgICAgPHNldHRpbmcgLz5cbiAgICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgICAgIDx0ZW1wbGF0ZSAjZHJvcGRvd24+XG4gICAgICAgICAgICAgIDxlbC1kcm9wZG93bi1tZW51PlxuICAgICAgICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlZpZXc8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgICAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWRkPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPkRlbGV0ZTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICAgICAgPC9lbC1kcm9wZG93bi1tZW51PlxuICAgICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgICA8L2VsLWRyb3Bkb3duPlxuICAgICAgICAgIDxzcGFuPlRvbTwvc3Bhbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2VsLWhlYWRlcj5cblxuICAgICAgPGVsLW1haW4+XG4gICAgICAgIDxlbC1zY3JvbGxiYXI+XG4gICAgICAgICAgPGVsLXRhYmxlIDpkYXRhPVwidGFibGVEYXRhXCI+XG4gICAgICAgICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJkYXRlXCIgbGFiZWw9XCJEYXRlXCIgd2lkdGg9XCIxNDBcIiAvPlxuICAgICAgICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIHdpZHRoPVwiMTIwXCIgLz5cbiAgICAgICAgICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiAvPlxuICAgICAgICAgIDwvZWwtdGFibGU+XG4gICAgICAgIDwvZWwtc2Nyb2xsYmFyPlxuICAgICAgPC9lbC1tYWluPlxuICAgIDwvZWwtY29udGFpbmVyPlxuICA8L2VsLWNvbnRhaW5lcj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBNZW51IGFzIEljb25NZW51LCBNZXNzYWdlLCBTZXR0aW5nIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IGl0ZW0gPSB7XG4gIGRhdGU6ICcyMDE2LTA1LTAyJyxcbiAgbmFtZTogJ1RvbScsXG4gIGFkZHJlc3M6ICdOby4gMTg5LCBHcm92ZSBTdCwgTG9zIEFuZ2VsZXMnLFxufVxuY29uc3QgdGFibGVEYXRhID0gcmVmKEFycmF5LmZyb20oeyBsZW5ndGg6IDIwIH0pLmZpbGwoaXRlbSkpXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5sYXlvdXQtY29udGFpbmVyLWRlbW8gLmVsLWhlYWRlciB7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgYmFja2dyb3VuZC1jb2xvcjogdmFyKC0tZWwtY29sb3ItcHJpbWFyeS1saWdodC03KTtcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3ItcHJpbWFyeSk7XG59XG4ubGF5b3V0LWNvbnRhaW5lci1kZW1vIC5lbC1hc2lkZSB7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXByaW1hcnkpO1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5LWxpZ2h0LTgpO1xufVxuLmxheW91dC1jb250YWluZXItZGVtbyAuZWwtbWVudSB7XG4gIGJvcmRlci1yaWdodDogbm9uZTtcbn1cbi5sYXlvdXQtY29udGFpbmVyLWRlbW8gLmVsLW1haW4ge1xuICBwYWRkaW5nOiAwO1xufVxuLmxheW91dC1jb250YWluZXItZGVtbyAudG9vbGJhciB7XG4gIGRpc3BsYXk6IGlubGluZS1mbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgaGVpZ2h0OiAxMDAlO1xuICByaWdodDogMjBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/container/example.vue)_

vue

```
<template>
  <el-container class="layout-container-demo" style="height: 500px">
    <el-aside width="200px">
      <el-scrollbar>
        <el-menu :default-openeds="['1', '3']">
          <el-sub-menu index="1">
            <template #title>
              <el-icon><message /></el-icon>Navigator One
            </template>
            <el-menu-item-group>
              <template #title>Group 1</template>
              <el-menu-item index="1-1">Option 1</el-menu-item>
              <el-menu-item index="1-2">Option 2</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="Group 2">
              <el-menu-item index="1-3">Option 3</el-menu-item>
            </el-menu-item-group>
            <el-sub-menu index="1-4">
              <template #title>Option4</template>
              <el-menu-item index="1-4-1">Option 4-1</el-menu-item>
            </el-sub-menu>
          </el-sub-menu>
          <el-sub-menu index="2">
            <template #title>
              <el-icon><icon-menu /></el-icon>Navigator Two
            </template>
            <el-menu-item-group>
              <template #title>Group 1</template>
              <el-menu-item index="2-1">Option 1</el-menu-item>
              <el-menu-item index="2-2">Option 2</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="Group 2">
              <el-menu-item index="2-3">Option 3</el-menu-item>
            </el-menu-item-group>
            <el-sub-menu index="2-4">
              <template #title>Option 4</template>
              <el-menu-item index="2-4-1">Option 4-1</el-menu-item>
            </el-sub-menu>
          </el-sub-menu>
          <el-sub-menu index="3">
            <template #title>
              <el-icon><setting /></el-icon>Navigator Three
            </template>
            <el-menu-item-group>
              <template #title>Group 1</template>
              <el-menu-item index="3-1">Option 1</el-menu-item>
              <el-menu-item index="3-2">Option 2</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="Group 2">
              <el-menu-item index="3-3">Option 3</el-menu-item>
            </el-menu-item-group>
            <el-sub-menu index="3-4">
              <template #title>Option 4</template>
              <el-menu-item index="3-4-1">Option 4-1</el-menu-item>
            </el-sub-menu>
          </el-sub-menu>
        </el-menu>
      </el-scrollbar>
    </el-aside>

    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <div class="toolbar">
          <el-dropdown>
            <el-icon style="margin-right: 8px; margin-top: 1px">
              <setting />
            </el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>View</el-dropdown-item>
                <el-dropdown-item>Add</el-dropdown-item>
                <el-dropdown-item>Delete</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <span>Tom</span>
        </div>
      </el-header>

      <el-main>
        <el-scrollbar>
          <el-table :data="tableData">
            <el-table-column prop="date" label="Date" width="140" />
            <el-table-column prop="name" label="Name" width="120" />
            <el-table-column prop="address" label="Address" />
          </el-table>
        </el-scrollbar>
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Menu as IconMenu, Message, Setting } from '@element-plus/icons-vue'

const item = {
  date: '2016-05-02',
  name: 'Tom',
  address: 'No. 189, Grove St, Los Angeles',
}
const tableData = ref(Array.from({ length: 20 }).fill(item))
</script>

<style scoped>
.layout-container-demo .el-header {
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
}
.layout-container-demo .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
}
.layout-container-demo .el-menu {
  border-right: none;
}
.layout-container-demo .el-main {
  padding: 0;
}
.layout-container-demo .toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}
</style>
```

隐藏源代码

## Container API [​](#container-api)

### Container Attributes [​](#container-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| direction | 子元素的排列方向 | `enum` | 子元素中有 `el-header` 或 `el-footer` 时为 vertical，否则为 horizontal |

### Container Slots [​](#container-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | Container / Header / Aside / Main / Footer |

## Header API [​](#header-api)

### Header Attributes [​](#header-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| height | 顶栏高度 | `string` | 60px |

### Header Slots [​](#header-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## Aside API [​](#aside-api)

### Aside Attributes [​](#aside-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| width | 侧边栏宽度 | `string` | 300px |

### Aside Slots [​](#aside-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## Main API [​](#main-api)

### Main Slots [​](#main-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## Footer API [​](#footer-api)

### Footer Attributes [​](#footer-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| height | 底栏高度 | `string` | 60px |

### Footer Slots [​](#footer-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/container) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/container.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/container.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/48633709?v=4&size=64)](https://github.com/cosine7)[![](https://avatars.githubusercontent.com/u/102197895?v=4&size=64)](https://github.com/deng-001)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/175172745?v=4&size=64)](https://github.com/JingGaoWei)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)

[Color 色彩](https://element-plus.org/zh-CN/component/color)

[Icon 图标](https://element-plus.org/zh-CN/component/icon)


