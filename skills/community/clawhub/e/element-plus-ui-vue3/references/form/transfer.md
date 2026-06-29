---
name: "transfer"
description: "Transfer 穿梭框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Transfer 穿梭框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/transfer.html"
---

---

# Transfer 穿梭框 [​](#transfer-穿梭框)

更新日志待解决

4

## 基础用法 [​](#基础用法)

Transfer 的数据通过 `data` 属性传入。 数据需要是一个对象数组，每个对象有以下属性：`key` 为数据的唯一性标识，`label` 为显示文本，`disabled` 表示该项数据是否禁止被操作。 目标列表中的数据项会同步到绑定至 `v-model` 的变量，值为数据项的 `key` 所组成的数组。 当然，如果希望在初始状态时目标列表不为空，可以像本例一样为 `v-model` 绑定的变量赋予一个初始值。

List 10/15

Option 1Option 2Option 3Option 4Option 5Option 6Option 7Option 8Option 9Option 10Option 11Option 12Option 13Option 14Option 15

No data

List 20/0

No data

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJhbnNmZXIgdi1tb2RlbD1cInZhbHVlXCIgOmRhdGE9XCJkYXRhXCIgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmludGVyZmFjZSBPcHRpb24ge1xuICBrZXk6IG51bWJlclxuICBsYWJlbDogc3RyaW5nXG4gIGRpc2FibGVkOiBib29sZWFuXG59XG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9ICgpID0+IHtcbiAgY29uc3QgZGF0YTogT3B0aW9uW10gPSBbXVxuICBmb3IgKGxldCBpID0gMTsgaSA8PSAxNTsgaSsrKSB7XG4gICAgZGF0YS5wdXNoKHtcbiAgICAgIGtleTogaSxcbiAgICAgIGxhYmVsOiBgT3B0aW9uICR7aX1gLFxuICAgICAgZGlzYWJsZWQ6IGkgJSA0ID09PSAwLFxuICAgIH0pXG4gIH1cbiAgcmV0dXJuIGRhdGFcbn1cblxuY29uc3QgZGF0YSA9IHJlZjxPcHRpb25bXT4oZ2VuZXJhdGVEYXRhKCkpXG5jb25zdCB2YWx1ZSA9IHJlZihbXSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/transfer/basic.vue)_

vue

```
<template>
  <el-transfer v-model="value" :data="data" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Option {
  key: number
  label: string
  disabled: boolean
}

const generateData = () => {
  const data: Option[] = []
  for (let i = 1; i <= 15; i++) {
    data.push({
      key: i,
      label: `Option ${i}`,
      disabled: i % 4 === 0,
    })
  }
  return data
}

const data = ref<Option[]>(generateData())
const value = ref([])
</script>
```

隐藏源代码

## 可搜索过滤 [​](#可搜索过滤)

在数据很多的情况下，可以对数据进行搜索和过滤。

设置 `filterable` 为 `true` 即可开启搜索模式。 默认情况下，若数据项的 `label` 属性包含搜索关键字，则会在搜索结果中显示。 你也可以使用 `filter-method` 定义自己的搜索逻辑。 `filter-method` 接收一个方法，当搜索关键字变化时，会将当前的关键字和每个数据项传给该方法。 若方法返回 `true`，则会在搜索结果中显示对应的数据项。

List 10/7

CaliforniaIllinoisMarylandTexasFloridaColoradoConnecticut

No data

List 20/0

No data

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJhbnNmZXJcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIGZpbHRlcmFibGVcbiAgICA6ZmlsdGVyLW1ldGhvZD1cImZpbHRlck1ldGhvZFwiXG4gICAgZmlsdGVyLXBsYWNlaG9sZGVyPVwiU3RhdGUgQWJicmV2aWF0aW9uc1wiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmludGVyZmFjZSBPcHRpb24ge1xuICBrZXk6IG51bWJlclxuICBsYWJlbDogc3RyaW5nXG4gIGluaXRpYWw6IHN0cmluZ1xufVxuXG5jb25zdCBnZW5lcmF0ZURhdGEgPSAoKSA9PiB7XG4gIGNvbnN0IGRhdGE6IE9wdGlvbltdID0gW11cbiAgY29uc3Qgc3RhdGVzID0gW1xuICAgICdDYWxpZm9ybmlhJyxcbiAgICAnSWxsaW5vaXMnLFxuICAgICdNYXJ5bGFuZCcsXG4gICAgJ1RleGFzJyxcbiAgICAnRmxvcmlkYScsXG4gICAgJ0NvbG9yYWRvJyxcbiAgICAnQ29ubmVjdGljdXQgJyxcbiAgXVxuICBjb25zdCBpbml0aWFscyA9IFsnQ0EnLCAnSUwnLCAnTUQnLCAnVFgnLCAnRkwnLCAnQ08nLCAnQ1QnXVxuICBzdGF0ZXMuZm9yRWFjaCgoY2l0eSwgaW5kZXgpID0+IHtcbiAgICBkYXRhLnB1c2goe1xuICAgICAgbGFiZWw6IGNpdHksXG4gICAgICBrZXk6IGluZGV4LFxuICAgICAgaW5pdGlhbDogaW5pdGlhbHNbaW5kZXhdLFxuICAgIH0pXG4gIH0pXG4gIHJldHVybiBkYXRhXG59XG5cbmNvbnN0IGRhdGEgPSByZWY8T3B0aW9uW10+KGdlbmVyYXRlRGF0YSgpKVxuY29uc3QgdmFsdWUgPSByZWYoW10pXG5cbmNvbnN0IGZpbHRlck1ldGhvZCA9IChxdWVyeSwgaXRlbSkgPT4ge1xuICByZXR1cm4gaXRlbS5pbml0aWFsLnRvTG93ZXJDYXNlKCkuaW5jbHVkZXMocXVlcnkudG9Mb3dlckNhc2UoKSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/transfer/filterable.vue)_

vue

```
<template>
  <el-transfer
    v-model="value"
    filterable
    :filter-method="filterMethod"
    filter-placeholder="State Abbreviations"
    :data="data"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Option {
  key: number
  label: string
  initial: string
}

const generateData = () => {
  const data: Option[] = []
  const states = [
    'California',
    'Illinois',
    'Maryland',
    'Texas',
    'Florida',
    'Colorado',
    'Connecticut ',
  ]
  const initials = ['CA', 'IL', 'MD', 'TX', 'FL', 'CO', 'CT']
  states.forEach((city, index) => {
    data.push({
      label: city,
      key: index,
      initial: initials[index],
    })
  })
  return data
}

const data = ref<Option[]>(generateData())
const value = ref([])

const filterMethod = (query, item) => {
  return item.initial.toLowerCase().includes(query.toLowerCase())
}
</script>
```

隐藏源代码

## 自定义 [​](#自定义)

可以对列表标题文案、按钮文案、数据项的渲染函数、列表底部的勾选状态文案、列表底部的内容区等进行自定义。

可以使用 `titles`、`button-texts`、`render-content` 和 `format` 属性分别对列表标题文案、按钮文案、数据项的渲染函数和列表顶部的勾选状态文案进行自定义。 数据项的渲染还可以使用 `scoped-slot` 进行自定义。 对于列表底部的内容区，提供了两个具名 slot：`left-footer` 和 `right-footer`。 此外，如果希望某些数据项在初始化时就被勾选，可以使用 `left-default-checked` 和 `right-default-checked` 属性。 最后，本例还展示了 `change` 事件的用法。 注意，由于 JSFiddle 不支持 JSX 语法，故该示例无法在 JSFiddle 运行。 但是在实际的项目中，只要正确地配置了相关依赖，就可以正常运行。

Customize data items using render-content

Source2/14

Option 2Option 3Option 4Option 5Option 6Option 7Option 8Option 9Option 10Option 11Option 12Option 13Option 14Option 15

No data

Operation

To leftTo right

Target1/1

Option 1

No data

Operation

Customize data items using scoped slot

Source2/14

2 - Option 23 - Option 34 - Option 45 - Option 56 - Option 67 - Option 78 - Option 89 - Option 910 - Option 1011 - Option 1112 - Option 1213 - Option 1314 - Option 1415 - Option 15

No data

Operation

To leftTo right

Target1/1

1 - Option 1

No data

Operation

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8cCBzdHlsZT1cInRleHQtYWxpZ246IGNlbnRlcjsgbWFyZ2luOiAwIDAgMjBweFwiPlxuICAgIEN1c3RvbWl6ZSBkYXRhIGl0ZW1zIHVzaW5nIHJlbmRlci1jb250ZW50XG4gIDwvcD5cbiAgPGRpdiBzdHlsZT1cInRleHQtYWxpZ246IGNlbnRlclwiPlxuICAgIDxlbC10cmFuc2ZlclxuICAgICAgdi1tb2RlbD1cImxlZnRWYWx1ZVwiXG4gICAgICBzdHlsZT1cInRleHQtYWxpZ246IGxlZnQ7IGRpc3BsYXk6IGlubGluZS1ibG9ja1wiXG4gICAgICBmaWx0ZXJhYmxlXG4gICAgICA6bGVmdC1kZWZhdWx0LWNoZWNrZWQ9XCJbMiwgM11cIlxuICAgICAgOnJpZ2h0LWRlZmF1bHQtY2hlY2tlZD1cIlsxXVwiXG4gICAgICA6cmVuZGVyLWNvbnRlbnQ9XCJyZW5kZXJGdW5jXCJcbiAgICAgIDp0aXRsZXM9XCJbJ1NvdXJjZScsICdUYXJnZXQnXVwiXG4gICAgICA6YnV0dG9uLXRleHRzPVwiWydUbyBsZWZ0JywgJ1RvIHJpZ2h0J11cIlxuICAgICAgOmZvcm1hdD1cIntcbiAgICAgICAgbm9DaGVja2VkOiAnJHt0b3RhbH0nLFxuICAgICAgICBoYXNDaGVja2VkOiAnJHtjaGVja2VkfS8ke3RvdGFsfScsXG4gICAgICB9XCJcbiAgICAgIDpkYXRhPVwiZGF0YVwiXG4gICAgICBAY2hhbmdlPVwiaGFuZGxlQ2hhbmdlXCJcbiAgICA+XG4gICAgICA8dGVtcGxhdGUgI2xlZnQtZm9vdGVyPlxuICAgICAgICA8ZWwtYnV0dG9uIGNsYXNzPVwidHJhbnNmZXItZm9vdGVyXCIgc2l6ZT1cInNtYWxsXCI+T3BlcmF0aW9uPC9lbC1idXR0b24+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgPHRlbXBsYXRlICNyaWdodC1mb290ZXI+XG4gICAgICAgIDxlbC1idXR0b24gY2xhc3M9XCJ0cmFuc2Zlci1mb290ZXJcIiBzaXplPVwic21hbGxcIj5PcGVyYXRpb248L2VsLWJ1dHRvbj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC10cmFuc2Zlcj5cbiAgICA8cCBzdHlsZT1cInRleHQtYWxpZ246IGNlbnRlcjsgbWFyZ2luOiA1MHB4IDAgMjBweFwiPlxuICAgICAgQ3VzdG9taXplIGRhdGEgaXRlbXMgdXNpbmcgc2NvcGVkIHNsb3RcbiAgICA8L3A+XG4gICAgPGRpdiBzdHlsZT1cInRleHQtYWxpZ246IGNlbnRlclwiPlxuICAgICAgPGVsLXRyYW5zZmVyXG4gICAgICAgIHYtbW9kZWw9XCJyaWdodFZhbHVlXCJcbiAgICAgICAgc3R5bGU9XCJ0ZXh0LWFsaWduOiBsZWZ0OyBkaXNwbGF5OiBpbmxpbmUtYmxvY2tcIlxuICAgICAgICBmaWx0ZXJhYmxlXG4gICAgICAgIDpsZWZ0LWRlZmF1bHQtY2hlY2tlZD1cIlsyLCAzXVwiXG4gICAgICAgIDpyaWdodC1kZWZhdWx0LWNoZWNrZWQ9XCJbMV1cIlxuICAgICAgICA6dGl0bGVzPVwiWydTb3VyY2UnLCAnVGFyZ2V0J11cIlxuICAgICAgICA6YnV0dG9uLXRleHRzPVwiWydUbyBsZWZ0JywgJ1RvIHJpZ2h0J11cIlxuICAgICAgICA6Zm9ybWF0PVwie1xuICAgICAgICAgIG5vQ2hlY2tlZDogJyR7dG90YWx9JyxcbiAgICAgICAgICBoYXNDaGVja2VkOiAnJHtjaGVja2VkfS8ke3RvdGFsfScsXG4gICAgICAgIH1cIlxuICAgICAgICA6ZGF0YT1cImRhdGFcIlxuICAgICAgICBAY2hhbmdlPVwiaGFuZGxlQ2hhbmdlXCJcbiAgICAgID5cbiAgICAgICAgPHRlbXBsYXRlICNkZWZhdWx0PVwieyBvcHRpb24gfVwiPlxuICAgICAgICAgIDxzcGFuPnt7IG9wdGlvbi5rZXkgfX0gLSB7eyBvcHRpb24ubGFiZWwgfX08L3NwYW4+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgIDx0ZW1wbGF0ZSAjbGVmdC1mb290ZXI+XG4gICAgICAgICAgPGVsLWJ1dHRvbiBjbGFzcz1cInRyYW5zZmVyLWZvb3RlclwiIHNpemU9XCJzbWFsbFwiPk9wZXJhdGlvbjwvZWwtYnV0dG9uPlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICA8dGVtcGxhdGUgI3JpZ2h0LWZvb3Rlcj5cbiAgICAgICAgICA8ZWwtYnV0dG9uIGNsYXNzPVwidHJhbnNmZXItZm9vdGVyXCIgc2l6ZT1cInNtYWxsXCI+T3BlcmF0aW9uPC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXRyYW5zZmVyPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHtcbiAgVHJhbnNmZXJEaXJlY3Rpb24sXG4gIFRyYW5zZmVyS2V5LFxuICByZW5kZXJDb250ZW50LFxufSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmludGVyZmFjZSBPcHRpb24ge1xuICBrZXk6IG51bWJlclxuICBsYWJlbDogc3RyaW5nXG4gIGRpc2FibGVkOiBib29sZWFuXG59XG5cbmNvbnN0IGdlbmVyYXRlRGF0YSA9ICgpOiBPcHRpb25bXSA9PiB7XG4gIGNvbnN0IGRhdGE6IE9wdGlvbltdID0gW11cbiAgZm9yIChsZXQgaSA9IDE7IGkgPD0gMTU7IGkrKykge1xuICAgIGRhdGEucHVzaCh7XG4gICAgICBrZXk6IGksXG4gICAgICBsYWJlbDogYE9wdGlvbiAke2l9YCxcbiAgICAgIGRpc2FibGVkOiBpICUgNCA9PT0gMCxcbiAgICB9KVxuICB9XG4gIHJldHVybiBkYXRhXG59XG5cbmNvbnN0IGRhdGEgPSByZWYoZ2VuZXJhdGVEYXRhKCkpXG5jb25zdCByaWdodFZhbHVlID0gcmVmKFsxXSlcbmNvbnN0IGxlZnRWYWx1ZSA9IHJlZihbMV0pXG5cbmNvbnN0IHJlbmRlckZ1bmM6IHJlbmRlckNvbnRlbnQgPSAoaCwgb3B0aW9uKSA9PiBoKCdzcGFuJywgbnVsbCwgb3B0aW9uLmxhYmVsKVxuXG5jb25zdCBoYW5kbGVDaGFuZ2UgPSAoXG4gIHZhbHVlOiBUcmFuc2ZlcktleVtdLFxuICBkaXJlY3Rpb246IFRyYW5zZmVyRGlyZWN0aW9uLFxuICBtb3ZlZEtleXM6IFRyYW5zZmVyS2V5W11cbikgPT4ge1xuICBjb25zb2xlLmxvZyh2YWx1ZSwgZGlyZWN0aW9uLCBtb3ZlZEtleXMpXG59XG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLnRyYW5zZmVyLWZvb3RlciB7XG4gIG1hcmdpbi1sZWZ0OiAxNXB4O1xuICBwYWRkaW5nOiA2cHggNXB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/transfer/customizable.vue)_

vue

```
<template>
  <p style="text-align: center; margin: 0 0 20px">
    Customize data items using render-content
  </p>
  <div style="text-align: center">
    <el-transfer
      v-model="leftValue"
      style="text-align: left; display: inline-block"
      filterable
      :left-default-checked="[2, 3]"
      :right-default-checked="[1]"
      :render-content="renderFunc"
      :titles="['Source', 'Target']"
      :button-texts="['To left', 'To right']"
      :format="{
        noChecked: '${total}',
        hasChecked: '${checked}/${total}',
      }"
      :data="data"
      @change="handleChange"
    >
      <template #left-footer>
        <el-button class="transfer-footer" size="small">Operation</el-button>
      </template>
      <template #right-footer>
        <el-button class="transfer-footer" size="small">Operation</el-button>
      </template>
    </el-transfer>
    <p style="text-align: center; margin: 50px 0 20px">
      Customize data items using scoped slot
    </p>
    <div style="text-align: center">
      <el-transfer
        v-model="rightValue"
        style="text-align: left; display: inline-block"
        filterable
        :left-default-checked="[2, 3]"
        :right-default-checked="[1]"
        :titles="['Source', 'Target']"
        :button-texts="['To left', 'To right']"
        :format="{
          noChecked: '${total}',
          hasChecked: '${checked}/${total}',
        }"
        :data="data"
        @change="handleChange"
      >
        <template #default="{ option }">
          <span>{{ option.key }} - {{ option.label }}</span>
        </template>
        <template #left-footer>
          <el-button class="transfer-footer" size="small">Operation</el-button>
        </template>
        <template #right-footer>
          <el-button class="transfer-footer" size="small">Operation</el-button>
        </template>
      </el-transfer>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type {
  TransferDirection,
  TransferKey,
  renderContent,
} from 'element-plus'

interface Option {
  key: number
  label: string
  disabled: boolean
}

const generateData = (): Option[] => {
  const data: Option[] = []
  for (let i = 1; i <= 15; i++) {
    data.push({
      key: i,
      label: `Option ${i}`,
      disabled: i % 4 === 0,
    })
  }
  return data
}

const data = ref(generateData())
const rightValue = ref([1])
const leftValue = ref([1])

const renderFunc: renderContent = (h, option) => h('span', null, option.label)

const handleChange = (
  value: TransferKey[],
  direction: TransferDirection,
  movedKeys: TransferKey[]
) => {
  console.log(value, direction, movedKeys)
}
</script>

<style>
.transfer-footer {
  margin-left: 15px;
  padding: 6px 5px;
}
</style>
```

隐藏源代码

## 自定义空内容 2.9.0 [​](#自定义空内容)

您可以自定义列表为空或未找到筛选结果时显示的内容。

使用 `left-empty` 和 `right-empty` 插槽来自定义每个面板的空内容。

List 10/15

Option 1Option 2Option 3Option 4Option 5Option 6Option 7Option 8Option 9Option 10Option 11Option 12Option 13Option 14Option 15

No data

List 20/0

No data

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJhbnNmZXIgdi1tb2RlbD1cInZhbHVlXCIgOmRhdGE9XCJkYXRhXCI+XG4gICAgPHRlbXBsYXRlICNsZWZ0LWVtcHR5PlxuICAgICAgPGVsLWVtcHR5IDppbWFnZS1zaXplPVwiNjBcIiBkZXNjcmlwdGlvbj1cIk5vIGRhdGFcIiAvPlxuICAgIDwvdGVtcGxhdGU+XG4gICAgPHRlbXBsYXRlICNyaWdodC1lbXB0eT5cbiAgICAgIDxlbC1lbXB0eSA6aW1hZ2Utc2l6ZT1cIjYwXCIgZGVzY3JpcHRpb249XCJObyBkYXRhXCIgLz5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLXRyYW5zZmVyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW50ZXJmYWNlIERhdGFJdGVtIHtcbiAga2V5OiBudW1iZXJcbiAgbGFiZWw6IHN0cmluZ1xuICBkaXNhYmxlZDogYm9vbGVhblxufVxuY29uc3QgZ2VuZXJhdGVEYXRhID0gKCk6IERhdGFJdGVtW10gPT4ge1xuICBjb25zdCBkYXRhOiBEYXRhSXRlbVtdID0gW11cbiAgZm9yIChsZXQgaSA9IDE7IGkgPD0gMTU7IGkrKykge1xuICAgIGRhdGEucHVzaCh7XG4gICAgICBrZXk6IGksXG4gICAgICBsYWJlbDogYE9wdGlvbiAke2l9YCxcbiAgICAgIGRpc2FibGVkOiBpICUgNCA9PT0gMCxcbiAgICB9KVxuICB9XG4gIHJldHVybiBkYXRhXG59XG5cbmNvbnN0IGRhdGEgPSByZWYoZ2VuZXJhdGVEYXRhKCkpXG5jb25zdCB2YWx1ZSA9IHJlZihbXSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/transfer/empty-content.vue)_

vue

```
<template>
  <el-transfer v-model="value" :data="data">
    <template #left-empty>
      <el-empty :image-size="60" description="No data" />
    </template>
    <template #right-empty>
      <el-empty :image-size="60" description="No data" />
    </template>
  </el-transfer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface DataItem {
  key: number
  label: string
  disabled: boolean
}
const generateData = (): DataItem[] => {
  const data: DataItem[] = []
  for (let i = 1; i <= 15; i++) {
    data.push({
      key: i,
      label: `Option ${i}`,
      disabled: i % 4 === 0,
    })
  }
  return data
}

const data = ref(generateData())
const value = ref([])
</script>
```

隐藏源代码

## 数据项属性别名 [​](#数据项属性别名)

默认情况下，Transfer 仅能识别数据项中的 `key`、`label` 和 `disabled` 字段。 如果你的数据的字段名不同，可以使用 `props` 属性为它们设置别名。

本例中的数据源没有 `key` 和 `label` 字段，在功能上与它们相同的字段名为 `value` 和 `desc`。 因此可以使用`props` 属性为 `key` 和 `label` 设置别名。

List 10/15

Option 1Option 2Option 3Option 4Option 5Option 6Option 7Option 8Option 9Option 10Option 11Option 12Option 13Option 14Option 15

No data

List 20/0

No data

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdHJhbnNmZXJcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIDpwcm9wcz1cIntcbiAgICAgIGtleTogJ3ZhbHVlJyxcbiAgICAgIGxhYmVsOiAnZGVzYycsXG4gICAgfVwiXG4gICAgOmRhdGE9XCJkYXRhXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmludGVyZmFjZSBPcHRpb24ge1xuICB2YWx1ZTogbnVtYmVyXG4gIGRlc2M6IHN0cmluZ1xuICBkaXNhYmxlZDogYm9vbGVhblxufVxuXG5jb25zdCBnZW5lcmF0ZURhdGEgPSAoKSA9PiB7XG4gIGNvbnN0IGRhdGE6IE9wdGlvbltdID0gW11cbiAgZm9yIChsZXQgaSA9IDE7IGkgPD0gMTU7IGkrKykge1xuICAgIGRhdGEucHVzaCh7XG4gICAgICB2YWx1ZTogaSxcbiAgICAgIGRlc2M6IGBPcHRpb24gJHtpfWAsXG4gICAgICBkaXNhYmxlZDogaSAlIDQgPT09IDAsXG4gICAgfSlcbiAgfVxuICByZXR1cm4gZGF0YVxufVxuXG5jb25zdCBkYXRhID0gcmVmPE9wdGlvbltdPihnZW5lcmF0ZURhdGEoKSlcbmNvbnN0IHZhbHVlID0gcmVmKFtdKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/transfer/prop-alias.vue)_

vue

```
<template>
  <el-transfer
    v-model="value"
    :props="{
      key: 'value',
      label: 'desc',
    }"
    :data="data"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Option {
  value: number
  desc: string
  disabled: boolean
}

const generateData = () => {
  const data: Option[] = []
  for (let i = 1; i <= 15; i++) {
    data.push({
      value: i,
      desc: `Option ${i}`,
      disabled: i % 4 === 0,
    })
  }
  return data
}

const data = ref<Option[]>(generateData())
const value = ref([])
</script>
```

隐藏源代码

## Transfer API [​](#transfer-api)

### Transfer Attributes [​](#transfer-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `array` | \[\] |
| data | Transfer 的数据源 | `array` | \[\] |
| filterable | 是否可搜索 | `boolean` | false |
| filter-placeholder | 搜索框占位符 | `string` | — |
| filter-method | 自定义搜索方法 | `Function` | — |
| target-order | 右侧列表元素的排序策略： 若为 `original`，则保持与数据源相同的顺序； 若为 `push`，则新加入的元素排在最后； 若为 `unshift`，则新加入的元素排在最前 | `enum` | original |
| titles | 自定义列表标题 | `array` | \[\] |
| button-texts | 自定义按钮文案 | `array` | \[\] |
| render-content | 自定义数据项渲染函数 | `object` | — |
| format | 列表顶部勾选状态文案 | `object` | {} |
| [props](#type-declarations) | 数据源的字段别名 | `object` | — |
| left-default-checked | 初始状态下左侧列表的已勾选项的 key 数组 | `array` | \[\] |
| right-default-checked | 初始状态下右侧列表的已勾选项的 key 数组 | `array` | \[\] |
| validate-event | 是否触发表单验证 | `boolean` | true |

### Transfer Events [​](#transfer-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 右侧列表元素变化时触发 | `Function` |
| left-check-change | 左侧列表元素被用户选中 / 取消选中时触发 | `Function` |
| right-check-change | 右侧列表元素被用户选中 / 取消选中时触发 | `Function` |

### Transfer Slots [​](#transfer-slots)

| 插槽名 | 说明 | 类型 |
| --- | --- | --- |
| default | 自定义数据项的内容， | `object` |
| left-footer | 左侧列表底部的内容 | — |
| right-footer | 右侧列表底部的内容 | — |
| left-empty 2.9.0 | 左侧面板为空或没有数据符合筛选条件时的内容 | — |
| right-empty 2.9.0 | 右侧面板为空或没有数据符合筛选条件时的内容 | — |

### Transfer Exposes [​](#transfer-exposes)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| clearQuery | 清空某个面板的搜索关键词 | `Function` |
| leftPanel | 左侧面板 ref | `object` |
| rightPanel | 右侧面板 ref | `object` |

## Transfer Panel API [​](#transfer-panel-api)

### Transfer Panel Exposes [​](#transfer-panel-exposes)

| 名称 | 描述 | Type |
| --- | --- | --- |
| query | 过滤关键词 | `string` |

## Type Declarations [​](#type-declarations)

显示类型声明

ts

```
import type { h as H, VNode } from 'vue'

type TransferKey = string | number

type TransferDirection = 'left' | 'right'

type TransferDataItem = Record<string, any>

type renderContent<T extends TransferDataItem = TransferDataItem> = (
  h: typeof H,
  option: T
) => VNode | VNode[]

interface TransferFormat {
  noChecked?: string
  hasChecked?: string
}

interface TransferPropsAlias {
  label?: string
  key?: string
  disabled?: string
}
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/transfer) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/transfer.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/transfer.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/50254496?v=4&size=64)](https://github.com/LoTwT)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/22429236?v=4&size=64)](https://github.com/zongzi531)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/54931083?v=4&size=64)](https://github.com/wjp980108)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/80675236?v=4&size=64)](https://github.com/evan2306)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/134276765?v=4&size=64)](https://github.com/zwgwf)[![](https://avatars.githubusercontent.com/u/19986739?v=4&size=64)](https://github.com/wjw-gavin)[![](https://avatars.githubusercontent.com/u/2755933?v=4&size=64)](https://github.com/BiosSun)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/54823984?v=4&size=64)](https://github.com/gezhiheng)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)

[Time Select 时间选择](https://element-plus.org/zh-CN/component/time-select)

[TreeSelect 树形选择](https://element-plus.org/zh-CN/component/tree-select)


