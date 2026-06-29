## Description: <br>
Use browser-backed fetch when a page needs real Chromium rendering, JavaScript execution, browser user agent behavior, proxy-aware navigation, or blocked-page diagnostics instead of plain HTTP fetch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-green](https://clawhub.ai/user/x-green) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch web pages through Chromium when plain HTTP fetch is insufficient because the page requires rendering, JavaScript execution, browser user-agent behavior, proxy-aware navigation, or blocked-page diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambient HTTP_PROXY or HTTPS_PROXY settings may route requests through an unintended proxy. <br>
Mitigation: Set FETCH_USE_ENV_PROXY=0 when inherited proxy settings should not be used, or pass --proxy-server explicitly for a deliberate proxy. <br>
Risk: Default stealth behavior may be unsuitable for ordinary fetching or policy-sensitive use cases. <br>
Mitigation: Use --no-stealth when standard browser automation behavior is preferred. <br>
Risk: Saved metadata can include sensitive URL or proxy details. <br>
Mitigation: Avoid saving or sharing metadata files when URLs or proxy strings may contain sensitive information. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML, JSON, files, shell commands] <br>
**Output Format:** [Plain text, HTML, or JSON metadata with content; optional content and metadata files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports status-aware exit codes, Chromium navigation timeouts, selector-based extraction, optional stealth behavior, and explicit or ambient proxy configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
