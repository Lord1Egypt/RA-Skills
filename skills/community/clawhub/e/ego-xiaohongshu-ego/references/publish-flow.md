# Xiaohongshu Ego Lite video publish flow

Captured 2026-11-04 on creator account 听懂AI. Do not invent APIs. This skill drives the creator web UI with ego-browser.

Cover flow re-captured 2026-11-05: the old `选择图片上传` control is gone. The main cover is set through the cover editor dialog (编辑封面).

Two public notes from the 2026-11-04 capture, after the PK cover was applied:

- https://www.xiaohongshu.com/explore/6aeae169000000000e00c4ad
- https://www.xiaohongshu.com/explore/6aeae281000000000e00cb56

The caller passes absolute paths. This file does not name a product directory.

## Preconditions

- Ego Lite and `ego-browser` on PATH
- Logged into https://creator.xiaohongshu.com as the intended account
- https://www.xiaohongshu.com may show a different account than the creator site. Always read the creator header nickname
- One video per run. The caller owns the rate limit

## Publish URL

`https://creator.xiaohongshu.com/publish/publish?from=tab_switch&source=official`

Also reachable from creator home → 发布笔记 → 上传视频.

## File inputs

1. Video: `input.upload-input[type=file]` accept `.mp4,.mov,.flv,.f4v,.mkv,.rm,.rmvb,.m4v,.mpg,.mpeg,.ts`
2. Main cover: `.upload-btn input.upload-input` inside the cover editor dialog (accept `image/png, image/jpeg, image/*`). Do not use `input.pk-cover-list-file-input` for `--cover`.

Use `page.setInputFiles`. Do not open an OS file dialog.

## When the video is ready

Wait until the body no longer matches `/上传中\s*\d+%/` and shows 重新上传 or 设置封面.

The platform then uses the **video first frame** as the main cover until the 编辑封面 dialog replaces it. A PK-slot upload does not do that.

## Cover, required when `--cover` is set

Verified on 2026-11-05: the cover editor dialog sets the **main** cover. 2026-11-05 UI facts:

- 「设置封面」 is now a section title, not a control. 「编辑封面」 (`.cover-edit-entry`) is the entry; it sits in a hover-revealed overlay on the 主封面 card, so it has a zero-size box until the card (`.cover--column .default.column`) is hovered.
- The dialog has 裁剪 / 模版 / 上传 tabs; the image input exists immediately. After `setInputFiles`, the 完成 button stays disabled for a moment (cover processing) and enables after a few seconds.
- Clicking 完成 closes the dialog and the 主封面 card renders the uploaded image as its `background-image` (a `ros-preview.xhscdn.com/spectrum/...` URL). That background-image is the change signal.
- PK may auto-fill 3 recommended covers (「PK封面 3/3 已自动填充推荐封面」) with the switch remembered on. PK slots are a different control (`input.pk-cover-list-file-input`). Filling only those leaves the main cover and the note-manager thumbnail as the video first frame, badged 封面待PK, until the 72-hour PK ends. `--cover` does not upload a PK slot.

The script:

1. Hovers the 主封面 card (`.cover--column .default.column`) to reveal 编辑封面, clicks `.cover-edit-entry`. Retries up to 4 times (press Escape between attempts); the dialog is confirmed by `.upload-btn input.upload-input` appearing.
2. Calls `setInputFiles` on the dialog's image input (marked `data-xhs-editor-cover`). It refuses the PK input.
3. Waits until the dialog's 完成 button exists and is enabled, clicks it, and waits for the dialog to close.
4. Waits until the main-cover card signature (background-image + card `img` srcs) changes.
5. Retries the whole sequence once. If the preview does not change, exits `1` and does not click 发布.

Without `--cover`, do not invent an image. Leave the first frame and say so in the plan.

## Form fields

- Title: `page.fill` on the input whose placeholder is 「填写标题」. The page counter weighs ASCII as half a unit: `两台Mac跑816B大模型｜听懂AI #053` is 16/20. Do not use `element.value` plus a synthetic event.
- Body: click the ProseMirror editor (`.ProseMirror`) and `keyboard.insertText`. Description, a blank line, then topics (`#a #b`).
- 发布 is not always a `<button>`. Use the element whose text is exactly `发布` (a div on the 2026-11-04 page) and click its center. Do not use `button:text-is("发布")` alone.
- Account gate: the creator nickname must match `--expect-account` before upload and again before 发布. A header nickname wins over other text on the page.

## Publish

- Click the control whose text is exactly `发布` (not 暂存离开, not 发布笔记).
- Success: URL contains `/publish/success` and the page says 「发布成功」.
- Note id: open `https://creator.xiaohongshu.com/new/note-manager`, take the first `.note-card` whose text contains the title, parse `data-impression` JSON, read `noteTarget.value.noteId`.
- Public URL: `https://www.xiaohongshu.com/explore/<noteId>`

If 发布成功 was seen but the note id cannot be read, exit `1` and do not run `--yes` again for the same file.

## Edit cover (best-effort, not the main path)

Prefer the pre-publish swap above. `scripts/edit-cover.mjs` is only for a note that already went out.

Verified path for note `6aeae281000000000e00cb56`:

1. Note manager → 编辑
2. `https://creator.xiaohongshu.com/publish/update?id=<noteId>&noteType=video`
3. The same 编辑封面 dialog main-cover input (`.upload-btn input.upload-input`), not `input.pk-cover-list-file-input`
4. The main-cover preview must change before 发布
5. Footer button whose text is exactly `发布`

Caveats from the same session:

- Saving can send the note back to 审核中
- The manager can show the badge 封面PK中
- Another note disappeared from the manager, and its update URL showed 加载失败

If the update page says 加载失败, do not click 发布. Do not treat a failed edit as a reason to publish a new note.

## Hard rules

- `--yes` is required to upload or to click 发布. Without it: validate, check login, print the plan JSON (including the cover path), exit `3`
- Title, description, and topics cannot contain links (`http(s)://`, `www.`, bare domains such as `github.com/xxx` or `x.com/xxx`, `t.co`). The same check runs on a dry run. Without `--strip-links` the command exits `4` and lists the fragments. `--strip-links` removes the links, a dangling `项目地址：` or `链接：` on that line, and leftover blank lines, then prints what was removed.
- `finish({ keep: [] })` unless `--keep`
- Exit `2` when ego-browser is missing, the creator site is logged out, or `--expect-account` does not match
- No MCP. No batch loop. No scheduled publish. No delete. Image-text notes are a separate path: `references/imagetext-flow.md`
