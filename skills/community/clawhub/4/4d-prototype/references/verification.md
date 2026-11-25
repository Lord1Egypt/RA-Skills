# Verification: milestone gates, browser checks and headless Chrome scripts

"Done" means: type check, tests and build pass; the running dev server has loaded the latest code; you have actually looked and clicked at 1920×1080 and have evidence.

## 1. Command gates (every milestone)

```bash
npm run typecheck
npm test
npm run build
```

- When a test fails, find the root cause. Don't delete assertions, loosen type strictness, or add `any` / `ts-ignore`.
- When a redesign changes expectations (e.g. data merged into one batch), first print actual values with a temporary probe test, confirm each one is reasonable, then update the assertions and delete the probe.
- Read the first-load chunk size from the build output and record it in the progress log.
- Never put a `cat` that waits on stdin into a command; one command hung that way in the original project.

## 2. Dev server

- Start it with `.claude/launch.json` + `preview_start`. Reuse it while HMR works; restart it if the process exits.
- If the page shows old code after an edit, reload first. If that doesn't help, check that the process is still alive.
- Before acceptance confirm four things: code is saved; the build passes; the running instance has the latest code; key pages are reachable.

## 3. Two browser tools

| Tool | Use it for | Limitation |
|---|---|---|
| In-app browser (`mcp__Claude_Browser__*`) | Interaction, reading page text (`get_page_text` / `read_page`), console checks, and showing the user the current state | A 1920×1080 page is scaled down; screenshots don't show detail |
| Headless Chrome (`scripts/cdp_run.mjs`) | Full-resolution 1920×1080 screenshots, polling long autoplay runs, collecting console errors and uncaught exceptions, sweeping many pages | The user doesn't see it happen; share screenshots or describe the results |

When screenshots come out tiny, check text by reading page text, and check visuals with headless Chrome screenshots viewed with Read.

## 4. Using `scripts/cdp_run.mjs`

```bash
node ~/.claude/skills/4d-prototype/scripts/cdp_run.mjs <out-dir> <steps.json> [--port 9333] [--width 1920 --height 1080]
```

- Put the output directory in the scratchpad. The script finds Chrome automatically; override with `CHROME=/path/to/chrome`.
- Every run uses a fresh temporary profile and closes Chrome at the end. If the port is taken, run `pkill -f "remote-debugging-port=9333"` first.
- A fresh profile can take more than 10 s to start the first time; the script waits up to 30 s.

`steps` is an array executed in order. Available steps:

| Step | Meaning |
|---|---|
| `{"nav": "http://localhost:5273/#/flow"}` | Open a page, then wait 1.5 s by default |
| `{"eval": "js expression", "log": "label"}` | Evaluate and print the return value. If the expression contains `await`, the script wraps it in an async IIFE (CDP's evaluate doesn't support top-level await — a pitfall hit before) |
| `{"click": "[data-demo=\"check-run\"]"}` | Click an element; prints `missing` if not found |
| `{"waitFor": "expression", "timeout": 20000}` | Poll until the expression is truthy |
| `{"wait": 3000}` | Wait |
| `{"shot": "name"}` | Screenshot to `<out-dir>/name.png` |
| `{"check": "overflow"}` | Print whether the page overflows horizontally |

At the end the script prints `ERRORS n` and the first 20 console errors or exceptions.

### Common script templates (generate steps.json with python3)

**Sweep every page**: clear localStorage, fix preferences, then for each route take a screenshot, check overflow and read the heading.

```python
steps=[{"nav":BASE+"/#/"},{"eval":"localStorage.clear(); location.reload(); 1"},{"wait":2500}]
for route,name in ROUTES:
    steps+=[{"nav":BASE+"/#"+route},{"wait":1800},{"check":"overflow"},
            {"eval":"document.querySelector('main')?.innerText.slice(0,120)","log":name},{"shot":name}]
```

**View a page as another role**: write the session store directly, then reload: `localStorage.setItem('<prefix>:session', JSON.stringify({role:'tier1'})); location.hash='#/cockpit'; location.reload()`.

**Run the whole flow and poll**: click "run the whole flow", then "start demo", then read the playback capsule's text every 3 s (`[role=toolbar]` with the capsule's `aria-label`, 演示播放控制 in the examples), taking screenshots at key moments, until it shows "finished N/N" (已完成 N/N). Record the total time and each step's side effects, e.g. rule version +1, case library +1, a new result batch.

**Drive the director directly** (faster and more precise than clicking): import the app's own modules and keep them on `window`, then poll with synchronous expressions — a `waitFor` expression that returns a Promise is always truthy.

```js
(async () => { const urls = performance.getEntriesByType('resource').map((e) => e.name); const pick = (p) => urls.find((u) => u.includes(p)) || p;
  const d = await import(pick('/src/flow/director.ts')); const w = await import(pick('/src/flow/workflow.ts')); window.__d = d; window.__w = w;
  d.setFlowSpeed(2); await d.startFlow({ mode: 'auto', reset: true }); return 'started'; })()
```

Import the URL the page actually loaded (`pick`): after hot updates Vite serves changed modules as `…/director.ts?t=…`, and importing the bare path creates a **second module instance** — your calls then drive a director the page does not listen to, every step ends by the watchdog, and the run looks merely slow. Then wait with `{"waitFor": "window.__w.STEPS[window.__d.flowStore.get().idx].id === 'cook' && window.__d.flowStore.get().sub >= 2"}` and `{"waitFor": "window.__d.flowStore.get().status === 'finished'"}`, and in step mode call `window.__d.goToStep('<id>')` to choose parallel branches in an unusual order.

**Interaction scenarios**: `click` through `data-demo` targets step by step, with `wait` + `shot` after each.

**Animation smoothness** (consumer projects): sample frame intervals with rAF during a busy animation and report the share of frames over ~20 ms:

```js
await new Promise(r=>{const t=[];let p=performance.now();const f=n=>{t.push(n-p);p=n;t.length<180?requestAnimationFrame(f):r(t)};requestAnimationFrame(f)}).then(t=>({avg:t.reduce((a,b)=>a+b)/t.length,slow:t.filter(x=>x>20).length}))
```

Headless Chrome throttles rendering, so treat the numbers as a relative check; confirm visually with a screenshot sequence.

## 5. Checklist

### Every page

- No horizontal overflow, no console errors or uncaught exceptions.
- Main content visible above the fold. Titles not truncated, or truncated with a full-text tooltip.
- Dialogs, drawers and toasts stack correctly, and the dock stays visible while they are open.
- Opened as different roles, the menus, button permissions and data scope are correct.

### The time axis (P6 and every change after it)

- Timeline order: a run from the start enters steps in business-time order (no 12:05 step before an 11:53 one), cross-day steps show their day ("next day 02:00"), and the business times on nodes, swimlanes, navigator and capsule agree.
- At 2×, one click runs from the start to "finished N/N"; record the time (toB example: about 73 s for 10/10 steps), with no errors along the way.
- Step mode: branch choices are correct, i.e. after a step finishes the listed ready steps match the DAG.
- Jumps: starting from a middle step marks upstream steps as "assumed done" and the following order is sensible. After finishing, clicking a node replays it on its own and returns to "finished".
- Pause: press Space, click a node, wait 5 s — the sub-step doesn't change and the status stays "paused"; press Space again and the flow moves on.
- Speed: 0.25× and 2× both work, and changing speed mid-step takes effect immediately.
- Cursor: visible over buttons and above dialogs; its label isn't clipped near the viewport edge; hidden while a machine acts.
- Dock: dragging the top edge changes its height (record pixels before and after); maximize / collapse work, and after collapsing `--flow-dock-h` is 0; the capsule stays usable while a drawer is open.
- Leaving the page: switching pages while a step runs pauses automatically, and resuming re-executes that step.

### Appearance (palette × light / dark × style)

- `npm test` includes the appearance tests: contrast over every preset × mode × style and a few brand colors, and the source scan for raw colors outside islands.
- At 1920×1080, screenshot the main pages in at least: default light, one other palette, dark, dark + sharp + a brand color. Set the choice through localStorage (`<prefix>:theme`) and reload. Check: no white-on-white or dark-on-dark text, chips and tags readable, islands (phones, map, format samples) unchanged, the playback capsule and dock readable.
- Switch the appearance during a one-click run: playback continues, the cursor and the highlights stay visible.

### Data consistency

- List statistics match details, and page numbers match exported files.
- After a global rename or migration, grep to confirm the old names are gone (e.g. "the old organization name no longer appears in any page").
- Old localStorage data is cleared after a store version bump. To verify: write old-version data, reload, confirm the old key is gone.

### Before delivery (P5 and every major version)

- Preview the static build with `npm run build` + `npm run preview`, confirm chunked loading and relative paths work, and stop the preview process afterwards.
- README and docs match the pages (the docs sync test passes).
- `git status` shows no `refer/`, `dist/`, `.env` or real samples.

## 6. How to report evidence

Give numbers and observations, not just "verified". For example:

> `npm test` 56/56 (new: batch-level country consistency, publishing applies only confirmed changes); `npm run build` passes, first load about 105 KB gzip; headless Chrome at 1920×1080: 15 page states with no console errors, one-click run at 2× completes 10 steps in about 73 s; manually verified natural-language maintenance (3 changes → confirm all → new version).

Be honest about what you could not verify, e.g. "no real download was performed in the browser; export content is covered by unit tests".
