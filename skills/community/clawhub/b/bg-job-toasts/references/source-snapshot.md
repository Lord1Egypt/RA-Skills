# Source Snapshot

Key code sections at time of writing (OpenClaw `upgrade-test-20260217` branch, 2026-03-05).

---

## `ui/src/ui/app-view-state.ts` — BackgroundJobToast type

```typescript
export type BackgroundJobToast = {
  jobId: string;
  jobName: string;
  status: "running" | "complete" | "error";
  startedAt: number;
  completedAt: number | null;
  errorMsg?: string;
};
```

---

## `ui/src/ui/app-render.ts` — renderBackgroundJobToasts

```typescript
function renderBackgroundJobToasts(state: AppViewState) {
  const toasts = state.backgroundJobToasts ?? [];
  if (!toasts.length) {
    return nothing;
  }
  return html`
    <div class="bg-job-toasts">
      ${toasts.map(
        (toast) => html`
          <div class="bg-job-toast bg-job-toast--${toast.status}">
            <span class="bg-job-toast__icon">
              ${
                toast.status === "running"
                  ? icons.loader
                  : toast.status === "error"
                    ? icons.x
                    : icons.check
              }
            </span>
            <span class="bg-job-toast__name">${toast.jobName}</span>
            <span class="bg-job-toast__label">
              ${
                toast.status === "running"
                  ? "running..."
                  : toast.status === "error"
                    ? "failed"
                    : "done"
              }
            </span>
          </div>
        `,
      )}
    </div>
  `;
}
```

---

## `src/gateway/server-cron.ts` — onEvent with name enrichment

```typescript
onEvent: (evt) => {
  // Enrich the event with the job name so the UI can display a meaningful
  // label in toasts even when the cron jobs list hasn't been loaded yet.
  const jobForName = cron.getJob(evt.jobId);
  const enriched = jobForName?.name
    ? { ...evt, name: jobForName.name }
    : evt;
  params.broadcast("cron", enriched, { dropIfSlow: true });
  if (evt.action === "finished") {
    // ... webhook handling unchanged
  }
},
```

---

## `ui/src/ui/app-gateway.ts` — cron event handler (name resolution)

```typescript
const cronPayload = evt.payload as {
  jobId?: string;
  name?: string;
  action?: string;
  status?: string;
  error?: string;
};
if (cronPayload?.action === "started" || cronPayload?.action === "finished") {
  const jobId = cronPayload.jobId ?? "unknown";
  // Prefer name from event payload (gateway enriches it), fall back to loaded cron jobs list
  const cronJobs =
    (host as unknown as { cronJobs?: Array<{ id: string; name?: string }> }).cronJobs ?? [];
  const matchedJob = cronJobs.find((j) => j.id === jobId);
  const jobName = cronPayload.name ?? matchedJob?.name ?? "Background job";
  // ... toast push unchanged
}
```

---

## `ui/src/ui/app-render.helpers.ts` — renderContextGauge (phase + spinner)

```typescript
// These must be defined BEFORE the return html`` block
const phaseLabel =
  compactState.phase === "running"
    ? "Summarizing your conversation…"
    : compactState.phase === "complete"
      ? "Done! Context has been reduced."
      : compactState.phase === "error"
        ? "Something went wrong."
        : "";
const isWorking = compactState.phase === "running";

return html`
  <button
    class="btn btn--sm btn--icon"
    title=${tooltip}
    ?disabled=${compactState.active || !state.connected || pct < 20}
    @click=${handleCompact}
  >
    ${isWorking
      ? html`<span style="font-size:12px;animation:spin 1s linear infinite;display:inline-block;">⟳</span>`
      : gaugeRing}
  </button>

  ${compactState.phase ? html`
    <div style="position:fixed; inset:0; z-index:1000; background:rgba(0,0,0,0.55); ...">
      <div style="...">
        <div style="font-size:15px; font-weight:600; ...">Memory Compaction</div>
        <div style="font-size:13px; color:var(--text-muted); ...">${phaseLabel}</div>
        ${isWorking ? html`
          <div style="height:4px; border-radius:2px; ...">
            <div style="animation:compactProgress 2s ease-in-out infinite; ..."></div>
          </div>
        ` : nothing}
      </div>
    </div>
  ` : nothing}
`;
```

---

## `ui/src/styles/components.css` — Toast styles

```css
.bg-job-toasts {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9000;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}

.bg-job-toast {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 14px;
  border-radius: var(--radius-lg, 10px);
  border: 1px solid var(--border);
  background: var(--panel-strong);
  color: var(--text);
  font-size: 13px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  animation: bg-job-toast-in 0.2s var(--ease-out, ease-out);
  white-space: nowrap;
  user-select: none;
}

.bg-job-toast--running  { color: var(--info);   border-color: rgba(59, 130, 246, 0.35); }
.bg-job-toast--complete { color: var(--ok);     border-color: rgba(34, 197, 94, 0.35); }
.bg-job-toast--error    { color: var(--danger); border-color: rgba(239, 68, 68, 0.35); }

.bg-job-toast__icon { display: flex; align-items: center; flex-shrink: 0; }
.bg-job-toast__icon svg { width: 15px; height: 15px; stroke: currentColor; fill: none;
  stroke-width: 1.5px; stroke-linecap: round; stroke-linejoin: round; }
.bg-job-toast--running .bg-job-toast__icon svg { animation: compaction-spin 1s linear infinite; }
.bg-job-toast__name  { font-weight: 500; }
.bg-job-toast__label { opacity: 0.7; }

@keyframes bg-job-toast-in {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
```
