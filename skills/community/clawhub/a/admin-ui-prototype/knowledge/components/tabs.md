# a-tabs 标签页

用于内容分类切换。

## 基本用法

```vue
<a-tabs v-model:active-key="activeTab">
  <a-tab-pane key="basic" title="基本信息">
    基本信息内容
  </a-tab-pane>
  <a-tab-pane key="detail" title="详细信息">
    详细信息内容
  </a-tab-pane>
</a-tabs>
```

## 圆角标签页

```vue
<a-tabs v-model:active-key="activeTab" type="rounded" destroy-on-hide>
  <a-tab-pane key="tab1" title="视图一">...</a-tab-pane>
  <a-tab-pane key="tab2" title="视图二">...</a-tab-pane>
</a-tabs>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `v-model:active-key` | 当前选中标签 |
| `type` | `rounded` 圆角风格 |
| `destroy-on-hide` | 切换时销毁隐藏的面板 |
| `default-active-key` | 默认选中（不受控） |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 密钥弹窗内标签页
- `src/views/tools/domestic-channel/index.vue` — 圆角标签页
