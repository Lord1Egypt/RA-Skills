## Description:

Generate seeded permuted-block randomization lists for small clinical trials, with stratification, reproducible outputs, audit records, and a methods paragraph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Trial researchers and developers can use the skill to create or regenerate a reproducible allocation schedule from specified arms, ratio, block sizes, strata, and a seed. It does not choose a trial design or provide medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release scan is partial, and the install command uses an unpinned GitHub revision that could run repository-controlled code during installation.

Mitigation: Review the upstream source and use a vetted, fixed commit or verified package in an isolated, least-privilege environment.

Risk: A short or guessable seed may be recovered from its hash, and exposure of the full allocation list or audit log may weaken allocation concealment.

Mitigation: Use a long, random seed; keep the full list and audit log confidential; and manage access to the sealed enrolment list as part of the trial's concealment process.

## Reference(s):

- [BlockRandom ClawHub release](https://clawhub.ai/raktikoo/skills/blockrandom)
- [BlockRandom install source referenced by the skill](https://github.com/RakTikoo/blockrandom)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Text]

**Output Format:** [CSV allocation and enrolment lists, per-stratum files, an audit log, and a plain-text methods paragraph]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seeded and reproducible from the same seed and parameters; a truncated final block is identified in the audit log and methods paragraph.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
