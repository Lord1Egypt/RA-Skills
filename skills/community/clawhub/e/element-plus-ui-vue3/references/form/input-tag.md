---
name: "input-tag"
description: "Input Tag 标签输入框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Input Tag 标签输入框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/input-tag.html"
---

---

# InputTag 标签输入框 [​](#inputtag-标签输入框)

更新日志待解决

0

InputTag 组件允许用户添加内容作为标签

## 基础用法 [​](#基础用法)

按Enter回车键添加输入内容为标签

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtdGFnXG4gICAgdi1tb2RlbD1cImlucHV0XCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgYXJpYS1sYWJlbD1cIlBsZWFzZSBjbGljayB0aGUgRW50ZXIga2V5IGFmdGVyIGlucHV0XCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGlucHV0ID0gcmVmPHN0cmluZ1tdPigpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/basic.vue)_

vue

```
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

隐藏源代码

## 自定义触发器 [​](#自定义触发器)

您可以自定义用于触发输入标签的键位， 默认是Enter 回车键

Enter

Space

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1zZWdtZW50ZWQgdi1tb2RlbD1cInRyaWdnZXJcIiA6b3B0aW9ucz1cIm9wdGlvbnNcIiAvPlxuICA8L2Rpdj5cbiAgPGJyIC8+XG4gIDxlbC1pbnB1dC10YWcgdi1tb2RlbD1cImlucHV0XCIgOnRyaWdnZXI9XCJ0cmlnZ2VyXCIgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXRcIiAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVWRU5UX0NPREUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHRyaWdnZXIgPSByZWY8J0VudGVyJyB8ICdTcGFjZSc+KCdTcGFjZScpXG5jb25zdCBpbnB1dCA9IHJlZjxzdHJpbmdbXT4oKVxuY29uc3Qgb3B0aW9ucyA9IFtFVkVOVF9DT0RFLmVudGVyLCBFVkVOVF9DT0RFLnNwYWNlXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/trigger.vue)_

vue

```
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

隐藏源代码

## 最大标签数 [​](#最大标签数)

您可以设置可以添加的标签数量限制。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtdGFnIHYtbW9kZWw9XCJpbnB1dFwiIDptYXg9XCIzXCIgcGxhY2Vob2xkZXI9XCJlbnRlciB1cCB0byAzIHRhZ3NcIiAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5wdXQgPSByZWY8c3RyaW5nW10+KClcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/max.vue)_

vue

```
<template>
  <el-input-tag v-model="input" :max="3" placeholder="enter up to 3 tags" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref<string[]>()
</script>
```

隐藏源代码

## 折叠标签2.11.0 [​](#折叠标签)

使用折叠标签属性将它们合并成一块文本。 您可以使用折叠标签工具提示属性来启用悬停在折叠文本上的行为来显示特定的选定值。 使用折叠标签工具提示属性会使最大属性无效。

use collapse-tags

use collapse-tags-tooltip

use max-collapse-tags

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+dXNlIGNvbGxhcHNlLXRhZ3M8L3A+XG4gICAgPGVsLWlucHV0LXRhZ1xuICAgICAgdi1tb2RlbD1cImlucHV0MVwiXG4gICAgICBjb2xsYXBzZS10YWdzXG4gICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgICBhcmlhLWxhYmVsPVwiUGxlYXNlIGNsaWNrIHRoZSBFbnRlciBrZXkgYWZ0ZXIgaW5wdXRcIlxuICAgIC8+XG4gICAgPHA+dXNlIGNvbGxhcHNlLXRhZ3MtdG9vbHRpcDwvcD5cbiAgICA8ZWwtaW5wdXQtdGFnXG4gICAgICB2LW1vZGVsPVwiaW5wdXQyXCJcbiAgICAgIGNvbGxhcHNlLXRhZ3NcbiAgICAgIGNvbGxhcHNlLXRhZ3MtdG9vbHRpcFxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXRcIlxuICAgICAgYXJpYS1sYWJlbD1cIlBsZWFzZSBjbGljayB0aGUgRW50ZXIga2V5IGFmdGVyIGlucHV0XCJcbiAgICAvPlxuICAgIDxwPnVzZSBtYXgtY29sbGFwc2UtdGFnczwvcD5cbiAgICA8ZWwtaW5wdXQtdGFnXG4gICAgICB2LW1vZGVsPVwiaW5wdXQzXCJcbiAgICAgIGNvbGxhcHNlLXRhZ3NcbiAgICAgIGNvbGxhcHNlLXRhZ3MtdG9vbHRpcFxuICAgICAgOm1heC1jb2xsYXBzZS10YWdzPVwiM1wiXG4gICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgICBhcmlhLWxhYmVsPVwiUGxlYXNlIGNsaWNrIHRoZSBFbnRlciBrZXkgYWZ0ZXIgaW5wdXRcIlxuICAgIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5wdXQxID0gcmVmPHN0cmluZ1tdPigpXG5jb25zdCBpbnB1dDIgPSByZWY8c3RyaW5nW10+KClcbmNvbnN0IGlucHV0MyA9IHJlZjxzdHJpbmdbXT4oKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/collapse.vue)_

vue

```
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

隐藏源代码

## 禁用状态 [​](#禁用状态)

您可以设置 InputTag 被禁用。

tag1tag2tag3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtdGFnIHYtbW9kZWw9XCJpbnB1dFwiIGRpc2FibGVkIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCIgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGlucHV0ID0gcmVmPHN0cmluZ1tdPihbJ3RhZzEnLCAndGFnMicsICd0YWczJ10pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/disabled.vue)_

vue

```
<template>
  <el-input-tag v-model="input" disabled placeholder="Please input" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref<string[]>(['tag1', 'tag2', 'tag3'])
</script>
```

隐藏源代码

## 可清空 [​](#可清空)

您可以设置是否显示清除按钮。

tag1tag2tag3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtdGFnIHYtbW9kZWw9XCJpbnB1dFwiIGNsZWFyYWJsZSBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBpbnB1dCA9IHJlZjxzdHJpbmdbXT4oWyd0YWcxJywgJ3RhZzInLCAndGFnMyddKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/clearable.vue)_

vue

```
<template>
  <el-input-tag v-model="input" clearable placeholder="Please input" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref<string[]>(['tag1', 'tag2', 'tag3'])
</script>
```

隐藏源代码

## 自定义清除图标2.11.0 [​](#自定义清除图标)

你可以通过`clear-icon`属性自定义清除图标

customclearicon

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtdGFnXG4gICAgdi1tb2RlbD1cImlucHV0XCJcbiAgICBjbGVhcmFibGVcbiAgICA6Y2xlYXItaWNvbj1cIkNsb3NlQm9sZFwiXG4gICAgcGxhY2Vob2xkZXI9XCJDdXN0b20gY2xlYXIgaWNvblwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgQ2xvc2VCb2xkIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IGlucHV0ID0gcmVmPHN0cmluZ1tdPihbJ2N1c3RvbScsICdjbGVhcicsICdpY29uJ10pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/clear-icon.vue)_

vue

```
<template>
  <el-input-tag
    v-model="input"
    clearable
    :clear-icon="CloseBold"
    placeholder="Custom clear icon"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CloseBold } from '@element-plus/icons-vue'

const input = ref<string[]>(['custom', 'clear', 'icon'])
</script>
```

隐藏源代码

## 可拖放 [​](#可拖放)

您可以设置是否可以拖动标签。

tag1tag2tag3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtdGFnIHYtbW9kZWw9XCJpbnB1dFwiIGRyYWdnYWJsZSBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBpbnB1dCA9IHJlZjxzdHJpbmdbXT4oWyd0YWcxJywgJ3RhZzInLCAndGFnMyddKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/draggable.vue)_

vue

```
<template>
  <el-input-tag v-model="input" draggable placeholder="Please input" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref<string[]>(['tag1', 'tag2', 'tag3'])
</script>
```

隐藏源代码

## 分隔符2.9.9 [​](#分隔符)

当一个分隔符匹配时，您可以添加一个标签。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtdGFnXG4gICAgdi1tb2RlbD1cImlucHV0XCJcbiAgICBkcmFnZ2FibGVcbiAgICBwbGFjZWhvbGRlcj1cIlRyeSB0byBzZXBhcmF0ZSB3b3JkcyB3aXRoICxcIlxuICAgIGRlbGltaXRlcj1cIixcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5wdXQgPSByZWY8c3RyaW5nW10+KFtdKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/delimiter.vue)_

vue

```
<template>
  <el-input-tag
    v-model="input"
    draggable
    placeholder="Try to separate words with ,"
    delimiter=","
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref<string[]>([])
</script>
```

隐藏源代码

## 尺寸 [​](#尺寸)

使用 `size` 属性改变输入框大小。 除了默认大小外，还有另外两个选项： `large`, `small`。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtdGFnIHYtbW9kZWw9XCJpbnB1dFwiIHNpemU9XCJsYXJnZVwiIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCIgLz5cbiAgPGJyIC8+XG4gIDxlbC1pbnB1dC10YWcgdi1tb2RlbD1cImlucHV0XCIgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXRcIiAvPlxuICA8YnIgLz5cbiAgPGVsLWlucHV0LXRhZyB2LW1vZGVsPVwiaW5wdXRcIiBzaXplPVwic21hbGxcIiBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBpbnB1dCA9IHJlZjxzdHJpbmdbXT4oKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/size.vue)_

vue

```
<template>
  <el-input-tag v-model="input" size="large" placeholder="Please input" />
  <br />
  <el-input-tag v-model="input" placeholder="Please input" />
  <br />
  <el-input-tag v-model="input" size="small" placeholder="Please input" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref<string[]>()
</script>
```

隐藏源代码

## 自定义标签 [​](#自定义标签)

您可以通过`tag`插槽自定义标签内容。

primary

success

info

warning

danger

light

dark

plain

tag1

tag2

tag3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1zZWdtZW50ZWQgdi1tb2RlbD1cInRhZ1R5cGVcIiA6b3B0aW9ucz1cInR5cGVcIiBjbGFzcz1cIm1yLTVcIiAvPlxuICAgIDxlbC1zZWdtZW50ZWQgdi1tb2RlbD1cInRhZ0VmZmVjdFwiIDpvcHRpb25zPVwiZWZmZWN0XCIgLz5cbiAgPC9kaXY+XG4gIDxiciAvPlxuICA8ZWwtaW5wdXQtdGFnXG4gICAgdi1tb2RlbD1cImlucHV0XCJcbiAgICA6dGFnLXR5cGU9XCJ0YWdUeXBlXCJcbiAgICA6dGFnLWVmZmVjdD1cInRhZ0VmZmVjdFwiXG4gICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXRcIlxuICA+XG4gICAgPHRlbXBsYXRlICN0YWc9XCJ7IHZhbHVlIH1cIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJmbGV4IGl0ZW1zLWNlbnRlclwiPlxuICAgICAgICA8ZWwtaWNvbiBjbGFzcz1cIm1yLTFcIj5cbiAgICAgICAgICA8RWxlbWVudFBsdXMgLz5cbiAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICA8c3Bhbj57eyB2YWx1ZSB9fTwvc3Bhbj5cbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtaW5wdXQtdGFnPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsZW1lbnRQbHVzIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmltcG9ydCB0eXBlIHsgVGFnUHJvcHMgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHR5cGU6IEFycmF5PFRhZ1Byb3BzWyd0eXBlJ10+ID0gW1xuICAncHJpbWFyeScsXG4gICdzdWNjZXNzJyxcbiAgJ2luZm8nLFxuICAnd2FybmluZycsXG4gICdkYW5nZXInLFxuXVxuY29uc3QgZWZmZWN0OiBBcnJheTxUYWdQcm9wc1snZWZmZWN0J10+ID0gWydsaWdodCcsICdkYXJrJywgJ3BsYWluJ11cblxuY29uc3QgdGFnVHlwZSA9IHJlZjxUYWdQcm9wc1sndHlwZSddPigncHJpbWFyeScpXG5jb25zdCB0YWdFZmZlY3QgPSByZWY8VGFnUHJvcHNbJ2VmZmVjdCddPigncGxhaW4nKVxuY29uc3QgaW5wdXQgPSByZWY8c3RyaW5nW10+KFsndGFnMScsICd0YWcyJywgJ3RhZzMnXSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/tag.vue)_

vue

```
<template>
  <div>
    <el-segmented v-model="tagType" :options="type" class="mr-5" />
    <el-segmented v-model="tagEffect" :options="effect" />
  </div>
  <br />
  <el-input-tag
    v-model="input"
    :tag-type="tagType"
    :tag-effect="tagEffect"
    placeholder="Please input"
  >
    <template #tag="{ value }">
      <div class="flex items-center">
        <el-icon class="mr-1">
          <ElementPlus />
        </el-icon>
        <span>{{ value }}</span>
      </div>
    </template>
  </el-input-tag>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElementPlus } from '@element-plus/icons-vue'

import type { TagProps } from 'element-plus'

const type: Array<TagProps['type']> = [
  'primary',
  'success',
  'info',
  'warning',
  'danger',
]
const effect: Array<TagProps['effect']> = ['light', 'dark', 'plain']

const tagType = ref<TagProps['type']>('primary')
const tagEffect = ref<TagProps['effect']>('plain')
const input = ref<string[]>(['tag1', 'tag2', 'tag3'])
</script>
```

隐藏源代码

## 自定义前缀和后缀 [​](#自定义前缀和后缀)

您可以通过`prefix`和 `suffix` 插槽自定义 InputTag 的前缀和后缀。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtdGFnIHYtbW9kZWw9XCJpbnB1dFwiIGNsZWFyYWJsZSBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiPlxuICAgIDx0ZW1wbGF0ZSAjcHJlZml4PlxuICAgICAgPGVsLWljb24+PEVsZW1lbnRQbHVzIC8+PC9lbC1pY29uPlxuICAgIDwvdGVtcGxhdGU+XG4gICAgPHRlbXBsYXRlICNzdWZmaXg+XG4gICAgICA8ZWwtaWNvbj48U2VhcmNoIC8+PC9lbC1pY29uPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtaW5wdXQtdGFnPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsZW1lbnRQbHVzLCBTZWFyY2ggfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgaW5wdXQgPSByZWY8c3RyaW5nW10+KClcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-tag/prefix-suffix.vue)_

vue

```
<template>
  <el-input-tag v-model="input" clearable placeholder="Please input">
    <template #prefix>
      <el-icon><ElementPlus /></el-icon>
    </template>
    <template #suffix>
      <el-icon><Search /></el-icon>
    </template>
  </el-input-tag>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElementPlus, Search } from '@element-plus/icons-vue'

const input = ref<string[]>()
</script>
```

隐藏源代码

## API [​](#api)

### 属性 [​](#属性)

| 名称 | 详情 | 类型 | 默认 |
| --- | --- | --- | --- |
| model-value / v-model | 绑定值 | `array` | — |
| max | 可添加标签的最大数量 | `number` | — |
| tag-type | 标签类型 | `enum` | info |
| tag-effect | 标签效果 | `enum` | light |
| effect 2.13.2 | tooltip 主题，内置了 `dark` / `light` 两种 | `enum``'dark' | 'light'` / `string` | light |
| trigger | 触发输入标签的按键 | `enum` | Enter |
| draggable | 是否可以拖动标签 | `boolean` | false |
| delimiter 2.9.9 | 在匹配分隔符时添加标签 | `string` / `regex` | — |
| size | 输入框尺寸 | `enum` | — |
| collapse-tags 2.11.0 | 多选时是否将选中值按文字的形式展示 | `boolean` | false |
| collapse-tags-tooltip 2.11.0 | 当鼠标悬停于折叠标签的文本时，是否显示所有选中的标签。 要使用此功能，`collapse-tags`的值必须为true | `boolean` | false |
| save-on-blur 2.9.7 | 当输入失去焦点时是否保存输入值 | `boolean` | true |
| clearable | 是否显示清除按钮 | `boolean` | false |
| clear-icon 2.11.0 | 自定义清除图标 | `string` / `object` | CircleClose |
| disabled | 是否禁用 | `boolean` | false |
| validate-event | 是否触发表单验证 | `boolean` | true |
| readonly | 等价于原生 `readonly` 属性 | `boolean` | false |
| autofocus | 等价于原生 `autofocus` 属性 | `boolean` | false |
| id | 等价于原生 input `id` 属性 | `string` | — |
| tabindex | 等价于原生 `tabindex` 属性 | `string` / `number` | — |
| max-collapse-tags 2.11.0 | 需要显示的 Tag 的最大数量 要使用此功能，`collapse-tags`的值必须为true | `number` | 1 |
| maxlength | 等价于原生 `maxlength` 属性 | `string` / `number` | — |
| minlength | 等价于原生 `minlength` 属性 | `string` / `number` | — |
| placeholder | 输入框占位文本 | `string` | — |
| autocomplete | 等价于原生 `autocomplete` 属性 | `string` | off |
| aria-label a11y | 等价于原生 `aria-label` 属性 | `string` | — |

### 事件 [​](#事件)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| change | 绑定值变化时触发的事件 | `Function` |
| input | 在 Input 值改变时触发 | `Function` |
| add-tag | tag 被添加时触发 | `Function` |
| remove-tag | tag 被移除时触发 | `Function` |
| drag-tag 2.11.3 | tag 被拖动时触发 | `Function` |
| focus | 在 Input 获得焦点时触发 | `Function` |
| blur | 在 Input 失去焦点时触发 | `Function` |
| clear | 点击清除图标时触发 | `Function` |

### Slots [​](#slots)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| tag | 作为tag的内容 | `object` |
| prefix | InputTag 头部内容 | — |
| suffix | InputTag 尾部内容 | — |

### 对外暴露的方法 [​](#对外暴露的方法)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| focus | 使 input 获取焦点 | `Function` |
| blur | 使 input 失去焦点 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/input-tag) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/input-tag.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/input-tag.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/189838704?v=4&size=64)](https://github.com/xiaocainiao633)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/69999356?v=4&size=64)](https://github.com/ll-huihui)[![](https://avatars.githubusercontent.com/u/32569372?v=4&size=64)](https://github.com/eighty-cents)[![](https://avatars.githubusercontent.com/u/49630878?v=4&size=64)](https://github.com/a869246700)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/66454152?v=4&size=64)](https://github.com/bryqiu)

[Input Number 数字输入框](https://element-plus.org/zh-CN/component/input-number)

[Input OTP](https://element-plus.org/zh-CN/component/input-otp)


