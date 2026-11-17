## Description:

Create, search, and manage Fabric resources via the Fabric HTTP API (notepads/notes, folders, bookmarks, files, tags).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to read or write content in a user's Fabric workspace through the Fabric HTTP API, including creating, searching, and managing notes, folders, bookmarks, files, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make lasting changes to a Fabric workspace, including delete and recover actions exposed by the API.

Mitigation: Require explicit review before delete, recover, space, or bulk operations, and avoid blind retries on create operations.

Risk: Fabric API keys could be sent to an untrusted endpoint if custom FABRIC_BASE, --base, or --with-key are used carelessly.

Mitigation: Use the default Fabric API endpoint unless the endpoint is trusted, and avoid --with-key for absolute URLs.

Risk: Invalid payloads can produce failed requests or misleading troubleshooting loops.

Mitigation: Follow the bundled OpenAPI spec and schema notes, starting with minimal required fields before adding optional fields such as tags or comments.

## Reference(s):

- [Fabric homepage](https://fabric.so)
- [Fabric API OpenAPI spec](fabric-api.yaml)
- [Fabric API skill reference](references/REFERENCE.md)
- [Troubleshooting Fabric API requests](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API Calls]

**Output Format:** [Markdown guidance with JSON payload examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FABRIC_API_KEY and a supported runtime such as Node.js or Python; helper commands print response bodies and error bodies.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
