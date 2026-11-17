## Description:

Searches recent arXiv papers for a user-selected topic, prepares daily paper digests, and supports PDF-based deep analysis of selected papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[champagne315](https://clawhub.ai/user/champagne315)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to track recent arXiv papers in chosen categories, generate daily Markdown digests, and prepare deeper reports for selected papers from PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound arXiv and PDF requests can fetch external documents into the agent environment.

Mitigation: Run the skill with constrained network and file permissions, and review or add PDF URL and size checks before broad deployment.

Risk: Downloaded PDFs are cached locally under the configured PDF directory.

Mitigation: Use an approved cache location, limit access to the cache, and clear cached PDFs when they are no longer needed.

Risk: Editable prompt templates persist under the user's home directory and can change report behavior.

Mitigation: Review custom prompt templates before use, restrict prompt editing in shared agent environments, and reset prompts when output behavior is unexpected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/champagne315/skills/follow-arxiv)
- [Publisher profile](https://clawhub.ai/user/champagne315)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON command results and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese, English, and bilingual reports; writes intermediate paper data to local JSON files for agent reading.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
