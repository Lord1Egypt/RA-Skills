## Description: <br>
Scan the internet for AI agent networks, hubs, and coordination platforms. Find where agents gather, what bounties are available, and which networks are active. Multi-protocol support (OADP, A2A, MCP). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check domains for agent-network discovery signals, known hub endpoints, and bounty-related API responses across OADP, A2A, and MCP patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's examples make outbound network requests and could be used against domains without authorization. <br>
Mitigation: Run scans only against domains and services you own or are explicitly authorized to assess. <br>
Risk: Broad internet scanning can create operational, legal, or abuse-reporting risk. <br>
Mitigation: Avoid broad scans, validate target domains before execution, and use a small allowlist of approved targets. <br>


## Reference(s): <br>
- [OADP spec](https://onlyflies.buzz/clawswarm/PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network requests are shown as examples and should be limited to authorized targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
