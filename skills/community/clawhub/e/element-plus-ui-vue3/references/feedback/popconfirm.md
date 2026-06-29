---
name: "popconfirm"
description: "Popconfirm 气泡确认框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Popconfirm 气泡确认框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/popconfirm.html"
---

---

# Popconfirm 气泡确认框 [​](#popconfirm-气泡确认框)

更新日志待解决

4

点击某个元素弹出一个简单的气泡确认框

## 展示位置 [​](#展示位置)

Popconfirm 提供 9 种展示位置。

使用 `title` 属性来设置点击参考元素时显示的信息。 由 `placement` 属性决定 Popconfirm 的位置。 该属性值格式为：`[方向]-[对齐位置]`，可供选择的四个方向分别是`top`、`left`、`right`、`bottom`，可供选择的三种对齐方式分别是`start`、`end`、`null`，默认的对齐方式为null。 以 `placement="left-end"` 为例，气泡确认框会显示在悬停元素的左侧，且提示信息的底部与悬停元素的底部对齐。

top-starttoptop-end

left-startright-start

leftright

left-endright-end

bottom-startbottombottom-end

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwicG9wY29uZmlybS1iYXNlLWJveFwiPlxuICAgIDxkaXYgY2xhc3M9XCJyb3cgY2VudGVyXCI+XG4gICAgICA8ZWwtcG9wY29uZmlybVxuICAgICAgICBjbGFzcz1cImJveC1pdGVtXCJcbiAgICAgICAgdGl0bGU9XCJUb3AgTGVmdCBwcm9tcHRzIGluZm9cIlxuICAgICAgICBwbGFjZW1lbnQ9XCJ0b3Atc3RhcnRcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgICAgICA8ZWwtYnV0dG9uPnRvcC1zdGFydDwvZWwtYnV0dG9uPlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgPC9lbC1wb3Bjb25maXJtPlxuICAgICAgPGVsLXBvcGNvbmZpcm1cbiAgICAgICAgY2xhc3M9XCJib3gtaXRlbVwiXG4gICAgICAgIHRpdGxlPVwiVG9wIENlbnRlciBwcm9tcHRzIGluZm9cIlxuICAgICAgICBwbGFjZW1lbnQ9XCJ0b3BcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgICAgICA8ZWwtYnV0dG9uPnRvcDwvZWwtYnV0dG9uPlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgPC9lbC1wb3Bjb25maXJtPlxuICAgICAgPGVsLXBvcGNvbmZpcm1cbiAgICAgICAgY2xhc3M9XCJib3gtaXRlbVwiXG4gICAgICAgIHRpdGxlPVwiVG9wIFJpZ2h0IHByb21wdHMgaW5mb1wiXG4gICAgICAgIHBsYWNlbWVudD1cInRvcC1lbmRcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgICAgICA8ZWwtYnV0dG9uPnRvcC1lbmQ8L2VsLWJ1dHRvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtcG9wY29uZmlybT5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwicm93XCI+XG4gICAgICA8ZWwtcG9wY29uZmlybVxuICAgICAgICBjbGFzcz1cImJveC1pdGVtXCJcbiAgICAgICAgdGl0bGU9XCJMZWZ0IFRvcCBwcm9tcHRzIGluZm9cIlxuICAgICAgICBwbGFjZW1lbnQ9XCJsZWZ0LXN0YXJ0XCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICAgICAgPGVsLWJ1dHRvbj5sZWZ0LXN0YXJ0PC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXBvcGNvbmZpcm0+XG4gICAgICA8ZWwtcG9wY29uZmlybVxuICAgICAgICBjbGFzcz1cImJveC1pdGVtXCJcbiAgICAgICAgdGl0bGU9XCJSaWdodCBUb3AgcHJvbXB0cyBpbmZvXCJcbiAgICAgICAgcGxhY2VtZW50PVwicmlnaHQtc3RhcnRcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgICAgICA8ZWwtYnV0dG9uPnJpZ2h0LXN0YXJ0PC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXBvcGNvbmZpcm0+XG4gICAgPC9kaXY+XG4gICAgPGRpdiBjbGFzcz1cInJvd1wiPlxuICAgICAgPGVsLXBvcGNvbmZpcm1cbiAgICAgICAgY2xhc3M9XCJib3gtaXRlbVwiXG4gICAgICAgIHRpdGxlPVwiTGVmdCBDZW50ZXIgcHJvbXB0cyBpbmZvXCJcbiAgICAgICAgcGxhY2VtZW50PVwibGVmdFwiXG4gICAgICA+XG4gICAgICAgIDx0ZW1wbGF0ZSAjcmVmZXJlbmNlPlxuICAgICAgICAgIDxlbC1idXR0b24gY2xhc3M9XCJtdC0zIG1iLTNcIj5sZWZ0PC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXBvcGNvbmZpcm0+XG4gICAgICA8ZWwtcG9wY29uZmlybVxuICAgICAgICBjbGFzcz1cImJveC1pdGVtXCJcbiAgICAgICAgdGl0bGU9XCJSaWdodCBDZW50ZXIgcHJvbXB0cyBpbmZvXCJcbiAgICAgICAgcGxhY2VtZW50PVwicmlnaHRcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgICAgICA8ZWwtYnV0dG9uPnJpZ2h0PC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXBvcGNvbmZpcm0+XG4gICAgPC9kaXY+XG4gICAgPGRpdiBjbGFzcz1cInJvd1wiPlxuICAgICAgPGVsLXBvcGNvbmZpcm1cbiAgICAgICAgY2xhc3M9XCJib3gtaXRlbVwiXG4gICAgICAgIHRpdGxlPVwiTGVmdCBCb3R0b20gcHJvbXB0cyBpbmZvXCJcbiAgICAgICAgcGxhY2VtZW50PVwibGVmdC1lbmRcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgICAgICA8ZWwtYnV0dG9uPmxlZnQtZW5kPC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXBvcGNvbmZpcm0+XG4gICAgICA8ZWwtcG9wY29uZmlybVxuICAgICAgICBjbGFzcz1cImJveC1pdGVtXCJcbiAgICAgICAgdGl0bGU9XCJSaWdodCBCb3R0b20gcHJvbXB0cyBpbmZvXCJcbiAgICAgICAgcGxhY2VtZW50PVwicmlnaHQtZW5kXCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICAgICAgPGVsLWJ1dHRvbj5yaWdodC1lbmQ8L2VsLWJ1dHRvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtcG9wY29uZmlybT5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwicm93IGNlbnRlclwiPlxuICAgICAgPGVsLXBvcGNvbmZpcm1cbiAgICAgICAgY2xhc3M9XCJib3gtaXRlbVwiXG4gICAgICAgIHRpdGxlPVwiQm90dG9tIExlZnQgcHJvbXB0cyBpbmZvXCJcbiAgICAgICAgcGxhY2VtZW50PVwiYm90dG9tLXN0YXJ0XCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+IDxlbC1idXR0b24+Ym90dG9tLXN0YXJ0PC9lbC1idXR0b24+PC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtcG9wY29uZmlybT5cbiAgICAgIDxlbC1wb3Bjb25maXJtXG4gICAgICAgIGNsYXNzPVwiYm94LWl0ZW1cIlxuICAgICAgICB0aXRsZT1cIkJvdHRvbSBDZW50ZXIgcHJvbXB0cyBpbmZvXCJcbiAgICAgICAgcGxhY2VtZW50PVwiYm90dG9tXCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+IDxlbC1idXR0b24+Ym90dG9tPC9lbC1idXR0b24+PC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtcG9wY29uZmlybT5cbiAgICAgIDxlbC1wb3Bjb25maXJtXG4gICAgICAgIGNsYXNzPVwiYm94LWl0ZW1cIlxuICAgICAgICB0aXRsZT1cIkJvdHRvbSBSaWdodCBwcm9tcHRzIGluZm9cIlxuICAgICAgICBwbGFjZW1lbnQ9XCJib3R0b20tZW5kXCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICAgICAgPGVsLWJ1dHRvbj5ib3R0b20tZW5kPC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXBvcGNvbmZpcm0+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlPlxuLnBvcGNvbmZpcm0tYmFzZS1ib3gge1xuICB3aWR0aDogNjAwcHg7XG59XG5cbi5wb3Bjb25maXJtLWJhc2UtYm94IC5yb3cge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47XG59XG5cbi5wb3Bjb25maXJtLWJhc2UtYm94IC5jZW50ZXIge1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbn1cblxuLnBvcGNvbmZpcm0tYmFzZS1ib3ggLmJveC1pdGVtIHtcbiAgd2lkdGg6IDExMHB4O1xuICBtYXJnaW4tdG9wOiAxMHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/popconfirm/placement.vue)_

vue

```
<template>
  <div class="popconfirm-base-box">
    <div class="row center">
      <el-popconfirm
        class="box-item"
        title="Top Left prompts info"
        placement="top-start"
      >
        <template #reference>
          <el-button>top-start</el-button>
        </template>
      </el-popconfirm>
      <el-popconfirm
        class="box-item"
        title="Top Center prompts info"
        placement="top"
      >
        <template #reference>
          <el-button>top</el-button>
        </template>
      </el-popconfirm>
      <el-popconfirm
        class="box-item"
        title="Top Right prompts info"
        placement="top-end"
      >
        <template #reference>
          <el-button>top-end</el-button>
        </template>
      </el-popconfirm>
    </div>
    <div class="row">
      <el-popconfirm
        class="box-item"
        title="Left Top prompts info"
        placement="left-start"
      >
        <template #reference>
          <el-button>left-start</el-button>
        </template>
      </el-popconfirm>
      <el-popconfirm
        class="box-item"
        title="Right Top prompts info"
        placement="right-start"
      >
        <template #reference>
          <el-button>right-start</el-button>
        </template>
      </el-popconfirm>
    </div>
    <div class="row">
      <el-popconfirm
        class="box-item"
        title="Left Center prompts info"
        placement="left"
      >
        <template #reference>
          <el-button class="mt-3 mb-3">left</el-button>
        </template>
      </el-popconfirm>
      <el-popconfirm
        class="box-item"
        title="Right Center prompts info"
        placement="right"
      >
        <template #reference>
          <el-button>right</el-button>
        </template>
      </el-popconfirm>
    </div>
    <div class="row">
      <el-popconfirm
        class="box-item"
        title="Left Bottom prompts info"
        placement="left-end"
      >
        <template #reference>
          <el-button>left-end</el-button>
        </template>
      </el-popconfirm>
      <el-popconfirm
        class="box-item"
        title="Right Bottom prompts info"
        placement="right-end"
      >
        <template #reference>
          <el-button>right-end</el-button>
        </template>
      </el-popconfirm>
    </div>
    <div class="row center">
      <el-popconfirm
        class="box-item"
        title="Bottom Left prompts info"
        placement="bottom-start"
      >
        <template #reference> <el-button>bottom-start</el-button></template>
      </el-popconfirm>
      <el-popconfirm
        class="box-item"
        title="Bottom Center prompts info"
        placement="bottom"
      >
        <template #reference> <el-button>bottom</el-button></template>
      </el-popconfirm>
      <el-popconfirm
        class="box-item"
        title="Bottom Right prompts info"
        placement="bottom-end"
      >
        <template #reference>
          <el-button>bottom-end</el-button>
        </template>
      </el-popconfirm>
    </div>
  </div>
</template>

<style>
.popconfirm-base-box {
  width: 600px;
}

.popconfirm-base-box .row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.popconfirm-base-box .center {
  justify-content: center;
}

.popconfirm-base-box .box-item {
  width: 110px;
  margin-top: 10px;
}
</style>
```

隐藏源代码

## 基础用法 [​](#基础用法)

Popconfirm 的属性与 Popover 很类似， 因此对于重复属性，请参考 Popover 的文档，在此文档中不做详尽解释。

在 Popconfirm 中，只有 `title` 属性可用，`content` 属性会被忽略。

Delete

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcG9wY29uZmlybSB0aXRsZT1cIkFyZSB5b3Ugc3VyZSB0byBkZWxldGUgdGhpcz9cIj5cbiAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgIDxlbC1idXR0b24+RGVsZXRlPC9lbC1idXR0b24+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1wb3Bjb25maXJtPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/popconfirm/basic-usage.vue)_

vue

```
<template>
  <el-popconfirm title="Are you sure to delete this?">
    <template #reference>
      <el-button>Delete</el-button>
    </template>
  </el-popconfirm>
</template>
```

隐藏源代码

## 自定义弹出框的内容 [​](#自定义弹出框的内容)

可以在 Popconfirm 中自定义内容。

Delete

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcG9wY29uZmlybVxuICAgIHdpZHRoPVwiMjIwXCJcbiAgICA6aWNvbj1cIkluZm9GaWxsZWRcIlxuICAgIGljb24tY29sb3I9XCIjNjI2QUVGXCJcbiAgICB0aXRsZT1cIkFyZSB5b3Ugc3VyZSB0byBkZWxldGUgdGhpcz9cIlxuICAgIEBjYW5jZWw9XCJvbkNhbmNlbFwiXG4gID5cbiAgICA8dGVtcGxhdGUgI3JlZmVyZW5jZT5cbiAgICAgIDxlbC1idXR0b24+RGVsZXRlPC9lbC1idXR0b24+XG4gICAgPC90ZW1wbGF0ZT5cbiAgICA8dGVtcGxhdGUgI2FjdGlvbnM9XCJ7IGNvbmZpcm0sIGNhbmNlbCB9XCI+XG4gICAgICA8ZWwtYnV0dG9uIHNpemU9XCJzbWFsbFwiIEBjbGljaz1cImNhbmNlbFwiPk5vITwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvblxuICAgICAgICB0eXBlPVwiZGFuZ2VyXCJcbiAgICAgICAgc2l6ZT1cInNtYWxsXCJcbiAgICAgICAgOmRpc2FibGVkPVwiIWNsaWNrZWRcIlxuICAgICAgICBAY2xpY2s9XCJjb25maXJtXCJcbiAgICAgID5cbiAgICAgICAgWWVzP1xuICAgICAgPC9lbC1idXR0b24+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1wb3Bjb25maXJtPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEluZm9GaWxsZWQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgY2xpY2tlZCA9IHJlZihmYWxzZSlcbmZ1bmN0aW9uIG9uQ2FuY2VsKCkge1xuICBjbGlja2VkLnZhbHVlID0gdHJ1ZVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/popconfirm/customize.vue)_

vue

```
<template>
  <el-popconfirm
    width="220"
    :icon="InfoFilled"
    icon-color="#626AEF"
    title="Are you sure to delete this?"
    @cancel="onCancel"
  >
    <template #reference>
      <el-button>Delete</el-button>
    </template>
    <template #actions="{ confirm, cancel }">
      <el-button size="small" @click="cancel">No!</el-button>
      <el-button
        type="danger"
        size="small"
        :disabled="!clicked"
        @click="confirm"
      >
        Yes?
      </el-button>
    </template>
  </el-popconfirm>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { InfoFilled } from '@element-plus/icons-vue'

const clicked = ref(false)
function onCancel() {
  clicked.value = true
}
</script>
```

隐藏源代码

## 多种让 Popconfirm 出现的方法 [​](#多种让-popconfirm-出现的方法)

点击按钮触发事件

Delete

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcG9wY29uZmlybVxuICAgIGNvbmZpcm0tYnV0dG9uLXRleHQ9XCJZZXNcIlxuICAgIGNhbmNlbC1idXR0b24tdGV4dD1cIk5vXCJcbiAgICA6aWNvbj1cIkluZm9GaWxsZWRcIlxuICAgIGljb24tY29sb3I9XCIjNjI2QUVGXCJcbiAgICB0aXRsZT1cIkFyZSB5b3Ugc3VyZSB0byBkZWxldGUgdGhpcz9cIlxuICAgIEBjb25maXJtPVwiY29uZmlybUV2ZW50XCJcbiAgICBAY2FuY2VsPVwiY2FuY2VsRXZlbnRcIlxuICA+XG4gICAgPHRlbXBsYXRlICNyZWZlcmVuY2U+XG4gICAgICA8ZWwtYnV0dG9uPkRlbGV0ZTwvZWwtYnV0dG9uPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtcG9wY29uZmlybT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+XG5pbXBvcnQgeyBJbmZvRmlsbGVkIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IGNvbmZpcm1FdmVudCA9ICgpID0+IHtcbiAgY29uc29sZS5sb2coJ2NvbmZpcm0hJylcbn1cbmNvbnN0IGNhbmNlbEV2ZW50ID0gKCkgPT4ge1xuICBjb25zb2xlLmxvZygnY2FuY2VsIScpXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/popconfirm/trigger-event.vue)_

vue

```
<template>
  <el-popconfirm
    confirm-button-text="Yes"
    cancel-button-text="No"
    :icon="InfoFilled"
    icon-color="#626AEF"
    title="Are you sure to delete this?"
    @confirm="confirmEvent"
    @cancel="cancelEvent"
  >
    <template #reference>
      <el-button>Delete</el-button>
    </template>
  </el-popconfirm>
</template>

<script setup lang="ts">
import { InfoFilled } from '@element-plus/icons-vue'

const confirmEvent = () => {
  console.log('confirm!')
}
const cancelEvent = () => {
  console.log('cancel!')
}
</script>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| title | 标题 | `string` | — |
| effect 2.11.2 | Tooltip 主题，内置了 `dark` / `light` 两种 | `enum` / `string` | light |
| confirm-button-text | 确认按钮文字 | `string` | — |
| cancel-button-text | 取消按钮文字 | `string` | — |
| confirm-button-type | 确认按钮类型 | `enum` | primary |
| cancel-button-type | 取消按钮类型 | `enum` | text |
| icon | 自定义图标 | `string` / `Component` | QuestionFilled |
| icon-color | Icon 颜色 | `string` | #f90 |
| hide-icon | 是否隐藏 Icon | `boolean` | false |
| hide-after | 关闭时的延迟 | `number` | 200 |
| teleported | 是否将 popover 的下拉列表插入至 body 元素 | `boolean` | true |
| persistent | 当 popover 组件长时间不触发且 `persistent` 属性设置为 `false` 时, popover 将会被删除 | `boolean` | false |
| width | 弹层宽度，最小宽度 150px | `string` / `number` | 150 |
| [tooltip](https://element-plus.org/zh-CN/component/tooltip#attributes) | 继承自 Tooltip 的所有属性，但不包括：`popper-class`、`popper-style`、`fallback-placements` | — | — |

### Events [​](#events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| confirm | 点击确认按钮时触发 | `Function` |
| cancel | 点击取消按钮时触发 | `Function` |

### Slots [​](#slots)

| 插槽名 | 说明 | 类型 |
| --- | --- | --- |
| reference | 触发 Popconfirm 显示的 HTML 元素 | — |
| actions 2.8.1 | 页脚的内容 | `object` |

### 暴露 [​](#暴露)

| 方法名 | 详情 | Type |
| --- | --- | --- |
| popperRef 2.10.7 | el-popper 组件实例 | `object` |
| hide 2.10.7 | hide popconfirm | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/popconfirm) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/popconfirm.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/popconfirm.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/31238760?v=4&size=64)](https://github.com/cloydlau)[![](https://avatars.githubusercontent.com/u/24540820?v=4&size=64)](https://github.com/catanswer)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/13634675?v=4&size=64)](https://github.com/virgosoy)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)

[Notification 通知](https://element-plus.org/zh-CN/component/notification)

[Popover 弹出框](https://element-plus.org/zh-CN/component/popover)


