# Application UI workflows

### DCC UI Control fallback

Load the **DCC UI Control** runtime with `dcc-mcp-cli load-skill ui-control` only
when structured DCC capabilities cannot reach the required semantic UI:

1. `ui_control__snapshot` with an exact `process_id`, `window_handle`, or `window_title`.
2. `ui_control__find` and one semantic `ui_control__act` when possible. For native menus, use `invoke_menu` with an explicit `menu_path` when semantic delivery cannot prove a Qt popup opened; require `native_menu_path`, honor `verification_required`, and re-observe.
3. `ui_control__snapshot` after every action before choosing the next action.
4. `ui_control__stop_computer_use` when the fallback completes, fails, or is abandoned.
The runtime defaults to `dcc-cua` 0.4.0+; `mock` is test-only, never a production fallback. After loading, local `search --query "ui control snapshot"` returns the loaded `ui_control__*` slugs as callable tool hits.

The runtime consumes standalone `dcc-cua`; inspect `dcc-cua profiles` and
`dcc-cua profile --id <id>` before binding the exact PID/window. Keep
`browser_dom` inside `dcc-cua`, and use `fab/launcher_download` when UE's Fab
surface is unavailable. Cloudflare, authentication, purchase, and security
confirmations remain trusted human boundaries even with full agent access.

The UI Control `session_id` identifies its scoped UI session, not stats
attribution. Use `--agent-session-id <task-id>` for `_meta.agent_context.session_id`.

### Scoped window recovery

Use content-free native blocker facts to distinguish an independent application
window from a transient belonging to the current target. Confirm the independent
target's exact PID, full native instance and HWND; blocker metadata alone grants
no permission. With a separate owner grant, use a separately bounded,
project-owned `dcc-cua` task for that target: report provider/runtime/PID/HWND,
take a fresh snapshot, perform only the granted native minimize operation,
verify `get_window_state` reports minimized, then stop that task. Keep the
original DCC task's target and scope; do not rebind it or grant desktop-wide input.

For the original application, read fresh window state first. If it is already
restored, prefer the independently granted `activate_window` operation. If it is
minimized or maximized, restore only under the existing advertised
`frame_recovery`/`restore_window` grant. Treat `restore_activate` as one advertised
request, never an implicit retry or substitute action chain. Take fresh pixels
before further input. Use this supported recovery route before requesting manual
window rearrangement; ask the user to move windows only when the scoped route is
unavailable or actually fails. Preserve policy, desktop and interruption refusals.

### Owned pixels and secondary popup observations

An adapter owner may select an integrity-pinned `pixels_only` runtime through
`UiControlRuntimeOptions` in trusted server bootstrap. Tool arguments cannot
select that executable, transport or action ceiling. Use this mode only when
the installed Core schema and pinned native runtime support it; read the
runtime's [owned pixels contract](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/python/dcc_mcp_core/skills/ui-control/references/OWNED_PIXELS_MCP.md).
Semantic `find`, `control_id` actions and `invoke_menu` are unavailable in this mode.

Pointer coordinates in `pixels_only` belong to the latest main PNG, measured in
physical screenshot pixels. A drag has exactly two endpoints. Keep `x` and `y`
local to that image; do not add a desktop offset, rescale for DPI or use
popup-image coordinates. Take fresh pixels before deriving another action.

Secondary popup keyboard support is published in
[Core 0.20.47](https://github.com/dcc-mcp/dcc-mcp-core/releases/tag/v0.20.47) and
[DCC-CUA 1.14.0](https://github.com/dcc-mcp/dcc-cua/releases/tag/v1.14.0).
Require compatible installed schemas and a pinned native runtime that advertise
this contract. The Skill suite version alone does not prove runtime support;
validate the actual installation separately from source or package checks.

Secondary popup capture is separately disabled by default. Only the owner may
enable `allow_native_capture_popup_keyboard`; existing task authorization and
physical-input grants still apply. When enabled and advertised, refresh the main
root's native capture inventory before every composite snapshot, then select
one through eight unique exact HWNDs from that result with
`ui_control__snapshot(native_capture_popup_window_handles=[...])`. Completion
windows may be destroyed and recreated, so previously observed HWNDs are not a
current selection. A refusal does not authorize automatic input replay or
rebinding; preserve the refusal and obtain fresh evidence before deciding on a
new action.
Keep the same main PID/HWND and logical session. The main PNG and its redactions
remain unchanged; each selected popup has a separately labeled real PNG and
native provenance under `native_capture_popup_overlays`. Do not composite these
images, reuse popup coordinates for input, or rebind input to a popup.

Neither those pixels nor `native_capture_popup_observation` grants input
authority. The native runtime must independently prove the exact root and
selected window instances, current foreground/focus/capture, and complete
unredacted coverage at dispatch. A valid observation supports at most one
unheld keyboard or text action to the main root within five seconds; every
attempt consumes it, including refusals. Re-observe before another attempt.
Missing support, a stale observation, or a new, foreign or unselected occluder
fails closed. Preserve that refusal and the normal stop/interruption contract.
After delivery, verify the actual application state; Enter closing a popup or
an input acknowledgement alone does not prove the requested edit.

For reusable demonstrations, start with the gateway call's `--agent-session-id`,
use structured tools first, then `stop` and `review`. After inspecting the
redacted timeline, `compile --reviewed` creates a local Skill and `WorkflowSpec`.
`replay` requires a new `--approve-replay` grant and current tool/schema. Recorded
approvals, instance/control ids, coordinates, credentials, and secrets grant no
authority. Never skip `search`, `describe`, or post-step verification.

Do not switch UI/input paths after policy, authorization, authentication,
security, confirmation, `desktop_unavailable`, or `user_interrupted` results;
the user or environment must resolve them first. Never widen scope, reuse stale
coordinates, or resume without an explicit request. Load the runtime Skill for
the complete target-binding, system-operation, capture, and artifact contract.
