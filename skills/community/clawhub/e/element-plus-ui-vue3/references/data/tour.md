---
name: "tour"
description: "Tour 漫游式引导 -- Element Plus Vue3 桌面端组件。Invoke when user needs Tour 漫游式引导 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/tour.html"
---

---

# Tour 漫游式引导 [​](#tour-漫游式引导)

更新日志待解决

0

用于分步引导用户了解产品功能的气泡组件。 用来引导用户并介绍产品

## 基础用法 [​](#基础用法)

最简单的用法。

Begin Tour

Upload

Save

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwib3BlbiA9IHRydWVcIj5CZWdpbiBUb3VyPC9lbC1idXR0b24+XG5cbiAgPGVsLWRpdmlkZXIgLz5cblxuICA8ZWwtc3BhY2U+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYxXCI+VXBsb2FkPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYyXCIgdHlwZT1cInByaW1hcnlcIj5TYXZlPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYzXCIgOmljb249XCJNb3JlRmlsbGVkXCIgLz5cbiAgPC9lbC1zcGFjZT5cblxuICA8ZWwtdG91ciB2LW1vZGVsPVwib3BlblwiPlxuICAgIDxlbC10b3VyLXN0ZXAgOnRhcmdldD1cInJlZjE/LiRlbFwiIHRpdGxlPVwiVXBsb2FkIEZpbGVcIj5cbiAgICAgIDxpbWdcbiAgICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgICBzcmM9XCJodHRwczovL2VsZW1lbnQtcGx1cy5vcmcvaW1hZ2VzL2VsZW1lbnQtcGx1cy1sb2dvLnN2Z1wiXG4gICAgICAgIGFsdD1cInRvdXIucG5nXCJcbiAgICAgIC8+XG4gICAgICA8ZGl2PlB1dCB5b3UgZmlsZXMgaGVyZS48L2Rpdj5cbiAgICA8L2VsLXRvdXItc3RlcD5cbiAgICA8ZWwtdG91ci1zdGVwXG4gICAgICA6dGFyZ2V0PVwicmVmMj8uJGVsXCJcbiAgICAgIHRpdGxlPVwiU2F2ZVwiXG4gICAgICBkZXNjcmlwdGlvbj1cIlNhdmUgeW91ciBjaGFuZ2VzXCJcbiAgICAvPlxuICAgIDxlbC10b3VyLXN0ZXBcbiAgICAgIDp0YXJnZXQ9XCJyZWYzPy4kZWxcIlxuICAgICAgdGl0bGU9XCJPdGhlciBBY3Rpb25zXCJcbiAgICAgIGRlc2NyaXB0aW9uPVwiQ2xpY2sgdG8gc2VlIG90aGVyXCJcbiAgICAvPlxuICA8L2VsLXRvdXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgTW9yZUZpbGxlZCB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5pbXBvcnQgdHlwZSB7IEJ1dHRvbkluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCByZWYxID0gcmVmPEJ1dHRvbkluc3RhbmNlPigpXG5jb25zdCByZWYyID0gcmVmPEJ1dHRvbkluc3RhbmNlPigpXG5jb25zdCByZWYzID0gcmVmPEJ1dHRvbkluc3RhbmNlPigpXG5cbmNvbnN0IG9wZW4gPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tour/basic.vue)_

vue

```
<template>
  <el-button type="primary" @click="open = true">Begin Tour</el-button>

  <el-divider />

  <el-space>
    <el-button ref="ref1">Upload</el-button>
    <el-button ref="ref2" type="primary">Save</el-button>
    <el-button ref="ref3" :icon="MoreFilled" />
  </el-space>

  <el-tour v-model="open">
    <el-tour-step :target="ref1?.$el" title="Upload File">
      <img
        style="width: 240px"
        src="https://element-plus.org/images/element-plus-logo.svg"
        alt="tour.png"
      />
      <div>Put you files here.</div>
    </el-tour-step>
    <el-tour-step
      :target="ref2?.$el"
      title="Save"
      description="Save your changes"
    />
    <el-tour-step
      :target="ref3?.$el"
      title="Other Actions"
      description="Click to see other"
    />
  </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MoreFilled } from '@element-plus/icons-vue'

import type { ButtonInstance } from 'element-plus'

const ref1 = ref<ButtonInstance>()
const ref2 = ref<ButtonInstance>()
const ref3 = ref<ButtonInstance>()

const open = ref(false)
</script>
```

隐藏源代码

## 非模态 [​](#非模态)

使用`:mask="false"`可以将引导变为非模态， 同时为了强调引导本身，建议与 type="primary" 组合使用。

Begin Tour

Upload

Save

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwib3BlbiA9IHRydWVcIj5CZWdpbiBUb3VyPC9lbC1idXR0b24+XG5cbiAgPGVsLWRpdmlkZXIgLz5cblxuICA8ZWwtc3BhY2U+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYxXCI+VXBsb2FkPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYyXCIgdHlwZT1cInByaW1hcnlcIj5TYXZlPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYzXCIgOmljb249XCJNb3JlRmlsbGVkXCIgLz5cbiAgPC9lbC1zcGFjZT5cblxuICA8ZWwtdG91ciB2LW1vZGVsPVwib3BlblwiIHR5cGU9XCJwcmltYXJ5XCIgOm1hc2s9XCJmYWxzZVwiPlxuICAgIDxlbC10b3VyLXN0ZXBcbiAgICAgIDp0YXJnZXQ9XCJyZWYxPy4kZWxcIlxuICAgICAgdGl0bGU9XCJVcGxvYWQgRmlsZVwiXG4gICAgICBkZXNjcmlwdGlvbj1cIlB1dCB5b3UgZmlsZXMgaGVyZS5cIlxuICAgIC8+XG4gICAgPGVsLXRvdXItc3RlcFxuICAgICAgOnRhcmdldD1cInJlZjI/LiRlbFwiXG4gICAgICB0aXRsZT1cIlNhdmVcIlxuICAgICAgZGVzY3JpcHRpb249XCJTYXZlIHlvdXIgY2hhbmdlc1wiXG4gICAgLz5cbiAgICA8ZWwtdG91ci1zdGVwXG4gICAgICA6dGFyZ2V0PVwicmVmMz8uJGVsXCJcbiAgICAgIHRpdGxlPVwiT3RoZXIgQWN0aW9uc1wiXG4gICAgICBkZXNjcmlwdGlvbj1cIkNsaWNrIHRvIHNlZSBvdGhlclwiXG4gICAgLz5cbiAgPC9lbC10b3VyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IE1vcmVGaWxsZWQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuaW1wb3J0IHR5cGUgeyBCdXR0b25JbnN0YW5jZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgcmVmMSA9IHJlZjxCdXR0b25JbnN0YW5jZT4oKVxuY29uc3QgcmVmMiA9IHJlZjxCdXR0b25JbnN0YW5jZT4oKVxuY29uc3QgcmVmMyA9IHJlZjxCdXR0b25JbnN0YW5jZT4oKVxuXG5jb25zdCBvcGVuID0gcmVmKGZhbHNlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tour/non-modal.vue)_

vue

```
<template>
  <el-button type="primary" @click="open = true">Begin Tour</el-button>

  <el-divider />

  <el-space>
    <el-button ref="ref1">Upload</el-button>
    <el-button ref="ref2" type="primary">Save</el-button>
    <el-button ref="ref3" :icon="MoreFilled" />
  </el-space>

  <el-tour v-model="open" type="primary" :mask="false">
    <el-tour-step
      :target="ref1?.$el"
      title="Upload File"
      description="Put you files here."
    />
    <el-tour-step
      :target="ref2?.$el"
      title="Save"
      description="Save your changes"
    />
    <el-tour-step
      :target="ref3?.$el"
      title="Other Actions"
      description="Click to see other"
    />
  </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MoreFilled } from '@element-plus/icons-vue'

import type { ButtonInstance } from 'element-plus'

const ref1 = ref<ButtonInstance>()
const ref2 = ref<ButtonInstance>()
const ref3 = ref<ButtonInstance>()

const open = ref(false)
</script>
```

隐藏源代码

## 位置 [​](#位置)

改变引导相对于目标的位置，共有 12 种位置可供选择。 当 `target` 为空时引导将会展示在正中央。

Begin Tour

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHJlZj1cImJ0blJlZlwiIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwib3BlbiA9IHRydWVcIj5cbiAgICBCZWdpbiBUb3VyXG4gIDwvZWwtYnV0dG9uPlxuXG4gIDxlbC10b3VyIHYtbW9kZWw9XCJvcGVuXCI+XG4gICAgPGVsLXRvdXItc3RlcFxuICAgICAgdGl0bGU9XCJDZW50ZXJcIlxuICAgICAgZGVzY3JpcHRpb249XCJEaXNwbGF5ZWQgaW4gdGhlIGNlbnRlciBvZiBzY3JlZW4uXCJcbiAgICAvPlxuICAgIDxlbC10b3VyLXN0ZXBcbiAgICAgIHRpdGxlPVwiUmlnaHRcIlxuICAgICAgZGVzY3JpcHRpb249XCJPbiB0aGUgcmlnaHQgb2YgdGFyZ2V0LlwiXG4gICAgICBwbGFjZW1lbnQ9XCJyaWdodFwiXG4gICAgICA6dGFyZ2V0PVwiYnRuUmVmPy4kZWxcIlxuICAgIC8+XG4gICAgPGVsLXRvdXItc3RlcFxuICAgICAgdGl0bGU9XCJUb3BcIlxuICAgICAgZGVzY3JpcHRpb249XCJPbiB0aGUgdG9wIG9mIHRhcmdldC5cIlxuICAgICAgcGxhY2VtZW50PVwidG9wXCJcbiAgICAgIDp0YXJnZXQ9XCJidG5SZWY/LiRlbFwiXG4gICAgLz5cbiAgPC9lbC10b3VyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBCdXR0b25JbnN0YW5jZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgYnRuUmVmID0gcmVmPEJ1dHRvbkluc3RhbmNlPigpXG5cbmNvbnN0IG9wZW4gPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tour/placement.vue)_

vue

```
<template>
  <el-button ref="btnRef" type="primary" @click="open = true">
    Begin Tour
  </el-button>

  <el-tour v-model="open">
    <el-tour-step
      title="Center"
      description="Displayed in the center of screen."
    />
    <el-tour-step
      title="Right"
      description="On the right of target."
      placement="right"
      :target="btnRef?.$el"
    />
    <el-tour-step
      title="Top"
      description="On the top of target."
      placement="top"
      :target="btnRef?.$el"
    />
  </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import type { ButtonInstance } from 'element-plus'

const btnRef = ref<ButtonInstance>()

const open = ref(false)
</script>
```

隐藏源代码

## 自定义遮罩样式 [​](#自定义遮罩样式)

自定义遮罩样式。

Begin Tour

Upload

Save

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwib3BlbiA9IHRydWVcIj5CZWdpbiBUb3VyPC9lbC1idXR0b24+XG5cbiAgPGVsLWRpdmlkZXIgLz5cblxuICA8ZWwtc3BhY2U+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYxXCI+VXBsb2FkPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYyXCIgdHlwZT1cInByaW1hcnlcIj5TYXZlPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYzXCIgOmljb249XCJNb3JlRmlsbGVkXCIgLz5cbiAgPC9lbC1zcGFjZT5cblxuICA8ZWwtdG91clxuICAgIHYtbW9kZWw9XCJvcGVuXCJcbiAgICA6bWFzaz1cIntcbiAgICAgIHN0eWxlOiB7XG4gICAgICAgIGJveFNoYWRvdzogJ2luc2V0IDAgMCAxNXB4ICMzMzMnLFxuICAgICAgfSxcbiAgICAgIGNvbG9yOiAncmdiYSg4MCwgMjU1LCAyNTUsIC40KScsXG4gICAgfVwiXG4gID5cbiAgICA8ZWwtdG91ci1zdGVwIDp0YXJnZXQ9XCJyZWYxPy4kZWxcIiB0aXRsZT1cIlVwbG9hZCBGaWxlXCI+XG4gICAgICA8aW1nXG4gICAgICAgIHNyYz1cImh0dHBzOi8vZWxlbWVudC1wbHVzLm9yZy9pbWFnZXMvZWxlbWVudC1wbHVzLWxvZ28uc3ZnXCJcbiAgICAgICAgYWx0PVwidG91ci5wbmdcIlxuICAgICAgLz5cbiAgICAgIDxkaXY+UHV0IHlvdSBmaWxlcyBoZXJlLjwvZGl2PlxuICAgIDwvZWwtdG91ci1zdGVwPlxuICAgIDxlbC10b3VyLXN0ZXBcbiAgICAgIDp0YXJnZXQ9XCJyZWYyPy4kZWxcIlxuICAgICAgdGl0bGU9XCJTYXZlXCJcbiAgICAgIGRlc2NyaXB0aW9uPVwiU2F2ZSB5b3VyIGNoYW5nZXNcIlxuICAgICAgOm1hc2s9XCJ7XG4gICAgICAgIHN0eWxlOiB7XG4gICAgICAgICAgYm94U2hhZG93OiAnaW5zZXQgMCAwIDE1cHggI2ZmZicsXG4gICAgICAgIH0sXG4gICAgICAgIGNvbG9yOiAncmdiYSg0MCwgMCwgMjU1LCAuNCknLFxuICAgICAgfVwiXG4gICAgLz5cbiAgICA8ZWwtdG91ci1zdGVwXG4gICAgICA6dGFyZ2V0PVwicmVmMz8uJGVsXCJcbiAgICAgIHRpdGxlPVwiT3RoZXIgQWN0aW9uc1wiXG4gICAgICBkZXNjcmlwdGlvbj1cIkNsaWNrIHRvIHNlZSBvdGhlclwiXG4gICAgICA6bWFzaz1cImZhbHNlXCJcbiAgICAvPlxuICA8L2VsLXRvdXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgTW9yZUZpbGxlZCB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5pbXBvcnQgdHlwZSB7IEJ1dHRvbkluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCByZWYxID0gcmVmPEJ1dHRvbkluc3RhbmNlPigpXG5jb25zdCByZWYyID0gcmVmPEJ1dHRvbkluc3RhbmNlPigpXG5jb25zdCByZWYzID0gcmVmPEJ1dHRvbkluc3RhbmNlPigpXG5cbmNvbnN0IG9wZW4gPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tour/mask.vue)_

vue

```
<template>
  <el-button type="primary" @click="open = true">Begin Tour</el-button>

  <el-divider />

  <el-space>
    <el-button ref="ref1">Upload</el-button>
    <el-button ref="ref2" type="primary">Save</el-button>
    <el-button ref="ref3" :icon="MoreFilled" />
  </el-space>

  <el-tour
    v-model="open"
    :mask="{
      style: {
        boxShadow: 'inset 0 0 15px #333',
      },
      color: 'rgba(80, 255, 255, .4)',
    }"
  >
    <el-tour-step :target="ref1?.$el" title="Upload File">
      <img
        src="https://element-plus.org/images/element-plus-logo.svg"
        alt="tour.png"
      />
      <div>Put you files here.</div>
    </el-tour-step>
    <el-tour-step
      :target="ref2?.$el"
      title="Save"
      description="Save your changes"
      :mask="{
        style: {
          boxShadow: 'inset 0 0 15px #fff',
        },
        color: 'rgba(40, 0, 255, .4)',
      }"
    />
    <el-tour-step
      :target="ref3?.$el"
      title="Other Actions"
      description="Click to see other"
      :mask="false"
    />
  </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MoreFilled } from '@element-plus/icons-vue'

import type { ButtonInstance } from 'element-plus'

const ref1 = ref<ButtonInstance>()
const ref2 = ref<ButtonInstance>()
const ref3 = ref<ButtonInstance>()

const open = ref(false)
</script>
```

隐藏源代码

## 自定义指示器 [​](#自定义指示器)

自定义指示器。

Begin Tour

Upload

Save

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwib3BlbiA9IHRydWVcIj5CZWdpbiBUb3VyPC9lbC1idXR0b24+XG5cbiAgPGVsLWRpdmlkZXIgLz5cblxuICA8ZWwtc3BhY2U+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYxXCI+VXBsb2FkPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYyXCIgdHlwZT1cInByaW1hcnlcIj5TYXZlPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiByZWY9XCJyZWYzXCIgOmljb249XCJNb3JlRmlsbGVkXCIgLz5cbiAgPC9lbC1zcGFjZT5cblxuICA8ZWwtdG91ciB2LW1vZGVsPVwib3BlblwiPlxuICAgIDxlbC10b3VyLXN0ZXBcbiAgICAgIDp0YXJnZXQ9XCJyZWYxPy4kZWxcIlxuICAgICAgdGl0bGU9XCJVcGxvYWQgRmlsZVwiXG4gICAgICBkZXNjcmlwdGlvbj1cIlB1dCB5b3UgZmlsZXMgaGVyZS5cIlxuICAgIC8+XG4gICAgPGVsLXRvdXItc3RlcFxuICAgICAgOnRhcmdldD1cInJlZjI/LiRlbFwiXG4gICAgICB0aXRsZT1cIlNhdmVcIlxuICAgICAgZGVzY3JpcHRpb249XCJTYXZlIHlvdXIgY2hhbmdlc1wiXG4gICAgLz5cbiAgICA8ZWwtdG91ci1zdGVwXG4gICAgICA6dGFyZ2V0PVwicmVmMz8uJGVsXCJcbiAgICAgIHRpdGxlPVwiT3RoZXIgQWN0aW9uc1wiXG4gICAgICBkZXNjcmlwdGlvbj1cIkNsaWNrIHRvIHNlZSBvdGhlclwiXG4gICAgLz5cbiAgICA8dGVtcGxhdGUgI2luZGljYXRvcnM9XCJ7IGN1cnJlbnQsIHRvdGFsIH1cIj5cbiAgICAgIDxzcGFuPnt7IGN1cnJlbnQgKyAxIH19IC8ge3sgdG90YWwgfX08L3NwYW4+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC10b3VyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IE1vcmVGaWxsZWQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuaW1wb3J0IHR5cGUgeyBCdXR0b25JbnN0YW5jZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgcmVmMSA9IHJlZjxCdXR0b25JbnN0YW5jZT4oKVxuY29uc3QgcmVmMiA9IHJlZjxCdXR0b25JbnN0YW5jZT4oKVxuY29uc3QgcmVmMyA9IHJlZjxCdXR0b25JbnN0YW5jZT4oKVxuXG5jb25zdCBvcGVuID0gcmVmKGZhbHNlKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tour/indicator.vue)_

vue

```
<template>
  <el-button type="primary" @click="open = true">Begin Tour</el-button>

  <el-divider />

  <el-space>
    <el-button ref="ref1">Upload</el-button>
    <el-button ref="ref2" type="primary">Save</el-button>
    <el-button ref="ref3" :icon="MoreFilled" />
  </el-space>

  <el-tour v-model="open">
    <el-tour-step
      :target="ref1?.$el"
      title="Upload File"
      description="Put you files here."
    />
    <el-tour-step
      :target="ref2?.$el"
      title="Save"
      description="Save your changes"
    />
    <el-tour-step
      :target="ref3?.$el"
      title="Other Actions"
      description="Click to see other"
    />
    <template #indicators="{ current, total }">
      <span>{{ current + 1 }} / {{ total }}</span>
    </template>
  </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MoreFilled } from '@element-plus/icons-vue'

import type { ButtonInstance } from 'element-plus'

const ref1 = ref<ButtonInstance>()
const ref2 = ref<ButtonInstance>()
const ref3 = ref<ButtonInstance>()

const open = ref(false)
</script>
```

隐藏源代码

## 目标 [​](#目标)

可以传入目标的各种类型的参数。 自2.5.2以来支持字符串和函数类型。

Begin Tour

Upload

Save

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwib3BlbiA9IHRydWVcIj5CZWdpbiBUb3VyPC9lbC1idXR0b24+XG5cbiAgPGVsLWRpdmlkZXIgLz5cblxuICA8ZWwtc3BhY2U+XG4gICAgPGVsLWJ1dHRvbiBpZD1cImJ0bjFcIj5VcGxvYWQ8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGlkPVwiYnRuMlwiIHR5cGU9XCJwcmltYXJ5XCI+U2F2ZTwvZWwtYnV0dG9uPlxuICAgIDxlbC1idXR0b24gcmVmPVwiYnRuUmVmXCIgOmljb249XCJNb3JlRmlsbGVkXCIgLz5cbiAgPC9lbC1zcGFjZT5cblxuICA8ZWwtdG91ciB2LW1vZGVsPVwib3BlblwiPlxuICAgIDxlbC10b3VyLXN0ZXBcbiAgICAgIHRhcmdldD1cIiNidG4xXCJcbiAgICAgIHRpdGxlPVwiVXBsb2FkIEZpbGVcIlxuICAgICAgZGVzY3JpcHRpb249XCJQdXQgeW91IGZpbGVzIGhlcmUuXCJcbiAgICAvPlxuICAgIDxlbC10b3VyLXN0ZXAgOnRhcmdldD1cImVsXCIgdGl0bGU9XCJTYXZlXCIgZGVzY3JpcHRpb249XCJTYXZlIHlvdXIgY2hhbmdlc1wiIC8+XG4gICAgPGVsLXRvdXItc3RlcFxuICAgICAgOnRhcmdldD1cImJ0blJlZj8uJGVsXCJcbiAgICAgIHRpdGxlPVwiT3RoZXIgQWN0aW9uc1wiXG4gICAgICBkZXNjcmlwdGlvbj1cIkNsaWNrIHRvIHNlZSBvdGhlclwiXG4gICAgLz5cbiAgPC9lbC10b3VyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IE1vcmVGaWxsZWQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuaW1wb3J0IHR5cGUgeyBCdXR0b25JbnN0YW5jZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgZWwgPSAoKSA9PiBkb2N1bWVudC5xdWVyeVNlbGVjdG9yPEhUTUxFbGVtZW50PignI2J0bjInKVxuY29uc3QgYnRuUmVmID0gcmVmPEJ1dHRvbkluc3RhbmNlPigpXG5cbmNvbnN0IG9wZW4gPSByZWYoZmFsc2UpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/tour/target.vue)_

vue

```
<template>
  <el-button type="primary" @click="open = true">Begin Tour</el-button>

  <el-divider />

  <el-space>
    <el-button id="btn1">Upload</el-button>
    <el-button id="btn2" type="primary">Save</el-button>
    <el-button ref="btnRef" :icon="MoreFilled" />
  </el-space>

  <el-tour v-model="open">
    <el-tour-step
      target="#btn1"
      title="Upload File"
      description="Put you files here."
    />
    <el-tour-step :target="el" title="Save" description="Save your changes" />
    <el-tour-step
      :target="btnRef?.$el"
      title="Other Actions"
      description="Click to see other"
    />
  </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MoreFilled } from '@element-plus/icons-vue'

import type { ButtonInstance } from 'element-plus'

const el = () => document.querySelector<HTMLElement>('#btn2')
const btnRef = ref<ButtonInstance>()

const open = ref(false)
</script>
```

隐藏源代码

## Tour API [​](#tour-api)

TIP

tour-step 组件上相同名称配置的优先级更高。

### Tour Attributes [​](#tour-attributes)

| 属性 | 描述 | 类型 | 默认值 |
| --- | --- | --- | --- |
| append-to | 挂载到哪个 DOM 元素 | `CSSSelector` / `HTMLElement` | `body` |
| show-arrow | 是否显示箭头 | `boolean` | true |
| placement | 引导卡片相对于目标元素的位置 | `enum` | `bottom` |
| content-style | 为content自定义样式 | `CSSProperties` | — |
| mask | 是否启用遮罩，通过自定义属性改变遮罩样式以及填充的颜色 | `boolean` | `Object` | `true` |
| gap | 遮罩和目标之间的透明的间距 | `TourGap` | `Object` |
| type | 类型，影响底色与文字颜色 | `default` | `primary` | `default` |
| model-value / v-model | 打开引导 | `boolean` | `false` |
| current / v-model:current | 当前值 | `number` | `0` |
| scroll-into-view-options | 是否支持当前元素滚动到视窗内，也可传入配置指定滚动视窗的相关参数 | `boolean` | `ScrollIntoViewOptions` | `Object` |
| z-index | Tour 的层级 | `number` | `2001` |
| show-close | 是否显示关闭按钮 | `boolean` | `true` |
| close-icon | 自定义关闭图标，默认Close | `string` | `Component` | — |
| close-on-press-escape | 是否可以通过按下 ESC 关闭引导 | `boolean` | `true` |
| target-area-clickable | 启用蒙层时，target 元素区域是否可以点击。 | `boolean` | `true` |

### Tour slots [​](#tour-slots)

| 插槽名 | 说明 | 类型 |
| --- | --- | --- |
| default | tourStep 组件列表 | — |
| indicators | 自定义指示器 | `object` |

### Tour events [​](#tour-events)

| 事件名 | 描述 | 类型 |
| --- | --- | --- |
| close | 关闭引导时的回调函数 | `Function` |
| finish | 引导完成时的回调 | `Function` |
| change | 步骤改变时的回调 | `Function` |

## TourStep API [​](#tourstep-api)

### TourStep Attributes [​](#tourstep-attributes)

| 属性 | 描述 | 事件参数 | 默认值 |
| --- | --- | --- | --- |
| target | 获取引导卡片指向的元素， 为空时居中于屏幕。 自2.5.2以来支持字符串和函数类型。 字符串类型是文档.querySelector的选择器。 | `HTMLElement` | `string` | `Function` | — |
| show-arrow | 是否显示箭头 | `boolean` | — |
| title | title | `string` | — |
| description | description | `string` | — |
| placement | 引导卡片相对于目标元素的位置 | `enum` | `bottom` |
| content-style | 为content自定义样式 | `CSSProperties` | — |
| mask | 是否启用蒙层，也可传入配置改变蒙层样式和填充色 | `boolean` | `Object` | — |
| type | 类型，影响底色与文字颜色 | `default` | `primary` | `default` |
| next-button-props | “下一步”按钮的属性 | `Object` | — |
| prev-button-props | “上一步”按钮的属性 | `Object` | — |
| scroll-into-view-options | 是否支持当前元素滚动到视窗内，也可传入配置指定滚动视窗的相关参数，默认跟随 Tour 的 `scrollIntoViewOptions` 属性 | `boolean` | `ScrollIntoViewOptions` | — |
| show-close | 是否显示关闭按钮 | `boolean` | — |
| close-icon | 自定义关闭图标，默认Close | `string` | `Component` | — |

### TourStep slots [​](#tourstep-slots)

| 插槽名 | 描述 |
| --- | --- |
| default | 自定义描述 |
| header | 自定义 header 内容 |

### TourStep events [​](#tourstep-events)

| 事件名 | 描述 | 参数 |
| --- | --- | --- |
| close | 关闭引导时的回调函数 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/tour) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/tour.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/tour.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/27912232?v=4&size=64)](https://github.com/Fuphoenixes)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/35091020?v=4&size=64)](https://github.com/zzh948498)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)

[Timeline 时间线](https://element-plus.org/zh-CN/component/timeline)

[Tree 树形控件](https://element-plus.org/zh-CN/component/tree)


