## Description: <br>
Guides agents through configuring the cn.clawhub-mirror.com ClawHub mirror, installing the Multi Search Engine skill, choosing search strategies, and archiving the setup in local knowledge files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roger0808](https://clawhub.ai/user/roger0808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when ClawHub installs are slow or rate-limited, to produce mirror-based install commands, choose search engines for research tasks, and record the configuration in workspace knowledge files. <br>

### Deployment Geography for Use: <br>
Global, with mirror guidance intended for users who can access cn.clawhub-mirror.com. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead agents to make persistent knowledge-base, cross-workspace sync, Git commit, and Git push changes beyond a simple mirror or search-skill install. <br>
Mitigation: Require the agent to list exact files, workspaces, branch, remote, and diff before archival changes; approve Git commits, Git pushes, cross-workspace sync, or clawhub update --all only when explicitly intended. <br>
Risk: The skill directs agents to use the cn.clawhub-mirror.com registry for ClawHub package resolution. <br>
Mitigation: Install only when you intentionally want agents to use that registry and trust the mirror for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roger0808/clawhub-mirror-config-and-search-skill) <br>
- [ClawHub mirror endpoint](https://cn.clawhub-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent file, workspace sync, and Git actions that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
