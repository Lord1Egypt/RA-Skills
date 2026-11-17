# bim revit: exports, model queries, C# against the Revit API

Full verb list: `bim describe --driver revit --json`. Domain notes: `https://bimcli.com/revit/llms.txt` (where it disagrees with `describe`, trust `describe`).

Needs Revit 2022 or newer installed and licensed. bim talks to a small add-in inside Revit over a local socket.

## Connect

```bash
bim revit status            # running? add-in loaded? which document is active?
bim revit instances         # every live Revit: pid, year, port, active document
bim revit install           # once per Revit year, if status says the add-in is missing
bim revit launch [--path model.rvt]   # start Revit and wait for the add-in (slow: minutes)
bim revit open --path C:/proj/model.rvt [--detached]   # --detached for workshared centrals
```

**The user's Revit is their workspace.** If `status` shows a document already open, work against it read-only unless the user asked for changes, and never `kill`, `restart` or `open --close-others` a session you didn't start.

## Read the model (no transaction, safe)

| Question | Verb |
|---|---|
| Sheets in the model | `sheet-list` |
| Elements of a category | `element-list --category Doors [--level "Level 1"] [--properties Mark,Width]` |
| A schedule's rows | `schedule-read --name "Door Schedule"` |
| Model warnings | `warnings-export` |
| Linked models | `linked-models` |
| Parameter names/values for a category | `param-dump` |
| Survey/base point, origin | `coords` |
| Which Revit year saved a file (no Revit needed) | `rvt-version <file>` |

## Export sheets to PDF

```bash
bim revit export --sheets A101,A102 --output C:/out          # combined PDF + embedded BIM sidecars
bim revit export --all-sheets --output C:/out --per-sheet
bim revit export --sheet-set "Issue 03" --output C:/out --no-bim   # plain PDF only
bim revit export --all-sheets --preflight                    # check for raster triggers, write nothing
```

By default the PDF is a **PDF-BIM package** (elements, marks, scales, levels, annotations, titleblock sidecars embedded). Read it back with `bim pdf` (see `references/pdf.md`). Exports stream NDJSON progress and can take minutes; wait for the final line.

## Anything else: `exec` (C# against the Revit API)

```bash
bim revit exec --no-transaction --code "return new FilteredElementCollector(doc).OfClass(typeof(Wall)).GetElementCount();"
bim revit exec --file script.cs --args-json @args.json
```

- Use a convenience verb first if one exists (`describe` lists them, plus `bim revit alias` for saved scripts).
- Look APIs up instead of guessing: `bim revit api.search --query Toposolid --kind all`, `bim revit api.type --name Autodesk.Revit.DB.Wall`. Both work without Revit running.
- `--compile-only` type-checks a script without touching Revit. Do this before any non-trivial script.
- `--no-transaction` for reads. Writes run inside an automatic transaction; `--rollback` runs the write and then rolls it back, which is the way to test a change before keeping it.
- `return` a value: it is serialised to JSON as the result. Keep it to plain objects/lists of ids, strings and numbers.

## Pitfalls

- **`exec` launches Revit if it is not running.** That takes minutes and opens a GUI on the user's desktop. Check `status` first and ask before launching.
- **Several instances:** without `--instance <pid>`, bim picks the newest Revit year and only warns on stderr. Pin it whenever `instances` shows more than one.
- **Timeouts:** exec defaults to 30s, export and launch to 300s. Raise with `--timeout` (or `BIM_REVIT_EXEC_TIMEOUT` / `BIM_REVIT_EXPORT_TIMEOUT`) instead of retrying.
- **A blocking dialog in Revit** (unsaved changes, missing links) stalls every call. `--dismiss-stale-dialogs` cancels it on exec; otherwise tell the user to clear it.
- **Units:** Revit internal units are feet. `move --dx` and coordinates from `location` are in feet.
- Error kind `driver-outdated` means the verb needs a newer driver; re-run the installer to upgrade.
