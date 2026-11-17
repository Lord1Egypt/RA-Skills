# Excalidraw file format reference

Contents: [Standard file (.excalidraw)](#standard-file-excalidraw) · [Obsidian file (.excalidraw.md)](#obsidian-file-excalidrawmd) · [Element fields](#element-fields) · [Bindings must be two-way](#bindings-must-be-two-way) · [Palette](#palette)

For manual layouts/edits, then `scripts/validate.py`. Baseline: `@excalidraw/excalidraw` 0.18 and the Obsidian plugin file layout.

## Standard file (.excalidraw)

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": { "gridSize": 20, "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

## Obsidian file (.excalidraw.md)

Frontmatter identifies an Obsidian drawing. `## Text Elements` exposes labels to search/block links; ` ^<id>` binds each label. `%%` hides scene JSON in reading view.

````markdown
---

excalidraw-plugin: parsed
tags: [excalidraw]

---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'


# Excalidraw Data

## Text Elements
Orders API ^aB3dE5fG7hJ9kL1mN3pQ

%%
## Drawing
```json
{"type":"excalidraw","version":2,"source":"https://github.com/zsviczian/obsidian-excalidraw-plugin","elements":[],"appState":{"gridSize":20,"viewBackgroundColor":"#ffffff"},"files":{}}
```
%%
````

If the plugin saves the note with compression on, the block becomes ```` ```compressed-json ````; `validate.py` then checks only the frontmatter.

## Element fields

Required: `id`, `type`, `x`, `y`, `width`, `height`. Write these additional fields for stable rendering:

| Field | Value |
|-------|-------|
| `angle` | `0` (radians) |
| `strokeColor`, `backgroundColor` | hex colour; background `"transparent"` for none |
| `fillStyle` | `"solid"`, `"hachure"`, `"cross-hatch"` |
| `strokeWidth` | `1`, `2` (normal), `4` |
| `strokeStyle` | `"solid"`, `"dashed"`, `"dotted"` |
| `roughness` | `0` clean, `1` sketch, `2` very rough |
| `opacity` | `0` to `100` |
| `groupIds` | `[]` |
| `frameId` | `null` |
| `roundness` | `{"type": 3}` rounded rectangle, `{"type": 2}` for ellipses, diamonds and curved arrows, `null` for sharp |
| `seed`, `versionNonce` | any positive integers |
| `version` | `1` |
| `isDeleted` | `false` |
| `boundElements` | `null` or a list of `{"id": ..., "type": "text"\|"arrow"}` |
| `updated` | any number; `1` is fine |
| `link` | `null` or a URL |
| `locked` | `false` |

`index` (fractional ordering) can be left out; Excalidraw assigns it on load. Element order in the array is the drawing order, so put background frames first.

### Text

Extra fields: `text`, `originalText` (same value), `fontSize`, `fontFamily`, `textAlign` (`left`, `center`, `right`), `verticalAlign` (`top`, `middle`), `containerId` (`null` or the shape or arrow it sits in), `autoResize: true`, `lineHeight: 1.25`.

`fontFamily` values: 1 Virgil, 2 Helvetica, 3 Cascadia, 5 Excalifont (current hand-drawn default), 6 Nunito, 7 Lilita One, 8 Comic Shanns. Use 14 px or more; 20 for node labels and 16 for edge labels read well.

Width is roughly `characters × fontSize × 0.6` for Latin text and `× 1.0` for CJK; height is `lines × fontSize × 1.25`.

### Arrows and lines

Extra fields: `points` (offsets from the element's `x`/`y`, first point `[0, 0]`), `startBinding`, `endBinding`, `startArrowhead` (`null`, `"arrow"`, `"bar"`, `"dot"`, `"triangle"`), `endArrowhead`, `lastCommittedPoint: null`, `elbowed: false`.

A binding is `{"elementId": "<shape id>", "focus": 0, "gap": 4, "fixedPoint": null}`.

## Bindings must be two-way

- A label inside a shape: the text has `containerId: "<shape id>"` and the shape's `boundElements` contains `{"id": "<text id>", "type": "text"}`.
- A label on an arrow: same pattern, with the arrow as the container.
- An arrow between shapes: `startBinding`/`endBinding` name the shapes, and each shape's `boundElements` contains `{"id": "<arrow id>", "type": "arrow"}`.

One-way bindings can detach during editing; the validator rejects them.

## Palette

| Name | Stroke | Fill |
|------|--------|------|
| blue | `#1971c2` | `#a5d8ff` |
| green | `#2f9e44` | `#b2f2bb` |
| red | `#e03131` | `#ffc9c9` |
| orange | `#e8590c` | `#ffd8a8` |
| purple | `#9c36b5` | `#d0bfff` |
| yellow | `#e67700` | `#fff3bf` |
| cyan | `#0c8599` | `#c3fae8` |
| pink | `#c2255c` | `#eebefa` |
| gray | `#495057` | `#e9ecef` |

Use dark text (`#1e1e1e`) on light fills.
