# 虚拟列表模式

## 先判断是否需要虚拟化

- 只有列表规模、渲染成本或滚动性能已经形成瓶颈时才引入虚拟化；小列表、轻量静态列表和分页后可控的列表不需要。
- SEO 关键内容、依赖浏览器原生 Ctrl+F 的全文内容、需要一次性打印/导出的内容，不要只存在于虚拟项中。
- 虚拟化只减少 DOM 渲染成本，不替代数据分页、接口缓存、图片懒加载或复杂行组件的渲染优化。

## 选型参考

先沿用项目已有虚拟列表库和框架约定；新增依赖时再按场景选择。

| 场景 | 候选方案 | 注意点 |
| --- | --- | --- |
| React 固定高度列表 | `react-window` 或 TanStack Virtual | `react-window` 轻量稳定；TanStack Virtual 更适合统一复杂场景。 |
| React 可变高度列表 | `react-window` 的 `VariableSizeList` 或 TanStack Virtual | 高度可计算时两者都可用；内容真实高度会变化时需要测量和重置。 |
| 动态测量、聊天流、展开行 | TanStack Virtual | 配合 `measureElement` / ResizeObserver，处理布局抖动和滚动锚点。 |
| Vue / Solid / Svelte / 跨框架 | TanStack Virtual 或项目既有生态库 | 不要为非 React 项目引入 React-only 虚拟列表库。 |
| 二维网格、表格、列虚拟化 | TanStack Virtual row/column 双轴方案或现有表格库虚拟化能力 | 固定列、粘性表头和键盘导航需要单独验证。 |
| 遗留 `react-virtualized` 项目 | 维护现有实现 | 不建议新功能继续扩散；大改时评估迁移成本。 |

## 通用实现原则

- 容器高度必须稳定，滚动容器必须明确，item key 必须来自稳定业务标识。
- 行根元素必须透传虚拟库提供的 `style`、定位属性和测量 ref。
- `overscan` 按设备和行渲染成本调节：过小会白屏，过大会接近全量渲染。
- 动态高度需要估算高度、真实测量、resize 更新和滚动锚点策略。
- 无限滚动要分离“数据分页”和“DOM 虚拟化”；不要在 render 阶段无条件触发请求。
- 验证键盘导航、屏幕阅读器语义、焦点保持、滚动恢复、空态/加载态和错误态。

## React 固定高度示例

```tsx
import { FixedSizeList as List } from "react-window";

const Row = ({ index, style, data }: { index: number; style: React.CSSProperties; data: User[] }) => (
  <div style={style}>{data[index].name}</div>
);

export const UserList = ({ users }: { users: User[] }) => (
  <List height={500} itemCount={users.length} itemSize={48} width="100%" itemData={users}>
    {Row}
  </List>
);
```

## React 可变高度示例

```tsx
import { VariableSizeList as List } from "react-window";

const getItemSize = (index: number) => (items[index].hasSummary ? 120 : 60);

<List height={600} itemCount={items.length} itemSize={getItemSize} width="100%">
  {CardRow}
</List>;
```

## TanStack Virtual 动态高度示例

```tsx
const virtualizer = useVirtualizer({
  count: messages.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 60,
  overscan: 5,
});
```

动态内容需要测量元素并处理 ResizeObserver；Vue/Solid/Svelte 项目使用 TanStack Virtual 对应框架 adapter，核心选项保持一致。

## 无限滚动

- `count` 包含 loader 占位项。
- 最后一个虚拟项进入视口时调用 `fetchNextPage()`。
- 不要在 render 中无条件触发请求，使用 effect 或明确状态保护。

## 网格虚拟化

二维网格使用 `FixedSizeGrid` 或 TanStack Virtual 的 row/column 双轴方案，确保单元格 style 透传。
