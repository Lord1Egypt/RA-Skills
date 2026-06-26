## Description: <br>
Enterprise AI Agent Security Scanner - 846 rules, three-layer detection architecture, risk tier classification. Detects prompt injection, credential theft, data exfiltration, and attack chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caidongyun](https://clawhub.ai/user/caidongyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan AI agent skill directories for prompt injection, credential theft, data exfiltration, risky curl usage, and attack-chain indicators. It supports text or JSON security reports from a command-line scanner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed release may overclaim or incompletely ship the advertised scanner capabilities, rule database, or CLI entrypoints. <br>
Mitigation: Verify the installed package contains the expected rule database, scanner files, and agent-scanner entrypoint before using it as a security gate. <br>
Risk: Optional LLM analysis can send scanned code or configuration content to an external provider. <br>
Mitigation: Do not enable LLM analysis for private or secret-bearing repositories unless the provider, data handling, and credential exposure risks are acceptable. <br>
Risk: Scan findings are advisory and may miss issues or produce false positives. <br>
Mitigation: Use the scanner as one review input and keep human security review in the release process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caidongyun/agent-security-skill-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/caidongyun) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Gitee project link from artifact](https://gitee.com/caidongyun/agent-security-skill-scanner) <br>
- [GitHub project link from artifact](https://github.com/caidongyun/agent-security-skill-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command-line examples and optional text or JSON scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scanner can write JSON reports with --output json and --output-file; optional LLM analysis may send scanned content to the configured provider.] <br>

## Skill Version(s): <br>
6.2.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
