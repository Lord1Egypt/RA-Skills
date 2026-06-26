## Description: <br>
AI agent that manages ad campaigns across Google Ads, Meta Ads, LinkedIn Ads, and TikTok Ads through natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amekala](https://clawhub.ai/user/amekala) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External marketing teams, agencies, PPC specialists, and business operators use this skill to analyze campaign performance, research keywords, create paused campaigns, manage ad assets, optimize budgets, and prepare cross-platform reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can take high-impact actions in real ad accounts, including campaign creation, campaign updates, and budget-related changes. <br>
Mitigation: Verify the selected ad account, review proposed changes, require explicit user confirmation for write actions, and keep newly created campaigns paused until approved. <br>
Risk: Creative asset uploads can expose or publish user-provided public asset URLs to connected ad platforms. <br>
Mitigation: Provide only public creative URLs intentionally meant for upload, and validate assets before campaign creation. <br>
Risk: Incorrect campaign, targeting, keyword, or budget choices could waste ad spend or reduce performance. <br>
Mitigation: Use the skill's read-only analysis, keyword research, and validation steps before write actions, and do not retry failed campaign creation automatically. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/amekala/adspirer-ads-agent) <br>
- [Adspirer](https://www.adspirer.com) <br>
- [Adspirer Connections](https://adspirer.ai/connections) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with tables, command snippets, and ad-platform tool call requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may reference live ad account data and propose or request confirmed write actions against connected ad platforms.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
