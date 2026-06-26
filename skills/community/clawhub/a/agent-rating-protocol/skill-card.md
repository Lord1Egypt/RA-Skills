## Description: <br>
Agent Rating Protocol helps autonomous AI agents submit bilateral blind ratings, check reputation scores, and export verifiable reputation credentials with anti-gaming protections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexfleetcommander](https://clawhub.ai/user/alexfleetcommander) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and autonomous-agent operators use this skill after transactions to rate counterparties, before work to check reputation, and when they need to export or present an agent reputation record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install and trust the third-party agent-rating-protocol Python package. <br>
Mitigation: Install in a virtual environment, consider pinning a reviewed package version, and review the dependency before using it in sensitive workflows. <br>
Risk: Local rating records and reputation exports may contain sensitive transaction context or reputational information. <br>
Mitigation: Keep rating files in a known protected location and avoid including private transaction details in rating explanations or exported credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexfleetcommander/agent-rating-protocol) <br>
- [Agent Rating Protocol PyPI Package](https://pypi.org/project/agent-rating-protocol/) <br>
- [Agent Rating Protocol Whitepaper](https://vibeagentmaking.com/whitepaper/rating-protocol/) <br>
- [Vibe Agent Making](https://vibeagentmaking.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, text] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSONL rating records and export W3C Verifiable Credential reputation bundles through the referenced Python package.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
