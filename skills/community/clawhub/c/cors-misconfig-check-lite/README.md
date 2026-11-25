Analyze pasted CORS headers for dangerous combos — reflected origin + credentials, wildcard misuse, null origin. Offline, zero deps.

`curl -sI -H "Origin: https://x" <url> | node scripts/cors.js -`

Free lite version of `cors-misconfig-check` — the full skill ($15) adds live origin probing + preflight tests. Also in the `security-audit-bundle-8-skills` bundle ($29). See SKILL.md for agent workflow.
