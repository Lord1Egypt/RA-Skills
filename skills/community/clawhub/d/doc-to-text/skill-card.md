## Description:

Doc To Text helps agents extract readable text from .doc and .docx Word documents with MinerU, returning Markdown or JSON text fields for downstream reading and processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert Word documents into readable Markdown or JSON text fields for search indexing, NLP preprocessing, data pipelines, and document review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party CLI installed globally without a pinned version.

Mitigation: Pin and audit the CLI version before deployment, and install it in an isolated environment.

Risk: The evidence does not clearly explain whether local documents may be sent to MinerU/OpenDataLab services.

Mitigation: Avoid sensitive or confidential Word documents until the processing location and data handling terms are confirmed.

Risk: The skill requires a MinerU token for .doc files and full extraction flows.

Mitigation: Limit token scope and filesystem access exposed to the tool, and avoid sharing the token in prompts or logs.

## Reference(s):

- [Doc To Text on ClawHub](https://clawhub.ai/mzlzyca/skills/doc-to-text)
- [MinerU](https://mineru.net)
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU)
- [MinerU API Token Management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document content is emitted to stdout by default; progress and status messages are emitted to stderr.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
