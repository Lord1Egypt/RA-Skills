## Description:

Sort chemicals by compatibility for safe laboratory storage. Prevents dangerous reactions by segregating incompatible chemicals (acids, bases, oxidizers, flammables) and provides storage recommendations compliant with safety regulations.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[theresayao0614-sudo](https://clawhub.ai/user/theresayao0614-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Lab staff, EHS reviewers, and developers can use this skill for demonstration or non-operational triage of chemical inventory grouping, compatibility checks, and storage-plan drafts. Do not use its outputs for real lab storage, inspection, relocation, or training decisions without independent SDS, SOP, and qualified EHS review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides safety-critical chemical storage advice, and the security evidence reports under-scoped warnings and unsafe classification behavior.

Mitigation: Use only for rough demonstration or non-operational triage; verify every output against current SDS data, institutional SOPs, and qualified EHS review before any lab action.

Risk: Chemical inventory files or lists may contain local lab data that the skill can read or transform during local workflows.

Mitigation: Run the skill only in an approved local environment and provide inventory data only when local data handling requirements are satisfied.

Risk: Unknown, ambiguous, mixed, or multi-hazard chemicals may be classified too broadly or default to general storage.

Mitigation: Treat uncertain classifications as unresolved, consult SDS or EHS staff, and document any manual overrides before relying on a storage plan.

## Reference(s):

- [OSHA Chemical Storage Guidelines](https://www.osha.gov/chemical-storage)
- [SDS Search (MSDSOnline)](https://www.msdsonline.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and plain text with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce storage groups, compatibility warnings, storage-plan drafts, and local command examples.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
