## Description: <br>
Chrome Control Proxy guides agents in using a local HTTP proxy to start, inspect, and automate Chrome with Playwright snapshots, scripts, and browser lifecycle endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengxiangqi](https://clawhub.ai/user/zhengxiangqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to a local Chrome Control Proxy service for browser lifecycle checks, page snapshots, scripted Playwright actions, and multi-step browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad local Chrome automation through the proxy, including actions against existing browser sessions and real accounts. <br>
Mitigation: Install only when local browser control is intended, use a dedicated browser profile or test account where possible, and require explicit approval before login, form submission, cookie clearing, or other account-impacting actions. <br>
Risk: The Playwright run endpoint can execute browser automation scripts and may be unsafe if exposed to untrusted containers or networks. <br>
Mitigation: Keep the service local and firewalled, avoid exposing port 3333 beyond trusted environments, and do not open the run endpoint to untrusted callers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhengxiangqi/chrome-control-proxy) <br>
- [Chrome Control Proxy homepage](https://github.com/zhengxiangqi/chrome-control-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with HTTP endpoint guidance and inline shell and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers local Chrome proxy endpoints, Playwright snapshot options, scripts, and sequencing guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
