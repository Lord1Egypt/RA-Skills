## Description:

Supports uploading and processing images, files, and CSVs, then uses the provided content to generate tailored text replies for chat-record and workflow scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[github2cao](https://clawhub.ai/user/github2cao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to generate text replies from uploaded images, documents, CSVs, and chat or workflow inputs. Review file authorization, retention, and deletion handling before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence flags the package as suspicious because it exposes sensitive endpoints, identifiers, and a bearer token example.

Mitigation: Install only after the publisher removes and rotates exposed tokens and replaces internal IPs and object paths with placeholders.

Risk: Uploaded file and image handling may be unclear for authorization, retention, and deletion.

Mitigation: Require HTTPS uploads and document exactly how uploaded files and images are authorized, retained, and deleted before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/github2cao/skills/111jjjjk)
- [Publisher profile](https://clawhub.ai/user/github2cao)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference uploaded image, file, CSV, chat-history, or workflow input content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
