# Ghost Foreach Loop Variables

Variables available inside `{{#foreach}}` loops.

| Variable | Type | Description |
| ---------- | ------ | ------------- |
| `@index` | number | The 0-based index of the current iteration |
| `@number` | number | The 1-based index of the current iteration |
| `@key` | string | The object key when iterating over an object |
| `@first` | boolean | `true` if this is the first iteration |
| `@last` | boolean | `true` if this is the last iteration |
| `@odd` | boolean | `true` if `@index` is odd |
| `@even` | boolean | `true` if `@index` is even |
| `@rowStart` | boolean | `true` if `columns` is set and this starts a new row |
| `@rowEnd` | boolean | `true` if `columns` is set and this ends a row |

Source: [Ghost Docs — Foreach Data Variables](https://ghost.org/docs/themes/helpers/foreach/#data-variable-examples)
