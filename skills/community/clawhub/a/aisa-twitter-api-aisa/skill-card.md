## Description: <br>
Twitter/X research, monitoring, watchlists, and OAuth-approved posting through AIsa for trend tracking, competitor monitoring, timeline analysis, relay-based reads, and OAuth-gated text or media posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research Twitter/X activity, monitor trends or competitors, and publish approved text or media posts through the AIsa relay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal command output may expose the AIsa API key. <br>
Mitigation: Avoid sharing command output, avoid running the skill in shared logs or CI, and rotate AISA_API_KEY if output may have been exposed. <br>
Risk: The skill can post externally to Twitter/X and upload selected media through the AIsa relay. <br>
Mitigation: Use only after explicit OAuth approval and only with media files the user selected for posting. <br>


## Reference(s): <br>
- [AIsa Twitter OAuth](references/post_twitter.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/aisa-twitter-api-aisa) <br>
- [AIsa Homepage](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OAuth authorization links, Twitter/X research summaries, posting status, tweet IDs, or tweet links when returned by the relay.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
