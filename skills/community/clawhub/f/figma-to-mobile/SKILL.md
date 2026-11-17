---
name: figma-to-mobile
version: 2.3.0
requires: [Bash, Read, Write, Grep, Glob]
description: >-
  Convert Figma designs to mobile UI code (Compose/XML/SwiftUI/UIKit/Flutter)
  via the Figma REST API with local resource scanning, multi-frame comparison,
  and feedback-log corrections. Activate when a user provides a Figma link and
  asks for mobile layout code.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"], "env": ["FIGMA_TOKEN"] },
        "primaryEnv": "FIGMA_TOKEN",
        "permissions":
          {
            "network": [ "api.figma.com" ],
            "fs":
              {
                "read": [ "project root — for resource scanning (colors, strings, components)" ],
                "write": [
                  "project root — for generated UI code files",
                  "project root — for feedback-log.md (user consent required)"
                ]
              }
          },
        "install":
          [
            {
              "id": "python-requests",
              "kind": "shell",
              "command": "pip3 install requests",
              "label": "Install Python requests package",
            },
          ],
      },
    "resourceManifest":
      {
        "cpu": "low — short-lived CLI scripts",
        "memory": "low (< 512 MB)",
        "timeout": "30s per API request; 3 retries; ~2s min interval between requests",
        "network": [ "api.figma.com" ],
      },
  }
---

# Figma to Mobile

Convert Figma designs to mobile UI code with interactive clarification.

Supported: Android Compose, Android XML, iOS SwiftUI, iOS UIKit.

## Prerequisites

- `FIGMA_TOKEN` environment variable set (Figma > Settings > Personal Access Tokens)
  ⚠️ **Your Figma token is sensitive** — treat it like a password. Never paste it into chat
    messages (they may be logged). Set it via your shell rc file or OpenClaw env config.
- Python 3.8+ with `requests` package

## Trigger & Input

This skill activates when a user **explicitly asks to convert a Figma design to mobile UI code** and provides a Figma link. It does NOT activate on casual mentions of Figma links, pasted URLs in logs, or design references without a conversion request.

The user may also include **inline hints** alongside the link, such as:
- Target platform: "Android XML", "Compose", "SwiftUI", "UIKit"
- Layout preferences: "use ConstraintLayout", "prefer StackView"
- Component notes: "the switch is our custom CompactSwitch", "this is a dynamic list"
- Any other context about the design

**If the user provides hints, respect them and skip the corresponding questions.**
For example, if the user says "Android XML, the 3 cards are a RecyclerView list", do NOT ask about output format or whether the cards are dynamic/static.

## Not Applicable

This skill is NOT for:

- **Screenshot / image → code**: it works only with Figma design links via the Figma REST API, not with screenshots or image files.
- **Layout code without a Figma link**: generic "write me a login screen" requests have no design to interpret.
- **Casual mentions or pasted URLs without a conversion request** — see Trigger & Input above.
- **Pure design discussion or Figma feature questions**: no code is generated.

## Deliverables

After a successful conversion, the user receives:

- **Generated UI code files** — platform-idiomatic (Compose / XML / SwiftUI / UIKit / Flutter). Multiple files are presented with a clear filename header (see Step 3).
- **`scan-report.json`** — project resource scan results, only when the user agrees to a project scan (Step 2.5).
- **`feedback-log.md`** — correction log written to the project root, only with user consent (Step 4).

## Workflow

### Step 1: Fetch & Analyze

When user provides Figma link(s):

1. **Determine the input type:**

   **A. Link without specific node-id** (no `node-id`, or `node-id=0-1`):
   This link points to the entire page, not a specific frame. Tell the user:
   > This link points to the whole page. Please select the frame you want in Figma, right-click it, and choose "Copy link to selection", then send that link.
   > If you want to convert multiple frames, send multiple links.

   **B. Single frame link** (has specific `node-id`):
   ```bash
   python scripts/figma_fetch.py "https://www.figma.com/design/<fileKey>/<name>?node-id=<id>"
   ```
   → returns that frame's design data. Proceed to analysis.

   **C. Multiple links** (user sends 2+ URLs):
   Determine the relationship by frame names and user context: same-page
   states → `--compare` mode (multi-state code); parent+overlay → independent
   layout files; independent pages → fetch one at a time, ask which to convert
   first. If unsure, ask the user.

   **Detailed multi-frame rules**: Read `references/multi-frame.md`

2. **If the link has no specific node-id**, ask the user to re-copy from the specific frame (see A above). Do NOT call the API.

3. Analyze the structure: identify sections, repeated patterns, component types
4. Note INSTANCE nodes — they indicate reusable components. Check `variantProperties` for component state (e.g. State=Default, Size=Large) — these map to multi-state code
5. Note gradient/shadow data — flag for the user if complex
6. Apply Figma node interpretation rules before generating code

**Detailed interpretation rules**: Read `references/figma-interpretation.md`

### Step 1.5: Structure Summary

Before asking any questions, present a brief **structure summary** to the user so they can confirm your understanding:

> I see: [navigation bar with back button + title] → [2 content sections: user profile card, settings list (8 items)] → [bottom action button]. Total ~25 nodes.

Keep it to 2-3 lines. Mention:
- Major sections identified (nav bar, content areas, footer)
- Repeated patterns ("8 similar list items", "3 tab labels")
- Notable elements (gradients, complex illustrations, stacked cards)

If the user says "that's wrong" or corrects the structure, adjust understanding before proceeding to Step 2.

If the design has ≤10 leaf nodes (visible elements that map to actual views), skip this step — the structure is simple enough to proceed directly.

### Step 2: Confirm & Clarify

**Question priority (strict order — ask earlier questions first):**

1. **Output format** (MUST ask first unless user already specified)
   → Android XML / Compose / SwiftUI / UIKit
   This determines all subsequent analysis phrasing and code output.

2. **Structural ambiguities** (only ask what you're genuinely unsure about)
   → "These N items look similar — dynamic list or fixed layout?"
   → "This area: single image asset or icon-on-background combo?"

3. **Component choices** (only if platform-relevant)
   → "Any custom components to use? (otherwise I'll use platform defaults)"

**Rules for questions:**
- Skip any question the user already answered via inline hints
- Max 3-5 questions total, fewer is better
- Each question gives concrete options with one-line pros/cons
- Every question includes an open option: "or tell me more about this"
- Use natural language, no JSON or technical dumps
- If everything is clear (user gave full context + simple structure), skip Step 2 entirely

**Confidence guide — when to ask vs. when to just generate:**
- ≥3 sibling nodes with similar structure → likely a list → ASK (dynamic vs static)
- INSTANCE nodes sharing same componentId → reusable component → MENTION but can default
- Single clear hierarchy, no ambiguity → high confidence → SKIP questions, go to Step 3
- Gradient/complex shadow in design → MENTION in summary ("I see a gradient here, I'll approximate it as X")

### Step 2.5: Project Scan — Ask First

**⚠️ Always ask the user before scanning their project.** Scanning reads local files;
the user should know and agree.

> "你的项目在 /path/to/project 对吗？要不要我先扫描一下项目里已有的资源
>（颜色、文案、图片、自定义组件），这样生成代码时可以直接复用已有的东西？"

If the user agrees:

```bash
python scripts/project_scan.py /path/to/project --json --output scan-report.json
```

Then read `scan-report.json` and `references/scan-usage.md`.

If the user declines: proceed with hardcoded values per generation rules.

**How to present scan results** (with sample phrasing): Read `references/scan-usage.md`

**If no project path is known yet, don't scan.** Proceed with hardcoded generation.

### Step 3: Generate Code

After user confirms (or if no questions needed), generate code files.

**Detailed generation rules**: Read `references/generation-rules.md`

If multiple files are needed, output each with a clear filename header:
```
📄 activity_notification_settings.xml
[code]

📄 item_expert_notification.xml
[code]
```

### Step 4: Iterate & Capture Feedback

After showing code, ask briefly:
> Matches the design? Any adjustments?

**The user can then give feedback to refine the output.** Common iterations:
- "间距大了" → adjust specific spacing
- "Switch 换成我们的 CustomSwitch" → swap component
- "把标题栏去掉" → remove section
- "换成 Compose 版本" → regenerate in different format
- "颜色不对，这里应该是 #333333" → fix specific values

Continue iterating until the user is satisfied.

**Iteration output rule:**
- If the file has already been written to disk → read the current file, apply only the minimal patch, output just the changed lines with clear context (file path + line range). Do NOT regenerate the whole file.
- If the code only exists in the conversation (not written to disk) → output only the changed snippet with a comment indicating where it replaces (e.g., `// replaces lines 12-18 in activity_main.xml`). Do NOT repeat the entire file.
- Only regenerate the full file if the user explicitly asks (e.g., "重新生成完整文件", "show me the full file").

**⚠️ Before logging any feedback, tell the user:**
  > "I'll save this correction locally to `feedback-log.md` to improve future output.
  > It stores before/after snippets — is that OK?"
  Only proceed if the user agrees.

**⚠️ IMPORTANT: Every time the user corrects your output (layout issue, wrong component, spacing problem, etc.), you MUST log it to `feedback-log.md` before proceeding with the fix (after user consent). Do not skip this step — the log is how the skill learns and improves over time.**

**Feedback format, logging rules, and analysis**: Read `references/feedback-log.md`

## API Request Limits

The bundled `scripts/figma_fetch.py` enforces these limits automatically:

- **Timeout**: 30s per request
- **Retries**: up to 3 attempts on connection/SSL errors (backoff 5s/10s/15s)
- **Rate limit**: ≥2s between requests; on HTTP 429, wait per `Retry-After` header (cap 30s)
- **Adaptive depth**: refetches with deeper depth (up to 15) when children look truncated

When a rate limit is exceeded, the script reports:

```json
{
  "status": "error",
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Figma API rate limit exceeded",
  "retry_after_seconds": 30,
  "plan_tier": "FREE",
  "limit_type": "requests_per_minute"
}
```

## Error Handling

Quick reference — full details in `references/error-handling.md`:

- **FIGMA_TOKEN not set** (`FIGMA_TOKEN_NOT_SET`) → guide user to set env var; never paste token into chat
- **403/401** → token expired/revoked; regenerate in Figma Settings → Security
- **Invalid URL** → show valid format: `https://www.figma.com/design/<fileKey>/<name>?node-id=<id>`
- **API error / node too large / depth auto-increased** → see `references/error-handling.md`

## Tips

- **Token safety**: never paste `FIGMA_TOKEN` into chat — set it as an environment variable (see Prerequisites).
- **Rate limits**: keep ≥2s between Figma API calls; the script enforces this, so avoid parallel fetches to save time.
- **Multi-frame**: compare shared components across frames before generating code to avoid duplication.
