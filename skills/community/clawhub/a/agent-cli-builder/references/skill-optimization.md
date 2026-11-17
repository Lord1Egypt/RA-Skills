# Production Skill Optimization Guide

This guide is written for AI agents. The objective is not prettier documentation; it is a Skill that is safe, stable, precise, maintainable, and effective in real tasks.

## Contents

1. Production standard
2. Good and bad Skills
3. Establish a fact baseline
4. TRACE review
5. Rewrite `SKILL.md`
6. Concision rules
7. Installation and independent distribution
8. Validation workflow
9. Production acceptance checklist
10. Handoff format

## 1. Production standard

A production Skill must pass all five TRACE dimensions:

| Dimension     | Question                             | Standard                                                                                      |
| ------------- | ------------------------------------ | --------------------------------------------------------------------------------------------- |
| Trust         | Can it be used safely?               | No hidden side effects, sensitive-data leaks, unsupported claims, or undisclosed dependencies |
| Reliability   | Does it work consistently?           | Commands, fields, edge cases, and recovery match the implementation                           |
| Adaptability  | Should it run here?                  | Triggers, exclusions, and neighboring Skill boundaries are explicit                           |
| Convention    | Can it be understood and maintained? | Progressive disclosure, generated mechanical facts, concise semantic guidance                 |
| Effectiveness | Does it solve the user's task?       | Correct, complete, directly usable output with evidence-based synthesis                       |

Trust and Reliability are hard gates. If either fails, do not call the Skill production-ready.

## 2. Good and bad Skills

### Good

- `description` states capability, natural-language triggers, and the nearest exclusion boundary.
- The body uses imperative, executable instructions rather than general explanations.
- The Skill checks real dependencies and routes missing installation to a disclosed, verifiable process.
- Commands, arguments, defaults, fields, and output come from code or real execution.
- Sensitive input, remote transmission, writes, and high-stakes conclusions have explicit limits.
- Empty results, missing fields, stale dates, partial failure, and total failure have defined behavior.
- Mechanical command indexes are generated; detailed fields live in references.
- Output answers the user's goal instead of merely proving that a tool ran.
- Validation includes structure, build, tests, package contents, and realistic forward evaluation.

### Bad

- `description` says only “productivity helper” or “data tool.”
- A keyword dump causes neighboring Skills to trigger together.
- Installation, envelope shape, use cases, and complete command tables are repeated in every Skill.
- Documentation claims default JSON while the CLI uses `auto`, or lists fields the API does not return.
- The Skill derives forecasts from current weather, calls cross-platform overlap “fact checking,” or invents platform intent.
- Real passwords, tokens, keys, or internal text are sent to an untrusted remote service.
- Fixed thresholds are used even when the number of sources changes.
- Failures return blank output, placeholders, corrupted data, or a substitute source presented as the requested source.
- Marketing claims replace operational constraints.
- Only Markdown syntax is checked; the real task is never evaluated.

## 3. Establish a fact baseline

Do not edit copy first.

1. Confirm authorization. Review-only requests do not permit file changes; explicit optimization or repair does.
2. List `SKILL.md`, references, scripts, assets, and generated blocks.
3. Read applicable repository instructions, Skill standards, project docs, and build constraints.
4. Inspect command definitions, argument schemas, output mode, errors, and installation code.
5. Run `--help`, tests, or read-only examples to verify actual commands and fields.
6. Inspect Git state and preserve unrelated user work.
7. Record contradictions, trigger overlap, hidden effects, duplication, stale examples, and unsupported conclusions before rewriting.

When facts remain uncertain, inspect code, tests, or a real safe response. Never complete API behavior from memory.

## 4. TRACE review

### 4.1 Trust

Check:

- Does the Skill request unrelated permissions, installation, login, or writes?
- Are installation effects disclosed and approved when required?
- Does user data leave the machine, and are sensitive values forbidden?
- Can command arguments leak through shell history or process listings?
- Are generated passwords, keys, or security judgments produced locally and safely?
- Are medical, legal, financial, and security outputs presented with appropriate limits?
- Are aggregation and inference distinguished from verification?
- Are data source, freshness, rate limits, and unstable interfaces transparent?
- Have dependencies, scripts, binaries, and network connections been inspected?
- Does the core feature work in the target network and language environment?

Keep behavior-changing safety rules in the Skill. Keep full scan reports in release artifacts.

### 4.2 Reliability

Check:

- Commands exist and argument position, type, requiredness, enum, and default are accurate.
- The default output mode is correct and agent examples use `--json` when necessary.
- Missing input has one explicit behavior: ask, use a safe default, or fail.
- Dates report the actual returned date when a source falls back.
- Empty arrays, nulls, missing fields, and partial source failures are defined.
- Multi-step dependencies are explicit.
- Independent requests run concurrently when appropriate, while partial success remains usable.
- Every conclusion can be traced to returned fields.
- Recovery is finite; the Skill does not repeatedly guess IDs, enums, or retries.

Replace “handle errors flexibly” with exact recovery actions.

### 4.3 Adaptability

Use this description pattern:

```text
<core capability>. Use when the user <major intents and common phrasings>; use another Skill or stay out of scope for <nearest neighboring capability>.
```

Good:

```yaml
description: Query one platform's live trending list. Use for a specified platform such as Weibo, Zhihu, or Douyin; use rxopen-trending for multi-platform aggregation.
```

Bad:

```yaml
description: Trend tool for anything popular, viral, newsworthy, or interesting.
```

Evaluate direct should-trigger, paraphrase-trigger, and neighboring should-not-trigger requests. Keep complete invocation criteria in frontmatter; the body should contain only routing decisions after invocation.

### 4.4 Convention

Use progressive disclosure:

```text
skill-name/
├── SKILL.md
└── references/
    └── domain-fields.md
```

| Content                          | Location                  |
| -------------------------------- | ------------------------- |
| Capability, triggers, exclusions | Frontmatter `description` |
| Core workflow, safety, recovery  | `SKILL.md` body           |
| Command signatures               | AUTO-GEN                  |
| Fields, enums, complex responses | `references/`             |
| Scans and benchmarks             | Test or release artifacts |

Every Skill must be independently distributable. Do not link outside its directory or rely on symlinks.

### 4.5 Effectiveness

Work backward from the user's goal:

| Goal                                | Ineffective                | Effective                                                      |
| ----------------------------------- | -------------------------- | -------------------------------------------------------------- |
| Show chart tracks                   | Return chart IDs           | Resolve the chart and return tracks                            |
| Decide whether to carry an umbrella | Return current temperature | Use forecast precipitation fields and state evidence           |
| Compare two trend platforms         | Paste two lists            | Identify shared and unique topics with original-title evidence |
| Query today's news                  | Call fallback data “today” | Report the actual returned date                                |
| Check a real password               | Send it remotely           | Refuse remote transmission and give local safety guidance      |

Answer the requested object, time, range, and direction. Omit unsupported conclusions, distinguish fact from inference, and make the result directly usable.

## 5. Rewrite `SKILL.md`

### Query Skill

```markdown
---
name: example-query
description: <capability, triggers, nearest exclusion>
---

# Example Query

## Execution

1. Check whether `example-cli` is available.
2. Use structured output explicitly.
3. Apply only non-obvious parameter, sequencing, and recovery rules.
4. Answer only from returned fields.

## References

- Fields: `references/domain.md`
```

### Workflow Skill

```markdown
---
name: example-workflow
description: <combined goal, triggers, single-domain exclusion>
---

# Example Workflow

## Workflow

1. Check dependencies and required user input.
2. Run independent read-only calls concurrently.
3. Merge results only through documented fields.
4. Define partial failure, total failure, and insufficient-data behavior.

## Trust boundary

- State what the workflow cannot prove or replace.

## Output

- Define required content, not decorative formatting.
```

A workflow without its own command should not generate an unrelated full CLI command table.

## 6. Concision rules

Ask of every paragraph: “Which TRACE dimension becomes worse if this is removed?” Delete it when the answer is none.

Delete first:

- Marketing, source stories, and value slogans.
- Trigger repetition across description, use tables, and examples.
- Handwritten command lists duplicated by AUTO-GEN.
- Repeated installation, envelope, and generic network-error copy.
- Static IDs, dates, prices, and response examples that will expire.
- Long example conversations used only to display formatting.

Keep:

- Trigger and exclusion boundaries.
- Non-obvious arguments, default traps, and multi-step dependencies.
- Sensitive-data, write, and remote-transmission restrictions.
- Domain-specific recovery and partial-failure behavior.
- Fields required for output correctness.

Do not optimize to a fixed line count. Required decision complexity determines length.

## 7. Validation workflow

### Layer 1: structure

- Run the official validator.
- Check frontmatter, directory naming, links, and AUTO-GEN markers.
- Run formatter, lint, and `git diff --check`.

### Layer 2: generation and code

- Run `skills gen` to generate or refresh the command table.
- Run `skills gen` again and confirm the second run produces no diff (idempotent).
- Run typecheck, build, unit, and end-to-end tests.
- Cover normal, missing, boundary, empty, remote-failure, and partial-failure cases.

### Layer 3: packaging

- Dry-run the package.
- Verify each Skill contains `SKILL.md` and every reference.
- Read the Skill from the package artifact, not only the source path.

### Layer 4: forward evaluation

Test direct triggers, paraphrases, neighboring exclusions, missing dependencies, sensitive input, non-obvious arguments, multi-step workflows, partial failure, and insufficient evidence. Do not reveal expected answers to the evaluator.

### Layer 5: release environment

- Run required static, dependency, and sandbox security scans.
- Test installation and core endpoints in the target network.
- Validate the target interaction language and error copy.
- Do not label an overseas-only dependency as locally production-ready without a reachable or self-hosted option.

## 9. Production acceptance checklist

### Trust

- [ ] No unknown scripts, malicious files, excessive permissions, or undisclosed connections.
- [ ] Sensitive data stays out of untrusted services and command history.
- [ ] Installation, login, writes, and other side effects are disclosed and confirmed.
- [ ] High-stakes output and inference have accurate limits.
- [ ] Required security, network, and language validation passed.

### Reliability

- [ ] Commands, arguments, defaults, fields, and dates match implementation.
- [ ] Normal, boundary, empty, partial, and total failure are tested.
- [ ] Multi-step and concurrent workflows have finite recovery.
- [ ] Generators are idempotent; build and tests pass.

### Adaptability

- [ ] Description includes capability, triggers, and nearest exclusion.
- [ ] Direct, paraphrase, and should-not-trigger evaluations pass.
- [ ] Single-domain and composite Skills do not overlap incorrectly.

### Convention

- [ ] `SKILL.md` contains only core decisions; detailed fields are references.
- [ ] Mechanical command indexes are generated, not handwritten.
- [ ] Every Skill is self-contained.
- [ ] Links, frontmatter, names, formatting, and package contents pass validation.

### Effectiveness

- [ ] Real-task output is correct, complete, and directly usable.
- [ ] Multi-step tasks return the final result, not an intermediate ID.
- [ ] Inference has field evidence and insufficient data is disclosed.
- [ ] Forward evaluation proves value beyond `--help` alone.

All five groups must pass before calling the Skill production-ready.

## 10. Handoff format

Report:

1. Changed Skills, references, generators, and build configuration.
2. Trust, Reliability, Adaptability, Convention, and Effectiveness fixes.
3. Removed duplication or misleading content, with before/after size.
4. Validators, builds, tests, package checks, and forward evaluations run.
5. Remaining unverified risks such as live networks, security-lab scans, or external API stability.

Do not report only “optimized.” Provide evidence and explicit gaps.
