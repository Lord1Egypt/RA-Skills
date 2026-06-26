## Description: <br>
Brainstorm Beagle helps users turn fuzzy project ideas into implementation-free WHAT/WHY specs through structured dialogue, prior-art checks, self-review, and saved Markdown spec documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product builders, and agents use this skill before planning or building to clarify fuzzy ideas, avoid duplicate brownfield work, and produce a standalone project spec. It is intended for concept shaping and requirements capture, not implementation planning or code generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow reads repository context and may save spec files into the working tree. <br>
Mitigation: Use it only in repositories where that context access is acceptable, and require the agent to show the exact output path and diff before accepting saved files. <br>
Risk: The artifact instructs the agent to make a git commit after writing the spec, while the scan notes no clear separate approval or file-scope control. <br>
Mitigation: Do not allow any git commit unless explicitly requested, and confirm the commit includes only the intended spec file. <br>


## Reference(s): <br>
- [Brainstorm Beagle on ClawHub](https://clawhub.ai/anderskev/skills/brainstorm-beagle) <br>
- [Publisher profile: anderskev](https://clawhub.ai/user/anderskev) <br>
- [Spec Self-Review Checklist](references/spec-reviewer.md) <br>
- [Spec Document Template](references/spec-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown spec document with conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves the approved spec to .beagle/concepts/<slug>/spec.md after explicit user approval and finalized path.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
