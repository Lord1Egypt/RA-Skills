# a-date-picker 日期选择器

日期、时间、范围选择。

## 日期选择

```vue
<a-date-picker
  v-model="formData.startDate"
  format="YYYY-MM-DD"
  value-format="YYYY-MM-DD"
  placeholder="请选择日期"
  style="width: 100%"
/>
```

## 日期范围

```vue
<a-range-picker
  v-model="req.data.timeRange"
  show-time
  format="YYYY-MM-DD HH:mm:ss"
  style="width: 100%"
/>
```

## 时间选择

```vue
<a-time-picker
  v-model="formData.startTime"
  format="HH:mm"
  placeholder="开始时间"
  style="width: 100%"
/>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `v-model` | 绑定值 |
| `format` | 显示格式 |
| `value-format` | 值格式 |
| `show-time` | 日期+时间模式 |
| `placeholder` | 占位文本 |

## 项目参考

- `src/views/policy/published-fare/components/edit-modal.vue` — 日期选择
- `src/views/supplier/resource-control/components/resource-control-edit-modal.vue` — 时间选择
- `src/views/log/business-log/index.vue` — 范围选择
