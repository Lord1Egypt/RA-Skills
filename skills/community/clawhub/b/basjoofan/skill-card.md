## Description:

Easy run test helps agents prepare basjoofan CLI commands and .fan examples for API, HTTP, performance, load, and stress testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lamb](https://clawhub.ai/user/lamb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to run basjoofan API test scripts, choose test options such as concurrency and duration, and produce GET or POST request examples for .fan files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer fetches a mutable native executable without integrity checks.

Mitigation: Install only from a trusted basjoofan release channel and verify the downloaded binary through an independent release or checksum process before use.

Risk: Load or stress tests can affect external services or systems without authorization.

Mitigation: Run tests only against systems you own or are explicitly authorized to test, and keep concurrency, duration, and run counts conservative.

Risk: Test scripts may send secrets, personal data, internal endpoints, or sensitive files in requests.

Mitigation: Use sanitized test data and avoid production credentials, personal data, internal URLs, and sensitive file uploads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lamb/skills/basjoofan)
- [ClawHub publisher profile](https://clawhub.ai/user/lamb)
- [basjoofan latest release endpoint](https://api.github.com/repos/basjoofan/core/releases/latest)
- [basjoofan binary release URL template](https://github.com/basjoofan/core/releases/download/v${VERSION}/basjoofan-${VERSION}-${ARCH}-${OS})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and basjoofan script examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include basjoofan test names, concurrency, duration, run count, script path, recording, and statistics options.]

## Skill Version(s):

0.0.1 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
