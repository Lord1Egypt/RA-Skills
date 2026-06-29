---
name: "affix"
description: "Affix 固钉 -- Element Plus Vue3 桌面端组件。Invoke when user needs Affix 固钉 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/affix.html"
---

---

# Affix 固钉 [​](#affix-固钉)

更新日志待解决

4

将页面元素固定在特定可视区域。

## 基础用法 [​](#基础用法)

固钉默认固定在页面顶部。

通过设置 `offset` 属性来改变吸顶距离，默认值为 0。

Offset top 120px

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYWZmaXggOm9mZnNldD1cIjEyMFwiPlxuICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIj5PZmZzZXQgdG9wIDEyMHB4PC9lbC1idXR0b24+XG4gIDwvZWwtYWZmaXg+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/affix/basic.vue)_

vue

```
<template>
  <el-affix :offset="120">
    <el-button type="primary">Offset top 120px</el-button>
  </el-affix>
</template>
```

隐藏源代码

## 指定容器 [​](#指定容器)

通过设置 `target` 属性，让固钉始终保持在容器内， 超过范围则隐藏。

请注意容器避免出现滚动条。

Target container

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiYWZmaXgtY29udGFpbmVyXCI+XG4gICAgPGVsLWFmZml4IHRhcmdldD1cIi5hZmZpeC1jb250YWluZXJcIiA6b2Zmc2V0PVwiODBcIj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIj5UYXJnZXQgY29udGFpbmVyPC9lbC1idXR0b24+XG4gICAgPC9lbC1hZmZpeD5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c3R5bGUgc2NvcGVkPlxuLmFmZml4LWNvbnRhaW5lciB7XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbiAgaGVpZ2h0OiA0MDBweDtcbiAgYm9yZGVyLXJhZGl1czogNHB4O1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5LWxpZ2h0LTkpO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/affix/target.vue)_

vue

```
<template>
  <div class="affix-container">
    <el-affix target=".affix-container" :offset="80">
      <el-button type="primary">Target container</el-button>
    </el-affix>
  </div>
</template>

<style scoped>
.affix-container {
  text-align: center;
  height: 400px;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
}
</style>
```

隐藏源代码

## 固定位置 [​](#固定位置)

Affix 组件提供 2 个固定的位置参数 `top` 和 `bottom`。

通过设置 `position` 属性来改变固定位置，默认值为 `top` 。

Offset bottom 20px

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYWZmaXggcG9zaXRpb249XCJib3R0b21cIiA6b2Zmc2V0PVwiMjBcIj5cbiAgICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCI+T2Zmc2V0IGJvdHRvbSAyMHB4PC9lbC1idXR0b24+XG4gIDwvZWwtYWZmaXg+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/affix/fixed.vue)_

vue

```
<template>
  <el-affix position="bottom" :offset="20">
    <el-button type="primary">Offset bottom 20px</el-button>
  </el-affix>
</template>
```

隐藏源代码

## API [​](#api)

### 属性 [​](#属性)

| 名称 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| offset | 偏移距离 | `number` | 0 |
| position | 固钉位置 | `enum` | top |
| target | 指定容器（CSS 选择器） | `string` | — |
| z-index | `z-index` | `number` | 100 |
| teleported 2.13.0 | Affix 元素是否使用 teleport 特性，设置为 `true` 将会使得该元素“传送”至 `append-to` 设置的位置 | `boolean` | false |
| append-to 2.13.0 | Affix 元素将被挂载至哪个元素 | `CSSSelector` / `HTMLElement` | body |

### 事件 [​](#事件)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| change | 固钉状态改变时触发的事件 | `Function` |
| scroll | 滚动时触发的事件 | `Function` |

### 插槽 [​](#插槽)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

### 暴露 [​](#暴露)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| update | 手动更新固钉状态 | `Function` |
| updateRoot | 手动更新根元素的盒模型信息 | `Function` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/affix) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/affix.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/affix.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/46664126?v=4&size=64)](https://github.com/btnkr)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/50874301?v=4&size=64)](https://github.com/markbiu)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/72804789?v=4&size=64)](https://github.com/akashbagchi)[![](https://avatars.githubusercontent.com/u/17726809?v=4&size=64)](https://github.com/LiZhequ)[![](https://avatars.githubusercontent.com/u/26272596?v=4&size=64)](https://github.com/CodeListener)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/47516844?v=4&size=64)](https://github.com/midcu)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/22695767?v=4&size=64)](https://github.com/deepthan)[![](https://avatars.githubusercontent.com/u/20411966?v=4&size=64)](https://github.com/SorrowX)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)

[Segmented 分段控制器](https://element-plus.org/zh-CN/component/segmented)

[Anchor 锚点](https://element-plus.org/zh-CN/component/anchor)


