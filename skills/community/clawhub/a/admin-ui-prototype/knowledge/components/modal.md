# a-modal 对话框

用于 CRUD 操作的弹窗，包裹子组件表单。

## 基本用法

```vue
<a-modal
  v-if="editModal.visible"
  draggable
  :align-center="false"
  :top="60"
  :mask-closable="false"
  width="700px"
  :footer="false"
  v-model:visible="editModal.visible"
  @cancel="handleModalClose(false)"
>
  <template #title>{{ editModal.isEdit ? '编辑' : '新增' }}</template>
  <EditComponent
    :item-id="editModal.itemId"
    :is-edit="editModal.isEdit"
    @close="handleModalClose"
  />
</a-modal>
```

## 状态管理

```typescript
const editModal = ref({
  visible: false,
  itemId: 0,
  isEdit: false,
});

// 打开
const handleEdit = (record: ItemDTO) => {
  editModal.value.itemId = record.id;
  editModal.value.isEdit = true;
  editModal.value.visible = true;
};

// 关闭（子组件 emit 触发）
const handleModalClose = (shouldRefresh: boolean) => {
  editModal.value.visible = false;
  editModal.value.itemId = 0;
  editModal.value.isEdit = false;
  if (shouldRefresh) getList();
};
```

## 子组件通信

```typescript
// 子组件
interface Emits {
  (e: 'close', shouldRefresh: boolean): void;
}
const emit = defineEmits<Emits>();

// 提交成功后
emit('close', true);  // true = 刷新列表

// 取消
emit('close', false);
```

## 常用 Props

| Prop | 值 | 说明 |
|---|---|---|
| `v-if` | `modal.visible` | 每次打开重新创建组件 |
| `draggable` | — | 允许拖拽移动 |
| `:align-center` | `false` | 不居中，配合 `:top` 使用 |
| `:top` | `60` | 距顶部距离（px） |
| `:mask-closable` | `false` | 点击遮罩不关闭 |
| `width` | `"700px"` / `"1000px"` | 弹窗宽度 |
| `:footer` | `false` | 隐藏默认底部按钮（表单自带提交按钮） |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 标准编辑弹窗
- `src/views/supplier/index.vue` — 多弹窗管理
- `src/views/policy/published-fare/index.vue` — 大尺寸详情弹窗
