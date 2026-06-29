---
name: "form"
description: "Form 表单 -- Element Plus Vue3 桌面端组件。Invoke when user needs Form 表单 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/form.html"
---

---

# Form 表单 [​](#form-表单)

更新日志待解决

37

表单包含 `input`、`radio`、`select`、`checkbox` 等需要用户输入的组件。 使用表单，您可以收集、验证和提交数据。

TIP

Form 组件已经从 2. x 的 Float 布局升级为 Flex 布局。

## 典型表单 [​](#典型表单)

最基础的表单包括各种输入表单项，比如`input`、`select`、`radio`、`checkbox`等。

在每一个 `form` 组件中，你需要一个 `form-item` 字段作为输入项的容器，用于获取值与验证值。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZm9ybSA6bW9kZWw9XCJmb3JtXCIgbGFiZWwtd2lkdGg9XCJhdXRvXCIgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCI+XG4gICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkFjdGl2aXR5IG5hbWVcIj5cbiAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwiZm9ybS5uYW1lXCIgLz5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiQWN0aXZpdHkgem9uZVwiPlxuICAgICAgPGVsLXNlbGVjdCB2LW1vZGVsPVwiZm9ybS5yZWdpb25cIiBwbGFjZWhvbGRlcj1cInBsZWFzZSBzZWxlY3QgeW91ciB6b25lXCI+XG4gICAgICAgIDxlbC1vcHRpb24gbGFiZWw9XCJab25lIG9uZVwiIHZhbHVlPVwic2hhbmdoYWlcIiAvPlxuICAgICAgICA8ZWwtb3B0aW9uIGxhYmVsPVwiWm9uZSB0d29cIiB2YWx1ZT1cImJlaWppbmdcIiAvPlxuICAgICAgPC9lbC1zZWxlY3Q+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkFjdGl2aXR5IHRpbWVcIj5cbiAgICAgIDxlbC1jb2wgOnNwYW49XCIxMVwiPlxuICAgICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgICB2LW1vZGVsPVwiZm9ybS5kYXRlMVwiXG4gICAgICAgICAgdHlwZT1cImRhdGVcIlxuICAgICAgICAgIHBsYWNlaG9sZGVyPVwiUGljayBhIGRhdGVcIlxuICAgICAgICAgIHN0eWxlPVwid2lkdGg6IDEwMCVcIlxuICAgICAgICAvPlxuICAgICAgPC9lbC1jb2w+XG4gICAgICA8ZWwtY29sIDpzcGFuPVwiMlwiIGNsYXNzPVwidGV4dC1jZW50ZXJcIj5cbiAgICAgICAgPHNwYW4gY2xhc3M9XCJ0ZXh0LWdyYXktNTAwXCI+LTwvc3Bhbj5cbiAgICAgIDwvZWwtY29sPlxuICAgICAgPGVsLWNvbCA6c3Bhbj1cIjExXCI+XG4gICAgICAgIDxlbC10aW1lLXBpY2tlclxuICAgICAgICAgIHYtbW9kZWw9XCJmb3JtLmRhdGUyXCJcbiAgICAgICAgICBwbGFjZWhvbGRlcj1cIlBpY2sgYSB0aW1lXCJcbiAgICAgICAgICBzdHlsZT1cIndpZHRoOiAxMDAlXCJcbiAgICAgICAgLz5cbiAgICAgIDwvZWwtY29sPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJJbnN0YW50IGRlbGl2ZXJ5XCI+XG4gICAgICA8ZWwtc3dpdGNoIHYtbW9kZWw9XCJmb3JtLmRlbGl2ZXJ5XCIgLz5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiQWN0aXZpdHkgdHlwZVwiPlxuICAgICAgPGVsLWNoZWNrYm94LWdyb3VwIHYtbW9kZWw9XCJmb3JtLnR5cGVcIj5cbiAgICAgICAgPGVsLWNoZWNrYm94IHZhbHVlPVwiT25saW5lIGFjdGl2aXRpZXNcIiBuYW1lPVwidHlwZVwiPlxuICAgICAgICAgIE9ubGluZSBhY3Rpdml0aWVzXG4gICAgICAgIDwvZWwtY2hlY2tib3g+XG4gICAgICAgIDxlbC1jaGVja2JveCB2YWx1ZT1cIlByb21vdGlvbiBhY3Rpdml0aWVzXCIgbmFtZT1cInR5cGVcIj5cbiAgICAgICAgICBQcm9tb3Rpb24gYWN0aXZpdGllc1xuICAgICAgICA8L2VsLWNoZWNrYm94PlxuICAgICAgICA8ZWwtY2hlY2tib3ggdmFsdWU9XCJPZmZsaW5lIGFjdGl2aXRpZXNcIiBuYW1lPVwidHlwZVwiPlxuICAgICAgICAgIE9mZmxpbmUgYWN0aXZpdGllc1xuICAgICAgICA8L2VsLWNoZWNrYm94PlxuICAgICAgICA8ZWwtY2hlY2tib3ggdmFsdWU9XCJTaW1wbGUgYnJhbmQgZXhwb3N1cmVcIiBuYW1lPVwidHlwZVwiPlxuICAgICAgICAgIFNpbXBsZSBicmFuZCBleHBvc3VyZVxuICAgICAgICA8L2VsLWNoZWNrYm94PlxuICAgICAgPC9lbC1jaGVja2JveC1ncm91cD5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiUmVzb3VyY2VzXCI+XG4gICAgICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cImZvcm0ucmVzb3VyY2VcIj5cbiAgICAgICAgPGVsLXJhZGlvIHZhbHVlPVwiU3BvbnNvclwiPlNwb25zb3I8L2VsLXJhZGlvPlxuICAgICAgICA8ZWwtcmFkaW8gdmFsdWU9XCJWZW51ZVwiPlZlbnVlPC9lbC1yYWRpbz5cbiAgICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkFjdGl2aXR5IGZvcm1cIj5cbiAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwiZm9ybS5kZXNjXCIgdHlwZT1cInRleHRhcmVhXCIgLz5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIEBjbGljaz1cIm9uU3VibWl0XCI+Q3JlYXRlPC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uPkNhbmNlbDwvZWwtYnV0dG9uPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICA8L2VsLWZvcm0+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVhY3RpdmUgfSBmcm9tICd2dWUnXG5cbi8vIGRvIG5vdCB1c2Ugc2FtZSBuYW1lIHdpdGggcmVmXG5jb25zdCBmb3JtID0gcmVhY3RpdmUoe1xuICBuYW1lOiAnJyxcbiAgcmVnaW9uOiAnJyxcbiAgZGF0ZTE6ICcnLFxuICBkYXRlMjogJycsXG4gIGRlbGl2ZXJ5OiBmYWxzZSxcbiAgdHlwZTogW10sXG4gIHJlc291cmNlOiAnJyxcbiAgZGVzYzogJycsXG59KVxuXG5jb25zdCBvblN1Ym1pdCA9ICgpID0+IHtcbiAgY29uc29sZS5sb2coJ3N1Ym1pdCEnKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/form/basic-form.vue)_

vue

```
<template>
  <el-form :model="form" label-width="auto" style="max-width: 600px">
    <el-form-item label="Activity name">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-form-item label="Activity zone">
      <el-select v-model="form.region" placeholder="please select your zone">
        <el-option label="Zone one" value="shanghai" />
        <el-option label="Zone two" value="beijing" />
      </el-select>
    </el-form-item>
    <el-form-item label="Activity time">
      <el-col :span="11">
        <el-date-picker
          v-model="form.date1"
          type="date"
          placeholder="Pick a date"
          style="width: 100%"
        />
      </el-col>
      <el-col :span="2" class="text-center">
        <span class="text-gray-500">-</span>
      </el-col>
      <el-col :span="11">
        <el-time-picker
          v-model="form.date2"
          placeholder="Pick a time"
          style="width: 100%"
        />
      </el-col>
    </el-form-item>
    <el-form-item label="Instant delivery">
      <el-switch v-model="form.delivery" />
    </el-form-item>
    <el-form-item label="Activity type">
      <el-checkbox-group v-model="form.type">
        <el-checkbox value="Online activities" name="type">
          Online activities
        </el-checkbox>
        <el-checkbox value="Promotion activities" name="type">
          Promotion activities
        </el-checkbox>
        <el-checkbox value="Offline activities" name="type">
          Offline activities
        </el-checkbox>
        <el-checkbox value="Simple brand exposure" name="type">
          Simple brand exposure
        </el-checkbox>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item label="Resources">
      <el-radio-group v-model="form.resource">
        <el-radio value="Sponsor">Sponsor</el-radio>
        <el-radio value="Venue">Venue</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="Activity form">
      <el-input v-model="form.desc" type="textarea" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Create</el-button>
      <el-button>Cancel</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

// do not use same name with ref
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

const onSubmit = () => {
  console.log('submit!')
}
</script>
```

隐藏源代码

TIP

[W3C](https://www.w3.org/MarkUp/html-spec/html-spec_8.html#SEC8.2) 标准定义：

> _当一个表单中只有一个单行文本输入字段时， 浏览器应当将在此字段中按下 Enter （回车键）的行为视为提交表单的请求。_ 如果希望阻止这一默认行为，可以在 `<el-form>` 标签上添加 `@submit.prevent`。

## 行内表单 [​](#行内表单)

当垂直方向空间受限且表单较简单时，可以在一行内放置表单。

通过设置 `inline` 属性为 `true` 可以让表单域变为行内的表单域。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZm9ybSA6aW5saW5lPVwidHJ1ZVwiIDptb2RlbD1cImZvcm1JbmxpbmVcIiBjbGFzcz1cImRlbW8tZm9ybS1pbmxpbmVcIj5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiQXBwcm92ZWQgYnlcIj5cbiAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwiZm9ybUlubGluZS51c2VyXCIgcGxhY2Vob2xkZXI9XCJBcHByb3ZlZCBieVwiIGNsZWFyYWJsZSAvPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJBY3Rpdml0eSB6b25lXCI+XG4gICAgICA8ZWwtc2VsZWN0XG4gICAgICAgIHYtbW9kZWw9XCJmb3JtSW5saW5lLnJlZ2lvblwiXG4gICAgICAgIHBsYWNlaG9sZGVyPVwiQWN0aXZpdHkgem9uZVwiXG4gICAgICAgIGNsZWFyYWJsZVxuICAgICAgPlxuICAgICAgICA8ZWwtb3B0aW9uIGxhYmVsPVwiWm9uZSBvbmVcIiB2YWx1ZT1cInNoYW5naGFpXCIgLz5cbiAgICAgICAgPGVsLW9wdGlvbiBsYWJlbD1cIlpvbmUgdHdvXCIgdmFsdWU9XCJiZWlqaW5nXCIgLz5cbiAgICAgIDwvZWwtc2VsZWN0PlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJBY3Rpdml0eSB0aW1lXCI+XG4gICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgdi1tb2RlbD1cImZvcm1JbmxpbmUuZGF0ZVwiXG4gICAgICAgIHR5cGU9XCJkYXRlXCJcbiAgICAgICAgcGxhY2Vob2xkZXI9XCJQaWNrIGEgZGF0ZVwiXG4gICAgICAgIGNsZWFyYWJsZVxuICAgICAgLz5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIEBjbGljaz1cIm9uU3VibWl0XCI+UXVlcnk8L2VsLWJ1dHRvbj5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgPC9lbC1mb3JtPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlYWN0aXZlIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBmb3JtSW5saW5lID0gcmVhY3RpdmUoe1xuICB1c2VyOiAnJyxcbiAgcmVnaW9uOiAnJyxcbiAgZGF0ZTogJycsXG59KVxuXG5jb25zdCBvblN1Ym1pdCA9ICgpID0+IHtcbiAgY29uc29sZS5sb2coJ3N1Ym1pdCEnKVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5kZW1vLWZvcm0taW5saW5lIC5lbC1pbnB1dCB7XG4gIC0tZWwtaW5wdXQtd2lkdGg6IDIyMHB4O1xufVxuXG4uZGVtby1mb3JtLWlubGluZSAuZWwtc2VsZWN0IHtcbiAgLS1lbC1zZWxlY3Qtd2lkdGg6IDIyMHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/form/inline-form.vue)_

vue

```
<template>
  <el-form :inline="true" :model="formInline" class="demo-form-inline">
    <el-form-item label="Approved by">
      <el-input v-model="formInline.user" placeholder="Approved by" clearable />
    </el-form-item>
    <el-form-item label="Activity zone">
      <el-select
        v-model="formInline.region"
        placeholder="Activity zone"
        clearable
      >
        <el-option label="Zone one" value="shanghai" />
        <el-option label="Zone two" value="beijing" />
      </el-select>
    </el-form-item>
    <el-form-item label="Activity time">
      <el-date-picker
        v-model="formInline.date"
        type="date"
        placeholder="Pick a date"
        clearable
      />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Query</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

const formInline = reactive({
  user: '',
  region: '',
  date: '',
})

const onSubmit = () => {
  console.log('submit!')
}
</script>

<style>
.demo-form-inline .el-input {
  --el-input-width: 220px;
}

.demo-form-inline .el-select {
  --el-select-width: 220px;
}
</style>
```

隐藏源代码

## 对齐方式 [​](#对齐方式)

根据你们的设计情况，来选择最佳的标签对齐方式。

您可以分别设置 `el-form-item` 的`label-position` 2.7.7. 如果值为空, 则会使用 `el-form`的`label-position`。

通过设置 `label-position` 属性可以改变表单域标签的位置，可选值为 `top`、`left`, 当设为 `top` 时标签会置于表单域的顶部

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZm9ybVxuICAgIDpsYWJlbC1wb3NpdGlvbj1cImxhYmVsUG9zaXRpb25cIlxuICAgIGxhYmVsLXdpZHRoPVwiYXV0b1wiXG4gICAgOm1vZGVsPVwiZm9ybUxhYmVsQWxpZ25cIlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gID5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiRm9ybSBBbGlnblwiIGxhYmVsLXBvc2l0aW9uPVwicmlnaHRcIj5cbiAgICAgIDxlbC1yYWRpby1ncm91cCB2LW1vZGVsPVwibGFiZWxQb3NpdGlvblwiIGFyaWEtbGFiZWw9XCJsYWJlbCBwb3NpdGlvblwiPlxuICAgICAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwibGVmdFwiPkxlZnQ8L2VsLXJhZGlvLWJ1dHRvbj5cbiAgICAgICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cInJpZ2h0XCI+UmlnaHQ8L2VsLXJhZGlvLWJ1dHRvbj5cbiAgICAgICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cInRvcFwiPlRvcDwvZWwtcmFkaW8tYnV0dG9uPlxuICAgICAgPC9lbC1yYWRpby1ncm91cD5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiRm9ybSBJdGVtIEFsaWduXCIgbGFiZWwtcG9zaXRpb249XCJyaWdodFwiPlxuICAgICAgPGVsLXJhZGlvLWdyb3VwXG4gICAgICAgIHYtbW9kZWw9XCJpdGVtTGFiZWxQb3NpdGlvblwiXG4gICAgICAgIGFyaWEtbGFiZWw9XCJpdGVtIGxhYmVsIHBvc2l0aW9uXCJcbiAgICAgID5cbiAgICAgICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cIlwiPkVtcHR5PC9lbC1yYWRpby1idXR0b24+XG4gICAgICAgIDxlbC1yYWRpby1idXR0b24gdmFsdWU9XCJsZWZ0XCI+TGVmdDwvZWwtcmFkaW8tYnV0dG9uPlxuICAgICAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwicmlnaHRcIj5SaWdodDwvZWwtcmFkaW8tYnV0dG9uPlxuICAgICAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwidG9wXCI+VG9wPC9lbC1yYWRpby1idXR0b24+XG4gICAgICA8L2VsLXJhZGlvLWdyb3VwPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJOYW1lXCIgOmxhYmVsLXBvc2l0aW9uPVwiaXRlbUxhYmVsUG9zaXRpb25cIj5cbiAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwiZm9ybUxhYmVsQWxpZ24ubmFtZVwiIC8+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkFjdGl2aXR5IHpvbmVcIiA6bGFiZWwtcG9zaXRpb249XCJpdGVtTGFiZWxQb3NpdGlvblwiPlxuICAgICAgPGVsLWlucHV0IHYtbW9kZWw9XCJmb3JtTGFiZWxBbGlnbi5yZWdpb25cIiAvPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJBY3Rpdml0eSBmb3JtXCIgOmxhYmVsLXBvc2l0aW9uPVwiaXRlbUxhYmVsUG9zaXRpb25cIj5cbiAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwiZm9ybUxhYmVsQWxpZ24udHlwZVwiIC8+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gIDwvZWwtZm9ybT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWFjdGl2ZSwgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IEZvcm1JdGVtUHJvcHMsIEZvcm1Qcm9wcyB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgbGFiZWxQb3NpdGlvbiA9IHJlZjxGb3JtUHJvcHNbJ2xhYmVsUG9zaXRpb24nXT4oJ3JpZ2h0JylcbmNvbnN0IGl0ZW1MYWJlbFBvc2l0aW9uID0gcmVmPEZvcm1JdGVtUHJvcHNbJ2xhYmVsUG9zaXRpb24nXT4oJycpXG5jb25zdCBmb3JtTGFiZWxBbGlnbiA9IHJlYWN0aXZlKHtcbiAgbmFtZTogJycsXG4gIHJlZ2lvbjogJycsXG4gIHR5cGU6ICcnLFxufSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/form/alignment.vue)_

vue

```
<template>
  <el-form
    :label-position="labelPosition"
    label-width="auto"
    :model="formLabelAlign"
    style="max-width: 600px"
  >
    <el-form-item label="Form Align" label-position="right">
      <el-radio-group v-model="labelPosition" aria-label="label position">
        <el-radio-button value="left">Left</el-radio-button>
        <el-radio-button value="right">Right</el-radio-button>
        <el-radio-button value="top">Top</el-radio-button>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="Form Item Align" label-position="right">
      <el-radio-group
        v-model="itemLabelPosition"
        aria-label="item label position"
      >
        <el-radio-button value="">Empty</el-radio-button>
        <el-radio-button value="left">Left</el-radio-button>
        <el-radio-button value="right">Right</el-radio-button>
        <el-radio-button value="top">Top</el-radio-button>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="Name" :label-position="itemLabelPosition">
      <el-input v-model="formLabelAlign.name" />
    </el-form-item>
    <el-form-item label="Activity zone" :label-position="itemLabelPosition">
      <el-input v-model="formLabelAlign.region" />
    </el-form-item>
    <el-form-item label="Activity form" :label-position="itemLabelPosition">
      <el-input v-model="formLabelAlign.type" />
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

import type { FormItemProps, FormProps } from 'element-plus'

const labelPosition = ref<FormProps['labelPosition']>('right')
const itemLabelPosition = ref<FormItemProps['labelPosition']>('')
const formLabelAlign = reactive({
  name: '',
  region: '',
  type: '',
})
</script>
```

隐藏源代码

## 表单校验 [​](#表单校验)

Form 组件允许你验证用户的输入是否符合规范，来帮助你找到和纠正错误。

`Form` 组件提供了表单验证的功能，只需为 `rules` 属性传入约定的验证规则，并将 `form-Item` 的 `prop` 属性设置为需要验证的特殊键值即可。 校验规则参见 [async-validator](https://github.com/yiminghe/async-validator)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZm9ybVxuICAgIHJlZj1cInJ1bGVGb3JtUmVmXCJcbiAgICBzdHlsZT1cIm1heC13aWR0aDogNjAwcHhcIlxuICAgIDptb2RlbD1cInJ1bGVGb3JtXCJcbiAgICA6cnVsZXM9XCJydWxlc1wiXG4gICAgbGFiZWwtd2lkdGg9XCJhdXRvXCJcbiAgPlxuICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJBY3Rpdml0eSBuYW1lXCIgcHJvcD1cIm5hbWVcIj5cbiAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwicnVsZUZvcm0ubmFtZVwiIC8+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkFjdGl2aXR5IHpvbmVcIiBwcm9wPVwicmVnaW9uXCI+XG4gICAgICA8ZWwtc2VsZWN0IHYtbW9kZWw9XCJydWxlRm9ybS5yZWdpb25cIiBwbGFjZWhvbGRlcj1cIkFjdGl2aXR5IHpvbmVcIj5cbiAgICAgICAgPGVsLW9wdGlvbiBsYWJlbD1cIlpvbmUgb25lXCIgdmFsdWU9XCJzaGFuZ2hhaVwiIC8+XG4gICAgICAgIDxlbC1vcHRpb24gbGFiZWw9XCJab25lIHR3b1wiIHZhbHVlPVwiYmVpamluZ1wiIC8+XG4gICAgICA8L2VsLXNlbGVjdD5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiQWN0aXZpdHkgY291bnRcIiBwcm9wPVwiY291bnRcIj5cbiAgICAgIDxlbC1zZWxlY3QtdjJcbiAgICAgICAgdi1tb2RlbD1cInJ1bGVGb3JtLmNvdW50XCJcbiAgICAgICAgcGxhY2Vob2xkZXI9XCJBY3Rpdml0eSBjb3VudFwiXG4gICAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICAvPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJBY3Rpdml0eSB0aW1lXCIgcmVxdWlyZWQ+XG4gICAgICA8ZWwtY29sIDpzcGFuPVwiMTFcIj5cbiAgICAgICAgPGVsLWZvcm0taXRlbSBwcm9wPVwiZGF0ZTFcIj5cbiAgICAgICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgICAgIHYtbW9kZWw9XCJydWxlRm9ybS5kYXRlMVwiXG4gICAgICAgICAgICB0eXBlPVwiZGF0ZVwiXG4gICAgICAgICAgICBhcmlhLWxhYmVsPVwiUGljayBhIGRhdGVcIlxuICAgICAgICAgICAgcGxhY2Vob2xkZXI9XCJQaWNrIGEgZGF0ZVwiXG4gICAgICAgICAgICBzdHlsZT1cIndpZHRoOiAxMDAlXCJcbiAgICAgICAgICAvPlxuICAgICAgICA8L2VsLWZvcm0taXRlbT5cbiAgICAgIDwvZWwtY29sPlxuICAgICAgPGVsLWNvbCBjbGFzcz1cInRleHQtY2VudGVyXCIgOnNwYW49XCIyXCI+XG4gICAgICAgIDxzcGFuIGNsYXNzPVwidGV4dC1ncmF5LTUwMFwiPi08L3NwYW4+XG4gICAgICA8L2VsLWNvbD5cbiAgICAgIDxlbC1jb2wgOnNwYW49XCIxMVwiPlxuICAgICAgICA8ZWwtZm9ybS1pdGVtIHByb3A9XCJkYXRlMlwiPlxuICAgICAgICAgIDxlbC10aW1lLXBpY2tlclxuICAgICAgICAgICAgdi1tb2RlbD1cInJ1bGVGb3JtLmRhdGUyXCJcbiAgICAgICAgICAgIGFyaWEtbGFiZWw9XCJQaWNrIGEgdGltZVwiXG4gICAgICAgICAgICBwbGFjZWhvbGRlcj1cIlBpY2sgYSB0aW1lXCJcbiAgICAgICAgICAgIHN0eWxlPVwid2lkdGg6IDEwMCVcIlxuICAgICAgICAgIC8+XG4gICAgICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgICAgPC9lbC1jb2w+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkluc3RhbnQgZGVsaXZlcnlcIiBwcm9wPVwiZGVsaXZlcnlcIj5cbiAgICAgIDxlbC1zd2l0Y2ggdi1tb2RlbD1cInJ1bGVGb3JtLmRlbGl2ZXJ5XCIgLz5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiQWN0aXZpdHkgbG9jYXRpb25cIiBwcm9wPVwibG9jYXRpb25cIj5cbiAgICAgIDxlbC1zZWdtZW50ZWQgdi1tb2RlbD1cInJ1bGVGb3JtLmxvY2F0aW9uXCIgOm9wdGlvbnM9XCJsb2NhdGlvbk9wdGlvbnNcIiAvPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJBY3Rpdml0eSB0eXBlXCIgcHJvcD1cInR5cGVcIj5cbiAgICAgIDxlbC1jaGVja2JveC1ncm91cCB2LW1vZGVsPVwicnVsZUZvcm0udHlwZVwiPlxuICAgICAgICA8ZWwtY2hlY2tib3ggdmFsdWU9XCJPbmxpbmUgYWN0aXZpdGllc1wiIG5hbWU9XCJ0eXBlXCI+XG4gICAgICAgICAgT25saW5lIGFjdGl2aXRpZXNcbiAgICAgICAgPC9lbC1jaGVja2JveD5cbiAgICAgICAgPGVsLWNoZWNrYm94IHZhbHVlPVwiUHJvbW90aW9uIGFjdGl2aXRpZXNcIiBuYW1lPVwidHlwZVwiPlxuICAgICAgICAgIFByb21vdGlvbiBhY3Rpdml0aWVzXG4gICAgICAgIDwvZWwtY2hlY2tib3g+XG4gICAgICAgIDxlbC1jaGVja2JveCB2YWx1ZT1cIk9mZmxpbmUgYWN0aXZpdGllc1wiIG5hbWU9XCJ0eXBlXCI+XG4gICAgICAgICAgT2ZmbGluZSBhY3Rpdml0aWVzXG4gICAgICAgIDwvZWwtY2hlY2tib3g+XG4gICAgICAgIDxlbC1jaGVja2JveCB2YWx1ZT1cIlNpbXBsZSBicmFuZCBleHBvc3VyZVwiIG5hbWU9XCJ0eXBlXCI+XG4gICAgICAgICAgU2ltcGxlIGJyYW5kIGV4cG9zdXJlXG4gICAgICAgIDwvZWwtY2hlY2tib3g+XG4gICAgICA8L2VsLWNoZWNrYm94LWdyb3VwPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJSZXNvdXJjZXNcIiBwcm9wPVwicmVzb3VyY2VcIj5cbiAgICAgIDxlbC1yYWRpby1ncm91cCB2LW1vZGVsPVwicnVsZUZvcm0ucmVzb3VyY2VcIj5cbiAgICAgICAgPGVsLXJhZGlvIHZhbHVlPVwiU3BvbnNvcnNoaXBcIj5TcG9uc29yc2hpcDwvZWwtcmFkaW8+XG4gICAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cIlZlbnVlXCI+VmVudWU8L2VsLXJhZGlvPlxuICAgICAgPC9lbC1yYWRpby1ncm91cD5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiQWN0aXZpdHkgZm9ybVwiIHByb3A9XCJkZXNjXCI+XG4gICAgICA8ZWwtaW5wdXQgdi1tb2RlbD1cInJ1bGVGb3JtLmRlc2NcIiB0eXBlPVwidGV4dGFyZWFcIiAvPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwic3VibWl0Rm9ybShydWxlRm9ybVJlZilcIj5cbiAgICAgICAgQ3JlYXRlXG4gICAgICA8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwicmVzZXRGb3JtKHJ1bGVGb3JtUmVmKVwiPlJlc2V0PC9lbC1idXR0b24+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gIDwvZWwtZm9ybT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWFjdGl2ZSwgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IEZvcm1JbnN0YW5jZSwgRm9ybVJ1bGVzIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbnRlcmZhY2UgUnVsZUZvcm0ge1xuICBuYW1lOiBzdHJpbmdcbiAgcmVnaW9uOiBzdHJpbmdcbiAgY291bnQ6IHN0cmluZ1xuICBkYXRlMTogc3RyaW5nXG4gIGRhdGUyOiBzdHJpbmdcbiAgZGVsaXZlcnk6IGJvb2xlYW5cbiAgbG9jYXRpb246IHN0cmluZ1xuICB0eXBlOiBzdHJpbmdbXVxuICByZXNvdXJjZTogc3RyaW5nXG4gIGRlc2M6IHN0cmluZ1xufVxuXG5jb25zdCBydWxlRm9ybVJlZiA9IHJlZjxGb3JtSW5zdGFuY2U+KClcbmNvbnN0IHJ1bGVGb3JtID0gcmVhY3RpdmU8UnVsZUZvcm0+KHtcbiAgbmFtZTogJ0hlbGxvJyxcbiAgcmVnaW9uOiAnJyxcbiAgY291bnQ6ICcnLFxuICBkYXRlMTogJycsXG4gIGRhdGUyOiAnJyxcbiAgZGVsaXZlcnk6IGZhbHNlLFxuICBsb2NhdGlvbjogJycsXG4gIHR5cGU6IFtdLFxuICByZXNvdXJjZTogJycsXG4gIGRlc2M6ICcnLFxufSlcblxuY29uc3QgbG9jYXRpb25PcHRpb25zID0gWydIb21lJywgJ0NvbXBhbnknLCAnU2Nob29sJ11cblxuY29uc3QgcnVsZXMgPSByZWFjdGl2ZTxGb3JtUnVsZXM8UnVsZUZvcm0+Pih7XG4gIG5hbWU6IFtcbiAgICB7IHJlcXVpcmVkOiB0cnVlLCBtZXNzYWdlOiAnUGxlYXNlIGlucHV0IEFjdGl2aXR5IG5hbWUnLCB0cmlnZ2VyOiAnYmx1cicgfSxcbiAgICB7IG1pbjogMywgbWF4OiA1LCBtZXNzYWdlOiAnTGVuZ3RoIHNob3VsZCBiZSAzIHRvIDUnLCB0cmlnZ2VyOiAnYmx1cicgfSxcbiAgXSxcbiAgcmVnaW9uOiBbXG4gICAge1xuICAgICAgcmVxdWlyZWQ6IHRydWUsXG4gICAgICBtZXNzYWdlOiAnUGxlYXNlIHNlbGVjdCBBY3Rpdml0eSB6b25lJyxcbiAgICAgIHRyaWdnZXI6ICdjaGFuZ2UnLFxuICAgIH0sXG4gIF0sXG4gIGNvdW50OiBbXG4gICAge1xuICAgICAgcmVxdWlyZWQ6IHRydWUsXG4gICAgICBtZXNzYWdlOiAnUGxlYXNlIHNlbGVjdCBBY3Rpdml0eSBjb3VudCcsXG4gICAgICB0cmlnZ2VyOiAnY2hhbmdlJyxcbiAgICB9LFxuICBdLFxuICBkYXRlMTogW1xuICAgIHtcbiAgICAgIHR5cGU6ICdkYXRlJyxcbiAgICAgIHJlcXVpcmVkOiB0cnVlLFxuICAgICAgbWVzc2FnZTogJ1BsZWFzZSBwaWNrIGEgZGF0ZScsXG4gICAgICB0cmlnZ2VyOiAnY2hhbmdlJyxcbiAgICB9LFxuICBdLFxuICBkYXRlMjogW1xuICAgIHtcbiAgICAgIHR5cGU6ICdkYXRlJyxcbiAgICAgIHJlcXVpcmVkOiB0cnVlLFxuICAgICAgbWVzc2FnZTogJ1BsZWFzZSBwaWNrIGEgdGltZScsXG4gICAgICB0cmlnZ2VyOiAnY2hhbmdlJyxcbiAgICB9LFxuICBdLFxuICBsb2NhdGlvbjogW1xuICAgIHtcbiAgICAgIHJlcXVpcmVkOiB0cnVlLFxuICAgICAgbWVzc2FnZTogJ1BsZWFzZSBzZWxlY3QgYSBsb2NhdGlvbicsXG4gICAgICB0cmlnZ2VyOiAnY2hhbmdlJyxcbiAgICB9LFxuICBdLFxuICB0eXBlOiBbXG4gICAge1xuICAgICAgdHlwZTogJ2FycmF5JyxcbiAgICAgIHJlcXVpcmVkOiB0cnVlLFxuICAgICAgbWVzc2FnZTogJ1BsZWFzZSBzZWxlY3QgYXQgbGVhc3Qgb25lIGFjdGl2aXR5IHR5cGUnLFxuICAgICAgdHJpZ2dlcjogJ2NoYW5nZScsXG4gICAgfSxcbiAgXSxcbiAgcmVzb3VyY2U6IFtcbiAgICB7XG4gICAgICByZXF1aXJlZDogdHJ1ZSxcbiAgICAgIG1lc3NhZ2U6ICdQbGVhc2Ugc2VsZWN0IGFjdGl2aXR5IHJlc291cmNlJyxcbiAgICAgIHRyaWdnZXI6ICdjaGFuZ2UnLFxuICAgIH0sXG4gIF0sXG4gIGRlc2M6IFtcbiAgICB7IHJlcXVpcmVkOiB0cnVlLCBtZXNzYWdlOiAnUGxlYXNlIGlucHV0IGFjdGl2aXR5IGZvcm0nLCB0cmlnZ2VyOiAnYmx1cicgfSxcbiAgXSxcbn0pXG5cbmNvbnN0IHN1Ym1pdEZvcm0gPSBhc3luYyAoZm9ybUVsOiBGb3JtSW5zdGFuY2UgfCB1bmRlZmluZWQpID0+IHtcbiAgaWYgKCFmb3JtRWwpIHJldHVyblxuICBhd2FpdCBmb3JtRWwudmFsaWRhdGUoKHZhbGlkLCBmaWVsZHMpID0+IHtcbiAgICBpZiAodmFsaWQpIHtcbiAgICAgIGNvbnNvbGUubG9nKCdzdWJtaXQhJylcbiAgICB9IGVsc2Uge1xuICAgICAgY29uc29sZS5sb2coJ2Vycm9yIHN1Ym1pdCEnLCBmaWVsZHMpXG4gICAgfVxuICB9KVxufVxuXG5jb25zdCByZXNldEZvcm0gPSAoZm9ybUVsOiBGb3JtSW5zdGFuY2UgfCB1bmRlZmluZWQpID0+IHtcbiAgaWYgKCFmb3JtRWwpIHJldHVyblxuICBmb3JtRWwucmVzZXRGaWVsZHMoKVxufVxuXG5jb25zdCBvcHRpb25zID0gQXJyYXkuZnJvbSh7IGxlbmd0aDogMTAwMDAgfSkubWFwKChfLCBpZHgpID0+ICh7XG4gIHZhbHVlOiBgJHtpZHggKyAxfWAsXG4gIGxhYmVsOiBgJHtpZHggKyAxfWAsXG59KSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/form/validation.vue)_

vue

```
<template>
  <el-form
    ref="ruleFormRef"
    style="max-width: 600px"
    :model="ruleForm"
    :rules="rules"
    label-width="auto"
  >
    <el-form-item label="Activity name" prop="name">
      <el-input v-model="ruleForm.name" />
    </el-form-item>
    <el-form-item label="Activity zone" prop="region">
      <el-select v-model="ruleForm.region" placeholder="Activity zone">
        <el-option label="Zone one" value="shanghai" />
        <el-option label="Zone two" value="beijing" />
      </el-select>
    </el-form-item>
    <el-form-item label="Activity count" prop="count">
      <el-select-v2
        v-model="ruleForm.count"
        placeholder="Activity count"
        :options="options"
      />
    </el-form-item>
    <el-form-item label="Activity time" required>
      <el-col :span="11">
        <el-form-item prop="date1">
          <el-date-picker
            v-model="ruleForm.date1"
            type="date"
            aria-label="Pick a date"
            placeholder="Pick a date"
            style="width: 100%"
          />
        </el-form-item>
      </el-col>
      <el-col class="text-center" :span="2">
        <span class="text-gray-500">-</span>
      </el-col>
      <el-col :span="11">
        <el-form-item prop="date2">
          <el-time-picker
            v-model="ruleForm.date2"
            aria-label="Pick a time"
            placeholder="Pick a time"
            style="width: 100%"
          />
        </el-form-item>
      </el-col>
    </el-form-item>
    <el-form-item label="Instant delivery" prop="delivery">
      <el-switch v-model="ruleForm.delivery" />
    </el-form-item>
    <el-form-item label="Activity location" prop="location">
      <el-segmented v-model="ruleForm.location" :options="locationOptions" />
    </el-form-item>
    <el-form-item label="Activity type" prop="type">
      <el-checkbox-group v-model="ruleForm.type">
        <el-checkbox value="Online activities" name="type">
          Online activities
        </el-checkbox>
        <el-checkbox value="Promotion activities" name="type">
          Promotion activities
        </el-checkbox>
        <el-checkbox value="Offline activities" name="type">
          Offline activities
        </el-checkbox>
        <el-checkbox value="Simple brand exposure" name="type">
          Simple brand exposure
        </el-checkbox>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item label="Resources" prop="resource">
      <el-radio-group v-model="ruleForm.resource">
        <el-radio value="Sponsorship">Sponsorship</el-radio>
        <el-radio value="Venue">Venue</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="Activity form" prop="desc">
      <el-input v-model="ruleForm.desc" type="textarea" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)">
        Create
      </el-button>
      <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

import type { FormInstance, FormRules } from 'element-plus'

interface RuleForm {
  name: string
  region: string
  count: string
  date1: string
  date2: string
  delivery: boolean
  location: string
  type: string[]
  resource: string
  desc: string
}

const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive<RuleForm>({
  name: 'Hello',
  region: '',
  count: '',
  date1: '',
  date2: '',
  delivery: false,
  location: '',
  type: [],
  resource: '',
  desc: '',
})

const locationOptions = ['Home', 'Company', 'School']

const rules = reactive<FormRules<RuleForm>>({
  name: [
    { required: true, message: 'Please input Activity name', trigger: 'blur' },
    { min: 3, max: 5, message: 'Length should be 3 to 5', trigger: 'blur' },
  ],
  region: [
    {
      required: true,
      message: 'Please select Activity zone',
      trigger: 'change',
    },
  ],
  count: [
    {
      required: true,
      message: 'Please select Activity count',
      trigger: 'change',
    },
  ],
  date1: [
    {
      type: 'date',
      required: true,
      message: 'Please pick a date',
      trigger: 'change',
    },
  ],
  date2: [
    {
      type: 'date',
      required: true,
      message: 'Please pick a time',
      trigger: 'change',
    },
  ],
  location: [
    {
      required: true,
      message: 'Please select a location',
      trigger: 'change',
    },
  ],
  type: [
    {
      type: 'array',
      required: true,
      message: 'Please select at least one activity type',
      trigger: 'change',
    },
  ],
  resource: [
    {
      required: true,
      message: 'Please select activity resource',
      trigger: 'change',
    },
  ],
  desc: [
    { required: true, message: 'Please input activity form', trigger: 'blur' },
  ],
})

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      console.log('submit!')
    } else {
      console.log('error submit!', fields)
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

const options = Array.from({ length: 10000 }).map((_, idx) => ({
  value: `${idx + 1}`,
  label: `${idx + 1}`,
}))
</script>
```

隐藏源代码

## 自定义校验规则 [​](#自定义校验规则)

这个例子中展示了如何使用自定义验证规则来完成密码的二次验证。

本例还使用`status-icon`属性为输入框添加了表示校验结果的反馈图标。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZm9ybVxuICAgIHJlZj1cInJ1bGVGb3JtUmVmXCJcbiAgICBzdHlsZT1cIm1heC13aWR0aDogNjAwcHhcIlxuICAgIDptb2RlbD1cInJ1bGVGb3JtXCJcbiAgICBzdGF0dXMtaWNvblxuICAgIDpydWxlcz1cInJ1bGVzXCJcbiAgICBsYWJlbC13aWR0aD1cImF1dG9cIlxuICAgIGNsYXNzPVwiZGVtby1ydWxlRm9ybVwiXG4gID5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiUGFzc3dvcmRcIiBwcm9wPVwicGFzc1wiPlxuICAgICAgPGVsLWlucHV0IHYtbW9kZWw9XCJydWxlRm9ybS5wYXNzXCIgdHlwZT1cInBhc3N3b3JkXCIgYXV0b2NvbXBsZXRlPVwib2ZmXCIgLz5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiQ29uZmlybVwiIHByb3A9XCJjaGVja1Bhc3NcIj5cbiAgICAgIDxlbC1pbnB1dFxuICAgICAgICB2LW1vZGVsPVwicnVsZUZvcm0uY2hlY2tQYXNzXCJcbiAgICAgICAgdHlwZT1cInBhc3N3b3JkXCJcbiAgICAgICAgYXV0b2NvbXBsZXRlPVwib2ZmXCJcbiAgICAgIC8+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkFnZVwiIHByb3A9XCJhZ2VcIj5cbiAgICAgIDxlbC1pbnB1dCB2LW1vZGVsLm51bWJlcj1cInJ1bGVGb3JtLmFnZVwiIC8+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbT5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBAY2xpY2s9XCJzdWJtaXRGb3JtKHJ1bGVGb3JtUmVmKVwiPlxuICAgICAgICBTdWJtaXRcbiAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJyZXNldEZvcm0ocnVsZUZvcm1SZWYpXCI+UmVzZXQ8L2VsLWJ1dHRvbj5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgPC9lbC1mb3JtPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlYWN0aXZlLCByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgRm9ybUluc3RhbmNlLCBGb3JtUnVsZXMgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHJ1bGVGb3JtUmVmID0gcmVmPEZvcm1JbnN0YW5jZT4oKVxuXG5jb25zdCBjaGVja0FnZSA9IChydWxlOiBhbnksIHZhbHVlOiBhbnksIGNhbGxiYWNrOiBhbnkpID0+IHtcbiAgaWYgKCF2YWx1ZSkge1xuICAgIHJldHVybiBjYWxsYmFjayhuZXcgRXJyb3IoJ1BsZWFzZSBpbnB1dCB0aGUgYWdlJykpXG4gIH1cbiAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgaWYgKCFOdW1iZXIuaXNJbnRlZ2VyKHZhbHVlKSkge1xuICAgICAgY2FsbGJhY2sobmV3IEVycm9yKCdQbGVhc2UgaW5wdXQgZGlnaXRzJykpXG4gICAgfSBlbHNlIHtcbiAgICAgIGlmICh2YWx1ZSA8IDE4KSB7XG4gICAgICAgIGNhbGxiYWNrKG5ldyBFcnJvcignQWdlIG11c3QgYmUgZ3JlYXRlciB0aGFuIDE4JykpXG4gICAgICB9IGVsc2Uge1xuICAgICAgICBjYWxsYmFjaygpXG4gICAgICB9XG4gICAgfVxuICB9LCAxMDAwKVxufVxuXG5jb25zdCB2YWxpZGF0ZVBhc3MgPSAocnVsZTogYW55LCB2YWx1ZTogYW55LCBjYWxsYmFjazogYW55KSA9PiB7XG4gIGlmICh2YWx1ZSA9PT0gJycpIHtcbiAgICBjYWxsYmFjayhuZXcgRXJyb3IoJ1BsZWFzZSBpbnB1dCB0aGUgcGFzc3dvcmQnKSlcbiAgfSBlbHNlIHtcbiAgICBpZiAocnVsZUZvcm0uY2hlY2tQYXNzICE9PSAnJykge1xuICAgICAgaWYgKCFydWxlRm9ybVJlZi52YWx1ZSkgcmV0dXJuXG4gICAgICBydWxlRm9ybVJlZi52YWx1ZS52YWxpZGF0ZUZpZWxkKCdjaGVja1Bhc3MnKVxuICAgIH1cbiAgICBjYWxsYmFjaygpXG4gIH1cbn1cbmNvbnN0IHZhbGlkYXRlUGFzczIgPSAocnVsZTogYW55LCB2YWx1ZTogYW55LCBjYWxsYmFjazogYW55KSA9PiB7XG4gIGlmICh2YWx1ZSA9PT0gJycpIHtcbiAgICBjYWxsYmFjayhuZXcgRXJyb3IoJ1BsZWFzZSBpbnB1dCB0aGUgcGFzc3dvcmQgYWdhaW4nKSlcbiAgfSBlbHNlIGlmICh2YWx1ZSAhPT0gcnVsZUZvcm0ucGFzcykge1xuICAgIGNhbGxiYWNrKG5ldyBFcnJvcihcIlR3byBpbnB1dHMgZG9uJ3QgbWF0Y2ghXCIpKVxuICB9IGVsc2Uge1xuICAgIGNhbGxiYWNrKClcbiAgfVxufVxuXG5jb25zdCBydWxlRm9ybSA9IHJlYWN0aXZlKHtcbiAgcGFzczogJycsXG4gIGNoZWNrUGFzczogJycsXG4gIGFnZTogJycsXG59KVxuXG5jb25zdCBydWxlcyA9IHJlYWN0aXZlPEZvcm1SdWxlczx0eXBlb2YgcnVsZUZvcm0+Pih7XG4gIHBhc3M6IFt7IHZhbGlkYXRvcjogdmFsaWRhdGVQYXNzLCB0cmlnZ2VyOiAnYmx1cicgfV0sXG4gIGNoZWNrUGFzczogW3sgdmFsaWRhdG9yOiB2YWxpZGF0ZVBhc3MyLCB0cmlnZ2VyOiAnYmx1cicgfV0sXG4gIGFnZTogW3sgdmFsaWRhdG9yOiBjaGVja0FnZSwgdHJpZ2dlcjogJ2JsdXInIH1dLFxufSlcblxuY29uc3Qgc3VibWl0Rm9ybSA9IChmb3JtRWw6IEZvcm1JbnN0YW5jZSB8IHVuZGVmaW5lZCkgPT4ge1xuICBpZiAoIWZvcm1FbCkgcmV0dXJuXG4gIGZvcm1FbC52YWxpZGF0ZSgodmFsaWQpID0+IHtcbiAgICBpZiAodmFsaWQpIHtcbiAgICAgIGNvbnNvbGUubG9nKCdzdWJtaXQhJylcbiAgICB9IGVsc2Uge1xuICAgICAgY29uc29sZS5sb2coJ2Vycm9yIHN1Ym1pdCEnKVxuICAgIH1cbiAgfSlcbn1cblxuY29uc3QgcmVzZXRGb3JtID0gKGZvcm1FbDogRm9ybUluc3RhbmNlIHwgdW5kZWZpbmVkKSA9PiB7XG4gIGlmICghZm9ybUVsKSByZXR1cm5cbiAgZm9ybUVsLnJlc2V0RmllbGRzKClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/form/custom-validation.vue)_

vue

```
<template>
  <el-form
    ref="ruleFormRef"
    style="max-width: 600px"
    :model="ruleForm"
    status-icon
    :rules="rules"
    label-width="auto"
    class="demo-ruleForm"
  >
    <el-form-item label="Password" prop="pass">
      <el-input v-model="ruleForm.pass" type="password" autocomplete="off" />
    </el-form-item>
    <el-form-item label="Confirm" prop="checkPass">
      <el-input
        v-model="ruleForm.checkPass"
        type="password"
        autocomplete="off"
      />
    </el-form-item>
    <el-form-item label="Age" prop="age">
      <el-input v-model.number="ruleForm.age" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)">
        Submit
      </el-button>
      <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

import type { FormInstance, FormRules } from 'element-plus'

const ruleFormRef = ref<FormInstance>()

const checkAge = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('Please input the age'))
  }
  setTimeout(() => {
    if (!Number.isInteger(value)) {
      callback(new Error('Please input digits'))
    } else {
      if (value < 18) {
        callback(new Error('Age must be greater than 18'))
      } else {
        callback()
      }
    }
  }, 1000)
}

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Please input the password'))
  } else {
    if (ruleForm.checkPass !== '') {
      if (!ruleFormRef.value) return
      ruleFormRef.value.validateField('checkPass')
    }
    callback()
  }
}
const validatePass2 = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Please input the password again'))
  } else if (value !== ruleForm.pass) {
    callback(new Error("Two inputs don't match!"))
  } else {
    callback()
  }
}

const ruleForm = reactive({
  pass: '',
  checkPass: '',
  age: '',
})

const rules = reactive<FormRules<typeof ruleForm>>({
  pass: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
  age: [{ validator: checkAge, trigger: 'blur' }],
})

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
    } else {
      console.log('error submit!')
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>
```

隐藏源代码

TIP

自定义的校验回调函数必须被调用。 校验规则参见 [async-validator](https://github.com/yiminghe/async-validator)

## 添加/删除表单项 [​](#添加-删除表单项)

除了一次通过表单组件上的所有验证规则外. 您也可以动态地通过验证规则或删除单个表单字段的规则。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZm9ybVxuICAgIHJlZj1cImZvcm1SZWZcIlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOm1vZGVsPVwiZHluYW1pY1ZhbGlkYXRlRm9ybVwiXG4gICAgbGFiZWwtd2lkdGg9XCJhdXRvXCJcbiAgICBjbGFzcz1cImRlbW8tZHluYW1pY1wiXG4gID5cbiAgICA8ZWwtZm9ybS1pdGVtXG4gICAgICBwcm9wPVwiZW1haWxcIlxuICAgICAgbGFiZWw9XCJFbWFpbFwiXG4gICAgICA6cnVsZXM9XCJbXG4gICAgICAgIHtcbiAgICAgICAgICByZXF1aXJlZDogdHJ1ZSxcbiAgICAgICAgICBtZXNzYWdlOiAnUGxlYXNlIGlucHV0IGVtYWlsIGFkZHJlc3MnLFxuICAgICAgICAgIHRyaWdnZXI6ICdibHVyJyxcbiAgICAgICAgfSxcbiAgICAgICAge1xuICAgICAgICAgIHR5cGU6ICdlbWFpbCcsXG4gICAgICAgICAgbWVzc2FnZTogJ1BsZWFzZSBpbnB1dCBjb3JyZWN0IGVtYWlsIGFkZHJlc3MnLFxuICAgICAgICAgIHRyaWdnZXI6IFsnYmx1cicsICdjaGFuZ2UnXSxcbiAgICAgICAgfSxcbiAgICAgIF1cIlxuICAgID5cbiAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwiZHluYW1pY1ZhbGlkYXRlRm9ybS5lbWFpbFwiIC8+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbVxuICAgICAgdi1mb3I9XCIoZG9tYWluLCBpbmRleCkgaW4gZHluYW1pY1ZhbGlkYXRlRm9ybS5kb21haW5zXCJcbiAgICAgIDprZXk9XCJkb21haW4ua2V5XCJcbiAgICAgIDpsYWJlbD1cIidEb21haW4nICsgaW5kZXhcIlxuICAgICAgOnByb3A9XCInZG9tYWlucy4nICsgaW5kZXggKyAnLnZhbHVlJ1wiXG4gICAgICA6cnVsZXM9XCJ7XG4gICAgICAgIHJlcXVpcmVkOiB0cnVlLFxuICAgICAgICBtZXNzYWdlOiAnZG9tYWluIGNhbiBub3QgYmUgbnVsbCcsXG4gICAgICAgIHRyaWdnZXI6ICdibHVyJyxcbiAgICAgIH1cIlxuICAgID5cbiAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwiZG9tYWluLnZhbHVlXCIgLz5cbiAgICAgIDxlbC1idXR0b24gY2xhc3M9XCJtdC0yXCIgQGNsaWNrLnByZXZlbnQ9XCJyZW1vdmVEb21haW4oZG9tYWluKVwiPlxuICAgICAgICBEZWxldGVcbiAgICAgIDwvZWwtYnV0dG9uPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwic3VibWl0Rm9ybShmb3JtUmVmKVwiPlN1Ym1pdDwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbiBAY2xpY2s9XCJhZGREb21haW5cIj5OZXcgZG9tYWluPC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIEBjbGljaz1cInJlc2V0Rm9ybShmb3JtUmVmKVwiPlJlc2V0PC9lbC1idXR0b24+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gIDwvZWwtZm9ybT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWFjdGl2ZSwgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IEZvcm1JbnN0YW5jZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgZm9ybVJlZiA9IHJlZjxGb3JtSW5zdGFuY2U+KClcbmNvbnN0IGR5bmFtaWNWYWxpZGF0ZUZvcm0gPSByZWFjdGl2ZTx7XG4gIGRvbWFpbnM6IERvbWFpbkl0ZW1bXVxuICBlbWFpbDogc3RyaW5nXG59Pih7XG4gIGRvbWFpbnM6IFtcbiAgICB7XG4gICAgICBrZXk6IDEsXG4gICAgICB2YWx1ZTogJycsXG4gICAgfSxcbiAgXSxcbiAgZW1haWw6ICcnLFxufSlcblxuaW50ZXJmYWNlIERvbWFpbkl0ZW0ge1xuICBrZXk6IG51bWJlclxuICB2YWx1ZTogc3RyaW5nXG59XG5cbmNvbnN0IHJlbW92ZURvbWFpbiA9IChpdGVtOiBEb21haW5JdGVtKSA9PiB7XG4gIGNvbnN0IGluZGV4ID0gZHluYW1pY1ZhbGlkYXRlRm9ybS5kb21haW5zLmluZGV4T2YoaXRlbSlcbiAgaWYgKGluZGV4ICE9PSAtMSkge1xuICAgIGR5bmFtaWNWYWxpZGF0ZUZvcm0uZG9tYWlucy5zcGxpY2UoaW5kZXgsIDEpXG4gIH1cbn1cblxuY29uc3QgYWRkRG9tYWluID0gKCkgPT4ge1xuICBkeW5hbWljVmFsaWRhdGVGb3JtLmRvbWFpbnMucHVzaCh7XG4gICAga2V5OiBEYXRlLm5vdygpLFxuICAgIHZhbHVlOiAnJyxcbiAgfSlcbn1cblxuY29uc3Qgc3VibWl0Rm9ybSA9IChmb3JtRWw6IEZvcm1JbnN0YW5jZSB8IHVuZGVmaW5lZCkgPT4ge1xuICBpZiAoIWZvcm1FbCkgcmV0dXJuXG4gIGZvcm1FbC52YWxpZGF0ZSgodmFsaWQpID0+IHtcbiAgICBpZiAodmFsaWQpIHtcbiAgICAgIGNvbnNvbGUubG9nKCdzdWJtaXQhJylcbiAgICB9IGVsc2Uge1xuICAgICAgY29uc29sZS5sb2coJ2Vycm9yIHN1Ym1pdCEnKVxuICAgIH1cbiAgfSlcbn1cblxuY29uc3QgcmVzZXRGb3JtID0gKGZvcm1FbDogRm9ybUluc3RhbmNlIHwgdW5kZWZpbmVkKSA9PiB7XG4gIGlmICghZm9ybUVsKSByZXR1cm5cbiAgZm9ybUVsLnJlc2V0RmllbGRzKClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/form/form-items.vue)_

vue

```
<template>
  <el-form
    ref="formRef"
    style="max-width: 600px"
    :model="dynamicValidateForm"
    label-width="auto"
    class="demo-dynamic"
  >
    <el-form-item
      prop="email"
      label="Email"
      :rules="[
        {
          required: true,
          message: 'Please input email address',
          trigger: 'blur',
        },
        {
          type: 'email',
          message: 'Please input correct email address',
          trigger: ['blur', 'change'],
        },
      ]"
    >
      <el-input v-model="dynamicValidateForm.email" />
    </el-form-item>
    <el-form-item
      v-for="(domain, index) in dynamicValidateForm.domains"
      :key="domain.key"
      :label="'Domain' + index"
      :prop="'domains.' + index + '.value'"
      :rules="{
        required: true,
        message: 'domain can not be null',
        trigger: 'blur',
      }"
    >
      <el-input v-model="domain.value" />
      <el-button class="mt-2" @click.prevent="removeDomain(domain)">
        Delete
      </el-button>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(formRef)">Submit</el-button>
      <el-button @click="addDomain">New domain</el-button>
      <el-button @click="resetForm(formRef)">Reset</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

import type { FormInstance } from 'element-plus'

const formRef = ref<FormInstance>()
const dynamicValidateForm = reactive<{
  domains: DomainItem[]
  email: string
}>({
  domains: [
    {
      key: 1,
      value: '',
    },
  ],
  email: '',
})

interface DomainItem {
  key: number
  value: string
}

const removeDomain = (item: DomainItem) => {
  const index = dynamicValidateForm.domains.indexOf(item)
  if (index !== -1) {
    dynamicValidateForm.domains.splice(index, 1)
  }
}

const addDomain = () => {
  dynamicValidateForm.domains.push({
    key: Date.now(),
    value: '',
  })
}

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
    } else {
      console.log('error submit!')
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>
```

隐藏源代码

## 数字类型验证 [​](#数字类型验证)

数字类型的验证需要在 `v-model` 处加上 `.number` 的修饰符，这是 Vue 自身提供的用于将绑定值转化为 number 类型的修饰符。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZm9ybVxuICAgIHJlZj1cImZvcm1SZWZcIlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOm1vZGVsPVwibnVtYmVyVmFsaWRhdGVGb3JtXCJcbiAgICBsYWJlbC13aWR0aD1cImF1dG9cIlxuICAgIGNsYXNzPVwiZGVtby1ydWxlRm9ybVwiXG4gID5cbiAgICA8ZWwtZm9ybS1pdGVtXG4gICAgICBsYWJlbD1cImFnZVwiXG4gICAgICBwcm9wPVwiYWdlXCJcbiAgICAgIDpydWxlcz1cIltcbiAgICAgICAgeyByZXF1aXJlZDogdHJ1ZSwgbWVzc2FnZTogJ2FnZSBpcyByZXF1aXJlZCcgfSxcbiAgICAgICAgeyB0eXBlOiAnbnVtYmVyJywgbWVzc2FnZTogJ2FnZSBtdXN0IGJlIGEgbnVtYmVyJyB9LFxuICAgICAgXVwiXG4gICAgPlxuICAgICAgPGVsLWlucHV0XG4gICAgICAgIHYtbW9kZWwubnVtYmVyPVwibnVtYmVyVmFsaWRhdGVGb3JtLmFnZVwiXG4gICAgICAgIHR5cGU9XCJ0ZXh0XCJcbiAgICAgICAgYXV0b2NvbXBsZXRlPVwib2ZmXCJcbiAgICAgIC8+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbT5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBAY2xpY2s9XCJzdWJtaXRGb3JtKGZvcm1SZWYpXCI+U3VibWl0PC9lbC1idXR0b24+XG4gICAgICA8ZWwtYnV0dG9uIEBjbGljaz1cInJlc2V0Rm9ybShmb3JtUmVmKVwiPlJlc2V0PC9lbC1idXR0b24+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gIDwvZWwtZm9ybT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWFjdGl2ZSwgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IEZvcm1JbnN0YW5jZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgZm9ybVJlZiA9IHJlZjxGb3JtSW5zdGFuY2U+KClcblxuY29uc3QgbnVtYmVyVmFsaWRhdGVGb3JtID0gcmVhY3RpdmUoe1xuICBhZ2U6ICcnLFxufSlcblxuY29uc3Qgc3VibWl0Rm9ybSA9IChmb3JtRWw6IEZvcm1JbnN0YW5jZSB8IHVuZGVmaW5lZCkgPT4ge1xuICBpZiAoIWZvcm1FbCkgcmV0dXJuXG4gIGZvcm1FbC52YWxpZGF0ZSgodmFsaWQpID0+IHtcbiAgICBpZiAodmFsaWQpIHtcbiAgICAgIGNvbnNvbGUubG9nKCdzdWJtaXQhJylcbiAgICB9IGVsc2Uge1xuICAgICAgY29uc29sZS5sb2coJ2Vycm9yIHN1Ym1pdCEnKVxuICAgIH1cbiAgfSlcbn1cblxuY29uc3QgcmVzZXRGb3JtID0gKGZvcm1FbDogRm9ybUluc3RhbmNlIHwgdW5kZWZpbmVkKSA9PiB7XG4gIGlmICghZm9ybUVsKSByZXR1cm5cbiAgZm9ybUVsLnJlc2V0RmllbGRzKClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/form/number-validate.vue)_

vue

```
<template>
  <el-form
    ref="formRef"
    style="max-width: 600px"
    :model="numberValidateForm"
    label-width="auto"
    class="demo-ruleForm"
  >
    <el-form-item
      label="age"
      prop="age"
      :rules="[
        { required: true, message: 'age is required' },
        { type: 'number', message: 'age must be a number' },
      ]"
    >
      <el-input
        v-model.number="numberValidateForm.age"
        type="text"
        autocomplete="off"
      />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(formRef)">Submit</el-button>
      <el-button @click="resetForm(formRef)">Reset</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

import type { FormInstance } from 'element-plus'

const formRef = ref<FormInstance>()

const numberValidateForm = reactive({
  age: '',
})

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
    } else {
      console.log('error submit!')
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>
```

隐藏源代码

TIP

当一个 `el-form-item` 嵌套在另一个 `el-form-item` 中时，其标签宽度将为 `0`。 如果需要可以为 `el-form-item` 单独设置 `label-width` 属性。

## 尺寸控制 [​](#尺寸控制)

表单中的所有子组件都继承了该表单的 `size` 属性。 同样，form-item 也有一个 `size` 属性。

如果希望某个表单项或某个表单组件的尺寸不同于 Form 上的 `size` 属性，直接为这个表单项或表单组件设置自己的 size 属性即可。

largedefaultsmall

LeftRightTop

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1yYWRpby1ncm91cCB2LW1vZGVsPVwic2l6ZVwiIGFyaWEtbGFiZWw9XCJzaXplIGNvbnRyb2xcIj5cbiAgICAgIDxlbC1yYWRpby1idXR0b24gdmFsdWU9XCJsYXJnZVwiPmxhcmdlPC9lbC1yYWRpby1idXR0b24+XG4gICAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwiZGVmYXVsdFwiPmRlZmF1bHQ8L2VsLXJhZGlvLWJ1dHRvbj5cbiAgICAgIDxlbC1yYWRpby1idXR0b24gdmFsdWU9XCJzbWFsbFwiPnNtYWxsPC9lbC1yYWRpby1idXR0b24+XG4gICAgPC9lbC1yYWRpby1ncm91cD5cbiAgICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cImxhYmVsUG9zaXRpb25cIiBhcmlhLWxhYmVsPVwicG9zaXRpb24gY29udHJvbFwiPlxuICAgICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cImxlZnRcIj5MZWZ0PC9lbC1yYWRpby1idXR0b24+XG4gICAgICA8ZWwtcmFkaW8tYnV0dG9uIHZhbHVlPVwicmlnaHRcIj5SaWdodDwvZWwtcmFkaW8tYnV0dG9uPlxuICAgICAgPGVsLXJhZGlvLWJ1dHRvbiB2YWx1ZT1cInRvcFwiPlRvcDwvZWwtcmFkaW8tYnV0dG9uPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDwvZGl2PlxuICA8YnIgLz5cbiAgPGVsLWZvcm1cbiAgICBzdHlsZT1cIm1heC13aWR0aDogNjAwcHhcIlxuICAgIDptb2RlbD1cInNpemVGb3JtXCJcbiAgICBsYWJlbC13aWR0aD1cImF1dG9cIlxuICAgIDpsYWJlbC1wb3NpdGlvbj1cImxhYmVsUG9zaXRpb25cIlxuICAgIDpzaXplPVwic2l6ZVwiXG4gID5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiQWN0aXZpdHkgbmFtZVwiPlxuICAgICAgPGVsLWlucHV0IHYtbW9kZWw9XCJzaXplRm9ybS5uYW1lXCIgLz5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiQWN0aXZpdHkgem9uZVwiPlxuICAgICAgPGVsLXNlbGVjdFxuICAgICAgICB2LW1vZGVsPVwic2l6ZUZvcm0ucmVnaW9uXCJcbiAgICAgICAgcGxhY2Vob2xkZXI9XCJwbGVhc2Ugc2VsZWN0IHlvdXIgem9uZVwiXG4gICAgICA+XG4gICAgICAgIDxlbC1vcHRpb24gbGFiZWw9XCJab25lIG9uZVwiIHZhbHVlPVwic2hhbmdoYWlcIiAvPlxuICAgICAgICA8ZWwtb3B0aW9uIGxhYmVsPVwiWm9uZSB0d29cIiB2YWx1ZT1cImJlaWppbmdcIiAvPlxuICAgICAgPC9lbC1zZWxlY3Q+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkFjdGl2aXR5IHRpbWVcIj5cbiAgICAgIDxlbC1jb2wgOnNwYW49XCIxMVwiPlxuICAgICAgICA8ZWwtZGF0ZS1waWNrZXJcbiAgICAgICAgICB2LW1vZGVsPVwic2l6ZUZvcm0uZGF0ZTFcIlxuICAgICAgICAgIHR5cGU9XCJkYXRlXCJcbiAgICAgICAgICBhcmlhLWxhYmVsPVwiUGljayBhIGRhdGVcIlxuICAgICAgICAgIHBsYWNlaG9sZGVyPVwiUGljayBhIGRhdGVcIlxuICAgICAgICAgIHN0eWxlPVwid2lkdGg6IDEwMCVcIlxuICAgICAgICAvPlxuICAgICAgPC9lbC1jb2w+XG4gICAgICA8ZWwtY29sIGNsYXNzPVwidGV4dC1jZW50ZXJcIiA6c3Bhbj1cIjFcIiBzdHlsZT1cIm1hcmdpbjogMCAwLjVyZW1cIj4tPC9lbC1jb2w+XG4gICAgICA8ZWwtY29sIDpzcGFuPVwiMTFcIj5cbiAgICAgICAgPGVsLXRpbWUtcGlja2VyXG4gICAgICAgICAgdi1tb2RlbD1cInNpemVGb3JtLmRhdGUyXCJcbiAgICAgICAgICBhcmlhLWxhYmVsPVwiUGljayBhIHRpbWVcIlxuICAgICAgICAgIHBsYWNlaG9sZGVyPVwiUGljayBhIHRpbWVcIlxuICAgICAgICAgIHN0eWxlPVwid2lkdGg6IDEwMCVcIlxuICAgICAgICAvPlxuICAgICAgPC9lbC1jb2w+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkFjdGl2aXR5IHR5cGVcIj5cbiAgICAgIDxlbC1jaGVja2JveC1ncm91cCB2LW1vZGVsPVwic2l6ZUZvcm0udHlwZVwiPlxuICAgICAgICA8ZWwtY2hlY2tib3gtYnV0dG9uIHZhbHVlPVwiT25saW5lIGFjdGl2aXRpZXNcIiBuYW1lPVwidHlwZVwiPlxuICAgICAgICAgIE9ubGluZSBhY3Rpdml0aWVzXG4gICAgICAgIDwvZWwtY2hlY2tib3gtYnV0dG9uPlxuICAgICAgICA8ZWwtY2hlY2tib3gtYnV0dG9uIHZhbHVlPVwiUHJvbW90aW9uIGFjdGl2aXRpZXNcIiBuYW1lPVwidHlwZVwiPlxuICAgICAgICAgIFByb21vdGlvbiBhY3Rpdml0aWVzXG4gICAgICAgIDwvZWwtY2hlY2tib3gtYnV0dG9uPlxuICAgICAgPC9lbC1jaGVja2JveC1ncm91cD5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiUmVzb3VyY2VzXCI+XG4gICAgICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInNpemVGb3JtLnJlc291cmNlXCI+XG4gICAgICAgIDxlbC1yYWRpbyBib3JkZXIgdmFsdWU9XCJTcG9uc29yXCI+U3BvbnNvcjwvZWwtcmFkaW8+XG4gICAgICAgIDxlbC1yYWRpbyBib3JkZXIgdmFsdWU9XCJWZW51ZVwiPlZlbnVlPC9lbC1yYWRpbz5cbiAgICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbT5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBAY2xpY2s9XCJvblN1Ym1pdFwiPkNyZWF0ZTwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWJ1dHRvbj5DYW5jZWw8L2VsLWJ1dHRvbj5cbiAgICA8L2VsLWZvcm0taXRlbT5cbiAgPC9lbC1mb3JtPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlYWN0aXZlLCByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgQ29tcG9uZW50U2l6ZSwgRm9ybVByb3BzIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBzaXplID0gcmVmPENvbXBvbmVudFNpemU+KCdkZWZhdWx0JylcbmNvbnN0IGxhYmVsUG9zaXRpb24gPSByZWY8Rm9ybVByb3BzWydsYWJlbFBvc2l0aW9uJ10+KCdyaWdodCcpXG5cbmNvbnN0IHNpemVGb3JtID0gcmVhY3RpdmUoe1xuICBuYW1lOiAnJyxcbiAgcmVnaW9uOiAnJyxcbiAgZGF0ZTE6ICcnLFxuICBkYXRlMjogJycsXG4gIGRlbGl2ZXJ5OiBmYWxzZSxcbiAgdHlwZTogW10sXG4gIHJlc291cmNlOiAnJyxcbiAgZGVzYzogJycsXG59KVxuXG5mdW5jdGlvbiBvblN1Ym1pdCgpIHtcbiAgY29uc29sZS5sb2coJ3N1Ym1pdCEnKVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5lbC1yYWRpby1ncm91cCB7XG4gIG1hcmdpbi1yaWdodDogMTJweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/form/size-control.vue)_

vue

```
<template>
  <div>
    <el-radio-group v-model="size" aria-label="size control">
      <el-radio-button value="large">large</el-radio-button>
      <el-radio-button value="default">default</el-radio-button>
      <el-radio-button value="small">small</el-radio-button>
    </el-radio-group>
    <el-radio-group v-model="labelPosition" aria-label="position control">
      <el-radio-button value="left">Left</el-radio-button>
      <el-radio-button value="right">Right</el-radio-button>
      <el-radio-button value="top">Top</el-radio-button>
    </el-radio-group>
  </div>
  <br />
  <el-form
    style="max-width: 600px"
    :model="sizeForm"
    label-width="auto"
    :label-position="labelPosition"
    :size="size"
  >
    <el-form-item label="Activity name">
      <el-input v-model="sizeForm.name" />
    </el-form-item>
    <el-form-item label="Activity zone">
      <el-select
        v-model="sizeForm.region"
        placeholder="please select your zone"
      >
        <el-option label="Zone one" value="shanghai" />
        <el-option label="Zone two" value="beijing" />
      </el-select>
    </el-form-item>
    <el-form-item label="Activity time">
      <el-col :span="11">
        <el-date-picker
          v-model="sizeForm.date1"
          type="date"
          aria-label="Pick a date"
          placeholder="Pick a date"
          style="width: 100%"
        />
      </el-col>
      <el-col class="text-center" :span="1" style="margin: 0 0.5rem">-</el-col>
      <el-col :span="11">
        <el-time-picker
          v-model="sizeForm.date2"
          aria-label="Pick a time"
          placeholder="Pick a time"
          style="width: 100%"
        />
      </el-col>
    </el-form-item>
    <el-form-item label="Activity type">
      <el-checkbox-group v-model="sizeForm.type">
        <el-checkbox-button value="Online activities" name="type">
          Online activities
        </el-checkbox-button>
        <el-checkbox-button value="Promotion activities" name="type">
          Promotion activities
        </el-checkbox-button>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item label="Resources">
      <el-radio-group v-model="sizeForm.resource">
        <el-radio border value="Sponsor">Sponsor</el-radio>
        <el-radio border value="Venue">Venue</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Create</el-button>
      <el-button>Cancel</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

import type { ComponentSize, FormProps } from 'element-plus'

const size = ref<ComponentSize>('default')
const labelPosition = ref<FormProps['labelPosition']>('right')

const sizeForm = reactive({
  name: '',
  region: '',
  date1: '',
  date2: '',
  delivery: false,
  type: [],
  resource: '',
  desc: '',
})

function onSubmit() {
  console.log('submit!')
}
</script>

<style>
.el-radio-group {
  margin-right: 12px;
}
</style>
```

隐藏源代码

## 无障碍 [​](#无障碍)

当在 `el-form-item` 内只有一个输入框（或相关的控制部件，如选择或复选框），表单项的标签将自动附加在那个输入框上。 如果 `el-form-item`内有多个 input，则表单项会被设置成 [WAI-ARIA](https://www.w3.org/WAI/standards-guidelines/aria/) [组](https://www.w3.org/TR/wai-aria/#group) 的 role。 在这种情况下，需要手动给每个 input 指定访问标签。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZm9ybSBsYWJlbC1wb3NpdGlvbj1cImxlZnRcIiBsYWJlbC13aWR0aD1cImF1dG9cIiBzdHlsZT1cIm1heC13aWR0aDogNjAwcHhcIj5cbiAgICA8ZWwtc3BhY2UgZmlsbD5cbiAgICAgIDxlbC1hbGVydCB0eXBlPVwiaW5mb1wiIHNob3ctaWNvbiA6Y2xvc2FibGU9XCJmYWxzZVwiPlxuICAgICAgICA8cD5cIkZ1bGwgTmFtZVwiIGxhYmVsIGlzIGF1dG9tYXRpY2FsbHkgYXR0YWNoZWQgdG8gdGhlIGlucHV0OjwvcD5cbiAgICAgIDwvZWwtYWxlcnQ+XG4gICAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiRnVsbCBOYW1lXCI+XG4gICAgICAgIDxlbC1pbnB1dCB2LW1vZGVsPVwiZm9ybUFjY2Vzc2liaWxpdHkuZnVsbE5hbWVcIiAvPlxuICAgICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPC9lbC1zcGFjZT5cbiAgICA8ZWwtc3BhY2UgZmlsbD5cbiAgICAgIDxlbC1hbGVydCB0eXBlPVwiaW5mb1wiIHNob3ctaWNvbiA6Y2xvc2FibGU9XCJmYWxzZVwiPlxuICAgICAgICA8cD5cbiAgICAgICAgICBcIllvdXIgSW5mb3JtYXRpb25cIiBzZXJ2ZXMgYXMgYSBsYWJlbCBmb3IgdGhlIGdyb3VwIG9mIGlucHV0cy4gPGJyIC8+XG4gICAgICAgICAgWW91IG11c3Qgc3BlY2lmeSBsYWJlbHMgb24gdGhlIGluZGl2aWRhbCBpbnB1dHMuIFBsYWNlaG9sZGVycyBhcmUgbm90XG4gICAgICAgICAgcmVwbGFjZW1lbnRzIGZvciB1c2luZyB0aGUgXCJsYWJlbFwiIGF0dHJpYnV0ZS5cbiAgICAgICAgPC9wPlxuICAgICAgPC9lbC1hbGVydD5cbiAgICAgIDxlbC1mb3JtLWl0ZW0gbGFiZWw9XCJZb3VyIEluZm9ybWF0aW9uXCI+XG4gICAgICAgIDxlbC1yb3cgOmd1dHRlcj1cIjIwXCI+XG4gICAgICAgICAgPGVsLWNvbCA6c3Bhbj1cIjEyXCI+XG4gICAgICAgICAgICA8ZWwtaW5wdXRcbiAgICAgICAgICAgICAgdi1tb2RlbD1cImZvcm1BY2Nlc3NpYmlsaXR5LmZpcnN0TmFtZVwiXG4gICAgICAgICAgICAgIGFyaWEtbGFiZWw9XCJGaXJzdCBOYW1lXCJcbiAgICAgICAgICAgICAgcGxhY2Vob2xkZXI9XCJGaXJzdCBOYW1lXCJcbiAgICAgICAgICAgIC8+XG4gICAgICAgICAgPC9lbC1jb2w+XG4gICAgICAgICAgPGVsLWNvbCA6c3Bhbj1cIjEyXCI+XG4gICAgICAgICAgICA8ZWwtaW5wdXRcbiAgICAgICAgICAgICAgdi1tb2RlbD1cImZvcm1BY2Nlc3NpYmlsaXR5Lmxhc3ROYW1lXCJcbiAgICAgICAgICAgICAgYXJpYS1sYWJlbD1cIkxhc3QgTmFtZVwiXG4gICAgICAgICAgICAgIHBsYWNlaG9sZGVyPVwiTGFzdCBOYW1lXCJcbiAgICAgICAgICAgIC8+XG4gICAgICAgICAgPC9lbC1jb2w+XG4gICAgICAgIDwvZWwtcm93PlxuICAgICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPC9lbC1zcGFjZT5cbiAgPC9lbC1mb3JtPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlYWN0aXZlIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBmb3JtQWNjZXNzaWJpbGl0eSA9IHJlYWN0aXZlKHtcbiAgZnVsbE5hbWU6ICcnLFxuICBmaXJzdE5hbWU6ICcnLFxuICBsYXN0TmFtZTogJycsXG59KVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/form/accessibility.vue)_

vue

```
<template>
  <el-form label-position="left" label-width="auto" style="max-width: 600px">
    <el-space fill>
      <el-alert type="info" show-icon :closable="false">
        <p>"Full Name" label is automatically attached to the input:</p>
      </el-alert>
      <el-form-item label="Full Name">
        <el-input v-model="formAccessibility.fullName" />
      </el-form-item>
    </el-space>
    <el-space fill>
      <el-alert type="info" show-icon :closable="false">
        <p>
          "Your Information" serves as a label for the group of inputs. <br />
          You must specify labels on the individal inputs. Placeholders are not
          replacements for using the "label" attribute.
        </p>
      </el-alert>
      <el-form-item label="Your Information">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-input
              v-model="formAccessibility.firstName"
              aria-label="First Name"
              placeholder="First Name"
            />
          </el-col>
          <el-col :span="12">
            <el-input
              v-model="formAccessibility.lastName"
              aria-label="Last Name"
              placeholder="Last Name"
            />
          </el-col>
        </el-row>
      </el-form-item>
    </el-space>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

const formAccessibility = reactive({
  fullName: '',
  firstName: '',
  lastName: '',
})
</script>
```

隐藏源代码

## Form API [​](#form-api)

### Form Attributes [​](#form-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model | 表单数据对象 | `object` | — |
| rules | 表单验证规则 | `object` | — |
| inline | 行内表单模式 | `boolean` | false |
| label-position | 表单域标签的位置， 当设置为 `left` 或 `right` 时，则也需要设置 `label-width` 属性 | `enum` | right |
| label-width | 标签的长度，例如 `'50px'`。 作为 Form 直接子元素的 form-item 会继承该值。 可以使用 `auto`。 | `string` / `number` | '' |
| label-suffix | 表单域标签的后缀 | `string` | '' |
| hide-required-asterisk | 是否隐藏必填字段标签旁边的红色星号。 | `boolean` | false |
| require-asterisk-position | 星号的位置。 | `enum` | left |
| show-message | 是否显示校验错误信息 | `boolean` | true |
| inline-message | 是否以行内形式展示校验信息 | `boolean` | false |
| status-icon | 是否在输入框中显示校验结果反馈图标 | `boolean` | false |
| validate-on-rule-change | 是否在 `rules` 属性改变后立即触发一次验证 | `boolean` | true |
| size | 用于控制该表单内组件的尺寸 | `enum` | — |
| disabled | 是否禁用该表单内的所有组件。 在 2.12.0 以前，如果设置为 `true`，它将覆盖内部组件的 `disabled` 属性。 在 2.12.0 之后，内部组件的配置优先。 | `boolean` | false |
| scroll-to-error | 当校验失败时，滚动到第一个错误表单项 | `boolean` | false |
| scroll-into-view-options 2.3.2 | 当校验有失败结果时，滚动到第一个失败的表单项目 可通过 [scrollIntoView](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView) 配置 | `object` / `boolean` | true |

### Form Events [​](#form-events)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| validate | 任一表单项被校验后触发 | `Function` |

### Form Slots [​](#form-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | FormItem |

### Form Exposes [​](#form-exposes)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| validate | 对整个表单的内容进行验证。 接收一个回调函数，或返回 `Promise`。 | `Function` |
| validateField | 验证具体的某个字段。 | `Function` |
| resetFields | 重置该表单项，将其值重置为初始值，并移除校验结果 | `Function` |
| scrollToField | 滚动到指定的字段 | `Function` |
| clearValidate | 清理某个字段的表单验证信息。 | `Function` |
| fields 2.7.3 | 获取所有字段的 context | `array` |
| getField 2.10.2 | 获取字段的 context | `Function` |
| setInitialValues 2.13.1 | 设置表单字段的初始值。 当调用 `resetFields` 时，字段将重置为这些值。 | `Function` |

## FormItem API [​](#formitem-api)

### FormItem Attributes [​](#formitem-attributes)

| 属性名 | 说明 | 类型 | Default |
| --- | --- | --- | --- |
| prop | `model` 的键名。 它可以是属性的路径（如 `a.b.0` 或 `['a', 'b', '0']`）。 在使用了 `validate`、`resetFields` 的方法时，该属性是必填的。 | `string` / `string[]` | — |
| label | 标签文本 | `string` | — |
| label-position 2.7.7 | 表单域标签的位置， 当设置为 `left` 或 `right` 时，则也需要设置 `label-width` 属性 默认会继承 `Form`的`label-position` | `enum` | '' |
| label-width | 标签宽度，例如 `'50px'`。 可以使用 `auto`。 | `string` / `number` | — |
| required | 是否为必填项，如不设置，则会根据校验规则确认 | `boolean` | — |
| rules | 表单验证规则, 具体配置见[下表](#formitemrule), 更多内容可以参考[async-validator](https://github.com/yiminghe/async-validator) | `object` | — |
| error | 表单域验证错误时的提示信息。设置该值会导致表单验证状态变为 error，并显示该错误信息。 | `string` | — |
| show-message | 是否显示校验错误信息 | `boolean` | true |
| inline-message | 是否在行内显示校验信息 | `boolean` | false |
| size | 用于控制该表单域下组件的默认尺寸 | `enum` | — |
| for | 和原生标签相同能力 | `string` | — |
| validate-status | formitem 校验的状态 | `enum` | — |

#### FormItemRule [​](#formitemrule)

| 名称 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| trigger | 验证逻辑的触发方式 | `enum` | — |

TIP

如果您不想根据输入事件触发验证器， 在相应的输入类型组件上设置 `validate-event` 属性为 `false` (`<el-input>`, `<el-radio>`, `<el-select>`, . ……).

### FormItem Slots [​](#formitem-slots)

| 插槽名 | 说明 | 类型 |
| --- | --- | --- |
| default | 表单的内容。 | — |
| label | 标签位置显示的内容 | `object` |
| error | 验证错误信息的显示内容 | `object` |

### FormItem Exposes [​](#formitem-exposes)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| size | 表单项大小 | `object` |
| validateMessage | 校验消息 | `object` |
| validateState | 校验状态 | `object` |
| validate | 验证表单项 | `Function` |
| resetField | 对该表单项进行重置，将其值重置为初始值并移除校验结果 | `Function` |
| clearValidate | 移除该表单项的校验结果 | `Function` |
| setInitialValue 2.13.1 | 设置表单字段的初始值。 当调用 `resetFields` 时，字段将重置为这些值。 | `Function` |

## 类型声明 [​](#类型声明)

显示类型声明

ts

```
type Arrayable<T> = T | T[]

type FormValidationResult = Promise<boolean>

// ValidateFieldsError: see [async-validator](https://github.com/yiminghe/async-validator/blob/master/src/interface.ts)
type FormValidateCallback = (
  isValid: boolean,
  invalidFields?: ValidateFieldsError
) => Promise<void> | void

// RuleItem: see [async-validator](https://github.com/yiminghe/async-validator/blob/master/src/interface.ts)
interface FormItemRule extends RuleItem {
  trigger?: Arrayable<string>
}

type Primitive = null | undefined | string | number | boolean | symbol | bigint
type BrowserNativeObject = Date | FileList | File | Blob | RegExp
type IsTuple<T extends ReadonlyArray<any>> = number extends T['length']
  ? false
  : true
type ArrayMethodKey = keyof any[]
type TupleKey<T extends ReadonlyArray<any>> = Exclude<keyof T, ArrayMethodKey>
type ArrayKey = number
type PathImpl<K extends string | number, V> = V extends
  | Primitive
  | BrowserNativeObject
  ? `${K}`
  : `${K}` | `${K}.${Path<V>}`
type Path<T> =
  T extends ReadonlyArray<infer V>
    ? IsTuple<T> extends true
      ? {
          [K in TupleKey<T>]-?: PathImpl<Exclude<K, symbol>, T[K]>
        }[TupleKey<T>]
      : PathImpl<ArrayKey, V>
    : {
        [K in keyof T]-?: PathImpl<Exclude<K, symbol>, T[K]>
      }[keyof T]
type FieldPath<T> = T extends object ? Path<T> : never
// MaybeRef: see [@vueuse/core](https://github.com/vueuse/vueuse/blob/main/packages/shared/utils/types.ts)
// UnwrapRef: see [vue](https://github.com/vuejs/core/blob/main/packages/reactivity/src/ref.ts)
type FormRules<T extends MaybeRef<Record<string, any> | string> = string> =
  Partial<
    Record<
      UnwrapRef<T> extends string ? UnwrapRef<T> : FieldPath<UnwrapRef<T>>,
      Arrayable<FormItemRule>
    >
  >

type FormItemValidateState = (typeof formItemValidateStates)[number]
type FormItemProps = ExtractPropTypes<typeof formItemProps>

type FormItemContext = FormItemProps & {
  $el: HTMLDivElement | undefined
  size: ComponentSize
  validateMessage: string
  validateState: FormItemValidateState
  isGroup: boolean
  labelId: string
  inputIds: string[]
  hasLabel: boolean
  fieldValue: any
  propString: string
  addInputId: (id: string) => void
  removeInputId: (id: string) => void
  validate: (
    trigger: string,
    callback?: FormValidateCallback
  ) => FormValidationResult
  resetField(): void
  clearValidate(): void
  setInitialValue: (value: any) => void
}
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/form) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/form.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/form.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/53589602?v=4&size=64)](https://github.com/l246804)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/24290011?v=4&size=64)](https://github.com/xingyixiang)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/31850793?v=4&size=64)](https://github.com/ModyQyW)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/32354856?v=4&size=64)](https://github.com/baiwusanyu-c)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/20052395?v=4&size=64)](https://github.com/guizoxxv)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/52363975?v=4&size=64)](https://github.com/wangbincyzj)[![](https://avatars.githubusercontent.com/u/7877834?v=4&size=64)](https://github.com/921)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/74746021?v=4&size=64)](https://github.com/xing403)[![](https://avatars.githubusercontent.com/u/35091020?v=4&size=64)](https://github.com/zzh948498)[![](https://avatars.githubusercontent.com/u/3362033?v=4&size=64)](https://github.com/cloudcome)[![](https://avatars.githubusercontent.com/u/47593280?v=4&size=64)](https://github.com/Xaw-xu)[![](https://avatars.githubusercontent.com/u/28420052?v=4&size=64)](https://github.com/Jackie-llv)[![](https://avatars.githubusercontent.com/u/46640919?v=4&size=64)](https://github.com/tiansQAQ)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/45762373?v=4&size=64)](https://github.com/koalaniu)[![](https://avatars.githubusercontent.com/u/1744129?v=4&size=64)](https://github.com/hminghe)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/17268607?v=4&size=64)](https://github.com/LYlanfeng)[![](https://avatars.githubusercontent.com/u/22659150?v=4&size=64)](https://github.com/ntnyq)[![](https://avatars.githubusercontent.com/u/83811542?v=4&size=64)](https://github.com/duyidao)[![](https://avatars.githubusercontent.com/u/57179957?v=4&size=64)](https://github.com/yeonjulee1005)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/18051955?v=4&size=64)](https://github.com/qige2016)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/113576575?v=4&size=64)](https://github.com/lkdhy)[![](https://avatars.githubusercontent.com/u/54520846?v=4&size=64)](https://github.com/manyuemeiquqi)[![](https://avatars.githubusercontent.com/u/38113445?v=4&size=64)](https://github.com/assasin0076)[![](https://avatars.githubusercontent.com/u/19164948?v=4&size=64)](https://github.com/achin797)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/28811207?v=4&size=64)](https://github.com/fanhefeng)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/13634675?v=4&size=64)](https://github.com/virgosoy)[![](https://avatars.githubusercontent.com/u/9958583?v=4&size=64)](https://github.com/Otto-J)[![](https://avatars.githubusercontent.com/u/20987775?v=4&size=64)](https://github.com/cbbfcd)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/293591?v=4&size=64)](https://github.com/digitalkaoz)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)[![](https://avatars.githubusercontent.com/u/9622779?v=4&size=64)](https://github.com/taosher)

[DateTime Picker 日期时间选择器](https://element-plus.org/zh-CN/component/datetime-picker)

[Input 输入框](https://element-plus.org/zh-CN/component/input)


