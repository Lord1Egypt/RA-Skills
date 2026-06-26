# a-radio 单选框

单选框组，用于互斥选项。

## 基本用法

```vue
<a-radio-group v-model="formData.status">
  <a-radio :value="1">有效</a-radio>
  <a-radio :value="0">无效</a-radio>
</a-radio-group>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `v-model` | 绑定值 |
| `value` | 选项值 |

## 项目参考

- `src/views/policy/published-fare/components/edit-modal.vue` — 有效/无效选择
