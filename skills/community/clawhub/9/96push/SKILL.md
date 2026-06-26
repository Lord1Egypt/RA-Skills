---
name: 96push
description: "User-approved 96Push desktop client publishing helper — query platforms/accounts, create content, inspect platform rules, and publish only after explicit confirmation. Use when user mentions 96push, publishing, social media, multi-platform, or content distribution."
homepage: https://push.96.cn
metadata:
  openclaw:
    homepage: https://push.96.cn
    requires:
      env:
        - PUSH_API_KEY
    primaryEnv: PUSH_API_KEY
---

# 96Push Remote Control

Use the bundled script to control the user's local 96Push desktop client via the 96.cn HTTPS proxy. This skill can affect logged-in social media accounts; treat publish, delete, queue cancel, and platform setting changes as high-impact actions.

## Safety First

- Do not run `update`, `publish`, `delete-article`, `cancel-queue`, `create-plat-set`, `update-plat-set`, or `delete-plat-set` until the user explicitly approves that exact action.
- Before asking for approval, show the content ID/title, content type, target account IDs/platforms, draft/live publish state, visibility, and platform settings.
- Prefer draft mode or a single account first. Publishing to multiple accounts requires a second explicit confirmation for the full account list.
- Never ask the user to paste `PUSH_API_KEY` into chat by default. Prefer that the user stores it locally in an environment variable or `~/.openclaw/.env`.
- Never echo API keys, draft private content, or unpublished media URLs in responses.
- Only use this skill when the user intends to operate 96Push and trusts the 96Push service at [https://push.96.cn](https://push.96.cn).

## Requirements

- The user should provide the API key locally via either:
  - environment variable: `PUSH_API_KEY`, or
  - `~/.openclaw/.env` line: `PUSH_API_KEY=pk_...`
- If the key is missing, the script will return setup instructions. Guide the user:
  1. Download 96Push from [https://push.96.cn](https://push.96.cn)
  2. Launch and login
  3. Go to profile (bottom-left avatar) → API Key → Generate
  4. Add it locally to `~/.openclaw/.env` or `PUSH_API_KEY`; do not paste it into chat unless they explicitly want the agent to write that local file.

## Commands

All commands via `python3 {baseDir}/scripts/96push.py <command> [options]`.

### Query

```bash
# health check
python3 {baseDir}/scripts/96push.py check

# platforms
python3 {baseDir}/scripts/96push.py platforms
python3 {baseDir}/scripts/96push.py platforms --article
python3 {baseDir}/scripts/96push.py platforms --video

# accounts
python3 {baseDir}/scripts/96push.py accounts
python3 {baseDir}/scripts/96push.py all-accounts

# content
python3 {baseDir}/scripts/96push.py articles --page 1 --size 10 --status 1
python3 {baseDir}/scripts/96push.py article --id 42

# publish records
python3 {baseDir}/scripts/96push.py records --page 1 --size 10
python3 {baseDir}/scripts/96push.py record --id 7

# dashboard
python3 {baseDir}/scripts/96push.py dashboard
python3 {baseDir}/scripts/96push.py overview
python3 {baseDir}/scripts/96push.py user

# platform configs
python3 {baseDir}/scripts/96push.py plat-sets --pid 3

# platform publishing rules (offline, no API key required)
python3 {baseDir}/scripts/96push.py rules --list
python3 {baseDir}/scripts/96push.py rules --platform wechat --type article
python3 {baseDir}/scripts/96push.py rules --platform wechat,zhihu --type article
```

### Upload Local Images

OpenClaw runs on a server and cannot read arbitrary user-local paths like `/Users/...` or `C:\...`. Images must become URLs before they are used in `thumb`, `files`, or article body markup.

- If the user attached/generated an image that exists in the OpenClaw runtime, upload it first and use the returned 96Push pix URL.
- If the image only exists on the user's computer, ask the user to upload it through 96Push or another image host and provide the returned URL. Do not invent or use the local path.
- `upload` returns a 96Push local pix URL (`http://127.0.0.1:.../pix/...`). It is already backed by the user's local 96Push client.

Uploading sends a file available to the skill runtime to 96Push, so it requires explicit user approval immediately before running.

```bash
python3 {baseDir}/scripts/96push.py upload --file "/workspace/uploads/cover.png" --confirm
```

### Create Content

```bash
# content type can be omitted when --files clearly indicates image/video
# video files (.mp4/.mov/.avi/.mkv/.webm/.m4v/.flv/.wmv) are inferred as --type video

# article — needs title + markdown (or content as HTML)
python3 {baseDir}/scripts/96push.py create --type article --title "标题" --markdown "# 内容" --desc "摘要"

# article with explicit cover image(s)
python3 {baseDir}/scripts/96push.py create --type article --title "标题" --markdown "# 内容" --thumb '["https://example.com/cover.jpg"]'

# graph_text — needs title + files (image URLs, at least 1)
python3 {baseDir}/scripts/96push.py create --type graph_text --title "图集" --files '["url1","url2"]'

# video — needs title + files (1 video URL), desc strongly recommended
python3 {baseDir}/scripts/96push.py create --type video --title "视频" --files '["video_url"]' --desc "视频描述"
python3 {baseDir}/scripts/96push.py create --title "视频" --files '["https://example.com/video.mp4"]' --desc "视频描述"
```

### Update / Delete Content

Updates change managed content in 96Push, and deletion is destructive. Both require explicit user approval immediately before running.

```bash
python3 {baseDir}/scripts/96push.py update --id 42 --title "新标题" --markdown "# 新内容" --confirm
python3 {baseDir}/scripts/96push.py delete-article --id 42 --confirm
```

### Publish

Publish is high-impact. First present the exact content, account list, draft/live state, and settings to the user. Run only after explicit approval.

```bash
# single-account live publish after explicit approval
python3 {baseDir}/scripts/96push.py publish --type article --id 42 --accounts "1" --confirm
python3 {baseDir}/scripts/96push.py publish --type video --id 42 --accounts "5" --confirm

# if --type is omitted, the script reads content detail and infers article/graph_text/video
# publish prints a rules-file hint for each recognized target platform
# use --show-rules only when you need the full rule text in the command output

# advanced mode — full settings per account (see platform settings reference)
python3 {baseDir}/scripts/96push.py publish --type article --id 42 --accounts-json '[{"id":1,"platName":"微信公众号","settings":{"publishType":"publish","origin":false}}]' --confirm --show-rules

# multi-account draft after explicit approval of the full target list
python3 {baseDir}/scripts/96push.py publish --type article --id 42 --accounts "1,5" --draft --confirm --confirm-multi-account

# poll result
python3 {baseDir}/scripts/96push.py poll --id 7
python3 {baseDir}/scripts/96push.py poll --id 7 --interval 10 --max 30
```

### Manage Platform Configs

Platform config changes affect future publishing behavior and require explicit user approval.

```bash
# create a reusable config
python3 {baseDir}/scripts/96push.py create-plat-set --pid 1 --name "公众号默认" --setting '{"publishType":"publish","leave":true}' --confirm

# update config
python3 {baseDir}/scripts/96push.py update-plat-set --sid 1 --pid 1 --name "公众号原创" --setting '{"publishType":"publish","origin":true}' --confirm

# delete config
python3 {baseDir}/scripts/96push.py delete-plat-set --sid 1 --confirm
```

## Typical Workflow

1. `check` — confirm client is online
2. `accounts` — list available accounts, let user pick targets
3. `rules` — read every target platform's rule file for the target content type before creating settings or choosing cover images
4. `create` — create content (see content creation rules below)
5. Ask the user to approve the exact content, target accounts, draft/live state, and settings.
6. `publish --confirm` — submit and wait for results (**call ONCE only**, see critical rules below). Use `--confirm-multi-account` only after the user approves every target account. The command automatically polls until completion — no need to call `poll` separately.
7. Report results to the user

---

## CRITICAL: Publish Anti-Spam Rules (MUST FOLLOW)

**⚠️ NEVER call `publish` more than ONCE per content per batch of accounts.**

The publish command triggers browser automation that takes 30-60 seconds to complete. The script has a built-in guard that rejects publish if another task is already running. Follow these rules strictly:

1. **ONE publish call per batch.** The `publish` command now automatically waits for completion — it submits the task and polls until done. Do NOT call `poll` separately unless you used `--no-wait`.
2. **Publish requires explicit approval.** Use `--confirm` only after the user approves the exact content, target accounts, draft/live state, and settings.
3. **Multi-account publish requires extra approval.** Use `--confirm-multi-account` only after the user approves every target account in the batch.
4. **If publish times out**, it does NOT mean publish failed — the browser automation may still be running. Do NOT retry publish. Instead, ask the user to check the 96Push client.
5. **If publish returns `PUBLISH_ALREADY_RUNNING`**, do NOT retry. Wait for the active task to complete.
6. **If publish returns HTTP 425**, another task is in progress. Wait and report to user, do NOT retry.
7. **NEVER loop or retry the publish command.** Each call creates a new browser automation task. Calling it 10 times creates 10 browser windows fighting for the same page.
8. **The complete sequence is always**: user approval → `publish --confirm` (once, waits automatically) → report result to user.

---

## Content Creation Rules (IMPORTANT)

The CLI now validates and minimizes create/update payloads:

- Article payloads do not send `files`; graph_text/video payloads do not send `markdown` or `content`.
- `thumb` and `files` are rejected unless every value is an HTTP(S) URL.
- `graph_text` requires at least one image URL in `files`.
- `video` requires exactly one video URL in `files`.
- `article` requires `markdown` or `content`.

Before creating content for a known target platform, read its rule file:

```bash
python3 {baseDir}/scripts/96push.py rules --platform <platform> --type <article|graph_text|video>
```

### PublishData Fields


| Field     | Type     | Required    | Description                                              |
| --------- | -------- | ----------- | -------------------------------------------------------- |
| title     | string   | **Yes**     | Content title                                            |
| desc      | string   | No          | Description/summary                                      |
| content   | string   | Conditional | HTML content (articles need this)                        |
| markdown  | string   | Conditional | Markdown source (articles need this)                     |
| autoThumb | bool     | No          | Auto-extract cover from content (default true)           |
| thumb     | string[] | Conditional | Cover image HTTP(S) URLs. Upload/host local images first; no local paths or base64/data URLs. |
| files     | string[] | Conditional | Media HTTP(S) URLs — only for graph_text images and video media. NOT used for articles. |


### By Content Type

**Type selection rule**:

- If the user wants to create or publish a video, use `--type video` explicitly whenever possible.
- If `--type` is omitted, the CLI now infers the type from `--files` or existing content detail.
- If `--type article` is passed together with `files`, the CLI treats the explicit article type as authoritative and rejects/ignores the misplaced media instead of silently creating graph_text/video content.
- Never create article content with video URLs in `files`; video URLs must be video content.

**Article (文章)**:

- **Must have**: `title` + `content` (HTML) or `markdown`
- **Cover image (thumb)**: Some platforms require at least one cover. Set `autoThumb: true` to auto-extract from content images, or provide explicit `thumb` URLs.
- **desc**: Optional summary text, some platforms use it.
- **Do NOT set `files`** for articles — `files` is only for graph_text/video. Images in articles go into the markdown/content body. Cover images go into `thumb`.

**Graph Text (图文/图集)**:

- **Must have**: `title` + `files` (array of image URLs, at least 1)
- **Cover**: Auto-generated from first image if `thumb` is empty.
- **No content/markdown needed** — the images ARE the content.

**Video (视频)**:

- **Must have**: `title` + `files` (array with exactly 1 video URL)
- **Cover**: Auto-generated from video frame if `thumb` is empty. Many platforms require a cover — provide one if possible.
- **desc**: Strongly recommended — most video platforms use it as the video description.

### Cover Image Requirements by Platform

Quick reference only. The source of truth is `references/platform-rules/<platform>.md`.

| Platform                  | Article Cover         | Graph Text Cover | Video Cover     |
| ------------------------- | --------------------- | ---------------- | --------------- |
| WeChat (wechat)           | Required (1 image)    | Auto from images | Required        |
| Douyin (douyin)           | N/A                   | Auto             | Auto from video |
| Toutiao (toutiaohao)      | Required (1-3 images) | Auto             | Auto            |
| Xiaohongshu (xiaohongshu) | N/A                   | Auto from images | Auto            |
| Bilibili (bilibili)       | Optional (headerImg)  | Auto             | Required        |
| Zhihu (zhihu)             | Optional              | Auto             | Auto            |
| Baijiahao (baijiahao)     | Required (1-3 images) | Auto             | Required        |
| CSDN (csdn)               | Optional              | N/A              | Auto            |
| Weibo (sina)              | N/A                   | Auto             | Auto            |
| Kuaishou (kuaishou)       | N/A                   | Auto             | Auto            |
| Sohu (sohuhao)            | Auto from content     | Auto             | Auto            |


**Rule**: When in doubt, always provide at least one `thumb` image. `autoThumb: true` will try to extract from content but may fail if content has no images.

**IMPORTANT**: `thumb` and `files` only accept HTTP(S) URLs. Use `upload --file ... --confirm` only when the file already exists in the OpenClaw runtime; then use the returned pix URL in `thumb`, `files`, or article image `src`. If the image only exists on the user's machine, ask the user to upload it through 96Push/hosting first. Never pass local paths or base64/data URLs.

At publish time, 96Push downloads `thumb`/`files` URLs into task-local files when a target platform needs file upload. Article body pix images are uploaded to temporary public storage only when the target platform needs public image URLs; that upload is cached by image hash for about 47 hours.

---

## Platform Settings Reference (IMPORTANT)

When publishing, each account in `postAccounts` needs a `settings` object. **Different platforms require different fields.** Settings are passed as JSON in the `--accounts-json` parameter or pre-configured via `plat-sets`.

**Before building settings, read only the target platform files in `references/platform-rules/`.** Do not copy settings from a different platform and do not include empty/unrelated fields just because they exist in the aggregate reference.

```bash
python3 {baseDir}/scripts/96push.py rules --platform toutiaohao --type article
python3 {baseDir}/scripts/96push.py rules --platform xiaohongshu,douyin --type video
```

### Common Fields


| Field        | Type   | Description                                                        |
| ------------ | ------ | ------------------------------------------------------------------ |
| timerPublish | object | `{"enable": true, "timer": "YYYY-MM-DD HH:MM:SS"}`                 |
| lookScope    | uint   | Visibility: 0=public, 1=friends, 2=private                         |
| source       | uint   | Content declaration (AI/repost/original, values vary per platform) |
| classify     | string | Category/section                                                   |
| collection   | string | Collection/column                                                  |
| origin       | bool   | Declare as original                                                |
| labels/tag   | string | Tags (separator varies: `/` or `,`)                                |


### Platform-Specific Settings

**wechat (微信公众号)** — Article/Graph Text:

- `author`: Author name
- `publishType`: `"mass"` (群发) or `"publish"` (发布)
- `origin`: Declare original (default false)
- `leave`: Enable comments (default true)
- Timer: now+5min ~ 7 days

**wechat (微信公众号)** — Video (extra fields):

- `materTitle`: Material title
- `barrage`: Enable bullet comments
- `turn2Channel`: Convert to Video Channel

**douyin (抖音)**:

- `allowSave`: Allow others to save (default true)
- `lookScope`: 0=public, 1=friends, 2=private
- `hotspot`: Related trending topic
- `music`: Background music

**toutiaohao (今日头条)** — Article:

- `starter`: Toutiao exclusive
- `syncPublish`: Also publish as Weitoutiao
- Timer: now+2h ~ 7 days. Cannot use timer if `collection` is set.

**xiaohongshu (小红书)**:

- `origin`: Declare original
- `source`: Content declaration — 0=none, 1=fiction/entertainment, 2=AI-generated, 3=marked in body, 4=self-shot, 5=repost source
- `reprint`: Media/source name, only used when `source=5`. Do not combine `origin=true` with `source=5`.
- `mark`: Tag user/location `{"user": true, "search": "keyword"}`
- `lookScope`: 0=public, 1=friends, 2=private
- Timer: now+1h ~ 14 days.
- Draft save clicks `暂存离开`; publish clicks `发布` or `定时发布`.

**bilibili (哔哩哔哩)** — Video/Graph Text:

- `partition`: Section/category (important!)
- `reprint`: Repost source (empty = self-made)
- `creation`: Allow derivative works
- `dynamic`: Fan notification text

**bilibili (哔哩哔哩)** — Article:

- `classify`: Column category
- `headerImg`: Header image URL
- `labels`: Tags (max 10)

**zhihu (知乎)** — Article:

- `question`: Submit to a question
- `source`: Creation declaration — 0=none, 1=spoiler, 2=medical, 3=fiction, 4=finance, 5=AI-assisted
- `topic`: Article topics (max 3, `/` separated)
- `collection`: Column name
- `origin`: Source type — 0=none, 1=official site, 2=news report, 3=TV media, 4=print media
- Draft save is auto-save based and waits for `/api/articles/drafts`; publish waits for `POST /content/publish`.
- Video: set `classify` when possible; `reprint=true` means repost, `false` means original. Timer: now+1h ~ 14 days.

**omtencent (腾讯内容开放平台)** — Article/Video:

- `classify`: Category. For stable tests, use `科技` for articles.
- `labels`: Tags separated by `/`, max 9 tags and max 8 Chinese chars each.
- `activity`: Platform activity keyword.
- `source`: Content declaration — 1=AI generated, 2=fiction/entertainment, 3=from internet, 4=personal opinion, 5=old news. Empty or 0 currently defaults to 4.
- Timer: now+5min ~ 7 days.
- Save/publish waits for platform submit responses; if the AIGC declaration dialog appears, submit it and click save/publish again.

**baijiahao (百家号)**:

- `classify`: Category `"一级/二级"` format
- `byAI`: AI creation declaration
- Timer: now+1h ~ 7 days

**csdn (CSDN)** — Article:

- `labels`: Tags (`/` separated, max 7)
- `artType`: 0=original, 1=repost, 2=translation
- `originLink`: Required for reposts
- Timer: now+4h ~ 7 days

**juejin (掘金)**:

- `tag`: **Required** — must have at least one tag
- `classify`: Category

**kuaishou (快手)**:

- `sameFrame`: Allow others to film with this
- `download`: Allow download
- `sameCity`: Show in same-city feed

**sina (新浪微博)** — Video/Graph Text:

- `type`: 0=original, 1=derivative, 2=repost
- `stress`: Allow highlights (default true)
- `wait`: Wait X seconds before posting

**sina (新浪微博)** — Article:

- `onlyFans`: Only fans can read full text (default true)

**sohuhao (搜狐号)** — Article/Graph Text/Video:

- `classify`: Attribute/category — 观点评论/故事传记/消息资讯/八卦爆料/经验教程/知识科普/测评盘点/见闻记录/运势/搞笑段子/美图/美文
- `declaration`: Source declaration — 0=无特别声明, 1=引用声明, 2=包含AI创作内容, 3=包含虚构创作
- `topic`: Topic keyword (search-based)
- `loginView`: Require login to read full text (default false)
- Timer: now+1h ~ 7 days
- Cover: Auto-extracted from article images if not manually provided; upload also supported

### Timer Publish Constraints


| Platform   | Min Time      | Max Time |
| ---------- | ------------- | -------- |
| wechat     | now + 5 min   | 7 days   |
| toutiaohao | now + 2 hours | 7 days   |
| baijiahao  | now + 1 hour  | 7 days   |
| csdn       | now + 4 hours | 7 days   |
| acfun      | now + 4 hours | 14 days  |
| pinduoduo  | now + 4 hours | 7 days   |
| sohuhao    | now + 1 hour  | 7 days   |
| tiktok     | now + 2 hours | 30 days  |


---

## Output Format Suggestions

### Publish Results

```
📤 Publish Results (Record #7)

✅ WeChat (@AccountA) — Success, 12s
✅ Zhihu (@AccountB) — Success, 8s
❌ Baijiahao (@AccountC) — Failed: Login expired

Success: 2/3, Failed: 1/3
```

### Account List

```
📋 Logged-in Accounts:

1. WeChat - AccountA (ID: 1) [article, graph_text]
2. Douyin - AccountB (ID: 5) [video, graph_text]
3. Bilibili - AccountC (ID: 8) [article, video, graph_text]
```

## Error Handling

- 503 CLIENT_OFFLINE → "96Push not running. Launch it from [https://push.96.cn](https://push.96.cn)"
- 425 → "Another publish task is running. Do NOT retry — use `poll` to wait for the active task."
- `PUBLISH_ALREADY_RUNNING` → A task is already in progress. Use `poll --id <active_record_id>` from the error response. Do NOT call publish again.
- 504 TIMEOUT → "Client response timed out. The task may still be running — check with `poll`."
- 401/403 → "API Key invalid or expired, regenerate in 96Push profile"
- Account `login=false` → "Account login expired, re-login in 96Push client"
- Poll timeout → Report to user: "Publishing is taking longer than expected. The browser automation may still be running. Please check the 96Push client." Do NOT retry publish.

## Safety Rules

- Never expose the API key in responses
- List target accounts and confirm with user before publishing; pass `--confirm` only after that approval
- For more than one target account, require separate approval of the full account list and pass `--confirm-multi-account`
- Require `--confirm` before content update, delete, queue cancel, or platform configuration changes
- Remote publish must use `headless: true`
- Never guess account IDs — always query first
- Don't output raw Base64 image data — just mention it exists
- `thumb` and `files` must be HTTP(S) URLs; never pass user-local paths or base64/data URLs
- If user provides only a local image path, explain that OpenClaw cannot read it and ask for an uploaded/hosted URL or an attachment available to the skill runtime
- When creating content, validate required fields before calling create API
- Before creating/publishing for known targets, run `rules --platform ... --type ...` and follow that platform file
- When building settings, include only fields supported by that platform — missing required fields cause publish failures, and unrelated fields make automation brittle
- **NEVER call `publish` more than once for the same content+accounts batch.** Each call creates a real browser automation task. Duplicate calls will open multiple browsers fighting over the same page, causing all of them to fail and potentially crashing the client.
- **NEVER retry `publish` on failure or timeout.** If publish fails, report the error to the user. If poll times out, report timeout to the user. Let the user decide what to do.
- `publish` now waits and polls automatically. Use `poll` only when you explicitly used `--no-wait` or need to inspect an existing publish record.
