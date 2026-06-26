# a-statistic 统计数值

用于 Dashboard 统计卡片展示。

## 基本用法

```vue
<a-card :bordered="false">
  <a-statistic title="总数" :value="1256" />
</a-card>
```

## 带前缀

```vue
<a-statistic title="收入" :value="58600" :precision="2">
  <template #prefix>¥</template>
</a-statistic>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `title` | 标题 |
| `value` | 数值 |
| `precision` | 小数精度 |
| `#prefix` | 前缀插槽 |
| `#suffix` | 后缀插槽 |

## 项目参考

- `src/views/tools/domestic-channel/index.vue` — 产品总数统计
