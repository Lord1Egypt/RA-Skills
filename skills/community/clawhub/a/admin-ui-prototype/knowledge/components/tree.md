# a-tree 树形组件

用于权限配置、分类选择等层级数据。

## 带复选框

```vue
<a-tree
  v-model:checked-keys="checkedKeys"
  :data="permissionTree"
  checkable
  :check-strictly="false"
  :default-expand-all="true"
/>
```

## 数据格式

```typescript
const permissionTree = [
  {
    title: '系统管理',
    key: 'system',
    children: [
      { title: '用户管理', key: 'system:user' },
      { title: '角色管理', key: 'system:role' },
    ],
  },
];
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `data` | 树数据 `{ title, key, children }[]` |
| `checkable` | 显示复选框 |
| `v-model:checked-keys` | 选中的 key 数组 |
| `check-strictly` | `false` 父子联动，`true` 独立选择 |
| `default-expand-all` | 默认展开全部 |

## 项目参考

- `src/views/supplier/sub-account/components/account-edit-modal.vue` — 权限树
