## Description:

A vehicle information query skill that lets an agent check vehicle location and status, including locks, doors, windows, air conditioning, power, and gear state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkisme](https://clawhub.ai/user/lkisme)

### License/Terms of Use:

MIT-0

## Use Case:

Vehicle owners and their agents use this skill to query where a vehicle is and inspect current status such as locks, doors, windows, air conditioning, power, and gear state after the user supplies vehicle API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive vehicle and access tokens are cached locally.

Mitigation: Use only on trusted machines, avoid elevated privileges, restrict access to the cache file, and delete the cache when credentials should no longer persist.

Risk: Local history can contain precise vehicle location information.

Mitigation: Treat the history file as sensitive, avoid shared or managed machines unless storage controls are hardened, and clear the history when it is no longer needed.

Risk: Vehicle status and location queries depend on a third-party vehicle API.

Mitigation: Review the script and API trust boundary before providing credentials, and use the skill only if the publisher and vehicle API are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkisme/skills/carkey)
- [Vehicle API endpoint](https://openapi.nokeeu.com)
- [Git for Windows](https://git-scm.com/download/win)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Terminal text with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; reads cached vehicle/access tokens and writes local query history.]

## Skill Version(s):

1.1.1 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
