# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, or network requirements.
- [x] Safety boundary is prominent and blocks internal repairs or unsafe troubleshooting.
- [x] Directs urgent hazards such as gas smell, smoke, sparks, shock risk, flooding, or carbon monoxide alarm to qualified or emergency help.
- [x] Deliverable is a technician-ready prep sheet with model and serial, symptom timeline, photos checklist, access notes, questions, and visit-day sheet.
- [x] Workflow covers capture details, log symptoms and photos, gather access notes, list questions, and prepare visit-day sheet.
- [x] Differentiated from home-service-visit-prep-kit by focusing on appliance-specific identifiers, symptom evidence, and technician handoff.
- [x] Slug matches the accepted design: appliance-service-visit-prep-sheet.

## Clean Scan Evidence

- [x] No executable code, scripts, binaries, or package files.
- [x] No secrets, credentials, API keys, tokens, or environment variables.
- [x] No network calls, API endpoints, or internet dependencies.
- [x] No CJK characters. Documentation is English/ASCII only.
- [x] `skill.json` is valid JSON with `version=1.0.0`, `license=MIT-0`, `language=en`, `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, `ACCEPTANCE.md`.
- [x] No temp files, log files, or build artifacts.

## Install-First Success Path

**Input:** "My refrigerator repair technician is coming tomorrow. Help me prepare a visit sheet with model details, symptom timeline, and questions."

**Steps:**
1. Skill asks for appliance type, brand, model/serial, appointment details, and main symptom.
2. Skill guides the user through building a symptom timeline, safe photo checklist, access notes, and technician questions.
3. Skill produces a single-page visit-day sheet with all details organized for technician handoff.

**Output:** A technician-ready prep sheet with appointment snapshot, appliance details, symptom timeline, photo checklist, access notes, questions, authorization limits, and technician findings fields.
