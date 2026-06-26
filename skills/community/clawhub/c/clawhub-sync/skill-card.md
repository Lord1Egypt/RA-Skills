## Description: <br>
ClawHub Sync helps developers publish locally developed skills to ClawHub in bulk or one at a time, with gitignore-based filtering, allowlist control, incremental sync records, and dry-run checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cat-xierluo](https://clawhub.ai/user/cat-xierluo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to publish local skills to ClawHub, run dry-run readiness checks, manage publish allowlists, and update sync records for incremental releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish local skill files to a public ClawHub release, which could expose secrets, customer data, or unrelated local files if the publish set is wrong. <br>
Mitigation: Confirm the logged-in ClawHub account, run a dry-run, review the allowlist, inspect the generated /tmp/clawhub-publish-* directory, and exclude secrets, customer data, and unrelated context files before publishing. <br>
Risk: A license mismatch can cause an unsuitable skill to be published to ClawHub. <br>
Mitigation: Check the target skill license before publishing and keep restrictive licenses out of the sync allowlist. <br>


## Reference(s): <br>
- [ClawHub Sync release page](https://clawhub.ai/cat-xierluo/clawhub-sync) <br>
- [ClawHub Skill Format](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and YAML configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce sync result summaries, error messages, publish commands, allowlist checks, and sync-record updates.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence; artifact frontmatter and changelog show 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
