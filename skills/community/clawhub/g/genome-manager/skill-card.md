## Description:

Genome Manager helps agents create, store, retrieve, mutate, validate, and track Genome Evolution Protocol genomes for reusable agent behavior patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylechen26](https://clawhub.ai/user/kylechen26)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to manage Genome Evolution Protocol genomes that capture successful task patterns, mutation history, validation status, and lineage for reuse or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Genome JSON files may persist prompt content or other sensitive data as shareable plaintext.

Mitigation: Do not store secrets or confidential prompts in genomes, and review genome content before saving or sharing.

Risk: Untrusted genome names may escape the intended storage folder until path validation is added.

Mitigation: Use trusted, simple genome names and inspect file paths before creating, retrieving, mutating, or validating genomes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, JSON, Configuration]

**Output Format:** [Markdown guidance with shell command, Python, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent genome JSON files to local genome storage when the CLI is executed.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
