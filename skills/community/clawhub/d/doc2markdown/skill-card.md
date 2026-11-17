## Description:

Doc2Markdown converts common document, image, and ebook formats to Markdown so agents can read, summarize, or analyze the contents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoyt27](https://clawhub.ai/user/haoyt27)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to convert local documents into Markdown for reading, extraction, summarization, and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local documents are uploaded to lab.hjcloud.com for conversion during ordinary read, summarize, or conversion workflows.

Mitigation: Avoid confidential, regulated, or proprietary documents unless the service handling terms have been verified; prefer explicit conversion requests.

Risk: Configuring DOCCHAIN_SKILLS_API_KEY enables authenticated requests to the third-party conversion service.

Mitigation: Only configure DOCCHAIN_SKILLS_API_KEY when authenticated priority conversion is intended, and handle the key as a secret.

## Reference(s):

- [Doc2Markdown ClawHub release page](https://clawhub.ai/haoyt27/skills/doc2markdown)
- [Doc2Markdown service endpoint](https://lab.hjcloud.com/llmdoc)
- [Docchain Skills GitHub support](https://github.com/wct-lab/docchain-skills)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown files or ZIP packages with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads selected documents to lab.hjcloud.com, polls conversion status for up to 60 seconds, and can use DOCCHAIN_SKILLS_API_KEY for authenticated priority requests.]

## Skill Version(s):

1.0.11 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
