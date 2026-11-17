## Popover 弹出框 ​

**URL:** https://element-plus.org/zh-CN/component/popover

**Contents:**
- Popover 弹出框 ​
- 展示位置 ​
- 基础用法 ​
- 虚拟触发 ​
- 内容可扩展 ​
- 嵌套操作 ​
- 指令 ​
- API ​
  - Attributes ​
  - Slots ​

Popover 弹出框提供 9 种展示位置。

使用 content 属性来设置悬停时显示的信息。 由 placement 属性决定 Popover 弹出框的位置。 该属性值格式为：[方向]-[对齐位置]，可供选择的四个方向分别是top、left、right、bottom，可供选择的三种对齐方式分别是start、end、null，默认的对齐方式为null。 以 placement="left-end" 为例，Popover 弹出框会显示在悬停元素的左侧，且提示信息的底部与悬停元素的底部对齐。

Popover 是在 ElTooltip 基础上开发出来的。 因此对于重复属性，请参考 Tooltip 的文档，在此文档中不做详尽解释。

trigger 属性被用来决定 popover 的触发方式，支持的触发方式： hover、click、focus 或 contextmenu。 如果你想手动控制它，可以设置 :visible 属性。

像 Tooltip一样，Popover 可以由虚拟元素触发，这个功能就很适合使用在触发元素和展示内容元素是分开的场景。通常我们使用 #reference 来放置我们的触发元素， 用 triggering-element API，您可以任意设置您的触发元素 但注意到触发元素应该是接受 mouse 和 keyboard 事件的元素。

v-popover 将被废弃，请使用 virtual-ref 作为替代。

可以在 Popover 中嵌套其它组件， 以下为嵌套表格的例子。

当然，你还可以嵌套操作， 它比使用dialog更加轻量。

您可以使用指令性方式弹出窗口，但这种方法不再推荐 ，因为这使得应用程序变得复杂， 您可以参考虚拟触发来实现一样的效果。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="popover-base-box">
    <div class="row center">
      <el-popover
        title="Title"
        content="Top Left prompts info"
        placement="top-start"
      >
        <template #reference>
          <el-button>top-start</el-button>
        </template>
      </el-popover>
      <el-popover
        title="Title"
        content="Top Center prompts info"
        placement="top"
      >
        <template #reference>
          <el-button>top</el-button>
        </template>
      </el-popover>
      <el-popover
        title="Title"
        content="Top Right prompts info"
        placement="top-end"
      >
        <template #reference>
          <el-button>top-end</el-button>
        </template>
      </el-popover>
    </div>
    <div class="row">
      <el-popover
        title="Title"
        content="Left Top prompts info"
        placement="left-start"
      >
        <template #reference>
          <el-button>left-start</el-button>
        </template>
      </el-popover>
      <el-popover
        title="Title"
        content="Right Top prompts info"
        placement="right-start"
      >
        <template #reference>
          <el-button>right-start</el-button>
        </template>
      </el-popover>
    </div>
    <div class="row">
      <el-popover
        title="Title"
        content="Left Center prompts info"
        placement="left"
      >
        <template #reference>
          <el-button class="mt-3 mb-3">left</el-button>
        </template>
      </el-popover>
      <el-popover
        title="Title"
        content="Right Center prompts info"
        placement="right"
      >
        <template #reference>
          <el-button>right</el-button>
        </template>
      </el-popover>
    </div>
    <div class="row">
      <el-popover
        title="Title"
        content="Left Bottom prompts info"
        placement="left-end"
      >
        <template #reference>
          <el-button>left-end</el-button>
        </template>
      </el-popover>
      <el-popover
        title="Title"
        content="Right Bottom prompts info"
        placement="right-end"
      >
        <template #reference>
          <el-button>right-end</el-button>
        </template>
      </el-popover>
    </div>
    <div class="row center">
      <el-popover
        title="Title"
        content="Bottom Left prompts info"
        placement="bottom-start"
      >
        <template #reference> <el-button>bottom-start</el-button></template>
      </el-popover>
      <el-popover
        title="Title"
        content="Bottom Center prompts info"
        placement="bottom"
      >
        <template #reference> <el-button>bottom</el-button></template>
      </el-popover>
      <el-popover
        title="Title"
        content="Bottom Right prompts info"
        placement="bottom-end"
      >
        <template #reference>
          <el-button>bottom-end</el-button>
        </template>
      </el-popover>
    </div>
  </div>
</template>

<style>
.popover-base-box {
  width: 600px;
}

.popover-base-box .row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.popover-base-box .center {
  justify-content: center;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <el-popover
    placement="top-start"
    title="Title"
    :width="200"
    trigger="hover"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <el-button class="m-2">Hover to activate</el-button>
    </template>
  </el-popover>

  <el-popover
    placement="bottom"
    title="Title"
    :width="200"
    trigger="click"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <el-button class="m-2">Click to activate</el-button>
    </template>
  </el-popover>

  <el-popover
    ref="popover"
    placement="right"
    title="Title"
    :width="200"
    trigger="focus"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <el-button class="m-2">Focus to activate</el-button>
    </template>
  </el-popover>

  <el-popover
    ref="popover"
    title="Title"
    :width="200"
    trigger="contextmenu"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <el-button class="m-2">contextmenu to activate</el-button>
    </template>
  </el-popover>

  <el-popover
    :visible="visible"
    placement="bottom"
    title="Title"
    :width="200"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <el-button class="m-2" @click="visible = !visible">
        Manual to activate
      </el-button>
    </template>
  </el-popover>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const visible = ref(false)
</script>

<style scoped>
.el-button + .el-button {
  margin-left: 8px;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <el-button ref="buttonRef" v-click-outside="onClickOutside">
    Click me
  </el-button>

  <el-popover
    ref="popoverRef"
    :virtual-ref="buttonRef"
    trigger="click"
    title="With title"
    virtual-triggering
  >
    <span> Some content </span>
  </el-popover>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ClickOutside as vClickOutside } from 'element-plus'

import type { PopoverInstance } from 'element-plus'

const buttonRef = ref()
const popoverRef = ref<PopoverInstance>()
const onClickOutside = () => {
  popoverRef.value?.hide()
}
</script>
```

Example 4 (sass):
```sass
<template>
  <div style="display: flex; align-items: center">
    <el-popover placement="right" :width="400" trigger="click">
      <template #reference>
        <el-button style="margin-right: 16px">Click to activate</el-button>
      </template>
      <el-table :data="gridData">
        <el-table-column width="150" property="date" label="date" />
        <el-table-column width="100" property="name" label="name" />
        <el-table-column width="300" property="address" label="address" />
      </el-table>
    </el-popover>

    <el-popover
      :width="300"
      popper-style="box-shadow: rgb(14 18 22 / 35%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px;"
    >
      <template #reference>
        <el-avatar src="https://avatars.githubusercontent.com/u/72015883?v=4" />
      </template>
      <template #default>
        <div
          class="demo-rich-conent"
          style="display: flex; gap: 16px; flex-direction: column"
        >
          <el-avatar
            :size="60"
            src="https://avatars.githubusercontent.com/u/72015883?v=4"
            style="margin-bottom: 8px"
          />
          <div>
            <p
              class="demo-rich-content__name"
              style="margin: 0; font-weight: 500"
            >
              Element Plus
            </p>
            <p
              class="demo-rich-content__mention"
              style="margin: 0; font-size: 14px; color: var(--el-color-info)"
            >
              @element-plus
            </p>
          </div>

          <p class="demo-rich-content__desc" style="margin: 0">
            Element Plus, a Vue 3 based component library for developers,
            designers and product managers
          </p>
        </div>
      </template>
    </el-popover>
  </div>
</template>

<script lang="ts" setup>
const gridData = [
  {
    date: '2016-05-02',
    name: 'Jack',
    address: 'New York City',
  },
  {
    date: '2016-05-04',
    name: 'Jack',
    address: 'New York City',
  },
  {
    date: '2016-05-01',
    name: 'Jack',
    address: 'New York City',
  },
  {
    date: '2016-05-03',
    name: 'Jack',
    address: 'New York City',
  },
]
</script>
```

---
