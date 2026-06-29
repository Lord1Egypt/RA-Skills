---
name: "popover"
description: "Popover 弹出框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Popover 弹出框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/popover.html"
---

---

# Popover 弹出框 [​](#popover-弹出框)

更新日志待解决

25

## 展示位置 [​](#展示位置)

Popover 弹出框提供 9 种展示位置。

使用 `content` 属性来设置悬停时显示的信息。 由 `placement` 属性决定 Popover 弹出框的位置。 该属性值格式为：`[方向]-[对齐位置]`，可供选择的四个方向分别是`top`、`left`、`right`、`bottom`，可供选择的三种对齐方式分别是`start`、`end`、`null`，默认的对齐方式为null。 以 `placement="left-end"` 为例，Popover 弹出框会显示在悬停元素的左侧，且提示信息的底部与悬停元素的底部对齐。

top-starttoptop-end

left-startright-start

leftright

left-endright-end

bottom-startbottombottom-end

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwicG9wb3Zlci1iYXNlLWJveFwiPlxuICAgIDxkaXYgY2xhc3M9XCJyb3cgY2VudGVyXCI+XG4gICAgICA8ZWwtcG9wb3ZlclxuICAgICAgICB0aXRsZT1cIlRpdGxlXCJcbiAgICAgICAgY29udGVudD1cIlRvcCBMZWZ0IHByb21wdHMgaW5mb1wiXG4gICAgICAgIHBsYWNlbWVudD1cInRvcC1zdGFydFwiXG4gICAgICA+XG4gICAgICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPlxuICAgICAgICAgIDxlbC1idXR0b24+dG9wLXN0YXJ0PC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXBvcG92ZXI+XG4gICAgICA8ZWwtcG9wb3ZlclxuICAgICAgICB0aXRsZT1cIlRpdGxlXCJcbiAgICAgICAgY29udGVudD1cIlRvcCBDZW50ZXIgcHJvbXB0cyBpbmZvXCJcbiAgICAgICAgcGxhY2VtZW50PVwidG9wXCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICAgICAgPGVsLWJ1dHRvbj50b3A8L2VsLWJ1dHRvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtcG9wb3Zlcj5cbiAgICAgIDxlbC1wb3BvdmVyXG4gICAgICAgIHRpdGxlPVwiVGl0bGVcIlxuICAgICAgICBjb250ZW50PVwiVG9wIFJpZ2h0IHByb21wdHMgaW5mb1wiXG4gICAgICAgIHBsYWNlbWVudD1cInRvcC1lbmRcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgICAgICA8ZWwtYnV0dG9uPnRvcC1lbmQ8L2VsLWJ1dHRvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtcG9wb3Zlcj5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwicm93XCI+XG4gICAgICA8ZWwtcG9wb3ZlclxuICAgICAgICB0aXRsZT1cIlRpdGxlXCJcbiAgICAgICAgY29udGVudD1cIkxlZnQgVG9wIHByb21wdHMgaW5mb1wiXG4gICAgICAgIHBsYWNlbWVudD1cImxlZnQtc3RhcnRcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgICAgICA8ZWwtYnV0dG9uPmxlZnQtc3RhcnQ8L2VsLWJ1dHRvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtcG9wb3Zlcj5cbiAgICAgIDxlbC1wb3BvdmVyXG4gICAgICAgIHRpdGxlPVwiVGl0bGVcIlxuICAgICAgICBjb250ZW50PVwiUmlnaHQgVG9wIHByb21wdHMgaW5mb1wiXG4gICAgICAgIHBsYWNlbWVudD1cInJpZ2h0LXN0YXJ0XCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICAgICAgPGVsLWJ1dHRvbj5yaWdodC1zdGFydDwvZWwtYnV0dG9uPlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgPC9lbC1wb3BvdmVyPlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJyb3dcIj5cbiAgICAgIDxlbC1wb3BvdmVyXG4gICAgICAgIHRpdGxlPVwiVGl0bGVcIlxuICAgICAgICBjb250ZW50PVwiTGVmdCBDZW50ZXIgcHJvbXB0cyBpbmZvXCJcbiAgICAgICAgcGxhY2VtZW50PVwibGVmdFwiXG4gICAgICA+XG4gICAgICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPlxuICAgICAgICAgIDxlbC1idXR0b24gY2xhc3M9XCJtdC0zIG1iLTNcIj5sZWZ0PC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXBvcG92ZXI+XG4gICAgICA8ZWwtcG9wb3ZlclxuICAgICAgICB0aXRsZT1cIlRpdGxlXCJcbiAgICAgICAgY29udGVudD1cIlJpZ2h0IENlbnRlciBwcm9tcHRzIGluZm9cIlxuICAgICAgICBwbGFjZW1lbnQ9XCJyaWdodFwiXG4gICAgICA+XG4gICAgICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPlxuICAgICAgICAgIDxlbC1idXR0b24+cmlnaHQ8L2VsLWJ1dHRvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtcG9wb3Zlcj5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwicm93XCI+XG4gICAgICA8ZWwtcG9wb3ZlclxuICAgICAgICB0aXRsZT1cIlRpdGxlXCJcbiAgICAgICAgY29udGVudD1cIkxlZnQgQm90dG9tIHByb21wdHMgaW5mb1wiXG4gICAgICAgIHBsYWNlbWVudD1cImxlZnQtZW5kXCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICAgICAgPGVsLWJ1dHRvbj5sZWZ0LWVuZDwvZWwtYnV0dG9uPlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgPC9lbC1wb3BvdmVyPlxuICAgICAgPGVsLXBvcG92ZXJcbiAgICAgICAgdGl0bGU9XCJUaXRsZVwiXG4gICAgICAgIGNvbnRlbnQ9XCJSaWdodCBCb3R0b20gcHJvbXB0cyBpbmZvXCJcbiAgICAgICAgcGxhY2VtZW50PVwicmlnaHQtZW5kXCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICAgICAgPGVsLWJ1dHRvbj5yaWdodC1lbmQ8L2VsLWJ1dHRvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtcG9wb3Zlcj5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwicm93IGNlbnRlclwiPlxuICAgICAgPGVsLXBvcG92ZXJcbiAgICAgICAgdGl0bGU9XCJUaXRsZVwiXG4gICAgICAgIGNvbnRlbnQ9XCJCb3R0b20gTGVmdCBwcm9tcHRzIGluZm9cIlxuICAgICAgICBwbGFjZW1lbnQ9XCJib3R0b20tc3RhcnRcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT4gPGVsLWJ1dHRvbj5ib3R0b20tc3RhcnQ8L2VsLWJ1dHRvbj48L3RlbXBsYXRlPlxuICAgICAgPC9lbC1wb3BvdmVyPlxuICAgICAgPGVsLXBvcG92ZXJcbiAgICAgICAgdGl0bGU9XCJUaXRsZVwiXG4gICAgICAgIGNvbnRlbnQ9XCJCb3R0b20gQ2VudGVyIHByb21wdHMgaW5mb1wiXG4gICAgICAgIHBsYWNlbWVudD1cImJvdHRvbVwiXG4gICAgICA+XG4gICAgICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPiA8ZWwtYnV0dG9uPmJvdHRvbTwvZWwtYnV0dG9uPjwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXBvcG92ZXI+XG4gICAgICA8ZWwtcG9wb3ZlclxuICAgICAgICB0aXRsZT1cIlRpdGxlXCJcbiAgICAgICAgY29udGVudD1cIkJvdHRvbSBSaWdodCBwcm9tcHRzIGluZm9cIlxuICAgICAgICBwbGFjZW1lbnQ9XCJib3R0b20tZW5kXCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICAgICAgPGVsLWJ1dHRvbj5ib3R0b20tZW5kPC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXBvcG92ZXI+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlPlxuLnBvcG92ZXItYmFzZS1ib3gge1xuICB3aWR0aDogNjAwcHg7XG59XG5cbi5wb3BvdmVyLWJhc2UtYm94IC5yb3cge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47XG59XG5cbi5wb3BvdmVyLWJhc2UtYm94IC5jZW50ZXIge1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/popover/placement.vue)_

vue

```
<template>
  <div class="popover-base-box">
    <div class="row center">
      <el-popover
        title="Title"
        content="Top Left prompts info"
        placement="top-start"
      >
        <template #reference>
          <el-button>top-start</el-button>
        </template>
      </el-popover>
      <el-popover
        title="Title"
        content="Top Center prompts info"
        placement="top"
      >
        <template #reference>
          <el-button>top</el-button>
        </template>
      </el-popover>
      <el-popover
        title="Title"
        content="Top Right prompts info"
        placement="top-end"
      >
        <template #reference>
          <el-button>top-end</el-button>
        </template>
      </el-popover>
    </div>
    <div class="row">
      <el-popover
        title="Title"
        content="Left Top prompts info"
        placement="left-start"
      >
        <template #reference>
          <el-button>left-start</el-button>
        </template>
      </el-popover>
      <el-popover
        title="Title"
        content="Right Top prompts info"
        placement="right-start"
      >
        <template #reference>
          <el-button>right-start</el-button>
        </template>
      </el-popover>
    </div>
    <div class="row">
      <el-popover
        title="Title"
        content="Left Center prompts info"
        placement="left"
      >
        <template #reference>
          <el-button class="mt-3 mb-3">left</el-button>
        </template>
      </el-popover>
      <el-popover
        title="Title"
        content="Right Center prompts info"
        placement="right"
      >
        <template #reference>
          <el-button>right</el-button>
        </template>
      </el-popover>
    </div>
    <div class="row">
      <el-popover
        title="Title"
        content="Left Bottom prompts info"
        placement="left-end"
      >
        <template #reference>
          <el-button>left-end</el-button>
        </template>
      </el-popover>
      <el-popover
        title="Title"
        content="Right Bottom prompts info"
        placement="right-end"
      >
        <template #reference>
          <el-button>right-end</el-button>
        </template>
      </el-popover>
    </div>
    <div class="row center">
      <el-popover
        title="Title"
        content="Bottom Left prompts info"
        placement="bottom-start"
      >
        <template #reference> <el-button>bottom-start</el-button></template>
      </el-popover>
      <el-popover
        title="Title"
        content="Bottom Center prompts info"
        placement="bottom"
      >
        <template #reference> <el-button>bottom</el-button></template>
      </el-popover>
      <el-popover
        title="Title"
        content="Bottom Right prompts info"
        placement="bottom-end"
      >
        <template #reference>
          <el-button>bottom-end</el-button>
        </template>
      </el-popover>
    </div>
  </div>
</template>

<style>
.popover-base-box {
  width: 600px;
}

.popover-base-box .row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.popover-base-box .center {
  justify-content: center;
}
</style>
```

隐藏源代码

## 基础用法 [​](#基础用法)

Popover 是在 `ElTooltip` 基础上开发出来的。 因此对于重复属性，请参考 Tooltip 的文档，在此文档中不做详尽解释。

`trigger` 属性被用来决定 popover 的触发方式，支持的触发方式： `hover`、`click`、`focus` 或 `contextmenu`。 如果你想手动控制它，可以设置 `:visible` 属性。

Hover to activateClick to activateFocus to activatecontextmenu to activate Manual to activate

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcG9wb3ZlclxuICAgIHBsYWNlbWVudD1cInRvcC1zdGFydFwiXG4gICAgdGl0bGU9XCJUaXRsZVwiXG4gICAgOndpZHRoPVwiMjAwXCJcbiAgICB0cmlnZ2VyPVwiaG92ZXJcIlxuICAgIGNvbnRlbnQ9XCJ0aGlzIGlzIGNvbnRlbnQsIHRoaXMgaXMgY29udGVudCwgdGhpcyBpcyBjb250ZW50XCJcbiAgPlxuICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPlxuICAgICAgPGVsLWJ1dHRvbiBjbGFzcz1cIm0tMlwiPkhvdmVyIHRvIGFjdGl2YXRlPC9lbC1idXR0b24+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1wb3BvdmVyPlxuXG4gIDxlbC1wb3BvdmVyXG4gICAgcGxhY2VtZW50PVwiYm90dG9tXCJcbiAgICB0aXRsZT1cIlRpdGxlXCJcbiAgICA6d2lkdGg9XCIyMDBcIlxuICAgIHRyaWdnZXI9XCJjbGlja1wiXG4gICAgY29udGVudD1cInRoaXMgaXMgY29udGVudCwgdGhpcyBpcyBjb250ZW50LCB0aGlzIGlzIGNvbnRlbnRcIlxuICA+XG4gICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICA8ZWwtYnV0dG9uIGNsYXNzPVwibS0yXCI+Q2xpY2sgdG8gYWN0aXZhdGU8L2VsLWJ1dHRvbj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLXBvcG92ZXI+XG5cbiAgPGVsLXBvcG92ZXJcbiAgICByZWY9XCJwb3BvdmVyXCJcbiAgICBwbGFjZW1lbnQ9XCJyaWdodFwiXG4gICAgdGl0bGU9XCJUaXRsZVwiXG4gICAgOndpZHRoPVwiMjAwXCJcbiAgICB0cmlnZ2VyPVwiZm9jdXNcIlxuICAgIGNvbnRlbnQ9XCJ0aGlzIGlzIGNvbnRlbnQsIHRoaXMgaXMgY29udGVudCwgdGhpcyBpcyBjb250ZW50XCJcbiAgPlxuICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPlxuICAgICAgPGVsLWJ1dHRvbiBjbGFzcz1cIm0tMlwiPkZvY3VzIHRvIGFjdGl2YXRlPC9lbC1idXR0b24+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1wb3BvdmVyPlxuXG4gIDxlbC1wb3BvdmVyXG4gICAgcmVmPVwicG9wb3ZlclwiXG4gICAgdGl0bGU9XCJUaXRsZVwiXG4gICAgOndpZHRoPVwiMjAwXCJcbiAgICB0cmlnZ2VyPVwiY29udGV4dG1lbnVcIlxuICAgIGNvbnRlbnQ9XCJ0aGlzIGlzIGNvbnRlbnQsIHRoaXMgaXMgY29udGVudCwgdGhpcyBpcyBjb250ZW50XCJcbiAgPlxuICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPlxuICAgICAgPGVsLWJ1dHRvbiBjbGFzcz1cIm0tMlwiPmNvbnRleHRtZW51IHRvIGFjdGl2YXRlPC9lbC1idXR0b24+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1wb3BvdmVyPlxuXG4gIDxlbC1wb3BvdmVyXG4gICAgOnZpc2libGU9XCJ2aXNpYmxlXCJcbiAgICBwbGFjZW1lbnQ9XCJib3R0b21cIlxuICAgIHRpdGxlPVwiVGl0bGVcIlxuICAgIDp3aWR0aD1cIjIwMFwiXG4gICAgY29udGVudD1cInRoaXMgaXMgY29udGVudCwgdGhpcyBpcyBjb250ZW50LCB0aGlzIGlzIGNvbnRlbnRcIlxuICA+XG4gICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICA8ZWwtYnV0dG9uIGNsYXNzPVwibS0yXCIgQGNsaWNrPVwidmlzaWJsZSA9ICF2aXNpYmxlXCI+XG4gICAgICAgIE1hbnVhbCB0byBhY3RpdmF0ZVxuICAgICAgPC9lbC1idXR0b24+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1wb3BvdmVyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmlzaWJsZSA9IHJlZihmYWxzZSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmVsLWJ1dHRvbiArIC5lbC1idXR0b24ge1xuICBtYXJnaW4tbGVmdDogOHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/popover/basic-usage.vue)_

vue

```
<template>
  <el-popover
    placement="top-start"
    title="Title"
    :width="200"
    trigger="hover"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <el-button class="m-2">Hover to activate</el-button>
    </template>
  </el-popover>

  <el-popover
    placement="bottom"
    title="Title"
    :width="200"
    trigger="click"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <el-button class="m-2">Click to activate</el-button>
    </template>
  </el-popover>

  <el-popover
    ref="popover"
    placement="right"
    title="Title"
    :width="200"
    trigger="focus"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <el-button class="m-2">Focus to activate</el-button>
    </template>
  </el-popover>

  <el-popover
    ref="popover"
    title="Title"
    :width="200"
    trigger="contextmenu"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <el-button class="m-2">contextmenu to activate</el-button>
    </template>
  </el-popover>

  <el-popover
    :visible="visible"
    placement="bottom"
    title="Title"
    :width="200"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <el-button class="m-2" @click="visible = !visible">
        Manual to activate
      </el-button>
    </template>
  </el-popover>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const visible = ref(false)
</script>

<style scoped>
.el-button + .el-button {
  margin-left: 8px;
}
</style>
```

隐藏源代码

## 虚拟触发 [​](#虚拟触发)

像 Tooltip一样，Popover 可以由虚拟元素触发，这个功能就很适合使用在触发元素和展示内容元素是分开的场景。通常我们使用 `#reference` 来放置我们的触发元素， 用 `triggering-element` API，您可以任意设置您的触发元素 但注意到触发元素应该是接受 `mouse` 和 `keyboard` 事件的元素。

WARNING

`v-popover` 将被废弃，请使用 `virtual-ref` 作为替代。

Click me

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHJlZj1cImJ1dHRvblJlZlwiIHYtY2xpY2stb3V0c2lkZT1cIm9uQ2xpY2tPdXRzaWRlXCI+XG4gICAgQ2xpY2sgbWVcbiAgPC9lbC1idXR0b24+XG5cbiAgPGVsLXBvcG92ZXJcbiAgICByZWY9XCJwb3BvdmVyUmVmXCJcbiAgICA6dmlydHVhbC1yZWY9XCJidXR0b25SZWZcIlxuICAgIHRyaWdnZXI9XCJjbGlja1wiXG4gICAgdGl0bGU9XCJXaXRoIHRpdGxlXCJcbiAgICB2aXJ0dWFsLXRyaWdnZXJpbmdcbiAgPlxuICAgIDxzcGFuPiBTb21lIGNvbnRlbnQgPC9zcGFuPlxuICA8L2VsLXBvcG92ZXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgQ2xpY2tPdXRzaWRlIGFzIHZDbGlja091dHNpZGUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmltcG9ydCB0eXBlIHsgUG9wb3Zlckluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBidXR0b25SZWYgPSByZWYoKVxuY29uc3QgcG9wb3ZlclJlZiA9IHJlZjxQb3BvdmVySW5zdGFuY2U+KClcbmNvbnN0IG9uQ2xpY2tPdXRzaWRlID0gKCkgPT4ge1xuICBwb3BvdmVyUmVmLnZhbHVlPy5oaWRlKClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/popover/virtual-triggering.vue)_

vue

```
<template>
  <el-button ref="buttonRef" v-click-outside="onClickOutside">
    Click me
  </el-button>

  <el-popover
    ref="popoverRef"
    :virtual-ref="buttonRef"
    trigger="click"
    title="With title"
    virtual-triggering
  >
    <span> Some content </span>
  </el-popover>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ClickOutside as vClickOutside } from 'element-plus'

import type { PopoverInstance } from 'element-plus'

const buttonRef = ref()
const popoverRef = ref<PopoverInstance>()
const onClickOutside = () => {
  popoverRef.value?.hide()
}
</script>
```

隐藏源代码

## 内容可扩展 [​](#内容可扩展)

可以在 Popover 中嵌套其它组件， 以下为嵌套表格的例子。

利用插槽取代 `content` 属性

Click to activate![](https://avatars.githubusercontent.com/u/72015883?v=4)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwiZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IGNlbnRlclwiPlxuICAgIDxlbC1wb3BvdmVyIHBsYWNlbWVudD1cInJpZ2h0XCIgOndpZHRoPVwiNDAwXCIgdHJpZ2dlcj1cImNsaWNrXCI+XG4gICAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgICAgPGVsLWJ1dHRvbiBzdHlsZT1cIm1hcmdpbi1yaWdodDogMTZweFwiPkNsaWNrIHRvIGFjdGl2YXRlPC9lbC1idXR0b24+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgPGVsLXRhYmxlIDpkYXRhPVwiZ3JpZERhdGFcIj5cbiAgICAgICAgPGVsLXRhYmxlLWNvbHVtbiB3aWR0aD1cIjE1MFwiIHByb3BlcnR5PVwiZGF0ZVwiIGxhYmVsPVwiZGF0ZVwiIC8+XG4gICAgICAgIDxlbC10YWJsZS1jb2x1bW4gd2lkdGg9XCIxMDBcIiBwcm9wZXJ0eT1cIm5hbWVcIiBsYWJlbD1cIm5hbWVcIiAvPlxuICAgICAgICA8ZWwtdGFibGUtY29sdW1uIHdpZHRoPVwiMzAwXCIgcHJvcGVydHk9XCJhZGRyZXNzXCIgbGFiZWw9XCJhZGRyZXNzXCIgLz5cbiAgICAgIDwvZWwtdGFibGU+XG4gICAgPC9lbC1wb3BvdmVyPlxuXG4gICAgPGVsLXBvcG92ZXJcbiAgICAgIDp3aWR0aD1cIjMwMFwiXG4gICAgICBwb3BwZXItc3R5bGU9XCJib3gtc2hhZG93OiByZ2IoMTQgMTggMjIgLyAzNSUpIDBweCAxMHB4IDM4cHggLTEwcHgsIHJnYigxNCAxOCAyMiAvIDIwJSkgMHB4IDEwcHggMjBweCAtMTVweDsgcGFkZGluZzogMjBweDtcIlxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPlxuICAgICAgICA8ZWwtYXZhdGFyIHNyYz1cImh0dHBzOi8vYXZhdGFycy5naXRodWJ1c2VyY29udGVudC5jb20vdS83MjAxNTg4Mz92PTRcIiAvPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD5cbiAgICAgICAgPGRpdlxuICAgICAgICAgIGNsYXNzPVwiZGVtby1yaWNoLWNvbmVudFwiXG4gICAgICAgICAgc3R5bGU9XCJkaXNwbGF5OiBmbGV4OyBnYXA6IDE2cHg7IGZsZXgtZGlyZWN0aW9uOiBjb2x1bW5cIlxuICAgICAgICA+XG4gICAgICAgICAgPGVsLWF2YXRhclxuICAgICAgICAgICAgOnNpemU9XCI2MFwiXG4gICAgICAgICAgICBzcmM9XCJodHRwczovL2F2YXRhcnMuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3UvNzIwMTU4ODM/dj00XCJcbiAgICAgICAgICAgIHN0eWxlPVwibWFyZ2luLWJvdHRvbTogOHB4XCJcbiAgICAgICAgICAvPlxuICAgICAgICAgIDxkaXY+XG4gICAgICAgICAgICA8cFxuICAgICAgICAgICAgICBjbGFzcz1cImRlbW8tcmljaC1jb250ZW50X19uYW1lXCJcbiAgICAgICAgICAgICAgc3R5bGU9XCJtYXJnaW46IDA7IGZvbnQtd2VpZ2h0OiA1MDBcIlxuICAgICAgICAgICAgPlxuICAgICAgICAgICAgICBFbGVtZW50IFBsdXNcbiAgICAgICAgICAgIDwvcD5cbiAgICAgICAgICAgIDxwXG4gICAgICAgICAgICAgIGNsYXNzPVwiZGVtby1yaWNoLWNvbnRlbnRfX21lbnRpb25cIlxuICAgICAgICAgICAgICBzdHlsZT1cIm1hcmdpbjogMDsgZm9udC1zaXplOiAxNHB4OyBjb2xvcjogdmFyKC0tZWwtY29sb3ItaW5mbylcIlxuICAgICAgICAgICAgPlxuICAgICAgICAgICAgICBAZWxlbWVudC1wbHVzXG4gICAgICAgICAgICA8L3A+XG4gICAgICAgICAgPC9kaXY+XG5cbiAgICAgICAgICA8cCBjbGFzcz1cImRlbW8tcmljaC1jb250ZW50X19kZXNjXCIgc3R5bGU9XCJtYXJnaW46IDBcIj5cbiAgICAgICAgICAgIEVsZW1lbnQgUGx1cywgYSBWdWUgMyBiYXNlZCBjb21wb25lbnQgbGlicmFyeSBmb3IgZGV2ZWxvcGVycyxcbiAgICAgICAgICAgIGRlc2lnbmVycyBhbmQgcHJvZHVjdCBtYW5hZ2Vyc1xuICAgICAgICAgIDwvcD5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtcG9wb3Zlcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuY29uc3QgZ3JpZERhdGEgPSBbXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMicsXG4gICAgbmFtZTogJ0phY2snLFxuICAgIGFkZHJlc3M6ICdOZXcgWW9yayBDaXR5JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA0JyxcbiAgICBuYW1lOiAnSmFjaycsXG4gICAgYWRkcmVzczogJ05ldyBZb3JrIENpdHknLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgIG5hbWU6ICdKYWNrJyxcbiAgICBhZGRyZXNzOiAnTmV3IFlvcmsgQ2l0eScsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ0phY2snLFxuICAgIGFkZHJlc3M6ICdOZXcgWW9yayBDaXR5JyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/popover/nested-information.vue)_

vue

```
<template>
  <div style="display: flex; align-items: center">
    <el-popover placement="right" :width="400" trigger="click">
      <template #reference>
        <el-button style="margin-right: 16px">Click to activate</el-button>
      </template>
      <el-table :data="gridData">
        <el-table-column width="150" property="date" label="date" />
        <el-table-column width="100" property="name" label="name" />
        <el-table-column width="300" property="address" label="address" />
      </el-table>
    </el-popover>

    <el-popover
      :width="300"
      popper-style="box-shadow: rgb(14 18 22 / 35%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px;"
    >
      <template #reference>
        <el-avatar src="https://avatars.githubusercontent.com/u/72015883?v=4" />
      </template>
      <template #default>
        <div
          class="demo-rich-conent"
          style="display: flex; gap: 16px; flex-direction: column"
        >
          <el-avatar
            :size="60"
            src="https://avatars.githubusercontent.com/u/72015883?v=4"
            style="margin-bottom: 8px"
          />
          <div>
            <p
              class="demo-rich-content__name"
              style="margin: 0; font-weight: 500"
            >
              Element Plus
            </p>
            <p
              class="demo-rich-content__mention"
              style="margin: 0; font-size: 14px; color: var(--el-color-info)"
            >
              @element-plus
            </p>
          </div>

          <p class="demo-rich-content__desc" style="margin: 0">
            Element Plus, a Vue 3 based component library for developers,
            designers and product managers
          </p>
        </div>
      </template>
    </el-popover>
  </div>
</template>

<script lang="ts" setup>
const gridData = [
  {
    date: '2016-05-02',
    name: 'Jack',
    address: 'New York City',
  },
  {
    date: '2016-05-04',
    name: 'Jack',
    address: 'New York City',
  },
  {
    date: '2016-05-01',
    name: 'Jack',
    address: 'New York City',
  },
  {
    date: '2016-05-03',
    name: 'Jack',
    address: 'New York City',
  },
]
</script>
```

隐藏源代码

## 嵌套操作 [​](#嵌套操作)

当然，你还可以嵌套操作， 它比使用dialog更加轻量。

Delete

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcG9wb3ZlciA6dmlzaWJsZT1cInZpc2libGVcIiBwbGFjZW1lbnQ9XCJ0b3BcIiA6d2lkdGg9XCIxODBcIj5cbiAgICA8cD5BcmUgeW91IHN1cmUgdG8gZGVsZXRlIHRoaXM/PC9wPlxuICAgIDxkaXYgc3R5bGU9XCJ0ZXh0LWFsaWduOiByaWdodDsgbWFyZ2luOiAwXCI+XG4gICAgICA8ZWwtYnV0dG9uIHNpemU9XCJzbWFsbFwiIHRleHQgQGNsaWNrPVwidmlzaWJsZSA9IGZhbHNlXCI+Y2FuY2VsPC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIHNpemU9XCJzbWFsbFwiIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwidmlzaWJsZSA9IGZhbHNlXCI+XG4gICAgICAgIGNvbmZpcm1cbiAgICAgIDwvZWwtYnV0dG9uPlxuICAgIDwvZGl2PlxuICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPlxuICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJ2aXNpYmxlID0gdHJ1ZVwiPkRlbGV0ZTwvZWwtYnV0dG9uPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtcG9wb3Zlcj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZpc2libGUgPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/popover/nested-operation.vue)_

vue

```
<template>
  <el-popover :visible="visible" placement="top" :width="180">
    <p>Are you sure to delete this?</p>
    <div style="text-align: right; margin: 0">
      <el-button size="small" text @click="visible = false">cancel</el-button>
      <el-button size="small" type="primary" @click="visible = false">
        confirm
      </el-button>
    </div>
    <template #reference>
      <el-button @click="visible = true">Delete</el-button>
    </template>
  </el-popover>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const visible = ref(false)
</script>
```

隐藏源代码

## 指令 [​](#指令)

您可以使用指令性方式弹出窗口，但这种方法**不再推荐** ，因为这使得应用程序变得复杂， 您可以参考虚拟触发来实现一样的效果。

Click me

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHYtcG9wb3Zlcj1cInBvcG92ZXJSZWZcIiB2LWNsaWNrLW91dHNpZGU9XCJvbkNsaWNrT3V0c2lkZVwiPlxuICAgIENsaWNrIG1lXG4gIDwvZWwtYnV0dG9uPlxuXG4gIDxlbC1wb3BvdmVyXG4gICAgcmVmPVwicG9wb3ZlclJlZlwiXG4gICAgdHJpZ2dlcj1cImNsaWNrXCJcbiAgICB0aXRsZT1cIldpdGggdGl0bGVcIlxuICAgIHZpcnR1YWwtdHJpZ2dlcmluZ1xuICAgIHBlcnNpc3RlbnRcbiAgPlxuICAgIDxzcGFuPiBTb21lIGNvbnRlbnQgPC9zcGFuPlxuICA8L2VsLXBvcG92ZXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgQ2xpY2tPdXRzaWRlIGFzIHZDbGlja091dHNpZGUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmltcG9ydCB0eXBlIHsgUG9wb3Zlckluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBwb3BvdmVyUmVmID0gcmVmPFBvcG92ZXJJbnN0YW5jZT4oKVxuY29uc3Qgb25DbGlja091dHNpZGUgPSAoKSA9PiB7XG4gIHBvcG92ZXJSZWYudmFsdWU/LmhpZGUoKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/popover/directive-usage.vue)_

vue

```
<template>
  <el-button v-popover="popoverRef" v-click-outside="onClickOutside">
    Click me
  </el-button>

  <el-popover
    ref="popoverRef"
    trigger="click"
    title="With title"
    virtual-triggering
    persistent
  >
    <span> Some content </span>
  </el-popover>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ClickOutside as vClickOutside } from 'element-plus'

import type { PopoverInstance } from 'element-plus'

const popoverRef = ref<PopoverInstance>()
const onClickOutside = () => {
  popoverRef.value?.hide()
}
</script>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | Default |
| --- | --- | --- | --- |
| trigger | popover 触发方式，在受控模式下无效。 | `enum` / `array` | hover |
| trigger-keys 2.9.8 | 当通过鼠标点击使触发元素获得焦点时，可以定义一组键盘按键代码，通过键盘控制气泡框的显示，在受控模式下无效。 | `Array` | \['Enter','Space'\] |
| title | 标题 | `string` | — |
| effect | Tooltip 主题，Element Plus 内置了 `dark` / `light` 两种主题 | `enum` / `string` | light |
| content | 显示的内容，也可以通过写入默认 `slot` 修改显示内容 | `string` | '' |
| width | 宽度 | `string` / `number` | 150 |
| placement | 出现位置 | `enum` | bottom |
| disabled | Popover 是否可用 | `boolean` | false |
| visible / v-model:visible | Popover 是否显示 | `boolean` / `null` | null |
| offset | 浮层偏移量, `Popover` 是在 `Tooltip`,基础上开发的， `Popover`的 offset 是 `undefined`, 但`Tooltip` 的 offset 是12 | `number` | undefined |
| transition | 定义渐变动画，默认是 el-fade-in-linear | `string` | — |
| show-arrow | 是否显示 Tooltip 箭头， 欲了解更多信息，请参考 [ElPopper](https://github.com/element-plus/element-plus/tree/dev/packages/components/popper) | `boolean` | true |
| popper-options | [popper.js](https://popper.js.org/docs/v2/) 的参数 | `object` | `{modifiers: [{name: 'computeStyles',options: {gpuAcceleration: false}}]}` |
| popper-class | 为 popper 添加类名 | `string` | — |
| popper-style | 为 popper 自定义样式 | `string` / `object` | — |
| show-after | 延迟显示时间（以毫秒为单位），在受控模式下无效。 | `number` | 0 |
| hide-after | 消失延迟时间（以毫秒为单位），在受控模式下无效。 | `number` | 200 |
| auto-close | 隐藏提示框的超时时间（以毫秒为单位），在受控模式下无效。 | `number` | 0 |
| tabindex | Popover 组件的 [tabindex](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Global_attributes/tabindex) | `number` / `string` | 0 |
| teleported | 是否将 popover 的下拉列表插入至 body 元素 | `boolean` | true |
| append-to 2.8.4 | 指示 Tooltip 的内容将附加在哪一个网页元素上 | `CSSSelector` / `HTMLElement` | body |
| persistent | 当 popover 组件长时间不触发且 `persistent` 属性设置为 `false` 时, popover 将会被删除 | `boolean` | true |
| virtual-triggering | 是否启用虚拟触发器 | `boolean` | — |
| virtual-ref | 代表 tooltip 所要附加的参照元素 | `HTMLElement` | — |
| [tooltip](https://element-plus.org/zh-CN/component/tooltip#attributes) | 继承自 Tooltip 的所有属性 | ::: | — |

### Slots [​](#slots)

| 插槽名 | 说明 | Type |
| --- | --- | --- |
| default | 弹出框的内容，2.13.4 及之后版本可以接收 hide 参数。 | `object` |
| reference | 触发弹出框的 HTML 元素，只接受单个根元素。 | \- |

### Events [​](#events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| show | 显示时触发 | `Function` |
| before-enter | 显示动画播放前触发 | `Function` |
| after-enter | 显示动画播放完毕后触发 | `Function` |
| hide | 隐藏时触发 | `Function` |
| before-leave | 隐藏动画播放前触发 | `Function` |
| after-leave | 隐藏动画播放完毕后触发 | `Function` |

### Exposes [​](#exposes)

| 名称 | 详情 | Type |
| --- | --- | --- |
| hide | 隐藏 popover | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/popover) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/popover.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/popover.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/200161722?v=4&size=64)](https://github.com/changchi666)[![](https://avatars.githubusercontent.com/u/62818957?v=4&size=64)](https://github.com/ZacharyBear)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/30046649?v=4&size=64)](https://github.com/MrWeilian)[![](https://avatars.githubusercontent.com/u/169252980?v=4&size=64)](https://github.com/xiaochenchen-igg-com)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/21095710?v=4&size=64)](https://github.com/zouhangwithsweet)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/140705167?v=4&size=64)](https://github.com/zhongli-kira)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/60031458?v=4&size=64)](https://github.com/sefaun)[![](https://avatars.githubusercontent.com/u/24362871?v=4&size=64)](https://github.com/Benleie)[![](https://avatars.githubusercontent.com/u/234136872?v=4&size=64)](https://github.com/z-kunf)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/56570859?v=4&size=64)](https://github.com/XSUV)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/84843371?v=4&size=64)](https://github.com/ignaceshi)[![](https://avatars.githubusercontent.com/u/36811055?v=4&size=64)](https://github.com/iDestin)[![](https://avatars.githubusercontent.com/u/643976?v=4&size=64)](https://github.com/ghiscoding)

[Popconfirm 气泡确认框](https://element-plus.org/zh-CN/component/popconfirm)

[Tooltip 文字提示](https://element-plus.org/zh-CN/component/tooltip)


