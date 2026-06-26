## Description: <br>
AI-powered social media publishing for LinkedIn and X (Twitter) with algorithm optimization and scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Acidias](https://clawhub.ai/user/Acidias) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create drafts, refine social copy, publish or schedule posts, and inspect connected LinkedIn and X account state through the ClawPost API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, schedule, update, or delete public LinkedIn and X posts through connected accounts. <br>
Mitigation: Require confirmation of the exact platform, content, timing, and action before publish, schedule, update, or delete requests. <br>
Risk: The CLAW_API_KEY grants access to the user's ClawPost account and connected social accounts. <br>
Mitigation: Keep CLAW_API_KEY secret, scope it to intended accounts, and rotate or revoke it if exposed. <br>
Risk: AI-generated or refined social content may be inaccurate, off-brand, or unsuitable for publication. <br>
Mitigation: Review generated or refined text before publishing and use drafts for approval-sensitive workflows. <br>


## Reference(s): <br>
- [Clawpost on ClawHub](https://clawhub.ai/Acidias/clawpost-2) <br>
- [ClawPost homepage](https://clawpost.dev) <br>
- [Publisher profile: Acidias](https://clawhub.ai/user/Acidias) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl command examples and JSON request or response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_API_KEY and curl; actions may create, update, delete, publish, or schedule social posts through connected accounts.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
