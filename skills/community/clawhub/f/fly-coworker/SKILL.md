---
name: fly-coworker
description: "Let the fly decide between tasks or PRs in Chrome; watch, veto, then Accept & start the chosen work in OpenClaw."
metadata: {"openclaw":{"emoji":"🪰","requires":{"bins":["openclaw"]}}}
---

# Fly Coworker

## Browser-first workflow

1. Collect 2–64 distinct, actionable tasks of 1–300 characters. Preserve PR URLs, repositories and constraints. Inspect the conversation for missing details; ask for the task list when absent. Identify the requesting session with `dashboard read` or `session_status`. Complete when every option identifies work the agent can begin and the owning session is known.

2. Discover `fly_coworker_create` and `fly_coworker_status`. If unavailable, check `openclaw plugins info fly-coworker` and consult `plugin-install.md` for the companion. Verify the plugin is loaded and Custom plugin UI is enabled. Reuse the installed companion; changing from the Mac app to Chrome needs no Gateway restart or auth changes.

3. Call `fly_coworker_create` with `{tasks:[...]}` in the requesting conversation. If the tool catalog is stale, call its registered session action with `openclaw gateway call plugins.sessionAction --json --params '<JSON>'`, using `{pluginId:"fly-coworker",actionId:"create",sessionKey:<current key>,agentId:<current agent>,payload:{tasks:[...]}}`. Pass task text as structured arguments or JSON through a file/script, not shell interpolation. Verify the returned round ID and session key.

4. Read the current dashboard, reuse or create tab `fly`, and `widget_put` with name `fly-picker`, kind `fly-coworker:picker`, `props:{roundId}`, size `full`. Open the Gateway's Control UI **in Google Chrome**, using the private `browserUrl` returned by `openclaw dashboard --json` as described in `references/browser-launch.md`. Navigate that browser to the owning session, focus the Fly tab, and expand the dashboard. This is the browser-hosted OpenClaw dashboard, not the native Mac window or the standalone viewer on port 4318. Verify the anatomical fly, brain panel, and **Accept & start** control render; report an actual error if they do not.

5. Leave the browser open for the human to watch the fly and click **Accept & start**, or **Salt blaster**, aim, and click the fly. A hit excludes the choice and respawns; a miss leaves it alive. The fullscreen button gives an arena-only view for recording. Never accept real work on the human's behalf. Yield once the browser is ready; no result polling or background watcher is needed.

6. Acceptance submits the exact chosen task into this same OpenClaw conversation using authenticated `chat.send` and a durable one-time dispatch key. When that message arrives, start the chosen task using the conversation's existing context and ordinary permissions. Do not start other options. A browser opened on the Gateway host still targets the requesting conversation, not a new chat or whichever chat happens to be visible elsewhere.

7. For status, call `fly_coworker_status` with the round ID (or its `status` session action). `chosen` awaits acceptance; `accepted` with `dispatch:started` proves a run receipt, not completed work. Check the conversation before any manual retry after an uncertain handoff. Reloading an accepted round must not send again. Verify completion from the task's output, separately from the handoff.

## Boundaries

The companion plugin is still required: Chrome loads its renderer and uses its existing secure handoff. The older standalone viewer's **Accept pick** only saves a local result and is not this workflow. Use Chrome for local HTTP on this host; the native Mac WebKit cookie issue is deferred, not fixed. Do not modify OpenClaw core or weaken authentication for this browser flow.

The fly uses FlyGym/NeuroMechFly anatomy and a 1,045-neuron MaleCNS circuit, not full Flyhard/Eon emulation or MuJoCo physics. Do not claim task comprehension or uniform randomness.
