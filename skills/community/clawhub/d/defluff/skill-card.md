## Description:

Reverse the AI in corporate email by classifying authorship, guessing likely LLM prompts when AI was involved, classifying urgency, extracting actual intent, and naming common scam patterns across single emails, threads, and batches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yozaz](https://clawhub.ai/user/yozaz)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use Defluff to triage corporate email by separating action, response, FYI, and noise while surfacing likely AI-authored messages and scam indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email content may contain sensitive or confidential information that the configured OpenClaw model will inspect.

Mitigation: Install and use only when comfortable sharing the provided email content with the configured local model or agent environment.

Risk: AI-authorship labels, guessed prompts, urgency verdicts, and scam classifications can be wrong or incomplete.

Mitigation: Treat outputs as triage signals and verify important decisions before replying, paying, clicking links, or escalating.

## Reference(s):

- [Openclaw](https://openclaw.ai)
- [Openclaw skills docs](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured header lines and bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mirrors the input email language while keeping fixed line labels and verdict tokens in English.]

## Skill Version(s):

0.0.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
