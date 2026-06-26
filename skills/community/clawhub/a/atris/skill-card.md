## Description: <br>
Codebase intelligence — generates structured navigation maps with file:line references so agents stop re-scanning the same files every session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keshav55](https://clawhub.ai/user/keshav55) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use Atris to create and maintain a repository navigation map for code exploration, onboarding, and answering file-location questions with exact file:line references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and maintains atris/MAP.md in the user's repository, which may capture sensitive file paths or implementation details in private codebases. <br>
Mitigation: Review atris/MAP.md before committing or sharing it, and require confirmation before creating or regenerating the map when stricter repository-change control is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keshav55/atris) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown navigation map with file:line references and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates atris/MAP.md in the target repository.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
