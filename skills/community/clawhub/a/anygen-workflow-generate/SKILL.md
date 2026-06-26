---
name: anygen-workflow-generate
version: 1.0.0
description: "AI-powered content creation suite. Create slides/PPT, documents, diagrams, websites, data visualizations, research reports, storybooks, financial analysis, and images. Supports: pitch decks, keynotes, technical docs, PRDs, white papers, architecture diagrams, flowcharts, mind maps, org charts, ER diagrams, sequence diagrams, UML, landing pages, CSV analysis, earnings research, posters, banners, comics, and more."
metadata:
  requires:
    bins: ["anygen"]
    env: ["ANYGEN_API_KEY"]
  install:
    - id: node
      kind: node
      package: "@anygen/cli"
      bins: ["anygen"]
  cliHelp: "anygen --help"
---

# Content Generation Workflow

> **PREREQUISITE:** Read [`../anygen-shared/SKILL.md`](../anygen-shared/SKILL.md) for auth, global flags, and security rules.

## Rules

**Follow these rules exactly.**

- Schema: run `anygen schema <resource.method>` to check required params and response if needed.
- Long-running: `--wait` commands will block, MUST use `sessions_spawn` to run in the background.
- Sending files on Feishu/Lark: Do not use the message tool to send files. It corrupts non-ASCII filenames into `%XX` garbage. Strictly follow the curl process in "Sending files".

## Steps

1. **Discover operations metadata**:
   `anygen task operations`
   Do not guess operation types. Always run to get supported operations and their estimated time and thumbnail support.

2. **Upload reference files** (skip if no reference files):
   `anygen file upload --data '{"file":"./data.csv"}'`
   → Save `file_token` for step 4. Tell user the file was uploaded.

3. **Gather requirements** (skip if requirements are already clear):
   `anygen task prepare --data '{"operation":"slide","messages":[{"role":"user","content":"Make a Q4 report PPT"}]}'`
   Present `reply` to user, collect their answer, then call again with `prepare_session_id` and updated `messages`:
   `anygen task prepare --data '{"operation":"slide","prepare_session_id":"<id>","messages":[...previous messages...,{"role":"user","content":"user's answer"}]}'`
   Repeat until `status=ready`.
   → When ready, show `suggested_task_params.prompt` as outline, confirm with user, then use it as `prompt` in step 4.

4. **Create task**:
   `anygen task create --data '{"operation":"slide","prompt":"...","file_tokens":["<file_token>"]}'`
   → Tell user the task is created, share `task_url` and estimated time (from step 1).

5. **Wait for completion** (long-running, must run in background via `sessions_spawn`):
   `anygen task get --params '{"task_id":"<id>"}' --wait`

6. **Deliver** (after step 5 completes, check the result):
   - **No files** (`output.files` empty): show `message` to user if present.
   - **Has files + has thumbnail** (`has_thumbnail` from step 1):
     `anygen task +download --task-id <id> --thumbnail`
     → Send thumbnail image with `task_url` as preview. Do not download files yet — wait for user to request download or modifications (→ step 7).
   - **Has files + no thumbnail**:
     `anygen task +download --task-id <id>`
     → Send files to user (see "Sending files" below).

7. **Modify** (on user request):
   `anygen task message send --params '{"task_id":"<id>"}' --data '{"content":"..."}'`
   Then wait for result (long-running, must run in background via `sessions_spawn`):
   `anygen task message list --params '{"task_id":"<id>"}' --wait`
   → Repeat from step 6 to re-export and deliver. All modifications reuse the same task.

## Sending files

When user requests file download, or when delivering files from step 6:
`anygen task +download --task-id <id>`
To download specific files: `anygen task +download --task-id <id> --file report.pptx`

**Feishu/Lark** (message tool corrupts non-ASCII filenames, use curl instead):
1. Get credentials: read `app_id` and `app_secret` from the config file (e.g. `cat ~/.openclaw/openclaw.json | jq '.channels.feishu'` instead of `openclaw config get`). Make sure to use the credentials matching the current account.
2. Get token: `curl -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' -H 'Content-Type: application/json' -d '{"app_id":"<app_id>","app_secret":"<app_secret>"}'`
3. Upload + Send per file type:
   - **Images** (thumbnail, png, jpg, etc.):
     Upload: `curl -X POST 'https://open.feishu.cn/open-apis/im/v1/images' -H 'Authorization: Bearer <tenant_access_token>' -F 'image_type=message' -F 'image=@./preview.png'`
     Send: `curl -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' -H 'Authorization: Bearer <tenant_access_token>' -H 'Content-Type: application/json' -d '{"receive_id":"<chat_id>","msg_type":"image","content":"{\"image_key\":\"<image_key>\"}"}'`
   - **Documents** (pptx/docx/pdf, etc.):
     Upload: `curl -X POST 'https://open.feishu.cn/open-apis/im/v1/files' -H 'Authorization: Bearer <tenant_access_token>' -F 'file_type=ppt' -F 'file=@./output.pptx' -F 'file_name=output.pptx'`
     `file_type` values: `opus` (audio), `mp4` (video), `pdf`, `doc`, `xls`, `ppt`, `stream` (other).
     Send: `curl -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' -H 'Authorization: Bearer <tenant_access_token>' -H 'Content-Type: application/json' -d '{"receive_id":"<chat_id>","msg_type":"file","content":"{\"file_key\":\"<file_key>\"}"}'`

**Other platforms:** Send via the platform's message tool.

## See Also

- [`anygen-task-download`](../anygen-task-download/SKILL.md) — Download artifacts from a completed task
