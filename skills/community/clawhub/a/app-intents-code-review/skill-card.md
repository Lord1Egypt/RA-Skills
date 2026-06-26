## Description: <br>
Reviews App Intents code for intent structure, entities, shortcuts, and parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review Swift App Intents implementations for intent structure, entities, shortcuts, parameters, and evidence-backed finding reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate review-verification-protocol skill for one hard gate, which may be unavailable in some installations. <br>
Mitigation: Treat that hard gate as an open question or verify the equivalent pre-report checklist before reporting findings. <br>
Risk: Code-review guidance can produce incorrect or overconfident findings if the reviewer does not inspect the current source location and surrounding type. <br>
Mitigation: Require each reported finding to include a current [FILE:LINE] location and a read of the full surrounding App Intents type before reporting. <br>


## Reference(s): <br>
- [Intent Structure](references/intent-structure.md) <br>
- [Entities and Queries](references/entities.md) <br>
- [Shortcuts Integration](references/shortcuts.md) <br>
- [Parameters](references/parameters.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown review guidance and finding summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to use [FILE:LINE] ISSUE_TITLE and be grounded in current repository evidence.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
