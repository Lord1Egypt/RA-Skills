# Domain Patterns

## Pivot table intent

Keywords:
- `pivot`, `透视`, `rows/columns/filters/values`, `aggregation`, `preset`

Use:
- `CPivotTable` standalone
- `usePivotTable` for controlled state + persistence

## Voice navigation intent

Keywords:
- `voice nav`, `space`, `speech`, `asr`, `hotkey`, `long press`

Use:
- `CAINavProvider` as page/app wrapper
- `useVoiceInput` only when custom recording pipeline is needed
