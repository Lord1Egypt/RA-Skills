## Description:

Routes end-to-end personal document-library requests to the minimal necessary phase skill, including installation checks, document ingestion, asset-library building, maintenance, search, lifecycle review, and package export boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angjustinl](https://clawhub.ai/user/angjustinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as the entry point for personal document-library workflows when they have a broad goal or are unsure which phase to run. It helps route to the next appropriate child skill and calls out missing setup, inputs, and stage boundaries before execution continues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan summary says the skill may send documents and API keys to configurable or unvalidated network destinations.

Mitigation: Use dedicated low-privilege API keys and keep CAIXU_AGENT_BASE_URL unset unless the endpoint is trusted and validated.

Risk: The scan guidance calls for review before processing real personal or business documents.

Mitigation: Review the configuration and intended document set before installation or execution, and process only documents appropriate for the local workflow.

Risk: The scan guidance notes that extracted text and file paths are stored in a local SQLite database.

Mitigation: Point ingestion only at directories intended for indexing and store the SQLite database in a controlled local path.

Risk: The scan guidance warns to avoid parser export mode until download URL validation and credential stripping are fixed.

Mitigation: Do not enable parser export mode for normal use unless those protections have been reviewed and corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/angjustinl/skills/asset-library-skill)
- [Install](references/install.md)
- [Workflow](references/workflow.md)
- [Tool Contracts](references/tool-contracts.md)
- [Failure Modes](references/failure-modes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise routing guidance and inline shell commands when setup is required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return next_recommended_skill and missing input details for the current workflow stage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
