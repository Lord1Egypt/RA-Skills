## Description: <br>
DeepSop TK工作台 guides an agent through DeepSOP Toby workflows for AI-generating TikTok videos, scheduling posts, and returning video performance metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuoai](https://clawhub.ai/user/kukuoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and marketing teams use this skill through an agent to turn natural-language TikTok campaign requests into DeepSOP Toby task submissions, scheduled publishing, and later performance summaries. It is intended for users who already have a DeepSOP API key and authorized TikTok accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit tasks that generate, schedule, and publish content to real TikTok accounts. <br>
Mitigation: Verify the selected TikTok account, generated prompt, privacy level, and posting schedule before task submission. <br>
Risk: The skill requires a DeepSOP API key and can interact with account balance or package purchase flows. <br>
Mitigation: Install only when the agent is expected to use the DeepSOP API key, and review any package or K-coin purchase choice before approving it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kukuoai/deepsop-tiktokflow) <br>
- [Publisher profile](https://clawhub.ai/user/kukuoai) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [DeepSOP platform](https://ai.deepsop.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPSOP_API_KEY and user confirmation before submitting TikTok posting tasks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
