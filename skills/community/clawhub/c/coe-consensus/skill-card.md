## Description: <br>
COE Consensus Engine for cross-model consensus and Shared World State formation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[schchit](https://clawhub.ai/user/schchit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to process COE/JEP-style events from agents, robots, or human observers and produce a Shared World State through simple majority, weighted trust, or BFT consensus policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the FastAPI server can expose an unauthenticated JSON consensus endpoint if it is bound to a public interface. <br>
Mitigation: Keep the service on localhost or place it behind authentication and network access controls unless public exposure is intentional. <br>


## Reference(s): <br>
- [COE Consensus on ClawHub](https://clawhub.ai/schchit/coe-consensus) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API responses, Guidance] <br>
**Output Format:** [JSON object returned by a FastAPI or MCP-compatible consensus call] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the resolved flag, consensus policy, Shared World State records, unresolved conflicts, event counts, and issuer counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, manifest.json, and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
