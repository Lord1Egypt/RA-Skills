## Button 按钮 ​

**URL:** https://element-plus.org/zh-CN/component/button

**Contents:**
- Button 按钮 ​
- 基础用法 ​
- 禁用状态 ​
- 链接按钮 ​
- 文字按钮 ​
- 图标按钮 ​
- 按钮组 ​
- 加载状态按钮 ​
- 调整尺寸 ​
- Tag 2.3.4 ​

使用 type, plain, round, dashed 和 circle 来定义按钮的样式。

你可以使用 disabled 属性来定义按钮是否被禁用。

使用 disabled 属性来控制按钮是否为禁用状态。 该属性接受一个 Boolean 类型的值。

type="text" 已被 废弃，将于版本 3.0.0 时 移除，请考虑切换至新的 API。

新的 API link 于 2.2.1 版本时添加，你可以使用 type API 设置链接按钮的主题样式

文字按钮在现在有了全新的设计样式。 2.2.0 如果您想要使用老版样式的按钮，可以考虑使用 Link 组件。

API也已更新，由于 type 属性会同时控制按钮的样式， 因此我们通过一个新的 API text: boolean 来控制文字按钮。

Background color always on

使用图标为按钮添加更多的含义。 你也可以单独使用图标不添加文字来节省显示区域占用。

使用 icon 属性来为按钮添加图标。 您可以在我们的 Icon 组件中找到所需图标。 通过向右方添加<i>标签来添加图标， 你也可以使用自定义图标。

在 2.11.9 中，您可以使用 direction 属性。

使用 <el-button-group> 对多个按钮分组。

点击按钮来加载数据，并向用户反馈加载状态。

通过设置 loading 属性为 true 来显示加载中状态。

您可以使用 loading 插槽或 loadingIcon属性自定义您的loading图标

ps: loading 插槽优先级高于loadingIcon属性

除了默认的大小，按钮组件还提供了几种额外的尺寸可供选择，以便适配不同的场景。

使用 size 属性额外配置尺寸，可使用 large和small两种值。

您可以自定义元素标签。例如，按钮，div，路由链接，nuxt链接。

我们将自动计算按钮处于 hover 和 active 状态时的颜色。

自 2.13.7 起，color 属性也适用于 link 和 text 按钮。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="button-example">
    <div class="button-row">
      <el-button>Default</el-button>
      <el-button type="primary">Primary</el-button>
      <el-button type="success">Success</el-button>
      <el-button type="info">Info</el-button>
      <el-button type="warning">Warning</el-button>
      <el-button type="danger">Danger</el-button>
    </div>

    <div class="button-row">
      <el-button plain>Plain</el-button>
      <el-button type="primary" plain>Primary</el-button>
      <el-button type="success" plain>Success</el-button>
      <el-button type="info" plain>Info</el-button>
      <el-button type="warning" plain>Warning</el-button>
      <el-button type="danger" plain>Danger</el-button>
    </div>

    <div class="button-row">
      <el-button round>Round</el-button>
      <el-button type="primary" round>Primary</el-button>
      <el-button type="success" round>Success</el-button>
      <el-button type="info" round>Info</el-button>
      <el-button type="warning" round>Warning</el-button>
      <el-button type="danger" round>Danger</el-button>
    </div>

    <div class="button-row">
      <el-button dashed>Dashed</el-button>
      <el-button type="primary" dashed>Primary</el-button>
      <el-button type="success" dashed>Success</el-button>
      <el-button type="info" dashed>Info</el-button>
      <el-button type="warning" dashed>Warning</el-button>
      <el-button type="danger" dashed>Danger</el-button>
    </div>

    <div class="button-row">
      <el-button :icon="Search" circle />
      <el-button type="primary" :icon="Edit" circle />
      <el-button type="success" :icon="Check" circle />
      <el-button type="info" :icon="Message" circle />
      <el-button type="warning" :icon="Star" circle />
      <el-button type="danger" :icon="Delete" circle />
    </div>
  </div>
</template>

<script lang="ts" setup>
import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'
</script>

<style scoped>
.button-example {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.button-row > * {
  margin: 0;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div class="button-example">
    <div class="button-row">
      <el-button disabled>Default</el-button>
      <el-button type="primary" disabled>Primary</el-button>
      <el-button type="success" disabled>Success</el-button>
      <el-button type="info" disabled>Info</el-button>
      <el-button type="warning" disabled>Warning</el-button>
      <el-button type="danger" disabled>Danger</el-button>
    </div>

    <div class="button-row">
      <el-button plain disabled>Plain</el-button>
      <el-button type="primary" plain disabled>Primary</el-button>
      <el-button type="success" plain disabled>Success</el-button>
      <el-button type="info" plain disabled>Info</el-button>
      <el-button type="warning" plain disabled>Warning</el-button>
      <el-button type="danger" plain disabled>Danger</el-button>
    </div>
  </div>
</template>

<style scoped>
.button-example {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.button-row > * {
  margin: 0;
}
</style>
```

Example 3 (typescript):
```typescript
<template>
  <p>Basic link button</p>
  <div class="mb-4">
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      link
    >
      {{ button.text }}
    </el-button>
  </div>

  <p>Disabled link button</p>
  <div>
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      link
      disabled
    >
      {{ button.text }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
const buttons = [
  { type: '', text: 'plain' },
  { type: 'primary', text: 'primary' },
  { type: 'success', text: 'success' },
  { type: 'info', text: 'info' },
  { type: 'warning', text: 'warning' },
  { type: 'danger', text: 'danger' },
] as const
</script>
```

Example 4 (typescript):
```typescript
<template>
  <p>Basic text button</p>
  <div class="mb-4">
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      text
    >
      {{ button.text }}
    </el-button>
  </div>

  <p>Background color always on</p>
  <div class="mb-4">
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      text
      bg
    >
      {{ button.text }}
    </el-button>
  </div>

  <p>Disabled text button</p>
  <div>
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      text
      disabled
    >
      {{ button.text }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
const buttons = [
  { type: '', text: 'plain' },
  { type: 'primary', text: 'primary' },
  { type: 'success', text: 'success' },
  { type: 'info', text: 'info' },
  { type: 'warning', text: 'warning' },
  { type: 'danger', text: 'danger' },
] as const
</script>
```

---
