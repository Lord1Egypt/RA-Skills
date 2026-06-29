---
name: "layout"
description: "Layout 布局 -- Element Plus Vue3 桌面端组件。Invoke when user needs Layout 布局 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/layout.html"
---

---

# Layout 布局 [​](#layout-布局)

更新日志待解决

5

通过基础的 24 分栏，迅速简便地创建布局。

TIP

组件默认使用 Flex 布局，不需要手动设置 `type="flex"`。

请注意父容器避免使用 `inline` 相关样式，会导致组件宽度不能撑满。

列的基本单位为1，最多24个，最少0个。

## 基础布局 [​](#基础布局)

使用列创建基础网格布局。

通过 `row` 和 `col` 组件，并通过 col 组件的 `span` 属性我们就可以自由地组合布局。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93PlxuICAgIDxlbC1jb2wgOnNwYW49XCIyNFwiPlxuICAgICAgPGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGUtZGFya1wiIC8+XG4gICAgPC9lbC1jb2w+XG4gIDwvZWwtcm93PlxuICA8ZWwtcm93PlxuICAgIDxlbC1jb2wgOnNwYW49XCIxMlwiPlxuICAgICAgPGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCIxMlwiPlxuICAgICAgPGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGUtbGlnaHRcIiAvPlxuICAgIDwvZWwtY29sPlxuICA8L2VsLXJvdz5cbiAgPGVsLXJvdz5cbiAgICA8ZWwtY29sIDpzcGFuPVwiOFwiPlxuICAgICAgPGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI4XCI+XG4gICAgICA8ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZS1saWdodFwiIC8+XG4gICAgPC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjhcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz5cbiAgICA8L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG4gIDxlbC1yb3c+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjZcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz5cbiAgICA8L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpzcGFuPVwiNlwiPlxuICAgICAgPGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGUtbGlnaHRcIiAvPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+XG4gICAgICA8ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+XG4gICAgPC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjZcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlLWxpZ2h0XCIgLz5cbiAgICA8L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG4gIDxlbC1yb3c+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjRcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz5cbiAgICA8L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpzcGFuPVwiNFwiPlxuICAgICAgPGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGUtbGlnaHRcIiAvPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI0XCI+XG4gICAgICA8ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+XG4gICAgPC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjRcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlLWxpZ2h0XCIgLz5cbiAgICA8L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpzcGFuPVwiNFwiPlxuICAgICAgPGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI0XCI+XG4gICAgICA8ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZS1saWdodFwiIC8+XG4gICAgPC9lbC1jb2w+XG4gIDwvZWwtcm93PlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlPlxuLmVsLXJvdyB7XG4gIG1hcmdpbi1ib3R0b206IDIwcHg7XG59XG5cbi5lbC1yb3c6bGFzdC1jaGlsZCB7XG4gIG1hcmdpbi1ib3R0b206IDA7XG59XG5cbi5lbC1jb2wge1xuICBib3JkZXItcmFkaXVzOiA0cHg7XG59XG5cbi5ncmlkLWNvbnRlbnQge1xuICBib3JkZXItcmFkaXVzOiA0cHg7XG4gIG1pbi1oZWlnaHQ6IDM2cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/layout/basic-layout.vue)_

vue

```
<template>
  <el-row>
    <el-col :span="24">
      <div class="grid-content ep-bg-purple-dark" />
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="12">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="12">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="8">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="8">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
    <el-col :span="8">
      <div class="grid-content ep-bg-purple" />
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="6">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="4">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
  </el-row>
</template>

<style>
.el-row {
  margin-bottom: 20px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
```

隐藏源代码

## 分栏间隔 [​](#分栏间隔)

支持列间距。

行提供 `gutter` 属性来指定列之间的间距，其默认值为0。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IDpndXR0ZXI9XCIyMFwiPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPjwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPjwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPjwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPjwvZWwtY29sPlxuICA8L2VsLXJvdz5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZT5cbi5lbC1yb3cge1xuICBtYXJnaW4tYm90dG9tOiAyMHB4O1xufVxuLmVsLXJvdzpsYXN0LWNoaWxkIHtcbiAgbWFyZ2luLWJvdHRvbTogMDtcbn1cbi5lbC1jb2wge1xuICBib3JkZXItcmFkaXVzOiA0cHg7XG59XG5cbi5ncmlkLWNvbnRlbnQge1xuICBib3JkZXItcmFkaXVzOiA0cHg7XG4gIG1pbi1oZWlnaHQ6IDM2cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/layout/column-spacing.vue)_

vue

```
<template>
  <el-row :gutter="20">
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
</template>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
```

隐藏源代码

## 混合布局 [​](#混合布局)

通过基础的 1/24 分栏任意扩展组合形成较为复杂的混合布局。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IDpndXR0ZXI9XCIyMFwiPlxuICAgIDxlbC1jb2wgOnNwYW49XCIxNlwiPjxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz48L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpzcGFuPVwiOFwiPjxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz48L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG4gIDxlbC1yb3cgOmd1dHRlcj1cIjIwXCI+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjhcIj48ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+PC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjhcIj48ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+PC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjRcIj48ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+PC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjRcIj48ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+PC9lbC1jb2w+XG4gIDwvZWwtcm93PlxuICA8ZWwtcm93IDpndXR0ZXI9XCIyMFwiPlxuICAgIDxlbC1jb2wgOnNwYW49XCI0XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPjwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCIxNlwiPjxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz48L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpzcGFuPVwiNFwiPjxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz48L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG48L3RlbXBsYXRlPlxuXG48c3R5bGU+XG4uZWwtcm93IHtcbiAgbWFyZ2luLWJvdHRvbTogMjBweDtcbn1cbi5lbC1yb3c6bGFzdC1jaGlsZCB7XG4gIG1hcmdpbi1ib3R0b206IDA7XG59XG4uZWwtY29sIHtcbiAgYm9yZGVyLXJhZGl1czogNHB4O1xufVxuXG4uZ3JpZC1jb250ZW50IHtcbiAgYm9yZGVyLXJhZGl1czogNHB4O1xuICBtaW4taGVpZ2h0OiAzNnB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/layout/hybrid-layout.vue)_

vue

```
<template>
  <el-row :gutter="20">
    <el-col :span="16"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="8"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="8"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="8"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="16"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
</template>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
```

隐藏源代码

## 列偏移 [​](#列偏移)

您可以指定列偏移量。

通过制定 col 组件的 `offset` 属性可以指定分栏偏移的栏数。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IDpndXR0ZXI9XCIyMFwiPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPjwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCIgOm9mZnNldD1cIjZcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz5cbiAgICA8L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG4gIDxlbC1yb3cgOmd1dHRlcj1cIjIwXCI+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjZcIiA6b2Zmc2V0PVwiNlwiPlxuICAgICAgPGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCIgOm9mZnNldD1cIjZcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz5cbiAgICA8L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG4gIDxlbC1yb3cgOmd1dHRlcj1cIjIwXCI+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjEyXCIgOm9mZnNldD1cIjZcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz5cbiAgICA8L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG48L3RlbXBsYXRlPlxuXG48c3R5bGU+XG4uZWwtcm93IHtcbiAgbWFyZ2luLWJvdHRvbTogMjBweDtcbn1cbi5lbC1yb3c6bGFzdC1jaGlsZCB7XG4gIG1hcmdpbi1ib3R0b206IDA7XG59XG4uZWwtY29sIHtcbiAgYm9yZGVyLXJhZGl1czogNHB4O1xufVxuXG4uZ3JpZC1jb250ZW50IHtcbiAgYm9yZGVyLXJhZGl1czogNHB4O1xuICBtaW4taGVpZ2h0OiAzNnB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/layout/column-offset.vue)_

vue

```
<template>
  <el-row :gutter="20">
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6" :offset="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="6" :offset="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :span="6" :offset="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="12" :offset="6">
      <div class="grid-content ep-bg-purple" />
    </el-col>
  </el-row>
</template>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
```

隐藏源代码

## 对齐方式 [​](#对齐方式)

默认使用 flex 布局来对分栏进行灵活的对齐。

您可以通过`justify` 属性来定义子元素的排版方式，其取值为start、center、end、space-between、space-around或space-evenly。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IGNsYXNzPVwicm93LWJnXCI+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjZcIj48ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+PC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjZcIj48ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZS1saWdodFwiIC8+PC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjZcIj48ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+PC9lbC1jb2w+XG4gIDwvZWwtcm93PlxuICA8ZWwtcm93IGNsYXNzPVwicm93LWJnXCIganVzdGlmeT1cImNlbnRlclwiPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPjwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGUtbGlnaHRcIiAvPjwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPjwvZWwtY29sPlxuICA8L2VsLXJvdz5cbiAgPGVsLXJvdyBjbGFzcz1cInJvdy1iZ1wiIGp1c3RpZnk9XCJlbmRcIj5cbiAgICA8ZWwtY29sIDpzcGFuPVwiNlwiPjxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz48L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpzcGFuPVwiNlwiPjxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlLWxpZ2h0XCIgLz48L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpzcGFuPVwiNlwiPjxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz48L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG4gIDxlbC1yb3cgY2xhc3M9XCJyb3ctYmdcIiBqdXN0aWZ5PVwic3BhY2UtYmV0d2VlblwiPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPjwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGUtbGlnaHRcIiAvPjwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI2XCI+PGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGVcIiAvPjwvZWwtY29sPlxuICA8L2VsLXJvdz5cbiAgPGVsLXJvdyBjbGFzcz1cInJvdy1iZ1wiIGp1c3RpZnk9XCJzcGFjZS1hcm91bmRcIj5cbiAgICA8ZWwtY29sIDpzcGFuPVwiNlwiPjxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz48L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpzcGFuPVwiNlwiPjxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlLWxpZ2h0XCIgLz48L2VsLWNvbD5cbiAgICA8ZWwtY29sIDpzcGFuPVwiNlwiPjxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz48L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG4gIDxlbC1yb3cgY2xhc3M9XCJyb3ctYmdcIiBqdXN0aWZ5PVwic3BhY2UtZXZlbmx5XCI+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjZcIj48ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+PC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjZcIj48ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZS1saWdodFwiIC8+PC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjZcIj48ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+PC9lbC1jb2w+XG4gIDwvZWwtcm93PlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlPlxuLmVsLXJvdyB7XG4gIG1hcmdpbi1ib3R0b206IDIwcHg7XG59XG4uZWwtcm93Omxhc3QtY2hpbGQge1xuICBtYXJnaW4tYm90dG9tOiAwO1xufVxuLmVsLWNvbCB7XG4gIGJvcmRlci1yYWRpdXM6IDRweDtcbn1cblxuLmdyaWQtY29udGVudCB7XG4gIGJvcmRlci1yYWRpdXM6IDRweDtcbiAgbWluLWhlaWdodDogMzZweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/layout/alignment.vue)_

vue

```
<template>
  <el-row class="row-bg">
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
  <el-row class="row-bg" justify="center">
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
  <el-row class="row-bg" justify="end">
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
  <el-row class="row-bg" justify="space-between">
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
  <el-row class="row-bg" justify="space-around">
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
  <el-row class="row-bg" justify="space-evenly">
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
    <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
  </el-row>
</template>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
```

隐藏源代码

## 响应式布局 [​](#响应式布局)

参照了 Bootstrap 的 响应式设计，预设了五个响应尺寸：xs、sm、md、lg 和 xl。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IDpndXR0ZXI9XCIxMFwiPlxuICAgIDxlbC1jb2wgOnhzPVwiOFwiIDpzbT1cIjZcIiA6bWQ9XCI0XCIgOmxnPVwiM1wiIDp4bD1cIjFcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJncmlkLWNvbnRlbnQgZXAtYmctcHVycGxlXCIgLz5cbiAgICA8L2VsLWNvbD5cbiAgICA8ZWwtY29sIDp4cz1cIjRcIiA6c209XCI2XCIgOm1kPVwiOFwiIDpsZz1cIjlcIiA6eGw9XCIxMVwiPlxuICAgICAgPGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGUtbGlnaHRcIiAvPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnhzPVwiNFwiIDpzbT1cIjZcIiA6bWQ9XCI4XCIgOmxnPVwiOVwiIDp4bD1cIjExXCI+XG4gICAgICA8ZGl2IGNsYXNzPVwiZ3JpZC1jb250ZW50IGVwLWJnLXB1cnBsZVwiIC8+XG4gICAgPC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6eHM9XCI4XCIgOnNtPVwiNlwiIDptZD1cIjRcIiA6bGc9XCIzXCIgOnhsPVwiMVwiPlxuICAgICAgPGRpdiBjbGFzcz1cImdyaWQtY29udGVudCBlcC1iZy1wdXJwbGUtbGlnaHRcIiAvPlxuICAgIDwvZWwtY29sPlxuICA8L2VsLXJvdz5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZT5cbi5lbC1jb2wge1xuICBib3JkZXItcmFkaXVzOiA0cHg7XG59XG5cbi5ncmlkLWNvbnRlbnQge1xuICBib3JkZXItcmFkaXVzOiA0cHg7XG4gIG1pbi1oZWlnaHQ6IDM2cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/layout/responsive-layout.vue)_

vue

```
<template>
  <el-row :gutter="10">
    <el-col :xs="8" :sm="6" :md="4" :lg="3" :xl="1">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :xs="4" :sm="6" :md="8" :lg="9" :xl="11">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
    <el-col :xs="4" :sm="6" :md="8" :lg="9" :xl="11">
      <div class="grid-content ep-bg-purple" />
    </el-col>
    <el-col :xs="8" :sm="6" :md="4" :lg="3" :xl="1">
      <div class="grid-content ep-bg-purple-light" />
    </el-col>
  </el-row>
</template>

<style>
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
```

隐藏源代码

## 基于断点的隐藏类 [​](#基于断点的隐藏类)

Element Plus 额外提供了一系列类名，用于在某些条件下隐藏元素。 这些类名可以添加在任何 DOM 元素或自定义组件上。 如果需要，请自行引入以下文件：

js

```
import 'element-plus/theme-chalk/display.css'
```

这些类名为：

-   `hidden-xs-only` - 当视口在 `xs` 尺寸时隐藏
-   `hidden-sm-only` - 当视口在 `sm` 尺寸时隐藏
-   `hidden-sm-and-down` - 当视口在 `sm` 及以下尺寸时隐藏
-   `hidden-sm-and-up` - 当视口在 `sm` 及以上尺寸时隐藏
-   `hidden-md-only` - 当视口在 `md` 尺寸时隐藏
-   `hidden-md-and-down` - 当视口在 `md` 及以下尺寸时隐藏
-   `hidden-md-and-up` - 当视口在 `md` 及以上尺寸时隐藏
-   `hidden-lg-only` - 当视口在 `lg` 尺寸时隐藏
-   `hidden-lg-and-down` - 当视口在 `lg` 及以下尺寸时隐藏
-   `hidden-lg-and-up` - 当视口在 `lg` 及以上尺寸时隐藏
-   `hidden-xl-only` - 当视口在 `xl` 尺寸时隐藏

## Row API [​](#row-api)

### Row Attributes [​](#row-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| gutter | 栅格间隔 | `number` | 0 |
| justify | flex 布局下的水平排列方式 | `enum` | start |
| align | flex 布局下的垂直排列方式 | `enum` | — |
| tag | 自定义元素标签 | `string` | div |

### Row Slots [​](#row-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | Col |

## Col API [​](#col-api)

### Col Attributes [​](#col-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| span | 栅格占据的列数 | `number` | 24 |
| offset | 栅格左侧的间隔格数 | `number` | 0 |
| push | 栅格向右移动格数 | `number` | 0 |
| pull | 栅格向左移动格数 | `number` | 0 |
| xs | `<768px` 响应式栅格数或者栅格属性对象 | `number` / `object` | — |
| sm | `≥768px` 响应式栅格数或者栅格属性对象 | `number` / `object` | — |
| md | `≥992px` 响应式栅格数或者栅格属性对象 | `number` / `object` | — |
| lg | `≥1200px` 响应式栅格数或者栅格属性对象 | `number` / `object` | — |
| xl | `≥1920px` 响应式栅格数或者栅格属性对象 | `number` / `object` | — |
| tag | 自定义元素标签 | `string` | div |

### Col Slots [​](#col-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## 源代码 [​](#源代码)

[文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/layout.md)

[Icon 图标](https://element-plus.org/zh-CN/component/icon)

[Link 链接](https://element-plus.org/zh-CN/component/link)


