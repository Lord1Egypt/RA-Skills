## Description: <br>
Manage conversation context with saving, loading, and pruning tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Ctxkeeper to record timestamped operational notes, inspect recent activity, search saved entries, and summarize local log history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided entries are saved persistently on the local device and may appear in recent or search results. <br>
Mitigation: Avoid entering secrets or sensitive conversation text, and remove ~/.local/share/ctxkeeper/ when saved entries should be cleared. <br>
Risk: The package evidence does not define an install mechanism for the ctxkeeper command. <br>
Mitigation: Verify that the installed ctxkeeper command resolves to the reviewed script before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output and local log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent local data under ~/.local/share/ctxkeeper/.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
