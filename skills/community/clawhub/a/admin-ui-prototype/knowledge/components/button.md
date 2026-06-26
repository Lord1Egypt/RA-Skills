# a-button 按钮

操作触发组件，支持多种类型和状态。

## 按钮类型

```vue
<!-- 主要按钮 -->
<a-button type="primary" @click="handleSubmit">提交</a-button>

<!-- 描边按钮 -->
<a-button type="outline" @click="handleCancel">取消</a-button>

<!-- 文本按钮 -->
<a-button type="text" size="small" @click="handleCopy">
  <icon-copy />
</a-button>

<!-- 默认按钮 -->
<a-button @click="handleReset">重置</a-button>
```

## 危险按钮

```vue
<a-button type="outline" status="danger" size="small" @click="handleDelete(record)">
  删除
</a-button>

<a-button type="outline" status="warning" size="small" @click="handleReset(record)">
  重置
</a-button>
```

## 加载状态

```vue
<a-button type="primary" :loading="submitLoading" @click="handleSubmit">
  保存
</a-button>
```

## 圆形图标按钮

```vue
<a-button type="text" :shape="'circle'">
  <template #icon><icon-settings /></template>
</a-button>
```

## 操作栏组合

```vue
<a-space>
  <a-button type="primary" @click="handleSearch">搜索</a-button>
  <a-button @click="handleReset">重置</a-button>
  <a-divider direction="vertical" />
  <a-button type="primary" @click="handleAdd">新增</a-button>
</a-space>
```

## 表格操作列

```vue
<template #action="{ record }">
  <a-space>
    <a-button type="primary" size="small" @click="handleEdit(record)">编辑</a-button>
    <a-button type="outline" size="small" @click="handleView(record)">查看</a-button>
    <a-button type="outline" status="danger" size="small" @click="handleDelete(record)">删除</a-button>
  </a-space>
</template>
```

## 常用 Props

| Prop | 值 | 说明 |
|---|---|---|
| `type` | `primary` / `outline` / `text` / 默认 | 按钮样式 |
| `status` | `danger` / `warning` / `success` | 状态颜色 |
| `size` | `small` / `mini` / 默认 | 尺寸 |
| `loading` | `boolean` | 加载中 |
| `shape` | `'circle'` | 圆形 |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 操作栏 + 表格操作
- `src/components/navbar/index.vue` — 圆形图标按钮
