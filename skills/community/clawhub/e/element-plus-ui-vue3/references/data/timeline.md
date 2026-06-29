---
name: "timeline"
description: "Timeline 时间线 -- Element Plus Vue3 桌面端组件。Invoke when user needs Timeline 时间线 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/timeline.html"
---

---

# Timeline 时间线 [​](#timeline-时间线)

更新日志待解决

2

可视化地呈现时间流信息。

## 基础用法 [​](#基础用法)

Timeline 可拆分成多个按照时间戳排列的活动， 时间戳是其区分于其他控件的重要特征， 使用时注意与 Steps 步骤条等区分。

-   Event start

    2018-04-15

-   Approved

    2018-04-13

-   Success

    2018-04-11

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGltZWxpbmU+XG4gICAgPGVsLXRpbWVsaW5lLWl0ZW1cbiAgICAgIHYtZm9yPVwiKGFjdGl2aXR5LCBpbmRleCkgaW4gYWN0aXZpdGllc1wiXG4gICAgICA6a2V5PVwiaW5kZXhcIlxuICAgICAgOnRpbWVzdGFtcD1cImFjdGl2aXR5LnRpbWVzdGFtcFwiXG4gICAgPlxuICAgICAge3sgYWN0aXZpdHkuY29udGVudCB9fVxuICAgIDwvZWwtdGltZWxpbmUtaXRlbT5cbiAgPC9lbC10aW1lbGluZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5jb25zdCBhY3Rpdml0aWVzID0gW1xuICB7XG4gICAgY29udGVudDogJ0V2ZW50IHN0YXJ0JyxcbiAgICB0aW1lc3RhbXA6ICcyMDE4LTA0LTE1JyxcbiAgfSxcbiAge1xuICAgIGNvbnRlbnQ6ICdBcHByb3ZlZCcsXG4gICAgdGltZXN0YW1wOiAnMjAxOC0wNC0xMycsXG4gIH0sXG4gIHtcbiAgICBjb250ZW50OiAnU3VjY2VzcycsXG4gICAgdGltZXN0YW1wOiAnMjAxOC0wNC0xMScsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/timeline/basic.vue)_

vue

```
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

隐藏源代码

## Mode 2.13.1 [​](#mode)

使用 `mode` 来控制时间线与内容的相对位置。

TIP

在 2.13.1 之后，`el-timeline` 显式设置了内边距样式。 如果您在项目中覆盖了 `ul` 标签的填充样式，请检查以确保布局正确。

startalternatealternate-reverseend

-   Event start

    2018-04-15

-   Approved

    2018-04-13

-   Success

    2018-04-11

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cIm1vZGVcIj5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIGxhYmVsPVwic3RhcnRcIiB2YWx1ZT1cInN0YXJ0XCIgLz5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIGxhYmVsPVwiYWx0ZXJuYXRlXCIgdmFsdWU9XCJhbHRlcm5hdGVcIiAvPlxuICAgIDxlbC1yYWRpby1idXR0b24gbGFiZWw9XCJhbHRlcm5hdGUtcmV2ZXJzZVwiIHZhbHVlPVwiYWx0ZXJuYXRlLXJldmVyc2VcIiAvPlxuICAgIDxlbC1yYWRpby1idXR0b24gbGFiZWw9XCJlbmRcIiB2YWx1ZT1cImVuZFwiIC8+XG4gIDwvZWwtcmFkaW8tZ3JvdXA+XG5cbiAgPGVsLXRpbWVsaW5lIGNsYXNzPVwibXQtNFwiIDptb2RlPVwibW9kZVwiPlxuICAgIDxlbC10aW1lbGluZS1pdGVtXG4gICAgICB2LWZvcj1cIihhY3Rpdml0eSwgaW5kZXgpIGluIGFjdGl2aXRpZXNcIlxuICAgICAgOmtleT1cImluZGV4XCJcbiAgICAgIDp0aW1lc3RhbXA9XCJhY3Rpdml0eS50aW1lc3RhbXBcIlxuICAgID5cbiAgICAgIHt7IGFjdGl2aXR5LmNvbnRlbnQgfX1cbiAgICA8L2VsLXRpbWVsaW5lLWl0ZW0+XG4gIDwvZWwtdGltZWxpbmU+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFRpbWVsaW5lUHJvcHMgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGFjdGl2aXRpZXMgPSBbXG4gIHtcbiAgICBjb250ZW50OiAnRXZlbnQgc3RhcnQnLFxuICAgIHRpbWVzdGFtcDogJzIwMTgtMDQtMTUnLFxuICB9LFxuICB7XG4gICAgY29udGVudDogJ0FwcHJvdmVkJyxcbiAgICB0aW1lc3RhbXA6ICcyMDE4LTA0LTEzJyxcbiAgfSxcbiAge1xuICAgIGNvbnRlbnQ6ICdTdWNjZXNzJyxcbiAgICB0aW1lc3RhbXA6ICcyMDE4LTA0LTExJyxcbiAgfSxcbl1cblxuY29uc3QgbW9kZSA9IHJlZjxUaW1lbGluZVByb3BzWydtb2RlJ10+KCdzdGFydCcpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/timeline/mode.vue)_

vue

```
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

隐藏源代码

## ⾃定义节点样式 [​](#自定义节点样式)

可根据实际场景⾃定义节点尺⼨、颜⾊，或直接使⽤图标。

-   Custom icon

    2018-04-12 20:46

-   Custom color

    2018-04-03 20:46

-   Custom size

    2018-04-03 20:46

-   Custom hollow

    2018-04-03 20:46

-   Default node

    2018-04-03 20:46

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGltZWxpbmU+XG4gICAgPGVsLXRpbWVsaW5lLWl0ZW1cbiAgICAgIHYtZm9yPVwiKGFjdGl2aXR5LCBpbmRleCkgaW4gYWN0aXZpdGllc1wiXG4gICAgICA6a2V5PVwiaW5kZXhcIlxuICAgICAgOmljb249XCJhY3Rpdml0eS5pY29uXCJcbiAgICAgIDp0eXBlPVwiYWN0aXZpdHkudHlwZVwiXG4gICAgICA6Y29sb3I9XCJhY3Rpdml0eS5jb2xvclwiXG4gICAgICA6c2l6ZT1cImFjdGl2aXR5LnNpemVcIlxuICAgICAgOmhvbGxvdz1cImFjdGl2aXR5LmhvbGxvd1wiXG4gICAgICA6dGltZXN0YW1wPVwiYWN0aXZpdHkudGltZXN0YW1wXCJcbiAgICA+XG4gICAgICB7eyBhY3Rpdml0eS5jb250ZW50IH19XG4gICAgPC9lbC10aW1lbGluZS1pdGVtPlxuICA8L2VsLXRpbWVsaW5lPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IE1vcmVGaWxsZWQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuaW1wb3J0IHR5cGUgeyBUaW1lbGluZUl0ZW1Qcm9wcyB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW50ZXJmYWNlIEFjdGl2aXR5VHlwZSBleHRlbmRzIFBhcnRpYWw8VGltZWxpbmVJdGVtUHJvcHM+IHtcbiAgY29udGVudDogc3RyaW5nXG59XG5cbmNvbnN0IGFjdGl2aXRpZXM6IEFjdGl2aXR5VHlwZVtdID0gW1xuICB7XG4gICAgY29udGVudDogJ0N1c3RvbSBpY29uJyxcbiAgICB0aW1lc3RhbXA6ICcyMDE4LTA0LTEyIDIwOjQ2JyxcbiAgICBzaXplOiAnbGFyZ2UnLFxuICAgIHR5cGU6ICdwcmltYXJ5JyxcbiAgICBpY29uOiBNb3JlRmlsbGVkLFxuICB9LFxuICB7XG4gICAgY29udGVudDogJ0N1c3RvbSBjb2xvcicsXG4gICAgdGltZXN0YW1wOiAnMjAxOC0wNC0wMyAyMDo0NicsXG4gICAgY29sb3I6ICcjMGJiZDg3JyxcbiAgfSxcbiAge1xuICAgIGNvbnRlbnQ6ICdDdXN0b20gc2l6ZScsXG4gICAgdGltZXN0YW1wOiAnMjAxOC0wNC0wMyAyMDo0NicsXG4gICAgc2l6ZTogJ2xhcmdlJyxcbiAgfSxcbiAge1xuICAgIGNvbnRlbnQ6ICdDdXN0b20gaG9sbG93JyxcbiAgICB0aW1lc3RhbXA6ICcyMDE4LTA0LTAzIDIwOjQ2JyxcbiAgICB0eXBlOiAncHJpbWFyeScsXG4gICAgaG9sbG93OiB0cnVlLFxuICB9LFxuICB7XG4gICAgY29udGVudDogJ0RlZmF1bHQgbm9kZScsXG4gICAgdGltZXN0YW1wOiAnMjAxOC0wNC0wMyAyMDo0NicsXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/timeline/custom-node.vue)_

vue

```
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

隐藏源代码

## ⾃定义时间戳 [​](#自定义时间戳)

当内容在垂直⽅向上过⾼时，可将时间戳置于内容之上。

-   2018/4/12

    #### Update Github template

    Tom committed 2018/4/12 20:46

-   2018/4/3

    #### Update Github template

    Tom committed 2018/4/3 20:46

-   2018/4/2

    #### Update Github template

    Tom committed 2018/4/2 20:46

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGltZWxpbmU+XG4gICAgPGVsLXRpbWVsaW5lLWl0ZW0gdGltZXN0YW1wPVwiMjAxOC80LzEyXCIgcGxhY2VtZW50PVwidG9wXCI+XG4gICAgICA8ZWwtY2FyZD5cbiAgICAgICAgPGg0PlVwZGF0ZSBHaXRodWIgdGVtcGxhdGU8L2g0PlxuICAgICAgICA8cD5Ub20gY29tbWl0dGVkIDIwMTgvNC8xMiAyMDo0NjwvcD5cbiAgICAgIDwvZWwtY2FyZD5cbiAgICA8L2VsLXRpbWVsaW5lLWl0ZW0+XG4gICAgPGVsLXRpbWVsaW5lLWl0ZW0gdGltZXN0YW1wPVwiMjAxOC80LzNcIiBwbGFjZW1lbnQ9XCJ0b3BcIj5cbiAgICAgIDxlbC1jYXJkPlxuICAgICAgICA8aDQ+VXBkYXRlIEdpdGh1YiB0ZW1wbGF0ZTwvaDQ+XG4gICAgICAgIDxwPlRvbSBjb21taXR0ZWQgMjAxOC80LzMgMjA6NDY8L3A+XG4gICAgICA8L2VsLWNhcmQ+XG4gICAgPC9lbC10aW1lbGluZS1pdGVtPlxuICAgIDxlbC10aW1lbGluZS1pdGVtIHRpbWVzdGFtcD1cIjIwMTgvNC8yXCIgcGxhY2VtZW50PVwidG9wXCI+XG4gICAgICA8ZWwtY2FyZD5cbiAgICAgICAgPGg0PlVwZGF0ZSBHaXRodWIgdGVtcGxhdGU8L2g0PlxuICAgICAgICA8cD5Ub20gY29tbWl0dGVkIDIwMTgvNC8yIDIwOjQ2PC9wPlxuICAgICAgPC9lbC1jYXJkPlxuICAgIDwvZWwtdGltZWxpbmUtaXRlbT5cbiAgPC9lbC10aW1lbGluZT5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/timeline/custom-timestamp.vue)_

vue

```
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

隐藏源代码

## 垂直居中 [​](#垂直居中)

垂直居中样式的 Timeline-Item

-   2018/4/12

    #### Update Github template

    Tom committed 2018/4/12 20:46

-   2018/4/3

    #### Update Github template

    Tom committed 2018/4/3 20:46

-   2018/4/2

    Event start

-   2018/4/2

    Event end

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGltZWxpbmU+XG4gICAgPGVsLXRpbWVsaW5lLWl0ZW0gY2VudGVyIHRpbWVzdGFtcD1cIjIwMTgvNC8xMlwiIHBsYWNlbWVudD1cInRvcFwiPlxuICAgICAgPGVsLWNhcmQ+XG4gICAgICAgIDxoND5VcGRhdGUgR2l0aHViIHRlbXBsYXRlPC9oND5cbiAgICAgICAgPHA+VG9tIGNvbW1pdHRlZCAyMDE4LzQvMTIgMjA6NDY8L3A+XG4gICAgICA8L2VsLWNhcmQ+XG4gICAgPC9lbC10aW1lbGluZS1pdGVtPlxuICAgIDxlbC10aW1lbGluZS1pdGVtIHRpbWVzdGFtcD1cIjIwMTgvNC8zXCIgcGxhY2VtZW50PVwidG9wXCI+XG4gICAgICA8ZWwtY2FyZD5cbiAgICAgICAgPGg0PlVwZGF0ZSBHaXRodWIgdGVtcGxhdGU8L2g0PlxuICAgICAgICA8cD5Ub20gY29tbWl0dGVkIDIwMTgvNC8zIDIwOjQ2PC9wPlxuICAgICAgPC9lbC1jYXJkPlxuICAgIDwvZWwtdGltZWxpbmUtaXRlbT5cbiAgICA8ZWwtdGltZWxpbmUtaXRlbSBjZW50ZXIgdGltZXN0YW1wPVwiMjAxOC80LzJcIiBwbGFjZW1lbnQ9XCJ0b3BcIj5cbiAgICAgIEV2ZW50IHN0YXJ0XG4gICAgPC9lbC10aW1lbGluZS1pdGVtPlxuICAgIDxlbC10aW1lbGluZS1pdGVtIHRpbWVzdGFtcD1cIjIwMTgvNC8yXCIgcGxhY2VtZW50PVwidG9wXCI+XG4gICAgICBFdmVudCBlbmRcbiAgICA8L2VsLXRpbWVsaW5lLWl0ZW0+XG4gIDwvZWwtdGltZWxpbmU+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/timeline/center.vue)_

vue

```
<template>
  <el-timeline>
    <el-timeline-item center timestamp="2018/4/12" placement="top">
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
    <el-timeline-item center timestamp="2018/4/2" placement="top">
      Event start
    </el-timeline-item>
    <el-timeline-item timestamp="2018/4/2" placement="top">
      Event end
    </el-timeline-item>
  </el-timeline>
</template>
```

隐藏源代码

## 反向 2.11.9 [​](#反向)

使用 reverse 属性来控制节点的顺序。

reverse

-   Success

    2018-04-11

-   Approved

    2018-04-13

-   Event start

    2018-04-15

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoIHYtbW9kZWw9XCJyZXZlcnNlXCIgYWN0aXZlLXRleHQ9XCJyZXZlcnNlXCIgLz5cblxuICA8ZWwtdGltZWxpbmUgY2xhc3M9XCJtdC0yXCIgOnJldmVyc2U9XCJyZXZlcnNlXCI+XG4gICAgPGVsLXRpbWVsaW5lLWl0ZW1cbiAgICAgIHYtZm9yPVwiKGFjdGl2aXR5LCBpbmRleCkgaW4gYWN0aXZpdGllc1wiXG4gICAgICA6a2V5PVwiaW5kZXhcIlxuICAgICAgOnRpbWVzdGFtcD1cImFjdGl2aXR5LnRpbWVzdGFtcFwiXG4gICAgPlxuICAgICAge3sgYWN0aXZpdHkuY29udGVudCB9fVxuICAgIDwvZWwtdGltZWxpbmUtaXRlbT5cbiAgPC9lbC10aW1lbGluZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHJldmVyc2UgPSByZWYodHJ1ZSlcbmNvbnN0IGFjdGl2aXRpZXMgPSBbXG4gIHtcbiAgICBjb250ZW50OiAnRXZlbnQgc3RhcnQnLFxuICAgIHRpbWVzdGFtcDogJzIwMTgtMDQtMTUnLFxuICB9LFxuICB7XG4gICAgY29udGVudDogJ0FwcHJvdmVkJyxcbiAgICB0aW1lc3RhbXA6ICcyMDE4LTA0LTEzJyxcbiAgfSxcbiAge1xuICAgIGNvbnRlbnQ6ICdTdWNjZXNzJyxcbiAgICB0aW1lc3RhbXA6ICcyMDE4LTA0LTExJyxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/timeline/reverse.vue)_

vue

```
<template>
  <el-switch v-model="reverse" active-text="reverse" />

  <el-timeline class="mt-2" :reverse="reverse">
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

const reverse = ref(true)
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

隐藏源代码

## Timeline API [​](#timeline-api)

### Timeline Attributes [​](#timeline-attributes)

| 插槽名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| reverse 2.11.9 | 是否逆序排序 | `boolean` | false |
| mode 2.13.1 | 时间线与内容的相对位置 | `enum` | start |

### Timeline Slots [​](#timeline-slots)

| 属性名 | 说明 | 子标签 |
| --- | --- | --- |
| default | timeline 组件的自定义默认内容 | Timeline-Item |

## Timeline-Item API [​](#timeline-item-api)

### Timeline-Item Attributes [​](#timeline-item-attributes)

| 插槽名 | 说明 | Type | Default |
| --- | --- | --- | --- |
| timestamp | 时间戳 | `string` | '' |
| hide-timestamp | 是否隐藏时间戳 | `boolean` | false |
| center | 是否垂直居中 | `boolean` | false |
| placement | 时间戳位置 | `enum` | bottom |
| type | 节点类型 | `enum` | '' |
| color | 节点颜色 | `string` | '' |
| size | 节点尺寸 | `enum` | normal |
| icon | 自定义图标 | `string` / `Component` | — |
| hollow | 是否空心点 | `boolean` | false |

### Timeline-Item Slots [​](#timeline-item-slots)

| 方法名 | 详情 |
| --- | --- |
| default | 自定义 timeline 项的默认内容 |
| dot | 为时间线项目自定义已定义的节点 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/timeline) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/timeline.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/timeline.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/5559812?v=4&size=64)](https://github.com/metanas)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)

[Tag 标签](https://element-plus.org/zh-CN/component/tag)

[Tour 漫游式引导](https://element-plus.org/zh-CN/component/tour)


