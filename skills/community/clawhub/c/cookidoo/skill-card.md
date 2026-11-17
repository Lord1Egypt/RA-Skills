## Description:

Access Cookidoo (Thermomix) recipes, shopping lists, and meal planning via the unofficial cookidoo-api Python package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thekie](https://clawhub.ai/user/thekie)

### License/Terms of Use:

MIT

## Use Case:

External users and personal automation agents use this skill to access Cookidoo account data, search recipes, view saved recipes and shopping lists, and assist with meal planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Cookidoo account email and plaintext password for an unofficial API client.

Mitigation: Provide credentials only through a protected session environment or a secrets manager; if using the documented env file, restrict permissions and avoid syncing or committing it.

Risk: The skill depends on an unofficial and unpinned Python package, so Cookidoo changes or dependency updates may break behavior.

Mitigation: Review and pin the dependency before deployment, then retest recipe, plan, shopping, search, recipe detail, and account-info commands after package or Cookidoo changes.

Risk: The documented favorites and sync claims are not supported by the reviewed version.

Mitigation: Treat favorites and sync workflows as unavailable unless a package update is reviewed and confirms those capabilities.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thekie/skills/cookidoo)
- [cookidoo-api Python package](https://pypi.org/project/cookidoo-api/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Cookidoo account credentials and an active Cookidoo subscription]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
