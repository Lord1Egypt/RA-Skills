---
name: "tag"
description: "Tag 标签 -- Element Plus Vue3 桌面端组件。Invoke when user needs Tag 标签 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/tag.html"
---

---

# Tag 标签 [​](#tag-标签)

更新日志待解决

7

用于标记和选择。

## 基础用法 [​](#基础用法)

由 `type` 属性来选择 tag 的类型。 也可以通过 `color` 属性来自定义背景色。

Tag 1Tag 2Tag 3Tag 4Tag 5

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtMlwiPlxuICAgIDxlbC10YWcgdHlwZT1cInByaW1hcnlcIj5UYWcgMTwvZWwtdGFnPlxuICAgIDxlbC10YWcgdHlwZT1cInN1Y2Nlc3NcIj5UYWcgMjwvZWwtdGFnPlxuICAgIDxlbC10YWcgdHlwZT1cImluZm9cIj5UYWcgMzwvZWwtdGFnPlxuICAgIDxlbC10YWcgdHlwZT1cIndhcm5pbmdcIj5UYWcgNDwvZWwtdGFnPlxuICAgIDxlbC10YWcgdHlwZT1cImRhbmdlclwiPlRhZyA1PC9lbC10YWc+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tag/basic.vue)_

vue

```
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

隐藏源代码

## 可移除标签 [​](#可移除标签)

设置 `closable` 属性可以定义一个标签是否可移除。 它接受一个 `Boolean`。 默认的标签移除时会附带渐变动画。 如果不想使用，可以设置 `disable-transitions` 属性，它接受一个 `Boolean`，`true` 为关闭。 当 Tag 被移除时会触发 `close` 事件。

Tag 1Tag 2Tag 3Tag 4Tag 5

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtMlwiPlxuICAgIDxlbC10YWcgdi1mb3I9XCJ0YWcgaW4gdGFnc1wiIDprZXk9XCJ0YWcubmFtZVwiIGNsb3NhYmxlIDp0eXBlPVwidGFnLnR5cGVcIj5cbiAgICAgIHt7IHRhZy5uYW1lIH19XG4gICAgPC9lbC10YWc+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBUYWdQcm9wcyB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW50ZXJmYWNlIFRhZ3NJdGVtIHtcbiAgbmFtZTogc3RyaW5nXG4gIHR5cGU6IFRhZ1Byb3BzWyd0eXBlJ11cbn1cblxuY29uc3QgdGFncyA9IHJlZjxUYWdzSXRlbVtdPihbXG4gIHsgbmFtZTogJ1RhZyAxJywgdHlwZTogJ3ByaW1hcnknIH0sXG4gIHsgbmFtZTogJ1RhZyAyJywgdHlwZTogJ3N1Y2Nlc3MnIH0sXG4gIHsgbmFtZTogJ1RhZyAzJywgdHlwZTogJ2luZm8nIH0sXG4gIHsgbmFtZTogJ1RhZyA0JywgdHlwZTogJ3dhcm5pbmcnIH0sXG4gIHsgbmFtZTogJ1RhZyA1JywgdHlwZTogJ2RhbmdlcicgfSxcbl0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tag/removable.vue)_

vue

```
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

隐藏源代码

## 动态编辑标签 [​](#动态编辑标签)

动态编辑标签可以通过点击标签关闭按钮后触发的 `close` 事件来实现。

Tag 1Tag 2Tag 3 + New Tag

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtMlwiPlxuICAgIDxlbC10YWdcbiAgICAgIHYtZm9yPVwidGFnIGluIGR5bmFtaWNUYWdzXCJcbiAgICAgIDprZXk9XCJ0YWdcIlxuICAgICAgY2xvc2FibGVcbiAgICAgIDpkaXNhYmxlLXRyYW5zaXRpb25zPVwiZmFsc2VcIlxuICAgICAgQGNsb3NlPVwiaGFuZGxlQ2xvc2UodGFnKVwiXG4gICAgPlxuICAgICAge3sgdGFnIH19XG4gICAgPC9lbC10YWc+XG4gICAgPGVsLWlucHV0XG4gICAgICB2LWlmPVwiaW5wdXRWaXNpYmxlXCJcbiAgICAgIHJlZj1cIklucHV0UmVmXCJcbiAgICAgIHYtbW9kZWw9XCJpbnB1dFZhbHVlXCJcbiAgICAgIGNsYXNzPVwidy0yMFwiXG4gICAgICBzaXplPVwic21hbGxcIlxuICAgICAgQGtleXVwLmVudGVyPVwiaGFuZGxlSW5wdXRDb25maXJtXCJcbiAgICAgIEBibHVyPVwiaGFuZGxlSW5wdXRDb25maXJtXCJcbiAgICAvPlxuICAgIDxlbC1idXR0b24gdi1lbHNlIGNsYXNzPVwiYnV0dG9uLW5ldy10YWdcIiBzaXplPVwic21hbGxcIiBAY2xpY2s9XCJzaG93SW5wdXRcIj5cbiAgICAgICsgTmV3IFRhZ1xuICAgIDwvZWwtYnV0dG9uPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBuZXh0VGljaywgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IElucHV0SW5zdGFuY2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGlucHV0VmFsdWUgPSByZWYoJycpXG5jb25zdCBkeW5hbWljVGFncyA9IHJlZihbJ1RhZyAxJywgJ1RhZyAyJywgJ1RhZyAzJ10pXG5jb25zdCBpbnB1dFZpc2libGUgPSByZWYoZmFsc2UpXG5jb25zdCBJbnB1dFJlZiA9IHJlZjxJbnB1dEluc3RhbmNlPigpXG5cbmNvbnN0IGhhbmRsZUNsb3NlID0gKHRhZzogc3RyaW5nKSA9PiB7XG4gIGR5bmFtaWNUYWdzLnZhbHVlLnNwbGljZShkeW5hbWljVGFncy52YWx1ZS5pbmRleE9mKHRhZyksIDEpXG59XG5cbmNvbnN0IHNob3dJbnB1dCA9ICgpID0+IHtcbiAgaW5wdXRWaXNpYmxlLnZhbHVlID0gdHJ1ZVxuICBuZXh0VGljaygoKSA9PiB7XG4gICAgSW5wdXRSZWYudmFsdWUhLmlucHV0IS5mb2N1cygpXG4gIH0pXG59XG5cbmNvbnN0IGhhbmRsZUlucHV0Q29uZmlybSA9ICgpID0+IHtcbiAgaWYgKGlucHV0VmFsdWUudmFsdWUpIHtcbiAgICBkeW5hbWljVGFncy52YWx1ZS5wdXNoKGlucHV0VmFsdWUudmFsdWUpXG4gIH1cbiAgaW5wdXRWaXNpYmxlLnZhbHVlID0gZmFsc2VcbiAgaW5wdXRWYWx1ZS52YWx1ZSA9ICcnXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tag/editable.vue)_

vue

```
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

隐藏源代码

## 不同尺寸 [​](#不同尺寸)

Tag 组件提供除了默认值以外的三种尺寸，可以在不同场景下选择合适的按钮尺寸。

使用 `size` 属性来设置额外尺寸, 可选值包括 `large`, `default` 或 `small`.

LargeDefaultSmall

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtMlwiPlxuICAgIDxlbC10YWcgc2l6ZT1cImxhcmdlXCI+TGFyZ2U8L2VsLXRhZz5cbiAgICA8ZWwtdGFnPkRlZmF1bHQ8L2VsLXRhZz5cbiAgICA8ZWwtdGFnIHNpemU9XCJzbWFsbFwiPlNtYWxsPC9lbC10YWc+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tag/sizes.vue)_

vue

```
<template>
  <div class="flex gap-2">
    <el-tag size="large">Large</el-tag>
    <el-tag>Default</el-tag>
    <el-tag size="small">Small</el-tag>
  </div>
</template>
```

隐藏源代码

## 主题 [​](#主题)

Tag 组件提供了三个不同的主题：`dark`、`light` 和 `plain`。

通过设置 `effect` 属性来改变主题，默认为 `light`。

DarkTag 1Tag 2Tag 3Tag 4Tag 5

LightTag 1Tag 2Tag 3Tag 4Tag 5

PlainTag 1Tag 2Tag 3Tag 4Tag 5

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtMlwiPlxuICAgIDxzcGFuPkRhcms8L3NwYW4+XG4gICAgPGVsLXRhZ1xuICAgICAgdi1mb3I9XCJpdGVtIGluIGl0ZW1zXCJcbiAgICAgIDprZXk9XCJpdGVtLmxhYmVsXCJcbiAgICAgIDp0eXBlPVwiaXRlbS50eXBlXCJcbiAgICAgIGVmZmVjdD1cImRhcmtcIlxuICAgID5cbiAgICAgIHt7IGl0ZW0ubGFiZWwgfX1cbiAgICA8L2VsLXRhZz5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJmbGV4IGdhcC0yIG10LTRcIj5cbiAgICA8c3Bhbj5MaWdodDwvc3Bhbj5cbiAgICA8ZWwtdGFnXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gaXRlbXNcIlxuICAgICAgOmtleT1cIml0ZW0ubGFiZWxcIlxuICAgICAgOnR5cGU9XCJpdGVtLnR5cGVcIlxuICAgICAgZWZmZWN0PVwibGlnaHRcIlxuICAgID5cbiAgICAgIHt7IGl0ZW0ubGFiZWwgfX1cbiAgICA8L2VsLXRhZz5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJmbGV4IGdhcC0yIG10LTRcIj5cbiAgICA8c3Bhbj5QbGFpbjwvc3Bhbj5cbiAgICA8ZWwtdGFnXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gaXRlbXNcIlxuICAgICAgOmtleT1cIml0ZW0ubGFiZWxcIlxuICAgICAgOnR5cGU9XCJpdGVtLnR5cGVcIlxuICAgICAgZWZmZWN0PVwicGxhaW5cIlxuICAgID5cbiAgICAgIHt7IGl0ZW0ubGFiZWwgfX1cbiAgICA8L2VsLXRhZz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFRhZ1Byb3BzIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG50eXBlIEl0ZW0gPSB7IHR5cGU6IFRhZ1Byb3BzWyd0eXBlJ107IGxhYmVsOiBzdHJpbmcgfVxuXG5jb25zdCBpdGVtcyA9IHJlZjxBcnJheTxJdGVtPj4oW1xuICB7IHR5cGU6ICdwcmltYXJ5JywgbGFiZWw6ICdUYWcgMScgfSxcbiAgeyB0eXBlOiAnc3VjY2VzcycsIGxhYmVsOiAnVGFnIDInIH0sXG4gIHsgdHlwZTogJ2luZm8nLCBsYWJlbDogJ1RhZyAzJyB9LFxuICB7IHR5cGU6ICd3YXJuaW5nJywgbGFiZWw6ICdUYWcgNCcgfSxcbiAgeyB0eXBlOiAnZGFuZ2VyJywgbGFiZWw6ICdUYWcgNScgfSxcbl0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tag/theme.vue)_

vue

```
<template>
  <div class="flex gap-2">
    <span>Dark</span>
    <el-tag
      v-for="item in items"
      :key="item.label"
      :type="item.type"
      effect="dark"
    >
      {{ item.label }}
    </el-tag>
  </div>
  <div class="flex gap-2 mt-4">
    <span>Light</span>
    <el-tag
      v-for="item in items"
      :key="item.label"
      :type="item.type"
      effect="light"
    >
      {{ item.label }}
    </el-tag>
  </div>
  <div class="flex gap-2 mt-4">
    <span>Plain</span>
    <el-tag
      v-for="item in items"
      :key="item.label"
      :type="item.type"
      effect="plain"
    >
      {{ item.label }}
    </el-tag>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TagProps } from 'element-plus'

type Item = { type: TagProps['type']; label: string }

const items = ref<Array<Item>>([
  { type: 'primary', label: 'Tag 1' },
  { type: 'success', label: 'Tag 2' },
  { type: 'info', label: 'Tag 3' },
  { type: 'warning', label: 'Tag 4' },
  { type: 'danger', label: 'Tag 5' },
])
</script>
```

隐藏源代码

## 圆形标签 [​](#圆形标签)

Tag 可以向按钮组件一样变为完全圆形。

Tag 1Tag 2Tag 3Tag 4Tag 5

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtMlwiPlxuICAgIDxlbC10YWdcbiAgICAgIHYtZm9yPVwiaXRlbSBpbiBpdGVtc1wiXG4gICAgICA6a2V5PVwiaXRlbS5sYWJlbFwiXG4gICAgICA6dHlwZT1cIml0ZW0udHlwZVwiXG4gICAgICBlZmZlY3Q9XCJkYXJrXCJcbiAgICAgIHJvdW5kXG4gICAgPlxuICAgICAge3sgaXRlbS5sYWJlbCB9fVxuICAgIDwvZWwtdGFnPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cImZsZXggZ2FwLTIgbXQtNFwiPlxuICAgIDxlbC10YWdcbiAgICAgIHYtZm9yPVwiaXRlbSBpbiBpdGVtc1wiXG4gICAgICA6a2V5PVwiaXRlbS5sYWJlbFwiXG4gICAgICA6dHlwZT1cIml0ZW0udHlwZVwiXG4gICAgICBlZmZlY3Q9XCJsaWdodFwiXG4gICAgICByb3VuZFxuICAgID5cbiAgICAgIHt7IGl0ZW0ubGFiZWwgfX1cbiAgICA8L2VsLXRhZz5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJmbGV4IGdhcC0yIG10LTRcIj5cbiAgICA8ZWwtdGFnXG4gICAgICB2LWZvcj1cIml0ZW0gaW4gaXRlbXNcIlxuICAgICAgOmtleT1cIml0ZW0ubGFiZWxcIlxuICAgICAgOnR5cGU9XCJpdGVtLnR5cGVcIlxuICAgICAgZWZmZWN0PVwicGxhaW5cIlxuICAgICAgcm91bmRcbiAgICA+XG4gICAgICB7eyBpdGVtLmxhYmVsIH19XG4gICAgPC9lbC10YWc+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBUYWdQcm9wcyB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxudHlwZSBJdGVtID0geyB0eXBlOiBUYWdQcm9wc1sndHlwZSddOyBsYWJlbDogc3RyaW5nIH1cblxuY29uc3QgaXRlbXMgPSByZWY8QXJyYXk8SXRlbT4+KFtcbiAgeyB0eXBlOiAncHJpbWFyeScsIGxhYmVsOiAnVGFnIDEnIH0sXG4gIHsgdHlwZTogJ3N1Y2Nlc3MnLCBsYWJlbDogJ1RhZyAyJyB9LFxuICB7IHR5cGU6ICdpbmZvJywgbGFiZWw6ICdUYWcgMycgfSxcbiAgeyB0eXBlOiAnd2FybmluZycsIGxhYmVsOiAnVGFnIDQnIH0sXG4gIHsgdHlwZTogJ2RhbmdlcicsIGxhYmVsOiAnVGFnIDUnIH0sXG5dKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tag/rounded.vue)_

vue

```
<template>
  <div class="flex gap-2">
    <el-tag
      v-for="item in items"
      :key="item.label"
      :type="item.type"
      effect="dark"
      round
    >
      {{ item.label }}
    </el-tag>
  </div>
  <div class="flex gap-2 mt-4">
    <el-tag
      v-for="item in items"
      :key="item.label"
      :type="item.type"
      effect="light"
      round
    >
      {{ item.label }}
    </el-tag>
  </div>
  <div class="flex gap-2 mt-4">
    <el-tag
      v-for="item in items"
      :key="item.label"
      :type="item.type"
      effect="plain"
      round
    >
      {{ item.label }}
    </el-tag>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { TagProps } from 'element-plus'

type Item = { type: TagProps['type']; label: string }

const items = ref<Array<Item>>([
  { type: 'primary', label: 'Tag 1' },
  { type: 'success', label: 'Tag 2' },
  { type: 'info', label: 'Tag 3' },
  { type: 'warning', label: 'Tag 4' },
  { type: 'danger', label: 'Tag 5' },
])
</script>
```

隐藏源代码

## 可选中的标签 [​](#可选中的标签)

有时候因为业务需求，我们可能会需要用到类似复选框的标签，但是**按钮式的复选框**的样式又不满足需求，此时我们就可以用到 `check-tag`组件。 您可以在2.5.4中使用 `type` 属性。

check-tag 的基础使用方法，check-tag 提供的 API 非常简单。

CheckedToggle meDisabled

Tag 1 Tag 2 Tag 3 Tag 4 Tag 5 Tag 6

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtMlwiPlxuICAgIDxlbC1jaGVjay10YWcgY2hlY2tlZD5DaGVja2VkPC9lbC1jaGVjay10YWc+XG4gICAgPGVsLWNoZWNrLXRhZyA6Y2hlY2tlZD1cImNoZWNrZWRcIiBAY2hhbmdlPVwib25DaGFuZ2VcIj5Ub2dnbGUgbWU8L2VsLWNoZWNrLXRhZz5cbiAgICA8ZWwtY2hlY2stdGFnIGRpc2FibGVkPkRpc2FibGVkPC9lbC1jaGVjay10YWc+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtMiBtdC00XCI+XG4gICAgPGVsLWNoZWNrLXRhZyA6Y2hlY2tlZD1cImNoZWNrZWQxXCIgdHlwZT1cInByaW1hcnlcIiBAY2hhbmdlPVwib25DaGFuZ2UxXCI+XG4gICAgICBUYWcgMVxuICAgIDwvZWwtY2hlY2stdGFnPlxuICAgIDxlbC1jaGVjay10YWcgOmNoZWNrZWQ9XCJjaGVja2VkMlwiIHR5cGU9XCJzdWNjZXNzXCIgQGNoYW5nZT1cIm9uQ2hhbmdlMlwiPlxuICAgICAgVGFnIDJcbiAgICA8L2VsLWNoZWNrLXRhZz5cbiAgICA8ZWwtY2hlY2stdGFnIDpjaGVja2VkPVwiY2hlY2tlZDNcIiB0eXBlPVwiaW5mb1wiIEBjaGFuZ2U9XCJvbkNoYW5nZTNcIj5cbiAgICAgIFRhZyAzXG4gICAgPC9lbC1jaGVjay10YWc+XG4gICAgPGVsLWNoZWNrLXRhZyA6Y2hlY2tlZD1cImNoZWNrZWQ0XCIgdHlwZT1cIndhcm5pbmdcIiBAY2hhbmdlPVwib25DaGFuZ2U0XCI+XG4gICAgICBUYWcgNFxuICAgIDwvZWwtY2hlY2stdGFnPlxuICAgIDxlbC1jaGVjay10YWcgOmNoZWNrZWQ9XCJjaGVja2VkNVwiIHR5cGU9XCJkYW5nZXJcIiBAY2hhbmdlPVwib25DaGFuZ2U1XCI+XG4gICAgICBUYWcgNVxuICAgIDwvZWwtY2hlY2stdGFnPlxuICAgIDxlbC1jaGVjay10YWdcbiAgICAgIDpjaGVja2VkPVwiY2hlY2tlZDZcIlxuICAgICAgZGlzYWJsZWRcbiAgICAgIHR5cGU9XCJzdWNjZXNzXCJcbiAgICAgIEBjaGFuZ2U9XCJvbkNoYW5nZTZcIlxuICAgID5cbiAgICAgIFRhZyA2XG4gICAgPC9lbC1jaGVjay10YWc+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgY2hlY2tlZCA9IHJlZihmYWxzZSlcbmNvbnN0IGNoZWNrZWQxID0gcmVmKHRydWUpXG5jb25zdCBjaGVja2VkMiA9IHJlZih0cnVlKVxuY29uc3QgY2hlY2tlZDMgPSByZWYodHJ1ZSlcbmNvbnN0IGNoZWNrZWQ0ID0gcmVmKHRydWUpXG5jb25zdCBjaGVja2VkNSA9IHJlZih0cnVlKVxuY29uc3QgY2hlY2tlZDYgPSByZWYodHJ1ZSlcblxuY29uc3Qgb25DaGFuZ2UgPSAoc3RhdHVzOiBib29sZWFuKSA9PiB7XG4gIGNoZWNrZWQudmFsdWUgPSBzdGF0dXNcbn1cblxuY29uc3Qgb25DaGFuZ2UxID0gKHN0YXR1czogYm9vbGVhbikgPT4ge1xuICBjaGVja2VkMS52YWx1ZSA9IHN0YXR1c1xufVxuXG5jb25zdCBvbkNoYW5nZTIgPSAoc3RhdHVzOiBib29sZWFuKSA9PiB7XG4gIGNoZWNrZWQyLnZhbHVlID0gc3RhdHVzXG59XG5cbmNvbnN0IG9uQ2hhbmdlMyA9IChzdGF0dXM6IGJvb2xlYW4pID0+IHtcbiAgY2hlY2tlZDMudmFsdWUgPSBzdGF0dXNcbn1cblxuY29uc3Qgb25DaGFuZ2U0ID0gKHN0YXR1czogYm9vbGVhbikgPT4ge1xuICBjaGVja2VkNC52YWx1ZSA9IHN0YXR1c1xufVxuXG5jb25zdCBvbkNoYW5nZTUgPSAoc3RhdHVzOiBib29sZWFuKSA9PiB7XG4gIGNoZWNrZWQ1LnZhbHVlID0gc3RhdHVzXG59XG5cbmNvbnN0IG9uQ2hhbmdlNiA9IChzdGF0dXM6IGJvb2xlYW4pID0+IHtcbiAgY2hlY2tlZDYudmFsdWUgPSBzdGF0dXNcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tag/checkable.vue)_

vue

```
<template>
  <div class="flex gap-2">
    <el-check-tag checked>Checked</el-check-tag>
    <el-check-tag :checked="checked" @change="onChange">Toggle me</el-check-tag>
    <el-check-tag disabled>Disabled</el-check-tag>
  </div>
  <div class="flex gap-2 mt-4">
    <el-check-tag :checked="checked1" type="primary" @change="onChange1">
      Tag 1
    </el-check-tag>
    <el-check-tag :checked="checked2" type="success" @change="onChange2">
      Tag 2
    </el-check-tag>
    <el-check-tag :checked="checked3" type="info" @change="onChange3">
      Tag 3
    </el-check-tag>
    <el-check-tag :checked="checked4" type="warning" @change="onChange4">
      Tag 4
    </el-check-tag>
    <el-check-tag :checked="checked5" type="danger" @change="onChange5">
      Tag 5
    </el-check-tag>
    <el-check-tag
      :checked="checked6"
      disabled
      type="success"
      @change="onChange6"
    >
      Tag 6
    </el-check-tag>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checked = ref(false)
const checked1 = ref(true)
const checked2 = ref(true)
const checked3 = ref(true)
const checked4 = ref(true)
const checked5 = ref(true)
const checked6 = ref(true)

const onChange = (status: boolean) => {
  checked.value = status
}

const onChange1 = (status: boolean) => {
  checked1.value = status
}

const onChange2 = (status: boolean) => {
  checked2.value = status
}

const onChange3 = (status: boolean) => {
  checked3.value = status
}

const onChange4 = (status: boolean) => {
  checked4.value = status
}

const onChange5 = (status: boolean) => {
  checked5.value = status
}

const onChange6 = (status: boolean) => {
  checked6.value = status
}
</script>
```

隐藏源代码

## Tag API [​](#tag-api)

### Tag Attributes [​](#tag-attributes)

| 属性名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| type | Tag 的类型 | `enum` | primary |
| closable | 是否可关闭 | `boolean` | false |
| disable-transitions | 是否禁用渐变动画 | `boolean` | false |
| hit | 是否有边框描边 | `boolean` | false |
| color | 背景色 | `string` | — |
| size | Tag 的尺寸 | `enum` | — |
| effect | Tag 的主题 | `enum` | light |
| round | Tag 是否为圆形 | `boolean` | false |

### Tag Events [​](#tag-events)

| 事件名 | 说明 | Type |
| --- | --- | --- |
| click | 点击 Tag 时触发的事件 | `Function` |
| close | 关闭 Tag 时触发的事件 | `Function` |

### Tag Slots [​](#tag-slots)

| 名称 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## CheckTag API [​](#checktag-api)

### CheckTag Attributes [​](#checktag-attributes)

| 属性名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| checked / v-model:checked | 是否选中 | `boolean` | false |
| disabled 2.8.2 | 是否禁用 | `boolean` | false |
| type 2.5.4 | CheckTag 类型 | `enum` | primary |

### CheckTag Events [​](#checktag-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 点击 Check Tag 时触发的事件 | `Function` |

### CheckTag Slots [​](#checktag-slots)

| 名称 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/tag) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/tag.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/tag.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/20987775?v=4&size=64)](https://github.com/cbbfcd)[![](https://avatars.githubusercontent.com/u/20396642?v=4&size=64)](https://github.com/zmyjs)[![](https://avatars.githubusercontent.com/u/75007029?v=4&size=64)](https://github.com/yj-liuzepeng)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/48341368?v=4&size=64)](https://github.com/HaceraI)[![](https://avatars.githubusercontent.com/u/26403700?v=4&size=64)](https://github.com/blesstosam)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/49635988?v=4&size=64)](https://github.com/BgaSol)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)

[Virtualized Table 虚拟化表格](https://element-plus.org/zh-CN/component/table-v2)

[Timeline 时间线](https://element-plus.org/zh-CN/component/timeline)


