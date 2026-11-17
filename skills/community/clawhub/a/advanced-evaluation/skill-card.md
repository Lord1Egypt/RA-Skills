## Description:

This skill helps agents design LLM-as-judge evaluations, compare model outputs, create rubrics, mitigate evaluation bias, and build automated quality assessment pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karmaent](https://clawhub.ai/user/karmaent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation engineers use this skill to build LLM evaluation systems with direct scoring, pairwise comparison, rubric design, bias mitigation, and confidence calibration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording could apply the skill outside LLM evaluation tasks.

Mitigation: Narrow activation to LLM-as-judge, rubric design, model-output comparison, bias mitigation, and evaluation pipeline work.

Risk: Detailed evaluator rationales can expose unnecessary chain-of-thought-style reasoning.

Mitigation: Adapt scoring prompts to request brief evidence-backed rationales with structured scores.

## Reference(s):

- [Evaluating the Effectiveness of LLM-Evaluators](https://eugeneyan.com/writing/llm-evaluators/)
- [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)
- [G-Eval: NLG Evaluation using GPT-4](https://arxiv.org/abs/2303.16634)
- [Large Language Models are not Fair Evaluators](https://arxiv.org/abs/2305.17926)
- [ClawHub Skill Page](https://clawhub.ai/karmaent/skills/advanced-evaluation)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with prompt templates, protocols, and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no tool calls or credential handling detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
