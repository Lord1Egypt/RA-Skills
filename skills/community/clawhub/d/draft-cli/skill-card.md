## Description: <br>
Manage InnoSage Draft pages and hosted Secret Shares using the @innosage/draft-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toliuweijing](https://clawhub.ai/user/toliuweijing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and authorized operators use this skill to manage Draft CLI page workflows, public review feedback, and hosted Secret Shares with explicit workspace anchoring and read-first guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft CLI actions can affect hosted pages, published links, Secret Shares, or credential configuration. <br>
Mitigation: Use the skill only when authorized, confirm the exact target and requested action before writes or sends, and keep read-only behavior as the default. <br>
Risk: The skill can involve sensitive credentials for Secret Share operations. <br>
Mitigation: Use runtime-provided secrets only when available, avoid exposing credential values in outputs, and verify authentication state before secret operations. <br>


## Reference(s): <br>
- [Draft Cli on ClawHub](https://clawhub.ai/toliuweijing/draft-cli) <br>
- [@innosage/draft-cli npm package](https://www.npmjs.com/package/@innosage/draft-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require the draft CLI, a JSON Workspace path, and authorized Secret Share credentials.] <br>

## Skill Version(s): <br>
1.9.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
