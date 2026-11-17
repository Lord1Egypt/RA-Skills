## Description:

Searches local Windows files through the Everything SDK, shows file details, and can send a selected file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andykungbj](https://clawhub.ai/user/andykungbj)

### License/Terms of Use:

MIT-0

## Use Case:

External users on trusted Windows hosts use this skill to search the local Everything index, inspect file metadata, and return a selected file when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search local indexed files and return readable file contents, which may expose sensitive files.

Mitigation: Use only in trusted, least-privileged Windows environments and avoid credentials, private keys, browser profiles, business documents, and other sensitive locations unless allowlist controls are added.

Risk: The skill depends on a local Everything installation and SDK DLL, so results reflect the host index and DLL loaded at runtime.

Mitigation: Install Everything and its SDK from the documented source, keep them running and current, and verify the DLL location before use.

## Reference(s):

- [Everything SDK](https://www.voidtools.com/support/everything/sdk/)
- [ClawHub skill page](https://clawhub.ai/andykungbj/skills/everything-find-files)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [Text responses with optional base64-encoded file payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are limited to the first 10 matches; sent files are limited to 10 MB.]

## Skill Version(s):

1.0.0 (source: skill.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
