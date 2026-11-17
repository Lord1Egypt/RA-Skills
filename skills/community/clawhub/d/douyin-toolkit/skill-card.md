## Description:

Automates publishing videos to Douyin by uploading a video, filling title and description fields, and handling SMS verification when required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-j-j](https://clawhub.ai/user/mr-j-j)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and agents use this skill to automate Douyin Creator Center video publishing from a local authenticated browser session. It is useful for repeat posting workflows that need video upload, metadata entry, session reuse, and optional SMS-code handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates an authenticated Douyin creator session and can publish content from the user's account.

Mitigation: Use it only with accounts and content workflows where automated publishing is authorized, and review each posting workflow before running it on a real account.

Risk: Authenticated browser state and troubleshooting screenshots may remain in the local skill directory.

Mitigation: Keep the skill directory private, avoid shared machines, and protect or delete chrome_profile/ and screenshots/ after use.

Risk: Browser automation depends on local Playwright and Chromium behavior.

Mitigation: Prefer a sandboxed or containerized environment with pinned Playwright versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mr-j-j/skills/douyin-toolkit)
- [Publisher profile](https://clawhub.ai/user/mr-j-j)
- [Douyin Creator Center](https://creator.douyin.com/)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or reuse local browser profile, SMS-code state, and screenshot files during operation.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
