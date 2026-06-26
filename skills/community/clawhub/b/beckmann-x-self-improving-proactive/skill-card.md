## Description: <br>
Combination skill that adds the Beckmann Knowledge Graph as a deep-reasoning escalation layer on top of the Self-Improving + Proactive Agent while keeping everyday tasks on the default self-improving workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthiasbeckmann987-spec](https://clawhub.ai/user/matthiasbeckmann987-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to coordinate a self-improving memory workflow with optional Beckmann Knowledge Graph escalation for paradoxes, open scientific or philosophical questions, strategic dead ends, AI safety questions, and other high-complexity reasoning tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill orchestrates two required base skills, so users may misunderstand its behavior if those skills are not reviewed or installed. <br>
Mitigation: Review the required base skills before installation and confirm both are available before relying on the combined workflow. <br>
Risk: Beckmann escalation can produce slower and more speculative deep-reasoning output than standard answers. <br>
Mitigation: Escalate only after user confirmation and reserve the workflow for the documented complex question categories. <br>
Risk: The workflow may store Beckmann insights and related notes in self-improving memory files under ~/self-improving/. <br>
Mitigation: Periodically inspect those memory files and avoid saving secrets or sensitive information there. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matthiasbeckmann987-spec/beckmann-x-self-improving-proactive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with optional JavaScript and markdown examples for graph loading, graph-grounded answers, self-reflection entries, and tiered memory logging.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the independent ivangdavila/self-improving and matthiasbeckmann987-spec/beckmann-knowledge-graph skills to be installed for the full workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
