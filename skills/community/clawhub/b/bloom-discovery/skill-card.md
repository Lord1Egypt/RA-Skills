## Description:

Bloom Discovery analyzes a user's MentalOS and local OpenClaw context to match use cases, verify installed skills, support SBT proof claiming, and report opt-in usage metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloomprotocol](https://clawhub.ai/user/bloomprotocol)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to generate a local personality and intent profile, discover matching skill-based use cases, verify their installed skill setup, and claim portable proof of verified configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive local conversation and USER.md profile data for local analysis.

Mitigation: Review the requested local file and conversation permissions before installation, and run it only in environments where this data access is acceptable.

Risk: The security summary reports that derived identity data uploaded to Bloom may be broader than the privacy text suggests.

Mitigation: Inspect the outbound identity payload before upload and prefer a release that clearly previews or documents all fields sent to Bloom.

Risk: The security guidance notes an invocation path that can download and run remote code.

Mitigation: Avoid first-run wrapper execution in shared environments unless remote code is pinned to an immutable commit and reviewed before execution.

Risk: Installation and wrapper setup expose users to npm and GitHub supply-chain risk, including vulnerable dependencies noted by the security guidance.

Mitigation: Install from a reviewed lockfile, audit dependencies, and update to a version that fixes known vulnerable packages.

## Reference(s):

- [Bloom Discovery on ClawHub](https://clawhub.ai/bloomprotocol/skills/bloom-discovery)
- [Bloom Protocol Publisher Profile](https://clawhub.ai/user/bloomprotocol)
- [Bloom Protocol Homepage](https://bloomprotocol.ai)
- [Architecture Diagram](artifact/docs/ARCHITECTURE-DIAGRAM.md)
- [Skills Pipeline Agent Instructions](artifact/docs/agent-skills-pipeline-instructions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Configuration, Guidance]

**Output Format:** [Markdown and structured text with local analysis results, matched use cases, verification status, recommendations, and dashboard links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include personality type, MentalOS spectrum scores, generated tagline and description, interest categories, use case match results, SBT claim guidance, and opt-in usage metrics status.]

## Skill Version(s):

4.0.2 (source: server release evidence; artifact frontmatter and package metadata show 4.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
