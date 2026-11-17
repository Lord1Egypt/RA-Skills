## Description:

Use browser-backed fetch when a page needs real Chromium rendering, JavaScript execution, browser user agent behavior, proxy-aware navigation, or blocked-page diagnostics instead of plain HTTP fetch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-green](https://clawhub.ai/user/x-green)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch web pages through a real Chromium browser when plain HTTP fetch is insufficient because the page requires JavaScript execution, browser-like navigation, proxy-aware access, or blocked-page diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch an unsandboxed browser that reaches arbitrary network locations, including sensitive local or private network endpoints if the agent environment allows it.

Mitigation: Run it only in a tightly isolated environment with no access to localhost services, private networks, cloud metadata, or sensitive mounted files.

Risk: Ambient HTTP_PROXY or HTTPS_PROXY variables are used by default and proxy details may appear in metadata output.

Mitigation: Set FETCH_USE_ENV_PROXY=0 unless ambient proxy use is intended, avoid authenticated proxy variables when output is not controlled, and review metadata before sharing it.

Risk: The --output and --metadata options write files at caller-provided paths.

Mitigation: Review output paths before execution and restrict writable locations in the agent runtime.

## Reference(s):

- [ClawHub Browser Fetch skill page](https://clawhub.ai/x-green/skills/fvg-browser-fetch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, HTML, or JSON metadata plus fetched content; optional files for content and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports timeout, user agent, proxy, Chromium path, wait condition, selector, output path, metadata path, metadata inclusion, stealth toggle, and failure handling options.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
