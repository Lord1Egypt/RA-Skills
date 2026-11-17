#State management mode

## Ownership Review Checklist

- Each status field has a unique ownership: local status, form status, server-side cache, URL status, global Store or browser persistence.
- Derived values are calculated from the source state rather than manually synchronized via effects or watchers.
- URL state is used for view states that are shareable and need to be retained after refresh, such as filtering, searching, sorting, and paging.
- Server-side data is kept in the request cache; the global Store only stores selected IDs, local preferences, or optimistic update prompts.
- Persistent client state requires a whitelist, schema version number, migration path and sensitive field exclusion rules.
- Store actions are named after domain events, not component processors.

## React Store shape example

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

Selectors should return stable raw values or memo-encoded slices whenever possible:

```tsx
const itemCount = useCartStore((state) =>
  state.lines.reduce((total, line) => total + line.quantity, 0),
);
```

## URL status boundaries

Use URL state when another user should be able to open the same view, or when the view needs to be preserved after a refresh.

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

## Persistence adapter boundary

Only persist stable client preferences or non-sensitive drafts. Serialization logic is placed outside the component.

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

## SSR is isolated from requests

- When the state may contain user data, a separate Store needs to be created for each request.
- Do not read `window`, `localStorage` or `document` during server rendering.
- Reload persistence preferences after hydration and provide deterministic defaults before hydration.
- Server-side cache dehydration is handled separately from pure client-side global Store.
