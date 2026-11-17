## Description:

Monitor websites for changes, new content, and price alerts. Perfect for tracking competitors, job postings, or product prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3mr0i](https://clawhub.ai/user/t3mr0i)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business operators use this skill to set up simple website monitoring for competitor pricing, job postings, product availability, and content updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The monitor can fetch arbitrary URLs, including sensitive or internal endpoints if a user supplies them.

Mitigation: Use only trusted public URLs; validate URL schemes and destinations, and block localhost or private network ranges unless explicitly allowed.

Risk: Unchecked monitor names can write monitor files outside the intended directory.

Mitigation: Sanitize monitor names, reject path separators and traversal sequences, and constrain writes to the monitor state directory.

Risk: Documented features may overstate what the included script supports.

Mitigation: Review supported commands before use and align documentation with implemented add, list, and check behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/t3mr0i/skills/clank-website-monitor)
- [Publisher profile](https://clawhub.ai/user/t3mr0i)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write monitor state and history files under the user's home directory when commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
