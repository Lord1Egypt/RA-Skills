# Claude Code — Harness Reference

Tool mappings for running the `design` skill inside Claude Code. Generic tools (Bash, Read, Write, Edit, Glob, Grep) are the same everywhere and not covered here.

## Tool map

| Capability | Claude Code tool |
|-----------|-----------------|
| Ask user questions | `AskUserQuestion` (up to 4 per call; answers returned inline) |
| Show file to user | `SendUserFile <path>` |
| Preview in browser | Claude Preview MCP — see "Preview & screenshot" below |
| Screenshot | `mcp__Claude_Preview__preview_screenshot` |
| Evaluate JS in page | `mcp__Claude_Preview__preview_eval` |
| Check console logs | `mcp__Claude_Preview__preview_console_logs` |
| Web fetch | `WebFetch` |
| Web search | `WebSearch` |

## AskUserQuestion

Use for: clarifying platform, design system choice, variations, reference screenshots.

```
AskUserQuestion([
  { question: "Which platform?", header: "Platform", options: [...], multiSelect: false },
  { question: "Use a brand design system?", header: "Design system", options: [...], multiSelect: false }
])
```

Answers return inline — ask once, then continue.

## Preview & screenshot

Always serve over HTTP first, then preview via MCP:

```bash
# Start server (reuse if already running)
python3 -m http.server 4311 --directory designs &
```

```
# Open in preview
mcp__Claude_Preview__preview_start { name: "designs" }

# Load the page
http://localhost:4311/<project>/preview.html

# Check for JS errors
mcp__Claude_Preview__preview_console_logs

# Take screenshot
mcp__Claude_Preview__preview_screenshot
```

Never open HTML via `file://` — multi-file prototypes (`.jsx` files loaded via `<script src>`) only work over HTTP.

**Preview gotchas with React + Babel:**
- `preview_click` does not reach React's delegated `onClick` (React 18 `createRoot` delegation). Use `preview_eval` instead: find the node, read `__reactProps$*` key, call `el[propKey].onClick(...)`.
- Global `keydown` listeners: `window.dispatchEvent(new KeyboardEvent('keydown', {key:'k', metaKey:true, bubbles:true}))`.
- Screenshot desyncs after `location.reload()` — use `preview_resize` to resync.

## Delivery

After verifying the design loads cleanly, deliver the five core files and acceptance evidence:

```
SendUserFile designs/<project>/preview.html
SendUserFile designs/<project>/annotated.html
SendUserFile designs/<project>/tokens.css
SendUserFile designs/<project>/spec.json
SendUserFile designs/<project>/assumptions.log
SendUserFile designs/<project>/preview.measure-report.json
SendUserFile designs/<project>/preview.measured.png
SendUserFile designs/<project>/acceptance.spec.mjs
```

Then surface the final screenshot and give the localhost URL so the user can open the prototype directly.

## Verification subagent (optional)

For thorough checks, spawn an `Agent` (type: `general-purpose`) with:
- The project directory path
- The served URL
- What to check (layout, interactions, spacing, etc.)

This keeps verification out of the main session context.

## Visual Critique Loop — L3.6 (required after every design generation)

This is the critical quality step. Use Preview MCP to see what Claude actually rendered,
then evaluate visually before delivering. No text rule can replace this.

**Sequence:**
```
1. python3 -m http.server 4311 --directory designs &   # start server

2. mcp__Claude_Preview__preview_start { name: "designs" }
   # navigate to http://localhost:4311/<project>/preview.html

3. mcp__Claude_Preview__preview_screenshot
   → NOW LOOK AT THE SCREENSHOT IMAGE
   → Do NOT review code. Review the pixels.

4. Ask yourself (from visual-critic.md protocol):
   - First word: "clean" or "busy"?  
   - Color count: ≤ 3 distinct colors in content?
   - Font sizes: ONE consistent size in tables/lists?
   - Dividers: invisible (barely there) or clearly solid?
   - Platform: compact controls or mobile-sized?

5. If any HIGH issue found:
   → Edit the HTML to fix it
   → mcp__Claude_Preview__preview_screenshot again
   → Confirm the fix is visually correct (not just syntactically correct)

6. Repeat until no HIGH issues. Max 3 iterations.
```

**Mental model shift:**
```
WITHOUT visual critique:  write CSS → "looks correct" → deliver
                          (developer mindset)

WITH visual critique:     write CSS → render → look → feel → fix → look again
                          (designer mindset)
```

The visual-critic.md file has the full evaluation protocol with specific questions
to answer and a priority system (HIGH / MEDIUM / LOW) for issues found.
