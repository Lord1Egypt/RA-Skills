# PDF extraction rules

Process one already verified local official PDF directly within the main Skill. Require normalized report metadata, one absolute `extracted.json` path, and `extract` or `vision` authorization.

## Native extraction

1. Process every physical page in ascending order.
2. Extract readable native text and native tables with bundled PDF tools.
3. Preserve table titles, headers, row order, footnotes, units, and original strings.
4. Keep uncertain output and add a warning; never repair values by guessing.
5. Add exactly one page object for each physical page.
6. If relevant content is visually encoded and unreadable natively, set `requires_vision=true`.
7. Derive `vision_pages` as the unique ascending page numbers requiring vision.

Do not persist page maps, coordinates, extraction evidence, screenshots, crops, or visual-task descriptions.

## Temporary and saved PDFs

When extraction does not include an explicit download request, place the verified PDF in a task-temporary directory and remove it after success or failure. When download is explicitly requested, the verified PDF may remain beside `extracted.json`.

The frozen influenza sample contains 19 physical pages; its extraction must contain 19 ordered page objects.
