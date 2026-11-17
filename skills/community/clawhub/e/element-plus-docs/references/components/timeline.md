## Timeline 时间线 ​

**URL:** https://element-plus.org/zh-CN/component/timeline

**Contents:**
- Timeline 时间线 ​
- 基础用法 ​
- Mode 2.13.1 ​
- ⾃定义节点样式 ​
- ⾃定义时间戳 ​
    - Update Github template
    - Update Github template
    - Update Github template
- 垂直居中 ​
    - Update Github template

Timeline 可拆分成多个按照时间戳排列的活动， 时间戳是其区分于其他控件的重要特征， 使用时注意与 Steps 步骤条等区分。

使用 mode 来控制时间线与内容的相对位置。

在 2.13.1 之后，el-timeline 显式设置了内边距样式。 如果您在项目中覆盖了 ul 标签的填充样式，请检查以确保布局正确。

可根据实际场景⾃定义节点尺⼨、颜⾊，或直接使⽤图标。

当内容在垂直⽅向上过⾼时，可将时间戳置于内容之上。

Tom committed 2018/4/12 20:46

Tom committed 2018/4/3 20:46

Tom committed 2018/4/2 20:46

垂直居中样式的 Timeline-Item

Tom committed 2018/4/12 20:46

Tom committed 2018/4/3 20:46

使用 reverse 属性来控制节点的顺序。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-timeline>
    <el-timeline-item
      v-for="(activity, index) in activities"
      :key="index"
      :timestamp="activity.timestamp"
    >
      {{ activity.content }}
    </el-timeline-item>
  </el-timeline>
</template>

<script lang="ts" setup>
const activities = [
  {
    content: 'Event start',
    timestamp: '2018-04-15',
  },
  {
    content: 'Approved',
    timestamp: '2018-04-13',
  },
  {
    content: 'Success',
    timestamp: '2018-04-11',
  },
]
</script>
```

Example 2 (vue):
```vue
<template>
  <el-radio-group v-model="mode">
    <el-radio-button label="start" value="start" />
    <el-radio-button label="alternate" value="alternate" />
    <el-radio-button label="alternate-reverse" value="alternate-reverse" />
    <el-radio-button label="end" value="end" />
  </el-radio-group>

  <el-timeline class="mt-4" :mode="mode">
    <el-timeline-item
      v-for="(activity, index) in activities"
      :key="index"
      :timestamp="activity.timestamp"
    >
      {{ activity.content }}
    </el-timeline-item>
  </el-timeline>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TimelineProps } from 'element-plus'

const activities = [
  {
    content: 'Event start',
    timestamp: '2018-04-15',
  },
  {
    content: 'Approved',
    timestamp: '2018-04-13',
  },
  {
    content: 'Success',
    timestamp: '2018-04-11',
  },
]

const mode = ref<TimelineProps['mode']>('start')
</script>
```

Example 3 (typescript):
```typescript
<template>
  <el-timeline>
    <el-timeline-item
      v-for="(activity, index) in activities"
      :key="index"
      :icon="activity.icon"
      :type="activity.type"
      :color="activity.color"
      :size="activity.size"
      :hollow="activity.hollow"
      :timestamp="activity.timestamp"
    >
      {{ activity.content }}
    </el-timeline-item>
  </el-timeline>
</template>

<script lang="ts" setup>
import { MoreFilled } from '@element-plus/icons-vue'

import type { TimelineItemProps } from 'element-plus'

interface ActivityType extends Partial<TimelineItemProps> {
  content: string
}

const activities: ActivityType[] = [
  {
    content: 'Custom icon',
    timestamp: '2018-04-12 20:46',
    size: 'large',
    type: 'primary',
    icon: MoreFilled,
  },
  {
    content: 'Custom color',
    timestamp: '2018-04-03 20:46',
    color: '#0bbd87',
  },
  {
    content: 'Custom size',
    timestamp: '2018-04-03 20:46',
    size: 'large',
  },
  {
    content: 'Custom hollow',
    timestamp: '2018-04-03 20:46',
    type: 'primary',
    hollow: true,
  },
  {
    content: 'Default node',
    timestamp: '2018-04-03 20:46',
  },
]
</script>
```

Example 4 (vue):
```vue
<template>
  <el-timeline>
    <el-timeline-item timestamp="2018/4/12" placement="top">
      <el-card>
        <h4>Update Github template</h4>
        <p>Tom committed 2018/4/12 20:46</p>
      </el-card>
    </el-timeline-item>
    <el-timeline-item timestamp="2018/4/3" placement="top">
      <el-card>
        <h4>Update Github template</h4>
        <p>Tom committed 2018/4/3 20:46</p>
      </el-card>
    </el-timeline-item>
    <el-timeline-item timestamp="2018/4/2" placement="top">
      <el-card>
        <h4>Update Github template</h4>
        <p>Tom committed 2018/4/2 20:46</p>
      </el-card>
    </el-timeline-item>
  </el-timeline>
</template>
```

---
