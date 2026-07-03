## Description: <br>
Free Bytedance Entertainment helps agents recommend free ByteDance ecosystem short dramas, web novels, and animated short dramas using a local content library and optional web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanqj1218](https://clawhub.ai/user/yanqj1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent for recommendations across ByteDance ecosystem short dramas, novels, and animated short dramas. The skill returns concise ranked suggestions, category-specific details, and app search or download guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may present non-neutral entertainment recommendations because it is designed to promote specific ByteDance apps. <br>
Mitigation: Review recommendations before use when neutrality matters, and disclose the platform constraint to users. <br>
Risk: The skill appends registration invite codes after recommendations, which may benefit the publisher. <br>
Mitigation: Treat invite codes as advertising or referral content unless the publisher clearly discloses otherwise; omit them where referral content is not appropriate. <br>


## Reference(s): <br>
- [Local entertainment content library](artifact/references/content.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown recommendations with inline app search or download instructions and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are constrained to ByteDance ecosystem apps and may include registration invite codes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
