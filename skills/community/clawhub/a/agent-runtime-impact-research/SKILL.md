---
name: agent-runtime-impact-research
slug: agent-runtime-impact-research
displayName: Agent Runtime Impact Research
description: >
  Research and analyze major Agent harness, runtime, coding-agent, skills,
  subagent, and plugin releases. Use when a model or platform launches an Agent
  execution layer and the user needs verified facts, architecture explanation,
  ecosystem impact, and implications for agent platforms and coding agents.
  Produces a fact table, runtime flow explanation, layered impact analysis,
  and a source register with judgment and evidence visibly separated.
  中文摘要：研究 Agent 运行时、编码代理、Skills、插件与子代理的重大发布。产出经核实的
  事实表、架构解析、分层影响分析与来源登记，判断与证据分离。触发词：Agent 运行时分析、
  Agent 发布影响评估、Harness 架构解读、插件生态影响.
description_zh: Agent 运行时影响研究
description_en: Agent Runtime Impact Research
version: "1.0.6"
agent_created: true
not_for:
  - Release news rewrites or short announcement summaries
  - Product tutorials, setup guides, or getting-started walkthroughs
  - Pure LLM model research with no runtime, harness, or agent-platform context
  - Vendor selection or purchase recommendations for agent products
---

# Agent Runtime Impact Research

## When to use

Use this skill when a user asks what an Agent harness or runtime release means, how it works, or how it changes coding agents, general agent platforms, Skills, plugins, subagents, evaluation, and enterprise adoption.

Do not use it for a short product summary, a pure tutorial, or a release-news rewrite.

## Steps

> This is a research-and-analysis skill; all steps are `[LLM]` except source retrieval which uses `[Deterministic]` search commands.

1. **[LLM]** Define the object precisely. Separate model, harness/runtime, product surface, skills, plugins, tools, agents, subagents, and connectors.
2. **[Deterministic]** Search current sources first. Prefer official release pages, repositories, architecture docs, papers, API docs, and maintainers' statements. Use reliable secondary sources only for details unavailable from first-party material.
3. **[LLM]** Build a fact table with date, release status, license, runtime architecture, supported modes, model/provider scope, session/logging, sandbox/security, extensibility, and known limitations. See `references/fact-table-schema.md`.
4. **[LLM]** Explain the runtime in a concrete flow: user intent → context assembly → model inference → tool calls → policy/approval → execution → session event log → resume/replay/evaluation.
5. **[LLM]** Explain the underlying architectural idea separately from product features. For plugin runtimes, distinguish temporal composition (load/unload/revert lifecycle effects) from spatial composition (dependency and service coordination).
6. **[LLM]** Compare the release with at least two relevant platforms, including an integrated product and an open or configurable runtime. For each comparison, separate confirmed facts from analytical judgment.
7. **[LLM]** Analyze impacts in layers per `references/impact-layers.md`: model economics, evaluation, runtime/platform competition, Skills and plugins, agent/subagent design, enterprise security/governance, and local/private deployment.
8. **[LLM]** For a named product, map the impact to user-visible platform layers: model routing, connectors, skills, agents, task orchestration, memory, approvals, auditability, artifacts, and ecosystem distribution. Do not infer private implementation details that are not available to the user.
9. **[LLM]** State what changes immediately, what may change over 6–18 months, and what remains uncertain. Include a counterargument and failure modes: preview instability, plugin dependency conflicts, supply-chain risk, log privacy, replay not equaling correctness, and model/runtime confounding.
10. **[LLM]** Deliver judgment first, then architecture, evidence table, layered impact analysis, platform comparisons, named-product implications, counterarguments and failure modes, and source register — matching all eight sections of the Output Format. Mark speculative claims as judgment or hypothesis.

## Hard Rules

1. Every specific number, date, license, version, or benchmark must have a first-party or reliable secondary source; unsourced fields are `unknown`, never invented.
2. Never turn a media interpretation into an official product claim; attribute interpretations as such.
3. Facts, observations, and judgments must be visibly separated in the output.
4. Current facts require current searches — no stale-knowledge assertions about releases.
5. Benchmark claims must be qualified by harness, mode, model version, and task set.
6. Distinguish "recorded" from "evaluated": an event log reconstructs execution but does not prove correctness.
7. Do not infer private implementation details that are not publicly documented.
8. Verify the release version and date under analysis before starting; assessing a stale release without labeling it misleads the impact judgment.

## Evidence and writing rules

- Current facts require current searches.
- A specific number, date, license, author, version, benchmark, or quotation must have a first-party or reliable secondary source.
- Never turn a media interpretation into an official product claim.
- Keep benchmark claims qualified by the harness, mode, model version, and task set.
- Distinguish "recorded" from "evaluated": an event log can reconstruct execution but does not prove correctness.
- Avoid claiming that a developer preview directly replaces an established product.
- Use concise Chinese with judgment first, evidence second, and boundaries explicit.
- Avoid marketing slogans and absolute competitive claims.

## Failure Handling

| Scenario | Action |
|---|---|
| No official first-party source exists yet | State clearly that the release is unverified; work only from the announcement and mark every architectural claim as inference |
| Conflicting sources | Present both with dates and confidence; do not silently pick one |
| Paywalled or inaccessible primary source | Use reliable secondary, mark the chain, and note what the primary would settle |
| Release is a preview with rapid churn | Freeze the fact table at a stated date; note that fields may be stale |
| Comparison target lacks public docs | Reduce to confirmed surface facts; mark deeper comparison as unavailable |

## Output Format

```markdown
# [Release] Impact Research

## 1. Judgment (three sentences: what it is, why it matters, what is unproven)
## 2. Architecture explained (runtime flow + composition model)
## 3. Fact table (per references/fact-table-schema.md)
## 4. Layered impact analysis (per references/impact-layers.md)
## 5. Platform comparisons (facts vs judgment separated)
## 6. Named-product implications (only publicly documented layers)
## 7. Counterarguments and failure modes
## 8. Source register (URL + date accessed + source tier)
```

## Pitfalls

- Treating Harness as another chat UI or assuming it is only a DeepSeek model client.
- Treating a plugin architecture as automatically secure, stable, or easy to govern.
- Equating Skills, plugins, MCP servers, tools, agents, and subagents.
- Claiming that open source guarantees ecosystem adoption.
- Using GitHub star counts as proof of production usage.
- Treating the paper's formal guarantees as proof that every production plugin is safe.
- Failing to disclose that a benchmark was run in a minimal or otherwise specific runtime mode.
- Comparing WorkBuddy, Codex, and Claude Code only by visible UI while ignoring execution, policy, storage, and ecosystem layers.
- Treating a GitHub Topic count such as `dsh-plugin` as a verified plugin count. Topic labels are self-declared discovery metadata; separate tagged repositories, installable artifacts, tested compatibility, and approved plugins.
- Treating a reported malicious-plugin incident as independently confirmed without a primary reproduction or reliable corroboration. Attribute it as a community/media report and label the evidence status.
- Claiming that CodeBuddy Security is already integrated with a plugin marketplace when official materials only document repository/archive scanning. Describe marketplace integration as a product design option unless an API or integration contract is verified.
- Assuming a portable `SKILL.md` makes the whole package portable. Re-check scripts, binaries, paths, credentials, network access, hooks, MCP configuration, runtime APIs, and OS dependencies.

## Verification

Before delivery, confirm:

- The release date and preview/stable status are sourced.
- The official architecture and license are sourced.
- At least one first-party source supports the core product description.
- At least two current platform sources support comparison claims.
- Every high-risk number or benchmark has a source and a qualification.
- Facts, observations, and judgments are visibly separated.
- A limitations section explains what the release does not yet prove.
- The final conclusion answers significance for the named platforms, Skills, and Agents rather than stopping at feature enumeration.
- No media interpretation is presented as an official product claim, and no speculative claim is left unmarked as judgment or hypothesis.
