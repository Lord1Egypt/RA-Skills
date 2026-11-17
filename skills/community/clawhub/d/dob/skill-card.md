## Description:

Provides a Deep Memory workflow for maintaining structured long-term knowledge files and keyword indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qshfu](https://clawhub.ai/user/qshfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to query, add, and maintain durable workspace knowledge in a structured Deep Memory index. It is intended for reusable notes about tools, libraries, documentation, and learned procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files may store sensitive, private, or stale information.

Mitigation: Require confirmation before every write, avoid saving secrets or private material, and periodically review or delete stale memory files.

Risk: Broad user or internet-derived content may be retained without enough context or trust checks.

Mitigation: Summarize instead of saving full source content and treat internet-derived entries as untrusted references until reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qshfu/skills/dob)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and structured file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent workspace memory files and indexes when used by an agent.]

## Skill Version(s):

0.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
