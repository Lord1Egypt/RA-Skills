# Performance

## Rebuild discipline

Flutter's performance model is fundamentally about minimizing the amount of widget tree that has to rebuild/relayout/repaint per frame. Most "jank" complaints trace back to one of these:

- **Missing `const`.** A `const` widget is skipped entirely during rebuilds if its parent rebuilds but its inputs haven't changed. Run `dart fix --apply` for quick wins, but also manually check `build()` methods — `const_constructors` lint doesn't catch everything (e.g. it won't tell you to *restructure* code to make more of the tree const-able).
- **Rebuilding too much from one `setState`/notifier change.** If calling `setState` at the top of a screen rebuilds a whole scrollable list, extract the parts that don't depend on that state into their own `const` or separately-listening widgets.
- **`context.watch`/`Consumer`/`BlocBuilder` scoped too broadly.** Wrap only the smallest subtree that actually needs to rebuild, not the whole screen.

## Lists

- Always use `ListView.builder` / `GridView.builder` (or `SliverList.builder`) for lists that could be long — never `ListView(children: [...])` with a dynamically-sized or unbounded list, since that builds every item eagerly.
- Give list items a stable `key` when the list can reorder/insert/delete, so Flutter can match elements correctly instead of rebuilding everything.
- For very long/complex lists, check `addAutomaticKeepAlives`/`addRepaintBoundaries` defaults aren't being fought against, and consider `ListView.separated` instead of manually inserting dividers as list items.

## Images

- Never load a full-resolution image just to display it as a 48x48 thumbnail — specify `cacheWidth`/`cacheHeight` on `Image` (or use a package like `cached_network_image` with resizing) so decoding happens at the display size, not source size. This is one of the highest-leverage fixes for memory and jank on image-heavy screens.
- Use `cached_network_image` (or similar) for network images so they aren't re-fetched/re-decoded on every rebuild/scroll.
- Prefer modern compressed formats (WebP) for bundled assets where platform support allows, to reduce app size.

## Build/startup time

- Keep `main()` lean before `runApp()`. Heavy synchronous initialization (large JSON parsing, blocking I/O) delays first frame. Move non-critical initialization to after first frame (`WidgetsBinding.instance.addPostFrameCallback`) or lazy-init on first use.
- Watch for expensive work inside `build()` — any parsing, filtering, sorting, or computation that doesn't need to happen every frame should be memoized/cached or moved to state that's computed once when its inputs change, not recomputed on every rebuild.

## Isolates

CPU-heavy work (large JSON decode/encode, image processing, heavy computation) on the main isolate blocks the UI thread and causes visible jank. Use `compute()` (a convenience wrapper around isolates) for one-off heavy work, or a full `Isolate`/`isolate` package for sustained background work. This is easy to miss because it "works" in testing with small data and only becomes visibly janky with production-sized payloads — worth asking about data size when reviewing JSON parsing code.

## Measuring, not guessing

Don't recommend performance changes purely by inspection when a real measurement is available and the stakes are non-trivial. Point users to:
- **Flutter DevTools** — Performance tab (frame times, jank), Memory tab (leaks, image cache size), Widget rebuild stats.
- `flutter run --profile` (not debug mode — debug mode has overhead that makes timing numbers meaningless) for any real performance investigation.

## App size

- `flutter build apk --analyze-size` / `--split-per-abi` to avoid shipping all architecture binaries in one APK.
- Check for unused/duplicate large assets bundled into `assets/`.
- Tree-shaking icons: use `flutter build --tree-shake-icons` (default in release builds) — but note it requires icon fonts to only be referenced via `IconData` const literals, not dynamically constructed ones, or tree-shaking silently can't apply.
