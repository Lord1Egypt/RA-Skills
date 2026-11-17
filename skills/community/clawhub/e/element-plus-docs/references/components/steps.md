## Steps 步骤条 ​

**URL:** https://element-plus.org/zh-CN/component/steps

**Contents:**
- Steps 步骤条 ​
- 基础用法 ​
- 含状态的步骤条 ​
- 居中的步骤条 ​
- 带描述的步骤栏 ​
- 带图标的步骤条 ​
- 垂直的步骤条 ​
- 简洁风格的步骤条 ​
- Steps API ​
  - Steps Attributes ​

引导用户按照流程完成任务的分步导航条， 可根据实际应用场景设定步骤，步骤不得少于 2 步。

设置 active 属性，接受一个 Number，表明步骤的 index，从 0 开始。 需要定宽的步骤条时，设置 space 属性即可，它接受 Number， 单位为 px， 如果不设置，则为自适应。 设置 finish-status 属性可以改变已经完成的步骤的状态。

也可以使用 title 具名插槽，可以用 slot 的方式来取代属性的设置， 在本文档最后的列表中有所有的插槽可供参考。

通过 icon 属性来设置图标， 图标的类型可以参考 Icon 组件的文档， 除此以外，还能通过具名 slot 来使用自定义的图标。

只需要在 el-steps 元素中设置 direction 属性为 vertical 即可。

设置 simple 可应用简洁风格，该条件下 align-center / description / direction / space 都将失效。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-steps style="max-width: 600px" :active="active" finish-status="success">
    <el-step title="Step 1" />
    <el-step title="Step 2" />
    <el-step title="Step 3" />
  </el-steps>

  <el-button style="margin-top: 12px" @click="next">Next step</el-button>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const active = ref(0)

const next = () => {
  if (active.value++ > 2) active.value = 0
}
</script>
```

Example 2 (typescript):
```typescript
<template>
  <el-steps
    style="max-width: 600px"
    :space="200"
    :active="1"
    finish-status="success"
  >
    <el-step title="Done" />
    <el-step title="Processing" />
    <el-step title="Step 3" />
  </el-steps>
</template>
```

Example 3 (typescript):
```typescript
<template>
  <el-steps style="max-width: 600px" :active="2" align-center>
    <el-step title="Step 1" description="Some description" />
    <el-step title="Step 2" description="Some description" />
    <el-step title="Step 3" description="Some description" />
  </el-steps>
</template>
```

Example 4 (typescript):
```typescript
<template>
  <el-steps style="max-width: 600px" :active="1">
    <el-step title="Step 1" description="Some description" />
    <el-step title="Step 2" description="Some description" />
    <el-step title="Step 3" description="Some description" />
  </el-steps>
</template>
```

---
