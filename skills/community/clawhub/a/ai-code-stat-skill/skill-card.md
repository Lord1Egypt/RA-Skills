## Description: <br>
Tracks AI and human code contributions, generates standardized commit messages, and analyzes AI code share across current and historical Git changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wgongrui](https://clawhub.ai/user/wgongrui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to label AI-generated versus human-written code, calculate non-empty line counts and AI percentage, create standardized Git commit messages, and review historical contribution trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The commit flow can stage and commit an entire repository with too little file-level review. <br>
Mitigation: Before using the commit flow, run git status, inspect the diff, remove secrets or unrelated files, and prefer staging explicit files instead of git add . <br>
Risk: AI contribution statistics can be misleading if @ai/@human markers are missing, inconsistent, or applied to the wrong changed files. <br>
Mitigation: Review markers and changed files before relying on reported percentages, and use the analysis-only scripts separately when no commit is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wgongrui/ai-code-stat-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with generated commit-message content and optional Python/Git command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Statistics are based on non-empty changed-file lines and @ai/@human markers; commit workflows may execute Git commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; skill frontmatter meta lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
