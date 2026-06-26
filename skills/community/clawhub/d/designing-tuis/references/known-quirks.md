# Known Quirks (TUI Design)

### Cross-axis `"fill"` collapses
- Symptom: child width/height collapses to `1` unexpectedly.
- Cause: non-main-axis sizing path falls back to min size for non-numeric values.
- Workaround: use explicit numeric width in column containers and explicit numeric height in row containers.

### `Box.title` is not rendered
- Symptom: setting `title` on `Box` has no visible output.
- Cause: renderer does not map `title` prop to border title drawing.
- Workaround: add a `Text` child in the box header region.

### `Popover` / `Tooltip` / `TextArea` listed but unavailable
- Symptom: schema accepts docs wording, but renderer/component map cannot instantiate those types.
- Cause: README drift versus actual registered component types.
- Workaround: do not use these types in `.tui`; use `Modal`, `Text`, or custom composition instead.

### Field placement confusion (`props` vs `layout`)
- Symptom: edits appear ignored or fail validation.
- Cause: width/height and component options are written to the wrong object level.
- Workaround: re-check component defaults in cheatsheet before editing existing files.
