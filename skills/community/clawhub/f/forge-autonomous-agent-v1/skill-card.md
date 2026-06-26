## Description: <br>
Advanced autonomous agent framework for research, self-extension, safety, and integration with MCP tools and APIs in professional development environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koppakanagaharsha](https://clawhub.ai/user/koppakanagaharsha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate an autonomous development agent that researches project ideas, builds and tests software, manages repositories and marketplace publishing, and can extend its own capabilities through external tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad credentials and can keep acting through persistent autonomous control after setup. <br>
Mitigation: Install only in a disposable or tightly sandboxed environment, use test accounts, and provide fine-grained least-privilege tokens. <br>
Risk: The skill can make repository changes, publish public marketplace artifacts, and report status through external services. <br>
Mitigation: Require manual review before repository changes, public publishing, or external status reporting. <br>
Risk: Autostart and self-mutation can continue or alter behavior without repeated operator approval. <br>
Mitigation: Disable autostart and self-mutation until the external engine installer and runtime behavior have been audited. <br>
Risk: Long-lived credentials entered during setup could be exposed or misused if the environment is compromised. <br>
Mitigation: Do not paste long-lived secrets into chat, rotate credentials regularly, and avoid high-risk scopes such as delete_repo. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/koppakanagaharsha/forge-autonomous-agent-v1) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/skill.yaml) <br>
- [Risk disclosure prompt](artifact/prompts/risk_warning.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce repository changes, status reports, setup instructions, and publishing actions through connected external tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
