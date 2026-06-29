---
name: "divider"
description: "Divider 分割线 -- Element Plus Vue3 桌面端组件。Invoke when user needs Divider 分割线 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/divider.html"
---

---

# Divider 分割线 [​](#divider-分割线)

更新日志待解决

1

区隔内容的分割线。

## 基础用法 [​](#基础用法)

对不同段落的文本进行分割。

I sit at my window this morning where the world like a passer-by stops for a moment, nods to me and goes.

There little thoughts are the rustle of leaves; they have their whisper of joy in my mind.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxzcGFuPlxuICAgICAgSSBzaXQgYXQgbXkgd2luZG93IHRoaXMgbW9ybmluZyB3aGVyZSB0aGUgd29ybGQgbGlrZSBhIHBhc3Nlci1ieSBzdG9wcyBmb3JcbiAgICAgIGEgbW9tZW50LCBub2RzIHRvIG1lIGFuZCBnb2VzLlxuICAgIDwvc3Bhbj5cbiAgICA8ZWwtZGl2aWRlciAvPlxuICAgIDxzcGFuPlxuICAgICAgVGhlcmUgbGl0dGxlIHRob3VnaHRzIGFyZSB0aGUgcnVzdGxlIG9mIGxlYXZlczsgdGhleSBoYXZlIHRoZWlyIHdoaXNwZXIgb2ZcbiAgICAgIGpveSBpbiBteSBtaW5kLlxuICAgIDwvc3Bhbj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/divider/basic-usage.vue)_

vue

```
<template>
  <div>
    <span>
      I sit at my window this morning where the world like a passer-by stops for
      a moment, nods to me and goes.
    </span>
    <el-divider />
    <span>
      There little thoughts are the rustle of leaves; they have their whisper of
      joy in my mind.
    </span>
  </div>
</template>
```

隐藏源代码

## 设置文案 [​](#设置文案)

可以在分割线上自定义文本内容。

What you are you do not see, what you see is your shadow.

Rabindranath Tagore

My wishes are fools, they shout across thy song, my Master. Let me but listen.

I cannot choose the best. The best chooses me.

Rabindranath Tagore

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxzcGFuPldoYXQgeW91IGFyZSB5b3UgZG8gbm90IHNlZSwgd2hhdCB5b3Ugc2VlIGlzIHlvdXIgc2hhZG93LiA8L3NwYW4+XG4gICAgPGVsLWRpdmlkZXIgY29udGVudC1wb3NpdGlvbj1cImxlZnRcIj5SYWJpbmRyYW5hdGggVGFnb3JlPC9lbC1kaXZpZGVyPlxuICAgIDxzcGFuPlxuICAgICAgTXkgd2lzaGVzIGFyZSBmb29scywgdGhleSBzaG91dCBhY3Jvc3MgdGh5IHNvbmcsIG15IE1hc3Rlci4gTGV0IG1lIGJ1dFxuICAgICAgbGlzdGVuLlxuICAgIDwvc3Bhbj5cbiAgICA8ZWwtZGl2aWRlcj5cbiAgICAgIDxlbC1pY29uPjxzdGFyLWZpbGxlZCAvPjwvZWwtaWNvbj5cbiAgICA8L2VsLWRpdmlkZXI+XG4gICAgPHNwYW4+SSBjYW5ub3QgY2hvb3NlIHRoZSBiZXN0LiBUaGUgYmVzdCBjaG9vc2VzIG1lLjwvc3Bhbj5cbiAgICA8ZWwtZGl2aWRlciBjb250ZW50LXBvc2l0aW9uPVwicmlnaHRcIj5SYWJpbmRyYW5hdGggVGFnb3JlPC9lbC1kaXZpZGVyPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBTdGFyRmlsbGVkIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/divider/custom-content.vue)_

vue

```
<template>
  <div>
    <span>What you are you do not see, what you see is your shadow. </span>
    <el-divider content-position="left">Rabindranath Tagore</el-divider>
    <span>
      My wishes are fools, they shout across thy song, my Master. Let me but
      listen.
    </span>
    <el-divider>
      <el-icon><star-filled /></el-icon>
    </el-divider>
    <span>I cannot choose the best. The best chooses me.</span>
    <el-divider content-position="right">Rabindranath Tagore</el-divider>
  </div>
</template>

<script lang="ts" setup>
import { StarFilled } from '@element-plus/icons-vue'
</script>
```

隐藏源代码

## 虚线 [​](#虚线)

您可以设置分隔符的样式。

What language is thine, O sea?

The language of eternal question.

What language is thy answer, O sky?

The language of eternal silence.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxzcGFuPldoYXQgbGFuZ3VhZ2UgaXMgdGhpbmUsIE8gc2VhPzwvc3Bhbj5cbiAgICA8ZWwtZGl2aWRlciBib3JkZXItc3R5bGU9XCJkYXNoZWRcIiAvPlxuICAgIDxzcGFuPlRoZSBsYW5ndWFnZSBvZiBldGVybmFsIHF1ZXN0aW9uLjwvc3Bhbj5cbiAgPC9kaXY+XG4gIDxlbC1kaXZpZGVyIGJvcmRlci1zdHlsZT1cImRvdHRlZFwiIC8+XG4gIDxzcGFuPldoYXQgbGFuZ3VhZ2UgaXMgdGh5IGFuc3dlciwgTyBza3k/PC9zcGFuPlxuICA8ZWwtZGl2aWRlciBib3JkZXItc3R5bGU9XCJkb3VibGVcIiAvPlxuICA8c3Bhbj5UaGUgbGFuZ3VhZ2Ugb2YgZXRlcm5hbCBzaWxlbmNlLjwvc3Bhbj5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/divider/line-dashed.vue)_

vue

```
<template>
  <div>
    <span>What language is thine, O sea?</span>
    <el-divider border-style="dashed" />
    <span>The language of eternal question.</span>
  </div>
  <el-divider border-style="dotted" />
  <span>What language is thy answer, O sky?</span>
  <el-divider border-style="double" />
  <span>The language of eternal silence.</span>
</template>
```

隐藏源代码

## 垂直分隔线 [​](#垂直分隔线)

Rain

Home

Grass

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxzcGFuPlJhaW48L3NwYW4+XG4gICAgPGVsLWRpdmlkZXIgZGlyZWN0aW9uPVwidmVydGljYWxcIiAvPlxuICAgIDxzcGFuPkhvbWU8L3NwYW4+XG4gICAgPGVsLWRpdmlkZXIgZGlyZWN0aW9uPVwidmVydGljYWxcIiBib3JkZXItc3R5bGU9XCJkYXNoZWRcIiAvPlxuICAgIDxzcGFuPkdyYXNzPC9zcGFuPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/divider/vertical-divider.vue)_

vue

```
<template>
  <div>
    <span>Rain</span>
    <el-divider direction="vertical" />
    <span>Home</span>
    <el-divider direction="vertical" border-style="dashed" />
    <span>Grass</span>
  </div>
</template>
```

隐藏源代码

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| direction | 设置分割线方向 | `enum` | horizontal |
| border-style | 设置分隔符样式 | `enum` [css/border-style](https://developer.mozilla.org/zh-CN/docs/Web/CSS/border-style) | solid |
| content-position | 自定义分隔线内容的位置 | `enum` | center |

### Slots [​](#slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 设置分割线文案的位置 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/divider) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/divider.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/divider.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/20151622?v=4&size=64)](https://github.com/william-xue)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/88016243?v=4&size=64)](https://github.com/wzrove)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/52314078?v=4&size=64)](https://github.com/vaebe)

[Tooltip 文字提示](https://element-plus.org/zh-CN/component/tooltip)

[Watermark 水印](https://element-plus.org/zh-CN/component/watermark)


