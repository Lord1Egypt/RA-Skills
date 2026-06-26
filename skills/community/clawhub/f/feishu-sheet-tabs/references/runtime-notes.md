# Runtime Notes: Feishu Sheets tab creation

## Summary

`feishu_sheet` API does not currently expose worksheet-tab creation.

Workaround:
- create tabs via browser runtime (`window.spread` methods)
- then populate tabs via `feishu_sheet`

## Useful runtime objects
- `window.spread`
- `window.spreadApp`

## Discovered methods on `spread`
- `getSheetsChangeEvents`
- `setActiveSheetId`
- `setActiveSheetIndex`
- `removeSheetFromId`
- `createWorksheet`
- `createWorksheetByData`
- `addSheet`
- `delSheet`
- `copySheet`
- `moveSheet`
- `renameSheet`
- `hideSheet`
- `unhideSheet`
- `setTabColor`
- `serializeWorksheet`

## Concrete example from this workspace
Spreadsheet token:
- `Bf6qsMV9fhqrD6tPE6TcQhF7nEe`

Final tabs created:
- `总览` (`0d138c`, renamed from `Sheet1`)
- `Skills` (`GxGIGa`)
- `Workflows` (`9dJYiB`)
- `Templates` (`pDfjgl`)
- `Content` (`ClS7jn`)

## Recommended split of responsibility
1. Browser automation: inspect runtime, create/rename tabs
2. `feishu_sheet`: structured read/write to each created tab
