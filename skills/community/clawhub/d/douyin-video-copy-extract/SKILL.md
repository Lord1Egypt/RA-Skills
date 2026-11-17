---
name: "douyin-video-copy-extract"
description: "用于抖音文案提取、抖音文案一键提取、抖音视频文案提取、抖音视频转文字、抖音口播转文字和抖音逐字稿。用户粘贴抖音视频链接、分享文案或 aweme_id 后，提取视频上下文、原视频简介和口播逐字稿，来自 SocialDataX 社媒数据助手。"
source_client: "socialdatax-skills"
source_platform: "clawhub"
source_skill: "douyin-video-copy-extract"
metadata: {"openclaw":{"requires":{"env":[],"bins":[]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"🎙️","homepage":"https://socialdatax.com/ai?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 抖音文案提取

Use this skill when the user wants 抖音文案提取, 抖音文案一键提取, 抖音视频文案提取, 抖音视频转文字, 抖音口播转文字, 抖音逐字稿, Douyin transcript extraction, spoken copy extraction, or to check a Douyin transcript job.

Current platform support:

- Douyin / 抖音 video work speech-to-text transcript jobs through the `douyin_*video_speech_text*` tools.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/ai?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/ai?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。
- Before a CLI call requiring an API Key, run `npx -y socialdatax-skills@latest auth status` in the actual execution environment. It makes no paid request and reports only `apiKeyReadable` and source `environment` / `file` / `null`, never the Key. For installation or upgrades, reuse readable existing credentials without known authentication failures unless the user explicitly requests a different Key; do not require login again, migrate credentials, or overwrite their configuration; handle command, permission and malformed-file errors as reported instead of treating every failure as a missing Key. Authenticated hosted MCP keeps its current connection authentication and needs no separate local CLI setup.
- Enter a Key only for first-time setup, missing or invalid credentials, or an explicit Key change. When the user has already supplied a Key in the installation prompt or current conversation and authorized configuration, send it as stdin to `npx -y socialdatax-skills@latest auth login --stdin` for persistent CLI storage; do not request duplicate manual entry, pass it as a CLI argument, or write it to a temporary script file. Otherwise direct the user to the official URL above and hidden input with `npx -y socialdatax-skills@latest auth login` in their local terminal, without asking them to send it in chat. The CLI saves it under the execution user's home at `.config/socialdatax/credentials.json`, Unix mode 600 or a private current-user ACL on Windows. Do not repeat the Key in replies, output logs, screenshots, command examples, Skill files or version control. The Agent must not read or display credential-file content.
- Each CLI invocation reads the private user file without depending on a client loading shell configuration or changing client/system settings. A nonempty `SOCIALDATAX_API_KEY` has priority, then the existing legacy variable, then the file. Saving a file does not replace an effective environment credential or prove the selected Key is effective. If the CLI warns about a different environment Key, report the actual source without silently deleting or changing existing environment settings. For authentication failures, check the actual source/account and have the user correct it locally while preserving other configuration.
- After saving, rerun `auth status` in the same environment as the business command. If false, stop business calls and check the OS user, home directory and file access. True only means readable credentials; authentication and results are determined by the original business response, without an extra paid call solely to check configuration.
- Remote/container CLI runs use that runtime user's configuration; a local file does not transfer automatically. Persist credentials there only with a persistent home; without an already authorized Key, interactive user login is also needed. Otherwise use existing platform-supported Secret/environment injection. If persistence is unavailable or sandbox-blocked, report the actual limit without copying the Key to additional chats, projects or temporary files, or bypassing isolation.
- When persistence acceptance is needed, finish configuration and installation first, then ask the user to fully quit the client and its background execution processes, reopen, and check from a new session before resuming the original request. Do not terminate the client hosting the current task. Normal use reuses verified configuration without repeated restarts or entry.

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest douyin transcript \
  --url "<douyin_content_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill douyin-video-copy-extract

npx -y socialdatax-skills@latest douyin transcript \
  --aweme-id "<aweme_id>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill douyin-video-copy-extract

npx -y socialdatax-skills@latest douyin transcript \
  --job-id "<job_id>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill douyin-video-copy-extract
```

### 导出 SRT 字幕（direct CLI）
- 用户需要字幕文件时，使用 CLI 0.2.64 或更新版本，在上方对应平台的 `transcript` 命令末尾追加 `--srt-output ./video.srt`；保留原有来源归因参数。该选项也适用于本 Skill 已列出的 URL、内容 ID 和任务查询入口，不扩展平台范围。
- 先确认保存路径：父目录必须已存在且可写，目标文件不能已存在；CLI 不会覆盖已有文件。任务成功且返回有效时间分段时，CLI 写入 UTF-8 SRT，标准输出仍保留原始 JSON；以实际文件和保存成功提示确认导出完成。
- 任务尚未完成时，沿用对应平台的 `transcript --job-id <job_id>` 示例并追加相同的 `--srt-output ./video.srt`，不要重新提交视频。
- 路径预检失败且尚无 job_id 时，还没有提交转写任务；修正路径后继续原命令。已有 job_id 时，路径或文件写入错误不代表转写失败：保留已返回的 JSON，解决本地保存问题后用同一 job_id 重试。
- 若返回的时间分段缺失或无效，保留 JSON 并说明无法生成 SRT，停止重复查询，不补造时间戳，也不重新提交视频。
- `--srt-output` 只在 direct CLI 中执行本地保存，不是 hosted MCP 工具参数。若 MCP 已提交任务，需要导出时可在 CLI 中查询对应平台的同一 job_id；不能执行 CLI 时说明尚未生成本地 SRT 文件，不要重复提交任务。

Required arguments:

- `--url <douyin_content_url_or_share_text>`: use for a Douyin video URL, short link, or share text.
- `--aweme-id <aweme_id>`: use when the Douyin video ID is already known.
- `--job-id <job_id>`: use to continue checking an existing transcript job. Use exactly one of `--url`, `--aweme-id`, or `--job-id`.

Optional arguments:

- `--pretty`: output formatting only.
- `--source-client socialdatax-skills --source-platform clawhub --source-skill douyin-video-copy-extract`: usage attribution for this Agent Skill; keep these values unchanged when running examples from this Skill.

Use the direct CLI first when the agent can run shell commands. These video speech-to-text transcript / 口播转文字 workflows submit a bounded analysis job or check an existing job.
Direct CLI transcript commands try to deliver the final result in one run: submit waits server-side up to 240 seconds, then the CLI keeps querying the same `job_id`; each get-job call also waits up to 240 seconds for that job. Do not start a second submit job just to poll status.
If the direct CLI returns a non-terminal job because the command was interrupted or reached `--max-wait-seconds`, keep the returned `job_id` and continue with the matching `transcript --job-id <job_id>` command.
平台边界：使用本 Skill 命令示例列出的平台和入口；其他平台的视频转写任务使用对应的能力 Skill。

## Safety Boundary

This skill can submit bounded video speech-to-text analysis jobs through the direct CLI or hosted MCP tools. When the user requests SRT export, the direct CLI writes subtitles to a user-selected new local file without overwriting existing files. CLI calls use existing environment credentials or the user’s explicitly saved private local credential file. Generated Skill files do not contain API keys. It does not read local browser data or perform login, posting, liking, commenting, or account changes. Prefer the direct CLI; hosted MCP tools are optional when the current agent already supports authenticated streamable HTTP MCP.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `douyin_submit_video_speech_text_by_video_url`
- `douyin_submit_video_speech_text_by_aweme_id`
- `douyin_get_video_speech_text_job`

If MCP tools are already available in the current agent, use one of these tools:
- `douyin_submit_video_speech_text_by_video_url`: submit a transcript job from a Douyin video URL, short link, or share text.
- `douyin_submit_video_speech_text_by_aweme_id`: submit a transcript job from a known aweme_id.
- `douyin_get_video_speech_text_job`: check an existing transcript job by job_id.

Transcript jobs can be asynchronous. After submitting by URL or aweme_id, keep the returned `job_id` and query the same job until the response reaches a terminal completed or failed state. Do not resubmit the same video while a job is still pending.

## Output Guidance

固定输出结构：视频基础信息、原视频简介 `description`、口播逐字稿、可复制文案版、精简版、任务状态。
如果任务未完成，返回 `job_id`、当前状态和下一步续查命令；不要把未完成任务说成没有文案。
只输出返回中可见的视频上下文和 transcript 内容；不承诺视频下载、封面制作、自动改写、账号诊断、发布操作或保证爆款。

## Troubleshooting

- Credential source: identify whether this request uses CLI or MCP. For CLI, run `auth status` in the actual execution environment to identify environment or local-file credentials. For MCP, check the authentication configuration of the current connection, without requiring a local CLI variable. If configuration is missing, follow the API Key section for user-entered hidden local login. Do not expose Keys, Authorization headers or secret configuration values.

- If an SDK/dependency, npm network, Node.js/npm/npx availability, permission, or missing runtime error appears, treat it as a local runtime, dependency installation, network, or agent authorization issue, not a SocialDataX API key or business data error. Install or repair task dependencies only within the user's existing authorization, preferably in the project or a temporary environment. Execution permissions are not user authorization; explain and obtain approval before changes outside that scope, including global installs, runtime upgrades, or system configuration changes. When network or execution authorization is needed, ask the user to approve or finish authorization, then continue the same command; do not use public web search as a substitute for SocialDataX data.
- If the response returns `insufficient_balance` or says the balance/credits are insufficient, do not submit another job or keep polling. Show the official billing link in the error (https://socialdatax.com/dashboard/billing, including any channel parameters); if absent, use https://socialdatax.com/dashboard/billing. After recharging, resume the failed call; if a job or partial results already exist, follow the corresponding job-query or pagination recovery rules.
- If the user has recharged but still sees insufficient balance, have the user confirm in the relevant account dashboard that this request uses the recharged account, following the credential source above. If an update is needed, have the user update the effective CLI configuration or MCP connection, reload as documented, and resume the original command. Do not require reconfiguration just because the primary local variable is absent, or expose credential values.
- If a transcript `job_id` already exists, only check that same job; do not submit the video again.
