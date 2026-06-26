## Description: <br>
Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hu-xiao-tian](https://clawhub.ai/user/hu-xiao-tian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to guide coding, reviewing, and refactoring work toward explicit assumptions, simpler implementations, targeted edits, and verifiable success criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may bias an agent toward cautious, small, explicitly verified coding changes and extra clarification, which can slow trivial tasks. <br>
Mitigation: Use it for coding, review, and refactoring tasks where explicit assumptions and verification are useful; avoid invoking it when speed on a trivial task is the priority. <br>
Risk: The guidance is advisory and may still produce unsuitable implementation choices if the surrounding task context is incomplete. <br>
Mitigation: Pair the skill with normal code review and task-specific validation such as tests, linting, or manual inspection. <br>


## Reference(s): <br>
- [Karpathy coding pitfalls post](https://x.com/karpathy/status/2015883857489522876) <br>
- [ClawHub skill page](https://clawhub.ai/hu-xiao-tian/clean-code-styleguide) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable commands, API calls, file writes, data access, or persistence are added by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
