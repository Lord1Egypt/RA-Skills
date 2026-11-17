## Description:

Helps individual creators and small businesses prepare China copyright registration materials, classify work types, generate registration documents, and navigate process, cost, and timing considerations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, small businesses, and assisting agents use this skill to gather copyright registration details, prepare Chinese-language application materials, and generate Word document templates or document packages for review before submission.

### Deployment Geography for Use:

Global, with substantive guidance focused on China copyright registration workflows.

## Known Risks and Mitigations:

Risk: The skill can collect and persist personal identity, address, and contact details in generated Word files.

Mitigation: Use only with data the user intends to include in registration materials, store generated files in a controlled local workspace, and delete files containing ID numbers or addresses when no longer needed.

Risk: The artifact can automatically install an unpinned package if python-docx is missing.

Mitigation: Install dependencies explicitly in an isolated environment before use and review dependency resolution before running document generation.

Risk: Copyright process guidance, fees, and document requirements may become outdated or may not fit a specific legal situation.

Mitigation: Verify current requirements with the official registration platform and seek qualified legal review before submitting materials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/golngod/skills/copyright-registration-helper)
- [China Copyright Protection Center](https://www.ccopyright.com.cn)
- [China Copyright Registration Platform](https://register.ccopyright.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Structured Markdown guidance, JSON command results, and generated .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Word files are saved locally under an output directory and may contain personal identity or contact details supplied by the user.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
