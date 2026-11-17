## Segmented 分段控制器 ​

**URL:** https://element-plus.org/zh-CN/component/segmented

**Contents:**
- Segmented 分段控制器 ​
- 基础用法 ​
- 配置方向2.8.7 ​
- 禁用状态 ​
- 自定义选项 2.9.8 ​
- Block 分段选择器 ​
- 自定义内容 ​
- 自定义样式 ​
- API ​
  - 属性 ​

用于展示多个选项并允许用户选择其中单个选项。

设置 disabled 属性来禁用一些选项。

当您的 options 格式不同于默认格式时，可通过 props 属性自定义 options

设置block为true以适应父元素的宽度。

设置 default slot 位来渲染自定义内容。

**Examples:**

Example 1 (vue):
```vue
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

Example 2 (vue):
```vue
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

Example 3 (vue):
```vue
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

Example 4 (vue):
```vue
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

---
