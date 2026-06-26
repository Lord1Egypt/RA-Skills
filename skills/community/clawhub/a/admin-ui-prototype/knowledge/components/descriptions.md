# a-descriptions 描述列表

用于详情页展示键值对信息。

## 基本用法

```vue
<a-descriptions :column="2" bordered>
  <a-descriptions-item label="客户端名称">{{ detail.name }}</a-descriptions-item>
  <a-descriptions-item label="状态">
    <a-tag :color="detail.status === 1 ? 'green' : 'red'">
      {{ detail.status === 1 ? '启用' : '禁用' }}
    </a-tag>
  </a-descriptions-item>
  <a-descriptions-item label="创建时间">{{ detail.createTime }}</a-descriptions-item>
</a-descriptions>
```

## 单列布局

```vue
<a-descriptions :column="1" bordered>
  <a-descriptions-item label="Client ID">
    <div style="display: flex; align-items: center; gap: 8px">
      <span>{{ detail.clientId }}</span>
      <a-button type="text" size="small" @click="copy(detail.clientId)">
        <icon-copy />
      </a-button>
    </div>
  </a-descriptions-item>
</a-descriptions>
```

## 控制标签宽度

```vue
<a-descriptions :column="3" bordered :label-style="{ width: '150px' }">
  ...
</a-descriptions>
```

## 常用 Props

| Prop | 值 | 说明 |
|---|---|---|
| `column` | `1` / `2` / `3` | 每行显示列数 |
| `bordered` | — | 带边框样式 |
| `size` | `small` / 默认 | 紧凑尺寸 |
| `label-style` | `{ width: '150px' }` | 标签列宽度 |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 密钥信息 + 端点信息
- `src/views/policy/published-fare/index.vue` — 三列描述列表
