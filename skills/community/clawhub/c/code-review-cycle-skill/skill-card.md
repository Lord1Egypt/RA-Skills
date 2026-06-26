## Description: <br>
Coordinates a coding agent and a read-only reviewer through a coding, review, and optional revision loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raccoon-office](https://clawhub.ai/user/raccoon-office) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to coordinate a two-agent code review workflow where one agent implements changes and another reviews them before the user decides whether to continue, revise, or finish. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The coding agent can make user-directed edits to the current workspace. <br>
Mitigation: Use the skill in a version-controlled workspace and review diffs before accepting changes. <br>
Risk: Repeated automatic review cycles can compound unwanted edits. <br>
Mitigation: Keep --rounds low and pause for user review when changes affect important files. <br>
Risk: Prompts or code shared with agents may include secrets. <br>
Mitigation: Avoid including secrets in task prompts, source snippets, or review context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raccoon-office/code-review-cycle-skill) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured review sections, command examples, and JSON-style agent invocation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include code change summaries, read-only review findings, and follow-up revision instructions.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
