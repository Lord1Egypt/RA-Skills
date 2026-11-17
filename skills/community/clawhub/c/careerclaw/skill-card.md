## Description:

Run a job search briefing, find job matches, draft outreach emails, or track job applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orestes-garcia-martinez](https://clawhub.ai/user/orestes-garcia-martinez)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use CareerClaw to turn a resume profile into job-search briefings, ranked matches, outreach drafts, and local application tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update a global npm package before running.

Mitigation: Require explicit user approval before any global npm install and verify the requested package version.

Risk: The skill reads resume/profile data and writes local .careerclaw tracking files.

Mitigation: Use it only in trusted workspaces and keep .careerclaw files out of version control and shared directories.

Risk: The skill contacts RemoteOK and Hacker News, and Pro mode can send license validation to Gumroad and draft context to a configured LLM provider.

Mitigation: Disclose network use before routine runs and review provider data-handling terms before enabling Pro LLM enhancement.

Risk: Generated outreach is based on public job listings and profile extraction and may be incomplete or misleading.

Mitigation: Review each briefing, match explanation, and outreach draft before saving jobs or sending messages.

Risk: Debug license scripts may expose sensitive operational context if run with real keys.

Mitigation: Avoid running debug license scripts with production credentials.

## Reference(s):

- [CareerClaw ClawHub Skill Page](https://clawhub.ai/orestes-garcia-martinez/skills/careerclaw)
- [CareerClaw README](artifact/README.md)
- [CareerClaw Security Policy](artifact/SECURITY.md)
- [CareerClaw Changelog](artifact/CHANGELOG.md)
- [careerclaw-js npm Package](https://www.npmjs.com/package/careerclaw-js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown summaries with inline shell commands, JSON CLI output when requested, and local JSON tracking files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js and npm; reads resume/profile files; can write .careerclaw tracking and run-log files.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter, package.json, CHANGELOG released 2026-03-08, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
