## Mention 提及 ​

**URL:** https://element-plus.org/zh-CN/component/mention

**Contents:**
- Mention 提及 ​
- 基础用法 ​
- Props 2.11.3 ​
- Textarea ​
- 自定义标签 ​
- 加载远程选项 ​
- 自定义触发字段 ​
- 整体删除 ​
- 在表单里使用 ​
- API ​

你可以通过 props 属性自定义 options 的别名。

通过 prefix 属性 自定义触发字段。 默认为 @, Array<string> 。

将whole属性设置为 true，当您按下退格键时，此处的 mention 区域将作为一个整体被删除。 设置 "check-is-whole" 属性来自定义检查逻辑。

由于这个组件是基于el-input派生的，他们的原始属性未被更改，故不在此重复。请跳转查看原组件的相应文档。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-mention
    v-model="value"
    :options="options"
    style="width: 320px"
    placeholder="Please input"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value = ref('@')

const options = ref([
  {
    label: 'Fuphoenixes',
    value: 'Fuphoenixes',
  },
  {
    label: 'kooriookami',
    value: 'kooriookami',
  },
  {
    label: 'Jeremy',
    value: 'Jeremy',
  },
  {
    label: 'btea',
    value: 'btea',
  },
])
</script>
```

Example 2 (vue):
```vue
<template>
  <el-mention
    v-model="value"
    :options="options"
    :props="props"
    style="width: 320px"
    placeholder="Please input"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value = ref('@')
const props = { label: 'name', value: 'id', disabled: 'unable' }
const options = ref([
  {
    name: 'Fuphoenixes',
    id: 'Fuphoenixes',
    unable: true,
  },
  {
    name: 'kooriookami',
    id: 'kooriookami',
  },
  {
    name: 'Jeremy',
    id: 'Jeremy',
    unable: true,
  },
  {
    name: 'btea',
    id: 'btea',
  },
])
</script>
```

Example 3 (vue):
```vue
<template>
  <el-mention
    v-model="value"
    type="textarea"
    :options="options"
    style="width: 320px"
    placeholder="Please input"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value = ref('')

const options = ref([
  {
    label: 'Fuphoenixes',
    value: 'Fuphoenixes',
  },
  {
    label: 'kooriookami',
    value: 'kooriookami',
  },
  {
    label: 'Jeremy',
    value: 'Jeremy',
  },
  {
    label: 'btea',
    value: 'btea',
  },
])
</script>
```

Example 4 (vue):
```vue
<template>
  <el-mention
    v-model="value"
    :options="options"
    style="width: 320px"
    placeholder="Please input"
  >
    <template #label="{ item }">
      <div style="display: flex; align-items: center">
        <el-avatar :size="24" :src="item.avatar" />
        <span style="margin-left: 6px">{{ item.value }}</span>
      </div>
    </template>
  </el-mention>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value = ref('')

const options = ref([
  {
    value: 'Fuphoenixes',
    avatar: 'https://avatars.githubusercontent.com/u/27912232',
  },
  {
    value: 'kooriookami',
    avatar: 'https://avatars.githubusercontent.com/u/38392315',
  },
  {
    value: 'Jeremy',
    avatar: 'https://avatars.githubusercontent.com/u/15975785',
  },
  {
    value: 'btea',
    avatar: 'https://avatars.githubusercontent.com/u/24516654',
  },
])
</script>
```

---
