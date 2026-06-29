---
name: "radio"
description: "Radio 单选框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Radio 单选框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/radio.html"
---

---

# Radio 单选框 [​](#radio-单选框)

更新日志待解决

12

在一组备选项中进行单选

WARNING

`label` 作为 `value` 来使用已经被 **废弃**, 建议`label` 只用来表示展示的文字，这个被废弃的用法**将会在** 3.0.0 版本被移除，请考虑使用新 API 替换.

TIP

新的 API `value` 已在 2.6.0 版本添加，文档中的示例都将使用 `value`。 如果您使用的版本 **低于** 2.6.0，请参考：

vue

```
<template>
  <el-radio-group v-model="radio1">
    <!-- works when >=2.6.0, recommended ✔️ not work when <2.6.0 ❌ -->
    <el-radio value="Value 1">Option 1</el-radio>
    <!-- works when <2.6.0, deprecated act as value when >=3.0.0 -->
    <el-radio label="Label 2 & Value 2">Option 2</el-radio>
  </el-radio-group>
</template>
```

## 基础用法 [​](#基础用法)

单选框不应该有太多的可选项， 如果你有很多的可选项你应该使用选择框而不是单选框。

要使用 Radio 组件，只需要设置`v-model`绑定变量， 选中意味着变量的值为相应 Radio `value`属性的值， `value`可以是`String`、`Number` 或 `Boolean`。

Option 1Option 2

Option 1Option 2

Option 1Option 2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibWItMiBtbC00XCI+XG4gICAgPGVsLXJhZGlvLWdyb3VwIHYtbW9kZWw9XCJyYWRpbzFcIj5cbiAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cIjFcIiBzaXplPVwibGFyZ2VcIj5PcHRpb24gMTwvZWwtcmFkaW8+XG4gICAgICA8ZWwtcmFkaW8gdmFsdWU9XCIyXCIgc2l6ZT1cImxhcmdlXCI+T3B0aW9uIDI8L2VsLXJhZGlvPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibXktMiBtbC00XCI+XG4gICAgPGVsLXJhZGlvLWdyb3VwIHYtbW9kZWw9XCJyYWRpbzJcIj5cbiAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cIjFcIj5PcHRpb24gMTwvZWwtcmFkaW8+XG4gICAgICA8ZWwtcmFkaW8gdmFsdWU9XCIyXCI+T3B0aW9uIDI8L2VsLXJhZGlvPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibXktNCBtbC00XCI+XG4gICAgPGVsLXJhZGlvLWdyb3VwIHYtbW9kZWw9XCJyYWRpbzNcIj5cbiAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cIjFcIiBzaXplPVwic21hbGxcIj5PcHRpb24gMTwvZWwtcmFkaW8+XG4gICAgICA8ZWwtcmFkaW8gdmFsdWU9XCIyXCIgc2l6ZT1cInNtYWxsXCI+T3B0aW9uIDI8L2VsLXJhZGlvPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgcmFkaW8xID0gcmVmKCcxJylcbmNvbnN0IHJhZGlvMiA9IHJlZignMScpXG5jb25zdCByYWRpbzMgPSByZWYoJzEnKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/radio/basic-usage.vue)_

vue

```
<template>
  <div class="mb-2 ml-4">
    <el-radio-group v-model="radio1">
      <el-radio value="1" size="large">Option 1</el-radio>
      <el-radio value="2" size="large">Option 2</el-radio>
    </el-radio-group>
  </div>
  <div class="my-2 ml-4">
    <el-radio-group v-model="radio2">
      <el-radio value="1">Option 1</el-radio>
      <el-radio value="2">Option 2</el-radio>
    </el-radio-group>
  </div>
  <div class="my-4 ml-4">
    <el-radio-group v-model="radio3">
      <el-radio value="1" size="small">Option 1</el-radio>
      <el-radio value="2" size="small">Option 2</el-radio>
    </el-radio-group>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const radio1 = ref('1')
const radio2 = ref('1')
const radio3 = ref('1')
</script>
```

隐藏源代码

## 禁用状态 [​](#禁用状态)

`disabled` 属性可以用来控制单选框的禁用状态。

你只需要为单选框设置 `disabled` 属性就能控制其禁用状态。

Option A Option B

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8gdi1tb2RlbD1cInJhZGlvXCIgZGlzYWJsZWQgdmFsdWU9XCJkaXNhYmxlZFwiPk9wdGlvbiBBPC9lbC1yYWRpbz5cbiAgPGVsLXJhZGlvIHYtbW9kZWw9XCJyYWRpb1wiIGRpc2FibGVkIHZhbHVlPVwic2VsZWN0ZWQgYW5kIGRpc2FibGVkXCI+XG4gICAgT3B0aW9uIEJcbiAgPC9lbC1yYWRpbz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHJhZGlvID0gcmVmKCdzZWxlY3RlZCBhbmQgZGlzYWJsZWQnKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/radio/disabled.vue)_

vue

```
<template>
  <el-radio v-model="radio" disabled value="disabled">Option A</el-radio>
  <el-radio v-model="radio" disabled value="selected and disabled">
    Option B
  </el-radio>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const radio = ref('selected and disabled')
</script>
```

隐藏源代码

## 单选框组 [​](#单选框组)

适用于在多个互斥的选项中选择的场景

结合`el-radio-group`元素和子元素`el-radio`可以实现单选组， 为 `el-radio-group` 绑定 `v-model`，再为 每一个 `el-radio` 设置好 `label` 属性即可， 另外，还可以通过 `change` 事件来响应变化，它会传入一个参数 `value` 来表示改变之后的值。

Option AOption BOption C

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInJhZGlvXCI+XG4gICAgPGVsLXJhZGlvIDp2YWx1ZT1cIjNcIj5PcHRpb24gQTwvZWwtcmFkaW8+XG4gICAgPGVsLXJhZGlvIDp2YWx1ZT1cIjZcIj5PcHRpb24gQjwvZWwtcmFkaW8+XG4gICAgPGVsLXJhZGlvIDp2YWx1ZT1cIjlcIj5PcHRpb24gQzwvZWwtcmFkaW8+XG4gIDwvZWwtcmFkaW8tZ3JvdXA+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCByYWRpbyA9IHJlZigzKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/radio/radio-group.vue)_

vue

```
<template>
  <el-radio-group v-model="radio">
    <el-radio :value="3">Option A</el-radio>
    <el-radio :value="6">Option B</el-radio>
    <el-radio :value="9">Option C</el-radio>
  </el-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const radio = ref(3)
</script>
```

隐藏源代码

## 带有边框 [​](#带有边框)

设置 `border` 属性为 true 可以渲染为带有边框的单选框。

Option AOption B

Option AOption B

Option AOption B

Option AOption B

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1yYWRpby1ncm91cCB2LW1vZGVsPVwicmFkaW8xXCI+XG4gICAgICA8ZWwtcmFkaW8gdmFsdWU9XCIxXCIgc2l6ZT1cImxhcmdlXCIgYm9yZGVyPk9wdGlvbiBBPC9lbC1yYWRpbz5cbiAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cIjJcIiBzaXplPVwibGFyZ2VcIiBib3JkZXI+T3B0aW9uIEI8L2VsLXJhZGlvPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDwvZGl2PlxuICA8ZGl2IHN0eWxlPVwibWFyZ2luLXRvcDogMjBweFwiPlxuICAgIDxlbC1yYWRpby1ncm91cCB2LW1vZGVsPVwicmFkaW8yXCI+XG4gICAgICA8ZWwtcmFkaW8gdmFsdWU9XCIxXCIgYm9yZGVyPk9wdGlvbiBBPC9lbC1yYWRpbz5cbiAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cIjJcIiBib3JkZXI+T3B0aW9uIEI8L2VsLXJhZGlvPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDwvZGl2PlxuICA8ZGl2IHN0eWxlPVwibWFyZ2luLXRvcDogMjBweFwiPlxuICAgIDxlbC1yYWRpby1ncm91cCB2LW1vZGVsPVwicmFkaW8zXCIgc2l6ZT1cInNtYWxsXCI+XG4gICAgICA8ZWwtcmFkaW8gdmFsdWU9XCIxXCIgYm9yZGVyPk9wdGlvbiBBPC9lbC1yYWRpbz5cbiAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cIjJcIiBib3JkZXIgZGlzYWJsZWQ+T3B0aW9uIEI8L2VsLXJhZGlvPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDwvZGl2PlxuICA8ZGl2IHN0eWxlPVwibWFyZ2luLXRvcDogMjBweFwiPlxuICAgIDxlbC1yYWRpby1ncm91cCB2LW1vZGVsPVwicmFkaW80XCIgc2l6ZT1cInNtYWxsXCIgZGlzYWJsZWQ+XG4gICAgICA8ZWwtcmFkaW8gdmFsdWU9XCIxXCIgYm9yZGVyPk9wdGlvbiBBPC9lbC1yYWRpbz5cbiAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cIjJcIiBib3JkZXI+T3B0aW9uIEI8L2VsLXJhZGlvPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgcmFkaW8xID0gcmVmKCcxJylcbmNvbnN0IHJhZGlvMiA9IHJlZignMScpXG5jb25zdCByYWRpbzMgPSByZWYoJzEnKVxuY29uc3QgcmFkaW80ID0gcmVmKCcxJylcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/radio/with-borders.vue)_

vue

```
<template>
  <div>
    <el-radio-group v-model="radio1">
      <el-radio value="1" size="large" border>Option A</el-radio>
      <el-radio value="2" size="large" border>Option B</el-radio>
    </el-radio-group>
  </div>
  <div style="margin-top: 20px">
    <el-radio-group v-model="radio2">
      <el-radio value="1" border>Option A</el-radio>
      <el-radio value="2" border>Option B</el-radio>
    </el-radio-group>
  </div>
  <div style="margin-top: 20px">
    <el-radio-group v-model="radio3" size="small">
      <el-radio value="1" border>Option A</el-radio>
      <el-radio value="2" border disabled>Option B</el-radio>
    </el-radio-group>
  </div>
  <div style="margin-top: 20px">
    <el-radio-group v-model="radio4" size="small" disabled>
      <el-radio value="1" border>Option A</el-radio>
      <el-radio value="2" border>Option B</el-radio>
    </el-radio-group>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const radio1 = ref('1')
const radio2 = ref('1')
const radio3 = ref('1')
const radio4 = ref('1')
</script>
```

隐藏源代码

## Options 属性 2.11.2 [​](#options-属性)

基础用法 `el-radio-group` 的快捷示例。 您可以通过 `props` 属性自定义 `options` 的别名。

Option AOption BOption C

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInJhZGlvXCIgOm9wdGlvbnM9XCJvcHRpb25zXCIgOnByb3BzPVwicHJvcHNcIiAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgcmFkaW8gPSByZWYoMylcbmNvbnN0IHByb3BzID0geyB2YWx1ZTogJ2lkJywgbGFiZWw6ICduYW1lJywgZGlzYWJsZWQ6ICd1bmFibGUnIH1cbmNvbnN0IG9wdGlvbnMgPSBbXG4gIHtcbiAgICBpZDogMyxcbiAgICBuYW1lOiAnT3B0aW9uIEEnLFxuICB9LFxuICB7XG4gICAgaWQ6IDYsXG4gICAgbmFtZTogJ09wdGlvbiBCJyxcbiAgfSxcbiAge1xuICAgIGlkOiA5LFxuICAgIG5hbWU6ICdPcHRpb24gQycsXG4gICAgdW5hYmxlOiB0cnVlLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/radio/options.vue)_

vue

```
<template>
  <el-radio-group v-model="radio" :options="options" :props="props" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const radio = ref(3)
const props = { value: 'id', label: 'name', disabled: 'unable' }
const options = [
  {
    id: 3,
    name: 'Option A',
  },
  {
    id: 6,
    name: 'Option B',
  },
  {
    id: 9,
    name: 'Option C',
    unable: true,
  },
]
</script>
```

隐藏源代码

## 单选按钮 [​](#单选按钮)

带有按钮组视觉效果的单选框

只需要把 `el-radio` 元素换成 `el-radio-button` 元素即可， :::demo 您可以使用 `填充` 和 `文本颜色` 设置按钮的样式。

New YorkWashingtonLos AngelesChicago

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1yYWRpby1ncm91cCB2LW1vZGVsPVwicmFkaW9cIiBzaXplPVwibGFyZ2VcIiBmaWxsPVwiIzQwOWVmZlwiPlxuICAgICAgPGVsLXJhZGlvLWJ1dHRvbiBsYWJlbD1cIk5ldyBZb3JrXCIgdmFsdWU9XCJOZXcgWW9ya1wiIC8+XG4gICAgICA8ZWwtcmFkaW8tYnV0dG9uIGxhYmVsPVwiV2FzaGluZ3RvblwiIHZhbHVlPVwiV2FzaGluZ3RvblwiIC8+XG4gICAgICA8ZWwtcmFkaW8tYnV0dG9uIGxhYmVsPVwiTG9zIEFuZ2VsZXNcIiB2YWx1ZT1cIkxvcyBBbmdlbGVzXCIgLz5cbiAgICAgIDxlbC1yYWRpby1idXR0b24gbGFiZWw9XCJDaGljYWdvXCIgdmFsdWU9XCJDaGljYWdvXCIgLz5cbiAgICA8L2VsLXJhZGlvLWdyb3VwPlxuICA8L2Rpdj5cbiAgPGRpdiBzdHlsZT1cIm1hcmdpbi10b3A6IDIwcHhcIj5cbiAgICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInJhZGlvXCIgdGV4dC1jb2xvcj1cIiNmZmZcIiBmaWxsPVwiIzZjNmNmZlwiPlxuICAgICAgPGVsLXJhZGlvLWJ1dHRvbiBsYWJlbD1cIk5ldyBZb3JrXCIgdmFsdWU9XCJOZXcgWW9ya1wiIC8+XG4gICAgICA8ZWwtcmFkaW8tYnV0dG9uIGxhYmVsPVwiV2FzaGluZ3RvblwiIHZhbHVlPVwiV2FzaGluZ3RvblwiIC8+XG4gICAgICA8ZWwtcmFkaW8tYnV0dG9uIGxhYmVsPVwiTG9zIEFuZ2VsZXNcIiB2YWx1ZT1cIkxvcyBBbmdlbGVzXCIgLz5cbiAgICAgIDxlbC1yYWRpby1idXR0b24gbGFiZWw9XCJDaGljYWdvXCIgdmFsdWU9XCJDaGljYWdvXCIgLz5cbiAgICA8L2VsLXJhZGlvLWdyb3VwPlxuICA8L2Rpdj5cbiAgPGRpdiBzdHlsZT1cIm1hcmdpbi10b3A6IDIwcHhcIj5cbiAgICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInJhZGlvXCIgc2l6ZT1cInNtYWxsXCI+XG4gICAgICA8ZWwtcmFkaW8tYnV0dG9uIGxhYmVsPVwiTmV3IFlvcmtcIiB2YWx1ZT1cIk5ldyBZb3JrXCIgLz5cbiAgICAgIDxlbC1yYWRpby1idXR0b24gbGFiZWw9XCJXYXNoaW5ndG9uXCIgdmFsdWU9XCJXYXNoaW5ndG9uXCIgZGlzYWJsZWQgLz5cbiAgICAgIDxlbC1yYWRpby1idXR0b24gbGFiZWw9XCJMb3MgQW5nZWxlc1wiIHZhbHVlPVwiTG9zIEFuZ2VsZXNcIiAvPlxuICAgICAgPGVsLXJhZGlvLWJ1dHRvbiBsYWJlbD1cIkNoaWNhZ29cIiB2YWx1ZT1cIkNoaWNhZ29cIiAvPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgcmFkaW8gPSByZWYoJ05ldyBZb3JrJylcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/radio/radio-button.vue)_

vue

```
<template>
  <div>
    <el-radio-group v-model="radio" size="large" fill="#409eff">
      <el-radio-button label="New York" value="New York" />
      <el-radio-button label="Washington" value="Washington" />
      <el-radio-button label="Los Angeles" value="Los Angeles" />
      <el-radio-button label="Chicago" value="Chicago" />
    </el-radio-group>
  </div>
  <div style="margin-top: 20px">
    <el-radio-group v-model="radio" text-color="#fff" fill="#6c6cff">
      <el-radio-button label="New York" value="New York" />
      <el-radio-button label="Washington" value="Washington" />
      <el-radio-button label="Los Angeles" value="Los Angeles" />
      <el-radio-button label="Chicago" value="Chicago" />
    </el-radio-group>
  </div>
  <div style="margin-top: 20px">
    <el-radio-group v-model="radio" size="small">
      <el-radio-button label="New York" value="New York" />
      <el-radio-button label="Washington" value="Washington" disabled />
      <el-radio-button label="Los Angeles" value="Los Angeles" />
      <el-radio-button label="Chicago" value="Chicago" />
    </el-radio-group>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const radio = ref('New York')
</script>
```

隐藏源代码

## Radio API [​](#radio-api)

### Radio Attributes [​](#radio-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `string` / `number` / `boolean` | — |
| value 2.6.0 | 单选框的值 | `string` / `number` / `boolean` | ::: |
| label | 单选框的 label 如果`value`没有值， `label`则作为`value`使用 | `string` / `number` / `boolean` | ::: |
| disabled | 是否禁用单选框 | `boolean` | false |
| border | 是否显示边框 | `boolean` | false |
| size | 单选框的尺寸 | `enum` | — |
| name | 原始 `name` 属性 | `string` | — |

### Radio Events [​](#radio-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 绑定值变化时触发的事件 | `Function` |

### Radio Slots [​](#radio-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## RadioGroup API [​](#radiogroup-api)

### RadioGroup Attributes [​](#radiogroup-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 绑定值 | `string` / `number` / `boolean` | — |
| size | 单选框按钮或边框按钮的大小 | `string` | default |
| disabled | 是否禁用 | `boolean` | false |
| validate-event | 输入时是否触发表单的校验 | `boolean` | true |
| text-color | 按钮形式的 Radio 激活时的文本颜色 | `string` | #ffffff |
| fill | 按钮形式的 Radio 激活时的填充色和边框色 | `string` | #409eff |
| aria-label a11y 2.7.2 | 与 RadioGroup 中的 `aria-label` 属性相同 | `string` | — |
| name | 原生 `name` 属性 | `string` | — |
| id | 原生 `id` 属性 | `string` | — |
| label a11y deprecated | 与 RadioGroup 中的 `aria-label` 属性相同 | `string` | — |
| options 2.11.2 | 选项的数据源， `value` 的 key 和 `label` 和 `disabled`可以通过 `props`自定义. | `array` | — |
| props 2.11.2 | options 的配置 | `object` | `{value: 'value', label: 'label', disabled: 'disabled'}` |
| type 2.11.5 | 用于渲染选项的组件类型（例如 `'button'`） | `enum` | 'radio' |

### RadioGroup Events [​](#radiogroup-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 绑定值变化时触发的事件 | `Function` |

### RadioGroup Slots [​](#radiogroup-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | Radio / RadioButton |

## RadioButton API [​](#radiobutton-api)

### RadioButton Attributes [​](#radiobutton-attributes)

| 名称 | 详情 | 类型 | 默认 |
| --- | --- | --- | --- |
| value 2.6.0 | 单选框的值 | `string` / `number` / `boolean` | — |
| label | 单选框的 label 如果没有 value， `label`则作为`value`使用 | `string` / `number` / `boolean` | — |
| disabled | 是否禁用单选框 | `boolean` | false |
| name | 原生 name 属性 | `string` | — |

### RadioButton Slots [​](#radiobutton-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 默认插槽内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/radio) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/radio.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/radio.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/50943004?v=4&size=64)](https://github.com/cactuser-Lu)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/41461715?v=4&size=64)](https://github.com/VENI-VIDIVICI)[![](https://avatars.githubusercontent.com/u/40999116?v=4&size=64)](https://github.com/jasonren0403)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/18263998?v=4&size=64)](https://github.com/taojunnan)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/26077227?v=4&size=64)](https://github.com/OneDayOneStep)

[Mention 提及](https://element-plus.org/zh-CN/component/mention)

[Rate 评分](https://element-plus.org/zh-CN/component/rate)


