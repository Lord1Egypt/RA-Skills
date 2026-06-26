## Description: <br>
Query Gerrit accounts, changes, groups, and projects, and generate explicit commands for actions such as reviewer updates, approvals, submissions, or deletions through the Gerrit API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[craftslab](https://clawhub.ai/user/craftslab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to prepare Gerrit CLI invocations for querying review data and applying targeted changes to matching Gerrit changes. It is suited to workflows that need explicit query selectors, optional JSON output, and careful handling of state-changing review actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install an unpinned external CLI package. <br>
Mitigation: Install only from a trusted package source and pin or verify the package before use. <br>
Risk: Gerrit credentials are required in configuration and could be over-privileged or accidentally committed. <br>
Mitigation: Use a low-privilege Gerrit account and avoid committing real credentials in configuration files. <br>
Risk: Approve, submit, delete, reviewer, or attention actions can affect every Gerrit change matched by a query. <br>
Mitigation: Run a query-only command first, inspect the matched changes, keep queries narrow, and require explicit confirmation before state-changing or bulk actions. <br>


## Reference(s): <br>
- [Gerrit Action Skill source](artifact/SKILL.md) <br>
- [Worker configuration example](artifact/config.yml) <br>
- [ClawHub skill page](https://clawhub.ai/craftslab/gerritaction) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require a YAML config file and exactly one Gerrit query selector; change actions require a change query.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
