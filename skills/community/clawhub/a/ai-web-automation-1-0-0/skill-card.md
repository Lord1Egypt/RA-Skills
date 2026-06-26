## Description: <br>
Provides a user-directed web scraping helper that fetches a URL and writes a markdown report with basic page metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kesepain](https://clawhub.ai/user/kesepain) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents can use this skill for authorized, user-directed webpage scraping and lightweight monitoring reports. Broader automation claims such as form filling, scheduling, testing, retries, proxies, and notifications should be verified before relying on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release documentation claims broader automation features than the bundled implementation demonstrates. <br>
Mitigation: Treat it as a basic scraping helper unless reviewed files add form filling, scheduling, testing, retry, proxy, or notification behavior. <br>
Risk: Web scraping can target websites or data the user is not authorized to access. <br>
Mitigation: Use only on websites you are authorized to access, and add rate limits, scope controls, and data-handling controls for scraping workflows. <br>
Risk: The script makes outbound HTTP requests to user-provided URLs and writes page-derived reports. <br>
Mitigation: Avoid private or internal targets unless intentional, and review generated reports before sharing or storing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kesepain/ai-web-automation-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown report files with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped scraping reports for user-provided URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
