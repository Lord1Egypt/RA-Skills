---
name: "space"
description: "Space 间距 -- Element Plus Vue3 桌面端组件。Invoke when user needs Space 间距 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/space.html"
---

---

# Space 间距 [​](#space-间距)

更新日志待解决

5

虽然我们拥有 [Divider 组件](https://element-plus.org/zh-CN/component/divider)，但很多时候我们需要不是一个被 [Divider 组件](https://element-plus.org/zh-CN/component/divider) 分割开的页面结构，因此我们会重复的使用很多的 [Divider 组件](https://element-plus.org/zh-CN/component/divider)，这在我们的开发效率上造成了一定的困扰。 **间距组件**就是为了解决这种困扰应运而生的。

## 基础用法 [​](#基础用法)

最基础的用法，通过这个组件来给组件之间提供统一的间距。

通过间距组件来给多个组件之间提供间距

Card nameOperation button

List item 1

List item 2

List item 3

List item 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2Ugd3JhcD5cbiAgICA8ZWwtY2FyZCB2LWZvcj1cImkgaW4gM1wiIDprZXk9XCJpXCIgY2xhc3M9XCJib3gtY2FyZFwiIHN0eWxlPVwid2lkdGg6IDI1MHB4XCI+XG4gICAgICA8dGVtcGxhdGUgI2hlYWRlcj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImNhcmQtaGVhZGVyXCI+XG4gICAgICAgICAgPHNwYW4+Q2FyZCBuYW1lPC9zcGFuPlxuICAgICAgICAgIDxlbC1idXR0b24gY2xhc3M9XCJidXR0b25cIiB0ZXh0Pk9wZXJhdGlvbiBidXR0b248L2VsLWJ1dHRvbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgPGRpdiB2LWZvcj1cIm8gaW4gNFwiIDprZXk9XCJvXCIgY2xhc3M9XCJ0ZXh0IGl0ZW1cIj5cbiAgICAgICAge3sgJ0xpc3QgaXRlbSAnICsgbyB9fVxuICAgICAgPC9kaXY+XG4gICAgPC9lbC1jYXJkPlxuICA8L2VsLXNwYWNlPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/space/basic.vue)_

vue

```
<template>
  <el-space wrap>
    <el-card v-for="i in 3" :key="i" class="box-card" style="width: 250px">
      <template #header>
        <div class="card-header">
          <span>Card name</span>
          <el-button class="button" text>Operation button</el-button>
        </div>
      </template>
      <div v-for="o in 4" :key="o" class="text item">
        {{ 'List item ' + o }}
      </div>
    </el-card>
  </el-space>
</template>
```

隐藏源代码

## 垂直布局 [​](#垂直布局)

使用 `direction` 来控制布局的方式, 背后实际上是利用了 `flex-direction` 来控制.

我们也提供垂直布局方式。

Card nameOperation button

List item 1

List item 2

List item 3

List item 4

Card nameOperation button

List item 1

List item 2

List item 3

List item 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgZGlyZWN0aW9uPVwidmVydGljYWxcIj5cbiAgICA8ZWwtY2FyZCB2LWZvcj1cImkgaW4gMlwiIDprZXk9XCJpXCIgY2xhc3M9XCJib3gtY2FyZFwiIHN0eWxlPVwid2lkdGg6IDI1MHB4XCI+XG4gICAgICA8dGVtcGxhdGUgI2hlYWRlcj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImNhcmQtaGVhZGVyXCI+XG4gICAgICAgICAgPHNwYW4+Q2FyZCBuYW1lPC9zcGFuPlxuICAgICAgICAgIDxlbC1idXR0b24gY2xhc3M9XCJidXR0b25cIiB0ZXh0Pk9wZXJhdGlvbiBidXR0b248L2VsLWJ1dHRvbj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgICAgPGRpdiB2LWZvcj1cIm8gaW4gNFwiIDprZXk9XCJvXCIgY2xhc3M9XCJ0ZXh0IGl0ZW1cIj5cbiAgICAgICAge3sgJ0xpc3QgaXRlbSAnICsgbyB9fVxuICAgICAgPC9kaXY+XG4gICAgPC9lbC1jYXJkPlxuICA8L2VsLXNwYWNlPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/space/vertical-layout.vue)_

vue

```
<template>
  <el-space direction="vertical">
    <el-card v-for="i in 2" :key="i" class="box-card" style="width: 250px">
      <template #header>
        <div class="card-header">
          <span>Card name</span>
          <el-button class="button" text>Operation button</el-button>
        </div>
      </template>
      <div v-for="o in 4" :key="o" class="text item">
        {{ 'List item ' + o }}
      </div>
    </el-card>
  </el-space>
</template>
```

隐藏源代码

## 控制间距的大小 [​](#控制间距的大小)

通过调整 `size` 的值来控制间距的大小

你可以使用内置的尺寸 `small`、`default`、`large` 来设置大小，这些尺寸分别对应 `8px`、`12px`、`16px`。 默认的间距大小为 `small`，也就是 `8px`。

您也可以通过自定义的 size 来控制大小， 参见下一个部分。

LargeDefaultSmall

Card nameOperation button

List item 1

List item 2

List item 3

List item 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgZGlyZWN0aW9uPVwidmVydGljYWxcIiBhbGlnbm1lbnQ9XCJzdGFydFwiIDpzaXplPVwiMzBcIj5cbiAgICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cInNpemVcIj5cbiAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cImxhcmdlXCI+TGFyZ2U8L2VsLXJhZGlvPlxuICAgICAgPGVsLXJhZGlvIHZhbHVlPVwiZGVmYXVsdFwiPkRlZmF1bHQ8L2VsLXJhZGlvPlxuICAgICAgPGVsLXJhZGlvIHZhbHVlPVwic21hbGxcIj5TbWFsbDwvZWwtcmFkaW8+XG4gICAgPC9lbC1yYWRpby1ncm91cD5cblxuICAgIDxlbC1zcGFjZSB3cmFwIDpzaXplPVwic2l6ZVwiPlxuICAgICAgPGVsLWNhcmQgdi1mb3I9XCJpIGluIDNcIiA6a2V5PVwiaVwiIGNsYXNzPVwiYm94LWNhcmRcIiBzdHlsZT1cIndpZHRoOiAyNTBweFwiPlxuICAgICAgICA8dGVtcGxhdGUgI2hlYWRlcj5cbiAgICAgICAgICA8ZGl2IGNsYXNzPVwiY2FyZC1oZWFkZXJcIj5cbiAgICAgICAgICAgIDxzcGFuPkNhcmQgbmFtZTwvc3Bhbj5cbiAgICAgICAgICAgIDxlbC1idXR0b24gY2xhc3M9XCJidXR0b25cIiB0ZXh0Pk9wZXJhdGlvbiBidXR0b248L2VsLWJ1dHRvbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgPGRpdiB2LWZvcj1cIm8gaW4gNFwiIDprZXk9XCJvXCIgY2xhc3M9XCJ0ZXh0IGl0ZW1cIj5cbiAgICAgICAgICB7eyAnTGlzdCBpdGVtICcgKyBvIH19XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jYXJkPlxuICAgIDwvZWwtc3BhY2U+XG4gIDwvZWwtc3BhY2U+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IENvbXBvbmVudFNpemUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHNpemUgPSByZWY8Q29tcG9uZW50U2l6ZT4oJ2RlZmF1bHQnKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/space/control-size.vue)_

vue

```
<template>
  <el-space direction="vertical" alignment="start" :size="30">
    <el-radio-group v-model="size">
      <el-radio value="large">Large</el-radio>
      <el-radio value="default">Default</el-radio>
      <el-radio value="small">Small</el-radio>
    </el-radio-group>

    <el-space wrap :size="size">
      <el-card v-for="i in 3" :key="i" class="box-card" style="width: 250px">
        <template #header>
          <div class="card-header">
            <span>Card name</span>
            <el-button class="button" text>Operation button</el-button>
          </div>
        </template>
        <div v-for="o in 4" :key="o" class="text item">
          {{ 'List item ' + o }}
        </div>
      </el-card>
    </el-space>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { ComponentSize } from 'element-plus'

const size = ref<ComponentSize>('default')
</script>
```

隐藏源代码

## 自定义 Size [​](#自定义-size)

很多时候，内建的大小不满足设计师的要求，我们可以通过传入自己定义的大小 (数值类型) 来设置。

Card nameOperation button

List item 1

List item 2

List item 3

List item 4

Card nameOperation button

List item 1

List item 2

List item 3

List item 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc2xpZGVyIHYtbW9kZWw9XCJzaXplXCIgLz5cbiAgPGVsLXNwYWNlIHdyYXAgOnNpemU9XCJzaXplXCI+XG4gICAgPGVsLWNhcmQgdi1mb3I9XCJpIGluIDJcIiA6a2V5PVwiaVwiIGNsYXNzPVwiYm94LWNhcmRcIiBzdHlsZT1cIndpZHRoOiAyNTBweFwiPlxuICAgICAgPHRlbXBsYXRlICNoZWFkZXI+XG4gICAgICAgIDxkaXYgY2xhc3M9XCJjYXJkLWhlYWRlclwiPlxuICAgICAgICAgIDxzcGFuPkNhcmQgbmFtZTwvc3Bhbj5cbiAgICAgICAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiYnV0dG9uXCIgdGV4dD5PcGVyYXRpb24gYnV0dG9uPC9lbC1idXR0b24+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDxkaXYgdi1mb3I9XCJvIGluIDRcIiA6a2V5PVwib1wiIGNsYXNzPVwidGV4dCBpdGVtXCI+XG4gICAgICAgIHt7ICdMaXN0IGl0ZW0gJyArIG8gfX1cbiAgICAgIDwvZGl2PlxuICAgIDwvZWwtY2FyZD5cbiAgPC9lbC1zcGFjZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHNpemUgPSByZWYoMjApXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/space/customized-size.vue)_

vue

```
<template>
  <el-slider v-model="size" />
  <el-space wrap :size="size">
    <el-card v-for="i in 2" :key="i" class="box-card" style="width: 250px">
      <template #header>
        <div class="card-header">
          <span>Card name</span>
          <el-button class="button" text>Operation button</el-button>
        </div>
      </template>
      <div v-for="o in 4" :key="o" class="text item">
        {{ 'List item ' + o }}
      </div>
    </el-card>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const size = ref(20)
</script>
```

隐藏源代码

TIP

不要让 `ElSpace` 与使用依赖父元素百分比宽度（或高度）的元素一起使用（例如 `ElSlider`），这样会造成光标不同步。

## 自动换行 [​](#自动换行)

在 \*\*水平 (horizontal) \*\* 模式下，通过使用 `wrap`（**布尔类型**）来控制自动换行行为。

利用 `wrap` 属性控制换行

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

Text button

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2Ugd3JhcD5cbiAgICA8ZGl2IHYtZm9yPVwiaSBpbiAyMFwiIDprZXk9XCJpXCI+XG4gICAgICA8ZWwtYnV0dG9uIHRleHQ+IFRleHQgYnV0dG9uIDwvZWwtYnV0dG9uPlxuICAgIDwvZGl2PlxuICA8L2VsLXNwYWNlPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/space/auto-wrapping.vue)_

vue

```
<template>
  <el-space wrap>
    <div v-for="i in 20" :key="i">
      <el-button text> Text button </el-button>
    </div>
  </el-space>
</template>
```

隐藏源代码

## 行间分隔符 [​](#行间分隔符)

有时候，仅仅在行间加空白并不能满足我们的日常需求，此时分隔符 (spacer) 就可以发挥非常好的作用了。

## 字母数字类型分隔符 [​](#字母数字类型分隔符)

button 1

|

button 2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgOnNpemU9XCJzaXplXCIgc3BhY2VyPVwifFwiPlxuICAgIDxkaXYgdi1mb3I9XCJpIGluIDJcIiA6a2V5PVwiaVwiPlxuICAgICAgPGVsLWJ1dHRvbj4gYnV0dG9uIHt7IGkgfX0gPC9lbC1idXR0b24+XG4gICAgPC9kaXY+XG4gIDwvZWwtc3BhY2U+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCBzaXplID0gcmVmKDEwKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/space/literal-type-spacer.vue)_

vue

```
<template>
  <el-space :size="size" spacer="|">
    <div v-for="i in 2" :key="i">
      <el-button> button {{ i }} </el-button>
    </div>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const size = ref(10)
</script>
```

隐藏源代码

## 分隔符还可以是 VNode 类型 [​](#分隔符还可以是-vnode-类型)

button 1

button 2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtc3BhY2UgOnNpemU9XCJzaXplXCIgOnNwYWNlcj1cInNwYWNlclwiPlxuICAgIDxkaXYgdi1mb3I9XCJpIGluIDJcIiA6a2V5PVwiaVwiPlxuICAgICAgPGVsLWJ1dHRvbj4gYnV0dG9uIHt7IGkgfX0gPC9lbC1idXR0b24+XG4gICAgPC9kaXY+XG4gIDwvZWwtc3BhY2U+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgaCwgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgRWxEaXZpZGVyIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBzaXplID0gcmVmKDEwKVxuY29uc3Qgc3BhY2VyID0gaChFbERpdmlkZXIsIHsgZGlyZWN0aW9uOiAndmVydGljYWwnIH0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/space/vnode-type-spacer.vue)_

vue

```
<template>
  <el-space :size="size" :spacer="spacer">
    <div v-for="i in 2" :key="i">
      <el-button> button {{ i }} </el-button>
    </div>
  </el-space>
</template>

<script lang="ts" setup>
import { h, ref } from 'vue'
import { ElDivider } from 'element-plus'

const size = ref(10)
const spacer = h(ElDivider, { direction: 'vertical' })
</script>
```

隐藏源代码

## 对齐方式 [​](#对齐方式)

设置该值可以调整所有子节点在容器内的对齐方式，可设置的值与 [align-items](https://developer.mozilla.org/en-US/docs/Web/CSS/align-items) 一致。

使用 `alignment` 属性来对齐

string

button

header

body

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiYWxpZ25tZW50LWNvbnRhaW5lclwiPlxuICAgIDxlbC1zcGFjZT5cbiAgICAgIHN0cmluZ1xuICAgICAgPGVsLWJ1dHRvbj4gYnV0dG9uIDwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWNhcmQ+XG4gICAgICAgIDx0ZW1wbGF0ZSAjaGVhZGVyPiBoZWFkZXIgPC90ZW1wbGF0ZT5cbiAgICAgICAgYm9keVxuICAgICAgPC9lbC1jYXJkPlxuICAgIDwvZWwtc3BhY2U+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwiYWxpZ25tZW50LWNvbnRhaW5lclwiPlxuICAgIDxlbC1zcGFjZSBhbGlnbm1lbnQ9XCJmbGV4LXN0YXJ0XCI+XG4gICAgICBzdHJpbmdcbiAgICAgIDxlbC1idXR0b24+IGJ1dHRvbiA8L2VsLWJ1dHRvbj5cbiAgICAgIDxlbC1jYXJkPlxuICAgICAgICA8dGVtcGxhdGUgI2hlYWRlcj4gaGVhZGVyIDwvdGVtcGxhdGU+XG4gICAgICAgIGJvZHlcbiAgICAgIDwvZWwtY2FyZD5cbiAgICA8L2VsLXNwYWNlPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cImFsaWdubWVudC1jb250YWluZXJcIj5cbiAgICA8ZWwtc3BhY2UgYWxpZ25tZW50PVwiZmxleC1lbmRcIj5cbiAgICAgIHN0cmluZ1xuICAgICAgPGVsLWJ1dHRvbj4gYnV0dG9uIDwvZWwtYnV0dG9uPlxuICAgICAgPGVsLWNhcmQ+XG4gICAgICAgIDx0ZW1wbGF0ZSAjaGVhZGVyPiBoZWFkZXIgPC90ZW1wbGF0ZT5cbiAgICAgICAgYm9keVxuICAgICAgPC9lbC1jYXJkPlxuICAgIDwvZWwtc3BhY2U+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlPlxuLmFsaWdubWVudC1jb250YWluZXIge1xuICB3aWR0aDogMjQwcHg7XG4gIG1hcmdpbi1ib3R0b206IDIwcHg7XG4gIHBhZGRpbmc6IDhweDtcbiAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0tZWwtYm9yZGVyLWNvbG9yKTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/space/alignment.vue)_

vue

```
<template>
  <div class="alignment-container">
    <el-space>
      string
      <el-button> button </el-button>
      <el-card>
        <template #header> header </template>
        body
      </el-card>
    </el-space>
  </div>
  <div class="alignment-container">
    <el-space alignment="flex-start">
      string
      <el-button> button </el-button>
      <el-card>
        <template #header> header </template>
        body
      </el-card>
    </el-space>
  </div>
  <div class="alignment-container">
    <el-space alignment="flex-end">
      string
      <el-button> button </el-button>
      <el-card>
        <template #header> header </template>
        body
      </el-card>
    </el-space>
  </div>
</template>

<style>
.alignment-container {
  width: 240px;
  margin-bottom: 20px;
  padding: 8px;
  border: 1px solid var(--el-border-color);
}
</style>
```

隐藏源代码

## 填充容器 [​](#填充容器)

通过 `fill`\*\*（布尔类型）\*\*参数，您可以控制子节点是否自动填充容器。

下面的例子中，当设置为 `fill` 时，子节点的宽度会自动适配容器的宽度。

用 fill 属性让子节点自动填充容器

fill:

Card nameOperation button

List item 1

List item 2

List item 3

List item 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxkaXYgc3R5bGU9XCJtYXJnaW4tYm90dG9tOiAxNXB4XCI+ZmlsbDogPGVsLXN3aXRjaCB2LW1vZGVsPVwiZmlsbFwiIC8+PC9kaXY+XG4gICAgPGVsLXNwYWNlIDpmaWxsPVwiZmlsbFwiIHdyYXA+XG4gICAgICA8ZWwtY2FyZCB2LWZvcj1cImkgaW4gM1wiIDprZXk9XCJpXCIgY2xhc3M9XCJib3gtY2FyZFwiPlxuICAgICAgICA8dGVtcGxhdGUgI2hlYWRlcj5cbiAgICAgICAgICA8ZGl2IGNsYXNzPVwiY2FyZC1oZWFkZXJcIj5cbiAgICAgICAgICAgIDxzcGFuPkNhcmQgbmFtZTwvc3Bhbj5cbiAgICAgICAgICAgIDxlbC1idXR0b24gY2xhc3M9XCJidXR0b25cIiB0ZXh0Pk9wZXJhdGlvbiBidXR0b248L2VsLWJ1dHRvbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgPGRpdiB2LWZvcj1cIm8gaW4gNFwiIDprZXk9XCJvXCIgY2xhc3M9XCJ0ZXh0IGl0ZW1cIj5cbiAgICAgICAgICB7eyAnTGlzdCBpdGVtICcgKyBvIH19XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jYXJkPlxuICAgIDwvZWwtc3BhY2U+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgZmlsbCA9IHJlZih0cnVlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/space/fill.vue)_

vue

```
<template>
  <div>
    <div style="margin-bottom: 15px">fill: <el-switch v-model="fill" /></div>
    <el-space :fill="fill" wrap>
      <el-card v-for="i in 3" :key="i" class="box-card">
        <template #header>
          <div class="card-header">
            <span>Card name</span>
            <el-button class="button" text>Operation button</el-button>
          </div>
        </template>
        <div v-for="o in 4" :key="o" class="text item">
          {{ 'List item ' + o }}
        </div>
      </el-card>
    </el-space>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const fill = ref(true)
</script>
```

隐藏源代码

也可以使用 `fillRatio` 参数，自定义填充的比例， 默认值为 `100`，代表基于父容器宽度的 `100%` 进行填充

需要注意的是，水平布局和垂直布局的表现形式稍有不同，具体的效果可以查看下面的例子

用 fillRatio 自定义填充比例

direction: horizontalvertical

fillRatio:

Card nameOperation button

List item 1

List item 2

List item 3

List item 4

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxkaXYgc3R5bGU9XCJtYXJnaW4tYm90dG9tOiAxNXB4XCI+XG4gICAgICBkaXJlY3Rpb246XG4gICAgICA8ZWwtcmFkaW8gdi1tb2RlbD1cImRpcmVjdGlvblwiIHZhbHVlPVwiaG9yaXpvbnRhbFwiPmhvcml6b250YWw8L2VsLXJhZGlvPlxuICAgICAgPGVsLXJhZGlvIHYtbW9kZWw9XCJkaXJlY3Rpb25cIiB2YWx1ZT1cInZlcnRpY2FsXCI+dmVydGljYWw8L2VsLXJhZGlvPlxuICAgIDwvZGl2PlxuICAgIDxkaXYgc3R5bGU9XCJtYXJnaW4tYm90dG9tOiAxNXB4XCI+XG4gICAgICBmaWxsUmF0aW86PGVsLXNsaWRlciB2LW1vZGVsPVwiZmlsbFJhdGlvXCIgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZWwtc3BhY2VcbiAgICAgIGZpbGxcbiAgICAgIHdyYXBcbiAgICAgIDpmaWxsLXJhdGlvPVwiZmlsbFJhdGlvXCJcbiAgICAgIDpkaXJlY3Rpb249XCJkaXJlY3Rpb25cIlxuICAgICAgc3R5bGU9XCJ3aWR0aDogMTAwJVwiXG4gICAgPlxuICAgICAgPGVsLWNhcmQgdi1mb3I9XCJpIGluIDVcIiA6a2V5PVwiaVwiIGNsYXNzPVwiYm94LWNhcmRcIj5cbiAgICAgICAgPHRlbXBsYXRlICNoZWFkZXI+XG4gICAgICAgICAgPGRpdiBjbGFzcz1cImNhcmQtaGVhZGVyXCI+XG4gICAgICAgICAgICA8c3Bhbj5DYXJkIG5hbWU8L3NwYW4+XG4gICAgICAgICAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiYnV0dG9uXCIgdGV4dD5PcGVyYXRpb24gYnV0dG9uPC9lbC1idXR0b24+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgIDxkaXYgdi1mb3I9XCJvIGluIDRcIiA6a2V5PVwib1wiIGNsYXNzPVwidGV4dCBpdGVtXCI+XG4gICAgICAgICAge3sgJ0xpc3QgaXRlbSAnICsgbyB9fVxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZWwtY2FyZD5cbiAgICA8L2VsLXNwYWNlPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgU3BhY2VJbnN0YW5jZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgZGlyZWN0aW9uID0gcmVmPFNwYWNlSW5zdGFuY2VbJ2RpcmVjdGlvbiddPignaG9yaXpvbnRhbCcpXG5jb25zdCBmaWxsUmF0aW8gPSByZWYoMzApXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/space/fill-ratio.vue)_

vue

```
<template>
  <div>
    <div style="margin-bottom: 15px">
      direction:
      <el-radio v-model="direction" value="horizontal">horizontal</el-radio>
      <el-radio v-model="direction" value="vertical">vertical</el-radio>
    </div>
    <div style="margin-bottom: 15px">
      fillRatio:<el-slider v-model="fillRatio" />
    </div>
    <el-space
      fill
      wrap
      :fill-ratio="fillRatio"
      :direction="direction"
      style="width: 100%"
    >
      <el-card v-for="i in 5" :key="i" class="box-card">
        <template #header>
          <div class="card-header">
            <span>Card name</span>
            <el-button class="button" text>Operation button</el-button>
          </div>
        </template>
        <div v-for="o in 4" :key="o" class="text item">
          {{ 'List item ' + o }}
        </div>
      </el-card>
    </el-space>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { SpaceInstance } from 'element-plus'

const direction = ref<SpaceInstance['direction']>('horizontal')
const fillRatio = ref(30)
</script>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| alignment | 对齐的方式 | `enum` [align-items](https://developer.mozilla.org/en-US/docs/Web/CSS/align-items) | center |
| class | className | `string` / `object` / `array` | — |
| direction | 排列的方向 | `enum` | horizontal |
| prefix-cls | 给 space-items 的类名前缀 | `string` | — |
| style | 额外样式 | `string` / `object` | — |
| spacer | 间隔符 | `string` / `number` / `VNode` | — |
| size | 间隔大小 | `enum` / `number` / `array` | small |
| wrap | 设置是否自动折行 | `boolean` | false |
| fill | 子元素是否填充父容器 | `boolean` | false |
| fill-ratio | 填充父容器的比例 | `number` | 100 |

### Slots [​](#slots)

| 名称 | 说明 |
| --- | --- |
| default | 需要添加间隔的元素 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/space) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/space.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/space.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/35091020?v=4&size=64)](https://github.com/zzh948498)[![](https://avatars.githubusercontent.com/u/43134418?v=4&size=64)](https://github.com/MonsterPi13)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/31943807?v=4&size=64)](https://github.com/ayay459547)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)

[Scrollbar 滚动条](https://element-plus.org/zh-CN/component/scrollbar)

[Splitter 分隔面板](https://element-plus.org/zh-CN/component/splitter)


