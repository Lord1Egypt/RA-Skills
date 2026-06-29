---
name: "message-box"
description: "Message Box 消息弹出框 -- Element Plus Vue3 桌面端组件。Invoke when user needs Message Box 消息弹出框 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/message-box.html"
---

---

# MessageBox 消息弹框 [​](#messagebox-消息弹框)

更新日志待解决

13

模拟系统的消息提示框而实现的一套模态对话框组件，用于消息提示、确认消息和提交内容。

TIP

从设计上来说，MessageBox 的作用是美化系统自带的 `alert`、`confirm` 和 `prompt`，因此适合展示较为简单的内容。 如果需要弹出较为复杂的内容，请使用 Dialog。

## 消息提示 [​](#消息提示)

当用户进行操作时会被触发，该对话框中断用户操作，直到用户确认知晓后才可关闭。

调用 `ElMessageBox.alert` 方法以打开 alert 框。 它模拟了系统的 `alert`，无法通过按下 ESC 或点击框外关闭。 此例中接收了两个参数，`message`和`title`。 值得一提的是，窗口被关闭后，它默认会返回一个`Promise`对象便于进行后续操作的处理。 若不确定浏览器是否支持`Promise`，可自行引入第三方 polyfill 或像本例一样使用回调进行后续处理。

Click to open the Message Box

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj5DbGljayB0byBvcGVuIHRoZSBNZXNzYWdlIEJveDwvZWwtYnV0dG9uPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEVsTWVzc2FnZSwgRWxNZXNzYWdlQm94IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5pbXBvcnQgdHlwZSB7IEFjdGlvbiB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3Qgb3BlbiA9ICgpID0+IHtcbiAgRWxNZXNzYWdlQm94LmFsZXJ0KCdUaGlzIGlzIGEgbWVzc2FnZScsICdUaXRsZScsIHtcbiAgICAvLyBpZiB5b3Ugd2FudCB0byBkaXNhYmxlIGl0cyBhdXRvZm9jdXNcbiAgICAvLyBhdXRvZm9jdXM6IGZhbHNlLFxuICAgIGNvbmZpcm1CdXR0b25UZXh0OiAnT0snLFxuICAgIGNhbGxiYWNrOiAoYWN0aW9uOiBBY3Rpb24pID0+IHtcbiAgICAgIEVsTWVzc2FnZSh7XG4gICAgICAgIHR5cGU6ICdpbmZvJyxcbiAgICAgICAgbWVzc2FnZTogYGFjdGlvbjogJHthY3Rpb259YCxcbiAgICAgIH0pXG4gICAgfSxcbiAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/alert.vue)_

vue

```
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

隐藏源代码

## 确认消息 [​](#确认消息)

提示用户确认其已经触发的动作，并询问是否进行此操作时会用到此对话框。

调用 `ElMessageBox.confirm` 方法以打开 confirm 框。它模拟了系统的 `confirm`。 Message Box 组件也拥有极高的定制性，我们可以传入 `options` 作为第三个参数，它是一个字面量对象。 `type` 字段表明消息类型，可以为`success`，`error`，`info`和 `warning` 需要注意的是，第二个参数 `title` 必须定义为 `String` 类型，如果是 `Object`，会被当做为 `options`使用。 在这里我们返回了一个 `Promise` 来处理后续响应。 `primary` 已被添加到2.9.11。

Click to open the Message Box

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj5DbGljayB0byBvcGVuIHRoZSBNZXNzYWdlIEJveDwvZWwtYnV0dG9uPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEVsTWVzc2FnZSwgRWxNZXNzYWdlQm94IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuID0gKCkgPT4ge1xuICBFbE1lc3NhZ2VCb3guY29uZmlybShcbiAgICAncHJveHkgd2lsbCBwZXJtYW5lbnRseSBkZWxldGUgdGhlIGZpbGUuIENvbnRpbnVlPycsXG4gICAgJ1dhcm5pbmcnLFxuICAgIHtcbiAgICAgIGNvbmZpcm1CdXR0b25UZXh0OiAnT0snLFxuICAgICAgY2FuY2VsQnV0dG9uVGV4dDogJ0NhbmNlbCcsXG4gICAgICB0eXBlOiAnd2FybmluZycsXG4gICAgfVxuICApXG4gICAgLnRoZW4oKCkgPT4ge1xuICAgICAgRWxNZXNzYWdlKHtcbiAgICAgICAgdHlwZTogJ3N1Y2Nlc3MnLFxuICAgICAgICBtZXNzYWdlOiAnRGVsZXRlIGNvbXBsZXRlZCcsXG4gICAgICB9KVxuICAgIH0pXG4gICAgLmNhdGNoKCgpID0+IHtcbiAgICAgIEVsTWVzc2FnZSh7XG4gICAgICAgIHR5cGU6ICdpbmZvJyxcbiAgICAgICAgbWVzc2FnZTogJ0RlbGV0ZSBjYW5jZWxlZCcsXG4gICAgICB9KVxuICAgIH0pXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/confirm.vue)_

vue

```
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

隐藏源代码

## 提交内容 [​](#提交内容)

当需要用户输入内容时，可以使用 Prompt 类型的消息框。

调用 `ElMessageBox.prompt` 方法以打开 prompt 框。它模拟了系统的 `prompt`。 可以用 `inputPattern` 字段自己规定匹配模式， 使用 `inputValidator` 来指定验证方法，它应该返回 `Boolean` 或 `String`。 返回 `false` 或 `String` 表示验证失败， 返回的字符串将用作 `inputErrorMessage`，用来提示用户错误原因。 此外，可以用 `inputPlaceholder` 字段来定义输入框的占位符。

Click to open Message Box

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj5DbGljayB0byBvcGVuIE1lc3NhZ2UgQm94PC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxNZXNzYWdlLCBFbE1lc3NhZ2VCb3ggfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IG9wZW4gPSAoKSA9PiB7XG4gIEVsTWVzc2FnZUJveC5wcm9tcHQoJ1BsZWFzZSBpbnB1dCB5b3VyIGUtbWFpbCcsICdUaXAnLCB7XG4gICAgY29uZmlybUJ1dHRvblRleHQ6ICdPSycsXG4gICAgY2FuY2VsQnV0dG9uVGV4dDogJ0NhbmNlbCcsXG4gICAgaW5wdXRQYXR0ZXJuOlxuICAgICAgL1tcXHchIyQlJicqKy89P15fYHt8fX4tXSsoPzpcXC5bXFx3ISMkJSYnKisvPT9eX2B7fH1+LV0rKSpAKD86W1xcd10oPzpbXFx3LV0qW1xcd10pP1xcLikrW1xcd10oPzpbXFx3LV0qW1xcd10pPy8sXG4gICAgaW5wdXRFcnJvck1lc3NhZ2U6ICdJbnZhbGlkIEVtYWlsJyxcbiAgfSlcbiAgICAudGhlbigoeyB2YWx1ZSB9KSA9PiB7XG4gICAgICBFbE1lc3NhZ2Uoe1xuICAgICAgICB0eXBlOiAnc3VjY2VzcycsXG4gICAgICAgIG1lc3NhZ2U6IGBZb3VyIGVtYWlsIGlzOiR7dmFsdWV9YCxcbiAgICAgIH0pXG4gICAgfSlcbiAgICAuY2F0Y2goKCkgPT4ge1xuICAgICAgRWxNZXNzYWdlKHtcbiAgICAgICAgdHlwZTogJ2luZm8nLFxuICAgICAgICBtZXNzYWdlOiAnSW5wdXQgY2FuY2VsZWQnLFxuICAgICAgfSlcbiAgICB9KVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/prompt.vue)_

vue

```
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

隐藏源代码

## 使用 VNode [​](#使用-vnode)

`message` 可以是 VNode。

Common VNodeDynamic props

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuXCI+Q29tbW9uIFZOb2RlPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgcGxhaW4gQGNsaWNrPVwib3BlbjFcIj5EeW5hbWljIHByb3BzPC9lbC1idXR0b24+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGgsIHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsTWVzc2FnZUJveCwgRWxTd2l0Y2ggfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IG9wZW4gPSAoKSA9PiB7XG4gIEVsTWVzc2FnZUJveCh7XG4gICAgdGl0bGU6ICdNZXNzYWdlJyxcbiAgICBtZXNzYWdlOiBoKCdwJywgbnVsbCwgW1xuICAgICAgaCgnc3BhbicsIG51bGwsICdNZXNzYWdlIGNhbiBiZSAnKSxcbiAgICAgIGgoJ2knLCB7IHN0eWxlOiAnY29sb3I6IHRlYWwnIH0sICdWTm9kZScpLFxuICAgIF0pLFxuICB9KVxufVxuXG5jb25zdCBvcGVuMSA9ICgpID0+IHtcbiAgY29uc3QgY2hlY2tlZCA9IHJlZjxib29sZWFuIHwgc3RyaW5nIHwgbnVtYmVyPihmYWxzZSlcbiAgRWxNZXNzYWdlQm94KHtcbiAgICB0aXRsZTogJ01lc3NhZ2UnLFxuICAgIC8vIFNob3VsZCBwYXNzIGEgZnVuY3Rpb24gaWYgVk5vZGUgY29udGFpbnMgZHluYW1pYyBwcm9wc1xuICAgIG1lc3NhZ2U6ICgpID0+XG4gICAgICBoKEVsU3dpdGNoLCB7XG4gICAgICAgIG1vZGVsVmFsdWU6IGNoZWNrZWQudmFsdWUsXG4gICAgICAgICdvblVwZGF0ZTptb2RlbFZhbHVlJzogKHZhbDogYm9vbGVhbiB8IHN0cmluZyB8IG51bWJlcikgPT4ge1xuICAgICAgICAgIGNoZWNrZWQudmFsdWUgPSB2YWxcbiAgICAgICAgfSxcbiAgICAgIH0pLFxuICB9KVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/use-vnode.vue)_

vue

```
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

隐藏源代码

## 使用带有事件处理函数的 VNode 2.14.0 [​](#使用带有事件处理函数的-vnode)

在 `message` 中可以接收 `{ confirm, cancel, close }` 作为参数，使自定义内容能够以编程方式触发相同的 MessageBox 操作，并自动关闭实例。

Click to open Message Box

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj5DbGljayB0byBvcGVuIE1lc3NhZ2UgQm94PC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgaCB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsQnV0dG9uLCBFbE1lc3NhZ2UsIEVsTWVzc2FnZUJveCB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3Qgb3BlbiA9ICgpID0+IHtcbiAgRWxNZXNzYWdlQm94LmNvbmZpcm0oXG4gICAgKHsgY29uZmlybSwgY2FuY2VsLCBjbG9zZSB9KSA9PiB7XG4gICAgICByZXR1cm4gaCgnZGl2JywgW1xuICAgICAgICBoKFxuICAgICAgICAgICdwJyxcbiAgICAgICAgICB7IHN0eWxlOiAnbWFyZ2luLWJvdHRvbTogOHB4JyB9LFxuICAgICAgICAgICdDdXN0b20gYnV0dG9ucyB3aXRoIE1lc3NhZ2VCb3ggYWN0aW9uIGhhbmRsZXJzJ1xuICAgICAgICApLFxuICAgICAgICBoKFxuICAgICAgICAgIEVsQnV0dG9uLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHR5cGU6ICdwcmltYXJ5JyxcbiAgICAgICAgICAgIG9uQ2xpY2s6ICgpID0+IHtcbiAgICAgICAgICAgICAgY29uZmlybSgpXG4gICAgICAgICAgICB9LFxuICAgICAgICAgIH0sXG4gICAgICAgICAgKCkgPT4gJ1Jlc29sdmUnXG4gICAgICAgICksXG4gICAgICAgIGgoXG4gICAgICAgICAgRWxCdXR0b24sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdHlwZTogJ2RhbmdlcicsXG4gICAgICAgICAgICBvbkNsaWNrOiAoKSA9PiB7XG4gICAgICAgICAgICAgIGNhbmNlbCgpXG4gICAgICAgICAgICB9LFxuICAgICAgICAgIH0sXG4gICAgICAgICAgKCkgPT4gJ1JlamVjdCdcbiAgICAgICAgKSxcbiAgICAgICAgaChcbiAgICAgICAgICBFbEJ1dHRvbixcbiAgICAgICAgICB7XG4gICAgICAgICAgICBvbkNsaWNrOiAoKSA9PiB7XG4gICAgICAgICAgICAgIGNsb3NlKClcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgfSxcbiAgICAgICAgICAoKSA9PiAnQ2xvc2UnXG4gICAgICAgICksXG4gICAgICBdKVxuICAgIH0sXG4gICAge1xuICAgICAgdGl0bGU6ICdNZXNzYWdlJyxcbiAgICAgIHNob3dDb25maXJtQnV0dG9uOiBmYWxzZSxcbiAgICAgIHNob3dDYW5jZWxCdXR0b246IGZhbHNlLFxuICAgICAgZGlzdGluZ3Vpc2hDYW5jZWxBbmRDbG9zZTogdHJ1ZSxcbiAgICB9XG4gIClcbiAgICAudGhlbigoYWN0aW9uKSA9PiB7XG4gICAgICBFbE1lc3NhZ2Uoe1xuICAgICAgICB0eXBlOiAnc3VjY2VzcycsXG4gICAgICAgIG1lc3NhZ2U6IGByZXNvbHZlZDogJHthY3Rpb259YCxcbiAgICAgIH0pXG4gICAgfSlcbiAgICAuY2F0Y2goKHJlYXNvbikgPT4ge1xuICAgICAgRWxNZXNzYWdlKHtcbiAgICAgICAgdHlwZTogJ2Vycm9yJyxcbiAgICAgICAgbWVzc2FnZTogYHJlamVjdGVkOiAke3JlYXNvbn1gLFxuICAgICAgfSlcbiAgICB9KVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/use-vnode-with-action-handlers.vue)_

vue

```
<template>
  <el-button plain @click="open">Click to open Message Box</el-button>
</template>

<script lang="ts" setup>
import { h } from 'vue'
import { ElButton, ElMessage, ElMessageBox } from 'element-plus'

const open = () => {
  ElMessageBox.confirm(
    ({ confirm, cancel, close }) => {
      return h('div', [
        h(
          'p',
          { style: 'margin-bottom: 8px' },
          'Custom buttons with MessageBox action handlers'
        ),
        h(
          ElButton,
          {
            type: 'primary',
            onClick: () => {
              confirm()
            },
          },
          () => 'Resolve'
        ),
        h(
          ElButton,
          {
            type: 'danger',
            onClick: () => {
              cancel()
            },
          },
          () => 'Reject'
        ),
        h(
          ElButton,
          {
            onClick: () => {
              close()
            },
          },
          () => 'Close'
        ),
      ])
    },
    {
      title: 'Message',
      showConfirmButton: false,
      showCancelButton: false,
      distinguishCancelAndClose: true,
    }
  )
    .then((action) => {
      ElMessage({
        type: 'success',
        message: `resolved: ${action}`,
      })
    })
    .catch((reason) => {
      ElMessage({
        type: 'error',
        message: `rejected: ${reason}`,
      })
    })
}
</script>
```

隐藏源代码

## 个性化 [​](#个性化)

消息弹框可以被定制来展示各种内容。

上面提到的三个方法都是对 `ElMessageBox` 方法的二次包装。 本例直接调用 `ElMessageBox` 方法，使用了 `showCancelButton` 字段，用于显示取消按钮。 另外可使用 `cancelButtonClass` 为其添加自定义样式，使用 `cancelButtonText` 来自定义取消按钮文本（Confirm 按钮也具有相同的字段，在文末的 API 说明中有完整的字段列表）。 此例还使用了 `beforeClose` 属性， 当 beforeClose 被赋值且被赋值为一个回调函数时，在消息弹框被关闭之前将会被调用，并且可以通过该方法来阻止弹框被关闭。 它是一个接收三个参数：`action`、`instance` 和`done` 的方法。 使用它能够在关闭前对实例进行一些操作，比如为确定按钮添加 `loading` 状态等；此时若需要关闭实例，可以调用 `done` 方法（若在 `beforeClose` 中没有调用 `done`，则弹框便不会关闭）。

Click to open Message Box

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj5DbGljayB0byBvcGVuIE1lc3NhZ2UgQm94PC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgaCB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsTWVzc2FnZSwgRWxNZXNzYWdlQm94IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuID0gKCkgPT4ge1xuICBFbE1lc3NhZ2VCb3goe1xuICAgIHRpdGxlOiAnTWVzc2FnZScsXG4gICAgbWVzc2FnZTogaCgncCcsIG51bGwsIFtcbiAgICAgIGgoJ3NwYW4nLCBudWxsLCAnTWVzc2FnZSBjYW4gYmUgJyksXG4gICAgICBoKCdpJywgeyBzdHlsZTogJ2NvbG9yOiB0ZWFsJyB9LCAnVk5vZGUnKSxcbiAgICBdKSxcbiAgICBzaG93Q2FuY2VsQnV0dG9uOiB0cnVlLFxuICAgIGNvbmZpcm1CdXR0b25UZXh0OiAnT0snLFxuICAgIGNhbmNlbEJ1dHRvblRleHQ6ICdDYW5jZWwnLFxuICAgIGJlZm9yZUNsb3NlOiAoYWN0aW9uLCBpbnN0YW5jZSwgZG9uZSkgPT4ge1xuICAgICAgaWYgKGFjdGlvbiA9PT0gJ2NvbmZpcm0nKSB7XG4gICAgICAgIGluc3RhbmNlLmNvbmZpcm1CdXR0b25Mb2FkaW5nID0gdHJ1ZVxuICAgICAgICBpbnN0YW5jZS5jb25maXJtQnV0dG9uVGV4dCA9ICdMb2FkaW5nLi4uJ1xuICAgICAgICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgICBkb25lKClcbiAgICAgICAgICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgICAgIGluc3RhbmNlLmNvbmZpcm1CdXR0b25Mb2FkaW5nID0gZmFsc2VcbiAgICAgICAgICB9LCAzMDApXG4gICAgICAgIH0sIDMwMDApXG4gICAgICB9IGVsc2Uge1xuICAgICAgICBkb25lKClcbiAgICAgIH1cbiAgICB9LFxuICB9KS50aGVuKChhY3Rpb24pID0+IHtcbiAgICBFbE1lc3NhZ2Uoe1xuICAgICAgdHlwZTogJ2luZm8nLFxuICAgICAgbWVzc2FnZTogYGFjdGlvbjogJHthY3Rpb259YCxcbiAgICB9KVxuICB9KVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/customization.vue)_

vue

```
<template>
  <el-button plain @click="open">Click to open Message Box</el-button>
</template>

<script lang="ts" setup>
import { h } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const open = () => {
  ElMessageBox({
    title: 'Message',
    message: h('p', null, [
      h('span', null, 'Message can be '),
      h('i', { style: 'color: teal' }, 'VNode'),
    ]),
    showCancelButton: true,
    confirmButtonText: 'OK',
    cancelButtonText: 'Cancel',
    beforeClose: (action, instance, done) => {
      if (action === 'confirm') {
        instance.confirmButtonLoading = true
        instance.confirmButtonText = 'Loading...'
        setTimeout(() => {
          done()
          setTimeout(() => {
            instance.confirmButtonLoading = false
          }, 300)
        }, 3000)
      } else {
        done()
      }
    },
  }).then((action) => {
    ElMessage({
      type: 'info',
      message: `action: ${action}`,
    })
  })
}
</script>
```

隐藏源代码

## 使用 HTML 片段 [​](#使用-html-片段)

`message` 支持传入 HTML 字符串来作为正文内容。

将 `dangerouslyUseHTMLString` 属性设置为 true，`message` 属性就会被当作 HTML 片段处理。

Click to open Message Box

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj5DbGljayB0byBvcGVuIE1lc3NhZ2UgQm94PC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxNZXNzYWdlQm94IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuID0gKCkgPT4ge1xuICBFbE1lc3NhZ2VCb3guYWxlcnQoXG4gICAgJzxzdHJvbmc+cHJveHkgaXMgPGk+SFRNTDwvaT4gc3RyaW5nPC9zdHJvbmc+JyxcbiAgICAnSFRNTCBTdHJpbmcnLFxuICAgIHtcbiAgICAgIGRhbmdlcm91c2x5VXNlSFRNTFN0cmluZzogdHJ1ZSxcbiAgICB9XG4gIClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/use-html.vue)_

vue

```
<template>
  <el-button plain @click="open">Click to open Message Box</el-button>
</template>

<script lang="ts" setup>
import { ElMessageBox } from 'element-plus'

const open = () => {
  ElMessageBox.alert(
    '<strong>proxy is <i>HTML</i> string</strong>',
    'HTML String',
    {
      dangerouslyUseHTMLString: true,
    }
  )
}
</script>
```

隐藏源代码

WARNING

`message` 属性虽然支持传入 HTML 片段，但是在网站上动态渲染任意 HTML 是非常危险的，因为容易导致 [XSS 攻击](https://en.wikipedia.org/wiki/Cross-site_scripting)。 因此在 `dangerouslyUseHTMLString` 打开的情况下，请确保 `message` 的内容是可信的，**永远不要**将用户提交的内容赋值给 `message` 属性。

## 区分取消操作与关闭操作 [​](#区分取消操作与关闭操作)

有些场景下，点击取消按钮与点击关闭按钮有着不同的含义。

默认情况下，当用户触发取消（点击取消按钮）和触发关闭（点击关闭按钮或遮罩层、按下 ESC 键）时，Promise 的 reject 回调和 `callback` 回调的参数均为 'cancel'。 如果将`distinguishCancelAndClose`属性设置为 true，则上述两种行为的参数分别为 'cancel' 和 'close'。

Click to open Message Box

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj5DbGljayB0byBvcGVuIE1lc3NhZ2UgQm94PC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxNZXNzYWdlLCBFbE1lc3NhZ2VCb3ggfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmltcG9ydCB0eXBlIHsgQWN0aW9uIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBvcGVuID0gKCkgPT4ge1xuICBFbE1lc3NhZ2VCb3guY29uZmlybShcbiAgICAnWW91IGhhdmUgdW5zYXZlZCBjaGFuZ2VzLCBzYXZlIGFuZCBwcm9jZWVkPycsXG4gICAgJ0NvbmZpcm0nLFxuICAgIHtcbiAgICAgIGRpc3Rpbmd1aXNoQ2FuY2VsQW5kQ2xvc2U6IHRydWUsXG4gICAgICBjb25maXJtQnV0dG9uVGV4dDogJ1NhdmUnLFxuICAgICAgY2FuY2VsQnV0dG9uVGV4dDogJ0Rpc2NhcmQgQ2hhbmdlcycsXG4gICAgfVxuICApXG4gICAgLnRoZW4oKCkgPT4ge1xuICAgICAgRWxNZXNzYWdlKHtcbiAgICAgICAgdHlwZTogJ2luZm8nLFxuICAgICAgICBtZXNzYWdlOiAnQ2hhbmdlcyBzYXZlZC4gUHJvY2VlZGluZyB0byBhIG5ldyByb3V0ZS4nLFxuICAgICAgfSlcbiAgICB9KVxuICAgIC5jYXRjaCgoYWN0aW9uOiBBY3Rpb24pID0+IHtcbiAgICAgIEVsTWVzc2FnZSh7XG4gICAgICAgIHR5cGU6ICdpbmZvJyxcbiAgICAgICAgbWVzc2FnZTpcbiAgICAgICAgICBhY3Rpb24gPT09ICdjYW5jZWwnXG4gICAgICAgICAgICA/ICdDaGFuZ2VzIGRpc2NhcmRlZC4gUHJvY2VlZGluZyB0byBhIG5ldyByb3V0ZS4nXG4gICAgICAgICAgICA6ICdTdGF5IGluIHRoZSBjdXJyZW50IHJvdXRlJyxcbiAgICAgIH0pXG4gICAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/distinguishable-close-cancel.vue)_

vue

```
<template>
  <el-button plain @click="open">Click to open Message Box</el-button>
</template>

<script lang="ts" setup>
import { ElMessage, ElMessageBox } from 'element-plus'

import type { Action } from 'element-plus'

const open = () => {
  ElMessageBox.confirm(
    'You have unsaved changes, save and proceed?',
    'Confirm',
    {
      distinguishCancelAndClose: true,
      confirmButtonText: 'Save',
      cancelButtonText: 'Discard Changes',
    }
  )
    .then(() => {
      ElMessage({
        type: 'info',
        message: 'Changes saved. Proceeding to a new route.',
      })
    })
    .catch((action: Action) => {
      ElMessage({
        type: 'info',
        message:
          action === 'cancel'
            ? 'Changes discarded. Proceeding to a new route.'
            : 'Stay in the current route',
      })
    })
}
</script>
```

隐藏源代码

## 内容居中 [​](#内容居中)

消息弹框支持使用居中布局。

将 `center` 属性设置为 `true` 可将内容居中显示。

Click to open Message Box

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj5DbGljayB0byBvcGVuIE1lc3NhZ2UgQm94PC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgRWxNZXNzYWdlLCBFbE1lc3NhZ2VCb3ggfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IG9wZW4gPSAoKSA9PiB7XG4gIEVsTWVzc2FnZUJveC5jb25maXJtKFxuICAgICdwcm94eSB3aWxsIHBlcm1hbmVudGx5IGRlbGV0ZSB0aGUgZmlsZS4gQ29udGludWU/JyxcbiAgICAnV2FybmluZycsXG4gICAge1xuICAgICAgY29uZmlybUJ1dHRvblRleHQ6ICdPSycsXG4gICAgICBjYW5jZWxCdXR0b25UZXh0OiAnQ2FuY2VsJyxcbiAgICAgIHR5cGU6ICd3YXJuaW5nJyxcbiAgICAgIGNlbnRlcjogdHJ1ZSxcbiAgICB9XG4gIClcbiAgICAudGhlbigoKSA9PiB7XG4gICAgICBFbE1lc3NhZ2Uoe1xuICAgICAgICB0eXBlOiAnc3VjY2VzcycsXG4gICAgICAgIG1lc3NhZ2U6ICdEZWxldGUgY29tcGxldGVkJyxcbiAgICAgIH0pXG4gICAgfSlcbiAgICAuY2F0Y2goKCkgPT4ge1xuICAgICAgRWxNZXNzYWdlKHtcbiAgICAgICAgdHlwZTogJ2luZm8nLFxuICAgICAgICBtZXNzYWdlOiAnRGVsZXRlIGNhbmNlbGVkJyxcbiAgICAgIH0pXG4gICAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/centered-content.vue)_

vue

```
<template>
  <el-button plain @click="open">Click to open Message Box</el-button>
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
      center: true,
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

隐藏源代码

## 自定义图标 [​](#自定义图标)

图标可以使用任意Vue 组件或 [渲染函数 (JSX)](https://vuejs.org/guide/extras/render-function.html)来自定义。

Click to open Message Box

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uIHBsYWluIEBjbGljaz1cIm9wZW5cIj5DbGljayB0byBvcGVuIE1lc3NhZ2UgQm94PC9lbC1idXR0b24+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgbWFya1JhdyB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IEVsTWVzc2FnZSwgRWxNZXNzYWdlQm94IH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuaW1wb3J0IHsgRGVsZXRlIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IG9wZW4gPSAoKSA9PiB7XG4gIEVsTWVzc2FnZUJveC5jb25maXJtKFxuICAgICdJdCB3aWxsIHBlcm1hbmVudGx5IGRlbGV0ZSB0aGUgZmlsZS4gQ29udGludWU/JyxcbiAgICAnV2FybmluZycsXG4gICAge1xuICAgICAgY29uZmlybUJ1dHRvblRleHQ6ICdPSycsXG4gICAgICBjYW5jZWxCdXR0b25UZXh0OiAnQ2FuY2VsJyxcbiAgICAgIHR5cGU6ICd3YXJuaW5nJyxcbiAgICAgIGljb246IG1hcmtSYXcoRGVsZXRlKSxcbiAgICB9XG4gIClcbiAgICAudGhlbigoKSA9PiB7XG4gICAgICBFbE1lc3NhZ2Uoe1xuICAgICAgICB0eXBlOiAnc3VjY2VzcycsXG4gICAgICAgIG1lc3NhZ2U6ICdEZWxldGUgY29tcGxldGVkJyxcbiAgICAgIH0pXG4gICAgfSlcbiAgICAuY2F0Y2goKCkgPT4ge1xuICAgICAgRWxNZXNzYWdlKHtcbiAgICAgICAgdHlwZTogJ2luZm8nLFxuICAgICAgICBtZXNzYWdlOiAnRGVsZXRlIGNhbmNlbGVkJyxcbiAgICAgIH0pXG4gICAgfSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/customized-icon.vue)_

vue

```
<template>
  <el-button plain @click="open">Click to open Message Box</el-button>
</template>

<script lang="ts" setup>
import { markRaw } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'

const open = () => {
  ElMessageBox.confirm(
    'It will permanently delete the file. Continue?',
    'Warning',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
      icon: markRaw(Delete),
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

隐藏源代码

## 可拖放 [​](#可拖放)

设置 MessageBox 可以拖拽。

设置`draggable`属性为`true`来开启拖拽弹窗能力。 设置 `overflow` 2.5.4 为 `true` 可以让拖拽范围超出可视区。

Open a draggable Message Box Open a overflow draggable Message Box Open a custom dragging style Message Box

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTFcIj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuXCI+XG4gICAgICBPcGVuIGEgZHJhZ2dhYmxlIE1lc3NhZ2UgQm94XG4gICAgPC9lbC1idXR0b24+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIiFtbC0wXCIgcGxhaW4gQGNsaWNrPVwib3BlbjJcIj5cbiAgICAgIE9wZW4gYSBvdmVyZmxvdyBkcmFnZ2FibGUgTWVzc2FnZSBCb3hcbiAgICA8L2VsLWJ1dHRvbj5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwiIW1sLTBcIiBwbGFpbiBAY2xpY2s9XCJvcGVuM1wiPlxuICAgICAgT3BlbiBhIGN1c3RvbSBkcmFnZ2luZyBzdHlsZSBNZXNzYWdlIEJveFxuICAgIDwvZWwtYnV0dG9uPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBFbE1lc3NhZ2UsIEVsTWVzc2FnZUJveCB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3Qgb3BlbiA9ICgpID0+IHtcbiAgRWxNZXNzYWdlQm94LmNvbmZpcm0oXG4gICAgJ3Byb3h5IHdpbGwgcGVybWFuZW50bHkgZGVsZXRlIHRoZSBmaWxlLiBDb250aW51ZT8nLFxuICAgICdXYXJuaW5nJyxcbiAgICB7XG4gICAgICBjb25maXJtQnV0dG9uVGV4dDogJ09LJyxcbiAgICAgIGNhbmNlbEJ1dHRvblRleHQ6ICdDYW5jZWwnLFxuICAgICAgdHlwZTogJ3dhcm5pbmcnLFxuICAgICAgZHJhZ2dhYmxlOiB0cnVlLFxuICAgIH1cbiAgKVxuICAgIC50aGVuKCgpID0+IHtcbiAgICAgIEVsTWVzc2FnZSh7XG4gICAgICAgIHR5cGU6ICdzdWNjZXNzJyxcbiAgICAgICAgbWVzc2FnZTogJ0RlbGV0ZSBjb21wbGV0ZWQnLFxuICAgICAgfSlcbiAgICB9KVxuICAgIC5jYXRjaCgoKSA9PiB7XG4gICAgICBFbE1lc3NhZ2Uoe1xuICAgICAgICB0eXBlOiAnaW5mbycsXG4gICAgICAgIG1lc3NhZ2U6ICdEZWxldGUgY2FuY2VsZWQnLFxuICAgICAgfSlcbiAgICB9KVxufVxuXG5jb25zdCBvcGVuMiA9ICgpID0+IHtcbiAgRWxNZXNzYWdlQm94LmNvbmZpcm0oXG4gICAgJ3Byb3h5IHdpbGwgcGVybWFuZW50bHkgZGVsZXRlIHRoZSBmaWxlLiBDb250aW51ZT8nLFxuICAgICdXYXJuaW5nJyxcbiAgICB7XG4gICAgICBjb25maXJtQnV0dG9uVGV4dDogJ09LJyxcbiAgICAgIGNhbmNlbEJ1dHRvblRleHQ6ICdDYW5jZWwnLFxuICAgICAgdHlwZTogJ3dhcm5pbmcnLFxuICAgICAgZHJhZ2dhYmxlOiB0cnVlLFxuICAgICAgb3ZlcmZsb3c6IHRydWUsXG4gICAgfVxuICApXG4gICAgLnRoZW4oKCkgPT4ge1xuICAgICAgRWxNZXNzYWdlKHtcbiAgICAgICAgdHlwZTogJ3N1Y2Nlc3MnLFxuICAgICAgICBtZXNzYWdlOiAnRGVsZXRlIGNvbXBsZXRlZCcsXG4gICAgICB9KVxuICAgIH0pXG4gICAgLmNhdGNoKCgpID0+IHtcbiAgICAgIEVsTWVzc2FnZSh7XG4gICAgICAgIHR5cGU6ICdpbmZvJyxcbiAgICAgICAgbWVzc2FnZTogJ0RlbGV0ZSBjYW5jZWxlZCcsXG4gICAgICB9KVxuICAgIH0pXG59XG5cbmNvbnN0IG9wZW4zID0gKCkgPT4ge1xuICBFbE1lc3NhZ2VCb3guY29uZmlybShcbiAgICAnVGhpcyBtZXNzYWdlIGJveCBoYXMgY3VzdG9tIGRyYWdnaW5nIHN0eWxlcy4gVHJ5IGRyYWdnaW5nIGl0IHRvIHNlZSB0aGUgZWZmZWN0cyEnLFxuICAgICdDdXN0b20gRHJhZ2dpbmcgU3R5bGUnLFxuICAgIHtcbiAgICAgIGNvbmZpcm1CdXR0b25UZXh0OiAnT0snLFxuICAgICAgY2FuY2VsQnV0dG9uVGV4dDogJ0NhbmNlbCcsXG4gICAgICB0eXBlOiAnaW5mbycsXG4gICAgICBkcmFnZ2FibGU6IHRydWUsXG4gICAgICBjdXN0b21DbGFzczogJ2N1c3RvbS1kcmFnZ2luZy1tZXNzYWdlLWJveCcsXG4gICAgfVxuICApXG4gICAgLnRoZW4oKCkgPT4ge1xuICAgICAgRWxNZXNzYWdlKHtcbiAgICAgICAgdHlwZTogJ3N1Y2Nlc3MnLFxuICAgICAgICBtZXNzYWdlOiAnQWN0aW9uIGNvbXBsZXRlZCcsXG4gICAgICB9KVxuICAgIH0pXG4gICAgLmNhdGNoKCgpID0+IHtcbiAgICAgIEVsTWVzc2FnZSh7XG4gICAgICAgIHR5cGU6ICdpbmZvJyxcbiAgICAgICAgbWVzc2FnZTogJ0FjdGlvbiBjYW5jZWxlZCcsXG4gICAgICB9KVxuICAgIH0pXG59XG48L3NjcmlwdD5cblxuPHN0eWxlPlxuLmN1c3RvbS1kcmFnZ2luZy1tZXNzYWdlLWJveC5pcy1kcmFnZ2luZyB7XG4gIGJvcmRlcjogMnB4IGRhc2hlZCB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgb3BhY2l0eTogMC42NTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/message-box/draggable.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" plain @click="open">
      Open a draggable Message Box
    </el-button>
    <el-button class="!ml-0" plain @click="open2">
      Open a overflow draggable Message Box
    </el-button>
    <el-button class="!ml-0" plain @click="open3">
      Open a custom dragging style Message Box
    </el-button>
  </div>
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
      draggable: true,
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

const open2 = () => {
  ElMessageBox.confirm(
    'proxy will permanently delete the file. Continue?',
    'Warning',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
      draggable: true,
      overflow: true,
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

const open3 = () => {
  ElMessageBox.confirm(
    'This message box has custom dragging styles. Try dragging it to see the effects!',
    'Custom Dragging Style',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'info',
      draggable: true,
      customClass: 'custom-dragging-message-box',
    }
  )
    .then(() => {
      ElMessage({
        type: 'success',
        message: 'Action completed',
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: 'Action canceled',
      })
    })
}
</script>

<style>
.custom-dragging-message-box.is-dragging {
  border: 2px dashed var(--el-color-primary);
  opacity: 0.65;
}
</style>
```

隐藏源代码

## 全局方法 [​](#全局方法)

如果你完整引入了 Element，它会为 `app.config.globalProperties` 添加如下全局方法：`$msgbox`、 `$alert`、 `$confirm` 和 `$prompt`。 因此在 Vue 实例中可以采用本页面中的方式来调用`MessageBox`。 参数如下：

-   `$msgbox(options)`
-   `$alert(message, title, options)` 或 `$alert(message, options)`
-   `$confirm(message, title, options)` 或 `$confirm(message, options)`
-   `$prompt(message, title, options)` 或 `$prompt(message, options)`

## 应用程序上下文继承 \> 2.0.4 [​](#应用程序上下文继承-2-0-4)

现在，消息框构造函数支持将 `context` 作为第二个参数（如果你使用的是消息框变体，则为第四个参数），这样你就可以向消息中注入当前应用的上下文，从而继承应用中的所有属性。

ts

```
import { getCurrentInstance } from 'vue'
import { ElMessageBox } from 'element-plus'

// 在你的 setup 方法中
const { appContext } = getCurrentInstance()!
// 你可以像这样传递参数：
ElMessageBox({}, appContext)
// 或者正在使用不同的调用方式
ElMessageBox.alert('Hello world!', 'Title', {}, appContext)
```

## 按需引入 [​](#按需引入)

如果您需要按需引入 `MessageBox`：

ts

```
import { ElMessageBox } from 'element-plus'
```

那么对应于上述四个全局方法的调用方法依次为：`ElMessageBox`、`ElMessageBox.alert`、`ElMessageBox.confirm` 和 `ElMessageBox.prompt`。 参数同上所述。

## API [​](#api)

### 配置项 [​](#配置项)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| autofocus | 打开 MessageBox 时是否自动获得焦点 | `boolean` | true |
| title | MessageBox 的标题 | `string` | '' |
| message | MessageBox 的正文内容 | `string` / `VNode` / `Function` 2.2.17 / `Function` 2.14.0 | — |
| dangerouslyUseHTMLString | 是否将 `message` 作为 HTML 片段处理 | `boolean` | false |
| type | 消息类型，用于图标显示 | `enum` | '' |
| icon | 自定义图标组件，会覆盖 `type` 的类型 | `string` / `Component` | '' |
| closeIcon 2.9.5 | 自定义关闭图标组件，默认是 Close | `string` / `Component` | '' |
| customClass | MessageBox 的自定义类名 | `string` | '' |
| customStyle | MessageBox 的自定义内联样式 | `CSSProperties` | {} |
| modal | 是否需要遮罩层 | `boolean` | true |
| modalClass | 遮罩的自定义类名 | string | — |
| callback | 若不使用 Promise，可以使用此参数指定 MessageBox 关闭后的回调 | `Function` | null |
| showClose | MessageBox 是否显示右上角关闭按钮 | `boolean` | true |
| beforeClose | messageBox 关闭前的回调，会暂停消息弹出框的关闭过程。 | `Function` | null |
| distinguishCancelAndClose | 是否将取消（点击取消按钮）与关闭（点击关闭按钮或遮罩层、按下 Esc 键）进行区分 | `boolean` | false |
| lockScroll | 是否在 MessageBox 出现时将 body 滚动锁定 | `boolean` | true |
| showCancelButton | 是否显示取消按钮 | `boolean` | false（以 confirm 和 prompt 方式调用时为 true） |
| showConfirmButton | 是否显示确定按钮 | `boolean` | true |
| cancelButtonText | 取消按钮的文本内容 | `string` | 取消 |
| confirmButtonText | 确定按钮的文本内容 | `string` | 确定 |
| cancelButtonType 2.13.1 | 取消按钮的类型 | `enum` | — |
| confirmButtonType 2.13.1 | 确认按钮类型 | `enum` | primary |
| cancelButtonLoadingIcon 2.7.7 | 取消按钮的加载图标内容 | `string` / `Component` | Loading |
| confirmButtonLoadingIcon 2.7.7 | 确认按钮的加载图标内容 | `string` / `Component` | Loading |
| cancelButtonClass | 取消按钮的自定义类名 | `string` | '' |
| confirmButtonClass | 确定按钮的自定义类名 | `string` | '' |
| closeOnClickModal | 是否可通过点击遮罩层关闭 MessageBox | `boolean` | true（以 alert 方式调用时为 false） |
| closeOnPressEscape | 是否可通过按下 ESC 键关闭 MessageBox | `boolean` | true（以 alert 方式调用时为 false） |
| closeOnHashChange | 是否在 hash 改变时关闭 MessageBox | `boolean` | true |
| showInput | 是否显示输入框 | `boolean` | false（以 prompt 方式调用时为 true） |
| inputPlaceholder | 输入框占位文本 | `string` | '' |
| inputType | 输入类型，更多信息请参见 [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#Form_%3Cinput%3E_types) | `string` | text |
| inputValue | 输入框的初始文本 | `string` | '' |
| inputPattern | 输入框的校验表达式 | `regexp` | null |
| inputValidator | 输入框的校验函数。 应该返回一个 boolean 或者 string， 如果返回的是一个 string 类型，那么该返回值会被赋值给 inputErrorMessage 用于向用户展示错误消息。 | `Function`/ `undefined` | undefined |
| inputErrorMessage | 校验未通过时的提示文本 | `string` | 输入的数据不合法! |
| center | 是否居中布局 | `boolean` | false |
| draggable | MessageBox 是否可拖放 | `boolean` | false |
| overflow 2.5.4 | MessageBox 拖动范围可以超出可视区 | `boolean` | false |
| roundButton | 是否使用圆角按钮 | `boolean` | false |
| buttonSize | 自定义确认按钮及取消按钮的大小 | `string` | default |
| appendTo 2.2.19 | 设置组件的根元素 | `CSSSelector` / `HTMLElement` | ::: |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/message-box) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/message-box.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/message-box.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/182307812?v=4&size=64)](https://github.com/whcanic)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/13410410?v=4&size=64)](https://github.com/jaa134)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/12488719?v=4&size=64)](https://github.com/a3660980)[![](https://avatars.githubusercontent.com/u/65892539?v=4&size=64)](https://github.com/xionkq)[![](https://avatars.githubusercontent.com/u/43703884?v=4&size=64)](https://github.com/DDDDD12138)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/29518699?v=4&size=64)](https://github.com/reiwang01)[![](https://avatars.githubusercontent.com/u/66702442?v=4&size=64)](https://github.com/danny-hebert)[![](https://avatars.githubusercontent.com/u/25543909?v=4&size=64)](https://github.com/MMmaXingXing)[![](https://avatars.githubusercontent.com/u/60056876?v=4&size=64)](https://github.com/LinZhanMing)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/43326199?v=4&size=64)](https://github.com/Wiensss)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/46836729?v=4&size=64)](https://github.com/yuzhang9804)[![](https://avatars.githubusercontent.com/u/15833290?v=4&size=64)](https://github.com/zhousg)[![](https://avatars.githubusercontent.com/u/29992752?v=4&size=64)](https://github.com/llllllllllx)[![](https://avatars.githubusercontent.com/u/31462942?v=4&size=64)](https://github.com/zhazhanitian)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/234919486?v=4&size=64)](https://github.com/linzx-jess)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/52314078?v=4&size=64)](https://github.com/vaebe)[![](https://avatars.githubusercontent.com/u/78132554?v=4&size=64)](https://github.com/momei-LJM)[![](https://avatars.githubusercontent.com/u/8591261?v=4&size=64)](https://github.com/zeyongTsai)[![](https://avatars.githubusercontent.com/u/22388686?v=4&size=64)](https://github.com/TomatoDroid)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)

[Message 消息提示](https://element-plus.org/zh-CN/component/message)

[Notification 通知](https://element-plus.org/zh-CN/component/notification)


