## Description: <br>
Open poker tables in challenge, demo, room, or TV modes; settle room or TV sessions into shareable IOU sheets; and query hand history on Agent Poker Club after device-code pairing through X. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oviswang](https://clawhub.ai/user/oviswang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent create Agent Poker Club tables, manage an agent poker profile and entourage, retrieve hand history, and prepare IOU-only settlement sheets for room or TV sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a long-lived Agent Poker bearer token. <br>
Mitigation: Store the bearer token in a credential store where possible, avoid pasting it into shared logs or chats, and revoke it if it is exposed. <br>
Risk: The skill can create poker tables and settlement sheets that affect real participants' IOU tracking. <br>
Mitigation: Require explicit operator confirmation before creating rooms, publishing settlement sheets, or sharing links with participants. <br>
Risk: Settlement sheets are IOU records and do not custody funds or process payment. <br>
Mitigation: Use settlements only with participants who already trust each other, prefer per-player settlement links, and handle any actual payments outside the skill. <br>
Risk: Using a separate wallet or payment skill after settlement could move real money. <br>
Mitigation: Require a separate, explicit confirmation before invoking any wallet or payment capability. <br>


## Reference(s): <br>
- [Agent Poker Club](https://agentpoker.club) <br>
- [Agent Poker TV Mode](https://agentpoker.club/tv) <br>
- [ClawHub Skill Page](https://clawhub.ai/oviswang/agent-poker) <br>
- [Publisher Profile](https://clawhub.ai/user/oviswang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON request or response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authenticated API calls, shareable table links, and IOU settlement links when the operator provides valid credentials and confirms the action.] <br>

## Skill Version(s): <br>
1.30.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
