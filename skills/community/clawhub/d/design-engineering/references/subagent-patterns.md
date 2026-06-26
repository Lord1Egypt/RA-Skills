# Sub-Agent Patterns for Design Work

## Dispatch Rules

### Context Budget
Sub-agents time out or produce poor output when given too much context. Rules:
- Extract the SPECIFIC code section into the task, not "read this 500-line file"
- If the file is >200 lines, paste only the relevant block + describe surrounding structure
- Include ONLY what the agent needs to make its change — not the full project history

### Task Specificity
- Name every file path explicitly **relative to the project root** (e.g., `src/components/Header.tsx`, not `/home/user/project/src/...`). If an absolute path is unavoidable, it must stay under the project root.
- Specify exact CSS class names, HTML structure to find
- Include before/after code when possible
- State the build/test command: `npm run build` or equivalent

### Parallel vs Sequential
- **Parallel**: Tasks that touch different files (CSS audit + content rewrite + OG images)
- **Sequential**: Tasks that depend on each other (content change → then style adjustment for new content)
- **Never parallel**: Two agents editing the same file → merge conflicts

### Model Routing for Design Tasks
| Task | Model |
|------|-------|
| Content writing, copy | Sonnet or Opus |
| CSS/styling changes | Sonnet |
| Complex JS (Canvas, animation) | Sonnet |
| Research/analysis | Sonnet |
| Quick config changes (version bump, path fix) | Sonnet |
| Creative direction, brand voice | Opus |

## Common Failure Modes

### 1. CSS ↔ JS Handshake Bugs
Sub-agents can't see across the boundary. If CSS expects `.ready` class and JS adds it, verify BOTH sides.

**Pattern**: After any sub-agent that touches both CSS and JS, grep for class names that appear in CSS selectors and verify they're toggled in JS:
```bash
grep -n '\.ready\|classList' file.js file.css
```

### 2. ES Module vs Script Tag
If JS uses `export`, it must load as `type="module"`. If loaded as regular `<script>`, `export` causes syntax error. Verify with:
```bash
node -e "new Function(require('fs').readFileSync('file.js','utf8'))"
```

### 3. Sub-Agent Forgets to Build-Test
Always include build command in the task. But also run it yourself after receiving output — sub-agents sometimes claim "build passes" when they didn't actually run it.

### 4. Resize/Viewport Assumptions
Sub-agents assume desktop. Always verify:
- Mobile viewport (375px width)
- Resize handling (does it regenerate state? Does it need to?)
- `prefers-reduced-motion` honored
