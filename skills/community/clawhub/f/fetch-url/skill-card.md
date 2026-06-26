## Description: <br>
Fetch raw HTTP response bodies from one or more URLs with optional custom headers and timeout, supporting JSON, XML, RSS, CSV, plain text, and files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roaycl](https://clawhub.ai/user/roaycl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch raw non-HTML HTTP responses from APIs, feeds, data files, and downloads for downstream analysis or processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-controlled headers can be sent to URLs selected at runtime, which can expose Authorization, Cookie, API key, or internal-service headers to untrusted destinations. <br>
Mitigation: Only provide sensitive headers for destination URLs you trust, and avoid sending credentials or internal-service headers when fetching arbitrary URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roaycl/fetch-url) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Raw response body text for a single URL; JSON array of result objects for multiple URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports custom per-URL headers and request timeout; Node.js 18+ is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
