# CleanShot Skill Examples

These examples are English-first and show how user phrases should map to the installed CleanShot Tool plugin.

## Example Mappings

| User phrase | Intended tool | Intended mode/action/params | Notes |
| --- | --- | --- | --- |
| "Take a screenshot." | `cleanshot_capture` | `mode: "fullscreen"`, `action: "copy"` | Default screenshot behavior favors fast paste/share workflows. |
| "Screenshot this and send it here." | `cleanshot_capture` | `mode: "fullscreen"`, `action: "copy"` | Send as an attachment only if the environment supports image attachments. |
| "Save a screenshot of the whole screen." | `cleanshot_capture` | `mode: "fullscreen"`, `action: "save"` | Use `save` when the user wants a file or persistent artifact. |
| "Copy a screenshot of the current window." | `cleanshot_capture` | `mode: "window"`, `action: "copy"` | Window screenshot for paste/share workflows. |
| "Take a screenshot of a selected area." | `cleanshot_capture` | `mode: "area"`, action by context | Let the user select manually when no coordinates are provided. |
| "Capture x 100 y 200 width 800 height 600." | `cleanshot_capture` | `mode: "area"`, `x: 100`, `y: 200`, `width: 800`, `height: 600` | Use exact coordinates only when provided. |
| "Repeat the previous area." | `cleanshot_capture` | `mode: "previous_area"`, action by context | Use for repeated captures of the same region. |
| "Take a bug-report screenshot and mark it up." | `cleanshot_capture` | mode by context, `action: "annotate"` | Annotation is best for arrows, blur, labels, redaction, and issue evidence. |
| "Pin this as a visual reference." | `cleanshot_capture` | mode by context, `action: "pin"` | Use `cleanshot_pin_file` instead if the user provides a filepath. |
| "Open CleanShot." | `cleanshot_quick_access` | no params | Interpret as CleanShot history / Quick Access. |
| "Show recent screenshots." | `cleanshot_quick_access` | no params | CleanShot Quick Access is the history entrypoint. |
| "Open CleanShot settings." | `cleanshot_settings` | no params | Use settings only when explicitly requested. |
| "Capture the full page." | `cleanshot_scrolling_capture` | usually no params | Open the scrolling capture UI unless autoscroll is explicitly requested. |
| "Take a scrolling screenshot with autoscroll." | `cleanshot_scrolling_capture` | `start: true`, `autoscroll: true` if supported | Use automatic start only when clearly requested. |
| "Extract text from the screen." | `cleanshot_ocr` | `linebreaks: true` | Do not promise OCR text will be returned directly to OpenClaw. |
| "Record the screen as a video." | `cleanshot_record_screen` | no params unless region/display is provided | Treat MP4/video as intended output if CleanShot offers that choice. |
| "Record this as a GIF." | `cleanshot_record_screen` | no params unless region/display is provided | Do not promise GIF output unless the tool/API supports selecting GIF directly. |
| "Annotate /tmp/example.png in CleanShot." | `cleanshot_annotate_file` | `filepath: "/tmp/example.png"` | Pass the filepath only; do not inspect or modify the file directly. |
| "Pin /tmp/example.png as a reference." | `cleanshot_pin_file` | `filepath: "/tmp/example.png"` | Pass the filepath only. |
| "CleanShot is not responding." | none first | troubleshooting guidance | Suggest enabling CleanShot API access and checking the CleanShot Tool plugin runtime. |

## Multilingual User Phrase Examples

The explanations remain English. Non-English phrases below are example user wording only.

| User phrase | Intended tool | Intended mode/action/params | Notes |
| --- | --- | --- | --- |
| "Сделай скрин" | `cleanshot_capture` | `mode: "fullscreen"`, `action: "copy"` | Default screenshot behavior. |
| "Заскринь и отправь сюда" | `cleanshot_capture` | `mode: "fullscreen"`, `action: "copy"` | Send only if attachments are supported. |
| "Скопируй скрин окна в буфер" | `cleanshot_capture` | `mode: "window"`, `action: "copy"` | Window screenshot copied for pasting. |
| "Дай выделить область и открой редактор" | `cleanshot_capture` | `mode: "area"`, `action: "annotate"` | Manual area selection with annotation. |
| "Повтори прошлую область" | `cleanshot_capture` | `mode: "previous_area"` | Reuse the previous CleanShot region. |
| "Сними ту же зону и скопируй" | `cleanshot_capture` | `mode: "previous_area"`, `action: "copy"` | Previous area copied to clipboard. |
| "Закрепи это как референс" | `cleanshot_capture` or `cleanshot_pin_file` | `action: "pin"` or `filepath` | Use file pinning if a filepath is provided. |
| "Сделай длинный скрин страницы" | `cleanshot_scrolling_capture` | no params unless autoscroll is requested | Scrolling capture workflow. |
| "Сними всю страницу с прокруткой" | `cleanshot_scrolling_capture` | no params unless autoscroll is requested | Scrolling capture workflow. |
| "Распознай текст с экрана" | `cleanshot_ocr` | `linebreaks: true` | OCR trigger only; text return is not guaranteed. |
| "Запиши экран" | `cleanshot_record_screen` | no params unless region/display is provided | Do not claim recording started unless confirmed. |
| "Открой настройки CleanShot" | `cleanshot_settings` | no params | Settings workflow. |
| "Открой Quick Access CleanShot" | `cleanshot_quick_access` | no params | CleanShot history / Quick Access. |

## Display And Multi-Monitor Examples

1. User:
   "Capture the left half of the main display."

   Action:
   - Call `cleanshot_get_displays`.
   - Select main display / display 1.
   - Calculate left half.
   - Call `cleanshot_capture` with mode `area`, action by context, and calculated coordinates.

2. User:
   "Заскринь левую часть экрана."

   Action:
   - Treat as an example user phrase.
   - Call `cleanshot_get_displays`.
   - Use main display by default.
   - Calculate left half if geometry is reliable.
   - Otherwise use manual `area`.

3. User:
   "Capture the right half of the second monitor."

   Action:
   - Call `cleanshot_get_displays`.
   - Select display 2.
   - Calculate right half.
   - Call `cleanshot_capture`.

4. User:
   "Record the second monitor."

   Action:
   - Call `cleanshot_get_displays`.
   - Select display 2.
   - Call `cleanshot_record_screen` with display or calculated bounds.

5. User:
   "Take a scrolling screenshot on the external monitor."

   Action:
   - Call `cleanshot_get_displays`.
   - Select external monitor if unambiguous.
   - Start `cleanshot_scrolling_capture`.
   - If region is unclear, let the user choose in CleanShot UI.

6. User:
   "Screenshot the top third of the right monitor."

   Action:
   - Call `cleanshot_get_displays`.
   - Select right monitor if geometry is clear.
   - Calculate top third.
   - Call `cleanshot_capture`.
