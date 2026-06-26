# a-divider 分割线

用于表单分区和内容分隔。

## 表单分区标题

```vue
<a-divider orientation="left">基本信息</a-divider>
```

## 操作栏分隔

```vue
<a-space>
  <a-button type="primary">搜索</a-button>
  <a-button>重置</a-button>
  <a-divider direction="vertical" />
  <a-button type="primary">新增</a-button>
</a-space>
```

## 常用 Props

| Prop | 值 | 说明 |
|---|---|---|
| `orientation` | `left` / `center` / `right` | 文字位置 |
| `direction` | `vertical` / `horizontal`(默认) | 方向 |
