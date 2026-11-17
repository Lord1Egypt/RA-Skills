## MessageBox 消息弹框 ​

**URL:** https://element-plus.org/zh-CN/component/message-box

**Contents:**
- MessageBox 消息弹框 ​
- 消息提示 ​
- 确认消息 ​
- 提交内容 ​
- 使用 VNode ​
- 使用带有事件处理函数的 VNode 2.14.0 ​
- 个性化 ​
- 使用 HTML 片段 ​
- 区分取消操作与关闭操作 ​
- 内容居中 ​

模拟系统的消息提示框而实现的一套模态对话框组件，用于消息提示、确认消息和提交内容。

从设计上来说，MessageBox 的作用是美化系统自带的 alert、confirm 和 prompt，因此适合展示较为简单的内容。 如果需要弹出较为复杂的内容，请使用 Dialog。

当用户进行操作时会被触发，该对话框中断用户操作，直到用户确认知晓后才可关闭。

调用 ElMessageBox.alert 方法以打开 alert 框。 它模拟了系统的 alert，无法通过按下 ESC 或点击框外关闭。 此例中接收了两个参数，message和title。 值得一提的是，窗口被关闭后，它默认会返回一个Promise对象便于进行后续操作的处理。 若不确定浏览器是否支持Promise，可自行引入第三方 polyfill 或像本例一样使用回调进行后续处理。

提示用户确认其已经触发的动作，并询问是否进行此操作时会用到此对话框。

调用 ElMessageBox.confirm 方法以打开 confirm 框。它模拟了系统的 confirm。 Message Box 组件也拥有极高的定制性，我们可以传入 options 作为第三个参数，它是一个字面量对象。 type 字段表明消息类型，可以为success，error，info和 warning 需要注意的是，第二个参数 title 必须定义为 String 类型，如果是 Object，会被当做为 options使用。 在这里我们返回了一个 Promise 来处理后续响应。 primary 已被添加到2.9.11。

当需要用户输入内容时，可以使用 Prompt 类型的消息框。

调用 ElMessageBox.prompt 方法以打开 prompt 框。它模拟了系统的 prompt。 可以用 inputPattern 字段自己规定匹配模式， 使用 inputValidator 来指定验证方法，它应该返回 Boolean 或 String。 返回 false 或 String 表示验证失败， 返回的字符串将用作 inputErrorMessage，用来提示用户错误原因。 此外，可以用 inputPlaceholder 字段来定义输入框的占位符。

在 message 中可以接收 { confirm, cancel, close } 作为参数，使自定义内容能够以编程方式触发相同的 MessageBox 操作，并自动关闭实例。

上面提到的三个方法都是对 ElMessageBox 方法的二次包装。 本例直接调用 ElMessageBox 方法，使用了 showCancelButton 字段，用于显示取消按钮。 另外可使用 cancelButtonClass 为其添加自定义样式，使用 cancelButtonText 来自定义取消按钮文本（Confirm 按钮也具有相同的字段，在文末的 API 说明中有完整的字段列表）。 此例还使用了 beforeClose 属性， 当 beforeClose 被赋值且被赋值为一个回调函数时，在消息弹框被关闭之前将会被调用，并且可以通过该方法来阻止弹框被关闭。 它是一个接收三个参数：action、instance 和done 的方法。 使用它能够在关闭前对实例进行一些操作，比如为确定按钮添加 loading 状态等；此时若需要关闭实例，可以调用 done 方法（若在 beforeClose 中没有调用 done，则弹框便不会关闭）。

message 支持传入 HTML 字符串来作为正文内容。

将 dangerouslyUseHTMLString 属性设置为 true，message 属性就会被当作 HTML 片段处理。

message 属性虽然支持传入 HTML 片段，但是在网站上动态渲染任意 HTML 是非常危险的，因为容易导致 XSS 攻击。 因此在 dangerouslyUseHTMLString 打开的情况下，请确保 message 的内容是可信的，永远不要将用户提交的内容赋值给 message 属性。

有些场景下，点击取消按钮与点击关闭按钮有着不同的含义。

默认情况下，当用户触发取消（点击取消按钮）和触发关闭（点击关闭按钮或遮罩层、按下 ESC 键）时，Promise 的 reject 回调和 callback 回调的参数均为 'cancel'。 如果将distinguishCancelAndClose属性设置为 true，则上述两种行为的参数分别为 'cancel' 和 'close'。

将 center 属性设置为 true 可将内容居中显示。

图标可以使用任意Vue 组件或 渲染函数 (JSX)来自定义。

设置draggable属性为true来开启拖拽弹窗能力。 设置 overflow 2.5.4 为 true 可以让拖拽范围超出可视区。

如果你完整引入了 Element，它会为 app.config.globalProperties 添加如下全局方法：$msgbox、 $alert、 $confirm 和 $prompt。 因此在 Vue 实例中可以采用本页面中的方式来调用MessageBox。 参数如下：

现在，消息框构造函数支持将 context 作为第二个参数（如果你使用的是消息框变体，则为第四个参数），这样你就可以向消息中注入当前应用的上下文，从而继承应用中的所有属性。

如果您需要按需引入 MessageBox：

那么对应于上述四个全局方法的调用方法依次为：ElMessageBox、ElMessageBox.alert、ElMessageBox.confirm 和 ElMessageBox.prompt。 参数同上所述。

**Examples:**

Example 1 (jsx):
```jsx
<template>
  <el-button plain @click="open">Click to open the Message Box</el-button>
</template>

<script lang="ts" setup>
import { ElMessage, ElMessageBox } from 'element-plus'

import type { Action } from 'element-plus'

const open = () => {
  ElMessageBox.alert('This is a message', 'Title', {
    // if you want to disable its autofocus
    // autofocus: false,
    confirmButtonText: 'OK',
    callback: (action: Action) => {
      ElMessage({
        type: 'info',
        message: `action: ${action}`,
      })
    },
  })
}
</script>
```

Example 2 (javascript):
```javascript
<template>
  <el-button plain @click="open">Click to open the Message Box</el-button>
</template>

<script lang="ts" setup>
import { ElMessage, ElMessageBox } from 'element-plus'

const open = () => {
  ElMessageBox.confirm(
    'proxy will permanently delete the file. Continue?',
    'Warning',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  )
    .then(() => {
      ElMessage({
        type: 'success',
        message: 'Delete completed',
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: 'Delete canceled',
      })
    })
}
</script>
```

Example 3 (javascript):
```javascript
<template>
  <el-button plain @click="open">Click to open Message Box</el-button>
</template>

<script lang="ts" setup>
import { ElMessage, ElMessageBox } from 'element-plus'

const open = () => {
  ElMessageBox.prompt('Please input your e-mail', 'Tip', {
    confirmButtonText: 'OK',
    cancelButtonText: 'Cancel',
    inputPattern:
      /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
    inputErrorMessage: 'Invalid Email',
  })
    .then(({ value }) => {
      ElMessage({
        type: 'success',
        message: `Your email is:${value}`,
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: 'Input canceled',
      })
    })
}
</script>
```

Example 4 (jsx):
```jsx
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" plain @click="open">Common VNode</el-button>
    <el-button class="!ml-0" plain @click="open1">Dynamic props</el-button>
  </div>
</template>

<script lang="ts" setup>
import { h, ref } from 'vue'
import { ElMessageBox, ElSwitch } from 'element-plus'

const open = () => {
  ElMessageBox({
    title: 'Message',
    message: h('p', null, [
      h('span', null, 'Message can be '),
      h('i', { style: 'color: teal' }, 'VNode'),
    ]),
  })
}

const open1 = () => {
  const checked = ref<boolean | string | number>(false)
  ElMessageBox({
    title: 'Message',
    // Should pass a function if VNode contains dynamic props
    message: () =>
      h(ElSwitch, {
        modelValue: checked.value,
        'onUpdate:modelValue': (val: boolean | string | number) => {
          checked.value = val
        },
      }),
  })
}
</script>
```

---
