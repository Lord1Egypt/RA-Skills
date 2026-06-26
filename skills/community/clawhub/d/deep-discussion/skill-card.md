## Description: <br>
Multi-agent deep discussion with Orchestrator coordination and agenda checklist tracking for complex problems that benefit from diverse expert perspectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LuciusCao](https://clawhub.ai/user/LuciusCao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, researchers, and operators use this skill to run structured multi-agent expert discussions, track agenda progress, preserve full discussion logs, and produce reports and action plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subagents may receive the discussion context and the skill saves full expert responses in local discussion logs. <br>
Mitigation: Do not include passwords, tokens, private customer data, or confidential material unless it is intended to appear in those logs; delete generated files after use when retention matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LuciusCao/deep-discussion) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Agenda tracking](artifact/references/agenda-tracking.md) <br>
- [Discussion protocol](artifact/references/discussion-protocol.md) <br>
- [Orchestrator logic](artifact/references/orchestrator-logic.md) <br>
- [Output template](artifact/references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown files and conversational text with occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates agenda.md, discussion-log.md, report.md, and action-plan.md under workspace/deep-discussion/{topic-slug}; discussion-log.md preserves full expert responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; source skill frontmatter reports 3.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
