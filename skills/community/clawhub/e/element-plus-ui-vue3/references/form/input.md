---
name: "input"
description: "Input 输入框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Input 输入框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/input.html"
---

---

# Input 输入框 [​](#input-输入框)

更新日志待解决

48

通过鼠标或键盘输入字符

## 基础用法 [​](#基础用法)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQgdi1tb2RlbD1cImlucHV0XCIgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIiBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBpbnB1dCA9IHJlZignJylcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/basic.vue)_

vue

```
<template>
  <el-input v-model="input" style="width: 240px" placeholder="Please input" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref('')
</script>
```

隐藏源代码

## 禁用状态 [​](#禁用状态)

通过 `disabled` 属性指定是否禁用 input 组件

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwiaW5wdXRcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICBkaXNhYmxlZFxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGlucHV0ID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/disabled.vue)_

vue

```
<template>
  <el-input
    v-model="input"
    style="width: 240px"
    disabled
    placeholder="Please input"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref('')
</script>
```

隐藏源代码

## 一键清空 [​](#一键清空)

使用`clearable`属性即可得到一个可一键清空的输入框 在版本 2.13.4 之后，Input 的 textarea 类型也支持 clearable 功能。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiaW5wdXQtZ3JvdXBcIj5cbiAgICA8ZWwtaW5wdXRcbiAgICAgIHYtbW9kZWw9XCJpbnB1dFwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgICBjbGVhcmFibGVcbiAgICAvPlxuICAgIDxlbC1pbnB1dFxuICAgICAgdi1tb2RlbD1cInRleHRhcmVhSW5wdXRcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXRcIlxuICAgICAgdHlwZT1cInRleHRhcmVhXCJcbiAgICAgIGNsZWFyYWJsZVxuICAgIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5wdXQgPSByZWYoJycpXG5jb25zdCB0ZXh0YXJlYUlucHV0ID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uaW5wdXQtZ3JvdXAge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBnYXA6IDFlbTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/clearable.vue)_

vue

```
<template>
  <div class="input-group">
    <el-input
      v-model="input"
      style="width: 240px"
      placeholder="Please input"
      clearable
    />
    <el-input
      v-model="textareaInput"
      style="width: 240px"
      placeholder="Please input"
      type="textarea"
      clearable
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref('')
const textareaInput = ref('')
</script>

<style scoped>
.input-group {
  display: flex;
  align-items: center;
  gap: 1em;
}
</style>
```

隐藏源代码

## 自定义清除图标2.11.0 [​](#自定义清除图标)

你可以通过`clear-icon`属性自定义清除图标

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiaW5wdXQtZ3JvdXBcIj5cbiAgICA8ZWwtaW5wdXRcbiAgICAgIHYtbW9kZWw9XCJpbnB1dFwiXG4gICAgICBjbGVhcmFibGVcbiAgICAgIDpjbGVhci1pY29uPVwiQ2xvc2VCb2xkXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiQ3VzdG9tIGNsZWFyIGljb25cIlxuICAgIC8+XG4gICAgPGVsLWlucHV0XG4gICAgICB2LW1vZGVsPVwidGV4dGFyZWFJbnB1dFwiXG4gICAgICBjbGVhcmFibGVcbiAgICAgIDpjbGVhci1pY29uPVwiQ2xvc2VCb2xkXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiQ3VzdG9tIGNsZWFyIGljb25cIlxuICAgICAgdHlwZT1cInRleHRhcmVhXCJcbiAgICAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBDbG9zZUJvbGQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgaW5wdXQgPSByZWYoJ0N1c3RvbSBjbGVhciBpY29uJylcbmNvbnN0IHRleHRhcmVhSW5wdXQgPSByZWYoJ0N1c3RvbSBjbGVhciBpY29uJylcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmlucHV0LWdyb3VwIHtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcbiAgZ2FwOiAxZW07XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/clear-icon.vue)_

vue

```
<template>
  <div class="input-group">
    <el-input
      v-model="input"
      clearable
      :clear-icon="CloseBold"
      placeholder="Custom clear icon"
    />
    <el-input
      v-model="textareaInput"
      clearable
      :clear-icon="CloseBold"
      placeholder="Custom clear icon"
      type="textarea"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CloseBold } from '@element-plus/icons-vue'

const input = ref('Custom clear icon')
const textareaInput = ref('Custom clear icon')
</script>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  gap: 1em;
}
</style>
```

隐藏源代码

## 格式化 [​](#格式化)

在 `formatter`的情况下显示值，我们通常同时使用 `parser`

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwiaW5wdXRcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgOmZvcm1hdHRlcj1cIih2YWx1ZSkgPT4gYCQgJHt2YWx1ZX1gLnJlcGxhY2UoL1xcQig/PShcXGR7M30pKyg/IVxcZCkpL2csICcsJylcIlxuICAgIDpwYXJzZXI9XCIodmFsdWUpID0+IHZhbHVlLnJlcGxhY2UoL1xcJFxccz98KCwqKS9nLCAnJylcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgaW5wdXQgPSByZWYoJycpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/formatter.vue)_

vue

```
<template>
  <el-input
    v-model="input"
    style="width: 240px"
    placeholder="Please input"
    :formatter="(value) => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')"
    :parser="(value) => value.replace(/\$\s?|(,*)/g, '')"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref('')
</script>
```

隐藏源代码

## 密码框 [​](#密码框)

使用 `show-password` 属性即可得到一个可切换显示隐藏的密码框 自 2.13.6 起，支持使用 `password-icon` 插槽覆盖默认图标。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiaW5wdXQtZ3JvdXBcIj5cbiAgICA8ZWwtaW5wdXRcbiAgICAgIHYtbW9kZWw9XCJpbnB1dFwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICB0eXBlPVwicGFzc3dvcmRcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXQgcGFzc3dvcmRcIlxuICAgICAgc2hvdy1wYXNzd29yZFxuICAgIC8+XG4gICAgPGVsLWlucHV0XG4gICAgICB2LW1vZGVsPVwiaW5wdXRcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgdHlwZT1cInBhc3N3b3JkXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0IHBhc3N3b3JkXCJcbiAgICAgIHNob3ctcGFzc3dvcmRcbiAgICA+XG4gICAgICA8dGVtcGxhdGUgI3Bhc3N3b3JkLWljb249XCJ7IHZpc2libGUgfVwiPlxuICAgICAgICA8ZWwtaWNvbiA6c2l6ZT1cIjE2XCI+XG4gICAgICAgICAgPFVubG9jayB2LWlmPVwidmlzaWJsZVwiIC8+XG4gICAgICAgICAgPExvY2sgdi1lbHNlIC8+XG4gICAgICAgIDwvZWwtaWNvbj5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1pbnB1dD5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgTG9jaywgVW5sb2NrIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IGlucHV0ID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uaW5wdXQtZ3JvdXAge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBnYXA6IDFlbTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/password.vue)_

vue

```
<template>
  <div class="input-group">
    <el-input
      v-model="input"
      style="width: 240px"
      type="password"
      placeholder="Please input password"
      show-password
    />
    <el-input
      v-model="input"
      style="width: 240px"
      type="password"
      placeholder="Please input password"
      show-password
    >
      <template #password-icon="{ visible }">
        <el-icon :size="16">
          <Unlock v-if="visible" />
          <Lock v-else />
        </el-icon>
      </template>
    </el-input>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Lock, Unlock } from '@element-plus/icons-vue'

const input = ref('')
</script>

<style scoped>
.input-group {
  display: flex;
  align-items: center;
  gap: 1em;
}
</style>
```

隐藏源代码

## 带图标的输入框 [​](#带图标的输入框)

带有图标标记输入类型

要在输入框中添加图标，你可以简单地使用 `prefix-icon` 和 `suffix-icon` 属性。 另外， `prefix` 和 `suffix` 命名的插槽也能正常工作。

Using attributes

Using slots

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1pbnB1dC13aXRoLWljb25cIj5cbiAgICA8ZGl2IGNsYXNzPVwiaW5wdXQtZ3JvdXBcIj5cbiAgICAgIDxzcGFuIGNsYXNzPVwibGFiZWxcIj5Vc2luZyBhdHRyaWJ1dGVzPC9zcGFuPlxuICAgICAgPGRpdiBjbGFzcz1cImlucHV0LWNvbnRhaW5lclwiPlxuICAgICAgICA8ZWwtaW5wdXRcbiAgICAgICAgICB2LW1vZGVsPVwiaW5wdXQxXCJcbiAgICAgICAgICBjbGFzcz1cInJlc3BvbnNpdmUtaW5wdXRcIlxuICAgICAgICAgIHBsYWNlaG9sZGVyPVwiUGljayBhIGRhdGVcIlxuICAgICAgICAgIDpzdWZmaXgtaWNvbj1cIkNhbGVuZGFyXCJcbiAgICAgICAgLz5cbiAgICAgICAgPGVsLWlucHV0XG4gICAgICAgICAgdi1tb2RlbD1cImlucHV0MlwiXG4gICAgICAgICAgY2xhc3M9XCJyZXNwb25zaXZlLWlucHV0XCJcbiAgICAgICAgICBwbGFjZWhvbGRlcj1cIlR5cGUgc29tZXRoaW5nXCJcbiAgICAgICAgICA6cHJlZml4LWljb249XCJTZWFyY2hcIlxuICAgICAgICAvPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+XG4gICAgPGRpdiBjbGFzcz1cImlucHV0LWdyb3VwXCI+XG4gICAgICA8c3BhbiBjbGFzcz1cImxhYmVsXCI+VXNpbmcgc2xvdHM8L3NwYW4+XG4gICAgICA8ZGl2IGNsYXNzPVwiaW5wdXQtY29udGFpbmVyXCI+XG4gICAgICAgIDxlbC1pbnB1dFxuICAgICAgICAgIHYtbW9kZWw9XCJpbnB1dDNcIlxuICAgICAgICAgIGNsYXNzPVwicmVzcG9uc2l2ZS1pbnB1dFwiXG4gICAgICAgICAgcGxhY2Vob2xkZXI9XCJQaWNrIGEgZGF0ZVwiXG4gICAgICAgID5cbiAgICAgICAgICA8dGVtcGxhdGUgI3N1ZmZpeD5cbiAgICAgICAgICAgIDxlbC1pY29uIGNsYXNzPVwiZWwtaW5wdXRfX2ljb25cIj48Y2FsZW5kYXIgLz48L2VsLWljb24+XG4gICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgPC9lbC1pbnB1dD5cbiAgICAgICAgPGVsLWlucHV0XG4gICAgICAgICAgdi1tb2RlbD1cImlucHV0NFwiXG4gICAgICAgICAgY2xhc3M9XCJyZXNwb25zaXZlLWlucHV0XCJcbiAgICAgICAgICBwbGFjZWhvbGRlcj1cIlR5cGUgc29tZXRoaW5nXCJcbiAgICAgICAgPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjcHJlZml4PlxuICAgICAgICAgICAgPGVsLWljb24gY2xhc3M9XCJlbC1pbnB1dF9faWNvblwiPjxzZWFyY2ggLz48L2VsLWljb24+XG4gICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgPC9lbC1pbnB1dD5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBDYWxlbmRhciwgU2VhcmNoIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IGlucHV0MSA9IHJlZignJylcbmNvbnN0IGlucHV0MiA9IHJlZignJylcbmNvbnN0IGlucHV0MyA9IHJlZignJylcbmNvbnN0IGlucHV0NCA9IHJlZignJylcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8taW5wdXQtd2l0aC1pY29uIHtcbiAgd2lkdGg6IDEwMCU7XG59XG5cbi5pbnB1dC1ncm91cCB7XG4gIG1hcmdpbi1ib3R0b206IDEuNXJlbTtcbn1cblxuLmxhYmVsIHtcbiAgZGlzcGxheTogYmxvY2s7XG4gIG1hcmdpbi1ib3R0b206IDFyZW07XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXJlZ3VsYXIpO1xufVxuXG4uaW5wdXQtY29udGFpbmVyIHtcbiAgZGlzcGxheTogZmxleDtcbiAgZ2FwOiAxcmVtO1xuICBmbGV4LXdyYXA6IHdyYXA7XG59XG5cbi5yZXNwb25zaXZlLWlucHV0IHtcbiAgd2lkdGg6IDI0MHB4O1xufVxuXG5AbWVkaWEgKG1heC13aWR0aDogNzY4cHgpIHtcbiAgLmlucHV0LWNvbnRhaW5lciB7XG4gICAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjtcbiAgICBnYXA6IDFyZW07XG4gIH1cblxuICAucmVzcG9uc2l2ZS1pbnB1dCB7XG4gICAgd2lkdGg6IDEwMCU7XG4gIH1cbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/with-icon.vue)_

vue

```
<template>
  <div class="demo-input-with-icon">
    <div class="input-group">
      <span class="label">Using attributes</span>
      <div class="input-container">
        <el-input
          v-model="input1"
          class="responsive-input"
          placeholder="Pick a date"
          :suffix-icon="Calendar"
        />
        <el-input
          v-model="input2"
          class="responsive-input"
          placeholder="Type something"
          :prefix-icon="Search"
        />
      </div>
    </div>
    <div class="input-group">
      <span class="label">Using slots</span>
      <div class="input-container">
        <el-input
          v-model="input3"
          class="responsive-input"
          placeholder="Pick a date"
        >
          <template #suffix>
            <el-icon class="el-input__icon"><calendar /></el-icon>
          </template>
        </el-input>
        <el-input
          v-model="input4"
          class="responsive-input"
          placeholder="Type something"
        >
          <template #prefix>
            <el-icon class="el-input__icon"><search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Calendar, Search } from '@element-plus/icons-vue'

const input1 = ref('')
const input2 = ref('')
const input3 = ref('')
const input4 = ref('')
</script>

<style scoped>
.demo-input-with-icon {
  width: 100%;
}

.input-group {
  margin-bottom: 1.5rem;
}

.label {
  display: block;
  margin-bottom: 1rem;
  color: var(--el-text-color-regular);
}

.input-container {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.responsive-input {
  width: 240px;
}

@media (max-width: 768px) {
  .input-container {
    flex-direction: column;
    gap: 1rem;
  }

  .responsive-input {
    width: 100%;
  }
}
</style>
```

隐藏源代码

## 文本域 [​](#文本域)

用于输入多行文本信息可缩放的输入框。 添加 `type="textarea"` 属性来将 `input` 元素转换为原生的 `textarea` 元素。

文本域高度可通过 `rows` 属性控制

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwidGV4dGFyZWFcIlxuICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICA6cm93cz1cIjJcIlxuICAgIHR5cGU9XCJ0ZXh0YXJlYVwiXG4gICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXRcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdGV4dGFyZWEgPSByZWYoJycpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/textarea.vue)_

vue

```
<template>
  <el-input
    v-model="textarea"
    style="width: 240px"
    :rows="2"
    type="textarea"
    placeholder="Please input"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const textarea = ref('')
</script>
```

隐藏源代码

## 自适应文本域 [​](#自适应文本域)

设置文字输入类型的 `autosize` 属性使得根据内容自动调整的高度。 你可以给 `autosize` 提供一个包含有最大和最小高度的对象，让输入框自动调整。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwidGV4dGFyZWExXCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgYXV0b3NpemVcbiAgICB0eXBlPVwidGV4dGFyZWFcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgLz5cbiAgPGRpdiBzdHlsZT1cIm1hcmdpbjogMjBweCAwXCIgLz5cbiAgPGVsLWlucHV0XG4gICAgdi1tb2RlbD1cInRleHRhcmVhMlwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgIDphdXRvc2l6ZT1cInsgbWluUm93czogMiwgbWF4Um93czogNCB9XCJcbiAgICB0eXBlPVwidGV4dGFyZWFcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHRleHRhcmVhMSA9IHJlZignJylcbmNvbnN0IHRleHRhcmVhMiA9IHJlZignJylcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/auto-sizing-textarea.vue)_

vue

```
<template>
  <el-input
    v-model="textarea1"
    style="width: 240px"
    autosize
    type="textarea"
    placeholder="Please input"
  />
  <div style="margin: 20px 0" />
  <el-input
    v-model="textarea2"
    style="width: 240px"
    :autosize="{ minRows: 2, maxRows: 4 }"
    type="textarea"
    placeholder="Please input"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const textarea1 = ref('')
const textarea2 = ref('')
</script>
```

隐藏源代码

## 复合型输入框 [​](#复合型输入框)

可以在输入框中前置或后置一个元素，通常是标签或按钮。

可通过 `slot` 来指定在 Input 中分发的前置或者后置的内容。

Http://

.com

Select

Select

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1pbnB1dFxuICAgICAgdi1tb2RlbD1cImlucHV0MVwiXG4gICAgICBzdHlsZT1cIm1heC13aWR0aDogNjAwcHhcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXRcIlxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjcHJlcGVuZD5IdHRwOi8vPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWlucHV0PlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cIm10LTRcIj5cbiAgICA8ZWwtaW5wdXRcbiAgICAgIHYtbW9kZWw9XCJpbnB1dDJcIlxuICAgICAgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgICA+XG4gICAgICA8dGVtcGxhdGUgI2FwcGVuZD4uY29tPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWlucHV0PlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cIm10LTRcIj5cbiAgICA8ZWwtaW5wdXRcbiAgICAgIHYtbW9kZWw9XCJpbnB1dDNcIlxuICAgICAgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgICAgIGNsYXNzPVwiaW5wdXQtd2l0aC1zZWxlY3RcIlxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjcHJlcGVuZD5cbiAgICAgICAgPGVsLXNlbGVjdCB2LW1vZGVsPVwic2VsZWN0XCIgcGxhY2Vob2xkZXI9XCJTZWxlY3RcIiBzdHlsZT1cIndpZHRoOiAxMTVweFwiPlxuICAgICAgICAgIDxlbC1vcHRpb24gbGFiZWw9XCJSZXN0YXVyYW50XCIgdmFsdWU9XCIxXCIgLz5cbiAgICAgICAgICA8ZWwtb3B0aW9uIGxhYmVsPVwiT3JkZXIgTm8uXCIgdmFsdWU9XCIyXCIgLz5cbiAgICAgICAgICA8ZWwtb3B0aW9uIGxhYmVsPVwiVGVsXCIgdmFsdWU9XCIzXCIgLz5cbiAgICAgICAgPC9lbC1zZWxlY3Q+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgPHRlbXBsYXRlICNhcHBlbmQ+XG4gICAgICAgIDxlbC1idXR0b24gOmljb249XCJTZWFyY2hcIiAvPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWlucHV0PlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cIm10LTRcIj5cbiAgICA8ZWwtaW5wdXRcbiAgICAgIHYtbW9kZWw9XCJpbnB1dDNcIlxuICAgICAgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgICAgIGNsYXNzPVwiaW5wdXQtd2l0aC1zZWxlY3RcIlxuICAgID5cbiAgICAgIDx0ZW1wbGF0ZSAjcHJlcGVuZD5cbiAgICAgICAgPGVsLWJ1dHRvbiA6aWNvbj1cIlNlYXJjaFwiIC8+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgPHRlbXBsYXRlICNhcHBlbmQ+XG4gICAgICAgIDxlbC1zZWxlY3Qgdi1tb2RlbD1cInNlbGVjdFwiIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCIgc3R5bGU9XCJ3aWR0aDogMTE1cHhcIj5cbiAgICAgICAgICA8ZWwtb3B0aW9uIGxhYmVsPVwiUmVzdGF1cmFudFwiIHZhbHVlPVwiMVwiIC8+XG4gICAgICAgICAgPGVsLW9wdGlvbiBsYWJlbD1cIk9yZGVyIE5vLlwiIHZhbHVlPVwiMlwiIC8+XG4gICAgICAgICAgPGVsLW9wdGlvbiBsYWJlbD1cIlRlbFwiIHZhbHVlPVwiM1wiIC8+XG4gICAgICAgIDwvZWwtc2VsZWN0PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWlucHV0PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgc2V0dXAgbGFuZz1cInRzXCI+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBTZWFyY2ggfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgaW5wdXQxID0gcmVmKCcnKVxuY29uc3QgaW5wdXQyID0gcmVmKCcnKVxuY29uc3QgaW5wdXQzID0gcmVmKCcnKVxuY29uc3Qgc2VsZWN0ID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5pbnB1dC13aXRoLXNlbGVjdCAuZWwtaW5wdXQtZ3JvdXBfX3ByZXBlbmQge1xuICBiYWNrZ3JvdW5kLWNvbG9yOiB2YXIoLS1lbC1maWxsLWNvbG9yLWJsYW5rKTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/mixed-input.vue)_

vue

```
<template>
  <div>
    <el-input
      v-model="input1"
      style="max-width: 600px"
      placeholder="Please input"
    >
      <template #prepend>Http://</template>
    </el-input>
  </div>
  <div class="mt-4">
    <el-input
      v-model="input2"
      style="max-width: 600px"
      placeholder="Please input"
    >
      <template #append>.com</template>
    </el-input>
  </div>
  <div class="mt-4">
    <el-input
      v-model="input3"
      style="max-width: 600px"
      placeholder="Please input"
      class="input-with-select"
    >
      <template #prepend>
        <el-select v-model="select" placeholder="Select" style="width: 115px">
          <el-option label="Restaurant" value="1" />
          <el-option label="Order No." value="2" />
          <el-option label="Tel" value="3" />
        </el-select>
      </template>
      <template #append>
        <el-button :icon="Search" />
      </template>
    </el-input>
  </div>
  <div class="mt-4">
    <el-input
      v-model="input3"
      style="max-width: 600px"
      placeholder="Please input"
      class="input-with-select"
    >
      <template #prepend>
        <el-button :icon="Search" />
      </template>
      <template #append>
        <el-select v-model="select" placeholder="Select" style="width: 115px">
          <el-option label="Restaurant" value="1" />
          <el-option label="Order No." value="2" />
          <el-option label="Tel" value="3" />
        </el-select>
      </template>
    </el-input>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

const input1 = ref('')
const input2 = ref('')
const input3 = ref('')
const select = ref('')
</script>

<style>
.input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
}
</style>
```

隐藏源代码

## 尺寸 [​](#尺寸)

使用 `size` 属性改变输入框大小。 除了默认大小外，还有另外两个选项： `large`, `small`。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtNCBtYi00IGl0ZW1zLWNlbnRlclwiPlxuICAgIDxlbC1pbnB1dFxuICAgICAgdi1tb2RlbD1cImlucHV0MVwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICBzaXplPVwibGFyZ2VcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgSW5wdXRcIlxuICAgIC8+XG4gICAgPGVsLWlucHV0XG4gICAgICB2LW1vZGVsPVwiaW5wdXQyXCJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIElucHV0XCJcbiAgICAvPlxuICAgIDxlbC1pbnB1dFxuICAgICAgdi1tb2RlbD1cImlucHV0M1wiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICBzaXplPVwic21hbGxcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgSW5wdXRcIlxuICAgIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtNCBtYi00IGl0ZW1zLWNlbnRlclwiPlxuICAgIDxlbC1pbnB1dFxuICAgICAgdi1tb2RlbD1cImlucHV0MVwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICBzaXplPVwibGFyZ2VcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgSW5wdXRcIlxuICAgICAgOnN1ZmZpeC1pY29uPVwiU2VhcmNoXCJcbiAgICAvPlxuICAgIDxlbC1pbnB1dFxuICAgICAgdi1tb2RlbD1cImlucHV0MlwiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBJbnB1dFwiXG4gICAgICA6c3VmZml4LWljb249XCJTZWFyY2hcIlxuICAgIC8+XG4gICAgPGVsLWlucHV0XG4gICAgICB2LW1vZGVsPVwiaW5wdXQzXCJcbiAgICAgIHN0eWxlPVwid2lkdGg6IDI0MHB4XCJcbiAgICAgIHNpemU9XCJzbWFsbFwiXG4gICAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBJbnB1dFwiXG4gICAgICA6c3VmZml4LWljb249XCJTZWFyY2hcIlxuICAgIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwiZmxleCBnYXAtNCBpdGVtcy1jZW50ZXJcIj5cbiAgICA8ZWwtaW5wdXRcbiAgICAgIHYtbW9kZWw9XCJpbnB1dDFcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgc2l6ZT1cImxhcmdlXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIElucHV0XCJcbiAgICAgIDpwcmVmaXgtaWNvbj1cIlNlYXJjaFwiXG4gICAgLz5cbiAgICA8ZWwtaW5wdXRcbiAgICAgIHYtbW9kZWw9XCJpbnB1dDJcIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgSW5wdXRcIlxuICAgICAgOnByZWZpeC1pY29uPVwiU2VhcmNoXCJcbiAgICAvPlxuICAgIDxlbC1pbnB1dFxuICAgICAgdi1tb2RlbD1cImlucHV0M1wiXG4gICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICBzaXplPVwic21hbGxcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgSW5wdXRcIlxuICAgICAgOnByZWZpeC1pY29uPVwiU2VhcmNoXCJcbiAgICAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBTZWFyY2ggfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgaW5wdXQxID0gcmVmKCcnKVxuY29uc3QgaW5wdXQyID0gcmVmKCcnKVxuY29uc3QgaW5wdXQzID0gcmVmKCcnKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/various-size.vue)_

vue

```
<template>
  <div class="flex gap-4 mb-4 items-center">
    <el-input
      v-model="input1"
      style="width: 240px"
      size="large"
      placeholder="Please Input"
    />
    <el-input
      v-model="input2"
      style="width: 240px"
      placeholder="Please Input"
    />
    <el-input
      v-model="input3"
      style="width: 240px"
      size="small"
      placeholder="Please Input"
    />
  </div>
  <div class="flex gap-4 mb-4 items-center">
    <el-input
      v-model="input1"
      style="width: 240px"
      size="large"
      placeholder="Please Input"
      :suffix-icon="Search"
    />
    <el-input
      v-model="input2"
      style="width: 240px"
      placeholder="Please Input"
      :suffix-icon="Search"
    />
    <el-input
      v-model="input3"
      style="width: 240px"
      size="small"
      placeholder="Please Input"
      :suffix-icon="Search"
    />
  </div>
  <div class="flex gap-4 items-center">
    <el-input
      v-model="input1"
      style="width: 240px"
      size="large"
      placeholder="Please Input"
      :prefix-icon="Search"
    />
    <el-input
      v-model="input2"
      style="width: 240px"
      placeholder="Please Input"
      :prefix-icon="Search"
    />
    <el-input
      v-model="input3"
      style="width: 240px"
      size="small"
      placeholder="Please Input"
      :prefix-icon="Search"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

const input1 = ref('')
const input2 = ref('')
const input3 = ref('')
</script>
```

隐藏源代码

## 输入长度限制 [​](#输入长度限制)

使用 `maxlength` 和 `minlength` 属性, 来控制输入内容的最大字数和最小字数。 "字符数"使用JavaScript字符串长度来衡量。 为文本或文本输入类型设置 `maxlength` prop可以限制输入值的长度。 允许你通过设置 `show-word-limit` 到 `true` 来显示剩余字数。 从 2.11.5 版本开始，你可以将 `word-limit-position` 设置为 `outside`，以在输入框外显示字数统计。

0 / 10

0 / 10

0 / 30

0 / 30

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwidGV4dFwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgIG1heGxlbmd0aD1cIjEwXCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgc2hvdy13b3JkLWxpbWl0XG4gICAgdHlwZT1cInRleHRcIlxuICAvPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwidGV4dFwiXG4gICAgY2xhc3M9XCJtbC00XCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgbWF4bGVuZ3RoPVwiMTBcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgICBzaG93LXdvcmQtbGltaXRcbiAgICB3b3JkLWxpbWl0LXBvc2l0aW9uPVwib3V0c2lkZVwiXG4gICAgdHlwZT1cInRleHRcIlxuICAvPlxuICA8ZGl2IHN0eWxlPVwibWFyZ2luOiAyMHB4IDBcIiAvPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwidGV4dGFyZWFcIlxuICAgIG1heGxlbmd0aD1cIjMwXCJcbiAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgcGxhY2Vob2xkZXI9XCJQbGVhc2UgaW5wdXRcIlxuICAgIHNob3ctd29yZC1saW1pdFxuICAgIHR5cGU9XCJ0ZXh0YXJlYVwiXG4gIC8+XG4gIDxlbC1pbnB1dFxuICAgIHYtbW9kZWw9XCJ0ZXh0YXJlYVwiXG4gICAgY2xhc3M9XCJtbC00XCJcbiAgICBtYXhsZW5ndGg9XCIzMFwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgICBzaG93LXdvcmQtbGltaXRcbiAgICB3b3JkLWxpbWl0LXBvc2l0aW9uPVwib3V0c2lkZVwiXG4gICAgdHlwZT1cInRleHRhcmVhXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHRleHQgPSByZWYoJycpXG5jb25zdCB0ZXh0YXJlYSA9IHJlZignJylcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/length-limiting.vue)_

vue

```
<template>
  <el-input
    v-model="text"
    style="width: 240px"
    maxlength="10"
    placeholder="Please input"
    show-word-limit
    type="text"
  />
  <el-input
    v-model="text"
    class="ml-4"
    style="width: 240px"
    maxlength="10"
    placeholder="Please input"
    show-word-limit
    word-limit-position="outside"
    type="text"
  />
  <div style="margin: 20px 0" />
  <el-input
    v-model="textarea"
    maxlength="30"
    style="width: 240px"
    placeholder="Please input"
    show-word-limit
    type="textarea"
  />
  <el-input
    v-model="textarea"
    class="ml-4"
    maxlength="30"
    style="width: 240px"
    placeholder="Please input"
    show-word-limit
    word-limit-position="outside"
    type="textarea"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const text = ref('')
const textarea = ref('')
</script>
```

隐藏源代码

## 计数图形2.13.7 [​](#计数图形)

设置 `count-graphemes` 以计算文本长度。 如果设置了该属性，则不会使用原生的 `maxlength` 和 `minlength`。

2 / 10

2 / 20

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwidGV4dFwiXG4gICAgbWF4bGVuZ3RoPVwiMTBcIlxuICAgIHBsYWNlaG9sZGVyPVwiUGxlYXNlIGlucHV0XCJcbiAgICBzaG93LXdvcmQtbGltaXRcbiAgICA6Y291bnQtZ3JhcGhlbWVzPVwiY2FsY1wiXG4gICAgdHlwZT1cInRleHRcIlxuICAvPlxuICA8ZGl2IHN0eWxlPVwibWFyZ2luOiAyMHB4IDBcIiAvPlxuICA8ZWwtaW5wdXRcbiAgICB2LW1vZGVsPVwidGV4dGFyZWFcIlxuICAgIG1heGxlbmd0aD1cIjIwXCJcbiAgICBwbGFjZWhvbGRlcj1cIlBsZWFzZSBpbnB1dFwiXG4gICAgc2hvdy13b3JkLWxpbWl0XG4gICAgOmNvdW50LWdyYXBoZW1lcz1cImNhbGNcIlxuICAgIHR5cGU9XCJ0ZXh0YXJlYVwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB0ZXh0ID0gcmVmKCfwn5iA8J+YgScpXG5jb25zdCB0ZXh0YXJlYSA9IHJlZign8J+YgPCfmIEnKVxuXG4vKipcbiAqIENvdW50IGZ1bmN0aW9uIGZvciBncmFwaGVtZSBjbHVzdGVyaW5nLlxuICogQ291bnRzIHRoZSBudW1iZXIgb2YgZ3JhcGhlbWVzICh2aXN1YWwgY2hhcmFjdGVycykgaW4gYSBzdHJpbmcuXG4gKlxuICogTm90ZTogVGhpcyBleGFtcGxlIHVzZXMgQXJyYXkuZnJvbSgpIGZvciBzaW1wbGljaXR5LlxuICogRm9yIHByb2R1Y3Rpb24gdXNlLCBjb25zaWRlciB1c2luZyBJbnRsLlNlZ21lbnRlciBmb3IgYmV0dGVyXG4gKiBoYW5kbGluZyBvZiBjb21wbGV4IGVtb2ppIGFuZCB1bmljb2RlIGNoYXJhY3RlcnMuXG4gKi9cbmNvbnN0IGNhbGMgPSAodmFsdWU6IHN0cmluZykgPT4ge1xuICAvLyBTaW1wbGlmaWVkIHZlcnNpb246IGNvdW50cyBjb2RlIHBvaW50cyAobm90IGZ1bGwgZ3JhcGhlbWUgY2x1c3RlcnMpXG4gIC8vIEZvciBwcm9kdWN0aW9uLCB1c2UgSW50bC5TZWdtZW50ZXIgbGlrZSB0aGUgY29tcG9uZW50IGRvZXNcbiAgcmV0dXJuIEFycmF5LmZyb20odmFsdWUpLmxlbmd0aFxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input/count-graphemes.vue)_

vue

```
<template>
  <el-input
    v-model="text"
    maxlength="10"
    placeholder="Please input"
    show-word-limit
    :count-graphemes="calc"
    type="text"
  />
  <div style="margin: 20px 0" />
  <el-input
    v-model="textarea"
    maxlength="20"
    placeholder="Please input"
    show-word-limit
    :count-graphemes="calc"
    type="textarea"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const text = ref('😀😁')
const textarea = ref('😀😁')

/**
 * Count function for grapheme clustering.
 * Counts the number of graphemes (visual characters) in a string.
 *
 * Note: This example uses Array.from() for simplicity.
 * For production use, consider using Intl.Segmenter for better
 * handling of complex emoji and unicode characters.
 */
const calc = (value: string) => {
  // Simplified version: counts code points (not full grapheme clusters)
  // For production, use Intl.Segmenter like the component does
  return Array.from(value).length
}
</script>
```

隐藏源代码

TIP

**浏览器支持 & 回退策略**

当使用 `count-graphemes` prop时，组件使用以下方法：

-   **主要**: 使用 `Intl.Segmenter` API (Chrome 87+, Firefox 125+, Safari 14.1+) 进行适当的图形集群处理。 它能够正确处理复杂的表情符号、组合标记和0宽度连接符序列。

-   **回退**: 旧版浏览器会回退到 `Array.from()` 进行基于码点的迭代。 请注意，这可能会拆分多码点字形序列（例如，带有肤色修饰符的表情符号）。

在实现自己的 `count-graphemes` 函数时，如果需要对复杂的 unicode 字符提供强大的支持，请考虑使用 `Intl.Segmenter`。

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| type | 输入类型，更多信息请参见 [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#Form_%3Cinput%3E_types) | `string` | text |
| model-value / v-model | 绑定值 | `string` / `number` | — |
| model-modifiers 2.11.5 | v-model 修饰符，参考 [Vue 修饰符](https://vuejs.org/guide/essentials/forms.html#modifiers) | `object` | — |
| maxlength | 同原生 `maxlength` 属性 | `string` / `number` | — |
| minlength | 原生属性，最小输入长度 | `string` / `number` | — |
| show-word-limit | 是否显示统计字数, 只在 `type` 为 'text' 或 'textarea' 的时候生效 | `boolean` | false |
| word-limit-position 2.11.5 | 字数统计的位置，仅当 `show-word-limit` 为 `true` 时生效。 | `enum` | "inside" |
| placeholder | 输入框占位文本 | `string` | — |
| clearable | 是否显示清除按钮，只有当 `type` 不是 textarea时生效 | `boolean` | false |
| clear-icon 2.11.0 | 自定义清除图标 | `string` / `object` | CircleClose |
| formatter | 指定输入值的格式。(只有当 `type` 是"text"时才能工作) | `Function` | — |
| parser | 指定从格式化器输入中提取的值。(仅当 `type` 是"text"时才起作用) | `Function` | — |
| show-password | 是否显示切换密码图标 | `boolean` | false |
| disabled | 是否禁用 | `boolean` | false |
| size | 输入框尺寸，只在 `type` 不为 'textarea' 时有效 | `enum` | — |
| prefix-icon | 自定义前缀图标 | `string` / `Component` | — |
| suffix-icon | 自定义后缀图标 | `string` / `Component` | — |
| rows | 输入框行数，仅 `type` 为 'textarea' 时有效 | `number` | 2 |
| autosize | textarea 高度是否自适应，仅 `type` 为 'textarea' 时生效。 可以接受一个对象，比如: `{ minRows: 2, maxRows: 6 }` | `boolean` / `object` | false |
| autocomplete | 原生 `autocomplete` 属性 | `string` | off |
| name | 等价于原生 input `name` 属性 | `string` | — |
| readonly | 原生 `readonly` 属性，是否只读 | `boolean` | false |
| max | 原生 `max` 属性，设置最大值 | — | — |
| min | 原生属性，设置最小值 | — | — |
| step | 原生属性，设置输入字段的合法数字间隔 | ::: | — |
| resize | 控制是否能被用户缩放 | `enum` | — |
| autofocus | 原生属性，自动获取焦点 | `boolean` | false |
| form | 原生属性 | `string` | — |
| aria-label a11y 2.7.2 | 等价于原生 input `aria-label` 属性 | `string` | — |
| tabindex | 输入框的 tabindex | `string` / `number` | — |
| validate-event | 输入时是否触发表单的校验 | `boolean` | true |
| input-style | input 元素或 textarea 元素的 style | `string` / `object` | {} |
| label a11y deprecated | 等价于原生 input `aria-label` 属性 | `string` | — |
| inputmode 2.10.3 | 等价于原生 input `inputmode` 属性 | `string` | — |
| count-graphemes 2.13.7 | 自定义函数用于计算字形；设置后，将绕过原生的 `maxlength`/`minlength` 约束。 组件使用 `Intl.Segmenter`（Chrome 87+、Firefox 125+、Safari 14.1+）进行正确的字素聚类；旧版浏览器回退到使用 `Array.from()` 进行码点迭代。 | `Function` | — |

### Events [​](#events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| blur | 当选择器的输入框失去焦点时触发 | `Function` |
| focus | 当选择器的输入框获得焦点时触发 | `Function` |
| change | 仅当 modelValue 改变时，当输入框失去焦点或用户按Enter时触发 | `Function` |
| input | 在 Input 值改变时触发 | `Function` |
| clear | 在点击由 `clearable` 属性生成的清空按钮时触发 | `Function` |
| keydown | 按下键时触发 | `Function` |
| mouseleave | 当鼠标离开输入元素时触发 | `Function` |
| mouseenter | 当鼠标进入输入元素时触发 | `Function` |
| compositionstart | 输入法输入开始时触发 | `Function` |
| compositionupdate | 输入法输入改变时触发 | `Function` |
| compositionend | 输入法输入完成时触发 | `Function` |

### Slots [​](#slots)

| 插槽名 | 说明 |
| --- | --- |
| prefix | 输入框头部内容，只对非 `type="textarea"` 有效 |
| suffix | 输入框尾部内容，只对非 `type="textarea"` 有效 |
| prepend | 输入框前置内容，只对非 `type="textarea"` 有效 |
| append | 输入框后置内容，只对非 `type="textarea"` 有效 |
| password-icon 2.13.6 | 作为输入密码图标的内容，仅在 `show-password` 为 true 时生效。 作用域变量为 `{ visible: boolean }` |

### Exposes [​](#exposes)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| blur | 使 input 失去焦点 | `Function` |
| clear | 清除 input 值 | `Function` |
| focus | 使 input 获取焦点 | `Function` |
| input | Input HTML 元素 | `object` |
| ref | HTML元素 input 或 textarea | `object` |
| resizeTextarea | 改变 textarea 大小 | `Function` |
| select | 选中 input 中的文字 | `Function` |
| textarea | HTML textarea 元素 | `object` |
| textareaStyle | textarea 的样式 | `object` |
| isComposing 2.8.0 | 是否是输入 composing 状态 | `object` |
| passwordVisible 2.13.7 | 密码是否可见 | `object` |

## 常见问题 [​](#常见问题)

#### ElInput 组件的宽度为什么在设置了 `clearable` 时会发生变化 [​](#elinput-组件的宽度为什么在设置了-clearable-时会发生变化)

典型问题： [#7287](https://github.com/element-plus/element-plus/issues/7287)

PS: 由于ElInput 组件没有默认宽度，当显示 clearable 图标时, 组件的宽度将被撑开，可以通过设置固定宽度属性来解决。

vue

```
<el-input v-model="input" clearable style="width: 200px" />
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/input) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/input.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/input.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/101238421?v=4&size=64)](https://github.com/acyza)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/5283258?v=4&size=64)](https://github.com/satrong)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/47766606?v=4&size=64)](https://github.com/ls57765867)[![](https://avatars.githubusercontent.com/u/71313168?v=4&size=64)](https://github.com/cc-hearts)[![](https://avatars.githubusercontent.com/u/49630878?v=4&size=64)](https://github.com/a869246700)[![](https://avatars.githubusercontent.com/u/22286818?v=4&size=64)](https://github.com/fratzinger)[![](https://avatars.githubusercontent.com/u/5850779?v=4&size=64)](https://github.com/IllegalCreed)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/28857867?v=4&size=64)](https://github.com/qq1037305420)[![](https://avatars.githubusercontent.com/u/6777923?v=4&size=64)](https://github.com/markpro-code)[![](https://avatars.githubusercontent.com/u/50254496?v=4&size=64)](https://github.com/LoTwT)[![](https://avatars.githubusercontent.com/u/26403700?v=4&size=64)](https://github.com/blesstosam)[![](https://avatars.githubusercontent.com/u/27912232?v=4&size=64)](https://github.com/Fuphoenixes)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/109908413?v=4&size=64)](https://github.com/sleepyShen1989)[![](https://avatars.githubusercontent.com/u/66891653?v=4&size=64)](https://github.com/YoungDan-hero)[![](https://avatars.githubusercontent.com/u/56245609?v=4&size=64)](https://github.com/pzzyf)[![](https://avatars.githubusercontent.com/u/55378595?v=4&size=64)](https://github.com/evanryuu)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/30046649?v=4&size=64)](https://github.com/MrWeilian)[![](https://avatars.githubusercontent.com/u/126545033?v=4&size=64)](https://github.com/dhj-l)[![](https://avatars.githubusercontent.com/u/57179957?v=4&size=64)](https://github.com/yeonjulee1005)[![](https://avatars.githubusercontent.com/u/48373109?v=4&size=64)](https://github.com/yuchiXiong)[![](https://avatars.githubusercontent.com/u/33423008?v=4&size=64)](https://github.com/shigma)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/28089690?v=4&size=64)](https://github.com/daonatural)[![](https://avatars.githubusercontent.com/u/4318293?v=4&size=64)](https://github.com/cn-troy)[![](https://avatars.githubusercontent.com/u/23720738?v=4&size=64)](https://github.com/kouchao)[![](https://avatars.githubusercontent.com/u/34675975?v=4&size=64)](https://github.com/dreamqyq)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/32129111?v=4&size=64)](https://github.com/Vgbire)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/22190579?v=4&size=64)](https://github.com/wangerzi)[![](https://avatars.githubusercontent.com/u/32960305?v=4&size=64)](https://github.com/KimYangOfCat)[![](https://avatars.githubusercontent.com/u/25458528?v=4&size=64)](https://github.com/weidehai)[![](https://avatars.githubusercontent.com/u/32354856?v=4&size=64)](https://github.com/baiwusanyu-c)[![](https://avatars.githubusercontent.com/u/18349295?v=4&size=64)](https://github.com/zt123123)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/45936772?v=4&size=64)](https://github.com/KawaiiZapic)[![](https://avatars.githubusercontent.com/u/39672197?v=4&size=64)](https://github.com/bchen1029)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)

[Form 表单组件](https://element-plus.org/zh-CN/component/form)

[Input Number 数字输入框](https://element-plus.org/zh-CN/component/input-number)


