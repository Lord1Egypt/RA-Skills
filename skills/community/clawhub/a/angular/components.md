# Components Traps

- `@ViewChild` undefined until `ngAfterViewInit` — accessing in constructor/`ngOnInit` throws
- `OnPush` ignores object mutations — must create new reference or call `markForCheck()`
- `ngOnChanges` only fires for reference changes — mutating parent object won't trigger
- `@Output` EventEmitter must call `emit()` — forgetting `.emit()` silently does nothing
- `@Input({ required: true })` only checked at compile time — runtime still allows undefined
- `ngAfterContentInit` runs before `ngAfterViewInit` — projected content ready before own template
- `@HostListener` on destroyed components keeps firing — unsubscribe or use `takeUntilDestroyed()`
