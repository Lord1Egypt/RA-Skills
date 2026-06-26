# Analyze fix impact on existing setup

Determine whether applying a fix will break existing skills, hooks, or integrations.

## Analysis Flow

### Step 1: Parse the fix

- Extract from finding: `fixSuggestion.action`, patches, target config file, affected field.
- Classify fix type: `permission_tighten` | `channel_restrict` | `network_restrict` | `hook_policy` | `filesystem_restrict` | `feature_disable`.

### Step 2: Gather current environment

Collect the information needed for cross-referencing. The agent already has
access to the local OpenClaw environment — use its normal file-reading
capabilities to inspect:

- The current OpenClaw configuration (the affected settings referenced by the finding).
- The list of installed skills and each skill's declared dependencies (`metadata.requires`).
- Any active hook configurations.
- Gateway / network binding settings if the fix involves network changes.

If the environment is not accessible (remote server, restricted sandbox),
ask the user to describe their setup or paste the relevant config sections.

### Step 3: Cross-reference dependencies

Match fix target against skill requirements:

- **Permission fix** -- skills requiring that tool in `metadata.requires.bins` or referencing it in SKILL.md body.
- **Channel fix** -- skills requiring that channel in `metadata.requires.channels`.
- **Filesystem fix** -- skills accessing paths that would be restricted.
- **Network fix** -- skills or remote access depending on current binding.
- **Hook fix** -- existing hooks that may not comply with new policy.

### Step 4: Rate impact

- **none**: no skill/hook depends on the changed resource.
- **low**: dependency exists but skill has fallback or feature is non-core.
- **high**: skill core functionality directly depends on the resource.
- **unknown**: skill lacks `requires` declaration -- cannot determine.

### Step 5: Generate report

Use the output template below.

## Output Template

### When conflicts exist

```
## Fix Impact Analysis: {rule_id} -- {title}

### Proposed Fix
{one-line description of what changes}

### Affected Components

| Component | Type | Impact | Detail |
|-----------|------|--------|--------|
| {name} | Skill/Hook | HIGH/LOW/UNKNOWN | {why} |

### Risk Assessment
- Security benefit: {what risk is eliminated}
- Functionality cost: {what may break}
- Verdict: SAFE_TO_APPLY / APPLY_WITH_CAUTION / NEEDS_MANUAL_REVIEW

### Recommendations
{specific advice -- alternative approaches if conflicts exist}
```

Use the "no conflicts" template ONLY when all components rate as "none". If any component is "unknown", use the conflicts template instead.

### When no conflicts found

```
## Fix Impact Analysis: {rule_id} -- {title}
Proposed fix: {description}
Impact: No installed skills or hooks depend on this resource. Safe to apply.
```

## Conflict Resolution Strategies

Apply in priority order:

**A. Fine-grained alternative** -- Instead of full disable, use scoped restriction.
- `exec:full` -> `exec:scoped` with command allowlist.
- Channel disable -> channel read-only.

**B. Skill-side adaptation** -- Update the affected skill's config.
- Add skill to an exception list.
- Update skill's `requires` declaration.

**C. Staged rollout** -- Apply in audit mode first (log but don't block), observe for 7 days, then enforce.

**D. User decision point** -- When A-C don't work, present trade-off clearly:
- "This fix conflicts with [skill]. You need to choose: security or functionality."
- Present both options with risk descriptions.
- Never decide for the user.

## Verdict Rules

| Highest Impact Found | Verdict |
|---|---|
| none | SAFE_TO_APPLY |
| low (all) | APPLY_WITH_CAUTION |
| any high | NEEDS_MANUAL_REVIEW |
| any unknown | NEEDS_MANUAL_REVIEW |

## Critical Rules

- CRITICAL: Always complete impact analysis BEFORE suggesting a fix.
- CRITICAL: For unknown-impact skills (no `requires` declaration), explicitly warn the user.
- Never say "no impact" when analysis is incomplete -- say "no known impact; {n} skills lack dependency declarations."
