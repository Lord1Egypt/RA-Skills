## Description: <br>
Cloudflare Global helps agents administer Cloudflare DNS, zone settings, cache, firewall and page rules, analytics, and tunnel operations through the legacy Global API Key flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill when an agent needs to inspect or change Cloudflare DNS records, zone settings, SSL mode, cache state, page rules, firewall rules, analytics, or Cloudflare tunnels using Global API Key authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Global API Key can authorize broad Cloudflare account changes. <br>
Mitigation: Prefer a scoped Cloudflare API token where possible, keep credentials in local environment variables, and grant access only for the zones needed. <br>
Risk: DNS deletes, DNS imports, SSL changes, full cache purges, and tunnel deletion can affect production traffic. <br>
Mitigation: Test on non-production zones first and manually review these commands before allowing an agent to execute them. <br>
Risk: The skill has no built-in confirmation step before destructive operations. <br>
Mitigation: Require a human approval gate for delete, import, setting change, cache purge, and tunnel deletion operations. <br>


## Reference(s): <br>
- [Cloudflare API endpoint used by this skill](https://api.cloudflare.com/client/v4) <br>
- [ClawHub skill page](https://clawhub.ai/ugvfpdcuwfnh/cloudflare-global) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Cloudflare credentials in environment variables and command-line tools such as curl and jq for script execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
