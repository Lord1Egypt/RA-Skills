## Description:

Helps agents build, compile, configure, and deploy Rust WebAssembly HTTP apps to Gcore FastEdge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geri4](https://clawhub.ai/user/geri4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold, build, upload, and release Rust WebAssembly HTTP applications on Gcore FastEdge. It also guides app configuration for environment variables, encrypted secrets, and edge storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled update helper can unintentionally wipe existing app configuration on a live Gcore deployment.

Mitigation: Avoid using the helper for existing production apps until it preserves full app configuration or shows a complete diff; when updating, re-send environment variables, secrets, stores, name, binary, and status.

Risk: Build, upload, and deploy commands can publish artifacts to live FastEdge endpoints when a valid Gcore API token is present.

Mitigation: Use a least-privileged Gcore API token, run builds in a minimal environment, and confirm the artifact, app name, binary id, and app id before upload or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geri4/skills/gcore-fastedge)
- [Gcore FastEdge docs](https://gcore.com/docs/fastedge)
- [Gcore FastEdge API reference for LLMs](https://gcore.com/docs/fastedge/llms.txt)
- [Gcore edge storage API](https://gcore.com/docs/api-reference/fastedge/edge-storage/create-a-new-edge-store)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local build commands and Gcore FastEdge API calls when the user chooses deployment steps.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
