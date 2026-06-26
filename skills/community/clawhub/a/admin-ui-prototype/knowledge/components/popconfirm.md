# a-popconfirm 气泡确认

轻量确认，替代 Modal.confirm 用于简单操作。

## 基本用法

```vue
<a-popconfirm content="确认删除该记录？" @ok="handleDelete(record)">
  <a-button type="outline" status="danger" size="small">删除</a-button>
</a-popconfirm>
```

## 指定位置

```vue
<a-popconfirm position="top" content="确认永久删除？" @ok="onDelete(record)">
  <a-button type="text" status="danger" size="small">
    <icon-delete />
  </a-button>
</a-popconfirm>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `content` | 确认文案 |
| `position` | 弹出位置（`top` / `bottom` / `left` / `right`） |
| `@ok` | 确认回调 |
| `@cancel` | 取消回调 |

## 何时使用

- 简单的删除/状态切换：用 `a-popconfirm`
- 需要展示详细信息的确认：用 `Modal.confirm`

## 项目参考

- `src/views/system/api-compare/index.vue` — 删除规则确认
