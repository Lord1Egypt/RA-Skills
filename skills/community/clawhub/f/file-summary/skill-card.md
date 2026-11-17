## Description:

Local document summary tool that extracts text from txt, docx, pdf, xlsx, and xls files and supports Chinese or English summary prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonthepro2012](https://clawhub.ai/user/leonthepro2012)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to extract local document content and request concise summaries through an OpenClaw LLM flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local documents selected by the user and pass extracted text into an LLM summarization flow.

Mitigation: Use it only with files approved for LLM processing, and prefer deployments that require explicit confirmation before reading or summarizing document contents.

Risk: The script may auto-install unpinned Python parser packages into the active Python environment.

Mitigation: Install reviewed, pinned dependencies through a controlled environment before use, or disable automatic package installation in managed deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leonthepro2012/skills/file-summary)
- [Publisher Profile](https://clawhub.ai/user/leonthepro2012)

## Skill Output:

**Output Type(s):** [Text, Analysis, Error messages]

**Output Format:** [Plain text content, concise summaries, or plain text error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports txt, docx, pdf, xlsx, and xls inputs; document content may be passed to the OpenClaw LLM summarization flow.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
