## Description: <br>
Helps an agent look up Xtreme Gaming's next Dota 2 match by fetching public schedule information from the Liquipedia MediaWiki API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earthking11](https://clawhub.ai/user/earthking11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Dota 2 fans and agents use this skill to answer questions about Xtreme Gaming's next scheduled match, including tournament, opponent, match time, round, and elimination context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents match times in Beijing time, which can be misleading for users expecting UTC or their local timezone. <br>
Mitigation: Ask the agent to include UTC or the user's local timezone when time precision matters. <br>
Risk: The skill uses a deliberately teasing fan tone around Ame and XG results, which may be inappropriate in neutral or professional contexts. <br>
Mitigation: Ask the agent to use a neutral tone when sharing the match summary outside the intended fan context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earthking11/dota2-xg-next-game) <br>
- [Liquipedia Dota 2 MediaWiki API endpoint for Xtreme Gaming](https://liquipedia.net/dota2/api.php?action=parse&page=Xtreme_Gaming&format=json&prop=text|sections) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style natural language with emphasized match details and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq to fetch public schedule data, converts match times to Beijing time, and summarizes the next known XG match.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
