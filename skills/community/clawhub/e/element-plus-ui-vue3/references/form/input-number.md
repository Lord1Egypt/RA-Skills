---
name: "input-number"
description: "Input Number 数字输入框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Input Number 数字输入框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/input-number.html"
---

---

# Input Number 数字输入框 [​](#input-number-数字输入框)

更新日志待解决

14

仅允许输入标准的数字值，可定义范围

## 基础用法 [​](#基础用法)

要使用它，只需要在 `<el-input-number>` 元素中使用 `v-model` 绑定变量即可，变量的初始值即为默认值。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtbnVtYmVyIHYtbW9kZWw9XCJudW1cIiA6bWluPVwiMVwiIDptYXg9XCIxMFwiIEBjaGFuZ2U9XCJoYW5kbGVDaGFuZ2VcIiAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgbnVtID0gcmVmKDEpXG5jb25zdCBoYW5kbGVDaGFuZ2UgPSAodmFsdWU6IG51bWJlciB8IHVuZGVmaW5lZCkgPT4ge1xuICBjb25zb2xlLmxvZyh2YWx1ZSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-number/basic.vue)_

vue

```
<template>
  <el-input-number v-model="num" :min="1" :max="10" @change="handleChange" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(1)
const handleChange = (value: number | undefined) => {
  console.log(value)
}
</script>
```

隐藏源代码

TIP

当输入无效的字符串到输入框时，由于错误，输入值将把 `NaN` 导入到上层

## 禁用状态 [​](#禁用状态)

`disabled`属性接受一个 `Boolean`，设置为`true`即可禁用整个组件。 ，如果你只需要控制数值在某一范围内，可以设置 `min` 属性和 `max` 属性， 默认情况下，最小值是 `Number.MIN_SAFE_INTEGER`。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtbnVtYmVyIHYtbW9kZWw9XCJudW1cIiA6ZGlzYWJsZWQ9XCJ0cnVlXCIgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IG51bSA9IHJlZigxKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-number/disabled.vue)_

vue

```
<template>
  <el-input-number v-model="num" :disabled="true" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(1)
</script>
```

隐藏源代码

## 步进 [​](#步进)

允许定义递增递减的步进控制

设置 `step` 属性可以控制步长。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtbnVtYmVyIHYtbW9kZWw9XCJudW1cIiA6c3RlcD1cIjJcIiAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgbnVtID0gcmVmKDUpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-number/steps.vue)_

vue

```
<template>
  <el-input-number v-model="num" :step="2" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(5)
</script>
```

隐藏源代码

## 严格步进 [​](#严格步进)

`step-strictly`属性接受一个`Boolean`。 如果这个属性被设置为 `true`，则只能输入步进的倍数。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtbnVtYmVyIHYtbW9kZWw9XCJudW1cIiA6c3RlcD1cIjJcIiBzdGVwLXN0cmljdGx5IC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBudW0gPSByZWYoMilcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-number/step-strictly.vue)_

vue

```
<template>
  <el-input-number v-model="num" :step="2" step-strictly />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(2)
</script>
```

隐藏源代码

## 精度 [​](#精度)

设置 `precision` 属性可以控制数值精度，接收一个 `Number`。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtbnVtYmVyIHYtbW9kZWw9XCJudW1cIiA6cHJlY2lzaW9uPVwiMlwiIDpzdGVwPVwiMC4xXCIgOm1heD1cIjEwXCIgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IG51bSA9IHJlZigxKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-number/precision.vue)_

vue

```
<template>
  <el-input-number v-model="num" :precision="2" :step="0.1" :max="10" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(1)
</script>
```

隐藏源代码

TIP

`precision` 的值必须是一个非负整数，并且不能小于 `step` 的小数位数。

## 不同的输入框尺寸 [​](#不同的输入框尺寸)

使用 `size` 属性额外配置尺寸，可选的尺寸大小为：`large` 或 `small`

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgaXRlbXMtY2VudGVyIGdhcC00XCI+XG4gICAgPGVsLWlucHV0LW51bWJlciB2LW1vZGVsPVwibnVtMVwiIHNpemU9XCJsYXJnZVwiIC8+XG4gICAgPGVsLWlucHV0LW51bWJlciB2LW1vZGVsPVwibnVtMlwiIC8+XG4gICAgPGVsLWlucHV0LW51bWJlciB2LW1vZGVsPVwibnVtM1wiIHNpemU9XCJzbWFsbFwiIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgbnVtMSA9IHJlZigxKVxuY29uc3QgbnVtMiA9IHJlZigyKVxuY29uc3QgbnVtMyA9IHJlZigzKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-number/size.vue)_

vue

```
<template>
  <div class="flex flex-wrap items-center gap-4">
    <el-input-number v-model="num1" size="large" />
    <el-input-number v-model="num2" />
    <el-input-number v-model="num3" size="small" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num1 = ref(1)
const num2 = ref(2)
const num3 = ref(3)
</script>
```

隐藏源代码

## 按钮位置 [​](#按钮位置)

设置 `controls-position` 属性可以控制按钮位置。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgaXRlbXMtY2VudGVyIGdhcC00XCI+XG4gICAgPGVsLWlucHV0LW51bWJlclxuICAgICAgdi1tb2RlbD1cIm51bVwiXG4gICAgICA6bWluPVwiMVwiXG4gICAgICA6bWF4PVwiMTBcIlxuICAgICAgY29udHJvbHMtcG9zaXRpb249XCJyaWdodFwiXG4gICAgICBzaXplPVwibGFyZ2VcIlxuICAgICAgQGNoYW5nZT1cImhhbmRsZUNoYW5nZVwiXG4gICAgLz5cbiAgICA8ZWwtaW5wdXQtbnVtYmVyXG4gICAgICB2LW1vZGVsPVwibnVtXCJcbiAgICAgIDptaW49XCIxXCJcbiAgICAgIDptYXg9XCIxMFwiXG4gICAgICBjb250cm9scy1wb3NpdGlvbj1cInJpZ2h0XCJcbiAgICAgIEBjaGFuZ2U9XCJoYW5kbGVDaGFuZ2VcIlxuICAgIC8+XG4gICAgPGVsLWlucHV0LW51bWJlclxuICAgICAgdi1tb2RlbD1cIm51bVwiXG4gICAgICA6bWluPVwiMVwiXG4gICAgICA6bWF4PVwiMTBcIlxuICAgICAgc2l6ZT1cInNtYWxsXCJcbiAgICAgIGNvbnRyb2xzLXBvc2l0aW9uPVwicmlnaHRcIlxuICAgICAgQGNoYW5nZT1cImhhbmRsZUNoYW5nZVwiXG4gICAgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBudW0gPSByZWYoMSlcbmNvbnN0IGhhbmRsZUNoYW5nZSA9ICh2YWx1ZTogbnVtYmVyIHwgdW5kZWZpbmVkKSA9PiB7XG4gIGNvbnNvbGUubG9nKHZhbHVlKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-number/controlled.vue)_

vue

```
<template>
  <div class="flex flex-wrap items-center gap-4">
    <el-input-number
      v-model="num"
      :min="1"
      :max="10"
      controls-position="right"
      size="large"
      @change="handleChange"
    />
    <el-input-number
      v-model="num"
      :min="1"
      :max="10"
      controls-position="right"
      @change="handleChange"
    />
    <el-input-number
      v-model="num"
      :min="1"
      :max="10"
      size="small"
      controls-position="right"
      @change="handleChange"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(1)
const handleChange = (value: number | undefined) => {
  console.log(value)
}
</script>
```

隐藏源代码

## 自定义图标 2.6.3 [​](#自定义图标)

使用 `decrease-icon` 和 `increase-icon` 设置自定义图标。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgZGlyZWN0aW9uPVwidmVydGljYWxcIj5cbiAgICA8ZWwtc3BhY2U+XG4gICAgICA8ZWwtaW5wdXQtbnVtYmVyIHYtbW9kZWw9XCJudW1cIiAvPlxuICAgICAgPGVsLWlucHV0LW51bWJlciB2LW1vZGVsPVwibnVtXCI+XG4gICAgICAgIDx0ZW1wbGF0ZSAjZGVjcmVhc2UtaWNvbj5cbiAgICAgICAgICA8ZWwtaWNvbj5cbiAgICAgICAgICAgIDxBcnJvd0Rvd24gLz5cbiAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgIDx0ZW1wbGF0ZSAjaW5jcmVhc2UtaWNvbj5cbiAgICAgICAgICA8ZWwtaWNvbj5cbiAgICAgICAgICAgIDxBcnJvd1VwIC8+XG4gICAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgPC9lbC1pbnB1dC1udW1iZXI+XG4gICAgPC9lbC1zcGFjZT5cbiAgICA8ZWwtc3BhY2U+XG4gICAgICA8ZWwtaW5wdXQtbnVtYmVyIHYtbW9kZWw9XCJudW1cIiBjb250cm9scy1wb3NpdGlvbj1cInJpZ2h0XCIgLz5cbiAgICAgIDxlbC1pbnB1dC1udW1iZXIgdi1tb2RlbD1cIm51bVwiIGNvbnRyb2xzLXBvc2l0aW9uPVwicmlnaHRcIj5cbiAgICAgICAgPHRlbXBsYXRlICNkZWNyZWFzZS1pY29uPlxuICAgICAgICAgIDxlbC1pY29uPlxuICAgICAgICAgICAgPE1pbnVzIC8+XG4gICAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICA8dGVtcGxhdGUgI2luY3JlYXNlLWljb24+XG4gICAgICAgICAgPGVsLWljb24+XG4gICAgICAgICAgICA8UGx1cyAvPlxuICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtaW5wdXQtbnVtYmVyPlxuICAgIDwvZWwtc3BhY2U+XG4gIDwvZWwtc3BhY2U+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgQXJyb3dEb3duLCBBcnJvd1VwLCBNaW51cywgUGx1cyB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5jb25zdCBudW0gPSByZWYoMSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-number/custom.vue)_

vue

```
<template>
  <el-space direction="vertical">
    <el-space>
      <el-input-number v-model="num" />
      <el-input-number v-model="num">
        <template #decrease-icon>
          <el-icon>
            <ArrowDown />
          </el-icon>
        </template>
        <template #increase-icon>
          <el-icon>
            <ArrowUp />
          </el-icon>
        </template>
      </el-input-number>
    </el-space>
    <el-space>
      <el-input-number v-model="num" controls-position="right" />
      <el-input-number v-model="num" controls-position="right">
        <template #decrease-icon>
          <el-icon>
            <Minus />
          </el-icon>
        </template>
        <template #increase-icon>
          <el-icon>
            <Plus />
          </el-icon>
        </template>
      </el-input-number>
    </el-space>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ArrowDown, ArrowUp, Minus, Plus } from '@element-plus/icons-vue'

const num = ref(1)
</script>
```

隐藏源代码

## 带前缀和后缀2.8.4 [​](#带前缀和后缀)

使用前缀和标名后缀。

￥

RMB

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2U+XG4gICAgPGVsLWlucHV0LW51bWJlciB2LW1vZGVsPVwibnVtXCIgOm1pbj1cIjFcIiA6bWF4PVwiMTBcIj5cbiAgICAgIDx0ZW1wbGF0ZSAjcHJlZml4PlxuICAgICAgICA8c3Bhbj7vv6U8L3NwYW4+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtaW5wdXQtbnVtYmVyPlxuICAgIDxlbC1pbnB1dC1udW1iZXIgdi1tb2RlbD1cIm51bVwiIDptaW49XCIxXCIgOm1heD1cIjEwXCI+XG4gICAgICA8dGVtcGxhdGUgI3N1ZmZpeD5cbiAgICAgICAgPHNwYW4+Uk1CPC9zcGFuPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWlucHV0LW51bWJlcj5cbiAgPC9lbC1zcGFjZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IG51bSA9IHJlZigxKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-number/with-prefix-suffix.vue)_

vue

```
<template>
  <el-space>
    <el-input-number v-model="num" :min="1" :max="10">
      <template #prefix>
        <span>￥</span>
      </template>
    </el-input-number>
    <el-input-number v-model="num" :min="1" :max="10">
      <template #suffix>
        <span>RMB</span>
      </template>
    </el-input-number>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const num = ref(1)
</script>
```

隐藏源代码

TIP

为了确保精度，输入的数值被限制在 [Number.MIN\_SAFE\_INTEGER](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MIN_SAFE_INTEGER) 到 [Number.MAX\_SAFE\_INTEGER](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER) 之间。

## Formatter 2.14.0 [​](#formatter)

使用 `formatter` 来显示值，通常会同时配合 `parser` 一起使用。

当设置了 `formatter` 时，内部输入框的 `type` 会变为 `text`，从而允许输入非数字字符。 组件内部使用 `Number.parseFloat` 处理输入：解析成功时，将解析后的数值写入 `model-value`；当解析结果为 `NaN` 时，将 `model-value` 设为 `null`。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtaW5wdXQtbnVtYmVyXG4gICAgdi1tb2RlbD1cImlucHV0XCJcbiAgICA6Zm9ybWF0dGVyPVwiKHZhbHVlKSA9PiBgJCAke3ZhbHVlfWAucmVwbGFjZSgvXFxCKD89KFxcZHszfSkrKD8hXFxkKSkvZywgJywnKVwiXG4gICAgOnBhcnNlcj1cIih2YWx1ZSkgPT4gdmFsdWUucmVwbGFjZSgvXFwkXFxzP3woLCopL2csICcnKVwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBpbnB1dCA9IHJlZigxMDAwMClcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/input-number/formatter.vue)_

vue

```
<template>
  <el-input-number
    v-model="input"
    :formatter="(value) => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')"
    :parser="(value) => value.replace(/\$\s?|(,*)/g, '')"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref(10000)
</script>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `number` / `null` | — |
| min | 设置计数器允许的最小值 | `number` | Number.MIN\_SAFE\_INTEGER |
| max | 设置计数器允许的最大值 | `number` | Number.MAX\_SAFE\_INTEGER |
| step | 计数器步长 | `number` | 1 |
| step-strictly | 是否只能输入 step 的倍数 | `boolean` | false |
| precision | 数值精度 | `number` | — |
| size | 计数器尺寸 | `enum` | default |
| readonly 2.2.16 | 原生 `readonly` 属性，是否只读 | `boolean` | false |
| disabled | 是否禁用状态 | `boolean` | false |
| controls | 是否使用控制按钮 | `boolean` | true |
| controls-position | 控制按钮位置 | `enum` | — |
| name | 等价于原生 input `name` 属性 | `string` | — |
| aria-label a11y 2.7.2 | 等价于原生 input `aria-label` 属性 | `string` | — |
| placeholder | 等价于原生 input `placeholder` 属性 | `string` | — |
| id | 等价于原生 input `id` 属性 | `string` | — |
| value-on-clear 2.2.0 | 当输入框被清空时显示的值 | `number` / `null` / `enum` | — |
| validate-event | 是否触发表单验证 | `boolean` | true |
| label a11y deprecated | 等价于原生 input `aria-label` 属性 | `string` | — |
| inputmode 2.10.3 | 等价于原生 input `inputmode` 属性 | `string` | — |
| align 2.10.5 | 内部输入文本对齐 | `enum` | 'center' |
| disabled-scientific 2.10.5 | 禁用科学计数法的输入（例如输入 'e'） | `boolean` | false |
| tabindex 2.14.0 | 输入框的 tabindex | `string` / `number` | 0 |
| formatter 2.14.0 | 指定输入值的格式 | `Function` | ::: |
| parser 2.14.0 | 指定从格式化输入中提取的值 | `Function` | — |

### Slots [​](#slots)

| 插槽名 | 说明 |
| --- | --- |
| decrease-icon 2.6.3 | 自定义输入框按钮减少图标 |
| increase-icon 2.6.3 | 自定义输入框按钮增加图标 |
| prefix 2.8.4 | 输入框头部内容 |
| suffix 2.8.4 | 输入框尾部内容 |

### Events [​](#events)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| change | 绑定值被改变时触发 | `Function` |
| blur | 在组件 Input 失去焦点时触发 | `Function` |
| focus | 在组件 Input 获得焦点时触发 | `Function` |

### Exposes [​](#exposes)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| focus | 使 input 组件获得焦点 | `Function` |
| blur | 使 input 组件失去焦点 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/input-number) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/input-number.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/input-number.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/42017165?v=4&size=64)](https://github.com/Mario34)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/7877834?v=4&size=64)](https://github.com/921)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/71313168?v=4&size=64)](https://github.com/cc-hearts)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/22286818?v=4&size=64)](https://github.com/fratzinger)[![](https://avatars.githubusercontent.com/u/119273236?v=4&size=64)](https://github.com/XL-YiBai)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/84778445?v=4&size=64)](https://github.com/yuxi-ovo)[![](https://avatars.githubusercontent.com/u/47178158?v=4&size=64)](https://github.com/Aaron-zon)[![](https://avatars.githubusercontent.com/u/80440359?v=4&size=64)](https://github.com/guze2003)[![](https://avatars.githubusercontent.com/u/30970336?v=4&size=64)](https://github.com/KESHAOYE)[![](https://avatars.githubusercontent.com/u/84954229?v=4&size=64)](https://github.com/Canroc)[![](https://avatars.githubusercontent.com/u/69418751?v=4&size=64)](https://github.com/selicens)[![](https://avatars.githubusercontent.com/u/97817985?v=4&size=64)](https://github.com/nova1751)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/86777555?v=4&size=64)](https://github.com/zhengsixsix)[![](https://avatars.githubusercontent.com/u/109908413?v=4&size=64)](https://github.com/sleepyShen1989)[![](https://avatars.githubusercontent.com/u/22910740?v=4&size=64)](https://github.com/StephenKe)[![](https://avatars.githubusercontent.com/u/32354856?v=4&size=64)](https://github.com/baiwusanyu-c)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/55891373?v=4&size=64)](https://github.com/so11y)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/17810772?v=4&size=64)](https://github.com/dingyuanjie)[![](https://avatars.githubusercontent.com/u/48650709?v=4&size=64)](https://github.com/MARIOMARUI)[![](https://avatars.githubusercontent.com/u/75007029?v=4&size=64)](https://github.com/yj-liuzepeng)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/26833520?v=4&size=64)](https://github.com/josonho)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/45936772?v=4&size=64)](https://github.com/KawaiiZapic)[![](https://avatars.githubusercontent.com/u/18051955?v=4&size=64)](https://github.com/qige2016)[![](https://avatars.githubusercontent.com/u/2755933?v=4&size=64)](https://github.com/BiosSun)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/8591261?v=4&size=64)](https://github.com/zeyongTsai)[![](https://avatars.githubusercontent.com/u/25502024?v=4&size=64)](https://github.com/imguolao)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)

[Input 输入框](https://element-plus.org/zh-CN/component/input)

[Input Tag 标签输入框](https://element-plus.org/zh-CN/component/input-tag)


