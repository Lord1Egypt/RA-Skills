---
name: "dropdown"
description: "Dropdown 下拉菜单 -- Element Plus Vue3 桌面端组件。Invoke when user needs Dropdown 下拉菜单 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/dropdown.html"
---

---

# Dropdown 下拉菜单 [​](#dropdown-下拉菜单)

更新日志待解决

24

将动作或菜单折叠到下拉菜单中。

## 基础用法 [​](#基础用法)

悬停在下拉菜单上以展开更多操作。

通过组件 `slot` 来设置下拉触发的元素以及需要通过具名 `slot` 为 `dropdown` 来设置下拉菜单。 默认情况下，只需要悬停在触发菜单的元素上即可，无需点击也会显示下拉菜单。

Dropdown List

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZHJvcGRvd24+XG4gICAgPHNwYW4gY2xhc3M9XCJlbC1kcm9wZG93bi1saW5rXCI+XG4gICAgICBEcm9wZG93biBMaXN0XG4gICAgICA8ZWwtaWNvbiBjbGFzcz1cImVsLWljb24tLXJpZ2h0XCI+XG4gICAgICAgIDxhcnJvdy1kb3duIC8+XG4gICAgICA8L2VsLWljb24+XG4gICAgPC9zcGFuPlxuICAgIDx0ZW1wbGF0ZSAjZHJvcGRvd24+XG4gICAgICA8ZWwtZHJvcGRvd24tbWVudT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWN0aW9uIDE8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPkFjdGlvbiAyPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gMzwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gZGlzYWJsZWQ+QWN0aW9uIDQ8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIGRpdmlkZWQ+QWN0aW9uIDU8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICA8L2VsLWRyb3Bkb3duLW1lbnU+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1kcm9wZG93bj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBBcnJvd0Rvd24gfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmV4YW1wbGUtc2hvd2Nhc2UgLmVsLWRyb3Bkb3duLWxpbmsge1xuICBjdXJzb3I6IHBvaW50ZXI7XG4gIGNvbG9yOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dropdown/basic-usage.vue)_

vue

```
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

隐藏源代码

## 位置 [​](#位置)

支持 6 个位置。

设置 `placement` 属性，使下拉菜单出现在不同位置。

topStart

top

topEnd

bottomStart

bottom

bottomEnd

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgaXRlbXMtY2VudGVyIGdhcC00XCI+XG4gICAgPGVsLWRyb3Bkb3duIHBsYWNlbWVudD1cInRvcC1zdGFydFwiPlxuICAgICAgPGVsLWJ1dHRvbj4gdG9wU3RhcnQgPC9lbC1idXR0b24+XG4gICAgICA8dGVtcGxhdGUgI2Ryb3Bkb3duPlxuICAgICAgICA8ZWwtZHJvcGRvd24tbWVudT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5UaGUgQWN0aW9uIDFzdDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5UaGUgQWN0aW9uIDJuZDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5UaGUgQWN0aW9uIDNyZDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPC9lbC1kcm9wZG93bi1tZW51PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWRyb3Bkb3duPlxuICAgIDxlbC1kcm9wZG93biBwbGFjZW1lbnQ9XCJ0b3BcIj5cbiAgICAgIDxlbC1idXR0b24+IHRvcCA8L2VsLWJ1dHRvbj5cbiAgICAgIDx0ZW1wbGF0ZSAjZHJvcGRvd24+XG4gICAgICAgIDxlbC1kcm9wZG93bi1tZW51PlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gMXN0PC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gMm5kPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gM3JkPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8L2VsLWRyb3Bkb3duLW1lbnU+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtZHJvcGRvd24+XG4gICAgPGVsLWRyb3Bkb3duIHBsYWNlbWVudD1cInRvcC1lbmRcIj5cbiAgICAgIDxlbC1idXR0b24+IHRvcEVuZCA8L2VsLWJ1dHRvbj5cbiAgICAgIDx0ZW1wbGF0ZSAjZHJvcGRvd24+XG4gICAgICAgIDxlbC1kcm9wZG93bi1tZW51PlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gMXN0PC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gMm5kPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gM3JkPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8L2VsLWRyb3Bkb3duLW1lbnU+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtZHJvcGRvd24+XG4gICAgPGVsLWRyb3Bkb3duIHBsYWNlbWVudD1cImJvdHRvbS1zdGFydFwiPlxuICAgICAgPGVsLWJ1dHRvbj4gYm90dG9tU3RhcnQgPC9lbC1idXR0b24+XG4gICAgICA8dGVtcGxhdGUgI2Ryb3Bkb3duPlxuICAgICAgICA8ZWwtZHJvcGRvd24tbWVudT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5UaGUgQWN0aW9uIDFzdDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5UaGUgQWN0aW9uIDJuZDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5UaGUgQWN0aW9uIDNyZDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPC9lbC1kcm9wZG93bi1tZW51PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWRyb3Bkb3duPlxuICAgIDxlbC1kcm9wZG93biBwbGFjZW1lbnQ9XCJib3R0b21cIj5cbiAgICAgIDxlbC1idXR0b24+IGJvdHRvbSA8L2VsLWJ1dHRvbj5cbiAgICAgIDx0ZW1wbGF0ZSAjZHJvcGRvd24+XG4gICAgICAgIDxlbC1kcm9wZG93bi1tZW51PlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gMXN0PC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gMm5kPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gM3JkPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8L2VsLWRyb3Bkb3duLW1lbnU+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtZHJvcGRvd24+XG4gICAgPGVsLWRyb3Bkb3duIHBsYWNlbWVudD1cImJvdHRvbS1lbmRcIj5cbiAgICAgIDxlbC1idXR0b24+IGJvdHRvbUVuZCA8L2VsLWJ1dHRvbj5cbiAgICAgIDx0ZW1wbGF0ZSAjZHJvcGRvd24+XG4gICAgICAgIDxlbC1kcm9wZG93bi1tZW51PlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gMXN0PC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gMm5kPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPlRoZSBBY3Rpb24gM3JkPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8L2VsLWRyb3Bkb3duLW1lbnU+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtZHJvcGRvd24+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dropdown/placements.vue)_

vue

```
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

隐藏源代码

## 触发对象 [​](#触发对象)

可使用按钮触发下拉菜单。

设置 `split-button` 属性来让触发下拉元素呈现为按钮组，左边是功能按钮，右边是触发下拉菜单的按钮，设置为 `true` 即可。 如果你想要在第三和第四个选项之间添加一个分隔符，你只需要为第四个选项添加一个 `divided` 的属性。

Dropdown List

Dropdown List

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgaXRlbXMtY2VudGVyXCI+XG4gICAgPGVsLWRyb3Bkb3duPlxuICAgICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiPlxuICAgICAgICBEcm9wZG93biBMaXN0PGVsLWljb24gY2xhc3M9XCJlbC1pY29uLS1yaWdodFwiPjxhcnJvdy1kb3duIC8+PC9lbC1pY29uPlxuICAgICAgPC9lbC1idXR0b24+XG4gICAgICA8dGVtcGxhdGUgI2Ryb3Bkb3duPlxuICAgICAgICA8ZWwtZHJvcGRvd24tbWVudT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gMTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gMjwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gMzwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gNDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gNTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPC9lbC1kcm9wZG93bi1tZW51PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWRyb3Bkb3duPlxuICAgIDxlbC1kcm9wZG93biBzcGxpdC1idXR0b24gdHlwZT1cInByaW1hcnlcIiBAY2xpY2s9XCJoYW5kbGVDbGlja1wiPlxuICAgICAgRHJvcGRvd24gTGlzdFxuICAgICAgPHRlbXBsYXRlICNkcm9wZG93bj5cbiAgICAgICAgPGVsLWRyb3Bkb3duLW1lbnU+XG4gICAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWN0aW9uIDE8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWN0aW9uIDI8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWN0aW9uIDM8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gZGl2aWRlZD5BY3Rpb24gNDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gNTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPC9lbC1kcm9wZG93bi1tZW51PlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWRyb3Bkb3duPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBBcnJvd0Rvd24gfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3QgaGFuZGxlQ2xpY2sgPSAoKSA9PiB7XG4gIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBuby1hbGVydFxuICBhbGVydCgnYnV0dG9uIGNsaWNrJylcbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmV4YW1wbGUtc2hvd2Nhc2UgLmVsLWRyb3Bkb3duICsgLmVsLWRyb3Bkb3duIHtcbiAgbWFyZ2luLWxlZnQ6IDE1cHg7XG59XG4uZXhhbXBsZS1zaG93Y2FzZSAuZWwtZHJvcGRvd24tbGluayB7XG4gIGN1cnNvcjogcG9pbnRlcjtcbiAgY29sb3I6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dropdown/triggering-element.vue)_

vue

```
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

隐藏源代码

## 触发方式 [​](#触发方式)

可以配置点击激活或者悬停激活。

将 `trigger` 属性设置为 click 即可， 默认为 `hover`。

hover to trigger

Dropdown List

right click to trigger

Dropdown List

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IGNsYXNzPVwiYmxvY2stY29sLTJcIj5cbiAgICA8ZWwtY29sIDpzcGFuPVwiOFwiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJkZW1vbnN0cmF0aW9uXCI+aG92ZXIgdG8gdHJpZ2dlcjwvc3Bhbj5cbiAgICAgIDxlbC1kcm9wZG93bj5cbiAgICAgICAgPHNwYW4gY2xhc3M9XCJlbC1kcm9wZG93bi1saW5rXCI+XG4gICAgICAgICAgRHJvcGRvd24gTGlzdDxlbC1pY29uIGNsYXNzPVwiZWwtaWNvbi0tcmlnaHRcIj48YXJyb3ctZG93biAvPjwvZWwtaWNvbj5cbiAgICAgICAgPC9zcGFuPlxuICAgICAgICA8dGVtcGxhdGUgI2Ryb3Bkb3duPlxuICAgICAgICAgIDxlbC1kcm9wZG93bi1tZW51PlxuICAgICAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gOmljb249XCJQbHVzXCI+QWN0aW9uIDE8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSA6aWNvbj1cIkNpcmNsZVBsdXNGaWxsZWRcIj5cbiAgICAgICAgICAgICAgQWN0aW9uIDJcbiAgICAgICAgICAgIDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIDppY29uPVwiQ2lyY2xlUGx1c1wiPkFjdGlvbiAzPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gOmljb249XCJDaGVja1wiPkFjdGlvbiA0PC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gOmljb249XCJDaXJjbGVDaGVja1wiPkFjdGlvbiA1PC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgIDwvZWwtZHJvcGRvd24tbWVudT5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgIDwvZWwtZHJvcGRvd24+XG4gICAgPC9lbC1jb2w+XG4gICAgPGVsLWNvbCA6c3Bhbj1cIjhcIj5cbiAgICAgIDxzcGFuIGNsYXNzPVwiZGVtb25zdHJhdGlvblwiPmNsaWNrIHRvIHRyaWdnZXI8L3NwYW4+XG4gICAgICA8ZWwtZHJvcGRvd24gdHJpZ2dlcj1cImNsaWNrXCI+XG4gICAgICAgIDxzcGFuIGNsYXNzPVwiZWwtZHJvcGRvd24tbGlua1wiPlxuICAgICAgICAgIERyb3Bkb3duIExpc3Q8ZWwtaWNvbiBjbGFzcz1cImVsLWljb24tLXJpZ2h0XCI+PGFycm93LWRvd24gLz48L2VsLWljb24+XG4gICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPHRlbXBsYXRlICNkcm9wZG93bj5cbiAgICAgICAgICA8ZWwtZHJvcGRvd24tbWVudT5cbiAgICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIDppY29uPVwiUGx1c1wiPkFjdGlvbiAxPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gOmljb249XCJDaXJjbGVQbHVzRmlsbGVkXCI+XG4gICAgICAgICAgICAgIEFjdGlvbiAyXG4gICAgICAgICAgICA8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSA6aWNvbj1cIkNpcmNsZVBsdXNcIj5BY3Rpb24gMzwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIDppY29uPVwiQ2hlY2tcIj5BY3Rpb24gNDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIDppY29uPVwiQ2lyY2xlQ2hlY2tcIj5BY3Rpb24gNTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICA8L2VsLWRyb3Bkb3duLW1lbnU+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLWRyb3Bkb3duPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnNwYW49XCI4XCI+XG4gICAgICA8c3BhbiBjbGFzcz1cImRlbW9uc3RyYXRpb25cIj5yaWdodCBjbGljayB0byB0cmlnZ2VyPC9zcGFuPlxuICAgICAgPGVsLWRyb3Bkb3duIHRyaWdnZXI9XCJjb250ZXh0bWVudVwiPlxuICAgICAgICA8c3BhbiBjbGFzcz1cImVsLWRyb3Bkb3duLWxpbmtcIj5cbiAgICAgICAgICBEcm9wZG93biBMaXN0PGVsLWljb24gY2xhc3M9XCJlbC1pY29uLS1yaWdodFwiPjxhcnJvdy1kb3duIC8+PC9lbC1pY29uPlxuICAgICAgICA8L3NwYW4+XG4gICAgICAgIDx0ZW1wbGF0ZSAjZHJvcGRvd24+XG4gICAgICAgICAgPGVsLWRyb3Bkb3duLW1lbnU+XG4gICAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSA6aWNvbj1cIlBsdXNcIj5BY3Rpb24gMTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIDppY29uPVwiQ2lyY2xlUGx1c0ZpbGxlZFwiPlxuICAgICAgICAgICAgICBBY3Rpb24gMlxuICAgICAgICAgICAgPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gOmljb249XCJDaXJjbGVQbHVzXCI+QWN0aW9uIDM8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSA6aWNvbj1cIkNoZWNrXCI+QWN0aW9uIDQ8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSA6aWNvbj1cIkNpcmNsZUNoZWNrXCI+QWN0aW9uIDU8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgICAgPC9lbC1kcm9wZG93bi1tZW51PlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgPC9lbC1kcm9wZG93bj5cbiAgICA8L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHtcbiAgQXJyb3dEb3duLFxuICBDaGVjayxcbiAgQ2lyY2xlQ2hlY2ssXG4gIENpcmNsZVBsdXMsXG4gIENpcmNsZVBsdXNGaWxsZWQsXG4gIFBsdXMsXG59IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uYmxvY2stY29sLTIgLmRlbW9uc3RyYXRpb24ge1xuICBkaXNwbGF5OiBibG9jaztcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3Itc2Vjb25kYXJ5KTtcbiAgZm9udC1zaXplOiAxNHB4O1xuICBtYXJnaW4tYm90dG9tOiAyMHB4O1xufVxuXG4uYmxvY2stY29sLTIgLmVsLWRyb3Bkb3duLWxpbmsge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dropdown/how-to-trigger.vue)_

vue

```
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

隐藏源代码

## 菜单隐藏方式 [​](#菜单隐藏方式)

可以通过 `hide-on-click` 属性来配置。

下拉菜单默认在点击菜单项后会被隐藏，将 hide-on-click 属性设置为 false 可以关闭此功能。

Dropdown List

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZHJvcGRvd24gOmhpZGUtb24tY2xpY2s9XCJmYWxzZVwiPlxuICAgIDxzcGFuIGNsYXNzPVwiZWwtZHJvcGRvd24tbGlua1wiPlxuICAgICAgRHJvcGRvd24gTGlzdDxlbC1pY29uIGNsYXNzPVwiZWwtaWNvbi0tcmlnaHRcIj48YXJyb3ctZG93biAvPjwvZWwtaWNvbj5cbiAgICA8L3NwYW4+XG4gICAgPHRlbXBsYXRlICNkcm9wZG93bj5cbiAgICAgIDxlbC1kcm9wZG93bi1tZW51PlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gMTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWN0aW9uIDI8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPkFjdGlvbiAzPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSBkaXNhYmxlZD5BY3Rpb24gNDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gZGl2aWRlZD5BY3Rpb24gNTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gZGl2aWRlZD5BY3Rpb24gNjwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgIDwvZWwtZHJvcGRvd24tbWVudT5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLWRyb3Bkb3duPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEFycm93RG93biB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG5cbjxzdHlsZSBzY29wZWQ+XG4uZXhhbXBsZS1zaG93Y2FzZSAuZWwtZHJvcGRvd24gKyAuZWwtZHJvcGRvd24ge1xuICBtYXJnaW4tbGVmdDogMTVweDtcbn1cbi5leGFtcGxlLXNob3djYXNlIC5lbC1kcm9wZG93bi1saW5rIHtcbiAgY3Vyc29yOiBwb2ludGVyO1xuICBjb2xvcjogdmFyKC0tZWwtY29sb3ItcHJpbWFyeSk7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dropdown/menu-hiding-behavior.vue)_

vue

```
<template>
  <el-dropdown :hide-on-click="false">
    <span class="el-dropdown-link">
      Dropdown List<el-icon class="el-icon--right"><arrow-down /></el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item>Action 1</el-dropdown-item>
        <el-dropdown-item>Action 2</el-dropdown-item>
        <el-dropdown-item>Action 3</el-dropdown-item>
        <el-dropdown-item disabled>Action 4</el-dropdown-item>
        <el-dropdown-item divided>Action 5</el-dropdown-item>
        <el-dropdown-item divided>Action 6</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script lang="ts" setup>
import { ArrowDown } from '@element-plus/icons-vue'
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

隐藏源代码

## 指令事件 [​](#指令事件)

点击菜单项后会触发事件，用户可以通过相应的菜单项 key 进行不同的操作。

Dropdown List

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZHJvcGRvd24gQGNvbW1hbmQ9XCJoYW5kbGVDb21tYW5kXCI+XG4gICAgPHNwYW4gY2xhc3M9XCJlbC1kcm9wZG93bi1saW5rXCI+XG4gICAgICBEcm9wZG93biBMaXN0PGVsLWljb24gY2xhc3M9XCJlbC1pY29uLS1yaWdodFwiPjxhcnJvdy1kb3duIC8+PC9lbC1pY29uPlxuICAgIDwvc3Bhbj5cbiAgICA8dGVtcGxhdGUgI2Ryb3Bkb3duPlxuICAgICAgPGVsLWRyb3Bkb3duLW1lbnU+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIGNvbW1hbmQ9XCJhXCI+QWN0aW9uIDE8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIGNvbW1hbmQ9XCJiXCI+QWN0aW9uIDI8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIGNvbW1hbmQ9XCJjXCI+QWN0aW9uIDM8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIGNvbW1hbmQ9XCJkXCIgZGlzYWJsZWQ+QWN0aW9uIDQ8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIGNvbW1hbmQ9XCJlXCIgZGl2aWRlZD5BY3Rpb24gNTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgIDwvZWwtZHJvcGRvd24tbWVudT5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLWRyb3Bkb3duPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IEVsTWVzc2FnZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcbmltcG9ydCB7IEFycm93RG93biB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5jb25zdCBoYW5kbGVDb21tYW5kID0gKGNvbW1hbmQ6IHN0cmluZyB8IG51bWJlciB8IG9iamVjdCkgPT4ge1xuICBFbE1lc3NhZ2UoYGNsaWNrIG9uIGl0ZW0gJHtjb21tYW5kfWApXG59XG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5leGFtcGxlLXNob3djYXNlIC5lbC1kcm9wZG93bi1saW5rIHtcbiAgY3Vyc29yOiBwb2ludGVyO1xuICBjb2xvcjogdmFyKC0tZWwtY29sb3ItcHJpbWFyeSk7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dropdown/command-event.vue)_

vue

```
<template>
  <el-dropdown @command="handleCommand">
    <span class="el-dropdown-link">
      Dropdown List<el-icon class="el-icon--right"><arrow-down /></el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="a">Action 1</el-dropdown-item>
        <el-dropdown-item command="b">Action 2</el-dropdown-item>
        <el-dropdown-item command="c">Action 3</el-dropdown-item>
        <el-dropdown-item command="d" disabled>Action 4</el-dropdown-item>
        <el-dropdown-item command="e" divided>Action 5</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'

const handleCommand = (command: string | number | object) => {
  ElMessage(`click on item ${command}`)
}
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

隐藏源代码

## 下拉方法 [​](#下拉方法)

您可以手动使用 `手动打开` 或 `手动关闭下拉菜单以打开或关闭`

open(close) the Dropdown list2 will close(open) the Dropdown List1.

show

Dropdown List1

Dropdown List2

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHN0eWxlPVwiZm9udC1zaXplOiAxNHB4XCI+XG4gICAgPHA+b3BlbihjbG9zZSkgdGhlIERyb3Bkb3duIGxpc3QyIHdpbGwgY2xvc2Uob3BlbikgdGhlIERyb3Bkb3duIExpc3QxLjwvcD5cbiAgPC9kaXY+XG4gIDxkaXYgc3R5bGU9XCJtYXJnaW46IDE1cHhcIj5cbiAgICA8ZWwtYnV0dG9uIEBjbGljaz1cInNob3dDbGlja1wiPnNob3c8L2VsLWJ1dHRvbj5cbiAgPC9kaXY+XG4gIDxlbC1kcm9wZG93biByZWY9XCJkcm9wZG93bjFcIiB0cmlnZ2VyPVwiY29udGV4dG1lbnVcIiBzdHlsZT1cIm1hcmdpbi1yaWdodDogMzBweFwiPlxuICAgIDxzcGFuIGNsYXNzPVwiZWwtZHJvcGRvd24tbGlua1wiPiBEcm9wZG93biBMaXN0MSA8L3NwYW4+XG4gICAgPHRlbXBsYXRlICNkcm9wZG93bj5cbiAgICAgIDxlbC1kcm9wZG93bi1tZW51PlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gMTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWN0aW9uIDI8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPkFjdGlvbiAzPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSBkaXNhYmxlZD5BY3Rpb24gNDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gZGl2aWRlZD5BY3Rpb24gNTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgIDwvZWwtZHJvcGRvd24tbWVudT5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLWRyb3Bkb3duPlxuXG4gIDxlbC1kcm9wZG93biB0cmlnZ2VyPVwiY29udGV4dG1lbnVcIiBAdmlzaWJsZS1jaGFuZ2U9XCJoYW5kbGVWaXNpYmxlMlwiPlxuICAgIDxzcGFuIGNsYXNzPVwiZWwtZHJvcGRvd24tbGlua1wiPiBEcm9wZG93biBMaXN0MiA8L3NwYW4+XG4gICAgPHRlbXBsYXRlICNkcm9wZG93bj5cbiAgICAgIDxlbC1kcm9wZG93bi1tZW51PlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gMTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWN0aW9uIDI8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPkFjdGlvbiAzPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSBkaXNhYmxlZD5BY3Rpb24gNDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gZGl2aWRlZD5BY3Rpb24gNTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgIDwvZWwtZHJvcGRvd24tbWVudT5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLWRyb3Bkb3duPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBEcm9wZG93bkluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBkcm9wZG93bjEgPSByZWY8RHJvcGRvd25JbnN0YW5jZT4oKVxuZnVuY3Rpb24gaGFuZGxlVmlzaWJsZTIodmlzaWJsZTogYW55KSB7XG4gIGlmICghZHJvcGRvd24xLnZhbHVlKSByZXR1cm5cbiAgaWYgKHZpc2libGUpIHtcbiAgICBkcm9wZG93bjEudmFsdWUuaGFuZGxlQ2xvc2UoKVxuICB9IGVsc2Uge1xuICAgIGRyb3Bkb3duMS52YWx1ZS5oYW5kbGVPcGVuKClcbiAgfVxufVxuZnVuY3Rpb24gc2hvd0NsaWNrKCkge1xuICBpZiAoIWRyb3Bkb3duMS52YWx1ZSkgcmV0dXJuXG4gIGRyb3Bkb3duMS52YWx1ZS5oYW5kbGVPcGVuKClcbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmV4YW1wbGUtc2hvd2Nhc2UgLmVsLWRyb3Bkb3duLWxpbmsge1xuICBjdXJzb3I6IHBvaW50ZXI7XG4gIGNvbG9yOiB2YXIoLS1lbC1jb2xvci1wcmltYXJ5KTtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dropdown/dropdown-methods.vue)_

vue

```
<template>
  <div style="font-size: 14px">
    <p>open(close) the Dropdown list2 will close(open) the Dropdown List1.</p>
  </div>
  <div style="margin: 15px">
    <el-button @click="showClick">show</el-button>
  </div>
  <el-dropdown ref="dropdown1" trigger="contextmenu" style="margin-right: 30px">
    <span class="el-dropdown-link"> Dropdown List1 </span>
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

  <el-dropdown trigger="contextmenu" @visible-change="handleVisible2">
    <span class="el-dropdown-link"> Dropdown List2 </span>
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

<script setup lang="ts">
import { ref } from 'vue'

import type { DropdownInstance } from 'element-plus'

const dropdown1 = ref<DropdownInstance>()
function handleVisible2(visible: any) {
  if (!dropdown1.value) return
  if (visible) {
    dropdown1.value.handleClose()
  } else {
    dropdown1.value.handleOpen()
  }
}
function showClick() {
  if (!dropdown1.value) return
  dropdown1.value.handleOpen()
}
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

隐藏源代码

## 尺寸 [​](#尺寸)

Dropdown 组件提供除了默认值以外的三种尺寸，可以在不同场景下选择合适的尺寸。

使用 `size` 属性配置尺寸，可选的尺寸大小有: `large`, `default` 或 `small`

Large

Default

Small

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtZHJvcGRvd24gc2l6ZT1cImxhcmdlXCIgc3BsaXQtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCI+XG4gICAgTGFyZ2VcbiAgICA8dGVtcGxhdGUgI2Ryb3Bkb3duPlxuICAgICAgPGVsLWRyb3Bkb3duLW1lbnU+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPkFjdGlvbiAxPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gMjwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWN0aW9uIDM8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPkFjdGlvbiA0PC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgPC9lbC1kcm9wZG93bi1tZW51PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtZHJvcGRvd24+XG5cbiAgPGVsLWRyb3Bkb3duIHNwbGl0LWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiPlxuICAgIERlZmF1bHRcbiAgICA8dGVtcGxhdGUgI2Ryb3Bkb3duPlxuICAgICAgPGVsLWRyb3Bkb3duLW1lbnU+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPkFjdGlvbiAxPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gMjwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWN0aW9uIDM8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPkFjdGlvbiA0PC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgPC9lbC1kcm9wZG93bi1tZW51PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtZHJvcGRvd24+XG5cbiAgPGVsLWRyb3Bkb3duIHNpemU9XCJzbWFsbFwiIHNwbGl0LWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiPlxuICAgIFNtYWxsXG4gICAgPHRlbXBsYXRlICNkcm9wZG93bj5cbiAgICAgIDxlbC1kcm9wZG93bi1tZW51PlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gMTwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0+QWN0aW9uIDI8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtPkFjdGlvbiAzPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbT5BY3Rpb24gNDwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgIDwvZWwtZHJvcGRvd24tbWVudT5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLWRyb3Bkb3duPlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlIHNjb3BlZD5cbi5leGFtcGxlLXNob3djYXNlIC5lbC1kcm9wZG93biArIC5lbC1kcm9wZG93biB7XG4gIG1hcmdpbi1sZWZ0OiAxNXB4O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dropdown/sizes.vue)_

vue

```
<template>
  <el-dropdown size="large" split-button type="primary">
    Large
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item>Action 1</el-dropdown-item>
        <el-dropdown-item>Action 2</el-dropdown-item>
        <el-dropdown-item>Action 3</el-dropdown-item>
        <el-dropdown-item>Action 4</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>

  <el-dropdown split-button type="primary">
    Default
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item>Action 1</el-dropdown-item>
        <el-dropdown-item>Action 2</el-dropdown-item>
        <el-dropdown-item>Action 3</el-dropdown-item>
        <el-dropdown-item>Action 4</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>

  <el-dropdown size="small" split-button type="primary">
    Small
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item>Action 1</el-dropdown-item>
        <el-dropdown-item>Action 2</el-dropdown-item>
        <el-dropdown-item>Action 3</el-dropdown-item>
        <el-dropdown-item>Action 4</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<style scoped>
.example-showcase .el-dropdown + .el-dropdown {
  margin-left: 15px;
}
</style>
```

隐藏源代码

## 虚拟触发2.11.3 [​](#虚拟触发)

有时候我们想把 dropdown 的触发元素放在别的地方，而不需要写在一起，这时候就可以使用虚拟触发。

Right click

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FyZFxuICAgIGNsYXNzPVwiY29udGVudFwiXG4gICAgYm9keS1jbGFzcz1cImNhcmQtYm9keVwiXG4gICAgQGNsaWNrPVwiaGFuZGxlQ2xpY2tcIlxuICAgIEBjb250ZXh0bWVudT1cImhhbmRsZUNvbnRleHRtZW51XCJcbiAgPlxuICAgIFJpZ2h0IGNsaWNrXG4gIDwvZWwtY2FyZD5cbiAgPGVsLWRyb3Bkb3duXG4gICAgcmVmPVwiZHJvcGRvd25SZWZcIlxuICAgIDp2aXJ0dWFsLXJlZj1cInRyaWdnZXJSZWZcIlxuICAgIDpzaG93LWFycm93PVwiZmFsc2VcIlxuICAgIDpwb3BwZXItb3B0aW9ucz1cIntcbiAgICAgIG1vZGlmaWVyczogW3sgbmFtZTogJ29mZnNldCcsIG9wdGlvbnM6IHsgb2Zmc2V0OiBbMCwgMF0gfSB9XSxcbiAgICB9XCJcbiAgICB2aXJ0dWFsLXRyaWdnZXJpbmdcbiAgICB0cmlnZ2VyPVwiY29udGV4dG1lbnVcIlxuICAgIHBsYWNlbWVudD1cImJvdHRvbS1zdGFydFwiXG4gID5cbiAgICA8dGVtcGxhdGUgI2Ryb3Bkb3duPlxuICAgICAgPGVsLWRyb3Bkb3duLW1lbnU+XG4gICAgICAgIDxlbC1kcm9wZG93bi1pdGVtIDppY29uPVwiUGx1c1wiPkFjdGlvbiAxPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSA6aWNvbj1cIkNpcmNsZVBsdXNGaWxsZWRcIj4gQWN0aW9uIDIgPC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSA6aWNvbj1cIkNpcmNsZVBsdXNcIj5BY3Rpb24gMzwvZWwtZHJvcGRvd24taXRlbT5cbiAgICAgICAgPGVsLWRyb3Bkb3duLWl0ZW0gOmljb249XCJDaGVja1wiPkFjdGlvbiA0PC9lbC1kcm9wZG93bi1pdGVtPlxuICAgICAgICA8ZWwtZHJvcGRvd24taXRlbSA6aWNvbj1cIkNpcmNsZUNoZWNrXCI+QWN0aW9uIDU8L2VsLWRyb3Bkb3duLWl0ZW0+XG4gICAgICA8L2VsLWRyb3Bkb3duLW1lbnU+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1kcm9wZG93bj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQge1xuICBDaGVjayxcbiAgQ2lyY2xlQ2hlY2ssXG4gIENpcmNsZVBsdXMsXG4gIENpcmNsZVBsdXNGaWxsZWQsXG4gIFBsdXMsXG59IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5pbXBvcnQgdHlwZSB7IERyb3Bkb3duSW5zdGFuY2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGRyb3Bkb3duUmVmID0gcmVmPERyb3Bkb3duSW5zdGFuY2U+KClcbmNvbnN0IHBvc2l0aW9uID0gcmVmKHtcbiAgdG9wOiAwLFxuICBsZWZ0OiAwLFxuICBib3R0b206IDAsXG4gIHJpZ2h0OiAwLFxufSBhcyBET01SZWN0KVxuXG5jb25zdCB0cmlnZ2VyUmVmID0gcmVmKHtcbiAgZ2V0Qm91bmRpbmdDbGllbnRSZWN0OiAoKSA9PiBwb3NpdGlvbi52YWx1ZSxcbn0pXG5cbmNvbnN0IGhhbmRsZUNsaWNrID0gKCkgPT4ge1xuICBkcm9wZG93blJlZi52YWx1ZT8uaGFuZGxlQ2xvc2UoKVxufVxuXG5jb25zdCBoYW5kbGVDb250ZXh0bWVudSA9IChldmVudDogTW91c2VFdmVudCkgPT4ge1xuICBjb25zdCB7IGNsaWVudFgsIGNsaWVudFkgfSA9IGV2ZW50XG4gIHBvc2l0aW9uLnZhbHVlID0gRE9NUmVjdC5mcm9tUmVjdCh7XG4gICAgeDogY2xpZW50WCxcbiAgICB5OiBjbGllbnRZLFxuICB9KVxuICBldmVudC5wcmV2ZW50RGVmYXVsdCgpXG4gIGRyb3Bkb3duUmVmLnZhbHVlPy5oYW5kbGVPcGVuKClcbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmNvbnRlbnQge1xuICBkaXNwbGF5OiBmbGV4O1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAgaGVpZ2h0OiAyMDBweDtcbn1cblxuLmNvbnRlbnQgOmRlZXAoLmNhcmQtYm9keSkge1xuICBmbGV4LWdyb3c6IDA7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/dropdown/virtual-trigger.vue)_

vue

```
<template>
  <el-card
    class="content"
    body-class="card-body"
    @click="handleClick"
    @contextmenu="handleContextmenu"
  >
    Right click
  </el-card>
  <el-dropdown
    ref="dropdownRef"
    :virtual-ref="triggerRef"
    :show-arrow="false"
    :popper-options="{
      modifiers: [{ name: 'offset', options: { offset: [0, 0] } }],
    }"
    virtual-triggering
    trigger="contextmenu"
    placement="bottom-start"
  >
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item :icon="Plus">Action 1</el-dropdown-item>
        <el-dropdown-item :icon="CirclePlusFilled"> Action 2 </el-dropdown-item>
        <el-dropdown-item :icon="CirclePlus">Action 3</el-dropdown-item>
        <el-dropdown-item :icon="Check">Action 4</el-dropdown-item>
        <el-dropdown-item :icon="CircleCheck">Action 5</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import {
  Check,
  CircleCheck,
  CirclePlus,
  CirclePlusFilled,
  Plus,
} from '@element-plus/icons-vue'

import type { DropdownInstance } from 'element-plus'

const dropdownRef = ref<DropdownInstance>()
const position = ref({
  top: 0,
  left: 0,
  bottom: 0,
  right: 0,
} as DOMRect)

const triggerRef = ref({
  getBoundingClientRect: () => position.value,
})

const handleClick = () => {
  dropdownRef.value?.handleClose()
}

const handleContextmenu = (event: MouseEvent) => {
  const { clientX, clientY } = event
  position.value = DOMRect.fromRect({
    x: clientX,
    y: clientY,
  })
  event.preventDefault()
  dropdownRef.value?.handleOpen()
}
</script>

<style scoped>
.content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.content :deep(.card-body) {
  flex-grow: 0;
}
</style>
```

隐藏源代码

## Dropdown API [​](#dropdown-api)

### Dropdown Attributes [​](#dropdown-attributes)

| 属性名 | 说明 | 类型 | Default |
| --- | --- | --- | --- |
| type | 菜单按钮类型，同 `Button` 组件一样，仅在 `split-button` 为 true 的情况下有效。 | `enum` | '' |
| size | 菜单尺寸，在 split-button 为 true 的情况下也对触发按钮生效。 | `enum` | '' |
| button-props | 按钮组件的 props，参考 [按钮属性](https://element-plus.org/zh-CN/component/button.html#button-attributes) | `object` | — |
| max-height | 菜单最大高度 | `string` / `number` | '' |
| split-button | 下拉触发元素呈现为按钮组 | `boolean` | false |
| disabled | 是否禁用 | `boolean` | false |
| placement | 菜单弹出位置 | `enum` | bottom |
| effect | Tooltip 主题，内置了 `dark` / `light` 两种主题 | `enum` / `string` | light |
| trigger | 触发下拉的行为 | `enum` / `array` | hover |
| trigger-keys 2.9.1 | 指定键盘上哪些按键可以触发操作 | `array` | `['Enter', 'Space', 'ArrowDown', 'NumpadEnter']` |
| virtual-triggering 2.11.3 | 是否启用虚拟触发器 | `boolean` | — |
| virtual-ref 2.11.3 | 指示下拉框所依附的参考元素 | `HTMLElement` | — |
| hide-on-click | 是否在点击菜单项后隐藏菜单 | `boolean` | true |
| show-arrow 2.11.3 | tooltip 的内容是否有箭头 | `boolean` | true |
| show-timeout | 展开下拉菜单的延时，仅在 trigger 为 hover 时有效 | `number` | 150 |
| hide-timeout | 收起下拉菜单的延时（仅在 trigger 为 hover 时有效） | `number` | 150 |
| role | 下拉菜单的 ARIA 属性。 根据具体场景，您可能想要将此更改为“navigation” | `enum` | menu |
| tabindex | Dropdown 组件的 [tabindex](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/tabindex) | `number` / `string` | 0 |
| popper-class | 自定义浮层类名 | `string` / `object` | '' |
| popper-style 2.11.5 | 自定义浮层类名 | `string` / `object` | — |
| popper-options | [popper.js](https://popper.js.org/docs/v2/) 参数 | `object` | `{modifiers: [{name: 'computeStyles',options: {gpuAcceleration: false}}]}` |
| teleported 2.2.20 | 是否将下拉列表插入至 body 元素 | `boolean` | true |
| append-to 2.13.0 | dropdown 的内容将挂载到哪一个元素上 | `CSSSelector` / `HTMLElement` | — |
| persistent 2.9.5 | 当下拉菜单处于非活动状态且 `persistent` 为 `false` 时，下拉菜单将被销毁 | `boolean` | true |

### Dropdown Slots [​](#dropdown-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 下拉菜单的内容。 注意：必须是有效的 html DOM 元素（例如 `<span>、<button>` 等）或 `el-component`，以附加监听触发器 | ::: |
| dropdown | 下拉列表，通常是 `<el-dropdown-menu>` 组件 | Dropdown-Menu |

### Dropdown Events [​](#dropdown-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| click | `split-button` 为 true 时，点击左侧按钮的回调 | `Function` |
| command | 当下拉项被点击时触发，参数是从下拉菜单中发送的命令 | `Function` |
| visible-change | 当下拉菜单出现/消失时触发器, 当它出现时, 参数将是 `true`, 否则将是 `false` | `Function` |

### Dropdown Exposes [​](#dropdown-exposes)

| 方法名 | 说明 | Type |
| --- | --- | --- |
| handleOpen | 打开下拉菜单 | `Function` |
| handleClose | 关闭下拉菜单 | `Function` |

## Dropdown-Menu API [​](#dropdown-menu-api)

### Dropdown-Menu Slots [​](#dropdown-menu-slots)

| 插槽名 | 说明 | 子标签 |
| --- | --- | --- |
| default | 下拉菜单的内容 | Dropdown-Item |

## Dropdown-Item API [​](#dropdown-item-api)

### Dropdown-Item Attributes [​](#dropdown-item-attributes)

| 属性名 | 说明 | Type | 默认值 |
| --- | --- | --- | --- |
| command | 派发到`command`回调函数的指令参数 | `string` / `number` / `object` | — |
| disabled | 是否禁用 | `boolean` | false |
| divided | 是否显示分隔符 | `boolean` | false |
| icon | 自定义图标 | `string` / `Component` | — |

### Dropdown-Item Slots [​](#dropdown-item-slots)

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义Dropdown-Item内容 |
| icon 2.13.1 | 自定义图标，它将覆盖图标prop |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/dropdown) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/dropdown.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/dropdown.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/57086651?v=4&size=64)](https://github.com/Simon-He95)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23609695?v=4&size=64)](https://github.com/shooterRao)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/21095710?v=4&size=64)](https://github.com/zouhangwithsweet)[![](https://avatars.githubusercontent.com/u/62818957?v=4&size=64)](https://github.com/ZacharyBear)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/134212703?v=4&size=64)](https://github.com/ydkdev)[![](https://avatars.githubusercontent.com/u/31850793?v=4&size=64)](https://github.com/ModyQyW)[![](https://avatars.githubusercontent.com/u/4075314?v=4&size=64)](https://github.com/Giwayume)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/66702442?v=4&size=64)](https://github.com/danny-hebert)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/44260795?v=4&size=64)](https://github.com/iwusong)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/49612241?v=4&size=64)](https://github.com/mawi1512)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/18509404?v=4&size=64)](https://github.com/inottn)[![](https://avatars.githubusercontent.com/u/32129111?v=4&size=64)](https://github.com/Vgbire)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/36978416?v=4&size=64)](https://github.com/SimonaliaChen)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/216826433?v=4&size=64)](https://github.com/vsqaq)[![](https://avatars.githubusercontent.com/u/171831965?v=4&size=64)](https://github.com/allenxu09)[![](https://avatars.githubusercontent.com/u/188531008?v=4&size=64)](https://github.com/dengguangmiaoyyds)[![](https://avatars.githubusercontent.com/u/234136872?v=4&size=64)](https://github.com/z-kunf)[![](https://avatars.githubusercontent.com/u/15611493?v=4&size=64)](https://github.com/smallbonelu)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)[![](https://avatars.githubusercontent.com/u/65441198?v=4&size=64)](https://github.com/tyj-321)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/60056876?v=4&size=64)](https://github.com/LinZhanMing)

[Breadcrumb 面包屑](https://element-plus.org/zh-CN/component/breadcrumb)

[Menu 菜单](https://element-plus.org/zh-CN/component/menu)


