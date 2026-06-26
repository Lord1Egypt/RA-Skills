## Description: <br>
Plan Denmark trips with compact route logic, verified entry rules, island transport choices, and practical local execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan Denmark trips with realistic region selection, entry and Schengen checks, transport tradeoffs, seasonal constraints, budgets, accessibility needs, and day-by-day route execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local trip memory may retain travel dates, budget, traveler mix, mobility notes, and route preferences. <br>
Mitigation: Review or delete ~/denmark/memory.md if those details should not be retained. <br>
Risk: Entry rules, transport schedules, ferry availability, weather warnings, and costs can change after the bundled references were last checked. <br>
Mitigation: Verify time-sensitive decisions against the official sources listed in sources.md before booking or travel. <br>


## Reference(s): <br>
- [Denmark skill homepage](https://clawic.com/skills/denmark) <br>
- [Official source map](sources.md) <br>
- [Entry and documents](entry-and-documents.md) <br>
- [Domestic transport](transport-domestic.md) <br>
- [Safety and emergencies](safety-and-emergencies.md) <br>
- [New to Denmark short-stay visa guidance](https://nyidanmark.dk/en-GB/You-want-to-apply/Short-stay-visa) <br>
- [VisitDenmark planning portal](https://www.visitdenmark.com/) <br>
- [DSB English portal](https://www.dsb.dk/en/) <br>
- [Rejseplanen journey planner](https://www.rejseplanen.dk/webapp/?language=en_EN) <br>
- [DMI dangerous weather warnings](https://www.dmi.dk/varsler/varsler-om-farligt-vejr-i-danmark/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands for local setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and reuse local trip memory at ~/denmark/memory.md when the user wants durable planning context.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
