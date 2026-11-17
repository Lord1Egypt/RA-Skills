---
name: architect-project-state
description: Maintain a versioned, source-traceable architectural project brief, decision state, change log, open-question register, and bounded task pool. Use when ingesting design briefs, client meeting notes, consultant feedback, planning conditions, or later revisions; when updating project state without overwriting history; or when handing the project to another architect or Agent. Do not use merely to generate design ideas or imitate an architect's style.
---

# Architect Project State

Turn changing project material into controlled state. Preserve evidence, authority, versions, unresolved conflicts, and human responsibility.

Read [state-schema.md](references/state-schema.md) before creating or updating project-state files.

## Non-negotiable rules

1. Confirm the allowed project root before reading or writing. Stop if the root is missing, ambiguous, or broader than intended.
2. Read only task-relevant files inside that root. Never silently search neighboring projects.
3. Never overwrite a source file or prior state version. Write a new version and a separate change log.
4. Record the source before interpreting it. Preserve filename, source date, author or role, confirmation status, and exact locator.
5. Keep source observations, current project facts, calculations, interpretations, recommendations, decisions, questions, and actions visibly separate.
6. An unconfirmed note cannot become a confirmed decision. Compare authority only within the relevant decision domain; a source from one domain cannot silently replace a source from another.
7. Do not carry an Agent recommendation into the next version unless a named human approved it. Unapproved recommendations remain proposals.
8. Do not invent dates, owners, deadlines, design strategies, quantities, regulations, or client commitments.
9. Preserve uncertainty. Missing evidence is not negative evidence, and an unreadable or absent file is not proof that information does not exist.
10. Keep architect-controlled judgments, statutory sign-off, client commitments, and external issue actions behind explicit human confirmation.

## State classes

Assign every consequential item exactly one primary class:

- **Source observation** — an identified source contains this claim; this proves what the source says, not that the claim is current project truth.
- **Current project fact** — accepted as current only when source authority and confirmation status are sufficient.
- **Stakeholder statement** — attributed preference, request, or assertion; not automatically a decision.
- **Confirmed decision** — explicitly approved by an identified authority with a traceable record.
- **Provisional assumption** — temporary working premise with owner and expiry or confirmation condition.
- **Derivation** — transparent calculation from named inputs.
- **Professional interpretation** — architectural reading that requires expert review.
- **Recommendation** — proposed action or design direction awaiting approval.
- **Open question** — unresolved issue and the person or evidence needed to close it.
- **Bounded task** — authorized work with explicit inputs, outputs, owner, reviewer, and completion test.
- **Superseded item** — retained history that is no longer current; link to its replacement.

## Source authority: domain, status, and attribution

Do not force all sources into one global ranking. For every consequential source, record three dimensions:

1. **Authority domain** — statutory/regulatory, contractual, client/brief, discipline/professional, operational/user, or Agent-generated.
2. **Source status** — issued/approved, confirmed decision, circulated-unconfirmed, individual statement, provided-unverified, or Agent-generated.
3. **Attribution** — the named person, role, organization, team, or tool responsible for the claim.

Authority is evaluated inside its domain. A confirmed client preference does not override a statutory requirement; a planning condition does not prove an operational need; a consultant opinion does not become a client decision. Where two sources address the same domain and question, issue/confirmation status, date, scope, and authorized role help determine the baseline. Across different domains, preserve both and record the relationship or conflict.

Never infer `issued`, `approved`, or `confirmed` from a filename such as “task brief”, “minutes”, “final”, or “v0”. If neither the source nor the user establishes issue status, use `provided-unverified`.

Treat phrases attributed to a client, consultant, user, marketer, or designer as stakeholder statements unless an authorized decision record in the relevant domain confirms them.

When sources conflict, keep both, compare domain, status, scope, attribution, and date, then create an open question. Do not choose silently.

## Workflow

### 1. Establish the boundary

- Report the project root, permitted source files, intended outputs, and prohibited locations.
- Report whether the operation is create, update, compare, or handoff.
- Refuse fallback to a parent directory if project binding fails.
- An `update` must read the current state version and its change log. If access is not allowed, do not claim version continuity; label the operation `reconstruction` or `comparison` and identify the missing predecessor.

### 2. Register sources

- Assign stable IDs such as `S001`, `S002`.
- Record file, date, author or role, document status, and locator format.
- Flag impossible dates, missing versions, unreadable pages, and unconfirmed minutes without speculating about their cause.

### 3. Extract atomic claims

- Split compound sentences into independently testable claims.
- Preserve original wording for ambiguous client language.
- Attach a source ID and locator to every source fact and stakeholder statement.
- Do not convert words such as “希望”, “原则上”, “倾向”, or “可以研究” into requirements or decisions.
- Keep class and effective status consistent. A `Current project fact` cannot have `provided-unverified`, `unconfirmed`, `proposed`, or `contested` effective status; use `Source observation` or `Stakeholder statement` instead.

### 4. Validate definitions before calculating

Before comparing quantities, record:

- metric name and definition;
- unit;
- included and excluded scope;
- gross, saleable, net, above-ground, below-ground, or FAR status;
- applicable date and version;
- source authority.

If definitions are not compatible, label the result **comparison blocked by undefined scope**. You may show a conditional calculation, but do not declare a confirmed conflict.

Treat saleable building area, gross floor area, FAR-counted area, net area, and unit marketing area as incompatible by default. A product-area mix multiplied by unit count may be reported as a conditional arithmetic total, but it may not be described as exceeding, fitting, closing, or conflicting with FAR-counted area until a source defines the mapping and included scopes.

For percentages, check the sum. Never repair a percentage mix unless the user or an authorized source supplies the adjustment rule.

### 5. Update state

For each new claim, assign one operation:

- `ADD`
- `CONFIRM`
- `MODIFY`
- `SUPERSEDE`
- `CONTRADICT`
- `NO_CHANGE`
- `PROPOSED_MODIFICATION`

Show old value, new value, source, authority, effective status, downstream impact, and required confirmation. `CONFIRM`, `MODIFY`, and `SUPERSEDE` require a source with sufficient authority and effective confirmation. A lower-authority or unconfirmed source may only create `PROPOSED_MODIFICATION` or `CONTRADICT`; it must not replace the current baseline. Carry forward only confirmed facts, confirmed decisions, and explicitly labelled unresolved items. Keep recommendations in a separate proposal register.

Do not select a preferred, primary, or working metric from competing unconfirmed values. Keep all candidates unresolved until an authorized human or higher-authority source selects the baseline.

Close an open question only when the closing evidence has sufficient authority. Otherwise mark it `partially answered — confirmation pending`.

### 6. Create bounded tasks

Do not turn every issue into an action. For each authorized task, record:

- task ID and trigger source;
- objective;
- permitted inputs;
- expected output and output path;
- responsible owner and reviewer, or `unassigned`;
- completion test;
- blockers and stop condition;
- deadline status: confirmed, proposed, or unknown;
- external confirmation required.

If owner, deadline, or completion test is unknown, keep the task in `DRAFT`, not `READY`.

A task deadline cannot be more certain than its source. A date from an unconfirmed or contradicted record is `proposed` or `unconfirmed`, never `confirmed`.

### 7. Write new artifacts

Create a new project-state version plus a change log. Include:

- source register;
- confirmed facts and decisions;
- unconfirmed statements;
- assumptions and derivations;
- conflicts and open questions;
- proposal register;
- bounded task pool;
- superseded-item links;
- version metadata and next review gate.

Never replace the previous version. Re-read written files and report every path touched.

## Quality gate

Before finishing, verify:

- Every consequential claim has a class and source or is explicitly marked Agent-generated.
- No filename has been used as evidence that a source is issued, approved, or confirmed.
- Source observations have not been promoted to current project facts without sufficient authority.
- Any claimed update has actually read its predecessor; otherwise the artifact is labelled reconstruction or comparison.
- No unconfirmed meeting item is labelled decided, fixed, approved, rejected, or final.
- “Not recommended for large-area use” has not become “material rejected”.
- “No approval to sacrifice area” has not become “area loss prohibited”.
- No prior Agent proposal was inherited as project fact.
- Every numeric comparison uses compatible definitions or states why comparison is blocked.
- Saleable or marketing area has not been declared to exceed or close against FAR-counted area without an explicit mapping source.
- Dates distinguish source dates, event dates, proposed dates, and confirmed deadlines.
- Change operation, effective status, question status, and deadline status do not contradict one another.
- No unconfirmed metric has been selected as the primary working baseline by the Agent.
- Tasks without owner, output, and completion test are not marked ready.
- Original files and prior versions remain unchanged.

If any check fails, correct the artifacts before reporting completion.

## Stop and ask

Stop rather than infer when:

- project root or write target is unclear;
- a requested overwrite could erase project history;
- source authority or metric definition changes the conclusion materially;
- the user asks for external issue, client commitment, regulatory conclusion, or professional sign-off without identified approval.
