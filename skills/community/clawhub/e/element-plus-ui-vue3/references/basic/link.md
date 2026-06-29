---
name: "link"
description: "Link 链接 -- Element Plus Vue3 桌面端组件。Invoke when user needs Link 链接 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/link.html"
---

---

# Link 链接 [​](#link-链接)

更新日志待解决

5

文字超链接

安全警告 `href` prop 将会直接渲染到 `<a>` 标签内部。 如果你传递类似 `javascript:alert(1)` 这样的值或恶意 URL，可能会导致 **XSS** 或**开放重定向漏洞**。

在使用前始终验证并净化 URL。 例如：

显示代码示例

js

```
function sanitigzeUrl(url) {
  const allowedprotocol= ['http:', 'https://']
  try {
    const parsed = new URL(url, window.location.origin)
    return allowedProtocols.includes(parsed.protocol) ? parsed.href : '#'
  } catch {
    return '#'
  }
}
```

## 基础用法 [​](#基础用法)

基础的文字链接用法。

[default](https://element-plus.org/)primarysuccesswarningdangerinfo

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1saW5rIGhyZWY9XCJodHRwczovL2VsZW1lbnQtcGx1cy5vcmdcIiB0YXJnZXQ9XCJfYmxhbmtcIj5kZWZhdWx0PC9lbC1saW5rPlxuICAgIDxlbC1saW5rIHR5cGU9XCJwcmltYXJ5XCI+cHJpbWFyeTwvZWwtbGluaz5cbiAgICA8ZWwtbGluayB0eXBlPVwic3VjY2Vzc1wiPnN1Y2Nlc3M8L2VsLWxpbms+XG4gICAgPGVsLWxpbmsgdHlwZT1cIndhcm5pbmdcIj53YXJuaW5nPC9lbC1saW5rPlxuICAgIDxlbC1saW5rIHR5cGU9XCJkYW5nZXJcIj5kYW5nZXI8L2VsLWxpbms+XG4gICAgPGVsLWxpbmsgdHlwZT1cImluZm9cIj5pbmZvPC9lbC1saW5rPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZWwtbGluayB7XG4gIG1hcmdpbi1yaWdodDogOHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/link/basic.vue)_

vue

```
<template>
  <div>
    <el-link href="https://element-plus.org" target="_blank">default</el-link>
    <el-link type="primary">primary</el-link>
    <el-link type="success">success</el-link>
    <el-link type="warning">warning</el-link>
    <el-link type="danger">danger</el-link>
    <el-link type="info">info</el-link>
  </div>
</template>

<style scoped>
.el-link {
  margin-right: 8px;
}
</style>
```

隐藏源代码

## 禁用状态 [​](#禁用状态)

文字链接不可用状态。

defaultprimarysuccesswarningdangerinfo

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1saW5rIGRpc2FibGVkPmRlZmF1bHQ8L2VsLWxpbms+XG4gICAgPGVsLWxpbmsgdHlwZT1cInByaW1hcnlcIiBkaXNhYmxlZD5wcmltYXJ5PC9lbC1saW5rPlxuICAgIDxlbC1saW5rIHR5cGU9XCJzdWNjZXNzXCIgZGlzYWJsZWQ+c3VjY2VzczwvZWwtbGluaz5cbiAgICA8ZWwtbGluayB0eXBlPVwid2FybmluZ1wiIGRpc2FibGVkPndhcm5pbmc8L2VsLWxpbms+XG4gICAgPGVsLWxpbmsgdHlwZT1cImRhbmdlclwiIGRpc2FibGVkPmRhbmdlcjwvZWwtbGluaz5cbiAgICA8ZWwtbGluayB0eXBlPVwiaW5mb1wiIGRpc2FibGVkPmluZm88L2VsLWxpbms+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlIHNjb3BlZD5cbi5lbC1saW5rIHtcbiAgbWFyZ2luLXJpZ2h0OiA4cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/link/disabled.vue)_

vue

```
<template>
  <div>
    <el-link disabled>default</el-link>
    <el-link type="primary" disabled>primary</el-link>
    <el-link type="success" disabled>success</el-link>
    <el-link type="warning" disabled>warning</el-link>
    <el-link type="danger" disabled>danger</el-link>
    <el-link type="info" disabled>info</el-link>
  </div>
</template>

<style scoped>
.el-link {
  margin-right: 8px;
}
</style>
```

隐藏源代码

## 下划线 [​](#下划线)

控制下划线是否出现

WARNING

属性 `boolean` 值 **将在** 3.0.0 版本中被**移除**，请考虑切换至新的 API。

TIP

从 2.9.9 开始，你可以使用 `'always' | 'hover' | 'never'` 来控制是否显示下划线。 文档中的示例将都使用这些值。 如果您使用的版本 **低于** 2.9.9，请参考：

vue

```
<template>
  <!-- works before 2.9.9, use 'hover' after, removed in 3.0.0 -->
  <el-link underline>link</el-link>
  <!-- works before 2.9.9, use 'never' after, removed in 3.0.0 -->
  <el-link :underline="false">link</el-link>
</template>
```

defaultalwayshovernever

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1saW5rPmRlZmF1bHQ8L2VsLWxpbms+XG4gICAgPGVsLWxpbmsgdW5kZXJsaW5lPVwiYWx3YXlzXCI+YWx3YXlzPC9lbC1saW5rPlxuICAgIDxlbC1saW5rIHVuZGVybGluZT1cImhvdmVyXCI+aG92ZXI8L2VsLWxpbms+XG4gICAgPGVsLWxpbmsgdW5kZXJsaW5lPVwibmV2ZXJcIj5uZXZlcjwvZWwtbGluaz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c3R5bGUgc2NvcGVkPlxuLmVsLWxpbmsge1xuICBtYXJnaW4tcmlnaHQ6IDhweDtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/link/underline.vue)_

vue

```
<template>
  <div>
    <el-link>default</el-link>
    <el-link underline="always">always</el-link>
    <el-link underline="hover">hover</el-link>
    <el-link underline="never">never</el-link>
  </div>
</template>

<style scoped>
.el-link {
  margin-right: 8px;
}
</style>
```

隐藏源代码

## 图标 [​](#图标)

带图标的链接

TIP

使用 `icon` 属性来为按钮添加图标。 您可以传递组件名称的字符串（提前注册）或组件本身是一个 SVG Vue 组件。 Element Plus 提供了一套图标，您可以在 [icon](https://element-plus.org/zh-CN/component/icon) 找到它们。

Edit Check

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxlbC1saW5rIDppY29uPVwiRWRpdFwiPkVkaXQ8L2VsLWxpbms+XG4gICAgPGVsLWxpbms+XG4gICAgICBDaGVjazxlbC1pY29uIGNsYXNzPVwiZWwtaWNvbi0tcmlnaHRcIj48aWNvbi12aWV3IC8+PC9lbC1pY29uPlxuICAgIDwvZWwtbGluaz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgRWRpdCwgVmlldyBhcyBJY29uVmlldyB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZWwtbGluayB7XG4gIG1hcmdpbi1yaWdodDogOHB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/link/with-icon.vue)_

vue

```
<template>
  <div>
    <el-link :icon="Edit">Edit</el-link>
    <el-link>
      Check<el-icon class="el-icon--right"><icon-view /></el-icon>
    </el-link>
  </div>
</template>

<script setup lang="ts">
import { Edit, View as IconView } from '@element-plus/icons-vue'
</script>

<style scoped>
.el-link {
  margin-right: 8px;
}
</style>
```

隐藏源代码

## Link API [​](#link-api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| type | 类型 | `enum` | default |
| underline | 控制下划线是否出现 | `enum` | hover |
| disabled | 是否禁用状态 | `boolean` | false |
| href | 原生 href 属性 | `string` | — |
| target | 同原生 `target` 属性 | `enum` | \_self |
| icon | 图标组件 | `string` / `Component` | — |

### Slots [​](#slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |
| icon | 自定义图标组件 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/link) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/link.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/link.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/45218946?v=4&size=64)](https://github.com/comp-squirrel)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/75007029?v=4&size=64)](https://github.com/yj-liuzepeng)[![](https://avatars.githubusercontent.com/u/13871363?v=4&size=64)](https://github.com/logustra)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/67825153?v=4&size=64)](https://github.com/FancyangY)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/57179957?v=4&size=64)](https://github.com/yeonjulee1005)[![](https://avatars.githubusercontent.com/u/43134418?v=4&size=64)](https://github.com/MonsterPi13)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)

[Layout 布局](https://element-plus.org/zh-CN/component/layout)

[Text 文本](https://element-plus.org/zh-CN/component/text)


