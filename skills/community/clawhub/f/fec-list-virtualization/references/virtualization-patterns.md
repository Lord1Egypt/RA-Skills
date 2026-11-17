# Virtual list mode

## First determine whether virtualization is required

- Introduce virtualization only when list size, rendering cost, or scrolling performance have become a bottleneck; not required for small lists, lightweight static lists, and controllable lists after paging.
- SEO-critical content, full-text content that relies on the browser's native Ctrl+F, and content that needs to be printed/exported once, do not exist only in virtual items.
- Virtualization only reduces DOM rendering costs and does not replace data paging, interface caching, lazy loading of images, or rendering optimization of complex row components.

## Selection reference

First, use the existing virtual list library and framework conventions of the project; when adding new dependencies, select them according to the scenario.

| Scenarios | Alternative solutions | Notes |
| --- | --- | --- |
| React fixed-height list | `react-window` or TanStack Virtual | `react-window` is lightweight and stable; TanStack Virtual is more suitable for unifying complex scenes. |
| React Variable Height List | `VariableSizeList` of `react-window` or TanStack Virtual | Both are available when the height can be calculated; measurement and reset are required when the real height of the content changes. |
| Dynamic measurement, chat flow, expanded rows | TanStack Virtual | Works with `measureElement` / ResizeObserver to handle layout jitter and scroll anchor points. |
| Vue / Solid / Svelte / Cross-framework | TanStack Virtual or the project's existing ecological library | Do not introduce React-only virtual list libraries for non-React projects. |
| Two-dimensional grid, table, column virtualization | TanStack Virtual row/column Dual-axis solution or existing table library virtualization capability | Fixed columns, sticky headers and keyboard navigation need to be verified separately. |
| Legacy `react-virtualized` project | Maintain existing implementation | It is not recommended that new features continue to spread; evaluate migration costs when making major changes. |

## General implementation principles

- The container height must be stable, the rolling container must be clear, and the item key must come from a stable business identity.
- The row root element must transparently pass the `style`, positioning attributes and measurement ref provided by the virtual library.
- `overscan` adjusts the rendering cost by device and row: if it is too small, the screen will be white, if it is too large, it will be close to full rendering.
- Dynamic height requires estimated height, real measurements, resize updates and scroll anchor strategy.
- Infinite scrolling must separate "data paging" and "DOM virtualization"; do not trigger requests unconditionally in the render phase.
- Validate keyboard navigation, screen reader semantics, focus maintenance, scroll recovery, empty/loading states, and error states.

## React fixed height example

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

## React variable height example

```tsx
import { VariableSizeList as List } from "react-window";

const getItemSize = (index: number) => (items[index].hasSummary ? 120 : 60);

<List height={600} itemCount={items.length} itemSize={getItemSize} width="100%">
  {CardRow}
</List>;
```

## TanStack Virtual dynamic height example

```tsx
const virtualizer = useVirtualizer({
  count: messages.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 60,
  overscan: 5,
});
```

Dynamic content requires measuring elements and processing ResizeObserver; Vue/Solid/Svelte projects use the TanStack Virtual corresponding framework adapter, and the core options remain the same.

## infinite scroll

- `count` contains loader placeholders.
- `fetchNextPage()` is called when the last virtual item enters the viewport.
- Do not trigger requests unconditionally in render, use effects or explicit state protection.

## Grid virtualization

The two-dimensional grid uses `FixedSizeGrid` or TanStack Virtual's row/column dual-axis solution to ensure that the cell style is transparently transmitted.
