## Description: <br>
Defines machine-readable service agreements for autonomous agents, including SLAs, quality thresholds, payment terms, escrow, and automated verification criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexfleetcommander](https://clawhub.ai/user/alexfleetcommander) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to define, negotiate, store, and verify service agreements before delegating work to other agents or resolving disputes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a third-party Python package and writes agreement records to local .jsonl files. <br>
Mitigation: Install only if you trust the referenced PyPI package, prefer a virtual environment or sandbox, and keep agreement files in a directory you control. <br>
Risk: Agreement records can include payment and escrow terms that may affect real agent transactions. <br>
Mitigation: Review payment, escrow, and release terms before relying on them for real transactions; the skill records terms but does not execute payments. <br>


## Reference(s): <br>
- [Agent Service Agreements on PyPI](https://pypi.org/project/agent-service-agreements/) <br>
- [Service Agreements Whitepaper](https://vibeagentmaking.com/whitepaper/service-agreements/) <br>
- [Vibe Agent Making](https://vibeagentmaking.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local agreement JSONL files and package installation steps.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
