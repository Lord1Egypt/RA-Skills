## Description:

Doc Extract helps agents extract text and content from Word .doc and .docx files into Markdown using MinerU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, assistants, and automation workflows use this skill to read Word documents from local files or URLs and convert their contents to Markdown for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents or URLs may be processed by an external MinerU service.

Mitigation: Avoid confidential, regulated, credential-containing, or internal-only documents and URLs unless MinerU/OpenDataLab data handling and retention terms have been reviewed and approved.

Risk: Installing the external mineru-open-api CLI may introduce supply-chain or environment risk.

Mitigation: Use a pinned, reviewed CLI version and install it in an isolated environment when possible.

Risk: Full extraction for .doc files and some .docx workflows require a MinerU token.

Mitigation: Store MINERU_TOKEN as a secret, avoid embedding it in prompts or files, and rotate it if exposure is suspected.

## Reference(s):

- [MinerU homepage](https://mineru.net)
- [OpenDataLab MinerU](https://github.com/opendatalab/MinerU)
- [MinerU token management](https://mineru.net/apiManage/token)
- [MinerU Ecosystem CLI source](https://github.com/opendatalab/MinerU-Ecosystem)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and extracted document text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document content is written to stdout by default; progress and status messages are written to stderr.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
