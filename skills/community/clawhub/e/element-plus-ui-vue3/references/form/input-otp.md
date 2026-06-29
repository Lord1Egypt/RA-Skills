---
name: "input-otp"
description: "Input OTP -- Element Plus Vue3 桌面端组件。Invoke when user needs Input OTP in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/input-otp.html"
---

---

# InputOtp 一次性密码输入框 beta [​](#inputotp-一次性密码输入框)

更新日志待解决

0

用于输入一次性密码

## 基础用法 [​](#基础用法)

Value: 123

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1pbnB1dC1vdHAgdi1tb2RlbD1cIm90cFwiIC8+XG4gICAgPGRpdiBzdHlsZT1cIm1hcmdpbi10b3A6IDIwcHhcIj5WYWx1ZToge3sgb3RwIH19PC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3Qgb3RwID0gcmVmKCcxMjMnKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-otp/basic.vue)_

vue

```
<template>
  <div>
    <el-input-otp v-model="otp" />
    <div style="margin-top: 20px">Value: {{ otp }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp = ref('123')
</script>
```

隐藏源代码

## 自定义长度 [​](#自定义长度)

输入字段长度可以通过设置`length`属性来自定义。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbnB1dC1vdHBcIj5cbiAgICA8ZWwtaW5wdXQtb3RwIHYtbW9kZWw9XCJvdHAxXCIgOmxlbmd0aD1cIjRcIiAvPlxuICAgIDxlbC1pbnB1dC1vdHAgdi1tb2RlbD1cIm90cDJcIiA6bGVuZ3RoPVwiOFwiIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3Qgb3RwMSA9IHJlZignJylcbmNvbnN0IG90cDIgPSByZWYoJycpXG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5kZW1vLWlucHV0LW90cCB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XG4gIGdhcDogMjBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-otp/custom-length.vue)_

vue

```
<template>
  <div class="demo-input-otp">
    <el-input-otp v-model="otp1" :length="4" />
    <el-input-otp v-model="otp2" :length="8" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp1 = ref('')
const otp2 = ref('')
</script>

<style scoped>
.demo-input-otp {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
```

隐藏源代码

## 展示类型 [​](#展示类型)

有三种类型可用：`outlined` （默认）、`filled` 和 `underlined`。

Outlined (Default)

Filled

Underlined

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbnB1dC1vdHBcIj5cbiAgICA8ZGl2PlxuICAgICAgPHA+T3V0bGluZWQgKERlZmF1bHQpPC9wPlxuICAgICAgPGVsLWlucHV0LW90cCB2LW1vZGVsPVwib3RwMVwiIHR5cGU9XCJvdXRsaW5lZFwiIC8+XG4gICAgPC9kaXY+XG4gICAgPGRpdj5cbiAgICAgIDxwPkZpbGxlZDwvcD5cbiAgICAgIDxlbC1pbnB1dC1vdHAgdi1tb2RlbD1cIm90cDJcIiB0eXBlPVwiZmlsbGVkXCIgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2PlxuICAgICAgPHA+VW5kZXJsaW5lZDwvcD5cbiAgICAgIDxlbC1pbnB1dC1vdHAgdi1tb2RlbD1cIm90cDNcIiB0eXBlPVwidW5kZXJsaW5lZFwiIC8+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3Qgb3RwMSA9IHJlZignJylcbmNvbnN0IG90cDIgPSByZWYoJycpXG5jb25zdCBvdHAzID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1pbnB1dC1vdHAge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBnYXA6IDIwcHg7XG59XG5cbnAge1xuICBtYXJnaW4tYm90dG9tOiA4cHg7XG4gIGZvbnQtc2l6ZTogMTRweDtcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-otp/types.vue)_

vue

```
<template>
  <div class="demo-input-otp">
    <div>
      <p>Outlined (Default)</p>
      <el-input-otp v-model="otp1" type="outlined" />
    </div>
    <div>
      <p>Filled</p>
      <el-input-otp v-model="otp2" type="filled" />
    </div>
    <div>
      <p>Underlined</p>
      <el-input-otp v-model="otp3" type="underlined" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp1 = ref('')
const otp2 = ref('')
const otp3 = ref('')
</script>

<style scoped>
.demo-input-otp {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

p {
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
</style>
```

隐藏源代码

## 调整尺寸 [​](#调整尺寸)

有三个尺寸可用：`large`、`default` 和 `small`。

Large

Default

Small

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbnB1dC1vdHBcIj5cbiAgICA8ZGl2PlxuICAgICAgPHA+TGFyZ2U8L3A+XG4gICAgICA8ZWwtaW5wdXQtb3RwIHYtbW9kZWw9XCJvdHAxXCIgc2l6ZT1cImxhcmdlXCIgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2PlxuICAgICAgPHA+RGVmYXVsdDwvcD5cbiAgICAgIDxlbC1pbnB1dC1vdHAgdi1tb2RlbD1cIm90cDJcIiBzaXplPVwiZGVmYXVsdFwiIC8+XG4gICAgPC9kaXY+XG4gICAgPGRpdj5cbiAgICAgIDxwPlNtYWxsPC9wPlxuICAgICAgPGVsLWlucHV0LW90cCB2LW1vZGVsPVwib3RwM1wiIHNpemU9XCJzbWFsbFwiIC8+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3Qgb3RwMSA9IHJlZignJylcbmNvbnN0IG90cDIgPSByZWYoJycpXG5jb25zdCBvdHAzID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1pbnB1dC1vdHAge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBnYXA6IDIwcHg7XG59XG5cbnAge1xuICBtYXJnaW4tYm90dG9tOiA4cHg7XG4gIGZvbnQtc2l6ZTogMTRweDtcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-otp/sizes.vue)_

vue

```
<template>
  <div class="demo-input-otp">
    <div>
      <p>Large</p>
      <el-input-otp v-model="otp1" size="large" />
    </div>
    <div>
      <p>Default</p>
      <el-input-otp v-model="otp2" size="default" />
    </div>
    <div>
      <p>Small</p>
      <el-input-otp v-model="otp3" size="small" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp1 = ref('')
const otp2 = ref('')
const otp3 = ref('')
</script>

<style scoped>
.demo-input-otp {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

p {
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
</style>
```

隐藏源代码

## 禁用 & 只读 [​](#禁用-只读)

支持禁用和只读状态。

Disabled

Readonly

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbnB1dC1vdHBcIj5cbiAgICA8ZGl2IGNsYXNzPVwidHlwZS13cmFwXCI+XG4gICAgICA8cD5EaXNhYmxlZDwvcD5cbiAgICAgIDxlbC1pbnB1dC1vdHAgdi1tb2RlbD1cIm90cDFcIiBkaXNhYmxlZCAvPlxuICAgICAgPGVsLWlucHV0LW90cCB2LW1vZGVsPVwib3RwMVwiIGRpc2FibGVkIHR5cGU9XCJmaWxsZWRcIiAvPlxuICAgICAgPGVsLWlucHV0LW90cCB2LW1vZGVsPVwib3RwMVwiIGRpc2FibGVkIHR5cGU9XCJ1bmRlcmxpbmVkXCIgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwidHlwZS13cmFwXCI+XG4gICAgICA8cD5SZWFkb25seTwvcD5cbiAgICAgIDxlbC1pbnB1dC1vdHAgdi1tb2RlbD1cIm90cDJcIiByZWFkb25seSAvPlxuICAgICAgPGVsLWlucHV0LW90cCB2LW1vZGVsPVwib3RwMlwiIHJlYWRvbmx5IHR5cGU9XCJmaWxsZWRcIiAvPlxuICAgICAgPGVsLWlucHV0LW90cCB2LW1vZGVsPVwib3RwMlwiIHJlYWRvbmx5IHR5cGU9XCJ1bmRlcmxpbmVkXCIgLz5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBvdHAxID0gcmVmKCcxMjMnKVxuY29uc3Qgb3RwMiA9IHJlZignNDU2Jylcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8taW5wdXQtb3RwIHtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcbiAgZ2FwOiAyMHB4O1xufVxuXG4udHlwZS13cmFwIHtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcbiAgZ2FwOiAxMnB4O1xufVxuXG5wIHtcbiAgbWFyZ2luLWJvdHRvbTogOHB4O1xuICBmb250LXNpemU6IDE0cHg7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-otp/disabled.vue)_

vue

```
<template>
  <div class="demo-input-otp">
    <div class="type-wrap">
      <p>Disabled</p>
      <el-input-otp v-model="otp1" disabled />
      <el-input-otp v-model="otp1" disabled type="filled" />
      <el-input-otp v-model="otp1" disabled type="underlined" />
    </div>
    <div class="type-wrap">
      <p>Readonly</p>
      <el-input-otp v-model="otp2" readonly />
      <el-input-otp v-model="otp2" readonly type="filled" />
      <el-input-otp v-model="otp2" readonly type="underlined" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp1 = ref('123')
const otp2 = ref('456')
</script>

<style scoped>
.demo-input-otp {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.type-wrap {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

p {
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
</style>
```

隐藏源代码

## 密码模式 [​](#密码模式)

使用 `mask` 属性来隐藏输入字符。

Value: 123

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1pbnB1dC1vdHAgdi1tb2RlbD1cIm90cFwiIG1hc2sgLz5cbiAgICA8ZGl2IHN0eWxlPVwibWFyZ2luLXRvcDogMjBweFwiPlZhbHVlOiB7eyBvdHAgfX08L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBvdHAgPSByZWYoJzEyMycpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-otp/mask.vue)_

vue

```
<template>
  <div>
    <el-input-otp v-model="otp" mask />
    <div style="margin-top: 20px">Value: {{ otp }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp = ref('123')
</script>
```

隐藏源代码

## 分隔符 [​](#分隔符)

自定义OTP字段之间的分隔符。

/////

——

•••••

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbnB1dC1vdHBcIj5cbiAgICA8ZWwtaW5wdXQtb3RwIHNlcGFyYXRvcj1cIi9cIiAvPlxuICAgIDxlbC1pbnB1dC1vdHAgOnNlcGFyYXRvcj1cImNhc3RTZXBhcmF0b3JcIiAvPlxuICAgIDxlbC1pbnB1dC1vdHA+XG4gICAgICA8dGVtcGxhdGUgI3NlcGFyYXRvcj7igKI8L3RlbXBsYXRlPlxuICAgIDwvZWwtaW5wdXQtb3RwPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+XG5pbXBvcnQgeyBoIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBjYXN0U2VwYXJhdG9yID0gKGluZGV4OiBudW1iZXIpID0+IHtcbiAgcmV0dXJuIGluZGV4ICYgMSA/IGgoJ3NwYW4nLCBudWxsLCAn4oCUJykgOiAnJ1xufVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZGVtby1pbnB1dC1vdHAge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBnYXA6IDIwcHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-otp/separator.vue)_

vue

```
<template>
  <div class="demo-input-otp">
    <el-input-otp separator="/" />
    <el-input-otp :separator="castSeparator" />
    <el-input-otp>
      <template #separator>•</template>
    </el-input-otp>
  </div>
</template>

<script setup lang="ts">
import { h } from 'vue'

const castSeparator = (index: number) => {
  return index & 1 ? h('span', null, '—') : ''
}
</script>

<style scoped>
.demo-input-otp {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
```

隐藏源代码

## 自定义验证 [​](#自定义验证)

设置 `validator` 属性以验证输入字符，并使用 `inputmode` 指定键盘类型。

Numbers only

Letters only

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbnB1dC1vdHBcIj5cbiAgICA8ZGl2PlxuICAgICAgPHA+TnVtYmVycyBvbmx5PC9wPlxuICAgICAgPGVsLWlucHV0LW90cFxuICAgICAgICB2LW1vZGVsPVwib3RwMVwiXG4gICAgICAgIDp2YWxpZGF0b3I9XCJvbmx5QWxsb3dOdW1iZXJcIlxuICAgICAgICBpbnB1dG1vZGU9XCJudW1lcmljXCJcbiAgICAgIC8+XG4gICAgPC9kaXY+XG4gICAgPGRpdj5cbiAgICAgIDxwPkxldHRlcnMgb25seTwvcD5cbiAgICAgIDxlbC1pbnB1dC1vdHAgdi1tb2RlbD1cIm90cDJcIiA6dmFsaWRhdG9yPVwib25seUFsbG93TGV0dGVyXCIgLz5cbiAgICA8L2Rpdj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBvdHAxID0gcmVmKCcnKVxuY29uc3Qgb3RwMiA9IHJlZignJylcblxuY29uc3Qgb25seUFsbG93TnVtYmVyID0gKHZhbHVlOiBzdHJpbmcpID0+IC9eXFxkJC8udGVzdCh2YWx1ZSlcbmNvbnN0IG9ubHlBbGxvd0xldHRlciA9ICh2YWx1ZTogc3RyaW5nKSA9PiAvXlthLXpBLVpdJC8udGVzdCh2YWx1ZSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8taW5wdXQtb3RwIHtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcbiAgZ2FwOiAyMHB4O1xufVxuXG5wIHtcbiAgbWFyZ2luLWJvdHRvbTogOHB4O1xuICBmb250LXNpemU6IDE0cHg7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-otp/validator.vue)_

vue

```
<template>
  <div class="demo-input-otp">
    <div>
      <p>Numbers only</p>
      <el-input-otp
        v-model="otp1"
        :validator="onlyAllowNumber"
        inputmode="numeric"
      />
    </div>
    <div>
      <p>Letters only</p>
      <el-input-otp v-model="otp2" :validator="onlyAllowLetter" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp1 = ref('')
const otp2 = ref('')

const onlyAllowNumber = (value: string) => /^\d$/.test(value)
const onlyAllowLetter = (value: string) => /^[a-zA-Z]$/.test(value)
</script>

<style scoped>
.demo-input-otp {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

p {
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
</style>
```

隐藏源代码

## 应用开发接口（API） [​](#应用开发接口-api)

### 属性 [​](#属性)

| 插槽名 | 详情 | 事件参数 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | OTP字段的值。 由于数字不能有前导零，`modelValue` 仅在初始化期间允许为数字。 | `string` / `number` | undefined |
| length | OTP字段长度 | `number` | 6 |
| validator | 自定义验证函数 | `Function` | () => true |
| inputmode | 原生 `inputmode` 属性 | `string` | — |
| type | OTP字段类型 | `enum` | 'outlined' |
| size | OTP字段的尺寸 | `enum` | 'default' |
| mask | 是否启用密码模式 | `boolean` | — |
| disabled | 是否禁用OTP字段 | `boolean` | undefined |
| separator | OTP字段之间的分隔符 | `string` / `VNode` / `Function` | — |
| validate-event | 是否触发表单验证 | `boolean` | true |
| readonly | 与原生输入中的 `readonly` 相同 | `boolean` | false |
| id | 原生 `id` 属性 | `string` | — |
| aria-label a11y | 原生 `aria-label` 属性 | `string` | — |

### Events [​](#events)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| update:modelValue | 值更新时触发 | `Function` |
| change | 当输入框失去焦点后且值发生变化时触发 | `Function` |
| finish | 当所有字段都已填写时触发 | `Function` |
| focus | 输入框获得焦点时触发 | `Function` |
| blur | 输入框失去焦点时触发 | `Function` |

### 插槽 [​](#插槽)

| 方法名 | 详情 | 事件参数 |
| --- | --- | --- |
| separator | OTP 字段之间的分隔符 | `object` |

### 对外暴露的方法 [​](#对外暴露的方法)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| inputRefs | HTML 输入框元素数组 | `object` |
| focus | 聚焦OTP输入字段 | `Function` |
| blur | 失焦OTP输入字段 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/input-otp) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/input-otp.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/input-otp.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/166777320?v=4&size=64)](https://github.com/ixyzorg)

[Input Tag 标签输入框](https://element-plus.org/zh-CN/component/input-tag)

[Mention 提及](https://element-plus.org/zh-CN/component/mention)


