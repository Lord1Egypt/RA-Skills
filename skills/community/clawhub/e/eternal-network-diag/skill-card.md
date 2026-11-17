## Description:

Perform network diagnostics including ping, DNS resolution, TCP port checks, and traceroute for specified hosts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternal0404](https://clawhub.ai/user/eternal0404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run local connectivity, DNS, TCP port, and traceroute diagnostics against hosts they are authorized to test.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network diagnostics send probes to specified hosts and may be inappropriate against systems the user does not own or have permission to test.

Mitigation: Run diagnostics only against hosts you own, administer, or have explicit permission to test.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and terminal-style diagnostic text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnostics may execute DNS lookups, ping, TCP connect checks, and traceroute against user-specified hosts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
