---
name: "drawer"
description: "Drawer 抽屉 -- Element Plus Vue3 桌面端组件。Invoke when user needs Drawer 抽屉 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/drawer.html"
---

---

# Drawer 抽屉 [​](#drawer-抽屉)

更新日志待解决

8

有些时候, `Dialog` 组件并不满足我们的需求, 比如你的表单很长, 亦或是你需要临时展示一些文档, `Drawer` 拥有和 `Dialog` 几乎相同的 API, 在 UI 上带来不一样的体验.

TIP

在 Vue 3 之后的版本 v-model 可以用于任何一个组件，`visible.sync` 已被移除，请使用 `v-model="visibilityBinding"` 来控制抽屉组件的显示和隐藏状态。

## 基础用法 [​](#基础用法)

呼出一个临时的侧边栏, 可以从多个方向呼出

你必须像 `Dialog`一样为 `Drawer` 设置 `model-value` 属性来控制 `Drawer` 的显示与隐藏状态，该属性接受一个 `boolean` 类型。 `Drawer` 包含三部分: `title` & `body` & `footer`, 其中 `title` 是一个具名 slot, 你还可以通过 `title` 属性来设置标题, 默认情况下它是一个空字符串, 其中 `body` 部分是 `Drawer` 组件的主区域, 它包含了用户定义的主要内容. footer和title用法一致, 用来显示页脚信息. 当 `Drawer` 打开时，默认设置是**从右至左**打开 **30%** 浏览器宽度。 你可以通过传入对应的 `direction` 和 `size` 属性来修改这一默认行为。 下面一个示例将展示如何使用 `before-close` API，更多详细用法请参考页面底部的 API 部分。

left to rightright to lefttop to bottombottom to top

open with footer

cancelconfirm

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cImRpcmVjdGlvblwiPlxuICAgIDxlbC1yYWRpbyB2YWx1ZT1cImx0clwiPmxlZnQgdG8gcmlnaHQ8L2VsLXJhZGlvPlxuICAgIDxlbC1yYWRpbyB2YWx1ZT1cInJ0bFwiPnJpZ2h0IHRvIGxlZnQ8L2VsLXJhZGlvPlxuICAgIDxlbC1yYWRpbyB2YWx1ZT1cInR0YlwiPnRvcCB0byBib3R0b208L2VsLXJhZGlvPlxuICAgIDxlbC1yYWRpbyB2YWx1ZT1cImJ0dFwiPmJvdHRvbSB0byB0b3A8L2VsLXJhZGlvPlxuICA8L2VsLXJhZGlvLWdyb3VwPlxuXG4gIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBzdHlsZT1cIm1hcmdpbi1sZWZ0OiAxNnB4XCIgQGNsaWNrPVwiZHJhd2VyID0gdHJ1ZVwiPlxuICAgIG9wZW5cbiAgPC9lbC1idXR0b24+XG4gIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBzdHlsZT1cIm1hcmdpbi1sZWZ0OiAxNnB4XCIgQGNsaWNrPVwiZHJhd2VyMiA9IHRydWVcIj5cbiAgICB3aXRoIGZvb3RlclxuICA8L2VsLWJ1dHRvbj5cblxuICA8ZWwtZHJhd2VyXG4gICAgdi1tb2RlbD1cImRyYXdlclwiXG4gICAgdGl0bGU9XCJJIGFtIHRoZSB0aXRsZVwiXG4gICAgOmRpcmVjdGlvbj1cImRpcmVjdGlvblwiXG4gICAgOmJlZm9yZS1jbG9zZT1cImhhbmRsZUNsb3NlXCJcbiAgPlxuICAgIDxzcGFuPkhpLCB0aGVyZSE8L3NwYW4+XG4gIDwvZWwtZHJhd2VyPlxuICA8ZWwtZHJhd2VyIHYtbW9kZWw9XCJkcmF3ZXIyXCIgOmRpcmVjdGlvbj1cImRpcmVjdGlvblwiPlxuICAgIDx0ZW1wbGF0ZSAjaGVhZGVyPlxuICAgICAgPGg0PnNldCB0aXRsZSBieSBzbG90PC9oND5cbiAgICA8L3RlbXBsYXRlPlxuICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD5cbiAgICAgIDxkaXY+XG4gICAgICAgIDxlbC1yYWRpbyB2LW1vZGVsPVwicmFkaW8xXCIgdmFsdWU9XCJPcHRpb24gMVwiIHNpemU9XCJsYXJnZVwiPlxuICAgICAgICAgIE9wdGlvbiAxXG4gICAgICAgIDwvZWwtcmFkaW8+XG4gICAgICAgIDxlbC1yYWRpbyB2LW1vZGVsPVwicmFkaW8xXCIgdmFsdWU9XCJPcHRpb24gMlwiIHNpemU9XCJsYXJnZVwiPlxuICAgICAgICAgIE9wdGlvbiAyXG4gICAgICAgIDwvZWwtcmFkaW8+XG4gICAgICA8L2Rpdj5cbiAgICA8L3RlbXBsYXRlPlxuICAgIDx0ZW1wbGF0ZSAjZm9vdGVyPlxuICAgICAgPGRpdiBzdHlsZT1cImZsZXg6IGF1dG9cIj5cbiAgICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJjYW5jZWxDbGlja1wiPmNhbmNlbDwvZWwtYnV0dG9uPlxuICAgICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwiY29uZmlybUNsaWNrXCI+Y29uZmlybTwvZWwtYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1kcmF3ZXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgRWxNZXNzYWdlQm94IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbXBvcnQgdHlwZSB7IERyYXdlclByb3BzIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBkcmF3ZXIgPSByZWYoZmFsc2UpXG5jb25zdCBkcmF3ZXIyID0gcmVmKGZhbHNlKVxuY29uc3QgZGlyZWN0aW9uID0gcmVmPERyYXdlclByb3BzWydkaXJlY3Rpb24nXT4oJ3J0bCcpXG5jb25zdCByYWRpbzEgPSByZWYoJ09wdGlvbiAxJylcbmNvbnN0IGhhbmRsZUNsb3NlID0gKGRvbmU6ICgpID0+IHZvaWQpID0+IHtcbiAgRWxNZXNzYWdlQm94LmNvbmZpcm0oJ0FyZSB5b3Ugc3VyZSB5b3Ugd2FudCB0byBjbG9zZSB0aGlzPycpXG4gICAgLnRoZW4oKCkgPT4ge1xuICAgICAgZG9uZSgpXG4gICAgfSlcbiAgICAuY2F0Y2goKCkgPT4ge1xuICAgICAgLy8gY2F0Y2ggZXJyb3JcbiAgICB9KVxufVxuZnVuY3Rpb24gY2FuY2VsQ2xpY2soKSB7XG4gIGRyYXdlcjIudmFsdWUgPSBmYWxzZVxufVxuZnVuY3Rpb24gY29uZmlybUNsaWNrKCkge1xuICBFbE1lc3NhZ2VCb3guY29uZmlybShgQXJlIHlvdSBjb25maXJtIHRvIGNob3NlICR7cmFkaW8xLnZhbHVlfSA/YClcbiAgICAudGhlbigoKSA9PiB7XG4gICAgICBkcmF3ZXIyLnZhbHVlID0gZmFsc2VcbiAgICB9KVxuICAgIC5jYXRjaCgoKSA9PiB7XG4gICAgICAvLyBjYXRjaCBlcnJvclxuICAgIH0pXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/drawer/basic-usage.vue)_

vue

```
<template>
  <el-radio-group v-model="direction">
    <el-radio value="ltr">left to right</el-radio>
    <el-radio value="rtl">right to left</el-radio>
    <el-radio value="ttb">top to bottom</el-radio>
    <el-radio value="btt">bottom to top</el-radio>
  </el-radio-group>

  <el-button type="primary" style="margin-left: 16px" @click="drawer = true">
    open
  </el-button>
  <el-button type="primary" style="margin-left: 16px" @click="drawer2 = true">
    with footer
  </el-button>

  <el-drawer
    v-model="drawer"
    title="I am the title"
    :direction="direction"
    :before-close="handleClose"
  >
    <span>Hi, there!</span>
  </el-drawer>
  <el-drawer v-model="drawer2" :direction="direction">
    <template #header>
      <h4>set title by slot</h4>
    </template>
    <template #default>
      <div>
        <el-radio v-model="radio1" value="Option 1" size="large">
          Option 1
        </el-radio>
        <el-radio v-model="radio1" value="Option 2" size="large">
          Option 2
        </el-radio>
      </div>
    </template>
    <template #footer>
      <div style="flex: auto">
        <el-button @click="cancelClick">cancel</el-button>
        <el-button type="primary" @click="confirmClick">confirm</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

import type { DrawerProps } from 'element-plus'

const drawer = ref(false)
const drawer2 = ref(false)
const direction = ref<DrawerProps['direction']>('rtl')
const radio1 = ref('Option 1')
const handleClose = (done: () => void) => {
  ElMessageBox.confirm('Are you sure you want to close this?')
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}
function cancelClick() {
  drawer2.value = false
}
function confirmClick() {
  ElMessageBox.confirm(`Are you confirm to chose ${radio1.value} ?`)
    .then(() => {
      drawer2.value = false
    })
    .catch(() => {
      // catch error
    })
}
</script>
```

隐藏源代码

## 不添加 Title [​](#不添加-title)

当你不需要标题的时候，你可以将它移除。

通过设置 `with-header` 属性为 **false** 来控制是否显示标题。 如果你的应用需要具备可访问性，请务必设置好 `title`。

open

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwiZHJhd2VyID0gdHJ1ZVwiPiBvcGVuIDwvZWwtYnV0dG9uPlxuXG4gIDxlbC1kcmF3ZXIgdi1tb2RlbD1cImRyYXdlclwiIHRpdGxlPVwiSSBhbSB0aGUgdGl0bGVcIiA6d2l0aC1oZWFkZXI9XCJmYWxzZVwiPlxuICAgIDxzcGFuPkhpIHRoZXJlITwvc3Bhbj5cbiAgPC9lbC1kcmF3ZXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBkcmF3ZXIgPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/drawer/no-title.vue)_

vue

```
<template>
  <el-button type="primary" @click="drawer = true"> open </el-button>

  <el-drawer v-model="drawer" title="I am the title" :with-header="false">
    <span>Hi there!</span>
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const drawer = ref(false)
</script>
```

隐藏源代码

## 自定义内容 [​](#自定义内容)

像 `Dialog` 组件一样，`Drawer` 也可以用来显示多种不同的交互。

Open Drawer with nested table Open Drawer with nested form

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHRleHQgQGNsaWNrPVwidGFibGUgPSB0cnVlXCI+XG4gICAgT3BlbiBEcmF3ZXIgd2l0aCBuZXN0ZWQgdGFibGVcbiAgPC9lbC1idXR0b24+XG4gIDxlbC1idXR0b24gdGV4dCBAY2xpY2s9XCJkaWFsb2cgPSB0cnVlXCI+XG4gICAgT3BlbiBEcmF3ZXIgd2l0aCBuZXN0ZWQgZm9ybVxuICA8L2VsLWJ1dHRvbj5cbiAgPGVsLWRyYXdlclxuICAgIHYtbW9kZWw9XCJ0YWJsZVwiXG4gICAgdGl0bGU9XCJJIGhhdmUgYSBuZXN0ZWQgdGFibGUgaW5zaWRlIVwiXG4gICAgZGlyZWN0aW9uPVwicnRsXCJcbiAgICBzaXplPVwiNTAlXCJcbiAgPlxuICAgIDxlbC10YWJsZSA6ZGF0YT1cImdyaWREYXRhXCI+XG4gICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3BlcnR5PVwiZGF0ZVwiIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTUwXCIgLz5cbiAgICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcGVydHk9XCJuYW1lXCIgbGFiZWw9XCJOYW1lXCIgd2lkdGg9XCIyMDBcIiAvPlxuICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wZXJ0eT1cImFkZHJlc3NcIiBsYWJlbD1cIkFkZHJlc3NcIiAvPlxuICAgIDwvZWwtdGFibGU+XG4gIDwvZWwtZHJhd2VyPlxuXG4gIDxlbC1kcmF3ZXJcbiAgICB2LW1vZGVsPVwiZGlhbG9nXCJcbiAgICB0aXRsZT1cIkkgaGF2ZSBhIG5lc3RlZCBmb3JtIGluc2lkZSFcIlxuICAgIDpiZWZvcmUtY2xvc2U9XCJoYW5kbGVDbG9zZVwiXG4gICAgZGlyZWN0aW9uPVwibHRyXCJcbiAgICBjbGFzcz1cImRlbW8tZHJhd2VyXCJcbiAgPlxuICAgIDxkaXYgY2xhc3M9XCJkZW1vLWRyYXdlcl9fY29udGVudFwiPlxuICAgICAgPGVsLWZvcm0gOm1vZGVsPVwiZm9ybVwiPlxuICAgICAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiTmFtZVwiIDpsYWJlbC13aWR0aD1cImZvcm1MYWJlbFdpZHRoXCI+XG4gICAgICAgICAgPGVsLWlucHV0IHYtbW9kZWw9XCJmb3JtLm5hbWVcIiBhdXRvY29tcGxldGU9XCJvZmZcIiAvPlxuICAgICAgICA8L2VsLWZvcm0taXRlbT5cbiAgICAgICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkFyZWFcIiA6bGFiZWwtd2lkdGg9XCJmb3JtTGFiZWxXaWR0aFwiPlxuICAgICAgICAgIDxlbC1zZWxlY3RcbiAgICAgICAgICAgIHYtbW9kZWw9XCJmb3JtLnJlZ2lvblwiXG4gICAgICAgICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3QgYWN0aXZpdHkgYXJlYVwiXG4gICAgICAgICAgPlxuICAgICAgICAgICAgPGVsLW9wdGlvbiBsYWJlbD1cIkFyZWExXCIgdmFsdWU9XCJzaGFuZ2hhaVwiIC8+XG4gICAgICAgICAgICA8ZWwtb3B0aW9uIGxhYmVsPVwiQXJlYTJcIiB2YWx1ZT1cImJlaWppbmdcIiAvPlxuICAgICAgICAgIDwvZWwtc2VsZWN0PlxuICAgICAgICA8L2VsLWZvcm0taXRlbT5cbiAgICAgIDwvZWwtZm9ybT5cbiAgICAgIDxkaXYgY2xhc3M9XCJkZW1vLWRyYXdlcl9fZm9vdGVyXCI+XG4gICAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwiY2FuY2VsRm9ybVwiPkNhbmNlbDwvZWwtYnV0dG9uPlxuICAgICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgOmxvYWRpbmc9XCJsb2FkaW5nXCIgQGNsaWNrPVwib25DbGlja1wiPlxuICAgICAgICAgIHt7IGxvYWRpbmcgPyAnU3VibWl0dGluZyAuLi4nIDogJ1N1Ym1pdCcgfX1cbiAgICAgICAgPC9lbC1idXR0b24+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj5cbiAgPC9lbC1kcmF3ZXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVhY3RpdmUsIHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsTWVzc2FnZUJveCB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgZm9ybUxhYmVsV2lkdGggPSAnODBweCdcbmxldCB0aW1lclxuXG5jb25zdCB0YWJsZSA9IHJlZihmYWxzZSlcbmNvbnN0IGRpYWxvZyA9IHJlZihmYWxzZSlcbmNvbnN0IGxvYWRpbmcgPSByZWYoZmFsc2UpXG5cbmNvbnN0IGZvcm0gPSByZWFjdGl2ZSh7XG4gIG5hbWU6ICcnLFxuICByZWdpb246ICcnLFxuICBkYXRlMTogJycsXG4gIGRhdGUyOiAnJyxcbiAgZGVsaXZlcnk6IGZhbHNlLFxuICB0eXBlOiBbXSxcbiAgcmVzb3VyY2U6ICcnLFxuICBkZXNjOiAnJyxcbn0pXG5cbmNvbnN0IGdyaWREYXRhID0gW1xuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDInLFxuICAgIG5hbWU6ICdQZXRlciBQYXJrZXInLFxuICAgIGFkZHJlc3M6ICdRdWVlbnMsIE5ldyBZb3JrIENpdHknLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDQnLFxuICAgIG5hbWU6ICdQZXRlciBQYXJrZXInLFxuICAgIGFkZHJlc3M6ICdRdWVlbnMsIE5ldyBZb3JrIENpdHknLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgIG5hbWU6ICdQZXRlciBQYXJrZXInLFxuICAgIGFkZHJlc3M6ICdRdWVlbnMsIE5ldyBZb3JrIENpdHknLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDMnLFxuICAgIG5hbWU6ICdQZXRlciBQYXJrZXInLFxuICAgIGFkZHJlc3M6ICdRdWVlbnMsIE5ldyBZb3JrIENpdHknLFxuICB9LFxuXVxuXG5jb25zdCBvbkNsaWNrID0gKCkgPT4ge1xuICBsb2FkaW5nLnZhbHVlID0gdHJ1ZVxuICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICBsb2FkaW5nLnZhbHVlID0gZmFsc2VcbiAgICBkaWFsb2cudmFsdWUgPSBmYWxzZVxuICB9LCA0MDApXG59XG5cbmNvbnN0IGhhbmRsZUNsb3NlID0gKGRvbmUpID0+IHtcbiAgaWYgKGxvYWRpbmcudmFsdWUpIHtcbiAgICByZXR1cm5cbiAgfVxuICBFbE1lc3NhZ2VCb3guY29uZmlybSgnRG8geW91IHdhbnQgdG8gc3VibWl0PycpXG4gICAgLnRoZW4oKCkgPT4ge1xuICAgICAgbG9hZGluZy52YWx1ZSA9IHRydWVcbiAgICAgIHRpbWVyID0gc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICAgIGRvbmUoKVxuICAgICAgICAvLyDliqjnlLvlhbPpl63pnIDopoHkuIDlrprnmoTml7bpl7RcbiAgICAgICAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICAgICAgbG9hZGluZy52YWx1ZSA9IGZhbHNlXG4gICAgICAgIH0sIDQwMClcbiAgICAgIH0sIDIwMDApXG4gICAgfSlcbiAgICAuY2F0Y2goKCkgPT4ge1xuICAgICAgLy8gY2F0Y2ggZXJyb3JcbiAgICB9KVxufVxuXG5jb25zdCBjYW5jZWxGb3JtID0gKCkgPT4ge1xuICBsb2FkaW5nLnZhbHVlID0gZmFsc2VcbiAgZGlhbG9nLnZhbHVlID0gZmFsc2VcbiAgY2xlYXJUaW1lb3V0KHRpbWVyKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/drawer/customization-content.vue)_

vue

```
<template>
  <el-button text @click="table = true">
    Open Drawer with nested table
  </el-button>
  <el-button text @click="dialog = true">
    Open Drawer with nested form
  </el-button>
  <el-drawer
    v-model="table"
    title="I have a nested table inside!"
    direction="rtl"
    size="50%"
  >
    <el-table :data="gridData">
      <el-table-column property="date" label="Date" width="150" />
      <el-table-column property="name" label="Name" width="200" />
      <el-table-column property="address" label="Address" />
    </el-table>
  </el-drawer>

  <el-drawer
    v-model="dialog"
    title="I have a nested form inside!"
    :before-close="handleClose"
    direction="ltr"
    class="demo-drawer"
  >
    <div class="demo-drawer__content">
      <el-form :model="form">
        <el-form-item label="Name" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Area" :label-width="formLabelWidth">
          <el-select
            v-model="form.region"
            placeholder="Please select activity area"
          >
            <el-option label="Area1" value="shanghai" />
            <el-option label="Area2" value="beijing" />
          </el-select>
        </el-form-item>
      </el-form>
      <div class="demo-drawer__footer">
        <el-button @click="cancelForm">Cancel</el-button>
        <el-button type="primary" :loading="loading" @click="onClick">
          {{ loading ? 'Submitting ...' : 'Submit' }}
        </el-button>
      </div>
    </div>
  </el-drawer>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { ElMessageBox } from 'element-plus'

const formLabelWidth = '80px'
let timer

const table = ref(false)
const dialog = ref(false)
const loading = ref(false)

const form = reactive({
  name: '',
  region: '',
  date1: '',
  date2: '',
  delivery: false,
  type: [],
  resource: '',
  desc: '',
})

const gridData = [
  {
    date: '2016-05-02',
    name: 'Peter Parker',
    address: 'Queens, New York City',
  },
  {
    date: '2016-05-04',
    name: 'Peter Parker',
    address: 'Queens, New York City',
  },
  {
    date: '2016-05-01',
    name: 'Peter Parker',
    address: 'Queens, New York City',
  },
  {
    date: '2016-05-03',
    name: 'Peter Parker',
    address: 'Queens, New York City',
  },
]

const onClick = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    dialog.value = false
  }, 400)
}

const handleClose = (done) => {
  if (loading.value) {
    return
  }
  ElMessageBox.confirm('Do you want to submit?')
    .then(() => {
      loading.value = true
      timer = setTimeout(() => {
        done()
        // 动画关闭需要一定的时间
        setTimeout(() => {
          loading.value = false
        }, 400)
      }, 2000)
    })
    .catch(() => {
      // catch error
    })
}

const cancelForm = () => {
  loading.value = false
  dialog.value = false
  clearTimeout(timer)
}
</script>
```

隐藏源代码

## 自定义头部 [​](#自定义头部)

`header` 可用于自定义显示标题的区域。 为了保持可用性，除了使用此插槽外，使用 `title` 属性，或使用 `titleId` 插槽属性来指定哪些元素应该读取为抽屉标题。

Open Drawer with customized header

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIEBjbGljaz1cInZpc2libGUgPSB0cnVlXCI+XG4gICAgT3BlbiBEcmF3ZXIgd2l0aCBjdXN0b21pemVkIGhlYWRlclxuICA8L2VsLWJ1dHRvbj5cbiAgPGVsLWRyYXdlciB2LW1vZGVsPVwidmlzaWJsZVwiIDpzaG93LWNsb3NlPVwiZmFsc2VcIj5cbiAgICA8dGVtcGxhdGUgI2hlYWRlcj1cInsgY2xvc2UsIHRpdGxlSWQsIHRpdGxlQ2xhc3MgfVwiPlxuICAgICAgPGg0IDppZD1cInRpdGxlSWRcIiA6Y2xhc3M9XCJ0aXRsZUNsYXNzXCI+VGhpcyBpcyBhIGN1c3RvbSBoZWFkZXIhPC9oND5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cImRhbmdlclwiIEBjbGljaz1cImNsb3NlXCI+XG4gICAgICAgIDxlbC1pY29uIGNsYXNzPVwiZWwtaWNvbi0tbGVmdFwiPjxDaXJjbGVDbG9zZUZpbGxlZCAvPjwvZWwtaWNvbj5cbiAgICAgICAgQ2xvc2VcbiAgICAgIDwvZWwtYnV0dG9uPlxuICAgIDwvdGVtcGxhdGU+XG4gICAgVGhpcyBpcyBkcmF3ZXIgY29udGVudC5cbiAgPC9lbC1kcmF3ZXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgQ2lyY2xlQ2xvc2VGaWxsZWQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgdmlzaWJsZSA9IHJlZihmYWxzZSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/drawer/customization-header.vue)_

vue

```
<template>
  <el-button @click="visible = true">
    Open Drawer with customized header
  </el-button>
  <el-drawer v-model="visible" :show-close="false">
    <template #header="{ close, titleId, titleClass }">
      <h4 :id="titleId" :class="titleClass">This is a custom header!</h4>
      <el-button type="danger" @click="close">
        <el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>
        Close
      </el-button>
    </template>
    This is drawer content.
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CircleCloseFilled } from '@element-plus/icons-vue'

const visible = ref(false)
</script>
```

隐藏源代码

## 可调整抽屉2.11.0 [​](#可调整抽屉)

尝试拖动边缘部分。

设置`resizable`属性为`true`以做到拖拽

toprightbottomleft

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cImRpcmVjdGlvblwiIEBjaGFuZ2U9XCJkcmF3ZXIgPSB0cnVlXCI+XG4gICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cInR0YlwiPnRvcDwvZWwtcmFkaW8tYnV0dG9uPlxuICAgIDxlbC1yYWRpby1idXR0b24gdmFsdWU9XCJydGxcIj5yaWdodDwvZWwtcmFkaW8tYnV0dG9uPlxuICAgIDxlbC1yYWRpby1idXR0b24gdmFsdWU9XCJidHRcIj5ib3R0b208L2VsLXJhZGlvLWJ1dHRvbj5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwibHRyXCI+bGVmdDwvZWwtcmFkaW8tYnV0dG9uPlxuICA8L2VsLXJhZGlvLWdyb3VwPlxuXG4gIDxlbC1kcmF3ZXIgdi1tb2RlbD1cImRyYXdlclwiIDpkaXJlY3Rpb249XCJkaXJlY3Rpb25cIiByZXNpemFibGU+XG4gICAgVGhpcyBpcyBkcmF3ZXIgY29udGVudC5cbiAgPC9lbC1kcmF3ZXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IERyYXdlclByb3BzIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBkaXJlY3Rpb24gPSByZWY8RHJhd2VyUHJvcHNbJ2RpcmVjdGlvbiddPigpXG5jb25zdCBkcmF3ZXIgPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/drawer/resizable.vue)_

vue

```
<template>
  <el-radio-group v-model="direction" @change="drawer = true">
    <el-radio-button value="ttb">top</el-radio-button>
    <el-radio-button value="rtl">right</el-radio-button>
    <el-radio-button value="btt">bottom</el-radio-button>
    <el-radio-button value="ltr">left</el-radio-button>
  </el-radio-group>

  <el-drawer v-model="drawer" :direction="direction" resizable>
    This is drawer content.
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { DrawerProps } from 'element-plus'

const direction = ref<DrawerProps['direction']>()
const drawer = ref(false)
</script>
```

隐藏源代码

## 嵌套抽屉 [​](#嵌套抽屉)

你可以像 `Dialog` 一样拥有多层嵌套的 `Drawer`

如果你需要在不同图层中多个抽屉，你必须设置 `append-to-body` 属性到 **true**

open

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwiZHJhd2VyID0gdHJ1ZVwiPiBvcGVuIDwvZWwtYnV0dG9uPlxuXG4gIDxlbC1kcmF3ZXIgdi1tb2RlbD1cImRyYXdlclwiIHRpdGxlPVwiSSdtIG91dGVyIERyYXdlclwiIHNpemU9XCI1MCVcIj5cbiAgICA8ZGl2PlxuICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJpbm5lckRyYXdlciA9IHRydWVcIj5DbGljayBtZSE8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1kcmF3ZXJcbiAgICAgICAgdi1tb2RlbD1cImlubmVyRHJhd2VyXCJcbiAgICAgICAgdGl0bGU9XCJJJ20gaW5uZXIgRHJhd2VyXCJcbiAgICAgICAgOmFwcGVuZC10by1ib2R5PVwidHJ1ZVwiXG4gICAgICAgIDpiZWZvcmUtY2xvc2U9XCJoYW5kbGVDbG9zZVwiXG4gICAgICA+XG4gICAgICAgIDxwPl8oOtC344Kd4oigKV88L3A+XG4gICAgICA8L2VsLWRyYXdlcj5cbiAgICA8L2Rpdj5cbiAgPC9lbC1kcmF3ZXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgRWxNZXNzYWdlQm94IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBkcmF3ZXIgPSByZWYoZmFsc2UpXG5jb25zdCBpbm5lckRyYXdlciA9IHJlZihmYWxzZSlcblxuY29uc3QgaGFuZGxlQ2xvc2UgPSAoZG9uZTogKCkgPT4gdm9pZCkgPT4ge1xuICBFbE1lc3NhZ2VCb3guY29uZmlybSgnWW91IHN0aWxsIGhhdmUgdW5zYXZlZCBkYXRhLCBwcm9jZWVkPycpXG4gICAgLnRoZW4oKCkgPT4ge1xuICAgICAgZG9uZSgpXG4gICAgfSlcbiAgICAuY2F0Y2goKCkgPT4ge1xuICAgICAgLy8gY2F0Y2ggZXJyb3JcbiAgICB9KVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/drawer/nested-drawer.vue)_

vue

```
<template>
  <el-button type="primary" @click="drawer = true"> open </el-button>

  <el-drawer v-model="drawer" title="I'm outer Drawer" size="50%">
    <div>
      <el-button @click="innerDrawer = true">Click me!</el-button>
      <el-drawer
        v-model="innerDrawer"
        title="I'm inner Drawer"
        :append-to-body="true"
        :before-close="handleClose"
      >
        <p>_(:зゝ∠)_</p>
      </el-drawer>
    </div>
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

const drawer = ref(false)
const innerDrawer = ref(false)

const handleClose = (done: () => void) => {
  ElMessageBox.confirm('You still have unsaved data, proceed?')
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}
</script>
```

隐藏源代码

## 模态框 [​](#模态框)

将 `modal` 设置为 `false` 将隐藏抽屉的模态层（遮罩层）。

从版本 2.11.7 起，新增了 `modal-penetrable` 属性，该属性可设置为“可穿透”。

Open the modal Drawer

Cancel Confirm

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cImRyYXdlclZpc2libGUgPSB0cnVlXCI+XG4gICAgT3BlbiB0aGUgbW9kYWwgRHJhd2VyXG4gIDwvZWwtYnV0dG9uPlxuXG4gIDxlbC1kcmF3ZXIgdi1tb2RlbD1cImRyYXdlclZpc2libGVcIiA6bW9kYWw9XCJmYWxzZVwiIG1vZGFsLXBlbmV0cmFibGU+XG4gICAgPHNwYW4+SXQncyBhIG1vZGFsIERyYXdlcjwvc3Bhbj5cbiAgICA8dGVtcGxhdGUgI2Zvb3Rlcj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkcmF3ZXItZm9vdGVyXCI+XG4gICAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwiZHJhd2VyVmlzaWJsZSA9IGZhbHNlXCI+Q2FuY2VsPC9lbC1idXR0b24+XG4gICAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBAY2xpY2s9XCJkcmF3ZXJWaXNpYmxlID0gZmFsc2VcIj5cbiAgICAgICAgICBDb25maXJtXG4gICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1kcmF3ZXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBkcmF3ZXJWaXNpYmxlID0gcmVmKGZhbHNlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/drawer/modal.vue)_

vue

```
<template>
  <el-button plain @click="drawerVisible = true">
    Open the modal Drawer
  </el-button>

  <el-drawer v-model="drawerVisible" :modal="false" modal-penetrable>
    <span>It's a modal Drawer</span>
    <template #footer>
      <div class="drawer-footer">
        <el-button @click="drawerVisible = false">Cancel</el-button>
        <el-button type="primary" @click="drawerVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const drawerVisible = ref(false)
</script>
```

隐藏源代码

TIP

Drawer 的内容是懒渲染的，即在第一次被打开之前，传入的默认 slot 不会被渲染到 DOM 上。 因此，如果需要执行 DOM 操作，或通过 `ref` 获取相应组件，请在 `open` 事件回调中进行。

TIP

Drawer 提供了一个名为 `destroy-on-close` 的 API，这是一个标志变量，用于指示在 Drawer 关闭后是否销毁其中的子内容。 当你需要每次打开抽屉都要调用 `mounted` 生命周期时，可以使用此 API。

## API [​](#api)

### 属性 [​](#属性)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 是否显示 Drawer | `boolean` | false |
| append-to-body | Drawer 自身是否插入至 body 元素上。嵌套的 Drawer 必须指定该属性并赋值为 **true** | `boolean` | false |
| append-to 2.8.0 | 挂载到哪个 DOM 元素 将覆盖 `append-to-body` | `CSSSelector` / `HTMLElement` | body |
| lock-scroll | 是否在 Drawer 出现时将 body 滚动锁定 | `boolean` | true |
| before-close | 关闭前的回调，会暂停 Drawer 的关闭 | `Function` | — |
| close-on-click-modal | 是否可以通过点击 modal 关闭 Drawer | `boolean` | true |
| close-on-press-escape | 是否可以通过按下 ESC 关闭 Drawer | `boolean` | true |
| open-delay | Drawer 打开的延时时间，单位毫秒 | `number` | 0 |
| close-delay | Drawer 关闭的延时时间，单位毫秒 | `number` | 0 |
| destroy-on-close | 控制是否在关闭 Drawer 之后将子元素全部销毁 | `boolean` | false |
| modal | 是否需要遮罩层 | `boolean` | true |
| modal-penetrable 2.11.7 | 是否允许穿透遮罩层。 modal 属性必须为 `false`。 | `boolean` | false |
| direction | Drawer 打开的方向 | `enum` | rtl |
| resizable 2.11.0 | 为抽屉启用可调整大小的功能 | `boolean` | false |
| show-close | 是否显示关闭按钮 | `boolean` | true |
| size | Drawer 窗体的大小, 当使用 `number` 类型时, 以像素为单位, 当使用 `string` 类型时, 请传入 'x%', 否则便会以 `number` 类型解释 | `number` / `string` | 30% |
| title | Drawer 的标题，也可通过具名 slot （见下表）传入 | `string` | — |
| with-header | 控制是否显示 header 栏, 默认为 true, 当此项为 false 时, title attribute 和 title slot 均不生效 | `boolean` | true |
| modal-class | 遮罩层的自定义类名 | `string` | — |
| header-class 2.9.3 | header 部分的自定义 class 名 | `string` | — |
| body-class 2.9.3 | body 部分的自定义 class 名 | `string` | — |
| footer-class 2.9.3 | footer 部分的自定义 class 名 | `string` | — |
| z-index | 设置 z-index | `number` | — |
| header-aria-level a11y | header 的 `aria-level` 属性 | `string` | 2 |
| custom-class deprecated | Drawer 的自定义类名 | `string` | — |

WARNING

`custom-class` 已被 **弃用**，**将会于** 2.3.0 移除, 请使用 `class`。

### 事件 [​](#事件)

| 事件名称 | 说明 | 类型 |
| --- | --- | --- |
| open | Drawer 打开的回调 | `Function` |
| opened | Drawer 打开动画结束时的回调 | `Function` |
| close | Drawer 关闭的回调 | `Function` |
| closed | Drawer 关闭动画结束时的回调 | `Function` |
| open-auto-focus | 输入焦点聚焦在 Drawer 内容时的回调 | `Function` |
| close-auto-focus | 输入焦点从 Drawer 内容失焦时的回调 | `Function` |
| resize-start 2.11.8 | 当开始调整大小时触发（当启用 `resizable` 时） | `Function` |
| resize 2.11.8 | 调整大小时触发（启用 `resizable` 时） | `Function` |
| resize-end 2.11.8 | 当调整大小结束时触发（当启用 `resizable` 时） | `Function` |

### 插槽 [​](#插槽)

| 名称 | 说明 |
| --- | --- |
| default | Drawer 的内容 |
| header | Drawer 标题的内容；会替换标题部分，但不会移除关闭按钮。 |
| footer | Drawer 页脚部分 |
| title deprecated | 与 header 作用相同 请使用 header |

WARNING

`title` 已被**弃用**，并将在 3.0.0 版本中**移除**，请使用 `header` 代替。

### 暴露 [​](#暴露)

| 名称 | 详情 |
| --- | --- |
| handleClose | 用于关闭 Drawer, 该方法会调用传入的 `before-close` 方法 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/drawer) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/drawer.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/drawer.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/138789658?v=4&size=64)](https://github.com/StudiousGao)[![](https://avatars.githubusercontent.com/u/69580637?v=4&size=64)](https://github.com/jevin98)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/80906525?v=4&size=64)](https://github.com/drylint)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/43806319?v=4&size=64)](https://github.com/qianjiachun)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/23442840?v=4&size=64)](https://github.com/liunnn1994)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/87807886?v=4&size=64)](https://github.com/briver0825)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)

[Dialog 对话框](https://element-plus.org/zh-CN/component/dialog)

[Loading 加载](https://element-plus.org/zh-CN/component/loading)


