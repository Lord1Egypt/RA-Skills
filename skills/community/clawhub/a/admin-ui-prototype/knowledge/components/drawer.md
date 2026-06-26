# a-drawer 抽屉面板

侧边滑出面板，用于详情查看或复杂操作。

## 基本用法

```vue
<a-drawer
  v-model:visible="drawerVisible"
  title="详情"
  :width="'88vw'"
  :footer="false"
  unmount-on-close
>
  <div>抽屉内容</div>
</a-drawer>
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `v-model:visible` | 显示控制 |
| `title` | 标题 |
| `width` | 宽度（支持 px、vw） |
| `placement` | 方向 `left` / `right`(默认) |
| `footer` | `false` 隐藏底部 |
| `unmount-on-close` | 关闭时销毁内容 |
| `mask-closable` | 点击遮罩关闭 |

## 项目参考

- `src/views/system/api-compare/index.vue` — 大尺寸抽屉
- `src/layout/default-layout.vue` — 移动端菜单抽屉
