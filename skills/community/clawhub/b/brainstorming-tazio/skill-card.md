## Description: <br>
Guides agents through collaborative brainstorming before creative work by exploring intent, requirements, design constraints, alternatives, and validation steps before implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tazio7](https://clawhub.ai/user/Tazio7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn early feature or behavior ideas into validated designs and implementation plans through one-question-at-a-time discovery, alternative analysis, and incremental design review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to make durable repository changes, including writing a design document and committing it to git, without an explicit separate approval step. <br>
Mitigation: Before use, instruct the agent to ask before creating files, show the planned path and content or diff, and obtain separate approval before any git commit or worktree setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tazio7/brainstorming-tazio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown and conversational text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to write a design document and propose repository setup steps after user validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
