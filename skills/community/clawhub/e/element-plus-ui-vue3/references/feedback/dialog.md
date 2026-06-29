---
name: "dialog"
description: "Dialog 对话框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Dialog 对话框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/dialog.html"
---

---

# Dialog 对话框 [​](#dialog-对话框)

更新日志待解决

28

在保留当前页面状态的情况下，告知用户并承载相关操作。

## 基础用法 [​](#基础用法)

Dialog 弹出一个对话框，适合需要定制性更大的场景。

需要设置 `model-value / v-model` 属性，它接收 `Boolean`，当为 `true` 时显示 Dialog。 Dialog 分为两个部分：`body` 和 `footer`，`footer` 需要具名为 `footer` 的 `slot`。 `title` 属性用于定义标题，它是可选的，默认值为空。 最后，本例还展示了 `before-close` 的用法。

Click to open the Dialog

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cImRpYWxvZ1Zpc2libGUgPSB0cnVlXCI+XG4gICAgQ2xpY2sgdG8gb3BlbiB0aGUgRGlhbG9nXG4gIDwvZWwtYnV0dG9uPlxuXG4gIDxlbC1kaWFsb2dcbiAgICB2LW1vZGVsPVwiZGlhbG9nVmlzaWJsZVwiXG4gICAgdGl0bGU9XCJUaXBzXCJcbiAgICB3aWR0aD1cIjUwMFwiXG4gICAgOmJlZm9yZS1jbG9zZT1cImhhbmRsZUNsb3NlXCJcbiAgPlxuICAgIDxzcGFuPlRoaXMgaXMgYSBtZXNzYWdlPC9zcGFuPlxuICAgIDx0ZW1wbGF0ZSAjZm9vdGVyPlxuICAgICAgPGRpdiBjbGFzcz1cImRpYWxvZy1mb290ZXJcIj5cbiAgICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJkaWFsb2dWaXNpYmxlID0gZmFsc2VcIj5DYW5jZWw8L2VsLWJ1dHRvbj5cbiAgICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIEBjbGljaz1cImRpYWxvZ1Zpc2libGUgPSBmYWxzZVwiPlxuICAgICAgICAgIENvbmZpcm1cbiAgICAgICAgPC9lbC1idXR0b24+XG4gICAgICA8L2Rpdj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLWRpYWxvZz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBFbE1lc3NhZ2VCb3ggfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGRpYWxvZ1Zpc2libGUgPSByZWYoZmFsc2UpXG5cbmNvbnN0IGhhbmRsZUNsb3NlID0gKGRvbmU6ICgpID0+IHZvaWQpID0+IHtcbiAgRWxNZXNzYWdlQm94LmNvbmZpcm0oJ0FyZSB5b3Ugc3VyZSB0byBjbG9zZSB0aGlzIGRpYWxvZz8nKVxuICAgIC50aGVuKCgpID0+IHtcbiAgICAgIGRvbmUoKVxuICAgIH0pXG4gICAgLmNhdGNoKCgpID0+IHtcbiAgICAgIC8vIGNhdGNoIGVycm9yXG4gICAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/basic-usage.vue)_

vue

```
<template>
  <el-button plain @click="dialogVisible = true">
    Click to open the Dialog
  </el-button>

  <el-dialog
    v-model="dialogVisible"
    title="Tips"
    width="500"
    :before-close="handleClose"
  >
    <span>This is a message</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

const dialogVisible = ref(false)

const handleClose = (done: () => void) => {
  ElMessageBox.confirm('Are you sure to close this dialog?')
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

TIP

`before-close` 只会在用户点击关闭按钮或者对话框的遮罩区域时被调用。 如果你在 `footer` 具名 slot 里添加了用于关闭 Dialog 的按钮，那么可以在按钮的点击回调函数里加入 `before-close` 的相关逻辑。

## 自定义内容 [​](#自定义内容)

对话框的内容可以是任何东西，甚至是一个表格或表单。 此示例显示如何在 Dialog 中使用 Element Plus 的表格和表单。

Open a Table nested Dialog Open a Form nested Dialog

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJkaWFsb2dUYWJsZVZpc2libGUgPSB0cnVlXCI+XG4gICAgICBPcGVuIGEgVGFibGUgbmVzdGVkIERpYWxvZ1xuICAgIDwvZWwtYnV0dG9uPlxuXG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgcGxhaW4gQGNsaWNrPVwiZGlhbG9nRm9ybVZpc2libGUgPSB0cnVlXCI+XG4gICAgICBPcGVuIGEgRm9ybSBuZXN0ZWQgRGlhbG9nXG4gICAgPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuXG4gIDxlbC1kaWFsb2cgdi1tb2RlbD1cImRpYWxvZ1RhYmxlVmlzaWJsZVwiIHRpdGxlPVwiU2hpcHBpbmcgYWRkcmVzc1wiIHdpZHRoPVwiODAwXCI+XG4gICAgPGVsLXRhYmxlIDpkYXRhPVwiZ3JpZERhdGFcIj5cbiAgICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcGVydHk9XCJkYXRlXCIgbGFiZWw9XCJEYXRlXCIgd2lkdGg9XCIxNTBcIiAvPlxuICAgICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wZXJ0eT1cIm5hbWVcIiBsYWJlbD1cIk5hbWVcIiB3aWR0aD1cIjIwMFwiIC8+XG4gICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3BlcnR5PVwiYWRkcmVzc1wiIGxhYmVsPVwiQWRkcmVzc1wiIC8+XG4gICAgPC9lbC10YWJsZT5cbiAgPC9lbC1kaWFsb2c+XG5cbiAgPGVsLWRpYWxvZyB2LW1vZGVsPVwiZGlhbG9nRm9ybVZpc2libGVcIiB0aXRsZT1cIlNoaXBwaW5nIGFkZHJlc3NcIiB3aWR0aD1cIjUwMFwiPlxuICAgIDxlbC1mb3JtIDptb2RlbD1cImZvcm1cIj5cbiAgICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJQcm9tb3Rpb24gbmFtZVwiIDpsYWJlbC13aWR0aD1cImZvcm1MYWJlbFdpZHRoXCI+XG4gICAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwiZm9ybS5uYW1lXCIgYXV0b2NvbXBsZXRlPVwib2ZmXCIgLz5cbiAgICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIlpvbmVzXCIgOmxhYmVsLXdpZHRoPVwiZm9ybUxhYmVsV2lkdGhcIj5cbiAgICAgICAgPGVsLXNlbGVjdCB2LW1vZGVsPVwiZm9ybS5yZWdpb25cIiBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3QgYSB6b25lXCI+XG4gICAgICAgICAgPGVsLW9wdGlvbiBsYWJlbD1cIlpvbmUgTm8uMVwiIHZhbHVlPVwic2hhbmdoYWlcIiAvPlxuICAgICAgICAgIDxlbC1vcHRpb24gbGFiZWw9XCJab25lIE5vLjJcIiB2YWx1ZT1cImJlaWppbmdcIiAvPlxuICAgICAgICA8L2VsLXNlbGVjdD5cbiAgICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDwvZWwtZm9ybT5cbiAgICA8dGVtcGxhdGUgI2Zvb3Rlcj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkaWFsb2ctZm9vdGVyXCI+XG4gICAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwiZGlhbG9nRm9ybVZpc2libGUgPSBmYWxzZVwiPkNhbmNlbDwvZWwtYnV0dG9uPlxuICAgICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwiZGlhbG9nRm9ybVZpc2libGUgPSBmYWxzZVwiPlxuICAgICAgICAgIENvbmZpcm1cbiAgICAgICAgPC9lbC1idXR0b24+XG4gICAgICA8L2Rpdj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLWRpYWxvZz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWFjdGl2ZSwgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBkaWFsb2dUYWJsZVZpc2libGUgPSByZWYoZmFsc2UpXG5jb25zdCBkaWFsb2dGb3JtVmlzaWJsZSA9IHJlZihmYWxzZSlcbmNvbnN0IGZvcm1MYWJlbFdpZHRoID0gJzE0MHB4J1xuXG5jb25zdCBmb3JtID0gcmVhY3RpdmUoe1xuICBuYW1lOiAnJyxcbiAgcmVnaW9uOiAnJyxcbiAgZGF0ZTE6ICcnLFxuICBkYXRlMjogJycsXG4gIGRlbGl2ZXJ5OiBmYWxzZSxcbiAgdHlwZTogW10sXG4gIHJlc291cmNlOiAnJyxcbiAgZGVzYzogJycsXG59KVxuXG5jb25zdCBncmlkRGF0YSA9IFtcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAyJyxcbiAgICBuYW1lOiAnSm9obiBTbWl0aCcsXG4gICAgYWRkcmVzczogJ05vLjE1MTgsICBKaW5zaGFqaWFuZyBSb2FkLCBQdXR1byBEaXN0cmljdCcsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wNCcsXG4gICAgbmFtZTogJ0pvaG4gU21pdGgnLFxuICAgIGFkZHJlc3M6ICdOby4xNTE4LCAgSmluc2hhamlhbmcgUm9hZCwgUHV0dW8gRGlzdHJpY3QnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDEnLFxuICAgIG5hbWU6ICdKb2huIFNtaXRoJyxcbiAgICBhZGRyZXNzOiAnTm8uMTUxOCwgIEppbnNoYWppYW5nIFJvYWQsIFB1dHVvIERpc3RyaWN0JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAzJyxcbiAgICBuYW1lOiAnSm9obiBTbWl0aCcsXG4gICAgYWRkcmVzczogJ05vLjE1MTgsICBKaW5zaGFqaWFuZyBSb2FkLCBQdXR1byBEaXN0cmljdCcsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/customization-content.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" plain @click="dialogTableVisible = true">
      Open a Table nested Dialog
    </el-button>

    <el-button class="!ml-0" plain @click="dialogFormVisible = true">
      Open a Form nested Dialog
    </el-button>
  </div>

  <el-dialog v-model="dialogTableVisible" title="Shipping address" width="800">
    <el-table :data="gridData">
      <el-table-column property="date" label="Date" width="150" />
      <el-table-column property="name" label="Name" width="200" />
      <el-table-column property="address" label="Address" />
    </el-table>
  </el-dialog>

  <el-dialog v-model="dialogFormVisible" title="Shipping address" width="500">
    <el-form :model="form">
      <el-form-item label="Promotion name" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Zones" :label-width="formLabelWidth">
        <el-select v-model="form.region" placeholder="Please select a zone">
          <el-option label="Zone No.1" value="shanghai" />
          <el-option label="Zone No.2" value="beijing" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

const dialogTableVisible = ref(false)
const dialogFormVisible = ref(false)
const formLabelWidth = '140px'

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
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-04',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-01',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-03',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
]
</script>
```

隐藏源代码

## 自定义头部 [​](#自定义头部)

`header` 可用于自定义显示标题的区域。 为了保持可用性，除了使用此插槽外，使用 `title` 属性，或使用 `titleId` 插槽属性来指定哪些元素应该读取为对话框标题。

Open Dialog with customized header

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cInZpc2libGUgPSB0cnVlXCI+XG4gICAgT3BlbiBEaWFsb2cgd2l0aCBjdXN0b21pemVkIGhlYWRlclxuICA8L2VsLWJ1dHRvbj5cblxuICA8ZWwtZGlhbG9nIHYtbW9kZWw9XCJ2aXNpYmxlXCIgOnNob3ctY2xvc2U9XCJmYWxzZVwiIHdpZHRoPVwiNTAwXCI+XG4gICAgPHRlbXBsYXRlICNoZWFkZXI9XCJ7IGNsb3NlLCB0aXRsZUlkLCB0aXRsZUNsYXNzIH1cIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJteS1oZWFkZXJcIj5cbiAgICAgICAgPGg0IDppZD1cInRpdGxlSWRcIiA6Y2xhc3M9XCJ0aXRsZUNsYXNzXCI+VGhpcyBpcyBhIGN1c3RvbSBoZWFkZXIhPC9oND5cbiAgICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwiZGFuZ2VyXCIgQGNsaWNrPVwiY2xvc2VcIj5cbiAgICAgICAgICA8ZWwtaWNvbiBjbGFzcz1cImVsLWljb24tLWxlZnRcIj48Q2lyY2xlQ2xvc2VGaWxsZWQgLz48L2VsLWljb24+XG4gICAgICAgICAgQ2xvc2VcbiAgICAgICAgPC9lbC1idXR0b24+XG4gICAgICA8L2Rpdj5cbiAgICA8L3RlbXBsYXRlPlxuICAgIFRoaXMgaXMgZGlhbG9nIGNvbnRlbnQuXG4gIDwvZWwtZGlhbG9nPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IENpcmNsZUNsb3NlRmlsbGVkIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IHZpc2libGUgPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5teS1oZWFkZXIge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogcm93O1xuICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47XG4gIGdhcDogMTZweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/customization-header.vue)_

vue

```
<template>
  <el-button plain @click="visible = true">
    Open Dialog with customized header
  </el-button>

  <el-dialog v-model="visible" :show-close="false" width="500">
    <template #header="{ close, titleId, titleClass }">
      <div class="my-header">
        <h4 :id="titleId" :class="titleClass">This is a custom header!</h4>
        <el-button type="danger" @click="close">
          <el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>
          Close
        </el-button>
      </div>
    </template>
    This is dialog content.
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CircleCloseFilled } from '@element-plus/icons-vue'

const visible = ref(false)
</script>

<style scoped>
.my-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 16px;
}
</style>
```

隐藏源代码

## 嵌套的对话框 [​](#嵌套的对话框)

如果需要在一个 Dialog 内部嵌套另一个 Dialog，需要使用 `append-to-body` 属性。

通常我们不建议使用嵌套对话框。 如果你需要在页面上呈现多个对话框，你可以简单地打平它们，以便它们彼此之间是平级关系。 如果必须要在一个对话框内展示另一个对话框，可以将内部嵌套的对话框属性 `append-to-body` 设置为 true，嵌套的对话框将附加到 body 而不是其父节点，这样两个对话框都可以被正确地渲染。

Open the outer Dialog

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm91dGVyVmlzaWJsZSA9IHRydWVcIj5cbiAgICBPcGVuIHRoZSBvdXRlciBEaWFsb2dcbiAgPC9lbC1idXR0b24+XG5cbiAgPGVsLWRpYWxvZyB2LW1vZGVsPVwib3V0ZXJWaXNpYmxlXCIgdGl0bGU9XCJPdXRlciBEaWFsb2dcIiB3aWR0aD1cIjgwMFwiPlxuICAgIDxzcGFuPlRoaXMgaXMgdGhlIG91dGVyIERpYWxvZzwvc3Bhbj5cbiAgICA8ZWwtZGlhbG9nXG4gICAgICB2LW1vZGVsPVwiaW5uZXJWaXNpYmxlXCJcbiAgICAgIHdpZHRoPVwiNTAwXCJcbiAgICAgIHRpdGxlPVwiSW5uZXIgRGlhbG9nXCJcbiAgICAgIGFwcGVuZC10by1ib2R5XG4gICAgPlxuICAgICAgPHNwYW4+VGhpcyBpcyB0aGUgaW5uZXIgRGlhbG9nPC9zcGFuPlxuICAgIDwvZWwtZGlhbG9nPlxuICAgIDx0ZW1wbGF0ZSAjZm9vdGVyPlxuICAgICAgPGRpdiBjbGFzcz1cImRpYWxvZy1mb290ZXJcIj5cbiAgICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJvdXRlclZpc2libGUgPSBmYWxzZVwiPkNhbmNlbDwvZWwtYnV0dG9uPlxuICAgICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwiaW5uZXJWaXNpYmxlID0gdHJ1ZVwiPlxuICAgICAgICAgIE9wZW4gdGhlIGlubmVyIERpYWxvZ1xuICAgICAgICA8L2VsLWJ1dHRvbj5cbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtZGlhbG9nPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3Qgb3V0ZXJWaXNpYmxlID0gcmVmKGZhbHNlKVxuY29uc3QgaW5uZXJWaXNpYmxlID0gcmVmKGZhbHNlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/nested-dialog.vue)_

vue

```
<template>
  <el-button plain @click="outerVisible = true">
    Open the outer Dialog
  </el-button>

  <el-dialog v-model="outerVisible" title="Outer Dialog" width="800">
    <span>This is the outer Dialog</span>
    <el-dialog
      v-model="innerVisible"
      width="500"
      title="Inner Dialog"
      append-to-body
    >
      <span>This is the inner Dialog</span>
    </el-dialog>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="outerVisible = false">Cancel</el-button>
        <el-button type="primary" @click="innerVisible = true">
          Open the inner Dialog
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const outerVisible = ref(false)
const innerVisible = ref(false)
</script>
```

隐藏源代码

## 内容居中 [​](#内容居中)

对话框的内容可以居中。

将`center`设置为`true`即可使标题和底部居中。 `center`仅影响标题和底部区域。 Dialog 的内容是任意的，在一些情况下，内容并不适合居中布局。 如果需要内容也水平居中，请自行为其添加 CSS 样式。

Click to open the Dialog

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cImNlbnRlckRpYWxvZ1Zpc2libGUgPSB0cnVlXCI+XG4gICAgQ2xpY2sgdG8gb3BlbiB0aGUgRGlhbG9nXG4gIDwvZWwtYnV0dG9uPlxuXG4gIDxlbC1kaWFsb2cgdi1tb2RlbD1cImNlbnRlckRpYWxvZ1Zpc2libGVcIiB0aXRsZT1cIldhcm5pbmdcIiB3aWR0aD1cIjUwMFwiIGNlbnRlcj5cbiAgICA8c3Bhbj5cbiAgICAgIEl0IHNob3VsZCBiZSBub3RlZCB0aGF0IHRoZSBjb250ZW50IHdpbGwgbm90IGJlIGFsaWduZWQgaW4gY2VudGVyIGJ5XG4gICAgICBkZWZhdWx0XG4gICAgPC9zcGFuPlxuICAgIDx0ZW1wbGF0ZSAjZm9vdGVyPlxuICAgICAgPGRpdiBjbGFzcz1cImRpYWxvZy1mb290ZXJcIj5cbiAgICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJjZW50ZXJEaWFsb2dWaXNpYmxlID0gZmFsc2VcIj5DYW5jZWw8L2VsLWJ1dHRvbj5cbiAgICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIEBjbGljaz1cImNlbnRlckRpYWxvZ1Zpc2libGUgPSBmYWxzZVwiPlxuICAgICAgICAgIENvbmZpcm1cbiAgICAgICAgPC9lbC1idXR0b24+XG4gICAgICA8L2Rpdj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLWRpYWxvZz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNlbnRlckRpYWxvZ1Zpc2libGUgPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/centered-content.vue)_

vue

```
<template>
  <el-button plain @click="centerDialogVisible = true">
    Click to open the Dialog
  </el-button>

  <el-dialog v-model="centerDialogVisible" title="Warning" width="500" center>
    <span>
      It should be noted that the content will not be aligned in center by
      default
    </span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="centerDialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const centerDialogVisible = ref(false)
</script>
```

隐藏源代码

TIP

Dialog 的内容是懒渲染的——在被第一次打开之前，传入的默认 slot 不会被立即渲染到 DOM 上。 因此，如果需要执行 DOM 操作，或通过 `ref` 获取相应组件，请在 `open` 事件回调中进行。

## 居中对话框 [​](#居中对话框)

从屏幕中心打开对话框。

设置 `align-center` 为 `true` 使对话框水平垂直居中。 由于对话框垂直居中在弹性盒子中，所以`top`属性将不起作用。

Click to open the Dialog

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cImNlbnRlckRpYWxvZ1Zpc2libGUgPSB0cnVlXCI+XG4gICAgQ2xpY2sgdG8gb3BlbiB0aGUgRGlhbG9nXG4gIDwvZWwtYnV0dG9uPlxuXG4gIDxlbC1kaWFsb2dcbiAgICB2LW1vZGVsPVwiY2VudGVyRGlhbG9nVmlzaWJsZVwiXG4gICAgdGl0bGU9XCJXYXJuaW5nXCJcbiAgICB3aWR0aD1cIjUwMFwiXG4gICAgYWxpZ24tY2VudGVyXG4gID5cbiAgICA8c3Bhbj5PcGVuIHRoZSBkaWFsb2cgZnJvbSB0aGUgY2VudGVyIGZyb20gdGhlIHNjcmVlbjwvc3Bhbj5cbiAgICA8dGVtcGxhdGUgI2Zvb3Rlcj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkaWFsb2ctZm9vdGVyXCI+XG4gICAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwiY2VudGVyRGlhbG9nVmlzaWJsZSA9IGZhbHNlXCI+Q2FuY2VsPC9lbC1idXR0b24+XG4gICAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBAY2xpY2s9XCJjZW50ZXJEaWFsb2dWaXNpYmxlID0gZmFsc2VcIj5cbiAgICAgICAgICBDb25maXJtXG4gICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1kaWFsb2c+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBjZW50ZXJEaWFsb2dWaXNpYmxlID0gcmVmKGZhbHNlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/align-center.vue)_

vue

```
<template>
  <el-button plain @click="centerDialogVisible = true">
    Click to open the Dialog
  </el-button>

  <el-dialog
    v-model="centerDialogVisible"
    title="Warning"
    width="500"
    align-center
  >
    <span>Open the dialog from the center from the screen</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="centerDialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const centerDialogVisible = ref(false)
</script>
```

隐藏源代码

## 关闭时销毁 [​](#关闭时销毁)

启用此功能时，默认栏位下的内容将使用 `v-if` 指令销毁。 当出现性能问题时，可以启用此功能。

需要注意的是，当这个属性被启用时，在 `transition.beforeEnter` 事件卸载前，除了 `overlay`、`header (可选)`与`footer(可选)` ，Dialog 内不会有其它任何其它的 DOM 节点存在。

Click to open Dialog

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cImNlbnRlckRpYWxvZ1Zpc2libGUgPSB0cnVlXCI+XG4gICAgQ2xpY2sgdG8gb3BlbiBEaWFsb2dcbiAgPC9lbC1idXR0b24+XG5cbiAgPGVsLWRpYWxvZ1xuICAgIHYtbW9kZWw9XCJjZW50ZXJEaWFsb2dWaXNpYmxlXCJcbiAgICB0aXRsZT1cIk5vdGljZVwiXG4gICAgd2lkdGg9XCI1MDBcIlxuICAgIGRlc3Ryb3ktb24tY2xvc2VcbiAgICBjZW50ZXJcbiAgPlxuICAgIDxzcGFuPlxuICAgICAgTm90aWNlOiBiZWZvcmUgdGhlIGRpYWxvZyBpcyBvcGVuZWQgZm9yIHRoZSBmaXJzdCB0aW1lLCB0aGlzIG5vZGUgYW5kIHRoZVxuICAgICAgb25lIGJlbG93IHdpbGwgbm90IGJlIHJlbmRlcmVkLlxuICAgIDwvc3Bhbj5cbiAgICA8ZGl2PlxuICAgICAgPHN0cm9uZz5FeHRyYSBjb250ZW50IChOb3QgcmVuZGVyZWQpPC9zdHJvbmc+XG4gICAgPC9kaXY+XG4gICAgPHRlbXBsYXRlICNmb290ZXI+XG4gICAgICA8ZGl2IGNsYXNzPVwiZGlhbG9nLWZvb3RlclwiPlxuICAgICAgICA8ZWwtYnV0dG9uIEBjbGljaz1cImNlbnRlckRpYWxvZ1Zpc2libGUgPSBmYWxzZVwiPkNhbmNlbDwvZWwtYnV0dG9uPlxuICAgICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwiY2VudGVyRGlhbG9nVmlzaWJsZSA9IGZhbHNlXCI+XG4gICAgICAgICAgQ29uZmlybVxuICAgICAgICA8L2VsLWJ1dHRvbj5cbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtZGlhbG9nPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgY2VudGVyRGlhbG9nVmlzaWJsZSA9IHJlZihmYWxzZSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/destroy-on-close.vue)_

vue

```
<template>
  <el-button plain @click="centerDialogVisible = true">
    Click to open Dialog
  </el-button>

  <el-dialog
    v-model="centerDialogVisible"
    title="Notice"
    width="500"
    destroy-on-close
    center
  >
    <span>
      Notice: before the dialog is opened for the first time, this node and the
      one below will not be rendered.
    </span>
    <div>
      <strong>Extra content (Not rendered)</strong>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="centerDialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const centerDialogVisible = ref(false)
</script>
```

隐藏源代码

## 可拖拽对话框 [​](#可拖拽对话框)

试着拖动一下`header`部分吧

设置`draggable`属性为`true`以做到拖拽 设置 `overflow` 2.5.4 为 `true` 可以让拖拽范围超出可视区。

Open a draggable Dialog Open a overflow draggable Dialog Open a custom dragging style Dialog

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJkaWFsb2dWaXNpYmxlID0gdHJ1ZVwiPlxuICAgICAgT3BlbiBhIGRyYWdnYWJsZSBEaWFsb2dcbiAgICA8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJkaWFsb2dPdmVyZmxvd1Zpc2libGUgPSB0cnVlXCI+XG4gICAgICBPcGVuIGEgb3ZlcmZsb3cgZHJhZ2dhYmxlIERpYWxvZ1xuICAgIDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gY2xhc3M9XCIhbWwtMFwiIHBsYWluIEBjbGljaz1cImN1c3RvbURyYWdnaW5nVmlzaWJsZSA9IHRydWVcIj5cbiAgICAgIE9wZW4gYSBjdXN0b20gZHJhZ2dpbmcgc3R5bGUgRGlhbG9nXG4gICAgPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuXG4gIDxlbC1kaWFsb2cgdi1tb2RlbD1cImRpYWxvZ1Zpc2libGVcIiB0aXRsZT1cIlRpcHNcIiB3aWR0aD1cIjUwMFwiIGRyYWdnYWJsZT5cbiAgICA8c3Bhbj5JdCdzIGEgZHJhZ2dhYmxlIERpYWxvZzwvc3Bhbj5cbiAgICA8dGVtcGxhdGUgI2Zvb3Rlcj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkaWFsb2ctZm9vdGVyXCI+XG4gICAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwiZGlhbG9nVmlzaWJsZSA9IGZhbHNlXCI+Q2FuY2VsPC9lbC1idXR0b24+XG4gICAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBAY2xpY2s9XCJkaWFsb2dWaXNpYmxlID0gZmFsc2VcIj5cbiAgICAgICAgICBDb25maXJtXG4gICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1kaWFsb2c+XG5cbiAgPGVsLWRpYWxvZ1xuICAgIHYtbW9kZWw9XCJkaWFsb2dPdmVyZmxvd1Zpc2libGVcIlxuICAgIHRpdGxlPVwiVGlwc1wiXG4gICAgd2lkdGg9XCI1MDBcIlxuICAgIGRyYWdnYWJsZVxuICAgIG92ZXJmbG93XG4gID5cbiAgICA8c3Bhbj5JdCdzIGEgb3ZlcmZsb3cgZHJhZ2dhYmxlIERpYWxvZzwvc3Bhbj5cbiAgICA8dGVtcGxhdGUgI2Zvb3Rlcj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkaWFsb2ctZm9vdGVyXCI+XG4gICAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwiZGlhbG9nT3ZlcmZsb3dWaXNpYmxlID0gZmFsc2VcIj5DYW5jZWw8L2VsLWJ1dHRvbj5cbiAgICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIEBjbGljaz1cImRpYWxvZ092ZXJmbG93VmlzaWJsZSA9IGZhbHNlXCI+XG4gICAgICAgICAgQ29uZmlybVxuICAgICAgICA8L2VsLWJ1dHRvbj5cbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtZGlhbG9nPlxuXG4gIDxlbC1kaWFsb2dcbiAgICB2LW1vZGVsPVwiY3VzdG9tRHJhZ2dpbmdWaXNpYmxlXCJcbiAgICBjbGFzcz1cImN1c3RvbS1kcmFnZ2luZy1zdHlsZVwiXG4gICAgdGl0bGU9XCJDdXN0b20gRHJhZ2dpbmcgU3R5bGVcIlxuICAgIHdpZHRoPVwiNTAwXCJcbiAgICBkcmFnZ2FibGVcbiAgPlxuICAgIDxzcGFuXG4gICAgICA+VGhpcyBkaWFsb2cgaGFzIGN1c3RvbSBkcmFnZ2luZyBzdHlsZXMuIFRyeSBkcmFnZ2luZyBpdCB0byBzZWUgdGhlXG4gICAgICBlZmZlY3RzITwvc3BhblxuICAgID5cbiAgICA8dGVtcGxhdGUgI2Zvb3Rlcj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkaWFsb2ctZm9vdGVyXCI+XG4gICAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwiY3VzdG9tRHJhZ2dpbmdWaXNpYmxlID0gZmFsc2VcIj5DYW5jZWw8L2VsLWJ1dHRvbj5cbiAgICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIEBjbGljaz1cImN1c3RvbURyYWdnaW5nVmlzaWJsZSA9IGZhbHNlXCI+XG4gICAgICAgICAgQ29uZmlybVxuICAgICAgICA8L2VsLWJ1dHRvbj5cbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtZGlhbG9nPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgZGlhbG9nVmlzaWJsZSA9IHJlZihmYWxzZSlcbmNvbnN0IGRpYWxvZ092ZXJmbG93VmlzaWJsZSA9IHJlZihmYWxzZSlcbmNvbnN0IGN1c3RvbURyYWdnaW5nVmlzaWJsZSA9IHJlZihmYWxzZSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuOmdsb2JhbCguY3VzdG9tLWRyYWdnaW5nLXN0eWxlLmlzLWRyYWdnaW5nKSB7XG4gIGJvcmRlcjogMnB4IGRhc2hlZCB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgb3BhY2l0eTogMC42NTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/draggable-dialog.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" plain @click="dialogVisible = true">
      Open a draggable Dialog
    </el-button>
    <el-button class="!ml-0" plain @click="dialogOverflowVisible = true">
      Open a overflow draggable Dialog
    </el-button>
    <el-button class="!ml-0" plain @click="customDraggingVisible = true">
      Open a custom dragging style Dialog
    </el-button>
  </div>

  <el-dialog v-model="dialogVisible" title="Tips" width="500" draggable>
    <span>It's a draggable Dialog</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog
    v-model="dialogOverflowVisible"
    title="Tips"
    width="500"
    draggable
    overflow
  >
    <span>It's a overflow draggable Dialog</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogOverflowVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogOverflowVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog
    v-model="customDraggingVisible"
    class="custom-dragging-style"
    title="Custom Dragging Style"
    width="500"
    draggable
  >
    <span
      >This dialog has custom dragging styles. Try dragging it to see the
      effects!</span
    >
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="customDraggingVisible = false">Cancel</el-button>
        <el-button type="primary" @click="customDraggingVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const dialogVisible = ref(false)
const dialogOverflowVisible = ref(false)
const customDraggingVisible = ref(false)
</script>

<style scoped>
:global(.custom-dragging-style.is-dragging) {
  border: 2px dashed var(--el-color-primary);
  opacity: 0.65;
}
</style>
```

隐藏源代码

TIP

当 `modal` 的值为 false 时，请一定要确保 `append-to-body` 属性为 **true**，由于 `Dialog` 使用 `position: relative` 定位，当外层的遮罩层被移除时，`Dialog` 则会根据当前 DOM 上的祖先节点来定位，因此可能造成定位问题。

## 全屏 [​](#全屏)

设置 `fullscreen` 属性来打开全屏对话框。

Open the fullscreen Dialog

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cImRpYWxvZ1Zpc2libGUgPSB0cnVlXCI+XG4gICAgT3BlbiB0aGUgZnVsbHNjcmVlbiBEaWFsb2dcbiAgPC9lbC1idXR0b24+XG5cbiAgPGVsLWRpYWxvZyB2LW1vZGVsPVwiZGlhbG9nVmlzaWJsZVwiIGZ1bGxzY3JlZW4+XG4gICAgPHNwYW4+SXQncyBhIGZ1bGxzY3JlZW4gRGlhbG9nPC9zcGFuPlxuICAgIDx0ZW1wbGF0ZSAjZm9vdGVyPlxuICAgICAgPGRpdiBjbGFzcz1cImRpYWxvZy1mb290ZXJcIj5cbiAgICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJkaWFsb2dWaXNpYmxlID0gZmFsc2VcIj5DYW5jZWw8L2VsLWJ1dHRvbj5cbiAgICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIEBjbGljaz1cImRpYWxvZ1Zpc2libGUgPSBmYWxzZVwiPlxuICAgICAgICAgIENvbmZpcm1cbiAgICAgICAgPC9lbC1idXR0b24+XG4gICAgICA8L2Rpdj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLWRpYWxvZz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGRpYWxvZ1Zpc2libGUgPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/fullscreen.vue)_

vue

```
<template>
  <el-button plain @click="dialogVisible = true">
    Open the fullscreen Dialog
  </el-button>

  <el-dialog v-model="dialogVisible" fullscreen>
    <span>It's a fullscreen Dialog</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const dialogVisible = ref(false)
</script>
```

隐藏源代码

TIP

如果 `fullscreen` 为 true，则 `width`、`top` 和 `draggable` 属性无效。

## 模态框 [​](#模态框)

将 `modal` 设置为 `false` 会隐藏对话框的模态（覆盖层）。

从版本 2.10.5 起，新增了 `modal-penetrable`属性，该属性可设置为“可穿透”（即允许穿透）。

Open the modal Dialog

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cImRpYWxvZ1Zpc2libGUgPSB0cnVlXCI+XG4gICAgT3BlbiB0aGUgbW9kYWwgRGlhbG9nXG4gIDwvZWwtYnV0dG9uPlxuXG4gIDxlbC1kaWFsb2cgdi1tb2RlbD1cImRpYWxvZ1Zpc2libGVcIiA6bW9kYWw9XCJmYWxzZVwiIG1vZGFsLXBlbmV0cmFibGU+XG4gICAgPHNwYW4+SXQncyBhIG1vZGFsIERpYWxvZzwvc3Bhbj5cbiAgICA8dGVtcGxhdGUgI2Zvb3Rlcj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkaWFsb2ctZm9vdGVyXCI+XG4gICAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwiZGlhbG9nVmlzaWJsZSA9IGZhbHNlXCI+Q2FuY2VsPC9lbC1idXR0b24+XG4gICAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBAY2xpY2s9XCJkaWFsb2dWaXNpYmxlID0gZmFsc2VcIj5cbiAgICAgICAgICBDb25maXJtXG4gICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1kaWFsb2c+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBkaWFsb2dWaXNpYmxlID0gcmVmKGZhbHNlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/modal.vue)_

vue

```
<template>
  <el-button plain @click="dialogVisible = true">
    Open the modal Dialog
  </el-button>

  <el-dialog v-model="dialogVisible" :modal="false" modal-penetrable>
    <span>It's a modal Dialog</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const dialogVisible = ref(false)
</script>
```

隐藏源代码

## 自定义动画 2.10.5 [​](#自定义动画)

通过 `transition` 属性自定义对话框动画，该属性可以接受以下任意一种值：

-   动画名称（字符串）

-   Vue 过渡配置（对象）

示例包括缩放（scale）、滑动（slide）、淡入淡出（fade）、弹跳（bounce）动画，以及带有自定义事件处理器的基于对象的配置。

Default Scale Slide Bounce Object Config

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1idXR0b24gcGxhaW4gQGNsaWNrPVwib3BlbkRpYWxvZygnZmFkZScpXCI+IERlZmF1bHQgPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBwbGFpbiBAY2xpY2s9XCJvcGVuRGlhbG9nKCdzY2FsZScpXCI+IFNjYWxlIDwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gcGxhaW4gQGNsaWNrPVwib3BlbkRpYWxvZygnc2xpZGUnKVwiPiBTbGlkZSA8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5EaWFsb2coJ2JvdW5jZScpXCI+IEJvdW5jZSA8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5EaWFsb2dXaXRoT2JqZWN0XCI+IE9iamVjdCBDb25maWcgPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuXG4gIDxlbC1kaWFsb2dcbiAgICB2LW1vZGVsPVwiZGlhbG9nVmlzaWJsZVwiXG4gICAgY2xhc3M9XCJjdXN0b20tdHJhbnNpdGlvbi1kaWFsb2dcIlxuICAgIDp0aXRsZT1cImAke2N1cnJlbnRBbmltYXRpb259IEFuaW1hdGlvbiBEaWFsb2dgXCJcbiAgICB3aWR0aD1cIjMwJVwiXG4gICAgOnRyYW5zaXRpb249XCJ0cmFuc2l0aW9uQ29uZmlnXCJcbiAgPlxuICAgIDxkaXY+XG4gICAgICA8cD5cbiAgICAgICAgQ3VycmVudCBhbmltYXRpb246IDxzdHJvbmc+e3sgY3VycmVudEFuaW1hdGlvbiB9fTwvc3Ryb25nPlxuICAgICAgPC9wPlxuICAgICAgPHA+XG4gICAgICAgIFRoaXMgZGlhbG9nIGRlbW9uc3RyYXRlcyB0aGUge3sgY3VycmVudEFuaW1hdGlvbiB9fSBhbmltYXRpb24gZWZmZWN0LlxuICAgICAgPC9wPlxuICAgICAgPHAgdi1pZj1cImlzT2JqZWN0Q29uZmlnXCI+XG4gICAgICAgIDxzdHJvbmc+VXNpbmcgb2JqZWN0IGNvbmZpZ3VyYXRpb246PC9zdHJvbmc+PGJyIC8+XG4gICAgICAgIDxjb2RlPnt7IEpTT04uc3RyaW5naWZ5KHRyYW5zaXRpb25Db25maWcsIG51bGwsIDIpIH19PC9jb2RlPlxuICAgICAgPC9wPlxuICAgIDwvZGl2PlxuICAgIDx0ZW1wbGF0ZSAjZm9vdGVyPlxuICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJkaWFsb2dWaXNpYmxlID0gZmFsc2VcIj5DYW5jZWw8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBAY2xpY2s9XCJkaWFsb2dWaXNpYmxlID0gZmFsc2VcIj5cbiAgICAgICAgQ29uZmlybVxuICAgICAgPC9lbC1idXR0b24+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1kaWFsb2c+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgY29tcHV0ZWQsIHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBEaWFsb2dUcmFuc2l0aW9uIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBkaWFsb2dWaXNpYmxlID0gcmVmKGZhbHNlKVxuY29uc3QgY3VycmVudEFuaW1hdGlvbiA9IHJlZignZmFkZScpXG5jb25zdCBpc09iamVjdENvbmZpZyA9IHJlZihmYWxzZSlcblxuY29uc3QgdHJhbnNpdGlvbkNvbmZpZyA9IGNvbXB1dGVkPERpYWxvZ1RyYW5zaXRpb24+KCgpID0+IHtcbiAgaWYgKGlzT2JqZWN0Q29uZmlnLnZhbHVlKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIG5hbWU6ICdkaWFsb2ctY3VzdG9tLW9iamVjdCcsXG4gICAgICBhcHBlYXI6IHRydWUsXG4gICAgICBtb2RlOiAnb3V0LWluJyxcbiAgICAgIGR1cmF0aW9uOiA1MDAsXG4gICAgfVxuICB9XG4gIHJldHVybiBgZGlhbG9nLSR7Y3VycmVudEFuaW1hdGlvbi52YWx1ZX1gXG59KVxuXG5jb25zdCBvcGVuRGlhbG9nID0gKHR5cGU6IHN0cmluZykgPT4ge1xuICBjdXJyZW50QW5pbWF0aW9uLnZhbHVlID0gdHlwZVxuICBpc09iamVjdENvbmZpZy52YWx1ZSA9IGZhbHNlXG4gIGRpYWxvZ1Zpc2libGUudmFsdWUgPSB0cnVlXG59XG5cbmNvbnN0IG9wZW5EaWFsb2dXaXRoT2JqZWN0ID0gKCkgPT4ge1xuICBjdXJyZW50QW5pbWF0aW9uLnZhbHVlID0gJ29iamVjdC1jb25maWcnXG4gIGlzT2JqZWN0Q29uZmlnLnZhbHVlID0gdHJ1ZVxuICBkaWFsb2dWaXNpYmxlLnZhbHVlID0gdHJ1ZVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG5jb2RlIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tZWwtYmctY29sb3ItcGFnZSk7XG4gIHBhZGRpbmc6IDRweCA4cHg7XG4gIGJvcmRlci1yYWRpdXM6IDRweDtcbiAgZm9udC1zaXplOiAxMnB4O1xuICBkaXNwbGF5OiBibG9jaztcbiAgbWFyZ2luLXRvcDogOHB4O1xufVxuPC9zdHlsZT5cblxuPHN0eWxlPlxuLyogU2NhbGUgQW5pbWF0aW9uICovXG4uZGlhbG9nLXNjYWxlLWVudGVyLWFjdGl2ZSxcbi5kaWFsb2ctc2NhbGUtbGVhdmUtYWN0aXZlLFxuLmRpYWxvZy1zY2FsZS1lbnRlci1hY3RpdmUgLmVsLWRpYWxvZyxcbi5kaWFsb2ctc2NhbGUtbGVhdmUtYWN0aXZlIC5lbC1kaWFsb2cge1xuICB0cmFuc2l0aW9uOiBhbGwgMC4ycyBjdWJpYy1iZXppZXIoMC42NDUsIDAuMDQ1LCAwLjM1NSwgMSk7XG59XG5cbi5kaWFsb2ctc2NhbGUtZW50ZXItZnJvbSxcbi5kaWFsb2ctc2NhbGUtbGVhdmUtdG8ge1xuICBvcGFjaXR5OiAwO1xufVxuXG4uZGlhbG9nLXNjYWxlLWVudGVyLWZyb20gLmVsLWRpYWxvZyxcbi5kaWFsb2ctc2NhbGUtbGVhdmUtdG8gLmVsLWRpYWxvZyB7XG4gIHRyYW5zZm9ybTogc2NhbGUoMC41KTtcbiAgb3BhY2l0eTogMDtcbn1cblxuLyogU2xpZGUgQW5pbWF0aW9uICovXG4uZGlhbG9nLXNsaWRlLWVudGVyLWFjdGl2ZSxcbi5kaWFsb2ctc2xpZGUtbGVhdmUtYWN0aXZlLFxuLmRpYWxvZy1zbGlkZS1lbnRlci1hY3RpdmUgLmVsLWRpYWxvZyxcbi5kaWFsb2ctc2xpZGUtbGVhdmUtYWN0aXZlIC5lbC1kaWFsb2cge1xuICB0cmFuc2l0aW9uOiBhbGwgMC4zcyBjdWJpYy1iZXppZXIoMC4yNSwgMC40NiwgMC40NSwgMC45NCk7XG59XG5cbi5kaWFsb2ctc2xpZGUtZW50ZXItZnJvbSxcbi5kaWFsb2ctc2xpZGUtbGVhdmUtdG8ge1xuICBvcGFjaXR5OiAwO1xufVxuXG4uZGlhbG9nLXNsaWRlLWVudGVyLWZyb20gLmVsLWRpYWxvZyxcbi5kaWFsb2ctc2xpZGUtbGVhdmUtdG8gLmVsLWRpYWxvZyB7XG4gIHRyYW5zZm9ybTogdHJhbnNsYXRlWSgtMTAwcHgpO1xuICBvcGFjaXR5OiAwO1xufVxuXG4vKiBCb3VuY2UgQW5pbWF0aW9uICovXG4uZGlhbG9nLWJvdW5jZS1lbnRlci1hY3RpdmUsXG4uZGlhbG9nLWJvdW5jZS1sZWF2ZS1hY3RpdmUsXG4uZGlhbG9nLWJvdW5jZS1lbnRlci1hY3RpdmUgLmVsLWRpYWxvZyxcbi5kaWFsb2ctYm91bmNlLWxlYXZlLWFjdGl2ZSAuZWwtZGlhbG9nIHtcbiAgdHJhbnNpdGlvbjogYWxsIDAuNXMgY3ViaWMtYmV6aWVyKDAuMTc1LCAwLjg4NSwgMC4zMiwgMS4yNzUpO1xufVxuXG4uZGlhbG9nLWJvdW5jZS1lbnRlci1mcm9tLFxuLmRpYWxvZy1ib3VuY2UtbGVhdmUtdG8ge1xuICBvcGFjaXR5OiAwO1xufVxuXG4uZGlhbG9nLWJvdW5jZS1lbnRlci1mcm9tIC5lbC1kaWFsb2csXG4uZGlhbG9nLWJvdW5jZS1sZWF2ZS10byAuZWwtZGlhbG9nIHtcbiAgdHJhbnNmb3JtOiBzY2FsZSgwLjMpIHRyYW5zbGF0ZVkoLTUwcHgpO1xuICBvcGFjaXR5OiAwO1xufVxuXG4vKiBPYmplY3QgQ29uZmlndXJhdGlvbiBBbmltYXRpb24gKi9cbi5kaWFsb2ctY3VzdG9tLW9iamVjdC1lbnRlci1hY3RpdmUsXG4uZGlhbG9nLWN1c3RvbS1vYmplY3QtbGVhdmUtYWN0aXZlLFxuLmRpYWxvZy1jdXN0b20tb2JqZWN0LWVudGVyLWFjdGl2ZSAuZWwtZGlhbG9nLFxuLmRpYWxvZy1jdXN0b20tb2JqZWN0LWxlYXZlLWFjdGl2ZSAuZWwtZGlhbG9nIHtcbiAgdHJhbnNpdGlvbjogYWxsIDAuNXMgY3ViaWMtYmV6aWVyKDAuMjUsIDAuOCwgMC4yNSwgMSk7XG59XG5cbi5kaWFsb2ctY3VzdG9tLW9iamVjdC1lbnRlci1mcm9tLFxuLmRpYWxvZy1jdXN0b20tb2JqZWN0LWxlYXZlLXRvIHtcbiAgb3BhY2l0eTogMDtcbn1cblxuLmRpYWxvZy1jdXN0b20tb2JqZWN0LWVudGVyLWZyb20gLmVsLWRpYWxvZyxcbi5kaWFsb2ctY3VzdG9tLW9iamVjdC1sZWF2ZS10byAuZWwtZGlhbG9nIHtcbiAgdHJhbnNmb3JtOiByb3RhdGUoMTgwZGVnKSBzY2FsZSgwLjUpO1xuICBvcGFjaXR5OiAwO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/custom-animation.vue)_

vue

```
<template>
  <div>
    <el-button plain @click="openDialog('fade')"> Default </el-button>
    <el-button plain @click="openDialog('scale')"> Scale </el-button>
    <el-button plain @click="openDialog('slide')"> Slide </el-button>
    <el-button plain @click="openDialog('bounce')"> Bounce </el-button>
    <el-button plain @click="openDialogWithObject"> Object Config </el-button>
  </div>

  <el-dialog
    v-model="dialogVisible"
    class="custom-transition-dialog"
    :title="`${currentAnimation} Animation Dialog`"
    width="30%"
    :transition="transitionConfig"
  >
    <div>
      <p>
        Current animation: <strong>{{ currentAnimation }}</strong>
      </p>
      <p>
        This dialog demonstrates the {{ currentAnimation }} animation effect.
      </p>
      <p v-if="isObjectConfig">
        <strong>Using object configuration:</strong><br />
        <code>{{ JSON.stringify(transitionConfig, null, 2) }}</code>
      </p>
    </div>
    <template #footer>
      <el-button @click="dialogVisible = false">Cancel</el-button>
      <el-button type="primary" @click="dialogVisible = false">
        Confirm
      </el-button>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'

import type { DialogTransition } from 'element-plus'

const dialogVisible = ref(false)
const currentAnimation = ref('fade')
const isObjectConfig = ref(false)

const transitionConfig = computed<DialogTransition>(() => {
  if (isObjectConfig.value) {
    return {
      name: 'dialog-custom-object',
      appear: true,
      mode: 'out-in',
      duration: 500,
    }
  }
  return `dialog-${currentAnimation.value}`
})

const openDialog = (type: string) => {
  currentAnimation.value = type
  isObjectConfig.value = false
  dialogVisible.value = true
}

const openDialogWithObject = () => {
  currentAnimation.value = 'object-config'
  isObjectConfig.value = true
  dialogVisible.value = true
}
</script>

<style scoped>
code {
  background: var(--el-bg-color-page);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  display: block;
  margin-top: 8px;
}
</style>

<style>
/* Scale Animation */
.dialog-scale-enter-active,
.dialog-scale-leave-active,
.dialog-scale-enter-active .el-dialog,
.dialog-scale-leave-active .el-dialog {
  transition: all 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
}

.dialog-scale-enter-from,
.dialog-scale-leave-to {
  opacity: 0;
}

.dialog-scale-enter-from .el-dialog,
.dialog-scale-leave-to .el-dialog {
  transform: scale(0.5);
  opacity: 0;
}

/* Slide Animation */
.dialog-slide-enter-active,
.dialog-slide-leave-active,
.dialog-slide-enter-active .el-dialog,
.dialog-slide-leave-active .el-dialog {
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.dialog-slide-enter-from,
.dialog-slide-leave-to {
  opacity: 0;
}

.dialog-slide-enter-from .el-dialog,
.dialog-slide-leave-to .el-dialog {
  transform: translateY(-100px);
  opacity: 0;
}

/* Bounce Animation */
.dialog-bounce-enter-active,
.dialog-bounce-leave-active,
.dialog-bounce-enter-active .el-dialog,
.dialog-bounce-leave-active .el-dialog {
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.dialog-bounce-enter-from,
.dialog-bounce-leave-to {
  opacity: 0;
}

.dialog-bounce-enter-from .el-dialog,
.dialog-bounce-leave-to .el-dialog {
  transform: scale(0.3) translateY(-50px);
  opacity: 0;
}

/* Object Configuration Animation */
.dialog-custom-object-enter-active,
.dialog-custom-object-leave-active,
.dialog-custom-object-enter-active .el-dialog,
.dialog-custom-object-leave-active .el-dialog {
  transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.dialog-custom-object-enter-from,
.dialog-custom-object-leave-to {
  opacity: 0;
}

.dialog-custom-object-enter-from .el-dialog,
.dialog-custom-object-leave-to .el-dialog {
  transform: rotate(180deg) scale(0.5);
  opacity: 0;
}
</style>
```

隐藏源代码

TIP

动画类会根据过渡名称动态生成。 为了更细致地控制动画行为，你可以明确地定义这些类。 详情请参见 [自定义过渡类（custom-transition-classes）](https://vuejs.org/guide/built-ins/transition.html#custom-transition-classes)。

## Events [​](#events)

打开开发者控制台(ctrl + shift + J)，查看事件的顺序。

Open the event Dialog

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cImRpYWxvZ1Zpc2libGUgPSB0cnVlXCI+XG4gICAgT3BlbiB0aGUgZXZlbnQgRGlhbG9nXG4gIDwvZWwtYnV0dG9uPlxuXG4gIDxlbC1kaWFsb2dcbiAgICB2LW1vZGVsPVwiZGlhbG9nVmlzaWJsZVwiXG4gICAgbW9kYWwtY2xhc3M9XCJvdmVyaWRlLWFuaW1hdGlvblwiXG4gICAgOmJlZm9yZS1jbG9zZT1cIlxuICAgICAgKGRvbmVGbikgPT4ge1xuICAgICAgICA7KGNvbnNvbGUubG9nKCdiZWZvcmUtY2xvc2UnKSwgZG9uZUZuKCkpXG4gICAgICB9XG4gICAgXCJcbiAgICBAb3Blbj1cImNvbnNvbGUubG9nKCdvcGVuJylcIlxuICAgIEBvcGVuLWF1dG8tZm9jdXM9XCJjb25zb2xlLmxvZygnb3Blbi1hdXRvLWZvY3VzJylcIlxuICAgIEBvcGVuZWQ9XCJjb25zb2xlLmxvZygnb3BlbmVkJylcIlxuICAgIEBjbG9zZT1cImNvbnNvbGUubG9nKCdjbG9zZScpXCJcbiAgICBAY2xvc2UtYXV0by1mb2N1cz1cImNvbnNvbGUubG9nKCdjbG9zZS1hdXRvLWZvY3VzJylcIlxuICAgIEBjbG9zZWQ9XCJjb25zb2xlLmxvZygnY2xvc2VkJylcIlxuICA+XG4gICAgPHNwYW4+SXQncyBhIGV2ZW50IERpYWxvZzwvc3Bhbj5cbiAgICA8dGVtcGxhdGUgI2Zvb3Rlcj5cbiAgICAgIDxkaXYgY2xhc3M9XCJkaWFsb2ctZm9vdGVyXCI+XG4gICAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwiZGlhbG9nVmlzaWJsZSA9IGZhbHNlXCI+Q2FuY2VsPC9lbC1idXR0b24+XG4gICAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBAY2xpY2s9XCJkaWFsb2dWaXNpYmxlID0gZmFsc2VcIj5cbiAgICAgICAgICBDb25maXJtXG4gICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1kaWFsb2c+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBkaWFsb2dWaXNpYmxlID0gcmVmKGZhbHNlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dialog/events.vue)_

vue

```
<template>
  <el-button plain @click="dialogVisible = true">
    Open the event Dialog
  </el-button>

  <el-dialog
    v-model="dialogVisible"
    modal-class="overide-animation"
    :before-close="
      (doneFn) => {
        ;(console.log('before-close'), doneFn())
      }
    "
    @open="console.log('open')"
    @open-auto-focus="console.log('open-auto-focus')"
    @opened="console.log('opened')"
    @close="console.log('close')"
    @close-auto-focus="console.log('close-auto-focus')"
    @closed="console.log('closed')"
  >
    <span>It's a event Dialog</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const dialogVisible = ref(false)
</script>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| model-value / v-model | 是否显示 Dialog | `boolean` | false |
| title | Dialog 对话框 Dialog 的标题， 也可通过具名 slot （见下表）传入 | `string` | '' |
| width | 对话框的宽度，默认值为 50% | `string` / `number` | '' |
| fullscreen | 是否为全屏 Dialog | `boolean` | false |
| top | dialog CSS 中的 margin-top 值，默认为 15vh | `string` | '' |
| modal | 是否需要遮罩层 | `boolean` | true |
| modal-penetrable 2.10.5 | 是否允许穿透遮罩层。 modal 属性必须为 `false`。 | `boolean` | false |
| modal-class | 遮罩的自定义类名 | `string` | — |
| header-class 2.9.3 | header 部分的自定义 class 名 | `string` | — |
| body-class 2.9.3 | body 部分的自定义 class 名 | `string` | — |
| footer-class 2.9.3 | footer 部分的自定义 class 名 | `string` | — |
| append-to-body | Dialog 自身是否插入至 body 元素上。 嵌套的 Dialog 必须指定该属性并赋值为 `true` | `boolean` | false |
| append-to 2.4.3 | Dialog 挂载到哪个 DOM 元素 将覆盖 `append-to-body` | `CSSSelector` / `HTMLElement` | body |
| lock-scroll | 是否在 Dialog 出现时将 body 滚动锁定 | `boolean` | true |
| open-delay | dialog 打开的延时时间，单位毫秒 | `number` | 0 |
| close-delay | dialog 关闭的延时时间，单位毫秒 | `number` | 0 |
| close-on-click-modal | 是否可以通过点击 modal 关闭 Dialog | `boolean` | true |
| close-on-press-escape | 是否可以通过按下 ESC 关闭 Dialog | `boolean` | true |
| show-close | 是否显示关闭按钮 | `boolean` | true |
| before-close | 关闭前的回调，会暂停 Dialog 的关闭. 回调函数内执行 done 参数方法的时候才是真正关闭对话框的时候. | `Function` | — |
| draggable | 为 Dialog 启用可拖拽功能 | `boolean` | false |
| overflow 2.5.4 | 拖动范围可以超出可视区 | `boolean` | false |
| center | 是否让 Dialog 的 header 和 footer 部分居中排列 | `boolean` | false |
| align-center 2.2.16 | 是否水平垂直对齐对话框 | `boolean` | false |
| destroy-on-close | 当关闭 Dialog 时，销毁其中的元素 | `boolean` | false |
| close-icon | 自定义关闭图标，默认 Close | `string` / `Component` | — |
| z-index | 和原生的 CSS 的 z-index 相同，改变 z 轴的顺序 | `number` | — |
| header-aria-level a11y | header 的 `aria-level` 属性 | `string` | 2 |
| transition 2.10.5 | 对话框动画的自定义过渡配置。 可以是一个字符串（过渡名称），也可以是一个包含 Vue 过渡属性的对象。 | `string` / `object` | dialog-fade |
| custom-class deprecated | Dialog 的自定义类名 | `string` | '' |

WARNING

`custom-class` 已被 **弃用**, 之后将会在 2.4.0 **移除**, 请使用 `class`.

### Slots [​](#slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 对话框的默认内容 |
| header | 对话框标题的内容；会替换标题部分，但不会移除关闭按钮。 |
| footer | Dialog 按钮操作区的内容 |
| title deprecated | 与 header 作用相同 请使用 header |

WARNING

`title` 已被**弃用**，并将在 3.0.0 版本中**移除**，请使用 `header` 代替。

### 事件 [​](#事件)

| 名称 | 详情 | Type |
| --- | --- | --- |
| open | Dialog 打开的回调 | `Function` |
| opened | Dialog 打开动画结束时的回调 | `Function` |
| close | Dialog 关闭的回调 | `Function` |
| closed | Dialog 关闭动画结束时的回调 | `Function` |
| open-auto-focus | 输入焦点聚焦在 Dialog 内容时的回调 | `Function` |
| close-auto-focus | 输入焦点从 Dialog 内容失焦时的回调 | `Function` |

### Exposes [​](#exposes)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| resetPosition 2.8.1 | 重置位置 | `Function` |
| handleClose 2.9.8 | 关闭对话框 | `Function` |

## FAQ [​](#faq)

#### 在 SFC 文件中使用对话框，scope 样式不会生效 [​](#在-sfc-文件中使用对话框-scope-样式不会生效)

典型议题：[#10515](https://github.com/element-plus/element-plus/issues/10515)

PS：既然对话框是使用 `Teleport` 渲染的，建议在全局范围写入根节点的样式。

#### 当对话框被显示及隐藏时，页面元素会来回移动（抖动） [​](#当对话框被显示及隐藏时-页面元素会来回移动-抖动)

典型议题：[#10481](https://github.com/element-plus/element-plus/issues/10481)

PS：建议将滚动区域放置在一个挂载的 vue 节点，如 `<div id="app" />` 下，并对 body 使用 `overflow: hidden` 样式。

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/dialog) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/dialog.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/dialog.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/1539496?v=4&size=64)](https://github.com/donga-gao)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/138789658?v=4&size=64)](https://github.com/StudiousGao)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/88474826?v=4&size=64)](https://github.com/wsVIC)[![](https://avatars.githubusercontent.com/u/54931083?v=4&size=64)](https://github.com/wjp980108)[![](https://avatars.githubusercontent.com/u/48633709?v=4&size=64)](https://github.com/cosine7)[![](https://avatars.githubusercontent.com/u/44218347?v=4&size=64)](https://github.com/yuuuuuyu)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/35426360?v=4&size=64)](https://github.com/Jungzl)[![](https://avatars.githubusercontent.com/u/30278419?v=4&size=64)](https://github.com/nothing-sy)[![](https://avatars.githubusercontent.com/u/23433168?v=4&size=64)](https://github.com/hunter-fl)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/4075314?v=4&size=64)](https://github.com/Giwayume)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/31959015?v=4&size=64)](https://github.com/Hfutsora)[![](https://avatars.githubusercontent.com/u/11536903?v=4&size=64)](https://github.com/zhoucan38)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/1411614?v=4&size=64)](https://github.com/spx443812507)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/234919486?v=4&size=64)](https://github.com/linzx-jess)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/57352899?v=4&size=64)](https://github.com/VisualYuki)[![](https://avatars.githubusercontent.com/u/45616067?v=4&size=64)](https://github.com/elioist)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/52314078?v=4&size=64)](https://github.com/vaebe)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)

[Alert 提示](https://element-plus.org/zh-CN/component/alert)

[Drawer 抽屉](https://element-plus.org/zh-CN/component/drawer)


