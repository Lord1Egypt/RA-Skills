## Description:

Generate, save, and modify GemDesign prototype pages via CLI. Invoke when user wants to create UI prototypes, design pages, or batch-generate pages from requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gemdesign-ai](https://clawhub.ai/user/gemdesign-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product teams use this skill to create or update high-fidelity GemDesign UI prototypes from requirements, preview them locally, and sync pages to a GemDesign account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify the local Node/npm environment by installing or updating the GemDesign CLI.

Mitigation: Install and pin the CLI version yourself before using the skill, and review global npm changes before allowing updates.

Risk: The skill may handle an authentication token for a GemDesign account.

Mitigation: Authenticate outside the chat when possible, use a narrowly scoped revocable token, and rotate the token if it is exposed.

Risk: The skill can start a local preview server, open a browser, and sync generated content to a remote GemDesign account.

Mitigation: Use it only in a workspace and account where those actions are expected, and review generated pages before relying on or sharing them.

Risk: Generated prototype pages may load third-party CDN scripts.

Mitigation: Avoid entering sensitive data into generated prototypes and review external script use before deployment or sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gemdesign-ai/skills/gemdesign-skill)
- [GemDesign platform](https://design.gemcoder.com)
- [Agent Skills open standard](https://agentskills.io)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML prototype code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local HTML prototype files and sync pages to a GemDesign account through the GemDesign CLI.]

## Skill Version(s):

0.1.11 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
