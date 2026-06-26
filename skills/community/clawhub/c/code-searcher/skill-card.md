## Description: <br>
Search codebases for patterns, symbols, and TODOs. Use when navigating large codebases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to search codebases for text patterns, symbol references, TODO-style markers, recent files, and basic file or line statistics while navigating large repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the artifacts were not identifiable for deeper review, so harmful behavior was not concretely evidenced but review depth was limited. <br>
Mitigation: Install only if the skill page or package files clearly match the purpose you expect. Because the actual artifacts were not available in this review context, read the skill instructions and setup requirements before granting credentials, filesystem access, or long-running automation. <br>
Risk: The artifact executes shell-based grep and find operations over user-selected directories, which can expose local source text in terminal output. <br>
Mitigation: Run the commands only in intended repositories and review the target directory before granting broad filesystem access. <br>
Risk: The bundled script creates a local data directory under ~/.local/share/code-searcher/. <br>
Mitigation: Confirm local storage expectations and remove that directory if the skill is uninstalled or no longer needed. <br>


## Reference(s): <br>
- [Code Searcher ClawHub page](https://clawhub.ai/bytesagain3/code-searcher) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [The Silver Searcher upstream project](https://github.com/ggreer/the_silver_searcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output is line-limited by the bundled shell scripts and may create a local data directory under ~/.local/share/code-searcher/.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
