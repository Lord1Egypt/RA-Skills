---
name: "watermark"
description: "Watermark 水印 -- Element Plus Vue3 桌面端组件。Invoke when user needs Watermark 水印 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/watermark.html"
---

---

# Watermark 水印 [​](#watermark-水印)

更新日志待解决

0

在页面上添加文本或图片等水印信息

## 基础用法 [​](#基础用法)

最简单的用法。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlYWN0aXZlLCB3YXRjaCB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IGlzRGFyayB9IGZyb20gJ34vY29tcG9zYWJsZXMvZGFyaydcblxuY29uc3QgZm9udCA9IHJlYWN0aXZlKHtcbiAgY29sb3I6ICdyZ2JhKDAsIDAsIDAsIC4xNSknLFxufSlcblxud2F0Y2goXG4gIGlzRGFyayxcbiAgKCkgPT4ge1xuICAgIGZvbnQuY29sb3IgPSBpc0RhcmsudmFsdWVcbiAgICAgID8gJ3JnYmEoMjU1LCAyNTUsIDI1NSwgLjE1KSdcbiAgICAgIDogJ3JnYmEoMCwgMCwgMCwgLjE1KSdcbiAgfSxcbiAge1xuICAgIGltbWVkaWF0ZTogdHJ1ZSxcbiAgfVxuKVxuPC9zY3JpcHQ+XG5cbjx0ZW1wbGF0ZT5cbiAgPGVsLXdhdGVybWFyayA6Zm9udD1cImZvbnRcIj5cbiAgICA8ZGl2IHN0eWxlPVwiaGVpZ2h0OiA1MDBweFwiIC8+XG4gIDwvZWwtd2F0ZXJtYXJrPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/watermark/basic.vue)_

vue

```
<script setup lang="ts">
import { reactive, watch } from 'vue'
import { isDark } from '~/composables/dark'

const font = reactive({
  color: 'rgba(0, 0, 0, .15)',
})

watch(
  isDark,
  () => {
    font.color = isDark.value
      ? 'rgba(255, 255, 255, .15)'
      : 'rgba(0, 0, 0, .15)'
  },
  {
    immediate: true,
  }
)
</script>

<template>
  <el-watermark :font="font">
    <div style="height: 500px" />
  </el-watermark>
</template>
```

隐藏源代码

## 多行水印 [​](#多行水印)

使用 `content`设置一个字符串数组来指定多行文本水印内容

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlYWN0aXZlLCB3YXRjaCB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IGlzRGFyayB9IGZyb20gJ34vY29tcG9zYWJsZXMvZGFyaydcblxuY29uc3QgZm9udCA9IHJlYWN0aXZlKHtcbiAgY29sb3I6ICdyZ2JhKDAsIDAsIDAsIC4xNSknLFxufSlcblxud2F0Y2goXG4gIGlzRGFyayxcbiAgKCkgPT4ge1xuICAgIGZvbnQuY29sb3IgPSBpc0RhcmsudmFsdWVcbiAgICAgID8gJ3JnYmEoMjU1LCAyNTUsIDI1NSwgLjE1KSdcbiAgICAgIDogJ3JnYmEoMCwgMCwgMCwgLjE1KSdcbiAgfSxcbiAge1xuICAgIGltbWVkaWF0ZTogdHJ1ZSxcbiAgfVxuKVxuPC9zY3JpcHQ+XG5cbjx0ZW1wbGF0ZT5cbiAgPGVsLXdhdGVybWFyayA6Zm9udD1cImZvbnRcIiA6Y29udGVudD1cIlsnRWxlbWVudCsnLCAnRWxlbWVudCBQbHVzJ11cIj5cbiAgICA8ZGl2IHN0eWxlPVwiaGVpZ2h0OiA1MDBweFwiIC8+XG4gIDwvZWwtd2F0ZXJtYXJrPlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/watermark/multi-line.vue)_

vue

```
<script setup lang="ts">
import { reactive, watch } from 'vue'
import { isDark } from '~/composables/dark'

const font = reactive({
  color: 'rgba(0, 0, 0, .15)',
})

watch(
  isDark,
  () => {
    font.color = isDark.value
      ? 'rgba(255, 255, 255, .15)'
      : 'rgba(0, 0, 0, .15)'
  },
  {
    immediate: true,
  }
)
</script>

<template>
  <el-watermark :font="font" :content="['Element+', 'Element Plus']">
    <div style="height: 500px" />
  </el-watermark>
</template>
```

隐藏源代码

## 图片水印 [​](#图片水印)

通过 `image` 指定图像地址。 为了确保图像清晰展示而不是被拉伸，请设置宽度和高度，建议使用至少两倍的宽度和高度的图片来保证显示效果。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtd2F0ZXJtYXJrXG4gICAgOndpZHRoPVwiMTMwXCJcbiAgICA6aGVpZ2h0PVwiMzBcIlxuICAgIGltYWdlPVwiaHR0cHM6Ly9lbGVtZW50LXBsdXMub3JnL2ltYWdlcy9lbGVtZW50LXBsdXMtbG9nby5zdmdcIlxuICA+XG4gICAgPGRpdiBzdHlsZT1cImhlaWdodDogNTAwcHhcIiAvPlxuICA8L2VsLXdhdGVybWFyaz5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/watermark/image.vue)_

vue

```
<template>
  <el-watermark
    :width="130"
    :height="30"
    image="https://element-plus.org/images/element-plus-logo.svg"
  >
    <div style="height: 500px" />
  </el-watermark>
</template>
```

隐藏源代码

## 自定义配置 [​](#自定义配置)

配置自定义参数预览水印效果。

# Element Plus

## A Vue 3 based component library for designers and developers

![示例图片](https://element-plus.org/images/hamburger.png)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlYWN0aXZlLCB3YXRjaCB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IGlzRGFyayB9IGZyb20gJ34vY29tcG9zYWJsZXMvZGFyaydcblxuY29uc3QgY29uZmlnID0gcmVhY3RpdmUoe1xuICBjb250ZW50OiAnRWxlbWVudCBQbHVzJyxcbiAgZm9udDoge1xuICAgIGZvbnRTaXplOiAxNixcbiAgICBjb2xvcjogJ3JnYmEoMCwgMCwgMCwgMC4xNSknLFxuICB9LFxuICB6SW5kZXg6IC0xLFxuICByb3RhdGU6IC0yMixcbiAgZ2FwOiBbMTAwLCAxMDBdIGFzIFtudW1iZXIsIG51bWJlcl0sXG4gIG9mZnNldDogW10gYXMgdW5rbm93biBhcyBbbnVtYmVyLCBudW1iZXJdLFxufSlcblxud2F0Y2goXG4gIGlzRGFyayxcbiAgKHZhbHVlKSA9PiB7XG4gICAgY29uZmlnLmZvbnQuY29sb3IgPSB2YWx1ZVxuICAgICAgPyAncmdiYSgyNTUsIDI1NSwgMjU1LCAuMTUpJ1xuICAgICAgOiAncmdiYSgwLCAwLCAwLCAuMTUpJ1xuICB9LFxuICB7IGltbWVkaWF0ZTogdHJ1ZSB9XG4pXG48L3NjcmlwdD5cblxuPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwid3JhcHBlclwiPlxuICAgIDxlbC13YXRlcm1hcmtcbiAgICAgIGNsYXNzPVwid2F0ZXJtYXJrXCJcbiAgICAgIDpjb250ZW50PVwiY29uZmlnLmNvbnRlbnRcIlxuICAgICAgOmZvbnQ9XCJjb25maWcuZm9udFwiXG4gICAgICA6ei1pbmRleD1cImNvbmZpZy56SW5kZXhcIlxuICAgICAgOnJvdGF0ZT1cImNvbmZpZy5yb3RhdGVcIlxuICAgICAgOmdhcD1cImNvbmZpZy5nYXBcIlxuICAgICAgOm9mZnNldD1cImNvbmZpZy5vZmZzZXRcIlxuICAgID5cbiAgICAgIDxkaXYgY2xhc3M9XCJ3YXRlcm1hcmstY29udGFpbmVyXCI+XG4gICAgICAgIDxoMT5FbGVtZW50IFBsdXM8L2gxPlxuICAgICAgICA8aDI+QSBWdWUgMyBiYXNlZCBjb21wb25lbnQgbGlicmFyeSBmb3IgZGVzaWduZXJzIGFuZCBkZXZlbG9wZXJzPC9oMj5cbiAgICAgICAgPGltZyBzcmM9XCIvaW1hZ2VzL2hhbWJ1cmdlci5wbmdcIiBhbHQ9XCLnpLrkvovlm77niYdcIiAvPlxuICAgICAgPC9kaXY+XG4gICAgPC9lbC13YXRlcm1hcms+XG4gICAgPGVsLWZvcm1cbiAgICAgIGNsYXNzPVwiZm9ybVwiXG4gICAgICA6bW9kZWw9XCJjb25maWdcIlxuICAgICAgbGFiZWwtcG9zaXRpb249XCJ0b3BcIlxuICAgICAgbGFiZWwtd2lkdGg9XCI1MHB4XCJcbiAgICA+XG4gICAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiQ29udGVudFwiPlxuICAgICAgICA8ZWwtaW5wdXQgdi1tb2RlbD1cImNvbmZpZy5jb250ZW50XCIgLz5cbiAgICAgIDwvZWwtZm9ybS1pdGVtPlxuICAgICAgPGVsLWZvcm0taXRlbSBsYWJlbD1cIkNvbG9yXCI+XG4gICAgICAgIDxlbC1jb2xvci1waWNrZXIgdi1tb2RlbD1cImNvbmZpZy5mb250LmNvbG9yXCIgc2hvdy1hbHBoYSAvPlxuICAgICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiRm9udFNpemVcIj5cbiAgICAgICAgPGVsLXNsaWRlciB2LW1vZGVsPVwiY29uZmlnLmZvbnQuZm9udFNpemVcIiAvPlxuICAgICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiekluZGV4XCI+XG4gICAgICAgIDxlbC1zbGlkZXIgdi1tb2RlbD1cImNvbmZpZy56SW5kZXhcIiAvPlxuICAgICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiUm90YXRlXCI+XG4gICAgICAgIDxlbC1zbGlkZXIgdi1tb2RlbD1cImNvbmZpZy5yb3RhdGVcIiA6bWluPVwiLTE4MFwiIDptYXg9XCIxODBcIiAvPlxuICAgICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiR2FwXCI+XG4gICAgICAgIDxlbC1zcGFjZT5cbiAgICAgICAgICA8ZWwtaW5wdXQtbnVtYmVyIHYtbW9kZWw9XCJjb25maWcuZ2FwWzBdXCIgY29udHJvbHMtcG9zaXRpb249XCJyaWdodFwiIC8+XG4gICAgICAgICAgPGVsLWlucHV0LW51bWJlciB2LW1vZGVsPVwiY29uZmlnLmdhcFsxXVwiIGNvbnRyb2xzLXBvc2l0aW9uPVwicmlnaHRcIiAvPlxuICAgICAgICA8L2VsLXNwYWNlPlxuICAgICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgICA8ZWwtZm9ybS1pdGVtIGxhYmVsPVwiT2Zmc2V0XCI+XG4gICAgICAgIDxlbC1zcGFjZT5cbiAgICAgICAgICA8ZWwtaW5wdXQtbnVtYmVyXG4gICAgICAgICAgICB2LW1vZGVsPVwiY29uZmlnLm9mZnNldFswXVwiXG4gICAgICAgICAgICBwbGFjZWhvbGRlcj1cIm9mZnNldExlZnRcIlxuICAgICAgICAgICAgY29udHJvbHMtcG9zaXRpb249XCJyaWdodFwiXG4gICAgICAgICAgLz5cbiAgICAgICAgICA8ZWwtaW5wdXQtbnVtYmVyXG4gICAgICAgICAgICB2LW1vZGVsPVwiY29uZmlnLm9mZnNldFsxXVwiXG4gICAgICAgICAgICBwbGFjZWhvbGRlcj1cIm9mZnNldFRvcFwiXG4gICAgICAgICAgICBjb250cm9scy1wb3NpdGlvbj1cInJpZ2h0XCJcbiAgICAgICAgICAvPlxuICAgICAgICA8L2VsLXNwYWNlPlxuICAgICAgPC9lbC1mb3JtLWl0ZW0+XG4gICAgPC9lbC1mb3JtPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzdHlsZSBzY29wZWQ+XG4ud3JhcHBlciB7XG4gIGRpc3BsYXk6IGZsZXg7XG59XG4ud2F0ZXJtYXJrIHtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleDogYXV0bztcbn1cbi53YXRlcm1hcmstY29udGFpbmVyIHtcbiAgZmxleDogYXV0bztcbn1cbi5mb3JtIHtcbiAgd2lkdGg6IDMzMHB4O1xuICBtYXJnaW4tbGVmdDogMjBweDtcbiAgYm9yZGVyLWxlZnQ6IDFweCBzb2xpZCAjZWVlO1xuICBwYWRkaW5nLWxlZnQ6IDIwcHg7XG59XG5cbmltZyB7XG4gIHotaW5kZXg6IDEwO1xuICB3aWR0aDogMTAwJTtcbiAgbWF4LXdpZHRoOiAzMDBweDtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/watermark/custom.vue)_

vue

```
<script setup lang="ts">
import { reactive, watch } from 'vue'
import { isDark } from '~/composables/dark'

const config = reactive({
  content: 'Element Plus',
  font: {
    fontSize: 16,
    color: 'rgba(0, 0, 0, 0.15)',
  },
  zIndex: -1,
  rotate: -22,
  gap: [100, 100] as [number, number],
  offset: [] as unknown as [number, number],
})

watch(
  isDark,
  (value) => {
    config.font.color = value
      ? 'rgba(255, 255, 255, .15)'
      : 'rgba(0, 0, 0, .15)'
  },
  { immediate: true }
)
</script>

<template>
  <div class="wrapper">
    <el-watermark
      class="watermark"
      :content="config.content"
      :font="config.font"
      :z-index="config.zIndex"
      :rotate="config.rotate"
      :gap="config.gap"
      :offset="config.offset"
    >
      <div class="watermark-container">
        <h1>Element Plus</h1>
        <h2>A Vue 3 based component library for designers and developers</h2>
        <img src="/images/hamburger.png" alt="示例图片" />
      </div>
    </el-watermark>
    <el-form
      class="form"
      :model="config"
      label-position="top"
      label-width="50px"
    >
      <el-form-item label="Content">
        <el-input v-model="config.content" />
      </el-form-item>
      <el-form-item label="Color">
        <el-color-picker v-model="config.font.color" show-alpha />
      </el-form-item>
      <el-form-item label="FontSize">
        <el-slider v-model="config.font.fontSize" />
      </el-form-item>
      <el-form-item label="zIndex">
        <el-slider v-model="config.zIndex" />
      </el-form-item>
      <el-form-item label="Rotate">
        <el-slider v-model="config.rotate" :min="-180" :max="180" />
      </el-form-item>
      <el-form-item label="Gap">
        <el-space>
          <el-input-number v-model="config.gap[0]" controls-position="right" />
          <el-input-number v-model="config.gap[1]" controls-position="right" />
        </el-space>
      </el-form-item>
      <el-form-item label="Offset">
        <el-space>
          <el-input-number
            v-model="config.offset[0]"
            placeholder="offsetLeft"
            controls-position="right"
          />
          <el-input-number
            v-model="config.offset[1]"
            placeholder="offsetTop"
            controls-position="right"
          />
        </el-space>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.wrapper {
  display: flex;
}
.watermark {
  display: flex;
  flex: auto;
}
.watermark-container {
  flex: auto;
}
.form {
  width: 330px;
  margin-left: 20px;
  border-left: 1px solid #eee;
  padding-left: 20px;
}

img {
  z-index: 10;
  width: 100%;
  max-width: 300px;
  position: relative;
}
</style>
```

隐藏源代码

## API [​](#api)

### 属性 [​](#属性)

| 属性名 | 描述 | 类型 | 默认值 |
| --- | --- | --- | --- |
| width | 水印的宽度， `content` 的默认值是它自己的宽度 | `number` | 120 |
| height | 水印的高度， `content` 的默认值是它自己的高度 | `number` | 64 |
| rotate | 水印的旋转角度, 单位 `°` | `number` | \-22 |
| z-index | 水印元素的z-index值 | `number` | 9 |
| image | 水印图片，建议使用 2x 或 3x 图像 | `string` | — |
| content | 水印文本内容 | `string`/`array` | Element Plus |
| font | 文字样式 | [Font](#font) | [字体](#font) |
| gap | 水印之间的间距 | `array` | \[100, 100\] |
| offset | 水印从容器左上角的偏移 默认值为 `gap/2` | `array` | \[gap\[0\]/2, gap\[1\]/2\] |

### Font [​](#font)

| 名称 | 详情 | 类型 | 默认 |
| --- | --- | --- | --- |
| color | 字体颜色 | `string` | rgba(0,0,0,.15) |
| fontSize | 字体大小 | `number` / `string` | 16 |
| fontWeight | 字重 | `enum` | normal |
| fontFamily | 字体 | `string` | sans-serif |
| fontGap 2.11.5 | 字体间隙 | `number` | 3 |
| fontStyle | 字体样式 | `enum` | normal |
| textAlign | 文本对齐 | `enum` | center |
| textBaseline | 文本基线 | `enum` | hanging |

### Slots [​](#slots)

| 名称 | 详情 |
| --- | --- |
| 默认 | 添加水印的容器 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/watermark) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/watermark.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/54931083?v=4&size=64)](https://github.com/wjp980108)[![](https://avatars.githubusercontent.com/u/52928534?v=4&size=64)](https://github.com/alonely-boy)[![](https://avatars.githubusercontent.com/u/45616067?v=4&size=64)](https://github.com/elioist)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/1532716?v=4&size=64)](https://github.com/godxiaoji)[![](https://avatars.githubusercontent.com/u/27912232?v=4&size=64)](https://github.com/Fuphoenixes)[![](https://avatars.githubusercontent.com/u/66096254?v=4&size=64)](https://github.com/IceyWu)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/22388686?v=4&size=64)](https://github.com/TomatoDroid)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)

[Divider 分割线](https://element-plus.org/zh-CN/component/divider)


