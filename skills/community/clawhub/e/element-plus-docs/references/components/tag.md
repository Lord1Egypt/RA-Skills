## Tag 标签 ​

**URL:** https://element-plus.org/zh-CN/component/tag

**Contents:**
- Tag 标签 ​
- 基础用法 ​
- 可移除标签 ​
- 动态编辑标签 ​
- 不同尺寸 ​
- 主题 ​
- 圆形标签 ​
- 可选中的标签 ​
- Tag API ​
  - Tag Attributes ​

由 type 属性来选择 tag 的类型。 也可以通过 color 属性来自定义背景色。

设置 closable 属性可以定义一个标签是否可移除。 它接受一个 Boolean。 默认的标签移除时会附带渐变动画。 如果不想使用，可以设置 disable-transitions 属性，它接受一个 Boolean，true 为关闭。 当 Tag 被移除时会触发 close 事件。

动态编辑标签可以通过点击标签关闭按钮后触发的 close 事件来实现。

Tag 组件提供除了默认值以外的三种尺寸，可以在不同场景下选择合适的按钮尺寸。

使用 size 属性来设置额外尺寸, 可选值包括 large, default 或 small.

Tag 组件提供了三个不同的主题：dark、light 和 plain。

通过设置 effect 属性来改变主题，默认为 light。

有时候因为业务需求，我们可能会需要用到类似复选框的标签，但是按钮式的复选框的样式又不满足需求，此时我们就可以用到 check-tag组件。 您可以在2.5.4中使用 type 属性。

check-tag 的基础使用方法，check-tag 提供的 API 非常简单。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="flex gap-2">
    <el-tag type="primary">Tag 1</el-tag>
    <el-tag type="success">Tag 2</el-tag>
    <el-tag type="info">Tag 3</el-tag>
    <el-tag type="warning">Tag 4</el-tag>
    <el-tag type="danger">Tag 5</el-tag>
  </div>
</template>
```

Example 2 (typescript):
```typescript
<template>
  <div class="flex gap-2">
    <el-tag v-for="tag in tags" :key="tag.name" closable :type="tag.type">
      {{ tag.name }}
    </el-tag>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TagProps } from 'element-plus'

interface TagsItem {
  name: string
  type: TagProps['type']
}

const tags = ref<TagsItem[]>([
  { name: 'Tag 1', type: 'primary' },
  { name: 'Tag 2', type: 'success' },
  { name: 'Tag 3', type: 'info' },
  { name: 'Tag 4', type: 'warning' },
  { name: 'Tag 5', type: 'danger' },
])
</script>
```

Example 3 (vue):
```vue
<template>
  <div class="flex gap-2">
    <el-tag
      v-for="tag in dynamicTags"
      :key="tag"
      closable
      :disable-transitions="false"
      @close="handleClose(tag)"
    >
      {{ tag }}
    </el-tag>
    <el-input
      v-if="inputVisible"
      ref="InputRef"
      v-model="inputValue"
      class="w-20"
      size="small"
      @keyup.enter="handleInputConfirm"
      @blur="handleInputConfirm"
    />
    <el-button v-else class="button-new-tag" size="small" @click="showInput">
      + New Tag
    </el-button>
  </div>
</template>

<script lang="ts" setup>
import { nextTick, ref } from 'vue'

import type { InputInstance } from 'element-plus'

const inputValue = ref('')
const dynamicTags = ref(['Tag 1', 'Tag 2', 'Tag 3'])
const inputVisible = ref(false)
const InputRef = ref<InputInstance>()

const handleClose = (tag: string) => {
  dynamicTags.value.splice(dynamicTags.value.indexOf(tag), 1)
}

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    InputRef.value!.input!.focus()
  })
}

const handleInputConfirm = () => {
  if (inputValue.value) {
    dynamicTags.value.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}
</script>
```

Example 4 (vue):
```vue
<template>
  <div class="flex gap-2">
    <el-tag size="large">Large</el-tag>
    <el-tag>Default</el-tag>
    <el-tag size="small">Small</el-tag>
  </div>
</template>
```

---
