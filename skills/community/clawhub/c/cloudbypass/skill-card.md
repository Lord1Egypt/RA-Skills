## Description: <br>
Use Cloudbypass API to fetch pages protected by Cloudflare, Turnstile, or JavaScript challenges when normal requests fail with challenge or 403 responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuanchuan007](https://clawhub.ai/user/chuanchuan007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to route authorized protected-page retrieval through Cloudbypass when ordinary HTTP requests encounter Cloudflare, Turnstile, JavaScript challenges, or 403 responses. It supports simple requests, challenge-heavy requests that require a proxy, and streamed downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Protected-site requests are routed through Cloudbypass and may bypass site protections. <br>
Mitigation: Use the skill only for targets you are authorized to access and review legal and ethical permissions before use. <br>
Risk: Broad request forwarding and write-method helpers can send sensitive headers, cookies, request bodies, or state-changing requests through a third-party provider. <br>
Mitigation: Avoid forwarding account cookies or authorization headers unless explicitly approved, restrict destinations, and require manual review before POST, PUT, DELETE, downloads, or autonomous browsing. <br>
Risk: Cloudbypass API usage requires credentials and may incur billing. <br>
Mitigation: Use a dedicated Cloudbypass key and proxy, monitor usage and billing, and rotate or revoke keys when needed. <br>


## Reference(s): <br>
- [Cloudbypass skill page](https://clawhub.ai/chuanchuan007/cloudbypass) <br>
- [Cloudbypass API quick reference](https://docs.cloudbypass.com/api-quick-reference.md) <br>
- [Cloudbypass website](https://www.cloudbypass.com/) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, text] <br>
**Output Format:** [JavaScript API responses with status, headers, data or stream, cookies, and thrown CloudbypassError objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLOUDBYPASS_APIKEY; V2 and streamed download modes require CLOUDBYPASS_PROXY.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
