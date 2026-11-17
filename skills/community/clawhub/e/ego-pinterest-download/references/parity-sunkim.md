# Parity vs `@sunkimkk/pinterest-mcp`

Checked against the public tool list: search, get pin, related pins, board feed, previews, image and MP4 download.

| Capability | sunkim MCP | this skill | done |
|------------|------------|------------|------|
| Keyword search (`query`) | `pinterest_search` | `search --query` via `BaseSearchResource` and page cookies | yes |
| Count / limit (1–100) | yes, default 20 | `--count`, default 10 | yes |
| Bookmark pages | yes | `--bookmark`, up to 4 pages | yes |
| Prefer originals, fall back to 736x | `size: originals` | `--size originals` | yes |
| Width / height when the JSON has them | yes | `pins[].width/height` | yes |
| Related pins | `pinterest_related_pins` | `related --pin` (`RelatedModulesResource`) | yes |
| Board feed | `pinterest_board_pins` | `board --board` (`BoardResource` + `BoardFeedResource`) | yes |
| One pin | `pinterest_get_pin` | `pin --pin` (`PinResource`), including `pin.it` | yes |
| Model-facing thumbnails | `pinterest_preview_images` / `previews` | `preview --url` or `--previews N` (base64, max 8, max 120KB) | yes |
| Save images to a directory | `pinterest_download` | `--out` + `manifest.json` | yes |
| Video MP4 | `pinterest_download` video URLs | `download --url …mp4`, `--media video`. mc HLS → `mc/720p/*.mp4`. iht HLS/cmfv → `iht/expMp4/<id>_720w.mp4` (then 540/360/240), then cmfv 720/540/360. Node `fetch failed` retries HTTP/1.1 and the logged-in page. Cap 200MB | yes |
| Min width / height | no | `--min-width` / `--min-height` before save. Both set means both sides. Direct `--url` is not filtered | extra |
| Skip promoted pins | yes | yes | yes |
| `e1_…` anonymous ids | cannot open | rejected with a login hint | yes |
| Session | anonymous cookie jar | Ego Lite. Logged out → exit 2 unless `--allow-anonymous` | different on purpose |
| Headless, no browser | yes | requires `ego-browser` | different on purpose |

`resource_response.message` is a locale status string (for example `确定`). It is not an error. Failures are HTTP status, `http_status >= 400`, or `status === "failure"`.
