## Description:

EvalLayer Evaluator sends text deliverables to the EvalLayer API to extract factual claims, score quality, and return structured JSON verdicts with pass/fail status, confidence scores, and payout recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanhall00](https://clawhub.ai/user/ryanhall00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to submit text deliverables to EvalLayer for factual-claim extraction, quality scoring, pass/fail verdicts, confidence scores, and payout recommendations in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted topics and deliverables are sent to EvalLayer and may be stored for aggregation.

Mitigation: Review content before submission and do not send secrets, regulated data, private customer data, or proprietary drafts without organizational approval.

Risk: The authenticated evaluation script requires an EvalLayer API key.

Mitigation: Use a dedicated API key and keep it in the EVALLAYER_API_KEY environment variable rather than embedding it in prompts, scripts, or deliverables.

Risk: Payout recommendations are advisory and the implementation submits evaluations as crypto_research tasks.

Mitigation: Treat scores and payout recommendations as one quality signal and review fit for the actual task before acting on results.

## Reference(s):

- [EvalLayer Evaluator Skill Page](https://clawhub.ai/ryanhall00/skills/evallayer-evaluator)
- [EvalLayer Evaluation API](https://api.evallayer.ai/evaluate)
- [EvalLayer Demo Evaluation API](https://api.evallayer.ai/demo/evaluate)
- [EvalLayer Intelligence API](https://api.evallayer.ai/intelligence)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evaluation responses include pass/fail status, quality and confidence scores, rationale, claim counts, payout recommendation, and evaluation ID.]

## Skill Version(s):

2.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
