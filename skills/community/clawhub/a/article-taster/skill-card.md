## Description:

Article Taster evaluates Chinese articles for quality, article type, AI-generation signals, originality exemptions, and reading value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forealmy](https://clawhub.ai/user/forealmy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, editors, and external users can use this skill to triage Chinese articles before reading or publishing. It classifies articles, scores quality dimensions, highlights AI-writing signals, preserves spoiler-free novel analysis, and returns reading recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic AI and originality labels may be unreliable or overconfident.

Mitigation: Treat scores and labels as screening signals, not proof; keep human review in any consequential reading, publishing, or moderation workflow.

Risk: Large or untrusted article inputs can create reliability or hardening concerns.

Mitigation: Limit input size and run the skill in a controlled environment when exposing it to untrusted users.

Risk: Dependency behavior can change over time.

Mitigation: Pin and review Python dependencies before deployment.

Risk: Future external LLM scoring could transmit article text outside the local environment.

Mitigation: Enable any external LLM scoring only after clear disclosure and explicit approval for article text transmission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forealmy/skills/article-taster)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [JSON report and Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes article type, confidence, quality scores, AI-generation probability, originality label, reading advice, and optional spoiler-free detail.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
