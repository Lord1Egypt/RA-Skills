# Entity slice template

Use for a real business/domain concept.

```txt
entities/<entity>/
  index.ts
  model/
    <entity>.types.ts
    <entity>.contract.ts
    <entity>.mapper.ts
    <entity>.model.ts
  api/
    <entity>.query.ts
  ui/
    <entity>-avatar.tsx        # optional visual, no feature/page orchestration
  lib/
    format-<entity>.ts         # optional domain-local helper
  @x/
    <other-entity>.ts          # optional explicit entity cross-import API
```

Public API example:

```ts
export { <entity>Query } from './api/<entity>.query';
export { $<entity>, <entity>Received } from './model/<entity>.model';
export type { <Entity> } from './model/<entity>.types';
export { <Entity>Contract } from './model/<entity>.contract';
```

Rules:

- Do not import features/pages/widgets/app.
- Keep page filters and action forms out of entities.
- Use `@x` only for explicit entity relationships.
