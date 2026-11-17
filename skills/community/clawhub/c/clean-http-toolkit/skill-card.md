## Description:

Local Python 3 HTTP toolkit that helps agents fetch URLs, send REST requests, download files with checksum verification, extract page content, and run local static or JSON echo test servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to make HTTP requests, inspect or extract web content, download artifacts, and run local mock endpoints without adding third-party Python dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can make arbitrary HTTP requests and may send bearer tokens, basic auth credentials, cookies, or sensitive headers to untrusted or redirected hosts.

Mitigation: Use trusted URLs, avoid credentials with untrusted URLs, and disable redirects or manually verify redirect targets before sending credentials.

Risk: The toolkit can read from and write to user-specified local paths for request bodies, outputs, and downloads.

Mitigation: Use workspace-scoped paths and review source and destination paths before running file operations.

Risk: The local server can expose files or request data if it is bound beyond localhost.

Mitigation: Keep the default 127.0.0.1 binding unless exposure is intentional and the served content has been reviewed.

## Reference(s):

- [Clean HTTP Toolkit on ClawHub](https://clawhub.ai/gopendrasharma89-tech/clean-http-toolkit)
- [Clean HTTP Toolkit skill page](https://clawhub.ai/gopendrasharma89-tech/skills/clean-http-toolkit)
- [Publisher profile](https://clawhub.ai/user/gopendrasharma89-tech)
- [clean-text-toolkit](https://clawhub.ai/gopendrasharma89-tech/clean-text-toolkit)
- [clean-json-toolkit](https://clawhub.ai/gopendrasharma89-tech/clean-json-toolkit)
- [clean-log-toolkit](https://clawhub.ai/gopendrasharma89-tech/clean-log-toolkit)
- [clean-csv-toolkit](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime scripts can emit plain text, JSON, HTTP response bodies, or downloaded files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports bounded retries, optional checksum verification for downloads, optional status-only output, and local static or JSON echo server modes.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
