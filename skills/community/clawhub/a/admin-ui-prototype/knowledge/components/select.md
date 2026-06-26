# a-select 下拉选择

支持单选、多选、远程搜索。

## 单选

```vue
<a-select
  v-model="req.data.status"
  placeholder="请选择状态"
  allow-clear
  :options="statusOptions"
/>
```

Options 格式：
```typescript
const statusOptions = [
  { label: '启用', value: 1 },
  { label: '禁用', value: 0 },
];
```

## 多选 + 可搜索

```vue
<a-select
  v-model="req.data.channels"
  multiple
  allow-search
  allow-clear
  :loading="channelLoading"
  :placeholder="channelLoading ? '正在加载...' : '请选择渠道'"
>
  <a-option v-for="item in channelList" :key="item.value" :value="item.value">
    {{ item.label }}
  </a-option>
  <template #empty>暂无数据</template>
</a-select>
```

## 从字典数据生成 Options

```typescript
const statusOptions = computed(() => {
  if (!dictionary.value?.statusDic) return [];
  return dictionary.value.statusDic.map((item: DictItem) => ({
    label: item.val,
    value: Number(item.key),
  }));
});
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `v-model` | 绑定值（单选: 单值，多选: 数组） |
| `options` | 选项数组 `{ label, value }[]` |
| `placeholder` | 占位文本 |
| `allow-clear` | 显示清除按钮 |
| `allow-search` | 可搜索 |
| `multiple` | 多选模式 |
| `loading` | 加载状态 |
| `disabled` | 禁用 |

## 项目参考

- `src/views/system/oidc/oauth-client/index.vue` — 字典驱动单选
- `src/views/tools/domestic-channel/index.vue` — 多选 + 远程加载
- `src/views/policy/published-fare/components/edit-modal.vue` — `a-option` 循环
