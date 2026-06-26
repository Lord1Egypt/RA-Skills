## Description: <br>
Scaffolds new Aptos projects using npx create-aptos-dapp, supporting fullstack Vite or Next.js apps and contract-only templates with network selection and an optional API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to start Aptos dApps or Move contract projects from the create-aptos-dapp scaffold, choosing project type, framework, network, and optional API key setup before continuing into build, test, audit, deploy, and frontend integration steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent beyond scaffolding into tests, audit, deployment, frontend integration, and git operations. <br>
Mitigation: Confirm the exact project name, framework, network, and stopping point before execution; require explicit approval before deployment or mainnet use. <br>
Risk: Scaffolding uses npx to fetch and execute create-aptos-dapp. <br>
Mitigation: Review or pin the npx package before execution when supply-chain control is required. <br>
Risk: Generated .env values and optional Geomi API keys may be sensitive. <br>
Mitigation: Treat API keys and .env values as secrets, verify .env is ignored before git operations, and never display private keys. <br>


## Reference(s): <br>
- [Geomi](https://geomi.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and ordered setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project files by running create-aptos-dapp and related Aptos, npm, and git commands after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
