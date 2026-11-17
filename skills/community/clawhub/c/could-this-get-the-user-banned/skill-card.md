## Description:

Checks planned third-party-service actions for ban, charge, credential-exposure, retry, upload, billed API, and purchase-path risks before an agent proceeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as a pre-action risk check before retrying refused hosts, uploading data, reading credential paths, calling billed APIs, or submitting purchase and billing requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill works best with a local ClawPhylax plugin that records request and tool-outcome history, which may be undesirable for users who do not want local activity retained.

Mitigation: Use degraded mode without enabling the plugin, or enable the plugin only after confirming local ledger retention is acceptable.

Risk: The skill's paid-API and purchase-path checks are fixed and incomplete, so a missing warning is not proof that an action is safe or free.

Mitigation: Treat OK as a pre-action signal rather than permission; apply human review for unfamiliar billing, purchase, upload, or account-risk actions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/aeneassoft/skills/could-this-get-the-user-banned)
- [Project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with an ACTION: OK, ACTION: CAUTION, or ACTION: STOP first line and concise reasons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [STOP outcomes ask the user before proceeding; CAUTION outcomes advise one attempt rather than looping.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
