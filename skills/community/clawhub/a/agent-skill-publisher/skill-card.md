## Description: <br>
End-to-end workflow for publishing agent skills to GitHub, ClawdHub, and skills.sh, covering repo creation, topic tagging, ClawdHub publishing, skills.sh index requests, and installation verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryant24hao](https://clawhub.ai/user/bryant24hao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this agent skill to publish an agent skill across GitHub, ClawdHub, and skills.sh in one guided workflow. It helps validate files, create and tag a repository, publish to ClawdHub, submit a skills.sh indexing request, verify installation paths, and summarize release links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can make public account changes, including repository creation, pushes, ClawdHub publishing, and skills.sh issue creation. <br>
Mitigation: Require a dry run and explicit user confirmation before any public account, repository, registry, or issue-tracker action. <br>
Risk: The artifact describes patching files under ~/.npm/_npx to work around a ClawdHub CLI payload issue. <br>
Mitigation: Do not allow automatic patching of local CLI cache files; use a fixed or updated ClawdHub CLI instead. <br>
Risk: Publishing workflows can expose secrets, user-specific paths, or unintended files if run without review. <br>
Mitigation: Review staged files and scan for secrets, personal paths, large binaries, and stale placeholder links before committing or publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bryant24hao/agent-skill-publisher) <br>
- [Publisher Profile](https://clawhub.ai/user/bryant24hao) <br>
- [Skill Homepage](https://github.com/bryant24hao/skill-publisher) <br>
- [GitHub CLI](https://cli.github.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and release checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose public account, repository, registry, and issue-tracker actions that require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
