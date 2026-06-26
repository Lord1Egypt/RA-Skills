# Publish Flow

Use this reference for video publishing, publish-page behavior, cover handling, fieldized publish tasks, and stability tests.

## Guarded Publish

Publish must be blocked if login is invalid, SMS/security verification is active, or the page is not stable.

```bash
node scripts/publish-with-guard.js --notify --file /abs/video.mp4 --title "标题" --description "简介 #标签"
```

Full task publish:

```bash
node scripts/validate-publish-task.js --task /abs/publish-task.json
node scripts/publish-task.js --task /abs/publish-task.json --execute
```

Large videos can spend a long time in upload/transcode/assistant checks. Do not wrap real publishing
in short OpenClaw request timeouts. Use the async job path or pass long limits:

```bash
BROWSER_PROTOCOL_TIMEOUT=1200000 DOUYIN_UPLOAD_TIMEOUT_MS=1800000 DOUYIN_PUBLISH_TASK_TIMEOUT_MS=3600000 node scripts/publish-task.js --task /abs/publish-task.json --execute
```

Real publish pages can keep a single CDP evaluation busy for more than 5 minutes during upload, cover, assistant checks, or draft recovery. Migration/lab environments must set `BROWSER_PROTOCOL_TIMEOUT=1200000` or higher before starting the daemon; otherwise Puppeteer may throw `Runtime.callFunctionOn timed out` even though the page is still recoverable.

## Fieldized Publish Task

An upstream agent may send fields:

```text
tags:#宠物险#保险
"封面图片": "https://...png"
标题："养宠不焦虑的秘诀？"
"视频地址": "https://...mp4"
```

Convert/download before publishing:

```bash
node scripts/prepare-upstream-publish-task.js --input templates/upstream-mentor-example.json --output templates/publish-task.from-upstream.json
node scripts/validate-publish-task.js --task templates/publish-task.from-upstream.json
node scripts/publish-task.js --task templates/publish-task.from-upstream.json --execute
```

`templates/publish-task.from-upstream.json` 是上面第一条命令生成的临时任务文件，不随公开包预置。

For OpenClaw/other agents outside Feishu DM, prefer asynchronous MCP to avoid request timeout:

1. Call `douyin__douyin_publish_from_upstream_text` with the full fieldized text.
2. Poll `douyin__douyin_publish_job_status(jobId)` until `status=succeeded` or `status=failed`.
3. Do not call low-level `douyin__douyin_publish_video` for fieldized text unless you explicitly pass `coverImageUrl` or `coverImagePath`.

For the full task contract, read `references/publish-task.md`.

## Publish Page Rules

- Upload video via file chooser first. If no chooser appears within 5 seconds, use hidden `input[type=file]`.
- After filling title/description, read page values back. Do not continue if values did not stick.
- Title is capped at 30 characters. The converter, task JSON, page filling, verification, and customer notification must use the same 30-character safe title.
- `tags`/`metadata.topics` must be filled through the editor `#添加话题` control, not only as plain description text. Support one, two, or more tags; verify all expected topic nodes exist before publishing.
- If `cover.imagePath` exists, upload and save custom cover. AI recommended cover is fallback only when no cover is provided.
- After saving a custom cover, Douyin may show `是否确认应用此封面？`. Confirm this dialog immediately, then verify the cover slot changed before publishing.
- Custom cover failure blocks publish. Prompt: `封面设置失败，请重新发送可用的封面图片。`
- If an agent insists on using low-level MCP `douyin_publish_video`, it must pass `coverImagePath` or `coverImageUrl`; otherwise the publisher has no custom cover input and will fall back to AI recommended cover.
- Video URL/download/upload failure prompt: `视频处理失败，请重新发送可用的视频。`
- Do not expose URLs, stack traces, or HTTP details to the customer.
- Publishing can trigger a second SMS check even after login succeeded. Treat `publish_sms` as a resumable draft state: request the SMS code, submit the latest 6-digit code, then resume `publish-current-draft` and verify the title in works management. Do not discard the draft or rebuild the environment just because publish SMS appears.
- On the publish SMS modal, click only the right-side `获取验证码` / `发送验证码` / `接收短信验证码` button next to the verification-code input. Do not click the bottom red `发送短信验证` link; that switches to the `编辑短信 YZ / 发送至 ...` channel and blocks the normal 6-digit-code flow.

## Publish Button

- Close nonessential popups, guide overlays, exit prompts, and blockers before clicking publish.
- Publish button may be near bottom or sticky footer; scroll if needed.
- The publish button appears in the bottom `发布暂存离开` area. Prefer the real button, but if mouse click returns to upload with a draft prompt, resume the draft and use the script's DOM/React fallback.
- Do not click `我知道了`, back, refresh, exit, or unrelated top-page controls by mistake.
- Once upload/processing is complete and publish button is usable, publish directly. Do not wait without a page signal.
- 发文助手/快速检测 can stall. After upload is complete, a soft wait has elapsed, and the real publish button is visible, publish instead of waiting for 100%.

## Success Verification

Never treat editor state as publish success. Success requires at least one:

- success toast,
- publish API signal such as `create_v2`,
- navigation to management page,
- `node scripts/douyin-cli.js verify-published --title "标题"` finds target title in works list.

If management page returns to login/QR or API says `session_expired`, this is a login blocker, not success.
If a title is provided, management-page URL alone is not success; the works list must contain that title.

## Publish Stability

Dry-run:

```bash
node scripts/run-publish-task-stability.js --task templates/publish-task.stability.json --rounds 3
```

Real publish only when explicitly requested:

```bash
node scripts/run-publish-task-stability.js --task templates/publish-task.stability.json --rounds 3 --execute
```

Pass rule: all three rounds must complete publish submission and be found in Douyin works list by unique generated titles. Any failure resets the count. Publish SMS/security verification is not a failed round by itself; it fails only if the human code/security step times out or the resumed draft cannot be verified.
