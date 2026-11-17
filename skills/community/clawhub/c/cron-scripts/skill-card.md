## Description:

Run bash scripts on a schedule without LLM involvement. Zero model cost, hot-reload, pure shell. A workaround until openclaw/openclaw#80793 lands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdxbsv](https://clawhub.ai/user/gdxbsv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to schedule local bash jobs in OpenClaw for deterministic tasks such as health checks, file cleanup, backups, and fixed notifications without invoking an LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent gateway startup code that auto-runs local shell scripts with the gateway user's privileges and inherited environment.

Mitigation: Install only when persistent scheduled shell execution is intended, restrict write access to the hook and script directories, review each script before adding it, and remove the hook when scheduled execution is no longer needed.

Risk: Scheduled scripts may receive secrets or sensitive configuration through the gateway environment.

Mitigation: Avoid placing secrets in the gateway environment and keep script-specific credentials scoped outside the scheduler whenever possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gdxbsv/skills/cron-scripts)
- [OpenClaw issue #80793: Support script target type in OpenClaw cron](https://github.com/openclaw/openclaw/issues/80793)
- [OpenClaw issue #18160: Direct Exec Mode for Cron Jobs](https://github.com/openclaw/openclaw/issues/18160)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation of an OpenClaw gateway startup hook and frontmatter-based shell scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
