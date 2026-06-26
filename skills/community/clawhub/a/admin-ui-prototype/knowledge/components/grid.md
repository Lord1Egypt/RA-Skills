# a-row / a-col 栅格布局

24 列栅格系统，用于表单和内容排列。

## 表单栅格

```vue
<a-row :gutter="16">
  <a-col :span="6">
    <a-form-item field="name" label="名称">
      <a-input v-model="formData.name" />
    </a-form-item>
  </a-col>
  <a-col :span="6">
    <a-form-item field="status" label="状态">
      <a-select v-model="formData.status" />
    </a-form-item>
  </a-col>
</a-row>
```

## 双向间距

```vue
<a-row :gutter="[24, 24]" style="margin: auto; width: 100%">
  <a-col :span="24">筛选表单</a-col>
  <a-col :span="24">操作按钮</a-col>
</a-row>
```

## 卡片布局

```vue
<a-row :gutter="16">
  <a-col :span="6"><a-card>统计1</a-card></a-col>
  <a-col :span="6"><a-card>统计2</a-card></a-col>
  <a-col :span="6"><a-card>统计3</a-card></a-col>
  <a-col :span="6"><a-card>统计4</a-card></a-col>
</a-row>
```

## 常用 span 值

| span | 宽度 | 典型用途 |
|---|---|---|
| `6` | 25% | 筛选字段、统计卡片 |
| `8` | 33% | 三等分 |
| `12` | 50% | 表单双列 |
| `16` | 67% | 主内容区 |
| `24` | 100% | 全宽 |

## 常用 Props

| Prop | 说明 |
|---|---|
| `gutter` | 间距，`16` 或 `[水平, 垂直]` |
| `span` | 列宽（1-24） |
