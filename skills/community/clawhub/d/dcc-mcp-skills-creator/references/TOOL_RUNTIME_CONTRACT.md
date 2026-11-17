## Current Tool Contract

Generated `tools.yaml` entries follow the modern contract:

- Local tool names are snake_case and client-safe. Do not use dotted names.
- Loaded tools are published as `<skill-name>__<tool_name>` when namespacing is needed.
- Skill package version metadata lives at `metadata.dcc-mcp.version` in
  `SKILL.md`; a top-level `version` key is rejected by the strict loader.
- Set `metadata.dcc-mcp.dcc` to the concrete host. Use `dcc: any` only when the
  same implementation is safe in every host; concrete-host tools override a
  same-named `any` tool during scoped lookup.
- Inter-skill dependencies live at `metadata.dcc-mcp.depends` as skill names,
  not repo names or prose-only instructions. Use it when one skill must be
  discovered or loaded before another, for example `depends: ["qt-ui-inspector"]`.
- `input_schema` and `output_schema` are declared explicitly.
- A zero-argument tool still declares a closed schema:
  `{"type":"object","properties":{},"additionalProperties":false}`.
- Runtime discovery never imports or executes tool scripts to infer missing
  schemas by default. Treat Python-derived schemas as an authoring-time helper:
  generate them before publishing, then commit the JSON Schema to `tools.yaml`.
- Keep MCP-facing `input_schema` shapes simple: prefer a top-level object with
  `properties`, `required`, primitive `type`, bounds, and descriptions. Put
  mutually exclusive forms, conditional requirements, and cross-field rules in
  the tool script or handler validation instead of `anyOf`, `oneOf`, `allOf`,
  `not`, `if`/`then`/`else`, or dependent-schema keywords. When a complex
  schema is unavoidable, discovery must route through `describe` before call.
- Published recipe `inputs_schema` references stay within one schema resource:
  use `#`, a local JSON Pointer such as `#/$defs/name`, or a local `$anchor`
  such as `#name`. Recipe admission rejects `$id`, `$dynamicRef`, and
  `$dynamicAnchor`; external and resource-relative `$ref` values are not
  supported by the dependency-free validator.
- A recipe `inputs_schema` may declare `$schema` only at the schema resource
  root, and its value must be the absolute canonical Draft 2020-12 URI
  `https://json-schema.org/draft/2020-12/schema`. Null, relative, unsupported,
  and nested dialect declarations fail closed during recipe admission.
- Recipe `pattern` and `patternProperties` expressions must use syntax shared
  by Python 3.7-3.14. Version-specific constructs such as atomic groups
  `(?>...)` fail closed; use portable constructs such as `(?:...)` only when
  they preserve the intended matching semantics. Global inline flags such as
  `(?i)` are portable only at the absolute start; use scoped flags such as
  `(?i:...)` when flags must appear after a prefix or inside another group.
  The `\B` non-boundary assertion is not portable because its empty-string
  behavior changes in Python 3.14; express the intended boundary explicitly.
- `execution` is `sync` or `async`; use `async` for deferred/long-running work.
- `job_strategy` is `monolithic` (default), `chunked`, or `isolated`. Agents
  use it to select a safe execution and recovery workflow.
- `affinity` is explicit. Use `main` for host API or scene mutation work and `any` for pure work.
- `enforce_thread_affinity: true` is emitted so adapter dispatch stays honest.
- `annotations` explicitly declare boolean `read_only_hint`,
  `destructive_hint`, `idempotent_hint`, and `open_world_hint`. Missing safety
  fields force `describe`, even for a zero-argument tool; `deferred_hint` stays
  optional.
- Keep tool groups independently usable. A correlated load carrying
  `target_tool_slug` activates only that tool's group; do not rely on a sibling
  default-active group being activated with it.
- `call_examples`: optional list of ready-to-copy argument payloads. Each entry has `arguments` (JSON object matching `input_schema.properties`) and an optional `note`. Surfaced in describe responses at `metadata.dcc.call_examples` so agents can construct correct arguments on the first attempt.

### Long-Running Main-Affinity Tools

`execution: async` changes the job lifecycle; it does not make one monolithic
host call interruptible. For long scene mutations:

```yaml
execution: async
job_strategy: chunked
affinity: main
enforce_thread_affinity: true
annotations:
  deferred_hint: true
```

When the adapter supports `HostUiDispatcherBase.submit_chunked_runner()`,
define bounded steps with the shared helper:

```python
from dcc_mcp_core import chunked_job

@chunked_job(total=100)
def build_bake_steps():
    for frame in range(100):
        yield lambda frame=frame: bake_one_frame(frame)
```

Return the runner from the declarative entry point. `HostExecutionBridge`
automatically submits it to the shared host pump and binds it to the outer
JobManager cancellation probe. Do not create a skill-local timer, thread,
pump, or second job registry.
Keep each yielded callable bounded, return a string when a progress message is
useful, and let cancellation become terminal only after a runner checkpoint.
If the adapter does not expose the shared chunked path, document that the tool
is monolithic and request an adapter/core integration instead of claiming
mid-call interruption.

Use `job_strategy: isolated` when the typed tool launches a process- or
service-owned operation and returns a durable job id immediately. Declare the
poll and cancel tools in `next-tools` and in the result recovery context.
Status must remain readable after a transport disconnect or adapter restart;
state cancellation ownership honestly when it cannot be reconstructed.
The launch result must include the same durable `job_id` plus one canonical
status. To make CLI `--wait` follow the adapter operation, declare the status
tool in `next-tools.on-success` with `execution: sync`, a string `job_id` as its
only required input, and both `read_only_hint: true` and `idempotent_hint: true`.
Every other input must be optional and safe when omitted. Core rejects async,
mutating, optional-id, multi-required-input, and untyped pollers. The status tool must
return the queried ID or an explicit unknown-ID error; it must never create a
new operation while polling.

Render and cook status tools should reuse the Core progress vocabulary:
`status`, `progress.current`, `progress.total`, and `progress.message`.
`current` and `total` are monotonic work-unit counts such as completed/total
frames; clients derive the percentage and render one progress bar. Prefer the
renderer or cook service's native counters. If files are the only source, keep
that counting inside the typed status tool instead of making the agent run
repeated directory scans.

During an active turn, agents should start once and use CLI `--wait`, REST job
events, or the declared status tool. Do not create an OS or DCC-MCP scheduled
workflow merely to poll one running operation. Only after the user explicitly
requests cross-session monitoring may an agent create a one-shot follow-up that
stores the existing job/operation id, performs read-only status checks, and
self-stops at a terminal state; it must never relaunch the render or cook.
Mirror this contract in `agents/openai.yaml`: tell the Agent to start once,
follow typed progress to a terminal state, and query the same job id after a
timeout instead of relaunching work.

For one indivisible DCC-native call, keep `job_strategy: monolithic`. Prefer
`execution: async` so the initial transport returns a core job id, then poll
the instance-routable `jobs_get_status`. A transport timeout is not completion
or cancellation: rediscover the instance and query the job before retrying.
Declare potentially long tools as `execution: async` with a realistic positive
`timeout_hint_secs`. The timeout hint describes a budget, not an execution mode;
do not rely on it to obtain a job envelope. Some older REST runtimes promoted
hinted synchronous tools differently from MCP, so validate both routes on the
exact target Core artifact and keep the execution declaration explicit.
The creator scaffold deliberately emits `monolithic` for async tools; change it
only with the matching chunked runner or isolated status/cancel implementation.

### Computer Use Fallback Contract

- Reuse the bundled `ui-control` skill instead of creating another screenshot,
  pointer, keyboard, or Windows `SendInput` tool set. Declare
  `metadata.dcc-mcp.depends: ["ui-control"]` only when it is a hard workflow
  dependency. Native UI Control requires standalone `dcc-cua` 0.4.0 or newer;
  do not preserve or add a legacy Core Host fallback.
- Keep the visual loop as `ui_control__snapshot` -> `ui_control__act` ->
  `ui_control__snapshot`, and pass the latest `snapshot_id` unchanged. End every
  path with `ui_control__stop_computer_use`. Screenshot coordinates belong to that
  observation only.
- Preserve `capture_provenance` with saved evidence. A live
  `backend=dcc-cua` snapshot plus `pixels_captured=true` proves native
  application capture; keep the logical UI Control `session_id`
  distinct from the gateway agent session used for stats attribution.
- Stateful UI tools must declare `requires_in_process: true` independently of
  `affinity`; keep UI Control at `affinity: any` so it does not block the DCC
  UI thread while preserving one persistent CUA bridge. The shared standalone
  Host owns observations, Esc interruption, markers, and cross-session input
  serialization; skill scripts must not instantiate another automation stack.
- Prefer a `control_id` and semantic UI Automation action. Use raw coordinates
  only when the UI does not expose a stable semantic control.
- For native application menu bars, use the negotiated `invoke_menu` action
  with an explicit `menu_path` when a semantic menu click or Alt mnemonic
  cannot prove that a popup opened. Never guess pixels or report native
  delivery as completion; take a fresh snapshot and honor
  `verification_required` before another mutation.
- For custom-drawn canvases, viewport manipulators, or face controls, use one
  `drag` path from the latest snapshot. `keys` may hold Ctrl, Shift, or Alt for
  pointer-modified drags; snapshot again immediately before deriving another
  path. In `pixels_only` mode, the path has exactly two endpoints and their `x`/`y`
  values are physical screenshot pixels local to the latest main PNG. Do not
  convert them to desktop coordinates, apply DPI scaling or use secondary
  popup-image coordinates.
- Never set `DCC_MCP_CUA_ALLOW_RAW_INPUT` from a skill script. Native input is
  enabled by default, and the operator-owned `false` setting disables it.
  Native input also requires the
  adapter/operator to bind its DCC with `DCC_MCP_UI_CONTROL_PROCESS_ID` or
  `DCC_MCP_UI_CONTROL_WINDOW_HANDLE`; a skill request may only narrow that
  trusted scope. Propagate `user_interrupted` immediately;
  do not retry the action or fall back to another input path after Esc interrupts a session.
- Never enter or retry another UI/input path after a policy, authorization,
  authentication, security, confirmation, `desktop_unavailable`, or
  `user_interrupted` result. Computer Use is a capability fallback, not a way
  around a control boundary.
- Keep mutating UI Control tools annotated as destructive. An optional
  consequence `intent` can only raise the native host's independent
  UIA/input classification. Never add a model-controlled `confirmed` or
  `approved` argument or treat an environment variable as per-action user
  approval.
- Generated record-replay Skills must stay local until reviewed. Compile
  structured calls to `WorkflowSpec` tool steps, compile semantic UI actions
  as fresh `snapshot` -> `find` -> one `act` -> verified wait/snapshot loops,
  and reject raw captured control ids or coordinates. Keep the demonstrated
  instance id as review provenance only. Never serialize approvals, grants,
  credentials, prompts, or secret-shaped fields. Visual fallback assets must
  be content-addressed, exact-window bounded, confidence gated, stable across
  multiple frames, and fail closed on geometry/DPI/topology drift.
