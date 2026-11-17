---
name: fec-state-management
description: Use when choosing, implementing, reviewing, or refactoring frontend state ownership across React, Vue, Next.js, Nuxt, URL state, server state, form state, browser persistence, or global stores. Prefer narrower skills for TanStack Query cache details, browser storage persistence, or form validation internals; Chinese triggers include state management, state ownership, store selection.
---

# Front-end status management

## Purpose

Determine clear ownership of front-end state to avoid global store bloat, duplicate caching, and derived state synchronization errors.

## Procedure

### 1. Classify status sources first

Don't choose Redux, Zustand, Pinia or Context first. First mark each state to its unique owner, and then decide on the tool.

| Status Type | Typical Example | Default Attribution |
| ---------------- | ------------------------------------ | ------------------------ |
| Local UI state | Pop-up window switch, tab, expand row, hover editing state | In-component state / ref |
| Form status | Input value, dirty field, validation error, submitting | Form library or form component |
| Server status | List, details, paging results, remote errors | Request cache library |
| URL status | Search terms, filter, sort, page number, selected tab | Routing parameters / search params |
| Global client status | Login users, topics, permission snapshots, shopping cart drafts | Global store |
| Browser persistent state | Drafts, preferences, offline queues retained across refreshes | Storage layer + state adapter |

```tsx
type ReportsStateMap = {
  search: "url";
  selectedReportId: "url";
  reports: "server-state-cache";
  isFilterPanelOpen: "local-ui";
  draftColumns: "browser-persistence";
};
```

### 2. Keep it minimal

Do not save a new copy of a value that can be inferred from props, server state, URL, or existing state.

```tsx
interface Invoice {
  id: string;
  status: "draft" | "sent" | "paid";
}

function InvoiceList({ invoices }: { invoices: Invoice[] }) {
  const paidInvoices = invoices.filter((invoice) => invoice.status === "paid");

  return <span>{paidInvoices.length}</span>;
}
```

### 3. Select the React global state solution

Priority is given to localization and combination in React; the global store is only introduced when cross-page, cross-feature or unified actions are required.

```tsx
import { create } from "zustand";

interface WorkspaceState {
  activeWorkspaceId: string | null;
  setActiveWorkspaceId: (workspaceId: string) => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  activeWorkspaceId: null,
  setActiveWorkspaceId: (activeWorkspaceId) => set({ activeWorkspaceId }),
}));
```

Decision order:

1. Use only in one component or a small subtree: `useState` / `useReducer`.
2. Low-frequency global configuration or dependency injection: Context.
3. Moderately complex business status: Zustand or Jotai, priority will be given based on the existing selection of the warehouse.
4. Large applications, strict action flow, auditing or time travel debugging: Redux Toolkit.
5. Remote data: Use the data acquisition skill to manage query keys, cache and invalidation policies.

### 4. Select Vue global state solution

In Vue 3, use `provide/inject` for local cross-level transfer; use Pinia or the existing store of the project for global business status.

```ts
import { computed, readonly, ref } from "vue";
import { defineStore } from "pinia";

export const useSessionStore = defineStore("session", () => {
  const userId = ref<string | null>(null);
  const isSignedIn = computed(() => userId.value !== null);

  function signIn(nextUserId: string) {
    userId.value = nextUserId;
  }

  return {
    userId: readonly(userId),
    isSignedIn,
    signIn,
  };
});
```

### 5. Clarify status boundaries and migration steps

When reconstructing the state, first make a state list, and then gradually move the read and write entries. Each step should keep the behavior verifiable.

```ts
interface StateMigrationItem {
  name: string;
  currentOwner: "component" | "context" | "store" | "query-cache" | "url";
  targetOwner: "component" | "context" | "store" | "query-cache" | "url";
  verification: string;
}

const migrationPlan: StateMigrationItem[] = [
  {
    name: "dashboard filters",
    currentOwner: "store",
    targetOwner: "url",
    verification: "refreshing the page preserves filters through search params",
  },
];
```

## Detailed reference

Load [references/state-patterns.md](references/state-patterns.md) when you need Store shape examples, selector patterns, URL state synchronization, persistence adapters, SSR boundaries, or review checklists.

## Constraints

- Do not copy the server response to the global store; caching, invalidation and retries belong to the data acquisition layer.
- Do not promote each field of the form to the global store; cross-step sharing is also handled first by the form context or submit draft adapter.
- No need to use Context to carry large objects that change frequently; it will expand the re-rendering range.
- Persistence state must specify field whitelist, version number, expiration policy and sensitive data exclusion.
- In SSR scenarios, do not create a singleton store with user data at the top level of the module.

## Expected Output

Output status attribution list, selection reasons, store/API boundaries and verification steps. Key behaviors such as loading/error/empty, refresh, rollback, cross-routing, and permission changes should be retained during implementation.
