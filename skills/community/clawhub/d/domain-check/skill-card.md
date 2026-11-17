## Description:

Check domain availability via Vercel and buy/manage domains via Vercel CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers, site owners, and agents use this skill to check Vercel domain availability, review registrar pricing, and prepare Vercel CLI or API commands for domain management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Vercel CLI commands may execute a different CLI version than the reviewer expects.

Mitigation: Prefer a pinned or locally installed Vercel CLI before running domain commands.

Risk: Domain purchase, transfer, move, removal, or project-assignment commands can affect real accounts and may create financial or operational impact.

Mitigation: Use narrowly scoped credentials where possible and require explicit confirmation before any account-changing domain command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brennerspear/skills/domain-check)
- [Vercel Registrar price endpoint](https://api.vercel.com/v1/registrar/domains/example.com/price)
- [Vercel Registrar domains endpoint](https://api.vercel.com/v1/registrar/domains)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include interactive CLI commands that require a PTY and explicit confirmation before account-changing actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
