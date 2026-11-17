## Description:

Helps frontend developers assign ownership to UI, form, server, URL, and persistent state, choose appropriate React or Vue stores, and plan safe state migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers use this skill to review state ownership, choose local or shared state patterns in React and Vue, and refactor stores without losing important behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may overlap with more specialized frontend skills.

Mitigation: Review skill routing and use dedicated data-fetching, form, or browser-storage guidance for those details.

Risk: Incorrect persistence or shared server-side store patterns can expose sensitive user state.

Mitigation: Exclude sensitive fields from persistence, define a field whitelist and migration policy, and isolate stores by request during server rendering.

## Reference(s):

- [State patterns reference](references/state-patterns.md)
- [ClawHub skill release](https://clawhub.ai/bovinphang/skills/fec-state-management)
- [Project homepage (package metadata)](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with state ownership lists, code examples, and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes store and API boundaries and migration rationale.]

## Skill Version(s):

2.9.0 (source: ClawHub release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
