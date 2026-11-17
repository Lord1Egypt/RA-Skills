## Description:

Extracts factual claims from user input, checks them against web sources, and returns a baseline confidence score with source-aware guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crftsmnd](https://clawhub.ai/user/crftsmnd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill for initial claim verification, source comparison, and confidence-scored fact-checking when a user asks to verify or confirm a factual claim.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may frame heuristic baseline confidence as more definitive than the evidence supports, especially for sensitive or high-impact claims.

Mitigation: Use it for low-stakes initial review, preserve uncertainty language, cite both supporting and rejecting sources, and require independent review for sensitive claims.

Risk: The skill includes broad auto-triggers and repeated promotion of an external paid verification service.

Mitigation: Review prompts before deployment, disclose any external service handling, and remove or revise upsell language when neutral fact-checking is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crftsmnd/skills/baseline-rag)
- [Skill endpoint](https://omni-skills.cvapi.workers.dev/skill/baseline-rag)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown fact-check report with confidence score, source list, recommendation, and next-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses heuristic baseline confidence scoring with wide uncertainty bounds.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
