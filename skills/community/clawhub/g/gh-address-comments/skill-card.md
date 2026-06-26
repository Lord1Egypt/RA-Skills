## Description: <br>
Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tbeard602](https://clawhub.ai/user/tbeard602) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to collect comments on the current branch's open GitHub pull request, decide which comments to address, and apply selected fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose private or sensitive pull request comments to the local agent context when used with GitHub credentials that can access those repositories. <br>
Mitigation: Run it only on pull requests whose comments are acceptable to share with the local agent context, and prefer the minimum gh scopes needed for the target repository. <br>
Risk: The skill asks for broad GitHub CLI scopes and elevated command access beyond what is clearly necessary. <br>
Mitigation: Review the requested scopes before use, avoid granting workflow scope unless explicitly needed, and inspect the helper before running it in sensitive repositories. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional code changes and JSON produced by the comment-fetch helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run authenticated gh commands to read pull request comments and review threads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
