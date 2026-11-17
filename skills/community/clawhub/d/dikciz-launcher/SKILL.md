---
name: "dikciz-launcher"
description: "Install and operate Dikciz Launcher on an owner-selected Android device. Use when controlling its home, HTML widgets, Lua, Android data, sensors, camera, audio, speech, Bluetooth, NFC, USB, Wi-Fi, files, APKs, shell sessions or command jobs through MCP, HTTP or WebSocket. Source builds use the Android Lab skill."
homepage: "https://github.com/psyb0t/dikciz-launcher"
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [python3]
permissions:
  network: "Connect only to the owner-selected Dikciz phone endpoint. Requested SMS, USSD, weather, speech and model-download operations can send data to their documented recipients or providers. Assistant conversations send messages and requested phone data to their configured model provider."
  shell: "Run the documented controller or explicitly requested ADB installation. Device shell commands require explicit task scope and remain subject to Android access."
  filesystem: "Read supplied APKs and task inputs; save requested screenshots, transfers and results in the task workspace. Keep bearer credentials in the secret environment."
---

# Dikciz launcher

Use this skill to install and operate Dikciz, not to develop its Android source or manage Android Lab.

## Security & safety

Operate only the selected owner-controlled device and requested resources. Reset, uninstall, SMS, file changes, privileged commands and permission changes require the owner's requested scope. A connection request alone does not authorize them. Use the configured secret environment for bearer credentials; never include them in prompts, command arguments or tracked files. Native commands use Android permissions; root shell is separate and defaults to root unless `root: false` is supplied.

## When to use

Install an existing APK or operate the launcher, files, apps, Android data, sensors, speech and hardware through its discovered APIs. Use direct native commands before UI tapping when they cover the task. The phone runs the MCP server; the client supplies its reachable `/mcp` URL and optional bearer credential.

## When NOT to use

Source edits and builds use the separate Dikciz Android Lab skill. This skill does not grant Android permissions, bypass the lock screen, make private endpoints public or imply unrestricted system access.

## Install or connect

Read [references/setup.md](references/setup.md) for APK installation, Android access, port forwarding, and connection checks. Take the APK and target device from the user. If either is missing or ambiguous, ask. Do not build an APK or start an emulator just to install one.

For a scoped connection, read `remoteAccessInfo` or `dikciz_remote_access_info` first. Use the owner's selected token grants; do not escalate a `remote_permission_denied` response through shell, UI, SDK calls or another binding. Tool discovery/search is permission-filtered, including provider/action enums. [Token management](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/remote-access-tokens.md) requires owner authority or explicit credential-administration grants, which can delegate owner-equivalent access. Read the [complete grant definitions](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/token-permissions.md) and [developer manual](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/developer-manual.md) for exact JavaScript/Lua bindings. The built-in chat uses its direct owner binding and independent read-only mode.

For an already connected launcher, discover its live contract before sending commands:

```bash
python3 scripts/dikciz-control.py websocket controlStatus --port 19101 --pretty
python3 scripts/dikciz-control.py websocket automationStatus --port 19101 --pretty
python3 scripts/dikciz-control.py mcp-tools --port 19102 --pretty
```

These examples use the repository's client and the forwarding ports in the setup reference. Use the actual client path, host and forwarded ports for the user's installation. A configured MCP client can connect directly to the forwarded `/mcp` endpoint instead.

## Use the launcher

Read [references/capabilities.md](references/capabilities.md) to choose among the supported features. It catalogs the launcher, configuration, event sources, actions, HTML bridge and remote controls, with links to their exact schemas.

- For Home selection, pages, app shortcuts, provider widgets, themes, and the native settings UI, read the [user guide](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/user-guide.md).
- For saved configuration, pages and widget files beneath `/sdcard/Dikciz/`, read the [configuration guide](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/dikciz-configuration.md) before editing them.
- For HTML bridge calls, Lua scripts, events, and automation policies, read the [scripting tutorial](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/scripting-tutorial.md).
- For WebSocket envelopes, MCP tools, semantic UI actions, screenshots, and device commands, read the [automation-control guide](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/automation-control.md). Discover the running build's names, fields and limits through `controlStatus` and `tools/list` rather than inventing them.

For arbitrary file browsing, binary upload/download, APK installation and shell output, read the [files, APKs and shell guide](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/files-and-apks.md). HTTP JSON commands share the MCP listener at `/v1/automation`; they require no MCP session. File APIs use Android permissions granted to Dikciz. An accepted installer session is not proof of successful installation; poll its final status.

Start with `snapshot`, `homeGet`, `configGet`, or the matching discovered MCP read tool. Use returned semantic IDs and page/widget addresses for actions. Read a fresh snapshot after an action to verify the change. Android accessibility actions require the phone owner to enable Dikciz's Accessibility service; ordinary launcher controls do not require it.

The bundled home has four pages: Home combines time/weather, app icons ranked by optional Usage access, and native Phone/Camera/Settings/store shortcuts; Tools has agenda and voice notes; Device has live battery and resource gauges, process CPU history and per-core data where Android exposes it. Home torch and speech demonstrations start only on a tap. Native app/group dragging requires a stationary one-second hold; release after the hold opens edit actions. Updated Most used documents subscribe to packageChanged for immediate removal. widgetGet exposes HTML eventSubscriptions, and JSON patchWidget replaces that array through the saved-configuration validator. appCatalogue reports nullable foregroundMilliseconds and usage availability; deviceState reports bounded per-core fields and an explicit non-requestable system CPU restriction. Native torch `durationMilliseconds` from 1 to 5000 bounds an on request independently of JS timers. Customized homes are preserved; untouched starters may refresh on update. Recording starts only on a tap and saves under its widget directory; deleting that widget removes its saved audio. Long press HTML content or its top handle for whole-document controls. Edit exposes HTML, CSS, JavaScript and state. Complete WebView templates are available in the HTML widget library, including system metrics and BTC/USD with economic news. Goblin adds manual speech, finite local alien audio, timed torch pulses and visible-page weather checks. Six Lua examples start disabled, including London entry, outdoor heat and GPS speed speech rules; a script dashboard can be added through the picker. The native picker can add third-party provider widgets. Lua runs as automation scripts, not as a widget type. Android permissions, special access and root remain device-controlled.

## Companion workflows

Complete custom apps combine editable HTML/CSS/JS, Lua or JS backend, app-local state and native event/timer/alert hosting. Fetch dikciz://docs/guides/custom-apps or read [custom apps](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/custom-apps.md) before creating one. Use discovered customAppsList/read/install/control/event/state/schedule/alert/runtime commands. Open Dikciz > Apps for the native manager. New apps start enabled and share all Android access granted to Dikciz. There are no per-app command allowlists or manifest approvals. Stop/start controls execution; source edits preserve that state. Read-only agents see list/read/runtime only and executor enforcement blocks direct mutations. SOS logic is apps/sos/main.js, with legacy sos* commands delegating to it. Its preview enforces read-only. Edited bundles survive updates; export excludes state/recordings, and encrypted backups include apps and assistant files with runtime metadata. Restored pending/claimed timers require review. Cancel pending work before removing an app; removal deletes its state/files. Inspect run/timers and actual UI visibility instead of treating queued work as success.

For SOS/check-ins, geofences/routes, retained peripherals, OCR/documents, Health Connect records, Wi-Fi approval, read-only routines or split APK installation, read [references/operations.md](references/operations.md) and the focused resource dikciz://docs/guides/companion. Saving/previewing safety plans never authorizes arming or SMS. Obtain requested scope for effects and verify actual receipt/install/network states.

## On-device assistant

Use discovered `dikciz_chat` (native `chatControl`) for shared provider connections, API model discovery, per-conversation model/token settings, messages, stop, event subscriptions and panel show/hide/fullscreen. Read [embedded chat](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/embedded-chat.md), or fetch `dikciz://docs/guides/chat`, `chat-context` and `chat-events` under the same guides prefix. Add a connection once, discover its models, then configure each conversation with independent settings. Read them with the settings action. The native chat exposes a model dropdown and a Tune button for model settings. The quiet Open chat notification opens the panel over another app while idle, without an extra service. Its Explain this screen button captures the app underneath. A running turn updates its activity notification with a Stop action; tapping it reopens that exact conversation. Stop cancels active and queued conversation work, preserves completed effects and leaves event subscriptions enabled. Its Make me a widget and Explain this screen shortcuts share `action:task` with `task:widget` (text required, writable access) or `task:explainScreen` (optional question), conversationId and requestKey. Widget tasks retain the current page target. Screen tasks hide chat, capture the display and force read-only tool execution for that turn before requesting chat reopening. Screenshots go to the chosen provider. Poll the transcript and preserve the request key on retries. API keys are write-only; never place real keys in prompts or command arguments. Queued sends and requested visibility changes require status/transcript verification. Event rules can incur provider usage while hidden; configure only the requested automation and clear rules when finished.

Use `dikciz_sim_list` for own SIM numbers before opening Settings. Each subscription includes nullable `phoneNumber` and `phoneNumberStatus`; missing number access returns `permissionRequest` for `phoneNumbers` while retaining metadata. A grant does not guarantee Android provides a number. The embedded assistant receives fresh per-turn access context and live tool contracts on rejected calls; inspect them before correcting arguments or requesting permissions.

## Owner assistant library

Use **Dikciz > Skills, agents & rules** for the manager. Discover assistantLibraryValidate and assistantLibraryManage for validated revision-checked saves. Read an existing file first; an empty expectedRevision means create only. Bundled @builtin guides teach skill, agent and rule authoring. Read-only and scoped restrictions remain enforced. For event-to-handler-to-command history and intercepted simulation, fetch dikciz://docs/guides/automation-debugger. Simulation never performs captured effects or saves state.

Owner skills, agents and rules live in /sdcard/Dikciz/assistant. Read [assistant library](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/assistant-library.md) or dikciz://docs/guides/assistant-library before installing them. assistantLibrary lists metadata and reads relative files through the shared executor. SKILL.md supports progressive disclosure and explicit $skill-name. Markdown agents run isolated conversations with inherited access, cancellation and timeout. settings.agent selects a named agent. Rules and skill catalogs reload between rounds. Harness-specific hooks and privilege settings are not portable. Instructions never grant Android access or bypass read-only/token restrictions.

## Offline documentation and reusable search

Use `dikciz_search_query` for an unfamiliar procedure before enumerating resources. Search a short task in collection `docs`, then read only an exact returned URI with `resources/read` or use `dikciz_search_read` with collection and ID. Collection `tools` returns ranked installed schemas that can be called directly. Search runs locally without a model or network. Reuse current contracts until the installed build or access context changes. See [offline search](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/search.md) for aliases, spelling correction and bounded pagination.

Owner collections require explicit requested indexing through `dikciz_search_index`. Do not crawl private files or messages merely to populate search. Built-in collections are protected. Read-only turns hide writable tool contracts and reject index mutations through the trusted executor.

Read `dikciz://docs/recipes/travel-todo` or the [GPS todo tutorial](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/todo-app-tutorial.md) for a complete source-linked UI/backend app. It subscribes to native geofence events and a custom task event. Opening never authorizes location monitoring; todo.watch requires owner intent, and todo.stop removes its fence.

## Background JavaScript

Background scripts can select language javascript, using main.js and synchronous onEvent(event), alongside existing Lua. Fetch dikciz://docs/guides/javascript before creating one. They share policies, owner commands, state, subscriptions and logs; HTML widgets retain their rendered-page lifecycle. Direct owner commands are not sandboxed by the returned-action allowlist. No WebView, Node.js, browser timers or Promise completion is provided by this backend.

## Complete capability reference

Read [operations](references/operations.md) for files, notification management and durable jobs, [capabilities](references/capabilities.md) for the inventory, [hardware and speech](references/hardware-and-speech.md) for native operation choices, and [setup](references/setup.md) for connection and package identity. The public [documentation index](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/index.md), [command reference](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/command-reference.md) and [coverage table](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/capability-coverage.md) cover accepted fields and implemented/remaining features. The installed server can serve short resources one section at a time. Read the [typed actions](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/typed-actions.md) for action fields and policy names, and [Android access](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/android-access.md) for feature grants and foreground restrictions. New commands require a build that advertises them; do not infer availability from the latest documentation alone.

## Boundaries and completion

An installation or connection request does not authorize resetting the home, uninstalling apps, replacing all configuration, enabling device administration, or running privileged shell commands. Explain the effect and obtain explicit approval for those operations. `shell` requests root by default; set `root: false` when app-sandbox execution is intended. Do not fall back to root after a denied action.

Preserve `/sdcard/Dikciz/` and the user's existing home. Keep bearer passwords in the user's secret environment, never in command arguments or public files. Forward only the selected device's ports to host loopback.

Finish after the requested installation or action is verified on that device. A queued automation event is not proof its actions succeeded; check script status and logs. Report access denials and connection failures instead of claiming completion.

Embedded chat supports per-conversation `settings:{"readOnly":true}`. Discovery hides mutating tools and the trusted executor flag blocks direct writes and permission prompts with `read_only_violation`. Tool arguments cannot disable it. Chat history and logs still save; other owner entrypoints retain their configured access. Read [embedded chat](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/embedded-chat.md) for the full contract.

For public SDK calls beyond the dedicated commands, first read `dikciz://docs/guides/android-sdk`. Discover exact overloads, inspect runtime and access restrictions, preserve typed handles and explicitly clean up SDK sessions. Read-only agents must never try to bypass hidden writes through the read bridge.

For command history, measured resource use and visual rules, fetch dikciz://docs/guides/operations. For encrypted home/chat archives, fetch dikciz://docs/guides/backups and preview before any confirmed restore. For camera/display frames, partial speech and explicit recorded-file upload, fetch dikciz://docs/guides/visual-streams. Inspect cursors, loss, terminal state and hardware cleanup. Read-only chat hides and blocks capture starts, stops, backup writes and resource changes.
