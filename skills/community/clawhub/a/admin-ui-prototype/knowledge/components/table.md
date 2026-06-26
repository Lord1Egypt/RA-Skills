# a-table 数据表格

列表页核心组件，用于展示分页数据、自定义列渲染和行操作。

## 基本用法

```vue
<a-table
  row-key="id"
  :columns="columns"
  :loading="req.loading"
  :data="data"
  :pagination="req.pagination"
  :scroll="{ x: 1200 }"
  @page-change="setPageChange"
  @page-size-change="setSizeChange"
>
  <template #status="{ record }">
    <a-tag :color="record.status === 1 ? 'green' : 'red'">
      {{ record.status === 1 ? '启用' : '禁用' }}
    </a-tag>
  </template>
  <template #action="{ record }">
    <a-space>
      <a-button type="primary" size="small" @click="handleEdit(record)">编辑</a-button>
      <a-button type="outline" status="danger" size="small" @click="handleDelete(record)">删除</a-button>
    </a-space>
  </template>
</a-table>
```

## 列定义

```typescript
const columns = [
  { title: '名称', dataIndex: 'name', width: 150 },           // 直接渲染字段
  { title: '状态', slotName: 'status', width: 80 },            // 自定义插槽渲染
  { title: '操作', slotName: 'action', width: 200, fixed: 'right' as const }, // 固定右侧
];
```

- `dataIndex`: 直接显示字段值
- `slotName`: 使用 `<template #slotName="{ record }">` 自定义渲染
- `fixed: 'right' as const`: 固定列（需配合 `:scroll="{ x: number }"`)
- `width`: 必须指定，保证对齐

## 分页

```typescript
const req = ref({
  loading: false,
  pagination: { current: 1, pageSize: 10, total: 0 },
});

const setPageChange = (val: number) => {
  req.value.pagination.current = val;
  getList();
};

const setSizeChange = (val: number) => {
  req.value.pagination.pageSize = val;
  req.value.pagination.current = 1;
  getList();
};
```

## 常用 Props

| Prop | 类型 | 说明 |
|---|---|---|
| `row-key` | `string` | 行唯一标识字段，通常为 `"id"` |
| `columns` | `TableColumnData[]` | 列配置数组 |
| `data` | `any[]` | 表格数据 |
| `loading` | `boolean` | 加载状态 |
| `pagination` | `PaginationProps` | 分页配置 `{ current, pageSize, total }` |
| `scroll` | `{ x?: number; y?: number }` | 横向/纵向滚动 |
| `stripe` | `boolean` | 斑马纹 |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 标准列表页
- `src/views/policy/published-fare/index.vue` — 复杂列表页（多 slot）
- `src/views/log/business-log/index.vue` — 带斑马纹表格
