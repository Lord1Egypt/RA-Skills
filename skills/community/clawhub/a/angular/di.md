# Dependency Injection Traps

- Circular dependency crashes at runtime — use `forwardRef()` or restructure to break cycle
- Component `providers` creates NEW instance — not the root singleton, data not shared
- `@Optional()` missing returns null, not error — unchecked access throws
- `@Inject(TOKEN)` required for InjectionToken — omitting uses class name which doesn't exist
- `providedIn: 'any'` creates instance per lazy module — not true singleton
- `useFactory` deps must match factory params order — wrong order injects wrong service
- Abstract class as token needs `useExisting` — `useClass` creates concrete directly
