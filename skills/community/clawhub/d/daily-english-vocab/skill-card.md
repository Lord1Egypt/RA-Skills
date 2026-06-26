## Description: <br>
Daily English Vocab delivers scheduled daily English vocabulary and conversation lessons with small-talk practice, themed word lists, pronunciation, examples, and Chinese explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forkercat](https://clawhub.ai/user/forkercat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and agents supporting them use this skill to set up recurring bite-sized English lessons for everyday vocabulary, small talk, and Chinese-language explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring scheduled delivery can continue after the user no longer wants daily lessons or can target the wrong channel or recipient. <br>
Mitigation: Confirm the cron schedule, timezone, channel, and recipient chat ID before enabling it, and remove or disable the cron when daily lessons are no longer wanted. <br>
Risk: The skill keeps a local progress file to track lesson rotation and previously used words. <br>
Mitigation: Keep memory/english-vocab-state.json free of sensitive information and delete or reset it when clearing learning history. <br>


## Reference(s): <br>
- [Vocabulary Categories](artifact/references/categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown lesson text with an optional shell command for cron setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use memory/english-vocab-state.json to rotate categories and avoid repeated vocabulary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
