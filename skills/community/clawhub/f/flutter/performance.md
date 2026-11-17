# Performance — Jank Triage, Rebuilds, and Memory

Two threads own a frame, and the fix depends entirely on which one missed it. The **UI thread** runs Dart: build, layout, paint recording. The **raster thread** turns the recording into GPU commands. Frame budget = 1000 / refresh rate ms — 16.7 ms at 60 Hz, 8.3 ms at 120 Hz (SKILL.md rule 6) — and the two threads share it.

Measure in profile mode on a physical device (SKILL.md rule 7). A debug-mode number ranks nothing.

## Triage Order

1. **Confirm which thread.** DevTools' Performance view colors each frame's UI and raster time separately; the overlay (`flutter run --profile` then `P`) shows two graphs. Tall UI bars → build/layout work. Tall raster bars → painting and GPU work. Both tall → usually a huge widget tree being rebuilt and repainted together.
2. **UI thread: find what rebuilds.** DevTools' rebuild counter (or "Track widget builds") names the widget rebuilding thousands of times. Apply the Rebuild Scope Ladder (SKILL.md).
3. **UI thread with few rebuilds: find the expensive build.** A single widget over budget means computation inside `build` — sorting, filtering, date formatting, regexes (`widgets.md`).
4. **Raster thread: find the expensive paint.** `saveLayer` (opacity on a subtree, `ClipRRect` with antialiasing, blend modes), shadows, blurs, and overlapping translucent layers. The "Highlight layers that need repainting" toggle shows what repaints per frame.
5. **Neither, but the app stalls entirely.** A synchronous block on the UI isolate: a big `jsonDecode`, a file read, a crypto call (`async.md`, isolates).
6. **Nothing reproduces in profile mode.** Then it is a debug-only cost (assertions, the inspector) or a release-only cost (`release.md`) — say which, and stop optimizing.

## Rebuild Cost

- Building widgets is cheap by design; building the WRONG subtree repeatedly is the cost. The ladder in SKILL.md is ordered by yield: `const`, then `child:` hoisting, then extraction, then narrow listening, then moving state down.
- `setState` in a screen-level `State` rebuilds the entire screen. That is the single most common source of "the app feels heavy" in Flutter code, and extraction — not micro-optimization — is the fix.
- A `Builder`, a `Consumer`, or a `ValueListenableBuilder` rebuilds only its own subtree: putting one deep in the tree is how you keep the rebuild small.
- Watch out for accidental full-tree rebuilds: `MediaQuery.of(context)` near the root (keyboard opens → whole app rebuilds), a top-level `ChangeNotifier` that notifies on every tick, or a `ThemeData` object constructed in `build` (new instance → every dependent rebuilds).

## Lists

- `ListView.builder` builds only what the viewport needs plus a cache region; the default `cacheExtent` is 250 logical pixels beyond each edge. Raising it smooths fast flings and costs memory; lowering it saves memory and shows blank tiles.
- `itemExtent` (or `prototypeItem`) lets the viewport compute positions arithmetically instead of measuring children — required for a scrollbar that behaves and for instant `jumpTo` in long lists.
- `addAutomaticKeepAlives: false` and `addRepaintBoundaries: false` are worth setting on very long simple lists: keep-alives defeat recycling, and a repaint boundary per item costs a layer each.
- Per-item work that recurs on every build (date formatting, regex, sorting) should be precomputed into the model once, not recalculated per frame per visible row.
- Nested scrollables and `shrinkWrap: true` are performance bugs disguised as layout fixes (`layout.md`).
- `ListView` with thousands of items and heavy tiles: measure the tile's build in isolation before restructuring the list. Usually one image or one shadow is the whole cost.

## Images

**Decoded size, not file size, is what costs memory: bytes = width × height × 4.** A 4000 × 3000 photo occupies about 48 MB decoded no matter how small the JPEG is. Flutter's `ImageCache` defaults to 1000 entries and 100 MiB — one such photo evicts a large share of the cache, so everything else re-decodes.

- Decode at display size: `Image.network(url, cacheWidth: 400)` (or `cacheHeight`) makes the decoder produce a smaller bitmap. This is the highest-yield memory fix in most image-heavy apps.
- `ResizeImage(provider, width: 400)` is the same idea for any `ImageProvider`.
- Ask the backend for a resized variant when it can produce one; decoding a full-resolution image only to shrink it wastes CPU as well as memory.
- `cached_network_image` adds disk caching and placeholders on top; Flutter's own cache is memory-only and is cleared when the app is backgrounded under pressure.
- `precacheImage` in `didChangeDependencies` removes the pop-in for hero images and above-the-fold content; used on a whole list it defeats the cache budget.
- Very large images that must be shown at full size (maps, scans) need tiling or a specialized viewer — not a bigger cache.

## Paint Cost

- `Opacity` around a subtree triggers `saveLayer`: an offscreen buffer allocated, painted, and composited every frame. On a leaf that paints once, it is cheap; over a list it is a raster-thread killer. Animate with `FadeTransition`, or set the alpha on a color/`Image` directly.
- `ClipRRect` with the default antialiasing also allocates a layer. `Clip.antiAliasWithSaveLayer` is the most expensive option and is rarely needed; a `BoxDecoration(borderRadius:)` on a `DecoratedBox` avoids clipping entirely.
- `BackdropFilter` (frosted glass) is the most expensive common widget: it reads back the framebuffer. One per screen at most, and never inside a scrolling list.
- Shadows are cheap individually and expensive per-item: 50 elevated cards means 50 shadow passes. A single background with a baked shadow image is a legitimate optimization for dense lists.
- `RepaintBoundary` isolates a repainting subtree (an animation, a progress ring) from a static one — but every boundary is a texture in GPU memory. Add them at animation boundaries, not everywhere.

## Startup Time

- The first frame cannot render until `runApp` runs. Everything awaited before it — reading preferences, opening a database, initializing a crash reporter, fetching remote config — is added directly to the user's wait (`architecture.md`, bootstrap).
- Move anything not needed for the first screen behind the first frame: show the UI, then hydrate.
- The native splash screen covers the gap only up to the first Flutter frame; a slow first build shows a blank window after the splash disappears.
- Deferred loading matters most on web, where code the user has not reached should not be in the initial bundle (`release.md`).

## Memory

- DevTools' Memory view: a sawtooth that always returns to the same floor is healthy; a floor that climbs across navigation cycles is a leak.
- The standard leak test: push a screen, pop it, force a GC, and check whether its `State` is still reachable. The usual culprits are an uncancelled subscription, a listener never removed, a `Timer.periodic`, or a static/global reference to a widget's state (SKILL.md rule 3).
- Keep-alives and `IndexedStack` retain whole subtrees deliberately (`state.md`) — count that as expected usage, not a leak, and bound how many pages you keep.
- Image memory dominates most Flutter apps' footprint; check it before hunting for object leaks.

## Shader and First-Run Jank

Historically, the first play of an animation compiled its shaders on demand and dropped frames exactly once per effect — the "first run is janky, then it's fine" signature. Impeller precompiles instead, and is the default renderer on iOS since `flutter >=3.10` and on Vulkan-capable Android in later releases; `flutter run --verbose` logs which renderer started. If you see this signature on a current SDK, confirm the renderer before chasing it as a code problem.
