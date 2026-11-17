## Description:

Launches a local Chrome browser with a remote debugging port, with modes for reusing an existing profile session or starting an independent profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1232023](https://clawhub.ai/user/luis1232023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and testing agents use this skill to start Chrome on a local debugging endpoint, reuse browser cookies when appropriate, and connect automation such as Playwright over CDP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose an authenticated Chrome session through a local remote debugging port.

Mitigation: Use independent profile mode when authentication reuse is not required, avoid personal or production browser profiles, and close the debug browser after use.

Risk: Reuse mode can close existing Chrome windows or processes using the debugging port and may leave a copied browser profile on disk.

Mitigation: Save browser work before reuse mode, prefer independent mode for routine testing, and remove copied debug or reuse profiles when they are no longer needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start Chrome on localhost port 9222; the health check is a separate optional command.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
