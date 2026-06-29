---
name: "select-v2"
description: "Virtualized Select 虚拟化选择器 -- Element Plus Vue3 桌面端组件。Invoke when user needs Virtualized Select 虚拟化选择器 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/select-v2.html"
---

---

# Virtualized Select 虚拟化选择器 [​](#virtualized-select-虚拟化选择器)

更新日志待解决

8

TIP

这个组件目前在测试当中，如果在使用中发现任何漏洞和问题，请在 [GitHub](https://github.com/element-plus/element-plus/issues) 中提交 issue 以便我们进行处理。

## 背景 [​](#背景)

在某些使用情况下，单个选择器可能最终加载数万行数据。 将这么多的数据渲染至 DOM 中可能会给浏览器带来负担，从而造成性能问题。 为了更好的用户和开发者体验，我们决定添加此组件。

## 基础用法 [​](#基础用法)

适用广泛的基础选择器

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIHNlbGVjdFwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5pdGlhbHMgPSBbJ2EnLCAnYicsICdjJywgJ2QnLCAnZScsICdmJywgJ2cnLCAnaCcsICdpJywgJ2onXVxuXG5jb25zdCB2YWx1ZSA9IHJlZigpXG5jb25zdCBvcHRpb25zID0gQXJyYXkuZnJvbSh7IGxlbmd0aDogMTAwMCB9KS5tYXAoKF8sIGlkeCkgPT4gKHtcbiAgdmFsdWU6IGBPcHRpb24gJHtpZHggKyAxfWAsXG4gIGxhYmVsOiBgJHtpbml0aWFsc1tpZHggJSAxMF19JHtpZHh9YCxcbn0pKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/basic-usage.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    :options="options"
    placeholder="Please select"
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref()
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>
```

隐藏源代码

## 多选 [​](#多选)

最基础的多选选择器

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIHNlbGVjdFwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgIG11bHRpcGxlXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBpbml0aWFscyA9IFsnYScsICdiJywgJ2MnLCAnZCcsICdlJywgJ2YnLCAnZycsICdoJywgJ2knLCAnaiddXG5cbmNvbnN0IHZhbHVlID0gcmVmKFtdKVxuY29uc3Qgb3B0aW9ucyA9IHJlZihcbiAgQXJyYXkuZnJvbSh7IGxlbmd0aDogMTAwMCB9KS5tYXAoKF8sIGlkeCkgPT4gKHtcbiAgICB2YWx1ZTogYE9wdGlvbiAke2lkeCArIDF9YCxcbiAgICBsYWJlbDogYCR7aW5pdGlhbHNbaWR4ICUgMTBdfSR7aWR4fWAsXG4gIH0pKVxuKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/multiple.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    :options="options"
    placeholder="Please select"
    style="width: 240px"
    multiple
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref([])
const options = ref(
  Array.from({ length: 1000 }).map((_, idx) => ({
    value: `Option ${idx + 1}`,
    label: `${initials[idx % 10]}${idx}`,
  }))
)
</script>
```

隐藏源代码

## 尺寸 [​](#尺寸)

使用 `size` 属性改变选择器大小。 除了默认大小外，还有另外两个选项： `large`, `small`。

Please select

Please select

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTQgaXRlbXMtY2VudGVyXCI+XG4gICAgPGVsLXNlbGVjdC12MlxuICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgICAgc2l6ZT1cImxhcmdlXCJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAvPlxuICAgIDxlbC1zZWxlY3QtdjJcbiAgICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2Ugc2VsZWN0XCJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAvPlxuICAgIDxlbC1zZWxlY3QtdjJcbiAgICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2Ugc2VsZWN0XCJcbiAgICAgIHNpemU9XCJzbWFsbFwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBpbml0aWFscyA9IFsnYScsICdiJywgJ2MnLCAnZCcsICdlJywgJ2YnLCAnZycsICdoJywgJ2knLCAnaiddXG5cbmNvbnN0IHZhbHVlID0gcmVmKClcbmNvbnN0IG9wdGlvbnMgPSBBcnJheS5mcm9tKHsgbGVuZ3RoOiAxMDAwIH0pLm1hcCgoXywgaWR4KSA9PiAoe1xuICB2YWx1ZTogYE9wdGlvbiAke2lkeCArIDF9YCxcbiAgbGFiZWw6IGAke2luaXRpYWxzW2lkeCAlIDEwXX0ke2lkeH1gLFxufSkpXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5leGFtcGxlLXNob3djYXNlIC5lbC1zZWxlY3QtdjIge1xuICBtYXJnaW4tcmlnaHQ6IDIwcHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/size.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-4 items-center">
    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      size="large"
      style="width: 240px"
    />
    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
    />
    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      size="small"
      style="width: 240px"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref()
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>

<style scoped>
.example-showcase .el-select-v2 {
  margin-right: 20px;
}
</style>
```

隐藏源代码

## 隐藏多余标签的多选 [​](#隐藏多余标签的多选)

默认情况下选中值会以 Tag 的形式展现，你也可以设置`collapse-tags`属性将它们合并为一段文字。 您可以使用 `collapse-tags-tooltip` 属性来启用鼠标悬停折叠文字以显示具体所选值的行为。

use collapse-tags

Please select

use collapse-tags-tooltip

Please select

use max-collapse-tags

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+dXNlIGNvbGxhcHNlLXRhZ3M8L3A+XG4gICAgPGVsLXNlbGVjdC12MlxuICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgbXVsdGlwbGVcbiAgICAgIGNvbGxhcHNlLXRhZ3NcbiAgICAvPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cIm0tNFwiPlxuICAgIDxwPnVzZSBjb2xsYXBzZS10YWdzLXRvb2x0aXA8L3A+XG4gICAgPGVsLXNlbGVjdC12MlxuICAgICAgdi1tb2RlbD1cInZhbHVlMlwiXG4gICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2Ugc2VsZWN0XCJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAgIG11bHRpcGxlXG4gICAgICBjb2xsYXBzZS10YWdzXG4gICAgICBjb2xsYXBzZS10YWdzLXRvb2x0aXBcbiAgICAvPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cIm0tNFwiPlxuICAgIDxwPnVzZSBtYXgtY29sbGFwc2UtdGFnczwvcD5cbiAgICA8ZWwtc2VsZWN0LXYyXG4gICAgICB2LW1vZGVsPVwidmFsdWUzXCJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgbXVsdGlwbGVcbiAgICAgIGNvbGxhcHNlLXRhZ3NcbiAgICAgIGNvbGxhcHNlLXRhZ3MtdG9vbHRpcFxuICAgICAgOm1heC1jb2xsYXBzZS10YWdzPVwiM1wiXG4gICAgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBpbml0aWFscyA9IFsnYScsICdiJywgJ2MnLCAnZCcsICdlJywgJ2YnLCAnZycsICdoJywgJ2knLCAnaiddXG5cbmNvbnN0IHZhbHVlID0gcmVmKFtdKVxuY29uc3QgdmFsdWUyID0gcmVmKFtdKVxuY29uc3QgdmFsdWUzID0gcmVmKFtdKVxuY29uc3Qgb3B0aW9ucyA9IEFycmF5LmZyb20oeyBsZW5ndGg6IDEwMDAgfSkubWFwKChfLCBpZHgpID0+ICh7XG4gIHZhbHVlOiBgT3B0aW9uICR7aWR4ICsgMX1gLFxuICBsYWJlbDogYCR7aW5pdGlhbHNbaWR4ICUgMTBdfSR7aWR4fWAsXG59KSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/hide-extra-tags.vue)_

vue

```
<template>
  <div class="m-4">
    <p>use collapse-tags</p>
    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
      multiple
      collapse-tags
    />
  </div>
  <div class="m-4">
    <p>use collapse-tags-tooltip</p>
    <el-select-v2
      v-model="value2"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
      multiple
      collapse-tags
      collapse-tags-tooltip
    />
  </div>
  <div class="m-4">
    <p>use max-collapse-tags</p>
    <el-select-v2
      v-model="value3"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
      multiple
      collapse-tags
      collapse-tags-tooltip
      :max-collapse-tags="3"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref([])
const value2 = ref([])
const value3 = ref([])
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>
```

隐藏源代码

## 可过滤的多选 [​](#可过滤的多选)

当选项太多时，你可以使用 `filterable` 选项来启用过滤功能来找到所需的选项。

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICBmaWx0ZXJhYmxlXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICBtdWx0aXBsZVxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5pdGlhbHMgPSBbJ2EnLCAnYicsICdjJywgJ2QnLCAnZScsICdmJywgJ2cnLCAnaCcsICdpJywgJ2onXVxuXG5jb25zdCB2YWx1ZSA9IHJlZihbXSlcbmNvbnN0IG9wdGlvbnMgPSBBcnJheS5mcm9tKHsgbGVuZ3RoOiAxMDAwIH0pLm1hcCgoXywgaWR4KSA9PiAoe1xuICB2YWx1ZTogYE9wdGlvbiR7aWR4ICsgMX1gLFxuICBsYWJlbDogYCR7aW5pdGlhbHNbaWR4ICUgMTBdfSR7aWR4fWAsXG59KSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/filterable.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    filterable
    :options="options"
    placeholder="Please select"
    style="width: 240px"
    multiple
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref([])
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>
```

隐藏源代码

## 禁用选择器本身或选项 [​](#禁用选择器本身或选项)

您可以选择禁用 Select 或者 Select 中的某个选项。

Please select

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICBmaWx0ZXJhYmxlXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4OyBtYXJnaW4tcmlnaHQ6IDE2cHg7IHZlcnRpY2FsLWFsaWduOiBtaWRkbGVcIlxuICAgIG11bHRpcGxlXG4gIC8+XG4gIDxlbC1zZWxlY3QtdjJcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIGRpc2FibGVkXG4gICAgZmlsdGVyYWJsZVxuICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgcGxhY2Vob2xkZXI9XCJQbGVhc2Ugc2VsZWN0XCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweDsgdmVydGljYWwtYWxpZ246IG1pZGRsZVwiXG4gICAgbXVsdGlwbGVcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGluaXRpYWxzID0gWydhJywgJ2InLCAnYycsICdkJywgJ2UnLCAnZicsICdnJywgJ2gnLCAnaScsICdqJ11cblxuY29uc3QgdmFsdWUgPSByZWYoW10pXG5jb25zdCBvcHRpb25zID0gQXJyYXkuZnJvbSh7IGxlbmd0aDogMTAwMCB9KS5tYXAoKF8sIGlkeCkgPT4gKHtcbiAgdmFsdWU6IGBPcHRpb24ke2lkeCArIDF9YCxcbiAgbGFiZWw6IGAke2luaXRpYWxzW2lkeCAlIDEwXX0ke2lkeH1gLFxuICBkaXNhYmxlZDogaWR4ICUgMTAgPT09IDAsXG59KSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/disabled.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    filterable
    :options="options"
    placeholder="Please select"
    style="width: 240px; margin-right: 16px; vertical-align: middle"
    multiple
  />
  <el-select-v2
    v-model="value"
    disabled
    filterable
    :options="options"
    placeholder="Please select"
    style="width: 240px; vertical-align: middle"
    multiple
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref([])
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
  disabled: idx % 10 === 0,
}))
</script>
```

隐藏源代码

## 给选项进行分组 [​](#给选项进行分组)

只要数据格式满足特定要求，我们就可以按照自己的意愿为选项进行分组。

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICBmaWx0ZXJhYmxlXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICBtdWx0aXBsZVxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5pdGlhbHMgPSBbJ2EnLCAnYicsICdjJywgJ2QnLCAnZScsICdmJywgJ2cnLCAnaCcsICdpJywgJ2onXVxuXG5jb25zdCB2YWx1ZSA9IHJlZihbXSlcbmNvbnN0IG9wdGlvbnMgPSBBcnJheS5mcm9tKHsgbGVuZ3RoOiAxMCB9KS5tYXAoKF8sIGlkeCkgPT4ge1xuICBjb25zdCBsYWJlbCA9IGlkeCArIDFcbiAgcmV0dXJuIHtcbiAgICB2YWx1ZTogYEdyb3VwICR7bGFiZWx9YCxcbiAgICBsYWJlbDogYEdyb3VwICR7bGFiZWx9YCxcbiAgICBvcHRpb25zOiBBcnJheS5mcm9tKHsgbGVuZ3RoOiAxMCB9KS5tYXAoKF8sIGlkeCkgPT4gKHtcbiAgICAgIHZhbHVlOiBgT3B0aW9uICR7aWR4ICsgMSArIDEwICogbGFiZWx9YCxcbiAgICAgIGxhYmVsOiBgJHtpbml0aWFsc1tpZHggJSAxMF19JHtpZHggKyAxICsgMTAgKiBsYWJlbH1gLFxuICAgIH0pKSxcbiAgfVxufSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/grouping.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    filterable
    :options="options"
    placeholder="Please select"
    style="width: 240px"
    multiple
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref([])
const options = Array.from({ length: 10 }).map((_, idx) => {
  const label = idx + 1
  return {
    value: `Group ${label}`,
    label: `Group ${label}`,
    options: Array.from({ length: 10 }).map((_, idx) => ({
      value: `Option ${idx + 1 + 10 * label}`,
      label: `${initials[idx % 10]}${idx + 1 + 10 * label}`,
    })),
  }
})
</script>
```

隐藏源代码

## 一键清除 [​](#一键清除)

我们可以同时清除所有选定的选项。此设定也适用于单选。

Please select

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlMVwiXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4OyBtYXJnaW4tcmlnaHQ6IDE2cHg7IHZlcnRpY2FsLWFsaWduOiBtaWRkbGVcIlxuICAgIG11bHRpcGxlXG4gICAgY2xlYXJhYmxlXG4gIC8+XG4gIDxlbC1zZWxlY3QtdjJcbiAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIHNlbGVjdFwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHg7IHZlcnRpY2FsLWFsaWduOiBtaWRkbGVcIlxuICAgIGNsZWFyYWJsZVxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5pdGlhbHMgPSBbJ2EnLCAnYicsICdjJywgJ2QnLCAnZScsICdmJywgJ2cnLCAnaCcsICdpJywgJ2onXVxuXG5jb25zdCB2YWx1ZTEgPSByZWYoW10pXG5jb25zdCB2YWx1ZTIgPSByZWYoKVxuY29uc3Qgb3B0aW9ucyA9IEFycmF5LmZyb20oeyBsZW5ndGg6IDEwMDAgfSkubWFwKChfLCBpZHgpID0+ICh7XG4gIHZhbHVlOiBgT3B0aW9uICR7aWR4ICsgMX1gLFxuICBsYWJlbDogYCR7aW5pdGlhbHNbaWR4ICUgMTBdfSR7aWR4fWAsXG59KSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/clearable.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value1"
    :options="options"
    placeholder="Please select"
    style="width: 240px; margin-right: 16px; vertical-align: middle"
    multiple
    clearable
  />
  <el-select-v2
    v-model="value2"
    :options="options"
    placeholder="Please select"
    style="width: 240px; vertical-align: middle"
    clearable
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value1 = ref([])
const value2 = ref()
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>
```

隐藏源代码

## 自定义选项的渲染模板 [​](#自定义选项的渲染模板)

我们也可以通过自定义模板来渲染自己想要的选项内容。

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICBmaWx0ZXJhYmxlXG4gICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICBtdWx0aXBsZVxuICA+XG4gICAgPHRlbXBsYXRlICNkZWZhdWx0PVwieyBpdGVtIH1cIj5cbiAgICAgIDxzcGFuIHN0eWxlPVwibWFyZ2luLXJpZ2h0OiA4cHhcIj57eyBpdGVtLmxhYmVsIH19PC9zcGFuPlxuICAgICAgPHNwYW4gc3R5bGU9XCJjb2xvcjogdmFyKC0tZWwtdGV4dC1jb2xvci1zZWNvbmRhcnkpOyBmb250LXNpemU6IDEzcHhcIj5cbiAgICAgICAge3sgaXRlbS52YWx1ZSB9fVxuICAgICAgPC9zcGFuPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtc2VsZWN0LXYyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5pdGlhbHMgPSBbJ2EnLCAnYicsICdjJywgJ2QnLCAnZScsICdmJywgJ2cnLCAnaCcsICdpJywgJ2onXVxuXG5jb25zdCB2YWx1ZSA9IHJlZihbXSlcbmNvbnN0IG9wdGlvbnMgPSBBcnJheS5mcm9tKHsgbGVuZ3RoOiAxMDAwIH0pLm1hcCgoXywgaWR4KSA9PiAoe1xuICB2YWx1ZTogYE9wdGlvbiAke2lkeCArIDF9YCxcbiAgbGFiZWw6IGAke2luaXRpYWxzW2lkeCAlIDEwXX0ke2lkeH1gLFxufSkpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/customized-option.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    filterable
    :options="options"
    placeholder="Please select"
    style="width: 240px"
    multiple
  >
    <template #default="{ item }">
      <span style="margin-right: 8px">{{ item.label }}</span>
      <span style="color: var(--el-text-color-secondary); font-size: 13px">
        {{ item.value }}
      </span>
    </template>
  </el-select-v2>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref([])
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>
```

隐藏源代码

## 自定义下拉菜单的头部 2.5.2 [​](#自定义下拉菜单的头部)

您可以自定义下拉菜单的头部。

使用slot 自定义内容

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgIG11bHRpcGxlXG4gICAgY2xlYXJhYmxlXG4gICAgY29sbGFwc2UtdGFnc1xuICAgIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCJcbiAgICBwb3BwZXItY2xhc3M9XCJjdXN0b20taGVhZGVyXCJcbiAgICA6bWF4LWNvbGxhcHNlLXRhZ3M9XCIxXCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gID5cbiAgICA8dGVtcGxhdGUgI2hlYWRlcj5cbiAgICAgIDxlbC1jaGVja2JveFxuICAgICAgICB2LW1vZGVsPVwiY2hlY2tBbGxcIlxuICAgICAgICA6aW5kZXRlcm1pbmF0ZT1cImluZGV0ZXJtaW5hdGVcIlxuICAgICAgICBAY2hhbmdlPVwiaGFuZGxlQ2hlY2tBbGxcIlxuICAgICAgPlxuICAgICAgICBBbGxcbiAgICAgIDwvZWwtY2hlY2tib3g+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1zZWxlY3QtdjI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmLCB3YXRjaCB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBDaGVja2JveFZhbHVlVHlwZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgaW5pdGlhbHMgPSBbJ2EnLCAnYicsICdjJywgJ2QnLCAnZScsICdmJywgJ2cnLCAnaCcsICdpJywgJ2onXVxuY29uc3QgY2hlY2tBbGwgPSByZWYoZmFsc2UpXG5jb25zdCBpbmRldGVybWluYXRlID0gcmVmKGZhbHNlKVxuY29uc3QgdmFsdWUgPSByZWY8Q2hlY2tib3hWYWx1ZVR5cGVbXT4oW10pXG5jb25zdCBvcHRpb25zID0gcmVmKFxuICBBcnJheS5mcm9tKHsgbGVuZ3RoOiAxMDAwIH0pLm1hcCgoXywgaWR4KSA9PiAoe1xuICAgIHZhbHVlOiBgT3B0aW9uICR7aWR4ICsgMX1gLFxuICAgIGxhYmVsOiBgJHtpbml0aWFsc1tpZHggJSAxMF19JHtpZHh9YCxcbiAgfSkpXG4pXG5cbndhdGNoKHZhbHVlLCAodmFsKSA9PiB7XG4gIGlmICh2YWwubGVuZ3RoID09PSAwKSB7XG4gICAgY2hlY2tBbGwudmFsdWUgPSBmYWxzZVxuICAgIGluZGV0ZXJtaW5hdGUudmFsdWUgPSBmYWxzZVxuICB9IGVsc2UgaWYgKHZhbC5sZW5ndGggPT09IG9wdGlvbnMudmFsdWUubGVuZ3RoKSB7XG4gICAgY2hlY2tBbGwudmFsdWUgPSB0cnVlXG4gICAgaW5kZXRlcm1pbmF0ZS52YWx1ZSA9IGZhbHNlXG4gIH0gZWxzZSB7XG4gICAgaW5kZXRlcm1pbmF0ZS52YWx1ZSA9IHRydWVcbiAgfVxufSlcblxuY29uc3QgaGFuZGxlQ2hlY2tBbGwgPSAodmFsOiBDaGVja2JveFZhbHVlVHlwZSkgPT4ge1xuICBpbmRldGVybWluYXRlLnZhbHVlID0gZmFsc2VcbiAgaWYgKHZhbCkge1xuICAgIHZhbHVlLnZhbHVlID0gb3B0aW9ucy52YWx1ZS5tYXAoKF8pID0+IF8udmFsdWUpXG4gIH0gZWxzZSB7XG4gICAgdmFsdWUudmFsdWUgPSBbXVxuICB9XG59XG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLmN1c3RvbS1oZWFkZXIge1xuICAuZWwtY2hlY2tib3gge1xuICAgIGRpc3BsYXk6IGZsZXg7XG4gICAgaGVpZ2h0OiB1bnNldDtcbiAgfVxufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/custom-header.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    :options="options"
    multiple
    clearable
    collapse-tags
    placeholder="Select"
    popper-class="custom-header"
    :max-collapse-tags="1"
    style="width: 240px"
  >
    <template #header>
      <el-checkbox
        v-model="checkAll"
        :indeterminate="indeterminate"
        @change="handleCheckAll"
      >
        All
      </el-checkbox>
    </template>
  </el-select-v2>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

import type { CheckboxValueType } from 'element-plus'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
const checkAll = ref(false)
const indeterminate = ref(false)
const value = ref<CheckboxValueType[]>([])
const options = ref(
  Array.from({ length: 1000 }).map((_, idx) => ({
    value: `Option ${idx + 1}`,
    label: `${initials[idx % 10]}${idx}`,
  }))
)

watch(value, (val) => {
  if (val.length === 0) {
    checkAll.value = false
    indeterminate.value = false
  } else if (val.length === options.value.length) {
    checkAll.value = true
    indeterminate.value = false
  } else {
    indeterminate.value = true
  }
})

const handleCheckAll = (val: CheckboxValueType) => {
  indeterminate.value = false
  if (val) {
    value.value = options.value.map((_) => _.value)
  } else {
    value.value = []
  }
}
</script>

<style>
.custom-header {
  .el-checkbox {
    display: flex;
    height: unset;
  }
}
</style>
```

隐藏源代码

## 自定义下拉菜单的底部 2.5.2 [​](#自定义下拉菜单的底部)

您可以自定义下拉菜单的底部。

使用slot 自定义内容

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgcmVmPVwic2VsZWN0XCJcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgcGxhY2Vob2xkZXI9XCJTZWxlY3RcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgPlxuICAgIDx0ZW1wbGF0ZSAjZm9vdGVyPlxuICAgICAgPGVsLWJ1dHRvbiB2LWlmPVwiIWlzQWRkaW5nXCIgdGV4dCBiZyBzaXplPVwic21hbGxcIiBAY2xpY2s9XCJvbkFkZE9wdGlvblwiPlxuICAgICAgICBBZGQgYW4gb3B0aW9uXG4gICAgICA8L2VsLWJ1dHRvbj5cbiAgICAgIDxkaXYgdi1lbHNlIGNsYXNzPVwic2VsZWN0LWZvb3RlclwiPlxuICAgICAgICA8ZWwtaW5wdXRcbiAgICAgICAgICB2LW1vZGVsPVwib3B0aW9uTmFtZVwiXG4gICAgICAgICAgY2xhc3M9XCJvcHRpb24taW5wdXRcIlxuICAgICAgICAgIHBsYWNlaG9sZGVyPVwiaW5wdXQgb3B0aW9uIG5hbWVcIlxuICAgICAgICAgIHNpemU9XCJzbWFsbFwiXG4gICAgICAgIC8+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiIHNpemU9XCJzbWFsbFwiIEBjbGljaz1cIm9uQ29uZmlybVwiPlxuICAgICAgICAgICAgY29uZmlybVxuICAgICAgICAgIDwvZWwtYnV0dG9uPlxuICAgICAgICAgIDxlbC1idXR0b24gc2l6ZT1cInNtYWxsXCIgQGNsaWNrPVwiY2xlYXJcIj5jYW5jZWw8L2VsLWJ1dHRvbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLXNlbGVjdC12Mj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBuZXh0VGljaywgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IENoZWNrYm94VmFsdWVUeXBlLCBTZWxlY3RWMkluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBpbml0aWFscyA9IFsnYScsICdiJywgJ2MnLCAnZCcsICdlJywgJ2YnLCAnZycsICdoJywgJ2knLCAnaiddXG5jb25zdCBzZWxlY3QgPSByZWY8U2VsZWN0VjJJbnN0YW5jZT4oKVxuY29uc3QgaXNBZGRpbmcgPSByZWYoZmFsc2UpXG5jb25zdCB2YWx1ZSA9IHJlZjxDaGVja2JveFZhbHVlVHlwZVtdPihbXSlcbmNvbnN0IG9wdGlvbk5hbWUgPSByZWYoJycpXG5jb25zdCBvcHRpb25zID0gcmVmKFxuICBBcnJheS5mcm9tKHsgbGVuZ3RoOiAxMDAwIH0pLm1hcCgoXywgaWR4KSA9PiAoe1xuICAgIHZhbHVlOiBgT3B0aW9uICR7aWR4ICsgMX1gLFxuICAgIGxhYmVsOiBgJHtpbml0aWFsc1tpZHggJSAxMF19JHtpZHh9YCxcbiAgfSkpXG4pXG5cbmNvbnN0IG9uQWRkT3B0aW9uID0gKCkgPT4ge1xuICBpc0FkZGluZy52YWx1ZSA9IHRydWVcbn1cblxuY29uc3Qgb25Db25maXJtID0gKCkgPT4ge1xuICBpZiAob3B0aW9uTmFtZS52YWx1ZSkge1xuICAgIG9wdGlvbnMudmFsdWUucHVzaCh7XG4gICAgICBsYWJlbDogb3B0aW9uTmFtZS52YWx1ZSxcbiAgICAgIHZhbHVlOiBvcHRpb25OYW1lLnZhbHVlLFxuICAgIH0pXG4gICAgY2xlYXIoKVxuICAgIG5leHRUaWNrKCgpID0+IHtcbiAgICAgIHNlbGVjdC52YWx1ZT8uc2Nyb2xsVG8ob3B0aW9ucy52YWx1ZS5sZW5ndGggLSAxKVxuICAgIH0pXG4gIH1cbn1cblxuY29uc3QgY2xlYXIgPSAoKSA9PiB7XG4gIG9wdGlvbk5hbWUudmFsdWUgPSAnJ1xuICBpc0FkZGluZy52YWx1ZSA9IGZhbHNlXG59XG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLnNlbGVjdC1mb290ZXIge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuXG4gIC5vcHRpb24taW5wdXQge1xuICAgIHdpZHRoOiAxMDAlO1xuICAgIG1hcmdpbi1ib3R0b206IDhweDtcbiAgfVxufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/custom-footer.vue)_

vue

```
<template>
  <el-select-v2
    ref="select"
    v-model="value"
    :options="options"
    placeholder="Select"
    style="width: 240px"
  >
    <template #footer>
      <el-button v-if="!isAdding" text bg size="small" @click="onAddOption">
        Add an option
      </el-button>
      <div v-else class="select-footer">
        <el-input
          v-model="optionName"
          class="option-input"
          placeholder="input option name"
          size="small"
        />
        <div>
          <el-button type="primary" size="small" @click="onConfirm">
            confirm
          </el-button>
          <el-button size="small" @click="clear">cancel</el-button>
        </div>
      </div>
    </template>
  </el-select-v2>
</template>

<script lang="ts" setup>
import { nextTick, ref } from 'vue'

import type { CheckboxValueType, SelectV2Instance } from 'element-plus'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
const select = ref<SelectV2Instance>()
const isAdding = ref(false)
const value = ref<CheckboxValueType[]>([])
const optionName = ref('')
const options = ref(
  Array.from({ length: 1000 }).map((_, idx) => ({
    value: `Option ${idx + 1}`,
    label: `${initials[idx % 10]}${idx}`,
  }))
)

const onAddOption = () => {
  isAdding.value = true
}

const onConfirm = () => {
  if (optionName.value) {
    options.value.push({
      label: optionName.value,
      value: optionName.value,
    })
    clear()
    nextTick(() => {
      select.value?.scrollTo(options.value.length - 1)
    })
  }
}

const clear = () => {
  optionName.value = ''
  isAdding.value = false
}
</script>

<style>
.select-footer {
  display: flex;
  flex-direction: column;

  .option-input {
    width: 100%;
    margin-bottom: 8px;
  }
}
</style>
```

隐藏源代码

## 创建临时选项 [​](#创建临时选项)

创建并选中未包含在初始选项中的条目。

通过使用 `allow-create` 属性，用户可以通过输入框创建新项目。 为了使 `allow-create` 正常工作， `filterable` 的值必须为 `true`。 本例还使用了 `default-first-option` 属性， 在该属性为 `true` 的情况下，按下回车就可以选中当前选项列表中的第一个选项，无需使用鼠标或键盘方向键进行定位。

TIP

最好在使用 `allow-create` 属性的同时设置 `:reserve-keyword="false"`。

Please select

Please select

set reserve-keyword false

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwiZmxleDogYXV0b1wiPlxuICAgIDxkaXY+XG4gICAgICA8ZWwtc2VsZWN0LXYyXG4gICAgICAgIHYtbW9kZWw9XCJ2YWx1ZTFcIlxuICAgICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgICAgICBzdHlsZT1cIndpZHRoOiAyNDBweDsgbWFyZ2luLXJpZ2h0OiAxNnB4OyB2ZXJ0aWNhbC1hbGlnbjogbWlkZGxlXCJcbiAgICAgICAgYWxsb3ctY3JlYXRlXG4gICAgICAgIGRlZmF1bHQtZmlyc3Qtb3B0aW9uXG4gICAgICAgIGZpbHRlcmFibGVcbiAgICAgICAgbXVsdGlwbGVcbiAgICAgICAgY2xlYXJhYmxlXG4gICAgICAvPlxuICAgICAgPGVsLXNlbGVjdC12MlxuICAgICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2Ugc2VsZWN0XCJcbiAgICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHg7IHZlcnRpY2FsLWFsaWduOiBtaWRkbGVcIlxuICAgICAgICBhbGxvdy1jcmVhdGVcbiAgICAgICAgZGVmYXVsdC1maXJzdC1vcHRpb25cbiAgICAgICAgZmlsdGVyYWJsZVxuICAgICAgICBjbGVhcmFibGVcbiAgICAgIC8+XG4gICAgPC9kaXY+XG4gICAgPGRpdj5cbiAgICAgIDxwIHN0eWxlPVwibWFyZ2luLXRvcDogMjBweDsgbWFyZ2luLWJvdHRvbTogOHB4XCI+XG4gICAgICAgIHNldCByZXNlcnZlLWtleXdvcmQgZmFsc2VcbiAgICAgIDwvcD5cbiAgICAgIDxlbC1zZWxlY3QtdjJcbiAgICAgICAgdi1tb2RlbD1cInZhbHVlM1wiXG4gICAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIHNlbGVjdFwiXG4gICAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4OyBtYXJnaW4tcmlnaHQ6IDE2cHg7IHZlcnRpY2FsLWFsaWduOiBtaWRkbGVcIlxuICAgICAgICBhbGxvdy1jcmVhdGVcbiAgICAgICAgZGVmYXVsdC1maXJzdC1vcHRpb25cbiAgICAgICAgZmlsdGVyYWJsZVxuICAgICAgICBtdWx0aXBsZVxuICAgICAgICBjbGVhcmFibGVcbiAgICAgICAgOnJlc2VydmUta2V5d29yZD1cImZhbHNlXCJcbiAgICAgIC8+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5pdGlhbHMgPSBbJ2EnLCAnYicsICdjJywgJ2QnLCAnZScsICdmJywgJ2cnLCAnaCcsICdpJywgJ2onXVxuXG5jb25zdCB2YWx1ZTEgPSByZWYoW10pXG5jb25zdCB2YWx1ZTIgPSByZWYoKVxuY29uc3QgdmFsdWUzID0gcmVmKFtdKVxuY29uc3Qgb3B0aW9ucyA9IEFycmF5LmZyb20oeyBsZW5ndGg6IDEwMDAgfSkubWFwKChfLCBpZHgpID0+ICh7XG4gIHZhbHVlOiBgT3B0aW9uICR7aWR4ICsgMX1gLFxuICBsYWJlbDogYCR7aW5pdGlhbHNbaWR4ICUgMTBdfSR7aWR4fWAsXG59KSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/allow-create.vue)_

vue

```
<template>
  <div style="flex: auto">
    <div>
      <el-select-v2
        v-model="value1"
        :options="options"
        placeholder="Please select"
        style="width: 240px; margin-right: 16px; vertical-align: middle"
        allow-create
        default-first-option
        filterable
        multiple
        clearable
      />
      <el-select-v2
        v-model="value2"
        :options="options"
        placeholder="Please select"
        style="width: 240px; vertical-align: middle"
        allow-create
        default-first-option
        filterable
        clearable
      />
    </div>
    <div>
      <p style="margin-top: 20px; margin-bottom: 8px">
        set reserve-keyword false
      </p>
      <el-select-v2
        v-model="value3"
        :options="options"
        placeholder="Please select"
        style="width: 240px; margin-right: 16px; vertical-align: middle"
        allow-create
        default-first-option
        filterable
        multiple
        clearable
        :reserve-keyword="false"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value1 = ref([])
const value2 = ref()
const value3 = ref([])
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>
```

隐藏源代码

## 远程搜索 [​](#远程搜索)

输入关键字以从远程服务器中查找数据。

从服务器搜索数据，输入关键字进行查找。为了启用远程搜索，需要将`filterable`和`remote`设置为`true`，同时传入一个`remote-method`。 `remote-method`为一个`Function`，它会在输入值发生变化时调用，参数为当前输入值。

default

Please enter a keyword

use remote-show-suffix

Please enter a keyword

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXBcIj5cbiAgICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgICA8cD5kZWZhdWx0PC9wPlxuICAgICAgPGVsLXNlbGVjdC12MlxuICAgICAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICAgIG11bHRpcGxlXG4gICAgICAgIGZpbHRlcmFibGVcbiAgICAgICAgcmVtb3RlXG4gICAgICAgIDpyZW1vdGUtbWV0aG9kPVwicmVtb3RlTWV0aG9kXCJcbiAgICAgICAgY2xlYXJhYmxlXG4gICAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICAgIDpsb2FkaW5nPVwibG9hZGluZ1wiXG4gICAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGVudGVyIGEga2V5d29yZFwiXG4gICAgICAvPlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJtLTRcIj5cbiAgICAgIDxwPnVzZSByZW1vdGUtc2hvdy1zdWZmaXg8L3A+XG4gICAgICA8ZWwtc2VsZWN0LXYyXG4gICAgICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAgICAgbXVsdGlwbGVcbiAgICAgICAgZmlsdGVyYWJsZVxuICAgICAgICByZW1vdGVcbiAgICAgICAgOnJlbW90ZS1tZXRob2Q9XCJyZW1vdGVNZXRob2RcIlxuICAgICAgICByZW1vdGUtc2hvdy1zdWZmaXhcbiAgICAgICAgY2xlYXJhYmxlXG4gICAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICAgIDpsb2FkaW5nPVwibG9hZGluZ1wiXG4gICAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGVudGVyIGEga2V5d29yZFwiXG4gICAgICAvPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHN0YXRlcyA9IFtcbiAgJ0FsYWJhbWEnLFxuICAnQWxhc2thJyxcbiAgJ0FyaXpvbmEnLFxuICAnQXJrYW5zYXMnLFxuICAnQ2FsaWZvcm5pYScsXG4gICdDb2xvcmFkbycsXG4gICdDb25uZWN0aWN1dCcsXG4gICdEZWxhd2FyZScsXG4gICdGbG9yaWRhJyxcbiAgJ0dlb3JnaWEnLFxuICAnSGF3YWlpJyxcbiAgJ0lkYWhvJyxcbiAgJ0lsbGlub2lzJyxcbiAgJ0luZGlhbmEnLFxuICAnSW93YScsXG4gICdLYW5zYXMnLFxuICAnS2VudHVja3knLFxuICAnTG91aXNpYW5hJyxcbiAgJ01haW5lJyxcbiAgJ01hcnlsYW5kJyxcbiAgJ01hc3NhY2h1c2V0dHMnLFxuICAnTWljaGlnYW4nLFxuICAnTWlubmVzb3RhJyxcbiAgJ01pc3Npc3NpcHBpJyxcbiAgJ01pc3NvdXJpJyxcbiAgJ01vbnRhbmEnLFxuICAnTmVicmFza2EnLFxuICAnTmV2YWRhJyxcbiAgJ05ldyBIYW1wc2hpcmUnLFxuICAnTmV3IEplcnNleScsXG4gICdOZXcgTWV4aWNvJyxcbiAgJ05ldyBZb3JrJyxcbiAgJ05vcnRoIENhcm9saW5hJyxcbiAgJ05vcnRoIERha290YScsXG4gICdPaGlvJyxcbiAgJ09rbGFob21hJyxcbiAgJ09yZWdvbicsXG4gICdQZW5uc3lsdmFuaWEnLFxuICAnUmhvZGUgSXNsYW5kJyxcbiAgJ1NvdXRoIENhcm9saW5hJyxcbiAgJ1NvdXRoIERha290YScsXG4gICdUZW5uZXNzZWUnLFxuICAnVGV4YXMnLFxuICAnVXRhaCcsXG4gICdWZXJtb250JyxcbiAgJ1ZpcmdpbmlhJyxcbiAgJ1dhc2hpbmd0b24nLFxuICAnV2VzdCBWaXJnaW5pYScsXG4gICdXaXNjb25zaW4nLFxuICAnV3lvbWluZycsXG5dXG5jb25zdCBsaXN0ID0gc3RhdGVzLm1hcCgoaXRlbSk6IExpc3RJdGVtID0+IHtcbiAgcmV0dXJuIHsgdmFsdWU6IGB2YWx1ZToke2l0ZW19YCwgbGFiZWw6IGBsYWJlbDoke2l0ZW19YCB9XG59KVxuXG5pbnRlcmZhY2UgTGlzdEl0ZW0ge1xuICB2YWx1ZTogc3RyaW5nXG4gIGxhYmVsOiBzdHJpbmdcbn1cblxuY29uc3QgdmFsdWUgPSByZWYoW10pXG5jb25zdCBvcHRpb25zID0gcmVmPExpc3RJdGVtW10+KFtdKVxuY29uc3QgbG9hZGluZyA9IHJlZihmYWxzZSlcblxuY29uc3QgcmVtb3RlTWV0aG9kID0gKHF1ZXJ5OiBzdHJpbmcpID0+IHtcbiAgaWYgKHF1ZXJ5ICE9PSAnJykge1xuICAgIGxvYWRpbmcudmFsdWUgPSB0cnVlXG4gICAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICBsb2FkaW5nLnZhbHVlID0gZmFsc2VcbiAgICAgIG9wdGlvbnMudmFsdWUgPSBsaXN0LmZpbHRlcigoaXRlbSkgPT4ge1xuICAgICAgICByZXR1cm4gaXRlbS5sYWJlbC50b0xvd2VyQ2FzZSgpLmluY2x1ZGVzKHF1ZXJ5LnRvTG93ZXJDYXNlKCkpXG4gICAgICB9KVxuICAgIH0sIDIwMClcbiAgfSBlbHNlIHtcbiAgICBvcHRpb25zLnZhbHVlID0gW11cbiAgfVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/remote-search.vue)_

vue

```
<template>
  <div class="flex flex-wrap">
    <div class="m-4">
      <p>default</p>
      <el-select-v2
        v-model="value"
        style="width: 240px"
        multiple
        filterable
        remote
        :remote-method="remoteMethod"
        clearable
        :options="options"
        :loading="loading"
        placeholder="Please enter a keyword"
      />
    </div>
    <div class="m-4">
      <p>use remote-show-suffix</p>
      <el-select-v2
        v-model="value"
        style="width: 240px"
        multiple
        filterable
        remote
        :remote-method="remoteMethod"
        remote-show-suffix
        clearable
        :options="options"
        :loading="loading"
        placeholder="Please enter a keyword"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const states = [
  'Alabama',
  'Alaska',
  'Arizona',
  'Arkansas',
  'California',
  'Colorado',
  'Connecticut',
  'Delaware',
  'Florida',
  'Georgia',
  'Hawaii',
  'Idaho',
  'Illinois',
  'Indiana',
  'Iowa',
  'Kansas',
  'Kentucky',
  'Louisiana',
  'Maine',
  'Maryland',
  'Massachusetts',
  'Michigan',
  'Minnesota',
  'Mississippi',
  'Missouri',
  'Montana',
  'Nebraska',
  'Nevada',
  'New Hampshire',
  'New Jersey',
  'New Mexico',
  'New York',
  'North Carolina',
  'North Dakota',
  'Ohio',
  'Oklahoma',
  'Oregon',
  'Pennsylvania',
  'Rhode Island',
  'South Carolina',
  'South Dakota',
  'Tennessee',
  'Texas',
  'Utah',
  'Vermont',
  'Virginia',
  'Washington',
  'West Virginia',
  'Wisconsin',
  'Wyoming',
]
const list = states.map((item): ListItem => {
  return { value: `value:${item}`, label: `label:${item}` }
})

interface ListItem {
  value: string
  label: string
}

const value = ref([])
const options = ref<ListItem[]>([])
const loading = ref(false)

const remoteMethod = (query: string) => {
  if (query !== '') {
    loading.value = true
    setTimeout(() => {
      loading.value = false
      options.value = list.filter((item) => {
        return item.label.toLowerCase().includes(query.toLowerCase())
      })
    }, 200)
  } else {
    options.value = []
  }
}
</script>
```

隐藏源代码

## 使用 value-key 键属性 [​](#使用-value-key-键属性)

当 `options.value` 是一个对象时，您应该为它设置一个唯一的标识名称

TIP

在 2.4.0 之前，`value-key`既用作所选对象的唯一值，也用作`options`中表示值的对应 key。 现在 `value-key` 仅作为所选对象的唯一值使用，选项中值的 key 是 `props.value`.

a0

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIHNlbGVjdFwiXG4gICAgdmFsdWUta2V5PVwibmFtZVwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5pdGlhbHMgPSBbJ2EnLCAnYicsICdjJywgJ2QnLCAnZScsICdmJywgJ2cnLCAnaCcsICdpJywgJ2onXVxuXG5jb25zdCB2YWx1ZSA9IHJlZih7IG5hbWU6ICdPcHRpb24gMScsIHRlc3Q6ICd0ZXN0IDAnIH0pXG5jb25zdCBvcHRpb25zID0gQXJyYXkuZnJvbSh7IGxlbmd0aDogMTAwMCB9KS5tYXAoKF8sIGlkeCkgPT4gKHtcbiAgdmFsdWU6IHtcbiAgICBuYW1lOiBgT3B0aW9uICR7aWR4ICsgMX1gLFxuICAgIHRlc3Q6IGB0ZXN0ICR7aWR4ICUgM31gLFxuICB9LFxuICBsYWJlbDogYCR7aW5pdGlhbHNbaWR4ICUgMTBdfSR7aWR4fWAsXG59KSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmV4YW1wbGUtc2hvd2Nhc2UgLmVsLXNlbGVjdC12MiB7XG4gIG1hcmdpbi1yaWdodDogMjBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/use-valueKey.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    :options="options"
    placeholder="Please select"
    value-key="name"
    style="width: 240px"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref({ name: 'Option 1', test: 'test 0' })
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: {
    name: `Option ${idx + 1}`,
    test: `test ${idx % 3}`,
  },
  label: `${initials[idx % 10]}${idx}`,
}))
</script>

<style scoped>
.example-showcase .el-select-v2 {
  margin-right: 20px;
}
</style>
```

隐藏源代码

## 自定义选项 2.4.2 [​](#自定义选项)

当您的 `options` 格式不同于默认格式 您可以通过 `props` 属性自定义 `options`

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgIDpwcm9wcz1cInByb3BzXCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICBmaWx0ZXJhYmxlXG4gICAgbXVsdGlwbGVcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGluaXRpYWxzID0gWydhJywgJ2InLCAnYycsICdkJywgJ2UnLCAnZicsICdnJywgJ2gnLCAnaScsICdqJ11cbmNvbnN0IHByb3BzID0ge1xuICBsYWJlbDogJ25hbWUnLFxuICB2YWx1ZTogJ2lkJyxcbn1cbmNvbnN0IHZhbHVlID0gcmVmKFtdKVxuY29uc3Qgb3B0aW9ucyA9IEFycmF5LmZyb20oeyBsZW5ndGg6IDEwMDAgfSkubWFwKChfLCBpZHgpID0+ICh7XG4gIGlkOiBgT3B0aW9uICR7aWR4ICsgMX1gLFxuICBuYW1lOiBgJHtpbml0aWFsc1tpZHggJSAxMF19JHtpZHh9YCxcbn0pKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/props.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    :options="options"
    :props="props"
    placeholder="Please select"
    style="width: 240px"
    filterable
    multiple
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
const props = {
  label: 'name',
  value: 'id',
}
const value = ref([])
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  id: `Option ${idx + 1}`,
  name: `${initials[idx % 10]}${idx}`,
}))
</script>
```

隐藏源代码

## 自定义标签 2.5.0 [​](#自定义标签)

您可以自定义标签。

将自定义的标签插入 `el-select` 的 slot 中即可。 `collapse-tags`, `collapse-tags-tooltip`, `max-collapse-tags` 在此模式下不生效.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICBtdWx0aXBsZVxuICAgIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCJcbiAgICA6b3B0aW9ucz1cImNvbG9yc1wiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICA+XG4gICAgPHRlbXBsYXRlICNkZWZhdWx0PVwieyBpdGVtIH1cIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJmbGV4IGl0ZW1zLWNlbnRlclwiPlxuICAgICAgICA8ZWwtdGFnIDpjb2xvcj1cIml0ZW0udmFsdWVcIiBzdHlsZT1cIm1hcmdpbi1yaWdodDogOHB4XCIgc2l6ZT1cInNtYWxsXCIgLz5cbiAgICAgICAgPHNwYW4gOnN0eWxlPVwieyBjb2xvcjogaXRlbS52YWx1ZSB9XCI+e3sgaXRlbS5sYWJlbCB9fTwvc3Bhbj5cbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gICAgPHRlbXBsYXRlICN0YWc+XG4gICAgICA8ZWwtdGFnIHYtZm9yPVwiY29sb3IgaW4gdmFsdWVcIiA6a2V5PVwiY29sb3JcIiA6Y29sb3I9XCJjb2xvclwiIC8+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1zZWxlY3QtdjI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZjxzdHJpbmdbXT4oW10pXG5jb25zdCBjb2xvcnMgPSBbXG4gIHtcbiAgICB2YWx1ZTogJyNFNjM0MTUnLFxuICAgIGxhYmVsOiAncmVkJyxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnI0ZGNjYwMCcsXG4gICAgbGFiZWw6ICdvcmFuZ2UnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICcjRkZERTBBJyxcbiAgICBsYWJlbDogJ3llbGxvdycsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJyMxRUM3OUQnLFxuICAgIGxhYmVsOiAnZ3JlZW4nLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICcjMTRDQ0NDJyxcbiAgICBsYWJlbDogJ2N5YW4nLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICcjNDE2N0YwJyxcbiAgICBsYWJlbDogJ2JsdWUnLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICcjNjIyMkM5JyxcbiAgICBsYWJlbDogJ3B1cnBsZScsXG4gIH0sXG5dXG5jb2xvcnMuZm9yRWFjaCgoY29sb3IpID0+IHtcbiAgdmFsdWUudmFsdWUucHVzaChjb2xvci52YWx1ZSlcbn0pXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5lbC10YWcge1xuICBib3JkZXI6IG5vbmU7XG4gIGFzcGVjdC1yYXRpbzogMTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/custom-tag.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    multiple
    placeholder="Select"
    :options="colors"
    style="width: 240px"
  >
    <template #default="{ item }">
      <div class="flex items-center">
        <el-tag :color="item.value" style="margin-right: 8px" size="small" />
        <span :style="{ color: item.value }">{{ item.label }}</span>
      </div>
    </template>
    <template #tag>
      <el-tag v-for="color in value" :key="color" :color="color" />
    </template>
  </el-select-v2>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref<string[]>([])
const colors = [
  {
    value: '#E63415',
    label: 'red',
  },
  {
    value: '#FF6600',
    label: 'orange',
  },
  {
    value: '#FFDE0A',
    label: 'yellow',
  },
  {
    value: '#1EC79D',
    label: 'green',
  },
  {
    value: '#14CCCC',
    label: 'cyan',
  },
  {
    value: '#4167F0',
    label: 'blue',
  },
  {
    value: '#6222C9',
    label: 'purple',
  },
]
colors.forEach((color) => {
  value.value.push(color.value)
})
</script>

<style scoped>
.el-tag {
  border: none;
  aspect-ratio: 1;
}
</style>
```

隐藏源代码

## 自定义加载 2.5.2 [​](#自定义加载)

修改加载区域内容

loading icon1

Please enter a keyword

loading icon2

Please enter a keyword

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXBcIj5cbiAgICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgICA8cD5sb2FkaW5nIGljb24xPC9wPlxuICAgICAgPGVsLXNlbGVjdC12MlxuICAgICAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgICAgICBtdWx0aXBsZVxuICAgICAgICBmaWx0ZXJhYmxlXG4gICAgICAgIHJlbW90ZVxuICAgICAgICByZXNlcnZlLWtleXdvcmRcbiAgICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgZW50ZXIgYSBrZXl3b3JkXCJcbiAgICAgICAgOnJlbW90ZS1tZXRob2Q9XCJyZW1vdGVNZXRob2RcIlxuICAgICAgICA6bG9hZGluZz1cImxvYWRpbmdcIlxuICAgICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICA+XG4gICAgICAgIDx0ZW1wbGF0ZSAjbG9hZGluZz5cbiAgICAgICAgICA8c3ZnIGNsYXNzPVwiY2lyY3VsYXJcIiB2aWV3Qm94PVwiMCAwIDUwIDUwXCI+XG4gICAgICAgICAgICA8Y2lyY2xlIGNsYXNzPVwicGF0aFwiIGN4PVwiMjVcIiBjeT1cIjI1XCIgcj1cIjIwXCIgZmlsbD1cIm5vbmVcIiAvPlxuICAgICAgICAgIDwvc3ZnPlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgPC9lbC1zZWxlY3QtdjI+XG4gICAgPC9kaXY+XG4gICAgPGRpdiBjbGFzcz1cIm0tNFwiPlxuICAgICAgPHA+bG9hZGluZyBpY29uMjwvcD5cbiAgICAgIDxlbC1zZWxlY3QtdjJcbiAgICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgICAgbXVsdGlwbGVcbiAgICAgICAgZmlsdGVyYWJsZVxuICAgICAgICByZW1vdGVcbiAgICAgICAgcmVzZXJ2ZS1rZXl3b3JkXG4gICAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGVudGVyIGEga2V5d29yZFwiXG4gICAgICAgIDpyZW1vdGUtbWV0aG9kPVwicmVtb3RlTWV0aG9kXCJcbiAgICAgICAgOmxvYWRpbmc9XCJsb2FkaW5nXCJcbiAgICAgICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI2xvYWRpbmc+XG4gICAgICAgICAgPGVsLWljb24gY2xhc3M9XCJpcy1sb2FkaW5nXCI+XG4gICAgICAgICAgICA8c3ZnIGNsYXNzPVwiY2lyY3VsYXJcIiB2aWV3Qm94PVwiMCAwIDIwIDIwXCI+XG4gICAgICAgICAgICAgIDxnXG4gICAgICAgICAgICAgICAgY2xhc3M9XCJwYXRoMiBsb2FkaW5nLXBhdGhcIlxuICAgICAgICAgICAgICAgIHN0cm9rZS13aWR0aD1cIjBcIlxuICAgICAgICAgICAgICAgIHN0eWxlPVwiYW5pbWF0aW9uOiBub25lOyBzdHJva2U6IG5vbmVcIlxuICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgPGNpcmNsZSByPVwiMy4zNzVcIiBjbGFzcz1cImRvdDFcIiByeD1cIjBcIiByeT1cIjBcIiAvPlxuICAgICAgICAgICAgICAgIDxjaXJjbGUgcj1cIjMuMzc1XCIgY2xhc3M9XCJkb3QyXCIgcng9XCIwXCIgcnk9XCIwXCIgLz5cbiAgICAgICAgICAgICAgICA8Y2lyY2xlIHI9XCIzLjM3NVwiIGNsYXNzPVwiZG90NFwiIHJ4PVwiMFwiIHJ5PVwiMFwiIC8+XG4gICAgICAgICAgICAgICAgPGNpcmNsZSByPVwiMy4zNzVcIiBjbGFzcz1cImRvdDNcIiByeD1cIjBcIiByeT1cIjBcIiAvPlxuICAgICAgICAgICAgICA8L2c+XG4gICAgICAgICAgICA8L3N2Zz5cbiAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXNlbGVjdC12Mj5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgb25Nb3VudGVkLCByZWYgfSBmcm9tICd2dWUnXG5cbmludGVyZmFjZSBMaXN0SXRlbSB7XG4gIHZhbHVlOiBzdHJpbmdcbiAgbGFiZWw6IHN0cmluZ1xufVxuXG5jb25zdCBsaXN0ID0gcmVmPExpc3RJdGVtW10+KFtdKVxuY29uc3Qgb3B0aW9ucyA9IHJlZjxMaXN0SXRlbVtdPihbXSlcbmNvbnN0IHZhbHVlID0gcmVmPHN0cmluZ1tdPihbXSlcbmNvbnN0IGxvYWRpbmcgPSByZWYoZmFsc2UpXG5cbm9uTW91bnRlZCgoKSA9PiB7XG4gIGxpc3QudmFsdWUgPSBzdGF0ZXMubWFwKChpdGVtKSA9PiB7XG4gICAgcmV0dXJuIHsgdmFsdWU6IGB2YWx1ZToke2l0ZW19YCwgbGFiZWw6IGBsYWJlbDoke2l0ZW19YCB9XG4gIH0pXG59KVxuXG5jb25zdCByZW1vdGVNZXRob2QgPSAocXVlcnk6IHN0cmluZykgPT4ge1xuICBpZiAocXVlcnkpIHtcbiAgICBsb2FkaW5nLnZhbHVlID0gdHJ1ZVxuICAgIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgbG9hZGluZy52YWx1ZSA9IGZhbHNlXG4gICAgICBvcHRpb25zLnZhbHVlID0gbGlzdC52YWx1ZS5maWx0ZXIoKGl0ZW0pID0+IHtcbiAgICAgICAgcmV0dXJuIGl0ZW0ubGFiZWwudG9Mb3dlckNhc2UoKS5pbmNsdWRlcyhxdWVyeS50b0xvd2VyQ2FzZSgpKVxuICAgICAgfSlcbiAgICB9LCAzMDAwKVxuICB9IGVsc2Uge1xuICAgIG9wdGlvbnMudmFsdWUgPSBbXVxuICB9XG59XG5cbmNvbnN0IHN0YXRlcyA9IFtcbiAgJ0FsYWJhbWEnLFxuICAnQWxhc2thJyxcbiAgJ0FyaXpvbmEnLFxuICAnQXJrYW5zYXMnLFxuICAnQ2FsaWZvcm5pYScsXG4gICdDb2xvcmFkbycsXG4gICdDb25uZWN0aWN1dCcsXG4gICdEZWxhd2FyZScsXG4gICdGbG9yaWRhJyxcbiAgJ0dlb3JnaWEnLFxuICAnSGF3YWlpJyxcbiAgJ0lkYWhvJyxcbiAgJ0lsbGlub2lzJyxcbiAgJ0luZGlhbmEnLFxuICAnSW93YScsXG4gICdLYW5zYXMnLFxuICAnS2VudHVja3knLFxuICAnTG91aXNpYW5hJyxcbiAgJ01haW5lJyxcbiAgJ01hcnlsYW5kJyxcbiAgJ01hc3NhY2h1c2V0dHMnLFxuICAnTWljaGlnYW4nLFxuICAnTWlubmVzb3RhJyxcbiAgJ01pc3Npc3NpcHBpJyxcbiAgJ01pc3NvdXJpJyxcbiAgJ01vbnRhbmEnLFxuICAnTmVicmFza2EnLFxuICAnTmV2YWRhJyxcbiAgJ05ldyBIYW1wc2hpcmUnLFxuICAnTmV3IEplcnNleScsXG4gICdOZXcgTWV4aWNvJyxcbiAgJ05ldyBZb3JrJyxcbiAgJ05vcnRoIENhcm9saW5hJyxcbiAgJ05vcnRoIERha290YScsXG4gICdPaGlvJyxcbiAgJ09rbGFob21hJyxcbiAgJ09yZWdvbicsXG4gICdQZW5uc3lsdmFuaWEnLFxuICAnUmhvZGUgSXNsYW5kJyxcbiAgJ1NvdXRoIENhcm9saW5hJyxcbiAgJ1NvdXRoIERha290YScsXG4gICdUZW5uZXNzZWUnLFxuICAnVGV4YXMnLFxuICAnVXRhaCcsXG4gICdWZXJtb250JyxcbiAgJ1ZpcmdpbmlhJyxcbiAgJ1dhc2hpbmd0b24nLFxuICAnV2VzdCBWaXJnaW5pYScsXG4gICdXaXNjb25zaW4nLFxuICAnV3lvbWluZycsXG5dXG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLmVsLXNlbGVjdC1kcm9wZG93bl9fbG9hZGluZyB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGp1c3RpZnktY29udGVudDogY2VudGVyO1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBoZWlnaHQ6IDEwMHB4O1xuICBmb250LXNpemU6IDIwcHg7XG59XG5cbi5jaXJjdWxhciB7XG4gIGRpc3BsYXk6IGlubGluZTtcbiAgaGVpZ2h0OiAzMHB4O1xuICB3aWR0aDogMzBweDtcbiAgYW5pbWF0aW9uOiBsb2FkaW5nLXJvdGF0ZSAycyBsaW5lYXIgaW5maW5pdGU7XG59XG4ucGF0aCB7XG4gIGFuaW1hdGlvbjogbG9hZGluZy1kYXNoIDEuNXMgZWFzZS1pbi1vdXQgaW5maW5pdGU7XG4gIHN0cm9rZS1kYXNoYXJyYXk6IDkwLCAxNTA7XG4gIHN0cm9rZS1kYXNob2Zmc2V0OiAwO1xuICBzdHJva2Utd2lkdGg6IDI7XG4gIHN0cm9rZTogdmFyKC0tZWwtY29sb3ItcHJpbWFyeSk7XG4gIHN0cm9rZS1saW5lY2FwOiByb3VuZDtcbn1cbi5sb2FkaW5nLXBhdGggLmRvdDEge1xuICB0cmFuc2Zvcm06IHRyYW5zbGF0ZSgzLjc1cHgsIDMuNzVweCk7XG4gIGZpbGw6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xuICBhbmltYXRpb246IGN1c3RvbS1zcGluLW1vdmUgMXMgaW5maW5pdGUgbGluZWFyIGFsdGVybmF0ZTtcbiAgb3BhY2l0eTogMC4zO1xufVxuLmxvYWRpbmctcGF0aCAuZG90MiB7XG4gIHRyYW5zZm9ybTogdHJhbnNsYXRlKGNhbGMoMTAwJSAtIDMuNzVweCksIDMuNzVweCk7XG4gIGZpbGw6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xuICBhbmltYXRpb246IGN1c3RvbS1zcGluLW1vdmUgMXMgaW5maW5pdGUgbGluZWFyIGFsdGVybmF0ZTtcbiAgb3BhY2l0eTogMC4zO1xuICBhbmltYXRpb24tZGVsYXk6IDAuNHM7XG59XG4ubG9hZGluZy1wYXRoIC5kb3QzIHtcbiAgdHJhbnNmb3JtOiB0cmFuc2xhdGUoMy43NXB4LCBjYWxjKDEwMCUgLSAzLjc1cHgpKTtcbiAgZmlsbDogdmFyKC0tZWwtY29sb3ItcHJpbWFyeSk7XG4gIGFuaW1hdGlvbjogY3VzdG9tLXNwaW4tbW92ZSAxcyBpbmZpbml0ZSBsaW5lYXIgYWx0ZXJuYXRlO1xuICBvcGFjaXR5OiAwLjM7XG4gIGFuaW1hdGlvbi1kZWxheTogMS4ycztcbn1cbi5sb2FkaW5nLXBhdGggLmRvdDQge1xuICB0cmFuc2Zvcm06IHRyYW5zbGF0ZShjYWxjKDEwMCUgLSAzLjc1cHgpLCBjYWxjKDEwMCUgLSAzLjc1cHgpKTtcbiAgZmlsbDogdmFyKC0tZWwtY29sb3ItcHJpbWFyeSk7XG4gIGFuaW1hdGlvbjogY3VzdG9tLXNwaW4tbW92ZSAxcyBpbmZpbml0ZSBsaW5lYXIgYWx0ZXJuYXRlO1xuICBvcGFjaXR5OiAwLjM7XG4gIGFuaW1hdGlvbi1kZWxheTogMC44cztcbn1cbkBrZXlmcmFtZXMgbG9hZGluZy1yb3RhdGUge1xuICB0byB7XG4gICAgdHJhbnNmb3JtOiByb3RhdGUoMzYwZGVnKTtcbiAgfVxufVxuQGtleWZyYW1lcyBsb2FkaW5nLWRhc2gge1xuICAwJSB7XG4gICAgc3Ryb2tlLWRhc2hhcnJheTogMSwgMjAwO1xuICAgIHN0cm9rZS1kYXNob2Zmc2V0OiAwO1xuICB9XG4gIDUwJSB7XG4gICAgc3Ryb2tlLWRhc2hhcnJheTogOTAsIDE1MDtcbiAgICBzdHJva2UtZGFzaG9mZnNldDogLTQwcHg7XG4gIH1cbiAgMTAwJSB7XG4gICAgc3Ryb2tlLWRhc2hhcnJheTogOTAsIDE1MDtcbiAgICBzdHJva2UtZGFzaG9mZnNldDogLTEyMHB4O1xuICB9XG59XG5Aa2V5ZnJhbWVzIGN1c3RvbS1zcGluLW1vdmUge1xuICB0byB7XG4gICAgb3BhY2l0eTogMTtcbiAgfVxufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/custom-loading.vue)_

vue

```
<template>
  <div class="flex flex-wrap">
    <div class="m-4">
      <p>loading icon1</p>
      <el-select-v2
        v-model="value"
        multiple
        filterable
        remote
        reserve-keyword
        placeholder="Please enter a keyword"
        :remote-method="remoteMethod"
        :loading="loading"
        :options="options"
        style="width: 240px"
      >
        <template #loading>
          <svg class="circular" viewBox="0 0 50 50">
            <circle class="path" cx="25" cy="25" r="20" fill="none" />
          </svg>
        </template>
      </el-select-v2>
    </div>
    <div class="m-4">
      <p>loading icon2</p>
      <el-select-v2
        v-model="value"
        multiple
        filterable
        remote
        reserve-keyword
        placeholder="Please enter a keyword"
        :remote-method="remoteMethod"
        :loading="loading"
        :options="options"
        style="width: 240px"
      >
        <template #loading>
          <el-icon class="is-loading">
            <svg class="circular" viewBox="0 0 20 20">
              <g
                class="path2 loading-path"
                stroke-width="0"
                style="animation: none; stroke: none"
              >
                <circle r="3.375" class="dot1" rx="0" ry="0" />
                <circle r="3.375" class="dot2" rx="0" ry="0" />
                <circle r="3.375" class="dot4" rx="0" ry="0" />
                <circle r="3.375" class="dot3" rx="0" ry="0" />
              </g>
            </svg>
          </el-icon>
        </template>
      </el-select-v2>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'

interface ListItem {
  value: string
  label: string
}

const list = ref<ListItem[]>([])
const options = ref<ListItem[]>([])
const value = ref<string[]>([])
const loading = ref(false)

onMounted(() => {
  list.value = states.map((item) => {
    return { value: `value:${item}`, label: `label:${item}` }
  })
})

const remoteMethod = (query: string) => {
  if (query) {
    loading.value = true
    setTimeout(() => {
      loading.value = false
      options.value = list.value.filter((item) => {
        return item.label.toLowerCase().includes(query.toLowerCase())
      })
    }, 3000)
  } else {
    options.value = []
  }
}

const states = [
  'Alabama',
  'Alaska',
  'Arizona',
  'Arkansas',
  'California',
  'Colorado',
  'Connecticut',
  'Delaware',
  'Florida',
  'Georgia',
  'Hawaii',
  'Idaho',
  'Illinois',
  'Indiana',
  'Iowa',
  'Kansas',
  'Kentucky',
  'Louisiana',
  'Maine',
  'Maryland',
  'Massachusetts',
  'Michigan',
  'Minnesota',
  'Mississippi',
  'Missouri',
  'Montana',
  'Nebraska',
  'Nevada',
  'New Hampshire',
  'New Jersey',
  'New Mexico',
  'New York',
  'North Carolina',
  'North Dakota',
  'Ohio',
  'Oklahoma',
  'Oregon',
  'Pennsylvania',
  'Rhode Island',
  'South Carolina',
  'South Dakota',
  'Tennessee',
  'Texas',
  'Utah',
  'Vermont',
  'Virginia',
  'Washington',
  'West Virginia',
  'Wisconsin',
  'Wyoming',
]
</script>

<style>
.el-select-dropdown__loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  font-size: 20px;
}

.circular {
  display: inline;
  height: 30px;
  width: 30px;
  animation: loading-rotate 2s linear infinite;
}
.path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-color-primary);
  stroke-linecap: round;
}
.loading-path .dot1 {
  transform: translate(3.75px, 3.75px);
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
}
.loading-path .dot2 {
  transform: translate(calc(100% - 3.75px), 3.75px);
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 0.4s;
}
.loading-path .dot3 {
  transform: translate(3.75px, calc(100% - 3.75px));
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 1.2s;
}
.loading-path .dot4 {
  transform: translate(calc(100% - 3.75px), calc(100% - 3.75px));
  fill: var(--el-color-primary);
  animation: custom-spin-move 1s infinite linear alternate;
  opacity: 0.3;
  animation-delay: 0.8s;
}
@keyframes loading-rotate {
  to {
    transform: rotate(360deg);
  }
}
@keyframes loading-dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -40px;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -120px;
  }
}
@keyframes custom-spin-move {
  to {
    opacity: 1;
  }
}
</style>
```

隐藏源代码

## 空值配置2.7.0 [​](#空值配置)

若想配置如空字符串为有效值而不是空值，可以配置 `empty-values` 为 `[null, undefined]`.

如果您想要将清空值更改为 `null`, 请设置 `value-on-clear` 为 `null`

All

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2VsZWN0LXYyXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgIDplbXB0eS12YWx1ZXM9XCJbbnVsbCwgdW5kZWZpbmVkXVwiXG4gICAgOnZhbHVlLW9uLWNsZWFyPVwibnVsbFwiXG4gICAgY2xlYXJhYmxlXG4gICAgcGxhY2Vob2xkZXI9XCJTZWxlY3RcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICBAY2xlYXI9XCJoYW5kbGVDbGVhclwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgRWxNZXNzYWdlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZignJylcblxuY29uc3QgaW5pdGlhbHMgPSBbJ2EnLCAnYicsICdjJywgJ2QnLCAnZScsICdmJywgJ2cnLCAnaCcsICdpJywgJ2onXVxuXG5jb25zdCBvcHRpb25zID0gQXJyYXkuZnJvbSh7IGxlbmd0aDogMTAwMCB9KS5tYXAoKF8sIGlkeCkgPT4gKHtcbiAgdmFsdWU6IGBPcHRpb24gJHtpZHggKyAxfWAsXG4gIGxhYmVsOiBgJHtpbml0aWFsc1tpZHggJSAxMF19JHtpZHh9YCxcbn0pKVxuXG5vcHRpb25zLnVuc2hpZnQoe1xuICB2YWx1ZTogJycsXG4gIGxhYmVsOiAnQWxsJyxcbn0pXG5cbmNvbnN0IGhhbmRsZUNsZWFyID0gKCkgPT4ge1xuICBFbE1lc3NhZ2UuaW5mbyhgVGhlIGNsZWFyIHZhbHVlIGlzOiAke3ZhbHVlLnZhbHVlfWApXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/empty-values.vue)_

vue

```
<template>
  <el-select-v2
    v-model="value"
    :options="options"
    :empty-values="[null, undefined]"
    :value-on-clear="null"
    clearable
    placeholder="Select"
    style="width: 240px"
    @clear="handleClear"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const value = ref('')

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))

options.unshift({
  value: '',
  label: 'All',
})

const handleClear = () => {
  ElMessage.info(`The clear value is: ${value.value}`)
}
</script>
```

隐藏源代码

## 自定义标签 2.7.4 [​](#自定义标签-1)

您可以自定义标签

a0: Option 1

a0: Option 1

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTQgaXRlbXMtY2VudGVyXCI+XG4gICAgPGVsLXNlbGVjdC12MlxuICAgICAgdi1tb2RlbD1cInZhbHVlMVwiXG4gICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJTZWxlY3RcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgY2xlYXJhYmxlXG4gICAgPlxuICAgICAgPHRlbXBsYXRlICNsYWJlbD1cInsgbGFiZWwsIHZhbHVlIH1cIj5cbiAgICAgICAgPHNwYW4+e3sgbGFiZWwgfX06IDwvc3Bhbj5cbiAgICAgICAgPHNwYW4gc3R5bGU9XCJmb250LXdlaWdodDogYm9sZFwiPnt7IHZhbHVlIH19PC9zcGFuPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLXNlbGVjdC12Mj5cblxuICAgIDxlbC1zZWxlY3QtdjJcbiAgICAgIHYtbW9kZWw9XCJ2YWx1ZTJcIlxuICAgICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAgIGNsZWFyYWJsZVxuICAgICAgbXVsdGlwbGVcbiAgICA+XG4gICAgICA8dGVtcGxhdGUgI2xhYmVsPVwieyBsYWJlbCwgdmFsdWUgfVwiPlxuICAgICAgICA8c3Bhbj57eyBsYWJlbCB9fTogPC9zcGFuPlxuICAgICAgICA8c3BhbiBzdHlsZT1cImZvbnQtd2VpZ2h0OiBib2xkXCI+e3sgdmFsdWUgfX08L3NwYW4+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtc2VsZWN0LXYyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGluaXRpYWxzID0gWydhJywgJ2InLCAnYycsICdkJywgJ2UnLCAnZicsICdnJywgJ2gnLCAnaScsICdqJ11cbmNvbnN0IHZhbHVlMSA9IHJlZjxzdHJpbmc+KCdPcHRpb24gMScpXG5jb25zdCB2YWx1ZTIgPSByZWY8c3RyaW5nW10+KFsnT3B0aW9uIDEnXSlcbmNvbnN0IG9wdGlvbnMgPSBBcnJheS5mcm9tKHsgbGVuZ3RoOiAxMDAwIH0pLm1hcCgoXywgaWR4KSA9PiAoe1xuICB2YWx1ZTogYE9wdGlvbiAke2lkeCArIDF9YCxcbiAgbGFiZWw6IGAke2luaXRpYWxzW2lkeCAlIDEwXX0ke2lkeH1gLFxufSkpXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/custom-label.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-4 items-center">
    <el-select-v2
      v-model="value1"
      :options="options"
      placeholder="Select"
      style="width: 240px"
      clearable
    >
      <template #label="{ label, value }">
        <span>{{ label }}: </span>
        <span style="font-weight: bold">{{ value }}</span>
      </template>
    </el-select-v2>

    <el-select-v2
      v-model="value2"
      :options="options"
      placeholder="Select"
      style="width: 240px"
      clearable
      multiple
    >
      <template #label="{ label, value }">
        <span>{{ label }}: </span>
        <span style="font-weight: bold">{{ value }}</span>
      </template>
    </el-select-v2>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
const value1 = ref<string>('Option 1')
const value2 = ref<string[]>(['Option 1'])
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}`,
}))
</script>

<style scoped></style>
```

隐藏源代码

## 自定义宽度 2.9.2 [​](#自定义宽度)

下拉框的宽度默认根据`label`的值计算。 如果通过`default slot`自定义下拉框选项，选项中显示的文本可能与`label`的值不相等，从而导致计算错误。 在这种情况下，可以通过设置`fit-input-width`属性为一个数字来固定其宽度。

Please select

Please select

Please select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTQgaXRlbXMtY2VudGVyXCI+XG4gICAgPGVsLXNlbGVjdC12MlxuICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgOmZpdC1pbnB1dC13aWR0aD1cImZhbHNlXCJcbiAgICAvPlxuXG4gICAgPGVsLXNlbGVjdC12MlxuICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBzZWxlY3RcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgZml0LWlucHV0LXdpZHRoXG4gICAgLz5cblxuICAgIDxlbC1zZWxlY3QtdjJcbiAgICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2Ugc2VsZWN0XCJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAgIDpmaXQtaW5wdXQtd2lkdGg9XCI0NDBcIlxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjZGVmYXVsdD1cInsgaXRlbSB9XCI+XG4gICAgICAgIDxzcGFuPnt7IGl0ZW0udmFsdWUgKyBpdGVtLmxhYmVsIH19PC9zcGFuPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLXNlbGVjdC12Mj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBpbml0aWFscyA9IFsnYScsICdiJywgJ2MnLCAnZCcsICdlJywgJ2YnLCAnZycsICdoJywgJ2knLCAnaiddXG5cbmNvbnN0IHZhbHVlID0gcmVmKClcbmNvbnN0IG9wdGlvbnMgPSBBcnJheS5mcm9tKHsgbGVuZ3RoOiAxMDAwIH0pLm1hcCgoXywgaWR4KSA9PiAoe1xuICB2YWx1ZTogYE9wdGlvbiAke2lkeCArIDF9YCxcbiAgbGFiZWw6IGAke2luaXRpYWxzW2lkeCAlIDEwXX0ke2lkeH0keyctJy5yZXBlYXQoTWF0aC5jZWlsKGlkeCAvIDI1KSl9YCxcbn0pKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/select-v2/custom-width.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-4 items-center">
    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
      :fit-input-width="false"
    />

    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
      fit-input-width
    />

    <el-select-v2
      v-model="value"
      :options="options"
      placeholder="Please select"
      style="width: 240px"
      :fit-input-width="440"
    >
      <template #default="{ item }">
        <span>{{ item.value + item.label }}</span>
      </template>
    </el-select-v2>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const initials = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const value = ref()
const options = Array.from({ length: 1000 }).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: `${initials[idx % 10]}${idx}${'-'.repeat(Math.ceil(idx / 25))}`,
}))
</script>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `string` / `number` / `boolean` / `object` / `array` | — |
| options | 选项的数据源， `value` 的 key 和 `label` 可以通过 `props`自定义. | `array` | — |
| [props](#props) 2.4.2 | 配置选项，具体看下表 | `object` | — |
| multiple | 是否多选 | `boolean` | false |
| disabled | 是否禁用 | `boolean` | false |
| value-key | 作为 value 唯一标识的键名，绑定值为对象类型时必填 | `string` | value |
| size | 组件大小 | `enum` | '' |
| clearable | 是否可以清空选项 | `boolean` | false |
| clear-icon | 自定义清除图标 | `string` / `object` | CircleClose |
| collapse-tags | 多选时是否将选中值按文字的形式展示 | `boolean` | false |
| multiple-limit | 多选时可被选择的最大数目。 当被设置为0时，可被选择的数目不设限。 | `number` | 0 |
| id | 原生 input 的 id | `string` | — |
| name | 选择器的原生name属性 | `string` | — |
| effect | tooltip 主题，内置了 `dark` / `light` 两种 | `enum` / `string` | light |
| autocomplete | 自动完成选择输入 | `string` | off |
| placeholder | 占位文字 | `string` | Please select |
| filterable | Select 组件是否可筛选 | `boolean` | false |
| allow-create | 是否允许创建新条目， 当使用该属性时，`filterable`必须设置为`true` | `boolean` | false |
| filter-method | 自定义筛选方法的第一个参数是当前输入的值。 当`filterable`设置为 true 时才会生效 | `Function` | — |
| loading | 是否从远程加载数据 | `boolean` | false |
| loading-text | 从服务器加载数据时显示的文本，默认为“Loading” | `string` | — |
| reserve-keyword | 筛选时，是否在选择选项后保留关键字 | `boolean` | true |
| default-first-option | 是否在输入框按下回车时，选择第一个匹配项。 需配合 `filterable` 或 `remote` 使用 | `boolean` | false |
| no-match-text | 搜索条件无匹配时显示的文字，也可以使用 `empty` 插槽设置，默认是 “No matching data'” | `string` | — |
| no-data-text | 当在没有数据时显示的文字，你同时可以使用empty插槽进行设置。 | `string` | No Data |
| popper-class | Select 下拉菜单和标签提示的自定义类名 | `string` / `object` | '' |
| popper-style 2.11.0 | Select 下拉菜单和标签提示的自定义样式 | `string` / `object` | — |
| teleported | 是否使用 teleport。设置成 `true`则会被追加到 `append-to` 的位置 | `boolean` | true |
| append-to 2.8.8 | 下拉框挂载到哪个 DOM 元素 | `CSSSelector` / `HTMLElement` | — |
| persistent | 当下拉选择器未被激活并且`persistent`设置为`false`，选择器会被删除。 | `boolean` | true |
| popper-options | [popper.js](https://popper.js.org/docs/v2/) parameters | `object`refer to [popper.js](https://popper.js.org/docs/v2/) doc | {} |
| automatic-dropdown | 对于不可搜索的 Select，是否在输入框获得焦点后自动弹出选项菜单 | `boolean` | false |
| fit-input-width 2.9.2 | 无论下拉框的宽度是否与输入框相同，如果值为`number`，则宽度是固定的。 | `boolean` / `number` | true |
| suffix-icon 2.9.8 | 自定义后缀图标组件 | `string` / `object` | ArrowDown |
| height | 下拉菜单的高度，每一个选项为34px | `number` | 274 |
| item-height | 下拉项的高度 | `number` | 34 |
| 估计选项高度 | 控制虚拟列表大小模式：如果未定义，则列表使用来自 `item-height` 的固定项目高度；如果提供，则列表使用动态项目大小，并将此值作为估计的项目高度。 | `number` | — |
| scrollbar-always-on | 是否总是展示滚动条 | `boolean` | false |
| remote | 是否从服务器获取数据 | `boolean` | false |
| debounce 2.11.7 | 远程搜索时的防抖延迟（以毫秒为单位） | `number` | 300 |
| remote-method | 当输入值发生变化时触发的函数。 它的参数就是当前的输入值。 当`filterable`设置为 true 时才会生效 | `Function` | — |
|  | 远程搜索方法显示后缀图标 | `boolean` | false |
| validate-event | 是否触发表单验证 | `boolean` | true |
| offset 2.8.8 | 下拉面板偏移量 | `number` | 12 |
| show-arrow 2.8.8 | 下拉菜单的内容是否有箭头 | `boolean` | true |
| placement | 下拉框出现的位置 | `enum` | bottom-start |
| fallback-placements 2.5.6 | dropdown 可用的 positions 请查看[popper.js 文档](https://popper.js.org/docs/v2/modifiers/flip/#fallbackplacements) | `array` | \['bottom-start', 'top-start', 'right', 'left'\] |
| collapse-tags-tooltip 2.3.0 | 当鼠标悬停于折叠标签的文本时，是否显示所有选中的标签。 要使用此功能，`collapse-tags`的值必须为true | `boolean` | false |
| [tag-tooltip](#tag-tooltip) 2.13.3 | 折叠标签工具提示的配置对象。 要使用此项， `collapse-tags` 和 `collapse-tags-tooltip` 必须为 true | `object` | {} |
| max-collapse-tags 2.3.0 | 需要显示的 Tag 的最大数量。 只有当 `collapse-tags` 设置为 true 时才会生效。 | `number` | 1 |
| tag-type 2.5.0 | 标签类型 | `enum` | info |
| tag-effect 2.7.7 | 标签效果 | `enum` | light |
| aria-label a11y 2.5.0 | 等价于原生 input `aria-label` 属性 | `string` | — |
| empty-values 2.7.0 | 组件的空值配置， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `array` | — |
| value-on-clear 2.7.0 | 清空选项的值， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `string` / `number` / `boolean` / `Function` | — |
| popper-append-to-body deprecated | 是否将弹出框插入至 body 元素 当弹出框的位置出现问题时，你可以尝试将该属性设置为false。 |  |  |
| tabindex 2.9.0 | input 的 tabindex | `string` / `number` | — |

### props [​](#props)

| Attribute | 说明 | Type | Default |
| --- | --- | --- | --- |
| value | 指定选项的值为选项对象的某个属性值 | `string` | value |
| label | 指定节点标签为节点对象的某个属性值 | `string` | label |
| options | 指定选项的子选项为选项对象的某个属性值 | `string` | options |
| disabled | 指定选项的禁用为选项对象的某个属性值 | `string` | disabled |

### tag-tooltip 2.13.3 [​](#tag-tooltip)

备用机制

标签工具提示中的属性遵循此优先级顺序：

1.  在标签工具提示对象中明确定义的字段。
2.  从 el-select 继承的共享属性（例如 effect、popper-class、popper-style、teleported、append-to、popper-options）。
3.  底层 el-tooltip 组件的默认值。 这样，您就可以覆盖标签的特定工具提示行为，同时保持与默认的“选择”下拉菜单的一致性。

自定义容器位置

当将 Tooltip 添加到自定义容器时（通过 `append-to` 属性），应将容器配置为 `position: relative` 或 `position: absolute`，以确保准确定位。 此外，如果需要防止工具提示超出其边界，可以对容器应用 `overflow: hidden`。

| 属性 | 说明 | 类型 | Default |
| --- | --- | --- | --- |
| append-to | 指示 Tooltip 的内容将附加在哪一个网页元素上 | `CSSSelector` / `HTMLElement` | — |
| placement | Tooltip 组件出现的位置 | `enum` | bottom |
| fallback-placements | Tooltip 可用的 positions 请查看[popper.js 文档](https://popper.js.org/docs/v2/modifiers/flip/#fallbackplacements) | `array` | \['bottom', 'top', 'right', 'left'\] |
| effect | 文字提示（Tooltip）的主题，内置`dark`和`light`两种。 | `enum` / `string` | ::: |
| popper-class | 为 Tooltip 的 popper 添加自定义类名 | `string` | — |
| popper-style | 为 Tooltip 的 popper 添加自定义样式 | `string` / `object` | — |
| transition | Tooltip 所应用过渡动画的名称 | `string` | — |
| teleported | 是否使用 teleport。设置成 `true`则会被追加到 `append-to` 的位置 | `boolean` | — |
| popper-options | [popper.js](https://popper.js.org/docs/v2/) parameters | `object`refer to [popper.js](https://popper.js.org/docs/v2/) doc | — |
| show-after | 在触发后多久显示内容，单位毫秒 | `number` | — |
| hide-after | 关闭时的延迟 | `number` | — |
| auto-close | tooltip 出现后自动隐藏延时，单位毫秒 | `number` | — |
| offset | Tooltip 出现位置的偏移量 | `number` | — |

### 事件 [​](#事件)

| 名称 | 详情 | Type |
| --- | --- | --- |
| change | 当所选值更改时触发，参数是当前选中的值 | `Function` |
| visible-change | 当下拉菜单出现/消失时触发器, 当它出现时, 参数将是 `true`, 否则将是 `false` | `Function` |
| remove-tag | 当一个标签在多个模式下被移除时触发，参数将被移除标签值 | `Function` |
| clear | 可清空的单选模式下用户点击清空按钮时触发 | `Function` |
| blur | 当选择器的输入框失去焦点时触发 | `Function` |
| focus | 当选择器的输入框获得焦点时触发 | `Function` |
| end-reached 2.14.0 | 下拉滚动到结束时触发器 | `Function` |

### Slots [​](#slots)

| 名称 | 描述 | 类型 |
| --- | --- | --- |
| default | 自定义 Option 模板 | — |
| header 2.5.2 | 下拉列表顶部的内容 | — |
| footer 2.5.2 | 下拉列表底部的内容 | — |
| empty | 自定义当选项为空时的内容 | — |
| prefix | 输入框的前缀 | ::: |
| tag 2.5.0 | 作为 Select 组件的内容时，子标签 `data`、`selectDisabled` 和 `deleteTag` 是在版本 2.10.3 中新增的。 | `object` |
| loading 2.5.2 | select 组件自定义 loading内容 | ::: |
| label 2.7.4 | select 组件自定义标签内容 `index` 引入于2.11.2 | `object` |

### Exposes [​](#exposes)

| 名称 | Description | Type |
| --- | --- | --- |
| focus | 使选择器的输入框获取焦点 | `Function` |
| blur | 使选择器的输入框失去焦点，并隐藏下拉框 | `Function` |
| selectedLabel 2.8.5 | 获取当前选中的标签 | `object` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/select-v2) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/select-v2.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/select-v2.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/27912232?v=4&size=64)](https://github.com/Fuphoenixes)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/166777320?v=4&size=64)](https://github.com/ixyzorg)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/27413795?v=4&size=64)](https://github.com/SpanManX)[![](https://avatars.githubusercontent.com/u/58826012?v=4&size=64)](https://github.com/stillgg)[![](https://avatars.githubusercontent.com/u/48341368?v=4&size=64)](https://github.com/HaceraI)[![](https://avatars.githubusercontent.com/u/132551120?v=4&size=64)](https://github.com/YiMo1)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)[![](https://avatars.githubusercontent.com/u/58846658?v=4&size=64)](https://github.com/JiuRanYa)[![](https://avatars.githubusercontent.com/u/26833520?v=4&size=64)](https://github.com/josonho)[![](https://avatars.githubusercontent.com/u/178066799?v=4&size=64)](https://github.com/Yeuvoir)[![](https://avatars.githubusercontent.com/u/37976544?v=4&size=64)](https://github.com/ALypovskyi)[![](https://avatars.githubusercontent.com/u/24487727?v=4&size=64)](https://github.com/LostElkByte)[![](https://avatars.githubusercontent.com/u/201188047?v=4&size=64)](https://github.com/YXY-cell)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/52928534?v=4&size=64)](https://github.com/alonely-boy)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/127940123?v=4&size=64)](https://github.com/baozjj)[![](https://avatars.githubusercontent.com/u/14144811?v=4&size=64)](https://github.com/cn-xufei)[![](https://avatars.githubusercontent.com/u/50254496?v=4&size=64)](https://github.com/LoTwT)[![](https://avatars.githubusercontent.com/u/35138018?v=4&size=64)](https://github.com/tuskermanshu)[![](https://avatars.githubusercontent.com/u/40554198?v=4&size=64)](https://github.com/WangYJEE)[![](https://avatars.githubusercontent.com/u/28584349?v=4&size=64)](https://github.com/wangcch)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/25458528?v=4&size=64)](https://github.com/weidehai)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/23378455?v=4&size=64)](https://github.com/Dreamcreative)[![](https://avatars.githubusercontent.com/u/81673017?v=4&size=64)](https://github.com/RSS1102)[![](https://avatars.githubusercontent.com/u/22659150?v=4&size=64)](https://github.com/ntnyq)[![](https://avatars.githubusercontent.com/u/8591261?v=4&size=64)](https://github.com/zeyongTsai)[![](https://avatars.githubusercontent.com/u/57179957?v=4&size=64)](https://github.com/yeonjulee1005)[![](https://avatars.githubusercontent.com/u/31885971?v=4&size=64)](https://github.com/wonderl17)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/33799081?v=4&size=64)](https://github.com/wuyadan)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/60056876?v=4&size=64)](https://github.com/LinZhanMing)[![](https://avatars.githubusercontent.com/u/13913084?v=4&size=64)](https://github.com/YornQiu)[![](https://avatars.githubusercontent.com/u/1183991?v=4&size=64)](https://github.com/calumk)[![](https://avatars.githubusercontent.com/u/19553651?v=4&size=64)](https://github.com/GUEThe)[![](https://avatars.githubusercontent.com/u/67454874?v=4&size=64)](https://github.com/nigiwen)[![](https://avatars.githubusercontent.com/u/69580637?v=4&size=64)](https://github.com/jevin98)[![](https://avatars.githubusercontent.com/u/26295849?v=4&size=64)](https://github.com/CeceWall)[![](https://avatars.githubusercontent.com/u/5701072?v=4&size=64)](https://github.com/Naeemo)[![](https://avatars.githubusercontent.com/u/16463481?v=4&size=64)](https://github.com/hellomrbigshot)[![](https://avatars.githubusercontent.com/u/61337085?v=4&size=64)](https://github.com/wizardAEI)[![](https://avatars.githubusercontent.com/u/5389932?v=4&size=64)](https://github.com/muuyao)[![](https://avatars.githubusercontent.com/u/73569598?v=4&size=64)](https://github.com/sechi747)[![](https://avatars.githubusercontent.com/u/12935577?v=4&size=64)](https://github.com/lshunran)[![](https://avatars.githubusercontent.com/u/73086438?v=4&size=64)](https://github.com/Cheerwhy)[![](https://avatars.githubusercontent.com/u/32354856?v=4&size=64)](https://github.com/baiwusanyu-c)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/1411614?v=4&size=64)](https://github.com/spx443812507)

[Select](https://element-plus.org/zh-CN/component/select)

[Slider 滑块](https://element-plus.org/zh-CN/component/slider)


