---
name: Angular
slug: angular
version: 1.0.1
description: Build reliable Angular apps avoiding RxJS leaks, change detection traps, and DI pitfalls.
---

## When to Use

User needs Angular expertise — component architecture, RxJS patterns, change detection, dependency injection, routing, and forms.

## Quick Reference

| Topic | File |
|-------|------|
| Components & change detection | `components.md` |
| RxJS & subscriptions | `rxjs.md` |
| Forms & validation | `forms.md` |
| Dependency injection | `di.md` |
| Routing & guards | `routing.md` |
| HTTP & interceptors | `http.md` |

## Common Mistakes

- `OnPush` with mutated objects won't trigger change detection — always create new reference: `{...obj}` or `[...arr]`
- `@ViewChild` is undefined in constructor/`ngOnInit` — access in `ngAfterViewInit` or later
- `*ngFor` without `trackBy` re-renders entire list on any change — add `trackBy` returning stable ID
- Manual `subscribe()` without unsubscribe leaks memory — use `async` pipe, `takeUntilDestroyed()`, or unsubscribe in `ngOnDestroy`
- `HttpClient` returns cold Observable — each `subscribe()` fires new HTTP request
- `setTimeout`/`setInterval` outside NgZone — change detection won't run, use `NgZone.run()` or signals
- Circular DI dependency crashes app — use `forwardRef()` or restructure services
- `ElementRef.nativeElement` direct DOM access breaks SSR — use `Renderer2` or `@defer`
- Route params via `snapshot` miss navigation changes — use `paramMap` Observable for same-component navigation
- `setValue()` on FormGroup requires ALL fields — use `patchValue()` for partial updates
