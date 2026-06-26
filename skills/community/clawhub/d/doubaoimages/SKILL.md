---
name: doubaoimg
description: Generate images with Doubao web chat, extract the final generated image URL from the page, save the image locally, and return the saved local path. Use when the user wants a low-cost browser-based image generation workflow instead of paid image APIs, especially for portraits, concept images, and local saving.
---

# Doubao Local Image Saver

Use this skill when the user wants to:
- use 豆包网页生图
- save the final generated image to local disk
- get back the saved local file path

## Inputs

Collect or infer:
- `prompt`: image prompt for 豆包
- `output_path`: local save path

If the user does not specify an output path, default to a timestamped file name in:
- `C:\Users\Administrator\.openclaw\workspace\tmp\`

Use this naming pattern:
- `doubao-YYYYMMDD-HHMMSS.png`

Example:
- `C:\Users\Administrator\.openclaw\workspace\tmp\doubao-20260318-131500.png`

## Workflow

### 1) Open Doubao

Open:
- `https://www.doubao.com/chat/`

Assume the user may already be logged in. Do not force re-login unless the page clearly requires it.

### 2) Submit the prompt

Preferred path:
1. Focus the chat textbox
2. Enter the prompt
3. Send it
4. Wait for generation to complete

If normal browser click/type fails on the textbox, use browser `evaluate` fallback.

Use this pattern when needed:

```js
() => {
  const ta = document.querySelector('textarea');
  if (!ta) return { ok: false, reason: 'no textarea' };
  const text = 'PROMPT_HERE';
  const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
  setter.call(ta, text);
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  ta.dispatchEvent(new Event('change', { bubbles: true }));
  return { ok: true, valueLength: ta.value.length };
}
```

If Enter does not submit, click the likely send button near the lower-right side of the input area.

### 3) Extract the highest-quality image URL

Do not assume the first visible image URL is the original file. Visible Doubao images often use display URLs containing clues like:
- `downsize`
- `watermark`

Those are usually preview assets, not the best download source.

Use this priority order:

#### Priority A: use Doubao's native download flow

After generation completes:
1. click the chosen generated image to open preview/lightbox
2. look for a button whose text or label suggests `下载`
3. click that button if present
4. if the browser exposes a direct URL, prefer that asset over page image URLs

#### Priority B: inspect preview-state DOM images

If preview opens but no explicit download button is found, inspect images again while the large preview is open.
Prefer the image candidate with the largest natural dimensions.

Use this pattern:

```js
() => {
  return [...document.images]
    .map((img, i) => ({
      i,
      src: img.src,
      width: img.naturalWidth,
      height: img.naturalHeight,
      alt: img.alt || ''
    }))
    .filter(x => x.width > 100 && x.height > 100)
    .filter(x => !x.src.startsWith('data:image/svg+xml'))
    .sort((a, b) => (b.width * b.height) - (a.width * a.height));
}
```

#### Priority C: inspect page images and rank quality

If no preview/download path works, inspect normal page images and rank them.
Use this pattern:

```js
() => {
  return [...document.images]
    .map((img, i) => ({
      i,
      src: img.src,
      width: img.naturalWidth,
      height: img.naturalHeight,
      alt: img.alt || '',
      score: (img.naturalWidth * img.naturalHeight)
    }))
    .filter(x => x.width > 100 && x.height > 100)
    .filter(x => !x.src.startsWith('data:image/svg+xml'))
    .sort((a, b) => b.score - a.score);
}
```

Pick the best result by this order:
1. native download result
2. largest preview-state image URL
3. largest page image URL without `downsize` / `watermark`
4. if all page URLs are processed previews, use the largest one as fallback

When comparing URLs, prefer the one that:
- has the largest dimensions
- comes from preview/download state rather than the base chat card
- does **not** contain `downsize`
- if available, prefer `image_pre` or original image-generation asset URLs over tiny chat thumbnails
- only accept `watermark` variants when they are still the highest-quality accessible preview
- looks like an original CDN asset rather than a transformed display asset

### 4) Save the image locally

Download the chosen URL directly to a local file.

If the user did not provide `output_path`, generate one with a timestamp first.

Use this pattern:

```powershell
@'
from datetime import datetime
import pathlib
base = pathlib.Path(r'C:\Users\Administrator\.openclaw\workspace\tmp')
base.mkdir(parents=True, exist_ok=True)
out = base / f"doubao-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
print(out)
'@ | python -
```

Then download to that path:

```powershell
@'
import urllib.request
url = 'IMAGE_URL_HERE'
out = r'OUTPUT_PATH_HERE'
urllib.request.urlretrieve(url, out)
print(out)
'@ | python -
```

### 5) Return the local path

After saving, confirm the file exists and return:
- the final local save path
- optionally the original image URL if useful

## Token-saving rules

To reduce token waste:
- do not repeatedly snapshot the full page unless the state is unclear
- after submit, wait briefly, then inspect DOM images directly
- prefer preview/download-state DOM inspection over repeated screenshots
- use direct download instead of screenshot cropping whenever possible
- only fall back to screenshot capture if no usable real image URL is available

## Failure handling

### Doubao not logged in
Ask the user to log in on the opened page, then continue.

### No textarea found
Refresh once and retry. If still missing, inspect for iframe or layout change.

### Only low-resolution preview URLs found
Try this sequence:
1. click one generated image to open preview
2. look for `下载` button or download-style control
3. inspect preview-state DOM images and choose the largest candidate
4. only if all URLs still contain transformed preview hints like `downsize`/`watermark`, use the largest fallback URL

### No final image URL found
Wait once more, inspect DOM again, then fall back to screenshot-based capture only if absolutely necessary.
