---
name: cleanshot-skill
description: Use when the user wants an OpenClaw agent to choose the right CleanShot Tool plugin call for screenshots, OCR, screen recording, scrolling capture, annotation, pinned references, CleanShot history, Quick Access, or settings. This skill provides workflow guidance only and assumes the CleanShot Tool plugin is installed.
---

# CleanShot Skill

CleanShot Skill is an optional OpenClaw Skill that teaches an OpenClaw agent how to use the CleanShot Tool plugin naturally for screenshots, OCR, screen recording, scrolling capture, annotation, pinned references, and CleanShot history access.

## Relationship To CleanShot Tool

This skill does not provide executable tools.

This skill assumes the CleanShot Tool plugin is installed. The CleanShot Tool plugin provides the actual tools.

This skill is a workflow and decision layer. The CleanShot Tool plugin remains universal and action-focused. This skill provides higher-level usage guidance for the OpenClaw agent.

CleanShot Tool plugin identity:

- Project/repo/package: `openclaw-plugin-cleanshot`
- Plugin id: `cleanshot`
- Public display name: CleanShot Tool

## Expected CleanShot Tool Plugin Tools

- `cleanshot_capture`
- `cleanshot_all_in_one`
- `cleanshot_scrolling_capture`
- `cleanshot_ocr`
- `cleanshot_record_screen`
- `cleanshot_annotate_file`
- `cleanshot_pin_file`
- `cleanshot_quick_access`
- `cleanshot_settings`
- `cleanshot_get_displays`

If these tools are unavailable, tell the user that the CleanShot Tool plugin may not be installed, enabled, loaded, or allowed in the current OpenClaw runtime.

## Default Screenshot Behavior

If the user asks for a screenshot without further details, use `cleanshot_capture` with `mode: "fullscreen"` and `action: "copy"`.

Example user phrases:

- "take a screenshot"
- "screenshot this"
- "capture the screen"
- "сделай скрин"
- "заскринь"

The default action is `copy` because it is usually the fastest workflow for pasting into the current chat, document, or app.

## Sending Screenshots To The Current Chat

If the user asks to "send me a screenshot", "send it here", "share the screenshot", or similar, capture the screenshot and send it to the current connected chat if the environment supports image attachments.

If the environment cannot send image attachments, use `copy` or `save` and clearly explain where the result is.

Do not claim that the image was sent if the environment only copied or saved it.

## Tool Selection Rules

Use `cleanshot_capture` for normal screenshots.

Use `mode: "fullscreen"` when the user wants the whole screen.

Use `mode: "window"` when the user wants a window screenshot.

Use `mode: "area"` when the user wants to select a region manually or the region is unknown.

Use `mode: "previous_area"` when the user asks to repeat the last region, capture the same area again, monitor the same part of the screen, or take repeated evidence screenshots.

Use `mode: "self_timer"` when the user needs time to open a menu, hover state, tooltip, dropdown, context menu, popover, or other transient UI.

Use `cleanshot_all_in_one` when the user wants the general CleanShot capture interface or is unsure what capture mode they need.

Use `cleanshot_scrolling_capture` for long pages, full web pages, long chats, long settings screens, documents, and any content requiring scrolling.

Use `cleanshot_ocr` when the user asks to recognize or extract text from the screen or an image.

Use `cleanshot_record_screen` when the user asks to record the screen.

Use `cleanshot_annotate_file` when the user provides an image filepath and asks to annotate, mark up, blur, label, or edit that image in CleanShot.

Use `cleanshot_pin_file` when the user provides an image filepath and wants the image as a floating reference.

Use `cleanshot_quick_access` when the user asks to open CleanShot, CleanShot history, screenshot history, recent screenshots, capture history, or Quick Access.

Use `cleanshot_settings` when the user specifically asks for CleanShot settings.

## Action Selection Rules For `cleanshot_capture`

Use `copy` when the user wants to paste, send, share, or place the screenshot into a chat or app.

Use `save` when the user wants a file, archive, evidence, report, or persistent screenshot.

Use `annotate` when the user wants arrows, blur, labels, markup, explanation, redaction, or issue-report evidence.

Use `pin` when the user wants a floating visual reference.

Use `upload` only when the user explicitly asks for a CleanShot Cloud link or shareable upload.

## Area And Coordinate Workflow

If the user asks for a region or area but provides no coordinates, use `mode: "area"` and let the user select the area manually.

Do not invent coordinates.

If the user provides coordinates, pass `x`, `y`, `width`, and `height`.

Coordinate meaning:

- `x` is the distance from the left edge of the display.
- `y` is the distance from the top edge of the display.
- `width` is the region width.
- `height` is the region height.

If the user describes a visual area in words, such as "right side", "top-left corner", "this part", or "that panel", prefer manual `area` selection unless exact coordinates are provided.

If the user wants a specific monitor or display and provides a display number, pass `display`.

If the user does not specify display, do not guess display unless the context is obvious.

## Display And Multi-Monitor Behavior

This skill assumes CleanShot Tool v1.1.0 or later provides `cleanshot_get_displays`.

### Default Display Behavior

If the user does not specify a monitor or display, assume the main display / display 1.

Do not ask which monitor if the request can reasonably use the main display.

For simple commands like "take a screenshot", "capture the left side", or "record the screen", default to the main display unless the user says otherwise.

### Explicit Display Selection

If the user specifies a display or monitor, use that display.

Accept phrases such as:

- main monitor
- primary display
- first monitor
- second monitor
- external monitor
- built-in display
- MacBook screen
- left monitor
- right monitor
- display 1
- display 2

Russian phrases may appear only as example user phrases:

- основной монитор
- первый монитор
- второй монитор
- внешний монитор
- экран макбука
- левый монитор
- правый монитор

### When To Call `cleanshot_get_displays`

Call `cleanshot_get_displays` first if the user asks for a named screen region such as:

- left half
- right half
- top half
- bottom half
- center
- left third
- right third
- left side of the second monitor
- right half of the external monitor

Use returned display geometry to calculate `x`, `y`, `width`, and `height`.

Then call the appropriate CleanShot capture or recording tool with calculated coordinates.

If geometry cannot be determined reliably, fall back to manual `area` selection.

### Multi-Monitor Coordinate Rules

Treat each display as a rectangle with its own `x`, `y`, `width`, and `height`.

If the display object includes global desktop coordinates, use them directly.

If both logical and pixel bounds are returned, prefer the coordinate system documented by `cleanshot_get_displays`.

If coordinate compatibility is uncertain, prefer manual area selection instead of guessing.

Do not invent monitor dimensions.

### Region Calculation Rules

For selected display `d`:

Left half:

- `x = d.x`
- `y = d.y`
- `width = d.width / 2`
- `height = d.height`

Right half:

- `x = d.x + d.width / 2`
- `y = d.y`
- `width = d.width / 2`
- `height = d.height`

Top half:

- `x = d.x`
- `y = d.y`
- `width = d.width`
- `height = d.height / 2`

Bottom half:

- `x = d.x`
- `y = d.y + d.height / 2`
- `width = d.width`
- `height = d.height / 2`

Left third:

- `x = d.x`
- `y = d.y`
- `width = d.width / 3`
- `height = d.height`

Middle third:

- `x = d.x + d.width / 3`
- `y = d.y`
- `width = d.width / 3`
- `height = d.height`

Right third:

- `x = d.x + (2 * d.width / 3)`
- `y = d.y`
- `width = d.width / 3`
- `height = d.height`

Center:

- If the user specifies center size, calculate a centered rectangle.
- If the user does not specify size, ask for size or use manual area selection.
- Do not invent arbitrary center dimensions.

### Screenshot Behavior With Displays

For screenshots without a display specified, use the default screenshot behavior from this skill: fullscreen + copy.

For "screenshot second monitor", call `cleanshot_get_displays`, select display 2, then capture that display if the tool supports display selection or use its geometry with area capture.

For "screenshot left half of the second monitor", call `cleanshot_get_displays`, select display 2, calculate left half, then call `cleanshot_capture` with `mode: "area"`, action chosen by context, and coordinates.

### Recording Behavior With Displays

For "record the screen" without display specified, default to main display / display 1.

For "record second monitor", call `cleanshot_get_displays`, select display 2, then use display selection or coordinates with `cleanshot_record_screen`.

For "record left half of the screen", call `cleanshot_get_displays`, select default display, calculate left half, then call `cleanshot_record_screen` with coordinates.

### Scrolling Capture Behavior With Displays

For scrolling capture without monitor specified, default to main display.

For scrolling capture on a specific monitor, select the requested display.

If the user asks for a long page, chat, or document but does not specify exact region, open CleanShot scrolling capture UI and let the user choose the region.

Use calculated geometry only when the region can be determined reliably.

### Ambiguity Handling

If the user says "left monitor" or "right monitor" and display geometry clearly indicates monitor positions, select the matching display.

If monitor positions are unclear, ask the user to specify display number.

If the user says "external monitor" and there is exactly one non-built-in display, use it.

If there are multiple external displays, ask which one.

If the user says "MacBook screen" or "built-in display", use the built-in display if it can be identified.

If it cannot be identified, ask or default to display 1 only when reasonable.

Do not ask unnecessary questions for simple main-display captures.

### Safety

Do not invent display geometry.

Do not invent coordinates.

Prefer manual area selection when uncertain.

Be explicit if a request requires the user to confirm region selection in CleanShot UI.

## Previous Area Workflow

If the user asks for the same area again, use `mode: "previous_area"`.

Example user phrases:

- "same area"
- "repeat the previous area"
- "capture that zone again"
- "сними ту же область"
- "повтори прошлую область"

For repeated captures of the same UI region, first use manual `area`, then use `previous_area`.

## Window Screenshots

If the user asks for a window screenshot, use `cleanshot_capture` with `mode: "window"`.

Choose the action by context:

- `copy` for paste, share, or send
- `save` for file or evidence
- `annotate` for markup

## CleanShot History And Quick Access

If the user says "open CleanShot", interpret it as opening CleanShot history or Quick Access.

Use `cleanshot_quick_access` for:

- "open CleanShot"
- "open screenshot history"
- "show recent screenshots"
- "open CleanShot history"
- "capture history"
- "open Quick Access"

If the user specifically asks for settings, use `cleanshot_settings`.

## Scrolling Capture

Use `cleanshot_scrolling_capture` for long pages, full web pages, long chats, long settings screens, documents, and any content requiring scrolling.

Default behavior should open the CleanShot scrolling capture UI and let the user select or confirm the scroll area.

Do not promise a precise scroll endpoint if the user did not define it.

If the user explicitly asks for autoscroll or automatic start, use `start: true` and `autoscroll: true` if supported by the installed tool/plugin.

Example user phrases:

- "capture the full page"
- "take a scrolling screenshot"
- "screenshot the whole chat"
- "сделай длинный скрин страницы"
- "сними всю страницу с прокруткой"

## OCR

Use `cleanshot_ocr` when the user asks to recognize or extract text from the screen or an image.

Default to `linebreaks: true`.

Do not promise that recognized text will be returned directly to OpenClaw.

CleanShot may show the OCR result in its UI or place it on the clipboard depending on CleanShot behavior and settings.

## Screen Recording

Use `cleanshot_record_screen` when the user asks to record the screen.

Do not claim recording has started if CleanShot only opened recording mode or requires UI confirmation.

If the user asks to record a region and provides no coordinates, open recording mode and let the user select the area.

If the user asks for MP4 or video, use `cleanshot_record_screen` and treat MP4/video as the intended output if CleanShot provides that choice.

If the user asks for GIF, use `cleanshot_record_screen`, but do not promise GIF output unless the tool/API supports selecting GIF directly. Let the user choose GIF in CleanShot UI if available.

Future note: if CleanShot Tool later exposes a format parameter, select MP4 or GIF automatically based on the user request.

## File Tools

Use `cleanshot_annotate_file` when the user provides a filepath and asks to annotate, mark up, blur, label, or edit that image in CleanShot.

Use `cleanshot_pin_file` when the user provides a filepath and wants the image as a floating reference.

The skill should not read, stat, modify, upload, or analyze files directly. It should only pass the filepath to the CleanShot Tool plugin.

## Safety And Privacy

Do not use `upload` unless explicitly requested.

Prefer local `copy` or `save` for private or sensitive screenshots.

Do not invent coordinates.

Do not promise OCR return text directly.

Do not claim recording has started unless confirmed.

Do not claim an image was sent if the environment cannot send attachments.

If CleanShot does not respond, suggest enabling:

```text
CleanShot X -> Settings -> Advanced -> API -> Allow Applications to control CleanShot
```

Be clear when an action opens CleanShot UI rather than completing the whole workflow automatically.

## Fast Decision Rules

- Screenshot without details -> `cleanshot_capture`, `mode: "fullscreen"`, `action: "copy"`.
- Send/share screenshot -> capture, then send to the current chat if attachments are supported.
- Screenshot to file/evidence -> `action: "save"`.
- Screenshot for bug report/markup -> `action: "annotate"`.
- Floating reference -> `action: "pin"` or `cleanshot_pin_file` if a filepath is provided.
- Region without coordinates -> manual `mode: "area"`.
- Same region again -> `mode: "previous_area"`.
- Long page/chat/document -> `cleanshot_scrolling_capture`.
- Extract text/OCR -> `cleanshot_ocr`, `linebreaks: true`.
- Record screen -> `cleanshot_record_screen`.
- Open CleanShot/history -> `cleanshot_quick_access`.
- Open CleanShot settings -> `cleanshot_settings`.

## Multilingual Example User Phrases

The skill instructions are English-first. Non-English phrases below are examples of user wording only.

| User phrase | Tool guidance |
| --- | --- |
| "Сделай скрин всего экрана" | Use `cleanshot_capture` with `mode: "fullscreen"` and usually `action: "copy"`. |
| "Скопируй скрин окна в буфер" | Use `cleanshot_capture` with `mode: "window"` and `action: "copy"`. |
| "Дай выделить область и открой редактор" | Use `cleanshot_capture` with `mode: "area"` and `action: "annotate"`. |
| "Повтори прошлую область" | Use `cleanshot_capture` with `mode: "previous_area"`. |
| "Сними ту же зону и скопируй" | Use `cleanshot_capture` with `mode: "previous_area"` and `action: "copy"`. |
| "Закрепи это как референс" | Use `action: "pin"` for a new capture, or `cleanshot_pin_file` if a filepath is provided. |
| "Запиши экран" | Use `cleanshot_record_screen`. |
| "Сделай длинный скрин страницы" | Use `cleanshot_scrolling_capture`. |
| "Распознай текст с экрана" | Use `cleanshot_ocr` with `linebreaks: true`. |
| "Открой настройки CleanShot" | Use `cleanshot_settings`. |
| "Открой Quick Access CleanShot" | Use `cleanshot_quick_access`. |
