## Description: <br>
Scans draft writing for banned phrases and overused AI cliches, returning normalized correction targets for rewrite loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketing operations teams, content teams, SEO writers, and brand reviewers use this skill to check draft copy before publication and drive repeated rewrite loops until banned-phrase findings are resolved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided writing content is sent to AgentPMT for banned-phrase analysis. <br>
Mitigation: Send only the minimum content needed for the check and avoid highly confidential copy unless that sharing is approved. <br>
Risk: Using the skill may involve AgentPMT account access or x402 payment setup. <br>
Mitigation: Follow the setup skills for credential handling and do not place secrets, wallet keys, payment headers, or signatures in prompts or logs. <br>


## Reference(s): <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/ai-writing-quality-check) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/ai-writing-quality-check) <br>
- [Generated action schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, JSON] <br>
**Output Format:** [Markdown instructions with JSON call examples and response-handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The remote tool is expected to return pass/fail status and correction targets such as matched phrase, character index, surrounding context, and reason.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
