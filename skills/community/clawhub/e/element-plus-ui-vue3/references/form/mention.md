---
name: "mention"
description: "Mention 提及 -- Element Plus Vue3 桌面端组件。Invoke when user needs Mention 提及 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/mention.html"
---

---

# Mention 提及 [​](#mention-提及)

更新日志待解决

1

用于在输入中提及某人或某事。

## 基础用法 [​](#基础用法)

最简单的用法。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtbWVudGlvblxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICBzdHlsZT1cIndpZHRoOiAzMjBweFwiXG4gICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXRcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoJ0AnKVxuXG5jb25zdCBvcHRpb25zID0gcmVmKFtcbiAge1xuICAgIGxhYmVsOiAnRnVwaG9lbml4ZXMnLFxuICAgIHZhbHVlOiAnRnVwaG9lbml4ZXMnLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdrb29yaW9va2FtaScsXG4gICAgdmFsdWU6ICdrb29yaW9va2FtaScsXG4gIH0sXG4gIHtcbiAgICBsYWJlbDogJ0plcmVteScsXG4gICAgdmFsdWU6ICdKZXJlbXknLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdidGVhJyxcbiAgICB2YWx1ZTogJ2J0ZWEnLFxuICB9LFxuXSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/mention/basic.vue)_

vue

```
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

隐藏源代码

## Props 2.11.3 [​](#props)

你可以通过 `props` 属性自定义 `options` 的别名。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtbWVudGlvblxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgc3R5bGU9XCJ3aWR0aDogMzIwcHhcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKCdAJylcbmNvbnN0IHByb3BzID0geyBsYWJlbDogJ25hbWUnLCB2YWx1ZTogJ2lkJywgZGlzYWJsZWQ6ICd1bmFibGUnIH1cbmNvbnN0IG9wdGlvbnMgPSByZWYoW1xuICB7XG4gICAgbmFtZTogJ0Z1cGhvZW5peGVzJyxcbiAgICBpZDogJ0Z1cGhvZW5peGVzJyxcbiAgICB1bmFibGU6IHRydWUsXG4gIH0sXG4gIHtcbiAgICBuYW1lOiAna29vcmlvb2thbWknLFxuICAgIGlkOiAna29vcmlvb2thbWknLFxuICB9LFxuICB7XG4gICAgbmFtZTogJ0plcmVteScsXG4gICAgaWQ6ICdKZXJlbXknLFxuICAgIHVuYWJsZTogdHJ1ZSxcbiAgfSxcbiAge1xuICAgIG5hbWU6ICdidGVhJyxcbiAgICBpZDogJ2J0ZWEnLFxuICB9LFxuXSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/mention/props.vue)_

vue

```
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

隐藏源代码

## Textarea [​](#textarea)

输入类型可以设置为 `textarea` 。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtbWVudGlvblxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgdHlwZT1cInRleHRhcmVhXCJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgIHN0eWxlPVwid2lkdGg6IDMyMHB4XCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZignJylcblxuY29uc3Qgb3B0aW9ucyA9IHJlZihbXG4gIHtcbiAgICBsYWJlbDogJ0Z1cGhvZW5peGVzJyxcbiAgICB2YWx1ZTogJ0Z1cGhvZW5peGVzJyxcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAna29vcmlvb2thbWknLFxuICAgIHZhbHVlOiAna29vcmlvb2thbWknLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdKZXJlbXknLFxuICAgIHZhbHVlOiAnSmVyZW15JyxcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAnYnRlYScsXG4gICAgdmFsdWU6ICdidGVhJyxcbiAgfSxcbl0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/mention/textarea.vue)_

vue

```
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

隐藏源代码

## 自定义标签 [​](#自定义标签)

使用 "label" 自定义标签。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtbWVudGlvblxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICBzdHlsZT1cIndpZHRoOiAzMjBweFwiXG4gICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXRcIlxuICA+XG4gICAgPHRlbXBsYXRlICNsYWJlbD1cInsgaXRlbSB9XCI+XG4gICAgICA8ZGl2IHN0eWxlPVwiZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IGNlbnRlclwiPlxuICAgICAgICA8ZWwtYXZhdGFyIDpzaXplPVwiMjRcIiA6c3JjPVwiaXRlbS5hdmF0YXJcIiAvPlxuICAgICAgICA8c3BhbiBzdHlsZT1cIm1hcmdpbi1sZWZ0OiA2cHhcIj57eyBpdGVtLnZhbHVlIH19PC9zcGFuPlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1tZW50aW9uPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoJycpXG5cbmNvbnN0IG9wdGlvbnMgPSByZWYoW1xuICB7XG4gICAgdmFsdWU6ICdGdXBob2VuaXhlcycsXG4gICAgYXZhdGFyOiAnaHR0cHM6Ly9hdmF0YXJzLmdpdGh1YnVzZXJjb250ZW50LmNvbS91LzI3OTEyMjMyJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAna29vcmlvb2thbWknLFxuICAgIGF2YXRhcjogJ2h0dHBzOi8vYXZhdGFycy5naXRodWJ1c2VyY29udGVudC5jb20vdS8zODM5MjMxNScsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ0plcmVteScsXG4gICAgYXZhdGFyOiAnaHR0cHM6Ly9hdmF0YXJzLmdpdGh1YnVzZXJjb250ZW50LmNvbS91LzE1OTc1Nzg1JyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnYnRlYScsXG4gICAgYXZhdGFyOiAnaHR0cHM6Ly9hdmF0YXJzLmdpdGh1YnVzZXJjb250ZW50LmNvbS91LzI0NTE2NjU0JyxcbiAgfSxcbl0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/mention/label.vue)_

vue

```
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

隐藏源代码

## 加载远程选项 [​](#加载远程选项)

异步加载选项。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtbWVudGlvblxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICA6bG9hZGluZz1cImxvYWRpbmdcIlxuICAgIHN0eWxlPVwid2lkdGg6IDMyMHB4XCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgQHNlYXJjaD1cImhhbmRsZVNlYXJjaFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgb25CZWZvcmVVbm1vdW50LCByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgTWVudGlvbk9wdGlvbiB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgdmFsdWUgPSByZWYoJycpXG5jb25zdCBsb2FkaW5nID0gcmVmKGZhbHNlKVxuY29uc3Qgb3B0aW9ucyA9IHJlZjxNZW50aW9uT3B0aW9uW10+KFtdKVxuXG5sZXQgdGltZXI6IFJldHVyblR5cGU8dHlwZW9mIHNldFRpbWVvdXQ+XG5jb25zdCBoYW5kbGVTZWFyY2ggPSAocGF0dGVybjogc3RyaW5nKSA9PiB7XG4gIGlmICh0aW1lcikgY2xlYXJUaW1lb3V0KHRpbWVyKVxuXG4gIGxvYWRpbmcudmFsdWUgPSB0cnVlXG4gIHRpbWVyID0gc2V0VGltZW91dCgoKSA9PiB7XG4gICAgb3B0aW9ucy52YWx1ZSA9IFsnRnVwaG9lbml4ZXMnLCAna29vcmlvb2thbWknLCAnSmVyZW15JywgJ2J0ZWEnXS5tYXAoXG4gICAgICAoaXRlbSkgPT4gKHtcbiAgICAgICAgbGFiZWw6IHBhdHRlcm4gKyBpdGVtLFxuICAgICAgICB2YWx1ZTogcGF0dGVybiArIGl0ZW0sXG4gICAgICB9KVxuICAgIClcbiAgICBsb2FkaW5nLnZhbHVlID0gZmFsc2VcbiAgfSwgMTUwMClcbn1cblxub25CZWZvcmVVbm1vdW50KCgpID0+IHtcbiAgaWYgKHRpbWVyKSBjbGVhclRpbWVvdXQodGltZXIpXG59KVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/mention/loading.vue)_

vue

```
<template>
  <el-mention
    v-model="value"
    :options="options"
    :loading="loading"
    style="width: 320px"
    placeholder="Please input"
    @search="handleSearch"
  />
</template>

<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'

import type { MentionOption } from 'element-plus'

const value = ref('')
const loading = ref(false)
const options = ref<MentionOption[]>([])

let timer: ReturnType<typeof setTimeout>
const handleSearch = (pattern: string) => {
  if (timer) clearTimeout(timer)

  loading.value = true
  timer = setTimeout(() => {
    options.value = ['Fuphoenixes', 'kooriookami', 'Jeremy', 'btea'].map(
      (item) => ({
        label: pattern + item,
        value: pattern + item,
      })
    )
    loading.value = false
  }, 1500)
}

onBeforeUnmount(() => {
  if (timer) clearTimeout(timer)
})
</script>
```

隐藏源代码

## 自定义触发字段 [​](#自定义触发字段)

通过 `prefix` 属性 自定义触发字段。 默认为 `@`, `Array<string>` 。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtbWVudGlvblxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICA6cHJlZml4PVwiWydAJywgJyMnXVwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMzIwcHhcIlxuICAgIHBsYWNlaG9sZGVyPVwiaW5wdXQgQCB0byBtZW50aW9uIHBlb3BsZSwgIyB0byBtZW50aW9uIHRhZ1wiXG4gICAgQHNlYXJjaD1cImhhbmRsZVNlYXJjaFwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IE1lbnRpb25PcHRpb24gfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IE1PQ0tfREFUQTogUmVjb3JkPHN0cmluZywgc3RyaW5nW10+ID0ge1xuICAnQCc6IFsnRnVwaG9lbml4ZXMnLCAna29vcmlvb2thbWknLCAnSmVyZW15JywgJ2J0ZWEnXSxcbiAgJyMnOiBbJzEuMCcsICcyLjAnLCAnMy4wJ10sXG59XG5jb25zdCB2YWx1ZSA9IHJlZignJylcbmNvbnN0IG9wdGlvbnMgPSByZWY8TWVudGlvbk9wdGlvbltdPihbXSlcblxuY29uc3QgaGFuZGxlU2VhcmNoID0gKF86IHN0cmluZywgcHJlZml4OiBzdHJpbmcpID0+IHtcbiAgb3B0aW9ucy52YWx1ZSA9IChNT0NLX0RBVEFbcHJlZml4XSB8fCBbXSkubWFwKCh2YWx1ZSkgPT4gKHtcbiAgICB2YWx1ZSxcbiAgfSkpXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/mention/prefix.vue)_

vue

```
<template>
  <el-mention
    v-model="value"
    :options="options"
    :prefix="['@', '#']"
    style="width: 320px"
    placeholder="input @ to mention people, # to mention tag"
    @search="handleSearch"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

import type { MentionOption } from 'element-plus'

const MOCK_DATA: Record<string, string[]> = {
  '@': ['Fuphoenixes', 'kooriookami', 'Jeremy', 'btea'],
  '#': ['1.0', '2.0', '3.0'],
}
const value = ref('')
const options = ref<MentionOption[]>([])

const handleSearch = (_: string, prefix: string) => {
  options.value = (MOCK_DATA[prefix] || []).map((value) => ({
    value,
  }))
}
</script>
```

隐藏源代码

## 整体删除 [​](#整体删除)

将`whole`属性设置为 `true`，当您按下退格键时，此处的 mention 区域将作为一个整体被删除。 设置 "check-is-whole" 属性来自定义检查逻辑。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtbWVudGlvblxuICAgIHYtbW9kZWw9XCJ2YWx1ZTFcIlxuICAgIHdob2xlXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zMVwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMzIwcHhcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgLz5cbiAgPGVsLWRpdmlkZXIgLz5cbiAgPGVsLW1lbnRpb25cbiAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnMyXCJcbiAgICA6cHJlZml4PVwiWydAJywgJyMnXVwiXG4gICAgd2hvbGVcbiAgICA6Y2hlY2staXMtd2hvbGU9XCJjaGVja0lzV2hvbGVcIlxuICAgIHN0eWxlPVwid2lkdGg6IDMyMHB4XCJcbiAgICBwbGFjZWhvbGRlcj1cImlucHV0IEAgdG8gbWVudGlvbiBwZW9wbGUsICMgdG8gbWVudGlvbiB0YWdcIlxuICAgIEBzZWFyY2g9XCJoYW5kbGVTZWFyY2hcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBNZW50aW9uT3B0aW9uIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBNT0NLX0RBVEE6IFJlY29yZDxzdHJpbmcsIHN0cmluZ1tdPiA9IHtcbiAgJ0AnOiBbJ0Z1cGhvZW5peGVzJywgJ2tvb3Jpb29rYW1pJywgJ0plcmVteScsICdidGVhJ10sXG4gICcjJzogWycxLjAnLCAnMi4wJywgJzMuMCddLFxufVxuY29uc3QgdmFsdWUxID0gcmVmKCcnKVxuY29uc3QgdmFsdWUyID0gcmVmKCcnKVxuY29uc3Qgb3B0aW9uczEgPSByZWY8TWVudGlvbk9wdGlvbltdPihcbiAgTU9DS19EQVRBWydAJ10ubWFwKCh2YWx1ZSkgPT4gKHsgdmFsdWUgfSkpXG4pXG5jb25zdCBvcHRpb25zMiA9IHJlZjxNZW50aW9uT3B0aW9uW10+KFtdKVxuXG5jb25zdCBoYW5kbGVTZWFyY2ggPSAoXzogc3RyaW5nLCBwcmVmaXg6IHN0cmluZykgPT4ge1xuICBvcHRpb25zMi52YWx1ZSA9IChNT0NLX0RBVEFbcHJlZml4XSB8fCBbXSkubWFwKCh2YWx1ZSkgPT4gKHtcbiAgICB2YWx1ZSxcbiAgfSkpXG59XG5cbmNvbnN0IGNoZWNrSXNXaG9sZSA9IChwYXR0ZXJuOiBzdHJpbmcsIHByZWZpeDogc3RyaW5nKSA9PiB7XG4gIHJldHVybiAoTU9DS19EQVRBW3ByZWZpeF0gfHwgW10pLmluY2x1ZGVzKHBhdHRlcm4pXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/mention/whole.vue)_

vue

```
<template>
  <el-mention
    v-model="value1"
    whole
    :options="options1"
    style="width: 320px"
    placeholder="Please input"
  />
  <el-divider />
  <el-mention
    v-model="value2"
    :options="options2"
    :prefix="['@', '#']"
    whole
    :check-is-whole="checkIsWhole"
    style="width: 320px"
    placeholder="input @ to mention people, # to mention tag"
    @search="handleSearch"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

import type { MentionOption } from 'element-plus'

const MOCK_DATA: Record<string, string[]> = {
  '@': ['Fuphoenixes', 'kooriookami', 'Jeremy', 'btea'],
  '#': ['1.0', '2.0', '3.0'],
}
const value1 = ref('')
const value2 = ref('')
const options1 = ref<MentionOption[]>(
  MOCK_DATA['@'].map((value) => ({ value }))
)
const options2 = ref<MentionOption[]>([])

const handleSearch = (_: string, prefix: string) => {
  options2.value = (MOCK_DATA[prefix] || []).map((value) => ({
    value,
  }))
}

const checkIsWhole = (pattern: string, prefix: string) => {
  return (MOCK_DATA[prefix] || []).includes(pattern)
}
</script>
```

隐藏源代码

## 在表单里使用 [​](#在表单里使用)

与 `el-form` 一起使用

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZm9ybVxuICAgIHJlZj1cInJ1bGVGb3JtUmVmXCJcbiAgICBzdHlsZT1cIm1heC13aWR0aDogNjAwcHhcIlxuICAgIDptb2RlbD1cInJ1bGVGb3JtXCJcbiAgICA6cnVsZXM9XCJydWxlc1wiXG4gID5cbiAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwibmFtZVwiIHByb3A9XCJuYW1lXCI+XG4gICAgICA8ZWwtbWVudGlvbiB2LW1vZGVsPVwicnVsZUZvcm0ubmFtZVwiIDpvcHRpb25zPVwib3B0aW9uc1wiIC8+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cImRlc2NcIiBwcm9wPVwiZGVzY1wiPlxuICAgICAgPGVsLW1lbnRpb24gdi1tb2RlbD1cInJ1bGVGb3JtLmRlc2NcIiB0eXBlPVwidGV4dGFyZWFcIiA6b3B0aW9ucz1cIm9wdGlvbnNcIiAvPlxuICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgIDxlbC1mb3JtLWl0ZW0+XG4gICAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwic3VibWl0Rm9ybShydWxlRm9ybVJlZilcIj5cbiAgICAgICAgU3VibWl0XG4gICAgICA8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwicmVzZXRGb3JtKHJ1bGVGb3JtUmVmKVwiPlJlc2V0PC9lbC1idXR0b24+XG4gICAgPC9lbC1mb3JtLWl0ZW0+XG4gIDwvZWwtZm9ybT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWFjdGl2ZSwgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IEZvcm1JbnN0YW5jZSwgRm9ybVJ1bGVzIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbnRlcmZhY2UgUnVsZUZvcm0ge1xuICBuYW1lOiBzdHJpbmdcbiAgZGVzYzogc3RyaW5nXG59XG5jb25zdCBydWxlRm9ybVJlZiA9IHJlZjxGb3JtSW5zdGFuY2U+KClcbmNvbnN0IHJ1bGVGb3JtID0gcmVhY3RpdmU8UnVsZUZvcm0+KHtcbiAgbmFtZTogJycsXG4gIGRlc2M6ICcnLFxufSlcblxuY29uc3Qgb3B0aW9ucyA9IHJlZihbXG4gIHtcbiAgICBsYWJlbDogJ0Z1cGhvZW5peGVzJyxcbiAgICB2YWx1ZTogJ0Z1cGhvZW5peGVzJyxcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAna29vcmlvb2thbWknLFxuICAgIHZhbHVlOiAna29vcmlvb2thbWknLFxuICB9LFxuICB7XG4gICAgbGFiZWw6ICdKZXJlbXknLFxuICAgIHZhbHVlOiAnSmVyZW15JyxcbiAgfSxcbiAge1xuICAgIGxhYmVsOiAnYnRlYScsXG4gICAgdmFsdWU6ICdidGVhJyxcbiAgfSxcbl0pXG5cbmNvbnN0IHJ1bGVzID0gcmVhY3RpdmU8Rm9ybVJ1bGVzPFJ1bGVGb3JtPj4oe1xuICBuYW1lOiBbeyByZXF1aXJlZDogdHJ1ZSwgbWVzc2FnZTogJ1BsZWFzZSBpbnB1dCBuYW1lJywgdHJpZ2dlcjogJ2JsdXInIH1dLFxuICBkZXNjOiBbeyByZXF1aXJlZDogdHJ1ZSwgbWVzc2FnZTogJ1BsZWFzZSBpbnB1dCBkZXNjJywgdHJpZ2dlcjogJ2JsdXInIH1dLFxufSlcblxuY29uc3Qgc3VibWl0Rm9ybSA9IGFzeW5jIChmb3JtRWw6IEZvcm1JbnN0YW5jZSB8IHVuZGVmaW5lZCkgPT4ge1xuICBpZiAoIWZvcm1FbCkgcmV0dXJuXG4gIGF3YWl0IGZvcm1FbC52YWxpZGF0ZSgodmFsaWQsIGZpZWxkcykgPT4ge1xuICAgIGlmICh2YWxpZCkge1xuICAgICAgY29uc29sZS5sb2coJ3N1Ym1pdCEnKVxuICAgIH0gZWxzZSB7XG4gICAgICBjb25zb2xlLmxvZygnZXJyb3Igc3VibWl0IScsIGZpZWxkcylcbiAgICB9XG4gIH0pXG59XG5cbmNvbnN0IHJlc2V0Rm9ybSA9IChmb3JtRWw6IEZvcm1JbnN0YW5jZSB8IHVuZGVmaW5lZCkgPT4ge1xuICBpZiAoIWZvcm1FbCkgcmV0dXJuXG4gIGZvcm1FbC5yZXNldEZpZWxkcygpXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/mention/form.vue)_

vue

```
<template>
  <el-form
    ref="ruleFormRef"
    style="max-width: 600px"
    :model="ruleForm"
    :rules="rules"
  >
    <el-form-item label="name" prop="name">
      <el-mention v-model="ruleForm.name" :options="options" />
    </el-form-item>
    <el-form-item label="desc" prop="desc">
      <el-mention v-model="ruleForm.desc" type="textarea" :options="options" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)">
        Submit
      </el-button>
      <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

import type { FormInstance, FormRules } from 'element-plus'

interface RuleForm {
  name: string
  desc: string
}
const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive<RuleForm>({
  name: '',
  desc: '',
})

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

const rules = reactive<FormRules<RuleForm>>({
  name: [{ required: true, message: 'Please input name', trigger: 'blur' }],
  desc: [{ required: true, message: 'Please input desc', trigger: 'blur' }],
})

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      console.log('submit!')
    } else {
      console.log('error submit!', fields)
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>
```

隐藏源代码

TIP

由于这个组件是基于[`el-input`](https://element-plus.org/zh-CN/component/input#attributes)派生的，他们的原始属性未被更改，故不在此重复。请跳转查看原组件的相应文档。

## API [​](#api)

### 属性 [​](#属性)

| 名称 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| options | 提及选项列表 | `array` | `[]` |
| props 2.11.3 | options 的配置 | `object` | `{value: 'value', label: 'label', disabled: 'disabled'}` |
| prefix | 触发字段的前缀。 字符串长度必须且只能为 1 | `string` | `array` | `'@'` |
| split | 用于拆分提及的字符。 字符串长度必须且只能为 1 | `string` | `' '` |
| filter-option | 定制筛选器选项逻辑 | `false` | `Function` | — |
| placement | 设置弹出位置 | `string` | `'bottom'` |
| show-arrow | 下拉菜单的内容是否有箭头 | `boolean` | `false` |
| offset | 下拉面板偏移量 | `number` | `0` |
| whole | 当退格键被按下做删除操作时，是否将提及部分作为整体删除 | `boolean` | `false` |
| check-is-whole | 当退格键被按下做删除操作时，检查是否将提及部分作为整体删除 | `Function` | — |
| loading | 提及的下拉面板是否处于加载状态 | `boolean` | `false` |
| model-value / v-model | 输入值 | `string` | — |
| popper-class | 自定义浮层类名 | `string` / `object` | `string` |
| popper-style 2.11.5 | 自定义浮层类名 | `string` / `object` | — |
| popper-options | [popper.js](https://popper.js.org/docs/v2/) 参数 | `object` refer to [popper.js doc](https://popper.js.org/docs/v2/) | — |
| [input props](https://element-plus.org/zh-CN/component/input#attributes) | — | — | — |

### 事件 [​](#事件)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| search | 按下触发字段时触发 | `Function` |
| select | 当用户选择选项时触发 | `Function` |
| whole-remove 2.10.4 | 当整个 mention 被移除，且 `whole` 为 `true` 或 `check-is-whole` 为 `true` 时触发。 | `Function` |
| [input events](https://element-plus.org/zh-CN/component/input#events) | — | — |

### Slots [​](#slots)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| label | 自定义标签内容 | `object` |
| loading | 自定义 loading内容 | — |
| header | 下拉列表顶部的内容 | — |
| footer | 下拉列表底部的内容 | — |
| [input slots](https://element-plus.org/zh-CN/component/input#slots) | — | — |

### Exposes [​](#exposes)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| input | el-input 组件实例 | `object` |
| tooltip | el-tooltip 组件实例 | `object` |
| dropdownVisible 2.8.5 | tooltip 显示状态 | `object` |

## 类型声明 [​](#类型声明)

显示类型声明

ts

```
type MentionOption = {
  value?: string
  label?: string
  disabled?: boolean
  [key: string]: any
}

type MentionOptionProps = {
  value?: string
  label?: string
  disabled?: string
  [key: string]: string | undefined
}
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/mention) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/mention.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/mention.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/20411966?v=4&size=64)](https://github.com/SorrowX)[![](https://avatars.githubusercontent.com/u/27912232?v=4&size=64)](https://github.com/Fuphoenixes)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/29424213?v=4&size=64)](https://github.com/56jun)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)

[Input OTP](https://element-plus.org/zh-CN/component/input-otp)

[Radio 单选框](https://element-plus.org/zh-CN/component/radio)


