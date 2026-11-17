# Example: auth flow with Effector/Farfetched

This example uses FSD-like paths only to make imports readable. For normative placement, use `effector-fsd`.

```txt
entities/session/
  index.ts
  model/session.contract.ts
  model/session.model.ts
  api/current-session.query.ts
  api/session-refresh-barrier.ts

features/session-login/
  index.ts
  ui/login-form.tsx
  model/login.model.ts
  api/login.mutation.ts

features/session-logout/
  index.ts
  model/logout.model.ts
  api/logout.mutation.ts

shared/api/
  base-url.ts
  errors.ts

pages/login/
  index.ts
  route.ts
  ui/login-page.tsx
  model/page.model.ts

app/routes/
  router.ts
  protected.ts
  redirects.ts
```

## Login model sketch

```ts
sample({
  clock: formSubmitted,
  source: $credentials,
  filter: $canSubmit,
  target: loginMutation.start,
});

sample({
  clock: loginMutation.finished.success,
  fn: ({ result }) => result,
  target: sessionReceived,
});

export const $$login = {
  email: $email,
  password: $password,
  submitDisabled: $submitDisabled,
  pending: loginMutation.$pending,
  onEmailChange: emailChanged,
  onPasswordChange: passwordChanged,
  onSubmit: formSubmitted,
};
```

## Connected component sketch

```tsx
import { useUnit } from 'effector-react';
import { $$login } from '../model/login.model';

export function LoginForm() {
  const {
    email,
    password,
    submitDisabled,
    pending,
    onEmailChange,
    onPasswordChange,
    onSubmit,
  } = useUnit($$login);

  return (
    <form onSubmit={(event) => { event.preventDefault(); onSubmit(); }}>
      <input value={email} onChange={(event) => onEmailChange(event.currentTarget.value)} />
      <input value={password} onChange={(event) => onPasswordChange(event.currentTarget.value)} />
      <button disabled={submitDisabled || pending}>Sign in</button>
    </form>
  );
}
```

## Auth barrier rule

A session-aware barrier should not navigate. It refreshes/restores session and emits success/failure facts. Routing models decide redirects.
