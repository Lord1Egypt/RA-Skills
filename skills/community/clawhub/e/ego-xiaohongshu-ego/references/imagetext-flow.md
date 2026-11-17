# Xiaohongshu Ego Lite image-text publish flow

Captured 2026-11-05 on creator account 听懂AI with a read-only probe (tab click only, nothing uploaded). This skill drives the creator web UI with ego-browser. Do not invent APIs.

The video flow is in `publish-flow.md`. Only the differences are documented here.

## Tab switch

`https://creator.xiaohongshu.com/publish/publish?from=tab_switch&source=official` opens on the 上传视频 tab. Clicking the leaf element whose text is exactly 上传图文 switches modes and the URL gains `&target=image`.

The tab area renders each label more than once (hover variants); the verified target is the last leaf element with that exact text. A container with children is not a reliable click target.

## Image upload input

After the switch there is exactly one `input[type=file]`:

- class `upload-input` — **the same class as the video input**
- accept `.jpg,.jpeg,.png,.webp` (no gif)
- attribute `multiple`

The accept attribute is the only safe discriminator. An `input.upload-input` whose accept lists video extensions is the video input and must never receive images.

Page hints from the same capture: max 32MB per image, png/jpg/jpeg/webp, no gif or live photos, recommended aspect 3:4 to 2:1, resolution at least 720*960, over 1280P uploads sharper through the web page. The editor supports up to 18 images per note.

## Verified steps

1. `creatorAct({ op: "image-tab" })` clicks the last 上传图文 leaf.
2. Poll `creatorAct({ op: "image-input" })` until the image-accept input appears (the tab click renders the pane asynchronously).
3. One `page.setInputFiles(selector, [allPaths])` with the whole array. Do not click the visible 上传图片 button — that path opens the upload UI instead of the file input.
4. Poll `creatorAct({ op: "image-state" })`: ready when no 上传中 N% and no 上传失败/格式不支持/图片过大, and the upload thumbnails (`img` with `blob:` or `sns-img` src) or the N/18 counter reach the expected count.
5. Title input placeholder is 「填写标题会有更多赞哦」 — the video flow's /填写标题/ match still hits it. Body is the same ProseMirror editor.
6. Then the shared flow: account gate, publish, `/publish/success` + 发布成功, note id from note manager.

## The 发布 button is inside a closed shadow root

Verified 2026-11-05 by publishing note `6aeb6a4d000000000e00dbcc`:

- The image editor footer (暂存离开 | 发布) does **not** appear in `document.body.innerText` and cannot be reached by `querySelectorAll` — no open shadow root, no reachable iframe. It renders in a **closed shadow root**.
- The accessibility snapshot still names it: a `button [ref=N]` whose exact text child is `发布`. `session.clickPublishImage()` parses that snapshot (`publishButtonRef`) and clicks `page.click("ref=N")`, falling back to `loc=role:button[name='发布']`.
- Do **not** reuse the video flow's exact-text 发布 match or any `.btn-wrapper` selector here. On the image editor, `div.publish-video > div.btn-wrapper` is the **sidebar 发布笔记 menu button** (top-left, around x=24,y=80). Clicking it opens the publish-mode popover (上传视频/上传图文/写长文/发播客), navigates to `?from=menu`, and silently saves the draft — the run before the fix lost three uploads that way (they landed in 草稿箱).
- A DOM op for the image footer button is impossible; only the snapshot ref (or ego's role selector) reaches it.

## Cover

There is no cover step. The first image is the note cover. `--cover` fails validation for `--images` notes. The 编辑封面 dialog and the PK slots belong to the video flow only.
