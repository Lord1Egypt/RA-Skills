## Description: <br>
Automate committing Markdown-only changes in a git repo with safe staging, ideal for note snapshots without affecting code or binaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gleb-urvanov](https://clawhub.ai/user/gleb-urvanov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and note-taking agents use Braingit to create git snapshots of Markdown-only changes in a repository without staging code, binaries, or unrelated files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create git commits for matching Markdown files, which may include unintended notes or sensitive text if those files are not excluded. <br>
Mitigation: Review the target repository, keep .gitignore exclusions current, use BRAINGIT_DRY_RUN=1 before automation, and avoid storing secrets in Markdown. <br>


## Reference(s): <br>
- [Braingit protocol](references/protocol.md) <br>
- [Braingit article](https://github.com/gleb-urvanov/braingit/blob/master/braingit-article.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces git commits when invoked outside dry-run mode; exits successfully when no matching Markdown changes are present.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
