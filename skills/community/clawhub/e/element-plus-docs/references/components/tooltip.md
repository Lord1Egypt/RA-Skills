## Tooltip 文字提示 ​

**URL:** https://element-plus.org/zh-CN/component/tooltip.html

**Contents:**
- Tooltip 文字提示 ​
- 基础用法 ​
- 主题 ​
- 更多内容的文字提示 ​
- 高级扩展 ​
- 显示 HTML 内容 ​
- 虚拟触发 ​
- 单例模式 ​
- 受控模式 ​
- 自定义动画 ​

常用于展示鼠标 hover 时的提示信息。

在这里我们提供 9 种不同方向的展示方式，可以通过以下完整示例来理解，选择你要的效果。

使用 content 属性来决定 hover 时的提示信息。 由 placement 属性决定展示效果： placement属性值为：[方向]-[对齐位置]；四个方向：top、left、right、bottom；三种对齐位置：start, end，默认为空。 如 placement="left-end"，则提示信息出现在目标元素的左侧，且提示信息的底部与目标元素的底部对齐。

Tooltip 组件内置了两个主题：dark和light。

要使用自定义主题，您必须知道您的工具提示在哪里渲染， 如果您的工具提示被呈现为根元素，您将需要全局设置css规则。

建议您使用自定义主题并同时显示箭头时不使用线性渐变背景颜色。 因为弹出箭头和内容是两个不同的元素， 弹出箭头的样式需要单独设置， 当它到渐变背景颜色时，会看起来很奇怪。

通过设置 effect 来修改主题，默认值为 dark.

用具名 slot content，替代tooltip中的content属性。

除了这些基本设置外，还有一些属性可以让使用者更好的定制自己的效果：

transition 属性可以定制显隐的动画效果，默认为fade-in-linear。

如果需要关闭 tooltip 功能，disabled 属性可以满足这个需求， 你只需要将其设置为 true。

事实上，Tooltip 是一个基于 ElPopper 的扩展，您可以使用 ElPopper 中允许的任何属性。

Tooltip 内不支持 router-link 组件，请使用 vm.$router.push 代替。

tooltip 内不支持 disabled form 元素，参考 MDN， 请在 disabled form 元素外层添加一层包裹元素。

content 属性虽然支持传入 HTML 片段，但是在网站上动态渲染任意 HTML 是非常危险的，因为容易导致 XSS 攻击。 因此在 raw-content 打开的情况下，请确保 content 的内容是可信的，永远不要将用户提交的内容赋值给 content 属性。

有时候我们想把 tooltip 的触发元素放在别的地方，而不需要写在一起，这时候就可以使用虚拟触发。

需要注意的是，虚拟触发的 tooltip 是受控组件，因此你必须自己去控制 tooltip 是否显示，你将无法通过点击空白处来关闭 tooltip。

Tooltip 可以作为单例，也就是是说你可以同时有多个触发同一个 tooltip 的触发元素，这个功能是在 虚拟触发 的基础上开发的。

已知问题：使用单例模式时，弹出窗口会从意料之外的位置弹出。

Tooltip 可以通过父组件使用 :visible 来控制它的显示与关闭。

Tooltip 可以自定义动画，您可以使用 transition 设置所需的动画效果。

过渡效果的更多信息可以在 Vue 过渡效果 中找到。

您必须等待 DOM 加载后才能使用 targetElement。

**Examples:**

Example 1 (jsx):
```jsx
<template>
  <div class="tooltip-base-box">
    <div class="row center">
      <el-tooltip
        class="box-item"
        effect="dark"
        content="Top Left prompts info"
        placement="top-start"
      >
        <el-button>top-start</el-button>
      </el-tooltip>
      <el-tooltip
        class="box-item"
        effect="dark"
        content="Top Center prompts info"
        placement="top"
      >
        <el-button>top</el-button>
      </el-tooltip>
      <el-tooltip
        class="box-item"
        effect="dark"
        content="Top Right prompts info"
        placement="top-end"
      >
        <el-button>top-end</el-button>
      </el-tooltip>
    </div>
    <div class="row">
      <el-tooltip class="box-item" effect="dark" placement="left-start">
        <template #content>
          Left Top
          <br />
          prompts info
        </template>
        <el-button>left-start</el-button>
      </el-tooltip>
      <el-tooltip class="box-item" effect="dark" placement="right-start">
        <template #content>
          Right Top
          <br />
          prompts info
        </template>
        <el-button>right-start</el-button>
      </el-tooltip>
    </div>
    <div class="row">
      <el-tooltip class="box-item" effect="dark" placement="left">
        <template #content>
          Left Center
          <br />
          prompts info
        </template>
        <el-button class="mt-3 mb-3">left</el-button>
      </el-tooltip>
      <el-tooltip class="box-item" effect="dark" placement="right">
        <template #content>
          Right Center
          <br />
          prompts info
        </template>
        <el-button>right</el-button>
      </el-tooltip>
    </div>
    <div class="row">
      <el-tooltip class="box-item" effect="dark" placement="left-end">
        <template #content>
          Left Bottom
          <br />
          prompts info
        </template>
        <el-button>left-end</el-button>
      </el-tooltip>
      <el-tooltip class="box-item" effect="dark" placement="right-end">
        <template #content>
          Right Bottom
          <br />
          prompts info
        </template>
        <el-button>right-end</el-button>
      </el-tooltip>
    </div>
    <div class="row center">
      <el-tooltip
        class="box-item"
        effect="dark"
        content="Bottom Left prompts info"
        placement="bottom-start"
      >
        <el-button>bottom-start</el-button>
      </el-tooltip>
      <el-tooltip
        class="box-item"
        effect="dark"
        content="Bottom Center prompts info"
        placement="bottom"
      >
        <el-button>bottom</el-button>
      </el-tooltip>
      <el-tooltip
        class="box-item"
        effect="dark"
        content="Bottom Right prompts info"
        placement="bottom-end"
      >
        <el-button>bottom-end</el-button>
      </el-tooltip>
    </div>
  </div>
</template>

<style>
.tooltip-base-box {
  width: 600px;
}
.tooltip-base-box .row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.tooltip-base-box .center {
  justify-content: center;
}
.tooltip-base-box .box-item {
  width: 110px;
  margin-top: 10px;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <el-tooltip content="Top center" placement="top">
    <el-button>Dark</el-button>
  </el-tooltip>
  <el-tooltip content="Bottom center" placement="bottom" effect="light">
    <el-button>Light</el-button>
  </el-tooltip>

  <el-tooltip content="Bottom center" effect="customized">
    <el-button>Customized theme</el-button>
  </el-tooltip>
</template>

<style>
.el-popper.is-customized {
  /* Set padding to ensure the height is 32px */
  padding: 6px 12px;
  background: linear-gradient(90deg, rgb(159, 229, 151), rgb(204, 229, 129));
}

.el-popper.is-customized .el-popper__arrow::before {
  background: linear-gradient(45deg, #b2e68d, #bce689);
  right: 0;
}
</style>
```

Example 3 (jsx):
```jsx
<template>
  <el-tooltip placement="top">
    <template #content> multiple lines<br />second line </template>
    <el-button>Top center</el-button>
  </el-tooltip>
</template>
```

Example 4 (vue):
```vue
<template>
  <el-tooltip
    :disabled="disabled"
    content="click to close tooltip function"
    placement="bottom"
    effect="light"
  >
    <el-button @click="disabled = !disabled">
      click to {{ disabled ? 'active' : 'close' }} tooltip function
    </el-button>
  </el-tooltip>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const disabled = ref(false)
</script>
```

---
