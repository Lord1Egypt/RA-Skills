## Description:

Guides the creation and review of Next.js App Router projects, including routes, rendering, server and client boundaries, caching, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to structure and review Next.js 14+ App Router applications, select rendering and caching strategies, and keep sensitive logic on the server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect rendering or cache guidance could expose private data or produce stale pages.

Mitigation: Verify route behavior with build output, response headers, traces, or routing tests; review private-data caching before deployment.

Risk: Putting sensitive logic or credentials in client components could expose them to users.

Mitigation: Keep sensitive logic on the server and exclude credentials from public environment variables.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bovinphang/skills/fec-nextjs-project-standard)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations call for build, header, trace, or routing evidence when evaluating rendering and caching behavior.]

## Skill Version(s):

2.9.0 (source: ClawHub release metadata and artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
