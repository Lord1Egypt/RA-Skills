## Description: <br>
AI-powered diary generation for agents - creates rich, reflective journal entries (400-600 words) with Quote Hall of Fame, Curiosity Backlog, Decision Archaeology, Relationship Evolution, mood analytics, weekly digests, "On This Day" resurfacing, and cron auto-generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use Agent Chronicle to turn local session activity into reflective diary entries, weekly digests, quote collections, curiosity logs, decision notes, relationship notes, and mood or topic summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive session-derived memories, quotes, decisions, and relationship notes. <br>
Mitigation: Use it only when persistent diary material is desired, keep the privacy level private, and avoid storing secrets or regulated data in session logs. <br>
Risk: Auto-generation and memory integration can create or append diary material with limited retention controls. <br>
Mitigation: Disable auto-generation and memory integration unless they are explicitly needed, and review generated entries before sharing them. <br>
Risk: HTML export can load remote CSS. <br>
Mitigation: Prefer PDF or local-styled exports when remote asset loading is not acceptable. <br>


## Reference(s): <br>
- [Agent Chronicle on ClawHub](https://clawhub.ai/robbyczgw-cla/agent-chronicle) <br>
- [Publisher profile](https://clawhub.ai/user/robbyczgw-cla) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [config.example.json](config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown entries and reports, JSON task payloads, configuration files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local diary, quote, curiosity, decision, relationship, digest, analysis, and export files according to configuration.] <br>

## Skill Version(s): <br>
0.7.2 (source: server release metadata, SKILL.md frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
