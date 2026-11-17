# Darktable 5.6 interface and navigation

## Contents

- Version scope
- Global layout
- Lighttable layout
- Darkroom layout
- Finding and operating modules
- Panels and shortcuts
- Screenshot-reading checklist

## Version scope

Use these names and locations as the baseline for Darktable 5.6.0 and the official development manual read on 2026-06-30. The development manual is continuously updated and is not a frozen 5.6 manual. When a screenshot disagrees, follow the screenshot and verify the installed version.

Official sources:

- [Development user manual](https://docs.darktable.org/usermanual/development/en/)
- [Darkroom view layout](https://docs.darktable.org/usermanual/development/en/darkroom/darkroom-view-layout/)
- [Module organization](https://docs.darktable.org/usermanual/development/en/darkroom/organization/overview/)
- [Darktable 5.6.0 release notes](https://www.darktable.org/2026/06/darktable-5.6.0-released/)

## Global layout

All views use the same main regions:

1. Center area: view-specific content; the developed image in darkroom.
2. Left panel: information and utility modules.
3. Right panel: image processing in darkroom; selection and actions in lighttable.
4. Top banner: current version and view switcher.
5. Top panel: global settings, filters, sort controls, and shortcuts.
6. Bottom panel: view-specific controls and warnings.
7. Filmstrip/timeline: optional image strip at the bottom.

Views in the top banner are `lighttable`, `darkroom`, `map`, `print`, `slideshow`, and `tethering`. Their default shortcuts are L, D, M, P, S, and T.

Resize a side panel by dragging its inner border. Collapse a panel with the small triangle on its outer edge. A hidden panel or search bar may reflect a custom workspace, not a removed feature.

## Lighttable layout

The center area shows the current collection in file-manager, zoomable-lighttable, culling, or full-preview mode.

Common left-panel modules:

- `import`
- `collections`
- `recently used collections`
- `image information`
- optional Lua-related utility modules, depending on build/version

Common right-panel modules:

- `selection`
- `actions on selection`
- `history stack`
- `styles`
- `metadata editor`
- `tagging`
- `geotagging`
- `export`

The bottom panel holds star ratings, color labels, the lighttable mode selector, thumbnail zoom, focus peaking, and display-profile selection. In 5.6, touchpad pinch zoom and two-finger pan are available in lighttable culling layouts when the preference is enabled.

## Darkroom layout

The center area is the image canvas. Middle-click cycles among fit, 1:1, and 2:1. Scrolling or a touchpad gesture can zoom according to preferences. Judge composition and global grading zoomed out; judge focus/noise at 100%.

Common left-panel utility modules:

- `navigation`
- `snapshots`
- `duplicate manager`
- `global color picker`
- `tagging`
- `image information`
- `mask manager`
- `export`

The right panel contains, from top to bottom:

- `scopes`;
- quick access, active modules, module groups, and module-layout preset menu;
- optional module search line;
- processing modules in pixelpipe order;
- `module order` at the bottom.

The bottom toolbar contains quick access to presets, styles, the second darkroom window, focus peaking, color assessment, high-quality processing, raw-overexposure warning, clipping warning, soft proof, gamut check, and guides/overlays. In 5.6, the second window can pin an image so it remains fixed while the main view or history changes.

Right-click an empty area of a side panel to list available utility modules and toggle visibility. Drag a utility module to change its panel position. Processing-module execution order is managed separately.

## Finding and operating modules

Use the search line beneath the group icons. It searches module name, user-defined instance name, and built-in tags such as hue, contrast, or vibrance.

Module group layouts are presets and can be customized. Common layouts include:

- `modules: all`;
- `workflow: scene-referred`;
- `workflow: display-referred`;
- `workflow: beginner`;
- `search only`;
- `modules: deprecated`.

The `modules: deprecated` layout is a compatibility path. Modules can eventually disappear from new edits after the deprecation period.

The processing-module header contains, from left to right:

- power: enable/disable;
- module name and instance name;
- mask indicator when a mask is active;
- multiple-instance menu;
- reset;
- presets menu.

Click the module name to expand it. Expansion does not enable processing. Ctrl-click the name to rename the instance. Use the multiple-instance menu to create, duplicate, move, delete, or rename instances. Each extra instance increases processing cost.

Use Shift-click on a module header to keep multiple modules expanded. Reset returns controls to defaults; Ctrl-click reset can reapply automatic presets. Warn the user before either action when it could erase deliberate settings.

The history stack records the sequence of edits. It does not show processing order. The processing modules on the right are executed from the bottom upward. Avoid moving modules unless the interaction is understood; a visually earlier editing step need not be moved lower in the pixelpipe.

## Panels and shortcuts

Useful default shortcuts:

- Tab: temporarily hide panels and fill the window with the center view.
- F11: full screen.
- Shift+Ctrl+T: top panel.
- Shift+Ctrl+B: bottom panel.
- Shift+Ctrl+L: left panel.
- Shift+Ctrl+R: right panel.
- Ctrl+F: filmstrip/timeline.
- Ctrl+H: top banner.
- B: panel-border and collapse controls.
- H: show shortcuts applicable to the current view.
- Ctrl+B in darkroom: color-assessment mode.

Shortcuts are customizable. When the key does not work, direct the user to Preferences > shortcuts or press H; do not insist that a default binding must still be present.

## Screenshot-reading checklist

When interpreting a screenshot, identify:

1. view name and installed version if visible;
2. left/right/bottom panels that are hidden;
3. selected module-layout preset and whether search is enabled;
4. active tone mapper: `sigmoid`, `AgX`, or `filmic rgb`;
5. power state versus expanded state;
6. mask indicator and multiple instances;
7. warning icons and clipping overlays;
8. history-stack position versus module order;
9. localized labels that may differ from the English manual;
10. whether the screenshot shows a RAW edit, exported image, or embedded JPEG preview.
