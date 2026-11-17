## Description:

Recognizes CAPTCHA images using ddddocr library. Invoke when user needs to recognize/decode CAPTCHA images or mentions captcha verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to recognize text from CAPTCHA or OCR images supplied as local files, HTTP/HTTPS image URLs, bytes, or PIL Image objects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make HTTP/HTTPS requests to user-provided image URLs from the agent environment.

Mitigation: Use only trusted image URLs and avoid localhost, private-network, cloud metadata, or untrusted redirected URLs.

Risk: The skill installs unpinned Python packages.

Mitigation: Run it in a restricted environment with pinned dependency versions when deploying or testing.

## Reference(s):

- [ddddocr GitHub repository](https://github.com/sml2h3/ddddocr)
- [ClawHub skill page](https://clawhub.ai/moxin1044/skills/captcha-recognition)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Plain text recognition result, Markdown guidance, Python API examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May raise errors for unsupported inputs, missing dependencies, network failures, or non-image URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
