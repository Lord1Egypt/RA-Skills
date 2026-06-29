---
name: "typography"
description: "Typography 排版 -- Element Plus Vue3 桌面端组件。Invoke when user needs Typography 排版 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/typography.html"
---

---

# Typography 排版 [​](#typography-排版)

我们对字体进行统一规范，力求在各个操作系统下都有最佳展示效果。

## 字体 [​](#字体)

![](https://element-plus.org/images/typography/term-pingfang.png)![](https://element-plus.org/images/typography/term-hiragino.png)![](https://element-plus.org/images/typography/term-microsoft.png)![](https://element-plus.org/images/typography/term-helvetica.png)![](https://element-plus.org/images/typography/term-arial.png)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGlzRGFyayB9IGZyb20gJ34vY29tcG9zYWJsZXMvZGFyaydcbjwvc2NyaXB0PlxuXG48dGVtcGxhdGU+XG4gIDxkaXYgdi1pZj1cIiFpc0RhcmtcIiBjbGFzcz1cImRlbW8tdGVybS1ib3hcIj5cbiAgICA8aW1nIHNyYz1cIi9pbWFnZXMvdHlwb2dyYXBoeS90ZXJtLXBpbmdmYW5nLnBuZ1wiIGFsdD1cIlwiIC8+XG4gICAgPGltZyBzcmM9XCIvaW1hZ2VzL3R5cG9ncmFwaHkvdGVybS1oaXJhZ2luby5wbmdcIiBhbHQ9XCJcIiAvPlxuICAgIDxpbWcgc3JjPVwiL2ltYWdlcy90eXBvZ3JhcGh5L3Rlcm0tbWljcm9zb2Z0LnBuZ1wiIGFsdD1cIlwiIC8+XG4gICAgPGltZyBzcmM9XCIvaW1hZ2VzL3R5cG9ncmFwaHkvdGVybS1oZWx2ZXRpY2EucG5nXCIgYWx0PVwiXCIgLz5cbiAgICA8aW1nIHNyYz1cIi9pbWFnZXMvdHlwb2dyYXBoeS90ZXJtLWFyaWFsLnBuZ1wiIGFsdD1cIlwiIC8+XG4gIDwvZGl2PlxuICA8ZGl2IHYtZWxzZSBjbGFzcz1cImRlbW8tdGVybS1ib3hcIj5cbiAgICA8aW1nIHNyYz1cIi9pbWFnZXMvdHlwb2dyYXBoeS90ZXJtLXBpbmdmYW5nLWRhcmsucG5nXCIgYWx0PVwiXCIgLz5cbiAgICA8aW1nIHNyYz1cIi9pbWFnZXMvdHlwb2dyYXBoeS90ZXJtLWhpcmFnaW5vLWRhcmsucG5nXCIgYWx0PVwiXCIgLz5cbiAgICA8aW1nIHNyYz1cIi9pbWFnZXMvdHlwb2dyYXBoeS90ZXJtLW1pY3Jvc29mdC1kYXJrLnBuZ1wiIGFsdD1cIlwiIC8+XG4gICAgPGltZyBzcmM9XCIvaW1hZ2VzL3R5cG9ncmFwaHkvdGVybS1oZWx2ZXRpY2EtZGFyay5wbmdcIiBhbHQ9XCJcIiAvPlxuICAgIDxpbWcgc3JjPVwiL2ltYWdlcy90eXBvZ3JhcGh5L3Rlcm0tYXJpYWwtZGFyay5wbmdcIiBhbHQ9XCJcIiAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG5pbWcge1xuICB3aWR0aDogMjIwcHg7XG4gIGhlaWdodDogMTc0cHg7XG4gIG1hcmdpbjogMCAyNHB4IDI0cHggMDtcbn1cbmltZzpudGgtb2YtdHlwZSgzKSB7XG4gIG1hcmdpbi1yaWdodDogMDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/typography/font.vue)_

vue

```
<script lang="ts" setup>
import { isDark } from '~/composables/dark'
</script>

<template>
  <div v-if="!isDark" class="demo-term-box">
    <img src="/images/typography/term-pingfang.png" alt="" />
    <img src="/images/typography/term-hiragino.png" alt="" />
    <img src="/images/typography/term-microsoft.png" alt="" />
    <img src="/images/typography/term-helvetica.png" alt="" />
    <img src="/images/typography/term-arial.png" alt="" />
  </div>
  <div v-else class="demo-term-box">
    <img src="/images/typography/term-pingfang-dark.png" alt="" />
    <img src="/images/typography/term-hiragino-dark.png" alt="" />
    <img src="/images/typography/term-microsoft-dark.png" alt="" />
    <img src="/images/typography/term-helvetica-dark.png" alt="" />
    <img src="/images/typography/term-arial-dark.png" alt="" />
  </div>
</template>

<style scoped>
img {
  width: 220px;
  height: 174px;
  margin: 0 24px 24px 0;
}
img:nth-of-type(3) {
  margin-right: 0;
}
</style>
```

隐藏源代码

## 字号 [​](#字号)

<table class="demo-typo-size"><tbody><tr><td>Level</td><td>Font Size</td><td class="color-dark-light">Demo</td></tr><tr style="font-size: var(--el-font-size-extra-small)"><td>Supplementary text</td><td>12px Extra Small</td><td>Build with Element</td></tr><tr style="font-size: var(--el-font-size-small)"><td>Body (small)</td><td>13px Small</td><td>Build with Element</td></tr><tr style="font-size: var(--el-font-size-base)"><td>Body</td><td>14px Base</td><td>Build with Element</td></tr><tr style="font-size: var(--el-font-size-medium)"><td>Small Title</td><td>16px Medium</td><td>Build with Element</td></tr><tr style="font-size: var(--el-font-size-large)"><td>Title</td><td>18px Large</td><td>Build with Element</td></tr><tr style="font-size: var(--el-font-size-extra-large)"><td>Main Title</td><td>20px Extra Large</td><td>Build with Element</td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/?extra_packages=%40vueuse%2Fcore#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8dGFibGUgY2xhc3M9XCJkZW1vLXR5cG8tc2l6ZVwiPlxuICAgIDx0Ym9keT5cbiAgICAgIDx0cj5cbiAgICAgICAgPHRkPkxldmVsPC90ZD5cbiAgICAgICAgPHRkPkZvbnQgU2l6ZTwvdGQ+XG4gICAgICAgIDx0ZCBjbGFzcz1cImNvbG9yLWRhcmstbGlnaHRcIj5EZW1vPC90ZD5cbiAgICAgIDwvdHI+XG4gICAgICA8dHJcbiAgICAgICAgdi1mb3I9XCIoZm9udFNpemUsIGkpIGluIGZvbnRTaXplc1wiXG4gICAgICAgIDprZXk9XCJpXCJcbiAgICAgICAgOnN0eWxlPVwiYGZvbnQtc2l6ZTogdmFyKC0tZWwtZm9udC1zaXplLSR7Zm9udFNpemUudHlwZX0pYFwiXG4gICAgICA+XG4gICAgICAgIDx0ZD57eyBmb250U2l6ZS5sZXZlbCB9fTwvdGQ+XG4gICAgICAgIDx0ZD5cbiAgICAgICAgICB7e1xuICAgICAgICAgICAgdXNlQ3NzVmFyKGAtLWVsLWZvbnQtc2l6ZS0ke2ZvbnRTaXplLnR5cGV9YCkudmFsdWUgK1xuICAgICAgICAgICAgJyAnICtcbiAgICAgICAgICAgIGZvcm1hdFR5cGUoZm9udFNpemUudHlwZSlcbiAgICAgICAgICB9fVxuICAgICAgICA8L3RkPlxuICAgICAgICA8dGQ+QnVpbGQgd2l0aCBFbGVtZW50PC90ZD5cbiAgICAgIDwvdHI+XG4gICAgPC90Ym9keT5cbiAgPC90YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyB1c2VDc3NWYXIgfSBmcm9tICdAdnVldXNlL2NvcmUnXG5cbmNvbnN0IGZvbnRTaXplcyA9IFtcbiAge1xuICAgIGxldmVsOiAnU3VwcGxlbWVudGFyeSB0ZXh0JyxcbiAgICB0eXBlOiAnZXh0cmEtc21hbGwnLFxuICB9LFxuICB7XG4gICAgbGV2ZWw6ICdCb2R5IChzbWFsbCknLFxuICAgIHR5cGU6ICdzbWFsbCcsXG4gIH0sXG4gIHtcbiAgICBsZXZlbDogJ0JvZHknLFxuICAgIHR5cGU6ICdiYXNlJyxcbiAgfSxcbiAge1xuICAgIGxldmVsOiAnU21hbGwgVGl0bGUnLFxuICAgIHR5cGU6ICdtZWRpdW0nLFxuICB9LFxuICB7XG4gICAgbGV2ZWw6ICdUaXRsZScsXG4gICAgdHlwZTogJ2xhcmdlJyxcbiAgfSxcbiAge1xuICAgIGxldmVsOiAnTWFpbiBUaXRsZScsXG4gICAgdHlwZTogJ2V4dHJhLWxhcmdlJyxcbiAgfSxcbl1cblxuZnVuY3Rpb24gZm9ybWF0VHlwZSh0eXBlOiBzdHJpbmcpIHtcbiAgcmV0dXJuIHR5cGVcbiAgICAuc3BsaXQoJy0nKVxuICAgIC5tYXAoKGl0ZW0pID0+IGl0ZW0uY2hhckF0KDApLnRvVXBwZXJDYXNlKCkgKyBpdGVtLnNsaWNlKDEpKVxuICAgIC5qb2luKCcgJylcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/typography/convention.vue)_

vue

```
<template>
  <table class="demo-typo-size">
    <tbody>
      <tr>
        <td>Level</td>
        <td>Font Size</td>
        <td class="color-dark-light">Demo</td>
      </tr>
      <tr
        v-for="(fontSize, i) in fontSizes"
        :key="i"
        :style="`font-size: var(--el-font-size-${fontSize.type})`"
      >
        <td>{{ fontSize.level }}</td>
        <td>
          {{
            useCssVar(`--el-font-size-${fontSize.type}`).value +
            ' ' +
            formatType(fontSize.type)
          }}
        </td>
        <td>Build with Element</td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts" setup>
import { useCssVar } from '@vueuse/core'

const fontSizes = [
  {
    level: 'Supplementary text',
    type: 'extra-small',
  },
  {
    level: 'Body (small)',
    type: 'small',
  },
  {
    level: 'Body',
    type: 'base',
  },
  {
    level: 'Small Title',
    type: 'medium',
  },
  {
    level: 'Title',
    type: 'large',
  },
  {
    level: 'Main Title',
    type: 'extra-large',
  },
]

function formatType(type: string) {
  return type
    .split('-')
    .map((item) => item.charAt(0).toUpperCase() + item.slice(1))
    .join(' ')
}
</script>
```

隐藏源代码

## 行高 [​](#行高)

![](https://element-plus.org/images/typography/line-height.png)

-   line-height:1 No line height
-   line-height:1.3 Compact
-   line-height:1.5 Regular
-   line-height:1.7 Loose

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGlzRGFyayB9IGZyb20gJ34vY29tcG9zYWJsZXMvZGFyaydcbjwvc2NyaXB0PlxuXG48dGVtcGxhdGU+XG4gIDxkaXY+XG4gICAgPGltZ1xuICAgICAgdi1pZj1cImlzRGFya1wiXG4gICAgICBjbGFzcz1cImxpbmVILWxlZnRcIlxuICAgICAgc3JjPVwiL2ltYWdlcy90eXBvZ3JhcGh5L2xpbmUtaGVpZ2h0LWRhcmsucG5nXCJcbiAgICAvPlxuICAgIDxpbWcgdi1lbHNlIGNsYXNzPVwibGluZUgtbGVmdFwiIHNyYz1cIi9pbWFnZXMvdHlwb2dyYXBoeS9saW5lLWhlaWdodC5wbmdcIiAvPlxuICAgIDx1bCBjbGFzcz1cImxpbmVILXJpZ2h0XCI+XG4gICAgICA8bGk+bGluZS1oZWlnaHQ6MSA8c3Bhbj5ObyBsaW5lIGhlaWdodDwvc3Bhbj48L2xpPlxuICAgICAgPGxpPmxpbmUtaGVpZ2h0OjEuMyA8c3Bhbj5Db21wYWN0PC9zcGFuPjwvbGk+XG4gICAgICA8bGk+bGluZS1oZWlnaHQ6MS41IDxzcGFuPlJlZ3VsYXI8L3NwYW4+PC9saT5cbiAgICAgIDxsaT5saW5lLWhlaWdodDoxLjcgPHNwYW4+TG9vc2U8L3NwYW4+PC9saT5cbiAgICA8L3VsPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/typography/line-height.vue)_

vue

```
<script lang="ts" setup>
import { isDark } from '~/composables/dark'
</script>

<template>
  <div>
    <img
      v-if="isDark"
      class="lineH-left"
      src="/images/typography/line-height-dark.png"
    />
    <img v-else class="lineH-left" src="/images/typography/line-height.png" />
    <ul class="lineH-right">
      <li>line-height:1 <span>No line height</span></li>
      <li>line-height:1.3 <span>Compact</span></li>
      <li>line-height:1.5 <span>Regular</span></li>
      <li>line-height:1.7 <span>Loose</span></li>
    </ul>
  </div>
</template>
```

隐藏源代码

## Font-family [​](#font-family)

css

```
font-family:
  Inter, 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
  'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
```

## 源代码 [​](#源代码)

[文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/typography.md)

[Splitter 分隔面板](https://element-plus.org/zh-CN/component/splitter)

[Config Provider 全局配置](https://element-plus.org/zh-CN/component/config-provider)


