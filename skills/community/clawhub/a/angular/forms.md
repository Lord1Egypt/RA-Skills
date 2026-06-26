# Forms Traps

- `setValue()` requires ALL FormGroup fields — missing field throws, use `patchValue()` for partial
- `valueChanges` fires before value settles — use `debounceTime` or check in subscription
- Async validators run after sync validators — if sync fails, async never runs
- `updateOn: 'blur'` at FormGroup doesn't cascade — set on each control that needs it
- `disabled` controls excluded from `value` — use `getRawValue()` to include them
- `FormArray` controls lose type info — use `FormRecord` or typed `FormArray<FormControl<T>>`
- Template-driven `[(ngModel)]` and reactive `formControlName` on same input breaks — pick one
