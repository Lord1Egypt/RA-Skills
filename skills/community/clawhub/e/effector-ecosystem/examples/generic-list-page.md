# Example: generic list page

This example is not admin-specific. It can represent posts, products, messages, projects, files, etc.

## Structure

```txt
entities/item/
  index.ts
  model/item.contract.ts
  model/item.types.ts
  api/items.query.ts
  ui/item-title.tsx

features/item-create/
  index.ts
  ui/item-create-button.tsx
  model/item-create.model.ts
  api/item-create.mutation.ts

pages/items/
  index.ts
  route.ts
  ui/items-page.tsx
  model/page.model.ts
  model/filters.model.ts
  api/items-page.query.ts  # only if list params/shape are page-specific
```

## Page orchestration

```ts
sample({
  clock: [itemsRoute.opened, searchDebounced, pageChanged],
  source: $queryParams,
  target: itemsQuery.start,
});

sample({
  clock: itemCreated,
  source: {
    isOpened: itemsRoute.$isOpened,
    queryParams: $queryParams,
  },
  filter: ({ isOpened }) => isOpened,
  fn: ({ queryParams }) => queryParams,
  target: itemsQuery.start,
});
```

The create feature should expose a semantic fact such as `itemCreated` instead of forcing the page to consume `createItemMutation.finished.success`. The page owns the refetch decision, but because Effector models are static after import, the refetch must be gated by `itemsRoute.$isOpened` or moved to an app/entity invalidation owner.

## Search/filter concurrency

```ts
concurrency(itemsQuery, { strategy: 'TAKE_LATEST' });
```

Use `TAKE_LATEST` for fast-changing search/filter requests. If both layout and page can start the same query, add a semantic request event with a `$pending`/cache guard or split the operations. Use `cache` or `keepFresh` only when freshness behavior is intentional.

## Page model UI shape

```ts
export const $$itemsPage = {
  items: itemsQuery.$data,
  pending: itemsQuery.$pending,
  search: $search,
  page: $page,
  onSearchChange: searchChanged,
  onPageChange: pageChanged,
  onRetryClick: itemsQuery.refresh,
};
```

## Page component binding

```tsx
const {
  items,
  pending,
  search,
  page,
  onSearchChange,
  onPageChange,
  onRetryClick,
} = useUnit($$itemsPage);
```

Keep table/list rendering in UI. Keep filtering, pagination params, refetch rules, and feature-completion reactions in the page model.
