## Description: <br>
AI Social Media Manager helps agents plan social media content calendars, recommend posting times, draft engagement replies, and summarize performance analytics across multiple platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operators, creators, ecommerce teams, and marketing agencies use this skill to generate content plans, choose publishing windows, draft replies, and review engagement metrics for supported social platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to place powerful social account credentials in TOOLS.md. <br>
Mitigation: Use scoped test accounts or a secret manager, avoid storing passwords, cookies, or production tokens in markdown, and rotate credentials after evaluation. <br>
Risk: Automated posting, replies, and bulk interactions can publish incorrect, off-brand, or policy-violating content. <br>
Mitigation: Require manual approval before any post, reply, or bulk interaction reaches a live social platform. <br>
Risk: The security verdict is suspicious because credential handling and automation risks are under-explained. <br>
Mitigation: Review the skill before installing and limit platform permissions to the minimum needed for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/ai-social-media-manager) <br>
- [API Documentation](src/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, CLI text, JavaScript objects, and JSON-like reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces content calendars, recommended posting times, generated replies, platform action results, and analytics summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, clawhub.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
