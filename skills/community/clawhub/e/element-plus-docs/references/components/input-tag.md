## InputTag 标签输入框 ​

**URL:** https://element-plus.org/zh-CN/component/input-tag

**Contents:**
- InputTag 标签输入框 ​
- 基础用法 ​
- 自定义触发器 ​
- 最大标签数 ​
- 折叠标签2.11.0 ​
- 禁用状态 ​
- 可清空 ​
- 自定义清除图标2.11.0 ​
- 可拖放 ​
- 分隔符2.9.9 ​

InputTag 组件允许用户添加内容作为标签

您可以自定义用于触发输入标签的键位， 默认是Enter 回车键

使用折叠标签属性将它们合并成一块文本。 您可以使用折叠标签工具提示属性来启用悬停在折叠文本上的行为来显示特定的选定值。 使用折叠标签工具提示属性会使最大属性无效。

use collapse-tags-tooltip

use max-collapse-tags

你可以通过clear-icon属性自定义清除图标

使用 size 属性改变输入框大小。 除了默认大小外，还有另外两个选项： large, small。

您可以通过prefix和 suffix 插槽自定义 InputTag 的前缀和后缀。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-input-tag
    v-model="input"
    placeholder="Please input"
    aria-label="Please click the Enter key after input"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref<string[]>()
</script>
```

Example 2 (jsx):
```jsx
<template>
  <div>
    <el-segmented v-model="trigger" :options="options" />
  </div>
  <br />
  <el-input-tag v-model="input" :trigger="trigger" placeholder="Please input" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { EVENT_CODE } from 'element-plus'

const trigger = ref<'Enter' | 'Space'>('Space')
const input = ref<string[]>()
const options = [EVENT_CODE.enter, EVENT_CODE.space]
</script>
```

Example 3 (vue):
```vue
<template>
  <el-input-tag v-model="input" :max="3" placeholder="enter up to 3 tags" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref<string[]>()
</script>
```

Example 4 (vue):
```vue
<template>
  <div class="m-4">
    <p>use collapse-tags</p>
    <el-input-tag
      v-model="input1"
      collapse-tags
      placeholder="Please input"
      aria-label="Please click the Enter key after input"
    />
    <p>use collapse-tags-tooltip</p>
    <el-input-tag
      v-model="input2"
      collapse-tags
      collapse-tags-tooltip
      placeholder="Please input"
      aria-label="Please click the Enter key after input"
    />
    <p>use max-collapse-tags</p>
    <el-input-tag
      v-model="input3"
      collapse-tags
      collapse-tags-tooltip
      :max-collapse-tags="3"
      placeholder="Please input"
      aria-label="Please click the Enter key after input"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input1 = ref<string[]>()
const input2 = ref<string[]>()
const input3 = ref<string[]>()
</script>
```

---
