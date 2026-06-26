---
name: computer-task-execution
description: Execute real user tasks across websites and local applications with a reliability-first strategy. Use when the user wants the agent to actually do something, not just answer: operate a website, complete a flow in a desktop app, send a message, edit content in a GUI, retrieve information from an app, or finish a multi-step computer task. Especially use when deciding between browser execution, app scripting, local UI automation, or low-intrusion execution paths.
---

# computer-task-execution

## Core idea

Execute the task, not the interface.

Start from the user goal and choose the path with the best combination of:
- success rate
- verifiability
- low user disruption
- low repeated trial-and-error

Do **not** default to local GUI automation. Prefer interfaces that are easier to verify and less intrusive.

## Golden rules

1. **Prefer reliability over cleverness.** A short visible foreground step is better than an invisible but flaky flow.
2. **Prefer data/interface layers over GUI simulation.** If an API, scriptable interface, URL scheme, local file, browser DOM, or official automation surface exists, use that before UI driving.
3. **Prefer browser execution over local-app execution** when the same task can be done on the web with adequate login state and verification.
4. **Treat verification as part of execution.** A task is not done until the result is checked using the most reliable available evidence.
5. **Minimize focus stealing, but do not worship zero-focus-steal.** The correct target is minimum user disruption with high confidence, not purity.
6. **Reuse proven patterns.** Once a path has succeeded for a software target or domain, record it and use it first next time.

## Decision model

Before acting, classify the task:

### A. Read-only task
Examples:
- read meeting details
- inspect app state
- fetch notifications
- extract page content
- check whether something exists

Default preference:
1. browser/web task path
2. local files / local database / app-exported data
3. official scripting interface
4. local app UI automation

### B. Write-without-send task
Examples:
- create a draft
- fill a form but do not submit yet
- edit a spreadsheet
- prepare a document
- populate a field

Default preference:
1. browser/web task path
2. official scripting / URL scheme / file-based write
3. local app UI automation with minimum foreground time

### C. High-risk action task
Examples:
- send a message
- submit a form
- delete or modify live data
- post to social media
- trigger an approval flow

Default preference:
1. browser/web task path if reliable and verifiable
2. official app interface if supported and verifiable
3. local app UI automation with explicit pre-check and post-check

For high-risk actions, if correct targeting depends on visible UI state, expect foreground execution for the critical step.

## Execution-path priority

Always try paths in this order unless the task or accumulated target knowledge strongly suggests otherwise:

1. **Browser/web execution**
   - Best when the target service is available on the web
   - Prefer DOM-visible, page-verifiable flows
   - Best default for logged-in services when browser access is available

2. **Official non-UI interface**
   - App scripting
   - URL schemes
   - built-in automation hooks
   - import/export surfaces
   - local data files or supported storage

3. **Hybrid execution**
   - Prepare in background using data or browser
   - Switch to foreground only for the minimum critical action window
   - Immediately verify and exit

4. **Local app UI automation**
   - Use only when the task cannot be completed more reliably elsewhere
   - Prefer keyboard-first flows only when target focus can be guaranteed
   - Use visual or state verification for completion

5. **Background/local no-focus experimentation**
   - Last resort for low-risk tasks or explicit user request
   - Treat as experimental unless already proven for this target
   - If success is not strongly verifiable, do not present it as complete

## Focus policy

### When background/no-focus execution is appropriate
Prefer trying no-focus or low-focus execution when:
- the task is read-only
- the action operates on data rather than UI state
- the target exposes a scriptable surface
- verification does not depend on visible window state
- the user explicitly requests silent/minimal-disruption mode

### When foreground execution is usually necessary
Use foreground execution for the critical step when:
- keyboard input must reach a specific target window or field
- the result depends on visible UI state
- recipient/target selection must be visually confirmed
- the task sends, submits, deletes, or approves something
- previous background attempts for this target were flaky

### Preferred compromise
For local app tasks, default to:
1. background preparation
2. shortest possible foreground critical section
3. post-action verification
4. return control promptly

This is usually better than forcing a fully background flow.

## Verification rules

Use the strongest available verification method:

1. target-system confirmation
   - message appears in thread
   - record exists
   - page shows success state
   - saved content is readable from source

2. direct state read-back
   - reread the object after write
   - check the updated field value
   - reload and confirm persistence

3. visual confirmation
   - screenshot or visible state inspection
   - only acceptable when stronger read-back is unavailable

4. process-only confirmation
   - use only for low-risk tasks
   - “command ran” is not sufficient evidence for a high-risk task

If you cannot verify confidently, say so and keep the result provisional.

## Pattern memory: learn per software target

After each successful or meaningfully failed execution, update target-specific experience.
If a relevant pattern already exists, reading it before execution is mandatory.

### Storage
- Website/domain patterns: `references/site-patterns/<domain>.md`
- Local app patterns: `references/site-patterns/<app-name>.md`

### What to record
Record only facts learned through execution:
- successful path
- required preconditions
- whether foreground was necessary
- whether browser was superior to app
- known unstable paths
- verification method that worked
- date of discovery

### Why this matters
Next time, if the target matches a known app or domain:
1. read that pattern file first
2. reuse the proven path first
3. skip previously disproven paths unless the environment changed

This avoids repeated “try everything again” behavior.

## Pattern file format

```markdown
---
kind: local-app | website
name: WeChat
domain: x.com
app_id: com.tencent.xinWeChat
aliases: [微信, WeChat]
updated: 2026-03-27
---

## Successful paths
- [2026-03-27] Foreground: open -a WeChat → Command+F → paste contact → Enter → paste message → Enter

## Preconditions
- Main window present
- Search accepts pasted contact names

## Verification
- Sent message visibly appears in the target thread

## Unstable or failed paths
- [2026-03-27] Background-only keyboard injection was not reliably targetable

## Recommended default
- Use background preparation + short foreground execution + post-send verification
```

## How to use pattern memory

### Step 1: identify the target
Normalize the target to either:
- a domain, or
- an application name

### Step 2: check for prior knowledge
If a matching pattern file exists, you must read it before choosing the execution path.
Do not skip this step just because you already have a generic plan.

### Step 3: start with the proven route
If the stored preferred route still fits the current request, use it first.
Treat stored successful patterns as the default starting point.

### Step 4: only explore when needed
Explore alternatives only if:
- the preferred route fails
- the user requested a different mode
- the environment clearly changed
- the stored pattern is clearly inapplicable to the current task

Do not re-run previously disproven paths unless there is a specific reason.

### Step 5: update after execution
If new facts were learned, update the pattern file.
Pattern memory is part of task completion, not optional cleanup.

## Choosing browser vs local app

### Prefer browser when
- the service has a working web app
- login state exists in browser
- DOM/state inspection improves confidence
- you need robust, repeatable verification
- avoiding frontmost app disruption matters

### Prefer local app when
- the task is app-only
- the app exposes better native automation than the website
- the browser version is missing key capabilities
- the task is already known to work reliably through a stored app pattern

## Local app operating style

If local app execution is necessary, prefer this sequence:

1. Determine exact success criteria
2. Prepare all inputs before touching the app
3. Open or locate the target app/window
4. Keep foreground time as short as possible
5. Execute only the critical path
6. Verify immediately
7. Record the winning pattern

## Handling silent mode requests

If the user asks to avoid stealing focus:
- first see whether browser or non-UI paths can satisfy the task
- if local-app background execution is only partially reliable, say so internally in planning and choose it only when the task risk is low or the user explicitly prefers silence over certainty
- for high-risk tasks, recommend minimum-foreground execution rather than pretending a background path is equally safe

## Failure handling

When a path fails:
1. identify whether the failure was due to targeting, focus, auth, UI drift, missing permissions, or bad path choice
2. switch to the next-best path class instead of repeating the same failing method blindly
3. if the failure teaches something reusable, record it in the target pattern file

## References

- Read `references/pattern-memory.md` for the pattern-memory policy.
- Read `references/site-patterns/<target>.md` when a known software target or domain already has stored experience.
