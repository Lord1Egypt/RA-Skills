## Description: <br>
Operate the disinto autonomous code factory when managing factory agents, filing issues on the forge, reading agent journals, querying CI pipelines, checking the dependency graph, or inspecting factory health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johba37](https://clawhub.ai/user/johba37) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and operate a Disinto autonomous code factory, including agent health, forge issues, CI pipelines, dependency state, and selected agent journals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses repo and CI credentials to query or mutate forge and pipeline state. <br>
Mitigation: Install only in the intended Disinto repository environment, use repo-scoped and CI-scoped tokens, and verify FORGE_API and WOODPECKER_SERVER before running helpers. <br>
Risk: Issue creation can publish unintended content to the forge. <br>
Mitigation: Review issue title, body, and labels before posting, and avoid embedding secrets in issue bodies. <br>
Risk: Date arguments for journal reading may be unsafe if crafted values are accepted. <br>
Mitigation: Avoid crafted --date values until read-journal.sh validates dates; use trusted YYYY-MM-DD dates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johba37/disinto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make authenticated Forgejo/Gitea and Woodpecker API calls when the required environment variables are configured.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
