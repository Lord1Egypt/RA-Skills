## Description:

Deploys apps to CapRover and helps set up GitHub Actions CI/CD workflows, captain-definition files, and GitHub secrets for new or existing projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guim4dev](https://clawhub.ai/user/guim4dev)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to trigger CapRover deployments, check GitHub Actions deployment status, and scaffold GitHub Actions deployment workflows for application projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger live deployments through GitHub Actions, CapRover webhooks, or the CapRover CLI.

Mitigation: Require manual confirmation before running deploy commands and scope credentials to the specific app or environment being deployed.

Risk: Configuration may contain high-value CapRover credentials, GitHub tokens, app tokens, and webhook URLs.

Mitigation: Prefer per-app CapRover tokens over the master password, keep local config out of version control, and redact webhook URLs and tokens from logs.

Risk: Bundled GitHub Actions templates reference external actions and package tooling that may change over time.

Mitigation: Pin GitHub Actions and package versions before production use and review generated workflows before committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guim4dev/skills/caprover-ci-deploys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, YAML workflow snippets, JSON configuration, and deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce or modify GitHub Actions workflow files and captain-definition configuration when used to scaffold a project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
