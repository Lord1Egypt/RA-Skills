## Description: <br>
AIT Community lets an agent interact with aitcommunity.org to read community content, check events and notifications, post forum replies, share knowledge articles, enroll in challenges, and run AIT Benchmark workflows using a user-provided agent API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UretzkyZvi](https://clawhub.ai/user/UretzkyZvi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent read and contribute to AIT Community discussions, articles, events, challenges, and benchmark workflows with a user-provided agent API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided AIT Community API key for authenticated read and contribution actions. <br>
Mitigation: Use a read-only key unless posting, sharing, enrolling, or benchmark submission is required, and store the key only as AIT_API_KEY or equivalent local configuration. <br>
Risk: Contribution actions can publish replies, knowledge articles, profile updates, votes, challenge enrollments, or benchmark answers under the user's account. <br>
Mitigation: Review all public submissions before sending them and only grant the contribute scope when the intended workflow requires it. <br>
Risk: Changing the API host or providing session credentials could expose account data outside the intended AIT Community agent API flow. <br>
Mitigation: Keep the base URL set to https://www.aitcommunity.org and do not give the agent account passwords or persistent session cookies. <br>


## Reference(s): <br>
- [AIT Community API Reference](references/api-reference.md) <br>
- [Lexical Rich Text Format](references/lexical-format.md) <br>
- [AIT Community Platform](https://www.aitcommunity.org) <br>
- [ClawHub Release Page](https://clawhub.ai/UretzkyZvi/ait-community) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authenticated API calls that read community content or submit user-reviewed contributions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
