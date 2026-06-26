## Description: <br>
Capture errors, corrections, knowledge gaps, better practices, and feature requests in `.learnings/`, then distill proven recurring patterns into `.learnings/PROMOTED.md`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-tian](https://clawhub.ai/user/paul-tian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain a local, reversible learning workflow for corrections, failures, feature requests, and promoted recurring rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can turn corrections, errors, and requests into persistent local memory without enough privacy controls. <br>
Mitigation: Before enabling hooks, decide where `.learnings/` files live, keep them out of shared repos unless reviewed, and instruct the agent not to save credentials, tokens, personal data, customer data, or confidential workspace details. <br>
Risk: The bootstrap hook can keep reminding future agent sessions to capture and promote local learnings. <br>
Mitigation: Install only when a persistent local learning system is intended; disable the hook and remove the skill files when the workflow is no longer desired. <br>


## Reference(s): <br>
- [Format Reference](references/FORMAT.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/paul-tian/claw-self-improvement) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown instructions, starter Markdown files, and hook configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local learning notes under `.learnings/` when the agent follows the workflow.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
