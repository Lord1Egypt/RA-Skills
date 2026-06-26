# Data, Comments, And DMs

Use this reference for analytics, Feishu Bitable sync/report, comment reply, and DM reply.

## Data Sync And Report

Commands:

```bash
node scripts/douyin-data-analysis.js --days 90 --output $HOME/.openclaw/workspace/douyin-ops/reports/data-analysis-latest.json
node scripts/sync-douyin-data-to-feishu-bitable.js --days 90 --notify
node scripts/douyin-data-report-from-bitable.js --days 90 --notify
node scripts/douyin-next-video-plan-from-bitable.js --days 90 --notify
```

MCP tools:

- `douyin__douyin_data_analysis`
- `douyin__douyin_sync_data_to_feishu_bitable`
- `douyin__douyin_data_report_from_feishu_bitable`
- `douyin__douyin_next_video_plan_from_feishu_bitable`

Rules:

- `更新数据` opens Douyin web, collects recent source data, and syncs to Feishu Bitable.
- `数据报告`/`数据分析`/`分析数据`/`查看数据` first syncs recent Douyin data to Feishu Bitable, then reports from Bitable.
- `生成下一条视频`/`下一条视频`/`内容方案` uses `douyin_feishu_route_text`, starts an async job, syncs recent Douyin data to Feishu Bitable, then sends exactly one complete next-video plan to Feishu from the worker.
- Reports include a deterministic numeric summary plus an enhanced analysis. Enhanced analysis defaults to the current OpenClaw model config, e.g. MiniMax-M2.7; do not use Codex/GPT output as proof when validating OpenClaw/MiniMax.
- Next-video plans include `标题`、`封面文案`、`tags`、`选题`、`口播脚本`、`画面建议` and `digitalHumanInput` for the digital-human video API layer. If the model call fails, the script must return a deterministic fallback plan instead of failing the whole workflow.
- If Bitable cumulative works and the latest sync count differ, the report must state both scopes instead of blending them.
- `douyin_data_analysis` is a compatibility entry and now also performs sync-to-Bitable first, then reports from Bitable.
- If Bitable has no data, ask customer to run `更新数据`.
- Sync with `--notify` must send update result and Bitable link to customer.
- Report wording must not claim the account overview covers 90 days. Say: `已同步近 N 天作品明细；账号概况为抖音后台当前展示周期。`
- Pass rule is 3 consecutive `ok=true`.

Collected work details include ID, title/description, publish time, review status, visibility, duration, cover URL, views, completion, 5s completion, 2s bounce, average watch time, likes, shares, comments, favorites, homepage visits, fan change, danmaku, downloads, dislikes, fan-view proportion, and interaction rates.

## Next Video Plan

Feishu triggers:

- `生成下一条视频`
- `下一条视频`
- `内容方案`
- `生成视频方案`
- `具体文案`
- `生成文案`
- `口播文案`

Output contract:

```json
{
  "plan": {
    "topic": "选题方向",
    "title": "发布标题",
    "coverText": "封面文案",
    "tags": ["#标签1", "#标签2"],
    "hook": "前2秒钩子",
    "script": ["口播句1", "口播句2"],
    "shotList": [{ "time": "0-3s", "visual": "画面建议", "narration": "对应口播" }],
    "publishFields": {
      "title": "发布标题",
      "description": "简介",
      "tags": ["#标签1", "#标签2"]
    },
    "digitalHumanInput": {
      "modelId": "数字人模型ID，可为空",
      "title": "发布标题",
      "scriptText": "完整口播文本",
      "coverText": "封面文案",
      "tags": ["#标签1", "#标签2"],
      "suggestedDurationSeconds": 25
    }
  }
}
```

Rules:

- Use OpenClaw/MiniMax or the configured compatible model first; fall back to deterministic rules if the model fails or returns invalid JSON.
- Do not answer from the previous data report free-form. These triggers must route through `douyin_feishu_route_text`; the route starts a background job and the worker sends the final Feishu message.
- Never call `douyin_next_video_plan_from_feishu_bitable` as a fallback inside Feishu DM/group flows, including after a route wait or timeout. That low-level tool is only for non-Feishu debugging and the worker.
- Do not manually format or duplicate a plan in the agent reply, do not expose thinking/tool timeout text, and do not ask “需要帮你生成封面图吗？” after the worker sends the plan.
- The final worker message must include concrete title, cover text, tags, script, shot list, and `digitalHumanInput`.
- Keep the Feishu message concise enough to read directly. The full JSON is available from the MCP/tool result or `--output`.
- The next layer should pass `digitalHumanInput` to the digital-human video API, then send the returned `视频地址/封面图片/标题/tags` back to this skill for automatic publishing.
- Daily scheduled report should include both the data report and this next-video plan.

Bitable tables:

- `抖音作品明细`: upsert by `作品ID`
- `抖音账号日报`: upsert by `日期`
- `抖音数据同步日志`: append each sync

If Feishu Bitable permission is missing, send authorization link and retry after customer authorizes.

## Comment Reply

Commands:

```bash
node scripts/douyin-comment-reply.js list --unreplied --author-reply-check --pages 8
node scripts/douyin-comment-reply.js list --all-works --unreplied --author-reply-check --pages 3 --max-works 20
node scripts/douyin-comment-reply.js reply --text "感谢支持" --index 0 --unreplied
node scripts/douyin-comment-reply.js reply --text "hhh" --index 0 --unreplied --execute
```

Default reply mode is dry-run: locate reply input, fill text, confirm send button, then clear draft.

Rules:

- Reply must be a comment reply, not a new top-level comment.
- Comment list output may include local audit metadata, but default reply decisions must not filter by `$HOME/.openclaw/workspace/douyin-ops/auto-reply-state.json`. If Douyin's `未回复` filter still shows a comment, treat it as pending unless the page itself shows this account already replied.
- `--all-works` scans works with visible comment count > 0. It is read-only for `list`; `reply` must reselect the target work before opening the target comment.
- Comment scanning should scroll/load multiple pages and expand visible reply threads. Page-confirmed already replied comments and own comments are skipped; local-state-only matches are not skipped unless `--trust-local-state` is explicitly enabled. Skipped rows must not stop scanning later pending comments.
- Skip own/author comments.
- Click target comment card's `回复`, then use the opened reply box.
- Do not use page top/global `发送` input.
- Real send must verify the reply text appears in the page after sending; a click without verification is not success.
- Real send requires explicit customer authorization, target comment, and exact text.
- Pass rule: list 3/3 success; dry-run reply 3/3 can locate input/send button and clear draft; real reply 3/3 must return `comment_reply_sent_verified`.
- 2026-05-15 real test: comment reply sent and verified 3/3.
- 2026-05-21 fix: latest-video duplicate issue fixed by local-state filtering; `--all-works` read-only scan found 19 pending comments on the 2026-03-19 work while latest work was filtered to 0 pending.

## DM Reply

Commands:

```bash
node scripts/douyin-dm-reply.js list
node scripts/douyin-dm-reply.js reply --text "您好，请问需要了解哪方面？"
node scripts/douyin-dm-reply.js reply --text "收到，我稍后回复你。" --index 0 --execute
```

Rules:

- Default is dry-run, not real send.
- The script must open the selected conversation, locate the reply input/send button, then send.
- Before filling or sending, the script must inspect the opened conversation's latest visible message. If the latest message is the account's own outgoing bubble, return `dm_latest_is_own_reply` and do not fill/send.
- If page says no permission, not opened, unavailable, or no input/send button is visible, return blocker honestly and save a screenshot.
- Real send must verify the reply text appears in the conversation after sending; a click without verification is not success.
- Real send requires explicit customer authorization, target conversation, and exact text.
- Pass rule: 3/3 can enter DM/conversation page and list; dry-run 3/3 can locate input/send button and clear draft; real reply 3/3 must return `dm_reply_sent_visible`.
- 2026-05-15 real test: DM reply sent and verified 3/3.

## Auto Reply By Content

Commands:

```bash
node scripts/douyin-auto-reply.js comment
node scripts/douyin-auto-reply.js dm
node scripts/douyin-auto-reply.js both --limit 50 --max-scan 200
node scripts/douyin-auto-reply.js both --limit 50 --max-scan 200 --execute
```

MCP tool:

- `douyin__douyin_auto_reply`

Feishu triggers:

- `自动回复`: process visible pending comments across works with comments plus DM conversations, then report counts. Scheduled auto-reply may be disabled independently.
- `自动回复评论`: process creator-center visible comments across works with comments. Prefer Douyin's per-work `未回复` dropdown when available: reply the first visible pending comment, wait 60 seconds, toggle `全部评论 -> 未回复`, and keep looping in the same work until the `未回复` list is empty before moving to the next work. Skip own comments and comments that already show an author reply/reply thread. Do not skip just because local state says it was replied; local state is audit-only unless `--trust-local-state` or `DOUYIN_COMMENT_TRUST_LOCAL_STATE=true` is explicitly enabled.
- `自动回复私信`: process visible DM conversations from top to bottom. If the latest message in a conversation is from this account, skip it to avoid loops. By default do not require a page unread marker unless `DOUYIN_DM_REQUIRE_UNREAD=true`.

Rules:

- Default is dry-run. Use `--execute` only when real auto reply is authorized.
- Reply text must be generated by the AI prompt when OpenClaw/MiniMax or a compatible API is configured. The AI prompt must generate one short Chinese reply that reflects the fan's actual text, encourages interaction, avoids hard promises, and never outputs links/contact info. If the model call fails or the output is unsafe, skip that target by default; deterministic rule fallback is only allowed with `--allow-rules-fallback` or `DOUYIN_AUTO_REPLY_ALLOW_RULES_FALLBACK=true`.
- Configure AI reply with `DOUYIN_AUTO_REPLY_LLM=auto|on|off`, `DOUYIN_AUTO_REPLY_API_KEY`, `DOUYIN_AUTO_REPLY_BASE_URL`, and `DOUYIN_AUTO_REPLY_MODEL`. By default the script reads OpenClaw's current model config first, then falls back to env vars.
- Feishu completion message must be concise: `自动回复完成：评论 X 条，私信 Y 条。`
- The script records replied targets in `DOUYIN_AUTO_REPLY_STATE` or `$HOME/.openclaw/workspace/douyin-ops/auto-reply-state.json` for audit/debugging. For `reply-unreplied-by-filter`, do not use this local state for default dedup; the 60-second wait plus Douyin's `未回复` filter is the source of truth.
- Default manual and scheduled runs should use `--limit 50 --max-scan 200`. Own comments are skipped and scanning continues. Page-confirmed author replies are skipped, not treated as a hard stop. Local-state dedup is opt-in only.
- Comment local-state keys include work identity when available, but they are audit records by default. Never let a previous local record for another work suppress a visible `未回复` comment.
- For DMs, dedup preserves the visible timestamp/summary so a repeated new `你好` later is not incorrectly skipped.
- For DMs, unread detection should come from page state (`unread`, `未读`, `陌生人消息`, or visible badge/dot), not just text content. If the conversation summary is the bot's own latest reply, skip it to avoid an auto-reply loop.
- DM list detection must not treat tabs/headers such as `全部 朋友私信 陌生人私信 群消息` as conversations. Real conversation rows should include a name plus latest time/summary.
- Browser tasks must be serialized. Comment and DM scripts use `scripts/browser-task-lock.js`; new browser scripts must use it too. Publishing has the highest priority: any comment/DM auto-reply process must defer when a `publish:*` lock or publish-priority request exists, and resume via the next manual/scheduled auto-reply run after publishing finishes.
- Use `--force` only for testing; it may reply to the same visible target again.
- Real success requires the underlying sender to verify visible text: comments require scoped `comment_reply_sent_verified` under the target comment card; DMs require `dm_reply_sent_visible`.
- 2026-05-21 real test: expanded `查看2条回复`, correctly skipped a comment already containing author replies, replied to remaining `Duduer: 这个怎么购买` as a scoped comment reply, then re-ran `both --execute` with 0 duplicate sends.
