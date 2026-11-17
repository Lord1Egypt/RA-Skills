## Description:

Generates GitHub Actions workflows from plain English for CI setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[branexp](https://clawhub.ai/user/branexp)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to turn plain-English CI, test, build, deploy, or scheduled job requirements into GitHub Actions workflow YAML. The generated workflow can be printed, written to a selected file, or installed into `.github/workflows/`.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflows may include inappropriate permissions, triggers, secret handling, third-party actions, or deployment behavior.

Mitigation: Manually inspect generated workflow YAML before committing or enabling it in a repository.

Risk: Unpinned npx usage can execute whichever package version resolves at runtime.

Mitigation: Prefer a pinned package version or a local locked installation, especially in sensitive repositories.

Risk: Prompt text may expose secrets or confidential infrastructure details to the model provider.

Mitigation: Do not include secrets or confidential infrastructure details in prompts; reference repository secrets only through reviewed workflow configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/branexp/skills/gh-action-gen)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, configuration]

**Output Format:** [GitHub Actions YAML, either printed to stdout or written to a workflow file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires `OPENAI_API_KEY`; `--install` writes `.github/workflows/ai-generated.yml`, and `--output` writes a user-selected file.]

## Skill Version(s):

1.0.1 (source: evidence.release.version; artifact package.json and _meta.json show 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
