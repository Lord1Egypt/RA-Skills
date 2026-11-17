---
name: fde-problem-discovery
description: "Stage 1 of FDE Delivery Loop. Turn customer interviews, frontline observations, tickets, meeting notes, and business data into an evidence-backed customer problem-discovery package. Use to uncover customer needs, reconstruct real workflows, design interview guides, validate problems, and screen POC candidates. Do not use to commit to a solution, write a PRD, or build a prototype."
---

# FDE Problem Discovery

Turn a verbal customer request into a bounded, handoff-ready problem worth testing. Do not rush into a solution.

## Accepted inputs

- Interview notes, transcripts, frontline observations, tickets, chat logs, or customer emails.
- Current workflows, sample data, metrics, and existing-system information.
- Customer ideas, complaints, or desired outcomes.

If the input is insufficient, ask no more than three critical questions and explain what each question is intended to validate. Do not assume the answers.

Use [references/discovery-input-guide.md](references/discovery-input-guide.md) to assess source reliability. When the material is extensive, do not summarize each document separately. Extract facts around `user → task → current state → pain → impact → constraint → evidence`.

## Method

1. **Collect evidence**: Separate customer statements, observable facts, inferences, and untested hypotheses.
2. **Reconstruct the current state**: Describe triggers, steps, roles, systems, manual actions, and breakpoints.
3. **Define the minimum valuable problem**: Identify affected users, frequency, business impact, current workaround, and cost of inaction.
4. **Assess POC readiness**: Confirm that the problem is real, material, testable within a limited time, and supported by necessary customer participation.

See [references/discovery-rules.md](references/discovery-rules.md) for decision rules, anti-patterns, and readiness scoring.

## Execution sequence

1. Inventory the material and label every item with source, date, role, and evidence level.
2. Extract the most recent real task before summarizing requested features.
3. Compare the prescribed workflow with the actual workflow; locate waiting, rework, errors, risk, and human judgment.
4. Interview users, accountable owners, and technical or risk stakeholders separately to expose conflicting perspectives.
5. Draft the problem statement, impact, and alternative explanations; actively seek disconfirming evidence.
6. Produce several POC candidates instead of assuming the first problem is the best one.
7. Use readiness scoring and hard gates to recommend proceed, gather evidence, or stop.

## Output modes

- **Material analysis**: Produce a discovery package from notes, tickets, or data.
- **Interview preparation**: Produce role sampling, questions, evidence targets, and a note-taking structure without prewriting answers.
- **Interview synthesis**: Merge several interviews and mark agreement, conflict, outliers, and open questions.
- **Field observation**: Focus on real actions, system switching, waiting, and manual fallback.
- **Problem screening**: Compare candidate problems by value, evidence, feasibility, and customer commitment.

## Question strategy

Prioritize behavior and evidence questions. Ask about outcomes and constraints only after understanding the current state. Never validate demand by asking, “Would you use an agent if one existed?” When a user cannot answer, request tickets, logs, sample documents, or a field observation instead of repeatedly rephrasing the same question.

## Interview principles

- Ask about the most recent real behavior and its evidence before asking abstract preferences.
- Understand the work and constraints before discussing a product or agent solution.
- Do not treat a customer suggestion as a requirement. Investigate the underlying job, motivation, and measure of success.
- Identify decision-makers, daily users, affected parties, and technical or compliance gatekeepers.

## Output

Use [references/problem-discovery-pack.md](references/problem-discovery-pack.md) to produce the **Customer Problem-Discovery Package**. Separate:

- Confirmed facts.
- Hypotheses requiring validation.
- The minimum problem recommended for the POC Charter.
- Problems to defer or reject, with rationale.

When designing interviews or decomposing complex needs, load [references/user-research.md](references/user-research.md) and [references/requirement-analysis.md](references/requirement-analysis.md) as needed. Use them only for discovery; they do not replace the POC Charter or PRD.

To generate consistent interview guides for several roles, run `node scripts/generate-interview-guide.js --input project.json --output interview-guide.md`. The script generates evidence-oriented prompts and note structures only. Adapt them to the industry, role, and existing evidence. Never treat generated questions or placeholders as discovery findings.

## Output quality gates

Before delivery, confirm that:

- At least one behavioral, observational, or data point supports the work; opinions alone are insufficient.
- The most recent real workflow can be reconstructed end to end.
- The problem statement does not contain a predetermined technical solution.
- Users, decision-makers, data or system owners, and risk gatekeepers are distinguished.
- Business impact is quantified, has a quantification plan, or explicitly states why measurement is not currently possible.
- Disconfirming evidence and alternative explanations are listed.
- The package recommends entering the POC Charter, continuing discovery, or stopping investment.

See [references/discovery-quality-rubric.md](references/discovery-quality-rubric.md) and [references/discovery-worked-example.md](references/discovery-worked-example.md) for detailed scoring and a complete example.

See [references/discovery-field-handbook.md](references/discovery-field-handbook.md) for enterprise interview sampling, observation, data analysis, and workshop operations.

For regulated or highly constrained contexts such as finance, healthcare, manufacturing, or enterprise support, load [references/industry-discovery-overlays.md](references/industry-discovery-overlays.md) as needed. Treat industry patterns as hypotheses, never as substitutes for customer-field facts.

## Boundary

Do not commit delivery scope, price, schedule, or technical solution in this skill. Route those decisions to `fde-engagement-charter` and downstream stages.

See [references/public-sources.md](references/public-sources.md) for public methodological sources.
