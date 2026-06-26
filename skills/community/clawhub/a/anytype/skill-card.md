## Description: <br>
Interact with Anytype via anytype-cli and its HTTP API for reading, creating, updating, searching, managing spaces, and automating Anytype workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tadas-subonis](https://clawhub.ai/user/tadas-subonis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to configure Anytype access, call local Anytype HTTP APIs, and manage linked knowledge-base objects, pages, spaces, collections, tags, and relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled setup file contains private-looking Anytype space configuration values. <br>
Mitigation: Replace or remove the bundled SETUP.md values before use and configure the skill only with the user's own Anytype space IDs, invite data, tags, and collections. <br>
Risk: The skill can grant an agent broad read, write, and delete access to an Anytype workspace. <br>
Mitigation: Use a dedicated bot account with the least practical workspace access, store ANYTYPE_API_KEY securely, and require explicit user confirmation before destructive operations. <br>
Risk: Updating page content may require deleting and recreating an object, which can break references or lose content if handled carelessly. <br>
Mitigation: Fetch and save existing content before deletion, confirm delete/recreate actions with the user, and update any stored object IDs or related page links after recreation. <br>


## Reference(s): <br>
- [Anytype API Reference](references/api.md) <br>
- [Anytype Developers Documentation](https://developers.anytype.io) <br>
- [Anytype CLI](https://github.com/anyproto/anytype-cli) <br>
- [Anytype OpenAPI 2025-11-08](https://raw.githubusercontent.com/anyproto/anytype-api/main/docs/reference/openapi-2025-11-08.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown instructions with inline shell commands, Python snippets, JSON request examples, and API helper usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ANYTYPE_API_KEY and a local Anytype API service at http://127.0.0.1:31012.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
