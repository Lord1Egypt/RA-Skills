# Widget slice template

Use for a large self-contained UI block.

```txt
widgets/<widget>/
  index.ts
  ui/
    <widget>.tsx
  model/
    <widget>.model.ts       # optional, only if widget owns state
  lib/
    group-items.ts          # optional widget-local helper
```

Public API example:

```ts
export { <Widget> } from './ui/<widget>';
```

Rules:

- Widget may import features, entities, shared.
- Widget must not import pages/app or sibling widgets.
- Do not create widgets for small one-page components.
