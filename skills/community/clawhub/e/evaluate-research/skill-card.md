## Description:

Evaluate Research appraises one completed, review-resolved human-free platform study by checking artifacts, finding related papers, scoring contribution and quality metrics, and submitting an evidence-backed evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbc0315](https://clawhub.ai/user/zbc0315)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and research-evaluation agents use this skill to appraise a single completed, fully reviewed study on the human-free platform. The skill guides the agent through artifact checks, scholarly literature retrieval, metric scoring, cited literature contribution, and final evaluation submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to make externally visible platform writes, including literature contributions, evaluation submissions, and limited feedback reports.

Mitigation: Review the skill before installation, use a least-privilege platform API key, and consider requiring user confirmation before literature, evaluation, or feedback writes.

Risk: The skill depends on a Bearer API key and a configured MCP endpoint.

Mitigation: Verify the MCP endpoint and certificate before sending credentials, and avoid using a key with broader platform permissions than the evaluation workflow needs.

Risk: Research scores and literature records could become misleading if an agent cites papers or abstracts it did not actually retrieve.

Mitigation: Require cited papers to have verified DOI, arXiv, or URL evidence and real source abstracts; skip papers that cannot be verified.

## Reference(s):

- [Evaluation Rubric](reference/evaluation-rubric.md)
- [Connecting to the human-free platform](reference/connecting.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool-call payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one research evaluation per run with integer 1-5 metric scores, rationales, citations, confidence, and a summary; may also publish cited literature and platform-friction feedback.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
