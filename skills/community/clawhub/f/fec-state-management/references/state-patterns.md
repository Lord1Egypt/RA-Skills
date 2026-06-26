# 状态管理模式

## 所有权审查清单

- 每个状态字段有唯一归属：本地状态、表单状态、服务端缓存、URL 状态、全局 Store 或浏览器持久化。
- 派生值由源状态计算得出，而不是通过 effect 或 watcher 手动同步。
- URL 状态用于可分享、刷新后需保留的视图状态，如筛选、搜索、排序和分页。
- 服务端数据保留在请求缓存中；全局 Store 仅存放选中的 ID、本地偏好或乐观更新提示。
- 持久化的客户端状态需有白名单、schema 版本号、迁移路径和敏感字段排除规则。
- Store 的 action 以领域事件命名，而非组件处理器命名。

## React Store 形状示例

```tsx
import { create } from "zustand";
import { subscribeWithSelector } from "zustand/middleware";

interface CartLine {
  sku: string;
  quantity: number;
}

interface CartState {
  lines: CartLine[];
  addLine: (line: CartLine) => void;
  removeLine: (sku: string) => void;
}

export const useCartStore = create<CartState>()(
  subscribeWithSelector((set) => ({
    lines: [],
    addLine: (line) =>
      set((state) => ({
        lines: [...state.lines.filter((item) => item.sku !== line.sku), line],
      })),
    removeLine: (sku) =>
      set((state) => ({
        lines: state.lines.filter((line) => line.sku !== sku),
      })),
  })),
);
```

选择器应尽可能返回稳定的原始值或经过 memo 的切片：

```tsx
const itemCount = useCartStore((state) =>
  state.lines.reduce((total, line) => total + line.quantity, 0),
);
```

## URL 状态边界

当另一个用户应能打开相同视图，或刷新后需要保留视图时，使用 URL 状态。

```tsx
import { useSearchParams } from "react-router-dom";

export function useReportFilters() {
  const [params, setParams] = useSearchParams();
  const status = params.get("status") ?? "open";

  function setStatus(nextStatus: string) {
    setParams((next) => {
      next.set("status", nextStatus);
      next.set("page", "1");
      return next;
    });
  }

  return { status, setStatus };
}
```

## 持久化适配器边界

仅持久化稳定的客户端偏好设置或非敏感草稿。序列化逻辑放在组件外部。

```ts
interface PersistedGridState {
  version: 1;
  visibleColumns: string[];
}

const storageKey = "reports:grid";

export function readGridState(): PersistedGridState | null {
  const raw = window.localStorage.getItem(storageKey);
  if (!raw) return null;

  try {
    const parsed = JSON.parse(raw) as PersistedGridState;
    return parsed.version === 1 ? parsed : null;
  } catch {
    return null;
  }
}

export function writeGridState(state: PersistedGridState): void {
  window.localStorage.setItem(storageKey, JSON.stringify(state));
}
```

## SSR 与请求隔离

- 当状态可能包含用户数据时，每次请求需创建独立的 Store。
- 服务端渲染期间不要读取 `window`、`localStorage` 或 `document`。
- 水合后再加载持久化偏好，并在水合前提供确定性默认值。
- 服务端缓存脱水与纯客户端全局 Store 分开处理。
