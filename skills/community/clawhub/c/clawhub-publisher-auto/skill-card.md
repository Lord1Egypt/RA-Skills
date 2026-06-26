## Description: <br>
Automates ClawHub skill publishing with version management, changelog generation, asset bundling, metadata validation, and acceptLicenseTerms support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bg1avd](https://clawhub.ai/user/bg1avd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to publish ClawHub skills, manage versions and changelogs, bundle assets, validate metadata, and support CI/CD release workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks users to install external npm or PyPI packages before publishing. <br>
Mitigation: Verify the package and repository provenance, pin exact versions, and run validation or dry-run steps before using the package in a release workflow. <br>
Risk: Broad ClawHub publishing credentials may allow public releases, rollbacks, or account and team changes. <br>
Mitigation: Use a revocable least-privilege ClawHub token, avoid logging credentials, and require manual approval for publish, batch publish, rollback, and team-member changes. <br>
Risk: Automated changelog, README, and Gumroad link changes can alter public release content. <br>
Mitigation: Review generated diffs and approve content changes manually before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bg1avd/clawhub-publisher-auto) <br>
- [Midas Skills ClawHub Publisher docs](https://docs.midas-skills.com/clawhub-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell, JavaScript, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include publish, batch publish, rollback, Gumroad link injection, analytics, team workflow, and CI/CD guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
