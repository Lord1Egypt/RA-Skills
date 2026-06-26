---
name: dom-to-image
description: Convert HTML DOM nodes to images (PNG/JPEG/SVG/Blob). Supports rendering options such as filter, backgroundColor, quality, and pixelRatio.
---

# HTML DOM To Image

Convert any HTML DOM node into an image in PNG, JPEG, SVG, or Blob format.

## Use Cases

Users request to convert HTML content to an image, take a screenshot of a web page element, generate a PNG/JPEG cover image, or export a specified DOM node as an image file.

## Installation

Install html-to-image in the project directory:

```bash
npm install html-to-image
```

## Core Workflow

**Step 1: Target the DOM Node**

Get the HTML element to convert using a `selector`:

```js
const node = document.querySelector('#target-element');
```

**Step 2: Choose Output Format**

| Format | Function | Description |
|--------|----------|-------------|
| PNG | `toPng(node, options)` | Default format, transparency preserved |
| JPEG | `toJpeg(node, { quality: 0.95 })` | Compressible, suitable for photos |
| SVG | `toSvg(node, { filter })` | Vector format |
| Blob | `toBlob(node)` | Binary format, suitable for file downloads |

**Step 3: Trigger Download**

```js
htmlToImage.toPng(node, { cacheBust: true })
  .then((dataUrl) => {
    const link = document.createElement('a');
    link.download = 'my-image.png';
    link.href = dataUrl;
    link.click();
  })
  .catch((err) => console.error('oops, something went wrong!', err));
```

## Common Rendering Options

| Option | Type | Description |
|--------|------|-------------|
| `backgroundColor` | string | CSS color value, e.g. `'#ffffff'` |
| `width`, `height` | number | Pixel dimensions to apply to the node before rendering |
| `canvasWidth`, `canvasHeight` | number | Scaling dimensions for the canvas |
| `quality` | number | JPEG quality 0~1, default 1.0 |
| `cacheBust` | boolean | Append a timestamp to disable caching, default false |
| `pixelRatio` | number | Pixel ratio; defaults to the device's actual pixel ratio; set to 1 to render at 1x initial scale |
| `filter` | function | `(node) => boolean`, returns true to keep the node |

### filter Example (Exclude Specific Elements)

```js
const filter = (node) => {
  const exclude = ['remove-me', 'secret-div'];
  return !exclude.some(c => node.classList?.contains(c));
};

htmlToImage.toJpeg(node, { quality: 0.95, filter });
```

## React Integration

```tsx
import { useCallback, useRef } from 'react';
import { toPng } from 'html-to-image';

const ExportButton = () => {
  const ref = useRef<HTMLDivElement>(null);

  const onClick = useCallback(() => {
    if (!ref.current) return;
    toPng(ref.current, { cacheBust: true })
      .then((dataUrl) => {
        const link = document.createElement('a');
        link.download = 'my-image.png';
        link.href = dataUrl;
        link.click();
      })
      .catch(console.error);
  }, []);

  return (
    <>
      <div ref={ref}>
        {/* Content to convert */}
      </div>
      <button onClick={onClick}>Download Image</button>
    </>
  );
};
```

## Notes

- Including a CORS-tainted `<canvas>` will cause rendering to fail
- Extremely large DOM nodes may fail due to dataURI length limits
- IE browser is not supported (incompatible with SVG `<foreignObject>`)