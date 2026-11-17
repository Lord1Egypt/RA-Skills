## Description:

Guides agents through building, debugging, and publishing Chrome extensions with Manifest V3, including manifests, service workers, content scripts, messaging, permissions, storage, networking, UI surfaces, TypeScript builds, and Chrome Web Store submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when creating or modifying Chrome extensions that rely on Manifest V3 APIs. It helps an agent choose the right extension context, draft code and configuration, debug lifecycle and messaging issues, and prepare for Chrome Web Store publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable extension examples may expose powerful browser-extension privileges with weak scoping if used without hardening.

Mitigation: Review generated extension code for exact origin checks, narrow host permissions, operation-specific handlers, payload schemas, and user-visible consent before deployment.

Risk: Relay, bridge, OAuth, storage, and CSP-related patterns can expose tokens or privileged fetch behavior to page code if implemented too broadly.

Mitigation: Apply PKCE and state for OAuth, avoid exposing raw tokens, validate all bridge messages, and restrict privileged fetch handlers to explicit trusted endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samber/skills/chrome-extension)
- [Source Homepage](https://github.com/samber/cc-skills)
- [Manifest V3 Complete Reference](references/manifest-v3.md)
- [Service Worker Reference](references/service-worker.md)
- [Content Scripts Reference](references/content-scripts.md)
- [Messaging and RPC Reference](references/messaging-rpc.md)
- [Execution Contexts, Communication Flows, and Limits](references/execution-contexts.md)
- [Permissions Reference](references/permissions.md)
- [Network Requests and CSP Bypass Reference](references/network-csp.md)
- [Storage Reference](references/storage.md)
- [UI Surfaces Reference](references/ui-surfaces.md)
- [TypeScript and Build Tooling Reference](references/typescript-build.md)
- [Chrome Web Store Publishing Reference](references/publishing.md)
- [Web Accessible Resources Reference](references/web-accessible-resources.md)
- [Debugging and Common Mistakes Reference](references/debugging-mistakes.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code, JSON manifest examples, TypeScript snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory development artifacts for review before use in production extensions.]

## Skill Version(s):

1.1.0 (source: artifact/SKILL.md frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
