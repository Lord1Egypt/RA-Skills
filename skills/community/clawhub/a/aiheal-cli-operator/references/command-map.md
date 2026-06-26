# Command Map (Full)

AIHeal (`https://aihealing.me/`) is an AI emotional-healing platform that supports audio healing, single-session healing, deep healing plans, AI chat support, emotion-space tracking, and user/subscription management.

`aihealingmecli` provides terminal access to those workflows. This reference is exhaustive for command families, command syntax, and parameter meanings.

If you want the full visual and interactive experience, visit `https://aihealing.me/` directly.

Command-family overview:

- account/session: `config`, `auth`, `whoami`
- user and content: `user`, `audio`
- healing generation: `single-job`, `plan`, `plan-stage-job`
- conversational healing: `chat`
- emotion-space: `emotion`
- billing/entitlement: `subscription`
- communication/feedback: `notification`, `feedback`
- memory context: `memory`, `behavior`
- advanced access: `api`, `healing`

## Runtime Setup

- Recommended: `npm install -g aihealingmecli`
- No-global fallback: `npx -y -p aihealingmecli aiheal ...`
- Canonical command prefix: `aiheal`

## Global Options

- `--api-base <url>`: Override API base for one command
- `--locale <zh|en>`: Override locale header
- `--region <zh|en>`: Override region header and token slot
- `--token <token>`: Inject temporary bearer token
- `--mock`: Enable mock context flag
- `--timeout-ms <ms>`: Override request timeout

## Full Command Catalog

### `config`

- `config get`
- `config set <key> <value>` where key is `apiBaseUrl|locale|region|mock|timeoutMs`
- `config token-set --token <token> [--region <zh|en>]`
- `config token-clear [--region <zh|en>]`

### `auth`

- `auth send-code --email <email> [--type register|reset_password]`
- `auth send-sms-code --phone <phone> [--type register|reset_password|login]`
- `auth register --email <email> --password <pwd> --code <code>`
- `auth register-phone --phone <phone> --password <pwd> --code <code>`
- `auth login --email <email> --password <pwd>`
- `auth login-phone --phone <phone> --code <code>`
- `auth login-phone-password --phone <phone> --password <pwd>`
- `auth reset-password --email <email> --code <code> --password <pwd>`
- `auth reset-password-phone --phone <phone> --code <code> --password <pwd>`
- `auth me`
- `auth onboarding-complete [--payload-file <path> | --body <json>]`
- `auth password-update [--payload-file <path> | --body <json>]`
- `auth logout [--region <zh|en>]`

### `user`

- `user profile <userId>`
- `user profile-update [--payload-file <path> | --body <json>]`
- `user follow <userId>`
- `user unfollow <userId>`
- `user followers <userId>`
- `user following <userId>`
- `user avatar-upload --file <path>`

### `audio`

- `audio list [--category <v>] [--search <v>] [--sort <trending|newest|popular>] [--locale <zh|en>] [--page <n>] [--limit <n>]`
- `audio recommended [--limit <n>] [--locale <zh|en>]`
- `audio get <audioId>`
- `audio by-request <requestId>`
- `audio my [--sort <v>] [--page <n>] [--limit <n>]`
- `audio liked [--sort <v>] [--page <n>] [--limit <n>]`
- `audio create [--payload-file <path> | --body <json>]`
- `audio update <audioId> [--payload-file <path> | --body <json>]`
- `audio delete <audioId>`
- `audio like <audioId>`
- `audio favorite <audioId>`
- `audio heart-echo <audioId> [--payload-file <path> | --body <json>]`
- `audio web-url <audioId>`
- `audio links <audioId>`
- `audio download-url --url <url> --output <path> [--audio-id <audioId>]`
- `audio download <audioId> --output <path>`

`audio comments`:

- `audio comments list <audioId> [--page <n>] [--limit <n>]`
- `audio comments add <audioId> [--payload-file <path> | --body <json>]`
- `audio comments delete <audioId> <commentId>`
- `audio comments like <audioId> <commentId>`

### `plan`

- `plan create [--payload-file <path> | --body <json>]`
- `plan my [--status <draft|active|completed>] [--page <n>] [--limit <n>]`
- `plan get <planId>`
- `plan by-request <requestId>`
- `plan update <planId> [--payload-file <path> | --body <json>]`

### `single-job`

- `single-job create [--payload-file <path> | --body <json>]`
- `single-job get <jobId>`
- `single-job by-request <requestId>`
- `single-job wait --request-id <requestId> [--interval-ms <ms>] [--timeout-ms <ms>]`

`single-job create` local payload validation behavior:

- `requestId` is optional; CLI auto-generates one when missing/blank.
- Payload is validated before request; failures return `error.code=VALIDATION_ERROR`.
- Validation errors include field-level `issues[]` with `field`, `message`, `expected`, `actual`, and optional `suggestion`.

### `plan-stage-job`

- `plan-stage-job create [--payload-file <path> | --body <json>]`
- `plan-stage-job get <planId> <stageIndex>`
- `plan-stage-job wait <planId> <stageIndex> [--interval-ms <ms>] [--timeout-ms <ms>]`

`plan-stage-job create` local payload validation behavior:

- Payload is validated before request; failures return `error.code=VALIDATION_ERROR`.
- Validation errors include field-level `issues[]` with `field`, `message`, `expected`, `actual`, and optional `suggestion`.
- `requestId` is optional and kept as-is when provided (no auto-generation).

### `chat`

- `chat config`
- `chat quota`
- `chat send <sessionId> --message <text>`
- `chat send-stream <sessionId> --message <text>`
- `chat single-healing-create <sessionId>`

`chat session`:

- `chat session create`
- `chat session list [--page <n>] [--limit <n>]`
- `chat session rename <sessionId> --title <title>`
- `chat session turns <sessionId> [--page <n>] [--limit <n>]`

`chat draft`:

- `chat draft get <sessionId>`
- `chat draft generate <sessionId> [--regenerate]`

### `emotion`

- `emotion overview`
- `emotion planet`
- `emotion curve [--days <n>]`
- `emotion timeline [--status <active|released|all>] [--page <n>] [--limit <n>]`
- `emotion text-job-create [--payload-file <path> | --body <json>]`
- `emotion text-job-get <jobId>`
- `emotion text-job-wait <jobId> [--interval-ms <ms>] [--timeout-ms <ms>]`
- `emotion text-entry-create [--payload-file <path> | --body <json>]`
- `emotion voice-entry-create --file <path> [--occurred-at <iso>]`
- `emotion release <entryId> [--payload-file <path> | --body <json>]`

### `subscription`

- `subscription status`
- `subscription orders`
- `subscription order-get <orderId>`
- `subscription order-cancel <orderId>`
- `subscription admin-refund --order-id <orderId> [--reason <text>]`
- `subscription create-order --plan-type <7d|1m|1y>`
- `subscription confirm --order-id <orderId>`
- `subscription paypal-create-order --plan-type <7d|1m|1y>`
- `subscription paypal-capture-order --order-id <orderId> --paypal-order-id <paypalOrderId>`
- `subscription creem-create-order --plan-type <7d|1m|1y>`
- `subscription creem-confirm-order --order-id <orderId> [--checkout-id <id>]`
- `subscription consume --feature <single|plan>`

### `notification`

- `notification list [--locale <zh|en>] [--page <n>] [--limit <n>]`
- `notification unread-count [--locale <zh|en>]`
- `notification read-all`
- `notification read <id>`

### `feedback`

- `feedback submit [--payload-file <path> | --body <json>]`

### `memory`

- `memory context [--mode <single|plan>]`
- `memory compact-plan <planId>`

### `behavior`

- `behavior ingest [--payload-file <path> | --body <json>]`
- `behavior rebuild`
- `behavior memory`

### `healing`

- `healing health --base <url>`
- `healing pipeline --base <url> [--payload-file <path> | --body <json>]`
- `healing plan --base <url> [--payload-file <path> | --body <json>]`
- `healing voice-preview --base <url> --output <path> [--payload-file <path> | --body <json>]`
- `healing download-file --base <url> --path <remotePath> --output <path>`

### `api`

- `api request --method <METHOD> --path <endpointPath> [--query key=value ...] [--payload-file <path> | --body <json>] [--no-auth]`

### `whoami`

- `whoami`

## Parameter Glossary

- `<userId>`: target user identifier
- `<email>`: email used for auth commands
- `<phone>`: phone number used for auth commands
- `<pwd>`: password value in command examples
- `<code>`: email or sms verification code
- `<audioId>`: audio identifier
- `<planId>`: healing plan identifier
- `<requestId>`: async request identifier (optional in `single-job create` payload because CLI can auto-generate; optional in `plan-stage-job create` payload without auto-generation)
- `<jobId>`: async job identifier
- `<stageIndex>`: zero-based plan stage index
- `<commentId>`: comment identifier under one audio
- `<sessionId>`: chat session identifier
- `<entryId>`: emotion entry identifier
- `<orderId>`: subscription order identifier
- `<id>`: notification identifier
- `<METHOD>`: HTTP method such as `GET|POST|PUT|DELETE|PATCH`
- `<endpointPath>`: API path, e.g. `/audio`
- `<base>`: healing service base URL
- `<path>`: remote file path argument for `healing download-file`
- `<remotePath>`: remote file path for healing file download endpoint
- `<paypalOrderId>`: PayPal platform order id
- `<title>`: new title for chat session rename
- `<text>` / `--message`: plain text input for chat turn
- `--type`: auth code purpose (`register`, `reset_password`, or `login` depending on endpoint)
- `--plan-type`: `7d|1m|1y`
- `--feature`: `single|plan`
- `--status`:
  - `plan my`: `draft|active|completed`
  - `emotion timeline`: `active|released|all`
- `--sort`:
  - `audio list`: `trending|newest|popular`
  - `audio my/liked`: service-supported sort value
- `--locale`: `zh|en`
- `--region`: `zh|en`
- `--page`: paginated page index
- `--limit`: paginated page size
- `--days`: aggregation window for emotion curve
- `--interval-ms`: polling interval
- `--timeout-ms`: timeout in milliseconds
- `--file`: local file path used by upload commands
- `--output`: local output file path for download/export commands
- `--url`: source URL/path for `audio download-url`
- `--audio-id`: optional audio id for `audio download-url`
- `--occurred-at`: ISO datetime for voice emotion entry timestamp
- `--query key=value`: repeated query kv pairs in raw API mode
- `--body`: inline JSON payload string
- `--payload-file`: JSON payload file path
- `--no-auth`: disable auth header in raw API mode
- `--regenerate`: regenerate chat draft
- `--checkout-id`: optional checkout identifier for creem confirm
- `--reason`: optional reason text for `subscription admin-refund`

## Required Field Matrix

Rules:

- Positional args (`<...>`) are required.
- Flags shown without `[]` are required.
- Payload required fields are primarily enforced by server validation.
- `single-job create` and `plan-stage-job create` additionally perform CLI local validation before request.

Payload commands summary:

- `auth send-code`: R=`email`; O=`type`
- `auth send-sms-code`: R=`phone`; O=`type`
- `auth register`: R=`email,password,code`
- `auth register-phone`: R=`phone,password,code`
- `auth login`: R=`email,password`
- `auth login-phone`: R=`phone,code`
- `auth login-phone-password`: R=`phone,password`
- `auth reset-password`: R=`email,password,code`
- `auth reset-password-phone`: R=`phone,password,code`
- `auth password-update`: R=`currentPassword,newPassword`
- `auth onboarding-complete`:
  - R=`birthDate,gender,lifeStage,traitRationality,traitPace,interests`
  - O=`nickname,lifeStageDetail,longTermGoals,responseLengthPreference,encouragementStrength,mbti,lowMoodCoping,therapyHistory,healingPreference,motto,bio`
- `user profile-update`: all optional
- `audio create`: R=`title,duration,category`; O=`description,healingOutline,audioUrl,healingFilePath,coverImage,tags,isPublic,shareText,userSelections,planId,planStage,healingRequestId`
- `audio update`: all optional
- `audio heart-echo`: R=`helpful`; O=`fitScore,whisper`
- `audio web-url`: R=`audioId`
- `audio links`: R=`audioId`
- `audio download-url`: R=`url,output`; O=`audioId`
- `audio comments add`: R=`content`; O=`parentComment`
- `plan create`: R=`title`; O=`description,stages,currentStage,status,totalDuration,healingRequestId,healingTheme,launchWish,userSelections`
- `plan update`: all optional
- `single-job create`: R=`userRequest`; O=`requestId(auto-generated when missing),shareText,voiceId,selectedEmotions,intensity,energyLevel,selectedScenarios,bodySensations,currentEnvironment,sessionGoal,sessionApproach,avoidTopics,useHistoryMemory,selectedGoals,gender,age,mbti,lifeStage,sleepQuality,meditationExp`
- `plan-stage-job create`: R=`planId,stageIndex,planPath,day`; O=`requestId(optional),userRequest,shareText,voiceModel,voiceId,userSelections,fixedTags`
- `chat send`: R=`message`
- `chat send-stream`: R=`message`
- `chat session rename`: R=`title`
- `emotion text-job-create`: R=`text`; O=`occurredAt`
- `emotion text-entry-create`: R=`text`; O=`occurredAt`
- `emotion voice-entry-create`: R=`file`; O=`occurredAt`
- `emotion release`: O=`style,message`
- `subscription create-order`: R=`planType`
- `subscription admin-refund`: R=`orderId`; O=`reason`
- `subscription confirm`: R=`orderId`
- `subscription paypal-create-order`: R=`planType`
- `subscription paypal-capture-order`: R=`orderId,paypalOrderId`
- `subscription creem-create-order`: R=`planType`
- `subscription creem-confirm-order`: R=`orderId`; O=`checkoutId`
- `subscription consume`: R=`feature`
- `feedback submit`: R=`content`; O=`contact,pageUrl`
- `behavior ingest`: O=`events` (array, recommended)
- `api request`: R=`method,path`; O=`query,body,payloadFile,noAuth`
- `healing pipeline`: R=`base` + payload
- `healing plan`: R=`base` + payload
- `healing voice-preview`: R=`base,output`; O=`payload`

## Fast Recipes

1. Login then verify:

```bash
aiheal auth login --email you@example.com --password '***'
aiheal whoami
```

2. List newest audios:

```bash
aiheal audio list --sort newest --limit 20
```

3. Create + wait single job:

```bash
aiheal single-job create --payload-file ./single-job.json
aiheal single-job wait --request-id <requestId>
```

Use `data.job.requestId` from the `single-job create` response as `<requestId>`.

4. Stream one chat turn:

```bash
aiheal chat send-stream <sessionId> --message "我现在很焦虑"
```

5. Submit raw endpoint request:

```bash
aiheal api request --method GET --path /audio --query page=1 limit=10 --no-auth
```

6. Smoke check installed CLI package (path-independent):

```bash
NPM_CONFIG_CACHE=/tmp/aiheal-npm-cache npx -y -p aihealingmecli aiheal --help
NPM_CONFIG_CACHE=/tmp/aiheal-npm-cache npx -y -p aihealingmecli aiheal config get
```

Smoke script parameters:

- Script: `scripts/smoke_check.sh`
- `AIHEAL_NPM_PACKAGE`: npm source used in `npx -p` (default `aihealingmecli`; can be tarball path)
- `AIHEAL_NPM_CACHE_DIR`: cache dir for npm/npx
- `RUN_NETWORK_SMOKE=1`: additionally run `audio list --limit 1 --sort newest`

7. Resolve website/detail and downloadable links for one audio:

```bash
aiheal audio links <audioId>
aiheal audio web-url <audioId>
```

8. Download from a raw OSS/direct URL:

```bash
aiheal audio download-url --url "<source-url-or-path>" --output ./audio.mp3
```
