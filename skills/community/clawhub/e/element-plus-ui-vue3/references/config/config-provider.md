---
name: "config-provider"
description: "Config Provider 全局配置 -- Element Plus Vue3 桌面端组件。Invoke when user needs Config Provider 全局配置 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/config-provider.html"
---

# Config Provider 全局配置 [​](#config-provider-全局配置)

Config Provider 被用来提供全局的配置选项，让你的配置能够在全局都能够被访问到。

## i18n 配置 [​](#i18n-配置)

通过 Config Provider 来配置多语言，让你的应用可以随时切换语言。

使用两个属性来提供 i18n 相关配置

暂无数据

-   1
-   2
-   3
-   4
-   5
-   6

-   10

前往

页

共 100 条

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1idXR0b24gbWItMiBAY2xpY2s9XCJ0b2dnbGVcIj5Td2l0Y2ggTGFuZ3VhZ2U8L2VsLWJ1dHRvbj5cbiAgICA8YnIgLz5cblxuICAgIDxlbC1jb25maWctcHJvdmlkZXIgOmxvY2FsZT1cImxvY2FsZVwiPlxuICAgICAgPGVsLXRhYmxlIG1iLTEgOmRhdGE9XCJbXVwiIC8+XG4gICAgICA8ZWwtcGFnaW5hdGlvbiA6dG90YWw9XCIxMDBcIiAvPlxuICAgIDwvZWwtY29uZmlnLXByb3ZpZGVyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBjb21wdXRlZCwgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHpoQ24gZnJvbSAnZWxlbWVudC1wbHVzL2VzL2xvY2FsZS9sYW5nL3poLWNuJ1xuaW1wb3J0IGVuIGZyb20gJ2VsZW1lbnQtcGx1cy9lcy9sb2NhbGUvbGFuZy9lbidcblxuY29uc3QgbGFuZ3VhZ2UgPSByZWYoJ3poLWNuJylcbmNvbnN0IGxvY2FsZSA9IGNvbXB1dGVkKCgpID0+IChsYW5ndWFnZS52YWx1ZSA9PT0gJ3poLWNuJyA/IHpoQ24gOiBlbikpXG5cbmNvbnN0IHRvZ2dsZSA9ICgpID0+IHtcbiAgbGFuZ3VhZ2UudmFsdWUgPSBsYW5ndWFnZS52YWx1ZSA9PT0gJ3poLWNuJyA/ICdlbicgOiAnemgtY24nXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/config-provider/usage.vue)_

vue

```
<template>
  <div>
    <el-button mb-2 @click="toggle">Switch Language</el-button>
    <br />

    <el-config-provider :locale="locale">
      <el-table mb-1 :data="[]" />
      <el-pagination :total="100" />
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'

const language = ref('zh-cn')
const locale = computed(() => (language.value === 'zh-cn' ? zhCn : en))

const toggle = () => {
  language.value = language.value === 'zh-cn' ? 'en' : 'zh-cn'
}
</script>
```

隐藏源代码

## 对按钮进行配置 [​](#对按钮进行配置)

autoInsertSpace plain round dashed text

default

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxkaXY+XG4gICAgICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNvbmZpZy5hdXRvSW5zZXJ0U3BhY2VcIj5cbiAgICAgICAgYXV0b0luc2VydFNwYWNlXG4gICAgICA8L2VsLWNoZWNrYm94PlxuICAgICAgPGVsLWNoZWNrYm94IHYtbW9kZWw9XCJjb25maWcucGxhaW5cIj4gcGxhaW4gPC9lbC1jaGVja2JveD5cbiAgICAgIDxlbC1jaGVja2JveCB2LW1vZGVsPVwiY29uZmlnLnJvdW5kXCI+IHJvdW5kIDwvZWwtY2hlY2tib3g+XG4gICAgICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNvbmZpZy5kYXNoZWRcIj4gZGFzaGVkIDwvZWwtY2hlY2tib3g+XG4gICAgICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNvbmZpZy50ZXh0XCI+IHRleHQgPC9lbC1jaGVja2JveD5cbiAgICAgIDxlbC1zZWxlY3Qgdi1tb2RlbD1cImNvbmZpZy50eXBlXCIgY2xhc3M9XCJtbC01XCIgc3R5bGU9XCJtYXgtd2lkdGg6IDE1MHB4XCI+XG4gICAgICAgIDxlbC1vcHRpb25cbiAgICAgICAgICB2LWZvcj1cInR5cGUgaW4gYnV0dG9uVHlwZXMuZmlsdGVyKEJvb2xlYW4pXCJcbiAgICAgICAgICA6a2V5PVwidHlwZVwiXG4gICAgICAgICAgOnZhbHVlPVwidHlwZVwiXG4gICAgICAgIC8+XG4gICAgICA8L2VsLXNlbGVjdD5cbiAgICA8L2Rpdj5cbiAgICA8ZWwtZGl2aWRlciAvPlxuICAgIDxlbC1jb25maWctcHJvdmlkZXIgOmJ1dHRvbj1cImNvbmZpZ1wiPlxuICAgICAgPGVsLWJ1dHRvbj7kuK3mloc8L2VsLWJ1dHRvbj5cbiAgICA8L2VsLWNvbmZpZy1wcm92aWRlcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVhY3RpdmUgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBidXR0b25UeXBlcyB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW1wb3J0IHR5cGUgeyBCdXR0b25Db25maWdDb250ZXh0IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBjb25maWcgPSByZWFjdGl2ZTxCdXR0b25Db25maWdDb250ZXh0Pih7XG4gIGF1dG9JbnNlcnRTcGFjZTogdHJ1ZSxcbiAgdHlwZTogJ2RlZmF1bHQnLFxuICBwbGFpbjogdHJ1ZSxcbiAgcm91bmQ6IHRydWUsXG4gIHRleHQ6IGZhbHNlLFxuICBkYXNoZWQ6IGZhbHNlLFxufSlcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/config-provider/button.vue)_

vue

```
<template>
  <div>
    <div>
      <el-checkbox v-model="config.autoInsertSpace">
        autoInsertSpace
      </el-checkbox>
      <el-checkbox v-model="config.plain"> plain </el-checkbox>
      <el-checkbox v-model="config.round"> round </el-checkbox>
      <el-checkbox v-model="config.dashed"> dashed </el-checkbox>
      <el-checkbox v-model="config.text"> text </el-checkbox>
      <el-select v-model="config.type" class="ml-5" style="max-width: 150px">
        <el-option
          v-for="type in buttonTypes.filter(Boolean)"
          :key="type"
          :value="type"
        />
      </el-select>
    </div>
    <el-divider />
    <el-config-provider :button="config">
      <el-button>中文</el-button>
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { buttonTypes } from 'element-plus'

import type { ButtonConfigContext } from 'element-plus'

const config = reactive<ButtonConfigContext>({
  autoInsertSpace: true,
  type: 'default',
  plain: true,
  round: true,
  text: false,
  dashed: false,
})
</script>
```

隐藏源代码

## 对链接进行配置2.9.11 [​](#对链接进行配置)

Type:

success

Underline:

always

Link desu!

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJmbGV4IGdhcC00XCI+XG4gICAgICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LWNvbCBiYXNpcy0xNTBweCBnYXAtMVwiPlxuICAgICAgICA8c3Bhbj5UeXBlOjwvc3Bhbj5cbiAgICAgICAgPGVsLXNlbGVjdCB2LW1vZGVsPVwiY29uZmlnLnR5cGVcIj5cbiAgICAgICAgICA8ZWwtb3B0aW9uIHYtZm9yPVwidHlwZSBpbiBsaW5rVHlwZXNcIiA6a2V5PVwidHlwZVwiIDp2YWx1ZT1cInR5cGVcIiAvPlxuICAgICAgICA8L2VsLXNlbGVjdD5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzcz1cImZsZXggZmxleC1jb2wgYmFzaXMtMTUwcHggZ2FwLTFcIj5cbiAgICAgICAgPHNwYW4+VW5kZXJsaW5lOjwvc3Bhbj5cbiAgICAgICAgPGVsLXNlbGVjdCB2LW1vZGVsPVwiY29uZmlnLnVuZGVybGluZVwiPlxuICAgICAgICAgIDxlbC1vcHRpb25cbiAgICAgICAgICAgIHYtZm9yPVwidHlwZSBpbiB1bmRlcmxpbmVPcHRpb25zXCJcbiAgICAgICAgICAgIDprZXk9XCJ0eXBlXCJcbiAgICAgICAgICAgIDp2YWx1ZT1cInR5cGVcIlxuICAgICAgICAgIC8+XG4gICAgICAgIDwvZWwtc2VsZWN0PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+XG4gICAgPGVsLWRpdmlkZXIgLz5cbiAgICA8ZWwtY29uZmlnLXByb3ZpZGVyIDpsaW5rPVwiY29uZmlnXCI+XG4gICAgICA8ZWwtbGluaz5MaW5rIGRlc3UhPC9lbC1saW5rPlxuICAgIDwvZWwtY29uZmlnLXByb3ZpZGVyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWFjdGl2ZSB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBMaW5rQ29uZmlnQ29udGV4dCB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgbGlua1R5cGVzID0gWydwcmltYXJ5JywgJ3N1Y2Nlc3MnLCAnd2FybmluZycsICdpbmZvJywgJ2RhbmdlcicsICdkZWZhdWx0J11cbmNvbnN0IHVuZGVybGluZU9wdGlvbnMgPSBbJ2Fsd2F5cycsICduZXZlcicsICdob3ZlciddXG5cbmNvbnN0IGNvbmZpZyA9IHJlYWN0aXZlPExpbmtDb25maWdDb250ZXh0Pih7XG4gIHR5cGU6ICdzdWNjZXNzJyxcbiAgdW5kZXJsaW5lOiAnYWx3YXlzJyxcbn0pXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/config-provider/link.vue)_

vue

```
<template>
  <div>
    <div class="flex gap-4">
      <div class="flex flex-col basis-150px gap-1">
        <span>Type:</span>
        <el-select v-model="config.type">
          <el-option v-for="type in linkTypes" :key="type" :value="type" />
        </el-select>
      </div>
      <div class="flex flex-col basis-150px gap-1">
        <span>Underline:</span>
        <el-select v-model="config.underline">
          <el-option
            v-for="type in underlineOptions"
            :key="type"
            :value="type"
          />
        </el-select>
      </div>
    </div>
    <el-divider />
    <el-config-provider :link="config">
      <el-link>Link desu!</el-link>
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

import type { LinkConfigContext } from 'element-plus'

const linkTypes = ['primary', 'success', 'warning', 'info', 'danger', 'default']
const underlineOptions = ['always', 'never', 'hover']

const config = reactive<LinkConfigContext>({
  type: 'success',
  underline: 'always',
})
</script>
```

隐藏源代码

## 对 Card 进行配置 2.10.5 [​](#对-card-进行配置)

Shadow:

alwayshovernever

Card desu!

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlYWN0aXZlIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IENhcmRDb25maWdDb250ZXh0IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBjb25maWcgPSByZWFjdGl2ZTxDYXJkQ29uZmlnQ29udGV4dD4oe1xuICBzaGFkb3c6ICdhbHdheXMnLFxufSlcbjwvc2NyaXB0PlxuXG48dGVtcGxhdGU+XG4gIFNoYWRvdzpcbiAgPGRpdiBjbGFzcz1cImZsZXggZmxleC1jb2wganVzdGlmeS1jZW50ZXJcIj5cbiAgICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cImNvbmZpZy5zaGFkb3dcIj5cbiAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cImFsd2F5c1wiPmFsd2F5czwvZWwtcmFkaW8+XG4gICAgICA8ZWwtcmFkaW8gdmFsdWU9XCJob3ZlclwiPmhvdmVyPC9lbC1yYWRpbz5cbiAgICAgIDxlbC1yYWRpbyB2YWx1ZT1cIm5ldmVyXCI+bmV2ZXI8L2VsLXJhZGlvPlxuICAgIDwvZWwtcmFkaW8tZ3JvdXA+XG4gICAgPGVsLWRpdmlkZXIgLz5cbiAgICA8ZWwtY29uZmlnLXByb3ZpZGVyIDpjYXJkPVwiY29uZmlnXCI+XG4gICAgICA8ZWwtY2FyZD5DYXJkIGRlc3UhPC9lbC1jYXJkPlxuICAgIDwvZWwtY29uZmlnLXByb3ZpZGVyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/config-provider/card.vue)_

vue

```
<script lang="ts" setup>
import { reactive } from 'vue'

import type { CardConfigContext } from 'element-plus'

const config = reactive<CardConfigContext>({
  shadow: 'always',
})
</script>

<template>
  Shadow:
  <div class="flex flex-col justify-center">
    <el-radio-group v-model="config.shadow">
      <el-radio value="always">always</el-radio>
      <el-radio value="hover">hover</el-radio>
      <el-radio value="never">never</el-radio>
    </el-radio-group>
    <el-divider />
    <el-config-provider :card="config">
      <el-card>Card desu!</el-card>
    </el-config-provider>
  </div>
</template>
```

隐藏源代码

## 对 Dialog 进行配置 2.10.7 [​](#对-dialog-进行配置)

transition: string

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGNvbXB1dGVkLCBuZXh0VGljaywgcmVmLCBzaGFsbG93UmVhY3RpdmUgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgQnV0dG9uSW5zdGFuY2UsIERpYWxvZ1RyYW5zaXRpb24gfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbnR5cGUgR2xvYmFsQ29uZmlnID0ge1xuICBhbGlnbkNlbnRlcjogYm9vbGVhblxuICBkcmFnZ2FibGU6IGJvb2xlYW5cbiAgb3ZlcmZsb3c6IGJvb2xlYW5cbiAgdHJhbnNpdGlvbj86IERpYWxvZ1RyYW5zaXRpb25cbn1cblxuY29uc3QgY29uZmlnID0gc2hhbGxvd1JlYWN0aXZlPEdsb2JhbENvbmZpZz4oe1xuICBhbGlnbkNlbnRlcjogZmFsc2UsXG4gIGRyYWdnYWJsZTogZmFsc2UsXG4gIG92ZXJmbG93OiBmYWxzZSxcbn0pXG5jb25zdCB2aXNpYmxlID0gcmVmKGZhbHNlKVxuY29uc3QgZW5hYmxlVHJhbnNpdGlvbiA9IHJlZihmYWxzZSlcbmNvbnN0IGlzT2JqZWN0VHJhbnNpdGlvbiA9IHJlZihmYWxzZSlcblxuY29uc3QgYnV0dG9uUmVmID0gcmVmPEJ1dHRvbkluc3RhbmNlPigpXG5cbmNvbnN0IEFOSU1BVElPTl9EVVJBVElPTiA9IDMwMFxuXG5jb25zdCBnbG9iYWxDb25maWcgPSBjb21wdXRlZDxHbG9iYWxDb25maWc+KCgpID0+IHtcbiAgbGV0IHRyYW5zaXRpb246IERpYWxvZ1RyYW5zaXRpb24gfCB1bmRlZmluZWRcbiAgaWYgKGVuYWJsZVRyYW5zaXRpb24udmFsdWUpIHtcbiAgICBpZiAoaXNPYmplY3RUcmFuc2l0aW9uLnZhbHVlKSB7XG4gICAgICB0cmFuc2l0aW9uID0ge1xuICAgICAgICBjc3M6IGZhbHNlLFxuICAgICAgICBvbkJlZm9yZUVudGVyKGVsKSB7XG4gICAgICAgICAgbmV4dFRpY2soKCkgPT4ge1xuICAgICAgICAgICAgaWYgKGJ1dHRvblJlZi52YWx1ZSkge1xuICAgICAgICAgICAgICBjb25zdCBidXR0b25SZWN0ID0gYnV0dG9uUmVmLnZhbHVlLnJlZiEuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KClcbiAgICAgICAgICAgICAgY29uc3QgZGlhbG9nRWwgPSBlbC5xdWVyeVNlbGVjdG9yKCcuZWwtZGlhbG9nJykgYXMgSFRNTEVsZW1lbnRcblxuICAgICAgICAgICAgICBpZiAoZGlhbG9nRWwpIHtcbiAgICAgICAgICAgICAgICBjb25zdCBkaWFsb2dSZWN0ID0gZGlhbG9nRWwuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KClcblxuICAgICAgICAgICAgICAgIGNvbnN0IG9mZnNldFggPVxuICAgICAgICAgICAgICAgICAgYnV0dG9uUmVjdC5sZWZ0ICtcbiAgICAgICAgICAgICAgICAgIGJ1dHRvblJlY3Qud2lkdGggLyAyIC1cbiAgICAgICAgICAgICAgICAgIChkaWFsb2dSZWN0LmxlZnQgKyBkaWFsb2dSZWN0LndpZHRoIC8gMilcbiAgICAgICAgICAgICAgICBjb25zdCBvZmZzZXRZID1cbiAgICAgICAgICAgICAgICAgIGJ1dHRvblJlY3QudG9wICtcbiAgICAgICAgICAgICAgICAgIGJ1dHRvblJlY3QuaGVpZ2h0IC8gMiAtXG4gICAgICAgICAgICAgICAgICAoZGlhbG9nUmVjdC50b3AgKyBkaWFsb2dSZWN0LmhlaWdodCAvIDIpXG5cbiAgICAgICAgICAgICAgICBkaWFsb2dFbC5zdHlsZS50cmFuc2Zvcm0gPSBgdHJhbnNsYXRlKCR7b2Zmc2V0WH1weCwgJHtvZmZzZXRZfXB4KSBzY2FsZSgwLjMpYFxuICAgICAgICAgICAgICAgIGRpYWxvZ0VsLnN0eWxlLm9wYWNpdHkgPSAnMCdcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH0pXG4gICAgICAgIH0sXG4gICAgICAgIG9uRW50ZXIoZWwsIGRvbmUpIHtcbiAgICAgICAgICBuZXh0VGljaygoKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBkaWFsb2dFbCA9IGVsLnF1ZXJ5U2VsZWN0b3IoJy5lbC1kaWFsb2cnKSBhcyBIVE1MRWxlbWVudFxuICAgICAgICAgICAgaWYgKGRpYWxvZ0VsKSB7XG4gICAgICAgICAgICAgIC8vIGZvcmNlIHJlZmxvd1xuICAgICAgICAgICAgICBkaWFsb2dFbC5vZmZzZXRIZWlnaHRcblxuICAgICAgICAgICAgICBkaWFsb2dFbC5zdHlsZS50cmFuc2l0aW9uID0gYGFsbCAke0FOSU1BVElPTl9EVVJBVElPTn1tcyBjdWJpYy1iZXppZXIoMC40LCAwLCAxLCAxKWBcbiAgICAgICAgICAgICAgZGlhbG9nRWwuc3R5bGUudHJhbnNmb3JtID0gJ3RyYW5zbGF0ZSgwLCAwKSBzY2FsZSgxKSdcbiAgICAgICAgICAgICAgZGlhbG9nRWwuc3R5bGUub3BhY2l0eSA9ICcxJ1xuXG4gICAgICAgICAgICAgIC8vIHdhaXQgZm9yIGFuaW1hdGlvbiB0byBjb21wbGV0ZSwgdGhlbiBjbGVhbnVwIGlubGluZSBzdHlsZXMgdG8gYXZvaWQgYWZmZWN0aW5nIGRyYWdcbiAgICAgICAgICAgICAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICAgICAgICAgICAgZGlhbG9nRWwuc3R5bGUudHJhbnNpdGlvbiA9ICcnXG4gICAgICAgICAgICAgICAgZGlhbG9nRWwuc3R5bGUudHJhbnNmb3JtID0gJydcbiAgICAgICAgICAgICAgICBkaWFsb2dFbC5zdHlsZS5vcGFjaXR5ID0gJydcbiAgICAgICAgICAgICAgICBkb25lKClcbiAgICAgICAgICAgICAgfSwgQU5JTUFUSU9OX0RVUkFUSU9OKVxuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgZG9uZSgpXG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSlcbiAgICAgICAgfSxcbiAgICAgICAgb25MZWF2ZShlbCwgZG9uZSkge1xuICAgICAgICAgIGNvbnN0IGRpYWxvZ0VsID0gZWwucXVlcnlTZWxlY3RvcignLmVsLWRpYWxvZycpIGFzIEhUTUxFbGVtZW50XG4gICAgICAgICAgaWYgKGRpYWxvZ0VsKSB7XG4gICAgICAgICAgICBpZiAoYnV0dG9uUmVmLnZhbHVlKSB7XG4gICAgICAgICAgICAgIGNvbnN0IGJ1dHRvblJlY3QgPSBidXR0b25SZWYudmFsdWUucmVmIS5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKVxuICAgICAgICAgICAgICBjb25zdCBkaWFsb2dSZWN0ID0gZGlhbG9nRWwuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KClcblxuICAgICAgICAgICAgICBjb25zdCBjdXJyZW50VHJhbnNmb3JtID0gZGlhbG9nRWwuc3R5bGUudHJhbnNmb3JtXG4gICAgICAgICAgICAgIGxldCBkcmFnT2Zmc2V0WCA9IDBcbiAgICAgICAgICAgICAgbGV0IGRyYWdPZmZzZXRZID0gMFxuXG4gICAgICAgICAgICAgIC8vIGF2b2lkIGRyYWdnYWJsZSBlZmZlY3RcbiAgICAgICAgICAgICAgaWYgKGN1cnJlbnRUcmFuc2Zvcm0pIHtcbiAgICAgICAgICAgICAgICBjb25zdCB0cmFuc2xhdGVNYXRjaCA9IGN1cnJlbnRUcmFuc2Zvcm0ubWF0Y2goXG4gICAgICAgICAgICAgICAgICAvdHJhbnNsYXRlXFwoKFteLF0rKSxcXHMqKFteKV0rKVxcKS9cbiAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgaWYgKHRyYW5zbGF0ZU1hdGNoKSB7XG4gICAgICAgICAgICAgICAgICBkcmFnT2Zmc2V0WCA9IE51bWJlci5wYXJzZUZsb2F0KHRyYW5zbGF0ZU1hdGNoWzFdKVxuICAgICAgICAgICAgICAgICAgZHJhZ09mZnNldFkgPSBOdW1iZXIucGFyc2VGbG9hdCh0cmFuc2xhdGVNYXRjaFsyXSlcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgICBjb25zdCBvZmZzZXRYID1cbiAgICAgICAgICAgICAgICBidXR0b25SZWN0LmxlZnQgK1xuICAgICAgICAgICAgICAgIGJ1dHRvblJlY3Qud2lkdGggLyAyIC1cbiAgICAgICAgICAgICAgICAoZGlhbG9nUmVjdC5sZWZ0ICsgZGlhbG9nUmVjdC53aWR0aCAvIDIpICtcbiAgICAgICAgICAgICAgICBkcmFnT2Zmc2V0WFxuICAgICAgICAgICAgICBjb25zdCBvZmZzZXRZID1cbiAgICAgICAgICAgICAgICBidXR0b25SZWN0LnRvcCArXG4gICAgICAgICAgICAgICAgYnV0dG9uUmVjdC5oZWlnaHQgLyAyIC1cbiAgICAgICAgICAgICAgICAoZGlhbG9nUmVjdC50b3AgKyBkaWFsb2dSZWN0LmhlaWdodCAvIDIpICtcbiAgICAgICAgICAgICAgICBkcmFnT2Zmc2V0WVxuXG4gICAgICAgICAgICAgIGRpYWxvZ0VsLnN0eWxlLnRyYW5zaXRpb24gPSBgYWxsICR7QU5JTUFUSU9OX0RVUkFUSU9OfW1zIGN1YmljLWJlemllcigwLjQsIDAsIDEsIDEpYFxuICAgICAgICAgICAgICBkaWFsb2dFbC5zdHlsZS50cmFuc2Zvcm0gPSBgdHJhbnNsYXRlKCR7b2Zmc2V0WH1weCwgJHtvZmZzZXRZfXB4KSBzY2FsZSgwLjMpYFxuICAgICAgICAgICAgICBkaWFsb2dFbC5zdHlsZS5vcGFjaXR5ID0gJzAnXG5cbiAgICAgICAgICAgICAgLy8gd2FpdCBmb3IgYW5pbWF0aW9uIHRvIGNvbXBsZXRlLCB0aGVuIGNsZWFudXAgaW5saW5lIHN0eWxlc1xuICAgICAgICAgICAgICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgICAgICAgICBkaWFsb2dFbC5zdHlsZS50cmFuc2l0aW9uID0gJydcbiAgICAgICAgICAgICAgICBkaWFsb2dFbC5zdHlsZS50cmFuc2Zvcm0gPSAnJ1xuICAgICAgICAgICAgICAgIGRpYWxvZ0VsLnN0eWxlLm9wYWNpdHkgPSAnJ1xuICAgICAgICAgICAgICAgIGRvbmUoKVxuICAgICAgICAgICAgICB9LCBBTklNQVRJT05fRFVSQVRJT04pXG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICBkb25lKClcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgZG9uZSgpXG4gICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICB0cmFuc2l0aW9uID0gJ2RpYWxvZy1ib3VuY2UnXG4gICAgfVxuICB9XG4gIHJldHVybiB7XG4gICAgYWxpZ25DZW50ZXI6IGNvbmZpZy5hbGlnbkNlbnRlcixcbiAgICBkcmFnZ2FibGU6IGNvbmZpZy5kcmFnZ2FibGUsXG4gICAgb3ZlcmZsb3c6IGNvbmZpZy5vdmVyZmxvdyxcbiAgICB0cmFuc2l0aW9uLFxuICB9XG59KVxuPC9zY3JpcHQ+XG5cbjx0ZW1wbGF0ZT5cbiAgPGRpdiBjbGFzcz1cImZsZXggZmxleC1jb2wgZ2FwLTQganVzdGlmeS1jZW50ZXJcIj5cbiAgICA8ZGl2IGNsYXNzPVwiZmxleCBpdGVtcy1jZW50ZXIgZ2FwLTJcIj5cbiAgICAgIDxlbC1zd2l0Y2ggdi1tb2RlbD1cImNvbmZpZy5hbGlnbkNlbnRlclwiIGFjdGl2ZS10ZXh0PVwiYWxpZ25DZW50ZXJcIiAvPlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJmbGV4IGl0ZW1zLWNlbnRlciBnYXAtNFwiPlxuICAgICAgPGVsLXN3aXRjaCB2LW1vZGVsPVwiY29uZmlnLmRyYWdnYWJsZVwiIGFjdGl2ZS10ZXh0PVwiZHJhZ2dhYmxlXCIgLz5cbiAgICAgIDxlbC1zd2l0Y2hcbiAgICAgICAgdi1tb2RlbD1cImNvbmZpZy5vdmVyZmxvd1wiXG4gICAgICAgIDpkaXNhYmxlZD1cIiFjb25maWcuZHJhZ2dhYmxlXCJcbiAgICAgICAgYWN0aXZlLXRleHQ9XCJvdmVyZmxvd1wiXG4gICAgICAvPlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJmbGV4IGl0ZW1zLWNlbnRlciBnYXAtMlwiPlxuICAgICAgPGVsLXN3aXRjaCB2LW1vZGVsPVwiZW5hYmxlVHJhbnNpdGlvblwiIGFjdGl2ZS10ZXh0PVwiZW5hYmxlIHRyYW5zaXRpb25cIiAvPlxuICAgICAgPGVsLXN3aXRjaFxuICAgICAgICB2LW1vZGVsPVwiaXNPYmplY3RUcmFuc2l0aW9uXCJcbiAgICAgICAgOmRpc2FibGVkPVwiIWVuYWJsZVRyYW5zaXRpb25cIlxuICAgICAgICBhY3RpdmUtdGV4dD1cInRyYW5zaXRpb246IG9iamVjdFwiXG4gICAgICAgIGluYWN0aXZlLXRleHQ9XCJ0cmFuc2l0aW9uOiBzdHJpbmdcIlxuICAgICAgLz5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2IGNsYXNzPVwiZmxleCBpdGVtcy1jZW50ZXIgZ2FwLTJcIj5cbiAgICAgIDxlbC1idXR0b25cbiAgICAgICAgcmVmPVwiYnV0dG9uUmVmXCJcbiAgICAgICAgdHlwZT1cInByaW1hcnlcIlxuICAgICAgICBzaXplPVwic21hbGxcIlxuICAgICAgICBAY2xpY2s9XCJ2aXNpYmxlID0gdHJ1ZVwiXG4gICAgICA+XG4gICAgICAgIE9wZW4gRGlhbG9nXG4gICAgICA8L2VsLWJ1dHRvbj5cbiAgICA8L2Rpdj5cbiAgICA8ZWwtY29uZmlnLXByb3ZpZGVyIDpkaWFsb2c9XCJnbG9iYWxDb25maWdcIj5cbiAgICAgIDxlbC1kaWFsb2cgdi1tb2RlbD1cInZpc2libGVcIiB0aXRsZT1cIkRpYWxvZyBUaXRsZVwiIGRlc3Ryb3ktb24tY2xvc2U+XG4gICAgICAgIERpYWxvZyBDb250ZW50XG4gICAgICA8L2VsLWRpYWxvZz5cbiAgICA8L2VsLWNvbmZpZy1wcm92aWRlcj5cbiAgICA8ZGl2IHYtaWY9XCJlbmFibGVUcmFuc2l0aW9uXCIgY2xhc3M9XCJ0ZXh0LXhzIG9wYWNpdHktNzBcIj5cbiAgICAgIDxkaXYgdi1pZj1cImlzT2JqZWN0VHJhbnNpdGlvblwiPlxuICAgICAgICBVc2luZyBKYXZhU2NyaXB0IGNvbnRyb2xsZWQgYW5pbWF0aW9uOlxuICAgICAgICA8Y29kZT57eyBKU09OLnN0cmluZ2lmeShnbG9iYWxDb25maWcudHJhbnNpdGlvbikgfX08L2NvZGU+XG4gICAgICA8L2Rpdj5cbiAgICAgIDxkaXYgdi1lbHNlPlxuICAgICAgICBVc2luZyBzdHJpbmcgdHJhbnNpdGlvbiBuYW1lOlxuICAgICAgICA8Y29kZT57eyBnbG9iYWxDb25maWcudHJhbnNpdGlvbiB9fTwvY29kZT5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZT5cbi8qIEJvdW5jZSBBbmltYXRpb24gKi9cbi5kaWFsb2ctYm91bmNlLWVudGVyLWFjdGl2ZSxcbi5kaWFsb2ctYm91bmNlLWxlYXZlLWFjdGl2ZSxcbi5kaWFsb2ctYm91bmNlLWVudGVyLWFjdGl2ZSAuZWwtZGlhbG9nLFxuLmRpYWxvZy1ib3VuY2UtbGVhdmUtYWN0aXZlIC5lbC1kaWFsb2cge1xuICB0cmFuc2l0aW9uOiBhbGwgMC41cyBjdWJpYy1iZXppZXIoMC4xNzUsIDAuODg1LCAwLjMyLCAxLjI3NSk7XG59XG5cbi5kaWFsb2ctYm91bmNlLWVudGVyLWZyb20sXG4uZGlhbG9nLWJvdW5jZS1sZWF2ZS10byB7XG4gIG9wYWNpdHk6IDA7XG59XG5cbi5kaWFsb2ctYm91bmNlLWVudGVyLWZyb20gLmVsLWRpYWxvZyxcbi5kaWFsb2ctYm91bmNlLWxlYXZlLXRvIC5lbC1kaWFsb2cge1xuICB0cmFuc2Zvcm06IHNjYWxlKDAuMykgdHJhbnNsYXRlWSgtNTBweCk7XG4gIG9wYWNpdHk6IDA7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/config-provider/dialog.vue)_

vue

```
<script lang="ts" setup>
import { computed, nextTick, ref, shallowReactive } from 'vue'

import type { ButtonInstance, DialogTransition } from 'element-plus'

type GlobalConfig = {
  alignCenter: boolean
  draggable: boolean
  overflow: boolean
  transition?: DialogTransition
}

const config = shallowReactive<GlobalConfig>({
  alignCenter: false,
  draggable: false,
  overflow: false,
})
const visible = ref(false)
const enableTransition = ref(false)
const isObjectTransition = ref(false)

const buttonRef = ref<ButtonInstance>()

const ANIMATION_DURATION = 300

const globalConfig = computed<GlobalConfig>(() => {
  let transition: DialogTransition | undefined
  if (enableTransition.value) {
    if (isObjectTransition.value) {
      transition = {
        css: false,
        onBeforeEnter(el) {
          nextTick(() => {
            if (buttonRef.value) {
              const buttonRect = buttonRef.value.ref!.getBoundingClientRect()
              const dialogEl = el.querySelector('.el-dialog') as HTMLElement

              if (dialogEl) {
                const dialogRect = dialogEl.getBoundingClientRect()

                const offsetX =
                  buttonRect.left +
                  buttonRect.width / 2 -
                  (dialogRect.left + dialogRect.width / 2)
                const offsetY =
                  buttonRect.top +
                  buttonRect.height / 2 -
                  (dialogRect.top + dialogRect.height / 2)

                dialogEl.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(0.3)`
                dialogEl.style.opacity = '0'
              }
            }
          })
        },
        onEnter(el, done) {
          nextTick(() => {
            const dialogEl = el.querySelector('.el-dialog') as HTMLElement
            if (dialogEl) {
              // force reflow
              dialogEl.offsetHeight

              dialogEl.style.transition = `all ${ANIMATION_DURATION}ms cubic-bezier(0.4, 0, 1, 1)`
              dialogEl.style.transform = 'translate(0, 0) scale(1)'
              dialogEl.style.opacity = '1'

              // wait for animation to complete, then cleanup inline styles to avoid affecting drag
              setTimeout(() => {
                dialogEl.style.transition = ''
                dialogEl.style.transform = ''
                dialogEl.style.opacity = ''
                done()
              }, ANIMATION_DURATION)
            } else {
              done()
            }
          })
        },
        onLeave(el, done) {
          const dialogEl = el.querySelector('.el-dialog') as HTMLElement
          if (dialogEl) {
            if (buttonRef.value) {
              const buttonRect = buttonRef.value.ref!.getBoundingClientRect()
              const dialogRect = dialogEl.getBoundingClientRect()

              const currentTransform = dialogEl.style.transform
              let dragOffsetX = 0
              let dragOffsetY = 0

              // avoid draggable effect
              if (currentTransform) {
                const translateMatch = currentTransform.match(
                  /translate\(([^,]+),\s*([^)]+)\)/
                )
                if (translateMatch) {
                  dragOffsetX = Number.parseFloat(translateMatch[1])
                  dragOffsetY = Number.parseFloat(translateMatch[2])
                }
              }

              const offsetX =
                buttonRect.left +
                buttonRect.width / 2 -
                (dialogRect.left + dialogRect.width / 2) +
                dragOffsetX
              const offsetY =
                buttonRect.top +
                buttonRect.height / 2 -
                (dialogRect.top + dialogRect.height / 2) +
                dragOffsetY

              dialogEl.style.transition = `all ${ANIMATION_DURATION}ms cubic-bezier(0.4, 0, 1, 1)`
              dialogEl.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(0.3)`
              dialogEl.style.opacity = '0'

              // wait for animation to complete, then cleanup inline styles
              setTimeout(() => {
                dialogEl.style.transition = ''
                dialogEl.style.transform = ''
                dialogEl.style.opacity = ''
                done()
              }, ANIMATION_DURATION)
            } else {
              done()
            }
          } else {
            done()
          }
        },
      }
    } else {
      transition = 'dialog-bounce'
    }
  }
  return {
    alignCenter: config.alignCenter,
    draggable: config.draggable,
    overflow: config.overflow,
    transition,
  }
})
</script>

<template>
  <div class="flex flex-col gap-4 justify-center">
    <div class="flex items-center gap-2">
      <el-switch v-model="config.alignCenter" active-text="alignCenter" />
    </div>
    <div class="flex items-center gap-4">
      <el-switch v-model="config.draggable" active-text="draggable" />
      <el-switch
        v-model="config.overflow"
        :disabled="!config.draggable"
        active-text="overflow"
      />
    </div>
    <div class="flex items-center gap-2">
      <el-switch v-model="enableTransition" active-text="enable transition" />
      <el-switch
        v-model="isObjectTransition"
        :disabled="!enableTransition"
        active-text="transition: object"
        inactive-text="transition: string"
      />
    </div>
    <div class="flex items-center gap-2">
      <el-button
        ref="buttonRef"
        type="primary"
        size="small"
        @click="visible = true"
      >
        Open Dialog
      </el-button>
    </div>
    <el-config-provider :dialog="globalConfig">
      <el-dialog v-model="visible" title="Dialog Title" destroy-on-close>
        Dialog Content
      </el-dialog>
    </el-config-provider>
    <div v-if="enableTransition" class="text-xs opacity-70">
      <div v-if="isObjectTransition">
        Using JavaScript controlled animation:
        <code>{{ JSON.stringify(globalConfig.transition) }}</code>
      </div>
      <div v-else>
        Using string transition name:
        <code>{{ globalConfig.transition }}</code>
      </div>
    </div>
  </div>
</template>

<style>
/* Bounce Animation */
.dialog-bounce-enter-active,
.dialog-bounce-leave-active,
.dialog-bounce-enter-active .el-dialog,
.dialog-bounce-leave-active .el-dialog {
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.dialog-bounce-enter-from,
.dialog-bounce-leave-to {
  opacity: 0;
}

.dialog-bounce-enter-from .el-dialog,
.dialog-bounce-leave-to .el-dialog {
  transform: scale(0.3) translateY(-50px);
  opacity: 0;
}
</style>
```

隐藏源代码

## 对消息进行配置 [​](#对消息进行配置)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1jb25maWctcHJvdmlkZXIgOm1lc3NhZ2U9XCJjb25maWdcIj5cbiAgICAgIDxlbC1idXR0b24gQGNsaWNrPVwib3BlblwiPk9QRU48L2VsLWJ1dHRvbj5cbiAgICA8L2VsLWNvbmZpZy1wcm92aWRlcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVhY3RpdmUgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBFbE1lc3NhZ2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGNvbmZpZyA9IHJlYWN0aXZlKHtcbiAgbWF4OiAzLFxuICBwbGFpbjogdHJ1ZSxcbiAgcGxhY2VtZW50OiAnYm90dG9tJyxcbn0pXG5cbmNvbnN0IG9wZW4gPSAoKSA9PiB7XG4gIEVsTWVzc2FnZSgnVGhpcyBpcyBhIG1lc3NhZ2UgZnJvbSBib3R0b20uJylcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/config-provider/message.vue)_

vue

```
<template>
  <div>
    <el-config-provider :message="config">
      <el-button @click="open">OPEN</el-button>
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'

const config = reactive({
  max: 3,
  plain: true,
  placement: 'bottom',
})

const open = () => {
  ElMessage('This is a message from bottom.')
}
</script>
```

隐藏源代码

## 空值配置2.7.0 [​](#空值配置)

支持的组件

-   Cascader 级联选择器
-   ColorPicker 2.10.3
-   DatePicker 日期选择器
-   Select 选择器
-   SelectV2 选择器
-   TimePicker 时间选择器
-   TimeSelect 时间选择
-   TreeSelect 树形选择

设置 `empty-values` 来配置组件的默认空值。 默认值是 `['', null, undefined]`。 如果认为空字符串不是一个空值，可以设置成 `[undefined, null]`。

设置 `value-on-clear` 以设置清空选项的值。 组件默认值是 `undefined`。 在日期组件中是 `null`。 如果想设置成 `undefined`，请使用 `() => undefined`。

All

All

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY29uZmlnLXByb3ZpZGVyIDp2YWx1ZS1vbi1jbGVhcj1cIm51bGxcIiA6ZW1wdHktdmFsdWVzPVwiW3VuZGVmaW5lZCwgbnVsbF1cIj5cbiAgICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTQgaXRlbXMtY2VudGVyXCI+XG4gICAgICA8ZWwtc2VsZWN0XG4gICAgICAgIHYtbW9kZWw9XCJ2YWx1ZTFcIlxuICAgICAgICBjbGVhcmFibGVcbiAgICAgICAgcGxhY2Vob2xkZXI9XCJTZWxlY3RcIlxuICAgICAgICBzdHlsZT1cIndpZHRoOiAyNDBweFwiXG4gICAgICAgIEBjaGFuZ2U9XCJoYW5kbGVDaGFuZ2VcIlxuICAgICAgPlxuICAgICAgICA8ZWwtb3B0aW9uXG4gICAgICAgICAgdi1mb3I9XCJpdGVtIGluIG9wdGlvbnNcIlxuICAgICAgICAgIDprZXk9XCJpdGVtLnZhbHVlXCJcbiAgICAgICAgICA6bGFiZWw9XCJpdGVtLmxhYmVsXCJcbiAgICAgICAgICA6dmFsdWU9XCJpdGVtLnZhbHVlXCJcbiAgICAgICAgLz5cbiAgICAgIDwvZWwtc2VsZWN0PlxuICAgICAgPGVsLXNlbGVjdC12MlxuICAgICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgICAgY2xlYXJhYmxlXG4gICAgICAgIHBsYWNlaG9sZGVyPVwiU2VsZWN0XCJcbiAgICAgICAgc3R5bGU9XCJ3aWR0aDogMjQwcHhcIlxuICAgICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgICA6dmFsdWUtb24tY2xlYXI9XCIoKSA9PiB1bmRlZmluZWRcIlxuICAgICAgICBAY2hhbmdlPVwiaGFuZGxlQ2hhbmdlXCJcbiAgICAgIC8+XG4gICAgPC9kaXY+XG4gIDwvZWwtY29uZmlnLXByb3ZpZGVyPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsTWVzc2FnZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgdmFsdWUxID0gcmVmKCcnKVxuY29uc3QgdmFsdWUyID0gcmVmKCcnKVxuY29uc3Qgb3B0aW9ucyA9IFtcbiAge1xuICAgIHZhbHVlOiAnJyxcbiAgICBsYWJlbDogJ0FsbCcsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjEnLFxuICAgIGxhYmVsOiAnT3B0aW9uMScsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjInLFxuICAgIGxhYmVsOiAnT3B0aW9uMicsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjMnLFxuICAgIGxhYmVsOiAnT3B0aW9uMycsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjQnLFxuICAgIGxhYmVsOiAnT3B0aW9uNCcsXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ09wdGlvbjUnLFxuICAgIGxhYmVsOiAnT3B0aW9uNScsXG4gIH0sXG5dXG5cbmNvbnN0IGhhbmRsZUNoYW5nZSA9ICh2YWx1ZSkgPT4ge1xuICBpZiAoW3VuZGVmaW5lZCwgbnVsbF0uaW5jbHVkZXModmFsdWUpKSB7XG4gICAgRWxNZXNzYWdlLmluZm8oYFRoZSBjbGVhciB2YWx1ZSBpczogJHt2YWx1ZX1gKVxuICB9XG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/config-provider/empty-values.vue)_

vue

```
<template>
  <el-config-provider :value-on-clear="null" :empty-values="[undefined, null]">
    <div class="flex flex-wrap gap-4 items-center">
      <el-select
        v-model="value1"
        clearable
        placeholder="Select"
        style="width: 240px"
        @change="handleChange"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-select-v2
        v-model="value2"
        clearable
        placeholder="Select"
        style="width: 240px"
        :options="options"
        :value-on-clear="() => undefined"
        @change="handleChange"
      />
    </div>
  </el-config-provider>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const value1 = ref('')
const value2 = ref('')
const options = [
  {
    value: '',
    label: 'All',
  },
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]

const handleChange = (value) => {
  if ([undefined, null].includes(value)) {
    ElMessage.info(`The clear value is: ${value}`)
  }
}
</script>
```

隐藏源代码

## 表格配置 2.13.3 [​](#表格配置)

showOverflowTooltip

dark

Date

Name

Address (inherited from config-provider)

Address (explicit false)

2016-05-04

Aleyna Kutzner

Lohrbergstr. 86c, Süd Lilli, Saarland

Lohrbergstr. 86c, Süd Lilli, Saarland

2016-05-03

Helen Jacobi

760 A Street, South Frankfield, Illinois

760 A Street, South Frankfield, Illinois

2016-05-02

Brandon Deckert

Arnold-Ohletz-Str. 41a, Alt Malinascheid, Thüringen

Arnold-Ohletz-Str. 41a, Alt Malinascheid, Thüringen

2016-05-01

Margie Smith

23618 Windsor Drive, West Ricardoview, Idaho

23618 Windsor Drive, West Ricardoview, Idaho

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxkaXY+XG4gICAgICA8ZWwtY2hlY2tib3ggdi1tb2RlbD1cImNvbmZpZy5zaG93T3ZlcmZsb3dUb29sdGlwXCI+XG4gICAgICAgIHNob3dPdmVyZmxvd1Rvb2x0aXBcbiAgICAgIDwvZWwtY2hlY2tib3g+XG4gICAgICA8ZWwtc2VsZWN0XG4gICAgICAgIHYtbW9kZWw9XCJjb25maWcudG9vbHRpcEVmZmVjdFwiXG4gICAgICAgIGNsYXNzPVwibWwtNVwiXG4gICAgICAgIHN0eWxlPVwibWF4LXdpZHRoOiAxNTBweFwiXG4gICAgICA+XG4gICAgICAgIDxlbC1vcHRpb24gdmFsdWU9XCJkYXJrXCIgbGFiZWw9XCJkYXJrXCIgLz5cbiAgICAgICAgPGVsLW9wdGlvbiB2YWx1ZT1cImxpZ2h0XCIgbGFiZWw9XCJsaWdodFwiIC8+XG4gICAgICA8L2VsLXNlbGVjdD5cbiAgICA8L2Rpdj5cbiAgICA8ZWwtZGl2aWRlciAvPlxuICAgIDxlbC1jb25maWctcHJvdmlkZXIgOnRhYmxlPVwiY29uZmlnXCI+XG4gICAgICA8ZWwtdGFibGUgOmRhdGE9XCJ0YWJsZURhdGFcIiBzdHlsZT1cIndpZHRoOiAxMDAlXCI+XG4gICAgICAgIDxlbC10YWJsZS1jb2x1bW4gdHlwZT1cInNlbGVjdGlvblwiIHdpZHRoPVwiNTVcIiAvPlxuICAgICAgICA8ZWwtdGFibGUtY29sdW1uIGxhYmVsPVwiRGF0ZVwiIHdpZHRoPVwiMTIwXCI+XG4gICAgICAgICAgPHRlbXBsYXRlICNkZWZhdWx0PVwic2NvcGVcIj57eyBzY29wZS5yb3cuZGF0ZSB9fTwvdGVtcGxhdGU+XG4gICAgICAgIDwvZWwtdGFibGUtY29sdW1uPlxuICAgICAgICA8ZWwtdGFibGUtY29sdW1uIHByb3BlcnR5PVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIHdpZHRoPVwiMTIwXCIgLz5cbiAgICAgICAgPGVsLXRhYmxlLWNvbHVtblxuICAgICAgICAgIHByb3BlcnR5PVwiYWRkcmVzc1wiXG4gICAgICAgICAgbGFiZWw9XCJBZGRyZXNzIChpbmhlcml0ZWQgZnJvbSBjb25maWctcHJvdmlkZXIpXCJcbiAgICAgICAgICB3aWR0aD1cIjMwMFwiXG4gICAgICAgIC8+XG4gICAgICAgIDxlbC10YWJsZS1jb2x1bW5cbiAgICAgICAgICBwcm9wZXJ0eT1cImFkZHJlc3NcIlxuICAgICAgICAgIGxhYmVsPVwiQWRkcmVzcyAoZXhwbGljaXQgZmFsc2UpXCJcbiAgICAgICAgICA6c2hvdy1vdmVyZmxvdy10b29sdGlwPVwiZmFsc2VcIlxuICAgICAgICAvPlxuICAgICAgPC9lbC10YWJsZT5cbiAgICA8L2VsLWNvbmZpZy1wcm92aWRlcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVhY3RpdmUgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgVGFibGVDb25maWdDb250ZXh0IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBjb25maWcgPSByZWFjdGl2ZTxUYWJsZUNvbmZpZ0NvbnRleHQ+KHtcbiAgc2hvd092ZXJmbG93VG9vbHRpcDogdHJ1ZSxcbiAgdG9vbHRpcEVmZmVjdDogJ2RhcmsnLFxufSlcblxuaW50ZXJmYWNlIFVzZXIge1xuICBkYXRlOiBzdHJpbmdcbiAgbmFtZTogc3RyaW5nXG4gIGFkZHJlc3M6IHN0cmluZ1xufVxuXG5jb25zdCB0YWJsZURhdGE6IFVzZXJbXSA9IFtcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA0JyxcbiAgICBuYW1lOiAnQWxleW5hIEt1dHpuZXInLFxuICAgIGFkZHJlc3M6ICdMb2hyYmVyZ3N0ci4gODZjLCBTw7xkIExpbGxpLCBTYWFybGFuZCcsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMycsXG4gICAgbmFtZTogJ0hlbGVuIEphY29iaScsXG4gICAgYWRkcmVzczogJzc2MCBBIFN0cmVldCwgU291dGggRnJhbmtmaWVsZCwgSWxsaW5vaXMnLFxuICB9LFxuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDInLFxuICAgIG5hbWU6ICdCcmFuZG9uIERlY2tlcnQnLFxuICAgIGFkZHJlc3M6ICdBcm5vbGQtT2hsZXR6LVN0ci4gNDFhLCBBbHQgTWFsaW5hc2NoZWlkLCBUaMO8cmluZ2VuJyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTAxJyxcbiAgICBuYW1lOiAnTWFyZ2llIFNtaXRoJyxcbiAgICBhZGRyZXNzOiAnMjM2MTggV2luZHNvciBEcml2ZSwgV2VzdCBSaWNhcmRvdmlldywgSWRhaG8nLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/config-provider/table.vue)_

vue

```
<template>
  <div>
    <div>
      <el-checkbox v-model="config.showOverflowTooltip">
        showOverflowTooltip
      </el-checkbox>
      <el-select
        v-model="config.tooltipEffect"
        class="ml-5"
        style="max-width: 150px"
      >
        <el-option value="dark" label="dark" />
        <el-option value="light" label="light" />
      </el-select>
    </div>
    <el-divider />
    <el-config-provider :table="config">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column type="selection" width="55" />
        <el-table-column label="Date" width="120">
          <template #default="scope">{{ scope.row.date }}</template>
        </el-table-column>
        <el-table-column property="name" label="Name" width="120" />
        <el-table-column
          property="address"
          label="Address (inherited from config-provider)"
          width="300"
        />
        <el-table-column
          property="address"
          label="Address (explicit false)"
          :show-overflow-tooltip="false"
        />
      </el-table>
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

import type { TableConfigContext } from 'element-plus'

const config = reactive<TableConfigContext>({
  showOverflowTooltip: true,
  tooltipEffect: 'dark',
})

interface User {
  date: string
  name: string
  address: string
}

const tableData: User[] = [
  {
    date: '2016-05-04',
    name: 'Aleyna Kutzner',
    address: 'Lohrbergstr. 86c, Süd Lilli, Saarland',
  },
  {
    date: '2016-05-03',
    name: 'Helen Jacobi',
    address: '760 A Street, South Frankfield, Illinois',
  },
  {
    date: '2016-05-02',
    name: 'Brandon Deckert',
    address: 'Arnold-Ohletz-Str. 41a, Alt Malinascheid, Thüringen',
  },
  {
    date: '2016-05-01',
    name: 'Margie Smith',
    address: '23618 Windsor Drive, West Ricardoview, Idaho',
  },
]
</script>
```

隐藏源代码

## 实验性功能 [​](#实验性功能)

在本节中，您可以学习如何使用 Config Provider 来提供实验性功能。 现在，我们还没有添加任何实验性功能，但在未来的规划中，我们将添加一些实验性功能。 您可以使用此配置来管理这些功能。

## API [​](#api)

### Config Provider Attributes [​](#config-provider-attributes)

属性名

说明

类型

默认值

locale

翻译文本对象

`object`[](https://github.com/element-plus/element-plus/blob/a98ff9b40c0c3d2b9959f99919bd8363e3e3c25a/packages/locale/index.ts#L5) [languages](https://github.com/element-plus/element-plus/tree/dev/packages/locale/lang)

[en](https://github.com/element-plus/element-plus/blob/dev/packages/locale/lang/en.ts)

size

全局组件大小

`enum`

default

zIndex

全局初始化 zIndex 的值

`number`

—

namespace

全局组件类名称前缀 (需要配合 [$namespace](https://github.com/element-plus/element-plus/blob/dev/packages/theme-chalk/src/mixins/config.scss#L1) 使用)

`string`

el

button

按钮相关配置，[详见下表](#button-attribute)

`object`

详见下表

link

链接相关的配置， [见下表](#link-attribute)

`object`

详见下表

dialog 2.10.7

dialog 相关的配置， [见下表](#dialog-attribute)

`object`

详见下表

message

消息相关配置， [详见下表](#message-attribute)

`object`

详见下表

experimental-features

将要添加的实验阶段的功能，所有功能都是默认设置为 false

`object`

—

empty-values 2.7.0

输入类组件空值

`array`

—

value-on-clear 2.7.0

输入类组件清空值

`string` / `number` / `boolean` / `Function`

—

table 2.13.3

表格相关配置， [详见下表](#table-attribute)

`object`

详见下表

### Button Attribute [​](#button-attribute)

参数

描述

类型

默认值

type 2.9.11

按钮类型，在设置`color`时，后者优先。

`enum`

—

autoInsertSpace

两个中文字符之间自动插入空格(仅当文本长度为 2 且所有字符均为中文时才生效)

`boolean`

false

plain 2.9.11

是否为朴素按钮

`boolean`

false

text 2.11.0

是否为文字按钮

`boolean`

false

round 2.9.11

是否为圆角按钮

`boolean`

false

dashed 2.13.3

是否是虚线按钮

`boolean`

false

### 链接属性 [​](#链接属性)

参数

描述

类型

默认值

type 2.9.11

类型

`enum`

default

underline 2.9.11

控制下划线是否出现

`enum`

hover

### Card Attribute [​](#card-attribute)

属性

描述

类型

默认值

shadow 2.10.5

设置阴影显示时机

`enum`

—

### Dialog 属性 [​](#dialog-属性)

属性

描述

类型

默认值

align-center 2.10.7

是否水平垂直对齐对话框

`boolean`

false

draggable 2.10.7

为 Dialog 启用可拖拽功能

`boolean`

false

overflow 2.10.7

拖动范围可以超出可视区

`boolean`

false

transition 2.10.7

对话框动画的自定义过渡配置。 可以是一个字符串（过渡名称），也可以是一个包含 Vue 过渡属性的对象。

`string` / `object`

—

### Message Attribute [​](#message-attribute)

属性

详情

类型

默认值

max

可同时显示的消息最大数量

`number`

—

grouping 2.8.2

合并内容相同的消息，不支持 VNode 类型的消息

`boolean`

—

duration 2.8.2

显示时间，单位为毫秒。 设为 0 则不会自动关闭

`number`

—

showClose 2.8.2

是否显示关闭按钮

`boolean`

—

offset 2.8.2

Message 距离窗口顶部的偏移量

`number`

—

plain 2.9.11

是否纯色

`boolean`

—

placement 2.11.0

消息放置位置

`enum`

—

### Table Attribute 2.13.3 [​](#table-attribute)

属性

详情

Type

Default

show-overflow-tooltip

是否隐藏额外内容并在单元格悬停时使用 Tooltip 显示它们。这将影响全部列的展示，详请参考[tooltip-options](#table-attributes)

`boolean` / \[`object`\]

—

tooltip-effect

溢出的 tooltip 的 `effect`

`enum`

dark

tooltip-options

溢出 tooltip 的选项，[参见下述 tooltip 组件](./tooltip.html#attributes)

`object`

`object`

tooltip-formatter

使用 `show-overflow-tooltip` 时自定义 tooltip 内容

`Function`

—

### Config Provider Slots [​](#config-provider-slots)

名称

Description

Type

default

自定义默认内容

config: 提供全局配置（从顶部继承）

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/config-provider) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/config-provider.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/config-provider.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/33687038?v=4&size=64)](https://github.com/guozi9999)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/35426360?v=4&size=64)](https://github.com/Jungzl)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)[![](https://avatars.githubusercontent.com/u/106626227?v=4&size=64)](https://github.com/build-admin)

[Typography 排版](/zh-CN/component/typography)

[Autocomplete 自动补全输入框](/zh-CN/component/autocomplete)