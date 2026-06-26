## Description: <br>
Resolve hostnames to IP addresses using `dig` from bind-utils. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate DNS lookup commands for A, AAAA, ANY, and reverse DNS records. It is useful when an agent needs concise guidance for resolving hostnames or IP addresses with the standard `dig` command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DNS queries can expose sensitive internal hostnames through normal DNS resolution paths. <br>
Mitigation: Avoid querying sensitive internal hostnames unless the user is comfortable with those names being visible to the configured resolver and related DNS infrastructure. <br>
Risk: The skill depends on the local `dig` binary and the system package repository used to install bind-utils. <br>
Mitigation: Install bind-utils only from trusted system repositories and confirm `dig` is available before relying on generated lookup commands. <br>


## Reference(s): <br>
- [Dns Lookup ClawHub page](https://clawhub.ai/Xejrax/dns-lookup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `dig` binary, provided by the bind-utils package in the artifact install guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
