## Description: <br>
This skill should be used when the user asks to "implement LLM-as-judge", "compare model outputs", "create evaluation rubrics", "mitigate evaluation bias", or mentions direct scoring, pairwise comparison, position bias, evaluation pipelines, or automated quality assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karmaent](https://clawhub.ai/user/karmaent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and evaluation engineers use this skill to design LLM-as-judge systems, compare model outputs, create rubrics, choose metrics, and mitigate common evaluator biases in automated quality assessment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation prompts may ask judges for hidden chain-of-thought or more reasoning detail than the use case needs. <br>
Mitigation: Ask for concise evidence, rubric-grounded rationale, scores, and confidence; do not ask models to reveal hidden chain-of-thought. <br>
Risk: Evaluation data may include sensitive prompts, responses, or user context. <br>
Mitigation: Run sensitive evaluations only through approved model providers and pipelines. <br>


## Reference(s): <br>
- [Evaluating the Effectiveness of LLM-Evaluators](https://eugeneyan.com/writing/llm-evaluators/) <br>
- [Judging LLM-as-a-Judge (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685) <br>
- [G-Eval: NLG Evaluation using GPT-4 (Liu et al., 2023)](https://arxiv.org/abs/2303.16634) <br>
- [Large Language Models are not Fair Evaluators (Wang et al., 2023)](https://arxiv.org/abs/2305.17926) <br>
- [ClawHub skill page](https://clawhub.ai/karmaent/advanced-evaluation) <br>
- [Publisher profile](https://clawhub.ai/user/karmaent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with prompt templates, structured JSON examples, rubric patterns, and implementation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no code execution, tool calls, credential access, or hidden data access were identified by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
