## Description: <br>
Manually retrieves social-bookmark items, extracts linked article content, and performs keyword-based analysis for one-off personal organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manually collect social-platform bookmarks, extract linked article content, and save keyword-based analysis into a local personal knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive social-platform session credentials such as auth_token and ct0. <br>
Mitigation: Run in dry-run or test mode first, keep the .env file private, do not commit credentials, and provide tokens only after verifying the package and CLI being executed. <br>
Risk: The skill may fetch bookmarked third-party links and save extracted content locally. <br>
Mitigation: Review configured storage paths, keep local outputs protected, and inspect fetched content before relying on the analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/bookmark-smart-hub-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local JSON bookmark-analysis outputs in the configured storage directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
