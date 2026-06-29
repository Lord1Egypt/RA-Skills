---
name: "anchor"
description: "Anchor 锚点 -- Element Plus Vue3 桌面端组件。Invoke when user needs Anchor 锚点 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/anchor.html"
---

---

# Anchor 锚点 [​](#anchor-锚点)

更新日志待解决

1

通过锚点，您可以很快找到当前页面上信息内容的位置。

## 基础用法 [​](#基础用法)

最简单的用法。

[基础用法](#基础用法)

[水平模式](#水平模式)

[滚动容器](#滚动的容器)

[Anchor API](#anchor-api)

[Anchor Attributes](#anchor-attributes)

[Anchor Events](#anchor-events)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYW5jaG9yIDpvZmZzZXQ9XCI3MFwiPlxuICAgIDxlbC1hbmNob3ItbGluayA6aHJlZj1cImAjJHtsb2NhbGVbJ2Jhc2ljLXVzYWdlJ119YFwiPlxuICAgICAge3sgbG9jYWxlWydCYXNpYyBVc2FnZSddIH19XG4gICAgPC9lbC1hbmNob3ItbGluaz5cbiAgICA8ZWwtYW5jaG9yLWxpbmsgOmhyZWY9XCJgIyR7bG9jYWxlWydob3Jpem9udGFsLW1vZGUnXX1gXCI+XG4gICAgICB7eyBsb2NhbGVbJ0hvcml6b250YWwgTW9kZSddIH19XG4gICAgPC9lbC1hbmNob3ItbGluaz5cbiAgICA8ZWwtYW5jaG9yLWxpbmsgOmhyZWY9XCJgIyR7bG9jYWxlWydzY3JvbGwtY29udGFpbmVyJ119YFwiPlxuICAgICAge3sgbG9jYWxlWydTY3JvbGwgQ29udGFpbmVyJ10gfX1cbiAgICA8L2VsLWFuY2hvci1saW5rPlxuICAgIDxlbC1hbmNob3ItbGluayA6aHJlZj1cImAjJHtsb2NhbGVbJ2FuY2hvci1hcGknXX1gXCI+XG4gICAgICB7eyBsb2NhbGVbJ0FuY2hvciBBUEknXSB9fVxuICAgICAgPHRlbXBsYXRlICNzdWItbGluaz5cbiAgICAgICAgPGVsLWFuY2hvci1saW5rIDpocmVmPVwiYCMke2xvY2FsZVsnYW5jaG9yLWF0dHJpYnV0ZXMnXX1gXCI+XG4gICAgICAgICAge3sgbG9jYWxlWydBbmNob3IgQXR0cmlidXRlcyddIH19XG4gICAgICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgICAgIDxlbC1hbmNob3ItbGluayA6aHJlZj1cImAjJHtsb2NhbGVbJ2FuY2hvci1ldmVudHMnXX1gXCI+XG4gICAgICAgICAge3sgbG9jYWxlWydBbmNob3IgRXZlbnRzJ10gfX1cbiAgICAgICAgPC9lbC1hbmNob3ItbGluaz5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1hbmNob3ItbGluaz5cbiAgPC9lbC1hbmNob3I+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgY29tcHV0ZWQgfSBmcm9tICd2dWUnXG5pbXBvcnQgYW5jaG9yTG9jYWxlIGZyb20gJy4uLy4uLy52aXRlcHJlc3MvaTE4bi9jb21wb25lbnQvYW5jaG9yLmpzb24nXG5pbXBvcnQgeyB1c2VMYW5nIH0gZnJvbSAnfi9jb21wb3NhYmxlcy9sYW5nJ1xuXG5jb25zdCBsYW5nID0gdXNlTGFuZygpXG5jb25zdCBsb2NhbGUgPSBjb21wdXRlZCgoKSA9PiBhbmNob3JMb2NhbGVbbGFuZy52YWx1ZV0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/anchor/basic.vue)_

vue

```
<template>
  <el-anchor :offset="70">
    <el-anchor-link :href="`#${locale['basic-usage']}`">
      {{ locale['Basic Usage'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['horizontal-mode']}`">
      {{ locale['Horizontal Mode'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['scroll-container']}`">
      {{ locale['Scroll Container'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['anchor-api']}`">
      {{ locale['Anchor API'] }}
      <template #sub-link>
        <el-anchor-link :href="`#${locale['anchor-attributes']}`">
          {{ locale['Anchor Attributes'] }}
        </el-anchor-link>
        <el-anchor-link :href="`#${locale['anchor-events']}`">
          {{ locale['Anchor Events'] }}
        </el-anchor-link>
      </template>
    </el-anchor-link>
  </el-anchor>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import anchorLocale from '../../.vitepress/i18n/component/anchor.json'
import { useLang } from '~/composables/lang'

const lang = useLang()
const locale = computed(() => anchorLocale[lang.value])
</script>
```

隐藏源代码

## 水平模式 [​](#水平模式)

水平排列的锚点

TIP

水平模式不支持`sub-link`槽位

[基础用法](#基础用法)

[水平模式](#水平模式)

[滚动容器](#滚动的容器)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYW5jaG9yIDpvZmZzZXQ9XCI3MFwiIGRpcmVjdGlvbj1cImhvcml6b250YWxcIj5cbiAgICA8ZWwtYW5jaG9yLWxpbmsgOmhyZWY9XCJgIyR7bG9jYWxlWydiYXNpYy11c2FnZSddfWBcIj5cbiAgICAgIHt7IGxvY2FsZVsnQmFzaWMgVXNhZ2UnXSB9fVxuICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgPGVsLWFuY2hvci1saW5rIDpocmVmPVwiYCMke2xvY2FsZVsnaG9yaXpvbnRhbC1tb2RlJ119YFwiPlxuICAgICAge3sgbG9jYWxlWydIb3Jpem9udGFsIE1vZGUnXSB9fVxuICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgPGVsLWFuY2hvci1saW5rIDpocmVmPVwiYCMke2xvY2FsZVsnc2Nyb2xsLWNvbnRhaW5lciddfWBcIj5cbiAgICAgIHt7IGxvY2FsZVsnU2Nyb2xsIENvbnRhaW5lciddIH19XG4gICAgPC9lbC1hbmNob3ItbGluaz5cbiAgPC9lbC1hbmNob3I+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgY29tcHV0ZWQgfSBmcm9tICd2dWUnXG5pbXBvcnQgYW5jaG9yTG9jYWxlIGZyb20gJy4uLy4uLy52aXRlcHJlc3MvaTE4bi9jb21wb25lbnQvYW5jaG9yLmpzb24nXG5pbXBvcnQgeyB1c2VMYW5nIH0gZnJvbSAnfi9jb21wb3NhYmxlcy9sYW5nJ1xuXG5jb25zdCBsYW5nID0gdXNlTGFuZygpXG5jb25zdCBsb2NhbGUgPSBjb21wdXRlZCgoKSA9PiBhbmNob3JMb2NhbGVbbGFuZy52YWx1ZV0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/anchor/horizontal.vue)_

vue

```
<template>
  <el-anchor :offset="70" direction="horizontal">
    <el-anchor-link :href="`#${locale['basic-usage']}`">
      {{ locale['Basic Usage'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['horizontal-mode']}`">
      {{ locale['Horizontal Mode'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['scroll-container']}`">
      {{ locale['Scroll Container'] }}
    </el-anchor-link>
  </el-anchor>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import anchorLocale from '../../.vitepress/i18n/component/anchor.json'
import { useLang } from '~/composables/lang'

const lang = useLang()
const locale = computed(() => anchorLocale[lang.value])
</script>
```

隐藏源代码

## 滚动容器 [​](#滚动容器)

自定义滚动区域，使用 `offset` props 可以设置锚点滚动偏移。 监听`link-click`事件并阻止浏览器的默认行为，从而不会更改历史记录。

Fixed Top Block

part1

part2

part3

[part1](#part1)

[part2](#part2)

[part3](#part3)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1yb3c+XG4gICAgICA8ZWwtY29sIDpzcGFuPVwiMThcIj5cbiAgICAgICAgPGRpdlxuICAgICAgICAgIHN0eWxlPVwiXG4gICAgICAgICAgICBoZWlnaHQ6IDMwcHg7XG4gICAgICAgICAgICB3aWR0aDogNzAlO1xuICAgICAgICAgICAgYmFja2dyb3VuZDogIzAwMDtcbiAgICAgICAgICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgICAgICAgICAgIHRvcDogMDtcbiAgICAgICAgICAgIGxlZnQ6IDA7XG4gICAgICAgICAgICBjb2xvcjogI2ZmZjtcbiAgICAgICAgICBcIlxuICAgICAgICA+XG4gICAgICAgICAgRml4ZWQgVG9wIEJsb2NrXG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2IHJlZj1cImNvbnRhaW5lclJlZlwiIHN0eWxlPVwiaGVpZ2h0OiAzMDBweDsgb3ZlcmZsb3cteTogYXV0b1wiPlxuICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgIGlkPVwicGFydDFcIlxuICAgICAgICAgICAgc3R5bGU9XCJcbiAgICAgICAgICAgICAgaGVpZ2h0OiAzMDBweDtcbiAgICAgICAgICAgICAgYmFja2dyb3VuZDogcmdiYSgyNTUsIDAsIDAsIDAuMDIpO1xuICAgICAgICAgICAgICBtYXJnaW4tdG9wOiAzMHB4O1xuICAgICAgICAgICAgXCJcbiAgICAgICAgICA+XG4gICAgICAgICAgICBwYXJ0MVxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgIGlkPVwicGFydDJcIlxuICAgICAgICAgICAgc3R5bGU9XCJcbiAgICAgICAgICAgICAgaGVpZ2h0OiAzMDBweDtcbiAgICAgICAgICAgICAgYmFja2dyb3VuZDogcmdiYSgwLCAyNTUsIDAsIDAuMDIpO1xuICAgICAgICAgICAgICBtYXJnaW4tdG9wOiAzMHB4O1xuICAgICAgICAgICAgXCJcbiAgICAgICAgICA+XG4gICAgICAgICAgICBwYXJ0MlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgIGlkPVwicGFydDNcIlxuICAgICAgICAgICAgc3R5bGU9XCJcbiAgICAgICAgICAgICAgaGVpZ2h0OiAzMDBweDtcbiAgICAgICAgICAgICAgYmFja2dyb3VuZDogcmdiYSgwLCAwLCAyNTUsIDAuMDIpO1xuICAgICAgICAgICAgICBtYXJnaW4tdG9wOiAzMHB4O1xuICAgICAgICAgICAgXCJcbiAgICAgICAgICA+XG4gICAgICAgICAgICBwYXJ0M1xuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZWwtY29sPlxuICAgICAgPGVsLWNvbCA6c3Bhbj1cIjZcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cInZwLXJhd1wiPlxuICAgICAgICAgIDxlbC1hbmNob3JcbiAgICAgICAgICAgIDpjb250YWluZXI9XCJjb250YWluZXJSZWZcIlxuICAgICAgICAgICAgZGlyZWN0aW9uPVwidmVydGljYWxcIlxuICAgICAgICAgICAgdHlwZT1cImRlZmF1bHRcIlxuICAgICAgICAgICAgOm9mZnNldD1cIjMwXCJcbiAgICAgICAgICAgIEBjbGljaz1cImhhbmRsZUNsaWNrXCJcbiAgICAgICAgICA+XG4gICAgICAgICAgICA8ZWwtYW5jaG9yLWxpbmsgaHJlZj1cIiNwYXJ0MVwiIHRpdGxlPVwicGFydDFcIiAvPlxuICAgICAgICAgICAgPGVsLWFuY2hvci1saW5rIGhyZWY9XCIjcGFydDJcIiB0aXRsZT1cInBhcnQyXCIgLz5cbiAgICAgICAgICAgIDxlbC1hbmNob3ItbGluayBocmVmPVwiI3BhcnQzXCIgdGl0bGU9XCJwYXJ0M1wiIC8+XG4gICAgICAgICAgPC9lbC1hbmNob3I+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jb2w+XG4gICAgPC9lbC1yb3c+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgY29udGFpbmVyUmVmID0gcmVmPEhUTUxFbGVtZW50IHwgbnVsbD4obnVsbClcblxuY29uc3QgaGFuZGxlQ2xpY2sgPSAoZTogTW91c2VFdmVudCkgPT4ge1xuICBlLnByZXZlbnREZWZhdWx0KClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/anchor/scroll.vue)_

vue

```
<template>
  <div>
    <el-row>
      <el-col :span="18">
        <div
          style="
            height: 30px;
            width: 70%;
            background: #000;
            position: absolute;
            top: 0;
            left: 0;
            color: #fff;
          "
        >
          Fixed Top Block
        </div>
        <div ref="containerRef" style="height: 300px; overflow-y: auto">
          <div
            id="part1"
            style="
              height: 300px;
              background: rgba(255, 0, 0, 0.02);
              margin-top: 30px;
            "
          >
            part1
          </div>
          <div
            id="part2"
            style="
              height: 300px;
              background: rgba(0, 255, 0, 0.02);
              margin-top: 30px;
            "
          >
            part2
          </div>
          <div
            id="part3"
            style="
              height: 300px;
              background: rgba(0, 0, 255, 0.02);
              margin-top: 30px;
            "
          >
            part3
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="vp-raw">
          <el-anchor
            :container="containerRef"
            direction="vertical"
            type="default"
            :offset="30"
            @click="handleClick"
          >
            <el-anchor-link href="#part1" title="part1" />
            <el-anchor-link href="#part2" title="part2" />
            <el-anchor-link href="#part3" title="part3" />
          </el-anchor>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const containerRef = ref<HTMLElement | null>(null)

const handleClick = (e: MouseEvent) => {
  e.preventDefault()
}
</script>
```

隐藏源代码

## 锚点链接变化 [​](#锚点链接变化)

监听锚点链接变化

[基础用法](#基础用法)

[水平模式](#水平模式)

[滚动容器](#滚动的容器)

[Anchor API](#anchor-api)

[Anchor Attributes](#anchor-attributes)

[Anchor Events](#anchor-events)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYW5jaG9yIDpvZmZzZXQ9XCI3MFwiIEBjaGFuZ2U9XCJoYW5kbGVDaGFuZ2VcIj5cbiAgICA8ZWwtYW5jaG9yLWxpbmsgOmhyZWY9XCJgIyR7bG9jYWxlWydiYXNpYy11c2FnZSddfWBcIj5cbiAgICAgIHt7IGxvY2FsZVsnQmFzaWMgVXNhZ2UnXSB9fVxuICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgPGVsLWFuY2hvci1saW5rIDpocmVmPVwiYCMke2xvY2FsZVsnaG9yaXpvbnRhbC1tb2RlJ119YFwiPlxuICAgICAge3sgbG9jYWxlWydIb3Jpem9udGFsIE1vZGUnXSB9fVxuICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgPGVsLWFuY2hvci1saW5rIDpocmVmPVwiYCMke2xvY2FsZVsnc2Nyb2xsLWNvbnRhaW5lciddfWBcIj5cbiAgICAgIHt7IGxvY2FsZVsnU2Nyb2xsIENvbnRhaW5lciddIH19XG4gICAgPC9lbC1hbmNob3ItbGluaz5cbiAgICA8ZWwtYW5jaG9yLWxpbmsgOmhyZWY9XCJgIyR7bG9jYWxlWydhbmNob3ItYXBpJ119YFwiPlxuICAgICAge3sgbG9jYWxlWydBbmNob3IgQVBJJ10gfX1cbiAgICAgIDx0ZW1wbGF0ZSAjc3ViLWxpbms+XG4gICAgICAgIDxlbC1hbmNob3ItbGluayA6aHJlZj1cImAjJHtsb2NhbGVbJ2FuY2hvci1hdHRyaWJ1dGVzJ119YFwiPlxuICAgICAgICAgIHt7IGxvY2FsZVsnQW5jaG9yIEF0dHJpYnV0ZXMnXSB9fVxuICAgICAgICA8L2VsLWFuY2hvci1saW5rPlxuICAgICAgICA8ZWwtYW5jaG9yLWxpbmsgOmhyZWY9XCJgIyR7bG9jYWxlWydhbmNob3ItZXZlbnRzJ119YFwiPlxuICAgICAgICAgIHt7IGxvY2FsZVsnQW5jaG9yIEV2ZW50cyddIH19XG4gICAgICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gIDwvZWwtYW5jaG9yPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IGNvbXB1dGVkIH0gZnJvbSAndnVlJ1xuaW1wb3J0IGFuY2hvckxvY2FsZSBmcm9tICcuLi8uLi8udml0ZXByZXNzL2kxOG4vY29tcG9uZW50L2FuY2hvci5qc29uJ1xuaW1wb3J0IHsgdXNlTGFuZyB9IGZyb20gJ34vY29tcG9zYWJsZXMvbGFuZydcblxuY29uc3QgbGFuZyA9IHVzZUxhbmcoKVxuY29uc3QgbG9jYWxlID0gY29tcHV0ZWQoKCkgPT4gYW5jaG9yTG9jYWxlW2xhbmcudmFsdWVdKVxuXG5jb25zdCBoYW5kbGVDaGFuZ2UgPSAoaHJlZjogc3RyaW5nKSA9PiB7XG4gIGNvbnNvbGUubG9nKGBhbmNob3IgY2hhbmdlOiAke2hyZWZ9YClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/anchor/change.vue)_

vue

```
<template>
  <el-anchor :offset="70" @change="handleChange">
    <el-anchor-link :href="`#${locale['basic-usage']}`">
      {{ locale['Basic Usage'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['horizontal-mode']}`">
      {{ locale['Horizontal Mode'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['scroll-container']}`">
      {{ locale['Scroll Container'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['anchor-api']}`">
      {{ locale['Anchor API'] }}
      <template #sub-link>
        <el-anchor-link :href="`#${locale['anchor-attributes']}`">
          {{ locale['Anchor Attributes'] }}
        </el-anchor-link>
        <el-anchor-link :href="`#${locale['anchor-events']}`">
          {{ locale['Anchor Events'] }}
        </el-anchor-link>
      </template>
    </el-anchor-link>
  </el-anchor>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import anchorLocale from '../../.vitepress/i18n/component/anchor.json'
import { useLang } from '~/composables/lang'

const lang = useLang()
const locale = computed(() => anchorLocale[lang.value])

const handleChange = (href: string) => {
  console.log(`anchor change: ${href}`)
}
</script>
```

隐藏源代码

## 下划线类型 [​](#下划线类型)

设置`type="underline"`以更改为下划线类型

[基础用法](#基础用法)

[水平模式](#水平模式)

[滚动容器](#滚动的容器)

[Anchor API](#anchor-api)

[Anchor Attributes](#anchor-attributes)

[Anchor Events](#anchor-events)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYW5jaG9yIHR5cGU9XCJ1bmRlcmxpbmVcIiA6b2Zmc2V0PVwiNzBcIj5cbiAgICA8ZWwtYW5jaG9yLWxpbmsgOmhyZWY9XCJgIyR7bG9jYWxlWydiYXNpYy11c2FnZSddfWBcIj5cbiAgICAgIHt7IGxvY2FsZVsnQmFzaWMgVXNhZ2UnXSB9fVxuICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgPGVsLWFuY2hvci1saW5rIDpocmVmPVwiYCMke2xvY2FsZVsnaG9yaXpvbnRhbC1tb2RlJ119YFwiPlxuICAgICAge3sgbG9jYWxlWydIb3Jpem9udGFsIE1vZGUnXSB9fVxuICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgPGVsLWFuY2hvci1saW5rIDpocmVmPVwiYCMke2xvY2FsZVsnc2Nyb2xsLWNvbnRhaW5lciddfWBcIj5cbiAgICAgIHt7IGxvY2FsZVsnU2Nyb2xsIENvbnRhaW5lciddIH19XG4gICAgPC9lbC1hbmNob3ItbGluaz5cbiAgICA8ZWwtYW5jaG9yLWxpbmsgOmhyZWY9XCJgIyR7bG9jYWxlWydhbmNob3ItYXBpJ119YFwiPlxuICAgICAge3sgbG9jYWxlWydBbmNob3IgQVBJJ10gfX1cbiAgICAgIDx0ZW1wbGF0ZSAjc3ViLWxpbms+XG4gICAgICAgIDxlbC1hbmNob3ItbGluayA6aHJlZj1cImAjJHtsb2NhbGVbJ2FuY2hvci1hdHRyaWJ1dGVzJ119YFwiPlxuICAgICAgICAgIHt7IGxvY2FsZVsnQW5jaG9yIEF0dHJpYnV0ZXMnXSB9fVxuICAgICAgICA8L2VsLWFuY2hvci1saW5rPlxuICAgICAgICA8ZWwtYW5jaG9yLWxpbmsgOmhyZWY9XCJgIyR7bG9jYWxlWydhbmNob3ItZXZlbnRzJ119YFwiPlxuICAgICAgICAgIHt7IGxvY2FsZVsnQW5jaG9yIEV2ZW50cyddIH19XG4gICAgICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gIDwvZWwtYW5jaG9yPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGNvbXB1dGVkIH0gZnJvbSAndnVlJ1xuaW1wb3J0IGFuY2hvckxvY2FsZSBmcm9tICcuLi8uLi8udml0ZXByZXNzL2kxOG4vY29tcG9uZW50L2FuY2hvci5qc29uJ1xuaW1wb3J0IHsgdXNlTGFuZyB9IGZyb20gJ34vY29tcG9zYWJsZXMvbGFuZydcblxuY29uc3QgbGFuZyA9IHVzZUxhbmcoKVxuY29uc3QgbG9jYWxlID0gY29tcHV0ZWQoKCkgPT4gYW5jaG9yTG9jYWxlW2xhbmcudmFsdWVdKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/anchor/underline.vue)_

vue

```
<template>
  <el-anchor type="underline" :offset="70">
    <el-anchor-link :href="`#${locale['basic-usage']}`">
      {{ locale['Basic Usage'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['horizontal-mode']}`">
      {{ locale['Horizontal Mode'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['scroll-container']}`">
      {{ locale['Scroll Container'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['anchor-api']}`">
      {{ locale['Anchor API'] }}
      <template #sub-link>
        <el-anchor-link :href="`#${locale['anchor-attributes']}`">
          {{ locale['Anchor Attributes'] }}
        </el-anchor-link>
        <el-anchor-link :href="`#${locale['anchor-events']}`">
          {{ locale['Anchor Events'] }}
        </el-anchor-link>
      </template>
    </el-anchor-link>
  </el-anchor>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import anchorLocale from '../../.vitepress/i18n/component/anchor.json'
import { useLang } from '~/composables/lang'

const lang = useLang()
const locale = computed(() => anchorLocale[lang.value])
</script>
```

隐藏源代码

## 固定模式 [​](#固定模式)

使用 affix 组件来固定住页面中的锚点。

[基础用法](#基础用法)

[水平模式](#水平模式)

[滚动容器](#滚动的容器)

[Anchor API](#anchor-api)

[Anchor Attributes](#anchor-attributes)

[Anchor Events](#anchor-events)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYWZmaXggOm9mZnNldD1cIjYwXCI+XG4gICAgPGVsLWFuY2hvciA6b2Zmc2V0PVwiNzBcIiBzdHlsZT1cIndpZHRoOiAzMDBweFwiPlxuICAgICAgPGVsLWFuY2hvci1saW5rIDpocmVmPVwiYCMke2xvY2FsZVsnYmFzaWMtdXNhZ2UnXX1gXCI+XG4gICAgICAgIHt7IGxvY2FsZVsnQmFzaWMgVXNhZ2UnXSB9fVxuICAgICAgPC9lbC1hbmNob3ItbGluaz5cbiAgICAgIDxlbC1hbmNob3ItbGluayA6aHJlZj1cImAjJHtsb2NhbGVbJ2hvcml6b250YWwtbW9kZSddfWBcIj5cbiAgICAgICAge3sgbG9jYWxlWydIb3Jpem9udGFsIE1vZGUnXSB9fVxuICAgICAgPC9lbC1hbmNob3ItbGluaz5cbiAgICAgIDxlbC1hbmNob3ItbGluayA6aHJlZj1cImAjJHtsb2NhbGVbJ3Njcm9sbC1jb250YWluZXInXX1gXCI+XG4gICAgICAgIHt7IGxvY2FsZVsnU2Nyb2xsIENvbnRhaW5lciddIH19XG4gICAgICA8L2VsLWFuY2hvci1saW5rPlxuICAgICAgPGVsLWFuY2hvci1saW5rIDpocmVmPVwiYCMke2xvY2FsZVsnYW5jaG9yLWFwaSddfWBcIj5cbiAgICAgICAge3sgbG9jYWxlWydBbmNob3IgQVBJJ10gfX1cbiAgICAgICAgPHRlbXBsYXRlICNzdWItbGluaz5cbiAgICAgICAgICA8ZWwtYW5jaG9yLWxpbmsgOmhyZWY9XCJgIyR7bG9jYWxlWydhbmNob3ItYXR0cmlidXRlcyddfWBcIj5cbiAgICAgICAgICAgIHt7IGxvY2FsZVsnQW5jaG9yIEF0dHJpYnV0ZXMnXSB9fVxuICAgICAgICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgICAgICAgPGVsLWFuY2hvci1saW5rIDpocmVmPVwiYCMke2xvY2FsZVsnYW5jaG9yLWV2ZW50cyddfWBcIj5cbiAgICAgICAgICAgIHt7IGxvY2FsZVsnQW5jaG9yIEV2ZW50cyddIH19XG4gICAgICAgICAgPC9lbC1hbmNob3ItbGluaz5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtYW5jaG9yLWxpbms+XG4gICAgPC9lbC1hbmNob3I+XG4gIDwvZWwtYWZmaXg+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgY29tcHV0ZWQgfSBmcm9tICd2dWUnXG5pbXBvcnQgYW5jaG9yTG9jYWxlIGZyb20gJy4uLy4uLy52aXRlcHJlc3MvaTE4bi9jb21wb25lbnQvYW5jaG9yLmpzb24nXG5pbXBvcnQgeyB1c2VMYW5nIH0gZnJvbSAnfi9jb21wb3NhYmxlcy9sYW5nJ1xuXG5jb25zdCBsYW5nID0gdXNlTGFuZygpXG5jb25zdCBsb2NhbGUgPSBjb21wdXRlZCgoKSA9PiBhbmNob3JMb2NhbGVbbGFuZy52YWx1ZV0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/anchor/affix.vue)_

vue

```
<template>
  <el-affix :offset="60">
    <el-anchor :offset="70" style="width: 300px">
      <el-anchor-link :href="`#${locale['basic-usage']}`">
        {{ locale['Basic Usage'] }}
      </el-anchor-link>
      <el-anchor-link :href="`#${locale['horizontal-mode']}`">
        {{ locale['Horizontal Mode'] }}
      </el-anchor-link>
      <el-anchor-link :href="`#${locale['scroll-container']}`">
        {{ locale['Scroll Container'] }}
      </el-anchor-link>
      <el-anchor-link :href="`#${locale['anchor-api']}`">
        {{ locale['Anchor API'] }}
        <template #sub-link>
          <el-anchor-link :href="`#${locale['anchor-attributes']}`">
            {{ locale['Anchor Attributes'] }}
          </el-anchor-link>
          <el-anchor-link :href="`#${locale['anchor-events']}`">
            {{ locale['Anchor Events'] }}
          </el-anchor-link>
        </template>
      </el-anchor-link>
    </el-anchor>
  </el-affix>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import anchorLocale from '../../.vitepress/i18n/component/anchor.json'
import { useLang } from '~/composables/lang'

const lang = useLang()
const locale = computed(() => anchorLocale[lang.value])
</script>
```

隐藏源代码

## Anchor API [​](#anchor-api)

### 属性 [​](#属性)

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| container | 滚动的容器 | `string` | `HTMLElement` | `Window` | — |
| offset | 设置锚点滚动的偏移量 | `number` | 0 |
| bound | 触发锚点的元素的位置偏移量 | `number` | 15 |
| duration | 设置容器滚动持续时间，单位为毫秒 | `number` | 300 |
| marker | 是否显示标记 | `boolean` | true |
| type | 设置锚点类型 | `enum` | `default` |
| direction | 设置锚点方向 | `enum` | `vertical` |
| select-scroll-top 2.9.2 | 滚动时，链接是否选中位于顶部 | `boolean` | false |

### Anchor Events [​](#anchor-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | step 改变时的回调 | `Function` |
| click | 当用户点击链接时触发 | `Function` |

### Anchor Exposes [​](#anchor-exposes)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| scrollTo | 手动滚动到特定位置。 | `Function` |

### Anchor Slots [​](#anchor-slots)

| 名称 | 说明 |
| --- | --- |
| default | AnchorLink 组件列表 |

### AnchorLink Attributes [​](#anchorlink-attributes)

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| title | 链接的文本内容 | `string` | — |
| href | 链接的地址。 | `string` | — |

### AnchorLink Slots [​](#anchorlink-slots)

| 名称 | 说明 |
| --- | --- |
| default | 链接的内容 |
| sub-link | 子链接的槽位 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/anchor) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/anchor.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/anchor.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/27912232?v=4&size=64)](https://github.com/Fuphoenixes)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/45098544?v=4&size=64)](https://github.com/tuzixiangs)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/48147837?v=4&size=64)](https://github.com/kcmeven)[![](https://avatars.githubusercontent.com/u/45616067?v=4&size=64)](https://github.com/elioist)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/8591261?v=4&size=64)](https://github.com/zeyongTsai)[![](https://avatars.githubusercontent.com/u/22683538?v=4&size=64)](https://github.com/hanyueqiang)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)

[Affix 固钉](https://element-plus.org/zh-CN/component/affix)

[Backtop 回到顶部](https://element-plus.org/zh-CN/component/backtop)


