# a-space 间距容器

控制子元素间距和排列方向。

## 垂直布局（页面外层）

```vue
<a-space direction="vertical" fill>
  <div class="toolbar">...</div>
  <a-table ... />
  <a-modal ... />
</a-space>
```

## 水平布局（按钮组）

```vue
<a-space>
  <a-button type="primary">搜索</a-button>
  <a-button>重置</a-button>
</a-space>
```

## 自定义间距

```vue
<a-space :size="8">
  <a-tag>标签1</a-tag>
  <a-tag>标签2</a-tag>
</a-space>
```

## 换行

```vue
<a-space wrap>
  <a-tag v-for="item in tags" :key="item">{{ item }}</a-tag>
</a-space>
```

## 常用 Props

| Prop | 值 | 说明 |
|---|---|---|
| `direction` | `vertical` / `horizontal`(默认) | 排列方向 |
| `fill` | — | 子元素撑满宽度（vertical 时常用） |
| `size` | `number` | 自定义间距 |
| `wrap` | — | 自动换行 |
