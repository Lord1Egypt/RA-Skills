---
name: "switch"
description: "Switch 开关 -- Element Plus Vue3 桌面端组件。Invoke when user needs Switch 开关 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/switch.html"
---

---

# Switch 开关 [​](#switch-开关)

更新日志待解决

6

表示两种相互对立的状态间的切换，多用于触发「开/关」。

## 基础用法 [​](#基础用法)

绑定 `v-model` 到一个 `Boolean` 类型的变量。 可以使用 `--el-switch-on-color` 属性与 `--el-switch-off-color` 属性来设置开关的背景色。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoIHYtbW9kZWw9XCJ2YWx1ZTFcIiAvPlxuICA8ZWwtc3dpdGNoXG4gICAgdi1tb2RlbD1cInZhbHVlMlwiXG4gICAgY2xhc3M9XCJtbC0yXCJcbiAgICBzdHlsZT1cIi0tZWwtc3dpdGNoLW9uLWNvbG9yOiAjMTNjZTY2OyAtLWVsLXN3aXRjaC1vZmYtY29sb3I6ICNmZjQ5NDlcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKHRydWUpXG5jb25zdCB2YWx1ZTIgPSByZWYodHJ1ZSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/switch/basic.vue)_

vue

```
<template>
  <el-switch v-model="value1" />
  <el-switch
    v-model="value2"
    class="ml-2"
    style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(true)
const value2 = ref(true)
</script>
```

隐藏源代码

## 尺寸 [​](#尺寸)

CloseOpen

CloseOpen

CloseOpen

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoXG4gICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICBzaXplPVwibGFyZ2VcIlxuICAgIGFjdGl2ZS10ZXh0PVwiT3BlblwiXG4gICAgaW5hY3RpdmUtdGV4dD1cIkNsb3NlXCJcbiAgLz5cbiAgPGJyIC8+XG4gIDxlbC1zd2l0Y2ggdi1tb2RlbD1cInZhbHVlXCIgYWN0aXZlLXRleHQ9XCJPcGVuXCIgaW5hY3RpdmUtdGV4dD1cIkNsb3NlXCIgLz5cbiAgPGJyIC8+XG4gIDxlbC1zd2l0Y2hcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIHNpemU9XCJzbWFsbFwiXG4gICAgYWN0aXZlLXRleHQ9XCJPcGVuXCJcbiAgICBpbmFjdGl2ZS10ZXh0PVwiQ2xvc2VcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYodHJ1ZSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/switch/sizes.vue)_

vue

```
<template>
  <el-switch
    v-model="value"
    size="large"
    active-text="Open"
    inactive-text="Close"
  />
  <br />
  <el-switch v-model="value" active-text="Open" inactive-text="Close" />
  <br />
  <el-switch
    v-model="value"
    size="small"
    active-text="Open"
    inactive-text="Close"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref(true)
</script>
```

隐藏源代码

## 文字描述 [​](#文字描述)

使用`active-text`属性与`inactive-text`属性来设置开关的文字描述。 使用 `inline-prompt` 属性来控制文本是否显示在点内。

使用`active-text`属性与`inactive-text`属性来设置开关的文字描述。

Pay by yearPay by month

Pay by yearPay by month

是

Y

超出省略

完整展示多个内容

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoXG4gICAgdi1tb2RlbD1cInZhbHVlMVwiXG4gICAgY2xhc3M9XCJtYi0yXCJcbiAgICBhY3RpdmUtdGV4dD1cIlBheSBieSBtb250aFwiXG4gICAgaW5hY3RpdmUtdGV4dD1cIlBheSBieSB5ZWFyXCJcbiAgLz5cbiAgPGJyIC8+XG4gIDxlbC1zd2l0Y2hcbiAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICBjbGFzcz1cIm1iLTJcIlxuICAgIHN0eWxlPVwiLS1lbC1zd2l0Y2gtb24tY29sb3I6ICMxM2NlNjY7IC0tZWwtc3dpdGNoLW9mZi1jb2xvcjogI2ZmNDk0OVwiXG4gICAgYWN0aXZlLXRleHQ9XCJQYXkgYnkgbW9udGhcIlxuICAgIGluYWN0aXZlLXRleHQ9XCJQYXkgYnkgeWVhclwiXG4gIC8+XG4gIDxiciAvPlxuICA8ZWwtc3dpdGNoXG4gICAgdi1tb2RlbD1cInZhbHVlM1wiXG4gICAgaW5saW5lLXByb21wdFxuICAgIGFjdGl2ZS10ZXh0PVwi5pivXCJcbiAgICBpbmFjdGl2ZS10ZXh0PVwi5ZCmXCJcbiAgLz5cbiAgPGVsLXN3aXRjaFxuICAgIHYtbW9kZWw9XCJ2YWx1ZTRcIlxuICAgIGNsYXNzPVwibWwtMlwiXG4gICAgaW5saW5lLXByb21wdFxuICAgIHN0eWxlPVwiLS1lbC1zd2l0Y2gtb24tY29sb3I6ICMxM2NlNjY7IC0tZWwtc3dpdGNoLW9mZi1jb2xvcjogI2ZmNDk0OVwiXG4gICAgYWN0aXZlLXRleHQ9XCJZXCJcbiAgICBpbmFjdGl2ZS10ZXh0PVwiTlwiXG4gIC8+XG4gIDxlbC1zd2l0Y2hcbiAgICB2LW1vZGVsPVwidmFsdWU2XCJcbiAgICBjbGFzcz1cIm1sLTJcIlxuICAgIHdpZHRoPVwiNjBcIlxuICAgIGlubGluZS1wcm9tcHRcbiAgICBhY3RpdmUtdGV4dD1cIui2heWHuuecgeeVpVwiXG4gICAgaW5hY3RpdmUtdGV4dD1cIui2heWHuuecgeeVpVwiXG4gIC8+XG4gIDxlbC1zd2l0Y2hcbiAgICB2LW1vZGVsPVwidmFsdWU1XCJcbiAgICBjbGFzcz1cIm1sLTJcIlxuICAgIGlubGluZS1wcm9tcHRcbiAgICBzdHlsZT1cIi0tZWwtc3dpdGNoLW9uLWNvbG9yOiAjMTNjZTY2OyAtLWVsLXN3aXRjaC1vZmYtY29sb3I6ICNmZjQ5NDlcIlxuICAgIGFjdGl2ZS10ZXh0PVwi5a6M5pW05bGV56S65aSa5Liq5YaF5a65XCJcbiAgICBpbmFjdGl2ZS10ZXh0PVwi5aSa5Liq5YaF5a65XCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlMSA9IHJlZih0cnVlKVxuY29uc3QgdmFsdWUyID0gcmVmKHRydWUpXG5jb25zdCB2YWx1ZTMgPSByZWYodHJ1ZSlcbmNvbnN0IHZhbHVlNCA9IHJlZih0cnVlKVxuY29uc3QgdmFsdWU1ID0gcmVmKHRydWUpXG5jb25zdCB2YWx1ZTYgPSByZWYodHJ1ZSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/switch/text-description.vue)_

vue

```
<template>
  <el-switch
    v-model="value1"
    class="mb-2"
    active-text="Pay by month"
    inactive-text="Pay by year"
  />
  <br />
  <el-switch
    v-model="value2"
    class="mb-2"
    style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
    active-text="Pay by month"
    inactive-text="Pay by year"
  />
  <br />
  <el-switch
    v-model="value3"
    inline-prompt
    active-text="是"
    inactive-text="否"
  />
  <el-switch
    v-model="value4"
    class="ml-2"
    inline-prompt
    style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
    active-text="Y"
    inactive-text="N"
  />
  <el-switch
    v-model="value6"
    class="ml-2"
    width="60"
    inline-prompt
    active-text="超出省略"
    inactive-text="超出省略"
  />
  <el-switch
    v-model="value5"
    class="ml-2"
    inline-prompt
    style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
    active-text="完整展示多个内容"
    inactive-text="多个内容"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(true)
const value2 = ref(true)
const value3 = ref(true)
const value4 = ref(true)
const value5 = ref(true)
const value6 = ref(true)
</script>
```

隐藏源代码

## 显示自定义图标 [​](#显示自定义图标)

TIP

使用 `inactive-icon` 和 `active-icon` 属性来添加图标。 您可以传递组件名称的字符串（提前注册）或组件本身是一个 SVG Vue 组件。 Element Plus 提供了一套图标，你可以在 [icon](https://element-plus.org/zh-CN/component/icon) 找到它们。

使用 `inactive-icon` 和 `active-icon` 属性来添加图标。 使用 `inline-prompt` 属性来控制图标显示在点内。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoIHYtbW9kZWw9XCJ2YWx1ZTFcIiA6YWN0aXZlLWljb249XCJDaGVja1wiIDppbmFjdGl2ZS1pY29uPVwiQ2xvc2VcIiAvPlxuICA8YnIgLz5cbiAgPGVsLXN3aXRjaFxuICAgIHYtbW9kZWw9XCJ2YWx1ZTJcIlxuICAgIGNsYXNzPVwibXQtMlwiXG4gICAgc3R5bGU9XCJtYXJnaW4tbGVmdDogMjRweFwiXG4gICAgaW5saW5lLXByb21wdFxuICAgIDphY3RpdmUtaWNvbj1cIkNoZWNrXCJcbiAgICA6aW5hY3RpdmUtaWNvbj1cIkNsb3NlXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBDaGVjaywgQ2xvc2UgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKHRydWUpXG5jb25zdCB2YWx1ZTIgPSByZWYodHJ1ZSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/switch/custom-icons.vue)_

vue

```
<template>
  <el-switch v-model="value1" :active-icon="Check" :inactive-icon="Close" />
  <br />
  <el-switch
    v-model="value2"
    class="mt-2"
    style="margin-left: 24px"
    inline-prompt
    :active-icon="Check"
    :inactive-icon="Close"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Check, Close } from '@element-plus/icons-vue'

const value1 = ref(true)
const value2 = ref(true)
</script>
```

隐藏源代码

## 扩展的 value 类型 [​](#扩展的-value-类型)

你可以设置 `active-value` 和 `inactive-value` 属性， 它们接受 `Boolean`、`String` 或 `Number` 类型的值。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdG9vbHRpcCA6Y29udGVudD1cIidTd2l0Y2ggdmFsdWU6ICcgKyB2YWx1ZVwiIHBsYWNlbWVudD1cInRvcFwiPlxuICAgIDxlbC1zd2l0Y2hcbiAgICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgICBzdHlsZT1cIi0tZWwtc3dpdGNoLW9uLWNvbG9yOiAjMTNjZTY2OyAtLWVsLXN3aXRjaC1vZmYtY29sb3I6ICNmZjQ5NDlcIlxuICAgICAgYWN0aXZlLXZhbHVlPVwiMTAwXCJcbiAgICAgIGluYWN0aXZlLXZhbHVlPVwiMFwiXG4gICAgLz5cbiAgPC9lbC10b29sdGlwPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoJzEwMCcpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/switch/extended-value-types.vue)_

vue

```
<template>
  <el-tooltip :content="'Switch value: ' + value" placement="top">
    <el-switch
      v-model="value"
      style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
      active-value="100"
      inactive-value="0"
    />
  </el-tooltip>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('100')
</script>
```

隐藏源代码

## 禁用状态 [​](#禁用状态)

设置`disabled`属性，接受一个`Boolean`，设置`true`即可禁用。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoIHYtbW9kZWw9XCJ2YWx1ZTFcIiBkaXNhYmxlZCAvPlxuICA8ZWwtc3dpdGNoIHYtbW9kZWw9XCJ2YWx1ZTJcIiBjbGFzcz1cIm1sLTJcIiAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKHRydWUpXG5jb25zdCB2YWx1ZTIgPSByZWYodHJ1ZSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/switch/disabled.vue)_

vue

```
<template>
  <el-switch v-model="value1" disabled />
  <el-switch v-model="value2" class="ml-2" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(true)
const value2 = ref(true)
</script>
```

隐藏源代码

## 加载状态 [​](#加载状态)

设置`loading`属性，接受一个`Boolean`，设置`true`即加载中状态。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoIHYtbW9kZWw9XCJ2YWx1ZTFcIiBsb2FkaW5nIC8+XG4gIDxlbC1zd2l0Y2ggdi1tb2RlbD1cInZhbHVlMlwiIGxvYWRpbmcgY2xhc3M9XCJtbC0yXCIgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlMSA9IHJlZih0cnVlKVxuY29uc3QgdmFsdWUyID0gcmVmKGZhbHNlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/switch/loading.vue)_

vue

```
<template>
  <el-switch v-model="value1" loading />
  <el-switch v-model="value2" loading class="ml-2" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(true)
const value2 = ref(false)
</script>
```

隐藏源代码

## 阻止切换 [​](#阻止切换)

设置`beforeChange`属性，若返回 false 或者返回 Promise 且被 reject，则停止切换。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoXG4gICAgdi1tb2RlbD1cInZhbHVlMVwiXG4gICAgOmxvYWRpbmc9XCJsb2FkaW5nMVwiXG4gICAgOmJlZm9yZS1jaGFuZ2U9XCJiZWZvcmVDaGFuZ2UxXCJcbiAgLz5cbiAgPGVsLXN3aXRjaFxuICAgIHYtbW9kZWw9XCJ2YWx1ZTJcIlxuICAgIGNsYXNzPVwibWwtMlwiXG4gICAgOmxvYWRpbmc9XCJsb2FkaW5nMlwiXG4gICAgOmJlZm9yZS1jaGFuZ2U9XCJiZWZvcmVDaGFuZ2UyXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBFbE1lc3NhZ2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHZhbHVlMSA9IHJlZihmYWxzZSlcbmNvbnN0IHZhbHVlMiA9IHJlZihmYWxzZSlcbmNvbnN0IGxvYWRpbmcxID0gcmVmKGZhbHNlKVxuY29uc3QgbG9hZGluZzIgPSByZWYoZmFsc2UpXG5cbmNvbnN0IGJlZm9yZUNoYW5nZTEgPSAoKTogUHJvbWlzZTxib29sZWFuPiA9PiB7XG4gIGxvYWRpbmcxLnZhbHVlID0gdHJ1ZVxuICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUpID0+IHtcbiAgICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgIGxvYWRpbmcxLnZhbHVlID0gZmFsc2VcbiAgICAgIEVsTWVzc2FnZS5zdWNjZXNzKCdTd2l0Y2ggc3VjY2VzcycpXG4gICAgICByZXR1cm4gcmVzb2x2ZSh0cnVlKVxuICAgIH0sIDEwMDApXG4gIH0pXG59XG5cbmNvbnN0IGJlZm9yZUNoYW5nZTIgPSAoKTogUHJvbWlzZTxib29sZWFuPiA9PiB7XG4gIGxvYWRpbmcyLnZhbHVlID0gdHJ1ZVxuICByZXR1cm4gbmV3IFByb21pc2UoKF8sIHJlamVjdCkgPT4ge1xuICAgIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgbG9hZGluZzIudmFsdWUgPSBmYWxzZVxuICAgICAgRWxNZXNzYWdlLmVycm9yKCdTd2l0Y2ggZmFpbGVkJylcbiAgICAgIHJldHVybiByZWplY3QobmV3IEVycm9yKCdFcnJvcicpKVxuICAgIH0sIDEwMDApXG4gIH0pXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/switch/prevent-switching.vue)_

vue

```
<template>
  <el-switch
    v-model="value1"
    :loading="loading1"
    :before-change="beforeChange1"
  />
  <el-switch
    v-model="value2"
    class="ml-2"
    :loading="loading2"
    :before-change="beforeChange2"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const value1 = ref(false)
const value2 = ref(false)
const loading1 = ref(false)
const loading2 = ref(false)

const beforeChange1 = (): Promise<boolean> => {
  loading1.value = true
  return new Promise((resolve) => {
    setTimeout(() => {
      loading1.value = false
      ElMessage.success('Switch success')
      return resolve(true)
    }, 1000)
  })
}

const beforeChange2 = (): Promise<boolean> => {
  loading2.value = true
  return new Promise((_, reject) => {
    setTimeout(() => {
      loading2.value = false
      ElMessage.error('Switch failed')
      return reject(new Error('Error'))
    }, 1000)
  })
}
</script>
```

隐藏源代码

## 自定义动作图标 2.3.9 [​](#自定义动作图标)

使用 `inactive-action-icon` 和 `active-action-icon` 属性来添加图标。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoXG4gICAgdi1tb2RlbD1cInZhbHVlMVwiXG4gICAgOmFjdGl2ZS1hY3Rpb24taWNvbj1cIlZpZXdcIlxuICAgIDppbmFjdGl2ZS1hY3Rpb24taWNvbj1cIkhpZGVcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEhpZGUsIFZpZXcgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKHRydWUpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/switch/custom-action-icon.vue)_

vue

```
<template>
  <el-switch
    v-model="value1"
    :active-action-icon="View"
    :inactive-action-icon="Hide"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Hide, View } from '@element-plus/icons-vue'

const value1 = ref(true)
</script>
```

隐藏源代码

## 自定义操作图标 2.4.4 [​](#自定义操作图标)

使用 `active-action` 和 `inactive-action` 属性来添加图标。

T

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3dpdGNoIHYtbW9kZWw9XCJ2YWx1ZTFcIj5cbiAgICA8dGVtcGxhdGUgI2FjdGl2ZS1hY3Rpb24+XG4gICAgICA8c3BhbiBjbGFzcz1cImN1c3RvbS1hY3RpdmUtYWN0aW9uXCI+VDwvc3Bhbj5cbiAgICA8L3RlbXBsYXRlPlxuICAgIDx0ZW1wbGF0ZSAjaW5hY3RpdmUtYWN0aW9uPlxuICAgICAgPHNwYW4gY2xhc3M9XCJjdXN0b20taW5hY3RpdmUtYWN0aW9uXCI+Rjwvc3Bhbj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLXN3aXRjaD5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlMSA9IHJlZih0cnVlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/switch/custom-action-slot.vue)_

vue

```
<template>
  <el-switch v-model="value1">
    <template #active-action>
      <span class="custom-active-action">T</span>
    </template>
    <template #inactive-action>
      <span class="custom-inactive-action">F</span>
    </template>
  </el-switch>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value1 = ref(true)
</script>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | Default |
| --- | --- | --- | --- |
| model-value / v-model | 绑定值，必须等于 `active-value` 或 `inactive-value`，默认为 `Boolean` 类型 | `boolean` / `string` / `number` | false |
| disabled | 是否禁用 | `boolean` | false |
| loading | 是否显示加载中 | `boolean` | false |
| size | switch 的大小 | `enum` | '' |
| width | switch 的宽度 | `number` / `string` | '' |
| inline-prompt | 无论图标或文本是否显示在点内，只会呈现文本的第一个字符 | `boolean` | false |
| active-icon | switch 状态为 `on` 时所显示图标，设置此项会忽略 `active-text` | `string` / `Component` | — |
| inactive-icon | switch 状态为 `off` 时所显示图标，设置此项会忽略 `inactive-text` | `string` / `Component` | — |
| active-action-icon 2.3.9 | `on`状态下显示的图标组件 | `string` / `Component` | — |
| inactive-action-icon 2.3.9 | `off`状态下显示的图标组件 | `string` / `Component` | — |
| active-text | switch 打开时的文字描述 | `string` | '' |
| inactive-text | switch 的状态为 `off` 时的文字描述 | `string` | '' |
| active-value | switch 状态为 `on` 时的值 | `boolean` / `string` / `number` | true |
| inactive-value | switch的状态为 `off` 时的值 | `boolean` / `string` / `number` | false |
| name | switch 对应的 name 属性 | `string` | '' |
| validate-event | 是否触发表单验证 | `boolean` | true |
| before-change | switch 状态改变前的钩子， 返回 `false` 或者返回 `Promise` 且被 reject 则停止切换 | `Function` | — |
| id | input 的 id | `string` | — |
| tabindex | input 的 tabindex | `string` / `number` | — |
| aria-label a11y 2.7.2 | 等价于原生 input `aria-label` 属性 | `string` | — |
| active-color deprecated | 当在 `on` 状态时的背景颜色(推荐使用 CSS var `--el-switch-on-color` ) | `string` | '' |
| inactive-color deprecated | `off` 状态时的背景颜色(推荐使用 CSS var `--el-switch-off-color` ) | `string` | '' |
| border-color deprecated | 开关的边框颜色 ( 推荐使用 CSS var `--el-switch-border-color` ) | `string` | '' |
| label a11y deprecated | 等价于原生 input `aria-label` 属性 | `string` | — |

### 事件 [​](#事件)

| 事件名 | 说明 | Type |
| --- | --- | --- |
| change | switch 状态发生变化时的回调函数 | `Function` |

### Switch Slots [​](#switch-slots)

| 名称 | 说明 |
| --- | --- |
| active-action 2.4.4 | 自定义 active 行为 |
| inactive-action 2.4.4 | 自定义 inactive 行为 |
| active 2.13.0 | 自定义 on 状态的内容 |
| inactive 2.13.0 | 自定义 off 状态的内容 |

### Exposes [​](#exposes)

| 方法 | 详情 | Type |
| --- | --- | --- |
| focus | 手动 focus 到 switch 组件 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/switch) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/switch.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/switch.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/62818957?v=4&size=64)](https://github.com/ZacharyBear)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/74746021?v=4&size=64)](https://github.com/xing403)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/57086651?v=4&size=64)](https://github.com/Simon-He95)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/26833520?v=4&size=64)](https://github.com/josonho)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/22695767?v=4&size=64)](https://github.com/deepthan)[![](https://avatars.githubusercontent.com/u/36007710?v=4&size=64)](https://github.com/sleepyfive)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/23232655?v=4&size=64)](https://github.com/MBearo)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/57524062?v=4&size=64)](https://github.com/Ther-su)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)

[Slider 滑块](https://element-plus.org/zh-CN/component/slider)

[Time Picker 时间选择器](https://element-plus.org/zh-CN/component/time-picker)


