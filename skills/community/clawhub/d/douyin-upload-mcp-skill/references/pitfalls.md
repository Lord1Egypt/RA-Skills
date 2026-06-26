# Pitfalls And Generalization Rules

Read this when a workflow behaves strangely, a test fails, or a new agent is taking over.

## Customer Communication

- Send Feishu messages only when customer action is needed.
- Do not repeat `建议/无需操作` messages.
- Do not send internal errors, script stacks, page debug text, or publish-page diagnostics to the customer.
- Customer must trigger flow with `发布抖音`, or upstream task must include `视频地址/标题`.

## Login

- Never send QR before customer replies `发送二维码`.
- Refresh/regenerate QR before capture and run quality detection.
- Do not send QR with gray overlay, refresh icon, expired state, abnormal size, or cropped edges.
- Do not continuously poll customer after QR. Ask them to reply `已登录` after scan and confirmation.
- For SMS, click send/resend first. Fill only the latest 6-digit code and click confirm.
- Wait 1-2 seconds before declaring logged in; require creator-backend signals.

## Browser And Environment

- Browser tasks are serial. Shared daemon/page means parallel tests can produce fake navigation/focus failures.
- Reuse existing daemon/CDP and cookies. Do not start competing browsers.
- If `X Server` or `DISPLAY` fails, use headless daemon or existing daemon; do not loop retries.
- For Feishu cold start, `douyin-skill-supervisor.service` must export GUI variables: `DISPLAY`, `WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, and `DBUS_SESSION_BUS_ADDRESS`. Without them, systemd can start watcher but Edge fails with `Missing X server`.
- `Missing X server`, `acquire_failed`, `Not connected`, `Target closed`, and `Session closed` are internal browser recoverable failures. Restart daemon and retry login check; do not tell the customer to do manual verification.
- If OpenClaw reports `douyin__... failed: Not connected`, the MCP bridge is disconnected even if the Douyin browser daemon is healthy. Run `node scripts/openclaw-douyin-health.js --fix --restart-gateway`, then ask the customer to resend the previous trigger. Do not send `NO_REPLY`, `contact admin`, or menu-bar restart instructions to the customer.
- If `douyin_feishu_route_text` returns `customerAlreadyNotifiedByTool:true`, the tool has already handled customer messaging. Do not send a visible Feishu reply and never output `NO_REPLY`; use `HEARTBEAT_OK` only when the runtime requires a placeholder response.
- In sandboxes, redirect state/output paths to writable current workdir.

## Publish

- Close popups/overlays/exit prompts before clicking page controls.
- Avoid refresh/back/exit/top-page buttons unless explicitly intended.
- Confirm upload input, title, description, and cover by reading page state.
- If custom cover exists, it must be uploaded/saved/verified. Failure blocks publish.
- Custom cover save is not complete until any `是否确认应用此封面？` dialog is confirmed and the dialog disappears.
- Stability tests must include `coverImagePath`; otherwise they do not prove field `封面图片` works.
- If the upload page shows `你还有上次未发布的视频，是否继续编辑？`, fresh upload must either click `放弃` and verify the prompt disappeared, or resume the draft intentionally. Do not upload through a stale draft prompt.
- If upload returns `上传失败，重新上传`, clean the failed draft and retry upload once before failing.
- The publish assistant progress can stall at a non-100 value. After video upload is complete, if the real publish button is visible after the soft timeout, publish instead of waiting indefinitely.
- In migration tests, set `BROWSER_PROTOCOL_TIMEOUT=1200000` before daemon startup. The default 300000ms can produce false `Runtime.callFunctionOn timed out` failures on real publish pages.
- Migration-only acceptance may skip Xiaoice generation by passing `--reuse-video-url` and optional `--reuse-cover-url`. In that mode the pass criterion covers clean deployment, OpenClaw/Feishu route, Douyin login, real publish, and delete; it does not claim Xiaoice video generation was revalidated in that run.
- Do not run OpenClaw agent route checks inside the same live Feishu login/SMS conversation. They can start a second Feishu consumer and reply to `已登录` or 6-digit codes as normal user text. For migration publish acceptance, isolate Feishu by stopping `openclaw-gateway.service`; run OpenClaw route checks separately with dry-run text and no customer conversation.
- The bottom publish control lives in a `发布暂存离开` area. A mouse click can return to the upload page while preserving the draft; in that case resume the draft and use DOM/React fallback instead of repeating the same mouse click.
- `publish-state` must not treat `/content/manage` or `加载中，请稍候` as success. With a title, success means the title is found in the works list.
- Do not use synchronous low-level MCP for long fieldized publishing. It may timeout while the page later publishes successfully, causing false failure reports.
- Fieldized publish text must use the async job entry or task scripts so `封面图片` becomes `coverImagePath`. Raw `filePath/title/description` loses the custom cover and falls back to AI cover.
- Publish can require SMS verification after all fields, cover, tags, and upload are ready. This is a resumable draft state, not an immediate publish failure. Request the code, submit the latest 6-digit code, then resume/verify the current draft.
- In publish SMS verification, the bottom red `发送短信验证` link is not the normal code-send button. It switches to an instruction page asking the user to send `YZ` to a phone number. The script must ignore that link and click the input-row `获取验证码` / `发送验证码` / `接收短信验证码` control instead.
- Locate publish button in bottom/sticky area; use script fallback when normal click fails.
- Publish success requires toast/API/management-page/title verification, not just a clickable button.

## Data And Interactions

- `数据报告` reads Feishu Bitable; `更新数据` performs web sync.
- Comment reply must use target card's reply box, not global comment input.
- `查看N条回复` only means the comment has replies; those replies may be from other users. Do not skip solely because a reply thread exists. Expand the thread and skip only when a reply row contains `作者`/the account's author marker.
- If Douyin no longer exposes an `未回复` filter, fall back to expanding visible reply threads and detecting author replies. Never reply from an unfiltered list without this author-reply check.
- Scheduled comment auto-reply is incremental: latest video, newest-first comments, scroll/load a few pages, expand reply threads, reply unreplied comments, and stop at the first already-author-replied/local-replied boundary. Do not sort by hot/likes for the default scheduled job.
- AI-generated replies must be short and grounded in the actual fan text. Reject links, contact info, hard insurance promises, and generic model-sounding output; fall back to deterministic rules if the model call fails or produces unsafe text.
- DM auto-reply has two guards: the list must only include real conversation rows, and the sender must inspect the opened chat before filling. If the latest visible message is our outgoing bubble, skip with `dm_latest_is_own_reply`.
- DM/comment real send requires explicit authorization and target.

## Model Boundary

- MiniMax/OpenClaw is good for stable MCP/script execution.
- Codex-like agents are better for page changes, environment faults, script repair, and cross-system debugging.
- Any fix must be tested. Critical loops require 3 consecutive successes; one failure resets the count.
