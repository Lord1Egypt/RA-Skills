# Adaptive — Phone, Tablet, Foldable, Web, and Desktop

Two separate questions, routinely conflated: **how much room do I have** (responsive) and **what platform conventions apply** (adaptive). A tablet layout on a phone-shaped window is wrong; iOS switches on a Windows desktop are also wrong, and they are different bugs.

## Size: Which API

| Question | API | Note |
|---|---|---|
| How much room does MY parent give me | `LayoutBuilder` | The honest answer; works inside splits, sheets, and panes |
| How big is the window | `MediaQuery.sizeOf(context)` (`flutter >=3.10`) | Rebuilds only on size change, unlike `MediaQuery.of` |
| Where are the system bars and notches | `MediaQuery.paddingOf`, or `SafeArea` | `padding` already subtracts what `SafeArea` consumed above you |
| How tall is the keyboard right now | `MediaQuery.viewInsetsOf(context).bottom` | Zero when closed (`forms.md`) |
| Is the device in landscape | `MediaQuery.orientationOf` | Derived from the aspect ratio, not from a sensor |
| Text size the user chose | `MediaQuery.textScalerOf` | A layout input (`accessibility.md`) |

`MediaQuery.of(context)` for any single field subscribes to all of them: the widget then rebuilds on keyboard open, rotation, and inset changes (SKILL.md Traps). Use the aspect accessors.

**`LayoutBuilder` over `MediaQuery` for component-level decisions.** A card that consults the window size renders a tablet layout inside a phone-width side panel. Only the top-level scaffold should reason about the window.

## Breakpoints

Material 3's window size classes give a defensible default set — compact below 600, medium 600 to 839, expanded 840 to 1199, large 1200 to 1599, extra-large 1600 and up (logical pixels, measured on width):

| Class | Typical layout | Navigation |
|---|---|---|
| Compact | One pane | Bottom navigation bar |
| Medium | One pane, wider gutters, or list-detail on landscape | Navigation rail |
| Expanded | Two panes (list + detail) | Navigation rail, or a drawer |
| Large / extra-large | Two or three panes, capped content width | Permanent navigation drawer |

- Use these as defaults, not doctrine: the honest breakpoint is where YOUR content breaks. Widen the window until the design fails, and put the boundary there.
- Cap the content width on large windows (a `ConstrainedBox` around the reading column). Full-width body text on a desktop monitor is unreadable no matter how correct the layout code is.
- List-detail is the payoff pattern: on compact, tapping a row pushes a route; on expanded, it selects into the second pane. That means the selection must live above both panes, not inside the list (`architecture.md`).

## Platform Conventions

- `Theme.of(context).platform` and `defaultTargetPlatform` report the platform; `kIsWeb` must be checked FIRST, since `dart:io`'s `Platform` throws on web (SKILL.md Traps).
- `Platform.isX` also lies during development: `defaultTargetPlatform` can be overridden for testing, `Platform.isX` cannot.
- Material vs Cupertino is a product decision, not a technical one. Three defensible positions: one Material design everywhere (cheapest, and increasingly normal), platform-adaptive widgets at the touchpoints users notice (switches, dialogs, scroll physics, page transitions), or two full designs (expensive, justified for platform-flagship apps). Record it under the design-system preference area (SKILL.md Configuration).
- Where users actually notice the difference: page transitions and swipe-back, alert dialogs, switches and pickers, scroll bounce physics, text selection handles, and the position of destructive actions. `Switch.adaptive`, `showAdaptiveDialog`, and friends cover several of these with one call.
- The safe-area double-padding trap: a `SafeArea` inside another `SafeArea` adds nothing (the inner one sees zero remaining padding), but a `SafeArea` around a scrollable clips the content behind the system bars instead of letting it scroll under. Put `SafeArea` inside the scrollable's slivers, or use `bottom: false` deliberately.

## Web

- The URL is application state. Path-based routing requires the host to serve `index.html` for unknown paths, or a refresh on a deep route returns 404 (`navigation.md`).
- There is no `dart:io`: file paths, `Platform`, and most local-storage plugins are unavailable or shimmed. Guard imports with conditional imports rather than runtime checks, since the import itself fails to compile.
- The first load downloads the engine plus your app. Treat initial bundle size as a product requirement, use deferred loading for routes users may never reach, and measure on a throttled connection.
- Text selection, right-click menus, hover states, and browser zoom all exist on web and nowhere else on mobile. Hover in particular changes layout expectations — `MouseRegion` and `InkWell`'s hover states are not decoration.
- SEO and social previews do not come from a canvas-rendered app. If they matter, that is a server-rendered surface next to the app, not a Flutter setting.
- CORS is the most common "works locally, fails deployed" web issue, and it is a backend fix.

## Desktop

- Windows can be resized to absurd shapes at runtime: a layout that assumes a minimum width breaks live, not at launch. Set a minimum window size, and test by dragging.
- Keyboard is a first-class input: every action needs a reachable focus path, `Shortcuts`/`Actions` for accelerators, and Escape to dismiss. Focus traversal order follows the widget tree, not the visual layout (`forms.md`).
- Mouse affordances: hover feedback, correct cursors (`MouseRegion(cursor:)`), right-click context menus, and scroll-wheel behavior that does not fight trackpad momentum.
- Multi-window, menu bars, tray icons, and file drag-and-drop come from packages, not the framework — check maintenance before designing around them (`dependencies.md`).
- Desktop text conventions differ from mobile: dense layouts, smaller tap targets are acceptable for mouse input but the keyboard path must still work (`accessibility.md`).

## Foldables and Unusual Shapes

- `MediaQuery.of(context).displayFeatures` reports hinges and cutouts; `DisplayFeatureSubScreen` keeps a dialog off the fold.
- A hinge splits the window into two logical panes: the two-pane layout you built for tablets is the right answer, keyed on display features rather than on width alone.
- Orientation changes and fold/unfold rebuild with a new size and can destroy state if the layout swaps widget types at the boundary (`state.md` element reuse). Keep the same widget types across breakpoints where state must survive; where it cannot, lift the state above the branch.
