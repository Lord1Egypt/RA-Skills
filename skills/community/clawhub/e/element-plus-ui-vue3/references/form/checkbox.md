---
name: "checkbox"
description: "Checkbox 多选框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Checkbox 多选框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/checkbox.html"
---

---

# Checkbox 多选框 [​](#checkbox-多选框)

更新日志待解决

25

在一组备选项中进行多选。

WARNING

`label` 作为 `value` 来使用已经被 **废弃**, 建议`label` 只用来表示展示的文字，这个被废弃的用法**将会在** 3.0.0 版本被移除，请考虑使用新 API 替换.

TIP

新的 API `value` 已在 2.6.0 版本添加，文档中的示例都将使用 `value`。 如果您使用的版本 **低于** 2.6.0 并且使用 `checkbox-group`，请参考：

vue

```
<template>
  <el-checkbox-group v-model="checkList">
    <!-- works when >=2.6.0, recommended ✔️ value not work when <2.6.0 ❌ -->
    <el-checkbox label="Option 1" value="Value 1" />
    <!-- works when <2.6.0, deprecated act as value when >=3.0.0 -->
    <el-checkbox label="Option 2 & Value 2" />
  </el-checkbox-group>
</template>
```

## 基础用法 [​](#基础用法)

单独使用可以表示两种状态之间的切换，写在标签中的内容为 checkbox 按钮后的介绍。

`checkbox-group`元素能把多个 checkbox 管理为一组，只需要在 Group 中使用 `v-model` 绑定 `Array` 类型的变量即可。 只有一个选项时的默认值类型为 `Boolean`，当选中时值为`true`。 `el-checkbox` 标签中的内容将成为复选框按钮之后的描述。

Option 1Option 2

Option 1Option 2

Option 1Option 2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1jaGVja2JveCB2LW1vZGVsPVwiY2hlY2tlZDFcIiBsYWJlbD1cIk9wdGlvbiAxXCIgc2l6ZT1cImxhcmdlXCIgLz5cbiAgICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNoZWNrZWQyXCIgbGFiZWw9XCJPcHRpb24gMlwiIHNpemU9XCJsYXJnZVwiIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibXktMlwiPlxuICAgIDxlbC1jaGVja2JveCB2LW1vZGVsPVwiY2hlY2tlZDNcIiBsYWJlbD1cIk9wdGlvbiAxXCIgLz5cbiAgICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNoZWNrZWQ0XCIgbGFiZWw9XCJPcHRpb24gMlwiIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibXQtMlwiPlxuICAgIDxlbC1jaGVja2JveCB2LW1vZGVsPVwiY2hlY2tlZDVcIiBsYWJlbD1cIk9wdGlvbiAxXCIgc2l6ZT1cInNtYWxsXCIgLz5cbiAgICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNoZWNrZWQ2XCIgbGFiZWw9XCJPcHRpb24gMlwiIHNpemU9XCJzbWFsbFwiIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgY2hlY2tlZDEgPSByZWYodHJ1ZSlcbmNvbnN0IGNoZWNrZWQyID0gcmVmKGZhbHNlKVxuY29uc3QgY2hlY2tlZDMgPSByZWYoZmFsc2UpXG5jb25zdCBjaGVja2VkNCA9IHJlZihmYWxzZSlcbmNvbnN0IGNoZWNrZWQ1ID0gcmVmKGZhbHNlKVxuY29uc3QgY2hlY2tlZDYgPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/checkbox/basic.vue)_

vue

```
<template>
  <div>
    <el-checkbox v-model="checked1" label="Option 1" size="large" />
    <el-checkbox v-model="checked2" label="Option 2" size="large" />
  </div>
  <div class="my-2">
    <el-checkbox v-model="checked3" label="Option 1" />
    <el-checkbox v-model="checked4" label="Option 2" />
  </div>
  <div class="mt-2">
    <el-checkbox v-model="checked5" label="Option 1" size="small" />
    <el-checkbox v-model="checked6" label="Option 2" size="small" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked1 = ref(true)
const checked2 = ref(false)
const checked3 = ref(false)
const checked4 = ref(false)
const checked5 = ref(false)
const checked6 = ref(false)
</script>
```

隐藏源代码

## 禁用状态 [​](#禁用状态)

多选框不可用状态。

设置 `disabled` 属性即可。

DisabledNot disabled

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNoZWNrZWQxXCIgZGlzYWJsZWQ+RGlzYWJsZWQ8L2VsLWNoZWNrYm94PlxuICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNoZWNrZWQyXCI+Tm90IGRpc2FibGVkPC9lbC1jaGVja2JveD5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNoZWNrZWQxID0gcmVmKGZhbHNlKVxuY29uc3QgY2hlY2tlZDIgPSByZWYodHJ1ZSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/checkbox/disabled.vue)_

vue

```
<template>
  <el-checkbox v-model="checked1" disabled>Disabled</el-checkbox>
  <el-checkbox v-model="checked2">Not disabled</el-checkbox>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked1 = ref(false)
const checked2 = ref(true)
</script>
```

隐藏源代码

## 多选框组 [​](#多选框组)

适用于多个勾选框绑定到同一个数组的情景，通过是否勾选来表示这一组选项中选中的项。

在 `el-checkbox` 元素中定义 `v-model` 绑定变量，单一的 `checkbox` 中，默认绑定变量的值会是 `Boolean`，选中为 `true`。 在 `el-checkbox` 组件中，`value` 是选择框的值。 如果该组件下没有被传入内容，那么 `label` 将会作为 checkbox 按钮后的介绍。 `value` 也与数组中的元素值相对应。 如果指定的值存在于数组中，就处于选择状态，反之亦然。

Option AOption BOption Cdisabledselected and disabled

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2hlY2tib3gtZ3JvdXAgdi1tb2RlbD1cImNoZWNrTGlzdFwiPlxuICAgIDxlbC1jaGVja2JveCBsYWJlbD1cIk9wdGlvbiBBXCIgdmFsdWU9XCJWYWx1ZSBBXCIgLz5cbiAgICA8ZWwtY2hlY2tib3ggbGFiZWw9XCJPcHRpb24gQlwiIHZhbHVlPVwiVmFsdWUgQlwiIC8+XG4gICAgPGVsLWNoZWNrYm94IGxhYmVsPVwiT3B0aW9uIENcIiB2YWx1ZT1cIlZhbHVlIENcIiAvPlxuICAgIDxlbC1jaGVja2JveCBsYWJlbD1cImRpc2FibGVkXCIgdmFsdWU9XCJWYWx1ZSBkaXNhYmxlZFwiIGRpc2FibGVkIC8+XG4gICAgPGVsLWNoZWNrYm94XG4gICAgICBsYWJlbD1cInNlbGVjdGVkIGFuZCBkaXNhYmxlZFwiXG4gICAgICB2YWx1ZT1cIlZhbHVlIHNlbGVjdGVkIGFuZCBkaXNhYmxlZFwiXG4gICAgICBkaXNhYmxlZFxuICAgIC8+XG4gIDwvZWwtY2hlY2tib3gtZ3JvdXA+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBjaGVja0xpc3QgPSByZWYoWydWYWx1ZSBzZWxlY3RlZCBhbmQgZGlzYWJsZWQnLCAnVmFsdWUgQSddKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/checkbox/grouping.vue)_

vue

```
<template>
  <el-checkbox-group v-model="checkList">
    <el-checkbox label="Option A" value="Value A" />
    <el-checkbox label="Option B" value="Value B" />
    <el-checkbox label="Option C" value="Value C" />
    <el-checkbox label="disabled" value="Value disabled" disabled />
    <el-checkbox
      label="selected and disabled"
      value="Value selected and disabled"
      disabled
    />
  </el-checkbox-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checkList = ref(['Value selected and disabled', 'Value A'])
</script>
```

隐藏源代码

## Options 属性 2.11.2 [​](#options-属性)

基础用法 `el-checkbox-group` 的快捷示例。 您可以通过 `props` 属性自定义 `options` 的别名。

Option AOption BOption Cdisabledselected and disabled

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2hlY2tib3gtZ3JvdXAgdi1tb2RlbD1cImNoZWNrTGlzdFwiIDpvcHRpb25zPVwib3B0aW9uc1wiIDpwcm9wcz1cInByb3BzXCIgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNoZWNrTGlzdCA9IHJlZihbJ1ZhbHVlIHNlbGVjdGVkIGFuZCBkaXNhYmxlZCcsICdWYWx1ZSBBJ10pXG5jb25zdCBwcm9wcyA9IHsgbGFiZWw6ICduYW1lJywgdmFsdWU6ICdpZCcsIGRpc2FibGVkOiAndW5hYmxlJyB9XG5jb25zdCBvcHRpb25zID0gW1xuICB7IG5hbWU6ICdPcHRpb24gQScsIGlkOiAnVmFsdWUgQScgfSxcbiAgeyBuYW1lOiAnT3B0aW9uIEInLCBpZDogJ1ZhbHVlIEInIH0sXG4gIHsgbmFtZTogJ09wdGlvbiBDJywgaWQ6ICdWYWx1ZSBDJyB9LFxuICB7IG5hbWU6ICdkaXNhYmxlZCcsIGlkOiAnVmFsdWUgZGlzYWJsZWQnLCB1bmFibGU6IHRydWUgfSxcbiAge1xuICAgIG5hbWU6ICdzZWxlY3RlZCBhbmQgZGlzYWJsZWQnLFxuICAgIGlkOiAnVmFsdWUgc2VsZWN0ZWQgYW5kIGRpc2FibGVkJyxcbiAgICB1bmFibGU6IHRydWUsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/checkbox/options.vue)_

vue

```
<template>
  <el-checkbox-group v-model="checkList" :options="options" :props="props" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checkList = ref(['Value selected and disabled', 'Value A'])
const props = { label: 'name', value: 'id', disabled: 'unable' }
const options = [
  { name: 'Option A', id: 'Value A' },
  { name: 'Option B', id: 'Value B' },
  { name: 'Option C', id: 'Value C' },
  { name: 'disabled', id: 'Value disabled', unable: true },
  {
    name: 'selected and disabled',
    id: 'Value selected and disabled',
    unable: true,
  },
]
</script>
```

隐藏源代码

## 中间状态 [​](#中间状态)

`indeterminate` 属性用以表示 checkbox 的不确定状态，一般用于实现全选的效果

 Check all

ShanghaiBeijingGuangzhouShenzhen

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2hlY2tib3hcbiAgICB2LW1vZGVsPVwiY2hlY2tBbGxcIlxuICAgIDppbmRldGVybWluYXRlPVwiaXNJbmRldGVybWluYXRlXCJcbiAgICBAY2hhbmdlPVwiaGFuZGxlQ2hlY2tBbGxDaGFuZ2VcIlxuICA+XG4gICAgQ2hlY2sgYWxsXG4gIDwvZWwtY2hlY2tib3g+XG4gIDxlbC1jaGVja2JveC1ncm91cFxuICAgIHYtbW9kZWw9XCJjaGVja2VkQ2l0aWVzXCJcbiAgICBAY2hhbmdlPVwiaGFuZGxlQ2hlY2tlZENpdGllc0NoYW5nZVwiXG4gID5cbiAgICA8ZWwtY2hlY2tib3ggdi1mb3I9XCJjaXR5IGluIGNpdGllc1wiIDprZXk9XCJjaXR5XCIgOmxhYmVsPVwiY2l0eVwiIDp2YWx1ZT1cImNpdHlcIj5cbiAgICAgIHt7IGNpdHkgfX1cbiAgICA8L2VsLWNoZWNrYm94PlxuICA8L2VsLWNoZWNrYm94LWdyb3VwPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBDaGVja2JveFZhbHVlVHlwZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgY2hlY2tBbGwgPSByZWYoZmFsc2UpXG5jb25zdCBpc0luZGV0ZXJtaW5hdGUgPSByZWYodHJ1ZSlcbmNvbnN0IGNoZWNrZWRDaXRpZXMgPSByZWYoWydTaGFuZ2hhaScsICdCZWlqaW5nJ10pXG5jb25zdCBjaXRpZXMgPSBbJ1NoYW5naGFpJywgJ0JlaWppbmcnLCAnR3Vhbmd6aG91JywgJ1NoZW56aGVuJ11cblxuY29uc3QgaGFuZGxlQ2hlY2tBbGxDaGFuZ2UgPSAodmFsOiBDaGVja2JveFZhbHVlVHlwZSkgPT4ge1xuICBjaGVja2VkQ2l0aWVzLnZhbHVlID0gdmFsID8gY2l0aWVzIDogW11cbiAgaXNJbmRldGVybWluYXRlLnZhbHVlID0gZmFsc2Vcbn1cbmNvbnN0IGhhbmRsZUNoZWNrZWRDaXRpZXNDaGFuZ2UgPSAodmFsdWU6IENoZWNrYm94VmFsdWVUeXBlW10pID0+IHtcbiAgY29uc3QgY2hlY2tlZENvdW50ID0gdmFsdWUubGVuZ3RoXG4gIGNoZWNrQWxsLnZhbHVlID0gY2hlY2tlZENvdW50ID09PSBjaXRpZXMubGVuZ3RoXG4gIGlzSW5kZXRlcm1pbmF0ZS52YWx1ZSA9IGNoZWNrZWRDb3VudCA+IDAgJiYgY2hlY2tlZENvdW50IDwgY2l0aWVzLmxlbmd0aFxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/checkbox/intermediate.vue)_

vue

```
<template>
  <el-checkbox
    v-model="checkAll"
    :indeterminate="isIndeterminate"
    @change="handleCheckAllChange"
  >
    Check all
  </el-checkbox>
  <el-checkbox-group
    v-model="checkedCities"
    @change="handleCheckedCitiesChange"
  >
    <el-checkbox v-for="city in cities" :key="city" :label="city" :value="city">
      {{ city }}
    </el-checkbox>
  </el-checkbox-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { CheckboxValueType } from 'element-plus'

const checkAll = ref(false)
const isIndeterminate = ref(true)
const checkedCities = ref(['Shanghai', 'Beijing'])
const cities = ['Shanghai', 'Beijing', 'Guangzhou', 'Shenzhen']

const handleCheckAllChange = (val: CheckboxValueType) => {
  checkedCities.value = val ? cities : []
  isIndeterminate.value = false
}
const handleCheckedCitiesChange = (value: CheckboxValueType[]) => {
  const checkedCount = value.length
  checkAll.value = checkedCount === cities.length
  isIndeterminate.value = checkedCount > 0 && checkedCount < cities.length
}
</script>
```

隐藏源代码

## 可选项目数量的限制 [​](#可选项目数量的限制)

使用 `min` 和 `max` 属性能够限制可以被勾选的项目的数量。

ShanghaiBeijingGuangzhouShenzhen

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2hlY2tib3gtZ3JvdXAgdi1tb2RlbD1cImNoZWNrZWRDaXRpZXNcIiA6bWluPVwiMVwiIDptYXg9XCIyXCI+XG4gICAgPGVsLWNoZWNrYm94IHYtZm9yPVwiY2l0eSBpbiBjaXRpZXNcIiA6a2V5PVwiY2l0eVwiIDpsYWJlbD1cImNpdHlcIiA6dmFsdWU9XCJjaXR5XCI+XG4gICAgICB7eyBjaXR5IH19XG4gICAgPC9lbC1jaGVja2JveD5cbiAgPC9lbC1jaGVja2JveC1ncm91cD5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNoZWNrZWRDaXRpZXMgPSByZWYoWydTaGFuZ2hhaScsICdCZWlqaW5nJ10pXG5jb25zdCBjaXRpZXMgPSBbJ1NoYW5naGFpJywgJ0JlaWppbmcnLCAnR3Vhbmd6aG91JywgJ1NoZW56aGVuJ11cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/checkbox/limitation.vue)_

vue

```
<template>
  <el-checkbox-group v-model="checkedCities" :min="1" :max="2">
    <el-checkbox v-for="city in cities" :key="city" :label="city" :value="city">
      {{ city }}
    </el-checkbox>
  </el-checkbox-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checkedCities = ref(['Shanghai', 'Beijing'])
const cities = ['Shanghai', 'Beijing', 'Guangzhou', 'Shenzhen']
</script>
```

隐藏源代码

## 按钮样式 [​](#按钮样式)

按钮样式的多选组合。

只需要把 `el-checkbox` 元素替换为 `el-checkbox-button` 元素即可。 此外，Element Plus 还提供了`size`属性。

ShanghaiBeijingGuangzhouShenzhen

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1jaGVja2JveC1ncm91cCB2LW1vZGVsPVwiY2hlY2tib3hHcm91cDFcIiBzaXplPVwibGFyZ2VcIj5cbiAgICAgIDxlbC1jaGVja2JveC1idXR0b24gdi1mb3I9XCJjaXR5IGluIGNpdGllc1wiIDprZXk9XCJjaXR5XCIgOnZhbHVlPVwiY2l0eVwiPlxuICAgICAgICB7eyBjaXR5IH19XG4gICAgICA8L2VsLWNoZWNrYm94LWJ1dHRvbj5cbiAgICA8L2VsLWNoZWNrYm94LWdyb3VwPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cImRlbW8tYnV0dG9uLXN0eWxlXCI+XG4gICAgPGVsLWNoZWNrYm94LWdyb3VwIHYtbW9kZWw9XCJjaGVja2JveEdyb3VwMlwiPlxuICAgICAgPGVsLWNoZWNrYm94LWJ1dHRvbiB2LWZvcj1cImNpdHkgaW4gY2l0aWVzXCIgOmtleT1cImNpdHlcIiA6dmFsdWU9XCJjaXR5XCI+XG4gICAgICAgIHt7IGNpdHkgfX1cbiAgICAgIDwvZWwtY2hlY2tib3gtYnV0dG9uPlxuICAgIDwvZWwtY2hlY2tib3gtZ3JvdXA+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwiZGVtby1idXR0b24tc3R5bGVcIj5cbiAgICA8ZWwtY2hlY2tib3gtZ3JvdXAgdi1tb2RlbD1cImNoZWNrYm94R3JvdXAzXCIgc2l6ZT1cInNtYWxsXCI+XG4gICAgICA8ZWwtY2hlY2tib3gtYnV0dG9uXG4gICAgICAgIHYtZm9yPVwiY2l0eSBpbiBjaXRpZXNcIlxuICAgICAgICA6a2V5PVwiY2l0eVwiXG4gICAgICAgIDp2YWx1ZT1cImNpdHlcIlxuICAgICAgICA6ZGlzYWJsZWQ9XCJjaXR5ID09PSAnQmVpamluZydcIlxuICAgICAgPlxuICAgICAgICB7eyBjaXR5IH19XG4gICAgICA8L2VsLWNoZWNrYm94LWJ1dHRvbj5cbiAgICA8L2VsLWNoZWNrYm94LWdyb3VwPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cImRlbW8tYnV0dG9uLXN0eWxlXCI+XG4gICAgPGVsLWNoZWNrYm94LWdyb3VwIHYtbW9kZWw9XCJjaGVja2JveEdyb3VwNFwiIHNpemU9XCJzbWFsbFwiIGRpc2FibGVkPlxuICAgICAgPGVsLWNoZWNrYm94LWJ1dHRvbiB2LWZvcj1cImNpdHkgaW4gY2l0aWVzXCIgOmtleT1cImNpdHlcIiA6dmFsdWU9XCJjaXR5XCI+XG4gICAgICAgIHt7IGNpdHkgfX1cbiAgICAgIDwvZWwtY2hlY2tib3gtYnV0dG9uPlxuICAgIDwvZWwtY2hlY2tib3gtZ3JvdXA+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgY2hlY2tib3hHcm91cDEgPSByZWYoWydTaGFuZ2hhaSddKVxuY29uc3QgY2hlY2tib3hHcm91cDIgPSByZWYoWydTaGFuZ2hhaSddKVxuY29uc3QgY2hlY2tib3hHcm91cDMgPSByZWYoWydTaGFuZ2hhaSddKVxuY29uc3QgY2hlY2tib3hHcm91cDQgPSByZWYoWydTaGFuZ2hhaSddKVxuY29uc3QgY2l0aWVzID0gWydTaGFuZ2hhaScsICdCZWlqaW5nJywgJ0d1YW5nemhvdScsICdTaGVuemhlbiddXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLWJ1dHRvbi1zdHlsZSB7XG4gIG1hcmdpbi10b3A6IDI0cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/checkbox/button-style.vue)_

vue

```
<template>
  <div>
    <el-checkbox-group v-model="checkboxGroup1" size="large">
      <el-checkbox-button v-for="city in cities" :key="city" :value="city">
        {{ city }}
      </el-checkbox-button>
    </el-checkbox-group>
  </div>
  <div class="demo-button-style">
    <el-checkbox-group v-model="checkboxGroup2">
      <el-checkbox-button v-for="city in cities" :key="city" :value="city">
        {{ city }}
      </el-checkbox-button>
    </el-checkbox-group>
  </div>
  <div class="demo-button-style">
    <el-checkbox-group v-model="checkboxGroup3" size="small">
      <el-checkbox-button
        v-for="city in cities"
        :key="city"
        :value="city"
        :disabled="city === 'Beijing'"
      >
        {{ city }}
      </el-checkbox-button>
    </el-checkbox-group>
  </div>
  <div class="demo-button-style">
    <el-checkbox-group v-model="checkboxGroup4" size="small" disabled>
      <el-checkbox-button v-for="city in cities" :key="city" :value="city">
        {{ city }}
      </el-checkbox-button>
    </el-checkbox-group>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checkboxGroup1 = ref(['Shanghai'])
const checkboxGroup2 = ref(['Shanghai'])
const checkboxGroup3 = ref(['Shanghai'])
const checkboxGroup4 = ref(['Shanghai'])
const cities = ['Shanghai', 'Beijing', 'Guangzhou', 'Shenzhen']
</script>

<style scoped>
.demo-button-style {
  margin-top: 24px;
}
</style>
```

隐藏源代码

## 带有边框 [​](#带有边框)

设置`border`属性可以渲染为带有边框的多选框。

Option1Option2

Option1Option2

Option1Option2

Option1Option2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1jaGVja2JveCB2LW1vZGVsPVwiY2hlY2tlZDFcIiBsYWJlbD1cIk9wdGlvbjFcIiBzaXplPVwibGFyZ2VcIiBib3JkZXIgLz5cbiAgICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNoZWNrZWQyXCIgbGFiZWw9XCJPcHRpb24yXCIgc2l6ZT1cImxhcmdlXCIgYm9yZGVyIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibXQtNFwiPlxuICAgIDxlbC1jaGVja2JveCB2LW1vZGVsPVwiY2hlY2tlZDNcIiBsYWJlbD1cIk9wdGlvbjFcIiBib3JkZXIgLz5cbiAgICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNoZWNrZWQ0XCIgbGFiZWw9XCJPcHRpb24yXCIgYm9yZGVyIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibXQtNFwiPlxuICAgIDxlbC1jaGVja2JveC1ncm91cCB2LW1vZGVsPVwiY2hlY2tib3hHcm91cDFcIiBzaXplPVwic21hbGxcIj5cbiAgICAgIDxlbC1jaGVja2JveCBsYWJlbD1cIk9wdGlvbjFcIiB2YWx1ZT1cIlZhbHVlMVwiIGJvcmRlciAvPlxuICAgICAgPGVsLWNoZWNrYm94IGxhYmVsPVwiT3B0aW9uMlwiIHZhbHVlPVwiVmFsdWUyXCIgYm9yZGVyIC8+XG4gICAgPC9lbC1jaGVja2JveC1ncm91cD5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJtdC00XCI+XG4gICAgPGVsLWNoZWNrYm94LWdyb3VwIHYtbW9kZWw9XCJjaGVja2JveEdyb3VwMVwiIHNpemU9XCJzbWFsbFwiPlxuICAgICAgPGVsLWNoZWNrYm94IGxhYmVsPVwiT3B0aW9uMVwiIHZhbHVlPVwiVmFsdWUxXCIgYm9yZGVyIGRpc2FibGVkIC8+XG4gICAgICA8ZWwtY2hlY2tib3ggbGFiZWw9XCJPcHRpb24yXCIgdmFsdWU9XCJWYWx1ZTJcIiBib3JkZXIgZGlzYWJsZWQgLz5cbiAgICA8L2VsLWNoZWNrYm94LWdyb3VwPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGNoZWNrZWQxID0gcmVmKHRydWUpXG5jb25zdCBjaGVja2VkMiA9IHJlZihmYWxzZSlcbmNvbnN0IGNoZWNrZWQzID0gcmVmKGZhbHNlKVxuY29uc3QgY2hlY2tlZDQgPSByZWYodHJ1ZSlcbmNvbnN0IGNoZWNrYm94R3JvdXAxID0gcmVmKFsnVmFsdWUxJ10pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/checkbox/with-border.vue)_

vue

```
<template>
  <div>
    <el-checkbox v-model="checked1" label="Option1" size="large" border />
    <el-checkbox v-model="checked2" label="Option2" size="large" border />
  </div>
  <div class="mt-4">
    <el-checkbox v-model="checked3" label="Option1" border />
    <el-checkbox v-model="checked4" label="Option2" border />
  </div>
  <div class="mt-4">
    <el-checkbox-group v-model="checkboxGroup1" size="small">
      <el-checkbox label="Option1" value="Value1" border />
      <el-checkbox label="Option2" value="Value2" border />
    </el-checkbox-group>
  </div>
  <div class="mt-4">
    <el-checkbox-group v-model="checkboxGroup1" size="small">
      <el-checkbox label="Option1" value="Value1" border disabled />
      <el-checkbox label="Option2" value="Value2" border disabled />
    </el-checkbox-group>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked1 = ref(true)
const checked2 = ref(false)
const checked3 = ref(false)
const checked4 = ref(true)
const checkboxGroup1 = ref(['Value1'])
</script>
```

隐藏源代码

## Checkbox API [​](#checkbox-api)

### Checkbox Attributes [​](#checkbox-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `string` / `number` / `boolean` | — |
| value 2.6.0 | 选中状态的值（只有在`checkbox-group`或者绑定对象类型为`array`时有效） | `string` / `number` / `boolean` / `object` | — |
| label | 选中状态的值，只有在绑定对象类型为 `array` 时有效。 如果没有 value， `label`则作为`value`使用 | `string` / `number` / `boolean` / `object` | — |
| true-value 2.6.0 | 选中时的值 | `string` / `number` | — |
| false-value 2.6.0 | 没有选中时的值 | `string` / `number` | — |
| disabled | 是否禁用 | `boolean` | false |
| border | 是否显示边框 | `boolean` | false |
| size | Checkbox 的尺寸 | `enum` | — |
| name | 原生 name 属性 | `string` | — |
| checked | 当前是否勾选 | `boolean` | false |
| indeterminate | 设置不确定状态，仅负责样式控制 | `boolean` | false |
| validate-event | 输入时是否触发表单的校验 | `boolean` | true |
| tabindex | 输入框的 tabindex | `string` / `number` | — |
| id | input id | `string` | — |
| aria-controls a11y 2.7.2 | 与 [aria-control](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-controls)一致, 当 `indeterminate`为 `true`时生效 | `string` | — |
| aria-label a11y | 原生 `aria-label`属性 | `string` | — |
| true-label deprecated | 选中时的值 | `string` / `number` | — |
| false-label deprecated | 没有选中时的值 | `string` / `number` | — |
| controls a11y deprecated | 和 [aria-control](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-controls)一致。当 `indeterminate` 为 `true` 时生效 | `string` | — |

### Checkbox Events [​](#checkbox-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当绑定值变化时触发的事件 | `Function` |

### Checkbox Slots [​](#checkbox-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## CheckboxGroup API [​](#checkboxgroup-api)

### CheckboxGroup Attributes [​](#checkboxgroup-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 绑定值 | `array` | \[\] |
| size | 多选框组尺寸 | `enum` | — |
| disabled | 是否禁用 | `boolean` | false |
| min | 可被勾选的 checkbox 的最小数量 | `number` | — |
| max | 可被勾选的 checkbox 的最大数量 | `number` | — |
| aria-label a11y 2.7.2 | 原生 `aria-label`属性 | `string` | — |
| text-color | 当按钮为活跃状态时的字体颜色 | `string` | #ffffff |
| fill | 当按钮为活跃状态时的边框和背景颜色 | `string` | #409eff |
| tag | 复选框组元素标签 | `string` | div |
| validate-event | 是否触发表单验证 | `boolean` | true |
| label a11y deprecated | 原生 `aria-label`属性 | `string` | — |
| options 2.11.2 | 选项的数据源， `value` 的 key 和 `label` 和 `disabled`可以通过 `props`自定义. | `array` | — |
| props 2.11.2 | options 的配置 | `object` | `{value: 'value', label: 'label', disabled: 'disabled'}` |
| type 2.11.5 | 用于渲染选项的组件类型（例如 `'button'`） | `enum` | 'checkbox' |

### CheckboxGroup Events [​](#checkboxgroup-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当绑定值变化时触发的事件 | `Function` |

### CheckboxGroup Slots [​](#checkboxgroup-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | Checkbox / Checkbox-button |

## CheckboxButton API [​](#checkboxbutton-api)

### CheckboxButton Attributes [​](#checkboxbutton-attributes)

| 名称 | 详情 | 类型 | 默认值 |
| --- | --- | --- | --- |
| value 2.6.0 | 选中状态的值，只有在绑定对象类型为 `array` 时有效。 | `string` / `number` / `boolean` / `object` | — |
| label | 选中状态的值，只有在绑定对象类型为 `array` 时有效。 如果没有 value， `label`则作为`value`使用 | `string` / `number` / `boolean` / `object` | — |
| true-value 2.6.0 | 选中时的值 | `string` / `number` | — |
| false-value 2.6.0 | 没有选中时的值 | `string` / `number` | — |
| disabled | 是否禁用 | `boolean` | false |
| name | 原生 name 属性 | `string` | — |
| checked | 当前是否勾选 | `boolean` | false |
| true-label deprecated | 选中时的值 | `string` / `number` | — |
| false-label deprecated | 没有选中时的值 | `string` / `number` | — |

### CheckboxButton Slots [​](#checkboxbutton-slots)

| 插槽名 | 描述 |
| --- | --- |
| default | 自定义默认内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/checkbox) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/checkbox.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/checkbox.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/72490874?v=4&size=64)](https://github.com/zuwenyin)[![](https://avatars.githubusercontent.com/u/140705167?v=4&size=64)](https://github.com/zhongli-kira)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/28594168?v=4&size=64)](https://github.com/neostfox)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/35138018?v=4&size=64)](https://github.com/tuskermanshu)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/36906371?v=4&size=64)](https://github.com/iamdin)[![](https://avatars.githubusercontent.com/u/59350883?v=4&size=64)](https://github.com/init-qy)[![](https://avatars.githubusercontent.com/u/43134418?v=4&size=64)](https://github.com/MonsterPi13)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/43210216?v=4&size=64)](https://github.com/ytx222)[![](https://avatars.githubusercontent.com/u/25120803?v=4&size=64)](https://github.com/leeonon)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/5445667?v=4&size=64)](https://github.com/iceshou)[![](https://avatars.githubusercontent.com/u/45122329?v=4&size=64)](https://github.com/cokemine)[![](https://avatars.githubusercontent.com/u/188531008?v=4&size=64)](https://github.com/dengguangmiaoyyds)[![](https://avatars.githubusercontent.com/u/25742988?v=4&size=64)](https://github.com/Geekhyt)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)

[Cascader 级联选择器](https://element-plus.org/zh-CN/component/cascader)

[ColorPickerPanel 颜色选择器面板](https://element-plus.org/zh-CN/component/color-picker-panel)


