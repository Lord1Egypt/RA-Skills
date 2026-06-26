## Description: <br>
Configure HTTP-to-HTTPS redirects on Alibaba Cloud ALB, including inspecting the current listener and rule setup, creating missing HTTP or HTTPS listeners, and adding a redirect rule that forces HTTP requests to HTTPS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect Alibaba Cloud ALB listeners, rules, certificates, and server groups, then configure HTTP-to-HTTPS redirects for an existing load balancer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ALB rule, listener, and server-group changes can reroute or block live service traffic. <br>
Mitigation: Use least-privilege RAM permissions, verify every resource ID, inspect existing listener and rule state, and run dry-run modes before write operations. <br>
Risk: Temporary or self-signed certificates can weaken production HTTPS handling if left attached. <br>
Mitigation: Use self-signed certificates only for testing, capture the current certificate before replacement, restore it after testing, and delete temporary uploaded certificates. <br>
Risk: Alibaba Cloud credentials are required for account-level changes. <br>
Mitigation: Use a preconfigured CLI profile or environment credentials, check status with credential-safe commands, and avoid printing or collecting access keys in the agent session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-network-alb-http-to-https) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Permissions](references/ram-policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash command sequences and references to bundled shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script outputs may include plain text, JSON when --json is used, dry-run results, or files written through --output.] <br>

## Skill Version(s): <br>
0.0.1-beta.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
