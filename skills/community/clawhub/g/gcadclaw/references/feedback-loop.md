# Feedback loop

Read this reference for every gcadclaw drawing task and every repair.

## Required artifacts

Each successful drawing-modifying workflow must include:

- `brief.md`
- `actions.jsonl`
- `before_entities.json`
- `after_entities.json`
- at least one PNG screenshot
- `feedback.md` or `feedback.json`
- final `.dwg` path when save succeeds

## Validation hierarchy

1. The script or action sequence ran without uncaught exceptions.
2. The `.dwg` was saved to the expected path.
3. `after_entities.json` contains the expected object classes and layers.
4. Entity counts and handles match the task intent.
5. Dimensions, labels, hatches, and tables required by the brief exist.
6. Screenshot capture succeeded after an appropriate zoom or viewport operation.
7. The screenshot is nonblank and not a uniform black/white repaint failure.
8. Visual inspection of the screenshot does not reveal missing, stale, or off-screen geometry.

## Failure classes

- **COM connection**: pywin32 unavailable, GstarCAD not registered, no active document, or startup failure.
- **Source/action**: syntax error, unknown `pygcadwin` API, missing required tool argument.
- **Geometry**: missing object, wrong scale, open outline, bad coordinate assumption, or duplicated entity.
- **Layer/style**: entity on the wrong layer, missing color/linetype/lineweight, or title/dimension layer misuse.
- **Screenshot**: no window handle, empty client area, capture backend failure, blank/uniform image, stale window content, or PNG file not written.
- **Save**: output directory missing, save path invalid, or GstarCAD save error.

## Repair procedure

1. Read the failing command output, entity JSON, and screenshot state.
2. Classify the failure.
3. Patch the smallest responsible source/action.
4. Rerun only the failed step and any dependent evidence capture.
5. Record the failed attempt and repair in `feedback.md`.

If screenshot capture fails or produces a blank/uniform image, try one focused repair: ensure GstarCAD is visible, restore or maximize the window, call `ctx.zoom_extents()`, wait briefly for repaint, and retry `ctx.view.snapshot().save(path)`. If it still fails, mark the workflow partial; entity evidence alone is not a full success.

## Feedback report

Recommended `feedback.md` shape:

```text
# GcadClaw Feedback

Files:
- Brief: ...
- Actions: ...
- Before entities: ...
- After entities: ...
- Screenshot: ...
- DWG: ...

Validation:
- Execution: pass/fail
- Save: pass/fail
- Entity evidence: pass/fail
- Screenshot: pass/fail
- Visual review: pass/fail/partial

Repairs:
- ...

Assumptions:
- ...

Caveats:
- ...
```
