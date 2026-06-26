## Description: <br>
Configures and manages Cloudflare DNS, caching, security rules, rate limiting, and Workers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to plan, review, and execute Cloudflare DNS, SSL/TLS, cache, security rule, rate limiting, and Workers changes for web applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A powerful Cloudflare token can allow live DNS, SSL, caching, and security setting changes. <br>
Mitigation: Use a token scoped to the intended zone and permissions, and review the proposed plan before any mutating API call. <br>
Risk: DNS deletes, SSL changes, WAF or rate-limit rules, and purge-all cache actions can cause downtime, traffic blocking, or operational disruption. <br>
Mitigation: Survey current state first, execute one API call at a time, verify each response, and confirm DNS propagation or configuration state after changes. <br>


## Reference(s): <br>
- [Cloudflare Guard on ClawHub](https://clawhub.ai/guifav/cloudflare-guard) <br>
- [Cloudflare API v4](https://api.cloudflare.com/client/v4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Cloudflare API credentials and zone context from the user environment.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
