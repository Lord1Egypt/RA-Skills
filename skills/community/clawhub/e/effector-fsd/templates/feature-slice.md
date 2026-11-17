# Feature slice template

Use for a user action or business capability.

```txt
features/<action-name>/
  index.ts
  ui/
    <action-name>-form.tsx
  model/
    form.model.ts
    submit.model.ts
    <action-name>.model.ts
    <action-name>.contract.ts      # if action-specific response/request validation
  api/
    <action-name>.mutation.ts
  lib/
    map-form-to-request.ts
```

Public API example:

```ts
export { <ActionName>Form } from './ui/<action-name>-form';
export { $$<actionName> } from './model/<action-name>.model';
export { <actionName>Mutation } from './api/<action-name>.mutation';
```

Rules:

- Name by user action: `profile-update`, `session-login`, `comment-create`.
- Do not name by UI event: `open-modal`, `button-click`, `set-search`.
- Feature may import entities and shared.
- Feature must not import pages/widgets/app or sibling features.
- Submit duplicate-click protection belongs in the feature/page model, not UI.
