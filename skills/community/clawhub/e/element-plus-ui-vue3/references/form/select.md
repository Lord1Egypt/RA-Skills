---
name: "select"
description: "Select 选择器 -- Element Plus Vue3 桌面端组件。Invoke when user needs Select 选择器 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/select.html"
---

---

# Select 选择器 [​](#select-选择器)

更新日志待解决

89

当选项过多时，使用下拉菜单展示并选择内容。

TIP

在版本 `2.5.0`之后， `el-select` 的默认宽度更改为 `100%` 当使用内联形式时，宽度将显示异常。 为了保持显示正常, 您需要手动配置 `el-select` 的宽度 (如: [例子](https://github.com/element-plus/element-plus/issues/15834#issuecomment-1936919229)).

## 基础用法 [​](#基础用法)

适用广泛的基础单选 `v-model` 的值为当前被选中的 `el-option` 的 value 属性值

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0IHYtbW9kZWw9XCJ2YWx1ZVwiIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIj5cbiAgICA8ZWwtb3B0aW9uXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICA6a2V5PVwiaXRlbS52YWx1ZVwiXG4gICAgICA6bGFiZWw9XCJpdGVtLmxhYmVsXCJcbiAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgIC8+XG4gIDwvZWwtc2VsZWN0PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoJycpXG5cbmNvbnN0IG9wdGlvbnMgPSBbXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjEnLFxuICAgIGxhYmVsOiAnT3B0aW9uMScsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjInLFxuICAgIGxhYmVsOiAnT3B0aW9uMicsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjMnLFxuICAgIGxhYmVsOiAnT3B0aW9uMycsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjQnLFxuICAgIGxhYmVsOiAnT3B0aW9uNCcsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjUnLFxuICAgIGxhYmVsOiAnT3B0aW9uNScsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/basic-usage.vue)_

vue

```
<template>
  <el-select v-model="value" placeholder="Select" style="width: 240px">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')

const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
</script>
```

隐藏源代码

## Options 属性 2.10.5 [​](#options-属性)

`el-option` 基本用法。 您可以通过 `props` 属性自定义 `options` 的别名。

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0XG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgIDpwcm9wcz1cInByb3BzXCJcbiAgICBwbGFjZWhvbGRlcj1cIlNlbGVjdFwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoJycpXG5cbmNvbnN0IHByb3BzID0ge1xuICB2YWx1ZTogJ2lkJyxcbiAgbGFiZWw6ICdsYWJlbCcsXG4gIG9wdGlvbnM6ICdvcHRpb25zJyxcbiAgZGlzYWJsZWQ6ICdkaXNhYmxlZCcsXG59XG5cbmNvbnN0IG9wdGlvbnMgPSBbXG4gIHtcbiAgICBpZDogJ09wdGlvbjEnLFxuICAgIGxhYmVsOiAnT3B0aW9uMScsXG4gIH0sXG4gIHtcbiAgICBpZDogJ09wdGlvbjInLFxuICAgIGxhYmVsOiAnT3B0aW9uMicsXG4gICAgZGlzYWJsZWQ6IHRydWUsXG4gIH0sXG4gIHtcbiAgICBpZDogJ09wdGlvbjMnLFxuICAgIGxhYmVsOiAnT3B0aW9uMycsXG4gIH0sXG4gIHtcbiAgICBpZDogJ09wdGlvbjQnLFxuICAgIGxhYmVsOiAnT3B0aW9uNCcsXG4gICAgZGlzYWJsZWQ6IHRydWUsXG4gIH0sXG4gIHtcbiAgICBpZDogJ09wdGlvbjUnLFxuICAgIGxhYmVsOiAnT3B0aW9uNScsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/options.vue)_

vue

```
<template>
  <el-select
    v-model="value"
    :options="options"
    :props="props"
    placeholder="Select"
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')

const props = {
  value: 'id',
  label: 'label',
  options: 'options',
  disabled: 'disabled',
}

const options = [
  {
    id: 'Option1',
    label: 'Option1',
  },
  {
    id: 'Option2',
    label: 'Option2',
    disabled: true,
  },
  {
    id: 'Option3',
    label: 'Option3',
  },
  {
    id: 'Option4',
    label: 'Option4',
    disabled: true,
  },
  {
    id: 'Option5',
    label: 'Option5',
  },
]
</script>
```

隐藏源代码

## 有禁用选项 [​](#有禁用选项)

在 `el-option` 中，设定 `disabled` 值为 true，即可禁用该选项

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0IHYtbW9kZWw9XCJ2YWx1ZVwiIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIj5cbiAgICA8ZWwtb3B0aW9uXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICA6a2V5PVwiaXRlbS52YWx1ZVwiXG4gICAgICA6bGFiZWw9XCJpdGVtLmxhYmVsXCJcbiAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgICAgOmRpc2FibGVkPVwiaXRlbS5kaXNhYmxlZFwiXG4gICAgLz5cbiAgPC9lbC1zZWxlY3Q+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZignJylcbmNvbnN0IG9wdGlvbnMgPSBbXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjEnLFxuICAgIGxhYmVsOiAnT3B0aW9uMScsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjInLFxuICAgIGxhYmVsOiAnT3B0aW9uMicsXG4gICAgZGlzYWJsZWQ6IHRydWUsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjMnLFxuICAgIGxhYmVsOiAnT3B0aW9uMycsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjQnLFxuICAgIGxhYmVsOiAnT3B0aW9uNCcsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjUnLFxuICAgIGxhYmVsOiAnT3B0aW9uNScsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/disabled-option.vue)_

vue

```
<template>
  <el-select v-model="value" placeholder="Select" style="width: 240px">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
      :disabled="item.disabled"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
    disabled: true,
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
</script>
```

隐藏源代码

## 禁用状态 [​](#禁用状态)

禁用整个选择器组件

为 `el-select` 设置 `disabled`属性，则整个选择器不可用。

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0IHYtbW9kZWw9XCJ2YWx1ZVwiIGRpc2FibGVkIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIj5cbiAgICA8ZWwtb3B0aW9uXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICA6a2V5PVwiaXRlbS52YWx1ZVwiXG4gICAgICA6bGFiZWw9XCJpdGVtLmxhYmVsXCJcbiAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgIC8+XG4gIDwvZWwtc2VsZWN0PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoJycpXG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICdPcHRpb24xJyxcbiAgICBsYWJlbDogJ09wdGlvbjEnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdPcHRpb24yJyxcbiAgICBsYWJlbDogJ09wdGlvbjInLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdPcHRpb24zJyxcbiAgICBsYWJlbDogJ09wdGlvbjMnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdPcHRpb240JyxcbiAgICBsYWJlbDogJ09wdGlvbjQnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdPcHRpb241JyxcbiAgICBsYWJlbDogJ09wdGlvbjUnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/disabled.vue)_

vue

```
<template>
  <el-select v-model="value" disabled placeholder="Select" style="width: 240px">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
</script>
```

隐藏源代码

## 可清空 [​](#可清空)

您可以使用清除图标来清除选择。

为 `el-select` 设置 `clearable` 属性，则可将选择器清空。

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0XG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICBjbGVhcmFibGVcbiAgICBwbGFjZWhvbGRlcj1cIlNlbGVjdFwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICA+XG4gICAgPGVsLW9wdGlvblxuICAgICAgdi1mb3I9XCJpdGVtIGluIG9wdGlvbnNcIlxuICAgICAgOmtleT1cIml0ZW0udmFsdWVcIlxuICAgICAgOmxhYmVsPVwiaXRlbS5sYWJlbFwiXG4gICAgICA6dmFsdWU9XCJpdGVtLnZhbHVlXCJcbiAgICAvPlxuICA8L2VsLXNlbGVjdD5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCcnKVxuY29uc3Qgb3B0aW9ucyA9IFtcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uMScsXG4gICAgbGFiZWw6ICdPcHRpb24xJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uMicsXG4gICAgbGFiZWw6ICdPcHRpb24yJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uMycsXG4gICAgbGFiZWw6ICdPcHRpb24zJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uNCcsXG4gICAgbGFiZWw6ICdPcHRpb240JyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uNScsXG4gICAgbGFiZWw6ICdPcHRpb241JyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/clearable.vue)_

vue

```
<template>
  <el-select
    v-model="value"
    clearable
    placeholder="Select"
    style="width: 240px"
  >
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
</script>
```

隐藏源代码

## 尺寸 [​](#尺寸)

使用 `size` 属性改变选择器大小。 除了默认大小外，还有另外两个选项： `large`, `small`。

Select

Select

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTQgaXRlbXMtY2VudGVyXCI+XG4gICAgPGVsLXNlbGVjdFxuICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCJcbiAgICAgIHNpemU9XCJsYXJnZVwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgPlxuICAgICAgPGVsLW9wdGlvblxuICAgICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgICAgOmxhYmVsPVwiaXRlbS5sYWJlbFwiXG4gICAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgICAgLz5cbiAgICA8L2VsLXNlbGVjdD5cbiAgICA8ZWwtc2VsZWN0IHYtbW9kZWw9XCJ2YWx1ZVwiIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIj5cbiAgICAgIDxlbC1vcHRpb25cbiAgICAgICAgdi1mb3I9XCJpdGVtIGluIG9wdGlvbnNcIlxuICAgICAgICA6a2V5PVwiaXRlbS52YWx1ZVwiXG4gICAgICAgIDpsYWJlbD1cIml0ZW0ubGFiZWxcIlxuICAgICAgICA6dmFsdWU9XCJpdGVtLnZhbHVlXCJcbiAgICAgIC8+XG4gICAgPC9lbC1zZWxlY3Q+XG4gICAgPGVsLXNlbGVjdFxuICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCJcbiAgICAgIHNpemU9XCJzbWFsbFwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgPlxuICAgICAgPGVsLW9wdGlvblxuICAgICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgICAgOmxhYmVsPVwiaXRlbS5sYWJlbFwiXG4gICAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgICAgLz5cbiAgICA8L2VsLXNlbGVjdD5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZignJylcblxuY29uc3Qgb3B0aW9ucyA9IFtcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uMScsXG4gICAgbGFiZWw6ICdPcHRpb24xJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uMicsXG4gICAgbGFiZWw6ICdPcHRpb24yJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uMycsXG4gICAgbGFiZWw6ICdPcHRpb24zJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uNCcsXG4gICAgbGFiZWw6ICdPcHRpb240JyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uNScsXG4gICAgbGFiZWw6ICdPcHRpb241JyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/size.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-4 items-center">
    <el-select
      v-model="value"
      placeholder="Select"
      size="large"
      style="width: 240px"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-select v-model="value" placeholder="Select" style="width: 240px">
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-select
      v-model="value"
      placeholder="Select"
      size="small"
      style="width: 240px"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')

const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
</script>
```

隐藏源代码

## 基础多选 [​](#基础多选)

多选选择器使用 tag 组件来展示已选中的选项。

为 `el-select` 设置 `multiple` 属性即可启用多选， 此时 `v-model` 的值为当前选中值所组成的数组。 默认情况下选中值会以 Tag 组件的形式展现， 你也可以设置 `collapse-tags` 属性将它们合并为一段文字。 您可以使用 `collapse-tags-tooltip` 属性来启用鼠标悬停折叠文字以显示具体所选值的行为。

default

Select

use collapse-tags

Select

use collapse-tags-tooltip

Select

use max-collapse-tags

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+ZGVmYXVsdDwvcD5cbiAgICA8ZWwtc2VsZWN0XG4gICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgIG11bHRpcGxlXG4gICAgICBwbGFjZWhvbGRlcj1cIlNlbGVjdFwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgPlxuICAgICAgPGVsLW9wdGlvblxuICAgICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgICAgOmxhYmVsPVwiaXRlbS5sYWJlbFwiXG4gICAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgICAgLz5cbiAgICA8L2VsLXNlbGVjdD5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJtLTRcIj5cbiAgICA8cD51c2UgY29sbGFwc2UtdGFnczwvcD5cbiAgICA8ZWwtc2VsZWN0XG4gICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgIG11bHRpcGxlXG4gICAgICBjb2xsYXBzZS10YWdzXG4gICAgICBwbGFjZWhvbGRlcj1cIlNlbGVjdFwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgPlxuICAgICAgPGVsLW9wdGlvblxuICAgICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgICAgOmxhYmVsPVwiaXRlbS5sYWJlbFwiXG4gICAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgICAgLz5cbiAgICA8L2VsLXNlbGVjdD5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJtLTRcIj5cbiAgICA8cD51c2UgY29sbGFwc2UtdGFncy10b29sdGlwPC9wPlxuICAgIDxlbC1zZWxlY3RcbiAgICAgIHYtbW9kZWw9XCJ2YWx1ZTNcIlxuICAgICAgbXVsdGlwbGVcbiAgICAgIGNvbGxhcHNlLXRhZ3NcbiAgICAgIGNvbGxhcHNlLXRhZ3MtdG9vbHRpcFxuICAgICAgcGxhY2Vob2xkZXI9XCJTZWxlY3RcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgID5cbiAgICAgIDxlbC1vcHRpb25cbiAgICAgICAgdi1mb3I9XCJpdGVtIGluIG9wdGlvbnNcIlxuICAgICAgICA6a2V5PVwiaXRlbS52YWx1ZVwiXG4gICAgICAgIDpsYWJlbD1cIml0ZW0ubGFiZWxcIlxuICAgICAgICA6dmFsdWU9XCJpdGVtLnZhbHVlXCJcbiAgICAgIC8+XG4gICAgPC9lbC1zZWxlY3Q+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+dXNlIG1heC1jb2xsYXBzZS10YWdzPC9wPlxuICAgIDxlbC1zZWxlY3RcbiAgICAgIHYtbW9kZWw9XCJ2YWx1ZTRcIlxuICAgICAgbXVsdGlwbGVcbiAgICAgIGNvbGxhcHNlLXRhZ3NcbiAgICAgIGNvbGxhcHNlLXRhZ3MtdG9vbHRpcFxuICAgICAgOm1heC1jb2xsYXBzZS10YWdzPVwiM1wiXG4gICAgICBwbGFjZWhvbGRlcj1cIlNlbGVjdFwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgPlxuICAgICAgPGVsLW9wdGlvblxuICAgICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgICAgOmxhYmVsPVwiaXRlbS5sYWJlbFwiXG4gICAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgICAgLz5cbiAgICA8L2VsLXNlbGVjdD5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZTEgPSByZWYoW10pXG5jb25zdCB2YWx1ZTIgPSByZWYoW10pXG5jb25zdCB2YWx1ZTMgPSByZWYoW10pXG5jb25zdCB2YWx1ZTQgPSByZWYoW10pXG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICdPcHRpb24xJyxcbiAgICBsYWJlbDogJ09wdGlvbjEnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdPcHRpb24yJyxcbiAgICBsYWJlbDogJ09wdGlvbjInLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdPcHRpb24zJyxcbiAgICBsYWJlbDogJ09wdGlvbjMnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdPcHRpb240JyxcbiAgICBsYWJlbDogJ09wdGlvbjQnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdPcHRpb241JyxcbiAgICBsYWJlbDogJ09wdGlvbjUnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/multiple.vue)_

vue

```
<template>
  <div class="m-4">
    <p>default</p>
    <el-select
      v-model="value1"
      multiple
      placeholder="Select"
      style="width: 240px"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>
  <div class="m-4">
    <p>use collapse-tags</p>
    <el-select
      v-model="value2"
      multiple
      collapse-tags
      placeholder="Select"
      style="width: 240px"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>
  <div class="m-4">
    <p>use collapse-tags-tooltip</p>
    <el-select
      v-model="value3"
      multiple
      collapse-tags
      collapse-tags-tooltip
      placeholder="Select"
      style="width: 240px"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>
  <div class="m-4">
    <p>use max-collapse-tags</p>
    <el-select
      v-model="value4"
      multiple
      collapse-tags
      collapse-tags-tooltip
      :max-collapse-tags="3"
      placeholder="Select"
      style="width: 240px"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref([])
const value2 = ref([])
const value3 = ref([])
const value4 = ref([])
const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
</script>
```

隐藏源代码

## 自定义模板 [​](#自定义模板)

你可以自定义如何来渲染每一个选项。

将自定义的 HTML 模板插入 `el-option` 的 slot 中即可。

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0IHYtbW9kZWw9XCJ2YWx1ZVwiIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIj5cbiAgICA8ZWwtb3B0aW9uXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gY2l0aWVzXCJcbiAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgIDpsYWJlbD1cIml0ZW0ubGFiZWxcIlxuICAgICAgOnZhbHVlPVwiaXRlbS52YWx1ZVwiXG4gICAgPlxuICAgICAgPHNwYW4gc3R5bGU9XCJmbG9hdDogbGVmdFwiPnt7IGl0ZW0ubGFiZWwgfX08L3NwYW4+XG4gICAgICA8c3BhblxuICAgICAgICBzdHlsZT1cIlxuICAgICAgICAgIGZsb2F0OiByaWdodDtcbiAgICAgICAgICBjb2xvcjogdmFyKC0tZWwtdGV4dC1jb2xvci1zZWNvbmRhcnkpO1xuICAgICAgICAgIGZvbnQtc2l6ZTogMTNweDtcbiAgICAgICAgXCJcbiAgICAgID5cbiAgICAgICAge3sgaXRlbS52YWx1ZSB9fVxuICAgICAgPC9zcGFuPlxuICAgIDwvZWwtb3B0aW9uPlxuICA8L2VsLXNlbGVjdD5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCcnKVxuY29uc3QgY2l0aWVzID0gW1xuICB7XG4gICAgdmFsdWU6ICdCZWlqaW5nJyxcbiAgICBsYWJlbDogJ0JlaWppbmcnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdTaGFuZ2hhaScsXG4gICAgbGFiZWw6ICdTaGFuZ2hhaScsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ05hbmppbmcnLFxuICAgIGxhYmVsOiAnTmFuamluZycsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ0NoZW5nZHUnLFxuICAgIGxhYmVsOiAnQ2hlbmdkdScsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ1NoZW56aGVuJyxcbiAgICBsYWJlbDogJ1NoZW56aGVuJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnR3Vhbmd6aG91JyxcbiAgICBsYWJlbDogJ0d1YW5nemhvdScsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/custom-template.vue)_

vue

```
<template>
  <el-select v-model="value" placeholder="Select" style="width: 240px">
    <el-option
      v-for="item in cities"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    >
      <span style="float: left">{{ item.label }}</span>
      <span
        style="
          float: right;
          color: var(--el-text-color-secondary);
          font-size: 13px;
        "
      >
        {{ item.value }}
      </span>
    </el-option>
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
const cities = [
  {
    value: 'Beijing',
    label: 'Beijing',
  },
  {
    value: 'Shanghai',
    label: 'Shanghai',
  },
  {
    value: 'Nanjing',
    label: 'Nanjing',
  },
  {
    value: 'Chengdu',
    label: 'Chengdu',
  },
  {
    value: 'Shenzhen',
    label: 'Shenzhen',
  },
  {
    value: 'Guangzhou',
    label: 'Guangzhou',
  },
]
</script>
```

隐藏源代码

## 自定义下拉菜单的头部 2.4.3 [​](#自定义下拉菜单的头部)

您可以自定义下拉菜单的头部。

Use slot to customize the content.

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0XG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICBtdWx0aXBsZVxuICAgIGNsZWFyYWJsZVxuICAgIGNvbGxhcHNlLXRhZ3NcbiAgICBwbGFjZWhvbGRlcj1cIlNlbGVjdFwiXG4gICAgcG9wcGVyLWNsYXNzPVwiY3VzdG9tLWhlYWRlclwiXG4gICAgOm1heC1jb2xsYXBzZS10YWdzPVwiMVwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICA+XG4gICAgPHRlbXBsYXRlICNoZWFkZXI+XG4gICAgICA8ZWwtY2hlY2tib3hcbiAgICAgICAgdi1tb2RlbD1cImNoZWNrQWxsXCJcbiAgICAgICAgOmluZGV0ZXJtaW5hdGU9XCJpbmRldGVybWluYXRlXCJcbiAgICAgICAgQGNoYW5nZT1cImhhbmRsZUNoZWNrQWxsXCJcbiAgICAgID5cbiAgICAgICAgQWxsXG4gICAgICA8L2VsLWNoZWNrYm94PlxuICAgIDwvdGVtcGxhdGU+XG4gICAgPGVsLW9wdGlvblxuICAgICAgdi1mb3I9XCJpdGVtIGluIGNpdGllc1wiXG4gICAgICA6a2V5PVwiaXRlbS52YWx1ZVwiXG4gICAgICA6bGFiZWw9XCJpdGVtLmxhYmVsXCJcbiAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgIC8+XG4gIDwvZWwtc2VsZWN0PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiwgd2F0Y2ggfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgQ2hlY2tib3hWYWx1ZVR5cGUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGNoZWNrQWxsID0gcmVmKGZhbHNlKVxuY29uc3QgaW5kZXRlcm1pbmF0ZSA9IHJlZihmYWxzZSlcbmNvbnN0IHZhbHVlID0gcmVmPENoZWNrYm94VmFsdWVUeXBlW10+KFtdKVxuY29uc3QgY2l0aWVzID0gcmVmKFtcbiAge1xuICAgIHZhbHVlOiAnQmVpamluZycsXG4gICAgbGFiZWw6ICdCZWlqaW5nJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnU2hhbmdoYWknLFxuICAgIGxhYmVsOiAnU2hhbmdoYWknLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdOYW5qaW5nJyxcbiAgICBsYWJlbDogJ05hbmppbmcnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdDaGVuZ2R1JyxcbiAgICBsYWJlbDogJ0NoZW5nZHUnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdTaGVuemhlbicsXG4gICAgbGFiZWw6ICdTaGVuemhlbicsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ0d1YW5nemhvdScsXG4gICAgbGFiZWw6ICdHdWFuZ3pob3UnLFxuICB9LFxuXSlcblxud2F0Y2godmFsdWUsICh2YWwpID0+IHtcbiAgaWYgKHZhbC5sZW5ndGggPT09IDApIHtcbiAgICBjaGVja0FsbC52YWx1ZSA9IGZhbHNlXG4gICAgaW5kZXRlcm1pbmF0ZS52YWx1ZSA9IGZhbHNlXG4gIH0gZWxzZSBpZiAodmFsLmxlbmd0aCA9PT0gY2l0aWVzLnZhbHVlLmxlbmd0aCkge1xuICAgIGNoZWNrQWxsLnZhbHVlID0gdHJ1ZVxuICAgIGluZGV0ZXJtaW5hdGUudmFsdWUgPSBmYWxzZVxuICB9IGVsc2Uge1xuICAgIGluZGV0ZXJtaW5hdGUudmFsdWUgPSB0cnVlXG4gIH1cbn0pXG5cbmNvbnN0IGhhbmRsZUNoZWNrQWxsID0gKHZhbDogQ2hlY2tib3hWYWx1ZVR5cGUpID0+IHtcbiAgaW5kZXRlcm1pbmF0ZS52YWx1ZSA9IGZhbHNlXG4gIGlmICh2YWwpIHtcbiAgICB2YWx1ZS52YWx1ZSA9IGNpdGllcy52YWx1ZS5tYXAoKF8pID0+IF8udmFsdWUpXG4gIH0gZWxzZSB7XG4gICAgdmFsdWUudmFsdWUgPSBbXVxuICB9XG59XG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLmN1c3RvbS1oZWFkZXIge1xuICAuZWwtY2hlY2tib3gge1xuICAgIGRpc3BsYXk6IGZsZXg7XG4gICAgaGVpZ2h0OiB1bnNldDtcbiAgfVxufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/custom-header.vue)_

vue

```
<template>
  <el-select
    v-model="value"
    multiple
    clearable
    collapse-tags
    placeholder="Select"
    popper-class="custom-header"
    :max-collapse-tags="1"
    style="width: 240px"
  >
    <template #header>
      <el-checkbox
        v-model="checkAll"
        :indeterminate="indeterminate"
        @change="handleCheckAll"
      >
        All
      </el-checkbox>
    </template>
    <el-option
      v-for="item in cities"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

import type { CheckboxValueType } from 'element-plus'

const checkAll = ref(false)
const indeterminate = ref(false)
const value = ref<CheckboxValueType[]>([])
const cities = ref([
  {
    value: 'Beijing',
    label: 'Beijing',
  },
  {
    value: 'Shanghai',
    label: 'Shanghai',
  },
  {
    value: 'Nanjing',
    label: 'Nanjing',
  },
  {
    value: 'Chengdu',
    label: 'Chengdu',
  },
  {
    value: 'Shenzhen',
    label: 'Shenzhen',
  },
  {
    value: 'Guangzhou',
    label: 'Guangzhou',
  },
])

watch(value, (val) => {
  if (val.length === 0) {
    checkAll.value = false
    indeterminate.value = false
  } else if (val.length === cities.value.length) {
    checkAll.value = true
    indeterminate.value = false
  } else {
    indeterminate.value = true
  }
})

const handleCheckAll = (val: CheckboxValueType) => {
  indeterminate.value = false
  if (val) {
    value.value = cities.value.map((_) => _.value)
  } else {
    value.value = []
  }
}
</script>

<style>
.custom-header {
  .el-checkbox {
    display: flex;
    height: unset;
  }
}
</style>
```

隐藏源代码

## 自定义下拉菜单的底部 2.4.3 [​](#自定义下拉菜单的底部)

您可以自定义下拉菜单的底部。

使用slot 自定义内容

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0IHYtbW9kZWw9XCJ2YWx1ZVwiIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIj5cbiAgICA8ZWwtb3B0aW9uXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gY2l0aWVzXCJcbiAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgIDpsYWJlbD1cIml0ZW0ubGFiZWxcIlxuICAgICAgOnZhbHVlPVwiaXRlbS52YWx1ZVwiXG4gICAgLz5cbiAgICA8dGVtcGxhdGUgI2Zvb3Rlcj5cbiAgICAgIDxlbC1idXR0b24gdi1pZj1cIiFpc0FkZGluZ1wiIHRleHQgYmcgc2l6ZT1cInNtYWxsXCIgQGNsaWNrPVwib25BZGRPcHRpb25cIj5cbiAgICAgICAgQWRkIGFuIG9wdGlvblxuICAgICAgPC9lbC1idXR0b24+XG4gICAgICA8dGVtcGxhdGUgdi1lbHNlPlxuICAgICAgICA8ZWwtaW5wdXRcbiAgICAgICAgICB2LW1vZGVsPVwib3B0aW9uTmFtZVwiXG4gICAgICAgICAgY2xhc3M9XCJvcHRpb24taW5wdXRcIlxuICAgICAgICAgIHBsYWNlaG9sZGVyPVwiaW5wdXQgb3B0aW9uIG5hbWVcIlxuICAgICAgICAgIHNpemU9XCJzbWFsbFwiXG4gICAgICAgIC8+XG4gICAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBzaXplPVwic21hbGxcIiBAY2xpY2s9XCJvbkNvbmZpcm1cIj5cbiAgICAgICAgICBjb25maXJtXG4gICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgICA8ZWwtYnV0dG9uIHNpemU9XCJzbWFsbFwiIEBjbGljaz1cImNsZWFyXCI+Y2FuY2VsPC9lbC1idXR0b24+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtc2VsZWN0PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBDaGVja2JveFZhbHVlVHlwZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgaXNBZGRpbmcgPSByZWYoZmFsc2UpXG5jb25zdCB2YWx1ZSA9IHJlZjxDaGVja2JveFZhbHVlVHlwZVtdPihbXSlcbmNvbnN0IG9wdGlvbk5hbWUgPSByZWYoJycpXG5jb25zdCBjaXRpZXMgPSByZWYoW1xuICB7XG4gICAgdmFsdWU6ICdCZWlqaW5nJyxcbiAgICBsYWJlbDogJ0JlaWppbmcnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdTaGFuZ2hhaScsXG4gICAgbGFiZWw6ICdTaGFuZ2hhaScsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ05hbmppbmcnLFxuICAgIGxhYmVsOiAnTmFuamluZycsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ0NoZW5nZHUnLFxuICAgIGxhYmVsOiAnQ2hlbmdkdScsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ1NoZW56aGVuJyxcbiAgICBsYWJlbDogJ1NoZW56aGVuJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnR3Vhbmd6aG91JyxcbiAgICBsYWJlbDogJ0d1YW5nemhvdScsXG4gIH0sXG5dKVxuXG5jb25zdCBvbkFkZE9wdGlvbiA9ICgpID0+IHtcbiAgaXNBZGRpbmcudmFsdWUgPSB0cnVlXG59XG5cbmNvbnN0IG9uQ29uZmlybSA9ICgpID0+IHtcbiAgaWYgKG9wdGlvbk5hbWUudmFsdWUpIHtcbiAgICBjaXRpZXMudmFsdWUucHVzaCh7XG4gICAgICBsYWJlbDogb3B0aW9uTmFtZS52YWx1ZSxcbiAgICAgIHZhbHVlOiBvcHRpb25OYW1lLnZhbHVlLFxuICAgIH0pXG4gICAgY2xlYXIoKVxuICB9XG59XG5cbmNvbnN0IGNsZWFyID0gKCkgPT4ge1xuICBvcHRpb25OYW1lLnZhbHVlID0gJydcbiAgaXNBZGRpbmcudmFsdWUgPSBmYWxzZVxufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5vcHRpb24taW5wdXQge1xuICB3aWR0aDogMTAwJTtcbiAgbWFyZ2luLWJvdHRvbTogOHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/custom-footer.vue)_

vue

```
<template>
  <el-select v-model="value" placeholder="Select" style="width: 240px">
    <el-option
      v-for="item in cities"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
    <template #footer>
      <el-button v-if="!isAdding" text bg size="small" @click="onAddOption">
        Add an option
      </el-button>
      <template v-else>
        <el-input
          v-model="optionName"
          class="option-input"
          placeholder="input option name"
          size="small"
        />
        <el-button type="primary" size="small" @click="onConfirm">
          confirm
        </el-button>
        <el-button size="small" @click="clear">cancel</el-button>
      </template>
    </template>
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { CheckboxValueType } from 'element-plus'

const isAdding = ref(false)
const value = ref<CheckboxValueType[]>([])
const optionName = ref('')
const cities = ref([
  {
    value: 'Beijing',
    label: 'Beijing',
  },
  {
    value: 'Shanghai',
    label: 'Shanghai',
  },
  {
    value: 'Nanjing',
    label: 'Nanjing',
  },
  {
    value: 'Chengdu',
    label: 'Chengdu',
  },
  {
    value: 'Shenzhen',
    label: 'Shenzhen',
  },
  {
    value: 'Guangzhou',
    label: 'Guangzhou',
  },
])

const onAddOption = () => {
  isAdding.value = true
}

const onConfirm = () => {
  if (optionName.value) {
    cities.value.push({
      label: optionName.value,
      value: optionName.value,
    })
    clear()
  }
}

const clear = () => {
  optionName.value = ''
  isAdding.value = false
}
</script>

<style>
.option-input {
  width: 100%;
  margin-bottom: 8px;
}
</style>
```

隐藏源代码

## 将选项进行分组 [​](#将选项进行分组)

你可以为选项进行分组来区分不同的选项

使用 `el-option-group` 对备选项进行分组，它的 `label` 属性为分组名

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0IHYtbW9kZWw9XCJ2YWx1ZVwiIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIj5cbiAgICA8ZWwtb3B0aW9uLWdyb3VwXG4gICAgICB2LWZvcj1cImdyb3VwIGluIG9wdGlvbnNcIlxuICAgICAgOmtleT1cImdyb3VwLmxhYmVsXCJcbiAgICAgIDpsYWJlbD1cImdyb3VwLmxhYmVsXCJcbiAgICA+XG4gICAgICA8ZWwtb3B0aW9uXG4gICAgICAgIHYtZm9yPVwiaXRlbSBpbiBncm91cC5vcHRpb25zXCJcbiAgICAgICAgOmtleT1cIml0ZW0udmFsdWVcIlxuICAgICAgICA6bGFiZWw9XCJpdGVtLmxhYmVsXCJcbiAgICAgICAgOnZhbHVlPVwiaXRlbS52YWx1ZVwiXG4gICAgICAvPlxuICAgIDwvZWwtb3B0aW9uLWdyb3VwPlxuICA8L2VsLXNlbGVjdD5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCcnKVxuY29uc3Qgb3B0aW9ucyA9IFtcbiAge1xuICAgIGxhYmVsOiAnUG9wdWxhciBjaXRpZXMnLFxuICAgIG9wdGlvbnM6IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdTaGFuZ2hhaScsXG4gICAgICAgIGxhYmVsOiAnU2hhbmdoYWknLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdCZWlqaW5nJyxcbiAgICAgICAgbGFiZWw6ICdCZWlqaW5nJyxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAnQ2l0eSBuYW1lJyxcbiAgICBvcHRpb25zOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnQ2hlbmdkdScsXG4gICAgICAgIGxhYmVsOiAnQ2hlbmdkdScsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ1NoZW56aGVuJyxcbiAgICAgICAgbGFiZWw6ICdTaGVuemhlbicsXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ0d1YW5nemhvdScsXG4gICAgICAgIGxhYmVsOiAnR3Vhbmd6aG91JyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnRGFsaWFuJyxcbiAgICAgICAgbGFiZWw6ICdEYWxpYW4nLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/grouping.vue)_

vue

```
<template>
  <el-select v-model="value" placeholder="Select" style="width: 240px">
    <el-option-group
      v-for="group in options"
      :key="group.label"
      :label="group.label"
    >
      <el-option
        v-for="item in group.options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-option-group>
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
const options = [
  {
    label: 'Popular cities',
    options: [
      {
        value: 'Shanghai',
        label: 'Shanghai',
      },
      {
        value: 'Beijing',
        label: 'Beijing',
      },
    ],
  },
  {
    label: 'City name',
    options: [
      {
        value: 'Chengdu',
        label: 'Chengdu',
      },
      {
        value: 'Shenzhen',
        label: 'Shenzhen',
      },
      {
        value: 'Guangzhou',
        label: 'Guangzhou',
      },
      {
        value: 'Dalian',
        label: 'Dalian',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 筛选选项 [​](#筛选选项)

可以利用筛选功能快速查找选项。

为`el-select`添加`filterable`属性即可启用搜索功能。 默认情况下，Select 会找出所有 `label` 属性包含输入值的选项。 如果希望使用其他的搜索逻辑，可以通过传入一个 `filter-method` 来实现。 `filter-method` 为一个 `Function`，它会在输入值发生变化时调用，参数为当前输入值。

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0XG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICBmaWx0ZXJhYmxlXG4gICAgcGxhY2Vob2xkZXI9XCJTZWxlY3RcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgPlxuICAgIDxlbC1vcHRpb25cbiAgICAgIHYtZm9yPVwiaXRlbSBpbiBvcHRpb25zXCJcbiAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgIDpsYWJlbD1cIml0ZW0ubGFiZWxcIlxuICAgICAgOnZhbHVlPVwiaXRlbS52YWx1ZVwiXG4gICAgLz5cbiAgPC9lbC1zZWxlY3Q+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZignJylcbmNvbnN0IG9wdGlvbnMgPSBbXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjEnLFxuICAgIGxhYmVsOiAnT3B0aW9uMScsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjInLFxuICAgIGxhYmVsOiAnT3B0aW9uMicsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjMnLFxuICAgIGxhYmVsOiAnT3B0aW9uMycsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjQnLFxuICAgIGxhYmVsOiAnT3B0aW9uNCcsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjUnLFxuICAgIGxhYmVsOiAnT3B0aW9uNScsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/filterable.vue)_

vue

```
<template>
  <el-select
    v-model="value"
    filterable
    placeholder="Select"
    style="width: 240px"
  >
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
</script>
```

隐藏源代码

## 远程搜索 [​](#远程搜索)

输入关键字以从远程服务器中查找数据。

从服务器搜索数据，输入关键字进行查找。为了启用远程搜索，需要将`filterable`和`remote`设置为`true`，同时传入一个`remote-method`。 `remote-method`为一个`Function`，它会在输入值发生变化时调用，参数为当前输入值。 需要注意的是，如果 `el-option` 是通过 `v-for` 指令渲染出来的，此时需要为 `el-option` 添加 `key` 属性， 且其值需具有唯一性，比如这个例子中的 `item.value`。

default

Please enter a keyword

use remote-show-suffix

Please enter a keyword

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXBcIj5cbiAgICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgICA8cD5kZWZhdWx0PC9wPlxuICAgICAgPGVsLXNlbGVjdFxuICAgICAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgICAgICBtdWx0aXBsZVxuICAgICAgICBmaWx0ZXJhYmxlXG4gICAgICAgIHJlbW90ZVxuICAgICAgICByZXNlcnZlLWtleXdvcmRcbiAgICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgZW50ZXIgYSBrZXl3b3JkXCJcbiAgICAgICAgOnJlbW90ZS1tZXRob2Q9XCJyZW1vdGVNZXRob2RcIlxuICAgICAgICA6bG9hZGluZz1cImxvYWRpbmdcIlxuICAgICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICA+XG4gICAgICAgIDxlbC1vcHRpb25cbiAgICAgICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICAgICAgOmtleT1cIml0ZW0udmFsdWVcIlxuICAgICAgICAgIDpsYWJlbD1cIml0ZW0ubGFiZWxcIlxuICAgICAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgICAgICAvPlxuICAgICAgPC9lbC1zZWxlY3Q+XG4gICAgPC9kaXY+XG4gICAgPGRpdiBjbGFzcz1cIm0tNFwiPlxuICAgICAgPHA+dXNlIHJlbW90ZS1zaG93LXN1ZmZpeDwvcD5cbiAgICAgIDxlbC1zZWxlY3RcbiAgICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgICAgbXVsdGlwbGVcbiAgICAgICAgZmlsdGVyYWJsZVxuICAgICAgICByZW1vdGVcbiAgICAgICAgcmVzZXJ2ZS1rZXl3b3JkXG4gICAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGVudGVyIGEga2V5d29yZFwiXG4gICAgICAgIHJlbW90ZS1zaG93LXN1ZmZpeFxuICAgICAgICA6cmVtb3RlLW1ldGhvZD1cInJlbW90ZU1ldGhvZFwiXG4gICAgICAgIDpsb2FkaW5nPVwibG9hZGluZ1wiXG4gICAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAgID5cbiAgICAgICAgPGVsLW9wdGlvblxuICAgICAgICAgIHYtZm9yPVwiaXRlbSBpbiBvcHRpb25zXCJcbiAgICAgICAgICA6a2V5PVwiaXRlbS52YWx1ZVwiXG4gICAgICAgICAgOmxhYmVsPVwiaXRlbS5sYWJlbFwiXG4gICAgICAgICAgOnZhbHVlPVwiaXRlbS52YWx1ZVwiXG4gICAgICAgIC8+XG4gICAgICA8L2VsLXNlbGVjdD5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgb25Nb3VudGVkLCByZWYgfSBmcm9tICd2dWUnXG5cbmludGVyZmFjZSBMaXN0SXRlbSB7XG4gIHZhbHVlOiBzdHJpbmdcbiAgbGFiZWw6IHN0cmluZ1xufVxuXG5jb25zdCBsaXN0ID0gcmVmPExpc3RJdGVtW10+KFtdKVxuY29uc3Qgb3B0aW9ucyA9IHJlZjxMaXN0SXRlbVtdPihbXSlcbmNvbnN0IHZhbHVlID0gcmVmPHN0cmluZ1tdPihbXSlcbmNvbnN0IGxvYWRpbmcgPSByZWYoZmFsc2UpXG5cbm9uTW91bnRlZCgoKSA9PiB7XG4gIGxpc3QudmFsdWUgPSBzdGF0ZXMubWFwKChpdGVtKSA9PiB7XG4gICAgcmV0dXJuIHsgdmFsdWU6IGB2YWx1ZToke2l0ZW19YCwgbGFiZWw6IGBsYWJlbDoke2l0ZW19YCB9XG4gIH0pXG59KVxuXG5jb25zdCByZW1vdGVNZXRob2QgPSAocXVlcnk6IHN0cmluZykgPT4ge1xuICBpZiAocXVlcnkpIHtcbiAgICBsb2FkaW5nLnZhbHVlID0gdHJ1ZVxuICAgIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgbG9hZGluZy52YWx1ZSA9IGZhbHNlXG4gICAgICBvcHRpb25zLnZhbHVlID0gbGlzdC52YWx1ZS5maWx0ZXIoKGl0ZW0pID0+IHtcbiAgICAgICAgcmV0dXJuIGl0ZW0ubGFiZWwudG9Mb3dlckNhc2UoKS5pbmNsdWRlcyhxdWVyeS50b0xvd2VyQ2FzZSgpKVxuICAgICAgfSlcbiAgICB9LCAyMDApXG4gIH0gZWxzZSB7XG4gICAgb3B0aW9ucy52YWx1ZSA9IFtdXG4gIH1cbn1cblxuY29uc3Qgc3RhdGVzID0gW1xuICAnQWxhYmFtYScsXG4gICdBbGFza2EnLFxuICAnQXJpem9uYScsXG4gICdBcmthbnNhcycsXG4gICdDYWxpZm9ybmlhJyxcbiAgJ0NvbG9yYWRvJyxcbiAgJ0Nvbm5lY3RpY3V0JyxcbiAgJ0RlbGF3YXJlJyxcbiAgJ0Zsb3JpZGEnLFxuICAnR2VvcmdpYScsXG4gICdIYXdhaWknLFxuICAnSWRhaG8nLFxuICAnSWxsaW5vaXMnLFxuICAnSW5kaWFuYScsXG4gICdJb3dhJyxcbiAgJ0thbnNhcycsXG4gICdLZW50dWNreScsXG4gICdMb3Vpc2lhbmEnLFxuICAnTWFpbmUnLFxuICAnTWFyeWxhbmQnLFxuICAnTWFzc2FjaHVzZXR0cycsXG4gICdNaWNoaWdhbicsXG4gICdNaW5uZXNvdGEnLFxuICAnTWlzc2lzc2lwcGknLFxuICAnTWlzc291cmknLFxuICAnTW9udGFuYScsXG4gICdOZWJyYXNrYScsXG4gICdOZXZhZGEnLFxuICAnTmV3IEhhbXBzaGlyZScsXG4gICdOZXcgSmVyc2V5JyxcbiAgJ05ldyBNZXhpY28nLFxuICAnTmV3IFlvcmsnLFxuICAnTm9ydGggQ2Fyb2xpbmEnLFxuICAnTm9ydGggRGFrb3RhJyxcbiAgJ09oaW8nLFxuICAnT2tsYWhvbWEnLFxuICAnT3JlZ29uJyxcbiAgJ1Blbm5zeWx2YW5pYScsXG4gICdSaG9kZSBJc2xhbmQnLFxuICAnU291dGggQ2Fyb2xpbmEnLFxuICAnU291dGggRGFrb3RhJyxcbiAgJ1Rlbm5lc3NlZScsXG4gICdUZXhhcycsXG4gICdVdGFoJyxcbiAgJ1Zlcm1vbnQnLFxuICAnVmlyZ2luaWEnLFxuICAnV2FzaGluZ3RvbicsXG4gICdXZXN0IFZpcmdpbmlhJyxcbiAgJ1dpc2NvbnNpbicsXG4gICdXeW9taW5nJyxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/remote-search.vue)_

vue

```
<template>
  <div class="flex flex-wrap">
    <div class="m-4">
      <p>default</p>
      <el-select
        v-model="value"
        multiple
        filterable
        remote
        reserve-keyword
        placeholder="Please enter a keyword"
        :remote-method="remoteMethod"
        :loading="loading"
        style="width: 240px"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </div>
    <div class="m-4">
      <p>use remote-show-suffix</p>
      <el-select
        v-model="value"
        multiple
        filterable
        remote
        reserve-keyword
        placeholder="Please enter a keyword"
        remote-show-suffix
        :remote-method="remoteMethod"
        :loading="loading"
        style="width: 240px"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

interface ListItem {
  value: string
  label: string
}

const list = ref<ListItem[]>([])
const options = ref<ListItem[]>([])
const value = ref<string[]>([])
const loading = ref(false)

onMounted(() => {
  list.value = states.map((item) => {
    return { value: `value:${item}`, label: `label:${item}` }
  })
})

const remoteMethod = (query: string) => {
  if (query) {
    loading.value = true
    setTimeout(() => {
      loading.value = false
      options.value = list.value.filter((item) => {
        return item.label.toLowerCase().includes(query.toLowerCase())
      })
    }, 200)
  } else {
    options.value = []
  }
}

const states = [
  'Alabama',
  'Alaska',
  'Arizona',
  'Arkansas',
  'California',
  'Colorado',
  'Connecticut',
  'Delaware',
  'Florida',
  'Georgia',
  'Hawaii',
  'Idaho',
  'Illinois',
  'Indiana',
  'Iowa',
  'Kansas',
  'Kentucky',
  'Louisiana',
  'Maine',
  'Maryland',
  'Massachusetts',
  'Michigan',
  'Minnesota',
  'Mississippi',
  'Missouri',
  'Montana',
  'Nebraska',
  'Nevada',
  'New Hampshire',
  'New Jersey',
  'New Mexico',
  'New York',
  'North Carolina',
  'North Dakota',
  'Ohio',
  'Oklahoma',
  'Oregon',
  'Pennsylvania',
  'Rhode Island',
  'South Carolina',
  'South Dakota',
  'Tennessee',
  'Texas',
  'Utah',
  'Vermont',
  'Virginia',
  'Washington',
  'West Virginia',
  'Wisconsin',
  'Wyoming',
]
</script>
```

隐藏源代码

## 创建新的选项 [​](#创建新的选项)

创建并选中未包含在初始选项中的条目。

通过使用 `allow-create` 属性，用户可以通过输入框创建新项目。 为了使 `allow-create` 正常工作， `filterable` 的值必须为 `true`。 本例还使用了 `default-first-option` 属性， 在该属性为 `true` 的情况下，按下回车就可以选中当前选项列表中的第一个选项，无需使用鼠标或键盘方向键进行定位。

Choose tags for your article

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0XG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICBtdWx0aXBsZVxuICAgIGZpbHRlcmFibGVcbiAgICBhbGxvdy1jcmVhdGVcbiAgICBkZWZhdWx0LWZpcnN0LW9wdGlvblxuICAgIDpyZXNlcnZlLWtleXdvcmQ9XCJmYWxzZVwiXG4gICAgcGxhY2Vob2xkZXI9XCJDaG9vc2UgdGFncyBmb3IgeW91ciBhcnRpY2xlXCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gID5cbiAgICA8ZWwtb3B0aW9uXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICA6a2V5PVwiaXRlbS52YWx1ZVwiXG4gICAgICA6bGFiZWw9XCJpdGVtLmxhYmVsXCJcbiAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgIC8+XG4gIDwvZWwtc2VsZWN0PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWY8c3RyaW5nW10+KFtdKVxuY29uc3Qgb3B0aW9ucyA9IFtcbiAge1xuICAgIHZhbHVlOiAnSFRNTCcsXG4gICAgbGFiZWw6ICdIVE1MJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnQ1NTJyxcbiAgICBsYWJlbDogJ0NTUycsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ0phdmFTY3JpcHQnLFxuICAgIGxhYmVsOiAnSmF2YVNjcmlwdCcsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/allow-create.vue)_

vue

```
<template>
  <el-select
    v-model="value"
    multiple
    filterable
    allow-create
    default-first-option
    :reserve-keyword="false"
    placeholder="Choose tags for your article"
    style="width: 240px"
  >
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref<string[]>([])
const options = [
  {
    value: 'HTML',
    label: 'HTML',
  },
  {
    value: 'CSS',
    label: 'CSS',
  },
  {
    value: 'JavaScript',
    label: 'JavaScript',
  },
]
</script>
```

隐藏源代码

## 使用值键 value-key 属性 [​](#使用值键-value-key-属性)

如果 Select 的绑定值为对象类型，请务必指定 `value-key` 作为它的唯一性标识。

通过使用 `value-key` 属性，可以正确处理带有重复label的数据。 这样虽然`label` 是重复的，但任可通过 `id` 来确认唯一性。

Select

selected option's description: no select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPGVsLXNlbGVjdFxuICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgIHZhbHVlLWtleT1cImlkXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICA+XG4gICAgICA8ZWwtb3B0aW9uXG4gICAgICAgIHYtZm9yPVwiaXRlbSBpbiBvcHRpb25zXCJcbiAgICAgICAgOmtleT1cIml0ZW0uaWRcIlxuICAgICAgICA6bGFiZWw9XCJpdGVtLmxhYmVsXCJcbiAgICAgICAgOnZhbHVlPVwiaXRlbVwiXG4gICAgICAvPlxuICAgIDwvZWwtc2VsZWN0PlxuICAgIDxwPlxuICAgICAgc2VsZWN0ZWQgb3B0aW9uJ3MgZGVzY3JpcHRpb246XG4gICAgICB7eyB2YWx1ZSA/IHZhbHVlLmRlc2MgOiAnbm8gc2VsZWN0JyB9fVxuICAgIDwvcD5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG50eXBlIE9wdGlvbiA9IHtcbiAgaWQ6IG51bWJlclxuICBsYWJlbDogc3RyaW5nXG4gIGRlc2M6IHN0cmluZ1xufVxuY29uc3QgdmFsdWUgPSByZWY8T3B0aW9uPigpXG5jb25zdCBvcHRpb25zID0gcmVmKFtcbiAgeyBpZDogMSwgbGFiZWw6ICdPcHRpb24gQScsIGRlc2M6ICdPcHRpb24gQSAtIDIzMDUwNicgfSxcbiAgeyBpZDogMiwgbGFiZWw6ICdPcHRpb24gQicsIGRlc2M6ICdPcHRpb24gQiAtIDIzMDUwNicgfSxcbiAgeyBpZDogMywgbGFiZWw6ICdPcHRpb24gQycsIGRlc2M6ICdPcHRpb24gQyAtIDIzMDUwNicgfSxcbiAgeyBpZDogNCwgbGFiZWw6ICdPcHRpb24gQScsIGRlc2M6ICdPcHRpb24gQSAtIDIzMDUwNycgfSxcbl0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/value-key.vue)_

vue

```
<template>
  <div class="m-4">
    <el-select
      v-model="value"
      value-key="id"
      placeholder="Select"
      style="width: 240px"
    >
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item.label"
        :value="item"
      />
    </el-select>
    <p>
      selected option's description:
      {{ value ? value.desc : 'no select' }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

type Option = {
  id: number
  label: string
  desc: string
}
const value = ref<Option>()
const options = ref([
  { id: 1, label: 'Option A', desc: 'Option A - 230506' },
  { id: 2, label: 'Option B', desc: 'Option B - 230506' },
  { id: 3, label: 'Option C', desc: 'Option C - 230506' },
  { id: 4, label: 'Option A', desc: 'Option A - 230507' },
])
</script>
```

隐藏源代码

## 自定义标签 2.5.0 [​](#自定义标签)

您可以自定义标签。

将自定义的标签插入 `el-select` 的 slot 中即可。 `collapse-tags`, `collapse-tags-tooltip`, `max-collapse-tags` 在此模式下不生效.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0IHYtbW9kZWw9XCJ2YWx1ZVwiIG11bHRpcGxlIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIj5cbiAgICA8ZWwtb3B0aW9uXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gY29sb3JzXCJcbiAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgIDpsYWJlbD1cIml0ZW0ubGFiZWxcIlxuICAgICAgOnZhbHVlPVwiaXRlbS52YWx1ZVwiXG4gICAgPlxuICAgICAgPGRpdiBjbGFzcz1cImZsZXggaXRlbXMtY2VudGVyXCI+XG4gICAgICAgIDxlbC10YWcgOmNvbG9yPVwiaXRlbS52YWx1ZVwiIHN0eWxlPVwibWFyZ2luLXJpZ2h0OiA4cHhcIiBzaXplPVwic21hbGxcIiAvPlxuICAgICAgICA8c3BhbiA6c3R5bGU9XCJ7IGNvbG9yOiBpdGVtLnZhbHVlIH1cIj57eyBpdGVtLmxhYmVsIH19PC9zcGFuPlxuICAgICAgPC9kaXY+XG4gICAgPC9lbC1vcHRpb24+XG4gICAgPHRlbXBsYXRlICN0YWc+XG4gICAgICA8ZWwtdGFnIHYtZm9yPVwiY29sb3IgaW4gdmFsdWVcIiA6a2V5PVwiY29sb3JcIiA6Y29sb3I9XCJjb2xvclwiIC8+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1zZWxlY3Q+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZjxzdHJpbmdbXT4oW10pXG5jb25zdCBjb2xvcnMgPSBbXG4gIHtcbiAgICB2YWx1ZTogJyNFNjM0MTUnLFxuICAgIGxhYmVsOiAncmVkJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnI0ZGNjYwMCcsXG4gICAgbGFiZWw6ICdvcmFuZ2UnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICcjRkZERTBBJyxcbiAgICBsYWJlbDogJ3llbGxvdycsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJyMxRUM3OUQnLFxuICAgIGxhYmVsOiAnZ3JlZW4nLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICcjMTRDQ0NDJyxcbiAgICBsYWJlbDogJ2N5YW4nLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICcjNDE2N0YwJyxcbiAgICBsYWJlbDogJ2JsdWUnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICcjNjIyMkM5JyxcbiAgICBsYWJlbDogJ3B1cnBsZScsXG4gIH0sXG5dXG5jb2xvcnMuZm9yRWFjaCgoY29sb3IpID0+IHtcbiAgdmFsdWUudmFsdWUucHVzaChjb2xvci52YWx1ZSlcbn0pXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5lbC10YWcge1xuICBib3JkZXI6IG5vbmU7XG4gIGFzcGVjdC1yYXRpbzogMTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/custom-tag.vue)_

vue

```
<template>
  <el-select v-model="value" multiple placeholder="Select" style="width: 240px">
    <el-option
      v-for="item in colors"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    >
      <div class="flex items-center">
        <el-tag :color="item.value" style="margin-right: 8px" size="small" />
        <span :style="{ color: item.value }">{{ item.label }}</span>
      </div>
    </el-option>
    <template #tag>
      <el-tag v-for="color in value" :key="color" :color="color" />
    </template>
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref<string[]>([])
const colors = [
  {
    value: '#E63415',
    label: 'red',
  },
  {
    value: '#FF6600',
    label: 'orange',
  },
  {
    value: '#FFDE0A',
    label: 'yellow',
  },
  {
    value: '#1EC79D',
    label: 'green',
  },
  {
    value: '#14CCCC',
    label: 'cyan',
  },
  {
    value: '#4167F0',
    label: 'blue',
  },
  {
    value: '#6222C9',
    label: 'purple',
  },
]
colors.forEach((color) => {
  value.value.push(color.value)
})
</script>

<style scoped>
.el-tag {
  border: none;
  aspect-ratio: 1;
}
</style>
```

隐藏源代码

## 自定义加载 2.5.2 [​](#自定义加载)

修改加载区域内容

loading icon1

Please enter a keyword

loading icon2

Please enter a keyword

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXBcIj5cbiAgICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgICA8cD5sb2FkaW5nIGljb24xPC9wPlxuICAgICAgPGVsLXNlbGVjdFxuICAgICAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgICAgICBtdWx0aXBsZVxuICAgICAgICBmaWx0ZXJhYmxlXG4gICAgICAgIHJlbW90ZVxuICAgICAgICByZXNlcnZlLWtleXdvcmRcbiAgICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgZW50ZXIgYSBrZXl3b3JkXCJcbiAgICAgICAgOnJlbW90ZS1tZXRob2Q9XCJyZW1vdGVNZXRob2RcIlxuICAgICAgICA6bG9hZGluZz1cImxvYWRpbmdcIlxuICAgICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICA+XG4gICAgICAgIDxlbC1vcHRpb25cbiAgICAgICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICAgICAgOmtleT1cIml0ZW0udmFsdWVcIlxuICAgICAgICAgIDpsYWJlbD1cIml0ZW0ubGFiZWxcIlxuICAgICAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgICAgICAvPlxuICAgICAgICA8dGVtcGxhdGUgI2xvYWRpbmc+XG4gICAgICAgICAgPHN2ZyBjbGFzcz1cImNpcmN1bGFyXCIgdmlld0JveD1cIjAgMCA1MCA1MFwiPlxuICAgICAgICAgICAgPGNpcmNsZSBjbGFzcz1cInBhdGhcIiBjeD1cIjI1XCIgY3k9XCIyNVwiIHI9XCIyMFwiIGZpbGw9XCJub25lXCIgLz5cbiAgICAgICAgICA8L3N2Zz5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtc2VsZWN0PlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJtLTRcIj5cbiAgICAgIDxwPmxvYWRpbmcgaWNvbjI8L3A+XG4gICAgICA8ZWwtc2VsZWN0XG4gICAgICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgICAgIG11bHRpcGxlXG4gICAgICAgIGZpbHRlcmFibGVcbiAgICAgICAgcmVtb3RlXG4gICAgICAgIHJlc2VydmUta2V5d29yZFxuICAgICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBlbnRlciBhIGtleXdvcmRcIlxuICAgICAgICA6cmVtb3RlLW1ldGhvZD1cInJlbW90ZU1ldGhvZFwiXG4gICAgICAgIDpsb2FkaW5nPVwibG9hZGluZ1wiXG4gICAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAgID5cbiAgICAgICAgPGVsLW9wdGlvblxuICAgICAgICAgIHYtZm9yPVwiaXRlbSBpbiBvcHRpb25zXCJcbiAgICAgICAgICA6a2V5PVwiaXRlbS52YWx1ZVwiXG4gICAgICAgICAgOmxhYmVsPVwiaXRlbS5sYWJlbFwiXG4gICAgICAgICAgOnZhbHVlPVwiaXRlbS52YWx1ZVwiXG4gICAgICAgIC8+XG4gICAgICAgIDx0ZW1wbGF0ZSAjbG9hZGluZz5cbiAgICAgICAgICA8ZWwtaWNvbiBjbGFzcz1cImlzLWxvYWRpbmdcIj5cbiAgICAgICAgICAgIDxzdmcgY2xhc3M9XCJjaXJjdWxhclwiIHZpZXdCb3g9XCIwIDAgMjAgMjBcIj5cbiAgICAgICAgICAgICAgPGdcbiAgICAgICAgICAgICAgICBjbGFzcz1cInBhdGgyIGxvYWRpbmctcGF0aFwiXG4gICAgICAgICAgICAgICAgc3Ryb2tlLXdpZHRoPVwiMFwiXG4gICAgICAgICAgICAgICAgc3R5bGU9XCJhbmltYXRpb246IG5vbmU7IHN0cm9rZTogbm9uZVwiXG4gICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICA8Y2lyY2xlIHI9XCIzLjM3NVwiIGNsYXNzPVwiZG90MVwiIHJ4PVwiMFwiIHJ5PVwiMFwiIC8+XG4gICAgICAgICAgICAgICAgPGNpcmNsZSByPVwiMy4zNzVcIiBjbGFzcz1cImRvdDJcIiByeD1cIjBcIiByeT1cIjBcIiAvPlxuICAgICAgICAgICAgICAgIDxjaXJjbGUgcj1cIjMuMzc1XCIgY2xhc3M9XCJkb3Q0XCIgcng9XCIwXCIgcnk9XCIwXCIgLz5cbiAgICAgICAgICAgICAgICA8Y2lyY2xlIHI9XCIzLjM3NVwiIGNsYXNzPVwiZG90M1wiIHJ4PVwiMFwiIHJ5PVwiMFwiIC8+XG4gICAgICAgICAgICAgIDwvZz5cbiAgICAgICAgICAgIDwvc3ZnPlxuICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtc2VsZWN0PlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBvbk1vdW50ZWQsIHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW50ZXJmYWNlIExpc3RJdGVtIHtcbiAgdmFsdWU6IHN0cmluZ1xuICBsYWJlbDogc3RyaW5nXG59XG5cbmNvbnN0IGxpc3QgPSByZWY8TGlzdEl0ZW1bXT4oW10pXG5jb25zdCBvcHRpb25zID0gcmVmPExpc3RJdGVtW10+KFtdKVxuY29uc3QgdmFsdWUgPSByZWY8c3RyaW5nW10+KFtdKVxuY29uc3QgbG9hZGluZyA9IHJlZihmYWxzZSlcblxub25Nb3VudGVkKCgpID0+IHtcbiAgbGlzdC52YWx1ZSA9IHN0YXRlcy5tYXAoKGl0ZW0pID0+IHtcbiAgICByZXR1cm4geyB2YWx1ZTogYHZhbHVlOiR7aXRlbX1gLCBsYWJlbDogYGxhYmVsOiR7aXRlbX1gIH1cbiAgfSlcbn0pXG5cbmNvbnN0IHJlbW90ZU1ldGhvZCA9IChxdWVyeTogc3RyaW5nKSA9PiB7XG4gIGlmIChxdWVyeSkge1xuICAgIGxvYWRpbmcudmFsdWUgPSB0cnVlXG4gICAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICBsb2FkaW5nLnZhbHVlID0gZmFsc2VcbiAgICAgIG9wdGlvbnMudmFsdWUgPSBsaXN0LnZhbHVlLmZpbHRlcigoaXRlbSkgPT4ge1xuICAgICAgICByZXR1cm4gaXRlbS5sYWJlbC50b0xvd2VyQ2FzZSgpLmluY2x1ZGVzKHF1ZXJ5LnRvTG93ZXJDYXNlKCkpXG4gICAgICB9KVxuICAgIH0sIDMwMDApXG4gIH0gZWxzZSB7XG4gICAgb3B0aW9ucy52YWx1ZSA9IFtdXG4gIH1cbn1cblxuY29uc3Qgc3RhdGVzID0gW1xuICAnQWxhYmFtYScsXG4gICdBbGFza2EnLFxuICAnQXJpem9uYScsXG4gICdBcmthbnNhcycsXG4gICdDYWxpZm9ybmlhJyxcbiAgJ0NvbG9yYWRvJyxcbiAgJ0Nvbm5lY3RpY3V0JyxcbiAgJ0RlbGF3YXJlJyxcbiAgJ0Zsb3JpZGEnLFxuICAnR2VvcmdpYScsXG4gICdIYXdhaWknLFxuICAnSWRhaG8nLFxuICAnSWxsaW5vaXMnLFxuICAnSW5kaWFuYScsXG4gICdJb3dhJyxcbiAgJ0thbnNhcycsXG4gICdLZW50dWNreScsXG4gICdMb3Vpc2lhbmEnLFxuICAnTWFpbmUnLFxuICAnTWFyeWxhbmQnLFxuICAnTWFzc2FjaHVzZXR0cycsXG4gICdNaWNoaWdhbicsXG4gICdNaW5uZXNvdGEnLFxuICAnTWlzc2lzc2lwcGknLFxuICAnTWlzc291cmknLFxuICAnTW9udGFuYScsXG4gICdOZWJyYXNrYScsXG4gICdOZXZhZGEnLFxuICAnTmV3IEhhbXBzaGlyZScsXG4gICdOZXcgSmVyc2V5JyxcbiAgJ05ldyBNZXhpY28nLFxuICAnTmV3IFlvcmsnLFxuICAnTm9ydGggQ2Fyb2xpbmEnLFxuICAnTm9ydGggRGFrb3RhJyxcbiAgJ09oaW8nLFxuICAnT2tsYWhvbWEnLFxuICAnT3JlZ29uJyxcbiAgJ1Blbm5zeWx2YW5pYScsXG4gICdSaG9kZSBJc2xhbmQnLFxuICAnU291dGggQ2Fyb2xpbmEnLFxuICAnU291dGggRGFrb3RhJyxcbiAgJ1Rlbm5lc3NlZScsXG4gICdUZXhhcycsXG4gICdVdGFoJyxcbiAgJ1Zlcm1vbnQnLFxuICAnVmlyZ2luaWEnLFxuICAnV2FzaGluZ3RvbicsXG4gICdXZXN0IFZpcmdpbmlhJyxcbiAgJ1dpc2NvbnNpbicsXG4gICdXeW9taW5nJyxcbl1cbjwvc2NyaXB0PlxuXG48c3R5bGU+XG4uZWwtc2VsZWN0LWRyb3Bkb3duX19sb2FkaW5nIHtcbiAgZGlzcGxheTogZmxleDtcbiAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGhlaWdodDogMTAwcHg7XG4gIGZvbnQtc2l6ZTogMjBweDtcbn1cblxuLmNpcmN1bGFyIHtcbiAgZGlzcGxheTogaW5saW5lO1xuICBoZWlnaHQ6IDMwcHg7XG4gIHdpZHRoOiAzMHB4O1xuICBhbmltYXRpb246IGxvYWRpbmctcm90YXRlIDJzIGxpbmVhciBpbmZpbml0ZTtcbn1cbi5wYXRoIHtcbiAgYW5pbWF0aW9uOiBsb2FkaW5nLWRhc2ggMS41cyBlYXNlLWluLW91dCBpbmZpbml0ZTtcbiAgc3Ryb2tlLWRhc2hhcnJheTogOTAsIDE1MDtcbiAgc3Ryb2tlLWRhc2hvZmZzZXQ6IDA7XG4gIHN0cm9rZS13aWR0aDogMjtcbiAgc3Ryb2tlOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgc3Ryb2tlLWxpbmVjYXA6IHJvdW5kO1xufVxuLmxvYWRpbmctcGF0aCAuZG90MSB7XG4gIHRyYW5zZm9ybTogdHJhbnNsYXRlKDMuNzVweCwgMy43NXB4KTtcbiAgZmlsbDogdmFyKC0tZWwtY29sb3ItcHJpbWFyeSk7XG4gIGFuaW1hdGlvbjogY3VzdG9tLXNwaW4tbW92ZSAxcyBpbmZpbml0ZSBsaW5lYXIgYWx0ZXJuYXRlO1xuICBvcGFjaXR5OiAwLjM7XG59XG4ubG9hZGluZy1wYXRoIC5kb3QyIHtcbiAgdHJhbnNmb3JtOiB0cmFuc2xhdGUoY2FsYygxMDAlIC0gMy43NXB4KSwgMy43NXB4KTtcbiAgZmlsbDogdmFyKC0tZWwtY29sb3ItcHJpbWFyeSk7XG4gIGFuaW1hdGlvbjogY3VzdG9tLXNwaW4tbW92ZSAxcyBpbmZpbml0ZSBsaW5lYXIgYWx0ZXJuYXRlO1xuICBvcGFjaXR5OiAwLjM7XG4gIGFuaW1hdGlvbi1kZWxheTogMC40cztcbn1cbi5sb2FkaW5nLXBhdGggLmRvdDMge1xuICB0cmFuc2Zvcm06IHRyYW5zbGF0ZSgzLjc1cHgsIGNhbGMoMTAwJSAtIDMuNzVweCkpO1xuICBmaWxsOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgYW5pbWF0aW9uOiBjdXN0b20tc3Bpbi1tb3ZlIDFzIGluZmluaXRlIGxpbmVhciBhbHRlcm5hdGU7XG4gIG9wYWNpdHk6IDAuMztcbiAgYW5pbWF0aW9uLWRlbGF5OiAxLjJzO1xufVxuLmxvYWRpbmctcGF0aCAuZG90NCB7XG4gIHRyYW5zZm9ybTogdHJhbnNsYXRlKGNhbGMoMTAwJSAtIDMuNzVweCksIGNhbGMoMTAwJSAtIDMuNzVweCkpO1xuICBmaWxsOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgYW5pbWF0aW9uOiBjdXN0b20tc3Bpbi1tb3ZlIDFzIGluZmluaXRlIGxpbmVhciBhbHRlcm5hdGU7XG4gIG9wYWNpdHk6IDAuMztcbiAgYW5pbWF0aW9uLWRlbGF5OiAwLjhzO1xufVxuQGtleWZyYW1lcyBsb2FkaW5nLXJvdGF0ZSB7XG4gIHRvIHtcbiAgICB0cmFuc2Zvcm06IHJvdGF0ZSgzNjBkZWcpO1xuICB9XG59XG5Aa2V5ZnJhbWVzIGxvYWRpbmctZGFzaCB7XG4gIDAlIHtcbiAgICBzdHJva2UtZGFzaGFycmF5OiAxLCAyMDA7XG4gICAgc3Ryb2tlLWRhc2hvZmZzZXQ6IDA7XG4gIH1cbiAgNTAlIHtcbiAgICBzdHJva2UtZGFzaGFycmF5OiA5MCwgMTUwO1xuICAgIHN0cm9rZS1kYXNob2Zmc2V0OiAtNDBweDtcbiAgfVxuICAxMDAlIHtcbiAgICBzdHJva2UtZGFzaGFycmF5OiA5MCwgMTUwO1xuICAgIHN0cm9rZS1kYXNob2Zmc2V0OiAtMTIwcHg7XG4gIH1cbn1cbkBrZXlmcmFtZXMgY3VzdG9tLXNwaW4tbW92ZSB7XG4gIHRvIHtcbiAgICBvcGFjaXR5OiAxO1xuICB9XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/custom-loading.vue)_

vue

```
<template>
  <div class="flex flex-wrap">
    <div class="m-4">
      <p>loading icon1</p>
      <el-select
        v-model="value"
        multiple
        filterable
        remote
        reserve-keyword
        placeholder="Please enter a keyword"
        :remote-method="remoteMethod"
        :loading="loading"
        style="width: 240px"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
        <template #loading>
          <svg class="circular" viewBox="0 0 50 50">
            <circle class="path" cx="25" cy="25" r="20" fill="none" />
          </svg>
        </template>
      </el-select>
    </div>
    <div class="m-4">
      <p>loading icon2</p>
      <el-select
        v-model="value"
        multiple
        filterable
        remote
        reserve-keyword
        placeholder="Please enter a keyword"
        :remote-method="remoteMethod"
        :loading="loading"
        style="width: 240px"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
        <template #loading>
          <el-icon class="is-loading">
            <svg class="circular" viewBox="0 0 20 20">
              <g
                class="path2 loading-path"
                stroke-width="0"
                style="animation: none; stroke: none"
              >
                <circle r="3.375" class="dot1" rx="0" ry="0" />
                <circle r="3.375" class="dot2" rx="0" ry="0" />
                <circle r="3.375" class="dot4" rx="0" ry="0" />
                <circle r="3.375" class="dot3" rx="0" ry="0" />
              </g>
            </svg>
          </el-icon>
        </template>
      </el-select>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

interface ListItem {
  value: string
  label: string
}

const list = ref<ListItem[]>([])
const options = ref<ListItem[]>([])
const value = ref<string[]>([])
const loading = ref(false)

onMounted(() => {
  list.value = states.map((item) => {
    return { value: `value:${item}`, label: `label:${item}` }
  })
})

const remoteMethod = (query: string) => {
  if (query) {
    loading.value = true
    setTimeout(() => {
      loading.value = false
      options.value = list.value.filter((item) => {
        return item.label.toLowerCase().includes(query.toLowerCase())
      })
    }, 3000)
  } else {
    options.value = []
  }
}

const states = [
  'Alabama',
  'Alaska',
  'Arizona',
  'Arkansas',
  'California',
  'Colorado',
  'Connecticut',
  'Delaware',
  'Florida',
  'Georgia',
  'Hawaii',
  'Idaho',
  'Illinois',
  'Indiana',
  'Iowa',
  'Kansas',
  'Kentucky',
  'Louisiana',
  'Maine',
  'Maryland',
  'Massachusetts',
  'Michigan',
  'Minnesota',
  'Mississippi',
  'Missouri',
  'Montana',
  'Nebraska',
  'Nevada',
  'New Hampshire',
  'New Jersey',
  'New Mexico',
  'New York',
  'North Carolina',
  'North Dakota',
  'Ohio',
  'Oklahoma',
  'Oregon',
  'Pennsylvania',
  'Rhode Island',
  'South Carolina',
  'South Dakota',
  'Tennessee',
  'Texas',
  'Utah',
  'Vermont',
  'Virginia',
  'Washington',
  'West Virginia',
  'Wisconsin',
  'Wyoming',
]
</script>

<style>
.el-select-dropdown__loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  font-size: 20px;
}

.circular {
  display: inline;
  height: 30px;
  width: 30px;
  animation: loading-rotate 2s linear infinite;
}
.path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-color-primary);
  stroke-linecap: round;
}
.loading-path .dot1 {
  transform: translate(3.75px, 3.75px);
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
}
.loading-path .dot2 {
  transform: translate(calc(100% - 3.75px), 3.75px);
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 0.4s;
}
.loading-path .dot3 {
  transform: translate(3.75px, calc(100% - 3.75px));
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 1.2s;
}
.loading-path .dot4 {
  transform: translate(calc(100% - 3.75px), calc(100% - 3.75px));
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 0.8s;
}
@keyframes loading-rotate {
  to {
    transform: rotate(360deg);
  }
}
@keyframes loading-dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -40px;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -120px;
  }
}
@keyframes custom-spin-move {
  to {
    opacity: 1;
  }
}
</style>
```

隐藏源代码

## 空值配置2.7.0 [​](#空值配置)

若想配置如空字符串为有效值而不是空值，可以配置 `empty-values` 为 `[null, undefined]`.

如果您想要将清空值更改为 `null`, 请设置 `value-on-clear` 为 `null`

All

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0XG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICA6ZW1wdHktdmFsdWVzPVwiW251bGwsIHVuZGVmaW5lZF1cIlxuICAgIDp2YWx1ZS1vbi1jbGVhcj1cIm51bGxcIlxuICAgIGNsZWFyYWJsZVxuICAgIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgQGNsZWFyPVwiaGFuZGxlQ2xlYXJcIlxuICA+XG4gICAgPGVsLW9wdGlvblxuICAgICAgdi1mb3I9XCJpdGVtIGluIG9wdGlvbnNcIlxuICAgICAgOmtleT1cIml0ZW0udmFsdWVcIlxuICAgICAgOmxhYmVsPVwiaXRlbS5sYWJlbFwiXG4gICAgICA6dmFsdWU9XCJpdGVtLnZhbHVlXCJcbiAgICAvPlxuICA8L2VsLXNlbGVjdD5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBFbE1lc3NhZ2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCcnKVxuXG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICcnLFxuICAgIGxhYmVsOiAnQWxsJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uMScsXG4gICAgbGFiZWw6ICdPcHRpb24xJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uMicsXG4gICAgbGFiZWw6ICdPcHRpb24yJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uMycsXG4gICAgbGFiZWw6ICdPcHRpb24zJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uNCcsXG4gICAgbGFiZWw6ICdPcHRpb240JyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uNScsXG4gICAgbGFiZWw6ICdPcHRpb241JyxcbiAgfSxcbl1cblxuY29uc3QgaGFuZGxlQ2xlYXIgPSAoKSA9PiB7XG4gIEVsTWVzc2FnZS5pbmZvKGBUaGUgY2xlYXIgdmFsdWUgaXM6ICR7dmFsdWUudmFsdWV9YClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/empty-values.vue)_

vue

```
<template>
  <el-select
    v-model="value"
    :empty-values="[null, undefined]"
    :value-on-clear="null"
    clearable
    placeholder="Select"
    style="width: 240px"
    @clear="handleClear"
  >
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const value = ref('')

const options = [
  {
    value: '',
    label: 'All',
  },
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]

const handleClear = () => {
  ElMessage.info(`The clear value is: ${value.value}`)
}
</script>
```

隐藏源代码

## 自定义标签 2.7.4 [​](#自定义标签-1)

您可以自定义标签

Label1: Option1

Label1: Option1

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTQgaXRlbXMtY2VudGVyXCI+XG4gICAgPGVsLXNlbGVjdFxuICAgICAgdi1tb2RlbD1cInZhbHVlMVwiXG4gICAgICBwbGFjZWhvbGRlcj1cIlNlbGVjdFwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICBjbGVhcmFibGVcbiAgICA+XG4gICAgICA8dGVtcGxhdGUgI2xhYmVsPVwieyBsYWJlbCwgdmFsdWUgfVwiPlxuICAgICAgICA8c3Bhbj57eyBsYWJlbCB9fTogPC9zcGFuPlxuICAgICAgICA8c3BhbiBzdHlsZT1cImZvbnQtd2VpZ2h0OiBib2xkXCI+e3sgdmFsdWUgfX08L3NwYW4+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgPGVsLW9wdGlvblxuICAgICAgICB2LWZvcj1cIml0ZW0gaW4gb3B0aW9uc1wiXG4gICAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgICAgOmxhYmVsPVwiaXRlbS5sYWJlbFwiXG4gICAgICAgIDp2YWx1ZT1cIml0ZW0udmFsdWVcIlxuICAgICAgLz5cbiAgICA8L2VsLXNlbGVjdD5cblxuICAgIDxlbC1zZWxlY3RcbiAgICAgIHYtbW9kZWw9XCJ2YWx1ZTJcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJTZWxlY3RcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgY2xlYXJhYmxlXG4gICAgICBtdWx0aXBsZVxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjbGFiZWw9XCJ7IGxhYmVsLCB2YWx1ZSB9XCI+XG4gICAgICAgIDxzcGFuPnt7IGxhYmVsIH19OiA8L3NwYW4+XG4gICAgICAgIDxzcGFuIHN0eWxlPVwiZm9udC13ZWlnaHQ6IGJvbGRcIj57eyB2YWx1ZSB9fTwvc3Bhbj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8ZWwtb3B0aW9uXG4gICAgICAgIHYtZm9yPVwiaXRlbSBpbiBvcHRpb25zXCJcbiAgICAgICAgOmtleT1cIml0ZW0udmFsdWVcIlxuICAgICAgICA6bGFiZWw9XCJpdGVtLmxhYmVsXCJcbiAgICAgICAgOnZhbHVlPVwiaXRlbS52YWx1ZVwiXG4gICAgICAvPlxuICAgIDwvZWwtc2VsZWN0PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlMSA9IHJlZjxzdHJpbmc+KCdPcHRpb24xJylcbmNvbnN0IHZhbHVlMiA9IHJlZjxzdHJpbmdbXT4oWydPcHRpb24xJ10pXG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICdPcHRpb24xJyxcbiAgICBsYWJlbDogJ0xhYmVsMScsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjInLFxuICAgIGxhYmVsOiAnTGFiZWwyJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnT3B0aW9uMycsXG4gICAgbGFiZWw6ICdMYWJlbDMnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdPcHRpb240JyxcbiAgICBsYWJlbDogJ0xhYmVsNCcsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjUnLFxuICAgIGxhYmVsOiAnTGFiZWw1JyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select/custom-label.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-4 items-center">
    <el-select
      v-model="value1"
      placeholder="Select"
      style="width: 240px"
      clearable
    >
      <template #label="{ label, value }">
        <span>{{ label }}: </span>
        <span style="font-weight: bold">{{ value }}</span>
      </template>
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>

    <el-select
      v-model="value2"
      placeholder="Select"
      style="width: 240px"
      clearable
      multiple
    >
      <template #label="{ label, value }">
        <span>{{ label }}: </span>
        <span style="font-weight: bold">{{ value }}</span>
      </template>
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<string>('Option1')
const value2 = ref<string[]>(['Option1'])
const options = [
  {
    value: 'Option1',
    label: 'Label1',
  },
  {
    value: 'Option2',
    label: 'Label2',
  },
  {
    value: 'Option3',
    label: 'Label3',
  },
  {
    value: 'Option4',
    label: 'Label4',
  },
  {
    value: 'Option5',
    label: 'Label5',
  },
]
</script>

<style scoped></style>
```

隐藏源代码

## Select API [​](#select-api)

### Select Attributes [​](#select-attributes)

| 属性名 | 说明 | 类型 | Default |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `string` / `number` / `boolean` / `object` / `array` | — |
| multiple | 是否多选 | `boolean` | false |
| options 2.10.5 | 选项的数据源， `value` 的 key 和 `label` 和 `disabled`可以通过 `props`自定义. | `array` | — |
| [props](#props) 2.10.5 | options 的配置 | `object` | — |
| disabled | 是否禁用 | `boolean` | false |
| value-key | 作为 value 唯一标识的键名，绑定值为对象类型时必填 | `string` | value |
| size | 输入框尺寸 | `enum` | — |
| clearable | 是否可以清空选项 | `boolean` | false |
| collapse-tags | 多选时是否将选中值按文字的形式展示 | `boolean` | false |
| collapse-tags-tooltip 2.3.0 | 当鼠标悬停于折叠标签的文本时，是否显示所有选中的标签。 要使用此属性，`collapse-tags`属性必须设定为 true | `boolean` | false |
| [tag-tooltip](#tag-tooltip) 2.13.3 | 折叠标签工具提示的配置对象。 要使用此项， `collapse-tags` 和 `collapse-tags-tooltip` 必须为 true | `object` | {} |
| multiple-limit | `multiple` 属性设置为 `true` 时，代表多选场景下用户最多可以选择的项目数， 为 0 则不限制 | `number` | 0 |
| id | 原生 input 的 id | `string` | — |
| name | Select 输入框的原生 name 属性 | `string` | — |
| effect | tooltip 主题，内置了 `dark` / `light` 两种 | `enum` / `string` | light |
| autocomplete | Select 输入框的原生 autocomplete 属性 | `string` | off |
| placeholder | 占位符，默认为“Select” | `string` | — |
| filterable | Select 组件是否可筛选 | `boolean` | false |
| allow-create | 是否允许用户创建新条目， 当`filterable`设置为 true 时才会生效 | `boolean` | false |
| filter-method | 自定义筛选方法的第一个参数是当前输入的值。 只有当 `filterable` 设置为 true 时才会生效。 | `Function` | — |
| remote | 其中的选项是否从服务器远程加载 | `boolean` | false |
| debounce 2.11.7 | 远程搜索时的防抖延迟（以毫秒为单位） | `number` | 300 |
| remote-method | 当输入值发生变化时触发的函数。 它的参数就是当前的输入值。 当`filterable`设置为 true 时才会生效 | `Function` | — |
| remote-show-suffix | 远程搜索方法显示后缀图标 | `boolean` | false |
| loading | 是否正在从远程获取数据 | `boolean` | false |
| loading-text | 从服务器加载数据时显示的文本，默认为“Loading” | `string` | — |
| no-match-text | 搜索条件无匹配时显示的文字，也可以使用 `empty` 插槽设置，默认是 “No matching data'” | `string` | — |
| no-data-text | 无选项时显示的文字，也可以使用 `empty` 插槽设置自定义内容，默认是 “No data” | `string` | — |
| popper-class | 为 Select 下拉菜单和标签提示设置自定义类名 | `string` | '' |
| popper-style 2.11.0 | 为 Select 下拉菜单和标签提示设置自定义样式 | `string` / `object` | — |
| reserve-keyword | 当 `multiple` 和 `filterable`被设置为 true 时，是否在选中一个选项后保留当前的搜索关键词 | `boolean` | true |
| default-first-option | 是否在输入框按下回车时，选择第一个匹配项。 需配合 `filterable` 或 `remote` 使用 | `boolean` | false |
| teleported | 是否使用 teleport。设置成 `true`则会被追加到 `append-to` 的位置 | `boolean` | true |
| append-to 2.8.4 | 下拉框挂载到哪个 DOM 元素 | `CSSSelector` / `HTMLElement` | — |
| persistent | 当下拉选择器未被激活并且`persistent`设置为`false`，选择器会被删除。 | `boolean` | true |
| automatic-dropdown | 对于不可搜索的 Select，是否在输入框获得焦点后自动弹出选项菜单 | `boolean` | false |
| clear-icon | 自定义清除图标 | `string` / `object` | CircleClose |
| fit-input-width | 下拉框的宽度是否与输入框相同 | `boolean` | false |
| suffix-icon | 自定义后缀图标组件 | `string` / `object` | ArrowDown |
| tag-type | 标签类型 | `enum` | info |
| tag-effect 2.7.7 | 标签效果 | `enum` | light |
| validate-event | 是否触发表单验证 | `boolean` | true |
| offset 2.8.8 | 下拉面板偏移量 | `number` | 12 |
| show-arrow 2.8.8 | 下拉菜单的内容是否有箭头 | `boolean` | true |
| placement 2.2.17 | 下拉框出现的位置 | `enum` | bottom-start |
| fallback-placements 2.5.6 | dropdown 可用的 positions 请查看[popper.js 文档](https://popper.js.org/docs/v2/modifiers/flip/#fallbackplacements) | `array` | \['bottom-start', 'top-start', 'right', 'left'\] |
| max-collapse-tags 2.3.0 | 需要显示的 Tag 的最大数量 只有当 `collapse-tags` 设置为 true 时才会生效。 | `number` | 1 |
| popper-options | [popper.js](https://popper.js.org/docs/v2/) 参数 | `object`refer to [popper.js](https://popper.js.org/docs/v2/) doc | {} |
| aria-label a11y | 等价于原生 input `aria-label` 属性 | `string` | — |
| empty-values 2.7.0 | 组件的空值配置， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `array` | — |
| value-on-clear 2.7.0 | 清空选项的值， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `string` / `number` / `boolean` / `Function` | — |
| suffix-transition deprecated | 下拉菜单显示/消失时后缀图标的动画 | `boolean` | true |
| tabindex 2.9.0 | input 的 tabindex | `string` / `number` | — |

WARNING

`suffix-transition` 已被 **弃用**, 并 **将会** 在2.4.0中删除, 请使用覆盖样式方案。

### Props [​](#props)

| Attribute | 说明 | Type | Default |
| --- | --- | --- | --- |
| value | 指定选项的值为选项对象的某个属性值 | `string` | value |
| label | 指定节点标签为节点对象的某个属性值 | `string` | label |
| options 2.11.0 | 指定选项的子选项为选项对象的某个属性值 | `string` | options |
| disabled | 指定选项的禁用为选项对象的某个属性值 | `string` | disabled |

### tag-tooltip 2.13.3 [​](#tag-tooltip)

备用机制

标签工具提示中的属性遵循此优先级顺序：

1.  在标签工具提示对象中明确定义的字段。
2.  从 el-select 继承的共享属性（例如 effect、popper-class、popper-style、teleported、append-to、popper-options）。
3.  底层 el-tooltip 组件的默认值。 这样，您就可以覆盖标签的特定工具提示行为，同时保持与默认的“选择”下拉菜单的一致性。

自定义容器位置

当将 Tooltip 添加到自定义容器时（通过 `append-to` 属性），应将容器配置为 `position: relative` 或 `position: absolute`，以确保准确定位。 此外，如果需要防止工具提示超出其边界，可以对容器应用 `overflow: hidden`。

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| append-to | 指示 Tooltip 的内容将附加在哪一个网页元素上 | `CSSSelector` / `HTMLElement` | — |
| placement | Tooltip 组件出现的位置 | `enum` | bottom |
| fallback-placements | Tooltip 可用的 positions 请查看[popper.js 文档](https://popper.js.org/docs/v2/modifiers/flip/#fallbackplacements) | `array` | \['bottom', 'top', 'right', 'left'\] |
| effect | 文字提示（Tooltip）的主题，内置`dark`和`light`两种。 | `enum` / `string` | — |
| popper-class | 为 Tooltip 的 popper 添加自定义类名 | `string` | — |
| popper-style | 为 Tooltip 的 popper 添加自定义样式 | `string` / `object` | — |
| transition | Tooltip 所应用过渡动画的名称 | `string` | — |
| teleported | 是否使用 teleport。设置成 `true`则会被追加到 `append-to` 的位置 | `boolean` | — |
| popper-options | [popper.js](https://popper.js.org/docs/v2/) 参数 | `object`refer to [popper.js](https://popper.js.org/docs/v2/) doc | — |
| show-after | 在触发后多久显示内容，单位毫秒 | `number` | — |
| hide-after | 关闭时的延迟 | `number` | — |
| auto-close | tooltip 出现后自动隐藏延时，单位毫秒 | `number` | — |
| offset | Tooltip 出现位置的偏移量 | `number` | — |

### Select Events [​](#select-events)

| 事件名 | 说明 | Type |
| --- | --- | --- |
| change | 选中值发生变化时触发 | `Function` |
| visible-change | 下拉框出现/隐藏时触发 | `Function` |
| remove-tag | 多选模式下移除tag时触发 | `Function` |
| clear | 可清空的单选模式下用户点击清空按钮时触发 | `Function` |
| blur | 当 input 失去焦点时触发 | `Function` |
| focus | 当 input 获得焦点时触发 | `Function` |
| popup-scroll 2.9.4 | 下拉滚动时触发 | `Function` |
| end-reached 2.14.0 | 下拉滚动到结束时触发器 | `Function` |

### Select Slots [​](#select-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | option 组件列表 | Option Group / Option |
| header 2.4.3 | 下拉列表顶部的内容 | — |
| footer 2.4.3 | 下拉列表底部的内容 | — |
| prefix | Select 组件头部内容 | — |
| empty | 无选项时的列表 | ::: |
| tag 2.5.0 | 作为 Select 组件的内容时，子标签 `data`、`selectDisabled` 和 `deleteTag` 是在版本 2.10.3 中新增的。 | `object` |
| loading 2.5.2 | select 组件自定义 loading内容 | — |
| label 2.7.4 | select 组件自定义标签内容 `index` 引入于2.11.2 | `object` |

### Select Exposes [​](#select-exposes)

| 方法名 | 详情 | 类型 |
| --- | --- | --- |
| focus | 使选择器的输入框获取焦点 | `Function` |
| blur | 使选择器的输入框失去焦点，并隐藏下拉框 | `Function` |
| selectedLabel 2.8.5 | 获取当前选中的标签 | `object` |

## Option Group API [​](#option-group-api)

### Option Group Attributes [​](#option-group-attributes)

| 名称 | 详情 | 类型 | 默认值 |
| --- | --- | --- | --- |
| label | 分组的名称 | `string` | — |
| disabled | 是否将该分组下所有选项置为禁用 | `boolean` | false |

### Option Group Slots [​](#option-group-slots)

| 插槽名 | 说明 | Subtags |
| --- | --- | --- |
| default | 自定义默认内容 | Option |

## Option API [​](#option-api)

### Option Attributes [​](#option-attributes)

| Name | 描述 | 类型 | 默认值 |
| --- | --- | --- | --- |
| value | 选项的值 | `string` / `number` / `boolean` / `object` | — |
| label | 选项的标签，若不设置则默认与`value`相同 | `string` / `number` | — |
| disabled | 是否禁用该选项 | `boolean` | false |

### Option Slots [​](#option-slots)

| 名称 | 说明 |
| --- | --- |
| default | 默认插槽内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/select) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/select.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/select.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/30046649?v=4&size=64)](https://github.com/MrWeilian)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/27912232?v=4&size=64)](https://github.com/Fuphoenixes)[![](https://avatars.githubusercontent.com/u/132551120?v=4&size=64)](https://github.com/YiMo1)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/204166003?v=4&size=64)](https://github.com/Putia3)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/48341368?v=4&size=64)](https://github.com/HaceraI)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/166777320?v=4&size=64)](https://github.com/ixyzorg)[![](https://avatars.githubusercontent.com/u/24487727?v=4&size=64)](https://github.com/LostElkByte)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/58782768?v=4&size=64)](https://github.com/dddssw)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/50254496?v=4&size=64)](https://github.com/LoTwT)[![](https://avatars.githubusercontent.com/u/47178158?v=4&size=64)](https://github.com/Aaron-zon)[![](https://avatars.githubusercontent.com/u/32354856?v=4&size=64)](https://github.com/baiwusanyu-c)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/36978416?v=4&size=64)](https://github.com/SimonaliaChen)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/73086438?v=4&size=64)](https://github.com/Cheerwhy)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)[![](https://avatars.githubusercontent.com/u/58846658?v=4&size=64)](https://github.com/JiuRanYa)[![](https://avatars.githubusercontent.com/u/109908413?v=4&size=64)](https://github.com/sleepyShen1989)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/59350883?v=4&size=64)](https://github.com/init-qy)[![](https://avatars.githubusercontent.com/u/27277138?v=4&size=64)](https://github.com/wuzhidexiaoming)[![](https://avatars.githubusercontent.com/u/1532716?v=4&size=64)](https://github.com/godxiaoji)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/178066799?v=4&size=64)](https://github.com/Yeuvoir)[![](https://avatars.githubusercontent.com/u/37976544?v=4&size=64)](https://github.com/ALypovskyi)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/41771224?v=4&size=64)](https://github.com/littlezo)[![](https://avatars.githubusercontent.com/u/201188047?v=4&size=64)](https://github.com/YXY-cell)[![](https://avatars.githubusercontent.com/u/27413795?v=4&size=64)](https://github.com/SpanManX)[![](https://avatars.githubusercontent.com/u/19580923?v=4&size=64)](https://github.com/wcttmf)[![](https://avatars.githubusercontent.com/u/42372070?v=4&size=64)](https://github.com/Map1en)[![](https://avatars.githubusercontent.com/u/33254923?v=4&size=64)](https://github.com/yicheny)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/127940123?v=4&size=64)](https://github.com/baozjj)[![](https://avatars.githubusercontent.com/u/198031266?v=4&size=64)](https://github.com/noki-maker)[![](https://avatars.githubusercontent.com/u/40554198?v=4&size=64)](https://github.com/WangYJEE)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/22659150?v=4&size=64)](https://github.com/ntnyq)[![](https://avatars.githubusercontent.com/u/57179957?v=4&size=64)](https://github.com/yeonjulee1005)[![](https://avatars.githubusercontent.com/u/10398024?v=4&size=64)](https://github.com/humorHan)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/57524062?v=4&size=64)](https://github.com/Ther-su)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/81673017?v=4&size=64)](https://github.com/RSS1102)[![](https://avatars.githubusercontent.com/u/2849255?v=4&size=64)](https://github.com/mg5566)[![](https://avatars.githubusercontent.com/u/8591261?v=4&size=64)](https://github.com/zeyongTsai)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/36811055?v=4&size=64)](https://github.com/iDestin)[![](https://avatars.githubusercontent.com/u/7065327?v=4&size=64)](https://github.com/LiuwqGit)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/65441198?v=4&size=64)](https://github.com/tyj-321)[![](https://avatars.githubusercontent.com/u/48283236?v=4&size=64)](https://github.com/raphaelbernhart)[![](https://avatars.githubusercontent.com/u/67454874?v=4&size=64)](https://github.com/nigiwen)[![](https://avatars.githubusercontent.com/u/79386745?v=4&size=64)](https://github.com/kamesan012)[![](https://avatars.githubusercontent.com/u/101374143?v=4&size=64)](https://github.com/sseinHu)[![](https://avatars.githubusercontent.com/u/18509404?v=4&size=64)](https://github.com/inottn)[![](https://avatars.githubusercontent.com/u/71313168?v=4&size=64)](https://github.com/cc-hearts)[![](https://avatars.githubusercontent.com/u/101238421?v=4&size=64)](https://github.com/acyza)[![](https://avatars.githubusercontent.com/u/31885971?v=4&size=64)](https://github.com/wonderl17)[![](https://avatars.githubusercontent.com/u/13410410?v=4&size=64)](https://github.com/jaa134)[![](https://avatars.githubusercontent.com/u/5701072?v=4&size=64)](https://github.com/Naeemo)[![](https://avatars.githubusercontent.com/u/4075314?v=4&size=64)](https://github.com/Giwayume)[![](https://avatars.githubusercontent.com/u/75945382?v=4&size=64)](https://github.com/yuanxin518)[![](https://avatars.githubusercontent.com/u/38248854?v=4&size=64)](https://github.com/Yueyanc)[![](https://avatars.githubusercontent.com/u/65154?v=4&size=64)](https://github.com/exherb)[![](https://avatars.githubusercontent.com/u/5389932?v=4&size=64)](https://github.com/muuyao)[![](https://avatars.githubusercontent.com/u/88016243?v=4&size=64)](https://github.com/wzrove)[![](https://avatars.githubusercontent.com/u/48196760?v=4&size=64)](https://github.com/eriksyuan)[![](https://avatars.githubusercontent.com/u/8401855?v=4&size=64)](https://github.com/JacBian)[![](https://avatars.githubusercontent.com/u/39672197?v=4&size=64)](https://github.com/bchen1029)

[Rate 评分](https://element-plus.org/zh-CN/component/rate)

[Virtualized Select 虚拟化选择器](https://element-plus.org/zh-CN/component/select-v2)


