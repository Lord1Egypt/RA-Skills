# Troubleshooting

Use this file when Chrome DevTools MCP browsing fails, partially fails, or behaves inconsistently.

## Error classes

### 1. Chrome not connected

Typical signs:

- `mcporter list --output json` does not show `chrome-devtools`
- MCP calls fail immediately because the browser cannot be reached
- no Chrome session / no tabs / no inspect bridge appears available

User-facing wording:

- “Chrome DevTools MCP isn’t connected to Chrome right now. Please open `chrome://inspect/#remote-debugging`, make sure remote debugging is enabled, then retry.”
- “I can’t reach Chrome from the MCP bridge yet. Please restart Chrome, confirm inspect / remote debugging is available, and I’ll continue.”

Remediation:

1. Run `mcporter list --output json`
2. If `chrome-devtools` is missing, tell the user to check Chrome remote debugging
3. Ask them to restart Chrome if needed
4. Retry `mcporter list --output json`
5. Resume normal browsing flow once `chrome-devtools` appears

### 2. Snapshot failed

Typical signs:

- `chrome-devtools.take_snapshot` errors
- snapshot returns incomplete / empty structure
- page is visibly open but no usable structure is returned

User-facing wording:

- “The page opened, but snapshot extraction failed on this attempt. I’m retrying once, then I’ll reopen the page if needed.”
- “The browser is reachable, but the page snapshot didn’t come through cleanly. I’ll retry the snapshot before escalating.”

Remediation:

1. Retry `take_snapshot` once immediately
2. If it still fails, verify MCP is still present with `mcporter list --output json`
3. If MCP is healthy, reopen the page with `chrome-devtools.new_page`
4. Retry `take_snapshot`
5. If repeated failures continue, tell the user the browser bridge is unstable and ask them to check Chrome

### 3. Tab lost / page context lost

Typical signs:

- a previously usable page/tab disappears
- click/fill operations fail because the page context is gone
- the selected page is no longer the expected one

User-facing wording:

- “The active page context was lost, so I’m reopening that page and resuming from the smallest safe step.”
- “That tab is no longer available through MCP. I’m recreating the page context now.”

Remediation:

1. Re-open the target page directly with `chrome-devtools.new_page`
2. Re-run `take_snapshot`
3. Resume from the smallest useful step rather than replaying the entire workflow
4. Close broken/unused pages if possible once the new page is ready

### 4. Interaction failed

Typical signs:

- click/fill/press actions fail on a valid-looking page
- target UID is stale after a page refresh or rerender
- element moved, re-rendered, or disappeared

User-facing wording:

- “That interaction target looks stale after the page updated. I’m taking a fresh snapshot and retrying with the current page structure.”
- “The page changed under us, so I need a new snapshot before repeating that action.”

Remediation:

1. Take a fresh snapshot
2. Find the current target again
3. Retry only the failed interaction
4. If the page keeps rerendering, prefer direct navigation or the smallest stable action

### 5. Google blocked / anti-bot / consent wall

Typical signs:

- captcha
- consent wall
- anti-automation interstitial
- search results unavailable despite page load

User-facing wording:

- “Google is blocked by a challenge/consent wall here, so I’m marking that leg blocked and continuing with X, then Reddit.”
- “Google didn’t yield usable browser-visible results because of anti-bot friction. I’m proceeding with the rest of the default search chain.”

Remediation:

1. Record Google as blocked
2. Continue directly to X search
3. Continue directly to Reddit search
4. Summarize with a note that the Google leg was unavailable

## Retry discipline

Default retry budget per failure:

- **1 immediate retry** of the same command
- **1 environment re-check** with `mcporter list --output json` if the retry fails
- **1 resumed attempt** using the smallest safe recovery step

Do not loop endlessly.

## Page hygiene

Close pages when they are no longer needed.

Example:

```bash
mcporter call chrome-devtools.close_page --args '{}' --output json
```

Guidelines:

- keep only the minimum number of pages open
- close each search leg after capturing what matters, unless comparison still requires it
- close broken or abandoned pages after recovery
- avoid leaving old Google/X/Reddit pages hanging around after the summary is complete
