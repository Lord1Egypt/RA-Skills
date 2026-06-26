## Description: <br>
Creates, updates, and chats with Bazi-based personas, including Bazi charts, dynamic time-flow analysis, and almanac/calendar queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojxiao2021](https://clawhub.ai/user/xiaojxiao2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to create and maintain persona files from birth data, chat facts, and Bazi analysis, then generate conversational responses, calendar guidance, and persona updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persona facts and imported chat records may include sensitive personal information stored on local disk. <br>
Mitigation: Review and redact private or third-party chat logs before import, and store personas only in locations appropriate for that data. <br>
Risk: A broad base_dir or BAZI_PERSONA_HOME setting could place persona data in an unintended filesystem location. <br>
Mitigation: Use a narrow, dedicated persona directory and verify the resolved path before creating, importing, or updating personas. <br>
Risk: Bazi analysis and almanac guidance could be mistaken for professional advice in high-risk decisions. <br>
Mitigation: Treat outputs as reference material only and do not use the skill as a substitute for medical, legal, investment, or other professional judgment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaojxiao2021/bazi-persona) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON-like tool results, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local persona files under the skill personas directory or a configured base_dir.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
