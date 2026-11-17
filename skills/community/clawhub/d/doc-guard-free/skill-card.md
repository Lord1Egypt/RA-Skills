## Description: <br>
Doc Guard Free helps agents create, read, update, list, search, and delete end-to-end encrypted Markdown documents for personal privacy-sensitive workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage encrypted Markdown notes and agent collaboration context through a configured MCP document service. It is intended for personal privacy-sensitive document workflows rather than general database or SQL tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Encrypted share URLs can expose document access when the full link includes the key fragment. <br>
Mitigation: Treat complete share links as secrets and share them only with intended recipients. <br>
Risk: The security summary says the skill is scoped too broadly and should not be treated as a general SQL or database tool. <br>
Mitigation: Use it only for encrypted Markdown document workflows through a trusted MCP server. <br>
Risk: Delete operations are described as irreversible. <br>
Mitigation: Confirm with the user before deletion and recommend exporting important content before destructive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/doc-guard-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce document IDs, encrypted share links, sync status values, search results, and deletion confirmations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
