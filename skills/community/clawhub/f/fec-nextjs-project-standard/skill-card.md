## Description: <br>
Use when creating or reviewing Next.js 14+ App Router projects, file routes, layouts, server/client component boundaries, SSR/SSG/ISR, streaming, metadata, middleware, server actions, or Next-specific data fetching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to create or review Next.js 14+ App Router projects, choose rendering and caching strategies, and keep server and client component responsibilities clear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Next.js changes could expose sensitive authentication logic, server actions, internal APIs, or environment variables to client-side code. <br>
Mitigation: Review auth, middleware, server actions, and NEXT_PUBLIC environment usage before accepting generated changes. <br>
Risk: Incorrect rendering, caching, or client/server boundary choices can cause stale data, unnecessary hydration, or larger client bundles. <br>
Mitigation: Verify the selected SSR, SSG, ISR, or CSR mode, fetch cache policy, and placement of browser-only libraries in client leaf components. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/fec-nextjs-project-standard) <br>
- [Frontend Craft Repository](https://github.com/bovinphang/frontend-craft) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on Next.js App Router structure, rendering modes, data-fetching boundaries, metadata, middleware, and server/client component placement.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata, package.json, metadata.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
