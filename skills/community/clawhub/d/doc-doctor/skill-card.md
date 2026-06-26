## Description: <br>
Say 'lint my docs' to scan your markdown KB for broken links, orphan pages, and missing metadata, then auto-fix them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[singggggyee](https://clawhub.ai/user/singggggyee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and documentation maintainers use this skill to inspect Markdown knowledge bases for broken links, orphan pages, missing frontmatter, thin articles, inconsistent metadata, and filename issues. It can propose or apply fixes after showing changes and rerun checks to report the before-and-after score. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and potentially edit Markdown files in a local workspace. <br>
Mitigation: Run it in a backed-up or git-tracked workspace and review proposed changes before applying them. <br>
Risk: Memory mode scans files under ~/.claude/. <br>
Mitigation: Use memory mode only when the user is comfortable allowing the agent to inspect local Claude memory files. <br>
Risk: The workflow depends on the external kb-lint package. <br>
Mitigation: Install only when the package and publisher are trusted, and verify package behavior before use in sensitive repositories. <br>


## Reference(s): <br>
- [Claude Doc Doctor on ClawHub](https://clawhub.ai/singggggyee/doc-doctor) <br>
- [kb-lint homepage](https://github.com/SingggggYee/kb-lint) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown summaries with inline shell commands and optional file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May consume kb-lint JSON output internally, but presents findings, proposed fixes, and verification results as concise agent-facing Markdown.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release evidence; artifact frontmatter lists 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
