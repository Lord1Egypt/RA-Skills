---
name: figma-plugin-writer
description: Write Figma plugin code to automate UI design in Figma files. Activate when user wants to create UI mockups, design systems, app screens, or visual prototypes directly in Figma via plugin code. NOT for: Figma API REST calls, file management, or commenting.
---

# Figma Plugin Writer

Write plugin code (`code.js`) to automate design in Figma files. After updating the code, notify the user to run the plugin.

## Prerequisites

The user must provide:
1. **Plugin directory** — folder containing `code.js` and `manifest.json`
2. **Code file** — typically `code.js`
3. **Target Figma file** — optional, for context

## Workflow

1. Receive design requirements from the user
2. Write plugin code to `code.js`
3. Notify user: `Plugins → Development → <plugin-name>`
4. Iterate based on feedback

## API Reference

### Font Loading (required before creating text)

```js
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
await figma.loadFontAsync({ family: "Inter", style: "Medium" });
await figma.loadFontAsync({ family: "Inter", style: "Semi Bold" });
await figma.loadFontAsync({ family: "Inter", style: "Bold" });
```

### Frame (Container)

```js
var frame = figma.createFrame();
frame.name = "MyFrame";
frame.resize(width, height);
frame.cornerRadius = 12;
frame.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
frame.x = 0;
frame.y = 0;
```

### Text

```js
var text = figma.createText();
text.characters = "Hello World";
text.fontSize = 16;
text.fontName = { family: "Inter", style: "Regular" };
text.fills = [{ type: "SOLID", color: { r: 0, g: 0, b: 0 } }];
```

### Rectangle

```js
var rect = figma.createRectangle();
rect.resize(100, 50);
rect.fills = [{ type: "SOLID", color: { r: 0.9, g: 0.2, b: 0.2 } }];
rect.cornerRadius = 8;
```

### Nesting Nodes

```js
frame.appendChild(text);
parentPage.appendChild(frame);
```

### Drop Shadow

```js
frame.effects = [{
  type: "DROP_SHADOW",
  color: { r: 0, g: 0, b: 0, a: 0.1 },
  offset: { x: 0, y: 4 },
  radius: 12,
  spread: 0,
  visible: true,
  blendMode: "NORMAL",
}];
```

### Stroke

```js
frame.strokes = [{ type: "SOLID", color: { r: 0.8, g: 0.8, b: 0.8 } }];
frame.strokeWeight = 1;
```

### Text Alignment

```js
text.textAlignHorizontal = "CENTER"; // LEFT | CENTER | RIGHT | JUSTIFIED
text.textAlignVertical = "CENTER";   // TOP | CENTER | BOTTOM
```

### Auto Layout (inside Frame)

```js
frame.layoutMode = "VERTICAL"; // or "HORIZONTAL"
frame.primaryAxisAlignItems = "CENTER";   // MIN | CENTER | MAX | SPACE_BETWEEN
frame.counterAxisAlignItems = "CENTER";
frame.paddingTop = 16;
frame.paddingBottom = 16;
frame.paddingLeft = 16;
frame.paddingRight = 16;
frame.itemSpacing = 8;
```

### Page Navigation

```js
var pages = figma.root.children;
var targetPage = pages[pages.length - 1];
await figma.setCurrentPageAsync(targetPage);
```

### Clear Page Content

```js
var old = targetPage.children.slice();
for (var i = 0; i < old.length; i++) {
  old[i].remove();
}
```

### Viewport

```js
figma.viewport.scrollAndZoomIntoView([frame]);
```

### Notifications

```js
figma.notify("Done!", { timeout: 3000 });
figma.notify("ERROR: " + e.message, { timeout: 10000 });
```

### Page Info

```js
var pages = figma.root.children;
var count = pages.length;
var pageName = pages[0].name;
```

## Code Template

```js
async function main() {
  try {
    // 1. Load fonts
    await figma.loadFontAsync({ family: "Inter", style: "Regular" });
    await figma.loadFontAsync({ family: "Inter", style: "Bold" });

    // 2. Get target page
    var pages = figma.root.children;
    var target = pages[pages.length - 1];
    await figma.setCurrentPageAsync(target);

    // 3. Clear old content
    var old = target.children.slice();
    for (var i = 0; i < old.length; i++) old[i].remove();

    // 4. Create design...
    var frame = figma.createFrame();
    frame.name = "Screen";
    frame.resize(375, 812);
    frame.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
    frame.x = 0;
    frame.y = 0;
    target.appendChild(frame);

    // 5. Done
    figma.viewport.scrollAndZoomIntoView([frame]);
    figma.notify("Design complete!", { timeout: 3000 });

  } catch (e) {
    figma.notify("ERROR: " + e.message, { timeout: 10000 });
  }
}

main();
```

## Pitfalls & Gotchas

### documentAccess: "dynamic-page" Mode

If `manifest.json` has `"documentAccess": "dynamic-page"`:
- ❌ `figma.currentPage = page` → ✅ `await figma.setCurrentPageAsync(page)`
- ❌ `figma.getNodeById()` → ✅ `await figma.getNodeByIdAsync()`
- ❌ `figma.closePlugin()` → ✅ `await figma.closePluginAsync()`

### Error Handling

- Always wrap code in `try-catch`
- Show errors via `figma.notify("ERROR: " + e.message, { timeout: 10000 })`
- Do not use emoji in text content (font may not support the glyph)
- Do not call `figma.closePlugin()` automatically (let user close manually)

### Free Tier Limits

- Max 3 Pages — do not create new Pages
- Work within existing Pages (clear and rebuild)

### Fonts

- Default: Inter (built into Figma)
- Supported styles: "Regular", "Medium", "Semi Bold", "Bold"
- Colors use `{ r, g, b }` format with 0-1 range

## Iteration Pattern

On each design iteration:
1. Clear old elements: `page.children.slice().forEach(c => c.remove())`
2. Recreate design with changes
3. Notify user to re-run the plugin
