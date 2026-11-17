## Description:

Shell-agnostic .env file loader that helps agents generate POSIX-compatible loader scripts and validation guidance for .env files across bash, zsh, dash, and ash.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaichao87](https://clawhub.ai/user/wuhaichao87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and deployment engineers use this skill to generate or review portable .env loading workflows for applications that need consistent environment variable behavior across common POSIX shells.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: .env files often contain secrets, and loader scripts can expose or mishandle those values if reviewed carelessly.

Mitigation: Review generated load-env.sh content before deployment and avoid printing or committing secret values.

Risk: The inspected artifact references helper scripts and a reference file that were not present, so users may receive guidance for files unavailable in this release.

Mitigation: Confirm required helper scripts are available in the installed package or use the documented POSIX patterns as guidance rather than assuming bundled script execution will work.

## Reference(s):

- [Env Loader release page](https://clawhub.ai/wuhaichao87/skills/env-loader)
- [wuhaichao87 publisher profile](https://clawhub.ai/user/wuhaichao87)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with POSIX shell snippets and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or review load-env.sh style shell script content and .env validation guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
