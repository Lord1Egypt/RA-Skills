## Description: <br>
De-agent your code by checking files and commit messages for AI-style patterns before committing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itscodejac](https://clawhub.ai/user/itscodejac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use dgent before commits to inspect source files and commit messages for AI-style naming, phrasing, emoji, trailers, and simple catch-rethrow patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: --fix mode and enabled git hooks can change files or commit messages. <br>
Mitigation: Run JSON or check modes first, then review git diffs before committing. <br>


## Reference(s): <br>
- [dgent GitHub repository](https://github.com/ItsCodejac/dgent) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-producing CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can report clean status, fixes, flags, and cleaned output; fix mode can write changes in place.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
