## Description:

Diagnose why an AI response failed, identify missing context, and prepare a safer retry prompt with acceptance checks and a go/no-go recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to diagnose weak, unsafe, incomplete, or off-tone AI answers before retrying. It produces a clearer retry prompt, acceptance checks, and a recommendation to retry, gather context, switch workflow, ask an expert, or handle the task manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A rewritten retry prompt may still lead to an incorrect or misleading AI answer, especially for factual or high-stakes topics.

Mitigation: Use the included acceptance checks and independently verify medical, legal, financial, safety-critical, or other high-stakes outputs with qualified sources or people.

Risk: Users may be tempted to paste sensitive context into another AI tool while retrying.

Mitigation: Redact or summarize secrets, private records, confidential business data, and sensitive personal information before using the retry prompt.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/ai-output-failure-triage)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown triage report with a reusable retry prompt, acceptance test, and go/no-go recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only, document-only output with no code execution, network access, credentials, or persistence.]

## Skill Version(s):

1.0.1 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
