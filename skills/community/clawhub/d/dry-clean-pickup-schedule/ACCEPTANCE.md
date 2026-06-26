# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, API requirements, credential needs, or network requirements.
- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] Boundary excludes payment handling, refunds, billing disputes, damage claims, missing-item disputes, legal claims, account handling, and loyalty credentials.
- [x] Boundary keeps notes neutral and focused on scheduling, garment counts, pickup references, reminders, and what to bring.
- [x] Deliverable is a pickup tracker plus bag tag note template.
- [x] Workflow covers item recording, pickup date capture, neutral special notes, reminder text, bag tag template, confirm items, and after-pickup checks.
- [x] Slug matches the accepted design: dry-clean-pickup-schedule.

## Clean Scan Evidence

- SKILL.md: English only, no CJK/non-ASCII characters, no secrets, no credentials, no API keys, no tokens, no passwords, no personal data.
- skill.json: valid JSON, English only, all required safety fields present (hasExecutableCode: false, requires_api: false, no_network: true, no_credentials: true, no_code_execution: true).
- ACCEPTANCE.md: English only, no secrets, no executable content.
- Directory: exactly 3 files (SKILL.md, skill.json, ACCEPTANCE.md). No package files, scripts, binaries, .env, .git, node_modules, or hidden configs.
- No executable code, no network calls, no API dependencies, no credential requirements.

## Install-First Success Path

1. **Input:** User provides cleaner name, drop-off date, pickup date, ticket reference, garment categories, item count, neutral special notes, and reminder timing preference.
2. **Steps:** Skill produces an Order Snapshot with cleaner, dates, ticket, and item count; a Garment Tracker table; a Reminder Plan with day-before and day-of text; a What to Bring checklist; a Bag Tag Note Template; a Confirm With Cleaner list; an After-Pickup Checklist; and a Next Errand Note.
3. **Output:** A one-page dry-clean pickup schedule with all 8 sections that the user can print, save to notes, or share with a household member for pickup.
