## Description:

Installs a curated set of OpenClaw skills for new users, server setup, and workspace recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianduoduo1422608857](https://clawhub.ai/user/qianduoduo1422608857)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install a bundle of recommended skills through the skillhub CLI. It is intended for onboarding, quick server setup, and restoring a working skill environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can force-install multiple mutable third-party skills with limited provenance checks.

Mitigation: Review each skill before installation and prefer pinned, publisher-verified installs where available.

Risk: The documentation scope is inconsistent: it says the one-click path installs five skills, while the script installs eight.

Mitigation: Review the script's skill list before execution and confirm the full set is acceptable.

## Reference(s):

- [Tavily API Key](https://tavily.com)
- [Notion Integrations](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs an interactive shell installer that reports successful and failed installs.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
