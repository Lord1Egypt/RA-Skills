# a-form 表单

表单容器，包含表单项 `a-form-item` 和验证规则。

## 筛选表单

```vue
<a-form :model="req.data" layout="vertical" ref="filterFormRef">
  <a-row :gutter="16">
    <a-col :span="6">
      <a-form-item field="name" label="名称">
        <a-input v-model="req.data.name" placeholder="请输入" allow-clear />
      </a-form-item>
    </a-col>
    <a-col :span="6">
      <a-form-item field="status" label="状态">
        <a-select v-model="req.data.status" placeholder="请选择" allow-clear :options="statusOptions" />
      </a-form-item>
    </a-col>
  </a-row>
</a-form>
```

## 编辑表单（带验证）

```vue
<a-form ref="formRef" :model="formData" :rules="rules" layout="vertical">
  <a-divider orientation="left">基本信息</a-divider>
  <a-row :gutter="16">
    <a-col :span="12">
      <a-form-item field="name" label="名称">
        <a-input v-model="formData.name" placeholder="请输入名称" />
      </a-form-item>
    </a-col>
  </a-row>
</a-form>
```

## 验证规则

```typescript
const rules = computed(() => ({
  name: [{ required: true, message: '请输入名称' }],
  email: [
    { required: true, message: '请输入邮箱' },
    { type: 'email', message: '邮箱格式不正确' },
  ],
  // 条件验证
  password: props.isEdit ? [] : [{ required: true, message: '请输入密码' }],
  // 自定义验证
  code: [{
    validator: (value: string, callback: (error?: string) => void) => {
      if (value && !/^[A-Z0-9]+$/.test(value)) {
        callback('只允许大写字母和数字');
      } else {
        callback();
      }
    },
  }],
}));
```

## 提交与重置

```typescript
const formRef = ref<FormInstance>();

// 提交
const handleSubmit = async () => {
  const errors = await formRef.value?.validate();
  if (errors) return; // 有错误，不提交
  // 调用 API...
};

// 重置
const handleReset = () => {
  filterFormRef.value?.resetFields();
};
```

## 常用 Props

| Prop | 值 | 说明 |
|---|---|---|
| `layout` | `"vertical"` | 项目统一使用垂直布局 |
| `model` | `ref对象` | 表单数据绑定 |
| `rules` | `Record<string, FieldRule[]>` | 验证规则 |
| `auto-label-width` | `boolean` | 自动对齐标签宽度 |

### a-form-item Props

| Prop | 说明 |
|---|---|
| `field` | 字段名，与 model 中的 key 对应 |
| `label` | 标签文本 |
| `extra` | 辅助提示文案（如 `"不勾选表示全平台适用"`） |
| `label-col-flex` | 标签宽度（如 `"100px"`） |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 筛选表单
- `src/views/policy/published-fare/components/edit-modal.vue` — 编辑表单 + 复杂验证
