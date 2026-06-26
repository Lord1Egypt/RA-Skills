## Description: <br>
Queries csfloat.com for data on skins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluesyparty-src](https://clawhub.ai/user/bluesyparty-src) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query CSFloat skin listings and prepare CSFloat marketplace API commands from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents a marketplace listing creation action that can affect a CSFloat account. <br>
Mitigation: Avoid create-listing commands unless you explicitly intend to post a listing and have verified the asset ID, price, and visibility. <br>
Risk: The skill requires a CSFloat API key. <br>
Mitigation: Install and use it only when you are comfortable giving the agent access to that API key. <br>


## Reference(s): <br>
- [CSFloat API documentation](https://docs.csfloat.com/#introduction) <br>
- [CSFloat profile API key setup](https://csfloat.com/profile) <br>
- [ClawHub skill page](https://clawhub.ai/bluesyparty-src/csfloat) <br>
- [Publisher profile](https://clawhub.ai/user/bluesyparty-src) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and CSFLOAT_API_KEY for documented command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
