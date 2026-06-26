# a-spin 加载遮罩

包裹内容，显示加载状态。

## 基本用法

```vue
<a-spin :loading="loading">
  <div>页面内容</div>
</a-spin>
```

## 带提示文案

```vue
<a-spin :loading="loading" tip="正在加载中..." :size="48">
  <div>内容区域</div>
</a-spin>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `loading` | 是否显示加载 |
| `tip` | 提示文案 |
| `size` | 图标大小 |

## 注意

表格加载使用 `a-table` 的 `:loading` prop，不需要额外包裹 `a-spin`。`a-spin` 主要用于表单、详情页等非表格场景。
