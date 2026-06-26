# a-dropdown 下拉菜单

用于操作聚合，减少按钮数量。

## 基本用法

```vue
<a-dropdown trigger="click">
  <a-button type="primary" size="small">
    更多 <icon-down />
  </a-button>
  <template #content>
    <a-doption @click="handleEdit(record)">编辑</a-doption>
    <a-doption @click="handleView(record)">查看</a-doption>
    <a-doption @click="handleDelete(record)">
      <span style="color: rgb(var(--danger-6))">删除</span>
    </a-doption>
  </template>
</a-dropdown>
```

## 表格操作列（多操作）

```vue
<template #action="{ record }">
  <a-space>
    <a-button type="primary" size="small" @click="handleEdit(record)">编辑</a-button>
    <a-dropdown>
      <a-button type="outline" size="small">更多 <icon-down /></a-button>
      <template #content>
        <a-doption @click="handleViewSecret(record)">查看密钥</a-doption>
        <a-doption @click="handleResetSecret(record)">重置密钥</a-doption>
        <a-doption @click="handleDelete(record)">删除</a-doption>
      </template>
    </a-dropdown>
  </a-space>
</template>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `trigger` | 触发方式 `click` / `hover`(默认) |

## 项目参考

- `src/components/navbar/index.vue` — 用户菜单下拉
- `src/views/supplier/index.vue` — 表格操作下拉
