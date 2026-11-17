# Example: generic list page placement

## Tree

```txt
entities/item/
  index.ts
  model/item.contract.ts
  model/item.mapper.ts
  api/item.query.ts
  ui/item-card.tsx

features/item-create/
  index.ts
  ui/item-create-form.tsx
  model/form.model.ts
  api/item-create.mutation.ts

pages/items/
  index.ts
  route.ts
  ui/items-page.tsx
  model/page.model.ts
  model/filters.model.ts
  model/pagination.model.ts
  api/items-page.query.ts
```

## Placement decisions

- `entities/item/api/item.query.ts`: reusable single-item or domain read.
- `pages/items/api/items-page.query.ts`: page-specific list query because params are page filters/pagination.
- `features/item-create`: user action and mutation.
- `pages/items/model`: route params, filters, pagination, refresh after creation.

## Page model orchestration

```ts
// features/item-create/index.ts
export { ItemCreateForm } from './ui/item-create-form';
export { $$itemCreate, itemCreated } from './model/form.model';
```

```ts
// pages/items/model/page.model.ts
import { createEvent, sample } from 'effector';
import { itemCreated } from '@/features/item-create';
import { itemsPageQuery } from '../api/items-page.query';
import { itemsRoute } from '../route';
import { $filters } from './filters.model';

export const pageStarted = createEvent();
export const refreshClicked = createEvent();

sample({
  clock: [pageStarted, refreshClicked],
  source: $filters,
  target: itemsPageQuery.start,
});

sample({
  clock: itemCreated,
  source: {
    isOpened: itemsRoute.$isOpened,
    filters: $filters,
  },
  filter: ({ isOpened }) => isOpened,
  fn: ({ filters }) => filters,
  target: itemsPageQuery.start,
});
```

This belongs to the page because it coordinates page filters and page list refresh. The mutation success is exposed as a semantic feature fact (`itemCreated`), and the page-local refetch is gated by route state because Effector page models are static after import.
