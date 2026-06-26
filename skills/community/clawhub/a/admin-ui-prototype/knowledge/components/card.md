# a-card 卡片容器

内容分组容器，用于信息面板和区域划分。

## 基本用法

```vue
<a-card title="基本信息" :bordered="false">
  <a-descriptions :column="2" bordered>
    ...
  </a-descriptions>
</a-card>
```

## 带操作的卡片

```vue
<a-card :bordered="false">
  <template #title>
    <a-space>
      <icon-apps />
      <span>面板标题</span>
    </a-space>
  </template>
  <template #extra>
    <a-button type="text" size="small" @click="toggle">
      {{ collapsed ? '展开' : '收起' }}
    </a-button>
  </template>
  <div v-show="!collapsed">卡片内容</div>
</a-card>
```

## 统计卡片

```vue
<a-col :span="6">
  <a-card :bordered="false">
    <a-statistic title="总数" :value="1256" />
  </a-card>
</a-col>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `title` | 标题文本 |
| `:bordered` | `false` 无边框 |
| `#title` | 自定义标题插槽 |
| `#extra` | 右上角操作区插槽 |

## 全局样式 `.general-card`

项目定义了 `.general-card` 类，可用于统一卡片样式：
- header padding: 20px
- body padding: 0 20px 20px 20px
