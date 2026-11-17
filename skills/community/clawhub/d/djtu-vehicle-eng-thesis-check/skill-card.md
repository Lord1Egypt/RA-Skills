## Description:

Validates DJTU Vehicle Engineering thesis drafts in Markdown and guides creation of formatted .docx documents when invoked through the explicit /djtu-vehicle-eng-thesis-check command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingmaker9](https://clawhub.ai/user/lingmaker9)

### License/Terms of Use:

MIT-0

## Use Case:

External users preparing DJTU Vehicle Engineering theses use this agent skill to validate a Markdown draft against section, heading, caption, citation, reference, length, and glossary checks, then produce a formatted Word document for final review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to run local scripts that are not included in the artifact.

Mitigation: Review the installed package before use and only proceed when the referenced scripts and reference files are present and trusted.

Risk: The environment check flow can ask the user to run sudo package-manager commands.

Mitigation: Do not run sudo commands unless they exactly match an official package-manager install of pandoc from trusted repositories and have been independently reviewed.

## Reference(s):

- [Source repository](https://github.com/LingMaker9/djtu-vehicle-eng-thesis-check)
- [ClawHub skill page](https://clawhub.ai/lingmaker9/skills/djtu-vehicle-eng-thesis-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell command blocks and generated .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation warnings report line numbers without echoing draft content; generated Word documents require final manual review.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
