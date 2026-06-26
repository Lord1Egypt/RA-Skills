# Routing Traps

- `snapshot.params` doesn't update on same-component navigation — use `paramMap` Observable
- Guard returning `false` shows blank page — return `UrlTree` to redirect
- `canDeactivate` doesn't fire on browser back without listener — add `beforeunload` for unsaved changes
- `loadChildren` path must be relative — absolute path fails silently with empty module
- Resolver errors block navigation completely — wrap in `catchError` returning fallback
- `relativeTo` required for relative navigation — omitting navigates from root
- Query params lost on `navigate()` — pass `queryParamsHandling: 'preserve'` or re-add manually
