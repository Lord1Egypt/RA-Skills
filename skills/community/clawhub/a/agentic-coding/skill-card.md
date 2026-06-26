## Description: <br>
Ship production code with AI agents through acceptance contracts, micro diffs, red green loops, and deterministic handoff checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure AI-assisted coding work around explicit acceptance contracts, focused diffs, verification evidence, and reviewer-ready handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opt-in local memory may record contracts, evidence notes, and handoff summaries under ~/agentic-coding/. <br>
Mitigation: Review what may be written before enabling memory and keep durable notes limited to execution preferences and validation evidence. <br>
Risk: Broad or vague coding contracts can lead to unnecessary changes outside the intended scope. <br>
Mitigation: Keep each task contract narrow, define non-goals, and require validation evidence before handoff. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ivangdavila/agentic-coding) <br>
- [Skill homepage](https://clawic.com/skills/agentic-coding) <br>
- [PACT loop protocol](protocol.md) <br>
- [Contract prompt templates](prompt-contracts.md) <br>
- [Merge handoff checklist](handoff.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured checklists, prompt templates, and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local memory templates and handoff notes under ~/agentic-coding/ when the user explicitly opts in.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
