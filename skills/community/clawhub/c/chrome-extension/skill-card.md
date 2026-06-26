## Description: <br>
Comprehensive guide for building Chrome extensions with Manifest V3, including manifest setup, content scripts, service workers, messaging, permissions, storage, UI surfaces, debugging, and Chrome Web Store publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build, extend, debug, and publish Chrome extensions that follow Manifest V3 architecture and Chrome extension API constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated extension guidance can involve powerful browser capabilities such as host permissions, OAuth flows, content-script injection, network relays, and CSP or header changes. <br>
Mitigation: Review generated extension changes for narrow host permissions, clear runtime consent, allowlisted relay destinations, and avoidance of broad CSP or header changes unless necessary. <br>
Risk: Suggested git, npm, or gh commands could affect local code, dependencies, or publishing workflows. <br>
Mitigation: Approve command execution only when the command matches the intended task and its target repository or package is clear. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/samber/cc-skills) <br>
- [Content Scripts Reference](references/content-scripts.md) <br>
- [Debugging and Common Mistakes Reference](references/debugging-mistakes.md) <br>
- [Execution Contexts, Communication Flows, and Limits](references/execution-contexts.md) <br>
- [Manifest V3 Complete Reference](references/manifest-v3.md) <br>
- [Messaging and RPC Reference](references/messaging-rpc.md) <br>
- [Network Requests and CSP Bypass Reference](references/network-csp.md) <br>
- [Permissions Reference](references/permissions.md) <br>
- [Chrome Web Store Publishing Reference](references/publishing.md) <br>
- [Service Worker Reference](references/service-worker.md) <br>
- [Storage Reference](references/storage.md) <br>
- [TypeScript and Build Tooling Reference](references/typescript-build.md) <br>
- [UI Surfaces Reference](references/ui-surfaces.md) <br>
- [Web Accessible Resources Reference](references/web-accessible-resources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code snippets, manifest examples, configuration examples, and command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose git, npm, or gh commands when appropriate for the user's Chrome extension task.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
