## Input 输入框 ​

**URL:** https://element-plus.org/zh-CN/component/input

**Contents:**
- Input 输入框 ​
- 基础用法 ​
- 禁用状态 ​
- 一键清空 ​
- 自定义清除图标2.11.0 ​
- 格式化 ​
- 密码框 ​
- 带图标的输入框 ​
- 文本域 ​
- 自适应文本域 ​

通过 disabled 属性指定是否禁用 input 组件

使用clearable属性即可得到一个可一键清空的输入框 在版本 2.13.4 之后，Input 的 textarea 类型也支持 clearable 功能。

你可以通过clear-icon属性自定义清除图标

在 formatter的情况下显示值，我们通常同时使用 parser

使用 show-password 属性即可得到一个可切换显示隐藏的密码框 自 2.13.6 起，支持使用 password-icon 插槽覆盖默认图标。

要在输入框中添加图标，你可以简单地使用 prefix-icon 和 suffix-icon 属性。 另外， prefix 和 suffix 命名的插槽也能正常工作。

用于输入多行文本信息可缩放的输入框。 添加 type="textarea" 属性来将 input 元素转换为原生的 textarea 元素。

设置文字输入类型的 autosize 属性使得根据内容自动调整的高度。 你可以给 autosize 提供一个包含有最大和最小高度的对象，让输入框自动调整。

可以在输入框中前置或后置一个元素，通常是标签或按钮。

可通过 slot 来指定在 Input 中分发的前置或者后置的内容。

使用 size 属性改变输入框大小。 除了默认大小外，还有另外两个选项： large, small。

使用 maxlength 和 minlength 属性, 来控制输入内容的最大字数和最小字数。 "字符数"使用JavaScript字符串长度来衡量。 为文本或文本输入类型设置 maxlength prop可以限制输入值的长度。 允许你通过设置 show-word-limit 到 true 来显示剩余字数。 从 2.11.5 版本开始，你可以将 word-limit-position 设置为 outside，以在输入框外显示字数统计。

设置 count-graphemes 以计算文本长度。 如果设置了该属性，则不会使用原生的 maxlength 和 minlength。

当使用 count-graphemes prop时，组件使用以下方法：

主要: 使用 Intl.Segmenter API (Chrome 87+, Firefox 125+, Safari 14.1+) 进行适当的图形集群处理。 它能够正确处理复杂的表情符号、组合标记和0宽度连接符序列。

回退: 旧版浏览器会回退到 Array.from() 进行基于码点的迭代。 请注意，这可能会拆分多码点字形序列（例如，带有肤色修饰符的表情符号）。

在实现自己的 count-graphemes 函数时，如果需要对复杂的 unicode 字符提供强大的支持，请考虑使用 Intl.Segmenter。

PS: 由于ElInput 组件没有默认宽度，当显示 clearable 图标时, 组件的宽度将被撑开，可以通过设置固定宽度属性来解决。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-input v-model="input" style="width: 240px" placeholder="Please input" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref('')
</script>
```

Example 2 (vue):
```vue
<template>
  <el-input
    v-model="input"
    style="width: 240px"
    disabled
    placeholder="Please input"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref('')
</script>
```

Example 3 (vue):
```vue
<template>
  <div class="input-group">
    <el-input
      v-model="input"
      style="width: 240px"
      placeholder="Please input"
      clearable
    />
    <el-input
      v-model="textareaInput"
      style="width: 240px"
      placeholder="Please input"
      type="textarea"
      clearable
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const input = ref('')
const textareaInput = ref('')
</script>

<style scoped>
.input-group {
  display: flex;
  align-items: center;
  gap: 1em;
}
</style>
```

Example 4 (vue):
```vue
<template>
  <div class="input-group">
    <el-input
      v-model="input"
      clearable
      :clear-icon="CloseBold"
      placeholder="Custom clear icon"
    />
    <el-input
      v-model="textareaInput"
      clearable
      :clear-icon="CloseBold"
      placeholder="Custom clear icon"
      type="textarea"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CloseBold } from '@element-plus/icons-vue'

const input = ref('Custom clear icon')
const textareaInput = ref('Custom clear icon')
</script>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  gap: 1em;
}
</style>
```

---
