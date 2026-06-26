## Description: <br>
Ultra-compressed commit message generator that cuts noise from commit messages while preserving intent and reasoning in Conventional Commits format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanford](https://clawhub.ai/user/seanford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft terse, ready-to-paste commit messages from staged changes or commit-message requests while preserving the reason for the change when it matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording could make the skill read staged changes sooner than intended. <br>
Mitigation: Review staged changes before invoking the skill and avoid using it in repositories with secrets or private work that should not enter agent context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanford/caveman-commit) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown code block containing a commit message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces only a ready-to-paste commit message and does not run git commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
