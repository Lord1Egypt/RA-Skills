## Drawer 抽屉 ​

**URL:** https://element-plus.org/zh-CN/component/drawer

**Contents:**
- Drawer 抽屉 ​
- 基础用法 ​
    - set title by slot
- 不添加 Title ​
- 自定义内容 ​
- 自定义头部 ​
    - This is a custom header!
- 可调整抽屉2.11.0 ​
- 嵌套抽屉 ​
- 模态框 ​

有些时候, Dialog 组件并不满足我们的需求, 比如你的表单很长, 亦或是你需要临时展示一些文档, Drawer 拥有和 Dialog 几乎相同的 API, 在 UI 上带来不一样的体验.

在 Vue 3 之后的版本 v-model 可以用于任何一个组件，visible.sync 已被移除，请使用 v-model="visibilityBinding" 来控制抽屉组件的显示和隐藏状态。

呼出一个临时的侧边栏, 可以从多个方向呼出

你必须像 Dialog一样为 Drawer 设置 model-value 属性来控制 Drawer 的显示与隐藏状态，该属性接受一个 boolean 类型。 Drawer 包含三部分: title & body & footer, 其中 title 是一个具名 slot, 你还可以通过 title 属性来设置标题, 默认情况下它是一个空字符串, 其中 body 部分是 Drawer 组件的主区域, 它包含了用户定义的主要内容. footer和title用法一致, 用来显示页脚信息. 当 Drawer 打开时，默认设置是从右至左打开 30% 浏览器宽度。 你可以通过传入对应的 direction 和 size 属性来修改这一默认行为。 下面一个示例将展示如何使用 before-close API，更多详细用法请参考页面底部的 API 部分。

通过设置 with-header 属性为 false 来控制是否显示标题。 如果你的应用需要具备可访问性，请务必设置好 title。

像 Dialog 组件一样，Drawer 也可以用来显示多种不同的交互。

header 可用于自定义显示标题的区域。 为了保持可用性，除了使用此插槽外，使用 title 属性，或使用 titleId 插槽属性来指定哪些元素应该读取为抽屉标题。

设置resizable属性为true以做到拖拽

你可以像 Dialog 一样拥有多层嵌套的 Drawer

如果你需要在不同图层中多个抽屉，你必须设置 append-to-body 属性到 true

将 modal 设置为 false 将隐藏抽屉的模态层（遮罩层）。

从版本 2.11.7 起，新增了 modal-penetrable 属性，该属性可设置为“可穿透”。

Drawer 的内容是懒渲染的，即在第一次被打开之前，传入的默认 slot 不会被渲染到 DOM 上。 因此，如果需要执行 DOM 操作，或通过 ref 获取相应组件，请在 open 事件回调中进行。

Drawer 提供了一个名为 destroy-on-close 的 API，这是一个标志变量，用于指示在 Drawer 关闭后是否销毁其中的子内容。 当你需要每次打开抽屉都要调用 mounted 生命周期时，可以使用此 API。

custom-class 已被 弃用，将会于 2.3.0 移除, 请使用 class。

title 已被弃用，并将在 3.0.0 版本中移除，请使用 header 代替。

**Examples:**

Example 1 (javascript):
```javascript
<template>
  <el-radio-group v-model="direction">
    <el-radio value="ltr">left to right</el-radio>
    <el-radio value="rtl">right to left</el-radio>
    <el-radio value="ttb">top to bottom</el-radio>
    <el-radio value="btt">bottom to top</el-radio>
  </el-radio-group>

  <el-button type="primary" style="margin-left: 16px" @click="drawer = true">
    open
  </el-button>
  <el-button type="primary" style="margin-left: 16px" @click="drawer2 = true">
    with footer
  </el-button>

  <el-drawer
    v-model="drawer"
    title="I am the title"
    :direction="direction"
    :before-close="handleClose"
  >
    <span>Hi, there!</span>
  </el-drawer>
  <el-drawer v-model="drawer2" :direction="direction">
    <template #header>
      <h4>set title by slot</h4>
    </template>
    <template #default>
      <div>
        <el-radio v-model="radio1" value="Option 1" size="large">
          Option 1
        </el-radio>
        <el-radio v-model="radio1" value="Option 2" size="large">
          Option 2
        </el-radio>
      </div>
    </template>
    <template #footer>
      <div style="flex: auto">
        <el-button @click="cancelClick">cancel</el-button>
        <el-button type="primary" @click="confirmClick">confirm</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

import type { DrawerProps } from 'element-plus'

const drawer = ref(false)
const drawer2 = ref(false)
const direction = ref<DrawerProps['direction']>('rtl')
const radio1 = ref('Option 1')
const handleClose = (done: () => void) => {
  ElMessageBox.confirm('Are you sure you want to close this?')
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}
function cancelClick() {
  drawer2.value = false
}
function confirmClick() {
  ElMessageBox.confirm(`Are you confirm to chose ${radio1.value} ?`)
    .then(() => {
      drawer2.value = false
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
  <el-button type="primary" @click="drawer = true"> open </el-button>

  <el-drawer v-model="drawer" title="I am the title" :with-header="false">
    <span>Hi there!</span>
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const drawer = ref(false)
</script>
```

Example 3 (vue):
```vue
<template>
  <el-button text @click="table = true">
    Open Drawer with nested table
  </el-button>
  <el-button text @click="dialog = true">
    Open Drawer with nested form
  </el-button>
  <el-drawer
    v-model="table"
    title="I have a nested table inside!"
    direction="rtl"
    size="50%"
  >
    <el-table :data="gridData">
      <el-table-column property="date" label="Date" width="150" />
      <el-table-column property="name" label="Name" width="200" />
      <el-table-column property="address" label="Address" />
    </el-table>
  </el-drawer>

  <el-drawer
    v-model="dialog"
    title="I have a nested form inside!"
    :before-close="handleClose"
    direction="ltr"
    class="demo-drawer"
  >
    <div class="demo-drawer__content">
      <el-form :model="form">
        <el-form-item label="Name" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Area" :label-width="formLabelWidth">
          <el-select
            v-model="form.region"
            placeholder="Please select activity area"
          >
            <el-option label="Area1" value="shanghai" />
            <el-option label="Area2" value="beijing" />
          </el-select>
        </el-form-item>
      </el-form>
      <div class="demo-drawer__footer">
        <el-button @click="cancelForm">Cancel</el-button>
        <el-button type="primary" :loading="loading" @click="onClick">
          {{ loading ? 'Submitting ...' : 'Submit' }}
        </el-button>
      </div>
    </div>
  </el-drawer>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { ElMessageBox } from 'element-plus'

const formLabelWidth = '80px'
let timer

const table = ref(false)
const dialog = ref(false)
const loading = ref(false)

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
    name: 'Peter Parker',
    address: 'Queens, New York City',
  },
  {
    date: '2016-05-04',
    name: 'Peter Parker',
    address: 'Queens, New York City',
  },
  {
    date: '2016-05-01',
    name: 'Peter Parker',
    address: 'Queens, New York City',
  },
  {
    date: '2016-05-03',
    name: 'Peter Parker',
    address: 'Queens, New York City',
  },
]

const onClick = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    dialog.value = false
  }, 400)
}

const handleClose = (done) => {
  if (loading.value) {
    return
  }
  ElMessageBox.confirm('Do you want to submit?')
    .then(() => {
      loading.value = true
      timer = setTimeout(() => {
        done()
        // 动画关闭需要一定的时间
        setTimeout(() => {
          loading.value = false
        }, 400)
      }, 2000)
    })
    .catch(() => {
      // catch error
    })
}

const cancelForm = () => {
  loading.value = false
  dialog.value = false
  clearTimeout(timer)
}
</script>
```

Example 4 (vue):
```vue
<template>
  <el-button @click="visible = true">
    Open Drawer with customized header
  </el-button>
  <el-drawer v-model="visible" :show-close="false">
    <template #header="{ close, titleId, titleClass }">
      <h4 :id="titleId" :class="titleClass">This is a custom header!</h4>
      <el-button type="danger" @click="close">
        <el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>
        Close
      </el-button>
    </template>
    This is drawer content.
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CircleCloseFilled } from '@element-plus/icons-vue'

const visible = ref(false)
</script>
```

---
