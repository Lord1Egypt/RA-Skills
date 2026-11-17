## Description:

Personalized daily astrological insights focused on relationships, work, personal growth, and luck. Positive framing only. Uses your natal chart + astronomy-engine transits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unicoleunicron](https://clawhub.ai/user/unicoleunicron)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a local natal chart and generate positive daily astrology guidance for relationships, work, personal growth, and luck. Developers can also use its JSON output for dashboards or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth date, birth time, and birthplace are stored in a local configuration file under the user's home directory.

Mitigation: Run setup only on a trusted machine or account and keep the local natal-chart file out of published artifacts or unintended backups.

Risk: The documentation references an upcoming.js command that is not present in the artifact.

Mitigation: Use the shipped daily.js and daily-json.js commands until the publisher adds the missing file or updates the documentation.

Risk: The optional dashboard integration uses a shell execution pattern that can be risky if adapted for a server context.

Mitigation: Use fixed command paths, avoid passing user-controlled input to shell execution, keep a timeout, and run with least privilege.

## Reference(s):

- [Astro Life Insights on ClawHub](https://clawhub.ai/unicoleunicron/skills/astro-life-insights)
- [astronomy-engine npm package archive](https://registry.npmjs.org/astronomy-engine/-/astronomy-engine-2.1.19.tgz)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text or JSON from Node.js scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local birth chart configuration; daily-json.js emits date, total transits, life-area insights, actions, and exactness fields.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
