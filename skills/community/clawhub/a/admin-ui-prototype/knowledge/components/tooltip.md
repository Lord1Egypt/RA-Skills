# a-tooltip 文字提示

鼠标悬浮显示提示信息。

## 基本用法

```vue
<a-tooltip content="这是提示内容">
  <span>悬浮查看</span>
</a-tooltip>
```

## 动态内容

```vue
<a-tooltip :content="record.routes.map(r => r.name).join('; ')">
  <span class="text-ellipsis">{{ record.routeSummary }}</span>
</a-tooltip>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `content` | 提示文本 |
| `position` | 位置（`top` / `bottom` / `left` / `right`） |

## 项目参考

- `src/views/policy/published-fare/index.vue` — 表格内长文本提示
- `src/views/system/oidc/oauth-client/index.vue` — 端点描述提示
