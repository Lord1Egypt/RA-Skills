---
name: "steps"
description: "Steps 步骤条 -- Element Plus Vue3 桌面端组件。Invoke when user needs Steps 步骤条 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/steps.html"
---

---

# Steps 步骤条 [​](#steps-步骤条)

更新日志待解决

4

引导用户按照流程完成任务的分步导航条， 可根据实际应用场景设定步骤，步骤不得少于 2 步。

## 基础用法 [​](#基础用法)

简单的步骤条。

设置 `active` 属性，接受一个 `Number`，表明步骤的 index，从 0 开始。 需要定宽的步骤条时，设置 `space` 属性即可，它接受 `Number`， 单位为 `px`， 如果不设置，则为自适应。 设置 `finish-status` 属性可以改变已经完成的步骤的状态。

Step 1

Step 2

Step 3

Next step

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3RlcHMgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCIgOmFjdGl2ZT1cImFjdGl2ZVwiIGZpbmlzaC1zdGF0dXM9XCJzdWNjZXNzXCI+XG4gICAgPGVsLXN0ZXAgdGl0bGU9XCJTdGVwIDFcIiAvPlxuICAgIDxlbC1zdGVwIHRpdGxlPVwiU3RlcCAyXCIgLz5cbiAgICA8ZWwtc3RlcCB0aXRsZT1cIlN0ZXAgM1wiIC8+XG4gIDwvZWwtc3RlcHM+XG5cbiAgPGVsLWJ1dHRvbiBzdHlsZT1cIm1hcmdpbi10b3A6IDEycHhcIiBAY2xpY2s9XCJuZXh0XCI+TmV4dCBzdGVwPC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBhY3RpdmUgPSByZWYoMClcblxuY29uc3QgbmV4dCA9ICgpID0+IHtcbiAgaWYgKGFjdGl2ZS52YWx1ZSsrID4gMikgYWN0aXZlLnZhbHVlID0gMFxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/steps/basic.vue)_

vue

```
<template>
  <el-steps style="max-width: 600px" :active="active" finish-status="success">
    <el-step title="Step 1" />
    <el-step title="Step 2" />
    <el-step title="Step 3" />
  </el-steps>

  <el-button style="margin-top: 12px" @click="next">Next step</el-button>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const active = ref(0)

const next = () => {
  if (active.value++ > 2) active.value = 0
}
</script>
```

隐藏源代码

## 含状态的步骤条 [​](#含状态的步骤条)

每一步骤显示出该步骤的状态。

也可以使用 `title` 具名插槽，可以用 `slot` 的方式来取代属性的设置， 在本文档最后的列表中有所有的插槽可供参考。

Done

Processing

Step 3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3RlcHNcbiAgICBzdHlsZT1cIm1heC13aWR0aDogNjAwcHhcIlxuICAgIDpzcGFjZT1cIjIwMFwiXG4gICAgOmFjdGl2ZT1cIjFcIlxuICAgIGZpbmlzaC1zdGF0dXM9XCJzdWNjZXNzXCJcbiAgPlxuICAgIDxlbC1zdGVwIHRpdGxlPVwiRG9uZVwiIC8+XG4gICAgPGVsLXN0ZXAgdGl0bGU9XCJQcm9jZXNzaW5nXCIgLz5cbiAgICA8ZWwtc3RlcCB0aXRsZT1cIlN0ZXAgM1wiIC8+XG4gIDwvZWwtc3RlcHM+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/steps/with-status.vue)_

vue

```
<template>
  <el-steps
    style="max-width: 600px"
    :space="200"
    :active="1"
    finish-status="success"
  >
    <el-step title="Done" />
    <el-step title="Processing" />
    <el-step title="Step 3" />
  </el-steps>
</template>
```

隐藏源代码

## 居中的步骤条 [​](#居中的步骤条)

标题和描述可以居中。

1

Step 1

Some description

2

Step 2

Some description

3

Step 3

Some description

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3RlcHMgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCIgOmFjdGl2ZT1cIjJcIiBhbGlnbi1jZW50ZXI+XG4gICAgPGVsLXN0ZXAgdGl0bGU9XCJTdGVwIDFcIiBkZXNjcmlwdGlvbj1cIlNvbWUgZGVzY3JpcHRpb25cIiAvPlxuICAgIDxlbC1zdGVwIHRpdGxlPVwiU3RlcCAyXCIgZGVzY3JpcHRpb249XCJTb21lIGRlc2NyaXB0aW9uXCIgLz5cbiAgICA8ZWwtc3RlcCB0aXRsZT1cIlN0ZXAgM1wiIGRlc2NyaXB0aW9uPVwiU29tZSBkZXNjcmlwdGlvblwiIC8+XG4gIDwvZWwtc3RlcHM+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/steps/centered.vue)_

vue

```
<template>
  <el-steps style="max-width: 600px" :active="2" align-center>
    <el-step title="Step 1" description="Some description" />
    <el-step title="Step 2" description="Some description" />
    <el-step title="Step 3" description="Some description" />
  </el-steps>
</template>
```

隐藏源代码

## 带描述的步骤栏 [​](#带描述的步骤栏)

每一步都有描述。

1

Step 1

Some description

2

Step 2

Some description

3

Step 3

Some description

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3RlcHMgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCIgOmFjdGl2ZT1cIjFcIj5cbiAgICA8ZWwtc3RlcCB0aXRsZT1cIlN0ZXAgMVwiIGRlc2NyaXB0aW9uPVwiU29tZSBkZXNjcmlwdGlvblwiIC8+XG4gICAgPGVsLXN0ZXAgdGl0bGU9XCJTdGVwIDJcIiBkZXNjcmlwdGlvbj1cIlNvbWUgZGVzY3JpcHRpb25cIiAvPlxuICAgIDxlbC1zdGVwIHRpdGxlPVwiU3RlcCAzXCIgZGVzY3JpcHRpb249XCJTb21lIGRlc2NyaXB0aW9uXCIgLz5cbiAgPC9lbC1zdGVwcz5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/steps/with-description.vue)_

vue

```
<template>
  <el-steps style="max-width: 600px" :active="1">
    <el-step title="Step 1" description="Some description" />
    <el-step title="Step 2" description="Some description" />
    <el-step title="Step 3" description="Some description" />
  </el-steps>
</template>
```

隐藏源代码

## 带图标的步骤条 [​](#带图标的步骤条)

可以在步骤栏中使用各种自定义图标。

通过 `icon` 属性来设置图标， 图标的类型可以参考 Icon 组件的文档， 除此以外，还能通过具名 `slot` 来使用自定义的图标。

Step 1

Step 2

Step 3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3RlcHMgc3R5bGU9XCJtYXgtd2lkdGg6IDYwMHB4XCIgOmFjdGl2ZT1cIjFcIj5cbiAgICA8ZWwtc3RlcCB0aXRsZT1cIlN0ZXAgMVwiIDppY29uPVwiRWRpdFwiIC8+XG4gICAgPGVsLXN0ZXAgdGl0bGU9XCJTdGVwIDJcIiA6aWNvbj1cIlVwbG9hZFwiIC8+XG4gICAgPGVsLXN0ZXAgdGl0bGU9XCJTdGVwIDNcIiA6aWNvbj1cIlBpY3R1cmVcIiAvPlxuICA8L2VsLXN0ZXBzPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEVkaXQsIFBpY3R1cmUsIFVwbG9hZCB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/steps/with-icon.vue)_

vue

```
<template>
  <el-steps style="max-width: 600px" :active="1">
    <el-step title="Step 1" :icon="Edit" />
    <el-step title="Step 2" :icon="Upload" />
    <el-step title="Step 3" :icon="Picture" />
  </el-steps>
</template>

<script lang="ts" setup>
import { Edit, Picture, Upload } from '@element-plus/icons-vue'
</script>
```

隐藏源代码

## 垂直的步骤条 [​](#垂直的步骤条)

垂直方向的步骤条。

只需要在 `el-steps` 元素中设置 `direction` 属性为 `vertical` 即可。

1

Step 1

2

Step 2

3

Step 3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwiaGVpZ2h0OiAzMDBweDsgbWF4LXdpZHRoOiA2MDBweFwiPlxuICAgIDxlbC1zdGVwcyBkaXJlY3Rpb249XCJ2ZXJ0aWNhbFwiIDphY3RpdmU9XCIxXCI+XG4gICAgICA8ZWwtc3RlcCB0aXRsZT1cIlN0ZXAgMVwiIC8+XG4gICAgICA8ZWwtc3RlcCB0aXRsZT1cIlN0ZXAgMlwiIC8+XG4gICAgICA8ZWwtc3RlcCB0aXRsZT1cIlN0ZXAgM1wiIC8+XG4gICAgPC9lbC1zdGVwcz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/steps/vertical.vue)_

vue

```
<template>
  <div style="height: 300px; max-width: 600px">
    <el-steps direction="vertical" :active="1">
      <el-step title="Step 1" />
      <el-step title="Step 2" />
      <el-step title="Step 3" />
    </el-steps>
  </div>
</template>
```

隐藏源代码

## 简洁风格的步骤条 [​](#简洁风格的步骤条)

设置 `simple` 可应用简洁风格，该条件下 `align-center` / `description` / `direction` / `space` 都将失效。

Step 1

Step 2

Step 3

Step 1

Step 2

Step 3

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3RlcHNcbiAgICBjbGFzcz1cIm1iLTRcIlxuICAgIHN0eWxlPVwibWF4LXdpZHRoOiA2MDBweFwiXG4gICAgOnNwYWNlPVwiMjAwXCJcbiAgICA6YWN0aXZlPVwiMVwiXG4gICAgc2ltcGxlXG4gID5cbiAgICA8ZWwtc3RlcCB0aXRsZT1cIlN0ZXAgMVwiIDppY29uPVwiRWRpdFwiIC8+XG4gICAgPGVsLXN0ZXAgdGl0bGU9XCJTdGVwIDJcIiA6aWNvbj1cIlVwbG9hZEZpbGxlZFwiIC8+XG4gICAgPGVsLXN0ZXAgdGl0bGU9XCJTdGVwIDNcIiA6aWNvbj1cIlBpY3R1cmVcIiAvPlxuICA8L2VsLXN0ZXBzPlxuXG4gIDxlbC1zdGVwcyBzdHlsZT1cIm1heC13aWR0aDogNjAwcHhcIiA6YWN0aXZlPVwiMVwiIGZpbmlzaC1zdGF0dXM9XCJzdWNjZXNzXCIgc2ltcGxlPlxuICAgIDxlbC1zdGVwIHRpdGxlPVwiU3RlcCAxXCIgLz5cbiAgICA8ZWwtc3RlcCB0aXRsZT1cIlN0ZXAgMlwiIC8+XG4gICAgPGVsLXN0ZXAgdGl0bGU9XCJTdGVwIDNcIiAvPlxuICA8L2VsLXN0ZXBzPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEVkaXQsIFBpY3R1cmUsIFVwbG9hZEZpbGxlZCB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/steps/simple.vue)_

vue

```
<template>
  <el-steps
    class="mb-4"
    style="max-width: 600px"
    :space="200"
    :active="1"
    simple
  >
    <el-step title="Step 1" :icon="Edit" />
    <el-step title="Step 2" :icon="UploadFilled" />
    <el-step title="Step 3" :icon="Picture" />
  </el-steps>

  <el-steps style="max-width: 600px" :active="1" finish-status="success" simple>
    <el-step title="Step 1" />
    <el-step title="Step 2" />
    <el-step title="Step 3" />
  </el-steps>
</template>

<script lang="ts" setup>
import { Edit, Picture, UploadFilled } from '@element-plus/icons-vue'
</script>
```

隐藏源代码

## Steps API [​](#steps-api)

### Steps Attributes [​](#steps-attributes)

| 属性名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| space | 每个 step 的间距，不填写将自适应间距。 支持百分比。 | `number` / `string` | '' |
| direction | 显示方向 | `enum` | horizontal |
| active | 设置当前激活步骤 | `number` | 0 |
| process-status | 设置当前步骤的状态 | `enum` | process |
| finish-status | 设置结束步骤的状态 | `enum` | finish |
| align-center | 进行居中对齐 | `boolean` | — |
| simple | 是否应用简洁风格 | `boolean` | — |

### Steps Events [​](#steps-events)

| 插槽名 | 说明 | 参数： |
| --- | --- | --- |
| change | 当活动步骤发生变化时触发 | `Function` |

### Steps Slots [​](#steps-slots)

| 属性名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 默认插槽 | Step |

## Step API [​](#step-api)

### Step Attributes [​](#step-attributes)

| 插槽名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| title | 标题 | `string` | '' |
| description | 描述文案 | `string` | '' |
| icon | Step 组件的自定义图标。 也支持 slot 方式写入 | `string` / `Component` | — |
| status | 设置当前步骤的状态， 不设置则根据 steps 确定状态 | `enum` | '' |

### Step Slots [​](#step-slots)

| 方法名 | 描述 |
| --- | --- |
| icon | 自定义图标 |
| title | 自定义标题 |
| description | 自定义描述文案 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/steps) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/steps.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/steps.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/33646534?v=4&size=64)](https://github.com/SevenDreamYang)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/126545033?v=4&size=64)](https://github.com/dhj-l)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/57086651?v=4&size=64)](https://github.com/Simon-He95)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/19829491?v=4&size=64)](https://github.com/z-ao)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/4318293?v=4&size=64)](https://github.com/cn-troy)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)

[Page Header 页头](https://element-plus.org/zh-CN/component/page-header)

[Tabs 标签页](https://element-plus.org/zh-CN/component/tabs)


