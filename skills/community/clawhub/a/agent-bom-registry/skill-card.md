## Description: <br>
MCP server security registry and trust assessment for looking up servers in the bundled metadata registry, running pre-install marketplace checks, batch fleet risk scoring, assessing skill file trust, and running SAST code scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to check MCP server trust signals, evaluate marketplace packages before installation, score server inventories, assess skill files, and run optional static analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install target is an external PyPI/GitHub package. <br>
Mitigation: Confirm that the operator trusts the package named agent-bom before installation. <br>
Risk: code_scan and skill_scan may read files selected by the user. <br>
Mitigation: Run scans only against intended paths and review the selected scope before execution. <br>
Risk: Optional Snyk enrichment uses a third-party network endpoint and requires SNYK_TOKEN. <br>
Mitigation: Use Snyk enrichment only when explicitly intended, keep SNYK_TOKEN in the operator environment, and avoid including token values in prompts or outputs. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/msaad00/agent-bom-registry) <br>
- [agent-bom project homepage](https://github.com/msaad00/agent-bom) <br>
- [agent-bom PyPI package](https://pypi.org/project/agent-bom/) <br>
- [OpenSSF Scorecard report](https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with command examples and scan results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include registry matches, risk scores, trust findings, verification results, and SAST findings for user-selected inputs.] <br>

## Skill Version(s): <br>
0.89.2 (source: artifact/SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
