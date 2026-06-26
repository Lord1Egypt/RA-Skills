#!/bin/bash
# Clinical Tempo / ClawHub skill — lightweight prompt reminder (~50–100 tokens).
# Pair with Claude Code / Codex UserPromptSubmit hooks. See references/hooks-setup.md

set -e

cat << 'EOF'
<clinicaltempo-clawhub-reminder>
Before closing this task on Clinical Tempo:
- If you changed docs that feed the bundle: run `npm run build:llm` and verify `public/llm-full.txt`.
- If you debugged MPP/402/8787: add a one-line Success or Failure to `CLAWHUB.md` (no secrets).
- API smoke: `GET http://localhost:8787/api/dance-extras/live` → JSON `flowKeys` when server is up.
- Full orientation: `@` `public/llm-full.txt`; tribal notes: `CLAWHUB.md`.
</clinicaltempo-clawhub-reminder>
EOF
