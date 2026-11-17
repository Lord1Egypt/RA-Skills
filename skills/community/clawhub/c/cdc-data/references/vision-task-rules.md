# Visual processing rules

Use vision only with explicit authorization and only for user-relevant pages already listed in `vision_pages`.

- Render the smallest useful page or region into task-temporary storage.
- Preserve OCR reading order, image-table structure, chart titles, axes, units, legends, series, annotations, and labeled values.
- Mark estimates from unlabeled curves with `approximate=true`.
- Write results into the matching page's `visuals` array in the same `extracted.json`.
- Set `requires_vision=false` only when the relevant content is resolved, then recompute `vision_pages`.
- On failure, keep the page number and add a concise warning.
- Delete every render and crop after success or failure.

Do not create visual-task records, retained images, retry ledgers, or separate output files.
