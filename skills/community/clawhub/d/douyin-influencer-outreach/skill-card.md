## Description: <br>
Search for Douyin influencers matching criteria, review their content, avoid duplicate contacts, and draft or send personalized direct messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangtao19911111](https://clawhub.ai/user/wangtao19911111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketing and business operators use this skill to find small or mid-sized Douyin creators, check fit against follower and engagement criteria, and conduct personalized outreach while tracking prior contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates outbound promotional direct messages and broad recipient targeting. <br>
Mitigation: Review every generated message before sending, keep recipient counts low, and confirm that outreach complies with Douyin policies and applicable marketing rules. <br>
Risk: The workflow stores contacted creator information and message content in a local CSV file. <br>
Mitigation: Limit the logged fields to what is necessary, protect the workspace, and periodically purge recipient records that are no longer needed. <br>
Risk: The dependency declaration allows any OpenClaw version. <br>
Mitigation: Pin or update the OpenClaw dependency to a reviewed version before using the skill in a production workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangtao19911111/douyin-influencer-outreach) <br>
- [Publisher Profile](https://clawhub.ai/user/wangtao19911111) <br>
- [Douyin Search URL Pattern](https://www.douyin.com/jingxuan/search/{keyword}?type=general) <br>
- [Douyin Creator Profile URL Pattern](https://www.douyin.com/user/{sec_uid}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with browser actions, JavaScript snippets, shell commands, and CSV records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces personalized outreach message text and local contact-tracking entries; user confirmation is required before sending messages.] <br>

## Skill Version(s): <br>
2.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
