## Description: <br>
Connects OpenClaw to Dazzle so an agent can answer personalization requests using the signed-in user's Dazzle photo intelligence data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dazzle](https://clawhub.ai/user/dazzle) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to query the signed-in user's Dazzle photo intelligence for personal facts, memories, places, recommendations, and context-aware decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal privacy-sensitive inferences from the user's own photos, including places, relationships, routines, and preferences. <br>
Mitigation: Use narrow prompts and invoke Dazzle only when personalization from the user's photo context is needed. <br>
Risk: After browser sign-in, follow-up access can continue silently until the local MCP server is removed or the Dazzle grant is revoked. <br>
Mitigation: Remove the Dazzle MCP server or revoke the Dazzle grant when ongoing access is no longer wanted. <br>


## Reference(s): <br>
- [Dazzle](https://dazzle.ai) <br>
- [ClawHub skill page](https://clawhub.ai/dazzle/dazzle-photo-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON photo URL blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries can take up to 60 seconds; matched photos are returned as URLs rather than inline image bytes.] <br>

## Skill Version(s): <br>
0.1.9 (source: pyproject.toml and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
