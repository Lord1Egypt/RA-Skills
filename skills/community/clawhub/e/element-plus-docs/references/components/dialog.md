## Dialog 对话框 ​

**URL:** https://element-plus.org/zh-CN/component/dialog

**Contents:**
- Dialog 对话框 ​
- 基础用法 ​
- 自定义内容 ​
- 自定义头部 ​
- 嵌套的对话框 ​
- 内容居中 ​
- 居中对话框 ​
- 关闭时销毁 ​
- 可拖拽对话框 ​
- 全屏 ​

在保留当前页面状态的情况下，告知用户并承载相关操作。

Dialog 弹出一个对话框，适合需要定制性更大的场景。

需要设置 model-value / v-model 属性，它接收 Boolean，当为 true 时显示 Dialog。 Dialog 分为两个部分：body 和 footer，footer 需要具名为 footer 的 slot。 title 属性用于定义标题，它是可选的，默认值为空。 最后，本例还展示了 before-close 的用法。

before-close 只会在用户点击关闭按钮或者对话框的遮罩区域时被调用。 如果你在 footer 具名 slot 里添加了用于关闭 Dialog 的按钮，那么可以在按钮的点击回调函数里加入 before-close 的相关逻辑。

对话框的内容可以是任何东西，甚至是一个表格或表单。 此示例显示如何在 Dialog 中使用 Element Plus 的表格和表单。

header 可用于自定义显示标题的区域。 为了保持可用性，除了使用此插槽外，使用 title 属性，或使用 titleId 插槽属性来指定哪些元素应该读取为对话框标题。

如果需要在一个 Dialog 内部嵌套另一个 Dialog，需要使用 append-to-body 属性。

通常我们不建议使用嵌套对话框。 如果你需要在页面上呈现多个对话框，你可以简单地打平它们，以便它们彼此之间是平级关系。 如果必须要在一个对话框内展示另一个对话框，可以将内部嵌套的对话框属性 append-to-body 设置为 true，嵌套的对话框将附加到 body 而不是其父节点，这样两个对话框都可以被正确地渲染。

将center设置为true即可使标题和底部居中。 center仅影响标题和底部区域。 Dialog 的内容是任意的，在一些情况下，内容并不适合居中布局。 如果需要内容也水平居中，请自行为其添加 CSS 样式。

Dialog 的内容是懒渲染的——在被第一次打开之前，传入的默认 slot 不会被立即渲染到 DOM 上。 因此，如果需要执行 DOM 操作，或通过 ref 获取相应组件，请在 open 事件回调中进行。

设置 align-center 为 true 使对话框水平垂直居中。 由于对话框垂直居中在弹性盒子中，所以top属性将不起作用。

启用此功能时，默认栏位下的内容将使用 v-if 指令销毁。 当出现性能问题时，可以启用此功能。

需要注意的是，当这个属性被启用时，在 transition.beforeEnter 事件卸载前，除了 overlay、header (可选)与footer(可选) ，Dialog 内不会有其它任何其它的 DOM 节点存在。

设置draggable属性为true以做到拖拽 设置 overflow 2.5.4 为 true 可以让拖拽范围超出可视区。

当 modal 的值为 false 时，请一定要确保 append-to-body 属性为 true，由于 Dialog 使用 position: relative 定位，当外层的遮罩层被移除时，Dialog 则会根据当前 DOM 上的祖先节点来定位，因此可能造成定位问题。

设置 fullscreen 属性来打开全屏对话框。

如果 fullscreen 为 true，则 width、top 和 draggable 属性无效。

将 modal 设置为 false 会隐藏对话框的模态（覆盖层）。

从版本 2.10.5 起，新增了 modal-penetrable属性，该属性可设置为“可穿透”（即允许穿透）。

通过 transition 属性自定义对话框动画，该属性可以接受以下任意一种值：

示例包括缩放（scale）、滑动（slide）、淡入淡出（fade）、弹跳（bounce）动画，以及带有自定义事件处理器的基于对象的配置。

动画类会根据过渡名称动态生成。 为了更细致地控制动画行为，你可以明确地定义这些类。 详情请参见 自定义过渡类（custom-transition-classes）。

打开开发者控制台(ctrl + shift + J)，查看事件的顺序。

custom-class 已被 弃用, 之后将会在 2.4.0 移除, 请使用 class.

title 已被弃用，并将在 3.0.0 版本中移除，请使用 header 代替。

PS：既然对话框是使用 Teleport 渲染的，建议在全局范围写入根节点的样式。

PS：建议将滚动区域放置在一个挂载的 vue 节点，如 <div id="app" /> 下，并对 body 使用 overflow: hidden 样式。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-button plain @click="dialogVisible = true">
    Click to open the Dialog
  </el-button>

  <el-dialog
    v-model="dialogVisible"
    title="Tips"
    width="500"
    :before-close="handleClose"
  >
    <span>This is a message</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

const dialogVisible = ref(false)

const handleClose = (done: () => void) => {
  ElMessageBox.confirm('Are you sure to close this dialog?')
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}
</script>
```

Example 2 (vue):
```vue
<template>
  <div class="flex flex-wrap gap-1">
    <el-button class="!ml-0" plain @click="dialogTableVisible = true">
      Open a Table nested Dialog
    </el-button>

    <el-button class="!ml-0" plain @click="dialogFormVisible = true">
      Open a Form nested Dialog
    </el-button>
  </div>

  <el-dialog v-model="dialogTableVisible" title="Shipping address" width="800">
    <el-table :data="gridData">
      <el-table-column property="date" label="Date" width="150" />
      <el-table-column property="name" label="Name" width="200" />
      <el-table-column property="address" label="Address" />
    </el-table>
  </el-dialog>

  <el-dialog v-model="dialogFormVisible" title="Shipping address" width="500">
    <el-form :model="form">
      <el-form-item label="Promotion name" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Zones" :label-width="formLabelWidth">
        <el-select v-model="form.region" placeholder="Please select a zone">
          <el-option label="Zone No.1" value="shanghai" />
          <el-option label="Zone No.2" value="beijing" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

const dialogTableVisible = ref(false)
const dialogFormVisible = ref(false)
const formLabelWidth = '140px'

const form = reactive({
  name: '',
  region: '',
  date1: '',
  date2: '',
  delivery: false,
  type: [],
  resource: '',
  desc: '',
})

const gridData = [
  {
    date: '2016-05-02',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-04',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-01',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-03',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
]
</script>
```

Example 3 (vue):
```vue
<template>
  <el-button plain @click="visible = true">
    Open Dialog with customized header
  </el-button>

  <el-dialog v-model="visible" :show-close="false" width="500">
    <template #header="{ close, titleId, titleClass }">
      <div class="my-header">
        <h4 :id="titleId" :class="titleClass">This is a custom header!</h4>
        <el-button type="danger" @click="close">
          <el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>
          Close
        </el-button>
      </div>
    </template>
    This is dialog content.
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CircleCloseFilled } from '@element-plus/icons-vue'

const visible = ref(false)
</script>

<style scoped>
.my-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 16px;
}
</style>
```

Example 4 (vue):
```vue
<template>
  <el-button plain @click="outerVisible = true">
    Open the outer Dialog
  </el-button>

  <el-dialog v-model="outerVisible" title="Outer Dialog" width="800">
    <span>This is the outer Dialog</span>
    <el-dialog
      v-model="innerVisible"
      width="500"
      title="Inner Dialog"
      append-to-body
    >
      <span>This is the inner Dialog</span>
    </el-dialog>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="outerVisible = false">Cancel</el-button>
        <el-button type="primary" @click="innerVisible = true">
          Open the inner Dialog
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const outerVisible = ref(false)
const innerVisible = ref(false)
</script>
```

---
