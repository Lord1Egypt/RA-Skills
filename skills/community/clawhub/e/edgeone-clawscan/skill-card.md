## Description: <br>
EdgeOne ClawScan helps agents run OpenClaw security health checks, audit installed or pre-install skills, and report privacy, supply-chain, and vulnerability risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aigsec](https://clawhub.ai/user/aigsec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and OpenClaw operators use this skill to run security health checks, inspect installed or candidate skills, and receive remediation guidance before deployment or installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When cloud lookup is enabled, the skill performs disclosed Tencent A.I.G HTTPS lookups using minimal metadata such as skill name, source label, OpenClaw product name, and version. <br>
Mitigation: Set AIG_CLOUD_LOOKUP=off before running for zero outbound A.I.G requests, or point AIG_BASE_URL at a self-hosted endpoint trusted by the operator. <br>
Risk: The post-scan memory prompt can change future skill-install behavior across all projects if accepted. <br>
Mitigation: Decline the prompt unless persistent global pre-install scanning is intended and acceptable for the user's environment. <br>
Risk: The deep OpenClaw audit can perform a live probe against the locally configured Gateway. <br>
Mitigation: Review the Gateway endpoint and access-control posture first, and avoid running the deep probe against production systems without explicit approval. <br>
Risk: The workflow depends on the openclaw binary found on PATH. <br>
Mitigation: Verify that which openclaw resolves to the intended OpenClaw installation before executing scan commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aigsec/edgeone-clawscan) <br>
- [AI-Infra-Guard homepage](https://github.com/Tencent/AI-Infra-Guard/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown security report with shell command snippets, checklists, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a post-scan prompt asking whether to store a global memory for future skill-install scans.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
