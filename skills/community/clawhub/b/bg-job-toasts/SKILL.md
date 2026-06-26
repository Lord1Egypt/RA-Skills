---
name: bg-job-toasts
description: "Background job toast notification system for the OpenClaw Control UI. Bottom-right corner toast bar that shows running/complete/error status for all background processes — cron jobs, memory compaction, knowledge extraction, and any custom jobs. Includes gateway cron event enrichment (job name forwarded in broadcast payload) and context gauge button with live spinner + progress modal. Use when adding or improving background job visibility in the OpenClaw UI, fixing 'Background job' fallback names on toasts, or troubleshooting the compaction button showing no progress."
---

# Background Job Toasts — OpenClaw Control UI

Real-time bottom-right toast bar that shows running / complete / error status for all background processes in the OpenClaw Control UI: cron jobs, memory compaction, knowledge extraction, and any consumer that pushes to `backgroundJobToasts`.

## Status: ✅ Active

| Component | Status |
|-----------|--------|
| Toast bar (bottom-right) | ✅ Working |
| Cron job name enrichment (gateway) | ✅ Working |
| Context gauge spinner during compaction | ✅ Working |
| Compaction modal phase labels + progress bar | ✅ Working |
| Auto-dismiss after completion | ✅ Working |

## Architecture

### Data Type (`ui/src/ui/app-view-state.ts`)

```typescript
export type BackgroundJobToast = {
  jobId: string;        // Unique identifier (use "cmp-" prefix for compaction)
  jobName: string;      // Human-readable label shown in the toast
  status: "running" | "complete" | "error";
  startedAt: number;    // Date.now()
  completedAt: number | null;
  errorMsg?: string;
};
```

`backgroundJobToasts: BackgroundJobToast[]` is a LitElement `@state()` property on `OpenClawApp` (`app.ts`). Assigning to it directly triggers an automatic re-render — no `requestUpdate()` needed for the toast array itself.

### Toast Rendering (`ui/src/ui/app-render.ts`)

`renderBackgroundJobToasts(state)` renders the `.bg-job-toasts` container at the bottom of the app shell (called in the root `render()` function). It maps each toast to a `.bg-job-toast--{status}` div with an icon, name, and label.

Status indicators:
- `running` → spinner icon (CSS animation `compaction-spin`), blue tint, "running..."
- `complete` → checkmark icon, green tint, "done"
- `error` → X icon, red tint, "failed"

### Styles (`ui/src/styles/components.css`)

```css
.bg-job-toasts   { position: fixed; bottom: 24px; right: 24px; z-index: 9000; … }
.bg-job-toast    { border-radius: var(--radius-lg); background: var(--panel-strong); … }
.bg-job-toast--running  { color: var(--info); … }
.bg-job-toast--complete { color: var(--ok); … }
.bg-job-toast--error    { color: var(--danger); … }
```

Entry animation: `bg-job-toast-in` (0.2s, slide up from 6px).

### Gateway Cron Event Enrichment (`src/gateway/server-cron.ts`)

The gateway's `onEvent` callback enriches cron events with the job name before broadcasting, so the UI can display a meaningful label even when the Cron tab hasn't been opened yet (and thus `cronJobs` isn't loaded):

```typescript
onEvent: (evt) => {
  const jobForName = cron.getJob(evt.jobId);
  const enriched = jobForName?.name ? { ...evt, name: jobForName.name } : evt;
  params.broadcast("cron", enriched, { dropIfSlow: true });
  // ... rest of webhook handling
}
```

### UI Cron Event Handler (`ui/src/ui/app-gateway.ts`)

```typescript
const cronPayload = evt.payload as {
  jobId?: string;
  name?: string;       // ← enriched by gateway
  action?: string;
  status?: string;
  error?: string;
};
// Priority: event.name > loaded cronJobs list > fallback
const jobName = cronPayload.name ?? matchedJob?.name ?? "Background job";
```

### Context Gauge + Compaction Button (`ui/src/ui/app-render.helpers.ts`)

The `renderContextGauge(state)` function renders a circular SVG ring in the chat toolbar. When compaction is running:

- The gauge ring is replaced by a spinning `⟳` icon
- A `compactState.phase` overlay modal appears with live status

Phase variables must be defined before the template:

```typescript
const phaseLabel =
  compactState.phase === "running"
    ? "Summarizing your conversation…"
    : compactState.phase === "complete"
      ? "Done! Context has been reduced."
      : compactState.phase === "error"
        ? "Something went wrong."
        : "";
const isWorking = compactState.phase === "running";
```

`compactState` is read from `(state as unknown as Record<string, unknown>).__compactState` — a plain property (not `@state()`), so `app.requestUpdate()` must be called explicitly after mutations.

**Compaction flow:**
1. Button click → `__compactState = { active: true, phase: "running" }` + push `"running"` toast → `requestUpdate()`
2. RPC `sessions.compact` resolves → update toast to `"complete"` with token counts → `__compactState = {}` → `requestUpdate()`
3. Auto-dismiss toast after 5 seconds

## Files Modified

| File | Change |
|------|--------|
| `src/gateway/server-cron.ts` | Enrich cron event with `name` before broadcasting |
| `ui/src/ui/app-gateway.ts` | Read `cronPayload.name` first in job name resolution |
| `ui/src/ui/app-render.helpers.ts` | Define `phaseLabel`/`isWorking`; spinner on gauge button while running |

## How to Push a Custom Toast from Anywhere

Any code with access to the `OpenClawApp` instance can push a toast:

```typescript
const app = state as unknown as OpenClawApp;
const jobId = "my-job-" + Date.now();

// Start
app.backgroundJobToasts = [
  ...(app.backgroundJobToasts ?? []).filter(t => t.jobId !== jobId),
  { jobId, jobName: "My Task", status: "running", startedAt: Date.now(), completedAt: null },
];

// Complete (with auto-dismiss)
app.backgroundJobToasts = [
  ...(app.backgroundJobToasts ?? []).filter(t => t.jobId !== jobId),
  { jobId, jobName: "My Task done", status: "complete", startedAt: Date.now(), completedAt: Date.now() },
];
window.setTimeout(() => {
  app.backgroundJobToasts = (app.backgroundJobToasts ?? []).filter(t => t.jobId !== jobId);
}, 5000);
```

> **Prefix convention:** Use `"cmp-"` for compaction jobs (filtered when a new compaction starts). Use a unique domain prefix for other job types.

## Known Gotchas

- **`phaseLabel`/`isWorking` must be defined before the template literal** — referencing them without defining them compiles fine (TypeScript doesn't catch undeclared variables inside template literals) but renders as `undefined` at runtime, producing a blank modal with no text and no progress bar.
- **`__compactState` is not `@state()`** — always call `app.requestUpdate()` after mutating it, or the UI won't re-render.
- **Cron job name fallback order matters** — the `name` field in the event payload (gateway-enriched) must be checked before the local `cronJobs` list, because the list is only loaded when the Cron tab is open.
- **`backgroundJobToasts` IS `@state()`** — assigning the array triggers a re-render automatically; no `requestUpdate()` needed specifically for that.

## Reference

See `references/source-snapshot.md` for a snapshot of the key code sections at time of writing.
