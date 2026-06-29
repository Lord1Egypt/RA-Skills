---
name: "rate"
description: "Rate 评分 -- Element Plus Vue3 桌面端组件。Invoke when user needs Rate 评分 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/rate.html"
---

---

# Rate 评分 [​](#rate-评分)

更新日志待解决

1

用于评分

## 基础用法 [​](#基础用法)

评分默认被分为三个等级，可以利用颜色数组对分数及情感倾向进行分级（默认情况下不区分颜色）。 三个等级所对应的颜色用 `colors` 属性设置，而它们对应的两个阈值则通过 `low-threshold` 和 `high-threshold` 设定。

Default

Color for different levels

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1yYXRlLWJsb2NrXCI+XG4gICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+RGVmYXVsdDwvc3Bhbj5cbiAgICA8ZWwtcmF0ZSB2LW1vZGVsPVwidmFsdWUxXCIgLz5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJkZW1vLXJhdGUtYmxvY2tcIj5cbiAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5Db2xvciBmb3IgZGlmZmVyZW50IGxldmVsczwvc3Bhbj5cbiAgICA8ZWwtcmF0ZSB2LW1vZGVsPVwidmFsdWUyXCIgOmNvbG9ycz1cImNvbG9yc1wiIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUxID0gcmVmKDApXG5jb25zdCB2YWx1ZTIgPSByZWYoMClcbmNvbnN0IGNvbG9ycyA9IHJlZihbJyM5OUE5QkYnLCAnI0Y3QkEyQScsICcjRkY5OTAwJ10pIC8vIHNhbWUgYXMgeyAyOiAnIzk5QTlCRicsIDQ6IHsgdmFsdWU6ICcjRjdCQTJBJywgZXhjbHVkZWQ6IHRydWUgfSwgNTogJyNGRjk5MDAnIH1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRlbW8tcmF0ZS1ibG9jayB7XG4gIHBhZGRpbmc6IDMwcHggMDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBib3JkZXItcmlnaHQ6IHNvbGlkIDFweCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICBkaXNwbGF5OiBpbmxpbmUtYmxvY2s7XG4gIHdpZHRoOiA0OSU7XG4gIGJveC1zaXppbmc6IGJvcmRlci1ib3g7XG59XG4uZGVtby1yYXRlLWJsb2NrOmxhc3QtY2hpbGQge1xuICBib3JkZXItcmlnaHQ6IG5vbmU7XG59XG4uZGVtby1yYXRlLWJsb2NrIC5kZW1vbnN0cmF0aW9uIHtcbiAgZGlzcGxheTogYmxvY2s7XG4gIGNvbG9yOiB2YXIoLS1lbC10ZXh0LWNvbG9yLXNlY29uZGFyeSk7XG4gIGZvbnQtc2l6ZTogMTRweDtcbiAgbWFyZ2luLWJvdHRvbTogMjBweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/rate/basic-usage.vue)_

vue

```
<template>
  <div class="demo-rate-block">
    <span class="demonstration">Default</span>
    <el-rate v-model="value1" />
  </div>
  <div class="demo-rate-block">
    <span class="demonstration">Color for different levels</span>
    <el-rate v-model="value2" :colors="colors" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref(0)
const value2 = ref(0)
const colors = ref(['#99A9BF', '#F7BA2A', '#FF9900']) // same as { 2: '#99A9BF', 4: { value: '#F7BA2A', excluded: true }, 5: '#FF9900' }
</script>

<style scoped>
.demo-rate-block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 49%;
  box-sizing: border-box;
}
.demo-rate-block:last-child {
  border-right: none;
}
.demo-rate-block .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
```

隐藏源代码

## 尺寸 [​](#尺寸)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmF0ZSB2LW1vZGVsPVwidmFsdWVcIiBzaXplPVwibGFyZ2VcIiAvPlxuICA8YnIgLz5cbiAgPGVsLXJhdGUgdi1tb2RlbD1cInZhbHVlXCIgLz5cbiAgPGJyIC8+XG4gIDxlbC1yYXRlIHYtbW9kZWw9XCJ2YWx1ZVwiIHNpemU9XCJzbWFsbFwiIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZigwKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/rate/sizes.vue)_

vue

```
<template>
  <el-rate v-model="value" size="large" />
  <br />
  <el-rate v-model="value" />
  <br />
  <el-rate v-model="value" size="small" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref(0)
</script>
```

隐藏源代码

## 允许半选 [​](#允许半选)

属性 `allow-half` 允许出现半星

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmF0ZSB2LW1vZGVsPVwidmFsdWVcIiBhbGxvdy1oYWxmIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZigpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/rate/allow-half.vue)_

vue

```
<template>
  <el-rate v-model="value" allow-half />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()
</script>
```

隐藏源代码

## 辅助文字 [​](#辅助文字)

用辅助文字直接地表达对应分数

为组件设置 `show-text` 属性会在右侧显示辅助文字。 通过设置 `texts` 可以为每一个分值指定对应的辅助文字。 `texts` 为一个数组，长度应等于最大值 `max`。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmF0ZVxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOnRleHRzPVwiWydvb3BzJywgJ2Rpc2FwcG9pbnRlZCcsICdub3JtYWwnLCAnZ29vZCcsICdncmVhdCddXCJcbiAgICBzaG93LXRleHRcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKClcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/rate/text.vue)_

vue

```
<template>
  <el-rate
    v-model="value"
    :texts="['oops', 'disappointed', 'normal', 'good', 'great']"
    show-text
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()
</script>
```

隐藏源代码

## 可清空 [​](#可清空)

当你再次点击相同的值时，可以将值重置为 `0`。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmF0ZSB2LW1vZGVsPVwidmFsdWVcIiBjbGVhcmFibGUgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKDMpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/rate/clearable.vue)_

vue

```
<template>
  <el-rate v-model="value" clearable />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref(3)
</script>
```

隐藏源代码

## 更多种类的图标 [​](#更多种类的图标)

当有多层评价时，可以用不同类型的图标区分评分层级。

设置`icons`属性可以自定义不同分段的图标。 若传入数组，共有 3 个元素，为 3 个分段所对应的类名；若传入对象，可自定义分段，键名为分段的界限值，键值为对应的类名。 本例还使用 `void-icon` 指定了未选中时的图标类名。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmF0ZVxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgOmljb25zPVwiaWNvbnNcIlxuICAgIDp2b2lkLWljb249XCJDaGF0Um91bmRcIlxuICAgIDpjb2xvcnM9XCJbJyM0MDllZmYnLCAnIzY3YzIzYScsICcjRkY5OTAwJ11cIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IENoYXREb3RSb3VuZCwgQ2hhdExpbmVSb3VuZCwgQ2hhdFJvdW5kIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKClcbmNvbnN0IGljb25zID0gW0NoYXRSb3VuZCwgQ2hhdExpbmVSb3VuZCwgQ2hhdERvdFJvdW5kXSAvLyBzYW1lIGFzIHsgMjogQ2hhdFJvdW5kLCA0OiB7IHZhbHVlOiBDaGF0TGluZVJvdW5kLCBleGNsdWRlZDogdHJ1ZSB9LCA1OiBDaGF0RG90Um91bmQgfVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/rate/more-icons.vue)_

vue

```
<template>
  <el-rate
    v-model="value"
    :icons="icons"
    :void-icon="ChatRound"
    :colors="['#409eff', '#67c23a', '#FF9900']"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ChatDotRound, ChatLineRound, ChatRound } from '@element-plus/icons-vue'

const value = ref()
const icons = [ChatRound, ChatLineRound, ChatDotRound] // same as { 2: ChatRound, 4: { value: ChatLineRound, excluded: true }, 5: ChatDotRound }
</script>
```

隐藏源代码

## 只读 [​](#只读)

只读的评分用来展示分数， 允许出现半星。

为组件设置 `disabled` 属性表示组件为只读。 此时若设置 `show-score`，则会在右侧显示目前的分值。 此外，您可以使用属性 `score-template` 来提供评分模板。 模板为一个包含了 `{value}` 的字符串，`{value}` 会被替换为当前分值。

3.7 points

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmF0ZVxuICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgZGlzYWJsZWRcbiAgICBzaG93LXNjb3JlXG4gICAgdGV4dC1jb2xvcj1cIiNmZjk5MDBcIlxuICAgIHNjb3JlLXRlbXBsYXRlPVwie3ZhbHVlfSBwb2ludHNcIlxuICAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoMy43KVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/rate/readonly.vue)_

vue

```
<template>
  <el-rate
    v-model="value"
    disabled
    show-score
    text-color="#ff9900"
    score-template="{value} points"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref(3.7)
</script>
```

隐藏源代码

## 自定义样式 [​](#自定义样式)

您可以为 rate 组件设定自定义样式。 使用 `css` 或 `scss` 改变全局或局部的颜色。 我们设置了一些全局颜色变量：`--el-rate-void-color`、`--el-rate-fill-color`、`--el-rate-disabled-void-color` 和 `--el-rate-text-color`。 您可以像这样使用：`:root { --el-rate-void-color: red; --el-rate-fill-color: blue; }`。

### 默认变量 [​](#默认变量)

| 变量 | 默认颜色 |
| --- | --- |
| \--el-rate-void-color | var(--el-border-color-darker) |
| \--el-rate-fill-color | #f7ba2a |
| \--el-rate-disabled-void-color | var(--el-fill-color) |
| \--el-rate-text-color | var(--el-text-color-primary) |

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `number` | 0 |
| max | 最大分值 | `number` | 5 |
| size | 尺寸 | `enum` | — |
| disabled | 是否为只读 | `boolean` | false |
| allow-half | 是否允许半选 | `boolean` | false |
| low-threshold | 低分和中等分数的界限值， 值本身被划分在低分中 | `number` | 2 |
| high-threshold | 高分和中等分数的界限值， 值本身被划分在高分中 | `number` | 4 |
| colors | icon 的颜色。 若传入数组，共有 3 个元素，为 3 个分段所对应的颜色；若传入对象，可自定义分段，键名为分段的界限值，键值为对应的颜色 | `array` / `object` | \['#f7ba2a', '#f7ba2a', '#f7ba2a'\] |
| void-color | 未选中 icon 的颜色 | `string` | #c6d1de |
| disabled-void-color | 只读时未选中 icon 的颜色 | `string` | #eff2f7 |
| icons | 图标组件 若传入数组，则需要传入 3 个元素，分别为 3 个部分所对应的类名；若传入对象，则可自定义分段，键名为分段的界限值，键值为对应的类名 | `array` / `object` | \[StarFilled, StarFilled, StarFilled\] |
| void-icon | 未被选中的图标组件 | `string` / `Component` | Star |
| disabled-void-icon | 禁用状态的未选择图标 | `string` / `Component` | StarFilled |
| show-text | 是否显示辅助文字，若为真，则会从 texts 数组中选取当前分数对应的文字内容 | `boolean` | false |
| show-score | 是否显示当前分数， show-score 和 show-text 不能同时为真 | `boolean` | false |
| text-color | 辅助文字的颜色 | `string` | '' |
| texts | 辅助文字数组 | `array` | \['Extremely bad', 'Disappointed', 'Fair', 'Satisfied', 'Surprise'\] |
| score-template | 分数显示模板 | `string` |  |
| clearable 2.2.18 | 是否可以重置值为 `0` | `boolean` | false |
| id | 原生 `id` 属性 | `string` | — |
| aria-label a11y 2.7.2 | 和 Rate 的 `aria-label` 属性保持一致 | `string` | — |
| label a11y deprecated | 和 Rate 的 `aria-label` 属性保持一致 | `string` | — |

### Events [​](#events)

| 事件名 | 描述说明 | 类型 |
| --- | --- | --- |
| change | 分值改变时触发 | `Function` |

### Exposes [​](#exposes)

| 名称 | 描述 | 类型 |
| --- | --- | --- |
| setCurrentValue | 设置当前值 | `Function` |
| resetCurrentValue | 重置当前值 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/rate) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/rate.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/rate.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/71313168?v=4&size=64)](https://github.com/cc-hearts)[![](https://avatars.githubusercontent.com/u/75007029?v=4&size=64)](https://github.com/yj-liuzepeng)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/31391693?v=4&size=64)](https://github.com/Shana-AE)[![](https://avatars.githubusercontent.com/u/33497338?v=4&size=64)](https://github.com/MoConWu)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/40431305?v=4&size=64)](https://github.com/Notryag)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/33979706?v=4&size=64)](https://github.com/jizai1125)[![](https://avatars.githubusercontent.com/u/36811055?v=4&size=64)](https://github.com/iDestin)

[Radio 单选框](https://element-plus.org/zh-CN/component/radio)

[Select](https://element-plus.org/zh-CN/component/select)


