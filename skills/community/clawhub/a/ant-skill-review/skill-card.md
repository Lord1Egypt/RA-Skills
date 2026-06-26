## Description: <br>
Skill Review scans Claude Code Skill packages for security risks before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antaisecuritylab](https://clawhub.ai/user/antaisecuritylab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit third-party Claude Code Skill packages for prompt injection, credential theft, data exfiltration, hidden backdoors, and supply-chain risk before installation or CI/CD approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The LLM-driven analysis path can run shell commands while reviewing untrusted skill packages. <br>
Mitigation: Install or run it only inside a disposable, network-restricted sandbox with no sensitive files or credentials beyond a limited model API key. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/antaisecuritylab/ant-skill-review) <br>
- [Publisher Profile](https://clawhub.ai/user/antaisecuritylab) <br>
- [npm Registry](https://registry.npmjs.org) <br>
- [PyPI](https://pypi.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Plain text security report or structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include layered findings, risk scores, an overall risk level, and an installation recommendation; output can be written to stdout or a file.] <br>

## Skill Version(s): <br>
1.0.2 (source: package.json and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
