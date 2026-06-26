# a-checkbox 复选框

单个复选或复选框组。

## 复选框组

```vue
<a-checkbox-group v-model="formData.platforms">
  <a-checkbox v-for="item in platformOptions" :key="item.value" :value="item.value">
    {{ item.label }}
  </a-checkbox>
</a-checkbox-group>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `v-model` | 绑定值（数组） |
| `value` | 单个选项的值 |
| `disabled` | 禁用 |

## 项目自定义组件

项目封装了 `CheckboxGroupAdapter`（`src/components/checkbox-group-adapter/`），支持全选/反选和值转换。

## 项目参考

- `src/views/policy/published-fare/components/edit-modal.vue` — 平台选择
