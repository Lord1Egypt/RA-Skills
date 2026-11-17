## Description:

Use @ainative/react-sdk to add AI chat, credit tracking, managed sessions, and React hook guidance to React apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when adding AINative React SDK chat, credit balance, provider setup, and loading or error handling patterns to React applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-delivered React configuration can expose a real AINative API key and chat or account data.

Mitigation: Keep real AINative API keys out of React source and browser-delivered environment variables; use backend mediation or short-lived scoped client tokens, and minimize data sent to the service.

Risk: Installing an unpinned SDK package can pull a version different from the reviewed release.

Mitigation: Pin and verify the @ainative/react-sdk package version before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urbantech/skills/ainative-react-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include React provider setup, hook usage, environment variable examples, and loading or error state handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
