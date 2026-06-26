## Description: <br>
A bilingual executive assistant for ADHD and anxiety that captures thoughts, tracks tasks, adapts recommendations to a 1-10 energy level, and provides gentle deadline and rhythm check-ins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sono19](https://clawhub.ai/user/sono19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill as a bilingual ADHD and anxiety support assistant for cognitive offloading, task capture, energy-aware prioritization, deadline preparation, task suspension, and daily check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to maintain Memory_Box and Task_Pool state, which can retain personal tasks, ideas, and errands. <br>
Mitigation: Confirm how the host agent stores and deletes these entries, and avoid saving highly sensitive information unless retention controls are clear. <br>
Risk: Broad trigger phrases such as deadline, review, or remember this may activate the skill unintentionally. <br>
Mitigation: Review generated reminders or task changes before acting on them, especially when the prompt was not meant as a task-management request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sono19/adhd-external-brain) <br>
- [Publisher profile](https://clawhub.ai/user/sono19) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational bilingual text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include short confirmations, task suggestions, micro-steps, reminders, task rollover notes, and empathetic check-in summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
