## Description:

CatFee Dokobot guides agents to use Dokobot with a real Chrome browser to read JavaScript-rendered or authenticated web pages and extract dynamic content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glory904649854](https://clawhub.ai/user/glory904649854)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill when normal page fetches cannot capture dynamic content from SPAs, authenticated sessions, or JavaScript-heavy pages. It provides command guidance for reading, monitoring, and extracting rendered web content through a local Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to automate a real local Chrome session, which can expose logged-in accounts or sensitive browser state.

Mitigation: Use a dedicated Chrome profile with no unrelated logged-in accounts, and install the skill only when browser rendering or authenticated access is intentionally needed.

Risk: The workflow depends on a globally installed Dokobot CLI, browser extension, and local bridge.

Mitigation: Verify and pin the Dokobot CLI and extension sources before installation, and review updates before use.

Risk: Broad webpage-reading triggers could cause routine fetches to use browser automation unnecessarily.

Mitigation: Prefer simpler fetch methods for routine public pages, and reserve this skill for JavaScript-rendered, interactive, or authenticated content.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Chrome, the Dokobot extension, and the Dokobot bridge; results depend on page rendering, timeout settings, and session state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
