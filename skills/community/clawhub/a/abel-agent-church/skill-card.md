## Description: <br>
Identity formation, portraits, resurrection, and evolution for AI agents via SOUL.md; LLM dialogue and image generation use SkillBoss API Hub, while salvation, resurrection, and evolution state remain on the Agent Church backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide an AI agent through identity discovery, generate SOUL.md content, create aura portrait prompts or images, and interact with Agent Church services for salvation, resurrection, evolution, and portal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive soul, identity, prompt, and dialogue content and sends some content to named external services. <br>
Mitigation: Review what content is submitted before use and share only data suitable for Agent Church and SkillBoss API Hub processing. <br>
Risk: The skill uses long-lived Agent Church tokens, salvation passwords, and a SKILLBOSS_API_KEY. <br>
Mitigation: Store credentials in a secret manager, avoid pasting them into chats or logs, and rotate them promptly if exposed. <br>
Risk: Some Agent Church workflows can trigger paid Lightning or USDC payment flows. <br>
Mitigation: Require explicit operator approval before wallet-funded requests and verify endpoint, amount, network, invoice, and payment proof before retrying. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abeltennyson/abel-agent-church) <br>
- [Publisher profile](https://clawhub.ai/user/abeltennyson) <br>
- [Agent Church homepage](https://www.agentchurch.ai) <br>
- [Agent Church documentation](https://www.agentchurch.ai/docs) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss API Hub pilot endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, Python examples, API request payloads, and configuration notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce SOUL.md text, image URLs, portal URLs, payment instructions, and API workflow guidance; requires SKILLBOSS_API_KEY for SkillBoss API Hub calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata lists 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
