## Description: <br>
Create and publish styled blog posts to GitHub Pages by generating HTML posts, updating the blog index, and committing and pushing changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t3mr0i](https://clawhub.ai/user/t3mr0i) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to draft and publish GitHub Pages blog posts, update the blog index, and push the resulting site changes to a configured repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to commit and publicly publish GitHub Pages content without a clear confirmation step. <br>
Mitigation: Confirm the remote, branch, GitHub identity, generated content, and diff before pushing; stage only the intended files. <br>
Risk: The referenced clank-blog-post command may resolve to an unreviewed local binary. <br>
Mitigation: Verify the installed command path and trustworthiness before execution, or run it only in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/t3mr0i/clank-blog-post) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git and may produce public repository changes; review generated content, target remote, branch, identity, and diff before pushing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
