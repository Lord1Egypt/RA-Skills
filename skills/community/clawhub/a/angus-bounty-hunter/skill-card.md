## Description: <br>
Automated smart contract bug bounty hunting that scans Immunefi and Code4rena targets with Slither static analysis, triages findings with local LLMs, and prepares PoC investigation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chipp11](https://clawhub.ai/user/Chipp11) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Smart contract security researchers and developers use this skill to clone in-scope Solidity repositories, run Slither scans, and triage high- and medium-impact findings before deeper manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner can install and run code from untrusted target repositories on the user's machine. <br>
Mitigation: Run it only in an isolated container or VM with no host secrets, and review or remove npm and pip install steps before scanning untrusted repositories. <br>
Risk: Local LLM triage sends prompts and finding summaries to the configured local Ollama service. <br>
Mitigation: Treat prompts as shared with that local service and avoid sending confidential findings unless the local service is trusted. <br>
Risk: The artifact references a missing PoC template script. <br>
Mitigation: Do not fetch a replacement script from an untrusted source; create or review any PoC template locally before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON scan outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local scripts that clone target repositories, invoke Slither, and may query a local Ollama service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
