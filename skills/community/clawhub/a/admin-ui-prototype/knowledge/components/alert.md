# a-alert 提示信息

内联提示，用于重要信息说明。

## 基本用法

```vue
<a-alert type="info" style="margin-top: 12px">
  <template #icon><icon-info-circle /></template>
  这是一段提示信息。
</a-alert>
```

## 可关闭提示

```vue
<a-alert type="info" closable>
  操作说明：请先选择渠道再进行查询。
</a-alert>
```

## 警告提示

```vue
<a-alert type="warning" style="margin-top: 16px">
  请妥善保管密钥，丢失后需要重新生成。
</a-alert>
```

## 常用 Props

| Prop | 值 | 说明 |
|---|---|---|
| `type` | `info` / `warning` / `error` / `success` | 提示类型 |
| `closable` | — | 可关闭 |
| `#icon` | — | 自定义图标插槽 |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 多种 alert 类型
- `src/views/tools/domestic-channel/index.vue` — 可关闭提示
