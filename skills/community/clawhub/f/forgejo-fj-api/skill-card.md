## Description: <br>
Forgejo via fj and REST API for repos, issues, PRs, wiki, CI, and reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerasse](https://clawhub.ai/user/nerasse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to manage self-hosted Forgejo repositories, issues, pull requests, wiki pages, CI status, and structured code reviews through fj, REST API calls, and local git review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Forgejo token and can change repository data. <br>
Mitigation: Use a least-privilege token scoped to the requested task and avoid storing it in shared shell profiles or logs. <br>
Risk: Commands can target the wrong Forgejo instance or repository if FORGEJO_URL or repository context is incorrect. <br>
Mitigation: Verify FORGEJO_URL and the target owner/repo before running CLI or REST operations. <br>
Risk: Delete, merge, migration, wiki delete, label delete, and milestone delete operations can be destructive. <br>
Mitigation: Require explicit user confirmation before those operations run. <br>


## Reference(s): <br>
- [Forgejo Skill Homepage](https://github.com/nerasse/forgejo-skill) <br>
- [Forgejo API Cheatsheet](references/api-cheatsheet.md) <br>
- [Forgejo CI and Actions](references/ci-actions.md) <br>
- [Forgejo Pull Request Review Workflow](references/code-review.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, REST API examples, and review text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Forgejo CLI commands, curl requests, jq filters, and pull request review comments for user confirmation.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
