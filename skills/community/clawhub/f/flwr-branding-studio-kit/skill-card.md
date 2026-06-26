## Description: <br>
An advanced AI agent that acts as a Senior Brand Strategist. It automates project setup, applies elite market methodologies (Archetypes, StoryBrand, Personas), and generates structured brand assets while preventing hallucinations via strict context shielding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vansearch](https://clawhub.ai/user/vansearch) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Brand strategists, designers, marketers, and agency teams use this skill to scaffold client branding projects, organize client intelligence, and guide an AI assistant through RACE-based brand strategy work. It helps produce structured Markdown strategy assets such as Golden Circle, archetypes, personas, and tone of voice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client briefs, transcripts, emails, and proprietary brand plans may contain sensitive or confidential information. <br>
Mitigation: Use only authorized and minimized client materials, redact sensitive details where practical, and do not upload client data to external AI tools unless the client and organization permit it. <br>
Risk: The CLI creates local clients/<Client_Name>/ folders in the current workspace. <br>
Mitigation: Run the scaffold command only from a workspace where creating client project directories is expected. <br>
Risk: Publisher setup documentation discusses ClawHub tokens for release automation. <br>
Mitigation: Treat token setup as maintainer-only publishing guidance and keep any token in a secret store. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [RACE Framework](docs/race_framework.md) <br>
- [Prompt Guide Template](docs/prompt_guide_template.md) <br>
- [Branding Glossary](docs/branding_glossary.md) <br>
- [Reference Branding Prompt](docs/reference_branding_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local clients/<Client_Name>/ project folders and guides brand strategy outputs from user-provided client materials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
