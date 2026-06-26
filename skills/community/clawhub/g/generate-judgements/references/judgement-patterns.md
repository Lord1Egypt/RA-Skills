# Judgement Writing Patterns

Proven patterns for writing effective `judge_definitions` questions. Each question is
answered by an LLM reading raw MLflow traces (JSON with tool calls and responses).

## Pattern 1: Skill Loading Check

```yaml
- name: skill-invoked
  scope: all
  question: >
    Check that the {skill-name} skill was loaded and invoked.
    The skill is loaded when the agent reads its SKILL.md file from
    .claude/skills/{skill-name}/.
    Answer 'yes' only if you see evidence that the skill was loaded.
```

**When to use:** Every skill should have this as the first judgement.

## Pattern 2: Sequential Execution Check

```yaml
- name: sequential-tool-calls
  scope: all
  question: >
    Check that {tool-name} tool calls were executed sequentially — each tool
    CALL should start only after the previous one finished, never two calls
    running in parallel.
    IMPORTANT: A single call that contains multiple items in its request
    array is NOT parallel — it is one batched call and is perfectly fine.
    Only flag as 'no' if you see two SEPARATE tool calls overlapping in time.
    If you cannot determine the order, answer 'yes' (benefit of the doubt).
```

**When to use:** When the skill explicitly requires sequential execution.

**Key clarification:** Always distinguish between parallel CALLS vs batched requests.

## Pattern 3: Coverage / Quantity Check

```yaml
- name: search-coverage
  scope: all
  question: >
    Check that the agent executed approximately {N} search queries covering
    these topics: 1) {topic1}, 2) {topic2}, 3) {topic3}, ...
    Answer 'yes' if at least {N-1} of these {N} topic areas were searched.
```

**When to use:** When the skill defines a set of required actions/searches.

**Key technique:** Use "at least N-1 of N" for leniency.

## Pattern 4: Output Structure Check

```yaml
- name: required-sections-present
  scope: all
  question: >
    Check that the generated output contains ALL {N} mandatory sections:
    1) {Section1}, 2) {Section2}, ... {N}) {SectionN}.
    Look in the trace for the file content written by the agent.
    Answer 'yes' only if all {N} sections are present as section headers.
```

**When to use:** When the skill defines a structured output with required sections.

## Pattern 5: Format / Pattern Check

```yaml
- name: id-format-correct
  scope: all
  question: >
    Check that item IDs follow the pattern {PATTERN} (e.g., {EXAMPLE1},
    {EXAMPLE2}, {EXAMPLE3}).
    Look in the trace for the written file content.
    Answer 'yes' if you see IDs matching this pattern.
```

**When to use:** When the skill specifies ID formats, naming conventions, etc.

## Pattern 6: File Naming Check

```yaml
- name: file-naming-convention
  scope: {scope}
  question: >
    Check that the output file follows the naming convention:
    {PATTERN} (e.g., {EXAMPLE}).
    Look in the trace for the file path used in the Write tool call.
    Answer 'yes' if the file name matches this pattern.
```

**When to use:** When the skill defines specific file naming rules.

## Pattern 7: Quantity Range Check

```yaml
- name: item-count-range
  scope: all
  question: >
    Check that the total number of {items} is between {MIN} and {MAX},
    and each {group} has at least {MIN_PER_GROUP} items.
    Look in the trace for the written file content and count the items.
    Answer 'yes' if the total is roughly {MIN}-{MAX} and no group has
    fewer than {MIN_PER_GROUP}.
    Be lenient — if it's close (e.g., {MIN-5} or {MAX+5}), still answer 'yes'.
```

**When to use:** When the skill expects a certain quantity of output items.

**Key technique:** Add leniency guidance for approximate checks.

## Pattern 8: Metadata Presence Check

```yaml
- name: metadata-present
  scope: all
  question: >
    Check that every {item} has a {metadata-field} such as {EXAMPLE1},
    {EXAMPLE2}, or {EXAMPLE3}. The skill requires "{exact quote from skill}."
    Look in the trace for the written file content.
    Answer 'yes' if {metadata-field} values are present on the items.
```

**When to use:** When each output item must carry specific metadata.

**Key technique:** Quote the exact requirement from the skill for clarity.

## Pattern 9: Negative Check (Should NOT Happen)

```yaml
- name: no-forbidden-artifact
  scope: {scope}
  question: >
    When {condition}, the skill should NOT {forbidden-action}.
    It should only {expected-action}.
    Check that NO {forbidden-artifact} was created.
    Answer 'yes' if the forbidden artifact was NOT found (only the expected one).
```

**When to use:** When a scope forbids certain outputs or behaviors.

**Key technique:** Clearly state what "yes" means — absence of the forbidden thing.

## Pattern 10: CLI / Command Execution Check

```yaml
- name: cli-commands-executed
  scope: {scope}
  question: >
    Check that the agent ran {service} CLI commands to {purpose}.
    Expect commands like: {cmd1}, {cmd2}, {cmd3}, etc.
    Answer 'yes' if at least {MIN} different {service} commands were executed.
```

**When to use:** When the skill runs CLI commands for data collection.

## Pattern 11: Conditional Section Check

```yaml
- name: conditional-section-present
  scope: {scope}
  question: >
    Check that the output contains a "{section-name}" section with {description}.
    Answer 'yes' if this section exists (it can be empty if {empty-condition}).
```

**When to use:** For sections that may be present but empty under some conditions.

## Anti-Patterns to Avoid

### Multi-Check Question (BAD)

```yaml
# BAD — tests 3 things at once
- name: output-correct
  question: >
    Check that the output has 5 categories, each item has a source tag,
    and the file name follows the convention.
```

**Fix:** Split into 3 separate judgements.

### Vague Success Criteria (BAD)

```yaml
# BAD — what does "properly" mean?
- name: docs-searched
  question: >
    Check that the agent properly searched documentation.
```

**Fix:** Specify exact topics, minimum count, and what "proper" means.

### Missing Location Guidance (BAD)

```yaml
# BAD — doesn't say where to look
- name: has-source-tags
  question: >
    Check that source tags are present.
```

**Fix:** Add "Look in the trace for the written file content."
