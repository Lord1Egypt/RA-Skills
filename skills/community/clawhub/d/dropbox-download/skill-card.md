## Description:

Downloads a file from a user's Dropbox account by path and returns the file content as binary data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foundergraph](https://clawhub.ai/user/foundergraph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve user-selected files from Dropbox when a workflow needs the file contents for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can retrieve Dropbox file contents for any path the user provides to the connected account.

Mitigation: Use a Dropbox connection scoped to file-content read access and provide only paths for files intended for retrieval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foundergraph/skills/dropbox-download)
- [Publisher profile](https://clawhub.ai/user/foundergraph)
- [Dropbox file download endpoint](https://api.dropboxapi.com/2/files/download)

## Skill Output:

**Output Type(s):** [binary data]

**Output Format:** [Binary file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Dropbox OAuth2 connection with files.content.read scope; path is required and rev is optional but deprecated.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
