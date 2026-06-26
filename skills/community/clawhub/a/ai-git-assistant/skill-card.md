## Description: <br>
AI-powered git commit messages, changelogs, release notes, PR descriptions, and commit review. Analyzes staged changes and git history to generate professional, Conventional Commits-compliant output. Powered by evolink.ai <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate and review Conventional Commits messages, changelogs, release notes, and pull request descriptions from git diffs and history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI commands transmit git diffs, commit messages, or git history to EvoLink for analysis. <br>
Mitigation: Use the skill only in repositories where sending that data to EvoLink is acceptable, and use a dedicated revocable API key. <br>
Risk: Security evidence reports that one changelog path can run unintended local shell commands from crafted git ref names. <br>
Mitigation: Avoid changelog --from with untrusted tag or ref names until the issue is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evolinkai/ai-git-assistant) <br>
- [Project homepage](https://github.com/EvoLinkAI/git-skill-for-openclaw) <br>
- [EvoLink Claude Messages API documentation](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown, with shell command examples and generated git workflow content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AI commands require EVOLINK_API_KEY and may send git diffs, commit messages, or git history to api.evolink.ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, npm/package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
