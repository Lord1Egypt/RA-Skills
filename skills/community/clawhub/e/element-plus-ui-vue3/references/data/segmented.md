---
name: "segmented"
description: "Segmented 分段控制器 -- Element Plus Vue3 桌面端组件。Invoke when user needs Segmented 分段控制器 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/segmented.html"
---

---

# Segmented 分段控制器 [​](#segmented-分段控制器)

更新日志待解决

1

用于展示多个选项并允许用户选择其中单个选项。

## 基础用法 [​](#基础用法)

设置`v-model`为选项值。

Mon

Tue

Wed

Thu

Fri

Sat

Sun

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LWNvbCBpdGVtcy1zdGFydCBnYXAtNFwiPlxuICAgIDxlbC1zZWdtZW50ZWQgdi1tb2RlbD1cInZhbHVlXCIgOm9wdGlvbnM9XCJvcHRpb25zXCIgc2l6ZT1cImxhcmdlXCIgLz5cbiAgICA8ZWwtc2VnbWVudGVkIHYtbW9kZWw9XCJ2YWx1ZVwiIDpvcHRpb25zPVwib3B0aW9uc1wiIHNpemU9XCJkZWZhdWx0XCIgLz5cbiAgICA8ZWwtc2VnbWVudGVkIHYtbW9kZWw9XCJ2YWx1ZVwiIDpvcHRpb25zPVwib3B0aW9uc1wiIHNpemU9XCJzbWFsbFwiIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoJ01vbicpXG5cbmNvbnN0IG9wdGlvbnMgPSBbJ01vbicsICdUdWUnLCAnV2VkJywgJ1RodScsICdGcmknLCAnU2F0JywgJ1N1biddXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/segmented/basic.vue)_

vue

```
<template>
  <div class="flex flex-col items-start gap-4">
    <el-segmented v-model="value" :options="options" size="large" />
    <el-segmented v-model="value" :options="options" size="default" />
    <el-segmented v-model="value" :options="options" size="small" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('Mon')

const options = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
</script>
```

隐藏源代码

## 配置方向2.8.7 [​](#配置方向)

设置 `vertical` 来改变方向。

large

default

small

Horizontal

Vertical

Apple

Cherry

Grape

Orange

Pear

Watermelon

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1zZWdtZW50ZWRcbiAgICAgIHYtbW9kZWw9XCJzaXplXCJcbiAgICAgIDpvcHRpb25zPVwic2l6ZU9wdGlvbnNcIlxuICAgICAgc3R5bGU9XCJtYXJnaW4tYm90dG9tOiAxcmVtXCJcbiAgICAvPlxuICAgIDxiciAvPlxuICAgIDxlbC1zZWdtZW50ZWRcbiAgICAgIHYtbW9kZWw9XCJkaXJlY3Rpb25cIlxuICAgICAgOm9wdGlvbnM9XCJkaXJlY3Rpb25PcHRpb25zXCJcbiAgICAgIHN0eWxlPVwibWFyZ2luLWJvdHRvbTogMXJlbVwiXG4gICAgLz5cbiAgICA8YnIgLz5cbiAgICA8ZWwtc2VnbWVudGVkXG4gICAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICAgIDpkaXJlY3Rpb249XCJkaXJlY3Rpb25cIlxuICAgICAgOnNpemU9XCJzaXplXCJcbiAgICA+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJzY29wZVwiPlxuICAgICAgICA8ZGl2XG4gICAgICAgICAgOmNsYXNzPVwiW1xuICAgICAgICAgICAgJ2ZsZXgnLFxuICAgICAgICAgICAgJ2l0ZW1zLWNlbnRlcicsXG4gICAgICAgICAgICAnZ2FwLTInLFxuICAgICAgICAgICAgJ2ZsZXgtY29sJyxcbiAgICAgICAgICAgIGRpcmVjdGlvbiA9PT0gJ2hvcml6b250YWwnICYmICdwLTInLFxuICAgICAgICAgIF1cIlxuICAgICAgICA+XG4gICAgICAgICAgPGVsLWljb24gc2l6ZT1cIjIwXCI+XG4gICAgICAgICAgICA8Y29tcG9uZW50IDppcz1cInNjb3BlLml0ZW0uaWNvblwiIC8+XG4gICAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICAgIDxkaXY+e3sgc2NvcGUuaXRlbS5sYWJlbCB9fTwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1zZWdtZW50ZWQ+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7XG4gIEFwcGxlLFxuICBDaGVycnksXG4gIEdyYXBlLFxuICBPcmFuZ2UsXG4gIFBlYXIsXG4gIFdhdGVybWVsb24sXG59IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFNlZ21lbnRlZFByb3BzIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZignQXBwbGUnKVxuY29uc3QgZGlyZWN0aW9uID0gcmVmPFNlZ21lbnRlZFByb3BzWydkaXJlY3Rpb24nXT4oJ2hvcml6b250YWwnKVxuY29uc3Qgc2l6ZSA9IHJlZjxTZWdtZW50ZWRQcm9wc1snc2l6ZSddPignZGVmYXVsdCcpXG5cbmNvbnN0IGRpcmVjdGlvbk9wdGlvbnMgPSBbXG4gIHsgbGFiZWw6ICdIb3Jpem9udGFsJywgdmFsdWU6ICdob3Jpem9udGFsJyB9LFxuICB7IGxhYmVsOiAnVmVydGljYWwnLCB2YWx1ZTogJ3ZlcnRpY2FsJyB9LFxuXVxuXG5jb25zdCBzaXplT3B0aW9ucyA9IFsnbGFyZ2UnLCAnZGVmYXVsdCcsICdzbWFsbCddXG5cbmNvbnN0IG9wdGlvbnMgPSBbXG4gIHtcbiAgICBsYWJlbDogJ0FwcGxlJyxcbiAgICB2YWx1ZTogJ0FwcGxlJyxcbiAgICBpY29uOiBBcHBsZSxcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAnQ2hlcnJ5JyxcbiAgICB2YWx1ZTogJ0NoZXJyeScsXG4gICAgaWNvbjogQ2hlcnJ5LFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdHcmFwZScsXG4gICAgdmFsdWU6ICdHcmFwZScsXG4gICAgaWNvbjogR3JhcGUsXG4gIH0sXG4gIHtcbiAgICBsYWJlbDogJ09yYW5nZScsXG4gICAgdmFsdWU6ICdPcmFuZ2UnLFxuICAgIGljb246IE9yYW5nZSxcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAnUGVhcicsXG4gICAgdmFsdWU6ICdQZWFyJyxcbiAgICBpY29uOiBQZWFyLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdXYXRlcm1lbG9uJyxcbiAgICB2YWx1ZTogJ1dhdGVybWVsb24nLFxuICAgIGljb246IFdhdGVybWVsb24sXG4gICAgZGlzYWJsZWQ6IHRydWUsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/segmented/custom-direction.vue)_

vue

```
<template>
  <div>
    <el-segmented
      v-model="size"
      :options="sizeOptions"
      style="margin-bottom: 1rem"
    />
    <br />
    <el-segmented
      v-model="direction"
      :options="directionOptions"
      style="margin-bottom: 1rem"
    />
    <br />
    <el-segmented
      v-model="value"
      :options="options"
      :direction="direction"
      :size="size"
    >
      <template #default="scope">
        <div
          :class="[
            'flex',
            'items-center',
            'gap-2',
            'flex-col',
            direction === 'horizontal' && 'p-2',
          ]"
        >
          <el-icon size="20">
            <component :is="scope.item.icon" />
          </el-icon>
          <div>{{ scope.item.label }}</div>
        </div>
      </template>
    </el-segmented>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import {
  Apple,
  Cherry,
  Grape,
  Orange,
  Pear,
  Watermelon,
} from '@element-plus/icons-vue'

import type { SegmentedProps } from 'element-plus'

const value = ref('Apple')
const direction = ref<SegmentedProps['direction']>('horizontal')
const size = ref<SegmentedProps['size']>('default')

const directionOptions = [
  { label: 'Horizontal', value: 'horizontal' },
  { label: 'Vertical', value: 'vertical' },
]

const sizeOptions = ['large', 'default', 'small']

const options = [
  {
    label: 'Apple',
    value: 'Apple',
    icon: Apple,
  },
  {
    label: 'Cherry',
    value: 'Cherry',
    icon: Cherry,
  },
  {
    label: 'Grape',
    value: 'Grape',
    icon: Grape,
  },
  {
    label: 'Orange',
    value: 'Orange',
    icon: Orange,
  },
  {
    label: 'Pear',
    value: 'Pear',
    icon: Pear,
  },
  {
    label: 'Watermelon',
    value: 'Watermelon',
    icon: Watermelon,
    disabled: true,
  },
]
</script>
```

隐藏源代码

## 禁用状态 [​](#禁用状态)

设置 `disabled` 属性来禁用一些选项。

Mon

Tue

Wed

Thu

Fri

Sat

Sun

Mon

Tue

Wed

Thu

Fri

Sat

Sun

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LWNvbCBpdGVtcy1zdGFydCBnYXAtNFwiPlxuICAgIDxlbC1zZWdtZW50ZWQgdi1tb2RlbD1cInZhbHVlXCIgOm9wdGlvbnM9XCJvcHRpb25zXCIgZGlzYWJsZWQgLz5cbiAgICA8ZWwtc2VnbWVudGVkIHYtbW9kZWw9XCJ2YWx1ZVwiIDpvcHRpb25zPVwib3B0aW9uc1wiIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoJ01vbicpXG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgbGFiZWw6ICdNb24nLFxuICAgIHZhbHVlOiAnTW9uJyxcbiAgICBkaXNhYmxlZDogdHJ1ZSxcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAnVHVlJyxcbiAgICB2YWx1ZTogJ1R1ZScsXG4gIH0sXG4gIHtcbiAgICBsYWJlbDogJ1dlZCcsXG4gICAgdmFsdWU6ICdXZWQnLFxuICAgIGRpc2FibGVkOiB0cnVlLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdUaHUnLFxuICAgIHZhbHVlOiAnVGh1JyxcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAnRnJpJyxcbiAgICB2YWx1ZTogJ0ZyaScsXG4gICAgZGlzYWJsZWQ6IHRydWUsXG4gIH0sXG4gIHtcbiAgICBsYWJlbDogJ1NhdCcsXG4gICAgdmFsdWU6ICdTYXQnLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdTdW4nLFxuICAgIHZhbHVlOiAnU3VuJyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/segmented/disabled.vue)_

vue

```
<template>
  <div class="flex flex-col items-start gap-4">
    <el-segmented v-model="value" :options="options" disabled />
    <el-segmented v-model="value" :options="options" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('Mon')
const options = [
  {
    label: 'Mon',
    value: 'Mon',
    disabled: true,
  },
  {
    label: 'Tue',
    value: 'Tue',
  },
  {
    label: 'Wed',
    value: 'Wed',
    disabled: true,
  },
  {
    label: 'Thu',
    value: 'Thu',
  },
  {
    label: 'Fri',
    value: 'Fri',
    disabled: true,
  },
  {
    label: 'Sat',
    value: 'Sat',
  },
  {
    label: 'Sun',
    value: 'Sun',
  },
]
</script>
```

隐藏源代码

## 自定义选项 2.9.8 [​](#自定义选项)

当您的 `options` 格式不同于默认格式时，可通过 `props` 属性自定义 `options`

Mon

Tue

Wed

Thu

Fri

Sat

Sun

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1zZWdtZW50ZWQgdi1tb2RlbD1cInZhbHVlXCIgOm9wdGlvbnM9XCJvcHRpb25zXCIgOnByb3BzPVwicHJvcHNcIiAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCdNb24nKVxuY29uc3QgcHJvcHMgPSB7XG4gIGxhYmVsOiAnbXlMYWJlbCcsXG4gIHZhbHVlOiAnbXlWYWx1ZScsXG4gIGRpc2FibGVkOiAnbXlEaXNhYmxlZCcsXG59XG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgbXlMYWJlbDogJ01vbicsXG4gICAgbXlWYWx1ZTogJ01vbicsXG4gICAgbXlEaXNhYmxlZDogdHJ1ZSxcbiAgfSxcbiAge1xuICAgIG15TGFiZWw6ICdUdWUnLFxuICAgIG15VmFsdWU6ICdUdWUnLFxuICB9LFxuICB7XG4gICAgbXlMYWJlbDogJ1dlZCcsXG4gICAgbXlWYWx1ZTogJ1dlZCcsXG4gICAgbXlEaXNhYmxlZDogdHJ1ZSxcbiAgfSxcbiAge1xuICAgIG15TGFiZWw6ICdUaHUnLFxuICAgIG15VmFsdWU6ICdUaHUnLFxuICB9LFxuICB7XG4gICAgbXlMYWJlbDogJ0ZyaScsXG4gICAgbXlWYWx1ZTogJ0ZyaScsXG4gICAgbXlEaXNhYmxlZDogdHJ1ZSxcbiAgfSxcbiAge1xuICAgIG15TGFiZWw6ICdTYXQnLFxuICAgIG15VmFsdWU6ICdTYXQnLFxuICB9LFxuICB7XG4gICAgbXlMYWJlbDogJ1N1bicsXG4gICAgbXlWYWx1ZTogJ1N1bicsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/segmented/props.vue)_

vue

```
<template>
  <div>
    <el-segmented v-model="value" :options="options" :props="props" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('Mon')
const props = {
  label: 'myLabel',
  value: 'myValue',
  disabled: 'myDisabled',
}
const options = [
  {
    myLabel: 'Mon',
    myValue: 'Mon',
    myDisabled: true,
  },
  {
    myLabel: 'Tue',
    myValue: 'Tue',
  },
  {
    myLabel: 'Wed',
    myValue: 'Wed',
    myDisabled: true,
  },
  {
    myLabel: 'Thu',
    myValue: 'Thu',
  },
  {
    myLabel: 'Fri',
    myValue: 'Fri',
    myDisabled: true,
  },
  {
    myLabel: 'Sat',
    myValue: 'Sat',
  },
  {
    myLabel: 'Sun',
    myValue: 'Sun',
  },
]
</script>
```

隐藏源代码

## Block 分段选择器 [​](#block-分段选择器)

设置`block`为`true`以适应父元素的宽度。

Mon

Tue

Wed

Thu

Fri

Sat

Sunday long long long long long long long

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1zZWdtZW50ZWQgdi1tb2RlbD1cInZhbHVlXCIgOm9wdGlvbnM9XCJvcHRpb25zXCIgYmxvY2sgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZignTW9uJylcblxuY29uc3Qgb3B0aW9ucyA9IFtcbiAgJ01vbicsXG4gICdUdWUnLFxuICAnV2VkJyxcbiAgJ1RodScsXG4gICdGcmknLFxuICAnU2F0JyxcbiAgJ1N1bmRheSBsb25nIGxvbmcgbG9uZyBsb25nIGxvbmcgbG9uZyBsb25nJyxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/segmented/block.vue)_

vue

```
<template>
  <div>
    <el-segmented v-model="value" :options="options" block />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('Mon')

const options = [
  'Mon',
  'Tue',
  'Wed',
  'Thu',
  'Fri',
  'Sat',
  'Sunday long long long long long long long',
]
</script>
```

隐藏源代码

## 自定义内容 [​](#自定义内容)

设置 default slot 位来渲染自定义内容。

Apple

Cherry

Grape

Orange

Pear

Watermelon

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1zZWdtZW50ZWQgdi1tb2RlbD1cInZhbHVlXCIgOm9wdGlvbnM9XCJvcHRpb25zXCI+XG4gICAgICA8dGVtcGxhdGUgI2RlZmF1bHQ9XCJzY29wZVwiPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LWNvbCBpdGVtcy1jZW50ZXIgZ2FwLTIgcC0yXCI+XG4gICAgICAgICAgPGVsLWljb24gc2l6ZT1cIjIwXCI+XG4gICAgICAgICAgICA8Y29tcG9uZW50IDppcz1cInNjb3BlLml0ZW0uaWNvblwiIC8+XG4gICAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICAgIDxkaXY+e3sgc2NvcGUuaXRlbS5sYWJlbCB9fTwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1zZWdtZW50ZWQ+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7XG4gIEFwcGxlLFxuICBDaGVycnksXG4gIEdyYXBlLFxuICBPcmFuZ2UsXG4gIFBlYXIsXG4gIFdhdGVybWVsb24sXG59IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZignQXBwbGUnKVxuXG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgbGFiZWw6ICdBcHBsZScsXG4gICAgdmFsdWU6ICdBcHBsZScsXG4gICAgaWNvbjogQXBwbGUsXG4gIH0sXG4gIHtcbiAgICBsYWJlbDogJ0NoZXJyeScsXG4gICAgdmFsdWU6ICdDaGVycnknLFxuICAgIGljb246IENoZXJyeSxcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAnR3JhcGUnLFxuICAgIHZhbHVlOiAnR3JhcGUnLFxuICAgIGljb246IEdyYXBlLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdPcmFuZ2UnLFxuICAgIHZhbHVlOiAnT3JhbmdlJyxcbiAgICBpY29uOiBPcmFuZ2UsXG4gIH0sXG4gIHtcbiAgICBsYWJlbDogJ1BlYXInLFxuICAgIHZhbHVlOiAnUGVhcicsXG4gICAgaWNvbjogUGVhcixcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAnV2F0ZXJtZWxvbicsXG4gICAgdmFsdWU6ICdXYXRlcm1lbG9uJyxcbiAgICBpY29uOiBXYXRlcm1lbG9uLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/segmented/custom-content.vue)_

vue

```
<template>
  <div>
    <el-segmented v-model="value" :options="options">
      <template #default="scope">
        <div class="flex flex-col items-center gap-2 p-2">
          <el-icon size="20">
            <component :is="scope.item.icon" />
          </el-icon>
          <div>{{ scope.item.label }}</div>
        </div>
      </template>
    </el-segmented>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import {
  Apple,
  Cherry,
  Grape,
  Orange,
  Pear,
  Watermelon,
} from '@element-plus/icons-vue'

const value = ref('Apple')

const options = [
  {
    label: 'Apple',
    value: 'Apple',
    icon: Apple,
  },
  {
    label: 'Cherry',
    value: 'Cherry',
    icon: Cherry,
  },
  {
    label: 'Grape',
    value: 'Grape',
    icon: Grape,
  },
  {
    label: 'Orange',
    value: 'Orange',
    icon: Orange,
  },
  {
    label: 'Pear',
    value: 'Pear',
    icon: Pear,
  },
  {
    label: 'Watermelon',
    value: 'Watermelon',
    icon: Watermelon,
  },
]
</script>
```

隐藏源代码

## 自定义样式 [​](#自定义样式)

使用 CSS 变量设置自定义样式。

Delicacy

Desserts&Drinks

Fresh foods

Supermarket

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY3VzdG9tLXN0eWxlXCI+XG4gICAgPGVsLXNlZ21lbnRlZCB2LW1vZGVsPVwidmFsdWVcIiA6b3B0aW9ucz1cIm9wdGlvbnNcIiAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCdEZWxpY2FjeScpXG5cbmNvbnN0IG9wdGlvbnMgPSBbJ0RlbGljYWN5JywgJ0Rlc3NlcnRzJkRyaW5rcycsICdGcmVzaCBmb29kcycsICdTdXBlcm1hcmtldCddXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5jdXN0b20tc3R5bGUgLmVsLXNlZ21lbnRlZCB7XG4gIC0tZWwtc2VnbWVudGVkLWl0ZW0tc2VsZWN0ZWQtY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3ItcHJpbWFyeSk7XG4gIC0tZWwtc2VnbWVudGVkLWl0ZW0tc2VsZWN0ZWQtYmctY29sb3I6ICNmZmQxMDA7XG4gIC0tZWwtYm9yZGVyLXJhZGl1cy1iYXNlOiAxNnB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/segmented/custom-style.vue)_

vue

```
<template>
  <div class="custom-style">
    <el-segmented v-model="value" :options="options" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('Delicacy')

const options = ['Delicacy', 'Desserts&Drinks', 'Fresh foods', 'Supermarket']
</script>

<style scoped>
.custom-style .el-segmented {
  --el-segmented-item-selected-color: var(--el-text-color-primary);
  --el-segmented-item-selected-bg-color: #ffd100;
  --el-border-radius-base: 16px;
}
</style>
```

隐藏源代码

## API [​](#api)

### 属性 [​](#属性)

| 名称 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 绑定值 | `string` / `number` / `boolean` | — |
| options | 选项的数据 | `array` | \[\] |
| [props](#props) 2.9.8 | 配置选项，详见下表 | `object` | — |
| size | 组件大小 | `enum` | '' |
| block | 撑满父元素宽度 | `boolean` | false |
| disabled | 是否禁用 | `boolean` | false |
| validate-event | 是否触发表单验证 | `boolean` | true |
| name | 原生 name 属性 | `string` | — |
| id | 原生 `id` 属性 | `string` | — |
| aria-label a11y | 原生 `aria-label` 属性 | `string` | — |
| direction 2.8.7 | 展示的方向 | `enum` | horizontal |

### props [​](#props)

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| value | 指定键为节点对象的某个属性值 | `string` | value |
| label | 指定标签为节点对象的某个属性值 | `string` | label |
| disabled | 指定禁用状态为节点对象的某个属性值 | `string` | disabled |

### 事件 [​](#事件)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| change | 当所选值更改时触发，参数是当前选中的值 | `Function` |

### Slots [​](#slots)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| default | 自定义 Option 模板 | `object` |

## 类型声明 [​](#类型声明)

显示类型声明

ts

```
type Option = Record<string, any> | string | number | boolean
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/segmented) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/segmented.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/segmented.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/124225078?v=4&size=64)](https://github.com/ykcory)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/52314078?v=4&size=64)](https://github.com/vaebe)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/35400818?v=4&size=64)](https://github.com/ToyCat93)[![](https://avatars.githubusercontent.com/u/47178158?v=4&size=64)](https://github.com/Aaron-zon)[![](https://avatars.githubusercontent.com/u/100760523?v=4&size=64)](https://github.com/jhinzhou)[![](https://avatars.githubusercontent.com/u/31943807?v=4&size=64)](https://github.com/ayay459547)[![](https://avatars.githubusercontent.com/u/50254496?v=4&size=64)](https://github.com/LoTwT)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)

[Statistic 统计组件](https://element-plus.org/zh-CN/component/statistic)

[Affix 固钉](https://element-plus.org/zh-CN/component/affix)


