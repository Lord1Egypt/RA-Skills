# Skill Authoring Anti-Patterns

## 1. Swiss-Army Skill

**Symptom:** Description covers many unrelated features. **Consequence:** Triggers on almost every conversation, wasting tokens and interfering with decisions. **Fix:** One Skill does one thing. Split into multiple Skills if functionality is broad.

## 2. Vague Description

**Symptom:** "Help with development", "Code assistant" — generic phrases. **Consequence:** Extremely high false-trigger rate; fails to trigger when actually needed. **Fix:** Description must include "what" + "when". ❌ "Help with development" → ✅ "Extract PDF text, fill forms. Use when handling PDFs."

## 3. Over-Prescription

**Symptom:** Every step locked down to exact commands and output wording. **Consequence:** Agent loses flexibility, gets stuck on minor deviations. **Fix:** Give direction, not scripts — list "what" (goals) not "how" (exact steps). Use "consider", "may" instead of "must".

## 4. Missing Gotchas

**Symptom:** Only documents happy paths, no known traps. **Consequence:** Agent repeats the same mistakes every new session. **Fix:** Add `## Gotchas` section. Format: problem → cause → solution. Update every time you hit one.

## 5. Monolithic File

**Symptom:** SKILL.md 2000+ lines. **Consequence:** Burns massive tokens on every activation, only 10% actually used. **Fix:** Split at >500 lines into `references/`; main file keeps skeleton + routing table.

## 6. Untested Description

**Symptom:** Ships without ever validating trigger accuracy. **Consequence:** Frequent false triggers or missed triggers in production. **Fix:** Test with 5–10 real prompts before shipping. Ensure relevant scenarios trigger, irrelevant ones don't.
