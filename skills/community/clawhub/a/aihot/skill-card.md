## Description: <br>
Aihot Skill Lite helps agents fetch current Chinese-language AI news from AI HOT and format results as readable Markdown briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkkkhazix](https://clawhub.ai/user/kkkkhazix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer current AI news questions by fetching AI HOT items or daily summaries and presenting Chinese Markdown briefings with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate eagerly on ambiguous AI or news-related prompts. <br>
Mitigation: Use it when the user is asking for current AI news, AI HOT, daily summaries, model releases, product releases, papers, or related industry updates. <br>
Risk: The skill may respond in Chinese even when the user uses another language. <br>
Mitigation: Preserve the user's language preference unless the user asks for Chinese output or the source material requires Chinese labels. <br>
Risk: Generated news briefings can be misleading if source links or timing context are omitted. <br>
Mitigation: Include source URLs and human-readable times for reported items, and avoid presenting fetched data as broader coverage than the source supports. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kkkkhazix/aihot) <br>
- [AI HOT website](https://aihot.virxact.com) <br>
- [AI HOT OpenAPI specification](https://aihot.virxact.com/openapi.yaml) <br>
- [Full AI HOT skill documentation](https://github.com/KKKKhazix/khazix-skills/tree/main/aihot) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefings with sourced AI news items and occasional curl command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language summaries; current data fetched from public AI HOT endpoints; no API key required.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
