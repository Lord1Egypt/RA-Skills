# RxJS Traps

- `subscribe()` without unsubscribe leaks memory — use `takeUntilDestroyed()`, `async` pipe, or manual cleanup
- `takeUntilDestroyed()` must be called in injection context — fails if called in callback or after constructor
- `switchMap` cancels in-flight requests — use `mergeMap` when all requests must complete
- `combineLatest` requires ALL sources to emit — use `startWith` for initial values
- `shareReplay` without `refCount: true` keeps subscription alive forever — memory leak
- `catchError` must return Observable — returning plain value throws "You provided invalid object"
- `forkJoin` fails completely if any source errors — wrap each in `catchError` for partial results
- `distinctUntilChanged` uses reference equality — pass comparator for objects
