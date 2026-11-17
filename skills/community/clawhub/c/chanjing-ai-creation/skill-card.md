## Description:

Chanjing AI creation Open API client for submitting image and video tasks, polling task status, listing and retrieving tasks, and optionally downloading outputs when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binkes](https://clawhub.ai/user/binkes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to drive Chanjing AI Creation workflows through the Open API: submit image or video generation tasks, poll asynchronous status, inspect task history or details, and download generated media only when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed network calls and downloads have broader control than the manifest safely scopes.

Mitigation: Review before installing, use only in a private trusted environment, and leave CHANJING_OPENAPI_BASE_URL and CHANJING_API_BASE unset unless the endpoint is fully trusted.

Risk: The skill reads and writes sensitive credentials and access tokens in ~/.chanjing/credentials.json or the configured credentials directory.

Mitigation: Protect the credentials file and directory, avoid shared or synced hosts for token storage, and do not commit credentials.json to version control.

Risk: download_result.py can fetch user-supplied URLs and write to custom output paths.

Mitigation: Download only trusted API response URLs, prefer the default outputs/ai-creation directory, and avoid custom output paths until downloader constraints are tightened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binkes/skills/chanjing-ai-creation)
- [Chanjing Open API documentation](https://doc.chanjing.cc)
- [Skill reference](artifact/reference.md)
- [Skill examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text, JSON task data, URLs, and optional downloaded files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits credentialed API requests and only writes generated media locally when download_result.py is explicitly invoked.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
