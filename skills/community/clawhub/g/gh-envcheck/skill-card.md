## Description:

Check if your environment is ready to run a skill by verifying that required environment variables are set and required CLI binaries are on PATH, returning a ready/not-ready verdict with lists of present and missing items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Envcheck as a pre-flight readiness check before running a skill, confirming that named environment variables and CLI binaries are available. It can be paired with ScopeCheck output to verify an environment against detected skill requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local readiness-check API can reveal whether requested environment variables and binaries exist to anyone who can call it.

Mitigation: Keep the service bound to localhost and do not expose it on a network.

Risk: The skill depends on a local FastAPI service and Python package dependencies before checks can run.

Mitigation: Install the declared dependencies and verify the service is started locally before relying on readiness results.

## Reference(s):

- [Envcheck ClawHub skill page](https://clawhub.ai/mirni/skills/gh-envcheck)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON response with boolean readiness verdict and present/missing environment variable and binary lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks only the environment variables and binaries named in the request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
