# a-input 输入框

文本输入系列组件，包含 input、textarea、input-number、input-password。

## 基本输入

```vue
<a-input v-model="formData.name" placeholder="请输入名称" allow-clear />
```

## 禁用输入

```vue
<a-input v-model="formData.id" placeholder="自动生成" disabled />
```

## 多行文本

```vue
<a-textarea v-model="formData.remark" placeholder="请输入备注" :max-length="200" show-word-limit />
```

## 数字输入

```vue
<a-input-number v-model="formData.price" :min="0" :precision="2" style="width: 100%">
  <template #prefix>¥</template>
</a-input-number>
```

## 密码输入

```vue
<a-input-password v-model="formData.password" placeholder="请输入密码" />
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `v-model` | 绑定值 |
| `placeholder` | 占位文本 |
| `allow-clear` | 清除按钮 |
| `disabled` | 禁用 |
| `max-length` | 最大长度 |
| `show-word-limit` | 显示字数统计 |

### a-input-number 额外 Props

| Prop | 说明 |
|---|---|
| `min` / `max` | 数值范围 |
| `precision` | 小数精度 |
| `#prefix` | 前缀插槽（如货币符号） |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 筛选输入
- `src/views/tools/domestic-channel/index.vue` — 数字输入 + 前缀
- `src/views/international-order/post-seat-config.vue` — textarea
