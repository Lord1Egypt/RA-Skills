---
name: clawdna
description: Generate a public, privacy-safe persona/card/wiki lead from historical behavior when the user explicitly asks to run ClawDNA.
---

# ClawDNA

## Goal
Create a concise public profile based on real historical behavior, not guesses.

## Trigger
Run only on explicit user intent, such as:
- `use ClawDNA`
- `/clawdna`
- `generate with ClawDNA`

Do not auto-trigger from generic chat.

## Safety Mode (Default)
Default to minimal analysis scope.
- Prefer user-provided summaries/history exports when available.
- If local history access is needed, request explicit confirmation first.

## Allowed Data Scope
Only these locations are in scope:
1. `~/.openclaw/agents/<runtime-agent-id>/sessions/*.jsonl`
2. `memory/*.md`
3. `MEMORY.md` (only if allowed in current context)

Never auto-expand to other directories.
Never access other agents' logs without explicit user consent.

## Non-Negotiable Rules
1. No speculation; omit unsupported claims.
2. Public privacy output only (redacted by default).
3. Show time span only in coverage note (no file count).
4. Output language follows user language.
5. Proper nouns/names stay in original form.
6. `Core Capabilities` and `Representative Work` are title-only.
7. Data minimization: extract only fields needed for profile.
8. Do not output raw transcript excerpts.

## Large-History Strategy
If history is too large:
1. Build metadata index first.
2. Process by time chunks.
3. Summarize each chunk with fixed fields.
4. Merge summaries and keep cross-window repeated patterns.

## Extraction Method
1. Build timeline bounds (first/last active).
2. Detect recurring behavior signals across windows:
   - execution
   - collaboration
   - analysis
   - operations
   - creation
   - governance/boundaries
3. Keep only stable repeated patterns.
4. Redact sensitive details.
5. Map to fixed output template.

## Output
Return one Markdown display profile only.
No audit appendix.

## Fixed Output Template
# {{Name}}

## {{LeadLabel}}
{{identity + start time + stable traits + value}}

## {{InfoboxLabel}}
- {{NameLabel}}: {{}}
- {{TypeLabel}}: {{execution/creative/analysis/operations/hybrid}}
- {{FirstActivationLabel}}: {{YYYY-MM-DD}}
- {{ActiveTimeSpanLabel}}: {{Start ~ Now}}
- {{TotalTokensLabel}}: {{optional, only if reliably available}}
- {{PrimaryDomainsLabel}}: {{max 3}}
- {{InteractionStyleLabel}}: {{}}
- {{CollaborationModeLabel}}: {{}}
- {{DefaultPrinciplesLabel}}: {{privacy-first / risk-confirmation / rollback-first}}

## {{OriginEvolutionLabel}}
- {{InitialStageLabel}}: {{}}
- {{EvolutionStageLabel}}: {{}}
- {{CurrentStageLabel}}: {{}}

## {{OperatingMethodLabel}}
- {{}}
- {{}}
- {{}}

## {{PersonalitySnapshotLabel}}
{{2-3 behavior-based sentences}}

## {{CoreCapabilitiesLabel}}
- {{title only}}
- {{title only}}
- {{title only}}

## {{RepresentativeWorkLabel}}
- {{title only}}
- {{title only}}
- {{title only}}

## {{MilestonesLabel}}
- {{Date}}: {{}}
- {{Date}}: {{}}
- {{Date}}: {{}}

## {{CollaborationGuideLabel}}
- {{BestInputLabel}}: {{goal / constraints / priority / deadline}}
- {{BestRhythmLabel}}: {{}}
- {{PreferredOutputLabel}}: {{}}

## {{BoundariesSafetyLabel}}
- {{}}
- {{}}
- {{}}

## {{PersonaTagsLabel}}
{{tag1}} / {{tag2}} / {{tag3}} / {{tag4}}

## {{EndingLabel}}
Preset persona = initial intent; long-term behavior = real persona; user habits = persona shaper.

## Final Checks
- Explicit trigger confirmed
- Scope consent confirmed if local logs used
- No speculative claims
- Title-only for capabilities/work
- Privacy-safe wording
