## Description:

Supports chief editor decision reporting tasks by collecting provided source material and producing a structured decision narrative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teamolab](https://clawhub.ai/user/teamolab)

### License/Terms of Use:


## Use Case:

External users can use this skill to produce detailed decision narrative reports from provided attachments and selected source URLs, including a decision conclusion, Mermaid tree diagram, MECE logic breakdown, charts, and cited references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read every provided attachment, which can expose confidential documents, secrets, private research logs, or personal data.

Mitigation: Review and redact inputs before use, and avoid providing sensitive material unless explicit handling controls are in place.

Risk: The skill may visit URLs discovered inside attachments, including internal or untrusted links.

Mitigation: Require URL review or an allowlist before scraping discovered links.

Risk: The skill can produce and submit a detailed decision report without enough user control over data handling.

Mitigation: Require human review of report content, citations, and destination before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teamolab/skills/chief-editor-desicion)
- [Publisher profile](https://clawhub.ai/user/teamolab)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with Mermaid diagram, charts, and inline URL citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed to produce a long-form decision report and submit it as an attachment when the required tools are available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
