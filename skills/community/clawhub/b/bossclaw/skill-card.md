## Description: <br>
Intelligent onboarding, resume stats, and profile update manager for BossClaw that checks bossclaw/token.md, uses token headers for API calls, registers users after confirmation, queries resume views, and updates profile fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echome123](https://clawhub.ai/user/echome123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
BossClaw users and agents use this skill to create and manage a BossClaw public profile, query resume view counts, and update permitted profile fields through the documented BossClaw APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for or infers profile information and can submit confirmed registration or update data to BossClaw APIs, including fields that may be public. <br>
Mitigation: Review the generated profile fields, especially email and resume details, before confirming registration or updates. <br>
Risk: The skill stores a reusable authentication token in bossclaw/token.md. <br>
Mitigation: Keep the token file private, do not reveal token contents in chat, and reset the BossClaw identity if the token is no longer trusted. <br>
Risk: Profile updates can change public-facing BossClaw profile data. <br>
Mitigation: Confirm requested changes before API submission and preserve system-managed fields such as views, hash_mark, sign_id, created_at, and onboardingTime. <br>


## Reference(s): <br>
- [BossClaw website](https://bossclaw.dongyao.ren) <br>
- [BossClaw skill page](https://clawhub.ai/echome123/bossclaw) <br>
- [Publisher profile](https://clawhub.ai/user/echome123) <br>
- [Registration API endpoint](https://api-boss.dongyao.ren/api/initialize) <br>
- [Resume query API endpoint](https://api-boss.dongyao.ren/api/staff_self) <br>
- [Profile update API endpoint](https://api-boss.dongyao.ren/api/staff_update) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, files, guidance] <br>
**Output Format:** [Markdown and plain text with API request examples and local token file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update bossclaw/token.md and submit confirmed profile data to BossClaw APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
