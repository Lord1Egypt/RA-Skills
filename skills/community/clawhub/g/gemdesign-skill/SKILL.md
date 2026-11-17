---
name: gemdesign-skill
description: Generate, save, and modify GemDesign prototype pages via CLI. Invoke when user wants to create UI prototypes, design pages, or batch-generate pages from requirements.
version: 0.1.11
license: MIT
compatibility: [claude, codex, cursor, trae, hermes, openclaw, qoder, opencode , workbuddy, qclaw]
---

# GemDesign Prototyping

Use the `gemdesign` CLI to create, save, and modify high-fidelity prototype pages on the GemDesign platform. You generate HTML following the GemDesign Page Spec, validate it, then save via CLI.

## When to Invoke

- User wants to create a UI prototype or design a page
- User has a requirements document and wants batch page generation
- User wants to modify an existing GemDesign page
- User wants to view existing GemDesign pages

## Prerequisites

> **CRITICAL: Step 1, Step 2, and Step 2.5 MUST be executed strictly in order BEFORE starting any Workflow. Each step MUST fully complete before proceeding to the next. Do NOT skip, parallelize, or advance until the current step is confirmed successful.**
>
> **IMPORTANT — Step 3 timing**: Step 3 (Start the Local Server) is NOT executed immediately after login. It MUST be executed INSIDE a Workflow, AFTER the app is created or reused (i.e., after `gemdesign app create` / `gemdesign app use` + `gemdesign app info`), and BEFORE any page generation. Starting the server before the app exists is a violation — the server serves pages from the project subdirectory derived from the app, so the app must exist first.

### Step 1: Verify & Install GemDesign CLI (MUST complete before Step 2)

**ALWAYS verify CLI installation and version first** before doing any other work. This step is a hard gate — no other operations (`auth`, `app`, `page`, `style`, etc.) may run until this step is confirmed complete.

1. **Check if CLI is installed**:
   ```bash
   npm list -g @gemdesign-ai/cli
   ```
   - If the command returns version info (e.g., `@gemdesign-ai/cli@1.2.3`), CLI is installed - proceed to step 2.
   - If the command returns empty or error (e.g., `(empty)` or `ERR!`), CLI is NOT installed. Run:
     ```bash
     npm install -g @gemdesign-ai/cli
     ```
     Wait for the installation to finish, then re-verify with `npm list -g @gemdesign-ai/cli`. Do NOT proceed until re-verification confirms the installed version.

2. **Check if CLI is latest version** (only after step 1 confirms CLI is installed):
   ```bash
   npm outdated -g @gemdesign-ai/cli
   ```
   - If the command returns empty or shows `Current=Latest`, CLI is up-to-date - this step is complete, proceed to Step 2.
   - If the command shows version info with different `Current` and `Latest` values, CLI is outdated. Update to latest:
     ```bash
     npm update -g @gemdesign-ai/cli
     ```
     Wait for the update to finish, then re-verify with `npm outdated -g @gemdesign-ai/cli`. Do NOT proceed until re-verification confirms the CLI is up-to-date.

After this step is confirmed complete, the `gemdesign-ai` command is available globally at the latest version. **Only then** may you advance to Step 2.

### Step 2: Verify Login (MUST complete after Step 1, before any Workflow)

**ALWAYS verify login status** after Step 1 is complete. Run this command:
```bash
gemdesign auth whoami
```
- If it succeeds (returns user info), the user is logged in — proceed to a Workflow (A/B/C). Step 3 (local server) will be executed INSIDE the workflow, after the app is created/reused.
- If it fails (returns an error like "GemDesign令牌 无效" or "未提供 GemDesign令牌"), the user is NOT authenticated. You MUST:
  1. Tell the user: if they don't have an account or GemDesign令牌 yet, go to **https://design.gemcoder.com** to register an account and get a GemDesign令牌. The GemDesign令牌 retrieval path is: log in to the platform -> click **个人中心** (Personal Center) -> get the **GemDesign令牌** (GemDesign令牌).
  2. Ask the user for their GemDesign令牌 (use `AskUserQuestion` tool to prompt the user to input their GemDesign令牌).
  3. Once the user provides their GemDesign令牌, **automatically run** the login command for them:
     ```bash
     gemdesign auth login --token <user_provided_token>
     ```
  4. Re-verify with `gemdesign auth whoami` to confirm login succeeded.
  5. If login still fails, repeat from step 2 (ask the user to provide their GemDesign令牌 again).
  6. Only proceed to a Workflow after login is confirmed.

**HARD GATE**: Until login is confirmed via `gemdesign auth whoami`, you MUST NOT perform ANY page-generation work — this includes CLI commands (`app`, `page`, `style`, `validate`) AND local file operations (writing `.html`, streaming write, creating the `./output/` directory). Local HTML generation is NOT a workaround for the login gate; a page can only be saved to the platform by an authenticated user, so generating it before login is wasted work. If login fails, stop and resolve authentication first — do not start writing any HTML.

### Step 2.5: Clean Up and Configure htmlWorkdir (MUST complete after Step 2, before any Workflow)

After login is confirmed, FIRST clean up stale empty project directories left over from previous interrupted sessions, THEN configure the HTML working directory (`htmlWorkdir`). The order is MANDATORY: `cleanup` MUST run BEFORE `workdir --path`, never after. Both operations MUST complete before starting any Workflow (in particular, before `app create`).

> **CRITICAL — Why cleanup MUST run BEFORE workdir (order is non-negotiable):** `gemdesign server workdir --path ./output` creates the `./output` directory — at this moment it is an empty workdir with NO project subdirectories (`{projectName}__{appuuid}`) yet, because `app create` has not run. `gemdesign server cleanup` runs `pruneEmptyWorkdirs()`, which deletes any workdir directory that contains zero project subdirectories AND removes it from the `htmlWorkdir` config. If you run `workdir` first and then `cleanup`, the freshly-created empty `./output` is treated as a stale empty workdir — `cleanup` deletes the directory and wipes it from config, leaving `htmlWorkdir` empty. Downstream effect: `app create` skips local folder creation (returns a `warning`), and `server start` refuses to start (`"未配置 htmlWorkdir..."`), causing "page generated but canvas not showing". Running `cleanup` FIRST avoids this: it clears stale state from previous sessions, then `workdir` creates `./output` LAST so it survives. (Note: `cleanup` does NOT require `htmlWorkdir` to be pre-configured — when unconfigured it simply returns `"未配置 htmlWorkdir，无需清理"` and exits cleanly.)

1. **Clean up empty project directories** (MUST run FIRST, before configuring htmlWorkdir):
   ```bash
   gemdesign server cleanup
   ```
   - If `htmlWorkdir` is not configured yet, the command returns `{"success":true,"message":"未配置 htmlWorkdir，无需清理","removedDirs":[],"removedLocks":[],"removedWorkdirs":[],"removedWorkdirDirs":[]}` — this is normal, continue to step 2.
   - If `htmlWorkdir` is already configured from a previous session, the command scans each configured workdir for project subdirectories (named `{projectName}__{appuuid}`) and:
     - Deletes **empty project directories**: project subdirectories that contain zero `.html` files (created by `app create` but never had a page saved — e.g., the session was interrupted).
     - Cleans **orphaned streaming files**: `.stream.lock` files left over from streaming write that was started but never completed.
     - Removes **empty workdirs**: workdir directories that contain zero project subdirectories are deleted and removed from config (this is exactly why `workdir --path` MUST run AFTER `cleanup`, not before).
   - Returns JSON: `{"success":true,"message":"清理完成：删除 N 个空项目目录，清理 M 个遗留文件，移除 K 个无项目的 htmlWorkdir","removedDirs":[...],"removedLocks":[...],"removedWorkdirs":[...],"removedWorkdirDirs":[...]}`
   - **This step is non-blocking**: cleanup failures do not prevent proceeding to a Workflow. The command always returns `success: true` unless an unexpected error occurs.

2. **Configure htmlWorkdir** (MUST run AFTER step 1; run once, persists across sessions):
   > **CRITICAL - `app create` sync-creates the local project folder under `htmlWorkdir`, and `server start` validates `htmlWorkdir` before launching.** If `htmlWorkdir` is not configured, `app create` skips local folder creation (returns a `warning`), and `server start` returns `{"success":false,"error":"未配置 htmlWorkdir，请先执行 gemdesign server workdir --path <path> 设置 HTML 工作目录"}` and refuses to start. This prevents the background process's cwd from mismatching the actual HTML generation directory, which would cause fileWatcher to miss `.html` changes and the canvas to stay blank ("page generated but canvas not showing").

   ```bash
   gemdesign server workdir --path ./output
   ```
   - Relative paths are resolved against the current working directory to an absolute path.
   - Verify with `gemdesign server workdir` (no flags) - returns `{"success":true,"htmlWorkdir":["<absolute path>"]}`.
   - The `./output` directory created here will NOT be deleted by `cleanup` within this same Step 2.5, because `cleanup` already ran in step 1. Do NOT re-run `cleanup` after this step — re-running it would delete the freshly-created empty `./output` (since `app create` has not run yet and there are no project subdirectories).

### Step 3: Start the Local Server (MUST complete after app is created/reused, before any page generation)

> **CRITICAL - HARD GATE: You MUST open the browser in this step.** This is NON-NEGOTIABLE and MUST NOT be skipped, deferred, or treated as optional. Generating any page before the browser is open is a SERIOUS VIOLATION - the user needs the real-time preview surface to see pages as they are generated. You MUST actively open the browser yourself using your platform's built-in browser/preview tool (see step 3 below for the fallback strategy). Do NOT just output a URL in chat text and wait for the user to click it — you MUST programmatically open the browser.

> **TIMING — Execute INSIDE a Workflow, NOT immediately after login.** Step 3 is invoked from within Workflow A/B/C (see each workflow's "Start the local server" step), AFTER the app has been created or reused via `gemdesign app create` / `gemdesign app use` and confirmed via `gemdesign app info`. Do NOT start the server right after Step 2 (login) — the server serves pages from the project subdirectory derived from the app (`<projectDir> = {projectName}__{appuuid}`), so the app must exist first. Starting the server before the app exists is a violation.

After Step 1 (CLI installed), Step 2 (Login verified), AND the app is created/reused (inside a Workflow) are all confirmed complete, start the local server for real-time streaming preview.

The local server provides real-time streaming preview of HTML pages as they are being generated. The server is built into the CLI and managed via the `gemdesign server` commands. The server runs on port `4056` by default; if that port is occupied it auto-retries the next available port (up to `4066`).

0. **Ensure htmlWorkdir is configured** (MUST complete before `app create` in a Workflow, and before `server start`):
   > htmlWorkdir is configured in Step 2.5 (persists across sessions). `app create` sync-creates the local project folder under `htmlWorkdir`, and `server start` validates `htmlWorkdir` before launching — if it is not configured, `app create` skips local folder creation (returns a `warning`) and `server start` refuses to start, causing fileWatcher to miss `.html` changes and the canvas to stay blank ("page generated but canvas not showing").
   >
   > If Step 2.5 was skipped (e.g. resuming a session), verify now: `gemdesign server workdir` (no flags) returns `{"success":true,"htmlWorkdir":"<absolute path>"}`. If it returns an empty `htmlWorkdir`, run `gemdesign server workdir --path ./output` before proceeding.

1. **Stop any previously running server** (MANDATORY before every `server start`, CANNOT be skipped):
   > **CRITICAL — 执行 `server start` 之前必须先执行 `server stop` 终止之前启动的服务**，无论应用是新建还是复用都不可跳过。这确保 fileWatcher 绑定到正确的项目目录，避免残留进程干扰新会话。
   >
   > **HARD GATE - 严禁跳过此步**：无论你认为当前是否已有服务在运行，都必须执行 `gemdesign server stop` 命令。禁止以"服务器未运行"、"上一次会话已启动"、"浏览器预览已打开"、"为了节省时间"等任何理由跳过 stop。必须以 `gemdesign server stop` 的实际返回结果作为唯一判定依据。
   >
   > ```bash
   > gemdesign server stop
   > ```
   - 返回 `{"success":true,"message":"本地服务已停止"}` 表示已停止，继续下一步。
   - 返回 `{"success":false,"error":"未发现运行中的本地服务"}` 表示无运行中的服务，忽略此错误继续下一步。
   - **必须等待上述命令返回结果后才能进入第 2 步**。在 stop 命令未返回前，不得执行任何 `server start` 操作。

2. **Start the local server** using the CLI command:
   ```bash
   gemdesign server start
   ```
   > **必须在执行此命令前先完成上一步的 `gemdesign server stop`**，不得在未停止旧服务的情况下直接 start。
   >
   > **HARD GATE - 顺序约束**：`server start` 必须在 `server stop` 命令返回结果（成功或"未发现运行中的本地服务"错误）之后才能执行。严禁以下行为：
   > - 将 `server stop` 与 `server start` 并行执行（例如在同一个并行工具调用批次中）；
   > - 在 `server stop` 命令尚未返回结果时就发起 `server start`；
   > - 先执行 `server start` 再执行 `server stop`；
   > - 因为"觉得没必要 stop"而跳过 stop 直接 start。
   >
   > 正确顺序：执行 `gemdesign server stop` -> 等待命令返回结果 -> 执行 `gemdesign server start`。这是不可逆的串行依赖关系。
   - If the server starts successfully, the command returns JSON: `{"success":true,"port":<port>,"url":"http://localhost:<port>"}`
   - If the server fails to start, the command returns JSON with an error: `{"success":false,"error":"<error message>"}`
   - **On error**: Read the error message carefully. Common errors:
     - `"服务文件不存在"`: The CLI installation is incomplete — reinstall the CLI.
     - `"服务启动失败，进程已退出"`: Possible port conflict or config file error — check `~/.gemdesign/config.json`.
   - Record the `<port>` from the success response for subsequent steps.

3. **Check server status** (optional, for debugging):
   ```bash
   gemdesign server status
   ```
   Returns: `{"success":true,"status":"running","port":<port>,"url":"http://localhost:<port>"}` or `{"success":true,"status":"stopped"}`

4. **Open the preview (MANDATORY — HARD GATE, DO NOT SKIP)**: After the server is confirmed running (the `server start` command returned success), you MUST open the browser and navigate to the service page named **GemDesign设计器** (URL: `http://localhost:<port>` - use the port from the `server start` response).

   > **This step is NON-NEGOTIABLE.** Do NOT proceed to any page generation workflow (Workflow A/B/C) until the browser is open at `http://localhost:<port>`. The server being up is NOT the same as the preview being open - the user must SEE the preview surface in the browser.
   >
   > **DO NOT just output a URL in chat text.** You MUST use a tool to actually open the browser. Outputting something like "服务器启动成功！请在浏览器中打开 http://localhost:4056" is a VIOLATION — the browser must be opened programmatically, not by asking the user to click a link.

   **How to open the browser — use the following methods in priority order:**

   Try the following methods in priority order. Use the FIRST one that is available and succeeds. If a method fails, skip it and try the next:

   | Priority | Method | How to use |
   |----------|--------|------------|
   | 1 | **Your platform's built-in browser/preview tool** | **You MUST check what browser/preview tools are available on your current agent platform and use the most appropriate one.** Different platforms provide different built-in tools — use whichever one your platform offers. Examples of platform-specific tools: Trae provides `OpenPreview` and the `integrated_browser` MCP's `browser_navigate`; Cursor provides its own preview mechanism; other platforms may have equivalent tools. **The key requirement is: you MUST use a tool to programmatically open the browser, not just output a URL in chat.** Navigate to `http://localhost:<port>/` using the tool. |
   | 2 | **OS default browser command** | If no built-in browser/preview tool is available (or it failed), open the default browser via OS command: Windows `start http://localhost:<port>/`, macOS `open http://localhost:<port>/`, Linux `xdg-open http://localhost:<port>/`. |
   | 3 | **Tell the user to open the URL** | If ALL above methods fail or are unavailable, as a **last resort**, clearly tell the user: "请在浏览器中打开 http://localhost:<port>/ 查看设计器预览" and wait for the user to confirm before proceeding. |

   **How to find your platform's built-in tool:** Check your available tools list — look for tools with names like `OpenPreview`, `browser_navigate`, `preview`, `browser`, or similar. Any tool that can open a URL in a browser panel qualifies. Use it with the URL `http://localhost:<port>/`.

   **Ensuring success:**
   - If the highest-priority method returned an error or you're unsure whether it succeeded, immediately fall back to the next method in the table.
   - After opening the browser, verify the server is still accessible by re-checking the debug endpoint (`http://localhost:<port>/api/local/stream/debug` returns 200).
   - Only proceed to page generation after you have made a best-effort attempt to open the browser using at least one available method.
   >
   > After the preview is open, you may proceed to page generation workflows.

   > **CRITICAL - The browser is opened EXACTLY ONCE, only here in Step 3.** Once the browser is open at `http://localhost:<port>` (the designer SPA root), you MUST NEVER open the browser again — not during page generation (Workflows A/B/C), not during modification flows, not to "refresh" or "show" a generated page. The designer SPA stays open for the entire session; generated HTML is loaded into an iframe INSIDE the designer via SSE (see "Streaming Write Workflow"), NOT by navigating the browser to a new URL.
   >
   > Opening the browser again will navigate it away from the designer to whatever URL you passed — this OVERWRITES the designer with the generated HTML (or a 404), destroying the preview surface the user needs. The URL used to open the browser MUST ALWAYS be the designer root URL `http://localhost:<port>/` — NEVER a path to a generated `.html` file (e.g. `http://localhost:<port>/output/<projectDir>/<pageuuid>.html`), NEVER a page-specific URL. Generated pages have no direct browser URL; they are only viewable through the designer's iframe via SSE.

## CLI Command Reference

### Server Management
```bash
gemdesign server start [--port <port>]   # 启动本地设计器服务（默认端口 4056）
gemdesign server stop                    # 停止本地设计器服务
gemdesign server status                  # 查看服务运行状态
gemdesign server workdir --path <path>   # 保存 HTML 工作目录（htmlWorkdir，相对路径基于当前目录解析为绝对路径）
gemdesign server workdir                 # 查看当前 htmlWorkdir
gemdesign server workdir --clear         # 清除 htmlWorkdir 配置
gemdesign server cleanup                 # 清理空项目目录和遗留的流式文件
```
> **server workdir** 保存 HTML 工作目录到 `~/.gemdesign/config.json` 的 `htmlWorkdir` 字段。本地服务启动后通过 fileWatcher 监听此目录下的 `.html` 文件变更，并经 SSE 推送到浏览器画布。**`app create` 会在此目录下同步创建项目子目录 `{projectName}__{appuuid}`**，**`server start` 也会在启动前校验 htmlWorkdir 是否已配置**--未配置时 `app create` 跳过本地目录创建（返回 `warning`），`server start` 拒绝启动并返回错误提示，避免后台进程 cwd 与实际 HTML 生成目录不一致导致"页面生成但画布不显示"。建议在登录后、**`app create` 之前**执行一次 `gemdesign server workdir --path ./output`（路径通常是 `./output`，即页面 HTML 的根目录）。配置一次后持久化，后续无需重复设置。
> **server start** 以后台进程方式启动本地服务。**执行 `server start` 之前必须先执行 `server stop` 终止之前的服务**，不得在未停止旧服务的情况下直接 start。**`server stop` 严禁跳过**（即使你认为没有运行中的服务也必须执行该命令），且 **`server start` 必须等 `server stop` 命令返回结果后才能执行**——禁止将两者并行执行、或在 stop 未返回时就发起 start。启动成功返回含 `port` 和 `url` 的 JSON；失败返回含 `error` 的 JSON，需仔细阅读错误信息诊断并修复后再重试（重试前同样要先 stop）。
> **server stop** stops the running server. On Windows, uses `taskkill` to terminate the process tree. Returns error if no server is running or if the process cannot be terminated — 此时该错误可忽略（表示本就无运行中的服务），但仍视为 stop 步骤已执行完成，可继续 start。
> **server status** returns the current status (`running` or `stopped`), port, and URL if running.

### Authentication
```bash
gemdesign auth login --token <token>   # 配置 GemDesign 令牌
gemdesign auth whoami                  # Verify identity
```

### App Management
```bash
gemdesign app create --name "MyApp" --workdir <path> [--type web|app] [--width <px>] [--height <px>]    # Create new app (sync-creates local project folder under --workdir), --type defaults to web
gemdesign app list                     # List all apps
gemdesign app info [--appuuid <id>]    # App details
gemdesign app use --appuuid <id> --workdir <path>       # Switch current default app (creates/locates local project folder under --workdir)
```
> **app create 画布尺寸**: `--width`/`--height` 用于指定画布像素尺寸。不传时按 `--type` 取默认值：`web` -> 1920×1080，`app` -> 440×956。传入的尺寸会随应用信息同步到本地设计器画布（覆盖默认值）。示例：`gemdesign app create --name "PadApp" --type app --width 768 --height 1024`。
> **CRITICAL - `app create` and `app use` require `--workdir`**: `app create` 和 `app use` 的 `--workdir <path>` 是**必填**参数，指定本地项目子目录 `{projectName}__{appuuid}` 的父目录。路径由 agent 显式给出，CLI 不再通过配置自动猜测。`--workdir` 会自动追加到 `htmlWorkdir` 配置数组（去重），local-server 据此扫描所有项目目录。建议传入 `./output`（即 `gemdesign server workdir --path ./output` 配置的同一目录）。`page create` 的 `--file <path>` 同理：lock 文件直接写入 `--file` 推导出的项目子目录，保证 lock 与 html 同目录。
> **appuuid priority**: `--appuuid` flag > `defaultAppUuid` (set by `app create`/`app use`) > `GEMDESIGN_APPUUID` env
> Once you run `app create` or `app use`, subsequent `page` commands don't need `--appuuid`.
> **IMPORTANT**: Always check `gemdesign app list` BEFORE creating a new app. Reuse existing apps to keep all pages in the same project folder. Only create a new app when the user explicitly asks for one.
> **CRITICAL - Never create duplicate apps**: Never call `gemdesign app create` more than once in a single session/task. If you have already run `app create` in this session, you MUST NOT run it again — even if a later workflow step or retry seems to require app setup. Instead, reuse the existing app by running `gemdesign app list` to find it, then `gemdesign app use --appuuid <id> --workdir ./output`. Creating a second app leaves the first one empty and orphaned on the platform.
> **CRITICAL - Session lock error handling**: The CLI now automatically verifies session locks via appuuid. If `app create` returns `stage: "appCreateSession"` (session lock exists and the app still exists on remote), do NOT retry with `--force`. Instead: (1) Run `gemdesign app use --appuuid <existingApp.appuuid> --workdir ./output` to reuse the app. (2) If the existing app is from a different completed task, run `gemdesign app end-session`, then `app create` (without `--force`). (3) Only use `--force` if you have verified via `app list` that the session-lock app was deleted from the remote — note that the CLI now auto-cleans stale session locks (app deleted from remote), so `--force` should rarely be needed. (4) If `app create` returns `stage: "appCreateSessionVerify"` (unable to verify app existence due to network error), wait and retry — do NOT use `--force`.
> **CRITICAL - Restart the server around every `app create` or `app use`**: 正确顺序为：`gemdesign server stop` -> (等待 stop 命令返回结果) -> (确保 `htmlWorkdir` 已配置) -> `gemdesign app create` / `gemdesign app use` -> `gemdesign server start`。该顺序由 workflow 步骤强制执行，不要作为独立序列重复执行。**执行 `server start` 之前必须先执行 `server stop` 终止之前的服务**，无论应用是新建还是复用，否则旧服务的 fileWatcher 仍绑定在前一个 app 的 `<projectDir>`，新页面不会推送到画布。**`server stop` 这一步严禁跳过**（即使你认为没有运行中的服务也必须执行），且 **`server start` 必须等 `server stop` 命令返回结果后才能执行**，禁止并行执行或先 start 后 stop。
> **IMPORTANT - Output app info to user**: After selecting/switching/creating an app (i.e., after any `app create`, `app use`, or `app info` call that establishes the working app), you MUST clearly tell the user in your text response which app is now the active target for page generation. At minimum, output the **app name** and **appuuid** (and ideally the computed `<projectDir>`). This ensures the user always knows which app pages will be generated/modified in, and can interrupt if the wrong app was picked. See the "Output current app info to user" step in each workflow for the exact format.
> **CRITICAL - App type determines page type**: Apps have a type - `web` (桌面端) or `app` (移动端) - returned by `app info` as the `pageScene` field. **When generating new pages, the page type MUST match the app type**: a `web` app can only contain `web` pages (desktop layout, wide screen), and an `app` app can only contain `app` pages (mobile layout, narrow screen). Before generating any HTML, check the app's `pageScene` from `app info` and design the page accordingly. Do NOT generate a desktop-width page for an `app` type app, or a mobile-width page for a `web` type app.

### Style Search (optional helper)
```bash
gemdesign style search --keywords "科技,深蓝,企业" --limit 5   # Search styles
gemdesign style get --id <styleId> --format html                 # Get full style
```
> Style search is optional. You can also design styles yourself or use other UI design skills.

### Page - View
```bash
gemdesign page list [--appuuid <id>]                                        # List pages
gemdesign page get --pageuuid <id> --file ./output/<projectDir>/<subfolder>/<id>.html  # Get page HTML (auto-creates projectDir)
gemdesign page doc get --pageuuid <id> --file ./output/<projectDir>/<subfolder>/<id>.md  # Get requirement doc
```

> **CRITICAL - 同步远程页面时必须保留文件夹结构**：`page list` 返回的每个页面包含 `dirName` 字段（远程所在文件夹，多级用 / 分隔，根级页面为 null/空）。将远程页面同步到本地（尤其是"同步后编辑"场景）时，`page get --file` 的 `<subfolder>` **必须与该页面的 `dirName` 一致**，即落盘到 `./output/<projectDir>/<dirName>/<pageuuid>.html`。严禁将所有页面统一放到项目根目录——否则后续编辑保存时本地推导的目录与远程不一致，可能导致页面脱离远程文件夹。例：`page list` 返回页面 `report-sales` 的 `dirName` 为 `reports`，则必须执行 `gemdesign page get --pageuuid report-sales --file ./output/<projectDir>/reports/report-sales.html`。

### Page - Create (streaming mode)
```bash
gemdesign page create --pageuuid <readable-id> --name "<pageName>" --file ./output/<projectDir>/<subfolder>/<readable-id>.html   # Create page + enter streaming mode (.stream.lock written next to --file)
```
> `page create` signals the local server to start streaming mode for this page, enabling real-time HTML preview as you write to the `.html` file. This command should be called BEFORE writing the HTML file, and the streaming mode is automatically ended when `page save` completes.
>
> **【CRITICAL - HTML 文件名必须等于 pageuuid】** `--file` 中的文件名部分必须与 `--pageuuid` 完全一致。例如 `--pageuuid customers-list` 必须搭配 `--file .../customers-list.html`。local-server 的 fileWatcher、streamPoller、pageCache 全部基于“文件名 = pageUuid”的假设工作。不一致会导致：lock 文件与 HTML 文件脱钩、前端流式状态异常、.meta.json 与远程 pageuuid 不匹配。`page create` 响应会在检测到不一致时发出 WARNING，务必按建议修正路径。

### Page - Save (with validation)
```bash
gemdesign page save --pageuuid <id> --file ./output/<projectDir>/<subfolder>/<id>.html                                         # Update existing
gemdesign page save --new --pageuuid <readable-id> --name "Login" --file ./output/<projectDir>/<subfolder>/<readable-id>.html  # Create new
gemdesign page doc save --pageuuid <id> --file ./output/<projectDir>/<subfolder>/doc.md                                                           # Save requirement doc
```
> `page save` automatically validates the HTML against the GemDesign Page Spec before uploading. After a successful save, it automatically ends streaming mode, triggering the browser to fetch the final render.
> `page doc save` saves an agent-generated requirement document to the platform.
> **`--pageuuid` for `--new`**: Use a human-readable id (e.g. filename without `.html`). Ensure uniqueness within the app. This id is used directly as `data-uuid` in navigation elements - no need to change them after saving.
> **Project subdirectory**: Always use `./output/<projectDir>/` in paths. The CLI is idempotent - if the path already contains `<projectDir>`, it won't duplicate it. See "Local File Management" for details.
> **Folder organization**: Include the folder path directly in `--file` (e.g. `--file ./output/<projectDir>/crm/客户管理/page.html`). The CLI automatically derives the remote `dirName` from the file path.

### Validate Only
```bash
gemdesign validate --file ./output/<projectDir>/<subfolder>/page.html    # Validate without saving
```

### Local File Management

For every page, save HTML files locally under `./output/`, organized by project subdirectory:

| File | Purpose | How to generate |
|------|---------|-----------------|
| `./output/<projectDir>/<subfolder>/<pageuuid>.html` | **Page HTML** (contains DSL, for editing and saving) | Written by the agent **only after `page create` has created the `.stream.lock`** (direct creation without the lock is FORBIDDEN; can include multi-level folder path in `<subfolder>`) |
| `./output/<projectDir>/<subfolder>/<pageuuid>.meta.json` | **Page position metadata** (stores `{ position: { x, y } }` for canvas layout) | **CLI-managed exclusively** — auto-generated by `page get`; used by `page save` to read position. The agent MUST NEVER create or modify this file manually. Located in the **same directory** as the HTML file. |

> **`.meta.json` follows the HTML file's directory**: The `.meta.json` file is always generated in the same directory as its corresponding `.html` file, regardless of folder depth. For example:
> - `--file ./output/<projectDir>/page.html` → meta.json at `./output/<projectDir>/page.meta.json`
> - `--file ./output/<projectDir>/crm/page.html` → meta.json at `./output/<projectDir>/crm/page.meta.json`
> - `--file ./output/<projectDir>/crm/客户管理/page.html` → meta.json at `./output/<projectDir>/crm/客户管理/page.meta.json`
>
> You MUST NOT manually create or modify `.meta.json` files — the CLI manages them exclusively (`page get` generates them, `page save` reads them). When `page save` is called, it reads the position from the `.meta.json` in the same directory as the HTML file (falling back to `--x`/`--y` flags if no meta.json exists).

> **Directory consistency check (automatic)**: Before `page get` or `page save` writes any files, the CLI automatically scans the project directory to check if a same-name `.html` file already exists in a DIFFERENT directory than where `--file` points to. If a mismatch is detected (e.g., HTML exists in `customers/` but `--file` points to root), the CLI returns an error with a `suggestedFilePath` — **you MUST use the suggested path to re-execute the command**. This check runs BEFORE any file writes to prevent dirty data. If you receive this error, do NOT ignore it — re-run the command with the exact `suggestedFilePath` from the error response.

> **Project subdirectory naming**: `<projectDir> = {projectName}__{appuuid}`
> - `projectName` comes from `app info` (illegal filesystem chars `\/:*?"<>|` removed, whitespace collapsed to `_`)
> - Empty `projectName` falls back to `默认项目`; empty `appuuid` falls back to `local`
> - Examples: `CRM系统__abc-123`, `电商App__9f3e`, `默认项目__local`
> - **Directory creation**: This subdirectory is sync-created by `app create` under `htmlWorkdir` (requires `htmlWorkdir` configured first via `server workdir`); `page get`/`page save` also create it idempotently when writing files.
>
> **How to write files**:
> - **Always use `./output/<projectDir>/<subfolder>/<pageuuid>.html`** in all file paths, whether writing files directly or passing to CLI commands. Include folder path in `<subfolder>` if needed (e.g. `./output/<projectDir>/crm/客户管理/page.html`). **HTML 文件名必须等于 pageuuid**（如 `--pageuuid customers-list` → 文件名必须是 `customers-list.html`，不能用 `list.html`）。
> - The CLI is **idempotent**: if the path already contains `<projectDir>`, it will NOT duplicate it. You can safely pass `./output/CRM系统__abc-123/home.html` to `page get --file` or `page save --file` without worrying about nesting.
> - **Compute `<projectDir>` first**: Run `gemdesign app info` -> get `{appuuid}` and `{projectName}` -> compute `<projectDir> = {projectName}__{appuuid}` (sanitize projectName).
> - **Validate `<projectDir>` before creating files**: Ensure `<projectDir>` is non-empty and matches `{nonEmptyName}__{nonEmptyUuid}`. If `projectName` or `appuuid` is empty/undefined, re-run `gemdesign app info`. Never create files with an empty or partial `<projectDir>` (e.g. `__abc` or `MyApp__`) - this creates orphaned unnamed directories.
>
> The local server automatically serves pages from the project subdirectory path.

### Page Folder Organization

Pages can be organized into sub-folders within the project directory. Simply include the folder path in `--file`:

- **Root-level pages**: `--file ./output/<projectDir>/page.html` → placed in project root
- **Sub-folder pages**: `--file ./output/<projectDir>/crm/page.html` → placed in `crm` sub-folder
- **Multi-level folders**: `--file ./output/<projectDir>/crm/客户管理/page.html` → nested directory structure

```bash
# Single-level folder
gemdesign page create --pageuuid customer-list --name "客户列表" --file ./output/<projectDir>/crm/customer-list.html
gemdesign page save --new --pageuuid customer-list --name "客户列表" --file ./output/<projectDir>/crm/customer-list.html

# Multi-level folder
gemdesign page create --pageuuid customer-detail --name "客户详情" --file ./output/<projectDir>/crm/客户管理/customer-detail.html
gemdesign page save --new --pageuuid customer-detail --name "客户详情" --file ./output/<projectDir>/crm/客户管理/customer-detail.html
```

> **When to use folders**: Use folders when the user describes organizing pages into modules/categories. For example, if the user says "put the customer pages under crm/客户", use `--file ./output/<projectDir>/crm/客户/page.html`.
> **Folder names**: Illegal filesystem characters (`\/:*?"<>|`) are automatically cleaned. Folder names should be descriptive and human-readable.
> **Local server**: The local server automatically recursively scans all sub-folders and displays them in a tree structure in the designer.
> **Remote sync**: When `page save` is called, the CLI automatically derives the folder path from `--file` and sends it to the remote server as `dirName`. You do NOT need to specify any extra parameter — the CLI handles this transparently.

## Streaming Write Workflow (Real-time Display)

When generating HTML pages, use the **streaming write workflow** to enable real-time display in the browser. The GemDesign local server watches for file changes and pushes incremental content to the browser via Server-Sent Events (SSE).

> **CRITICAL — Do NOT open the browser again during streaming write (or at any point after Step 3).** The designer SPA (already open in the browser from Step 3) watches for `.html` file changes and auto-loads the generated HTML into its inner iframe via SSE. You do NOT need to "open" or "refresh" anything — just write the files and the designer updates itself in real time. Navigating the browser to the generated `.html` URL (e.g. via a preview tool or OS browser command with a page-specific URL) will OVERWRITE the designer with the generated HTML and break the preview surface. The only valid URL for opening the browser is the designer root `http://localhost:<port>/`, and even that should NOT be re-used after Step 3.

> **HARD GATE — 本地文件生成后必须调用 `page save` 命令**：写入 HTML 文件后，**必须**调用 `gemdesign page save` 命令将页面保存到远程服务器。**严禁**只写入本地文件而跳过 `page save`——这会导致页面只存在于本地但不会出现在平台上，用户无法看到或使用该页面。完整流程为：`page create` → 写入 HTML → `page save`。`page save` 内置了规范验证，验证失败会返回错误，修复后重新执行 `page save` 即可。只写入本地文件而不调用 `page save` 是严重违规。

> **注意：`page create` 的 JSON 响应中包含 `warning` 和 `requiredNextSteps` 字段，明确列出后续必须执行的步骤。你在收到该响应后，必须按照 `requiredNextSteps` 中的步骤依次执行，不可在写入 HTML 后停止。**

> **HARD GATE — 严禁直接创建 `.html` 和 `.meta.json` 文件**：不允许智能体使用文件工具（Write/Edit 等）直接创建 `.html` 或 `.meta.json` 文件——这两类文件的创建**必须由 CLI 命令驱动**：
> - **新建页面**：必须先执行 `gemdesign page create`（它会在 `--file` 同目录创建 `.stream.lock` 并进入流式模式），之后才允许写入 HTML。**没有 lock 就写入 HTML 文件是严重违规**——local-server 无法进入流式模式，实时预览失效，兜底保存也无法识别该页面尚未保存。
> - **修改已有页面**：必须先执行 `gemdesign page get` 拉取 HTML（由 CLI 生成 `.html` 和 `.meta.json`），之后才允许修改。
> - **`.meta.json` 为 CLI 专属文件**：由 `page get` 自动生成、由 `page save` 读取，**任何情况下智能体都严禁手动创建或修改 `.meta.json` 文件**。
>
> **自检标准**：在写入任何 `.html` 之前，必须先存在该页面的 `.stream.lock`（新建，由 `page create` 创建）或 `page get` 的输出（修改已有页面）。违反该顺序（先写文件、后补命令，或完全跳过命令）都是严重违规。

### How It Works

The CLI automatically manages the streaming lifecycle for you. The `gemdesign page create` command starts streaming mode, and `gemdesign page save` automatically ends it. The browser receives incremental HTML as you append to the `.html` file:

1. **`gemdesign page create`** → browser enters streaming mode for that page
2. **Append to `.html`** → browser receives incremental HTML and re-renders in real-time
3. **`gemdesign page save`** → browser fetches the complete HTML and switches to final render

### Steps

For each page you generate, follow this workflow. The workflow has **3 required steps** — `page create`, write HTML, and `page save`. You MUST complete all 3 steps for every page. **Stopping after writing HTML is a SERIOUS VIOLATION — the page will NOT appear on the platform.**

1. **Compute path**:
   - `htmlPath = ./output/<projectDir>/<subfolder>/<pageuuid>.html` (include folder path in `<subfolder>`, or omit `<subfolder>` for root-level pages)

2. **Create the page (enter streaming mode)**:
   ```bash
   gemdesign page create --pageuuid <pageuuid> --name "<pageName>" --file ./output/<projectDir>/<subfolder>/<pageuuid>.html
   ```
   This signals the local server to start streaming mode for this page. The `.stream.lock` is written next to `--file`, so the lock and HTML share the same directory. The browser will enter streaming mode and prepare to receive incremental HTML.
   > **The response contains `requiredNextSteps` — you MUST follow them.** After calling `page create`, you MUST write the HTML file and then call `page save`. Do NOT stop after writing HTML.

3. **Write the HTML file** (append-only after the first write, NEVER overwrite with shorter content):
   - **Precondition**: step 2's `page create` MUST have succeeded (the `.stream.lock` exists next to `--file`). NEVER create/write the HTML file without the lock — see the "严禁直接创建 `.html` 和 `.meta.json` 文件" HARD GATE above.
   - You may write the HTML in one shot or in multiple appends — the local server detects file changes and pushes each append to the browser in real-time.
   - The HTML must be a complete document: `<!DOCTYPE html>` + `<head>` (with all dependencies and styles) + `<body>...</body>` + `</html>`.
   - If writing in multiple appends, ensure the first write includes the `<body>` tag so the browser can start rendering immediately (the browser only renders after `<body>` appears).

   > **CRITICAL RULES**:
   > - Always **append** to the file after the first write. Never overwrite with shorter content during streaming — this triggers a `pageReset` event and forces the browser to re-render from scratch.
   > - If you must rewrite from scratch, delete the `.html` file first, then start over.
   > - The first write creates the file (length goes from 0 to N), subsequent writes append (length goes from N to N+M).
   > - **No delays or chunk-size limits**: Write as fast as you like, in any size. The local server pushes every file change to the browser within ~10ms.
   > - **Clean up on failure**: If streaming write fails or is interrupted, delete any partial `.html` file for that page. You can also run `gemdesign server cleanup` to clean up orphaned files and empty project directories.

4. **(Optional) Validate the HTML** — only if you want early error detection before saving:
   ```bash
   gemdesign validate --file ./output/<projectDir>/<subfolder>/<pageuuid>.html
   ```
   If validation fails, fix the HTML and re-validate. Note: `page save` also validates internally — if validation fails during save, fix the HTML and re-run `page save`.

5. **Save to platform (MANDATORY — MUST call after writing HTML)**:
   ```bash
   gemdesign page save --new --pageuuid <pageuuid> --name "<pageName>" --file ./output/<projectDir>/<subfolder>/<pageuuid>.html
   ```
   `page save` **automatically validates the HTML before saving** — if validation fails, it returns an error; fix the HTML and re-run `page save`. When the save completes, the CLI automatically ends streaming mode. The browser fetches the complete HTML and switches to the final render.
   > **This step is NON-NEGOTIABLE.** Writing HTML locally without calling `page save` means the page exists ONLY on your local machine and will NOT appear on the platform. The user will NOT see the page. This is the most common and serious mistake — do NOT make it.
   >
   > **CRITICAL — Call IMMEDIATELY after the page's HTML write completes; NEVER defer or batch**: The moment one page's HTML is fully written, you MUST call that page's `page save` right away — do NOT delay it until other pages are generated. `page save` is the ONLY action that deletes the `.stream.lock`, ends streaming mode, and syncs the page to the remote server. Deferring the save leaves the lock in place: the page stays stuck in streaming state, is never synced to the platform, and the browser canvas never triggers its final render. When generating multiple pages, see the "批量生成：逐页立即保存" HARD GATE below.

> **HARD GATE — 批量生成时每页写完必须立即保存（允许并行，严禁攒批）**：生成多个页面时，可以并行推进多个页面的生成，但**每个页面的 HTML 一写完，就必须立即执行该页对应的后续命令**（`page save`，或先 `validate` 再 `page save`），确认 save 返回成功后该页才算完成。正确示例：`create(p1)` → 写 p1 → **立即** `save(p1)`；`create(p2)` → 写 p2 → **立即** `save(p2)`——各页之间互不等待。
>
> **严禁**把所有页面的 `page save` 攒到最后统一执行（即等全部页面 HTML 都写完后再批量 `save(p1)…save(pN)` 是严重违规）。攒批保存的后果：每个页面的 `.stream.lock` 迟迟不被删除，页面一直处于流式状态、不同步到远程服务器，浏览器画布无法切换到最终渲染，用户体验为"所有页面都在加载中"直到整批结束。
>
> **自检标准**：任何一个页面的 HTML 写完后，该页的下一个执行命令必须是它自己的 `page save`（或先 `validate` 再 `save`）——不得先去写别的页面的 HTML，更不得等到所有页面都写完才统一处理。并行场景下允许同时存在多个已 `create` 的页面，但不允许存在任何"HTML 已写完却迟迟未 save"的页面。

### Example (Streaming Write for a "home" page)

```bash
# Step 1: Create the page (enter streaming mode)
gemdesign page create --pageuuid home --name "首页" --file ./output/MyApp__abc-123/home.html
# → Response includes requiredNextSteps — you MUST follow them

# Step 2: Write the HTML file (one shot or multiple appends)
#    Use Write tool to create ./output/MyApp__abc-123/home.html with the complete HTML

# Step 3 (OPTIONAL): Validate early to catch errors before saving
gemdesign validate --file ./output/MyApp__abc-123/home.html
# If validation fails, fix and re-validate

# Step 4 (MANDATORY): Save to platform — MUST call, otherwise page won't appear
gemdesign page save --new --pageuuid home --name "首页" --file ./output/MyApp__abc-123/home.html
# → page save also validates internally; if validation fails, fix HTML and re-run this command
```

## Workflows

> **PRECONDITION FOR ALL WORKFLOWS**: Step 1 (CLI installed & up-to-date), Step 2 (Login verified via `gemdesign auth whoami`), AND Step 2.5 (htmlWorkdir configured + cleanup) MUST be confirmed complete BEFORE starting any workflow. If login is not confirmed, do NOT generate HTML, do NOT create `./output/` files, do NOT start streaming write - stop and resolve authentication first. Step 3 (local server running AND browser preview opened) is NOT executed before starting a workflow — it is executed INSIDE each workflow, AFTER the app is created/reused (and `app info` confirms `<projectDir>`), and BEFORE any page generation. This applies to Workflow A, B, and C alike.

### Workflow A: Batch Generation from Requirements

1. **Complete Prerequisites**: Ensure Step 1 (CLI install/update), Step 2 (Login), AND Step 2.5 (htmlWorkdir configured + cleanup) are confirmed complete before proceeding. Step 3 (local server + browser preview) is NOT done here — it is executed in step 5 below, AFTER the app is created/reused.
2. **Ensure app exists (reuse first!)**:
   - **Ensure htmlWorkdir is configured**: htmlWorkdir was configured in Step 2.5 (persists across sessions). `app create --workdir` and `app use --workdir` will automatically append the path to htmlWorkdir config (deduplicated). Verify with `gemdesign server workdir` (no flags); if it returns an empty `htmlWorkdir`, you can still pass `--workdir ./output` directly to `app create`/`app use`.
   - Run `gemdesign app list` to check existing apps
   - **If apps already exist**: Run `gemdesign app use --appuuid <id> --workdir ./output` to set the target app as default. Do NOT create a new app unless the user explicitly asks for a new one.
   - **If no apps exist**: Run `gemdesign app create --name "<AppName>" --workdir ./output [--type web|app] [--width <px>] [--height <px>]` to create one (default type is `web`; default canvas size: `web` -> 1920×1080, `app` -> 440×956). `app create` sync-creates the local project folder under `--workdir` (auto-appended to htmlWorkdir config). **After creating, immediately run `gemdesign app info` to confirm the app exists and record its appuuid. Do NOT run `app create` again for any reason in this session.** 之前运行中的服务会在步骤 5 的 `server stop` 中统一终止。
   - **CRITICAL - No duplicate apps**: If you already ran `app create` earlier in this session (even in a previous workflow attempt), do NOT run it again. Reuse the existing app via `app list` + `app use`. Creating a second app leaves the first one empty and orphaned.
   - **CRITICAL - Session lock error handling**: If `app create` returns `stage: "appCreateSession"` (session lock exists and app exists on remote), do NOT retry with `--force`. Instead: (1) Run `app use --appuuid <existingApp.appuuid> --workdir ./output` to reuse. (2) If from a different completed task, run `gemdesign app end-session`, then `app create` (without `--force`). (3) If `stage: "appCreateSessionVerify"` (network error), wait and retry. The CLI auto-cleans stale locks (app deleted from remote), so `--force` is rarely needed.
   - **CRITICAL**: All pages in the same batch MUST go into the same app. Reusing an existing app prevents pages from being scattered across different project folders.
3. **Get project directory name**:
   - Run `gemdesign app info` to get `{appuuid}` and `{projectName}`
   - Compute `<projectDir> = {projectName}__{appuuid}` (remove illegal chars `\/:*?"<>|` from projectName, collapse whitespace to `_`)
   - Example: project name "电商 App" with appuuid "abc-123" → `<projectDir> = "电商_App__abc-123"`
4. **Output current app info to user** (CRITICAL — user must know which app pages will be generated into):
   - Before generating any HTML, clearly tell the user in your text response which app you are generating pages into. At minimum, output:
     - **App name** (`projectName` from `app info`)
     - **App UUID** (`appuuid` from `app info`)
     - **App type** (`pageScene` from `app info` - `web` for 桌面端, `app` for 移动端)
     - **Project directory** (`<projectDir>` computed in step 3)
     - **Page count** to be generated in this batch (from step 7 analysis)
   - Example output format:
     ```
     📦 当前应用信息
     - 应用名称：电商 App
     - 应用 ID：abc-123
     - 应用类型：app（移动端）
     - 项目目录：电商_App__abc-123
     - 本次将生成页面数：5
     ```
   - **Type matching**: The `pageScene` value determines the page layout you MUST follow. Generate `web` (desktop, wide-screen) pages for `web` apps, `app` (mobile, narrow-screen) pages for `app` apps. Do NOT mix types - a web app cannot contain app pages, and vice versa.
   - If the user did not explicitly specify an app and you reused an existing app, also tell the user which app was selected (e.g. "已复用现有应用：电商 App") so they can interrupt if it's the wrong one.
   - **Pause-friendly**: This is informational only - no user reply is required unless the user wants to switch apps. Continue to the next step immediately after outputting.
5. **Start the local server (Step 3)**: Now that the app exists and `<projectDir>` is computed, execute Step 3 (see the "Step 3: Start the Local Server" section above) — **必须先执行 `gemdesign server stop` 终止之前的服务**（无论应用是新建还是复用，也无论之前是否已运行服务，均不可跳过此步），**必须等 `server stop` 命令返回结果（确认已停止或无运行中的服务）之后**，才能执行 `gemdesign server start` 启动本地服务，并仅打开一次浏览器到设计器 `http://localhost:<port>/`。记录 `server start` 返回的 `<port>` 供后续步骤使用。这是 HARD GATE：服务未运行或浏览器预览未打开前，不得进入任何页面生成。
   - **CRITICAL - 严禁跳过 `server stop` 这一步**：即使你认为当前会话中没有运行中的服务，也必须执行 `gemdesign server stop` 命令并以命令返回结果为准。禁止以"服务器已在运行"、"上一次 workflow 已启动"、"浏览器预览已打开"等理由跳过 stop。stop 返回 `{"success":false,"error":"未发现运行中的本地服务"}` 时表示无服务可停，此时可继续下一步 start。
   - **CRITICAL - `server start` 必须等 `server stop` 执行完成后再执行**：禁止将 stop 和 start 并行执行、或先 start 后 stop。`server start` 的前置条件是 `server stop` 已返回结果。
   - Never open the browser with a generated-page URL (e.g. `http://localhost:<port>/output/<projectDir>/<pageuuid>.html`) - that overwrites the designer with the generated HTML and destroys the preview surface.
6. **Search style** (optional): `gemdesign style search --keywords "电商,现代,简洁"` → select one → `gemdesign style get --id <id>`
7. **Analyze requirements**: Read the requirements doc, break down into individual pages. Assign each page a readable `pageuuid` (e.g. `home`, `product-list`, `cart`).
8. **Generate design system page (only for newly created apps)**: If a new app was created in step 2 (not reused), generate a design system page as the visual style baseline before generating business pages. All subsequent business pages should follow this style. Determine the design system type based on `pageScene` from `app info`, and generate the page following the type table and page structure in the dedicated **"Design System Page Spec"** section below. The pageuuid is fixed as `design-system` and is NOT counted as a business page. **You MUST save the design system page to the platform (not just write it locally) - otherwise it will not appear in the app and cannot serve as the style baseline.** Use the **Streaming Write Workflow** with these explicit steps (same create-validate-save process as business pages):
   - Create page (enter streaming mode): `gemdesign page create --pageuuid design-system --name "设计系统" --file ./output/<projectDir>/design-system.html`
   - Write the HTML file to `./output/<projectDir>/design-system.html` (follow the Design System Page Spec; pageuuid is `design-system`)
   - **(Optional)** Validate: `gemdesign validate --file ./output/<projectDir>/design-system.html` (fix errors and re-validate)
   - **Save to platform (MANDATORY - do NOT skip)**: `gemdesign page save --new --pageuuid design-system --name "设计系统" --file ./output/<projectDir>/design-system.html` (uploads the design system page into the app so it persists on the platform and shows up in `page list`; automatically ends streaming mode)
   - Verify it was saved: `gemdesign page list` (confirm `design-system` appears in the list)
   If the app was reused (switched via `app use` in step 2), skip this step AND skip step 9.
9. **Design System Review Gate (CRITICAL — only when step 8 generated a design system page)**: Before generating any business page, you MUST apply the **"Design System Review Gate"** rules (see that section below). Evaluate the continue conditions; if none apply, STOP and ask the user for confirmation/feedback on the design system using the format specified in that section. Do not proceed to step 10 until the design system is confirmed by the user or a continue condition is met. If the app was reused (step 8 was skipped), skip this step too.
10. **For each page** (use **Streaming Write Workflow** above for real-time display):
    - **HARD GATE — 每页写完立即 save，严禁攒批**：生成方式不限（串行或并行均可），但每个页面的 HTML 一写完，就必须立即执行该页的 `page save`（最多先 `validate` 再 `save`），以此删除 `.stream.lock`、结束流式状态并同步远程服务器，确认 save 成功后该页才算完成。**严禁**等所有页面的 HTML 都写完后再统一批量 `page save`（攒批会导致 lock 滞留、页面一直处于流式状态且不同步远程）。详见 Streaming Write Workflow 章节的"批量生成：逐页立即保存"HARD GATE。
    - Generate HTML following the Page Spec below (incorporate style if available). Use the assigned `pageuuid` as `data-uuid` in navigation elements. All business pages MUST follow the style baseline established (and, if applicable, confirmed) in the design system page.
    - **Use streaming write** (3 required steps: create → write HTML → save, per page in sequence):
      - `gemdesign page create --pageuuid <pageuuid> --name "页面名" --file ./output/<projectDir>/<subfolder>/<pageuuid>.html`
      - Write the HTML file to the `--file` path (include folder in path if needed; create the directory if it doesn't exist)
      - **(Optional)** `gemdesign validate --file ...` for early error detection
      - **`gemdesign page save --new --pageuuid <pageuuid> --name "页面名" --file ./output/<projectDir>/<subfolder>/<pageuuid>.html`** — MANDATORY, page won't appear on platform without this step; call it IMMEDIATELY after this page's HTML is written, BEFORE touching the next page
    - **CRITICAL**: `page save` is the most important step. Only writing HTML locally without calling `page save` means the page will NOT appear on the platform. `page save` validates internally — if validation fails, fix and re-run.
11. **Verify**: `gemdesign page list`
12. **Output designer link (MANDATORY - output ONCE, only after ALL pages are generated)**: After ALL pages in the batch are generated, validated, and saved (i.e., after step 10's loop is fully complete and step 11 verification passes), you MUST output a clickable link in your text response so the user can easily open the designer to view the final result. The link MUST be:
    - **Name**: `gemdesign 设计器` (exact text, do NOT change or translate)
    - **URL**: `http://localhost:<port>` (use the port recorded from Step 3's `server start` response)
    - **Format** (markdown link): `[gemdesign 设计器](http://localhost:<port>)`
    - Example: `[gemdesign 设计器](http://localhost:4056)`
    > **CRITICAL - Do NOT output this link after each individual page in step 10.** Output it exactly ONCE, at the very end of the entire batch, after every page has been generated and saved. Outputting the link after each page clutters the conversation and violates the "all pages complete" requirement.
    >
    > **Note**: This is the ONLY exception to the "do not output URLs in chat text" rule in Step 3. Step 3's rule prohibits outputting a URL *instead of* programmatically opening the browser during setup. This step is different - it runs AFTER all page generation is complete, and outputs a text link for the user to click at their discretion (e.g. if they closed the browser or want to reopen the designer). This is NOT an automatic browser open action - it is a markdown link in your final summary.

### Workflow B: Conversational Generation

When user asks for a page in conversation:
1. **Complete Prerequisites**: Ensure Step 1 (CLI install/update), Step 2 (Login), AND Step 2.5 (htmlWorkdir configured + cleanup) are confirmed complete before proceeding. Step 3 (local server + browser preview) is NOT done here — it is executed in step 5 below, AFTER the app is created/reused.
2. **Ensure app exists (reuse first!)**:
   - **Ensure htmlWorkdir is configured**: htmlWorkdir was configured in Step 2.5 (persists across sessions). `app create --workdir` and `app use --workdir` will automatically append the path to htmlWorkdir config (deduplicated). Verify with `gemdesign server workdir` (no flags); if it returns an empty `htmlWorkdir`, you can still pass `--workdir ./output` directly to `app create`/`app use`.
   - Run `gemdesign app list` to check existing apps
   - **If apps already exist**: Run `gemdesign app use --appuuid <id> --workdir ./output` to set the target app as default. Do NOT create a new app unless the user explicitly asks for a new one.
   - **If no apps exist**: Run `gemdesign app create --name "<AppName>" --workdir ./output [--type web|app] [--width <px>] [--height <px>]` to create one (default type is `web`; default canvas size: `web` -> 1920×1080, `app` -> 440×956). `app create` sync-creates the local project folder under `--workdir` (auto-appended to htmlWorkdir config). **After creating, immediately run `gemdesign app info` to confirm the app exists and record its appuuid. Do NOT run `app create` again for any reason in this session.** 之前运行中的服务会在步骤 5 的 `server stop` 中统一终止。
   - **CRITICAL - No duplicate apps**: If you already ran `app create` earlier in this session (even in a previous workflow attempt), do NOT run it again. Reuse the existing app via `app list` + `app use`. Creating a second app leaves the first one empty and orphaned.
   - **CRITICAL - Session lock error handling**: If `app create` returns `stage: "appCreateSession"` (session lock exists and app exists on remote), do NOT retry with `--force`. Instead: (1) Run `app use --appuuid <existingApp.appuuid> --workdir ./output` to reuse. (2) If from a different completed task, run `gemdesign app end-session`, then `app create` (without `--force`). (3) If `stage: "appCreateSessionVerify"` (network error), wait and retry. The CLI auto-cleans stale locks (app deleted from remote), so `--force` is rarely needed.
   - **CRITICAL**: All pages MUST go into the same app. Reusing an existing app prevents pages from being scattered across different project folders.
3. **Get project directory name**: 
   - Run `gemdesign app info` to get `{appuuid}` and `{projectName}`
   - Compute `<projectDir> = {projectName}__{appuuid}` (remove illegal chars `\/:*?"<>|` from projectName, collapse whitespace to `_`)
4. **Output current app info to user** (CRITICAL — user must know which app the page will be generated into):
   - Before generating any HTML, clearly tell the user in your text response which app you are generating the page into. At minimum, output:
     - **App name** (`projectName` from `app info`)
     - **App UUID** (`appuuid` from `app info`)
     - **App type** (`pageScene` from `app info` - `web` for 桌面端, `app` for 移动端)
     - **Project directory** (`<projectDir>` computed in step 3)
   - Example output format:
     ```
     📦 当前应用信息
     - 应用名称：电商 App
     - 应用 ID：abc-123
     - 应用类型：app（移动端）
     - 项目目录：电商_App__abc-123
     ```
   - **Type matching**: The `pageScene` value determines the page layout you MUST follow. Generate `web` (desktop, wide-screen) pages for `web` apps, `app` (mobile, narrow-screen) pages for `app` apps. Do NOT mix types - a web app cannot contain app pages, and vice versa.
   - If the user did not explicitly specify an app and you reused an existing app, also tell the user which app was selected (e.g. "已复用现有应用：电商 App") so they can interrupt if it's the wrong one.
   - **Pause-friendly**: This is informational only — no user reply is required unless the user wants to switch apps. Continue to the next step immediately after outputting.
5. **Start the local server (Step 3)**: Now that the app exists and `<projectDir>` is computed, execute Step 3 (see the "Step 3: Start the Local Server" section above) — **必须先执行 `gemdesign server stop` 终止之前的服务**（无论应用是新建还是复用，也无论之前是否已运行服务，均不可跳过此步），**必须等 `server stop` 命令返回结果（确认已停止或无运行中的服务）之后**，才能执行 `gemdesign server start` 启动本地服务，并仅打开一次浏览器到设计器 `http://localhost:<port>/`。记录 `server start` 返回的 `<port>` 供后续步骤使用。这是 HARD GATE：服务未运行或浏览器预览未打开前，不得进入任何页面生成。
   - **CRITICAL - 严禁跳过 `server stop` 这一步**：即使你认为当前会话中没有运行中的服务，也必须执行 `gemdesign server stop` 命令并以命令返回结果为准。禁止以"服务器已在运行"、"上一次 workflow 已启动"、"浏览器预览已打开"等理由跳过 stop。stop 返回 `{"success":false,"error":"未发现运行中的本地服务"}` 时表示无服务可停，此时可继续下一步 start。
   - **CRITICAL - `server start` 必须等 `server stop` 执行完成后再执行**：禁止将 stop 和 start 并行执行、或先 start 后 stop。`server start` 的前置条件是 `server stop` 已返回结果。
   - Never open the browser with a generated-page URL (e.g. `http://localhost:<port>/output/<projectDir>/<pageuuid>.html`) - that overwrites the designer with the generated HTML and destroys the preview surface.
6. **Generate design system page (only for newly created apps)**: If a new app was created in step 2 (not reused), generate a design system page as the visual style baseline before generating business pages. All subsequent business pages should follow this style. Determine the design system type based on `pageScene` from `app info`, and generate the page following the type table and page structure in the dedicated **"Design System Page Spec"** section below. The pageuuid is fixed as `design-system` and is NOT counted as a business page. **You MUST save the design system page to the platform (not just write it locally) - otherwise it will not appear in the app and cannot serve as the style baseline.** Use the **Streaming Write Workflow** with these explicit steps (same create-validate-save process as business pages):
   - Create page (enter streaming mode): `gemdesign page create --pageuuid design-system --name "设计系统" --file ./output/<projectDir>/design-system.html`
   - Write the HTML file to `./output/<projectDir>/design-system.html` (follow the Design System Page Spec; pageuuid is `design-system`)
   - **(Optional)** Validate: `gemdesign validate --file ./output/<projectDir>/design-system.html` (fix errors and re-validate)
   - **Save to platform (MANDATORY - do NOT skip)**: `gemdesign page save --new --pageuuid design-system --name "设计系统" --file ./output/<projectDir>/design-system.html` (uploads the design system page into the app so it persists on the platform and shows up in `page list`; automatically ends streaming mode)
   - Verify it was saved: `gemdesign page list` (confirm `design-system` appears in the list)
   If the app was reused (switched via `app use` in step 2), skip this step AND skip step 7.
7. **Design System Review Gate (CRITICAL — only when step 6 generated a design system page)**: Apply the **"Design System Review Gate"** rules (see that section below). If no continue condition applies, STOP and ask the user for confirmation/feedback before proceeding. Do not proceed to step 8 until the design system is confirmed or a continue condition is met. If the app was reused (step 6 was skipped), skip this step too.
8. Determine a readable `pageuuid` (e.g. filename without `.html`, unique within the app)
9. Generate HTML following the Page Spec, using `pageuuid` as `data-uuid` in navigation elements. Follow the style baseline established (and, if applicable, confirmed) in the design system page.
10. **Use streaming write** (3 required steps: create → write HTML → save):
    - `gemdesign page create --pageuuid <pageuuid> --name "<pageName>" --file ./output/<projectDir>/<subfolder>/<pageuuid>.html`
    - Write the HTML file to the `--file` path (include folder in path if needed; create the directory if it doesn't exist)
    - **(Optional)** `gemdesign validate --file ...` for early error detection
    - **`gemdesign page save --new --pageuuid <pageuuid> --name "<pageName>" --file ./output/<projectDir>/<subfolder>/<pageuuid>.html`** — MANDATORY, page won't appear on platform without this step
    - **CRITICAL**: Only writing HTML locally without calling `page save` means the page will NOT appear on the platform.
14. Describe the result to the user
15. **Output designer link (MANDATORY - output ONCE, only after ALL page work is complete)**: After the page is generated, validated, and saved, you MUST output a clickable link in your text response so the user can easily open the designer. The link MUST be:
    - **Name**: `gemdesign 设计器` (exact text, do NOT change or translate)
    - **URL**: `http://localhost:<port>` (use the port recorded from Step 3's `server start` response)
    - **Format** (markdown link): `[gemdesign 设计器](http://localhost:<port>)`
    - Example: `[gemdesign 设计器](http://localhost:4056)`
    > **CRITICAL - Output this link exactly ONCE, at the very end of the workflow.** Do NOT output it after each intermediate step. This is a text link for the user to click at their discretion, NOT an automatic browser open action. See Workflow A step 12 for the full rationale on why this does not conflict with Step 3's "do not output URLs in chat" rule.

When user requests modifications:
1. `gemdesign page get --pageuuid <id> --file ./output/<projectDir>/<subfolder>/<id>.html` to retrieve HTML+DSL for editing
2. Modify the HTML (adjust DOM, add/remove interaction DSL, update jsHandle)
   - For substantial modifications, use the **Streaming Write Workflow**: rewrite the HTML (delete the old file first if starting fresh, or append if only adding)
3. **(Optional)** `gemdesign validate --file ./output/<projectDir>/<subfolder>/<id>.html` — fix errors if any
4. `gemdesign page save --pageuuid <id> --file ./output/<projectDir>/<subfolder>/<id>.html` — MANDATORY
5. If requirement doc needs updating: `gemdesign page doc save --pageuuid <id> --file ./output/<projectDir>/<subfolder>/updated-doc.md`

### Workflow C: Modify Existing Page

1. **Complete Prerequisites**: Ensure Step 1 (CLI install/update), Step 2 (Login), AND Step 2.5 (htmlWorkdir configured + cleanup) are confirmed complete before proceeding. Step 3 (local server + browser preview) is NOT done here — it is executed in step 4 below, AFTER `app info` confirms `<projectDir>`.
2. **Get project directory name**: Run `gemdesign app info` → compute `<projectDir> = {projectName}__{appuuid}` (remove illegal chars `\/:*?"<>|` from projectName, collapse whitespace to `_`)
3. **Output current app info to user** (CRITICAL — user must know which app the page being modified belongs to):
   - Before modifying any HTML, clearly tell the user in your text response which app the target page belongs to. At minimum, output:
     - **App name** (`projectName` from `app info`)
     - **App UUID** (`appuuid` from `app info`)
     - **App type** (`pageScene` from `app info` - `web` for 桌面端, `app` for 移动端)
     - **Project directory** (`<projectDir>` computed in step 2)
   - Example output format:
     ```
     📦 当前应用信息
     - 应用名称：电商 App
     - 应用 ID：abc-123
     - 应用类型：app（移动端）
     - 项目目录：电商_App__abc-123
     ```
   - **Type matching**: The `pageScene` value determines the page layout you MUST follow. Generate `web` (desktop, wide-screen) pages for `web` apps, `app` (mobile, narrow-screen) pages for `app` apps. Do NOT mix types - a web app cannot contain app pages, and vice versa.
   - This confirms to the user that the modification will land in the correct app, especially when multiple apps exist. If the user wanted a different app, they can interrupt here to switch via `gemdesign app use`.
   - **Pause-friendly**: This is informational only — no user reply is required unless the user wants to switch apps. Continue to the next step immediately after outputting.
4. **Start the local server (Step 3)**: Now that the app exists and `<projectDir>` is computed, execute Step 3 (see the "Step 3: Start the Local Server" section above) — **必须先执行 `gemdesign server stop` 终止之前的服务**（无论应用是新建还是复用，也无论之前是否已运行服务，均不可跳过此步），**必须等 `server stop` 命令返回结果（确认已停止或无运行中的服务）之后**，才能执行 `gemdesign server start` 启动本地服务，并仅打开一次浏览器到设计器 `http://localhost:<port>/`。记录 `server start` 返回的 `<port>` 供后续步骤使用。这是 HARD GATE：服务未运行或浏览器预览未打开前，不得进入任何页面修改。
   - **CRITICAL - 严禁跳过 `server stop` 这一步**：即使你认为当前会话中没有运行中的服务，也必须执行 `gemdesign server stop` 命令并以命令返回结果为准。禁止以"服务器已在运行"、"上一次 workflow 已启动"、"浏览器预览已打开"等理由跳过 stop。stop 返回 `{"success":false,"error":"未发现运行中的本地服务"}` 时表示无服务可停，此时可继续下一步 start。
   - **CRITICAL - `server start` 必须等 `server stop` 执行完成后再执行**：禁止将 stop 和 start 并行执行、或先 start 后 stop。`server start` 的前置条件是 `server stop` 已返回结果。
   - Never open the browser with a generated-page URL (e.g. `http://localhost:<port>/output/<projectDir>/<pageuuid>.html`) - that overwrites the designer with the generated HTML and destroys the preview surface.
5. `gemdesign page list` -> find the target page
6. `gemdesign page get --pageuuid <id> --file ./output/<projectDir>/<subfolder>/<id>.html` -> retrieve HTML+DSL for editing
7. Analyze HTML structure and interactions
8. Modify HTML as needed
   - For substantial modifications, use the **Streaming Write Workflow** (see above): rewrite the HTML
9. **(Optional) Validate**: `gemdesign validate --file ./output/<projectDir>/<subfolder>/<id>.html` — fix errors if any
10. **Save to platform (MANDATORY)**: `gemdesign page save --pageuuid <id> --file ./output/<projectDir>/<subfolder>/<id>.html`
    - **CRITICAL**: Only modifying local files without calling `page save` means changes will NOT sync to the platform. `page save` validates internally.
12. If requirement doc needs updating: `gemdesign page doc save --pageuuid <id> --file ./output/<projectDir>/<subfolder>/updated-doc.md`
13. **Output designer link (MANDATORY - output ONCE, only after ALL page work is complete)**: After the page is modified, validated, and saved, you MUST output a clickable link in your text response so the user can easily open the designer to view the updated result. The link MUST be:
    - **Name**: `gemdesign 设计器` (exact text, do NOT change or translate)
    - **URL**: `http://localhost:<port>` (use the port recorded from Step 3's `server start` response)
    - **Format** (markdown link): `[gemdesign 设计器](http://localhost:<port>)`
    - Example: `[gemdesign 设计器](http://localhost:4056)`
    > **CRITICAL - Output this link exactly ONCE, at the very end of the workflow.** Do NOT output it after each intermediate step. This is a text link for the user to click at their discretion, NOT an automatic browser open action. See Workflow A step 12 for the full rationale on why this does not conflict with Step 3's "do not output URLs in chat" rule.

---

## Design System Page Spec

When the app is newly created, generate a design system page (with pageuuid fixed as `design-system`) before generating business pages, serving as the visual style baseline for the app. All subsequent business pages should follow the colors, border radii, shadows, and component styles established in this design system. The design system page also follows the GemDesign Page Specification (see below), including tech stack rules, CSS rules, Lite-Interaction DSL, etc.

### Type Determination

Determine the design system type based on the `pageScene` field returned by `app info`:

| pageScene | Design System Type | Core Objective |
|-----------|-------------------|----------------|
| `app` | Mobile C-end experience-driven | Create a consumer-facing, experience-and-emotion-driven mobile app UI design system showcase page. Showcase common interaction patterns and visual components of C-end apps, emphasizing content consumption, social interaction, and personalized experience. The page uses a mobile-width layout directly (no phone frame/外框 wrapper), presenting the mobile app interface as-is. |
| `web` | Enterprise admin function-driven | Create a function-driven, enterprise/admin-management-oriented Web UI design system showcase page. Showcase common framework structures, data operations, and form input components of admin systems, emphasizing information density, operational efficiency, and status feedback. The page uses a full-width admin layout, simulating a real admin management system interface. |
| Other | Flexible analysis | Analyze the most suitable design system type based on requirements, and design flexibly using the Header + Design Tokens + Components basic structure. |

### Page Structure — `app` Type (Mobile C-end)

**Header**

- Include system logo/icon, system name (Chinese), and brief description
- Use dark or brand-color background with white text
- Fixed at top or as a page-top banner

**Section 1: Design Tokens**

- **Section title style**: Use a left-side colored border bar (`border-l-4`, using the style's primary color) + large title + tag badge combination
- **Color system**: Use color swatch cards to display primary, secondary, functional, and neutral colors, with Hex values and usage notes
- **Border radius & shadows**: Use physicalized blocks to display shadow effects at different levels, large radius specs (e.g. 16px/24px), soft shadows or diffuse glow

**Section 2: Components**

- **Media Cards**: Image-text cards (large image mode), masonry/waterfall cards, video/live cover containers
- **Social Elements**: User avatars, like/favorite/comment icons (with micro-interaction styles), follow buttons
- **Interactive Containers**: Bottom sheet panels (Bottom Sheet/Drawer), Toast notifications (shown only as style effect displays within containers — do NOT simulate real popup effects fixed in page layout)
- **Navigation**: Immersive top bar (transparent gradient), bottom navigation bar (icon + text, with selected-state animation hints)
- **Empty/Loading**: Loading placeholders (Skeleton), empty-state illustration placeholders

### Page Structure — `web` Type (Enterprise Admin)

**Header**

- Include system logo/icon, system name (Chinese), and brief description
- Use dark or brand-color background with white text
- Fixed at top or as a page-top banner

**Section 1: Design Tokens**

- **Section title style**: Use a left-side colored border bar (`border-l-4`, using the style's primary color) + large title + tag badge combination
- **Color system**: Use color swatch cards to display primary, secondary, functional, and neutral colors, with Hex values and usage notes
- **Typography hierarchy**: Display H1-H4, Body, and Caption level comparisons within cards, with font/size/weight annotations
- **Border radius & shadows**: Use physicalized blocks to display shadow effects at different levels

**Section 2: Components**

- Use grid layout (`grid-cols-1 lg:grid-cols-2/3`) to organize component displays
- **Structure/Shell**: Sidebar nav items (selected/hover), top breadcrumb, Page Header
- **Data Display**: Data tables (header, zebra striping, row hover, pagination), Tab pages, Tags (Tag/Badge), key-value pair lists
- **Form Elements**: Input boxes (Input), dropdown selects (Select), checkboxes/radio buttons (Checkbox/Radio), switches (Switch) — must include default, Hover, Focus, and Error states
- **Actions**: Action buttons (Primary, Secondary, Ghost, Icon Button)
- **Feedback/Overlays**: Global messages (Message), notifications (Notification), dialogs (Modal/Dialog, shown as example displays — do NOT use full-screen modals), loading states (Skeleton/Spinner)

### Page Structure — Other Types

Follow the Header + Design Tokens + Components basic structure, and determine suitable components and visual style based on requirements analysis.

---

## Design System Review Gate (CRITICAL)

> **When the design system page is generated (newly created apps only), you MUST apply this review gate before generating any business page.** This gate does not apply to reused apps (which skip design system generation) or to Workflow C (modify existing page).

### Why this gate exists (first principles)

The design system page is a **high-leverage decision point**. It locks in the colors, typography, shadows, radii, and component styles that every subsequent business page will inherit. Two properties make the moment right after its generation a natural checkpoint:

1. **Asymmetric error cost.** A wrong style decision made here propagates to every business page generated afterward. Correcting it after N pages exist means reworking N pages; correcting it immediately costs one round-trip with the user. The expected cost of skipping the gate grows linearly with page count, while the cost of pausing is constant and tiny.

2. **Information-state flip.** Before generation, the agent can only *infer* the user's visual preference from the requirements doc — an uncertain state. After generation, the user can *see* a concrete proposal rendered in the browser — a certain state. This is the first moment the user possesses actionable information to confirm or redirect. Capturing that signal here yields maximum value: it is the cheapest point in the whole workflow to correct course.

### Decision rule — stop or continue?

After the design system page is generated, validated, and saved, evaluate the **continue conditions** below. The default is **STOP and ask**; you may only continue without asking if at least one continue condition is clearly met.

**Continue conditions** (any ONE is sufficient to skip the pause and proceed directly to business pages):

| # | Condition | Why it's safe to continue |
|---|-----------|---------------------------|
| C1 | The user explicitly specified the visual style in their original request (e.g. specific brand colors, "深蓝科技风", "参考某App的样式", a mood-board, a hex code) | The style direction is already locked by the user — there is no information gap for the gate to close. |
| C2 | The user ran `style search` + `style get` earlier in this session AND the design system page faithfully reflects that selected style | The user pre-signaled their preference through an explicit selection action; the design system is executing that choice, not proposing a new one. |
| C3 | The user explicitly waived the review (e.g. "不用确认，直接全部生成", "全自动跑完", "不要中途停") | The user has voluntarily forfeited the checkpoint. Respect their stated preference. |

**If NO continue condition applies → you MUST stop.** This is the default and the most common case for a freshly created app driven only by a requirements document.

### When you stop — what to present

Do not merely announce "设计系统已生成". Present a **decision-ready summary** so the user can confirm or redirect with minimal effort:

1. **Style decisions made** — primary/secondary colors (with hex), overall direction (e.g. 科技感/温暖/极简), key component treatments (card radius, shadow style, button style). Be concrete, not vague.
2. **Reasoning link** — connect the decisions back to the requirements (e.g. "基于需求文档中'面向年轻人的社交平台'定位，主色选用高饱和的紫色…").
3. **Explicit ask** — use the `AskUserQuestion` tool to structure the choice. Suggested options:
   - "确认，继续生成业务页面"
   - "调整配色方案"
   - "调整整体风格方向"
   - (the user can also type a custom response via "其他")

### After the user responds

- **User confirms** → proceed to business page generation, treating the confirmed design system as the locked style baseline for all pages.
- **User requests adjustments** -> modify the design system page first (edit -> validate -> save), then either re-present (if the change is major/subjective, e.g. a pivot from "科技蓝" to "温暖橙") or proceed (if the change is minor and clearly resolved, e.g. a single hex value tweak). Use judgment here. The "save" step here means re-running `gemdesign page save --pageuuid design-system --file ./output/<projectDir>/design-system.html` (NO `--new` flag - the page already exists on the platform from step 7/5; `--new` would error on duplicate pageuuid). Confirm the update with `gemdesign page list`.
- **Never start business pages** until the design system is either (a) confirmed by the user or (b) covered by a continue condition above.

---

## GemDesign Page Specification

You MUST follow this spec when generating HTML. The `gemdesign validate` command checks all these rules.

### Overview

A GemDesign page = **HTML(DOM) + TailwindCSS(style) + Lite-Interaction DSL(interaction)**.

### Tech Stack Rules

**Allowed**: HTML native tags, TailwindCSS (via `<script>` tag), CSS (`<style>`), Font Awesome, ECharts
**Forbidden**: Any JS framework (Vue/React/jQuery), hand-written DOM JS (except jsHandle), CSS Hack, `vh` unit

### Only Two Types of Scripts Allowed

1. `<script id="interaction-data">` — Lite-Interaction JSON string (interaction logic)
2. `<script id="funcName">function funcName(event){...}</script>` — jsHandle custom function

### Dependencies

```html
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<!-- ECharts (only when using charts): -->
<script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js"></script>
<!-- ECharts China map (only when using china map): -->
<script src="https://cdn.jsdmirror.com/npm/echarts/map/js/china.js"></script>
```

### Layout Rules

1. Use TailwindCSS for layout component classes.
2. Prefer flexbox layout; Flexbox, padding, and gap are the core tools for interface layout.
3. Block elements can be used for simple elements (text, decorative images), but NOT for layout. All elements default to the `border-box` box model.
4. Fixed elements (sidebars, nav bars) must have explicit height/width; content area needs matching padding.
5. Masks and modals/drawers must be nested. The mask/overlay layer MUST have a semi-transparent background color (e.g. `bg-black/50`), and the inner modal/drawer content container MUST have an opaque background color (e.g. `bg-white`) - a transparent content container is a SERIOUS VIOLATION, as it lets the mask color bleed through.
6. When centering elements, absolutely do NOT use `mx-auto` or `m-auto` - you MUST use flex layout's `justify-center` and `items-center` on the parent element.

### CSS Rules

#### Rule 1: No `vh` unit

Forbidden: the `vh` unit, any Tailwind CSS class containing `vh`, and any class containing `vh` (e.g. `h-[80vh]`).

#### Rule 2: HIGHEST-LEVEL RED LINE - ABSOLUTELY NO Margin

The entire page is ABSOLUTELY FORBIDDEN from using ANY margin! This includes native CSS and ALL Tailwind class names with margin semantics! The model is highly prone to habitually using margin for "icon spacing" and "element top/bottom spacing" - you MUST overcome this habit!

If your output code contains ANY of the following prefixes (positive OR negative), it is a SERIOUS VIOLATION:

- `m-` (e.g. `m-2`, `m-auto`)
- `mt-` (e.g. `mt-4`)
- `mb-` (e.g. `mb-3`, `mb-4`, `mb-6`)
- `ml-` (e.g. `ml-2`)
- `mr-` (e.g. `mr-1`, `mr-2`)
- `mx-` (e.g. `mx-auto`)
- `my-` (e.g. `my-4`)
- `space-x-` / `space-y-` (the underlying implementation is also margin, ABSOLUTELY forbidden)

**Mandatory alternatives - for the scenarios you are most prone to violating**:

- ❌ Violation habit 1 (icon and text spacing): `<i class="fas fa-edit mr-1"></i>编辑`
- ✅ Correct practice 1 (use flex + gap): `<div class="flex items-center gap-1"><i class="fas fa-edit"></i><span>编辑</span></div>`

- ❌ Violation habit 2 (title/paragraph bottom spacing): `<h3 class="mb-4">标题</h3><form>...</form>`
- ✅ Correct practice 2 (parent flex + gap): `<div class="flex flex-col gap-4"><h3>标题</h3><form>...</form></div>`

- ❌ Violation habit 3 (center alignment): `class="mx-auto"` or `class="m-auto"`
- ✅ Correct practice 3 (parent centering): use `flex justify-center items-center` on the parent element

### Lite-Interaction DSL (Core)

All interactions are declared in `<script id="interaction-data">` as a JSON array wrapped in backticks.

```typescript
interface TriggerEvent {
  original: string;        // Selector: #id or .class only
  trigger: 'click' | 'mouseover' | 'mouseenter' | 'mouseleave' | 'mousedown' | 'mouseup';
  actions: Action[];
}

interface Action {
  operation: 'show' | 'hide' | 'openModal' | 'closeModal' | 'addClass' | 'removeClass' | 'openPage' | 'back' | 'openLink' | 'jsHandle';
  target?: string;         // Required for show/hide/addClass/removeClass. #id only, multiple: "#id1,#id2"
  params?: string;         // addClass/removeClass: class names (comma-separated); openPage: pageUuid; openLink: URL. Forbidden for jsHandle. Must be a plain string, no code/variables.
  funcName?: string;       // Only for jsHandle
  operationTitle?: string; // Required for jsHandle/addClass/removeClass (2-8 Chinese chars)
  animation?: string;      // Animation effect name
  animationTime?: number;  // Animation duration in seconds
  delayTime?: number;      // Delay before execution in seconds
}
```

#### Selector Rules (CRITICAL)

| Rule | Detail |
|------|--------|
| `original` and `target` | Only `#id` or `.class` — NO attribute selectors (`[data-xxx]`) |
| `original` | Single element only — no multiple selectors |
| `target` | Multiple IDs allowed: `"#id1,#id2"` — NO `.class` allowed |
| If element only has data attributes | You MUST add an `id` to it, then use `#id` in DSL |

#### Operation Priority

1. `show`/`hide` — preferred for opening/closing modals
2. `addClass`/`removeClass` — CSS changes
3. `openPage` — page navigation (params must be pageUuid string only)
4. `back` — go back
5. `jsHandle` — only when above can't satisfy the requirement

#### jsHandle Rules

1. Each function in its own `<script>` tag
2. Script `id` MUST match function name exactly
3. Only one parameter: `event`
4. No API calls inside

```html
<script id="tabSwitchXxx">
function tabSwitchXxx(event) {
  // full implementation
}
</script>
```

### Page Navigation

For navigation elements, add `id` AND `data-uuid` to the HTML tag. The `data-uuid` value MUST match the `--pageuuid` you pass to `page save --new`:
```html
<!-- If you will save this target page with: page save --new --pageuuid home --name "首页" -->
<a id="nav-home" data-uuid="home" href="javascript:void(0);">首页</a>
```
Do NOT add openPage events in interaction-data for these — they are auto-generated.

### Image Placeholders

Use placeholder URLs, the platform replaces them with real images:
```html
<img src="./api/searchImage?query=premium laptop on white background&width=400&height=400" class="w-full h-full object-cover" />
```

### Button Rules

- ALL buttons must have `type="button"`
- NO `type="submit"`
- Use `href="javascript:void(0);"` for links, never `href="#"`

### Design Constraints

- **Shadows**: Use diffuse shadows: `shadow-[0_8px_30px_rgba(0,0,0,0.04)]`, not short dark shadows
- **Native controls**: No `<select>` or radio buttons for option switching — use capsule segmented controls
- **Horizontal scroll**: Hide scrollbar with `scrollbar-hide`
- **Modals/masks/drawers**: Add `hidden` class by default; use nested structure. The mask/overlay layer MUST have a semi-transparent background color (e.g. `bg-black/50`), and the inner modal/drawer content container MUST have an opaque background color (e.g. `bg-white`). A transparent content container is a SERIOUS VIOLATION - the mask color will bleed through and the popup content area will appear as the mask color. Example:
  ```html
  <div id="modalMask" class="modal-mask hidden fixed inset-0 bg-black/50 flex justify-center items-center z-50">
    <div class="bg-white rounded-lg p-6">
      <!-- Modal content - inner container MUST have bg-white or other opaque color -->
    </div>
  </div>
  ```
- **CSS override**: When status class (like `hidden`) overrides component class, combine in stylesheet: `.modal-mask.hidden { display: none; }` — do NOT use `@apply hidden`

### Script Order

1. TailwindCSS (in `<head>`)
2. ECharts dependency (in `<head>`, optional)
3. `tailwind.config` configuration
4. ECharts config scripts (`<script id="echarts_*" type="echarts">`, optional)
5. jsHandle function scripts (`<script id="funcName">`, optional)
6. **`interaction-data` MUST be the last `<script>` tag**

### Complete Page Template

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: { primary: '#1890ff' }
        }
      }
    };
  </script>
  <style>
    .modal-mask.hidden { display: none; }
  </style>
</head>
<body>
  <div id="app">
    <!-- Page DOM -->
  </div>

  <!-- jsHandle functions (optional) -->
  <!-- <script id="funcName">function funcName(event) {...}</script> -->

  <!-- Interaction DSL (MUST be last script) -->
  <script id="interaction-data">
`
[
  {
    "original": "#elementId",
    "trigger": "click",
    "actions": [
      { "operation": "show", "target": "#targetId" }
    ]
  }
]
`
  </script>
</body>
</html>
```

## Validation Rules Summary

The `gemdesign validate` command checks:

| # | Rule | What it checks |
|---|------|---------------|
| 1 | interaction_data_exists | `<script id="interaction-data">` present |
| 2 | dsl_json_valid | Content is valid JSON array |
| 3 | selector_exists | All original/target selectors exist in DOM |
| 4 | selector_format | Only #id and .class, no attribute selectors |
| 5 | original_single | original has only one selector |
| 6 | target_no_class | target uses only #id, no .class |
| 7 | jshandle_func_match | Each funcName has matching `<script id="funcName">` |
| 8 | script_id_funcname_match | script id equals function name |
| 9 | button_type | All buttons have type="button", no type="submit" |
| 10 | no_vh | No vh unit in classes or styles |
| 11 | no_hash_href | No href="#" |
| 12 | image_url_format | Placeholder image URLs use `./api/searchImage?query=...&width=...&height=...` with numeric width/height, no spaces around `&` |
| 13 | data_uuid_complete | Tags with data-uuid also have id |
| 14 | interaction_data_last | interaction-data is the last script tag |

## Tips

- **HARD GATE — 严禁直接创建 `.html` / `.meta.json` 文件**：新建页面必须先执行 `page create`（创建 `.stream.lock`）再写入 HTML，无 lock 直接创建 HTML 是严重违规；修改已有页面必须先 `page get`。`.meta.json` 由 CLI 专属管理（`page get` 生成、`page save` 读取），智能体严禁创建或修改。
- **HARD GATE — `page save` 不可跳过**: 写入 HTML 文件后，**必须**调用 `gemdesign page save` 保存到平台。只生成本地文件而不调用 `page save` 是严重违规——页面不会出现在平台上，用户无法看到或使用该页面。完整流程：`page create` → 写入 HTML → `page save`。`page save` 内置了规范验证，验证失败会返回错误，修复后重新执行 `page save` 即可。
- **HARD GATE — 批量生成逐页立即保存**: 生成多个页面时可以并行推进，但每个页面的 HTML 一写完，必须立即执行该页对应的 `page save`（删除 `.stream.lock`、结束流式、同步远程），确认成功后该页才算完成；严禁等所有页面都生成完再攒批统一 save——否则 lock 滞留、页面一直处于流式状态且不同步远程服务器。
- `page create` 的响应包含 `requiredNextSteps` 字段，列出后续必须执行的步骤。收到该响应后必须按步骤执行，不可在写入 HTML 后停止。
- `gemdesign validate` 是可选的早期错误检测工具——`page save` 内部已包含验证，但 `validate` 可以在保存前捕获错误
- **Save HTML locally** for every page: `./output/<projectDir>/<pageuuid>.html` for editing and saving to the platform. Always compute `<projectDir> = {projectName}__{appuuid}` first via `gemdesign app info`. The CLI is idempotent - passing a path that already contains `<projectDir>` will not duplicate it.
- When creating a new page, pass a readable `--pageuuid` (e.g. `home`, `login`) - use the same value as `data-uuid` in navigation elements, so you don't need to update them after saving
- Use `gemdesign page get --file <path>` to retrieve editable HTML+DSL before modifying
- The full page spec is available at `page-spec.md` in the CLI project directory