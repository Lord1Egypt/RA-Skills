## Description: <br>
Clawtrix Skill Advisor audits an agent's installed skills for dead weight, updates, and mission-aligned skill gaps, then recommends owner-approved changes using ClawHub and optional peer signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicope](https://clawhub.ai/user/nicope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators and developers use this skill to review installed skills, identify unused or misaligned capabilities, check for updates, and receive recommendations for skills that better match the agent's mission. It is intended to provide guidance and exact commands for human approval, not to install or remove skills automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the installed skill list and SOUL.md, then may use mission-derived search terms with ClawHub, HN Algolia, and optional ClawBrain. <br>
Mitigation: Use it only when that local context and those search terms are acceptable to expose to the referenced services; avoid heartbeat use if reviews should happen only on explicit request. <br>
Risk: Recommended install or remove commands could be unnecessary, unwanted, or mismatched to the agent's actual mission. <br>
Mitigation: Review the briefing, rationale, and exact command manually before running anything; the skill itself does not install or remove skills. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nicope/clawtrix-skill-advisor) <br>
- [Publisher Profile](https://clawhub.ai/user/nicope) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefing with inline shell commands and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations require owner approval before any install or removal command is run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
