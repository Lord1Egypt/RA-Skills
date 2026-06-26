# a-switch 开关

用于状态切换，常配合确认弹窗使用。

## 表格内开关（带确认）

```vue
<template #status="{ record }">
  <a-switch
    :model-value="record.status === 1"
    @change="(val: string | number | boolean) => handleToggle(record, Boolean(val))"
  >
    <template #checked>启用</template>
    <template #unchecked>禁用</template>
  </a-switch>
</template>
```

```typescript
const handleToggle = (record: ItemDTO, checked: boolean) => {
  const action = checked ? '启用' : '禁用';
  Modal.confirm({
    title: `确认${action}`,
    content: `确定要${action}"${record.name}"吗？`,
    onOk: () => {
      // API 调用
      switchStatus(record.id, checked ? 1 : 0).then(() => {
        Notification.success(`${action}成功`);
        getList();
      });
    },
    onCancel: () => getList(), // 恢复原状态
  });
};
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `model-value` | 绑定值（boolean） |
| `@change` | 值变化事件 |
| `#checked` | 开启时文本 |
| `#unchecked` | 关闭时文本 |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 客户端状态切换
- `src/views/policy/published-fare/index.vue` — 有效/无效切换
