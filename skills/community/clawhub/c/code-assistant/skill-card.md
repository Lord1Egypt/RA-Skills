## Description: <br>
Specialized programming assistant that analyzes code, finds bugs, suggests optimizations, refactors, and automatically generates documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miguelguerra200022-sudo](https://clawhub.ai/user/miguelguerra200022-sudo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to inspect selected code files or directories for bugs, complexity, security patterns, performance issues, and style concerns. It also helps produce documentation, tests, refactoring suggestions, command examples, and code-review guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the files or directories selected for analysis, which may include private code or secrets if broad paths are provided. <br>
Mitigation: Run it only on intended project paths, avoid unrelated private directories, and exclude files that may contain secrets. <br>
Risk: The skill advertises refactoring, formatting, and self-repair behavior that could change code incorrectly if accepted without review. <br>
Mitigation: Keep automatic fixes disabled unless deliberate, review diffs before accepting edits, and test changed code before relying on it. <br>
Risk: Pattern-based code findings can miss issues or report false positives. <br>
Mitigation: Treat results as review guidance and confirm important security, correctness, or performance findings with human review and project tests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miguelguerra200022-sudo/code-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and console-style text with code snippets and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-selected files or directories and emits findings, suggestions, generated documentation, and recommended next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
