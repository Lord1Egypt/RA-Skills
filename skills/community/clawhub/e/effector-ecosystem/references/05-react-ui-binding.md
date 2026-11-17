# React UI binding with Effector

Use this file when writing or reviewing React components.

## Contents

- Connected vs dumb components
- Main rule: one `useUnit` shape per connected component
- What to avoid
- Scope and SSR
- Deprecated/legacy bindings
- Lists and item subscriptions
- Gates
- Forms
- Effector units in render
- Event handlers
- Handler alias names

## Connected vs dumb components

Dumb component:

- receives ordinary props
- renders markup
- knows nothing about Effector units

Connected component:

- imports a model/query/mutation/route from the owning module boundary
- calls `useUnit`
- passes plain values/callbacks to dumb UI

Prefer small connected components at ownership boundaries.

## Main rule: one `useUnit` shape per connected component

For units from the same model, prefer one `useUnit` call with an object or array shape and destructure the result.

### Object shape: preferred for readability

```tsx
import { useUnit } from 'effector-react';
import { $$profileUpdate } from '../model/profile-update.model';

export function ProfileUpdateForm() {
  const {
    name,
    email,
    errors,
    submitDisabled,
    onNameChange,
    onEmailChange,
    onSubmit,
  } = useUnit($$profileUpdate);

  return (
    <form onSubmit={(event) => {
      event.preventDefault();
      onSubmit();
    }}>
      <input value={name} onChange={(event) => onNameChange(event.currentTarget.value)} />
      <input value={email} onChange={(event) => onEmailChange(event.currentTarget.value)} />
      <button disabled={submitDisabled}>Save</button>
    </form>
  );
}
```

Model shape:

```ts
export const $$profileUpdate = {
  name: $name,
  email: $email,
  errors: $errors,
  submitDisabled: $submitDisabled,
  onNameChange: nameChanged,
  onEmailChange: emailChanged,
  onSubmit: submitted,
};
```

### Array shape: useful for local small bindings

```tsx
const [value, submitDisabled, onValueChange, onSubmit] = useUnit([
  $value,
  $submitDisabled,
  valueChanged,
  submitted,
]);
```

Use arrays only when order is obvious and stable. Prefer object shape for public model APIs.

## What to avoid

Avoid many separate `useUnit` calls in one component:

```tsx
// bad by default
const value = useUnit($value);
const submitDisabled = useUnit($submitDisabled);
const onValueChange = useUnit(valueChangedEvent);
const onSubmit = useUnit(submittedEvent);
```

This is harder to review, easier to partially refactor incorrectly, and increases the chance of unused subscriptions. Split the component when different parts need independent subscriptions.

Avoid passing raw events/effects to DOM handlers:

```tsx
// bad in Scope/SSR-aware apps
<button onClick={() => submittedEvent()}>Save</button>
```

Use the bound function returned by `useUnit`:

```tsx
const { onSubmit } = useUnit({ onSubmit: submittedEvent });
<button onClick={() => onSubmit()}>Save</button>
```

## Scope and SSR

When an app uses Scope, tests, SSR, or hydration, events/effects must be bound to the current Scope before passing to DOM/event handlers.

Use:

```tsx
<Provider value={scope}>
  <App />
</Provider>
```

and bind units with `useUnit` in React.

Do not call raw units directly from components.

## Deprecated/legacy bindings

Avoid in new code:

- `useStore`
- `useEvent`
- `connect`
- HOCs from older Effector React patterns

Use `useUnit` instead.

## Lists and item subscriptions

For large lists, avoid subscribing a whole list item component to the entire list if it only needs one item.

Use:

- `useList` for rendering store-backed lists
- `useStoreMap` for selecting one item by id
- component splitting when only a small subtree needs a store

Keep list transformation in models when it is business/domain behavior. UI-only presentation mapping can stay in UI.

## Gates

Use Gates only for lifecycle facts that genuinely belong to a component boundary:

- component mounted/unmounted
- route widget appeared
- visible props entered a model

Do not use Gate as a hidden API call trigger when route/page events are clearer.

## Forms

UI should:

- bind form values/errors/actions through a single `useUnit` shape
- translate labels/messages
- call bound events in handlers

UI should not:

- decide if a business transition is allowed
- call mutations directly if a form event should own the flow
- parse backend errors

## Effector units in render

Never create units in render or hooks:

```tsx
function Component() {
  const clicked = createEvent(); // bad
}
```

Create models statically and import them.

## Event handlers

Good:

```tsx
const { onSearchChange } = useUnit({ onSearchChange: searchChanged });
<input onChange={(event) => onSearchChange(event.currentTarget.value)} />
```

Good for submit:

```tsx
const { onSubmit } = useUnit({ onSubmit: submitted });
<form onSubmit={(event) => {
  event.preventDefault();
  onSubmit();
}} />
```

Avoid putting business logic in handlers.

## Handler alias names

Events in Effector models should keep fact names such as `submitted`, `formSubmitted`, or `searchChanged`.

Handler-like values returned by `useUnit` should use React-style `on*` aliases:

```ts
const { onSubmit, onSearchChange } = useUnit({
  onSubmit: submitted,
  onSearchChange: searchChanged,
});
```

Public `$$model` shapes should expose the same aliases, so JSX never destructures event fact names as callbacks.

## Next.js Client Components

In Next.js App Router, any component that uses `useUnit` or other React hooks must be a Client Component:

```tsx
'use client';

import { useUnit } from 'effector-react';

export function SaveButton() {
  const { onSubmit } = useUnit({ onSubmit: submitted });
  return <button onClick={() => onSubmit()}>Save</button>;
}
```

Server Components should create Scope, run `allSettled`, serialize values, and render Client Components. They should not call `useUnit`.
