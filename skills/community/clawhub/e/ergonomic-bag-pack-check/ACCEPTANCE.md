# Acceptance Criteria - Ergonomic Bag Pack Check

## File Completeness

- [ ] Directory exists at `~/.openclaw/skills/ergonomic-bag-pack-check`.
- [ ] `SKILL.md` exists.
- [ ] `skill.json` exists and parses as valid JSON.
- [ ] `ACCEPTANCE.md` exists.
- [ ] No other files are present in the skill directory.

## Metadata Compliance

- [ ] `skill.json` uses version `1.0.0`.
- [ ] `skill.json` uses license `MIT-0`.
- [ ] `skill.json` uses language `en`.
- [ ] `skill.json` sets `hasExecutableCode` to `false`.
- [ ] `skill.json` sets `promptOnly` to `true`.
- [ ] No handler, script, command, package, API credential, or executable entry point is declared.

## Content Quality

- [ ] The trigger is clear: a user carries a bag that feels heavy, awkward, or uncomfortable.
- [ ] The deliverable is clear: bag weight audit, fit checklist, repacking plan, and weekly reset routine.
- [ ] The workflow includes contents inventory, weight estimate, discomfort mapping, fit review, item removal or relocation, repacking, and a one-week test plan.
- [ ] The skill prioritizes practical carry changes over broad posture advice.
- [ ] The output preserves necessary medication, safety, accessibility, school, work, and weather items.
- [ ] The skill can handle backpacks, totes, purses, shoulder bags, messenger bags, rolling bags, and work bags.

## Safety Boundary

- [ ] The skill does not diagnose pain, posture conditions, nerve issues, injuries, or musculoskeletal disorders.
- [ ] The skill does not prescribe treatment, exercise, stretching, braces, medication, or therapy.
- [ ] Severe pain, numbness, tingling, weakness, injury signs, or persistent symptoms are routed to medical care or qualified professional evaluation.
- [ ] Discomfort notes use neutral, non-diagnostic language.

## Language and No-Code Compliance

- [ ] All content is English only.
- [ ] No CJK characters are present.
- [ ] No executable code is present.
- [ ] No API, network, credential, package, or script files are present.

## Clean Scan Evidence

- [x] No executable code, scripts, or binary files in the skill directory.
- [x] No API keys, tokens, passwords, secrets, or credentials present.
- [x] No network, API, or external service dependencies declared.
- [x] All content in English, ASCII-safe, no CJK or non-ASCII characters.
- [x] No PII, private data, or sensitive identifiers embedded.
- [x] Directory contains exactly 3 files: SKILL.md, skill.json, ACCEPTANCE.md.
- [x] No hidden files, temp files, logs, or build artifacts.
- [x] skill.json is valid JSON with document-only metadata.
