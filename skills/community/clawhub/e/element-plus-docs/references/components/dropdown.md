## Dropdown 下拉菜单 ​

**URL:** https://element-plus.org/zh-CN/component/dropdown

**Contents:**
- Dropdown 下拉菜单 ​
- 基础用法 ​
- 位置 ​
- 触发对象 ​
- 触发方式 ​
- 菜单隐藏方式 ​
- 指令事件 ​
- 下拉方法 ​
- 尺寸 ​
- 虚拟触发2.11.3 ​

通过组件 slot 来设置下拉触发的元素以及需要通过具名 slot 为 dropdown 来设置下拉菜单。 默认情况下，只需要悬停在触发菜单的元素上即可，无需点击也会显示下拉菜单。

设置 placement 属性，使下拉菜单出现在不同位置。

设置 split-button 属性来让触发下拉元素呈现为按钮组，左边是功能按钮，右边是触发下拉菜单的按钮，设置为 true 即可。 如果你想要在第三和第四个选项之间添加一个分隔符，你只需要为第四个选项添加一个 divided 的属性。

将 trigger 属性设置为 click 即可， 默认为 hover。

可以通过 hide-on-click 属性来配置。

下拉菜单默认在点击菜单项后会被隐藏，将 hide-on-click 属性设置为 false 可以关闭此功能。

点击菜单项后会触发事件，用户可以通过相应的菜单项 key 进行不同的操作。

您可以手动使用 手动打开 或 手动关闭下拉菜单以打开或关闭

open(close) the Dropdown list2 will close(open) the Dropdown List1.

Dropdown 组件提供除了默认值以外的三种尺寸，可以在不同场景下选择合适的尺寸。

使用 size 属性配置尺寸，可选的尺寸大小有: large, default 或 small

有时候我们想把 dropdown 的触发元素放在别的地方，而不需要写在一起，这时候就可以使用虚拟触发。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-dropdown>
    <span class="el-dropdown-link">
      Dropdown List
      <el-icon class="el-icon--right">
        <arrow-down />
      </el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item>Action 1</el-dropdown-item>
        <el-dropdown-item>Action 2</el-dropdown-item>
        <el-dropdown-item>Action 3</el-dropdown-item>
        <el-dropdown-item disabled>Action 4</el-dropdown-item>
        <el-dropdown-item divided>Action 5</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script lang="ts" setup>
import { ArrowDown } from '@element-plus/icons-vue'
</script>

<style scoped>
.example-showcase .el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div class="flex flex-wrap items-center gap-4">
    <el-dropdown placement="top-start">
      <el-button> topStart </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>The Action 1st</el-dropdown-item>
          <el-dropdown-item>The Action 2nd</el-dropdown-item>
          <el-dropdown-item>The Action 3rd</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <el-dropdown placement="top">
      <el-button> top </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>The Action 1st</el-dropdown-item>
          <el-dropdown-item>The Action 2nd</el-dropdown-item>
          <el-dropdown-item>The Action 3rd</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <el-dropdown placement="top-end">
      <el-button> topEnd </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>The Action 1st</el-dropdown-item>
          <el-dropdown-item>The Action 2nd</el-dropdown-item>
          <el-dropdown-item>The Action 3rd</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <el-dropdown placement="bottom-start">
      <el-button> bottomStart </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>The Action 1st</el-dropdown-item>
          <el-dropdown-item>The Action 2nd</el-dropdown-item>
          <el-dropdown-item>The Action 3rd</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <el-dropdown placement="bottom">
      <el-button> bottom </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>The Action 1st</el-dropdown-item>
          <el-dropdown-item>The Action 2nd</el-dropdown-item>
          <el-dropdown-item>The Action 3rd</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <el-dropdown placement="bottom-end">
      <el-button> bottomEnd </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>The Action 1st</el-dropdown-item>
          <el-dropdown-item>The Action 2nd</el-dropdown-item>
          <el-dropdown-item>The Action 3rd</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>
```

Example 3 (vue):
```vue
<template>
  <div class="flex flex-wrap items-center">
    <el-dropdown>
      <el-button type="primary">
        Dropdown List<el-icon class="el-icon--right"><arrow-down /></el-icon>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>Action 1</el-dropdown-item>
          <el-dropdown-item>Action 2</el-dropdown-item>
          <el-dropdown-item>Action 3</el-dropdown-item>
          <el-dropdown-item>Action 4</el-dropdown-item>
          <el-dropdown-item>Action 5</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <el-dropdown split-button type="primary" @click="handleClick">
      Dropdown List
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>Action 1</el-dropdown-item>
          <el-dropdown-item>Action 2</el-dropdown-item>
          <el-dropdown-item>Action 3</el-dropdown-item>
          <el-dropdown-item divided>Action 4</el-dropdown-item>
          <el-dropdown-item>Action 5</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script lang="ts" setup>
import { ArrowDown } from '@element-plus/icons-vue'

const handleClick = () => {
  // eslint-disable-next-line no-alert
  alert('button click')
}
</script>

<style scoped>
.example-showcase .el-dropdown + .el-dropdown {
  margin-left: 15px;
}
.example-showcase .el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>
```

Example 4 (vue):
```vue
<template>
  <el-row class="block-col-2">
    <el-col :span="8">
      <span class="demonstration">hover to trigger</span>
      <el-dropdown>
        <span class="el-dropdown-link">
          Dropdown List<el-icon class="el-icon--right"><arrow-down /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item :icon="Plus">Action 1</el-dropdown-item>
            <el-dropdown-item :icon="CirclePlusFilled">
              Action 2
            </el-dropdown-item>
            <el-dropdown-item :icon="CirclePlus">Action 3</el-dropdown-item>
            <el-dropdown-item :icon="Check">Action 4</el-dropdown-item>
            <el-dropdown-item :icon="CircleCheck">Action 5</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-col>
    <el-col :span="8">
      <span class="demonstration">click to trigger</span>
      <el-dropdown trigger="click">
        <span class="el-dropdown-link">
          Dropdown List<el-icon class="el-icon--right"><arrow-down /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item :icon="Plus">Action 1</el-dropdown-item>
            <el-dropdown-item :icon="CirclePlusFilled">
              Action 2
            </el-dropdown-item>
            <el-dropdown-item :icon="CirclePlus">Action 3</el-dropdown-item>
            <el-dropdown-item :icon="Check">Action 4</el-dropdown-item>
            <el-dropdown-item :icon="CircleCheck">Action 5</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-col>
    <el-col :span="8">
      <span class="demonstration">right click to trigger</span>
      <el-dropdown trigger="contextmenu">
        <span class="el-dropdown-link">
          Dropdown List<el-icon class="el-icon--right"><arrow-down /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item :icon="Plus">Action 1</el-dropdown-item>
            <el-dropdown-item :icon="CirclePlusFilled">
              Action 2
            </el-dropdown-item>
            <el-dropdown-item :icon="CirclePlus">Action 3</el-dropdown-item>
            <el-dropdown-item :icon="Check">Action 4</el-dropdown-item>
            <el-dropdown-item :icon="CircleCheck">Action 5</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import {
  ArrowDown,
  Check,
  CircleCheck,
  CirclePlus,
  CirclePlusFilled,
  Plus,
} from '@element-plus/icons-vue'
</script>

<style scoped>
.block-col-2 .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}

.block-col-2 .el-dropdown-link {
  display: flex;
  align-items: center;
}
</style>
```

---
