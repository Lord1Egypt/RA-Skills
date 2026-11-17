## Description:

Helps developers choose, implement, and review browser storage for preferences, sessions, structured offline data, and cookies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to select browser persistence, implement storage and cookie helpers, and review retention and sensitive-data handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated storage code could expose authentication tokens or sensitive data to JavaScript.

Mitigation: Review authentication and session handling; prefer server-set httpOnly cookies for tokens and avoid sensitive data in JavaScript-readable storage.

Risk: Browser storage quotas and privacy-mode behavior can disrupt persistence.

Mitigation: Review generated error handling, quota protection, cleanup, and cross-browser behavior before deployment.

## Reference(s):

- [Browser storage patterns](references/storage-patterns.md)
- [Browser Storage on ClawHub](https://clawhub.ai/bovinphang/skills/fec-browser-storage)
- [Project repository listed in package metadata](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Storage selection, namespaced keys, expiration or cleanup guidance, and sensitive-data boundaries.]

## Skill Version(s):

2.9.0 (source: server release evidence, README.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
