# Feedback Log Format

**⚠️ Every time the user corrects your output (layout issue, wrong component,
spacing problem, etc.), you MUST log it to `feedback-log.md` before proceeding
with the fix (after user consent). Do not skip this step — the log is how the
skill learns and improves over time.**

Whenever the user corrects your generated output (with consent), log the
correction to `feedback-log.md` in the project root (create if it doesn't
exist). Each entry follows this format:

```
## YYYY-MM-DD HH:MM
- **Platform**: Android XML / Compose / SwiftUI / UIKit
- **Figma node type**: (e.g., FRAME with icon, Tab bar, Button group)
- **Issue**: Brief description of what was wrong
- **Before**: What the agent generated (snippet or description)
- **After**: What the user wanted (snippet or description)
- **Rule candidate**: (optional) If this correction suggests a general pattern rule, note it here
```

Log entries should be:

- **Concise** — only the relevant diff, not entire files
- **Categorized** — always include platform and Figma node type for later analysis
- **Actionable** — focus on the mapping error, not cosmetic preferences (e.g., "user prefers 16dp" is not a rule; "VECTOR compositions should be single ImageView" is)

Do NOT log:

- One-off personal preferences (specific color choices, naming conventions)
- Corrections to non-mapping issues (typos, import statements)
- Feedback the user explicitly says is project-specific, not general

Periodically (or when asked), run `scripts/feedback_analyze.py` to identify
patterns and generate rule candidates.
