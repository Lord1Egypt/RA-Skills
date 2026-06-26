# OpenClaw / portable import notes

This folder is a portable copy of the ACMG workflow skill.

What it is:
- A self-contained skill-like bundle with SKILL.md, templates, references, and a Python classifier script.

What it is not:
- Not confirmed as an automatically discoverable native OpenClaw plugin format.
- It may need to be copied into whatever shared skill directory your OpenClaw setup uses.

Ways to use it:
1. Manual use inside workspace
   - Read SKILL.md
   - Use templates/intake.md and templates/evidence-table.md
   - Run scripts/classifier.py on filled evidence counts

2. If your OpenClaw setup supports shared skills with SKILL.md
   - Copy this directory into that shared skills location
   - Reload/restart the agent

Validation command:
python3 scripts/classifier.py references/test_cases.json

Expected result:
- all 6 bundled test cases pass
