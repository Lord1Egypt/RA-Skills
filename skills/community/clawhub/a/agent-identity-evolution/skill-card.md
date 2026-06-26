## Description: <br>
Watch your agent's identity evolve from its own experience through continuous discovery, genome snapshots, and growth tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to the Live Neon platform, sync experience sources, run identity discovery, review evolved beliefs and responsibilities, compare snapshots, and fetch evolved prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected source content and agent observations to Live Neon, where persistent identity data may be maintained. <br>
Mitigation: Use it only with content approved for Live Neon processing, and avoid private, regulated, customer, or credential-bearing material unless retention and deletion controls are confirmed. <br>
Risk: Externally generated identity prompts can influence future agent behavior. <br>
Mitigation: Require explicit operator approval before fetching, prepending, or otherwise applying evolved prompts to an agent runtime. <br>
Risk: Sync, discovery, observe, and consensus actions may process or derive new identity data without adequate consent boundaries. <br>
Mitigation: Require explicit approval before observe, sync, discover, or consensus actions, and review proposed beliefs and responsibilities before using them. <br>


## Reference(s): <br>
- [Live Neon Agent Platform](https://persona.liveneon.ai) <br>
- [Live Neon](https://liveneon.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/liveneon/agent-identity-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API request examples, JSON response examples, and configuration variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, a Live Neon API token, and explicit operator review before syncing content or applying externally generated identity prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
