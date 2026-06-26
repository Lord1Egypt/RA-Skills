# a-tag 标签

用于状态标识和分类展示。

## 状态标签（条件颜色）

```vue
<a-tag :color="record.status === 1 ? 'green' : 'red'">
  {{ record.status === 1 ? '启用' : '禁用' }}
</a-tag>
```

## 分类标签（循环渲染）

```vue
<a-space wrap>
  <a-tag v-for="type in record.types" :key="type" size="small" color="arcoblue">
    {{ typeMap[type] || type }}
  </a-tag>
</a-space>
```

## 动态颜色映射

```typescript
const getLevelColor = (level: string) => {
  const map: Record<string, string> = {
    info: 'blue',
    warning: 'orange',
    error: 'red',
    success: 'green',
  };
  return map[level] || 'gray';
};
```

```vue
<a-tag :color="getLevelColor(record.level)" size="small">
  {{ record.level }}
</a-tag>
```

## 常用 Props

| Prop | 值 | 说明 |
|---|---|---|
| `color` | `green` / `red` / `blue` / `arcoblue` / `orange` / `gray` | 预设颜色 |
| `size` | `small` / 默认 | 尺寸 |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 分类标签循环
- `src/views/log/business-log/index.vue` — 动态颜色映射
